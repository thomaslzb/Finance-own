param(
    [Parameter(Mandatory = $true)]
    [int]$MoneyHomeProcessId,
    [long]$RootHandle = 0,
    [switch]$VisibleOnly
)

$ErrorActionPreference = "Stop"

if (-not ("MoneyHomeChildWindowNative" -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
using System.Text;

public static class MoneyHomeChildWindowNative
{
    public delegate bool EnumWindowsProc(IntPtr windowHandle, IntPtr parameter);

    [StructLayout(LayoutKind.Sequential)]
    public struct RECT
    {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    [DllImport("user32.dll")]
    public static extern bool EnumChildWindows(IntPtr parent, EnumWindowsProc callback, IntPtr parameter);

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr windowHandle, out uint processId);

    [DllImport("user32.dll")]
    public static extern IntPtr GetParent(IntPtr windowHandle);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern int GetClassName(IntPtr windowHandle, StringBuilder className, int maxCount);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern int GetWindowText(IntPtr windowHandle, StringBuilder title, int maxCount);

    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr windowHandle, out RECT rectangle);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr windowHandle);

    [DllImport("user32.dll")]
    public static extern bool IsWindowEnabled(IntPtr windowHandle);
}
'@
}

if ($RootHandle -eq 0) {
    throw "必须提供属于指定 MoneyHome8 进程的 RootHandle。"
}

$rootProcessId = 0
[void][MoneyHomeChildWindowNative]::GetWindowThreadProcessId(
    [IntPtr]$RootHandle,
    [ref]$rootProcessId
)
if ($rootProcessId -ne $MoneyHomeProcessId) {
    throw "RootHandle $RootHandle 不属于 MoneyHome8 PID $MoneyHomeProcessId。"
}

$windows = [System.Collections.Generic.List[object]]::new()
[MoneyHomeChildWindowNative]::EnumChildWindows(
    [IntPtr]$RootHandle,
    {
        param([IntPtr]$windowHandle, [IntPtr]$parameter)

        $processId = 0
        [void][MoneyHomeChildWindowNative]::GetWindowThreadProcessId(
            $windowHandle,
            [ref]$processId
        )
        if ($processId -ne $MoneyHomeProcessId) {
            return $true
        }

        $visible = [MoneyHomeChildWindowNative]::IsWindowVisible($windowHandle)
        if ($VisibleOnly -and -not $visible) {
            return $true
        }

        $className = [System.Text.StringBuilder]::new(256)
        $title = [System.Text.StringBuilder]::new(1024)
        $rectangle = New-Object MoneyHomeChildWindowNative+RECT
        [void][MoneyHomeChildWindowNative]::GetClassName(
            $windowHandle,
            $className,
            $className.Capacity
        )
        [void][MoneyHomeChildWindowNative]::GetWindowText(
            $windowHandle,
            $title,
            $title.Capacity
        )
        [void][MoneyHomeChildWindowNative]::GetWindowRect(
            $windowHandle,
            [ref]$rectangle
        )

        $windows.Add([pscustomobject]@{
            handle = $windowHandle.ToInt64()
            parent_handle = [MoneyHomeChildWindowNative]::GetParent($windowHandle).ToInt64()
            class_name = $className.ToString()
            title = $title.ToString()
            visible = $visible
            enabled = [MoneyHomeChildWindowNative]::IsWindowEnabled($windowHandle)
            left = $rectangle.Left
            top = $rectangle.Top
            width = $rectangle.Right - $rectangle.Left
            height = $rectangle.Bottom - $rectangle.Top
        })
        return $true
    },
    [IntPtr]::Zero
) | Out-Null

$windows | ConvertTo-Json -Depth 4
