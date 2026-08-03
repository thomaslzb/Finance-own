use super::money::MoneyAmount;

/// 待摊费用创建或导入前的领域草稿。
///
/// 页面中的“已摊销次数”只用于兼容旧账簿导入。新版正常创建必须从零开始，后续次数由
/// 已入账期次派生，不能直接修改计数而不生成对应交易。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PrepaidExpenseDraft {
    /// 目标账簿稳定标识。
    pub ledger_id: String,
    /// 待摊费用账户名称。
    pub name: String,
    /// 人员或机构稳定标识。
    pub party_id: String,
    /// 摊销支出项目稳定标识。
    pub expense_category_id: String,
    /// 可选初始资金来源账户；为空表示外部期初余额。
    pub funding_account_id: Option<String>,
    /// 待摊费用原始金额，必须为正数。
    pub amount: MoneyAmount,
    /// 业务发生日期，格式为 `YYYY-MM-DD`。
    pub business_date: String,
    /// 首次摊销日期，格式为 `YYYY-MM-DD`。
    pub first_amortization_date: String,
    /// 摊销间隔月数，旧页面单位固定为“月/次”。
    pub frequency_months: u32,
    /// 总摊销次数。
    pub total_installments: u32,
    /// 兼容导入时已经完成的期次数。
    pub imported_posted_installments: u32,
    /// 可选备注。
    pub note: Option<String>,
}

/// 待摊费用在提交前可确认的输入错误。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PrepaidExpenseValidationError {
    /// 未指定账簿。
    MissingLedgerId,
    /// 未选择人员或机构。
    MissingPartyId,
    /// 未输入款项名称。
    MissingName,
    /// 金额缺少币种代码。
    MissingCurrencyCode,
    /// 待摊金额必须大于零。
    NonPositiveAmount,
    /// 未选择摊销支出项目。
    MissingExpenseCategoryId,
    /// 未指定业务日期。
    MissingBusinessDate,
    /// 未指定首次摊销日期。
    MissingFirstAmortizationDate,
    /// 摊销频率必须大于零。
    ZeroFrequency,
    /// 总摊销次数必须大于零。
    ZeroTotalInstallments,
    /// 已摊销次数不能超过总摊销次数。
    PostedInstallmentsExceedTotal,
}

impl PrepaidExpenseDraft {
    /// 校验运行态已确认的必填项和期次边界。
    pub fn validate(&self) -> Result<(), Vec<PrepaidExpenseValidationError>> {
        let mut errors = Vec::new();

        if self.ledger_id.trim().is_empty() {
            errors.push(PrepaidExpenseValidationError::MissingLedgerId);
        }
        if self.party_id.trim().is_empty() {
            errors.push(PrepaidExpenseValidationError::MissingPartyId);
        }
        if self.name.trim().is_empty() {
            errors.push(PrepaidExpenseValidationError::MissingName);
        }
        if self.amount.currency_code.trim().is_empty() {
            errors.push(PrepaidExpenseValidationError::MissingCurrencyCode);
        }
        if self.amount.minor_units <= 0 {
            errors.push(PrepaidExpenseValidationError::NonPositiveAmount);
        }
        if self.expense_category_id.trim().is_empty() {
            errors.push(PrepaidExpenseValidationError::MissingExpenseCategoryId);
        }
        if self.business_date.trim().is_empty() {
            errors.push(PrepaidExpenseValidationError::MissingBusinessDate);
        }
        if self.first_amortization_date.trim().is_empty() {
            errors.push(PrepaidExpenseValidationError::MissingFirstAmortizationDate);
        }
        if self.frequency_months == 0 {
            errors.push(PrepaidExpenseValidationError::ZeroFrequency);
        }
        if self.total_installments == 0 {
            errors.push(PrepaidExpenseValidationError::ZeroTotalInstallments);
        }
        if self.imported_posted_installments > self.total_installments {
            errors.push(PrepaidExpenseValidationError::PostedInstallmentsExceedTotal);
        }

        if errors.is_empty() {
            Ok(())
        } else {
            Err(errors)
        }
    }

    /// 按新版确定性策略生成每期最小货币单位金额。
    ///
    /// 前 `n-1` 期使用整数除法结果，最后一期吸收全部尾差，保证期次合计精确等于原始金额。
    /// 该策略是 Finance Own 的目标实现规则，不代表 MoneyHome8 旧公式已经动态验证。
    pub fn planned_installment_amounts(
        &self,
    ) -> Result<Vec<i64>, Vec<PrepaidExpenseValidationError>> {
        self.validate()?;

        let count = i64::from(self.total_installments);
        let regular_amount = self.amount.minor_units / count;
        let final_amount = self.amount.minor_units - regular_amount * (count - 1);
        let mut amounts = vec![regular_amount; self.total_installments as usize];
        if let Some(last) = amounts.last_mut() {
            *last = final_amount;
        }
        Ok(amounts)
    }

    /// 返回兼容导入计数之后仍未摊销的计划金额。
    pub fn remaining_minor_units(&self) -> Result<i64, Vec<PrepaidExpenseValidationError>> {
        let amounts = self.planned_installment_amounts()?;
        Ok(amounts[self.imported_posted_installments as usize..]
            .iter()
            .sum())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn draft() -> PrepaidExpenseDraft {
        PrepaidExpenseDraft {
            ledger_id: "ledger-1".to_owned(),
            name: "年度服务费".to_owned(),
            party_id: "party-1".to_owned(),
            expense_category_id: "category-1".to_owned(),
            funding_account_id: None,
            amount: MoneyAmount::new(10_001, "CNY"),
            business_date: "2026-08-02".to_owned(),
            first_amortization_date: "2026-08-02".to_owned(),
            frequency_months: 1,
            total_installments: 3,
            imported_posted_installments: 0,
            note: None,
        }
    }

    #[test]
    fn validates_observed_required_fields_and_installment_bounds() {
        let mut invalid = draft();
        invalid.party_id.clear();
        invalid.name.clear();
        invalid.amount.minor_units = 0;
        invalid.expense_category_id.clear();
        invalid.frequency_months = 0;
        invalid.total_installments = 2;
        invalid.imported_posted_installments = 3;

        let errors = invalid.validate().unwrap_err();

        assert!(errors.contains(&PrepaidExpenseValidationError::MissingPartyId));
        assert!(errors.contains(&PrepaidExpenseValidationError::MissingName));
        assert!(errors.contains(&PrepaidExpenseValidationError::NonPositiveAmount));
        assert!(errors.contains(&PrepaidExpenseValidationError::MissingExpenseCategoryId));
        assert!(errors.contains(&PrepaidExpenseValidationError::ZeroFrequency));
        assert!(errors.contains(&PrepaidExpenseValidationError::PostedInstallmentsExceedTotal));
    }

    #[test]
    fn assigns_all_minor_unit_remainder_to_the_final_installment() {
        let amounts = draft().planned_installment_amounts().unwrap();

        assert_eq!(amounts, vec![3_333, 3_333, 3_335]);
        assert_eq!(amounts.iter().sum::<i64>(), 10_001);
    }

    #[test]
    fn derives_remaining_amount_from_posted_installments() {
        let mut imported = draft();
        imported.imported_posted_installments = 1;

        assert_eq!(imported.remaining_minor_units().unwrap(), 6_668);
    }
}
