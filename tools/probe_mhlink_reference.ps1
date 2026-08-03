param(
    [string]$Path = ".\artifacts\mhlink-copy.mdb",
    [switch]$IncludeRows
)

$ErrorActionPreference = "Stop"

$resolvedPath = (Resolve-Path -LiteralPath $Path).Path
$tables = @("HBRate", "TBSecuPrice", "TBTransFee")

$connection = New-Object -ComObject ADODB.Connection
$connection.Open("Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$resolvedPath;Mode=Read;")

try {
    $results = foreach ($table in $tables) {
        $countRecordset = New-Object -ComObject ADODB.Recordset
        $countRecordset.Open("SELECT COUNT(*) AS RowCount FROM [$table]", $connection, 0, 1)
        $rowCount = [int]$countRecordset.Fields.Item("RowCount").Value
        $countRecordset.Close()

        $sampleRecordset = New-Object -ComObject ADODB.Recordset
        $sampleRecordset.Open("SELECT TOP 1 * FROM [$table]", $connection, 0, 1)

        $fields = @()
        $sample = [ordered]@{}
        for ($index = 0; $index -lt $sampleRecordset.Fields.Count; $index++) {
            $field = $sampleRecordset.Fields.Item($index)
            $fields += $field.Name
            $sample[$field.Name] = $field.Value
        }
        $sampleRecordset.Close()

        $tableResult = [ordered]@{
            table = $table
            row_count = $rowCount
            fields = $fields
            first_row = $sample
        }

        if ($IncludeRows) {
            $rows = @()
            $rowsRecordset = New-Object -ComObject ADODB.Recordset
            $rowsRecordset.Open("SELECT * FROM [$table]", $connection, 0, 1)
            while (-not $rowsRecordset.EOF) {
                $row = [ordered]@{}
                for ($index = 0; $index -lt $rowsRecordset.Fields.Count; $index++) {
                    $field = $rowsRecordset.Fields.Item($index)
                    $row[$field.Name] = $field.Value
                }
                $rows += $row
                $rowsRecordset.MoveNext()
            }
            $rowsRecordset.Close()
            $tableResult["rows"] = $rows
        }

        $tableResult
    }

    [ordered]@{
        path = $resolvedPath
        provider = "Microsoft.ACE.OLEDB.16.0"
        mode = "Read"
        includes_rows = [bool]$IncludeRows
        tables = $results
    } | ConvertTo-Json -Depth 5
}
finally {
    $connection.Close()
}
