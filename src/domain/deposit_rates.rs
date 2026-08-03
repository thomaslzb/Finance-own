use super::money::ScaledValue;

/// 新版存款利率允许的最大小数位，满足精确计算且避免任意精度输入拖垮换算。
pub const MAX_DEPOSIT_RATE_SCALE: u8 = 12;

/// 存款利率版本的来源。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DepositRateSource {
    /// 用户在矩阵中手工提交。
    Manual,
    /// 通过在线抓取批次发布。
    Online,
    /// 从 MoneyHome8 或其它旧格式导入。
    LegacyImport,
}

/// 存款利率发布前的领域草稿。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DepositRateDraft {
    /// 目标账簿稳定标识。
    pub ledger_id: String,
    /// 币种代码，对应 `currencies.code`。
    pub currency_code: String,
    /// 存款产品类型稳定代码，例如活期或整存整取。
    pub deposit_type: String,
    /// 期限稳定代码，例如 `demand`、`1m` 或 `notice_7d`。
    pub term_code: String,
    /// 以百分数表达的年利率；`units=36, scale=2` 表示 `0.36%`。
    pub annual_rate_percent: ScaledValue,
    /// 版本生效时间，使用带时区的 ISO 8601 文本。
    pub effective_at: String,
    /// 手工、在线或旧数据导入来源。
    pub source: DepositRateSource,
    /// 在线或导入来源必须关联已验证批次；手工来源必须为空。
    pub batch_id: Option<String>,
}

/// 存款利率在发布前可确认的输入错误。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DepositRateValidationError {
    /// 未指定账簿。
    MissingLedgerId,
    /// 未指定币种。
    MissingCurrencyCode,
    /// 未指定存款类型。
    MissingDepositType,
    /// 未指定期限代码。
    MissingTermCode,
    /// 未指定生效时间。
    MissingEffectiveAt,
    /// 年利率不能为负数。
    NegativeRate,
    /// 年利率小数位超过目标系统允许范围。
    ScaleTooLarge,
    /// 存款年利率超过目标系统的 `100%` 防误录上限。
    RateAboveOneHundredPercent,
    /// 在线或旧数据导入没有关联校验批次。
    MissingBatchId,
    /// 手工编辑错误地关联了在线批次。
    UnexpectedBatchId,
}

impl DepositRateDraft {
    /// 校验目标系统的明确范围，避免复制旧版“只要能解析就提交”的宽松行为。
    pub fn validate(&self) -> Result<(), Vec<DepositRateValidationError>> {
        let mut errors = Vec::new();

        if self.ledger_id.trim().is_empty() {
            errors.push(DepositRateValidationError::MissingLedgerId);
        }
        if self.currency_code.trim().is_empty() {
            errors.push(DepositRateValidationError::MissingCurrencyCode);
        }
        if self.deposit_type.trim().is_empty() {
            errors.push(DepositRateValidationError::MissingDepositType);
        }
        if self.term_code.trim().is_empty() {
            errors.push(DepositRateValidationError::MissingTermCode);
        }
        if self.effective_at.trim().is_empty() {
            errors.push(DepositRateValidationError::MissingEffectiveAt);
        }
        if self.annual_rate_percent.units < 0 {
            errors.push(DepositRateValidationError::NegativeRate);
        }
        if self.annual_rate_percent.scale > MAX_DEPOSIT_RATE_SCALE {
            errors.push(DepositRateValidationError::ScaleTooLarge);
        } else {
            let factor = 10_i64.pow(u32::from(self.annual_rate_percent.scale));
            if self.annual_rate_percent.units > factor * 100 {
                errors.push(DepositRateValidationError::RateAboveOneHundredPercent);
            }
        }

        match self.source {
            DepositRateSource::Manual if self.batch_id.is_some() => {
                errors.push(DepositRateValidationError::UnexpectedBatchId);
            }
            DepositRateSource::Online | DepositRateSource::LegacyImport
                if self
                    .batch_id
                    .as_deref()
                    .is_none_or(|batch_id| batch_id.trim().is_empty()) =>
            {
                errors.push(DepositRateValidationError::MissingBatchId);
            }
            _ => {}
        }

        if errors.is_empty() {
            Ok(())
        } else {
            Err(errors)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn draft() -> DepositRateDraft {
        DepositRateDraft {
            ledger_id: "ledger-1".to_owned(),
            currency_code: "CNY".to_owned(),
            deposit_type: "demand".to_owned(),
            term_code: "demand".to_owned(),
            annual_rate_percent: ScaledValue::new(36, 2),
            effective_at: "2026-08-02T06:00:00+08:00".to_owned(),
            source: DepositRateSource::Manual,
            batch_id: None,
        }
    }

    #[test]
    fn accepts_zero_and_observed_decimal_rate() {
        let mut rate = draft();
        rate.validate().unwrap();

        rate.annual_rate_percent = ScaledValue::new(0, 4);
        rate.validate().unwrap();
    }

    #[test]
    fn rejects_negative_excessive_and_over_precise_rates() {
        let mut negative = draft();
        negative.annual_rate_percent = ScaledValue::new(-1, 2);
        assert!(negative
            .validate()
            .unwrap_err()
            .contains(&DepositRateValidationError::NegativeRate));

        let mut excessive = draft();
        excessive.annual_rate_percent = ScaledValue::new(10_001, 2);
        assert!(excessive
            .validate()
            .unwrap_err()
            .contains(&DepositRateValidationError::RateAboveOneHundredPercent));

        let mut over_precise = draft();
        over_precise.annual_rate_percent = ScaledValue::new(1, 13);
        assert!(over_precise
            .validate()
            .unwrap_err()
            .contains(&DepositRateValidationError::ScaleTooLarge));
    }

    #[test]
    fn requires_batches_only_for_online_and_imported_versions() {
        let mut online = draft();
        online.source = DepositRateSource::Online;
        assert!(online
            .validate()
            .unwrap_err()
            .contains(&DepositRateValidationError::MissingBatchId));

        online.batch_id = Some("batch-1".to_owned());
        online.validate().unwrap();

        let mut manual = draft();
        manual.batch_id = Some("batch-1".to_owned());
        assert!(manual
            .validate()
            .unwrap_err()
            .contains(&DepositRateValidationError::UnexpectedBatchId));
    }
}
