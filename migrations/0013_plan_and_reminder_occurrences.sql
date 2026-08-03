-- 计划定义与每次应发生实例分离，避免用 next_due_date 和最后一笔交易覆盖执行、跳过及失败历史。
ALTER TABLE schedules ADD COLUMN max_occurrences INTEGER
    CHECK (max_occurrences IS NULL OR max_occurrences > 0);
ALTER TABLE schedules ADD COLUMN reminder_lead_days INTEGER NOT NULL DEFAULT 0
    CHECK (reminder_lead_days >= 0);
ALTER TABLE schedules ADD COLUMN recurrence_version INTEGER NOT NULL DEFAULT 1
    CHECK (recurrence_version > 0);

-- 提醒条件版本和投递方式必须随规则保存，触发实例再冻结当时的条件与观测值。
ALTER TABLE reminders ADD COLUMN condition_version INTEGER NOT NULL DEFAULT 1
    CHECK (condition_version > 0);
ALTER TABLE reminders ADD COLUMN delivery_mode TEXT NOT NULL DEFAULT 'in_app'
    CHECK (delivery_mode IN ('in_app', 'system_notification', 'both'));

CREATE TABLE schedule_occurrences (
    id TEXT PRIMARY KEY,
    schedule_id TEXT NOT NULL REFERENCES schedules(id) ON DELETE CASCADE,
    due_date TEXT NOT NULL,
    recurrence_version INTEGER NOT NULL CHECK (recurrence_version > 0),
    execution_mode TEXT NOT NULL CHECK (execution_mode IN ('manual', 'automatic')),
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'executing', 'executed', 'skipped', 'failed', 'cancelled')),
    source_snapshot_json TEXT NOT NULL CHECK (json_valid(source_snapshot_json)),
    transaction_id TEXT REFERENCES transactions(id) ON DELETE RESTRICT,
    idempotency_key TEXT NOT NULL,
    attempt_count INTEGER NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
    actioned_at TEXT,
    failure_code TEXT,
    failure_message TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (schedule_id, due_date, recurrence_version),
    UNIQUE (idempotency_key),
    CHECK (
        (status = 'executed' AND transaction_id IS NOT NULL AND actioned_at IS NOT NULL)
        OR (status IN ('skipped', 'cancelled') AND transaction_id IS NULL AND actioned_at IS NOT NULL)
        OR (status IN ('pending', 'executing', 'failed') AND transaction_id IS NULL)
    ),
    CHECK (
        (status = 'failed' AND failure_code IS NOT NULL)
        OR (status <> 'failed' AND failure_code IS NULL AND failure_message IS NULL)
    )
) STRICT;

CREATE TABLE reminder_occurrences (
    id TEXT PRIMARY KEY,
    reminder_id TEXT NOT NULL REFERENCES reminders(id) ON DELETE CASCADE,
    trigger_at TEXT NOT NULL,
    condition_version INTEGER NOT NULL CHECK (condition_version > 0),
    condition_snapshot_json TEXT NOT NULL CHECK (json_valid(condition_snapshot_json)),
    observed_value_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(observed_value_json)),
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'acknowledged', 'dismissed', 'expired')),
    action_kind TEXT CHECK (action_kind IN ('open_detail', 'disable_rule', 'acknowledge', 'dismiss')),
    actioned_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (reminder_id, trigger_at, condition_version),
    CHECK (
        (status = 'pending' AND action_kind IS NULL AND actioned_at IS NULL)
        OR (status <> 'pending' AND action_kind IS NOT NULL AND actioned_at IS NOT NULL)
    )
) STRICT;

CREATE INDEX idx_schedule_occurrences_due_status
    ON schedule_occurrences (status, due_date, schedule_id);
CREATE INDEX idx_schedule_occurrences_schedule_status
    ON schedule_occurrences (schedule_id, status, due_date);
CREATE INDEX idx_reminder_occurrences_trigger_status
    ON reminder_occurrences (status, trigger_at, reminder_id);
CREATE INDEX idx_reminder_occurrences_rule_status
    ON reminder_occurrences (reminder_id, status, trigger_at);

CREATE VIEW v_pending_schedule_occurrences AS
SELECT
    s.ledger_id,
    o.id AS occurrence_id,
    o.schedule_id,
    s.name AS schedule_name,
    o.due_date,
    o.execution_mode,
    o.recurrence_version,
    o.source_snapshot_json,
    s.reminder_lead_days,
    o.attempt_count
FROM schedule_occurrences o
JOIN schedules s ON s.id = o.schedule_id
WHERE s.status = 'active' AND o.status = 'pending';

CREATE VIEW v_schedule_lifecycle AS
SELECT
    s.ledger_id,
    s.id AS schedule_id,
    s.name,
    s.status,
    s.execution_mode,
    s.start_date,
    s.end_date,
    s.next_due_date,
    s.max_occurrences,
    s.reminder_lead_days,
    s.recurrence_version,
    COUNT(o.id) AS occurrence_count,
    COALESCE(SUM(CASE WHEN o.status = 'executed' THEN 1 ELSE 0 END), 0) AS executed_count,
    COALESCE(SUM(CASE WHEN o.status = 'skipped' THEN 1 ELSE 0 END), 0) AS skipped_count,
    COALESCE(SUM(CASE WHEN o.status = 'failed' THEN 1 ELSE 0 END), 0) AS failed_count,
    MIN(CASE WHEN o.status = 'pending' THEN o.due_date END) AS next_pending_due_date,
    MAX(CASE WHEN o.status = 'executed' THEN o.actioned_at END) AS last_executed_at
FROM schedules s
LEFT JOIN schedule_occurrences o ON o.schedule_id = s.id
GROUP BY s.id;

-- 今日提醒统一投影计划实例和阈值触发实例，执行与跳过能力只属于计划实例。
CREATE VIEW v_today_reminder_inbox AS
SELECT
    s.ledger_id,
    o.id AS inbox_item_id,
    'schedule' AS source_kind,
    o.schedule_id AS source_id,
    s.name AS title,
    o.due_date AS due_at,
    o.status,
    1 AS can_execute,
    1 AS can_skip,
    o.source_snapshot_json AS details_json
FROM schedule_occurrences o
JOIN schedules s ON s.id = o.schedule_id
WHERE o.status = 'pending'
UNION ALL
SELECT
    r.ledger_id,
    o.id AS inbox_item_id,
    'reminder' AS source_kind,
    o.reminder_id AS source_id,
    r.name AS title,
    o.trigger_at AS due_at,
    o.status,
    0 AS can_execute,
    0 AS can_skip,
    json_object(
        'condition', json(o.condition_snapshot_json),
        'observed_value', json(o.observed_value_json)
    ) AS details_json
FROM reminder_occurrences o
JOIN reminders r ON r.id = o.reminder_id
WHERE o.status = 'pending';

PRAGMA user_version = 13;
