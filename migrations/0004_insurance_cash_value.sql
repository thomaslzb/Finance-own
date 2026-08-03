-- 现金价值是保单估值，不进入资金账户分录；同一保单同一估值日只有一个当前有效值。
CREATE TABLE insurance_cash_value_snapshots (
    policy_id TEXT NOT NULL REFERENCES insurance_policies(id),
    valuation_date TEXT NOT NULL,
    value_minor INTEGER NOT NULL,
    source TEXT NOT NULL DEFAULT 'manual',
    version INTEGER NOT NULL DEFAULT 1 CHECK (version >= 1),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (policy_id, valuation_date)
) STRICT;

-- 变更历史保留同日 upsert、显式修改和未来删除的审计事实，不参与当前余额投影。
CREATE TABLE insurance_cash_value_history (
    id INTEGER PRIMARY KEY,
    policy_id TEXT NOT NULL REFERENCES insurance_policies(id),
    valuation_date TEXT NOT NULL,
    operation TEXT NOT NULL CHECK (operation IN ('insert', 'update', 'delete')),
    value_minor INTEGER,
    previous_value_minor INTEGER,
    source TEXT NOT NULL,
    version INTEGER NOT NULL CHECK (version >= 1),
    changed_at TEXT NOT NULL,
    UNIQUE (policy_id, valuation_date, version, operation)
) STRICT;

-- 保险业务事件独立于资金交易；开户调整可无资金分录，实际收付通过可选交易 ID 关联。
CREATE TABLE insurance_events (
    id TEXT PRIMARY KEY,
    policy_id TEXT NOT NULL REFERENCES insurance_policies(id),
    funding_transaction_id TEXT UNIQUE REFERENCES transactions(id),
    event_kind TEXT NOT NULL CHECK (event_kind IN (
        'initial_premium_adjustment',
        'premium_payment',
        'premium_return',
        'dividend',
        'surrender',
        'migration_adjustment'
    )),
    event_date TEXT NOT NULL,
    amount_minor INTEGER NOT NULL CHECK (amount_minor >= 0),
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    source TEXT NOT NULL DEFAULT 'manual',
    status TEXT NOT NULL DEFAULT 'posted' CHECK (status IN ('draft', 'posted', 'void')),
    details_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(details_json)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
) STRICT;

-- 更新必须显式递增版本，防止并发覆盖绕过乐观锁和审计序列。
CREATE TRIGGER trg_insurance_cash_value_update_version
BEFORE UPDATE ON insurance_cash_value_snapshots
FOR EACH ROW
WHEN NEW.version <> OLD.version + 1 OR NEW.created_at <> OLD.created_at
BEGIN
    SELECT RAISE(ABORT, 'insurance cash value version conflict');
END;

CREATE TRIGGER trg_insurance_cash_value_history_insert
AFTER INSERT ON insurance_cash_value_snapshots
FOR EACH ROW
BEGIN
    INSERT INTO insurance_cash_value_history (
        policy_id, valuation_date, operation, value_minor,
        previous_value_minor, source, version, changed_at
    ) VALUES (
        NEW.policy_id, NEW.valuation_date, 'insert', NEW.value_minor,
        NULL, NEW.source, NEW.version, NEW.updated_at
    );
END;

CREATE TRIGGER trg_insurance_cash_value_history_update
AFTER UPDATE ON insurance_cash_value_snapshots
FOR EACH ROW
BEGIN
    INSERT INTO insurance_cash_value_history (
        policy_id, valuation_date, operation, value_minor,
        previous_value_minor, source, version, changed_at
    ) VALUES (
        NEW.policy_id, NEW.valuation_date, 'update', NEW.value_minor,
        OLD.value_minor, NEW.source, NEW.version, NEW.updated_at
    );
END;

CREATE TRIGGER trg_insurance_cash_value_history_delete
BEFORE DELETE ON insurance_cash_value_snapshots
FOR EACH ROW
BEGIN
    INSERT INTO insurance_cash_value_history (
        policy_id, valuation_date, operation, value_minor,
        previous_value_minor, source, version, changed_at
    ) VALUES (
        OLD.policy_id, OLD.valuation_date, 'delete', NULL,
        OLD.value_minor, OLD.source, OLD.version + 1, CURRENT_TIMESTAMP
    );
END;

CREATE INDEX idx_insurance_cash_value_history_policy_date
    ON insurance_cash_value_history (policy_id, valuation_date, version);

CREATE INDEX idx_insurance_events_policy_date
    ON insurance_events (policy_id, event_date, event_kind, status);

-- 当前余额使用最新估值日快照；投保金额和累计缴费不进入该投影。
CREATE VIEW v_insurance_current_cash_values AS
SELECT
    p.ledger_id,
    p.account_id,
    s.policy_id,
    s.valuation_date,
    s.value_minor,
    p.currency_code,
    s.version,
    s.updated_at
FROM insurance_cash_value_snapshots s
JOIN insurance_policies p ON p.id = s.policy_id
WHERE NOT EXISTS (
    SELECT 1
    FROM insurance_cash_value_snapshots newer
    WHERE newer.policy_id = s.policy_id
      AND newer.valuation_date > s.valuation_date
);

PRAGMA user_version = 4;
