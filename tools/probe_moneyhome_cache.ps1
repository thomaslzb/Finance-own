param(
    [string]$MoneyHomeCachePath = ".\tools\moneyhome8-runtime\MoneyHome8.cache",
    [string]$InvestmentCachePath = ".\tools\moneyhome8-runtime\Investment.cache"
)

$ErrorActionPreference = "Stop"

function Get-Bytes {
    param([string]$Path)
    $resolved = (Resolve-Path -LiteralPath $Path).Path
    [ordered]@{
        path = $resolved
        bytes = [System.IO.File]::ReadAllBytes($resolved)
    }
}

function Count-Marker {
    param(
        [byte[]]$Bytes,
        [byte[]]$Marker
    )

    $count = 0
    for ($index = 0; $index -le $Bytes.Length - $Marker.Length; $index++) {
        $matches = $true
        for ($offset = 0; $offset -lt $Marker.Length; $offset++) {
            if ($Bytes[$index + $offset] -ne $Marker[$offset]) {
                $matches = $false
                break
            }
        }
        if ($matches) {
            $count++
        }
    }
    $count
}

function Inspect-Cache {
    param(
        [string]$Role,
        [string]$Path
    )

    $loaded = Get-Bytes -Path $Path
    $bytes = $loaded.bytes
    $ascii = [System.Text.Encoding]::ASCII
    $header = $ascii.GetString($bytes, 0, [Math]::Min(14, $bytes.Length))
    if ($header -ne "MoneyHomeCache") {
        throw "$Role 文件头不是 MoneyHomeCache：$($loaded.path)"
    }

    [ordered]@{
        role = $Role
        path = $loaded.path
        bytes = $bytes.Length
        header = $header
        py_markers = Count-Marker -Bytes $bytes -Marker $ascii.GetBytes("_PY")
        list_markers = Count-Marker -Bytes $bytes -Marker $ascii.GetBytes("_LIST")
        type_3_markers = Count-Marker -Bytes $bytes -Marker $ascii.GetBytes("_3")
        type_4_markers = Count-Marker -Bytes $bytes -Marker $ascii.GetBytes("_4")
        type_9_markers = Count-Marker -Bytes $bytes -Marker $ascii.GetBytes("_9")
    }
}

[ordered]@{
    status = "PASS"
    caches = @(
        Inspect-Cache -Role "MoneyHome8.cache" -Path $MoneyHomeCachePath
        Inspect-Cache -Role "Investment.cache" -Path $InvestmentCachePath
    )
} | ConvertTo-Json -Depth 4
