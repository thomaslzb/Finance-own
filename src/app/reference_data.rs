use crate::domain::reference_data::{
    AccountGroupRecord, AccountRecord, CategoryDirection, CategoryRecord, LedgerRecord,
    PartyBirthday, PartyKind, PartyRecord, PersonSex, TagRecord,
};

/// 新账簿的本位币定义。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewCurrency {
    /// 币种代码，例如 `CNY`；允许兼容旧账簿中的自定义代码。
    pub code: String,
    /// 币种显示名称。
    pub name: String,
    /// 最小单位小数位，必须在 `0..=8` 范围内。
    pub minor_unit: u8,
}

/// 新账簿的首个账户定义。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InitialAccount {
    /// 账户显示名称。
    pub name: String,
    /// 账户类型键，例如 `cash` 或 `credit_card`。
    pub kind: String,
    /// `true` 表示资产账户，`false` 表示负债账户。
    pub is_asset: bool,
}

/// 创建可立即记账的新账簿所需输入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InitializeLedgerRequest {
    /// 账簿显示名称。
    pub name: String,
    /// 账簿本位币及精度。
    pub base_currency: NewCurrency,
    /// 首个账户；与账簿同事务创建，避免产生不可用空账簿。
    pub initial_account: InitialAccount,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
}

/// 新账簿初始化结果。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InitializedLedger {
    /// 新账簿标识。
    pub ledger_id: String,
    /// 同事务创建的首个账户标识。
    pub initial_account_id: String,
}

/// 新账户组输入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewAccountGroup {
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 可选父组标识。
    pub parent_id: Option<String>,
    /// 账户组显示名称。
    pub name: String,
    /// 分组类型键。
    pub kind: String,
    /// 同级排序值。
    pub sort_order: i64,
}

/// 账户组可编辑资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AccountGroupChanges {
    /// 账户组稳定标识。
    pub id: String,
    /// 所属账簿标识，防止跨账簿误更新。
    pub ledger_id: String,
    /// 新父组标识；为空表示移动到根级。
    pub parent_id: Option<String>,
    /// 新显示名称。
    pub name: String,
    /// 新分组类型键。
    pub kind: String,
    /// 新排序值。
    pub sort_order: i64,
}

/// 删除账户组后的关系迁移结果。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeletedAccountGroup {
    /// 被删除的账户组标识。
    pub group_id: String,
    /// 迁移到父级或根级的直属账户数量。
    pub reassigned_accounts: usize,
    /// 迁移到父级或根级的直属子组数量。
    pub reassigned_child_groups: usize,
}

/// 新账户输入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewAccount {
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 可选账户组标识。
    pub group_id: Option<String>,
    /// 账户显示名称。
    pub name: String,
    /// 账户类型键。
    pub kind: String,
    /// 账户币种代码。
    pub currency_code: String,
    /// 可选金融机构名称。
    pub institution_name: Option<String>,
    /// 脱敏后的账号或卡号。
    pub account_number_masked: Option<String>,
    /// 资产或负债口径。
    pub is_asset: bool,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
}

/// 账户可编辑资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AccountChanges {
    /// 账户稳定标识。
    pub id: String,
    /// 所属账簿标识，防止跨账簿误更新。
    pub ledger_id: String,
    /// 可选账户组标识。
    pub group_id: Option<String>,
    /// 新显示名称。
    pub name: String,
    /// 新账户类型键。
    pub kind: String,
    /// 新金融机构名称。
    pub institution_name: Option<String>,
    /// 新脱敏账号或卡号。
    pub account_number_masked: Option<String>,
    /// 是否在常规账户列表隐藏。
    pub is_hidden: bool,
    /// 可选关闭日期；清空表示重新启用。
    pub closed_on: Option<String>,
}

/// 新分类输入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewCategory {
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 可选父分类标识。
    pub parent_id: Option<String>,
    /// 分类显示名称。
    pub name: String,
    /// 分类适用方向。
    pub direction: CategoryDirection,
    /// 同级排序值。
    pub sort_order: i64,
}

/// 分类可编辑资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CategoryChanges {
    /// 分类稳定标识。
    pub id: String,
    /// 所属账簿标识，防止跨账簿误更新。
    pub ledger_id: String,
    /// 可选父分类标识。
    pub parent_id: Option<String>,
    /// 新显示名称。
    pub name: String,
    /// 新适用方向。
    pub direction: CategoryDirection,
    /// 新排序值。
    pub sort_order: i64,
    /// 是否归档。
    pub is_archived: bool,
}

/// 新标签输入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewTag {
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 标签显示名称。
    pub name: String,
    /// 可选颜色值。
    pub color: Option<String>,
}

/// 标签可编辑资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TagChanges {
    /// 标签稳定标识。
    pub id: String,
    /// 所属账簿标识，防止跨账簿误更新。
    pub ledger_id: String,
    /// 新显示名称。
    pub name: String,
    /// 新颜色值。
    pub color: Option<String>,
    /// 是否归档。
    pub is_archived: bool,
}

/// 新往来方输入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewParty {
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 往来方显示名称。
    pub name: String,
    /// 往来方类型。
    pub kind: PartyKind,
    /// 可选联系方式，旧版运行态上限为 20 个字符。
    pub contact: Option<String>,
    /// 可选地址，旧版运行态上限为 40 个字符。
    pub address: Option<String>,
    /// 人员性别；机构必须为空。
    pub sex: Option<PersonSex>,
    /// 可选生日，保留公历或农历及原始年月日分量。
    pub birthday: Option<PartyBirthday>,
}

/// 往来方可编辑资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PartyChanges {
    /// 往来方稳定标识。
    pub id: String,
    /// 所属账簿标识，防止跨账簿误更新。
    pub ledger_id: String,
    /// 新显示名称。
    pub name: String,
    /// 新往来方类型。
    pub kind: PartyKind,
    /// 新联系方式。
    pub contact: Option<String>,
    /// 新地址。
    pub address: Option<String>,
    /// 新人员性别；机构必须为空。
    pub sex: Option<PersonSex>,
    /// 新生日；机构必须为空。
    pub birthday: Option<PartyBirthday>,
    /// 是否隐藏；隐藏后默认列表排除，但名称仍保持账簿级唯一。
    pub is_hidden: bool,
}

/// 基础资料读写失败。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReferenceDataError {
    /// 输入缺少必填值或超出明确边界。
    InvalidInput(String),
    /// 指定对象不存在或不属于目标账簿。
    NotFound(String),
    /// 唯一键、外键或并发状态发生冲突。
    Conflict(String),
    /// 本地数据库操作失败；消息不得包含密钥或完整敏感路径。
    Storage(String),
}

/// 账簿初始化与基础资料仓储端口。
///
/// 分类和标签通过归档保留历史引用；人员与机构通过隐藏保留历史引用；账户通过隐藏和关闭保留流水。
pub trait ReferenceDataRepository {
    /// 原子创建币种、账簿和首个账户。
    fn initialize_ledger(
        &mut self,
        request: &InitializeLedgerRequest,
    ) -> Result<InitializedLedger, ReferenceDataError>;

    /// 读取账簿基础信息。
    fn get_ledger(&self, ledger_id: &str) -> Result<LedgerRecord, ReferenceDataError>;

    /// 创建账户组并返回稳定标识。
    fn create_account_group(
        &mut self,
        group: &NewAccountGroup,
    ) -> Result<String, ReferenceDataError>;

    /// 更新账户组资料；实现必须拒绝跨账簿父组和循环父子关系。
    fn update_account_group(
        &mut self,
        changes: &AccountGroupChanges,
    ) -> Result<(), ReferenceDataError>;

    /// 查询账簿全部账户组。
    fn list_account_groups(
        &self,
        ledger_id: &str,
    ) -> Result<Vec<AccountGroupRecord>, ReferenceDataError>;

    /// 删除账户组并把直属账户和子组迁移到其父级，绝不删除账户和交易。
    fn delete_account_group(
        &mut self,
        ledger_id: &str,
        group_id: &str,
    ) -> Result<DeletedAccountGroup, ReferenceDataError>;

    /// 创建账户并返回稳定标识。
    fn create_account(&mut self, account: &NewAccount) -> Result<String, ReferenceDataError>;

    /// 更新账户资料和停用状态；账户币种不允许在此入口变更。
    fn update_account(&mut self, changes: &AccountChanges) -> Result<(), ReferenceDataError>;

    /// 查询账簿全部账户，包含隐藏和已关闭账户。
    fn list_accounts(&self, ledger_id: &str) -> Result<Vec<AccountRecord>, ReferenceDataError>;

    /// 创建分类并返回稳定标识。
    fn create_category(&mut self, category: &NewCategory) -> Result<String, ReferenceDataError>;

    /// 更新分类资料和归档状态。
    fn update_category(&mut self, changes: &CategoryChanges) -> Result<(), ReferenceDataError>;

    /// 查询账簿全部分类，包含归档分类。
    fn list_categories(&self, ledger_id: &str) -> Result<Vec<CategoryRecord>, ReferenceDataError>;

    /// 创建标签并返回稳定标识。
    fn create_tag(&mut self, tag: &NewTag) -> Result<String, ReferenceDataError>;

    /// 更新标签资料和归档状态。
    fn update_tag(&mut self, changes: &TagChanges) -> Result<(), ReferenceDataError>;

    /// 查询账簿全部标签，包含归档标签。
    fn list_tags(&self, ledger_id: &str) -> Result<Vec<TagRecord>, ReferenceDataError>;

    /// 创建往来方并返回稳定标识。
    fn create_party(&mut self, party: &NewParty) -> Result<String, ReferenceDataError>;

    /// 更新往来方资料和隐藏状态。
    fn update_party(&mut self, changes: &PartyChanges) -> Result<(), ReferenceDataError>;

    /// 查询账簿全部往来方，包含隐藏往来方。
    fn list_parties(&self, ledger_id: &str) -> Result<Vec<PartyRecord>, ReferenceDataError>;
}

/// 校验新账簿输入后调用仓储，避免产生没有首个账户的空账簿。
pub fn initialize_ledger(
    repository: &mut impl ReferenceDataRepository,
    request: &InitializeLedgerRequest,
) -> Result<InitializedLedger, ReferenceDataError> {
    validate_name(&request.name, "账簿名称")?;
    validate_name(&request.base_currency.code, "币种代码")?;
    validate_name(&request.base_currency.name, "币种名称")?;
    if request.base_currency.minor_unit > 8 {
        return Err(ReferenceDataError::InvalidInput(
            "币种最小单位小数位必须在 0 到 8 之间".to_owned(),
        ));
    }
    validate_name(&request.initial_account.name, "初始账户名称")?;
    validate_name(&request.initial_account.kind, "初始账户类型")?;
    validate_name(&request.created_at, "创建时间")?;
    repository.initialize_ledger(request)
}

fn validate_name(value: &str, label: &str) -> Result<(), ReferenceDataError> {
    if value.trim().is_empty() {
        return Err(ReferenceDataError::InvalidInput(format!("{label}不能为空")));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    struct RejectingRepository {
        calls: usize,
    }

    impl ReferenceDataRepository for RejectingRepository {
        fn initialize_ledger(
            &mut self,
            _request: &InitializeLedgerRequest,
        ) -> Result<InitializedLedger, ReferenceDataError> {
            self.calls += 1;
            unreachable!("无效输入不应进入仓储")
        }

        fn get_ledger(&self, _ledger_id: &str) -> Result<LedgerRecord, ReferenceDataError> {
            unreachable!()
        }

        fn create_account_group(
            &mut self,
            _group: &NewAccountGroup,
        ) -> Result<String, ReferenceDataError> {
            unreachable!()
        }

        fn update_account_group(
            &mut self,
            _changes: &AccountGroupChanges,
        ) -> Result<(), ReferenceDataError> {
            unreachable!()
        }

        fn list_account_groups(
            &self,
            _ledger_id: &str,
        ) -> Result<Vec<AccountGroupRecord>, ReferenceDataError> {
            unreachable!()
        }

        fn delete_account_group(
            &mut self,
            _ledger_id: &str,
            _group_id: &str,
        ) -> Result<DeletedAccountGroup, ReferenceDataError> {
            unreachable!()
        }

        fn create_account(&mut self, _account: &NewAccount) -> Result<String, ReferenceDataError> {
            unreachable!()
        }

        fn update_account(&mut self, _changes: &AccountChanges) -> Result<(), ReferenceDataError> {
            unreachable!()
        }

        fn list_accounts(
            &self,
            _ledger_id: &str,
        ) -> Result<Vec<AccountRecord>, ReferenceDataError> {
            unreachable!()
        }

        fn create_category(
            &mut self,
            _category: &NewCategory,
        ) -> Result<String, ReferenceDataError> {
            unreachable!()
        }

        fn update_category(
            &mut self,
            _changes: &CategoryChanges,
        ) -> Result<(), ReferenceDataError> {
            unreachable!()
        }

        fn list_categories(
            &self,
            _ledger_id: &str,
        ) -> Result<Vec<CategoryRecord>, ReferenceDataError> {
            unreachable!()
        }

        fn create_tag(&mut self, _tag: &NewTag) -> Result<String, ReferenceDataError> {
            unreachable!()
        }

        fn update_tag(&mut self, _changes: &TagChanges) -> Result<(), ReferenceDataError> {
            unreachable!()
        }

        fn list_tags(&self, _ledger_id: &str) -> Result<Vec<TagRecord>, ReferenceDataError> {
            unreachable!()
        }

        fn create_party(&mut self, _party: &NewParty) -> Result<String, ReferenceDataError> {
            unreachable!()
        }

        fn update_party(&mut self, _changes: &PartyChanges) -> Result<(), ReferenceDataError> {
            unreachable!()
        }

        fn list_parties(&self, _ledger_id: &str) -> Result<Vec<PartyRecord>, ReferenceDataError> {
            unreachable!()
        }
    }

    #[test]
    fn rejects_invalid_ledger_before_calling_repository() {
        let mut repository = RejectingRepository { calls: 0 };
        let request = InitializeLedgerRequest {
            name: " ".to_owned(),
            base_currency: NewCurrency {
                code: "CNY".to_owned(),
                name: "人民币".to_owned(),
                minor_unit: 2,
            },
            initial_account: InitialAccount {
                name: "现金".to_owned(),
                kind: "cash".to_owned(),
                is_asset: true,
            },
            created_at: "2026-07-29T00:00:00+08:00".to_owned(),
        };

        let error = initialize_ledger(&mut repository, &request).unwrap_err();

        assert!(matches!(error, ReferenceDataError::InvalidInput(_)));
        assert_eq!(repository.calls, 0);
    }
}
