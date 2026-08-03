param(
    [ValidateSet("status", "click", "post-click", "capture", "inspect")]
    [string]$Action = "status",
    [Parameter(Mandatory = $true)]
    [long]$WindowHandle,
    [long]$TargetHandle = 0,
    [int]$X = 0,
    [int]$Y = 0,
    [string]$OutputPath,
    [int]$WaitMilliseconds = 0,
    [int]$MaxNodes = 200
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;

public static class MoneyHomeRuntimeNative
{
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT
    {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool IsIconic(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern IntPtr SendMessage(IntPtr hWnd, uint message, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern bool PostMessage(IntPtr hWnd, uint message, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern bool PrintWindow(IntPtr hWnd, IntPtr deviceContext, uint flags);
}
'@

function Get-MoneyHomeRoot {
    param([long]$Handle)

    $root = [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]$Handle)
    if ($null -eq $root) {
        throw "无法读取 MoneyHome UI Automation 根节点：$Handle"
    }
    $root
}

function Get-NamedNodes {
    param(
        [System.Windows.Automation.AutomationElement]$Root,
        [int]$Limit
    )

    $nodes = $Root.FindAll(
        [System.Windows.Automation.TreeScope]::Descendants,
        [System.Windows.Automation.Condition]::TrueCondition
    )
    $result = @()
    for ($index = 0; $index -lt $nodes.Count -and $result.Count -lt $Limit; $index++) {
        $node = $nodes.Item($index)
        if ([string]::IsNullOrWhiteSpace($node.Current.Name)) {
            continue
        }
        $result += [pscustomobject]@{
            index = $index
            name = $node.Current.Name
            class_name = $node.Current.ClassName
            control_type = $node.Current.ControlType.ProgrammaticName
            native_handle = $node.Current.NativeWindowHandle
            enabled = $node.Current.IsEnabled
            offscreen = $node.Current.IsOffscreen
            rectangle = $node.Current.BoundingRectangle.ToString()
        }
    }
    $result
}

$root = Get-MoneyHomeRoot -Handle $WindowHandle

switch ($Action) {
    "status" {
        $rect = New-Object MoneyHomeRuntimeNative+RECT
        [void][MoneyHomeRuntimeNative]::GetWindowRect([IntPtr]$WindowHandle, [ref]$rect)
        [pscustomobject]@{
            handle = $WindowHandle
            name = $root.Current.Name
            class_name = $root.Current.ClassName
            enabled = $root.Current.IsEnabled
            visible = [MoneyHomeRuntimeNative]::IsWindowVisible([IntPtr]$WindowHandle)
            minimized = [MoneyHomeRuntimeNative]::IsIconic([IntPtr]$WindowHandle)
            left = $rect.Left
            top = $rect.Top
            width = $rect.Right - $rect.Left
            height = $rect.Bottom - $rect.Top
        } | ConvertTo-Json -Depth 4
    }
    "click" {
        if ($TargetHandle -eq 0) {
            $TargetHandle = $WindowHandle
        }
        $position = [IntPtr](($Y -shl 16) -bor ($X -band 0xffff))
        [void][MoneyHomeRuntimeNative]::SendMessage(
            [IntPtr]$TargetHandle,
            0x0200,
            [IntPtr]::Zero,
            $position
        )
        [void][MoneyHomeRuntimeNative]::SendMessage(
            [IntPtr]$TargetHandle,
            0x0201,
            [IntPtr]1,
            $position
        )
        [void][MoneyHomeRuntimeNative]::SendMessage(
            [IntPtr]$TargetHandle,
            0x0202,
            [IntPtr]::Zero,
            $position
        )
        if ($WaitMilliseconds -gt 0) {
            Start-Sleep -Milliseconds $WaitMilliseconds
        }
        Get-NamedNodes -Root $root -Limit $MaxNodes | ConvertTo-Json -Depth 4
    }
    "post-click" {
        if ($TargetHandle -eq 0) {
            $TargetHandle = $WindowHandle
        }
        $position = [IntPtr](($Y -shl 16) -bor ($X -band 0xffff))
        # Delphi 模态命令会阻塞同步 SendMessage；异步投递后由下一次观察确认结果。
        [void][MoneyHomeRuntimeNative]::PostMessage(
            [IntPtr]$TargetHandle,
            0x0200,
            [IntPtr]::Zero,
            $position
        )
        [void][MoneyHomeRuntimeNative]::PostMessage(
            [IntPtr]$TargetHandle,
            0x0201,
            [IntPtr]1,
            $position
        )
        [void][MoneyHomeRuntimeNative]::PostMessage(
            [IntPtr]$TargetHandle,
            0x0202,
            [IntPtr]::Zero,
            $position
        )
        if ($WaitMilliseconds -gt 0) {
            Start-Sleep -Milliseconds $WaitMilliseconds
        }
        Get-NamedNodes -Root $root -Limit $MaxNodes | ConvertTo-Json -Depth 4
    }
    "capture" {
        if ([string]::IsNullOrWhiteSpace($OutputPath)) {
            throw "capture 操作必须提供 OutputPath"
        }
        $rect = New-Object MoneyHomeRuntimeNative+RECT
        [void][MoneyHomeRuntimeNative]::GetWindowRect([IntPtr]$WindowHandle, [ref]$rect)
        $width = $rect.Right - $rect.Left
        $height = $rect.Bottom - $rect.Top
        if ($width -le 0 -or $height -le 0) {
            throw "MoneyHome 窗口尺寸无效：${width}x${height}"
        }
        $parent = Split-Path -Parent $OutputPath
        if (-not [string]::IsNullOrWhiteSpace($parent)) {
            New-Item -ItemType Directory -Force -Path $parent | Out-Null
        }
        $bitmap = New-Object System.Drawing.Bitmap($width, $height)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        try {
            $deviceContext = $graphics.GetHdc()
            try {
                $captured = [MoneyHomeRuntimeNative]::PrintWindow(
                    [IntPtr]$WindowHandle,
                    $deviceContext,
                    2
                )
            }
            finally {
                $graphics.ReleaseHdc($deviceContext)
            }
            if (-not $captured) {
                throw "PrintWindow 截图失败：$WindowHandle"
            }
            $bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
        }
        finally {
            $graphics.Dispose()
            $bitmap.Dispose()
        }
        Get-Item -LiteralPath $OutputPath |
            Select-Object FullName, Length, LastWriteTime |
            ConvertTo-Json -Depth 4
    }
    "inspect" {
        Get-NamedNodes -Root $root -Limit $MaxNodes | ConvertTo-Json -Depth 4
    }
}
