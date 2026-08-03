-- 现金价值允许保存未来估值；当前值必须由调用方传入查询时点，不能直接取最大估值日。
DROP VIEW v_insurance_current_cash_values;

-- 每条快照从估值日起生效，直到同一保单的下一估值日之前；NULL 表示目前没有更晚快照。
CREATE VIEW v_insurance_cash_value_effective_ranges AS
SELECT
    p.ledger_id,
    p.account_id,
    s.policy_id,
    s.valuation_date AS effective_from,
    (
        SELECT MIN(newer.valuation_date)
        FROM insurance_cash_value_snapshots newer
        WHERE newer.policy_id = s.policy_id
          AND newer.valuation_date > s.valuation_date
    ) AS effective_to_exclusive,
    s.value_minor,
    p.currency_code,
    s.version,
    s.updated_at
FROM insurance_cash_value_snapshots s
JOIN insurance_policies p ON p.id = s.policy_id;

PRAGMA user_version = 5;
