use std::fs;
use std::path::{Path, PathBuf};

use serde_json::{Map, Value};

use crate::domain::money::ScaledValue;
use crate::domain::reference_store::{
    FeeRule, Quote, RateRule, ReferenceStoreError, ReferenceStoreRepository,
};

/// 从受控 JSON 中间文件读取共享参考数据。
///
/// JSON 由 `tools/probe_mhlink_reference.ps1 -IncludeRows` 生成，Rust 侧只做字段映射和
/// 查询，不直接依赖 Windows COM。这样第一期可以先固定领域契约，再按需替换底层适配器。
#[derive(Debug, Clone)]
pub struct ReferenceJsonRepository {
    /// JSON 中间文件路径，用于错误定位和交付记录。
    pub path: PathBuf,
    root: Value,
}

impl ReferenceJsonRepository {
    /// 从 JSON 文件加载共享参考数据。
    pub fn from_path(path: impl AsRef<Path>) -> Result<Self, ReferenceStoreError> {
        let path = path.as_ref().to_path_buf();
        let content = fs::read_to_string(&path)
            .map_err(|error| ReferenceStoreError::Io(error.kind().to_string()))?;
        Self::from_json(path, &content)
    }

    /// 从 JSON 文本加载共享参考数据；测试和离线转换都复用同一映射逻辑。
    pub fn from_json(path: PathBuf, content: &str) -> Result<Self, ReferenceStoreError> {
        let root = serde_json::from_str(content)
            .map_err(|error| ReferenceStoreError::SchemaMismatch(error.to_string()))?;
        Ok(Self { path, root })
    }

    fn table_rows(
        &self,
        table_name: &str,
    ) -> Result<Vec<&Map<String, Value>>, ReferenceStoreError> {
        let tables = self
            .root
            .get("tables")
            .and_then(Value::as_array)
            .ok_or_else(|| ReferenceStoreError::SchemaMismatch("缺少 tables 数组".to_owned()))?;

        let table = tables
            .iter()
            .find(|table| {
                table
                    .get("table")
                    .and_then(Value::as_str)
                    .is_some_and(|name| name.eq_ignore_ascii_case(table_name))
            })
            .ok_or_else(|| {
                ReferenceStoreError::SchemaMismatch(format!("缺少参考表 {table_name}"))
            })?;

        let rows = table.get("rows").and_then(Value::as_array).ok_or_else(|| {
            ReferenceStoreError::AdapterUnavailable(format!(
                "参考表 {table_name} 缺少 rows；请使用 -IncludeRows 生成 JSON"
            ))
        })?;

        rows.iter()
            .map(|row| {
                row.as_object().ok_or_else(|| {
                    ReferenceStoreError::SchemaMismatch(format!("参考表 {table_name} 包含非对象行"))
                })
            })
            .collect()
    }
}

impl ReferenceStoreRepository for ReferenceJsonRepository {
    fn list_rate_rules(&self) -> Result<Vec<RateRule>, ReferenceStoreError> {
        self.table_rows("HBRate")?
            .into_iter()
            .map(map_rate_rule)
            .collect()
    }

    fn find_quotes_by_code(&self, code: &str) -> Result<Vec<Quote>, ReferenceStoreError> {
        let normalized = code.trim();
        if normalized.is_empty() {
            return Ok(Vec::new());
        }

        self.table_rows("TBSecuPrice")?
            .into_iter()
            .filter(|row| {
                get_string(row, "SecuCode")
                    .is_ok_and(|value| value.eq_ignore_ascii_case(normalized))
            })
            .map(map_quote)
            .collect()
    }

    fn list_quotes(&self, limit: Option<usize>) -> Result<Vec<Quote>, ReferenceStoreError> {
        let limit = limit.unwrap_or(500);
        self.table_rows("TBSecuPrice")?
            .into_iter()
            .take(limit)
            .map(map_quote)
            .collect()
    }

    fn list_fee_rules(&self) -> Result<Vec<FeeRule>, ReferenceStoreError> {
        self.table_rows("TBTransFee")?
            .into_iter()
            .map(map_fee_rule)
            .collect()
    }
}

fn map_rate_rule(row: &Map<String, Value>) -> Result<RateRule, ReferenceStoreError> {
    Ok(RateRule {
        legacy_currency_type: get_i64(row, "CurrType")?,
        legacy_deposit_type: get_i64(row, "DepoType")?,
        legacy_deposit_term: get_i64(row, "DepoTime")?,
        legacy_rate_value: get_scaled(row, "ARate")?,
        legacy_row_id: get_optional_legacy_id(row),
    })
}

fn map_quote(row: &Map<String, Value>) -> Result<Quote, ReferenceStoreError> {
    Ok(Quote {
        instrument_code: get_string(row, "SecuCode")?,
        price_date: normalize_access_date(&get_string(row, "PriceDate")?),
        price: get_scaled(row, "Price")?,
        legacy_object_type: get_i64(row, "ObjType")?,
        legacy_currency_type: get_i64(row, "CurrType")?,
        legacy_row_id: get_optional_legacy_id(row),
    })
}

fn map_fee_rule(row: &Map<String, Value>) -> Result<FeeRule, ReferenceStoreError> {
    Ok(FeeRule {
        legacy_type: get_i64(row, "Type")?,
        commission_rate: get_optional_scaled(row, "YJFL")?,
        stamp_tax_rate: get_optional_scaled(row, "YHSL_SELL")?
            .or(get_optional_scaled(row, "YHSL")?),
        minimum_commission: get_optional_scaled(row, "ZDYJ")?,
        transfer_fee_rate: get_optional_scaled(row, "GHF")?,
        surcharge_rate: get_optional_scaled(row, "FJF")?,
        settlement_rate: get_optional_scaled(row, "JSFL")?,
        legacy_row_id: get_optional_legacy_id(row),
    })
}

fn get_i64(row: &Map<String, Value>, field: &str) -> Result<i64, ReferenceStoreError> {
    let value = required_field(row, field)?;
    if let Some(number) = value.as_i64() {
        return Ok(number);
    }
    if let Some(number) = value.as_f64() {
        if number.fract() == 0.0 {
            return Ok(number as i64);
        }
    }
    if let Some(text) = value.as_str() {
        return text
            .parse::<i64>()
            .map_err(|_| ReferenceStoreError::SchemaMismatch(format!("{field} 不是整数：{text}")));
    }
    Err(ReferenceStoreError::SchemaMismatch(format!(
        "{field} 不是可解析整数"
    )))
}

fn get_string(row: &Map<String, Value>, field: &str) -> Result<String, ReferenceStoreError> {
    let value = required_field(row, field)?;
    if let Some(text) = value.as_str() {
        return Ok(text.to_owned());
    }
    Ok(value_to_decimal_text(value))
}

fn get_scaled(row: &Map<String, Value>, field: &str) -> Result<ScaledValue, ReferenceStoreError> {
    decimal_text_to_scaled(&value_to_decimal_text(required_field(row, field)?))
}

fn get_optional_scaled(
    row: &Map<String, Value>,
    field: &str,
) -> Result<Option<ScaledValue>, ReferenceStoreError> {
    match row.get(field) {
        Some(Value::Null) | None => Ok(None),
        Some(value) => decimal_text_to_scaled(&value_to_decimal_text(value)).map(Some),
    }
}

fn required_field<'a>(
    row: &'a Map<String, Value>,
    field: &str,
) -> Result<&'a Value, ReferenceStoreError> {
    row.get(field)
        .ok_or_else(|| ReferenceStoreError::SchemaMismatch(format!("缺少字段 {field}")))
}

fn get_optional_legacy_id(row: &Map<String, Value>) -> Option<String> {
    row.get("ID").map(value_to_decimal_text)
}

fn value_to_decimal_text(value: &Value) -> String {
    match value {
        Value::Number(number) => number.to_string(),
        Value::String(text) => text.clone(),
        other => other.to_string(),
    }
}

fn decimal_text_to_scaled(text: &str) -> Result<ScaledValue, ReferenceStoreError> {
    let trimmed = text.trim();
    let sign = if trimmed.starts_with('-') { -1 } else { 1 };
    let unsigned = trimmed.trim_start_matches(['-', '+']);
    let (whole, fraction) = unsigned.split_once('.').unwrap_or((unsigned, ""));
    if whole.is_empty() && fraction.is_empty() {
        return Err(ReferenceStoreError::SchemaMismatch(
            "空数值不能转换为定点数".to_owned(),
        ));
    }

    let digits = format!("{whole}{fraction}");
    let units = digits
        .parse::<i64>()
        .map_err(|_| ReferenceStoreError::SchemaMismatch(format!("无法转换定点数：{trimmed}")))?
        * sign;
    let scale = u8::try_from(fraction.len())
        .map_err(|_| ReferenceStoreError::SchemaMismatch(format!("定点数小数位过长：{trimmed}")))?;
    Ok(ScaledValue::new(units, scale))
}

fn normalize_access_date(text: &str) -> String {
    text.split(['T', ' '])
        .next()
        .unwrap_or(text)
        .replace('/', "-")
}

#[cfg(test)]
mod tests {
    use super::*;

    fn repository() -> ReferenceJsonRepository {
        let json = r#"
        {
          "tables": [
            {
              "table": "HBRate",
              "rows": [
                {"ID":1,"CurrType":1,"DepoType":10,"DepoTime":0,"ARate":3500}
              ]
            },
            {
              "table": "TBSecuPrice",
              "rows": [
                {"ID":1,"SecuCode":"002560","PriceDate":"2020-06-22T00:00:00","Price":1.461,"ObjectQuant":1.0,"CurrType":1,"ObjType":4},
                {"ID":2,"SecuCode":"ABC","PriceDate":"2020/6/23 0:00:00","Price":"2.500","ObjectQuant":1,"CurrType":2,"ObjType":3}
              ]
            },
            {
              "table": "TBTransFee",
              "rows": [
                {"ID":1,"Type":1,"YJFL":0.003,"YHSL":0,"YHSL_SELL":0.001,"ZDYJ":5,"GHF":0.01,"FJF":0,"JSFL":0,"JSFSX":0,"JYGF":0,"YJFL_SELL":0.003,"ZDYJ_SELL":5}
              ]
            }
          ]
        }
        "#;
        ReferenceJsonRepository::from_json(PathBuf::from("fixture.json"), json).unwrap()
    }

    #[test]
    fn maps_reference_json_rows_to_domain_records() {
        let repository = repository();

        let rates = repository.list_rate_rules().unwrap();
        assert_eq!(rates[0].legacy_currency_type, 1);
        assert_eq!(rates[0].legacy_rate_value, ScaledValue::new(3500, 0));

        let quotes = repository.find_quotes_by_code("002560").unwrap();
        assert_eq!(quotes.len(), 1);
        assert_eq!(quotes[0].price_date, "2020-06-22");
        assert_eq!(quotes[0].price, ScaledValue::new(1461, 3));

        let fee_rules = repository.list_fee_rules().unwrap();
        assert_eq!(fee_rules[0].commission_rate, Some(ScaledValue::new(3, 3)));
        assert_eq!(fee_rules[0].stamp_tax_rate, Some(ScaledValue::new(1, 3)));
    }

    #[test]
    fn limits_quote_listing_and_reports_missing_rows() {
        let repository = repository();

        assert_eq!(repository.list_quotes(Some(1)).unwrap().len(), 1);

        let json_without_rows = r#"{"tables":[{"table":"HBRate"}]}"#;
        let repository =
            ReferenceJsonRepository::from_json(PathBuf::from("missing.json"), json_without_rows)
                .unwrap();
        let error = repository.list_rate_rules().unwrap_err();
        assert!(matches!(error, ReferenceStoreError::AdapterUnavailable(_)));
    }

    #[test]
    fn reads_generated_mhlink_reference_json_when_present() {
        let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("artifacts")
            .join("reference")
            .join("mhlink-reference.json");
        if !path.is_file() {
            return;
        }

        let repository = ReferenceJsonRepository::from_path(path).unwrap();

        assert_eq!(repository.list_rate_rules().unwrap().len(), 113);
        assert_eq!(repository.list_fee_rules().unwrap().len(), 11);
        assert_eq!(repository.list_quotes(Some(20_000)).unwrap().len(), 12_207);
        assert_eq!(
            repository.find_quotes_by_code("002560").unwrap()[0].instrument_code,
            "002560"
        );
    }
}
