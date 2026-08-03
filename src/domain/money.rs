/// 带币种的定点金额。
///
/// `minor_units` 使用币种最小单位，例如人民币 `100.25` 元保存为 `10025`。
/// 字段允许负数，以便查询投影直接表达带方向的发生额和余额。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MoneyAmount {
    /// 币种最小单位金额；正负号表达资金方向。
    pub minor_units: i64,
    /// 币种代码，对应 SQLite `currencies.code`。
    pub currency_code: String,
}

impl MoneyAmount {
    /// 创建定点金额，不执行币种精度换算。
    pub fn new(minor_units: i64, currency_code: impl Into<String>) -> Self {
        Self {
            minor_units,
            currency_code: currency_code.into(),
        }
    }
}

/// 带显式小数位的定点数。
///
/// 投资数量、价格和汇率不能使用 `f64` 写回账本；`units=12345, scale=3`
/// 表示 `12.345`。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ScaledValue {
    /// 去除小数点后的整数值。
    pub units: i64,
    /// 小数位数，必须与持久化层字段的 scale 一致。
    pub scale: u8,
}

impl ScaledValue {
    /// 创建带精度的定点值。
    pub const fn new(units: i64, scale: u8) -> Self {
        Self { units, scale }
    }
}

#[cfg(test)]
mod tests {
    use super::{MoneyAmount, ScaledValue};

    #[test]
    fn preserves_minor_units_and_scale() {
        assert_eq!(MoneyAmount::new(10_025, "CNY").minor_units, 10_025);
        assert_eq!(ScaledValue::new(12_345, 3).scale, 3);
    }
}
