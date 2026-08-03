PRAGMA foreign_keys = ON;

-- Finance Own 把 SQLite 作为应用文件格式，固定文件头标识以阻止误打开其它 SQLite 数据库。
PRAGMA application_id = 1179604814;

-- 工资头只保存复合业务的身份和计算版本；金额汇总由明细与账户分录重建，避免缓存漂移。
CREATE TABLE payroll_income_details (
    transaction_id TEXT PRIMARY KEY REFERENCES transactions(id) ON DELETE CASCADE,
    receiving_account_id TEXT NOT NULL REFERENCES accounts(id),
    person_id TEXT REFERENCES parties(id),
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    calculation_version INTEGER NOT NULL DEFAULT 1 CHECK (calculation_version > 0),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
) STRICT;

-- 税前收入和普通扣款分开保存；同一分类在同一工资区域内只能出现一次。
CREATE TABLE payroll_category_components (
    id TEXT PRIMARY KEY,
    transaction_id TEXT NOT NULL REFERENCES payroll_income_details(transaction_id) ON DELETE CASCADE,
    line_no INTEGER NOT NULL CHECK (line_no > 0),
    component_kind TEXT NOT NULL CHECK (component_kind IN ('income', 'deduction')),
    category_id TEXT NOT NULL REFERENCES categories(id),
    amount_minor INTEGER NOT NULL CHECK (amount_minor > 0),
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    memo TEXT,
    UNIQUE (transaction_id, component_kind, line_no),
    UNIQUE (transaction_id, component_kind, category_id)
) STRICT;

-- 个人缴费减少实收现金，公司缴费只增加社保权益；两者不能同时为零。
CREATE TABLE payroll_social_contributions (
    id TEXT PRIMARY KEY,
    transaction_id TEXT NOT NULL REFERENCES payroll_income_details(transaction_id) ON DELETE CASCADE,
    line_no INTEGER NOT NULL CHECK (line_no > 0),
    social_account_id TEXT NOT NULL REFERENCES accounts(id),
    personal_amount_minor INTEGER NOT NULL DEFAULT 0 CHECK (personal_amount_minor >= 0),
    company_amount_minor INTEGER NOT NULL DEFAULT 0 CHECK (company_amount_minor >= 0),
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    memo TEXT,
    UNIQUE (transaction_id, line_no),
    UNIQUE (transaction_id, social_account_id),
    CHECK (personal_amount_minor > 0 OR company_amount_minor > 0)
) STRICT;

-- 工资交易、实收账户和可选人员必须属于同一账簿，且交易使用稳定专属类型键。
CREATE TRIGGER trg_payroll_income_details_scope_insert
BEFORE INSERT ON payroll_income_details
FOR EACH ROW
WHEN NOT EXISTS (
    SELECT 1
    FROM transactions t
    JOIN accounts a ON a.id = NEW.receiving_account_id
    WHERE t.id = NEW.transaction_id
      AND t.kind = 'payroll_income'
      AND t.ledger_id = a.ledger_id
      AND a.currency_code = NEW.currency_code
      AND (
          NEW.person_id IS NULL
          OR EXISTS (
              SELECT 1 FROM parties p
              WHERE p.id = NEW.person_id AND p.ledger_id = t.ledger_id
          )
      )
)
BEGIN
    SELECT RAISE(ABORT, 'payroll income scope mismatch');
END;

CREATE TRIGGER trg_payroll_income_details_scope_update
BEFORE UPDATE OF transaction_id, receiving_account_id, person_id, currency_code
ON payroll_income_details
FOR EACH ROW
WHEN NOT EXISTS (
    SELECT 1
    FROM transactions t
    JOIN accounts a ON a.id = NEW.receiving_account_id
    WHERE t.id = NEW.transaction_id
      AND t.kind = 'payroll_income'
      AND t.ledger_id = a.ledger_id
      AND a.currency_code = NEW.currency_code
      AND (
          NEW.person_id IS NULL
          OR EXISTS (
              SELECT 1 FROM parties p
              WHERE p.id = NEW.person_id AND p.ledger_id = t.ledger_id
          )
      )
)
BEGIN
    SELECT RAISE(ABORT, 'payroll income scope mismatch');
END;

-- 分类明细必须与工资交易同账簿、同币种，并使用与区域一致的收支方向。
CREATE TRIGGER trg_payroll_category_component_scope_insert
BEFORE INSERT ON payroll_category_components
FOR EACH ROW
WHEN NOT EXISTS (
    SELECT 1
    FROM payroll_income_details d
    JOIN transactions t ON t.id = d.transaction_id
    JOIN categories c ON c.id = NEW.category_id
    WHERE d.transaction_id = NEW.transaction_id
      AND d.currency_code = NEW.currency_code
      AND c.ledger_id = t.ledger_id
      AND (
          (NEW.component_kind = 'income' AND c.direction = 'income')
          OR (NEW.component_kind = 'deduction' AND c.direction = 'expense')
      )
)
BEGIN
    SELECT RAISE(ABORT, 'payroll category component scope mismatch');
END;

CREATE TRIGGER trg_payroll_category_component_scope_update
BEFORE UPDATE OF transaction_id, component_kind, category_id, currency_code
ON payroll_category_components
FOR EACH ROW
WHEN NOT EXISTS (
    SELECT 1
    FROM payroll_income_details d
    JOIN transactions t ON t.id = d.transaction_id
    JOIN categories c ON c.id = NEW.category_id
    WHERE d.transaction_id = NEW.transaction_id
      AND d.currency_code = NEW.currency_code
      AND c.ledger_id = t.ledger_id
      AND (
          (NEW.component_kind = 'income' AND c.direction = 'income')
          OR (NEW.component_kind = 'deduction' AND c.direction = 'expense')
      )
)
BEGIN
    SELECT RAISE(ABORT, 'payroll category component scope mismatch');
END;

-- 存在社保组成时工资头必须指定人员，社保账户还必须与交易同账簿、同币种。
CREATE TRIGGER trg_payroll_social_contribution_scope_insert
BEFORE INSERT ON payroll_social_contributions
FOR EACH ROW
WHEN NOT EXISTS (
    SELECT 1
    FROM payroll_income_details d
    JOIN transactions t ON t.id = d.transaction_id
    JOIN accounts a ON a.id = NEW.social_account_id
    WHERE d.transaction_id = NEW.transaction_id
      AND d.person_id IS NOT NULL
      AND d.currency_code = NEW.currency_code
      AND a.ledger_id = t.ledger_id
      AND a.currency_code = NEW.currency_code
)
BEGIN
    SELECT RAISE(ABORT, 'payroll social contribution scope mismatch');
END;

CREATE TRIGGER trg_payroll_social_contribution_scope_update
BEFORE UPDATE OF transaction_id, social_account_id, currency_code
ON payroll_social_contributions
FOR EACH ROW
WHEN NOT EXISTS (
    SELECT 1
    FROM payroll_income_details d
    JOIN transactions t ON t.id = d.transaction_id
    JOIN accounts a ON a.id = NEW.social_account_id
    WHERE d.transaction_id = NEW.transaction_id
      AND d.person_id IS NOT NULL
      AND d.currency_code = NEW.currency_code
      AND a.ledger_id = t.ledger_id
      AND a.currency_code = NEW.currency_code
)
BEGIN
    SELECT RAISE(ABORT, 'payroll social contribution scope mismatch');
END;

CREATE INDEX idx_payroll_income_details_person
    ON payroll_income_details (person_id, transaction_id);
CREATE INDEX idx_payroll_category_components_transaction
    ON payroll_category_components (transaction_id, component_kind, line_no);
CREATE INDEX idx_payroll_social_contributions_transaction
    ON payroll_social_contributions (transaction_id, social_account_id);

-- 该视图同时给出业务公式和账户投影核对结果；不匹配时应用层不得把工资标记为完成。
CREATE VIEW v_payroll_income_reconciliation AS
WITH category_totals AS (
    SELECT
        transaction_id,
        SUM(CASE WHEN component_kind = 'income' THEN amount_minor ELSE 0 END) AS gross_income_minor,
        SUM(CASE WHEN component_kind = 'deduction' THEN amount_minor ELSE 0 END) AS deduction_minor
    FROM payroll_category_components
    GROUP BY transaction_id
),
social_totals AS (
    SELECT
        transaction_id,
        SUM(personal_amount_minor) AS personal_contribution_minor,
        SUM(company_amount_minor) AS company_contribution_minor
    FROM payroll_social_contributions
    GROUP BY transaction_id
),
account_movements AS (
    SELECT
        d.transaction_id,
        SUM(
            CASE
                WHEN e.account_id = d.receiving_account_id AND e.direction = 'inflow' THEN e.amount_minor
                WHEN e.account_id = d.receiving_account_id AND e.direction = 'outflow' THEN -e.amount_minor
                ELSE 0
            END
        ) AS receiving_account_movement_minor,
        SUM(
            CASE
                WHEN s.social_account_id IS NOT NULL AND e.direction = 'inflow' THEN e.amount_minor
                WHEN s.social_account_id IS NOT NULL AND e.direction = 'outflow' THEN -e.amount_minor
                ELSE 0
            END
        ) AS social_account_movement_minor
    FROM payroll_income_details d
    LEFT JOIN transaction_entries e ON e.transaction_id = d.transaction_id
    LEFT JOIN payroll_social_contributions s
      ON s.transaction_id = d.transaction_id
     AND s.social_account_id = e.account_id
    GROUP BY d.transaction_id
)
SELECT
    d.transaction_id,
    t.ledger_id,
    t.status,
    d.receiving_account_id,
    d.person_id,
    d.currency_code,
    COALESCE(c.gross_income_minor, 0) AS gross_income_minor,
    COALESCE(c.deduction_minor, 0) AS deduction_minor,
    COALESCE(s.personal_contribution_minor, 0) AS personal_contribution_minor,
    COALESCE(s.company_contribution_minor, 0) AS company_contribution_minor,
    COALESCE(c.gross_income_minor, 0)
        - COALESCE(c.deduction_minor, 0)
        - COALESCE(s.personal_contribution_minor, 0) AS net_cash_minor,
    COALESCE(s.personal_contribution_minor, 0)
        + COALESCE(s.company_contribution_minor, 0) AS social_account_credit_minor,
    COALESCE(a.receiving_account_movement_minor, 0) AS receiving_account_movement_minor,
    COALESCE(a.social_account_movement_minor, 0) AS social_account_movement_minor,
    COALESCE(c.gross_income_minor, 0)
        >= COALESCE(c.deduction_minor, 0) + COALESCE(s.personal_contribution_minor, 0)
        AS is_component_formula_valid,
    COALESCE(a.receiving_account_movement_minor, 0)
        = COALESCE(c.gross_income_minor, 0)
            - COALESCE(c.deduction_minor, 0)
            - COALESCE(s.personal_contribution_minor, 0)
        AS is_cash_projection_matched,
    COALESCE(a.social_account_movement_minor, 0)
        = COALESCE(s.personal_contribution_minor, 0)
            + COALESCE(s.company_contribution_minor, 0)
        AS is_social_projection_matched
FROM payroll_income_details d
JOIN transactions t ON t.id = d.transaction_id
LEFT JOIN category_totals c ON c.transaction_id = d.transaction_id
LEFT JOIN social_totals s ON s.transaction_id = d.transaction_id
LEFT JOIN account_movements a ON a.transaction_id = d.transaction_id;

PRAGMA user_version = 7;
