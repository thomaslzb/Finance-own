use std::collections::HashSet;

use super::money::MoneyAmount;

/// 余额调整页面读取到的不可变计算基线。
///
/// 账面余额必须与账户、币种、有效日期和版本一起传回应用层，避免用户确认前发生的
/// 新交易被旧页面快照覆盖。版本使用不透明文本，持久化适配器可以映射 SQLite 序号或哈希。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BalanceAdjustmentBaseline {
    /// 目标账簿稳定标识。
    pub ledger_id: String,
    /// 目标账户稳定标识。
    pub account_id: String,
    /// 调整生效日期，格式为 `YYYY-MM-DD`。
    pub effective_date: String,
    /// 读取账面余额时取得的不透明并发版本。
    pub balance_version: String,
    /// 该账户、币种和日期对应的账面余额。
    pub book_balance: MoneyAmount,
}

/// 用户确认前的余额调整领域草稿。
///
/// 该类型只固定已经确认的差额计算和并发边界。旧程序的系统对手分录与报表分类尚未
/// 动态校准，因此这里不会提前把草稿转换为通用交易分录。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BalanceAdjustmentDraft {
    /// 页面读取到的账面余额基线。
    pub baseline: BalanceAdjustmentBaseline,
    /// 用户盘点或对账后输入的真实余额。
    pub actual_balance: MoneyAmount,
    /// 与调整事件关联的标签稳定标识。
    pub tag_ids: Vec<String>,
    /// 可选调整说明。
    pub description: Option<String>,
}

/// 余额差额的业务落账策略。
///
/// 默认策略保留独立调整事件；日常收支策略把差额转换为普通收入或支出交易。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BalanceAdjustmentStrategy {
    /// 保存可审计的余额调整事件。
    AdjustmentEvent,
    /// 转换为普通对账收入或对账支出。
    DailyIncomeExpense,
}

/// 余额差额最终形成的业务事实类型。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BalanceAdjustmentPostingKind {
    /// 独立余额调整事件，差额可以为正、负或零。
    AdjustmentEvent,
    /// 普通收入，使用稳定对账收入分类。
    ReconciliationIncome,
    /// 普通支出，使用稳定对账支出分类。
    ReconciliationExpense,
}

impl BalanceAdjustmentStrategy {
    /// 按已校准的 MoneyHome8 规则确定差额最终落账类型。
    ///
    /// 日常收支只有负差额进入支出；正差额和零差额都进入对账收入。
    pub fn posting_kind(self, delta_minor_units: i64) -> BalanceAdjustmentPostingKind {
        match self {
            Self::AdjustmentEvent => BalanceAdjustmentPostingKind::AdjustmentEvent,
            Self::DailyIncomeExpense if delta_minor_units < 0 => {
                BalanceAdjustmentPostingKind::ReconciliationExpense
            }
            Self::DailyIncomeExpense => BalanceAdjustmentPostingKind::ReconciliationIncome,
        }
    }
}

/// 余额调整进入应用服务前可确认的输入错误。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BalanceAdjustmentValidationError {
    /// 未指定目标账簿。
    MissingLedgerId,
    /// 未指定目标账户。
    MissingAccountId,
    /// 未指定调整生效日期。
    MissingEffectiveDate,
    /// 未携带读取账面余额时取得的并发版本。
    MissingBalanceVersion,
    /// 账面余额缺少币种代码。
    MissingBookCurrencyCode,
    /// 真实余额缺少币种代码。
    MissingActualCurrencyCode,
    /// 真实余额币种与账面余额币种不一致。
    CurrencyMismatch {
        /// 账面余额币种。
        book_currency_code: String,
        /// 真实余额币种。
        actual_currency_code: String,
    },
    /// 同一调整事件重复关联标签。
    DuplicateTagId(String),
    /// 两个合法金额的差额超出 `i64` 最小货币单位范围。
    DeltaOverflow,
}

impl BalanceAdjustmentDraft {
    /// 校验稳定身份、并发基线和币种一致性。
    pub fn validate(&self) -> Result<(), Vec<BalanceAdjustmentValidationError>> {
        let mut errors = Vec::new();

        if self.baseline.ledger_id.trim().is_empty() {
            errors.push(BalanceAdjustmentValidationError::MissingLedgerId);
        }
        if self.baseline.account_id.trim().is_empty() {
            errors.push(BalanceAdjustmentValidationError::MissingAccountId);
        }
        if self.baseline.effective_date.trim().is_empty() {
            errors.push(BalanceAdjustmentValidationError::MissingEffectiveDate);
        }
        if self.baseline.balance_version.trim().is_empty() {
            errors.push(BalanceAdjustmentValidationError::MissingBalanceVersion);
        }

        let book_currency_code = self.baseline.book_balance.currency_code.trim();
        let actual_currency_code = self.actual_balance.currency_code.trim();
        if book_currency_code.is_empty() {
            errors.push(BalanceAdjustmentValidationError::MissingBookCurrencyCode);
        }
        if actual_currency_code.is_empty() {
            errors.push(BalanceAdjustmentValidationError::MissingActualCurrencyCode);
        }
        if !book_currency_code.is_empty()
            && !actual_currency_code.is_empty()
            && book_currency_code != actual_currency_code
        {
            errors.push(BalanceAdjustmentValidationError::CurrencyMismatch {
                book_currency_code: book_currency_code.to_owned(),
                actual_currency_code: actual_currency_code.to_owned(),
            });
        }

        let mut seen_tag_ids = HashSet::new();
        for tag_id in &self.tag_ids {
            if !seen_tag_ids.insert(tag_id) {
                errors.push(BalanceAdjustmentValidationError::DuplicateTagId(
                    tag_id.clone(),
                ));
            }
        }

        if errors.is_empty() {
            Ok(())
        } else {
            Err(errors)
        }
    }

    /// 按“真实余额减账面余额”计算带方向的最小货币单位差额。
    ///
    /// 正数表示需要增加账户余额，负数表示需要减少账户余额。MoneyHome8 已真实确认
    /// 零差额允许提交，因此本方法必须保留零值供策略层生成可审计事件。
    pub fn calculated_delta(&self) -> Result<MoneyAmount, Vec<BalanceAdjustmentValidationError>> {
        self.validate()?;

        let Some(minor_units) = self
            .actual_balance
            .minor_units
            .checked_sub(self.baseline.book_balance.minor_units)
        else {
            return Err(vec![BalanceAdjustmentValidationError::DeltaOverflow]);
        };

        Ok(MoneyAmount::new(
            minor_units,
            self.baseline.book_balance.currency_code.clone(),
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn draft(book_minor_units: i64, actual_minor_units: i64) -> BalanceAdjustmentDraft {
        BalanceAdjustmentDraft {
            baseline: BalanceAdjustmentBaseline {
                ledger_id: "ledger-1".to_owned(),
                account_id: "account-1".to_owned(),
                effective_date: "2026-07-31".to_owned(),
                balance_version: "sequence-42".to_owned(),
                book_balance: MoneyAmount::new(book_minor_units, "CNY"),
            },
            actual_balance: MoneyAmount::new(actual_minor_units, "CNY"),
            tag_ids: Vec::new(),
            description: None,
        }
    }

    #[test]
    fn calculates_positive_and_negative_delta_from_the_same_baseline() {
        assert_eq!(
            draft(10_000, 10_025)
                .calculated_delta()
                .unwrap()
                .minor_units,
            25
        );
        assert_eq!(
            draft(10_000, 9_975).calculated_delta().unwrap().minor_units,
            -25
        );
    }

    #[test]
    fn preserves_zero_delta_for_auditable_zero_value_posting() {
        assert_eq!(
            draft(10_000, 10_000)
                .calculated_delta()
                .unwrap()
                .minor_units,
            0
        );
    }

    #[test]
    fn classifies_daily_zero_delta_as_reconciliation_income() {
        assert_eq!(
            BalanceAdjustmentStrategy::DailyIncomeExpense.posting_kind(1),
            BalanceAdjustmentPostingKind::ReconciliationIncome
        );
        assert_eq!(
            BalanceAdjustmentStrategy::DailyIncomeExpense.posting_kind(0),
            BalanceAdjustmentPostingKind::ReconciliationIncome
        );
        assert_eq!(
            BalanceAdjustmentStrategy::DailyIncomeExpense.posting_kind(-1),
            BalanceAdjustmentPostingKind::ReconciliationExpense
        );
        assert_eq!(
            BalanceAdjustmentStrategy::AdjustmentEvent.posting_kind(0),
            BalanceAdjustmentPostingKind::AdjustmentEvent
        );
    }

    #[test]
    fn rejects_currency_mismatch_and_missing_balance_version() {
        let mut invalid = draft(10_000, 10_025);
        invalid.actual_balance.currency_code = "USD".to_owned();
        invalid.baseline.balance_version.clear();

        let errors = invalid.validate().unwrap_err();

        assert!(errors.contains(&BalanceAdjustmentValidationError::MissingBalanceVersion));
        assert!(
            errors.contains(&BalanceAdjustmentValidationError::CurrencyMismatch {
                book_currency_code: "CNY".to_owned(),
                actual_currency_code: "USD".to_owned(),
            })
        );
    }

    #[test]
    fn rejects_delta_overflow_without_wrapping_minor_units() {
        let invalid = draft(i64::MIN, i64::MAX);

        assert_eq!(
            invalid.calculated_delta(),
            Err(vec![BalanceAdjustmentValidationError::DeltaOverflow])
        );
    }
}
