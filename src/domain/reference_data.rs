/// 账簿基础信息。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LedgerRecord {
    /// 账簿稳定标识。
    pub id: String,
    /// 账簿显示名称。
    pub name: String,
    /// 本位币代码，对应 `currencies.code`。
    pub base_currency_code: String,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
    /// 最近更新时间，使用带时区的 ISO 8601 文本。
    pub updated_at: String,
}

/// 账户树中的分组节点。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AccountGroupRecord {
    /// 账户组稳定标识。
    pub id: String,
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 可选父组标识；为空表示根组。
    pub parent_id: Option<String>,
    /// 账户组显示名称。
    pub name: String,
    /// 分组类型键，用于区分资产、负债或自定义分组口径。
    pub kind: String,
    /// 同级排序值，数值较小者优先。
    pub sort_order: i64,
}

/// 账户资料及其停用状态。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AccountRecord {
    /// 账户稳定标识。
    pub id: String,
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 可选账户组；删除账户组时只解除或迁移该关系。
    pub group_id: Option<String>,
    /// 账户显示名称，在同一账簿内唯一。
    pub name: String,
    /// 账户类型键，保留旧软件多账户类型的扩展能力。
    pub kind: String,
    /// 账户币种代码。
    pub currency_code: String,
    /// 可选金融机构名称。
    pub institution_name: Option<String>,
    /// 脱敏后的账号或卡号，不保存完整敏感号码。
    pub account_number_masked: Option<String>,
    /// `true` 表示资产账户，`false` 表示负债账户。
    pub is_asset: bool,
    /// 隐藏账户仍保留历史交易和报表追溯能力。
    pub is_hidden: bool,
    /// 可选关闭日期，格式为 `YYYY-MM-DD`。
    pub closed_on: Option<String>,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
}

/// 分类适用的收支方向。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CategoryDirection {
    /// 仅用于收入分录。
    Income,
    /// 仅用于支出分录。
    Expense,
    /// 可用于收入和支出分录。
    Both,
}

/// 收支分类资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CategoryRecord {
    /// 分类稳定标识。
    pub id: String,
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 可选父分类标识。
    pub parent_id: Option<String>,
    /// 分类显示名称。
    pub name: String,
    /// 分类适用方向。
    pub direction: CategoryDirection,
    /// 同级分类排序值，数值较小者优先。
    pub sort_order: i64,
    /// 归档分类不能用于新录入，但历史分录继续显示。
    pub is_archived: bool,
}

/// 标签资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TagRecord {
    /// 标签稳定标识。
    pub id: String,
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 标签显示名称，在同一账簿内唯一。
    pub name: String,
    /// 可选颜色值，由 UI 解释，不影响账务计算。
    pub color: Option<String>,
    /// 归档标签不能用于新关联，但历史关联继续显示。
    pub is_archived: bool,
}

/// 人员与机构类型，对应旧版资料管理中的三个独立分类。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PartyKind {
    /// 家庭成员，可作为账户所有者或家庭关系主体。
    FamilyMember,
    /// 家庭外的自然人往来对象。
    ContactPerson,
    /// 银行、公司或其他组织机构。
    Institution,
}

/// 人员性别；机构不使用该字段。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PersonSex {
    /// 男性。
    Male,
    /// 女性。
    Female,
}

/// 生日录入所使用的历法。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BirthdayCalendar {
    /// 公历日期。
    Gregorian,
    /// 农历日期；年月日按用户录入分量保存，不隐式换算为公历。
    Lunar,
}

/// 人员生日分量。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PartyBirthday {
    /// 生日历法。
    pub calendar: BirthdayCalendar,
    /// 年份。
    pub year: u16,
    /// 月份，公历和农历均使用 `1..=12`。
    pub month: u8,
    /// 日期，公历按真实月份校验，农历使用 `1..=30`。
    pub day: u8,
}

/// 交易往来方资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PartyRecord {
    /// 往来方稳定标识。
    pub id: String,
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 往来方显示名称。
    pub name: String,
    /// 往来方类型。
    pub kind: PartyKind,
    /// 可选联系方式；空白值应在命令边界转换为 `None`。
    pub contact: Option<String>,
    /// 可选地址；空白值应在命令边界转换为 `None`。
    pub address: Option<String>,
    /// 人员性别；机构必须为 `None`。
    pub sex: Option<PersonSex>,
    /// 可选生日；机构必须为 `None`。
    pub birthday: Option<PartyBirthday>,
    /// 隐藏往来方默认不进入候选列表，但历史交易和“显示隐藏”视图继续显示。
    pub is_hidden: bool,
}
