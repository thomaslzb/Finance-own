param(
    [string]$Path = ".\artifacts\reference\mhlink-reference.json"
)

$ErrorActionPreference = "Stop"

$jsonPath = (Resolve-Path -LiteralPath $Path).Path
$content = [System.IO.File]::ReadAllText($jsonPath, [System.Text.Encoding]::UTF8)
$document = $content | ConvertFrom-Json

if (-not $document.includes_rows) {
    throw "参考库 JSON 缺少全量 rows；请使用 export_mhlink_reference_json.ps1 生成。"
}

$expected = @{
    "HBRate" = @{
        row_count = 113
        fields = @("ID", "CurrType", "DepoType", "DepoTime", "ARate")
    }
    "TBSecuPrice" = @{
        row_count = 12207
        fields = @("ID", "SecuCode", "PriceDate", "Price", "ObjectQuant", "CurrType", "ObjType")
    }
    "TBTransFee" = @{
        row_count = 11
        fields = @("ID", "Type", "YJFL", "YHSL", "YHSL_SELL", "ZDYJ", "GHF", "FJF", "JSFL", "JSFSX", "JYGF", "YJFL_SELL", "ZDYJ_SELL")
    }
}

$results = foreach ($tableName in $expected.Keys) {
    $table = $document.tables | Where-Object { $_.table -eq $tableName } | Select-Object -First 1
    if ($null -eq $table) {
        throw "参考库 JSON 缺少表：$tableName"
    }

    $expectedSpec = $expected[$tableName]
    if ([int]$table.row_count -ne [int]$expectedSpec.row_count) {
        throw "表 $tableName 行数不匹配：实际 $($table.row_count)，预期 $($expectedSpec.row_count)"
    }
    if ([int]$table.rows.Count -ne [int]$expectedSpec.row_count) {
        throw "表 $tableName rows 数组长度不匹配：实际 $($table.rows.Count)，预期 $($expectedSpec.row_count)"
    }

    $actualFields = @($table.fields)
    $expectedFields = @($expectedSpec.fields)
    if (($actualFields -join "|") -ne ($expectedFields -join "|")) {
        throw "表 $tableName 字段不匹配：实际 $($actualFields -join ','), 预期 $($expectedFields -join ',')"
    }

    [ordered]@{
        table = $tableName
        row_count = [int]$table.row_count
        rows_count = [int]$table.rows.Count
        fields = $actualFields
    }
}

[ordered]@{
    path = $jsonPath
    status = "PASS"
    tables = $results
} | ConvertTo-Json -Depth 4
