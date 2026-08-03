use std::collections::HashSet;

use super::money::MoneyAmount;

/// 工资收入或普通扣款中的一条分类明细。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PayrollCategoryLine {
    /// 稳定收支分类标识，不能使用页面显示文字替代。
    pub category_id: String,
    /// 明细原币金额；已提交明细必须大于零。
    pub amount: MoneyAmount,
}

/// 一个人员名下某个社保账户的缴费组成。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PayrollSocialContributionLine {
    /// 社保账户稳定标识。
    pub social_account_id: String,
    /// 由职工承担并减少实收现金的个人缴费。
    pub personal_amount: MoneyAmount,
    /// 由单位承担并直接增加社保权益的公司缴费。
    pub company_amount: MoneyAmount,
}

/// 工资收入复合交易草稿。
///
/// 旧页面同时维护收入、扣款和社保缴费三组明细。目标模型把这些事实分开保存，
/// 避免仅以最终实收金额生成普通收入而丢失税费和福利组成。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PayrollIncomeDraft {
    /// 目标账簿稳定标识。
    pub ledger_id: String,
    /// 实收现金进入的账户稳定标识。
    pub receiving_account_id: String,
    /// 工资交易原币代码。
    pub currency_code: String,
    /// 工资业务日期，格式为 `YYYY-MM-DD`。
    pub business_date: String,
    /// 可选社保人员；存在社保缴费明细时必须提供。
    pub person_id: Option<String>,
    /// 税前工资、奖金和补贴等收入组成。
    pub income_lines: Vec<PayrollCategoryLine>,
    /// 个税及其它不进入社保账户的普通扣款组成。
    pub deduction_lines: Vec<PayrollCategoryLine>,
    /// 个人和公司社保缴费组成。
    pub social_contribution_lines: Vec<PayrollSocialContributionLine>,
    /// 交易关联标签稳定标识。
    pub tag_ids: Vec<String>,
    /// 可选工资说明。
    pub description: Option<String>,
}

/// 工资草稿按最小货币单位计算出的确定性汇总。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PayrollTotals {
    /// 全部收入项目合计。
    pub gross_income_minor_units: i64,
    /// 普通扣款项目合计。
    pub deduction_minor_units: i64,
    /// 个人社保缴费合计。
    pub personal_contribution_minor_units: i64,
    /// 公司社保缴费合计。
    pub company_contribution_minor_units: i64,
    /// 进入收入账户的实收现金。
    pub net_cash_minor_units: i64,
    /// 个人与公司缴费共同形成的社保账户权益增加额。
    pub social_account_credit_minor_units: i64,
}

/// 工资草稿进入应用服务前可确定的输入错误。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PayrollValidationError {
    /// 未指定目标账簿。
    MissingLedgerId,
    /// 未指定实收账户。
    MissingReceivingAccountId,
    /// 未指定工资币种。
    MissingCurrencyCode,
    /// 未指定工资业务日期。
    MissingBusinessDate,
    /// 工资没有任何收入明细。
    MissingIncomeLines,
    /// 指定收入明细缺少稳定分类标识。
    MissingIncomeCategoryId {
        /// 从零开始的收入明细位置。
        line_index: usize,
    },
    /// 指定扣款明细缺少稳定分类标识。
    MissingDeductionCategoryId {
        /// 从零开始的扣款明细位置。
        line_index: usize,
    },
    /// 指定分类明细金额不是正数。
    NonPositiveCategoryAmount {
        /// `income` 或 `deduction`。
        section: &'static str,
        /// 从零开始的明细位置。
        line_index: usize,
    },
    /// 明细币种与工资交易币种不一致。
    CurrencyMismatch {
        /// 发生错误的明细区域。
        section: &'static str,
        /// 从零开始的明细位置。
        line_index: usize,
        /// 明细实际币种。
        actual_currency_code: String,
    },
    /// 同一工资重复使用收入分类。
    DuplicateIncomeCategoryId(String),
    /// 同一工资重复使用扣款分类。
    DuplicateDeductionCategoryId(String),
    /// 社保缴费明细存在，但没有指定对应人员。
    SocialContributionRequiresPerson,
    /// 指定社保缴费明细缺少账户标识。
    MissingSocialAccountId {
        /// 从零开始的社保明细位置。
        line_index: usize,
    },
    /// 社保明细的个人或公司缴费为负数。
    NegativeSocialContribution {
        /// 从零开始的社保明细位置。
        line_index: usize,
    },
    /// 社保明细的个人和公司缴费同时为零。
    EmptySocialContribution {
        /// 从零开始的社保明细位置。
        line_index: usize,
    },
    /// 同一工资重复使用社保账户。
    DuplicateSocialAccountId(String),
    /// 扣款与个人缴费超过收入合计。
    NegativeNetCash,
    /// 汇总金额超出 `i64` 最小货币单位范围。
    AmountOverflow,
    /// 同一工资重复关联标签。
    DuplicateTagId(String),
}

impl PayrollIncomeDraft {
    /// 校验身份、币种、明细唯一性和目标实收公式。
    pub fn validate(&self) -> Result<(), Vec<PayrollValidationError>> {
        let mut errors = Vec::new();

        if self.ledger_id.trim().is_empty() {
            errors.push(PayrollValidationError::MissingLedgerId);
        }
        if self.receiving_account_id.trim().is_empty() {
            errors.push(PayrollValidationError::MissingReceivingAccountId);
        }
        if self.currency_code.trim().is_empty() {
            errors.push(PayrollValidationError::MissingCurrencyCode);
        }
        if self.business_date.trim().is_empty() {
            errors.push(PayrollValidationError::MissingBusinessDate);
        }
        if self.income_lines.is_empty() {
            errors.push(PayrollValidationError::MissingIncomeLines);
        }

        validate_category_lines(
            &self.income_lines,
            "income",
            &self.currency_code,
            &mut errors,
        );
        validate_category_lines(
            &self.deduction_lines,
            "deduction",
            &self.currency_code,
            &mut errors,
        );

        collect_duplicate_ids(
            self.income_lines
                .iter()
                .map(|line| line.category_id.as_str()),
            &mut errors,
            PayrollValidationError::DuplicateIncomeCategoryId,
        );
        collect_duplicate_ids(
            self.deduction_lines
                .iter()
                .map(|line| line.category_id.as_str()),
            &mut errors,
            PayrollValidationError::DuplicateDeductionCategoryId,
        );

        if !self.social_contribution_lines.is_empty()
            && self
                .person_id
                .as_deref()
                .is_none_or(|person_id| person_id.trim().is_empty())
        {
            errors.push(PayrollValidationError::SocialContributionRequiresPerson);
        }

        for (line_index, line) in self.social_contribution_lines.iter().enumerate() {
            if line.social_account_id.trim().is_empty() {
                errors.push(PayrollValidationError::MissingSocialAccountId { line_index });
            }
            if line.personal_amount.minor_units < 0 || line.company_amount.minor_units < 0 {
                errors.push(PayrollValidationError::NegativeSocialContribution { line_index });
            }
            if line.personal_amount.minor_units == 0 && line.company_amount.minor_units == 0 {
                errors.push(PayrollValidationError::EmptySocialContribution { line_index });
            }
            for (section, amount) in [
                ("personal_social", &line.personal_amount),
                ("company_social", &line.company_amount),
            ] {
                if amount.currency_code != self.currency_code {
                    errors.push(PayrollValidationError::CurrencyMismatch {
                        section,
                        line_index,
                        actual_currency_code: amount.currency_code.clone(),
                    });
                }
            }
        }

        collect_duplicate_ids(
            self.social_contribution_lines
                .iter()
                .map(|line| line.social_account_id.as_str()),
            &mut errors,
            PayrollValidationError::DuplicateSocialAccountId,
        );
        collect_duplicate_ids(
            self.tag_ids.iter().map(String::as_str),
            &mut errors,
            PayrollValidationError::DuplicateTagId,
        );

        match self.compute_totals() {
            Ok(totals) if totals.net_cash_minor_units < 0 => {
                errors.push(PayrollValidationError::NegativeNetCash);
            }
            Err(error) => errors.push(error),
            Ok(_) => {}
        }

        if errors.is_empty() {
            Ok(())
        } else {
            Err(errors)
        }
    }

    /// 计算目标工资口径：实收等于收入减普通扣款和个人社保缴费。
    ///
    /// 公司缴费直接增加社保账户权益，不进入收入账户现金。该规则是 Rust 目标设计；
    /// MoneyHome8 的精确社保投影仍须用真实提交样例校准。
    pub fn calculate_totals(&self) -> Result<PayrollTotals, Vec<PayrollValidationError>> {
        self.validate()?;
        self.compute_totals().map_err(|error| vec![error])
    }

    fn compute_totals(&self) -> Result<PayrollTotals, PayrollValidationError> {
        let gross_income_minor_units =
            checked_sum(self.income_lines.iter().map(|line| line.amount.minor_units))?;
        let deduction_minor_units = checked_sum(
            self.deduction_lines
                .iter()
                .map(|line| line.amount.minor_units),
        )?;
        let personal_contribution_minor_units = checked_sum(
            self.social_contribution_lines
                .iter()
                .map(|line| line.personal_amount.minor_units),
        )?;
        let company_contribution_minor_units = checked_sum(
            self.social_contribution_lines
                .iter()
                .map(|line| line.company_amount.minor_units),
        )?;
        let net_cash_minor_units = gross_income_minor_units
            .checked_sub(deduction_minor_units)
            .and_then(|value| value.checked_sub(personal_contribution_minor_units))
            .ok_or(PayrollValidationError::AmountOverflow)?;
        let social_account_credit_minor_units = personal_contribution_minor_units
            .checked_add(company_contribution_minor_units)
            .ok_or(PayrollValidationError::AmountOverflow)?;

        Ok(PayrollTotals {
            gross_income_minor_units,
            deduction_minor_units,
            personal_contribution_minor_units,
            company_contribution_minor_units,
            net_cash_minor_units,
            social_account_credit_minor_units,
        })
    }
}

fn validate_category_lines(
    lines: &[PayrollCategoryLine],
    section: &'static str,
    currency_code: &str,
    errors: &mut Vec<PayrollValidationError>,
) {
    for (line_index, line) in lines.iter().enumerate() {
        if line.category_id.trim().is_empty() {
            errors.push(match section {
                "income" => PayrollValidationError::MissingIncomeCategoryId { line_index },
                _ => PayrollValidationError::MissingDeductionCategoryId { line_index },
            });
        }
        if line.amount.minor_units <= 0 {
            errors.push(PayrollValidationError::NonPositiveCategoryAmount {
                section,
                line_index,
            });
        }
        if line.amount.currency_code != currency_code {
            errors.push(PayrollValidationError::CurrencyMismatch {
                section,
                line_index,
                actual_currency_code: line.amount.currency_code.clone(),
            });
        }
    }
}

fn collect_duplicate_ids<'a>(
    ids: impl Iterator<Item = &'a str>,
    errors: &mut Vec<PayrollValidationError>,
    duplicate_error: impl Fn(String) -> PayrollValidationError,
) {
    let mut seen = HashSet::new();
    for id in ids {
        if !seen.insert(id) {
            errors.push(duplicate_error(id.to_owned()));
        }
    }
}

fn checked_sum(mut values: impl Iterator<Item = i64>) -> Result<i64, PayrollValidationError> {
    values.try_fold(0_i64, |total, value| {
        total
            .checked_add(value)
            .ok_or(PayrollValidationError::AmountOverflow)
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn amount(minor_units: i64) -> MoneyAmount {
        MoneyAmount::new(minor_units, "CNY")
    }

    fn category_line(category_id: &str, minor_units: i64) -> PayrollCategoryLine {
        PayrollCategoryLine {
            category_id: category_id.to_owned(),
            amount: amount(minor_units),
        }
    }

    fn draft() -> PayrollIncomeDraft {
        PayrollIncomeDraft {
            ledger_id: "ledger-1".to_owned(),
            receiving_account_id: "cash-cny".to_owned(),
            currency_code: "CNY".to_owned(),
            business_date: "2026-07-31".to_owned(),
            person_id: Some("person-1".to_owned()),
            income_lines: vec![category_line("salary", 100_000)],
            deduction_lines: vec![category_line("income-tax", 10_000)],
            social_contribution_lines: vec![PayrollSocialContributionLine {
                social_account_id: "social-pension".to_owned(),
                personal_amount: amount(8_000),
                company_amount: amount(12_000),
            }],
            tag_ids: Vec::new(),
            description: None,
        }
    }

    #[test]
    fn calculates_net_cash_and_social_credit_from_separate_components() {
        let totals = draft().calculate_totals().unwrap();

        assert_eq!(totals.gross_income_minor_units, 100_000);
        assert_eq!(totals.deduction_minor_units, 10_000);
        assert_eq!(totals.personal_contribution_minor_units, 8_000);
        assert_eq!(totals.company_contribution_minor_units, 12_000);
        assert_eq!(totals.net_cash_minor_units, 82_000);
        assert_eq!(totals.social_account_credit_minor_units, 20_000);
    }

    #[test]
    fn requires_person_when_social_contributions_are_present() {
        let mut invalid = draft();
        invalid.person_id = None;

        assert!(invalid
            .validate()
            .unwrap_err()
            .contains(&PayrollValidationError::SocialContributionRequiresPerson));
    }

    #[test]
    fn rejects_duplicate_categories_and_negative_net_cash() {
        let mut invalid = draft();
        invalid
            .deduction_lines
            .push(category_line("income-tax", 100_000));

        let errors = invalid.validate().unwrap_err();

        assert!(
            errors.contains(&PayrollValidationError::DuplicateDeductionCategoryId(
                "income-tax".to_owned()
            ))
        );
        assert!(errors.contains(&PayrollValidationError::NegativeNetCash));
    }

    #[test]
    fn rejects_currency_mismatch_and_sum_overflow() {
        let mut invalid = draft();
        invalid.income_lines[0].amount.currency_code = "USD".to_owned();
        invalid.income_lines.push(category_line("bonus", i64::MAX));

        let errors = invalid.validate().unwrap_err();

        assert!(errors.contains(&PayrollValidationError::CurrencyMismatch {
            section: "income",
            line_index: 0,
            actual_currency_code: "USD".to_owned(),
        }));
        assert!(errors.contains(&PayrollValidationError::AmountOverflow));
    }
}
