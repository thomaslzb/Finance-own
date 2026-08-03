param(
    [ValidateSet("all", "fmt", "check", "test", "run")]
    [string]$Action = "all"
)

$ErrorActionPreference = "Stop"

$workspace = Split-Path -Parent $PSScriptRoot
$toolRoot = Join-Path $workspace ".tools"
$cargoHome = Join-Path $toolRoot "cargo"
$rustupHome = Join-Path $toolRoot "rustup"
$sqliteRoot = Join-Path $toolRoot "sqlite3"

$env:CARGO_HOME = $cargoHome
$env:RUSTUP_HOME = $rustupHome
$env:CARGO_TARGET_DIR = Join-Path $toolRoot "target"
$env:SQLITE3_LIB_DIR = $sqliteRoot
$env:SQLITE3_STATIC = "0"

$toolchain = Get-ChildItem -LiteralPath (Join-Path $rustupHome "toolchains") -Directory |
    Select-Object -First 1
if ($null -eq $toolchain) {
    throw "项目内 Rust toolchain 不存在：$rustupHome"
}

$rustLld = Get-ChildItem -LiteralPath $toolchain.FullName -Recurse -Filter "rust-lld.exe" |
    Where-Object { $_.FullName -like "*x86_64-pc-windows-gnu*" } |
    Select-Object -First 1
if ($null -eq $rustLld) {
    throw "项目内 rust-lld.exe 不存在：$($toolchain.FullName)"
}

foreach ($requiredFile in @("sqlite3.dll", "libsqlite3.a")) {
    $requiredPath = Join-Path $sqliteRoot $requiredFile
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "SQLite 构建依赖不存在：$requiredPath"
    }
}

$env:CARGO_TARGET_X86_64_PC_WINDOWS_GNU_LINKER = $rustLld.FullName
$env:Path = @(
    (Join-Path $cargoHome "bin")
    (Join-Path $toolchain.FullName "bin")
    $sqliteRoot
    $env:Path
) -join ";"

function Invoke-Cargo {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments)

    & cargo @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "cargo $($Arguments -join ' ') 执行失败，退出码：$LASTEXITCODE"
    }
}

Push-Location $workspace
try {
    switch ($Action) {
        "fmt" {
            Invoke-Cargo fmt --check
        }
        "check" {
            Invoke-Cargo check
        }
        "test" {
            Invoke-Cargo test
        }
        "run" {
            Invoke-Cargo run
        }
        "all" {
            Invoke-Cargo fmt --check
            Invoke-Cargo check
            Invoke-Cargo test
        }
    }
}
finally {
    Pop-Location
}
