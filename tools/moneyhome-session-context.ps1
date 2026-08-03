param(
    [Parameter(Mandatory = $true)]
    [string]$ExpectedLedgerSha256,
    [string]$BaselineBackupPath = "",
    [string]$LedgerPath = "C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8",
    [string]$ExpectedProcessPath = "C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
    [string]$ExpectedApplicationTitle = "test - 财智8",
    [string]$ExpectedShellTitle = "财智8"
)

$ErrorActionPreference = "Stop"

if (-not ("MoneyHomeSessionContextNative" -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
using System.Text;

public static class MoneyHomeSessionContextNative
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
    public static extern bool EnumChildWindows(IntPtr parent, EnumWindowsProc callback, IntPtr parameter);

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

function Get-WindowRecord {
    param([IntPtr]$Handle)

    $processId = 0
    [void][MoneyHomeSessionContextNative]::GetWindowThreadProcessId($Handle, [ref]$processId)
    $className = [System.Text.StringBuilder]::new(256)
    $title = [System.Text.StringBuilder]::new(1024)
    $rectangle = New-Object MoneyHomeSessionContextNative+RECT
    [void][MoneyHomeSessionContextNative]::GetClassName($Handle, $className, $className.Capacity)
    [void][MoneyHomeSessionContextNative]::GetWindowText($Handle, $title, $title.Capacity)
    [void][MoneyHomeSessionContextNative]::GetWindowRect($Handle, [ref]$rectangle)

    [pscustomobject]@{
        handle = $Handle.ToInt64()
        process_id = $processId
        class_name = $className.ToString()
        title = $title.ToString()
        visible = [MoneyHomeSessionContextNative]::IsWindowVisible($Handle)
        enabled = [MoneyHomeSessionContextNative]::IsWindowEnabled($Handle)
        left = $rectangle.Left
        top = $rectangle.Top
        width = $rectangle.Right - $rectangle.Left
        height = $rectangle.Bottom - $rectangle.Top
    }
}

function Get-UniqueRecord {
    param(
        [object[]]$Records,
        [string]$Description
    )

    if ($Records.Count -ne 1) {
        $summary = $Records | Select-Object handle, class_name, title, visible, enabled
        throw "$Description 应唯一，实际为 $($Records.Count)：$($summary | ConvertTo-Json -Compress)"
    }
    $Records[0]
}

$resolvedLedgerPath = (Resolve-Path -LiteralPath $LedgerPath).Path
if ($resolvedLedgerPath -ne "C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8") {
    throw "本项目只允许操作指定测试账簿：$resolvedLedgerPath"
}

$expectedLedgerHash = $ExpectedLedgerSha256.ToUpperInvariant()
$ledgerHash = $null
$ledgerHashReadError = $null
try {
    $ledgerHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $resolvedLedgerPath).Hash
}
catch {
    $ledgerHashReadError = $_.Exception.Message
}

$resolvedBaselineBackupPath = $null
$baselineBackupHash = $null
if (-not [string]::IsNullOrWhiteSpace($BaselineBackupPath)) {
    $resolvedBaselineBackupPath = (Resolve-Path -LiteralPath $BaselineBackupPath).Path
    $allowedBackupRoot = [System.IO.Path]::GetFullPath(
        "C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\backups"
    ).TrimEnd('\') + '\'
    if (-not $resolvedBaselineBackupPath.StartsWith(
        $allowedBackupRoot,
        [StringComparison]::OrdinalIgnoreCase
    )) {
        throw "基线副本不在项目证据目录：$resolvedBaselineBackupPath"
    }
    $baselineBackupHash = (
        Get-FileHash -Algorithm SHA256 -LiteralPath $resolvedBaselineBackupPath
    ).Hash
    if ($baselineBackupHash -ne $expectedLedgerHash) {
        throw "基线副本指纹不符合场景基线，期望 $expectedLedgerHash，实际 $baselineBackupHash。"
    }
}

if ($null -ne $ledgerHash -and $ledgerHash -ne $expectedLedgerHash) {
    throw "测试账簿指纹不符合场景基线，期望 $expectedLedgerHash，实际 $ledgerHash。"
}
if ($null -eq $ledgerHash -and $null -eq $baselineBackupHash) {
    throw "运行中的测试账簿无法读取指纹，且未提供可核对的 BaselineBackupPath：$ledgerHashReadError"
}

$processes = @(Get-Process MoneyHome8 -ErrorAction SilentlyContinue)
if ($processes.Count -ne 1) {
    throw "动态场景要求唯一 MoneyHome8 进程，实际为 $($processes.Count)。"
}
$process = $processes[0]
$actualProcessPath = [System.IO.Path]::GetFullPath($process.Path)
$resolvedExpectedProcessPath = [System.IO.Path]::GetFullPath($ExpectedProcessPath)
if (-not $actualProcessPath.Equals($resolvedExpectedProcessPath, [StringComparison]::OrdinalIgnoreCase)) {
    throw "MoneyHome8 进程路径不符合预期：$actualProcessPath"
}

$topLevelWindows = [System.Collections.Generic.List[object]]::new()
[MoneyHomeSessionContextNative]::EnumWindows(
    {
        param([IntPtr]$windowHandle, [IntPtr]$parameter)

        $record = Get-WindowRecord -Handle $windowHandle
        if ($record.process_id -eq $process.Id) {
            $topLevelWindows.Add($record)
        }
        return $true
    },
    [IntPtr]::Zero
) | Out-Null

$applicationWindow = Get-UniqueRecord -Description "TApplication 账簿容器" -Records @(
    $topLevelWindows | Where-Object {
        $_.class_name -eq "TApplication" -and
        $_.title -eq $ExpectedApplicationTitle
    }
)
$shellWindow = Get-UniqueRecord -Description "TMoneyHome8 主内容窗体" -Records @(
    $topLevelWindows | Where-Object {
        $_.class_name -eq "TMoneyHome8" -and
        $_.title -eq $ExpectedShellTitle -and
        $_.visible
    }
)

$childWindows = [System.Collections.Generic.List[object]]::new()
[MoneyHomeSessionContextNative]::EnumChildWindows(
    [IntPtr]$shellWindow.handle,
    {
        param([IntPtr]$windowHandle, [IntPtr]$parameter)

        $record = Get-WindowRecord -Handle $windowHandle
        if ($record.process_id -eq $process.Id) {
            $childWindows.Add($record)
        }
        return $true
    },
    [IntPtr]::Zero
) | Out-Null

# 记账按钮位于主窗体客户端区顶部。主题边框可能让客户端区相对外层窗体内缩 1 至 2 像素，
# 因此按边框容差识别，但仍要求候选唯一、接近全宽且高度稳定，避免误选普通内容面板。
$bookkeepingToolbar = Get-UniqueRecord -Description "顶部记账工具栏 TRzPanel" -Records @(
    $childWindows | Where-Object {
        $_.class_name -eq "TRzPanel" -and
        $_.visible -and
        $_.enabled -and
        $_.width -ge ($shellWindow.width - 4) -and
        $_.width -le $shellWindow.width -and
        $_.height -ge 45 -and
        $_.height -le 60 -and
        $_.left -ge $shellWindow.left -and
        $_.left -le ($shellWindow.left + 2) -and
        $_.top -ge $shellWindow.top -and
        $_.top -le ($shellWindow.top + 2)
    }
)

$ledgerInfo = Get-Item -LiteralPath $resolvedLedgerPath
$recoveryFiles = @(
    Get-ChildItem -Force -LiteralPath (Split-Path -Parent $resolvedLedgerPath) |
        Where-Object { $_.Name -like '~$test*' } |
        Select-Object FullName, Length, LastWriteTime
)

[pscustomobject]@{
    captured_at = (Get-Date).ToString("o")
    ledger = [pscustomobject]@{
        path = $resolvedLedgerPath
        sha256 = $ledgerHash
        sha256_accessible = $null -ne $ledgerHash
        sha256_read_error = $ledgerHashReadError
        expected_sha256 = $expectedLedgerHash
        baseline_backup_path = $resolvedBaselineBackupPath
        baseline_backup_sha256 = $baselineBackupHash
        length = $ledgerInfo.Length
        last_write_time = $ledgerInfo.LastWriteTime.ToString("o")
        recovery_files = $recoveryFiles
    }
    process = [pscustomobject]@{
        id = $process.Id
        path = $actualProcessPath
        start_time = $process.StartTime.ToString("o")
        responding = $process.Responding
    }
    application_window = $applicationWindow
    shell_window = $shellWindow
    bookkeeping_toolbar = $bookkeepingToolbar
} | ConvertTo-Json -Depth 8
