param(
    [string]$SourcePath = ".\artifacts\mhlink-copy.mdb",
    [string]$OutputPath = ".\artifacts\reference\mhlink-reference.json"
)

$ErrorActionPreference = "Stop"

$workspace = Split-Path -Parent $PSScriptRoot
$resolvedOutput = if ([System.IO.Path]::IsPathRooted($OutputPath)) {
    $OutputPath
}
else {
    Join-Path $workspace $OutputPath
}

$outputDirectory = Split-Path -Parent $resolvedOutput
if (-not [System.IO.Directory]::Exists($outputDirectory)) {
    [System.IO.Directory]::CreateDirectory($outputDirectory) | Out-Null
}

$json = & (Join-Path $PSScriptRoot "probe_mhlink_reference.ps1") -Path $SourcePath -IncludeRows
if ($null -ne $LASTEXITCODE -and $LASTEXITCODE -ne 0) {
    throw "probe_mhlink_reference.ps1 执行失败，退出码：$LASTEXITCODE"
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($resolvedOutput, ($json -join [Environment]::NewLine), $utf8NoBom)

[ordered]@{
    source_path = (Resolve-Path -LiteralPath $SourcePath).Path
    output_path = $resolvedOutput
    bytes = (Get-Item -LiteralPath $resolvedOutput).Length
} | ConvertTo-Json
