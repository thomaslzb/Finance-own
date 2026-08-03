-- 待摊费用以独立主体管理账户身份、原始金额和摊销参数，不能只依赖余额调整备注重建。
CREATE TABLE prepaid_expenses (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    account_id TEXT NOT NULL UNIQUE REFERENCES accounts(id) ON DELETE CASCADE,
    party_id TEXT NOT NULL REFERENCES parties(id),
    expense_category_id TEXT NOT NULL REFERENCES categories(id),
    funding_account_id TEXT REFERENCES accounts(id),
    initial_transaction_id TEXT NOT NULL UNIQUE REFERENCES transactions(id),
    original_amount_minor INTEGER NOT NULL CHECK (original_amount_minor > 0),
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    business_date TEXT NOT NULL,
    first_amortization_date TEXT NOT NULL,
    frequency_months INTEGER NOT NULL CHECK (frequency_months > 0),
    total_installments INTEGER NOT NULL CHECK (total_installments > 0),
    posted_installments INTEGER NOT NULL DEFAULT 0 CHECK (
        posted_installments >= 0 AND posted_installments <= total_installments
    ),
    note TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK (
        status IN ('active', 'completed', 'voided')
    ),
    version INTEGER NOT NULL DEFAULT 1 CHECK (version > 0),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (funding_account_id IS NULL OR funding_account_id <> account_id)
) STRICT;

-- 每一期保存确定金额和幂等交易引用；已摊销次数应由已入账期次派生。
CREATE TABLE prepaid_expense_installments (
    id TEXT PRIMARY KEY,
    prepaid_expense_id TEXT NOT NULL REFERENCES prepaid_expenses(id) ON DELETE CASCADE,
    installment_no INTEGER NOT NULL CHECK (installment_no > 0),
    due_date TEXT NOT NULL,
    amount_minor INTEGER NOT NULL CHECK (amount_minor > 0),
    status TEXT NOT NULL DEFAULT 'pending' CHECK (
        status IN ('pending', 'posted', 'voided')
    ),
    transaction_id TEXT UNIQUE REFERENCES transactions(id),
    posted_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (prepaid_expense_id, installment_no),
    CHECK (
        (status = 'posted' AND transaction_id IS NOT NULL AND posted_at IS NOT NULL)
        OR
        (status <> 'posted' AND transaction_id IS NULL AND posted_at IS NULL)
    )
) STRICT;

CREATE INDEX idx_prepaid_expenses_ledger_status_first_due
    ON prepaid_expenses (ledger_id, status, first_amortization_date);

CREATE INDEX idx_prepaid_expenses_party_status
    ON prepaid_expenses (party_id, status, account_id);

CREATE INDEX idx_prepaid_installments_due_status
    ON prepaid_expense_installments (status, due_date, prepaid_expense_id, installment_no);

-- 概况金额由原始金额减去已入账期次得到，避免账户行和摊销计划各存一份可漂移余额。
CREATE VIEW v_prepaid_expense_overview AS
SELECT
    pe.id AS prepaid_expense_id,
    pe.ledger_id,
    pe.account_id,
    a.name AS account_name,
    pe.party_id,
    p.name AS party_name,
    pe.expense_category_id,
    c.name AS expense_category_name,
    pe.original_amount_minor,
    pe.original_amount_minor - COALESCE(SUM(
        CASE WHEN pei.status = 'posted' THEN pei.amount_minor ELSE 0 END
    ), 0) AS remaining_amount_minor,
    pe.currency_code,
    pe.business_date,
    pe.first_amortization_date,
    pe.frequency_months,
    pe.total_installments,
    COALESCE(SUM(CASE WHEN pei.status = 'posted' THEN 1 ELSE 0 END), 0)
        AS posted_installments,
    pe.note,
    pe.status,
    pe.version
FROM prepaid_expenses pe
JOIN accounts a ON a.id = pe.account_id
JOIN parties p ON p.id = pe.party_id
JOIN categories c ON c.id = pe.expense_category_id
LEFT JOIN prepaid_expense_installments pei ON pei.prepaid_expense_id = pe.id
GROUP BY
    pe.id,
    pe.ledger_id,
    pe.account_id,
    a.name,
    pe.party_id,
    p.name,
    pe.expense_category_id,
    c.name,
    pe.original_amount_minor,
    pe.currency_code,
    pe.business_date,
    pe.first_amortization_date,
    pe.frequency_months,
    pe.total_installments,
    pe.note,
    pe.status,
    pe.version;

PRAGMA user_version = 10;
