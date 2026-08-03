ALTER TABLE parties ADD COLUMN category TEXT NOT NULL DEFAULT 'contact_person'
    CHECK (category IN ('family_member', 'contact_person', 'institution'));

ALTER TABLE parties ADD COLUMN contact TEXT
    CHECK (contact IS NULL OR (length(contact) BETWEEN 1 AND 20));

ALTER TABLE parties ADD COLUMN address TEXT
    CHECK (address IS NULL OR (length(address) BETWEEN 1 AND 40));

ALTER TABLE parties ADD COLUMN sex TEXT
    CHECK (sex IS NULL OR sex IN ('male', 'female'));

ALTER TABLE parties ADD COLUMN birthday_calendar TEXT
    CHECK (birthday_calendar IS NULL OR birthday_calendar IN ('gregorian', 'lunar'));

ALTER TABLE parties ADD COLUMN birth_year INTEGER
    CHECK (birth_year IS NULL OR birth_year BETWEEN 1 AND 9999);

ALTER TABLE parties ADD COLUMN birth_month INTEGER
    CHECK (birth_month IS NULL OR birth_month BETWEEN 1 AND 12);

ALTER TABLE parties ADD COLUMN birth_day INTEGER
    CHECK (
        (birthday_calendar IS NULL AND birth_year IS NULL AND birth_month IS NULL AND birth_day IS NULL)
        OR
        (birthday_calendar IS NOT NULL AND birth_year IS NOT NULL AND birth_month IS NOT NULL AND birth_day BETWEEN 1 AND 31)
    );

-- 旧版模型只有 person/institution/other；无法区分的自然人统一迁移为往来人员。
UPDATE parties
SET category = CASE kind
    WHEN 'institution' THEN 'institution'
    ELSE 'contact_person'
END;

PRAGMA user_version = 8;
