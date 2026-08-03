param(
    [string]$SourcePath = ".\tools\moneyhome8-runtime\MoneyHome8.data",
    [string]$OutputPath = ".\artifacts\MoneyHome8.data.decompressed.mdb",
    [int]$ZlibOffset = 125
)

$ErrorActionPreference = "Stop"

function Resolve-LocalPath {
    param([string]$Path)

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return $Path
    }
    return [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Path))
}

$source = Resolve-LocalPath -Path $SourcePath
$output = Resolve-LocalPath -Path $OutputPath
$outputDirectory = Split-Path -Parent $output
if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
    throw "MoneyHome8.data 不存在：$source"
}
if (-not (Test-Path -LiteralPath $outputDirectory -PathType Container)) {
    New-Item -ItemType Directory -Path $outputDirectory | Out-Null
}

$sourceStream = [System.IO.File]::Open($source, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
try {
    if ($sourceStream.Length -le ($ZlibOffset + 2)) {
        throw "MoneyHome8.data 长度不足，无法从偏移 $ZlibOffset 解压"
    }
    $sourceStream.Position = $ZlibOffset
    $zlibHeader = New-Object byte[] 2
    [void]$sourceStream.Read($zlibHeader, 0, 2)

    # 当前运行环境没有 ZLibStream；MoneyHome8.data 在偏移 125 处是 zlib 包，
    # 跳过 2 字节 zlib 头后使用 DeflateStream 读取压缩体，并忽略尾部 Adler32。
    $deflateStream = New-Object System.IO.Compression.DeflateStream($sourceStream, [System.IO.Compression.CompressionMode]::Decompress, $true)
    try {
        $outputStream = [System.IO.File]::Open($output, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
        try {
            $deflateStream.CopyTo($outputStream)
        }
        finally {
            $outputStream.Dispose()
        }
    }
    finally {
        $deflateStream.Dispose()
    }
}
finally {
    $sourceStream.Dispose()
}

$hash = Get-FileHash -LiteralPath $output -Algorithm SHA256
$item = Get-Item -LiteralPath $output
$stream = [System.IO.File]::Open($output, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::Read)
try {
    $buffer = New-Object byte[] 256
    $read = $stream.Read($buffer, 0, $buffer.Length)
    $headerText = [System.Text.Encoding]::ASCII.GetString($buffer, 0, $read)
    $hasJetHeader = $headerText.Contains("Standard Jet DB")
}
finally {
    $stream.Dispose()
}

$status = "PASS"
if (-not $hasJetHeader) {
    $status = "WARN"
}

[ordered]@{
    status = $status
    source = $source
    output = $output
    zlib_offset = $ZlibOffset
    zlib_header_hex = ([System.BitConverter]::ToString($zlibHeader)).Replace("-", "")
    bytes = $item.Length
    sha256 = $hash.Hash
    has_jet_header = $hasJetHeader
} | ConvertTo-Json -Depth 4
