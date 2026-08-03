PRAGMA foreign_keys = ON;

-- 模板只保存默认业务意图和分录草稿；实际交易仍通过 transactions 原子提交。
CREATE TABLE transaction_templates (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    transaction_kind TEXT NOT NULL,
    default_party_id TEXT REFERENCES parties(id),
    description TEXT,
    is_archived INTEGER NOT NULL DEFAULT 0 CHECK (is_archived IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (ledger_id, name)
) STRICT;

CREATE TABLE transaction_template_entries (
    id TEXT PRIMARY KEY,
    template_id TEXT NOT NULL REFERENCES transaction_templates(id) ON DELETE CASCADE,
    line_no INTEGER NOT NULL CHECK (line_no > 0),
    role TEXT NOT NULL CHECK (role IN ('primary', 'counterparty', 'split', 'fee', 'interest', 'adjustment', 'opening')),
    direction TEXT NOT NULL CHECK (direction IN ('inflow', 'outflow')),
    account_id TEXT REFERENCES accounts(id),
    category_id TEXT REFERENCES categories(id),
    amount_minor INTEGER CHECK (amount_minor >= 0),
    currency_code TEXT REFERENCES currencies(code),
    memo TEXT,
    UNIQUE (template_id, line_no),
    CHECK ((amount_minor IS NULL) = (currency_code IS NULL))
) STRICT;

-- recurrence_json 由 Rust 领域层版本化校验，避免在 SQLite 中复制复杂日历规则。
CREATE TABLE schedules (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    template_id TEXT NOT NULL REFERENCES transaction_templates(id),
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    recurrence_json TEXT NOT NULL CHECK (json_valid(recurrence_json)),
    start_date TEXT NOT NULL,
    end_date TEXT,
    next_due_date TEXT,
    execution_mode TEXT NOT NULL CHECK (execution_mode IN ('manual', 'automatic')),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed')),
    last_generated_transaction_id TEXT REFERENCES transactions(id) ON DELETE SET NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (end_date IS NULL OR end_date >= start_date),
    UNIQUE (ledger_id, name)
) STRICT;

CREATE TABLE budgets (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    period_kind TEXT NOT NULL CHECK (period_kind IN ('monthly', 'quarterly', 'yearly', 'custom')),
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'closed')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (end_date >= start_date),
    UNIQUE (ledger_id, name, start_date, end_date)
) STRICT;

CREATE TABLE budget_items (
    id TEXT PRIMARY KEY,
    budget_id TEXT NOT NULL REFERENCES budgets(id) ON DELETE CASCADE,
    category_id TEXT NOT NULL REFERENCES categories(id),
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    amount_minor INTEGER NOT NULL CHECK (amount_minor >= 0),
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    rollover_mode TEXT NOT NULL DEFAULT 'none' CHECK (rollover_mode IN ('none', 'positive', 'all')),
    note TEXT,
    CHECK (period_end >= period_start),
    UNIQUE (budget_id, category_id, period_start, period_end)
) STRICT;

-- 提醒目标跨账户、投资品和计划，使用稳定目标类型与标识，由应用服务校验引用。
CREATE TABLE reminders (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    reminder_kind TEXT NOT NULL,
    target_kind TEXT,
    target_id TEXT,
    condition_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(condition_json)),
    remind_at TEXT,
    recurrence_json TEXT CHECK (recurrence_json IS NULL OR json_valid(recurrence_json)),
    next_trigger_at TEXT,
    last_triggered_at TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'snoozed', 'completed')),
    is_enabled INTEGER NOT NULL DEFAULT 1 CHECK (is_enabled IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK ((target_kind IS NULL) = (target_id IS NULL)),
    UNIQUE (ledger_id, name)
) STRICT;

CREATE TABLE financial_goals (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    target_amount_minor INTEGER NOT NULL CHECK (target_amount_minor >= 0),
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    target_date TEXT,
    progress_mode TEXT NOT NULL CHECK (progress_mode IN ('balance', 'market_value', 'net_asset', 'custom')),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (ledger_id, name)
) STRICT;

-- 账户删除必须先由应用层预览并处理目标关系，不能静默丢失目标进度来源。
CREATE TABLE financial_goal_accounts (
    goal_id TEXT NOT NULL REFERENCES financial_goals(id) ON DELETE CASCADE,
    account_id TEXT NOT NULL REFERENCES accounts(id),
    PRIMARY KEY (goal_id, account_id)
) WITHOUT ROWID, STRICT;

-- 规划公式尚待旧程序样例校准，输入采用带版本的 JSON 包而不是提前固化错误字段。
CREATE TABLE financial_plan_scenarios (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    base_year INTEGER NOT NULL CHECK (base_year BETWEEN 1900 AND 9999),
    schema_version INTEGER NOT NULL CHECK (schema_version > 0),
    assumptions_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(assumptions_json)),
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'archived')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (ledger_id, name)
) STRICT;

CREATE TABLE financial_plan_inputs (
    id TEXT PRIMARY KEY,
    scenario_id TEXT NOT NULL REFERENCES financial_plan_scenarios(id) ON DELETE CASCADE,
    topic TEXT NOT NULL CHECK (length(trim(topic)) > 0),
    input_year INTEGER CHECK (input_year BETWEEN 1900 AND 9999),
    values_json TEXT NOT NULL CHECK (json_valid(values_json)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
) STRICT;

CREATE UNIQUE INDEX ux_financial_plan_inputs_topic_year
    ON financial_plan_inputs (scenario_id, topic, COALESCE(input_year, -1));

CREATE TABLE financial_plan_accounts (
    scenario_id TEXT NOT NULL REFERENCES financial_plan_scenarios(id) ON DELETE CASCADE,
    account_id TEXT NOT NULL REFERENCES accounts(id),
    role TEXT NOT NULL DEFAULT 'included',
    PRIMARY KEY (scenario_id, account_id, role)
) WITHOUT ROWID, STRICT;

CREATE INDEX idx_template_entries_template
    ON transaction_template_entries (template_id, line_no);
CREATE INDEX idx_schedules_due
    ON schedules (ledger_id, status, next_due_date);
CREATE INDEX idx_budgets_period
    ON budgets (ledger_id, status, start_date, end_date);
CREATE INDEX idx_budget_items_category_period
    ON budget_items (category_id, currency_code, period_start, period_end);
CREATE INDEX idx_reminders_due
    ON reminders (ledger_id, is_enabled, status, next_trigger_at);
CREATE INDEX idx_goals_status_date
    ON financial_goals (ledger_id, status, target_date);
CREATE INDEX idx_goal_accounts_account
    ON financial_goal_accounts (account_id, goal_id);
CREATE INDEX idx_financial_plan_scenarios_status
    ON financial_plan_scenarios (ledger_id, status, base_year);
CREATE INDEX idx_financial_plan_accounts_account
    ON financial_plan_accounts (account_id, scenario_id);

-- 只提供预算消耗输入；收入预算、退款和特殊分类口径由 Rust 计算策略校准。
CREATE VIEW v_budget_consumption_inputs AS
SELECT
    b.ledger_id,
    b.id AS budget_id,
    bi.id AS budget_item_id,
    bi.category_id,
    bi.currency_code,
    bi.period_start,
    bi.period_end,
    bi.amount_minor AS budget_amount_minor,
    COALESCE(SUM(CASE WHEN t.status = 'posted' AND e.direction = 'outflow' THEN e.amount_minor ELSE 0 END), 0) AS outflow_minor,
    COALESCE(SUM(CASE WHEN t.status = 'posted' AND e.direction = 'inflow' THEN e.amount_minor ELSE 0 END), 0) AS inflow_minor
FROM budgets b
JOIN budget_items bi ON bi.budget_id = b.id
LEFT JOIN transaction_entries e
    ON e.category_id = bi.category_id
   AND e.currency_code = bi.currency_code
LEFT JOIN transactions t
    ON t.id = e.transaction_id
   AND t.business_date BETWEEN bi.period_start AND bi.period_end
GROUP BY b.ledger_id, b.id, bi.id, bi.category_id, bi.currency_code,
         bi.period_start, bi.period_end, bi.amount_minor;

-- 目标服务根据 progress_mode 决定使用余额、市值或净资产；视图只输出账户余额输入。
CREATE VIEW v_goal_account_balance_inputs AS
SELECT
    g.ledger_id,
    g.id AS goal_id,
    g.progress_mode,
    g.currency_code AS goal_currency_code,
    ga.account_id,
    ab.currency_code AS account_currency_code,
    ab.balance_minor
FROM financial_goals g
JOIN financial_goal_accounts ga ON ga.goal_id = g.id
LEFT JOIN v_account_balances ab ON ab.account_id = ga.account_id;

CREATE VIEW v_due_schedules AS
SELECT
    s.id,
    s.ledger_id,
    s.template_id,
    s.name,
    s.next_due_date,
    s.execution_mode,
    s.status
FROM schedules s
WHERE s.status = 'active' AND s.next_due_date IS NOT NULL;

PRAGMA user_version = 2;
