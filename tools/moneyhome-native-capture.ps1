param(
    [Parameter(Mandatory = $true)]
    [long]$WindowHandle,
    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing
if (-not ("MoneyHomeNativeCapture" -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;

public static class MoneyHomeNativeCapture
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
    public static extern bool GetWindowRect(IntPtr windowHandle, out RECT rectangle);

    [DllImport("user32.dll")]
    public static extern bool PrintWindow(IntPtr windowHandle, IntPtr deviceContext, uint flags);
}
'@
}

$rectangle = New-Object MoneyHomeNativeCapture+RECT
if (-not [MoneyHomeNativeCapture]::GetWindowRect(
    [IntPtr]$WindowHandle,
    [ref]$rectangle
)) {
    throw "无法读取窗口尺寸：$WindowHandle"
}

$width = $rectangle.Right - $rectangle.Left
$height = $rectangle.Bottom - $rectangle.Top
if ($width -le 0 -or $height -le 0) {
    throw "窗口已关闭或尺寸无效：$WindowHandle (${width}x${height})"
}

$resolvedOutput = [System.IO.Path]::GetFullPath(
    $OutputPath,
    (Get-Location).Path
)
$parent = Split-Path -Parent $resolvedOutput
if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
    throw "截图目录不存在：$parent"
}

# PrintWindow 只读取指定句柄的像素，适用于 UIA 无法识别的 Delphi 所有者绘制菜单。
$bitmap = New-Object System.Drawing.Bitmap($width, $height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
try {
    $deviceContext = $graphics.GetHdc()
    try {
        if (-not [MoneyHomeNativeCapture]::PrintWindow(
            [IntPtr]$WindowHandle,
            $deviceContext,
            2
        )) {
            throw "PrintWindow 截图失败：$WindowHandle"
        }
    } finally {
        $graphics.ReleaseHdc($deviceContext)
    }
    $bitmap.Save($resolvedOutput, [System.Drawing.Imaging.ImageFormat]::Png)
} finally {
    $graphics.Dispose()
    $bitmap.Dispose()
}

Get-Item -LiteralPath $resolvedOutput |
    Select-Object FullName, Length, LastWriteTime |
    ConvertTo-Json -Depth 3
