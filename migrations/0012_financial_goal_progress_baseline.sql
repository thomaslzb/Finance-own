-- 财务目标的标准进度必须从创建时基线出发；当前余额变化后不能反推或覆盖初始值。
ALTER TABLE financial_goals ADD COLUMN start_date TEXT;
ALTER TABLE financial_goals ADD COLUMN initial_value_minor INTEGER;
ALTER TABLE financial_goals ADD COLUMN initial_value_captured_at TEXT;
ALTER TABLE financial_goals ADD COLUMN initial_inputs_json TEXT
    CHECK (initial_inputs_json IS NULL OR json_valid(initial_inputs_json));
ALTER TABLE financial_goals ADD COLUMN account_scope_mode TEXT NOT NULL DEFAULT 'selected'
    CHECK (account_scope_mode IN ('all', 'selected'));
ALTER TABLE financial_goals ADD COLUMN progress_formula_version TEXT;

-- 兼容旧迁移产生的空日期记录，但新旧调用均不得只写单侧日期或倒置目标期间。
CREATE TRIGGER trg_financial_goals_period_validate_insert
BEFORE INSERT ON financial_goals
WHEN (NEW.start_date IS NULL) <> (NEW.target_date IS NULL)
    OR (
        NEW.start_date IS NOT NULL
        AND julianday(NEW.target_date) < julianday(NEW.start_date)
    )
BEGIN
    SELECT RAISE(ABORT, 'financial goal period is invalid');
END;

CREATE TRIGGER trg_financial_goals_period_validate_update
BEFORE UPDATE OF start_date, target_date ON financial_goals
WHEN (NEW.start_date IS NULL) <> (NEW.target_date IS NULL)
    OR (
        NEW.start_date IS NOT NULL
        AND julianday(NEW.target_date) < julianday(NEW.start_date)
    )
BEGIN
    SELECT RAISE(ABORT, 'financial goal period is invalid');
END;

-- 初始总值、估值时间和逐账户输入属于同一个不可拆分快照，避免产生无法解释的进度基线。
CREATE TRIGGER trg_financial_goals_baseline_validate_insert
BEFORE INSERT ON financial_goals
WHEN (NEW.initial_value_minor IS NULL) <> (NEW.initial_value_captured_at IS NULL)
    OR (NEW.initial_value_minor IS NULL) <> (NEW.initial_inputs_json IS NULL)
BEGIN
    SELECT RAISE(ABORT, 'financial goal baseline snapshot is incomplete');
END;

CREATE TRIGGER trg_financial_goals_baseline_validate_update
BEFORE UPDATE OF initial_value_minor, initial_value_captured_at, initial_inputs_json
ON financial_goals
WHEN (NEW.initial_value_minor IS NULL) <> (NEW.initial_value_captured_at IS NULL)
    OR (NEW.initial_value_minor IS NULL) <> (NEW.initial_inputs_json IS NULL)
BEGIN
    SELECT RAISE(ABORT, 'financial goal baseline snapshot is incomplete');
END;

CREATE INDEX idx_goals_status_period
    ON financial_goals (ledger_id, status, start_date, target_date);

-- 视图保留目标规则、初始快照和当前逐账户输入；跨币种折算由带版本的估值服务完成。
CREATE VIEW v_goal_progress_inputs AS
SELECT
    g.ledger_id,
    g.id AS goal_id,
    g.name AS goal_name,
    g.start_date,
    g.target_date,
    g.target_amount_minor,
    g.currency_code AS goal_currency_code,
    g.initial_value_minor,
    g.initial_value_captured_at,
    g.initial_inputs_json,
    g.account_scope_mode,
    g.progress_mode,
    g.progress_formula_version,
    input.account_id,
    input.account_currency_code,
    input.balance_minor
FROM financial_goals g
LEFT JOIN v_goal_account_balance_inputs input ON input.goal_id = g.id;

PRAGMA user_version = 12;
