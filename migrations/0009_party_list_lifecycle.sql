-- 旧版人员与机构列表在三个分类之间共享同一名称空间，隐藏记录也继续占用名称。
CREATE UNIQUE INDEX idx_parties_ledger_name_unique
ON parties(ledger_id, name);

-- 列表按账簿、分类和隐藏状态读取，再按名称稳定排序。
CREATE INDEX idx_parties_ledger_category_hidden_name
ON parties(ledger_id, category, is_archived, name);

PRAGMA user_version = 9;
