param(
    [Parameter(Mandatory = $true)]
    [int]$MoneyHomeProcessId,
    [switch]$VisibleOnly
)

$ErrorActionPreference = "Stop"

if (-not ("MoneyHomeWindowListNative" -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
using System.Text;

public static class MoneyHomeWindowListNative
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
    public static extern bool EnumWindows(EnumWindowsProc callback, IntPtr parameter);

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr windowHandle, out uint processId);

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

# 只枚举指定进程，避免把用户其它 MoneyHome8 实例或桌面窗口混入结果。
$windows = [System.Collections.Generic.List[object]]::new()
[MoneyHomeWindowListNative]::EnumWindows(
    {
        param([IntPtr]$windowHandle, [IntPtr]$parameter)

        $processId = 0
        [void][MoneyHomeWindowListNative]::GetWindowThreadProcessId(
            $windowHandle,
            [ref]$processId
        )
        if ($processId -ne $MoneyHomeProcessId) {
            return $true
        }

        $visible = [MoneyHomeWindowListNative]::IsWindowVisible($windowHandle)
        if ($VisibleOnly -and -not $visible) {
            return $true
        }

        $className = [System.Text.StringBuilder]::new(256)
        $title = [System.Text.StringBuilder]::new(1024)
        $rectangle = New-Object MoneyHomeWindowListNative+RECT
        [void][MoneyHomeWindowListNative]::GetClassName(
            $windowHandle,
            $className,
            $className.Capacity
        )
        [void][MoneyHomeWindowListNative]::GetWindowText(
            $windowHandle,
            $title,
            $title.Capacity
        )
        [void][MoneyHomeWindowListNative]::GetWindowRect(
            $windowHandle,
            [ref]$rectangle
        )

        $windows.Add([pscustomobject]@{
            handle = $windowHandle.ToInt64()
            class_name = $className.ToString()
            title = $title.ToString()
            visible = $visible
            enabled = [MoneyHomeWindowListNative]::IsWindowEnabled($windowHandle)
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
