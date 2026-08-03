param(
    [Parameter(Mandatory = $true)]
    [long]$MainWindowHandle,
    [Parameter(Mandatory = $true)]
    [long]$TreeHandle,
    [int]$StartIndex = 0,
    [int]$EndIndex = 12,
    [int]$NavigationWaitMilliseconds = 700,
    [int]$QueryWaitMilliseconds = 2500
)

$ErrorActionPreference = "Stop"

$workspace = Split-Path -Parent $PSScriptRoot
$runtimeTool = Join-Path $PSScriptRoot "moneyhome-runtime-window.ps1"
$outputDirectory = Join-Path $workspace "artifacts\runtime-validation\screenshots"

# 坐标是报表树客户区坐标；探针只覆盖当前无需滚动即可到达的日常收支和资产负债报表。
$reports = @(
    [pscustomobject]@{ key = "daily-income-expense"; y = 49 }
    [pscustomobject]@{ key = "daily-income-expense-detail"; y = 80 }
    [pscustomobject]@{ key = "account-income-expense"; y = 110 }
    [pscustomobject]@{ key = "tag-income-expense"; y = 140 }
    [pscustomobject]@{ key = "period-income-expense-compare"; y = 171 }
    [pscustomobject]@{ key = "income-expense-statistics"; y = 201 }
    [pscustomobject]@{ key = "income-expense-trend"; y = 231 }
    [pscustomobject]@{ key = "monthly-average-income-expense"; y = 261 }
    [pscustomobject]@{ key = "cash-flow"; y = 291 }
    [pscustomobject]@{ key = "balance-sheet"; y = 363 }
    [pscustomobject]@{ key = "available-funds"; y = 393 }
    [pscustomobject]@{ key = "credit-debt"; y = 423 }
    [pscustomobject]@{ key = "monthly-assets-trend"; y = 453 }
    [pscustomobject]@{ key = "investment-overview"; y = 523 }
    [pscustomobject]@{ key = "investment-income-overview"; y = 553 }
    [pscustomobject]@{ key = "investment-performance"; y = 584 }
    [pscustomobject]@{ key = "security-investment-overview"; y = 614 }
    [pscustomobject]@{ key = "security-fee-profit-loss"; y = 644 }
    [pscustomobject]@{ key = "security-market-value-trend"; y = 674 }
    [pscustomobject]@{ key = "open-fund-investment-overview"; y = 704 }
    [pscustomobject]@{ key = "open-fund-fee-profit-loss"; y = 734 }
    [pscustomobject]@{ key = "open-fund-market-value-trend"; y = 764 }
    [pscustomobject]@{ key = "online-lending-profit-loss"; y = 793 }
    [pscustomobject]@{ key = "financial-product-return"; y = 823 }
    [pscustomobject]@{ key = "foreign-exchange-overview"; y = 853 }
)

if ($StartIndex -lt 0 -or $EndIndex -ge $reports.Count -or $StartIndex -gt $EndIndex) {
    throw "报表索引范围无效：$StartIndex..$EndIndex / $($reports.Count)"
}

$results = [System.Collections.Generic.List[object]]::new()
for ($index = $StartIndex; $index -le $EndIndex; $index++) {
    $report = $reports[$index]
    [void](& $runtimeTool `
        -Action post-click `
        -WindowHandle $MainWindowHandle `
        -TargetHandle $TreeHandle `
        -X 110 `
        -Y $report.y `
        -WaitMilliseconds $NavigationWaitMilliseconds `
        -MaxNodes 20)

    $nodes = @(& $runtimeTool `
        -Action inspect `
        -WindowHandle $MainWindowHandle `
        -MaxNodes 220 | ConvertFrom-Json)
    $activeForm = $nodes |
        Where-Object { $_.class_name -like "TRpt*" } |
        Select-Object -First 1
    if ($null -eq $activeForm) {
        throw "未识别到活动报表窗体：$($report.key)"
    }

    $queryButton = $nodes |
        Where-Object { $_.name -eq "查询" -and $_.enabled -and -not $_.offscreen } |
        Select-Object -First 1
    $queried = $false
    if ($null -ne $queryButton) {
        # TRzButton 对鼠标消息的处理不一致，标准按钮命令可稳定触发只读查询。
        [void][MoneyHomeRuntimeNative]::SendMessage(
            [IntPtr]$queryButton.native_handle,
            0x00F5,
            [IntPtr]::Zero,
            [IntPtr]::Zero
        )
        Start-Sleep -Milliseconds $QueryWaitMilliseconds
        $queried = $true
    }

    $screenshotPath = Join-Path $outputDirectory "b16-$($report.key)-result.png"
    [void](& $runtimeTool `
        -Action capture `
        -WindowHandle $MainWindowHandle `
        -OutputPath $screenshotPath)

    $results.Add([pscustomobject]@{
        index = $index
        key = $report.key
        form_name = $activeForm.name
        form_class = $activeForm.class_name
        form_handle = $activeForm.native_handle
        queried = $queried
        screenshot = $screenshotPath.Substring($workspace.Length + 1).Replace("\", "/")
    })
}

$results | ConvertTo-Json -Depth 4
