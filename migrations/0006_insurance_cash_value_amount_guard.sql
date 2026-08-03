-- 现金价值是非负保单估值；旧程序会把负数静默写成零，目标库改为明确拒绝。
CREATE TRIGGER trg_insurance_cash_value_nonnegative_insert
BEFORE INSERT ON insurance_cash_value_snapshots
FOR EACH ROW
WHEN NEW.value_minor < 0
BEGIN
    SELECT RAISE(ABORT, 'insurance cash value must be nonnegative');
END;

CREATE TRIGGER trg_insurance_cash_value_nonnegative_update
BEFORE UPDATE OF value_minor ON insurance_cash_value_snapshots
FOR EACH ROW
WHEN NEW.value_minor < 0
BEGIN
    SELECT RAISE(ABORT, 'insurance cash value must be nonnegative');
END;

PRAGMA user_version = 6;
