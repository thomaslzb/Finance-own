use std::collections::HashSet;

use super::money::MoneyAmount;

/// 新系统支持的通用交易类型。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TransactionKind {
    /// 日常收入。
    Income,
    /// 日常支出。
    Expense,
    /// 账户之间的资金转移。
    Transfer,
    /// 余额、期初或其它人工调整。
    Adjustment,
    /// 投资等扩展领域提供的稳定类型键。
    DomainSpecific(String),
}

/// 新建交易的初始状态。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum NewTransactionStatus {
    /// 尚未进入余额和报表投影的草稿。
    Draft,
    /// 已确认并进入余额和报表投影的交易。
    Posted,
}

/// 原子账户分录在业务交易中的角色。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransactionEntryRole {
    /// 收入或支出的主要账户分录。
    Primary,
    /// 转账的对方账户分录。
    Counterparty,
    /// 分类或账户拆分产生的分录。
    Split,
    /// 手续费分录。
    Fee,
    /// 利息分录。
    Interest,
    /// 调整分录。
    Adjustment,
    /// 期初余额分录。
    Opening,
}

/// 账户分录相对账户余额的资金方向。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EntryDirection {
    /// 增加账户余额。
    Inflow,
    /// 减少账户余额。
    Outflow,
}

/// 新建交易中的一条原子账户分录。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewTransactionEntry {
    /// 发生额所属账户。
    pub account_id: String,
    /// 分录在交易中的业务角色。
    pub role: TransactionEntryRole,
    /// 发生额对账户余额的影响方向。
    pub direction: EntryDirection,
    /// 原币发生额；写入命令要求最小单位金额大于零。
    pub amount: MoneyAmount,
    /// 可选本币折算金额；缺少历史汇率时必须为空。
    pub base_amount: Option<MoneyAmount>,
    /// 可选历史汇率快照标识。
    pub fx_snapshot_id: Option<String>,
    /// 可选收支分类；普通转账分录可以为空。
    pub category_id: Option<String>,
    /// 分录级备注。
    pub memo: Option<String>,
}

/// 一次原子提交的新交易。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewTransaction {
    /// 目标账簿；仓储不得从全局状态隐式推断。
    pub ledger_id: String,
    /// 业务日期，格式为 `YYYY-MM-DD`。
    pub business_date: String,
    /// 实际发生时间，使用 ISO 8601 文本。
    pub occurred_at: String,
    /// 交易业务类型。
    pub kind: TransactionKind,
    /// 新交易的初始状态。
    pub status: NewTransactionStatus,
    /// 可选人员或机构标识。
    pub party_id: Option<String>,
    /// 可选交易主题。
    pub theme: Option<String>,
    /// 可选交易说明。
    pub description: Option<String>,
    /// 按稳定顺序写入的全部原子账户分录。
    pub entries: Vec<NewTransactionEntry>,
    /// 关联标签标识；同一交易内不得重复。
    pub tag_ids: Vec<String>,
    /// 已存在附件标识；文件落盘和哈希校验在附件服务完成。
    pub attachment_ids: Vec<String>,
}

/// 新交易在进入仓储前发现的业务输入错误。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TransactionValidationError {
    /// 未指定目标账簿。
    MissingLedgerId,
    /// 未指定业务日期。
    MissingBusinessDate,
    /// 未指定实际发生时间。
    MissingOccurredAt,
    /// 扩展领域类型键为空。
    MissingDomainSpecificKind,
    /// 交易没有任何原子账户分录。
    MissingEntries,
    /// 指定分录缺少账户标识。
    MissingAccountId {
        /// 从零开始的分录位置。
        entry_index: usize,
    },
    /// 指定分录金额不是正数。
    NonPositiveAmount {
        /// 从零开始的分录位置。
        entry_index: usize,
    },
    /// 指定分录缺少原币代码。
    MissingCurrencyCode {
        /// 从零开始的分录位置。
        entry_index: usize,
    },
    /// 指定分录的本币折算金额不是正数。
    NonPositiveBaseAmount {
        /// 从零开始的分录位置。
        entry_index: usize,
    },
    /// 指定分录的本币折算金额缺少币种代码。
    MissingBaseCurrencyCode {
        /// 从零开始的分录位置。
        entry_index: usize,
    },
    /// 收入交易缺少流入分录。
    IncomeRequiresInflow,
    /// 支出交易缺少流出分录。
    ExpenseRequiresOutflow,
    /// 转账交易缺少流入或流出分录。
    TransferRequiresBothDirections,
    /// 同一交易重复关联标签。
    DuplicateTagId(String),
    /// 同一交易重复关联附件。
    DuplicateAttachmentId(String),
}

impl NewTransaction {
    /// 校验 SQLite 写入前能够确认的结构和方向规则。
    ///
    /// 跨币种换算、投资成本和旧程序金额守恒口径仍待样例校准，因此不在这里猜测。
    pub fn validate(&self) -> Result<(), Vec<TransactionValidationError>> {
        let mut errors = Vec::new();

        if self.ledger_id.trim().is_empty() {
            errors.push(TransactionValidationError::MissingLedgerId);
        }
        if self.business_date.trim().is_empty() {
            errors.push(TransactionValidationError::MissingBusinessDate);
        }
        if self.occurred_at.trim().is_empty() {
            errors.push(TransactionValidationError::MissingOccurredAt);
        }
        if matches!(&self.kind, TransactionKind::DomainSpecific(value) if value.trim().is_empty()) {
            errors.push(TransactionValidationError::MissingDomainSpecificKind);
        }
        if self.entries.is_empty() {
            errors.push(TransactionValidationError::MissingEntries);
        }

        for (entry_index, entry) in self.entries.iter().enumerate() {
            if entry.account_id.trim().is_empty() {
                errors.push(TransactionValidationError::MissingAccountId { entry_index });
            }
            if entry.amount.minor_units <= 0 {
                errors.push(TransactionValidationError::NonPositiveAmount { entry_index });
            }
            if entry.amount.currency_code.trim().is_empty() {
                errors.push(TransactionValidationError::MissingCurrencyCode { entry_index });
            }
            if let Some(base_amount) = &entry.base_amount {
                if base_amount.minor_units <= 0 {
                    errors.push(TransactionValidationError::NonPositiveBaseAmount { entry_index });
                }
                if base_amount.currency_code.trim().is_empty() {
                    errors
                        .push(TransactionValidationError::MissingBaseCurrencyCode { entry_index });
                }
            }
        }

        let has_inflow = self
            .entries
            .iter()
            .any(|entry| entry.direction == EntryDirection::Inflow);
        let has_outflow = self
            .entries
            .iter()
            .any(|entry| entry.direction == EntryDirection::Outflow);

        match &self.kind {
            TransactionKind::Income if !has_inflow => {
                errors.push(TransactionValidationError::IncomeRequiresInflow);
            }
            TransactionKind::Expense if !has_outflow => {
                errors.push(TransactionValidationError::ExpenseRequiresOutflow);
            }
            TransactionKind::Transfer if !(has_inflow && has_outflow) => {
                errors.push(TransactionValidationError::TransferRequiresBothDirections);
            }
            _ => {}
        }

        collect_duplicate_ids(
            &self.tag_ids,
            &mut errors,
            TransactionValidationError::DuplicateTagId,
        );
        collect_duplicate_ids(
            &self.attachment_ids,
            &mut errors,
            TransactionValidationError::DuplicateAttachmentId,
        );

        if errors.is_empty() {
            Ok(())
        } else {
            Err(errors)
        }
    }
}

fn collect_duplicate_ids(
    ids: &[String],
    errors: &mut Vec<TransactionValidationError>,
    duplicate_error: impl Fn(String) -> TransactionValidationError,
) {
    let mut seen = HashSet::new();
    for id in ids {
        if !seen.insert(id) {
            errors.push(duplicate_error(id.clone()));
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn entry(direction: EntryDirection, role: TransactionEntryRole) -> NewTransactionEntry {
        NewTransactionEntry {
            account_id: "account-1".to_owned(),
            role,
            direction,
            amount: MoneyAmount::new(10_000, "CNY"),
            base_amount: Some(MoneyAmount::new(10_000, "CNY")),
            fx_snapshot_id: None,
            category_id: None,
            memo: None,
        }
    }

    fn transaction(kind: TransactionKind, entries: Vec<NewTransactionEntry>) -> NewTransaction {
        NewTransaction {
            ledger_id: "ledger-1".to_owned(),
            business_date: "2026-07-28".to_owned(),
            occurred_at: "2026-07-28T10:00:00+08:00".to_owned(),
            kind,
            status: NewTransactionStatus::Posted,
            party_id: None,
            theme: None,
            description: None,
            entries,
            tag_ids: Vec::new(),
            attachment_ids: Vec::new(),
        }
    }

    #[test]
    fn accepts_transfer_with_fee_as_one_business_command() {
        let transfer = transaction(
            TransactionKind::Transfer,
            vec![
                entry(EntryDirection::Outflow, TransactionEntryRole::Primary),
                entry(EntryDirection::Inflow, TransactionEntryRole::Counterparty),
                entry(EntryDirection::Outflow, TransactionEntryRole::Fee),
            ],
        );

        assert_eq!(transfer.validate(), Ok(()));
    }

    #[test]
    fn rejects_transfer_without_both_directions() {
        let transfer = transaction(
            TransactionKind::Transfer,
            vec![entry(
                EntryDirection::Outflow,
                TransactionEntryRole::Primary,
            )],
        );

        assert!(transfer
            .validate()
            .unwrap_err()
            .contains(&TransactionValidationError::TransferRequiresBothDirections));
    }

    #[test]
    fn rejects_duplicate_tag_ids_before_sqlite_primary_key_failure() {
        let mut income = transaction(
            TransactionKind::Income,
            vec![entry(EntryDirection::Inflow, TransactionEntryRole::Primary)],
        );
        income.tag_ids = vec!["tag-1".to_owned(), "tag-1".to_owned()];

        assert!(income.validate().unwrap_err().contains(
            &TransactionValidationError::DuplicateTagId("tag-1".to_owned())
        ));
    }
}
