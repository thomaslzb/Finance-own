PRAGMA foreign_keys = ON;

-- 金额统一保存为币种最小单位，数量、价格和汇率保存为带显式 scale 的整数。
CREATE TABLE currencies (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    minor_unit INTEGER NOT NULL CHECK (minor_unit BETWEEN 0 AND 8),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
) STRICT;

CREATE TABLE ledgers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    base_currency_code TEXT NOT NULL REFERENCES currencies(code),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
) STRICT;

CREATE TABLE account_groups (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    parent_id TEXT REFERENCES account_groups(id),
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    kind TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    UNIQUE (ledger_id, parent_id, name)
) STRICT;

CREATE TABLE accounts (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    -- 删除账户组只解除分组关系，账户、交易和余额必须保留。
    group_id TEXT REFERENCES account_groups(id) ON DELETE SET NULL,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    kind TEXT NOT NULL,
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    institution_name TEXT,
    account_number_masked TEXT,
    is_asset INTEGER NOT NULL CHECK (is_asset IN (0, 1)),
    is_hidden INTEGER NOT NULL DEFAULT 0 CHECK (is_hidden IN (0, 1)),
    closed_on TEXT,
    created_at TEXT NOT NULL,
    UNIQUE (ledger_id, name)
) STRICT;

CREATE TABLE categories (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    parent_id TEXT REFERENCES categories(id),
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    direction TEXT NOT NULL CHECK (direction IN ('income', 'expense', 'both')),
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_archived INTEGER NOT NULL DEFAULT 0 CHECK (is_archived IN (0, 1)),
    UNIQUE (ledger_id, parent_id, name, direction)
) STRICT;

CREATE TABLE tags (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    color TEXT,
    is_archived INTEGER NOT NULL DEFAULT 0 CHECK (is_archived IN (0, 1)),
    UNIQUE (ledger_id, name)
) STRICT;

CREATE TABLE parties (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    kind TEXT NOT NULL CHECK (kind IN ('person', 'institution', 'other')),
    is_archived INTEGER NOT NULL DEFAULT 0 CHECK (is_archived IN (0, 1)),
    UNIQUE (ledger_id, name, kind)
) STRICT;

CREATE TABLE exchange_rate_snapshots (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    source_currency_code TEXT NOT NULL REFERENCES currencies(code),
    target_currency_code TEXT NOT NULL REFERENCES currencies(code),
    rate_units INTEGER NOT NULL CHECK (rate_units > 0),
    rate_scale INTEGER NOT NULL CHECK (rate_scale BETWEEN 0 AND 12),
    quoted_at TEXT NOT NULL,
    source TEXT NOT NULL,
    CHECK (source_currency_code <> target_currency_code)
) STRICT;

CREATE TABLE transactions (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    sequence_no INTEGER NOT NULL CHECK (sequence_no > 0),
    business_date TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    kind TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'posted' CHECK (status IN ('draft', 'posted', 'voided')),
    party_id TEXT REFERENCES parties(id),
    theme TEXT,
    description TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (ledger_id, sequence_no)
) STRICT;

CREATE TABLE transaction_entries (
    id TEXT PRIMARY KEY,
    transaction_id TEXT NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    account_id TEXT NOT NULL REFERENCES accounts(id),
    line_no INTEGER NOT NULL CHECK (line_no > 0),
    role TEXT NOT NULL CHECK (role IN ('primary', 'counterparty', 'split', 'fee', 'interest', 'adjustment', 'opening')),
    direction TEXT NOT NULL CHECK (direction IN ('inflow', 'outflow')),
    amount_minor INTEGER NOT NULL CHECK (amount_minor >= 0),
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    base_amount_minor INTEGER CHECK (base_amount_minor >= 0),
    base_currency_code TEXT REFERENCES currencies(code),
    fx_snapshot_id TEXT REFERENCES exchange_rate_snapshots(id),
    category_id TEXT REFERENCES categories(id),
    memo TEXT,
    UNIQUE (transaction_id, line_no),
    CHECK ((base_amount_minor IS NULL) = (base_currency_code IS NULL))
) STRICT;

CREATE TABLE transaction_tags (
    transaction_id TEXT NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    tag_id TEXT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (transaction_id, tag_id)
) WITHOUT ROWID, STRICT;

CREATE TABLE account_tags (
    account_id TEXT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    tag_id TEXT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (account_id, tag_id)
) WITHOUT ROWID, STRICT;

CREATE TABLE attachments (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    file_name TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    media_type TEXT,
    byte_size INTEGER NOT NULL CHECK (byte_size >= 0),
    sha256 TEXT NOT NULL CHECK (length(sha256) = 64),
    created_at TEXT NOT NULL,
    UNIQUE (ledger_id, sha256)
) STRICT;

CREATE TABLE transaction_attachments (
    transaction_id TEXT NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    -- 附件仍被任一交易引用时禁止物理删除内容记录。
    attachment_id TEXT NOT NULL REFERENCES attachments(id) ON DELETE RESTRICT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (transaction_id, attachment_id)
) WITHOUT ROWID, STRICT;

CREATE TABLE investment_instruments (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    code TEXT,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    kind TEXT NOT NULL,
    quote_currency_code TEXT NOT NULL REFERENCES currencies(code),
    quantity_scale INTEGER NOT NULL CHECK (quantity_scale BETWEEN 0 AND 12),
    price_scale INTEGER NOT NULL CHECK (price_scale BETWEEN 0 AND 12),
    is_archived INTEGER NOT NULL DEFAULT 0 CHECK (is_archived IN (0, 1)),
    UNIQUE (ledger_id, kind, code)
) STRICT;

CREATE TABLE investment_trades (
    id TEXT PRIMARY KEY,
    transaction_id TEXT NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    cash_entry_id TEXT REFERENCES transaction_entries(id),
    account_id TEXT NOT NULL REFERENCES accounts(id),
    instrument_id TEXT NOT NULL REFERENCES investment_instruments(id),
    trade_kind TEXT NOT NULL CHECK (trade_kind IN ('buy', 'sell', 'dividend', 'interest', 'split', 'transfer_in', 'transfer_out', 'other')),
    position_effect INTEGER NOT NULL CHECK (position_effect IN (-1, 0, 1)),
    quantity_units INTEGER NOT NULL CHECK (quantity_units >= 0),
    price_units INTEGER CHECK (price_units >= 0),
    price_scale INTEGER CHECK (price_scale BETWEEN 0 AND 12),
    UNIQUE (cash_entry_id),
    CHECK ((price_units IS NULL) = (price_scale IS NULL))
) STRICT;

CREATE TABLE investment_lot_allocations (
    id TEXT PRIMARY KEY,
    sell_trade_id TEXT NOT NULL REFERENCES investment_trades(id) ON DELETE CASCADE,
    buy_trade_id TEXT NOT NULL REFERENCES investment_trades(id),
    quantity_units INTEGER NOT NULL CHECK (quantity_units > 0),
    allocated_cost_minor INTEGER NOT NULL CHECK (allocated_cost_minor >= 0),
    allocated_proceeds_minor INTEGER NOT NULL CHECK (allocated_proceeds_minor >= 0),
    UNIQUE (sell_trade_id, buy_trade_id)
) STRICT;

CREATE TABLE market_quotes (
    id TEXT PRIMARY KEY,
    instrument_id TEXT NOT NULL REFERENCES investment_instruments(id) ON DELETE CASCADE,
    quoted_at TEXT NOT NULL,
    price_units INTEGER NOT NULL CHECK (price_units >= 0),
    price_scale INTEGER NOT NULL CHECK (price_scale BETWEEN 0 AND 12),
    source TEXT NOT NULL,
    UNIQUE (instrument_id, quoted_at, source)
) STRICT;

CREATE TABLE report_presets (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    report_key TEXT NOT NULL,
    name TEXT NOT NULL,
    filter_json TEXT NOT NULL CHECK (json_valid(filter_json)),
    chart_series_json TEXT NOT NULL DEFAULT '[]' CHECK (json_valid(chart_series_json)),
    is_default INTEGER NOT NULL DEFAULT 0 CHECK (is_default IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (ledger_id, report_key, name)
) STRICT;

CREATE TABLE legacy_id_map (
    id INTEGER PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    source_name TEXT NOT NULL,
    entity_kind TEXT NOT NULL,
    legacy_id TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    imported_at TEXT NOT NULL,
    UNIQUE (ledger_id, source_name, entity_kind, legacy_id)
) STRICT;

CREATE INDEX idx_accounts_ledger_group
    ON accounts (ledger_id, group_id, is_hidden, name);
CREATE UNIQUE INDEX ux_account_groups_sibling_name
    ON account_groups (ledger_id, COALESCE(parent_id, ''), name);
CREATE UNIQUE INDEX ux_categories_sibling_name_direction
    ON categories (ledger_id, COALESCE(parent_id, ''), name, direction);
CREATE INDEX idx_exchange_rates_pair_time
    ON exchange_rate_snapshots (ledger_id, source_currency_code, target_currency_code, quoted_at DESC);
CREATE INDEX idx_transactions_ledger_status_date
    ON transactions (ledger_id, status, business_date, sequence_no);
CREATE INDEX idx_entries_account_currency_transaction
    ON transaction_entries (account_id, currency_code, transaction_id, line_no);
CREATE INDEX idx_entries_category_transaction
    ON transaction_entries (category_id, transaction_id);
CREATE INDEX idx_transaction_tags_tag_transaction
    ON transaction_tags (tag_id, transaction_id);
CREATE INDEX idx_account_tags_tag_account
    ON account_tags (tag_id, account_id);
CREATE INDEX idx_investment_trades_position
    ON investment_trades (account_id, instrument_id, trade_kind);
CREATE INDEX idx_lot_allocations_buy_trade
    ON investment_lot_allocations (buy_trade_id, sell_trade_id);
CREATE INDEX idx_market_quotes_latest
    ON market_quotes (instrument_id, quoted_at DESC);
CREATE INDEX idx_report_presets_lookup
    ON report_presets (ledger_id, report_key, is_default, name);
CREATE INDEX idx_legacy_id_map_entity
    ON legacy_id_map (ledger_id, entity_kind, entity_id);

CREATE VIEW v_ledger_entries AS
SELECT
    t.ledger_id,
    t.id AS transaction_id,
    e.id AS entry_id,
    t.sequence_no,
    e.line_no,
    t.business_date,
    t.occurred_at,
    t.kind AS transaction_kind,
    t.status,
    e.role,
    e.direction,
    e.account_id,
    a.name AS account_name,
    e.category_id,
    c.name AS category_name,
    e.currency_code,
    e.amount_minor,
    CASE e.direction WHEN 'inflow' THEN e.amount_minor ELSE -e.amount_minor END AS signed_amount_minor,
    e.base_currency_code,
    e.base_amount_minor,
    CASE
        WHEN e.base_amount_minor IS NULL THEN NULL
        WHEN e.direction = 'inflow' THEN e.base_amount_minor
        ELSE -e.base_amount_minor
    END AS signed_base_amount_minor,
    t.theme,
    t.description,
    e.memo,
    EXISTS (
        SELECT 1 FROM transaction_attachments ta WHERE ta.transaction_id = t.id
    ) AS has_attachments,
    (
        SELECT group_concat(tag_name, ',')
        FROM (
            SELECT tg.name AS tag_name
            FROM transaction_tags tt
            JOIN tags tg ON tg.id = tt.tag_id
            WHERE tt.transaction_id = t.id
            ORDER BY tg.name
        )
    ) AS tag_names
FROM transactions t
JOIN transaction_entries e ON e.transaction_id = t.id
JOIN accounts a ON a.id = e.account_id
LEFT JOIN categories c ON c.id = e.category_id;

CREATE VIEW v_account_transaction_running_balance AS
SELECT
    le.*,
    SUM(le.signed_amount_minor) OVER (
        PARTITION BY le.ledger_id, le.account_id, le.currency_code
        ORDER BY le.business_date, le.sequence_no, le.line_no, le.entry_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS balance_minor
FROM v_ledger_entries le
WHERE le.status = 'posted';

CREATE VIEW v_account_balances AS
SELECT
    ledger_id,
    account_id,
    account_name,
    currency_code,
    SUM(signed_amount_minor) AS balance_minor
FROM v_ledger_entries
WHERE status = 'posted'
GROUP BY ledger_id, account_id, account_name, currency_code;

CREATE VIEW v_life_theme_transactions AS
SELECT
    tg.id AS tag_id,
    tg.name AS tag_name,
    le.*
FROM transaction_tags tt
JOIN tags tg ON tg.id = tt.tag_id
JOIN v_ledger_entries le ON le.transaction_id = tt.transaction_id;

CREATE VIEW v_life_theme_assets AS
SELECT
    tg.id AS tag_id,
    tg.name AS tag_name,
    ab.ledger_id,
    ab.account_id,
    ab.account_name,
    ab.currency_code,
    ab.balance_minor
FROM account_tags atg
JOIN tags tg ON tg.id = atg.tag_id
JOIN v_account_balances ab ON ab.account_id = atg.account_id;

-- 只输出持仓计算输入。成本法、含费盈亏和收益率须经旧程序样例校准后再固化。
CREATE VIEW v_investment_position_inputs AS
SELECT
    t.ledger_id,
    it.account_id,
    it.instrument_id,
    i.name AS instrument_name,
    i.kind AS instrument_kind,
    i.quote_currency_code,
    i.quantity_scale,
    SUM(it.position_effect * it.quantity_units) AS net_quantity_units,
    SUM(CASE WHEN it.trade_kind = 'buy' THEN it.quantity_units ELSE 0 END) AS bought_quantity_units,
    SUM(CASE WHEN it.trade_kind = 'sell' THEN it.quantity_units ELSE 0 END) AS sold_quantity_units
FROM investment_trades it
JOIN transactions t ON t.id = it.transaction_id
JOIN investment_instruments i ON i.id = it.instrument_id
WHERE t.status = 'posted'
GROUP BY t.ledger_id, it.account_id, it.instrument_id, i.name, i.kind, i.quote_currency_code, i.quantity_scale;

-- 只输出已实现盈亏输入，最终盈亏和收益率公式由 Rust 计算策略负责。
CREATE VIEW v_investment_realized_profit_inputs AS
SELECT
    t.ledger_id,
    t.business_date,
    it.id AS sell_trade_id,
    it.account_id,
    it.instrument_id,
    i.name AS instrument_name,
    it.quantity_units AS sold_quantity_units,
    it.price_units,
    it.price_scale,
    COALESCE(SUM(la.quantity_units), 0) AS allocated_quantity_units,
    COALESCE(SUM(la.allocated_cost_minor), 0) AS allocated_cost_minor,
    COALESCE(SUM(la.allocated_proceeds_minor), 0) AS allocated_proceeds_minor
FROM investment_trades it
JOIN transactions t ON t.id = it.transaction_id
JOIN investment_instruments i ON i.id = it.instrument_id
LEFT JOIN investment_lot_allocations la ON la.sell_trade_id = it.id
WHERE t.status = 'posted' AND it.trade_kind = 'sell'
GROUP BY t.ledger_id, t.business_date, it.id, it.account_id, it.instrument_id,
         i.name, it.quantity_units, it.price_units, it.price_scale;
