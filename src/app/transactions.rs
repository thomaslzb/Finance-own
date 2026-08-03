use crate::domain::transactions::{NewTransaction, TransactionValidationError};

/// 成功写入后返回给应用层的稳定标识和账簿内顺序。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CreatedTransaction {
    /// 新交易标识。
    pub transaction_id: String,
    /// 仓储在同一 SQLite 事务中分配的账簿内单调递增序号。
    pub sequence_no: i64,
}

/// 通用交易写入失败。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TransactionWriteError {
    /// 应用层输入未满足已确认的交易结构规则。
    InvalidInput(Vec<TransactionValidationError>),
    /// 账户、标签、附件或序号等数据发生并发冲突。
    Conflict(String),
    /// 本地数据库事务失败；消息不得包含密钥或完整敏感路径。
    Storage(String),
}

/// 通用交易原子写入端口。
///
/// 实现必须在一个 SQLite 事务中分配 `sequence_no`，并写入交易头、全部账户分录、
/// 标签和附件关系。任一步失败都必须整体回滚，且不得直接更新余额或报表投影。
pub trait TransactionWriteRepository {
    /// 原子创建一笔已通过应用层校验的交易。
    fn create_transaction(
        &mut self,
        transaction: &NewTransaction,
    ) -> Result<CreatedTransaction, TransactionWriteError>;
}

/// 校验并提交一笔通用交易。
///
/// 该入口确保所有 UI、导入和计划执行流程共享同一套最低业务校验。
pub fn create_transaction(
    repository: &mut impl TransactionWriteRepository,
    transaction: &NewTransaction,
) -> Result<CreatedTransaction, TransactionWriteError> {
    transaction
        .validate()
        .map_err(TransactionWriteError::InvalidInput)?;
    repository.create_transaction(transaction)
}

#[cfg(test)]
mod tests {
    use crate::domain::{
        money::MoneyAmount,
        transactions::{
            EntryDirection, NewTransactionEntry, NewTransactionStatus, TransactionEntryRole,
            TransactionKind,
        },
    };

    use super::*;

    struct RecordingRepository {
        calls: usize,
    }

    impl TransactionWriteRepository for RecordingRepository {
        fn create_transaction(
            &mut self,
            _transaction: &NewTransaction,
        ) -> Result<CreatedTransaction, TransactionWriteError> {
            self.calls += 1;
            Ok(CreatedTransaction {
                transaction_id: "transaction-1".to_owned(),
                sequence_no: 1,
            })
        }
    }

    fn valid_income() -> NewTransaction {
        NewTransaction {
            ledger_id: "ledger-1".to_owned(),
            business_date: "2026-07-28".to_owned(),
            occurred_at: "2026-07-28T10:00:00+08:00".to_owned(),
            kind: TransactionKind::Income,
            status: NewTransactionStatus::Posted,
            party_id: None,
            theme: None,
            description: None,
            entries: vec![NewTransactionEntry {
                account_id: "account-1".to_owned(),
                role: TransactionEntryRole::Primary,
                direction: EntryDirection::Inflow,
                amount: MoneyAmount::new(10_000, "CNY"),
                base_amount: Some(MoneyAmount::new(10_000, "CNY")),
                fx_snapshot_id: None,
                category_id: Some("salary".to_owned()),
                memo: None,
            }],
            tag_ids: Vec::new(),
            attachment_ids: Vec::new(),
        }
    }

    #[test]
    fn validates_before_calling_repository() {
        let mut repository = RecordingRepository { calls: 0 };
        let mut invalid = valid_income();
        invalid.entries.clear();

        let result = create_transaction(&mut repository, &invalid);

        assert!(matches!(
            result,
            Err(TransactionWriteError::InvalidInput(_))
        ));
        assert_eq!(repository.calls, 0);
    }

    #[test]
    fn forwards_valid_transaction_once() {
        let mut repository = RecordingRepository { calls: 0 };

        let created = create_transaction(&mut repository, &valid_income()).unwrap();

        assert_eq!(created.sequence_no, 1);
        assert_eq!(repository.calls, 1);
    }
}
