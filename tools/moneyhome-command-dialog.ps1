param(
    [Parameter(Mandatory = $true)]
    [int]$CommandId,
    [Parameter(Mandatory = $true)]
    [string]$OutputPath,
    [Parameter(Mandatory = $true)]
    [long]$MainWindowHandle,
    [Parameter(Mandatory = $true)]
    [long]$BookkeepingToolbarHandle,
    [Parameter(Mandatory = $true)]
    [int]$MoneyHomeProcessId,
    [Parameter(Mandatory = $true)]
    [string]$ExpectedDialogClass,
    [string]$ExpectedDialogTitle = "",
    [int]$BookkeepingButtonX = 550,
    [int]$BookkeepingButtonY = 25,
    [int]$TimeoutMilliseconds = 8000,
    [int]$MaxNodes = 300,
    [switch]$KeepOpen
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
if (-not ("MoneyHomeCommandNative" -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
using System.Text;

public static class MoneyHomeCommandNative
{
    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    [StructLayout(LayoutKind.Sequential)]
    public struct RECT
    {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct GUITHREADINFO
    {
        public int cbSize;
        public int flags;
        public IntPtr hwndActive;
        public IntPtr hwndFocus;
        public IntPtr hwndCapture;
        public IntPtr hwndMenuOwner;
        public IntPtr hwndMoveSize;
        public IntPtr hwndCaret;
        public RECT rcCaret;
    }

    [DllImport("user32.dll")]
    public static extern bool EnumWindows(EnumWindowsProc callback, IntPtr lParam);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern int GetClassName(IntPtr hWnd, StringBuilder className, int maxCount);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder title, int maxCount);

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);

    [DllImport("user32.dll")]
    public static extern bool GetGUIThreadInfo(uint threadId, ref GUITHREADINFO info);

    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);

    [DllImport("user32.dll")]
    public static extern bool IsWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool IsWindowEnabled(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern IntPtr GetWindow(IntPtr hWnd, uint command);

    [DllImport("user32.dll", EntryPoint = "GetWindowLongPtrW")]
    public static extern IntPtr GetWindowLongPtr(IntPtr hWnd, int index);

    [DllImport("user32.dll")]
    public static extern bool PostMessage(IntPtr hWnd, uint message, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern IntPtr SendMessage(IntPtr hWnd, uint message, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern bool PrintWindow(IntPtr hWnd, IntPtr deviceContext, uint flags);
}
'@
}

function Assert-MoneyHomeWindow {
    param(
        [long]$Handle,
        [int]$ExpectedProcessId,
        [string]$ExpectedClass,
        [string]$Description
    )

    if (-not [MoneyHomeCommandNative]::IsWindow([IntPtr]$Handle)) {
        throw "$Description 已失效：$Handle"
    }
    $actualProcessId = 0
    [void][MoneyHomeCommandNative]::GetWindowThreadProcessId(
        [IntPtr]$Handle,
        [ref]$actualProcessId
    )
    if ($actualProcessId -ne $ExpectedProcessId) {
        throw "$Description 不属于 MoneyHome8 PID $ExpectedProcessId。"
    }
    $className = [System.Text.StringBuilder]::new(256)
    [void][MoneyHomeCommandNative]::GetClassName(
        [IntPtr]$Handle,
        $className,
        $className.Capacity
    )
    if ($className.ToString() -ne $ExpectedClass) {
        throw "$Description 类名应为 $ExpectedClass，实际为 $($className.ToString())。"
    }
}

function Get-TopLevelWindows {
    param([int]$TargetProcessId)

    $windows = [System.Collections.Generic.List[object]]::new()
    [MoneyHomeCommandNative]::EnumWindows(
        {
            param([IntPtr]$handle, [IntPtr]$lParam)

            $processId = 0
            [void][MoneyHomeCommandNative]::GetWindowThreadProcessId($handle, [ref]$processId)
            if ($processId -ne $TargetProcessId) {
                return $true
            }

            $className = [System.Text.StringBuilder]::new(256)
            $title = [System.Text.StringBuilder]::new(1024)
            [void][MoneyHomeCommandNative]::GetClassName($handle, $className, $className.Capacity)
            [void][MoneyHomeCommandNative]::GetWindowText($handle, $title, $title.Capacity)
            $rect = New-Object MoneyHomeCommandNative+RECT
            [void][MoneyHomeCommandNative]::GetWindowRect($handle, [ref]$rect)

            $windows.Add([pscustomobject]@{
                handle = $handle.ToInt64()
                class_name = $className.ToString()
                title = $title.ToString()
                visible = [MoneyHomeCommandNative]::IsWindowVisible($handle)
                enabled = [MoneyHomeCommandNative]::IsWindowEnabled($handle)
                left = $rect.Left
                top = $rect.Top
                width = $rect.Right - $rect.Left
                height = $rect.Bottom - $rect.Top
            })
            return $true
        },
        [IntPtr]::Zero
    ) | Out-Null
    $windows
}

function Wait-Until {
    param(
        [scriptblock]$Condition,
        [int]$Timeout
    )

    $watch = [System.Diagnostics.Stopwatch]::StartNew()
    while ($watch.ElapsedMilliseconds -lt $Timeout) {
        $result = & $Condition
        if ($null -ne $result -and $false -ne $result) {
            return $result
        }
        Start-Sleep -Milliseconds 100
    }
    $null
}

function Save-WindowCapture {
    param(
        [long]$Handle,
        [string]$Path
    )

    $rect = New-Object MoneyHomeCommandNative+RECT
    [void][MoneyHomeCommandNative]::GetWindowRect([IntPtr]$Handle, [ref]$rect)
    $width = $rect.Right - $rect.Left
    $height = $rect.Bottom - $rect.Top
    if ($width -le 0 -or $height -le 0) {
        throw "MoneyHome 对话框尺寸无效：${width}x${height}"
    }

    $parent = Split-Path -Parent $Path
    if (-not [string]::IsNullOrWhiteSpace($parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }

    $bitmap = New-Object System.Drawing.Bitmap($width, $height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $deviceContext = $graphics.GetHdc()
        try {
            if (-not [MoneyHomeCommandNative]::PrintWindow([IntPtr]$Handle, $deviceContext, 2)) {
                throw "PrintWindow 截图失败：$Handle"
            }
        }
        finally {
            $graphics.ReleaseHdc($deviceContext)
        }
        $bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    }
    finally {
        $graphics.Dispose()
        $bitmap.Dispose()
    }
}

function Get-NamedNodes {
    param(
        [long]$Handle,
        [int]$Limit
    )

    $root = [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]$Handle)
    if ($null -eq $root) {
        return @()
    }
    $nodes = $root.FindAll(
        [System.Windows.Automation.TreeScope]::Descendants,
        [System.Windows.Automation.Condition]::TrueCondition
    )
    $result = [System.Collections.Generic.List[object]]::new()
    for ($index = 0; $index -lt $nodes.Count -and $result.Count -lt $Limit; $index++) {
        $node = $nodes.Item($index)
        if ([string]::IsNullOrWhiteSpace($node.Current.Name)) {
            continue
        }
        $result.Add([pscustomobject]@{
            index = $index
            name = $node.Current.Name
            class_name = $node.Current.ClassName
            control_type = $node.Current.ControlType.ProgrammaticName
            native_handle = $node.Current.NativeWindowHandle
            enabled = $node.Current.IsEnabled
            offscreen = $node.Current.IsOffscreen
            rectangle = $node.Current.BoundingRectangle.ToString()
        })
    }
    $result
}

Assert-MoneyHomeWindow `
    -Handle $MainWindowHandle `
    -ExpectedProcessId $MoneyHomeProcessId `
    -ExpectedClass "TMoneyHome8" `
    -Description "MoneyHome8 主内容窗体"
Assert-MoneyHomeWindow `
    -Handle $BookkeepingToolbarHandle `
    -ExpectedProcessId $MoneyHomeProcessId `
    -ExpectedClass "TRzPanel" `
    -Description "MoneyHome8 顶部记账工具栏"

if (-not [MoneyHomeCommandNative]::IsWindowEnabled([IntPtr]$MainWindowHandle)) {
    throw "MoneyHome8 主窗口当前不可用，可能仍有模态对话框未关闭。"
}

$position = [IntPtr](($BookkeepingButtonY -shl 16) -bor ($BookkeepingButtonX -band 0xffff))
[void][MoneyHomeCommandNative]::PostMessage(
    [IntPtr]$BookkeepingToolbarHandle,
    0x0200,
    [IntPtr]::Zero,
    $position
)
[void][MoneyHomeCommandNative]::PostMessage(
    [IntPtr]$BookkeepingToolbarHandle,
    0x0201,
    [IntPtr]1,
    $position
)
[void][MoneyHomeCommandNative]::PostMessage(
    [IntPtr]$BookkeepingToolbarHandle,
    0x0202,
    [IntPtr]::Zero,
    $position
)
$popup = Wait-Until -Timeout $TimeoutMilliseconds -Condition {
    Get-TopLevelWindows -TargetProcessId $MoneyHomeProcessId |
        Where-Object { $_.visible -and $_.class_name -eq "#32768" } |
        Select-Object -First 1
}
if ($null -eq $popup) {
    throw "未能打开 MoneyHome8 顶层记账菜单。"
}
$popupProcessId = 0
$popupThreadId = [MoneyHomeCommandNative]::GetWindowThreadProcessId(
    [IntPtr]$popup.handle,
    [ref]$popupProcessId
)
$threadInfo = New-Object MoneyHomeCommandNative+GUITHREADINFO
$threadInfo.cbSize = [System.Runtime.InteropServices.Marshal]::SizeOf($threadInfo)
if (-not [MoneyHomeCommandNative]::GetGUIThreadInfo($popupThreadId, [ref]$threadInfo)) {
    throw "无法读取 MoneyHome8 弹出菜单线程状态。"
}
$ownerHandle = $threadInfo.hwndMenuOwner.ToInt64()
if ($ownerHandle -eq 0) {
    throw "未找到 MoneyHome8 弹出菜单的命令接收窗口。"
}
[void][MoneyHomeCommandNative]::SendMessage(
    [IntPtr]$popup.handle,
    0x01E6,
    [IntPtr]::Zero,
    [IntPtr]::Zero
)
Start-Sleep -Milliseconds 150

$before = @(Get-TopLevelWindows -TargetProcessId $MoneyHomeProcessId)
$beforeHandles = @($before | ForEach-Object handle)

# Delphi 菜单命令由当前弹出菜单的隐藏 owner 接收；异步投递避免模态窗口阻塞当前脚本。
if (-not [MoneyHomeCommandNative]::PostMessage(
    [IntPtr]$ownerHandle,
    0x0111,
    [IntPtr]$CommandId,
    [IntPtr]::Zero
)) {
    throw "投递 MoneyHome8 命令失败：$CommandId"
}

$dialog = Wait-Until -Timeout $TimeoutMilliseconds -Condition {
    Get-TopLevelWindows -TargetProcessId $MoneyHomeProcessId |
        Where-Object {
            $_.visible -and
            $_.enabled -and
            $_.width -gt 0 -and
            $_.height -gt 0 -and
            $_.handle -notin $beforeHandles -and
            $_.class_name -eq $ExpectedDialogClass -and
            (
                [string]::IsNullOrWhiteSpace($ExpectedDialogTitle) -or
                $_.title -eq $ExpectedDialogTitle
            )
        } |
        Select-Object -First 1
}
if ($null -eq $dialog) {
    throw "命令 $CommandId 未打开预期对话框 $ExpectedDialogClass / $ExpectedDialogTitle。"
}

$resolvedOutputPath = if ([System.IO.Path]::IsPathRooted($OutputPath)) {
    $OutputPath
}
else {
    Join-Path (Get-Location) $OutputPath
}
Save-WindowCapture -Handle $dialog.handle -Path $resolvedOutputPath
$nodes = @(Get-NamedNodes -Handle $dialog.handle -Limit $MaxNodes)

# 默认只观察初始状态并立即关闭；显式保留时由调用方负责取消对话框。
$mainReady = $false
if (-not $KeepOpen) {
    [void][MoneyHomeCommandNative]::PostMessage(
        [IntPtr]$dialog.handle,
        0x0010,
        [IntPtr]::Zero,
        [IntPtr]::Zero
    )
    $mainReady = Wait-Until -Timeout $TimeoutMilliseconds -Condition {
        [MoneyHomeCommandNative]::IsWindow([IntPtr]$MainWindowHandle) -and
        [MoneyHomeCommandNative]::IsWindowEnabled([IntPtr]$MainWindowHandle)
    }
    if (-not $mainReady) {
        throw "关闭命令 $CommandId 的对话框后，MoneyHome8 主窗口未恢复可用状态。"
    }
}

[pscustomobject]@{
    command_id = $CommandId
    expected_dialog_class = $ExpectedDialogClass
    expected_dialog_title = $ExpectedDialogTitle
    owner_handle = $ownerHandle
    dialog = $dialog
    screenshot = $resolvedOutputPath
    named_nodes = $nodes
    kept_open = [bool]$KeepOpen
    main_window_restored = $mainReady
} | ConvertTo-Json -Depth 8
