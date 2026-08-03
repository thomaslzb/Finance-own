-- 在线利率先进入不可变批次，整批校验通过后才允许发布为当前参考数据。
CREATE TABLE deposit_rate_update_batches (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    source TEXT NOT NULL CHECK (source IN ('online', 'legacy_import')),
    status TEXT NOT NULL DEFAULT 'staged' CHECK (
        status IN ('staged', 'published', 'failed', 'cancelled')
    ),
    requested_at TEXT NOT NULL,
    completed_at TEXT,
    received_count INTEGER NOT NULL DEFAULT 0 CHECK (received_count >= 0),
    valid_count INTEGER NOT NULL DEFAULT 0 CHECK (
        valid_count >= 0 AND valid_count <= received_count
    ),
    published_count INTEGER NOT NULL DEFAULT 0 CHECK (
        published_count >= 0 AND published_count <= valid_count
    ),
    error_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (id, ledger_id),
    CHECK (
        (status = 'staged' AND completed_at IS NULL AND published_count = 0)
        OR
        (status = 'published' AND completed_at IS NOT NULL
            AND received_count = valid_count AND valid_count = published_count)
        OR
        (status IN ('failed', 'cancelled') AND completed_at IS NOT NULL
            AND published_count = 0)
    )
) STRICT;

-- 批次明细保留原始文本和校验结果，失败批次不能通过跳过坏行形成部分发布。
CREATE TABLE deposit_rate_update_items (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL REFERENCES deposit_rate_update_batches(id) ON DELETE CASCADE,
    line_no INTEGER NOT NULL CHECK (line_no > 0),
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    deposit_type TEXT NOT NULL,
    term_code TEXT NOT NULL,
    raw_rate_text TEXT NOT NULL,
    annual_rate_units INTEGER,
    annual_rate_scale INTEGER,
    validation_status TEXT NOT NULL CHECK (
        validation_status IN ('valid', 'invalid', 'duplicate')
    ),
    validation_error TEXT,
    created_at TEXT NOT NULL,
    UNIQUE (batch_id, line_no),
    UNIQUE (id, batch_id),
    CHECK ((annual_rate_units IS NULL) = (annual_rate_scale IS NULL)),
    CHECK (annual_rate_units IS NULL OR annual_rate_units >= 0),
    CHECK (annual_rate_scale IS NULL OR annual_rate_scale BETWEEN 0 AND 12),
    CHECK (
        annual_rate_units IS NULL OR annual_rate_units <= CASE annual_rate_scale
            WHEN 0 THEN 100
            WHEN 1 THEN 1000
            WHEN 2 THEN 10000
            WHEN 3 THEN 100000
            WHEN 4 THEN 1000000
            WHEN 5 THEN 10000000
            WHEN 6 THEN 100000000
            WHEN 7 THEN 1000000000
            WHEN 8 THEN 10000000000
            WHEN 9 THEN 100000000000
            WHEN 10 THEN 1000000000000
            WHEN 11 THEN 10000000000000
            WHEN 12 THEN 100000000000000
        END
    ),
    CHECK (
        (validation_status = 'valid' AND annual_rate_units IS NOT NULL
            AND validation_error IS NULL)
        OR
        (validation_status <> 'valid' AND validation_error IS NOT NULL)
    )
) STRICT;

-- 已发布版本不可原位覆盖；存单和历史计算保存其实际采用的版本或独立快照。
CREATE TABLE deposit_rate_versions (
    id TEXT PRIMARY KEY,
    ledger_id TEXT NOT NULL REFERENCES ledgers(id) ON DELETE CASCADE,
    currency_code TEXT NOT NULL REFERENCES currencies(code),
    deposit_type TEXT NOT NULL,
    term_code TEXT NOT NULL,
    annual_rate_units INTEGER NOT NULL CHECK (annual_rate_units >= 0),
    annual_rate_scale INTEGER NOT NULL CHECK (annual_rate_scale BETWEEN 0 AND 12),
    effective_at TEXT NOT NULL,
    source TEXT NOT NULL CHECK (source IN ('manual', 'online', 'legacy_import')),
    batch_id TEXT,
    source_item_id TEXT,
    version INTEGER NOT NULL CHECK (version > 0),
    supersedes_id TEXT REFERENCES deposit_rate_versions(id),
    created_at TEXT NOT NULL,
    UNIQUE (ledger_id, currency_code, deposit_type, term_code, version),
    UNIQUE (source_item_id),
    FOREIGN KEY (batch_id, ledger_id)
        REFERENCES deposit_rate_update_batches(id, ledger_id),
    FOREIGN KEY (source_item_id, batch_id)
        REFERENCES deposit_rate_update_items(id, batch_id),
    CHECK (
        (source = 'manual' AND batch_id IS NULL AND source_item_id IS NULL)
        OR
        (source IN ('online', 'legacy_import')
            AND batch_id IS NOT NULL AND source_item_id IS NOT NULL)
    ),
    CHECK (supersedes_id IS NULL OR supersedes_id <> id),
    CHECK (annual_rate_units <= CASE annual_rate_scale
        WHEN 0 THEN 100
        WHEN 1 THEN 1000
        WHEN 2 THEN 10000
        WHEN 3 THEN 100000
        WHEN 4 THEN 1000000
        WHEN 5 THEN 10000000
        WHEN 6 THEN 100000000
        WHEN 7 THEN 1000000000
        WHEN 8 THEN 10000000000
        WHEN 9 THEN 100000000000
        WHEN 10 THEN 1000000000000
        WHEN 11 THEN 10000000000000
        WHEN 12 THEN 100000000000000
    END)
) STRICT;

-- 发布动作按实际明细复核计数，避免调用方仅修改汇总数字绕过坏行。
CREATE TRIGGER trg_deposit_rate_batches_publish_validate
BEFORE UPDATE OF status ON deposit_rate_update_batches
WHEN NEW.status = 'published' AND OLD.status <> 'published'
BEGIN
    SELECT CASE WHEN
        (SELECT COUNT(*) FROM deposit_rate_update_items WHERE batch_id = NEW.id)
            <> NEW.received_count
        OR
        (SELECT COUNT(*) FROM deposit_rate_update_items
         WHERE batch_id = NEW.id AND validation_status = 'valid')
            <> NEW.valid_count
        OR NEW.received_count <> NEW.valid_count
        OR NEW.valid_count <> NEW.published_count
    THEN RAISE(ABORT, 'deposit rate batch contains unpublished or invalid items') END;
END;

-- 已发布批次和明细是在线利率版本的审计依据，发布后不得原位改写。
CREATE TRIGGER trg_deposit_rate_batches_published_immutable
BEFORE UPDATE ON deposit_rate_update_batches
WHEN OLD.status = 'published'
BEGIN
    SELECT RAISE(ABORT, 'published deposit rate batch is immutable');
END;

CREATE TRIGGER trg_deposit_rate_items_published_immutable
BEFORE UPDATE ON deposit_rate_update_items
WHEN EXISTS (
    SELECT 1
    FROM deposit_rate_update_batches batch
    WHERE batch.id = OLD.batch_id AND batch.status = 'published'
)
BEGIN
    SELECT RAISE(ABORT, 'published deposit rate item is immutable');
END;

-- 在线或导入版本只能来自同账簿、已发布且内容完全一致的有效明细。
CREATE TRIGGER trg_deposit_rate_versions_source_guard
BEFORE INSERT ON deposit_rate_versions
WHEN NEW.source IN ('online', 'legacy_import')
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1
        FROM deposit_rate_update_batches batch
        JOIN deposit_rate_update_items item ON item.batch_id = batch.id
        WHERE batch.id = NEW.batch_id
          AND batch.ledger_id = NEW.ledger_id
          AND batch.source = NEW.source
          AND batch.status = 'published'
          AND item.id = NEW.source_item_id
          AND item.validation_status = 'valid'
          AND item.currency_code = NEW.currency_code
          AND item.deposit_type = NEW.deposit_type
          AND item.term_code = NEW.term_code
          AND item.annual_rate_units = NEW.annual_rate_units
          AND item.annual_rate_scale = NEW.annual_rate_scale
    ) THEN RAISE(ABORT, 'deposit rate version source is not a matching published item') END;
END;

-- 业务修订必须追加新版本，不能覆盖已经被存单或审计引用的历史值。
CREATE TRIGGER trg_deposit_rate_versions_immutable
BEFORE UPDATE ON deposit_rate_versions
BEGIN
    SELECT RAISE(ABORT, 'deposit rate version is immutable');
END;

CREATE INDEX idx_deposit_rate_batches_ledger_status_requested
    ON deposit_rate_update_batches (ledger_id, status, requested_at DESC);

CREATE INDEX idx_deposit_rate_items_batch_status_key
    ON deposit_rate_update_items (
        batch_id, validation_status, currency_code, deposit_type, term_code
    );

CREATE INDEX idx_deposit_rate_versions_lookup
    ON deposit_rate_versions (
        ledger_id, currency_code, deposit_type, term_code,
        effective_at DESC, version DESC
    );

-- 当前矩阵只读取每个业务键的最近有效版本，历史版本继续供存单和审计追溯。
CREATE VIEW v_current_deposit_rates AS
WITH ranked AS (
    SELECT
        drv.*,
        ROW_NUMBER() OVER (
            PARTITION BY ledger_id, currency_code, deposit_type, term_code
            ORDER BY effective_at DESC, version DESC, created_at DESC, id DESC
        ) AS row_rank
    FROM deposit_rate_versions drv
)
SELECT
    id AS deposit_rate_version_id,
    ledger_id,
    currency_code,
    deposit_type,
    term_code,
    annual_rate_units,
    annual_rate_scale,
    effective_at,
    source,
    batch_id,
    source_item_id,
    version,
    supersedes_id
FROM ranked
WHERE row_rank = 1;

PRAGMA user_version = 11;
