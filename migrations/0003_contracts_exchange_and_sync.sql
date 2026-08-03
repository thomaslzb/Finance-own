PRAGMA foreign_keys = ON;

-- 设置值使用带版本 JSON，允许应用级与账簿级配置共用同一结构。
CREATE TABLE application_settings (
    id TEXT PRIMARY KEY,
    scope_kind TEXT NOT NULL CHECK (scope_kind IN ('application', 'ledger')),
    ledger_id TEXT REFERENCES ledgers(id) ON DELETE CASCADE,
    setting_key TEXT NOT NULL CHECK (length(trim(setting_key)) > 0),
    schema_version INTEGER NOT NULL DEFAULT 1 CHECK (schema_version > 0),
    value_json TEXT NOT NULL CHECK (json_valid(value_json)),
    updated_at TEXT NOT NULL,
    CHECK (
        (scope_kind = 'application' AND ledger_id IS NULL)
        OR (scope_kind = 'ledger' AND ledger_id IS NOT NULL)
    )
) STRICT;

-- 债务合同只保存期限、利率等条款；本金收付和还款仍写入交易分录。
CREATE TABLE debt_contracts (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    account_id TEXT NOT NULL REFERENCES accounts(id),
    counterparty_id TEXT REFERENCES parties(id),
    contract_kind TEXT NOT NULL,
    principal_minor INTEGER NOT NULL CHECK (principal_minor >= 0),
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    annual_rate_units INTEGER CHECK (annual_rate_units >= 0),
    annual_rate_scale INTEGER CHECK (annual_rate_scale BETWEEN 0 AND 12),
    started_on TEXT NOT NULL,
    due_on TEXT,
    repayment_rule_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(repayment_rule_json)),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('draft', 'active', 'settled', 'cancelled')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK ((annual_rate_units IS NULL) = (annual_rate_scale IS NULL)),
    CHECK (due_on IS NULL OR due_on >= started_on),
    UNIQUE (account_id)
) STRICT;

-- 信用账户条款不保存账单累计值，账单金额必须由交易和账期投影重建。
CREATE TABLE credit_account_terms (
    account_id TEXT PRIMARY KEY REFERENCES accounts(id),
    credit_limit_minor INTEGER NOT NULL DEFAULT 0 CHECK (credit_limit_minor >= 0),
    statement_day INTEGER NOT NULL CHECK (statement_day BETWEEN 1 AND 31),
    due_day INTEGER NOT NULL CHECK (due_day BETWEEN 1 AND 31),
    grace_days INTEGER NOT NULL DEFAULT 0 CHECK (grace_days BETWEEN 0 AND 366),
    annual_rate_units INTEGER CHECK (annual_rate_units >= 0),
    annual_rate_scale INTEGER CHECK (annual_rate_scale BETWEEN 0 AND 12),
    minimum_payment_rule_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(minimum_payment_rule_json)),
    updated_at TEXT NOT NULL,
    CHECK ((annual_rate_units IS NULL) = (annual_rate_scale IS NULL))
) STRICT;

-- 期货标的的合约乘数、最小变动和保证金规则独立于通用成交表。
CREATE TABLE futures_contract_terms (
    instrument_id TEXT PRIMARY KEY REFERENCES investment_instruments(id),
    underlying_code TEXT,
    contract_multiplier_units INTEGER NOT NULL CHECK (contract_multiplier_units > 0),
    contract_multiplier_scale INTEGER NOT NULL CHECK (contract_multiplier_scale BETWEEN 0 AND 12),
    tick_size_units INTEGER NOT NULL CHECK (tick_size_units > 0),
    tick_size_scale INTEGER NOT NULL CHECK (tick_size_scale BETWEEN 0 AND 12),
    initial_margin_units INTEGER CHECK (initial_margin_units >= 0),
    initial_margin_scale INTEGER CHECK (initial_margin_scale BETWEEN 0 AND 12),
    settlement_kind TEXT NOT NULL CHECK (settlement_kind IN ('cash', 'physical')),
    expires_on TEXT,
    rule_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(rule_json)),
    updated_at TEXT NOT NULL,
    CHECK ((initial_margin_units IS NULL) = (initial_margin_scale IS NULL))
) STRICT;

-- 融资融券账户条款用于风险提示，实时负债和担保比例由账户、持仓与行情投影计算。
CREATE TABLE margin_account_terms (
    account_id TEXT PRIMARY KEY REFERENCES accounts(id),
    credit_line_minor INTEGER NOT NULL DEFAULT 0 CHECK (credit_line_minor >= 0),
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    maintenance_ratio_units INTEGER CHECK (maintenance_ratio_units >= 0),
    maintenance_ratio_scale INTEGER CHECK (maintenance_ratio_scale BETWEEN 0 AND 12),
    terms_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(terms_json)),
    updated_at TEXT NOT NULL,
    CHECK ((maintenance_ratio_units IS NULL) = (maintenance_ratio_scale IS NULL))
) STRICT;

-- 单笔融资或融券合同保存额度与期限，实际资金和证券变化仍由交易与成交表达。
CREATE TABLE margin_contracts (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    account_id TEXT NOT NULL REFERENCES accounts(id),
    instrument_id TEXT REFERENCES investment_instruments(id),
    contract_kind TEXT NOT NULL CHECK (contract_kind IN ('financing', 'security_lending')),
    principal_minor INTEGER CHECK (principal_minor >= 0),
    currency_code TEXT REFERENCES currencies(code),
    quantity_units INTEGER CHECK (quantity_units >= 0),
    quantity_scale INTEGER CHECK (quantity_scale BETWEEN 0 AND 12),
    annual_rate_units INTEGER CHECK (annual_rate_units >= 0),
    annual_rate_scale INTEGER CHECK (annual_rate_scale BETWEEN 0 AND 12),
    opened_on TEXT NOT NULL,
    due_on TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('draft', 'active', 'settled', 'cancelled')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK ((principal_minor IS NULL) = (currency_code IS NULL)),
    CHECK ((quantity_units IS NULL) = (quantity_scale IS NULL)),
    CHECK ((annual_rate_units IS NULL) = (annual_rate_scale IS NULL)),
    CHECK (due_on IS NULL OR due_on >= opened_on)
) STRICT;

-- 实物资产属性与通用投资标的分离，估值继续使用 market_quotes 的时点来源记录。
CREATE TABLE tangible_asset_details (
    instrument_id TEXT PRIMARY KEY REFERENCES investment_instruments(id),
    acquired_on TEXT,
    acquisition_amount_minor INTEGER CHECK (acquisition_amount_minor >= 0),
    acquisition_currency_code TEXT REFERENCES currencies(code),
    location_label TEXT,
    identifier_masked TEXT,
    attributes_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(attributes_json)),
    updated_at TEXT NOT NULL,
    CHECK ((acquisition_amount_minor IS NULL) = (acquisition_currency_code IS NULL))
) STRICT;

-- 保单条款保存保障和缴费约定；保费、领取和退保资金必须落为普通交易。
CREATE TABLE insurance_policies (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    account_id TEXT REFERENCES accounts(id),
    insurer_party_id TEXT REFERENCES parties(id),
    policy_number_masked TEXT,
    policy_kind TEXT NOT NULL,
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    coverage_amount_minor INTEGER CHECK (coverage_amount_minor >= 0),
    premium_amount_minor INTEGER CHECK (premium_amount_minor >= 0),
    started_on TEXT NOT NULL,
    expires_on TEXT,
    payment_rule_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(payment_rule_json)),
    benefit_rule_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(benefit_rule_json)),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('draft', 'active', 'paid_up', 'expired', 'surrendered', 'cancelled')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (expires_on IS NULL OR expires_on >= started_on)
) STRICT;

-- 社保参数是地区和时期相关的输入快照，缴费与领取仍通过账户分录记录。
CREATE TABLE social_security_profiles (
    account_id TEXT PRIMARY KEY REFERENCES accounts(id),
    region_code TEXT NOT NULL,
    contribution_base_minor INTEGER CHECK (contribution_base_minor >= 0),
    currency_code TEXT REFERENCES currencies(code),
    employee_rate_units INTEGER CHECK (employee_rate_units >= 0),
    employee_rate_scale INTEGER CHECK (employee_rate_scale BETWEEN 0 AND 12),
    employer_rate_units INTEGER CHECK (employer_rate_units >= 0),
    employer_rate_scale INTEGER CHECK (employer_rate_scale BETWEEN 0 AND 12),
    retirement_date TEXT,
    rule_snapshot_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(rule_snapshot_json)),
    updated_at TEXT NOT NULL,
    CHECK ((contribution_base_minor IS NULL) = (currency_code IS NULL)),
    CHECK ((employee_rate_units IS NULL) = (employee_rate_scale IS NULL)),
    CHECK ((employer_rate_units IS NULL) = (employer_rate_scale IS NULL))
) STRICT;

-- 字段映射保存可复用的解析口径，不记录来源文件的敏感内容。
CREATE TABLE import_field_mappings (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    source_kind TEXT NOT NULL,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    schema_version INTEGER NOT NULL DEFAULT 1 CHECK (schema_version > 0),
    mapping_json TEXT NOT NULL CHECK (json_valid(mapping_json)),
    duplicate_rule_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(duplicate_rule_json)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (ledger_id, source_kind, name)
) STRICT;

-- 导入批次只保存显示名与内容哈希，避免把机器绝对路径写入账簿。
CREATE TABLE import_batches (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    mapping_id TEXT REFERENCES import_field_mappings(id) ON DELETE SET NULL,
    source_kind TEXT NOT NULL,
    source_display_name TEXT NOT NULL,
    source_sha256 TEXT NOT NULL CHECK (length(source_sha256) = 64),
    status TEXT NOT NULL DEFAULT 'staged' CHECK (status IN ('staged', 'validated', 'committed', 'failed', 'cancelled')),
    total_rows INTEGER NOT NULL DEFAULT 0 CHECK (total_rows >= 0),
    accepted_rows INTEGER NOT NULL DEFAULT 0 CHECK (accepted_rows >= 0),
    rejected_rows INTEGER NOT NULL DEFAULT 0 CHECK (rejected_rows >= 0),
    duplicate_rows INTEGER NOT NULL DEFAULT 0 CHECK (duplicate_rows >= 0),
    created_at TEXT NOT NULL,
    committed_at TEXT,
    CHECK (accepted_rows + rejected_rows + duplicate_rows <= total_rows),
    UNIQUE (ledger_id, source_kind, source_sha256)
) STRICT;

-- 原始行和规范化结果同时保留，保证预览、错误修正与最终提交可追溯。
CREATE TABLE import_rows (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL REFERENCES import_batches(id) ON DELETE CASCADE,
    row_no INTEGER NOT NULL CHECK (row_no > 0),
    raw_json TEXT NOT NULL CHECK (json_valid(raw_json)),
    normalized_json TEXT CHECK (normalized_json IS NULL OR json_valid(normalized_json)),
    error_json TEXT CHECK (error_json IS NULL OR json_valid(error_json)),
    row_status TEXT NOT NULL DEFAULT 'pending' CHECK (row_status IN ('pending', 'accepted', 'rejected', 'duplicate', 'committed')),
    resolved_entity_kind TEXT,
    resolved_entity_id TEXT,
    CHECK ((resolved_entity_kind IS NULL) = (resolved_entity_id IS NULL)),
    UNIQUE (batch_id, row_no)
) STRICT;

-- 同步配置只能保存非秘密参数；令牌和凭据必须由系统凭据存储或外部适配器管理。
CREATE TABLE sync_profiles (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    provider_kind TEXT NOT NULL,
    display_name TEXT NOT NULL CHECK (length(trim(display_name)) > 0),
    remote_ledger_id TEXT,
    device_id TEXT NOT NULL,
    config_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(config_json)),
    status TEXT NOT NULL DEFAULT 'disabled' CHECK (status IN ('disabled', 'active', 'paused', 'error')),
    last_cursor TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (ledger_id, provider_kind, display_name)
) STRICT;

-- 同步批次记录游标推进和汇总结果，不影响本地账簿独立写入。
CREATE TABLE sync_batches (
    id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL REFERENCES sync_profiles(id),
    direction TEXT NOT NULL CHECK (direction IN ('push', 'pull', 'bidirectional')),
    status TEXT NOT NULL DEFAULT 'running' CHECK (status IN ('running', 'completed', 'partial', 'failed', 'cancelled')),
    cursor_before TEXT,
    cursor_after TEXT,
    attempted_objects INTEGER NOT NULL DEFAULT 0 CHECK (attempted_objects >= 0),
    succeeded_objects INTEGER NOT NULL DEFAULT 0 CHECK (succeeded_objects >= 0),
    failed_objects INTEGER NOT NULL DEFAULT 0 CHECK (failed_objects >= 0),
    conflict_objects INTEGER NOT NULL DEFAULT 0 CHECK (conflict_objects >= 0),
    started_at TEXT NOT NULL,
    completed_at TEXT,
    CHECK (succeeded_objects + failed_objects + conflict_objects <= attempted_objects)
) STRICT;

-- 对象级结果用于重试和审计，不把远端响应覆盖进本地真相表。
CREATE TABLE sync_object_results (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL REFERENCES sync_batches(id) ON DELETE CASCADE,
    entity_kind TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    operation TEXT NOT NULL CHECK (operation IN ('upsert', 'delete')),
    result_status TEXT NOT NULL CHECK (result_status IN ('succeeded', 'failed', 'conflict', 'skipped')),
    remote_version TEXT,
    error_json TEXT CHECK (error_json IS NULL OR json_valid(error_json)),
    UNIQUE (batch_id, entity_kind, entity_id, operation)
) STRICT;

-- 冲突同时保存本地和远端快照，必须由明确策略或用户选择后才能关闭。
CREATE TABLE sync_conflicts (
    id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL REFERENCES sync_profiles(id),
    entity_kind TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    local_revision TEXT,
    remote_revision TEXT,
    local_json TEXT NOT NULL CHECK (json_valid(local_json)),
    remote_json TEXT NOT NULL CHECK (json_valid(remote_json)),
    resolution TEXT CHECK (resolution IN ('keep_local', 'keep_remote', 'merge', 'dismiss')),
    resolved_json TEXT CHECK (resolved_json IS NULL OR json_valid(resolved_json)),
    detected_at TEXT NOT NULL,
    resolved_at TEXT,
    CHECK ((resolution IS NULL) = (resolved_at IS NULL))
) STRICT;

-- 墓碑用于传播删除，保留到远端确认后再由维护任务清理。
CREATE TABLE sync_tombstones (
    id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL REFERENCES sync_profiles(id),
    entity_kind TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    local_revision TEXT NOT NULL,
    deleted_at TEXT NOT NULL,
    pushed_at TEXT,
    UNIQUE (profile_id, entity_kind, entity_id)
) STRICT;

-- 投递日志与提醒真相分离，删除提醒后仍保留发送结果和失败原因。
CREATE TABLE notification_delivery_log (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    reminder_id TEXT REFERENCES reminders(id) ON DELETE SET NULL,
    channel TEXT NOT NULL CHECK (channel IN ('in_app', 'system', 'email', 'sms', 'webhook', 'other')),
    destination_masked TEXT,
    delivery_status TEXT NOT NULL CHECK (delivery_status IN ('queued', 'sent', 'failed', 'cancelled')),
    attempt_no INTEGER NOT NULL DEFAULT 1 CHECK (attempt_no > 0),
    requested_at TEXT NOT NULL,
    completed_at TEXT,
    next_retry_at TEXT,
    provider_reference TEXT,
    error_json TEXT CHECK (error_json IS NULL OR json_valid(error_json))
) STRICT;

-- 费用规则是外部参考输入快照，交易最终费用仍以 fee 分录为准。
CREATE TABLE fee_rule_snapshots (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    source_name TEXT NOT NULL,
    rule_kind TEXT NOT NULL,
    effective_from TEXT,
    effective_to TEXT,
    rate_units INTEGER CHECK (rate_units >= 0),
    rate_scale INTEGER CHECK (rate_scale BETWEEN 0 AND 12),
    parameters_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(parameters_json)),
    source_sha256 TEXT CHECK (source_sha256 IS NULL OR length(source_sha256) = 64),
    captured_at TEXT NOT NULL,
    CHECK ((rate_units IS NULL) = (rate_scale IS NULL)),
    CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_to >= effective_from)
) STRICT;

CREATE UNIQUE INDEX ux_application_settings_scope_key
    ON application_settings (scope_kind, COALESCE(ledger_id, ''), setting_key);
CREATE INDEX idx_debt_contracts_status_due
    ON debt_contracts (ledger_id, status, due_on);
CREATE INDEX idx_margin_contracts_account_status
    ON margin_contracts (account_id, status, due_on);
CREATE INDEX idx_insurance_policies_status_date
    ON insurance_policies (ledger_id, status, expires_on);
CREATE INDEX idx_import_field_mappings_lookup
    ON import_field_mappings (ledger_id, source_kind, name);
CREATE INDEX idx_import_batches_status_created
    ON import_batches (ledger_id, status, created_at DESC);
CREATE INDEX idx_import_rows_batch_status
    ON import_rows (batch_id, row_status, row_no);
CREATE INDEX idx_sync_profiles_status
    ON sync_profiles (ledger_id, status, provider_kind);
CREATE INDEX idx_sync_batches_profile_started
    ON sync_batches (profile_id, started_at DESC);
CREATE INDEX idx_sync_object_results_status
    ON sync_object_results (batch_id, result_status, entity_kind);
CREATE INDEX idx_sync_conflicts_open
    ON sync_conflicts (profile_id, resolved_at, detected_at DESC);
CREATE INDEX idx_sync_tombstones_pending
    ON sync_tombstones (profile_id, pushed_at, deleted_at);
CREATE INDEX idx_notification_delivery_retry
    ON notification_delivery_log (delivery_status, next_retry_at, requested_at);
CREATE INDEX idx_fee_rule_snapshots_lookup
    ON fee_rule_snapshots (ledger_id, rule_kind, effective_from DESC, captured_at DESC);

-- 债务页面只消费合同与账户输入，余额和已还金额由交易投影在应用层组合。
CREATE VIEW v_debt_contract_inputs AS
SELECT
    dc.id AS debt_contract_id,
    dc.ledger_id,
    dc.account_id,
    a.name AS account_name,
    dc.counterparty_id,
    p.name AS counterparty_name,
    dc.contract_kind,
    dc.principal_minor,
    dc.currency_code,
    dc.annual_rate_units,
    dc.annual_rate_scale,
    dc.started_on,
    dc.due_on,
    dc.status
FROM debt_contracts dc
JOIN accounts a ON a.id = dc.account_id
LEFT JOIN parties p ON p.id = dc.counterparty_id;

-- 导入审计视图提供批次计数与逐行状态聚合，不复制最终业务对象。
CREATE VIEW v_import_batch_audit AS
SELECT
    b.id AS batch_id,
    b.ledger_id,
    b.source_kind,
    b.source_display_name,
    b.source_sha256,
    b.status,
    b.total_rows,
    b.accepted_rows,
    b.rejected_rows,
    b.duplicate_rows,
    COUNT(r.id) AS staged_row_count,
    SUM(CASE WHEN r.row_status = 'committed' THEN 1 ELSE 0 END) AS committed_row_count
FROM import_batches b
LEFT JOIN import_rows r ON r.batch_id = b.id
GROUP BY b.id;

-- 未解决同步冲突按检测时间返回，UI 必须显式展示而不能静默覆盖。
CREATE VIEW v_open_sync_conflicts AS
SELECT
    c.id AS conflict_id,
    p.ledger_id,
    c.profile_id,
    c.entity_kind,
    c.entity_id,
    c.local_revision,
    c.remote_revision,
    c.local_json,
    c.remote_json,
    c.detected_at
FROM sync_conflicts c
JOIN sync_profiles p ON p.id = c.profile_id
WHERE c.resolved_at IS NULL;

PRAGMA user_version = 3;
