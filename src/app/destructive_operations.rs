/// 需要影响预览和用户确认的破坏性操作。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DestructiveOperation {
    /// 删除账户及其关联交易、转账和计划。
    DeleteAccount { account_id: String },
    /// 删除账户组；只解除账户归属，不删除账户。
    DeleteAccountGroup { account_group_id: String },
    /// 删除收支分类；存在交易引用或子分类时应阻止或先迁移。
    DeleteCategory { category_id: String },
    /// 删除人员或机构；存在业务引用时应阻止或改为停用。
    DeleteParty { party_id: String },
    /// 删除币种；本币或已使用币种不得删除。
    DeleteCurrency { currency_code: String },
    /// 删除附件内容；仍有业务引用时不得执行。
    DeleteAttachment { attachment_id: String },
    /// 批量删除稳定交易标识集合。
    DeleteTransactions { transaction_ids: Vec<String> },
}

/// 破坏性操作提交前展示给用户的影响范围。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DestructiveImpactPreview {
    /// 本次预览对应的操作，提交时必须保持一致。
    pub operation: DestructiveOperation,
    /// 受影响的交易数量。
    pub transaction_count: u64,
    /// 受影响的跨账户转账数量。
    pub transfer_count: u64,
    /// 受影响的计划、提醒或目标数量。
    pub plan_count: u64,
    /// 将解除的分组、标签、附件或其它关系数量。
    pub relation_count: u64,
    /// 阻止执行的业务原因；非空时不能提交。
    pub blockers: Vec<String>,
    /// 防止预览后数据变化的仓储修订标记。
    pub revision_token: String,
}

/// 破坏性操作成功后的可审计结果。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DestructiveOperationResult {
    /// 实际删除的业务对象数量。
    pub deleted_object_count: u64,
    /// 实际解除的关系数量。
    pub detached_relation_count: u64,
    /// 实际删除或作废的交易数量。
    pub affected_transaction_count: u64,
}

/// 破坏性操作失败。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DestructiveOperationError {
    /// 操作被业务引用、本币保护或其它规则阻止。
    Blocked(Vec<String>),
    /// 确认的预览不属于当前操作。
    PreviewMismatch,
    /// 预览后数据发生变化，需要重新展示影响范围。
    StalePreview,
    /// 本地事务或文件操作失败；消息不得包含密钥或完整敏感路径。
    Storage(String),
}

/// 破坏性操作仓储端口。
///
/// 实现必须在同一事务中重新校验修订标记并执行全部删除、作废或解除关系动作。
pub trait DestructiveOperationRepository {
    /// 只读计算影响范围，不得修改业务数据。
    fn preview(
        &self,
        operation: &DestructiveOperation,
    ) -> Result<DestructiveImpactPreview, DestructiveOperationError>;

    /// 使用用户确认过的修订标记原子执行操作。
    fn execute(
        &mut self,
        operation: &DestructiveOperation,
        expected_revision_token: &str,
    ) -> Result<DestructiveOperationResult, DestructiveOperationError>;
}

/// 获取可展示的破坏性操作影响预览。
pub fn preview_destructive_operation(
    repository: &impl DestructiveOperationRepository,
    operation: &DestructiveOperation,
) -> Result<DestructiveImpactPreview, DestructiveOperationError> {
    repository.preview(operation)
}

/// 提交用户已经确认且未被业务规则阻止的破坏性操作。
pub fn execute_confirmed_destructive_operation(
    repository: &mut impl DestructiveOperationRepository,
    operation: &DestructiveOperation,
    confirmed_preview: &DestructiveImpactPreview,
) -> Result<DestructiveOperationResult, DestructiveOperationError> {
    if &confirmed_preview.operation != operation {
        return Err(DestructiveOperationError::PreviewMismatch);
    }
    if !confirmed_preview.blockers.is_empty() {
        return Err(DestructiveOperationError::Blocked(
            confirmed_preview.blockers.clone(),
        ));
    }
    repository.execute(operation, &confirmed_preview.revision_token)
}

#[cfg(test)]
mod tests {
    use super::*;

    struct RecordingRepository {
        execute_calls: usize,
    }

    impl DestructiveOperationRepository for RecordingRepository {
        fn preview(
            &self,
            operation: &DestructiveOperation,
        ) -> Result<DestructiveImpactPreview, DestructiveOperationError> {
            Ok(DestructiveImpactPreview {
                operation: operation.clone(),
                transaction_count: 2,
                transfer_count: 1,
                plan_count: 1,
                relation_count: 0,
                blockers: Vec::new(),
                revision_token: "revision-1".to_owned(),
            })
        }

        fn execute(
            &mut self,
            _operation: &DestructiveOperation,
            expected_revision_token: &str,
        ) -> Result<DestructiveOperationResult, DestructiveOperationError> {
            assert_eq!(expected_revision_token, "revision-1");
            self.execute_calls += 1;
            Ok(DestructiveOperationResult {
                deleted_object_count: 1,
                detached_relation_count: 0,
                affected_transaction_count: 2,
            })
        }
    }

    #[test]
    fn blocks_execution_when_preview_contains_business_blockers() {
        let operation = DestructiveOperation::DeleteCurrency {
            currency_code: "CNY".to_owned(),
        };
        let preview = DestructiveImpactPreview {
            operation: operation.clone(),
            transaction_count: 0,
            transfer_count: 0,
            plan_count: 0,
            relation_count: 0,
            blockers: vec!["本币不能删除".to_owned()],
            revision_token: "revision-1".to_owned(),
        };
        let mut repository = RecordingRepository { execute_calls: 0 };

        let result = execute_confirmed_destructive_operation(&mut repository, &operation, &preview);

        assert!(matches!(result, Err(DestructiveOperationError::Blocked(_))));
        assert_eq!(repository.execute_calls, 0);
    }

    #[test]
    fn executes_once_with_the_confirmed_revision() {
        let operation = DestructiveOperation::DeleteAccount {
            account_id: "account-1".to_owned(),
        };
        let mut repository = RecordingRepository { execute_calls: 0 };
        let preview = preview_destructive_operation(&repository, &operation).unwrap();

        let result =
            execute_confirmed_destructive_operation(&mut repository, &operation, &preview).unwrap();

        assert_eq!(result.affected_transaction_count, 2);
        assert_eq!(repository.execute_calls, 1);
    }
}
