/// 预算周期类型。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BudgetPeriodKind {
    /// 月度预算。
    Monthly,
    /// 季度预算。
    Quarterly,
    /// 年度预算。
    Yearly,
    /// 自定义起止日期预算。
    Custom,
}

/// 预算生命周期状态。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BudgetStatus {
    /// 草稿预算，不进入正式提醒或消耗分析。
    Draft,
    /// 生效预算，可参与消耗查询。
    Active,
    /// 已关闭预算，保留历史追溯但不再更新。
    Closed,
}

/// 预算结转方式。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BudgetRolloverMode {
    /// 不结转剩余额度。
    None,
    /// 只结转正向剩余额度。
    Positive,
    /// 正负差额都结转。
    All,
}

/// 预算主体记录。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BudgetRecord {
    /// 预算稳定标识。
    pub id: String,
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 预算显示名称。
    pub name: String,
    /// 预算周期类型。
    pub period_kind: BudgetPeriodKind,
    /// 预算开始日期，格式为 `YYYY-MM-DD`。
    pub start_date: String,
    /// 预算结束日期，格式为 `YYYY-MM-DD`。
    pub end_date: String,
    /// 预算生命周期状态。
    pub status: BudgetStatus,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
    /// 最近更新时间，使用带时区的 ISO 8601 文本。
    pub updated_at: String,
}

/// 预算分类额度记录。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BudgetItemRecord {
    /// 预算项稳定标识。
    pub id: String,
    /// 所属预算标识。
    pub budget_id: String,
    /// 预算约束的分类标识。
    pub category_id: String,
    /// 本预算项覆盖的开始日期。
    pub period_start: String,
    /// 本预算项覆盖的结束日期。
    pub period_end: String,
    /// 预算金额，使用币种最小单位，必须非负。
    pub amount_minor: i64,
    /// 预算金额币种代码。
    pub currency_code: String,
    /// 超支或剩余额度结转规则。
    pub rollover_mode: BudgetRolloverMode,
    /// 预算项备注；为空表示没有补充说明。
    pub note: Option<String>,
}

/// 财务目标进度计算口径。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FinancialGoalProgressMode {
    /// 使用关联账户余额计算进度。
    Balance,
    /// 使用投资市值计算进度。
    MarketValue,
    /// 使用净资产口径计算进度。
    NetAsset,
    /// 使用后续策略服务定义的自定义口径。
    Custom,
}

/// 财务目标生命周期状态。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FinancialGoalStatus {
    /// 目标正在进行。
    Active,
    /// 目标已经完成。
    Completed,
    /// 目标已取消，保留历史追溯。
    Cancelled,
}

/// 财务目标账户范围。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FinancialGoalAccountScopeMode {
    /// 使用账簿全部账户作为进度输入。
    All,
    /// 只使用显式关联的账户作为进度输入。
    Selected,
}

/// 财务目标主体记录。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FinancialGoalRecord {
    /// 目标稳定标识。
    pub id: String,
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 目标显示名称。
    pub name: String,
    /// 目标金额，使用目标币种最小单位。
    pub target_amount_minor: i64,
    /// 目标币种代码。
    pub currency_code: String,
    /// 目标开始日期；为空表示未设置期间。
    pub start_date: Option<String>,
    /// 目标日期；为空表示未设置期间。
    pub target_date: Option<String>,
    /// 进度计算口径。
    pub progress_mode: FinancialGoalProgressMode,
    /// 目标生命周期状态。
    pub status: FinancialGoalStatus,
    /// 初始进度值；与捕获时间和输入快照必须同有同无。
    pub initial_value_minor: Option<i64>,
    /// 初始进度捕获时间。
    pub initial_value_captured_at: Option<String>,
    /// 初始进度输入快照 JSON。
    pub initial_inputs_json: Option<String>,
    /// 账户范围口径。
    pub account_scope_mode: FinancialGoalAccountScopeMode,
    /// 进度公式版本；为空表示使用当前默认公式。
    pub progress_formula_version: Option<String>,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
    /// 最近更新时间，使用带时区的 ISO 8601 文本。
    pub updated_at: String,
}

/// 计划交易执行方式。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ScheduleExecutionMode {
    /// 到期后由用户手动确认执行。
    Manual,
    /// 到期后由系统自动执行；具体执行仍需应用服务保证幂等。
    Automatic,
}

/// 计划交易状态。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ScheduleStatus {
    /// 计划正在生效。
    Active,
    /// 计划已暂停，不再生成新的应发生实例。
    Paused,
    /// 计划已完成，保留历史实例。
    Completed,
}

/// 计划交易定义记录。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ScheduleRecord {
    /// 计划稳定标识。
    pub id: String,
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 计划生成交易所使用的模板标识。
    pub template_id: String,
    /// 计划显示名称。
    pub name: String,
    /// 版本化 recurrence JSON，由应用层解释日历规则。
    pub recurrence_json: String,
    /// 计划开始日期。
    pub start_date: String,
    /// 计划结束日期；为空表示未设置固定结束日。
    pub end_date: Option<String>,
    /// 下一次应发生日期；为空表示暂无待生成实例。
    pub next_due_date: Option<String>,
    /// 执行方式。
    pub execution_mode: ScheduleExecutionMode,
    /// 计划状态。
    pub status: ScheduleStatus,
    /// 最大发生次数；为空表示不限次数。
    pub max_occurrences: Option<i64>,
    /// 提前提醒天数。
    pub reminder_lead_days: i64,
    /// 递推规则版本；修改规则时递增，用于保护历史实例。
    pub recurrence_version: i64,
    /// 最后生成的交易标识。
    pub last_generated_transaction_id: Option<String>,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
    /// 最近更新时间，使用带时区的 ISO 8601 文本。
    pub updated_at: String,
}

/// 提醒状态。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ReminderStatus {
    /// 提醒规则正在生效。
    Active,
    /// 提醒已延后。
    Snoozed,
    /// 提醒已完成，保留历史触发记录。
    Completed,
}

/// 提醒投递方式。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ReminderDeliveryMode {
    /// 只在应用内提醒。
    InApp,
    /// 只使用系统通知。
    SystemNotification,
    /// 应用内和系统通知都投递。
    Both,
}

/// 提醒规则记录。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReminderRecord {
    /// 提醒稳定标识。
    pub id: String,
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 提醒显示名称。
    pub name: String,
    /// 提醒类型键，例如账户余额、日期到期或投资价格。
    pub reminder_kind: String,
    /// 可选目标类型。
    pub target_kind: Option<String>,
    /// 可选目标标识；与 `target_kind` 必须同有同无。
    pub target_id: Option<String>,
    /// 条件 JSON，由应用服务按提醒类型解释。
    pub condition_json: String,
    /// 固定提醒时间；为空表示由条件或递推规则决定。
    pub remind_at: Option<String>,
    /// 递推 JSON；为空表示非重复提醒。
    pub recurrence_json: Option<String>,
    /// 下一次触发时间。
    pub next_trigger_at: Option<String>,
    /// 最近一次触发时间。
    pub last_triggered_at: Option<String>,
    /// 提醒状态。
    pub status: ReminderStatus,
    /// 是否启用该提醒规则。
    pub is_enabled: bool,
    /// 条件版本；修改条件时递增，用于冻结历史触发实例。
    pub condition_version: i64,
    /// 投递方式。
    pub delivery_mode: ReminderDeliveryMode,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
    /// 最近更新时间，使用带时区的 ISO 8601 文本。
    pub updated_at: String,
}
