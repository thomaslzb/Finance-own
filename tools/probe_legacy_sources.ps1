param(
    [string]$LedgerPath = "C:\DCG-SZ\IT Manage\Private\Personal-Docs\test001.mh8",
    [string]$RuntimeDataPath = ".\tools\moneyhome8-runtime\MoneyHome8.data",
    [string]$DecompressedDataPath = ".\artifacts\MoneyHome8.data.decompressed.mdb"
)

$ErrorActionPreference = "Stop"

function Resolve-ProbePath {
    param([string]$Path)

    $candidate = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Path))
    if ([System.IO.Path]::IsPathRooted($Path)) {
        $candidate = $Path
    }
    return $candidate
}

function Test-JetHeader {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $false
    }

    $stream = [System.IO.File]::Open($Path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
    try {
        $buffer = New-Object byte[] 256
        $read = $stream.Read($buffer, 0, $buffer.Length)
        $text = [System.Text.Encoding]::ASCII.GetString($buffer, 0, $read)
        return $text.Contains("Standard Jet DB")
    }
    finally {
        $stream.Dispose()
    }
}

function Get-LockIndicators {
    param([string]$Path)

    $indicators = New-Object System.Collections.Generic.List[string]
    $directory = Split-Path -Parent $Path
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($Path)
    foreach ($candidate in @((Join-Path $directory "~`$$stem.ldb"), (Join-Path $directory "mh.ldb"), (Join-Path $directory "MoneyHome8.ldb"))) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $indicators.Add($candidate)
        }
    }
    return @($indicators)
}

function Get-SharedSha256 {
    param([string]$Path)

    $stream = [System.IO.File]::Open($Path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
    try {
        $sha = [System.Security.Cryptography.SHA256]::Create()
        try {
            $hashBytes = $sha.ComputeHash($stream)
            return ([System.BitConverter]::ToString($hashBytes)).Replace("-", "")
        }
        finally {
            $sha.Dispose()
        }
    }
    finally {
        $stream.Dispose()
    }
}

function Test-AceReadOnlyOpen {
    param([string]$Path)

    $connection = New-Object -ComObject ADODB.Connection
    $connection.ConnectionTimeout = 5
    $connectionString = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$Path;Mode=Read;Persist Security Info=False;"
    try {
        $connection.Open($connectionString)
        return [ordered]@{
            status = "open_ok"
            error = $null
        }
    }
    catch {
        $message = $_.Exception.Message
        $status = "open_failed"
        if ($message -like "*不可识别的数据库格式*") {
            $status = "invalid_format"
        }
        elseif ($message -like "*必要权限*" -or $message -like "*账户名称或密码*") {
            $status = "auth_failed"
        }
        elseif ($message -like "*使用中*" -or $message -like "*锁定*") {
            $status = "locked"
        }
        return [ordered]@{
            status = $status
            error = $message
        }
    }
    finally {
        if ($connection.State -eq 1) {
            $connection.Close()
        }
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($connection) | Out-Null
    }
}

function Inspect-Source {
    param(
        [string]$Role,
        [string]$Path,
        [bool]$ExpectJetHeader
    )

    $resolved = Resolve-ProbePath -Path $Path
    $exists = Test-Path -LiteralPath $resolved -PathType Leaf
    $locks = Get-LockIndicators -Path $resolved
    $processes = @(Get-Process -Name "MoneyHome8" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id)

    if (-not $exists) {
        return [ordered]@{
            role = $Role
            path = $resolved
            status = "file_not_found"
            exists = $false
            bytes = $null
            sha256 = $null
            has_jet_header = $false
            lock_indicators = $locks
            moneyhome8_process_ids = $processes
        }
    }

    $item = Get-Item -LiteralPath $resolved
    $diagnostics = New-Object System.Collections.Generic.List[string]
    $hash = $null
    $hasJetHeader = $false
    $readBlocked = $false
    try {
        $hash = Get-SharedSha256 -Path $resolved
        $hasJetHeader = Test-JetHeader -Path $resolved
    }
    catch {
        $readBlocked = $true
        $diagnostics.Add($_.Exception.Message)
    }

    $status = "success"
    if ($readBlocked -or $locks.Count -gt 0) {
        $status = "locked"
    }
    elseif ($ExpectJetHeader -and -not $hasJetHeader) {
        $status = "invalid_format"
    }
    $ace = Test-AceReadOnlyOpen -Path $resolved
    if ($ace.status -in @("auth_failed", "invalid_format", "locked")) {
        $status = $ace.status
    }

    return [ordered]@{
        role = $Role
        path = $resolved
        status = $status
        exists = $true
        bytes = $item.Length
        sha256 = $hash
        has_jet_header = $hasJetHeader
        lock_indicators = $locks
        moneyhome8_process_ids = $processes
        ace_read_only = $ace
        diagnostics = @($diagnostics)
    }
}

$sources = @(
    Inspect-Source -Role "test.mh8" -Path $LedgerPath -ExpectJetHeader $true
    Inspect-Source -Role "MoneyHome8.data" -Path $RuntimeDataPath -ExpectJetHeader $false
    Inspect-Source -Role "MoneyHome8.data.decompressed.mdb" -Path $DecompressedDataPath -ExpectJetHeader $true
)

$overallStatus = "PASS"
foreach ($source in $sources) {
    if ($source.status -in @("file_not_found", "invalid_format")) {
        $overallStatus = "WARN"
    }
}

[ordered]@{
    status = $overallStatus
    sources = $sources
} | ConvertTo-Json -Depth 6
