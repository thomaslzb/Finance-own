use crate::domain::planning::{
    BudgetItemRecord, BudgetPeriodKind, BudgetRecord, BudgetRolloverMode, BudgetStatus,
    FinancialGoalAccountScopeMode, FinancialGoalProgressMode, FinancialGoalRecord,
    FinancialGoalStatus, ReminderDeliveryMode, ReminderRecord, ReminderStatus,
    ScheduleExecutionMode, ScheduleRecord, ScheduleStatus,
};

/// 新预算项输入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewBudgetItem {
    /// 预算约束的分类标识，必须属于同一账簿。
    pub category_id: String,
    /// 预算项开始日期，格式为 `YYYY-MM-DD`。
    pub period_start: String,
    /// 预算项结束日期，格式为 `YYYY-MM-DD`。
    pub period_end: String,
    /// 预算金额，使用币种最小单位，必须非负。
    pub amount_minor: i64,
    /// 预算币种代码。
    pub currency_code: String,
    /// 剩余额度结转方式。
    pub rollover_mode: BudgetRolloverMode,
    /// 可选备注；为空表示没有补充说明。
    pub note: Option<String>,
}

/// 新预算输入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewBudget {
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
    /// 初始预算状态。
    pub status: BudgetStatus,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
    /// 同事务创建的分类额度。
    pub items: Vec<NewBudgetItem>,
}

/// 预算主体可编辑资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BudgetChanges {
    /// 预算稳定标识。
    pub id: String,
    /// 所属账簿标识，防止跨账簿误更新。
    pub ledger_id: String,
    /// 新预算显示名称。
    pub name: String,
    /// 新预算周期类型。
    pub period_kind: BudgetPeriodKind,
    /// 新开始日期。
    pub start_date: String,
    /// 新结束日期。
    pub end_date: String,
    /// 新生命周期状态。
    pub status: BudgetStatus,
    /// 最近更新时间，使用带时区的 ISO 8601 文本。
    pub updated_at: String,
}

/// 新财务目标输入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewFinancialGoal {
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 目标显示名称。
    pub name: String,
    /// 目标金额，使用目标币种最小单位。
    pub target_amount_minor: i64,
    /// 目标币种代码。
    pub currency_code: String,
    /// 目标开始日期；与 `target_date` 必须同有同无。
    pub start_date: Option<String>,
    /// 目标日期；与 `start_date` 必须同有同无。
    pub target_date: Option<String>,
    /// 进度计算口径。
    pub progress_mode: FinancialGoalProgressMode,
    /// 初始目标状态。
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
    /// 显式关联账户；当范围为 `Selected` 时用于计算进度。
    pub account_ids: Vec<String>,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
}

/// 财务目标可编辑资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FinancialGoalChanges {
    /// 目标稳定标识。
    pub id: String,
    /// 所属账簿标识，防止跨账簿误更新。
    pub ledger_id: String,
    /// 新目标显示名称。
    pub name: String,
    /// 新目标金额。
    pub target_amount_minor: i64,
    /// 新目标币种代码。
    pub currency_code: String,
    /// 新目标开始日期；与 `target_date` 必须同有同无。
    pub start_date: Option<String>,
    /// 新目标日期；与 `start_date` 必须同有同无。
    pub target_date: Option<String>,
    /// 新进度计算口径。
    pub progress_mode: FinancialGoalProgressMode,
    /// 新生命周期状态。
    pub status: FinancialGoalStatus,
    /// 新账户范围口径。
    pub account_scope_mode: FinancialGoalAccountScopeMode,
    /// 新进度公式版本。
    pub progress_formula_version: Option<String>,
    /// 最近更新时间，使用带时区的 ISO 8601 文本。
    pub updated_at: String,
}

/// 新计划交易输入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewSchedule {
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 计划生成交易所使用的模板标识，必须属于同一账簿。
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
    /// 初始计划状态。
    pub status: ScheduleStatus,
    /// 最大发生次数；为空表示不限次数。
    pub max_occurrences: Option<i64>,
    /// 提前提醒天数。
    pub reminder_lead_days: i64,
    /// 递推规则版本；新计划通常为 `1`。
    pub recurrence_version: i64,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
}

/// 计划交易可编辑资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ScheduleChanges {
    /// 计划稳定标识。
    pub id: String,
    /// 所属账簿标识，防止跨账簿误更新。
    pub ledger_id: String,
    /// 计划使用的模板标识。
    pub template_id: String,
    /// 新计划显示名称。
    pub name: String,
    /// 新 recurrence JSON。
    pub recurrence_json: String,
    /// 新开始日期。
    pub start_date: String,
    /// 新结束日期。
    pub end_date: Option<String>,
    /// 新下一次应发生日期。
    pub next_due_date: Option<String>,
    /// 新执行方式。
    pub execution_mode: ScheduleExecutionMode,
    /// 新计划状态。
    pub status: ScheduleStatus,
    /// 新最大发生次数。
    pub max_occurrences: Option<i64>,
    /// 新提前提醒天数。
    pub reminder_lead_days: i64,
    /// 新递推规则版本。
    pub recurrence_version: i64,
    /// 最近更新时间，使用带时区的 ISO 8601 文本。
    pub updated_at: String,
}

/// 新提醒规则输入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NewReminder {
    /// 所属账簿标识。
    pub ledger_id: String,
    /// 提醒显示名称。
    pub name: String,
    /// 提醒类型键。
    pub reminder_kind: String,
    /// 可选目标类型。
    pub target_kind: Option<String>,
    /// 可选目标标识；与 `target_kind` 必须同有同无。
    pub target_id: Option<String>,
    /// 条件 JSON。
    pub condition_json: String,
    /// 固定提醒时间。
    pub remind_at: Option<String>,
    /// 递推 JSON。
    pub recurrence_json: Option<String>,
    /// 下一次触发时间。
    pub next_trigger_at: Option<String>,
    /// 初始提醒状态。
    pub status: ReminderStatus,
    /// 是否启用该提醒。
    pub is_enabled: bool,
    /// 条件版本；新提醒通常为 `1`。
    pub condition_version: i64,
    /// 投递方式。
    pub delivery_mode: ReminderDeliveryMode,
    /// 创建时间，使用带时区的 ISO 8601 文本。
    pub created_at: String,
}

/// 提醒规则可编辑资料。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReminderChanges {
    /// 提醒稳定标识。
    pub id: String,
    /// 所属账簿标识，防止跨账簿误更新。
    pub ledger_id: String,
    /// 新提醒显示名称。
    pub name: String,
    /// 新提醒类型键。
    pub reminder_kind: String,
    /// 新目标类型。
    pub target_kind: Option<String>,
    /// 新目标标识。
    pub target_id: Option<String>,
    /// 新条件 JSON。
    pub condition_json: String,
    /// 新固定提醒时间。
    pub remind_at: Option<String>,
    /// 新递推 JSON。
    pub recurrence_json: Option<String>,
    /// 新下一次触发时间。
    pub next_trigger_at: Option<String>,
    /// 新最近触发时间。
    pub last_triggered_at: Option<String>,
    /// 新提醒状态。
    pub status: ReminderStatus,
    /// 是否启用该提醒。
    pub is_enabled: bool,
    /// 新条件版本。
    pub condition_version: i64,
    /// 新投递方式。
    pub delivery_mode: ReminderDeliveryMode,
    /// 最近更新时间，使用带时区的 ISO 8601 文本。
    pub updated_at: String,
}

/// 计划、预算和目标读写失败。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PlanningDataError {
    /// 输入缺少必填值、期间倒置、金额为负或 JSON 快照非法。
    InvalidInput(String),
    /// 指定对象不存在或不属于目标账簿。
    NotFound(String),
    /// 唯一键、外键或业务状态发生冲突。
    Conflict(String),
    /// 本地数据库操作失败；消息不得包含密钥或完整敏感路径。
    Storage(String),
}

/// 预算和财务目标应用仓储端口。
pub trait PlanningRepository {
    /// 原子创建预算和预算项，返回预算稳定标识。
    fn create_budget(&mut self, budget: &NewBudget) -> Result<String, PlanningDataError>;

    /// 更新预算主体资料，不改写预算项。
    fn update_budget(&mut self, changes: &BudgetChanges) -> Result<(), PlanningDataError>;

    /// 查询账簿全部预算，按开始日期和名称稳定排序。
    fn list_budgets(&self, ledger_id: &str) -> Result<Vec<BudgetRecord>, PlanningDataError>;

    /// 查询指定预算下全部预算项。
    fn list_budget_items(
        &self,
        budget_id: &str,
    ) -> Result<Vec<BudgetItemRecord>, PlanningDataError>;

    /// 用一组新预算项替换旧预算项，适合预算编辑页一次性保存。
    fn replace_budget_items(
        &mut self,
        ledger_id: &str,
        budget_id: &str,
        items: &[NewBudgetItem],
    ) -> Result<(), PlanningDataError>;

    /// 原子创建财务目标和关联账户，返回目标稳定标识。
    fn create_financial_goal(
        &mut self,
        goal: &NewFinancialGoal,
    ) -> Result<String, PlanningDataError>;

    /// 更新财务目标主体资料，不改写初始进度快照。
    fn update_financial_goal(
        &mut self,
        changes: &FinancialGoalChanges,
    ) -> Result<(), PlanningDataError>;

    /// 查询账簿全部财务目标，按目标日期和名称稳定排序。
    fn list_financial_goals(
        &self,
        ledger_id: &str,
    ) -> Result<Vec<FinancialGoalRecord>, PlanningDataError>;

    /// 替换财务目标的显式账户范围。
    fn replace_financial_goal_accounts(
        &mut self,
        ledger_id: &str,
        goal_id: &str,
        account_ids: &[String],
    ) -> Result<(), PlanningDataError>;

    /// 创建计划交易定义，返回计划稳定标识。
    fn create_schedule(&mut self, schedule: &NewSchedule) -> Result<String, PlanningDataError>;

    /// 更新计划交易定义，不改写已生成的计划实例。
    fn update_schedule(&mut self, changes: &ScheduleChanges) -> Result<(), PlanningDataError>;

    /// 查询账簿全部计划交易定义。
    fn list_schedules(&self, ledger_id: &str) -> Result<Vec<ScheduleRecord>, PlanningDataError>;

    /// 创建提醒规则，返回提醒稳定标识。
    fn create_reminder(&mut self, reminder: &NewReminder) -> Result<String, PlanningDataError>;

    /// 更新提醒规则，不改写已触发的提醒实例。
    fn update_reminder(&mut self, changes: &ReminderChanges) -> Result<(), PlanningDataError>;

    /// 查询账簿全部提醒规则。
    fn list_reminders(&self, ledger_id: &str) -> Result<Vec<ReminderRecord>, PlanningDataError>;
}

/// 创建预算前做轻量输入校验，避免无效草稿进入仓储事务。
pub fn create_budget(
    repository: &mut impl PlanningRepository,
    budget: &NewBudget,
) -> Result<String, PlanningDataError> {
    validate_name(&budget.ledger_id, "账簿标识")?;
    validate_name(&budget.name, "预算名称")?;
    validate_period(&budget.start_date, &budget.end_date, "预算期间")?;
    validate_name(&budget.created_at, "创建时间")?;
    if budget.items.is_empty() {
        return Err(PlanningDataError::InvalidInput(
            "预算至少需要一个分类额度".to_owned(),
        ));
    }
    for item in &budget.items {
        validate_budget_item(item)?;
    }
    repository.create_budget(budget)
}

/// 创建财务目标前做轻量输入校验。
pub fn create_financial_goal(
    repository: &mut impl PlanningRepository,
    goal: &NewFinancialGoal,
) -> Result<String, PlanningDataError> {
    validate_name(&goal.ledger_id, "账簿标识")?;
    validate_name(&goal.name, "目标名称")?;
    validate_name(&goal.currency_code, "目标币种")?;
    validate_non_negative(goal.target_amount_minor, "目标金额")?;
    validate_optional_period(goal.start_date.as_deref(), goal.target_date.as_deref())?;
    validate_goal_baseline(
        goal.initial_value_minor,
        goal.initial_value_captured_at.as_deref(),
        goal.initial_inputs_json.as_deref(),
    )?;
    validate_name(&goal.created_at, "创建时间")?;
    repository.create_financial_goal(goal)
}

/// 创建计划交易定义前做轻量输入校验。
pub fn create_schedule(
    repository: &mut impl PlanningRepository,
    schedule: &NewSchedule,
) -> Result<String, PlanningDataError> {
    validate_name(&schedule.ledger_id, "账簿标识")?;
    validate_name(&schedule.template_id, "交易模板标识")?;
    validate_name(&schedule.name, "计划名称")?;
    validate_json(&schedule.recurrence_json, "计划递推规则")?;
    validate_schedule_period(&schedule.start_date, schedule.end_date.as_deref())?;
    validate_non_negative(schedule.reminder_lead_days, "提前提醒天数")?;
    validate_positive_optional(schedule.max_occurrences, "最大发生次数")?;
    validate_positive(schedule.recurrence_version, "递推规则版本")?;
    validate_name(&schedule.created_at, "创建时间")?;
    repository.create_schedule(schedule)
}

/// 创建提醒规则前做轻量输入校验。
pub fn create_reminder(
    repository: &mut impl PlanningRepository,
    reminder: &NewReminder,
) -> Result<String, PlanningDataError> {
    validate_name(&reminder.ledger_id, "账簿标识")?;
    validate_name(&reminder.name, "提醒名称")?;
    validate_name(&reminder.reminder_kind, "提醒类型")?;
    validate_target_pair(
        reminder.target_kind.as_deref(),
        reminder.target_id.as_deref(),
    )?;
    validate_json(&reminder.condition_json, "提醒条件")?;
    if let Some(recurrence_json) = &reminder.recurrence_json {
        validate_json(recurrence_json, "提醒递推规则")?;
    }
    validate_positive(reminder.condition_version, "提醒条件版本")?;
    validate_name(&reminder.created_at, "创建时间")?;
    repository.create_reminder(reminder)
}

fn validate_budget_item(item: &NewBudgetItem) -> Result<(), PlanningDataError> {
    validate_name(&item.category_id, "预算分类")?;
    validate_period(&item.period_start, &item.period_end, "预算项期间")?;
    validate_non_negative(item.amount_minor, "预算金额")?;
    validate_name(&item.currency_code, "预算币种")
}

fn validate_optional_period(
    start_date: Option<&str>,
    target_date: Option<&str>,
) -> Result<(), PlanningDataError> {
    match (start_date, target_date) {
        (None, None) => Ok(()),
        (Some(start), Some(end)) => validate_period(start, end, "目标期间"),
        _ => Err(PlanningDataError::InvalidInput(
            "目标开始日期和目标日期必须同有同无".to_owned(),
        )),
    }
}

fn validate_schedule_period(start: &str, end: Option<&str>) -> Result<(), PlanningDataError> {
    validate_name(start, "计划开始日期")?;
    if let Some(end) = end {
        validate_name(end, "计划结束日期")?;
        if end < start {
            return Err(PlanningDataError::InvalidInput(
                "计划结束日期不能早于开始日期".to_owned(),
            ));
        }
    }
    Ok(())
}

fn validate_goal_baseline(
    value: Option<i64>,
    captured_at: Option<&str>,
    inputs_json: Option<&str>,
) -> Result<(), PlanningDataError> {
    match (value, captured_at, inputs_json) {
        (None, None, None) => Ok(()),
        (Some(value), Some(captured_at), Some(inputs_json)) => {
            validate_non_negative(value, "初始目标进度值")?;
            validate_name(captured_at, "初始进度捕获时间")?;
            serde_json::from_str::<serde_json::Value>(inputs_json).map_err(|_| {
                PlanningDataError::InvalidInput("初始进度输入快照必须是合法 JSON".to_owned())
            })?;
            Ok(())
        }
        _ => Err(PlanningDataError::InvalidInput(
            "初始进度值、捕获时间和输入快照必须同有同无".to_owned(),
        )),
    }
}

fn validate_json(value: &str, label: &str) -> Result<(), PlanningDataError> {
    serde_json::from_str::<serde_json::Value>(value)
        .map(|_| ())
        .map_err(|_| PlanningDataError::InvalidInput(format!("{label}必须是合法 JSON")))
}

fn validate_target_pair(
    target_kind: Option<&str>,
    target_id: Option<&str>,
) -> Result<(), PlanningDataError> {
    match (target_kind, target_id) {
        (None, None) => Ok(()),
        (Some(kind), Some(id)) => {
            validate_name(kind, "提醒目标类型")?;
            validate_name(id, "提醒目标标识")
        }
        _ => Err(PlanningDataError::InvalidInput(
            "提醒目标类型和目标标识必须同有同无".to_owned(),
        )),
    }
}

fn validate_positive(value: i64, label: &str) -> Result<(), PlanningDataError> {
    if value <= 0 {
        return Err(PlanningDataError::InvalidInput(format!(
            "{label}必须大于零"
        )));
    }
    Ok(())
}

fn validate_positive_optional(value: Option<i64>, label: &str) -> Result<(), PlanningDataError> {
    if let Some(value) = value {
        validate_positive(value, label)?;
    }
    Ok(())
}

fn validate_period(start: &str, end: &str, label: &str) -> Result<(), PlanningDataError> {
    validate_name(start, &format!("{label}开始日期"))?;
    validate_name(end, &format!("{label}结束日期"))?;
    if end < start {
        return Err(PlanningDataError::InvalidInput(format!(
            "{label}结束日期不能早于开始日期"
        )));
    }
    Ok(())
}

fn validate_non_negative(value: i64, label: &str) -> Result<(), PlanningDataError> {
    if value < 0 {
        return Err(PlanningDataError::InvalidInput(format!(
            "{label}不能为负数"
        )));
    }
    Ok(())
}

fn validate_name(value: &str, label: &str) -> Result<(), PlanningDataError> {
    if value.trim().is_empty() {
        return Err(PlanningDataError::InvalidInput(format!("{label}不能为空")));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    struct RejectingPlanningRepository;

    impl PlanningRepository for RejectingPlanningRepository {
        fn create_budget(&mut self, _budget: &NewBudget) -> Result<String, PlanningDataError> {
            unreachable!("无效预算不应进入仓储")
        }

        fn update_budget(&mut self, _changes: &BudgetChanges) -> Result<(), PlanningDataError> {
            unreachable!()
        }

        fn list_budgets(&self, _ledger_id: &str) -> Result<Vec<BudgetRecord>, PlanningDataError> {
            unreachable!()
        }

        fn list_budget_items(
            &self,
            _budget_id: &str,
        ) -> Result<Vec<BudgetItemRecord>, PlanningDataError> {
            unreachable!()
        }

        fn replace_budget_items(
            &mut self,
            _ledger_id: &str,
            _budget_id: &str,
            _items: &[NewBudgetItem],
        ) -> Result<(), PlanningDataError> {
            unreachable!()
        }

        fn create_financial_goal(
            &mut self,
            _goal: &NewFinancialGoal,
        ) -> Result<String, PlanningDataError> {
            unreachable!("无效目标不应进入仓储")
        }

        fn update_financial_goal(
            &mut self,
            _changes: &FinancialGoalChanges,
        ) -> Result<(), PlanningDataError> {
            unreachable!()
        }

        fn list_financial_goals(
            &self,
            _ledger_id: &str,
        ) -> Result<Vec<FinancialGoalRecord>, PlanningDataError> {
            unreachable!()
        }

        fn replace_financial_goal_accounts(
            &mut self,
            _ledger_id: &str,
            _goal_id: &str,
            _account_ids: &[String],
        ) -> Result<(), PlanningDataError> {
            unreachable!()
        }

        fn create_schedule(
            &mut self,
            _schedule: &NewSchedule,
        ) -> Result<String, PlanningDataError> {
            unreachable!("无效计划不应进入仓储")
        }

        fn update_schedule(&mut self, _changes: &ScheduleChanges) -> Result<(), PlanningDataError> {
            unreachable!()
        }

        fn list_schedules(
            &self,
            _ledger_id: &str,
        ) -> Result<Vec<ScheduleRecord>, PlanningDataError> {
            unreachable!()
        }

        fn create_reminder(
            &mut self,
            _reminder: &NewReminder,
        ) -> Result<String, PlanningDataError> {
            unreachable!("无效提醒不应进入仓储")
        }

        fn update_reminder(&mut self, _changes: &ReminderChanges) -> Result<(), PlanningDataError> {
            unreachable!()
        }

        fn list_reminders(
            &self,
            _ledger_id: &str,
        ) -> Result<Vec<ReminderRecord>, PlanningDataError> {
            unreachable!()
        }
    }

    #[test]
    fn budget_requires_at_least_one_item() {
        let budget = NewBudget {
            ledger_id: "ledger-1".to_owned(),
            name: "月度预算".to_owned(),
            period_kind: BudgetPeriodKind::Monthly,
            start_date: "2026-08-01".to_owned(),
            end_date: "2026-08-31".to_owned(),
            status: BudgetStatus::Draft,
            created_at: "2026-08-03T10:00:00+08:00".to_owned(),
            items: vec![],
        };
        let error = create_budget(&mut RejectingPlanningRepository, &budget).unwrap_err();
        assert!(matches!(error, PlanningDataError::InvalidInput(_)));
    }

    #[test]
    fn goal_baseline_requires_complete_snapshot() {
        let goal = NewFinancialGoal {
            ledger_id: "ledger-1".to_owned(),
            name: "买房目标".to_owned(),
            target_amount_minor: 100_000,
            currency_code: "CNY".to_owned(),
            start_date: Some("2026-08-01".to_owned()),
            target_date: Some("2027-08-01".to_owned()),
            progress_mode: FinancialGoalProgressMode::Balance,
            status: FinancialGoalStatus::Active,
            initial_value_minor: Some(1),
            initial_value_captured_at: None,
            initial_inputs_json: Some("{}".to_owned()),
            account_scope_mode: FinancialGoalAccountScopeMode::Selected,
            progress_formula_version: None,
            account_ids: vec![],
            created_at: "2026-08-03T10:00:00+08:00".to_owned(),
        };
        let error = create_financial_goal(&mut RejectingPlanningRepository, &goal).unwrap_err();
        assert!(matches!(error, PlanningDataError::InvalidInput(_)));
    }
}
