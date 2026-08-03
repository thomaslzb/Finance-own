use std::{
    fs,
    path::{Path, PathBuf},
};

use rusqlite::{
    params, params_from_iter,
    types::{Type, Value},
    Connection, Error as RusqliteError, ErrorCode, OpenFlags, Row, TransactionBehavior,
};

use crate::{
    app::{
        planning::{
            BudgetChanges, FinancialGoalChanges, NewBudget, NewBudgetItem, NewFinancialGoal,
            NewReminder, NewSchedule, PlanningDataError, PlanningRepository, ReminderChanges,
            ScheduleChanges,
        },
        reference_data::{
            AccountChanges, AccountGroupChanges, CategoryChanges, DeletedAccountGroup,
            InitializeLedgerRequest, InitializedLedger, NewAccount, NewAccountGroup, NewCategory,
            NewParty, NewTag, PartyChanges, ReferenceDataError, ReferenceDataRepository,
            TagChanges,
        },
        reporting::{
            DateRange, InvestmentProjectionFilter, LedgerEntryFilter, ReportReadError,
            ReportReadRepository,
        },
        transactions::{CreatedTransaction, TransactionWriteError, TransactionWriteRepository},
    },
    domain::{
        money::ScaledValue,
        planning::{
            BudgetItemRecord, BudgetPeriodKind, BudgetRecord, BudgetRolloverMode, BudgetStatus,
            FinancialGoalAccountScopeMode, FinancialGoalProgressMode, FinancialGoalRecord,
            FinancialGoalStatus, ReminderDeliveryMode, ReminderRecord, ReminderStatus,
            ScheduleExecutionMode, ScheduleRecord, ScheduleStatus,
        },
        reference_data::{
            AccountGroupRecord, AccountRecord, BirthdayCalendar, CategoryDirection, CategoryRecord,
            LedgerRecord, PartyBirthday, PartyKind, PartyRecord, PersonSex, TagRecord,
        },
        reporting::{
            AccountBalanceProjection, InvestmentPositionInput, LedgerEntryProjection,
            RealizedProfitInput, RunningBalanceProjection, TaggedAssetProjection,
            TaggedLedgerEntryProjection,
        },
        transactions::{
            EntryDirection, NewTransaction, NewTransactionStatus, TransactionEntryRole,
            TransactionKind,
        },
    },
};

/// SQLite 核心交易迁移脚本。
pub const CORE_SCHEMA: &str = include_str!("../../migrations/0001_core.sql");

/// 模板、计划、预算、提醒、目标和规划输入迁移脚本。
pub const PLANNING_AND_AUTOMATION_SCHEMA: &str =
    include_str!("../../migrations/0002_planning_and_automation.sql");

/// 专属合同、导入审计、同步冲突和外部适配器边界迁移脚本。
pub const CONTRACTS_EXCHANGE_AND_SYNC_SCHEMA: &str =
    include_str!("../../migrations/0003_contracts_exchange_and_sync.sql");

/// 保险现金价值快照、变更历史和旧版最新记录视图迁移脚本。
pub const INSURANCE_CASH_VALUE_SCHEMA: &str =
    include_str!("../../migrations/0004_insurance_cash_value.sql");

/// 保险现金价值按查询时点选择有效快照的迁移脚本。
pub const INSURANCE_CASH_VALUE_AS_OF_SCHEMA: &str =
    include_str!("../../migrations/0005_insurance_cash_value_as_of.sql");

/// 保险现金价值非负金额约束迁移脚本。
pub const INSURANCE_CASH_VALUE_AMOUNT_GUARD_SCHEMA: &str =
    include_str!("../../migrations/0006_insurance_cash_value_amount_guard.sql");

/// 工资收入复合明细和 Finance Own SQLite 文件标识迁移脚本。
pub const PAYROLL_INCOME_AND_APPLICATION_IDENTITY_SCHEMA: &str =
    include_str!("../../migrations/0007_payroll_income_and_application_identity.sql");

/// 人员与机构精确分类、联系方式、地址、性别和生日迁移脚本。
pub const PARTY_PROFILE_SCHEMA: &str = include_str!("../../migrations/0008_party_profile.sql");

/// 人员与机构全局名称唯一性、隐藏列表和排序索引迁移脚本。
pub const PARTY_LIST_LIFECYCLE_SCHEMA: &str =
    include_str!("../../migrations/0009_party_list_lifecycle.sql");

/// 待摊费用主体、确定性摊销期次和概况投影迁移脚本。
pub const PREPAID_EXPENSES_SCHEMA: &str =
    include_str!("../../migrations/0010_prepaid_expenses.sql");

/// 存款利率抓取批次、校验明细、不可变版本和当前有效投影迁移脚本。
pub const DEPOSIT_RATE_VERSIONS_SCHEMA: &str =
    include_str!("../../migrations/0011_deposit_rate_versions.sql");

/// 财务目标开始日期、初始估值快照和进度输入视图迁移脚本。
pub const FINANCIAL_GOAL_PROGRESS_BASELINE_SCHEMA: &str =
    include_str!("../../migrations/0012_financial_goal_progress_baseline.sql");

/// 计划执行实例、提醒触发实例和今日提醒统一投影迁移脚本。
pub const PLAN_AND_REMINDER_OCCURRENCES_SCHEMA: &str =
    include_str!("../../migrations/0013_plan_and_reminder_occurrences.sql");

/// 新建或升级账簿时必须按顺序执行的全部迁移。
pub const MIGRATIONS: &[&str] = &[
    CORE_SCHEMA,
    PLANNING_AND_AUTOMATION_SCHEMA,
    CONTRACTS_EXCHANGE_AND_SYNC_SCHEMA,
    INSURANCE_CASH_VALUE_SCHEMA,
    INSURANCE_CASH_VALUE_AS_OF_SCHEMA,
    INSURANCE_CASH_VALUE_AMOUNT_GUARD_SCHEMA,
    PAYROLL_INCOME_AND_APPLICATION_IDENTITY_SCHEMA,
    PARTY_PROFILE_SCHEMA,
    PARTY_LIST_LIFECYCLE_SCHEMA,
    PREPAID_EXPENSES_SCHEMA,
    DEPOSIT_RATE_VERSIONS_SCHEMA,
    FINANCIAL_GOAL_PROGRESS_BASELINE_SCHEMA,
    PLAN_AND_REMINDER_OCCURRENCES_SCHEMA,
];

/// 当前代码能够完整读取和写入的 SQLite 模式版本。
pub const CURRENT_SCHEMA_VERSION: i64 = 13;

/// SQLite 文件头中的 Finance Own 应用标识，对应 ASCII `FOWN`。
pub const EXPECTED_APPLICATION_ID: i64 = 1_179_604_814;

/// 新格式 SQLite 账簿的位置。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SqliteLedgerLocation {
    /// SQLite 单文件账簿的完整路径。
    pub path: PathBuf,
}

impl SqliteLedgerLocation {
    /// 构造新格式账簿位置；此方法不创建或修改文件。
    pub fn new(path: impl AsRef<Path>) -> Self {
        Self {
            path: path.as_ref().to_path_buf(),
        }
    }
}

/// SQLite 账簿创建或打开失败。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SqliteLedgerError {
    /// 创建目标已经存在，调用方必须显式选择其它路径或进入打开流程。
    AlreadyExists,
    /// 打开目标不存在。
    NotFound,
    /// 文件系统或 SQLite 操作失败；消息不得包含密钥。
    Storage(String),
    /// 账簿模式版本不受当前代码支持。
    UnsupportedSchemaVersion {
        /// 文件中的 `PRAGMA user_version`。
        found: i64,
        /// 当前代码要求的版本。
        expected: i64,
    },
    /// SQLite 文件不是 Finance Own 账簿，避免把其它应用数据库误当作财务文件打开。
    InvalidApplicationId {
        /// 文件头中实际读取到的 `PRAGMA application_id`。
        found: i64,
        /// Finance Own 固定要求的应用标识。
        expected: i64,
    },
    /// SQLite 完整性检查未返回 `ok`。
    IntegrityCheckFailed(String),
}

/// SQLite 新账簿、交易写入和只读投影的首个具体适配器。
pub struct SqliteLedgerStore {
    connection: Connection,
    location: Option<SqliteLedgerLocation>,
}

impl SqliteLedgerStore {
    /// 创建全新账簿并在一个事务中执行全部迁移。
    ///
    /// 迁移失败时会关闭连接并删除本次创建的半成品文件。已存在目标不会被覆盖。
    pub fn create(location: SqliteLedgerLocation) -> Result<Self, SqliteLedgerError> {
        if location.path.exists() {
            return Err(SqliteLedgerError::AlreadyExists);
        }
        if let Some(parent) = location.path.parent() {
            fs::create_dir_all(parent).map_err(storage_error)?;
        }

        let connection = Connection::open_with_flags(
            &location.path,
            OpenFlags::SQLITE_OPEN_READ_WRITE | OpenFlags::SQLITE_OPEN_CREATE,
        )
        .map_err(storage_error)?;
        let mut store = Self {
            connection,
            location: Some(location.clone()),
        };
        if let Err(error) = store.configure_and_migrate() {
            drop(store);
            let _ = fs::remove_file(&location.path);
            return Err(error);
        }
        Ok(store)
    }

    /// 打开已有账簿并验证模式版本、外键和快速完整性结果。
    pub fn open(location: SqliteLedgerLocation) -> Result<Self, SqliteLedgerError> {
        if !location.path.is_file() {
            return Err(SqliteLedgerError::NotFound);
        }
        let connection =
            Connection::open_with_flags(&location.path, OpenFlags::SQLITE_OPEN_READ_WRITE)
                .map_err(storage_error)?;
        let store = Self {
            connection,
            location: Some(location),
        };
        store.configure_connection()?;
        store.migrate_supported_schema()?;
        store.verify_schema_and_integrity()?;
        Ok(store)
    }

    /// 返回当前文件位置；内存测试账簿返回 `None`。
    pub fn location(&self) -> Option<&SqliteLedgerLocation> {
        self.location.as_ref()
    }

    /// 返回账簿当前 `PRAGMA user_version`。
    pub fn schema_version(&self) -> Result<i64, SqliteLedgerError> {
        self.connection
            .query_row("PRAGMA user_version", [], |row| row.get(0))
            .map_err(storage_error)
    }

    /// 返回 SQLite 文件头中的 Finance Own 应用标识。
    pub fn application_id(&self) -> Result<i64, SqliteLedgerError> {
        self.connection
            .query_row("PRAGMA application_id", [], |row| row.get(0))
            .map_err(storage_error)
    }

    #[cfg(test)]
    fn create_in_memory() -> Result<Self, SqliteLedgerError> {
        let connection = Connection::open_in_memory().map_err(storage_error)?;
        let mut store = Self {
            connection,
            location: None,
        };
        store.configure_and_migrate()?;
        Ok(store)
    }

    fn configure_connection(&self) -> Result<(), SqliteLedgerError> {
        self.connection
            .execute_batch(
                "PRAGMA foreign_keys = ON;\nPRAGMA busy_timeout = 5000;\nPRAGMA synchronous = FULL;\nPRAGMA trusted_schema = OFF;",
            )
            .map_err(storage_error)
    }

    fn configure_and_migrate(&mut self) -> Result<(), SqliteLedgerError> {
        self.configure_connection()?;
        self.connection
            .execute_batch("BEGIN IMMEDIATE")
            .map_err(storage_error)?;
        for migration in MIGRATIONS {
            if let Err(error) = self.connection.execute_batch(migration) {
                let _ = self.connection.execute_batch("ROLLBACK");
                return Err(storage_error(error));
            }
        }
        if let Err(error) = self.connection.execute_batch("COMMIT") {
            let _ = self.connection.execute_batch("ROLLBACK");
            return Err(storage_error(error));
        }
        self.verify_schema_and_integrity()
    }

    fn migrate_supported_schema(&self) -> Result<(), SqliteLedgerError> {
        let found = self.schema_version()?;
        if found == CURRENT_SCHEMA_VERSION {
            return Ok(());
        }
        if !matches!(found, 6 | 7 | 8 | 9 | 10 | 11 | 12) {
            return Err(SqliteLedgerError::UnsupportedSchemaVersion {
                found,
                expected: CURRENT_SCHEMA_VERSION,
            });
        }

        if found == 6 {
            // v1-v6 尚未写入 application_id，只允许具备核心表指纹的已知前序版本升级。
            let legacy_core_objects: i64 = self
                .connection
                .query_row(
                    "SELECT COUNT(*) FROM sqlite_schema \
                     WHERE type = 'table' AND name IN ('ledgers', 'transactions', 'transaction_entries')",
                    [],
                    |row| row.get(0),
                )
                .map_err(storage_error)?;
            if legacy_core_objects != 3 {
                return Err(SqliteLedgerError::IntegrityCheckFailed(
                    "version 6 schema fingerprint is incomplete".to_owned(),
                ));
            }
        } else {
            let application_id = self.application_id()?;
            if application_id != EXPECTED_APPLICATION_ID {
                return Err(SqliteLedgerError::InvalidApplicationId {
                    found: application_id,
                    expected: EXPECTED_APPLICATION_ID,
                });
            }
        }

        self.connection
            .execute_batch("BEGIN IMMEDIATE")
            .map_err(storage_error)?;
        for migration in &MIGRATIONS[found as usize..] {
            if let Err(error) = self.connection.execute_batch(migration) {
                let _ = self.connection.execute_batch("ROLLBACK");
                return Err(storage_error(error));
            }
        }
        if let Err(error) = self.connection.execute_batch("COMMIT") {
            let _ = self.connection.execute_batch("ROLLBACK");
            return Err(storage_error(error));
        }
        Ok(())
    }

    fn verify_schema_and_integrity(&self) -> Result<(), SqliteLedgerError> {
        let found = self.schema_version()?;
        if found != CURRENT_SCHEMA_VERSION {
            return Err(SqliteLedgerError::UnsupportedSchemaVersion {
                found,
                expected: CURRENT_SCHEMA_VERSION,
            });
        }
        let application_id = self.application_id()?;
        if application_id != EXPECTED_APPLICATION_ID {
            return Err(SqliteLedgerError::InvalidApplicationId {
                found: application_id,
                expected: EXPECTED_APPLICATION_ID,
            });
        }
        let quick_check: String = self
            .connection
            .query_row("PRAGMA quick_check", [], |row| row.get(0))
            .map_err(storage_error)?;
        if quick_check != "ok" {
            return Err(SqliteLedgerError::IntegrityCheckFailed(quick_check));
        }
        let foreign_key_violations: i64 = self
            .connection
            .query_row("SELECT COUNT(*) FROM pragma_foreign_key_check", [], |row| {
                row.get(0)
            })
            .map_err(storage_error)?;
        if foreign_key_violations != 0 {
            return Err(SqliteLedgerError::IntegrityCheckFailed(format!(
                "foreign_key_check returned {foreign_key_violations} row(s)"
            )));
        }
        Ok(())
    }
}

impl ReferenceDataRepository for SqliteLedgerStore {
    fn initialize_ledger(
        &mut self,
        request: &InitializeLedgerRequest,
    ) -> Result<InitializedLedger, ReferenceDataError> {
        let transaction = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(reference_data_storage_error)?;
        let result = (|| -> Result<InitializedLedger, RusqliteError> {
            let ledger_id = random_id(&transaction)?;
            let initial_account_id = random_id(&transaction)?;
            transaction.execute(
                "INSERT INTO currencies(code, name, minor_unit) VALUES (?1, ?2, ?3)",
                params![
                    request.base_currency.code,
                    request.base_currency.name,
                    i64::from(request.base_currency.minor_unit),
                ],
            )?;
            transaction.execute(
                "INSERT INTO ledgers(id, name, base_currency_code, created_at, updated_at) \
                 VALUES (?1, ?2, ?3, ?4, ?4)",
                params![
                    ledger_id,
                    request.name,
                    request.base_currency.code,
                    request.created_at,
                ],
            )?;
            transaction.execute(
                "INSERT INTO accounts(\
                    id, ledger_id, name, kind, currency_code, is_asset, created_at\
                 ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
                params![
                    initial_account_id,
                    ledger_id,
                    request.initial_account.name,
                    request.initial_account.kind,
                    request.base_currency.code,
                    bool_to_integer(request.initial_account.is_asset),
                    request.created_at,
                ],
            )?;
            Ok(InitializedLedger {
                ledger_id,
                initial_account_id,
            })
        })();

        match result {
            Ok(initialized) => {
                transaction.commit().map_err(reference_data_storage_error)?;
                Ok(initialized)
            }
            Err(error) => Err(reference_data_storage_error(error)),
        }
    }

    fn get_ledger(&self, ledger_id: &str) -> Result<LedgerRecord, ReferenceDataError> {
        validate_reference_id(ledger_id, "账簿标识")?;
        self.connection
            .query_row(
                "SELECT id, name, base_currency_code, created_at, updated_at \
                 FROM ledgers WHERE id = ?1",
                [ledger_id],
                |row| {
                    Ok(LedgerRecord {
                        id: row.get(0)?,
                        name: row.get(1)?,
                        base_currency_code: row.get(2)?,
                        created_at: row.get(3)?,
                        updated_at: row.get(4)?,
                    })
                },
            )
            .map_err(|error| reference_data_query_error(error, "账簿不存在"))
    }

    fn create_account_group(
        &mut self,
        group: &NewAccountGroup,
    ) -> Result<String, ReferenceDataError> {
        validate_reference_id(&group.ledger_id, "账簿标识")?;
        validate_reference_name(&group.name, "账户组名称")?;
        validate_reference_name(&group.kind, "账户组类型")?;
        ensure_optional_reference_in_ledger(
            &self.connection,
            group.parent_id.as_deref(),
            &group.ledger_id,
            "account_groups",
            "父账户组",
        )?;
        let group_id = random_connection_id(&self.connection)?;
        self.connection
            .execute(
                "INSERT INTO account_groups(id, ledger_id, parent_id, name, kind, sort_order)\
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
                params![
                    group_id,
                    group.ledger_id,
                    group.parent_id,
                    group.name,
                    group.kind,
                    group.sort_order,
                ],
            )
            .map_err(reference_data_storage_error)?;
        Ok(group_id)
    }

    fn update_account_group(
        &mut self,
        changes: &AccountGroupChanges,
    ) -> Result<(), ReferenceDataError> {
        validate_reference_id(&changes.id, "账户组标识")?;
        validate_reference_id(&changes.ledger_id, "账簿标识")?;
        validate_reference_name(&changes.name, "账户组名称")?;
        validate_reference_name(&changes.kind, "账户组类型")?;
        if changes.parent_id.as_deref() == Some(changes.id.as_str()) {
            return Err(ReferenceDataError::InvalidInput(
                "账户组不能将自身设为父组".to_owned(),
            ));
        }
        ensure_optional_reference_in_ledger(
            &self.connection,
            changes.parent_id.as_deref(),
            &changes.ledger_id,
            "account_groups",
            "父账户组",
        )?;
        ensure_parent_is_not_descendant(
            &self.connection,
            "account_groups",
            &changes.ledger_id,
            &changes.id,
            changes.parent_id.as_deref(),
            "账户组",
        )?;
        let changed = self
            .connection
            .execute(
                "UPDATE account_groups SET parent_id = ?1, name = ?2, kind = ?3, sort_order = ?4\
                 WHERE id = ?5 AND ledger_id = ?6",
                params![
                    changes.parent_id,
                    changes.name,
                    changes.kind,
                    changes.sort_order,
                    changes.id,
                    changes.ledger_id,
                ],
            )
            .map_err(reference_data_storage_error)?;
        ensure_reference_updated(changed, "账户组不存在")
    }

    fn list_account_groups(
        &self,
        ledger_id: &str,
    ) -> Result<Vec<AccountGroupRecord>, ReferenceDataError> {
        validate_reference_id(ledger_id, "账簿标识")?;
        let mut statement = self
            .connection
            .prepare(
                "SELECT id, ledger_id, parent_id, name, kind, sort_order \
                 FROM account_groups WHERE ledger_id = ?1 \
                 ORDER BY sort_order, name, id",
            )
            .map_err(reference_data_storage_error)?;
        let rows = statement
            .query_map([ledger_id], |row| {
                Ok(AccountGroupRecord {
                    id: row.get(0)?,
                    ledger_id: row.get(1)?,
                    parent_id: row.get(2)?,
                    name: row.get(3)?,
                    kind: row.get(4)?,
                    sort_order: row.get(5)?,
                })
            })
            .map_err(reference_data_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(reference_data_storage_error)
    }

    fn delete_account_group(
        &mut self,
        ledger_id: &str,
        group_id: &str,
    ) -> Result<DeletedAccountGroup, ReferenceDataError> {
        validate_reference_id(ledger_id, "账簿标识")?;
        validate_reference_id(group_id, "账户组标识")?;
        let transaction = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(reference_data_storage_error)?;
        let parent_id: Option<String> = transaction
            .query_row(
                "SELECT parent_id FROM account_groups WHERE id = ?1 AND ledger_id = ?2",
                params![group_id, ledger_id],
                |row| row.get(0),
            )
            .map_err(|error| reference_data_query_error(error, "账户组不存在"))?;
        let result = (|| -> Result<DeletedAccountGroup, RusqliteError> {
            let reassigned_accounts = transaction.execute(
                "UPDATE accounts SET group_id = ?1 WHERE ledger_id = ?2 AND group_id = ?3",
                params![parent_id, ledger_id, group_id],
            )?;
            let reassigned_child_groups = transaction.execute(
                "UPDATE account_groups SET parent_id = ?1\
                 WHERE ledger_id = ?2 AND parent_id = ?3",
                params![parent_id, ledger_id, group_id],
            )?;
            transaction.execute(
                "DELETE FROM account_groups WHERE id = ?1 AND ledger_id = ?2",
                params![group_id, ledger_id],
            )?;
            Ok(DeletedAccountGroup {
                group_id: group_id.to_owned(),
                reassigned_accounts,
                reassigned_child_groups,
            })
        })();
        match result {
            Ok(deleted) => {
                transaction.commit().map_err(reference_data_storage_error)?;
                Ok(deleted)
            }
            Err(error) => Err(reference_data_storage_error(error)),
        }
    }

    fn create_account(&mut self, account: &NewAccount) -> Result<String, ReferenceDataError> {
        validate_reference_name(&account.ledger_id, "账簿标识")?;
        validate_reference_name(&account.name, "账户名称")?;
        validate_reference_name(&account.kind, "账户类型")?;
        validate_reference_name(&account.currency_code, "账户币种")?;
        validate_reference_name(&account.created_at, "创建时间")?;
        ensure_optional_reference_in_ledger(
            &self.connection,
            account.group_id.as_deref(),
            &account.ledger_id,
            "account_groups",
            "账户组",
        )?;
        let account_id = random_connection_id(&self.connection)?;
        self.connection
            .execute(
                "INSERT INTO accounts(\
                    id, ledger_id, group_id, name, kind, currency_code, institution_name,\
                    account_number_masked, is_asset, created_at\
                 ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10)",
                params![
                    account_id,
                    account.ledger_id,
                    account.group_id,
                    account.name,
                    account.kind,
                    account.currency_code,
                    account.institution_name,
                    account.account_number_masked,
                    bool_to_integer(account.is_asset),
                    account.created_at,
                ],
            )
            .map_err(reference_data_storage_error)?;
        Ok(account_id)
    }

    fn update_account(&mut self, changes: &AccountChanges) -> Result<(), ReferenceDataError> {
        validate_reference_id(&changes.id, "账户标识")?;
        validate_reference_id(&changes.ledger_id, "账簿标识")?;
        validate_reference_name(&changes.name, "账户名称")?;
        validate_reference_name(&changes.kind, "账户类型")?;
        ensure_optional_reference_in_ledger(
            &self.connection,
            changes.group_id.as_deref(),
            &changes.ledger_id,
            "account_groups",
            "账户组",
        )?;
        let changed = self
            .connection
            .execute(
                "UPDATE accounts SET group_id = ?1, name = ?2, kind = ?3, institution_name = ?4,\
                    account_number_masked = ?5, is_hidden = ?6, closed_on = ?7\
                 WHERE id = ?8 AND ledger_id = ?9",
                params![
                    changes.group_id,
                    changes.name,
                    changes.kind,
                    changes.institution_name,
                    changes.account_number_masked,
                    bool_to_integer(changes.is_hidden),
                    changes.closed_on,
                    changes.id,
                    changes.ledger_id,
                ],
            )
            .map_err(reference_data_storage_error)?;
        ensure_reference_updated(changed, "账户不存在")
    }

    fn list_accounts(&self, ledger_id: &str) -> Result<Vec<AccountRecord>, ReferenceDataError> {
        validate_reference_id(ledger_id, "账簿标识")?;
        let mut statement = self
            .connection
            .prepare(
                "SELECT id, ledger_id, group_id, name, kind, currency_code, institution_name,\
                    account_number_masked, is_asset, is_hidden, closed_on, created_at \
                 FROM accounts WHERE ledger_id = ?1 ORDER BY is_hidden, name, id",
            )
            .map_err(reference_data_storage_error)?;
        let rows = statement
            .query_map([ledger_id], |row| {
                Ok(AccountRecord {
                    id: row.get(0)?,
                    ledger_id: row.get(1)?,
                    group_id: row.get(2)?,
                    name: row.get(3)?,
                    kind: row.get(4)?,
                    currency_code: row.get(5)?,
                    institution_name: row.get(6)?,
                    account_number_masked: row.get(7)?,
                    is_asset: row.get::<_, i64>(8)? != 0,
                    is_hidden: row.get::<_, i64>(9)? != 0,
                    closed_on: row.get(10)?,
                    created_at: row.get(11)?,
                })
            })
            .map_err(reference_data_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(reference_data_storage_error)
    }

    fn create_category(&mut self, category: &NewCategory) -> Result<String, ReferenceDataError> {
        validate_reference_id(&category.ledger_id, "账簿标识")?;
        validate_reference_name(&category.name, "分类名称")?;
        ensure_optional_reference_in_ledger(
            &self.connection,
            category.parent_id.as_deref(),
            &category.ledger_id,
            "categories",
            "父分类",
        )?;
        let category_id = random_connection_id(&self.connection)?;
        self.connection
            .execute(
                "INSERT INTO categories(\
                    id, ledger_id, parent_id, name, direction, sort_order\
                 ) VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
                params![
                    category_id,
                    category.ledger_id,
                    category.parent_id,
                    category.name,
                    category_direction_key(category.direction),
                    category.sort_order,
                ],
            )
            .map_err(reference_data_storage_error)?;
        Ok(category_id)
    }

    fn update_category(&mut self, changes: &CategoryChanges) -> Result<(), ReferenceDataError> {
        validate_reference_id(&changes.id, "分类标识")?;
        validate_reference_id(&changes.ledger_id, "账簿标识")?;
        validate_reference_name(&changes.name, "分类名称")?;
        if changes.parent_id.as_deref() == Some(changes.id.as_str()) {
            return Err(ReferenceDataError::InvalidInput(
                "分类不能将自身设为父分类".to_owned(),
            ));
        }
        ensure_optional_reference_in_ledger(
            &self.connection,
            changes.parent_id.as_deref(),
            &changes.ledger_id,
            "categories",
            "父分类",
        )?;
        ensure_parent_is_not_descendant(
            &self.connection,
            "categories",
            &changes.ledger_id,
            &changes.id,
            changes.parent_id.as_deref(),
            "分类",
        )?;
        let changed = self
            .connection
            .execute(
                "UPDATE categories SET parent_id = ?1, name = ?2, direction = ?3,\
                    sort_order = ?4, is_archived = ?5\
                 WHERE id = ?6 AND ledger_id = ?7",
                params![
                    changes.parent_id,
                    changes.name,
                    category_direction_key(changes.direction),
                    changes.sort_order,
                    bool_to_integer(changes.is_archived),
                    changes.id,
                    changes.ledger_id,
                ],
            )
            .map_err(reference_data_storage_error)?;
        ensure_reference_updated(changed, "分类不存在")
    }

    fn list_categories(&self, ledger_id: &str) -> Result<Vec<CategoryRecord>, ReferenceDataError> {
        validate_reference_id(ledger_id, "账簿标识")?;
        let mut statement = self
            .connection
            .prepare(
                "SELECT id, ledger_id, parent_id, name, direction, sort_order, is_archived \
                 FROM categories WHERE ledger_id = ?1 \
                 ORDER BY is_archived, sort_order, name, id",
            )
            .map_err(reference_data_storage_error)?;
        let rows = statement
            .query_map([ledger_id], |row| {
                let direction: String = row.get(4)?;
                Ok(CategoryRecord {
                    id: row.get(0)?,
                    ledger_id: row.get(1)?,
                    parent_id: row.get(2)?,
                    name: row.get(3)?,
                    direction: category_direction_from_key(&direction, 4)?,
                    sort_order: row.get(5)?,
                    is_archived: row.get::<_, i64>(6)? != 0,
                })
            })
            .map_err(reference_data_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(reference_data_storage_error)
    }

    fn create_tag(&mut self, tag: &NewTag) -> Result<String, ReferenceDataError> {
        validate_reference_id(&tag.ledger_id, "账簿标识")?;
        validate_reference_name(&tag.name, "标签名称")?;
        let tag_id = random_connection_id(&self.connection)?;
        self.connection
            .execute(
                "INSERT INTO tags(id, ledger_id, name, color) VALUES (?1, ?2, ?3, ?4)",
                params![tag_id, tag.ledger_id, tag.name, tag.color],
            )
            .map_err(reference_data_storage_error)?;
        Ok(tag_id)
    }

    fn update_tag(&mut self, changes: &TagChanges) -> Result<(), ReferenceDataError> {
        validate_reference_id(&changes.id, "标签标识")?;
        validate_reference_id(&changes.ledger_id, "账簿标识")?;
        validate_reference_name(&changes.name, "标签名称")?;
        let changed = self
            .connection
            .execute(
                "UPDATE tags SET name = ?1, color = ?2, is_archived = ?3\
                 WHERE id = ?4 AND ledger_id = ?5",
                params![
                    changes.name,
                    changes.color,
                    bool_to_integer(changes.is_archived),
                    changes.id,
                    changes.ledger_id,
                ],
            )
            .map_err(reference_data_storage_error)?;
        ensure_reference_updated(changed, "标签不存在")
    }

    fn list_tags(&self, ledger_id: &str) -> Result<Vec<TagRecord>, ReferenceDataError> {
        validate_reference_id(ledger_id, "账簿标识")?;
        let mut statement = self
            .connection
            .prepare(
                "SELECT id, ledger_id, name, color, is_archived FROM tags \
                 WHERE ledger_id = ?1 ORDER BY is_archived, name, id",
            )
            .map_err(reference_data_storage_error)?;
        let rows = statement
            .query_map([ledger_id], |row| {
                Ok(TagRecord {
                    id: row.get(0)?,
                    ledger_id: row.get(1)?,
                    name: row.get(2)?,
                    color: row.get(3)?,
                    is_archived: row.get::<_, i64>(4)? != 0,
                })
            })
            .map_err(reference_data_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(reference_data_storage_error)
    }

    fn create_party(&mut self, party: &NewParty) -> Result<String, ReferenceDataError> {
        validate_reference_id(&party.ledger_id, "账簿标识")?;
        validate_party_profile(
            &party.name,
            party.kind,
            party.contact.as_deref(),
            party.address.as_deref(),
            party.sex,
            party.birthday,
        )?;
        let party_id = random_connection_id(&self.connection)?;
        self.connection
            .execute(
                "INSERT INTO parties(\
                    id, ledger_id, name, kind, category, contact, address, sex, \
                    birthday_calendar, birth_year, birth_month, birth_day\
                 ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12)",
                params![
                    party_id,
                    party.ledger_id,
                    party.name,
                    legacy_party_kind_key(party.kind),
                    party_kind_key(party.kind),
                    party.contact,
                    party.address,
                    party.sex.map(party_sex_key),
                    party
                        .birthday
                        .map(|birthday| birthday_calendar_key(birthday.calendar)),
                    party.birthday.map(|birthday| i64::from(birthday.year)),
                    party.birthday.map(|birthday| i64::from(birthday.month)),
                    party.birthday.map(|birthday| i64::from(birthday.day)),
                ],
            )
            .map_err(reference_data_storage_error)?;
        Ok(party_id)
    }

    fn update_party(&mut self, changes: &PartyChanges) -> Result<(), ReferenceDataError> {
        validate_reference_id(&changes.id, "往来方标识")?;
        validate_reference_id(&changes.ledger_id, "账簿标识")?;
        validate_party_profile(
            &changes.name,
            changes.kind,
            changes.contact.as_deref(),
            changes.address.as_deref(),
            changes.sex,
            changes.birthday,
        )?;
        let changed = self
            .connection
            .execute(
                "UPDATE parties SET \
                    name = ?1, kind = ?2, category = ?3, contact = ?4, address = ?5, \
                    sex = ?6, birthday_calendar = ?7, birth_year = ?8, birth_month = ?9, \
                    birth_day = ?10, is_archived = ?11 \
                 WHERE id = ?12 AND ledger_id = ?13",
                params![
                    changes.name,
                    legacy_party_kind_key(changes.kind),
                    party_kind_key(changes.kind),
                    changes.contact,
                    changes.address,
                    changes.sex.map(party_sex_key),
                    changes
                        .birthday
                        .map(|birthday| birthday_calendar_key(birthday.calendar)),
                    changes.birthday.map(|birthday| i64::from(birthday.year)),
                    changes.birthday.map(|birthday| i64::from(birthday.month)),
                    changes.birthday.map(|birthday| i64::from(birthday.day)),
                    bool_to_integer(changes.is_hidden),
                    changes.id,
                    changes.ledger_id,
                ],
            )
            .map_err(reference_data_storage_error)?;
        ensure_reference_updated(changed, "往来方不存在")
    }

    fn list_parties(&self, ledger_id: &str) -> Result<Vec<PartyRecord>, ReferenceDataError> {
        validate_reference_id(ledger_id, "账簿标识")?;
        let mut statement = self
            .connection
            .prepare(
                "SELECT \
                    id, ledger_id, name, category, contact, address, sex, birthday_calendar, \
                    birth_year, birth_month, birth_day, is_archived \
                 FROM parties WHERE ledger_id = ?1 \
                 ORDER BY is_archived, name, category, id",
            )
            .map_err(reference_data_storage_error)?;
        let rows = statement
            .query_map([ledger_id], |row| {
                let kind: String = row.get(3)?;
                let sex: Option<String> = row.get(6)?;
                let birthday_calendar: Option<String> = row.get(7)?;
                Ok(PartyRecord {
                    id: row.get(0)?,
                    ledger_id: row.get(1)?,
                    name: row.get(2)?,
                    kind: party_kind_from_key(&kind, 3)?,
                    contact: row.get(4)?,
                    address: row.get(5)?,
                    sex: party_sex_from_key(sex.as_deref(), 6)?,
                    birthday: party_birthday_from_columns(
                        birthday_calendar.as_deref(),
                        row.get(8)?,
                        row.get(9)?,
                        row.get(10)?,
                    )?,
                    is_hidden: row.get::<_, i64>(11)? != 0,
                })
            })
            .map_err(reference_data_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(reference_data_storage_error)
    }
}

impl PlanningRepository for SqliteLedgerStore {
    fn create_budget(&mut self, budget: &NewBudget) -> Result<String, PlanningDataError> {
        validate_planning_name(&budget.ledger_id, "账簿标识")?;
        validate_planning_name(&budget.name, "预算名称")?;
        ensure_ledger_exists(&self.connection, &budget.ledger_id)?;
        for item in &budget.items {
            validate_budget_item_reference(&self.connection, &budget.ledger_id, item)?;
        }

        let transaction = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(planning_storage_error)?;
        let result = (|| -> Result<String, RusqliteError> {
            let budget_id = random_id(&transaction)?;
            transaction.execute(
                "INSERT INTO budgets(
                    id, ledger_id, name, period_kind, start_date, end_date, status, created_at, updated_at
                 ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?8)",
                params![
                    budget_id,
                    budget.ledger_id,
                    budget.name,
                    budget_period_kind_key(budget.period_kind),
                    budget.start_date,
                    budget.end_date,
                    budget_status_key(budget.status),
                    budget.created_at,
                ],
            )?;
            insert_budget_items(&transaction, &budget_id, &budget.items)?;
            Ok(budget_id)
        })();

        match result {
            Ok(budget_id) => {
                transaction.commit().map_err(planning_storage_error)?;
                Ok(budget_id)
            }
            Err(error) => Err(planning_storage_error(error)),
        }
    }

    fn update_budget(&mut self, changes: &BudgetChanges) -> Result<(), PlanningDataError> {
        validate_planning_name(&changes.id, "预算标识")?;
        validate_planning_name(&changes.ledger_id, "账簿标识")?;
        validate_planning_name(&changes.name, "预算名称")?;
        validate_planning_name(&changes.updated_at, "更新时间")?;
        let changed = self
            .connection
            .execute(
                "UPDATE budgets SET
                    name = ?1, period_kind = ?2, start_date = ?3, end_date = ?4,
                    status = ?5, updated_at = ?6
                 WHERE id = ?7 AND ledger_id = ?8",
                params![
                    changes.name,
                    budget_period_kind_key(changes.period_kind),
                    changes.start_date,
                    changes.end_date,
                    budget_status_key(changes.status),
                    changes.updated_at,
                    changes.id,
                    changes.ledger_id,
                ],
            )
            .map_err(planning_storage_error)?;
        ensure_planning_updated(changed, "预算不存在")
    }

    fn list_budgets(&self, ledger_id: &str) -> Result<Vec<BudgetRecord>, PlanningDataError> {
        validate_planning_name(ledger_id, "账簿标识")?;
        let mut statement = self
            .connection
            .prepare(
                "SELECT id, ledger_id, name, period_kind, start_date, end_date, status, created_at, updated_at
                 FROM budgets WHERE ledger_id = ?1
                 ORDER BY start_date, end_date, name, id",
            )
            .map_err(planning_storage_error)?;
        let rows = statement
            .query_map([ledger_id], map_budget_record)
            .map_err(planning_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(planning_storage_error)
    }

    fn list_budget_items(
        &self,
        budget_id: &str,
    ) -> Result<Vec<BudgetItemRecord>, PlanningDataError> {
        validate_planning_name(budget_id, "预算标识")?;
        let mut statement = self
            .connection
            .prepare(
                "SELECT id, budget_id, category_id, period_start, period_end, amount_minor,
                    currency_code, rollover_mode, note
                 FROM budget_items WHERE budget_id = ?1
                 ORDER BY period_start, period_end, category_id, id",
            )
            .map_err(planning_storage_error)?;
        let rows = statement
            .query_map([budget_id], map_budget_item_record)
            .map_err(planning_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(planning_storage_error)
    }

    fn replace_budget_items(
        &mut self,
        ledger_id: &str,
        budget_id: &str,
        items: &[NewBudgetItem],
    ) -> Result<(), PlanningDataError> {
        validate_planning_name(ledger_id, "账簿标识")?;
        validate_planning_name(budget_id, "预算标识")?;
        ensure_budget_in_ledger(&self.connection, ledger_id, budget_id)?;
        for item in items {
            validate_budget_item_reference(&self.connection, ledger_id, item)?;
        }

        let transaction = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(planning_storage_error)?;
        let result = (|| -> Result<(), RusqliteError> {
            transaction.execute("DELETE FROM budget_items WHERE budget_id = ?1", [budget_id])?;
            insert_budget_items(&transaction, budget_id, items)?;
            Ok(())
        })();

        match result {
            Ok(()) => transaction.commit().map_err(planning_storage_error),
            Err(error) => Err(planning_storage_error(error)),
        }
    }

    fn create_financial_goal(
        &mut self,
        goal: &NewFinancialGoal,
    ) -> Result<String, PlanningDataError> {
        validate_planning_name(&goal.ledger_id, "账簿标识")?;
        validate_planning_name(&goal.name, "目标名称")?;
        ensure_ledger_exists(&self.connection, &goal.ledger_id)?;
        ensure_currency_exists(&self.connection, &goal.currency_code)?;
        for account_id in &goal.account_ids {
            ensure_account_in_ledger(&self.connection, &goal.ledger_id, account_id)?;
        }

        let transaction = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(planning_storage_error)?;
        let result = (|| -> Result<String, RusqliteError> {
            let goal_id = random_id(&transaction)?;
            transaction.execute(
                "INSERT INTO financial_goals(
                    id, ledger_id, name, target_amount_minor, currency_code, target_date,
                    progress_mode, status, created_at, updated_at, start_date,
                    initial_value_minor, initial_value_captured_at, initial_inputs_json,
                    account_scope_mode, progress_formula_version
                 ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?9, ?10, ?11, ?12, ?13, ?14, ?15)",
                params![
                    goal_id,
                    goal.ledger_id,
                    goal.name,
                    goal.target_amount_minor,
                    goal.currency_code,
                    goal.target_date,
                    financial_goal_progress_mode_key(goal.progress_mode),
                    financial_goal_status_key(goal.status),
                    goal.created_at,
                    goal.start_date,
                    goal.initial_value_minor,
                    goal.initial_value_captured_at,
                    goal.initial_inputs_json,
                    financial_goal_account_scope_key(goal.account_scope_mode),
                    goal.progress_formula_version,
                ],
            )?;
            insert_financial_goal_accounts(&transaction, &goal_id, &goal.account_ids)?;
            Ok(goal_id)
        })();

        match result {
            Ok(goal_id) => {
                transaction.commit().map_err(planning_storage_error)?;
                Ok(goal_id)
            }
            Err(error) => Err(planning_storage_error(error)),
        }
    }

    fn update_financial_goal(
        &mut self,
        changes: &FinancialGoalChanges,
    ) -> Result<(), PlanningDataError> {
        validate_planning_name(&changes.id, "目标标识")?;
        validate_planning_name(&changes.ledger_id, "账簿标识")?;
        validate_planning_name(&changes.name, "目标名称")?;
        validate_planning_name(&changes.updated_at, "更新时间")?;
        ensure_currency_exists(&self.connection, &changes.currency_code)?;
        let changed = self
            .connection
            .execute(
                "UPDATE financial_goals SET
                    name = ?1, target_amount_minor = ?2, currency_code = ?3, start_date = ?4,
                    target_date = ?5, progress_mode = ?6, status = ?7, account_scope_mode = ?8,
                    progress_formula_version = ?9, updated_at = ?10
                 WHERE id = ?11 AND ledger_id = ?12",
                params![
                    changes.name,
                    changes.target_amount_minor,
                    changes.currency_code,
                    changes.start_date,
                    changes.target_date,
                    financial_goal_progress_mode_key(changes.progress_mode),
                    financial_goal_status_key(changes.status),
                    financial_goal_account_scope_key(changes.account_scope_mode),
                    changes.progress_formula_version,
                    changes.updated_at,
                    changes.id,
                    changes.ledger_id,
                ],
            )
            .map_err(planning_storage_error)?;
        ensure_planning_updated(changed, "财务目标不存在")
    }

    fn list_financial_goals(
        &self,
        ledger_id: &str,
    ) -> Result<Vec<FinancialGoalRecord>, PlanningDataError> {
        validate_planning_name(ledger_id, "账簿标识")?;
        let mut statement = self
            .connection
            .prepare(
                "SELECT id, ledger_id, name, target_amount_minor, currency_code, start_date,
                    target_date, progress_mode, status, initial_value_minor,
                    initial_value_captured_at, initial_inputs_json, account_scope_mode,
                    progress_formula_version, created_at, updated_at
                 FROM financial_goals WHERE ledger_id = ?1
                 ORDER BY COALESCE(target_date, ''), name, id",
            )
            .map_err(planning_storage_error)?;
        let rows = statement
            .query_map([ledger_id], map_financial_goal_record)
            .map_err(planning_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(planning_storage_error)
    }

    fn replace_financial_goal_accounts(
        &mut self,
        ledger_id: &str,
        goal_id: &str,
        account_ids: &[String],
    ) -> Result<(), PlanningDataError> {
        validate_planning_name(ledger_id, "账簿标识")?;
        validate_planning_name(goal_id, "目标标识")?;
        ensure_goal_in_ledger(&self.connection, ledger_id, goal_id)?;
        for account_id in account_ids {
            ensure_account_in_ledger(&self.connection, ledger_id, account_id)?;
        }

        let transaction = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(planning_storage_error)?;
        let result = (|| -> Result<(), RusqliteError> {
            transaction.execute(
                "DELETE FROM financial_goal_accounts WHERE goal_id = ?1",
                [goal_id],
            )?;
            insert_financial_goal_accounts(&transaction, goal_id, account_ids)?;
            Ok(())
        })();

        match result {
            Ok(()) => transaction.commit().map_err(planning_storage_error),
            Err(error) => Err(planning_storage_error(error)),
        }
    }

    fn create_schedule(&mut self, schedule: &NewSchedule) -> Result<String, PlanningDataError> {
        validate_planning_name(&schedule.ledger_id, "账簿标识")?;
        validate_planning_name(&schedule.template_id, "交易模板标识")?;
        validate_planning_name(&schedule.name, "计划名称")?;
        ensure_ledger_exists(&self.connection, &schedule.ledger_id)?;
        ensure_template_in_ledger(&self.connection, &schedule.ledger_id, &schedule.template_id)?;
        let schedule_id = random_planning_id(&self.connection)?;
        self.connection
            .execute(
                "INSERT INTO schedules(
                    id, ledger_id, template_id, name, recurrence_json, start_date, end_date,
                    next_due_date, execution_mode, status, max_occurrences, reminder_lead_days,
                    recurrence_version, created_at, updated_at
                 ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?14)",
                params![
                    schedule_id,
                    schedule.ledger_id,
                    schedule.template_id,
                    schedule.name,
                    schedule.recurrence_json,
                    schedule.start_date,
                    schedule.end_date,
                    schedule.next_due_date,
                    schedule_execution_mode_key(schedule.execution_mode),
                    schedule_status_key(schedule.status),
                    schedule.max_occurrences,
                    schedule.reminder_lead_days,
                    schedule.recurrence_version,
                    schedule.created_at,
                ],
            )
            .map_err(planning_storage_error)?;
        Ok(schedule_id)
    }

    fn update_schedule(&mut self, changes: &ScheduleChanges) -> Result<(), PlanningDataError> {
        validate_planning_name(&changes.id, "计划标识")?;
        validate_planning_name(&changes.ledger_id, "账簿标识")?;
        validate_planning_name(&changes.template_id, "交易模板标识")?;
        validate_planning_name(&changes.name, "计划名称")?;
        validate_planning_name(&changes.updated_at, "更新时间")?;
        ensure_template_in_ledger(&self.connection, &changes.ledger_id, &changes.template_id)?;
        let changed = self
            .connection
            .execute(
                "UPDATE schedules SET
                    template_id = ?1, name = ?2, recurrence_json = ?3, start_date = ?4,
                    end_date = ?5, next_due_date = ?6, execution_mode = ?7, status = ?8,
                    max_occurrences = ?9, reminder_lead_days = ?10, recurrence_version = ?11,
                    updated_at = ?12
                 WHERE id = ?13 AND ledger_id = ?14",
                params![
                    changes.template_id,
                    changes.name,
                    changes.recurrence_json,
                    changes.start_date,
                    changes.end_date,
                    changes.next_due_date,
                    schedule_execution_mode_key(changes.execution_mode),
                    schedule_status_key(changes.status),
                    changes.max_occurrences,
                    changes.reminder_lead_days,
                    changes.recurrence_version,
                    changes.updated_at,
                    changes.id,
                    changes.ledger_id,
                ],
            )
            .map_err(planning_storage_error)?;
        ensure_planning_updated(changed, "计划不存在")
    }

    fn list_schedules(&self, ledger_id: &str) -> Result<Vec<ScheduleRecord>, PlanningDataError> {
        validate_planning_name(ledger_id, "账簿标识")?;
        let mut statement = self
            .connection
            .prepare(
                "SELECT id, ledger_id, template_id, name, recurrence_json, start_date, end_date,
                    next_due_date, execution_mode, status, max_occurrences, reminder_lead_days,
                    recurrence_version, last_generated_transaction_id, created_at, updated_at
                 FROM schedules WHERE ledger_id = ?1
                 ORDER BY COALESCE(next_due_date, start_date), name, id",
            )
            .map_err(planning_storage_error)?;
        let rows = statement
            .query_map([ledger_id], map_schedule_record)
            .map_err(planning_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(planning_storage_error)
    }

    fn create_reminder(&mut self, reminder: &NewReminder) -> Result<String, PlanningDataError> {
        validate_planning_name(&reminder.ledger_id, "账簿标识")?;
        validate_planning_name(&reminder.name, "提醒名称")?;
        validate_planning_name(&reminder.reminder_kind, "提醒类型")?;
        ensure_ledger_exists(&self.connection, &reminder.ledger_id)?;
        let reminder_id = random_planning_id(&self.connection)?;
        self.connection
            .execute(
                "INSERT INTO reminders(
                    id, ledger_id, name, reminder_kind, target_kind, target_id,
                    condition_json, remind_at, recurrence_json, next_trigger_at, status,
                    is_enabled, condition_version, delivery_mode, created_at, updated_at
                 ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?15)",
                params![
                    reminder_id,
                    reminder.ledger_id,
                    reminder.name,
                    reminder.reminder_kind,
                    reminder.target_kind,
                    reminder.target_id,
                    reminder.condition_json,
                    reminder.remind_at,
                    reminder.recurrence_json,
                    reminder.next_trigger_at,
                    reminder_status_key(reminder.status),
                    bool_to_integer(reminder.is_enabled),
                    reminder.condition_version,
                    reminder_delivery_mode_key(reminder.delivery_mode),
                    reminder.created_at,
                ],
            )
            .map_err(planning_storage_error)?;
        Ok(reminder_id)
    }

    fn update_reminder(&mut self, changes: &ReminderChanges) -> Result<(), PlanningDataError> {
        validate_planning_name(&changes.id, "提醒标识")?;
        validate_planning_name(&changes.ledger_id, "账簿标识")?;
        validate_planning_name(&changes.name, "提醒名称")?;
        validate_planning_name(&changes.reminder_kind, "提醒类型")?;
        validate_planning_name(&changes.updated_at, "更新时间")?;
        let changed = self
            .connection
            .execute(
                "UPDATE reminders SET
                    name = ?1, reminder_kind = ?2, target_kind = ?3, target_id = ?4,
                    condition_json = ?5, remind_at = ?6, recurrence_json = ?7,
                    next_trigger_at = ?8, last_triggered_at = ?9, status = ?10,
                    is_enabled = ?11, condition_version = ?12, delivery_mode = ?13,
                    updated_at = ?14
                 WHERE id = ?15 AND ledger_id = ?16",
                params![
                    changes.name,
                    changes.reminder_kind,
                    changes.target_kind,
                    changes.target_id,
                    changes.condition_json,
                    changes.remind_at,
                    changes.recurrence_json,
                    changes.next_trigger_at,
                    changes.last_triggered_at,
                    reminder_status_key(changes.status),
                    bool_to_integer(changes.is_enabled),
                    changes.condition_version,
                    reminder_delivery_mode_key(changes.delivery_mode),
                    changes.updated_at,
                    changes.id,
                    changes.ledger_id,
                ],
            )
            .map_err(planning_storage_error)?;
        ensure_planning_updated(changed, "提醒不存在")
    }

    fn list_reminders(&self, ledger_id: &str) -> Result<Vec<ReminderRecord>, PlanningDataError> {
        validate_planning_name(ledger_id, "账簿标识")?;
        let mut statement = self
            .connection
            .prepare(
                "SELECT id, ledger_id, name, reminder_kind, target_kind, target_id,
                    condition_json, remind_at, recurrence_json, next_trigger_at,
                    last_triggered_at, status, is_enabled, condition_version, delivery_mode,
                    created_at, updated_at
                 FROM reminders WHERE ledger_id = ?1
                 ORDER BY is_enabled DESC, COALESCE(next_trigger_at, remind_at, ''), name, id",
            )
            .map_err(planning_storage_error)?;
        let rows = statement
            .query_map([ledger_id], map_reminder_record)
            .map_err(planning_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(planning_storage_error)
    }
}

impl TransactionWriteRepository for SqliteLedgerStore {
    fn create_transaction(
        &mut self,
        transaction: &NewTransaction,
    ) -> Result<CreatedTransaction, TransactionWriteError> {
        let sqlite_transaction = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(transaction_storage_error)?;
        let result = (|| -> Result<CreatedTransaction, RusqliteError> {
            let sequence_no: i64 = sqlite_transaction.query_row(
                "SELECT COALESCE(MAX(sequence_no), 0) + 1 FROM transactions WHERE ledger_id = ?1",
                [&transaction.ledger_id],
                |row| row.get(0),
            )?;
            let transaction_id = random_id(&sqlite_transaction)?;
            sqlite_transaction.execute(
                "INSERT INTO transactions(\
                    id, ledger_id, sequence_no, business_date, occurred_at, kind, status,\
                    party_id, theme, description, created_at, updated_at\
                 ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?5, ?5)",
                params![
                    transaction_id,
                    transaction.ledger_id,
                    sequence_no,
                    transaction.business_date,
                    transaction.occurred_at,
                    transaction_kind_key(&transaction.kind),
                    transaction_status_key(transaction.status),
                    transaction.party_id,
                    transaction.theme,
                    transaction.description,
                ],
            )?;

            for (entry_index, entry) in transaction.entries.iter().enumerate() {
                let entry_id = random_id(&sqlite_transaction)?;
                sqlite_transaction.execute(
                    "INSERT INTO transaction_entries(\
                        id, transaction_id, account_id, line_no, role, direction,\
                        amount_minor, currency_code, base_amount_minor, base_currency_code,\
                        fx_snapshot_id, category_id, memo\
                     ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13)",
                    params![
                        entry_id,
                        transaction_id,
                        entry.account_id,
                        i64::try_from(entry_index + 1).expect("分录数量不会超过 i64"),
                        entry_role_key(entry.role),
                        entry_direction_key(entry.direction),
                        entry.amount.minor_units,
                        entry.amount.currency_code,
                        entry.base_amount.as_ref().map(|amount| amount.minor_units),
                        entry
                            .base_amount
                            .as_ref()
                            .map(|amount| amount.currency_code.as_str()),
                        entry.fx_snapshot_id,
                        entry.category_id,
                        entry.memo,
                    ],
                )?;
            }

            for tag_id in &transaction.tag_ids {
                sqlite_transaction.execute(
                    "INSERT INTO transaction_tags(transaction_id, tag_id) VALUES (?1, ?2)",
                    params![transaction_id, tag_id],
                )?;
            }
            for attachment_id in &transaction.attachment_ids {
                sqlite_transaction.execute(
                    "INSERT INTO transaction_attachments(transaction_id, attachment_id) VALUES (?1, ?2)",
                    params![transaction_id, attachment_id],
                )?;
            }

            Ok(CreatedTransaction {
                transaction_id,
                sequence_no,
            })
        })();

        match result {
            Ok(created) => {
                sqlite_transaction
                    .commit()
                    .map_err(transaction_storage_error)?;
                Ok(created)
            }
            Err(error) => Err(transaction_storage_error(error)),
        }
    }
}

impl ReportReadRepository for SqliteLedgerStore {
    fn list_ledger_entries(
        &self,
        filter: &LedgerEntryFilter,
    ) -> Result<Vec<LedgerEntryProjection>, ReportReadError> {
        validate_ledger_filter(filter)?;
        let mut values = Vec::new();
        let mut sql = format!(
            "SELECT {} FROM v_ledger_entries le WHERE le.ledger_id = ?",
            ledger_entry_columns("le")
        );
        values.push(Value::Text(filter.ledger_id.clone()));
        append_ledger_entry_filter(&mut sql, &mut values, filter, "le", true);
        sql.push_str(" ORDER BY le.business_date, le.sequence_no, le.line_no, le.entry_id");
        query_ledger_entries(&self.connection, &sql, values, 0)
    }

    fn list_account_running_balances(
        &self,
        filter: &LedgerEntryFilter,
    ) -> Result<Vec<RunningBalanceProjection>, ReportReadError> {
        validate_ledger_filter(filter)?;
        let mut values = vec![Value::Text(filter.ledger_id.clone())];
        let mut sql = format!(
            "SELECT {}, rb.balance_minor \
             FROM v_account_transaction_running_balance rb WHERE rb.ledger_id = ?",
            ledger_entry_columns("rb")
        );
        append_ledger_entry_filter(&mut sql, &mut values, filter, "rb", false);
        sql.push_str(" ORDER BY rb.business_date, rb.sequence_no, rb.line_no, rb.entry_id");
        let mut statement = self
            .connection
            .prepare(&sql)
            .map_err(report_storage_error)?;
        let rows = statement
            .query_map(params_from_iter(values.iter()), |row| {
                Ok(RunningBalanceProjection {
                    entry: map_ledger_entry(row, 0)?,
                    balance_minor: row.get(22)?,
                })
            })
            .map_err(report_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(report_storage_error)
    }

    fn list_account_balances(
        &self,
        ledger_id: &str,
    ) -> Result<Vec<AccountBalanceProjection>, ReportReadError> {
        validate_required_id(ledger_id, "账簿标识")?;
        let mut statement = self
            .connection
            .prepare(
                "SELECT ledger_id, account_id, account_name, currency_code, balance_minor \
                 FROM v_account_balances WHERE ledger_id = ?1 ORDER BY account_name, account_id",
            )
            .map_err(report_storage_error)?;
        let rows = statement
            .query_map([ledger_id], |row| {
                Ok(AccountBalanceProjection {
                    ledger_id: row.get(0)?,
                    account_id: row.get(1)?,
                    account_name: row.get(2)?,
                    currency_code: row.get(3)?,
                    balance_minor: row.get(4)?,
                })
            })
            .map_err(report_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(report_storage_error)
    }

    fn list_tagged_entries(
        &self,
        filter: &LedgerEntryFilter,
    ) -> Result<Vec<TaggedLedgerEntryProjection>, ReportReadError> {
        validate_ledger_filter(filter)?;
        let mut values = vec![Value::Text(filter.ledger_id.clone())];
        let mut sql = format!(
            "SELECT lt.tag_id, lt.tag_name, {} \
             FROM v_life_theme_transactions lt WHERE lt.ledger_id = ?",
            ledger_entry_columns("lt")
        );
        append_ledger_entry_filter(&mut sql, &mut values, filter, "lt", false);
        append_in_filter(&mut sql, &mut values, "lt.tag_id", &filter.tag_ids);
        sql.push_str(
            " ORDER BY lt.tag_name, lt.business_date, lt.sequence_no, lt.line_no, lt.entry_id",
        );
        let mut statement = self
            .connection
            .prepare(&sql)
            .map_err(report_storage_error)?;
        let rows = statement
            .query_map(params_from_iter(values.iter()), |row| {
                Ok(TaggedLedgerEntryProjection {
                    tag_id: row.get(0)?,
                    tag_name: row.get(1)?,
                    entry: map_ledger_entry(row, 2)?,
                })
            })
            .map_err(report_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(report_storage_error)
    }

    fn list_tagged_assets(
        &self,
        ledger_id: &str,
        tag_ids: &[String],
    ) -> Result<Vec<TaggedAssetProjection>, ReportReadError> {
        validate_required_id(ledger_id, "账簿标识")?;
        let mut values = vec![Value::Text(ledger_id.to_owned())];
        let mut sql = String::from(
            "SELECT tag_id, tag_name, ledger_id, account_id, account_name, currency_code, balance_minor \
             FROM v_life_theme_assets WHERE ledger_id = ?",
        );
        append_in_filter(&mut sql, &mut values, "tag_id", tag_ids);
        sql.push_str(" ORDER BY tag_name, account_name, account_id");
        let mut statement = self
            .connection
            .prepare(&sql)
            .map_err(report_storage_error)?;
        let rows = statement
            .query_map(params_from_iter(values.iter()), |row| {
                Ok(TaggedAssetProjection {
                    tag_id: row.get(0)?,
                    tag_name: row.get(1)?,
                    account: AccountBalanceProjection {
                        ledger_id: row.get(2)?,
                        account_id: row.get(3)?,
                        account_name: row.get(4)?,
                        currency_code: row.get(5)?,
                        balance_minor: row.get(6)?,
                    },
                })
            })
            .map_err(report_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(report_storage_error)
    }

    fn list_investment_position_inputs(
        &self,
        filter: &InvestmentProjectionFilter,
    ) -> Result<Vec<InvestmentPositionInput>, ReportReadError> {
        validate_investment_filter(filter)?;
        let mut values = vec![Value::Text(filter.ledger_id.clone())];
        let mut sql = String::from(
            "SELECT t.ledger_id, it.account_id, it.instrument_id, i.name, i.kind, \
                    i.quote_currency_code, i.quantity_scale, \
                    SUM(it.position_effect * it.quantity_units), \
                    SUM(CASE WHEN it.trade_kind = 'buy' THEN it.quantity_units ELSE 0 END), \
                    SUM(CASE WHEN it.trade_kind = 'sell' THEN it.quantity_units ELSE 0 END) \
             FROM investment_trades it \
             JOIN transactions t ON t.id = it.transaction_id \
             JOIN investment_instruments i ON i.id = it.instrument_id \
             WHERE t.status = 'posted' AND t.ledger_id = ?",
        );
        append_date_range(&mut sql, &mut values, "t.business_date", &filter.date_range);
        append_in_filter(&mut sql, &mut values, "it.account_id", &filter.account_ids);
        append_in_filter(
            &mut sql,
            &mut values,
            "it.instrument_id",
            &filter.instrument_ids,
        );
        sql.push_str(
            " GROUP BY t.ledger_id, it.account_id, it.instrument_id, i.name, i.kind, \
                       i.quote_currency_code, i.quantity_scale \
              ORDER BY i.name, it.instrument_id, it.account_id",
        );
        let mut statement = self
            .connection
            .prepare(&sql)
            .map_err(report_storage_error)?;
        let rows = statement
            .query_map(params_from_iter(values.iter()), |row| {
                let scale = read_scale(row, 6)?;
                Ok(InvestmentPositionInput {
                    ledger_id: row.get(0)?,
                    account_id: row.get(1)?,
                    instrument_id: row.get(2)?,
                    instrument_name: row.get(3)?,
                    instrument_kind: row.get(4)?,
                    quote_currency_code: row.get(5)?,
                    net_quantity: ScaledValue::new(row.get(7)?, scale),
                    bought_quantity: ScaledValue::new(row.get(8)?, scale),
                    sold_quantity: ScaledValue::new(row.get(9)?, scale),
                })
            })
            .map_err(report_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(report_storage_error)
    }

    fn list_realized_profit_inputs(
        &self,
        filter: &InvestmentProjectionFilter,
    ) -> Result<Vec<RealizedProfitInput>, ReportReadError> {
        validate_investment_filter(filter)?;
        let mut values = vec![Value::Text(filter.ledger_id.clone())];
        let mut sql = String::from(
            "SELECT rp.ledger_id, rp.business_date, rp.sell_trade_id, rp.account_id, \
                    rp.instrument_id, rp.instrument_name, rp.sold_quantity_units, \
                    i.quantity_scale, rp.price_units, rp.price_scale, \
                    rp.allocated_quantity_units, rp.allocated_cost_minor, \
                    rp.allocated_proceeds_minor \
             FROM v_investment_realized_profit_inputs rp \
             JOIN investment_instruments i ON i.id = rp.instrument_id \
             WHERE rp.ledger_id = ?",
        );
        append_date_range(
            &mut sql,
            &mut values,
            "rp.business_date",
            &filter.date_range,
        );
        append_in_filter(&mut sql, &mut values, "rp.account_id", &filter.account_ids);
        append_in_filter(
            &mut sql,
            &mut values,
            "rp.instrument_id",
            &filter.instrument_ids,
        );
        sql.push_str(" ORDER BY rp.business_date, rp.sell_trade_id");
        let mut statement = self
            .connection
            .prepare(&sql)
            .map_err(report_storage_error)?;
        let rows = statement
            .query_map(params_from_iter(values.iter()), |row| {
                let quantity_scale = read_scale(row, 7)?;
                let price_units: Option<i64> = row.get(8)?;
                let price_scale: Option<i64> = row.get(9)?;
                let price = match (price_units, price_scale) {
                    (Some(units), Some(scale)) => {
                        Some(ScaledValue::new(units, scale_to_u8(scale, 9)?))
                    }
                    (None, None) => None,
                    _ => {
                        return Err(RusqliteError::InvalidColumnType(
                            9,
                            "price_scale".to_owned(),
                            Type::Null,
                        ));
                    }
                };
                Ok(RealizedProfitInput {
                    ledger_id: row.get(0)?,
                    business_date: row.get(1)?,
                    sell_trade_id: row.get(2)?,
                    account_id: row.get(3)?,
                    instrument_id: row.get(4)?,
                    instrument_name: row.get(5)?,
                    sold_quantity: ScaledValue::new(row.get(6)?, quantity_scale),
                    price,
                    allocated_quantity: ScaledValue::new(row.get(10)?, quantity_scale),
                    allocated_cost_minor: row.get(11)?,
                    allocated_proceeds_minor: row.get(12)?,
                })
            })
            .map_err(report_storage_error)?;
        rows.collect::<Result<Vec<_>, _>>()
            .map_err(report_storage_error)
    }
}

fn random_id(connection: &Connection) -> Result<String, RusqliteError> {
    connection.query_row("SELECT lower(hex(randomblob(16)))", [], |row| row.get(0))
}

fn random_connection_id(connection: &Connection) -> Result<String, ReferenceDataError> {
    random_id(connection).map_err(reference_data_storage_error)
}

fn bool_to_integer(value: bool) -> i64 {
    i64::from(value)
}

fn budget_period_kind_key(kind: BudgetPeriodKind) -> &'static str {
    match kind {
        BudgetPeriodKind::Monthly => "monthly",
        BudgetPeriodKind::Quarterly => "quarterly",
        BudgetPeriodKind::Yearly => "yearly",
        BudgetPeriodKind::Custom => "custom",
    }
}

fn budget_period_kind_from_key(
    value: &str,
    index: usize,
) -> Result<BudgetPeriodKind, RusqliteError> {
    match value {
        "monthly" => Ok(BudgetPeriodKind::Monthly),
        "quarterly" => Ok(BudgetPeriodKind::Quarterly),
        "yearly" => Ok(BudgetPeriodKind::Yearly),
        "custom" => Ok(BudgetPeriodKind::Custom),
        _ => Err(invalid_reference_value(index, "预算周期类型", value)),
    }
}

fn budget_status_key(status: BudgetStatus) -> &'static str {
    match status {
        BudgetStatus::Draft => "draft",
        BudgetStatus::Active => "active",
        BudgetStatus::Closed => "closed",
    }
}

fn budget_status_from_key(value: &str, index: usize) -> Result<BudgetStatus, RusqliteError> {
    match value {
        "draft" => Ok(BudgetStatus::Draft),
        "active" => Ok(BudgetStatus::Active),
        "closed" => Ok(BudgetStatus::Closed),
        _ => Err(invalid_reference_value(index, "预算状态", value)),
    }
}

fn budget_rollover_mode_key(mode: BudgetRolloverMode) -> &'static str {
    match mode {
        BudgetRolloverMode::None => "none",
        BudgetRolloverMode::Positive => "positive",
        BudgetRolloverMode::All => "all",
    }
}

fn budget_rollover_mode_from_key(
    value: &str,
    index: usize,
) -> Result<BudgetRolloverMode, RusqliteError> {
    match value {
        "none" => Ok(BudgetRolloverMode::None),
        "positive" => Ok(BudgetRolloverMode::Positive),
        "all" => Ok(BudgetRolloverMode::All),
        _ => Err(invalid_reference_value(index, "预算结转方式", value)),
    }
}

fn financial_goal_progress_mode_key(mode: FinancialGoalProgressMode) -> &'static str {
    match mode {
        FinancialGoalProgressMode::Balance => "balance",
        FinancialGoalProgressMode::MarketValue => "market_value",
        FinancialGoalProgressMode::NetAsset => "net_asset",
        FinancialGoalProgressMode::Custom => "custom",
    }
}

fn financial_goal_progress_mode_from_key(
    value: &str,
    index: usize,
) -> Result<FinancialGoalProgressMode, RusqliteError> {
    match value {
        "balance" => Ok(FinancialGoalProgressMode::Balance),
        "market_value" => Ok(FinancialGoalProgressMode::MarketValue),
        "net_asset" => Ok(FinancialGoalProgressMode::NetAsset),
        "custom" => Ok(FinancialGoalProgressMode::Custom),
        _ => Err(invalid_reference_value(index, "财务目标进度口径", value)),
    }
}

fn financial_goal_status_key(status: FinancialGoalStatus) -> &'static str {
    match status {
        FinancialGoalStatus::Active => "active",
        FinancialGoalStatus::Completed => "completed",
        FinancialGoalStatus::Cancelled => "cancelled",
    }
}

fn financial_goal_status_from_key(
    value: &str,
    index: usize,
) -> Result<FinancialGoalStatus, RusqliteError> {
    match value {
        "active" => Ok(FinancialGoalStatus::Active),
        "completed" => Ok(FinancialGoalStatus::Completed),
        "cancelled" => Ok(FinancialGoalStatus::Cancelled),
        _ => Err(invalid_reference_value(index, "财务目标状态", value)),
    }
}

fn financial_goal_account_scope_key(scope: FinancialGoalAccountScopeMode) -> &'static str {
    match scope {
        FinancialGoalAccountScopeMode::All => "all",
        FinancialGoalAccountScopeMode::Selected => "selected",
    }
}

fn financial_goal_account_scope_from_key(
    value: &str,
    index: usize,
) -> Result<FinancialGoalAccountScopeMode, RusqliteError> {
    match value {
        "all" => Ok(FinancialGoalAccountScopeMode::All),
        "selected" => Ok(FinancialGoalAccountScopeMode::Selected),
        _ => Err(invalid_reference_value(index, "财务目标账户范围", value)),
    }
}

fn schedule_execution_mode_key(mode: ScheduleExecutionMode) -> &'static str {
    match mode {
        ScheduleExecutionMode::Manual => "manual",
        ScheduleExecutionMode::Automatic => "automatic",
    }
}

fn schedule_execution_mode_from_key(
    value: &str,
    index: usize,
) -> Result<ScheduleExecutionMode, RusqliteError> {
    match value {
        "manual" => Ok(ScheduleExecutionMode::Manual),
        "automatic" => Ok(ScheduleExecutionMode::Automatic),
        _ => Err(invalid_reference_value(index, "计划执行方式", value)),
    }
}

fn schedule_status_key(status: ScheduleStatus) -> &'static str {
    match status {
        ScheduleStatus::Active => "active",
        ScheduleStatus::Paused => "paused",
        ScheduleStatus::Completed => "completed",
    }
}

fn schedule_status_from_key(value: &str, index: usize) -> Result<ScheduleStatus, RusqliteError> {
    match value {
        "active" => Ok(ScheduleStatus::Active),
        "paused" => Ok(ScheduleStatus::Paused),
        "completed" => Ok(ScheduleStatus::Completed),
        _ => Err(invalid_reference_value(index, "计划状态", value)),
    }
}

fn reminder_status_key(status: ReminderStatus) -> &'static str {
    match status {
        ReminderStatus::Active => "active",
        ReminderStatus::Snoozed => "snoozed",
        ReminderStatus::Completed => "completed",
    }
}

fn reminder_status_from_key(value: &str, index: usize) -> Result<ReminderStatus, RusqliteError> {
    match value {
        "active" => Ok(ReminderStatus::Active),
        "snoozed" => Ok(ReminderStatus::Snoozed),
        "completed" => Ok(ReminderStatus::Completed),
        _ => Err(invalid_reference_value(index, "提醒状态", value)),
    }
}

fn reminder_delivery_mode_key(mode: ReminderDeliveryMode) -> &'static str {
    match mode {
        ReminderDeliveryMode::InApp => "in_app",
        ReminderDeliveryMode::SystemNotification => "system_notification",
        ReminderDeliveryMode::Both => "both",
    }
}

fn reminder_delivery_mode_from_key(
    value: &str,
    index: usize,
) -> Result<ReminderDeliveryMode, RusqliteError> {
    match value {
        "in_app" => Ok(ReminderDeliveryMode::InApp),
        "system_notification" => Ok(ReminderDeliveryMode::SystemNotification),
        "both" => Ok(ReminderDeliveryMode::Both),
        _ => Err(invalid_reference_value(index, "提醒投递方式", value)),
    }
}

fn category_direction_key(direction: CategoryDirection) -> &'static str {
    match direction {
        CategoryDirection::Income => "income",
        CategoryDirection::Expense => "expense",
        CategoryDirection::Both => "both",
    }
}

fn category_direction_from_key(
    value: &str,
    index: usize,
) -> Result<CategoryDirection, RusqliteError> {
    match value {
        "income" => Ok(CategoryDirection::Income),
        "expense" => Ok(CategoryDirection::Expense),
        "both" => Ok(CategoryDirection::Both),
        _ => Err(invalid_reference_value(index, "分类方向", value)),
    }
}

fn party_kind_key(kind: PartyKind) -> &'static str {
    match kind {
        PartyKind::FamilyMember => "family_member",
        PartyKind::ContactPerson => "contact_person",
        PartyKind::Institution => "institution",
    }
}

fn party_kind_from_key(value: &str, index: usize) -> Result<PartyKind, RusqliteError> {
    match value {
        "family_member" => Ok(PartyKind::FamilyMember),
        "contact_person" => Ok(PartyKind::ContactPerson),
        "institution" => Ok(PartyKind::Institution),
        _ => Err(invalid_reference_value(index, "往来方类型", value)),
    }
}

fn legacy_party_kind_key(kind: PartyKind) -> &'static str {
    match kind {
        PartyKind::FamilyMember | PartyKind::ContactPerson => "person",
        PartyKind::Institution => "institution",
    }
}

fn party_sex_key(sex: PersonSex) -> &'static str {
    match sex {
        PersonSex::Male => "male",
        PersonSex::Female => "female",
    }
}

fn party_sex_from_key(
    value: Option<&str>,
    index: usize,
) -> Result<Option<PersonSex>, RusqliteError> {
    match value {
        None => Ok(None),
        Some("male") => Ok(Some(PersonSex::Male)),
        Some("female") => Ok(Some(PersonSex::Female)),
        Some(value) => Err(invalid_reference_value(index, "人员性别", value)),
    }
}

fn birthday_calendar_key(calendar: BirthdayCalendar) -> &'static str {
    match calendar {
        BirthdayCalendar::Gregorian => "gregorian",
        BirthdayCalendar::Lunar => "lunar",
    }
}

fn party_birthday_from_columns(
    calendar: Option<&str>,
    year: Option<i64>,
    month: Option<i64>,
    day: Option<i64>,
) -> Result<Option<PartyBirthday>, RusqliteError> {
    match (calendar, year, month, day) {
        (None, None, None, None) => Ok(None),
        (Some(calendar), Some(year), Some(month), Some(day)) => {
            let calendar = match calendar {
                "gregorian" => BirthdayCalendar::Gregorian,
                "lunar" => BirthdayCalendar::Lunar,
                value => return Err(invalid_reference_value(7, "生日历法", value)),
            };
            let year = u16::try_from(year)
                .map_err(|_| invalid_reference_value(8, "生日年份", &year.to_string()))?;
            let month = u8::try_from(month)
                .map_err(|_| invalid_reference_value(9, "生日月份", &month.to_string()))?;
            let day = u8::try_from(day)
                .map_err(|_| invalid_reference_value(10, "生日日期", &day.to_string()))?;
            Ok(Some(PartyBirthday {
                calendar,
                year,
                month,
                day,
            }))
        }
        _ => Err(invalid_reference_value(7, "生日分量", "不完整")),
    }
}

fn invalid_reference_value(index: usize, label: &str, value: &str) -> RusqliteError {
    RusqliteError::FromSqlConversionFailure(
        index,
        Type::Text,
        Box::new(std::io::Error::new(
            std::io::ErrorKind::InvalidData,
            format!("无法识别的{label}: {value}"),
        )),
    )
}

fn map_budget_record(row: &Row<'_>) -> Result<BudgetRecord, RusqliteError> {
    let period_kind: String = row.get(3)?;
    let status: String = row.get(6)?;
    Ok(BudgetRecord {
        id: row.get(0)?,
        ledger_id: row.get(1)?,
        name: row.get(2)?,
        period_kind: budget_period_kind_from_key(&period_kind, 3)?,
        start_date: row.get(4)?,
        end_date: row.get(5)?,
        status: budget_status_from_key(&status, 6)?,
        created_at: row.get(7)?,
        updated_at: row.get(8)?,
    })
}

fn map_budget_item_record(row: &Row<'_>) -> Result<BudgetItemRecord, RusqliteError> {
    let rollover_mode: String = row.get(7)?;
    Ok(BudgetItemRecord {
        id: row.get(0)?,
        budget_id: row.get(1)?,
        category_id: row.get(2)?,
        period_start: row.get(3)?,
        period_end: row.get(4)?,
        amount_minor: row.get(5)?,
        currency_code: row.get(6)?,
        rollover_mode: budget_rollover_mode_from_key(&rollover_mode, 7)?,
        note: row.get(8)?,
    })
}

fn map_financial_goal_record(row: &Row<'_>) -> Result<FinancialGoalRecord, RusqliteError> {
    let progress_mode: String = row.get(7)?;
    let status: String = row.get(8)?;
    let account_scope_mode: String = row.get(12)?;
    Ok(FinancialGoalRecord {
        id: row.get(0)?,
        ledger_id: row.get(1)?,
        name: row.get(2)?,
        target_amount_minor: row.get(3)?,
        currency_code: row.get(4)?,
        start_date: row.get(5)?,
        target_date: row.get(6)?,
        progress_mode: financial_goal_progress_mode_from_key(&progress_mode, 7)?,
        status: financial_goal_status_from_key(&status, 8)?,
        initial_value_minor: row.get(9)?,
        initial_value_captured_at: row.get(10)?,
        initial_inputs_json: row.get(11)?,
        account_scope_mode: financial_goal_account_scope_from_key(&account_scope_mode, 12)?,
        progress_formula_version: row.get(13)?,
        created_at: row.get(14)?,
        updated_at: row.get(15)?,
    })
}

fn map_schedule_record(row: &Row<'_>) -> Result<ScheduleRecord, RusqliteError> {
    let execution_mode: String = row.get(8)?;
    let status: String = row.get(9)?;
    Ok(ScheduleRecord {
        id: row.get(0)?,
        ledger_id: row.get(1)?,
        template_id: row.get(2)?,
        name: row.get(3)?,
        recurrence_json: row.get(4)?,
        start_date: row.get(5)?,
        end_date: row.get(6)?,
        next_due_date: row.get(7)?,
        execution_mode: schedule_execution_mode_from_key(&execution_mode, 8)?,
        status: schedule_status_from_key(&status, 9)?,
        max_occurrences: row.get(10)?,
        reminder_lead_days: row.get(11)?,
        recurrence_version: row.get(12)?,
        last_generated_transaction_id: row.get(13)?,
        created_at: row.get(14)?,
        updated_at: row.get(15)?,
    })
}

fn map_reminder_record(row: &Row<'_>) -> Result<ReminderRecord, RusqliteError> {
    let status: String = row.get(11)?;
    let delivery_mode: String = row.get(14)?;
    Ok(ReminderRecord {
        id: row.get(0)?,
        ledger_id: row.get(1)?,
        name: row.get(2)?,
        reminder_kind: row.get(3)?,
        target_kind: row.get(4)?,
        target_id: row.get(5)?,
        condition_json: row.get(6)?,
        remind_at: row.get(7)?,
        recurrence_json: row.get(8)?,
        next_trigger_at: row.get(9)?,
        last_triggered_at: row.get(10)?,
        status: reminder_status_from_key(&status, 11)?,
        is_enabled: row.get::<_, i64>(12)? != 0,
        condition_version: row.get(13)?,
        delivery_mode: reminder_delivery_mode_from_key(&delivery_mode, 14)?,
        created_at: row.get(15)?,
        updated_at: row.get(16)?,
    })
}

fn insert_budget_items(
    connection: &Connection,
    budget_id: &str,
    items: &[NewBudgetItem],
) -> Result<(), RusqliteError> {
    for item in items {
        let item_id = random_id(connection)?;
        connection.execute(
            "INSERT INTO budget_items(
                id, budget_id, category_id, period_start, period_end, amount_minor,
                currency_code, rollover_mode, note
             ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)",
            params![
                item_id,
                budget_id,
                item.category_id,
                item.period_start,
                item.period_end,
                item.amount_minor,
                item.currency_code,
                budget_rollover_mode_key(item.rollover_mode),
                item.note,
            ],
        )?;
    }
    Ok(())
}

fn insert_financial_goal_accounts(
    connection: &Connection,
    goal_id: &str,
    account_ids: &[String],
) -> Result<(), RusqliteError> {
    for account_id in account_ids {
        connection.execute(
            "INSERT INTO financial_goal_accounts(goal_id, account_id) VALUES (?1, ?2)",
            params![goal_id, account_id],
        )?;
    }
    Ok(())
}

fn ensure_optional_reference_in_ledger(
    connection: &Connection,
    reference_id: Option<&str>,
    ledger_id: &str,
    table: &str,
    label: &str,
) -> Result<(), ReferenceDataError> {
    let Some(reference_id) = reference_id else {
        return Ok(());
    };
    validate_reference_id(reference_id, label)?;
    let sql = match table {
        "account_groups" => {
            "SELECT EXISTS(SELECT 1 FROM account_groups WHERE id = ?1 AND ledger_id = ?2)"
        }
        "categories" => "SELECT EXISTS(SELECT 1 FROM categories WHERE id = ?1 AND ledger_id = ?2)",
        _ => {
            return Err(ReferenceDataError::Storage(
                "未支持的账簿关系校验".to_owned(),
            ));
        }
    };
    let exists: i64 = connection
        .query_row(sql, params![reference_id, ledger_id], |row| row.get(0))
        .map_err(reference_data_storage_error)?;
    if exists == 0 {
        return Err(ReferenceDataError::Conflict(format!(
            "{label}不存在或不属于目标账簿"
        )));
    }
    Ok(())
}

fn ensure_parent_is_not_descendant(
    connection: &Connection,
    table: &str,
    ledger_id: &str,
    entity_id: &str,
    parent_id: Option<&str>,
    label: &str,
) -> Result<(), ReferenceDataError> {
    let Some(parent_id) = parent_id else {
        return Ok(());
    };
    let sql = match table {
        "account_groups" => {
            "WITH RECURSIVE descendants(id) AS ( \
                SELECT id FROM account_groups WHERE ledger_id = ?1 AND parent_id = ?2 \
                UNION ALL \
                SELECT child.id FROM account_groups child \
                JOIN descendants parent ON child.parent_id = parent.id \
                WHERE child.ledger_id = ?1 \
             ) SELECT EXISTS(SELECT 1 FROM descendants WHERE id = ?3)"
        }
        "categories" => {
            "WITH RECURSIVE descendants(id) AS ( \
                SELECT id FROM categories WHERE ledger_id = ?1 AND parent_id = ?2 \
                UNION ALL \
                SELECT child.id FROM categories child \
                JOIN descendants parent ON child.parent_id = parent.id \
                WHERE child.ledger_id = ?1 \
             ) SELECT EXISTS(SELECT 1 FROM descendants WHERE id = ?3)"
        }
        _ => {
            return Err(ReferenceDataError::Storage(
                "未支持的层级关系校验".to_owned(),
            ));
        }
    };
    let creates_cycle: i64 = connection
        .query_row(sql, params![ledger_id, entity_id, parent_id], |row| {
            row.get(0)
        })
        .map_err(reference_data_storage_error)?;
    if creates_cycle != 0 {
        return Err(ReferenceDataError::Conflict(format!(
            "{label}父子关系不能形成循环"
        )));
    }
    Ok(())
}

fn ensure_ledger_exists(connection: &Connection, ledger_id: &str) -> Result<(), PlanningDataError> {
    validate_planning_name(ledger_id, "账簿标识")?;
    let exists: i64 = connection
        .query_row(
            "SELECT EXISTS(SELECT 1 FROM ledgers WHERE id = ?1)",
            [ledger_id],
            |row| row.get(0),
        )
        .map_err(planning_storage_error)?;
    if exists == 0 {
        return Err(PlanningDataError::NotFound("账簿不存在".to_owned()));
    }
    Ok(())
}

fn ensure_currency_exists(
    connection: &Connection,
    currency_code: &str,
) -> Result<(), PlanningDataError> {
    validate_planning_name(currency_code, "币种代码")?;
    let exists: i64 = connection
        .query_row(
            "SELECT EXISTS(SELECT 1 FROM currencies WHERE code = ?1)",
            [currency_code],
            |row| row.get(0),
        )
        .map_err(planning_storage_error)?;
    if exists == 0 {
        return Err(PlanningDataError::Conflict(
            "币种不存在，不能创建预算或目标".to_owned(),
        ));
    }
    Ok(())
}

fn ensure_category_in_ledger(
    connection: &Connection,
    ledger_id: &str,
    category_id: &str,
) -> Result<(), PlanningDataError> {
    validate_planning_name(category_id, "分类标识")?;
    let exists: i64 = connection
        .query_row(
            "SELECT EXISTS(SELECT 1 FROM categories WHERE id = ?1 AND ledger_id = ?2)",
            params![category_id, ledger_id],
            |row| row.get(0),
        )
        .map_err(planning_storage_error)?;
    if exists == 0 {
        return Err(PlanningDataError::Conflict(
            "预算分类不存在或不属于目标账簿".to_owned(),
        ));
    }
    Ok(())
}

fn ensure_account_in_ledger(
    connection: &Connection,
    ledger_id: &str,
    account_id: &str,
) -> Result<(), PlanningDataError> {
    validate_planning_name(account_id, "账户标识")?;
    let exists: i64 = connection
        .query_row(
            "SELECT EXISTS(SELECT 1 FROM accounts WHERE id = ?1 AND ledger_id = ?2)",
            params![account_id, ledger_id],
            |row| row.get(0),
        )
        .map_err(planning_storage_error)?;
    if exists == 0 {
        return Err(PlanningDataError::Conflict(
            "目标账户不存在或不属于目标账簿".to_owned(),
        ));
    }
    Ok(())
}

fn ensure_budget_in_ledger(
    connection: &Connection,
    ledger_id: &str,
    budget_id: &str,
) -> Result<(), PlanningDataError> {
    let exists: i64 = connection
        .query_row(
            "SELECT EXISTS(SELECT 1 FROM budgets WHERE id = ?1 AND ledger_id = ?2)",
            params![budget_id, ledger_id],
            |row| row.get(0),
        )
        .map_err(planning_storage_error)?;
    if exists == 0 {
        return Err(PlanningDataError::NotFound("预算不存在".to_owned()));
    }
    Ok(())
}

fn ensure_goal_in_ledger(
    connection: &Connection,
    ledger_id: &str,
    goal_id: &str,
) -> Result<(), PlanningDataError> {
    let exists: i64 = connection
        .query_row(
            "SELECT EXISTS(SELECT 1 FROM financial_goals WHERE id = ?1 AND ledger_id = ?2)",
            params![goal_id, ledger_id],
            |row| row.get(0),
        )
        .map_err(planning_storage_error)?;
    if exists == 0 {
        return Err(PlanningDataError::NotFound("财务目标不存在".to_owned()));
    }
    Ok(())
}

fn ensure_template_in_ledger(
    connection: &Connection,
    ledger_id: &str,
    template_id: &str,
) -> Result<(), PlanningDataError> {
    validate_planning_name(template_id, "交易模板标识")?;
    let exists: i64 = connection
        .query_row(
            "SELECT EXISTS(SELECT 1 FROM transaction_templates WHERE id = ?1 AND ledger_id = ?2)",
            params![template_id, ledger_id],
            |row| row.get(0),
        )
        .map_err(planning_storage_error)?;
    if exists == 0 {
        return Err(PlanningDataError::Conflict(
            "计划模板不存在或不属于目标账簿".to_owned(),
        ));
    }
    Ok(())
}

fn validate_budget_item_reference(
    connection: &Connection,
    ledger_id: &str,
    item: &NewBudgetItem,
) -> Result<(), PlanningDataError> {
    ensure_category_in_ledger(connection, ledger_id, &item.category_id)?;
    ensure_currency_exists(connection, &item.currency_code)
}

fn validate_planning_name(value: &str, label: &str) -> Result<(), PlanningDataError> {
    if value.trim().is_empty() {
        return Err(PlanningDataError::InvalidInput(format!("{label}不能为空")));
    }
    Ok(())
}

fn ensure_planning_updated(changed: usize, message: &str) -> Result<(), PlanningDataError> {
    if changed == 0 {
        Err(PlanningDataError::NotFound(message.to_owned()))
    } else {
        Ok(())
    }
}

fn validate_reference_id(value: &str, label: &str) -> Result<(), ReferenceDataError> {
    validate_reference_name(value, label)
}

fn validate_reference_name(value: &str, label: &str) -> Result<(), ReferenceDataError> {
    if value.trim().is_empty() {
        return Err(ReferenceDataError::InvalidInput(format!("{label}不能为空")));
    }
    Ok(())
}

fn validate_party_profile(
    name: &str,
    kind: PartyKind,
    contact: Option<&str>,
    address: Option<&str>,
    sex: Option<PersonSex>,
    birthday: Option<PartyBirthday>,
) -> Result<(), ReferenceDataError> {
    validate_reference_name(name, "人员或机构名称")?;
    validate_text_length(name, "人员或机构名称", 20)?;
    validate_optional_text(contact, "联系方式", 20)?;
    validate_optional_text(address, "地址", 40)?;

    if kind == PartyKind::Institution && (sex.is_some() || birthday.is_some()) {
        return Err(ReferenceDataError::InvalidInput(
            "机构不能保存人员性别或生日".to_owned(),
        ));
    }
    if let Some(birthday) = birthday {
        validate_party_birthday(birthday)?;
    }
    Ok(())
}

fn validate_optional_text(
    value: Option<&str>,
    label: &str,
    maximum_characters: usize,
) -> Result<(), ReferenceDataError> {
    let Some(value) = value else {
        return Ok(());
    };
    if value.trim().is_empty() {
        return Err(ReferenceDataError::InvalidInput(format!(
            "{label}为空时必须使用None"
        )));
    }
    validate_text_length(value, label, maximum_characters)
}

fn validate_text_length(
    value: &str,
    label: &str,
    maximum_characters: usize,
) -> Result<(), ReferenceDataError> {
    if value.chars().count() > maximum_characters {
        return Err(ReferenceDataError::InvalidInput(format!(
            "{label}不能超过{maximum_characters}个字符"
        )));
    }
    Ok(())
}

fn validate_party_birthday(birthday: PartyBirthday) -> Result<(), ReferenceDataError> {
    if birthday.year == 0 || !(1..=12).contains(&birthday.month) {
        return Err(ReferenceDataError::InvalidInput(
            "生日年月超出允许范围".to_owned(),
        ));
    }
    let maximum_day = match birthday.calendar {
        BirthdayCalendar::Lunar => 30,
        BirthdayCalendar::Gregorian => gregorian_month_days(birthday.year, birthday.month),
    };
    if birthday.day == 0 || birthday.day > maximum_day {
        return Err(ReferenceDataError::InvalidInput(
            "生日日期超出对应月份范围".to_owned(),
        ));
    }
    Ok(())
}

fn gregorian_month_days(year: u16, month: u8) -> u8 {
    match month {
        4 | 6 | 9 | 11 => 30,
        2 if is_gregorian_leap_year(year) => 29,
        2 => 28,
        _ => 31,
    }
}

fn is_gregorian_leap_year(year: u16) -> bool {
    year % 4 == 0 && (year % 100 != 0 || year % 400 == 0)
}

fn ensure_reference_updated(changed: usize, message: &str) -> Result<(), ReferenceDataError> {
    if changed == 0 {
        Err(ReferenceDataError::NotFound(message.to_owned()))
    } else {
        Ok(())
    }
}

fn random_planning_id(connection: &Connection) -> Result<String, PlanningDataError> {
    random_id(connection).map_err(planning_storage_error)
}

fn reference_data_query_error(error: RusqliteError, not_found: &str) -> ReferenceDataError {
    if matches!(error, RusqliteError::QueryReturnedNoRows) {
        ReferenceDataError::NotFound(not_found.to_owned())
    } else {
        reference_data_storage_error(error)
    }
}

fn reference_data_storage_error(error: RusqliteError) -> ReferenceDataError {
    match &error {
        RusqliteError::SqliteFailure(details, _)
            if details.code == ErrorCode::ConstraintViolation =>
        {
            ReferenceDataError::Conflict("SQLite 约束冲突".to_owned())
        }
        _ => ReferenceDataError::Storage(error.to_string()),
    }
}

fn planning_storage_error(error: RusqliteError) -> PlanningDataError {
    match &error {
        RusqliteError::SqliteFailure(details, _)
            if details.code == ErrorCode::ConstraintViolation =>
        {
            PlanningDataError::Conflict("SQLite 约束冲突".to_owned())
        }
        _ => PlanningDataError::Storage(error.to_string()),
    }
}

fn transaction_kind_key(kind: &TransactionKind) -> &str {
    match kind {
        TransactionKind::Income => "income",
        TransactionKind::Expense => "expense",
        TransactionKind::Transfer => "transfer",
        TransactionKind::Adjustment => "adjustment",
        TransactionKind::DomainSpecific(value) => value,
    }
}

fn transaction_status_key(status: NewTransactionStatus) -> &'static str {
    match status {
        NewTransactionStatus::Draft => "draft",
        NewTransactionStatus::Posted => "posted",
    }
}

fn entry_role_key(role: TransactionEntryRole) -> &'static str {
    match role {
        TransactionEntryRole::Primary => "primary",
        TransactionEntryRole::Counterparty => "counterparty",
        TransactionEntryRole::Split => "split",
        TransactionEntryRole::Fee => "fee",
        TransactionEntryRole::Interest => "interest",
        TransactionEntryRole::Adjustment => "adjustment",
        TransactionEntryRole::Opening => "opening",
    }
}

fn entry_direction_key(direction: EntryDirection) -> &'static str {
    match direction {
        EntryDirection::Inflow => "inflow",
        EntryDirection::Outflow => "outflow",
    }
}

fn validate_ledger_filter(filter: &LedgerEntryFilter) -> Result<(), ReportReadError> {
    validate_required_id(&filter.ledger_id, "账簿标识")?;
    validate_date_range(&filter.date_range)
}

fn validate_investment_filter(filter: &InvestmentProjectionFilter) -> Result<(), ReportReadError> {
    validate_required_id(&filter.ledger_id, "账簿标识")?;
    validate_date_range(&filter.date_range)
}

fn validate_required_id(value: &str, label: &str) -> Result<(), ReportReadError> {
    if value.trim().is_empty() {
        Err(ReportReadError::InvalidFilter(format!("{label}不能为空")))
    } else {
        Ok(())
    }
}

fn validate_date_range(date_range: &Option<DateRange>) -> Result<(), ReportReadError> {
    let Some(date_range) = date_range else {
        return Ok(());
    };
    if date_range.start.trim().is_empty() || date_range.end.trim().is_empty() {
        return Err(ReportReadError::InvalidFilter(
            "日期范围必须同时包含开始和结束日期".to_owned(),
        ));
    }
    if date_range.start > date_range.end {
        return Err(ReportReadError::InvalidFilter(
            "日期范围开始日期不能晚于结束日期".to_owned(),
        ));
    }
    Ok(())
}

fn append_ledger_entry_filter(
    sql: &mut String,
    values: &mut Vec<Value>,
    filter: &LedgerEntryFilter,
    alias: &str,
    include_tag_filter: bool,
) {
    if filter.include_voided {
        sql.push_str(&format!(" AND {alias}.status IN ('posted', 'voided')"));
    } else {
        sql.push_str(&format!(" AND {alias}.status = 'posted'"));
    }
    append_date_range(
        sql,
        values,
        &format!("{alias}.business_date"),
        &filter.date_range,
    );
    append_in_filter(
        sql,
        values,
        &format!("{alias}.account_id"),
        &filter.account_ids,
    );
    append_in_filter(
        sql,
        values,
        &format!("{alias}.category_id"),
        &filter.category_ids,
    );
    if include_tag_filter && !filter.tag_ids.is_empty() {
        sql.push_str(&format!(
            " AND EXISTS (SELECT 1 FROM transaction_tags filter_tt \
             WHERE filter_tt.transaction_id = {alias}.transaction_id AND filter_tt.tag_id IN ("
        ));
        append_placeholders(sql, filter.tag_ids.len());
        sql.push(')');
        for tag_id in &filter.tag_ids {
            values.push(Value::Text(tag_id.clone()));
        }
    }
}

fn append_date_range(
    sql: &mut String,
    values: &mut Vec<Value>,
    column: &str,
    date_range: &Option<DateRange>,
) {
    if let Some(date_range) = date_range {
        sql.push_str(&format!(" AND {column} BETWEEN ? AND ?"));
        values.push(Value::Text(date_range.start.clone()));
        values.push(Value::Text(date_range.end.clone()));
    }
}

fn append_in_filter(sql: &mut String, values: &mut Vec<Value>, column: &str, ids: &[String]) {
    if ids.is_empty() {
        return;
    }
    sql.push_str(&format!(" AND {column} IN ("));
    append_placeholders(sql, ids.len());
    sql.push(')');
    for id in ids {
        values.push(Value::Text(id.clone()));
    }
}

fn append_placeholders(sql: &mut String, count: usize) {
    for index in 0..count {
        if index > 0 {
            sql.push_str(", ");
        }
        sql.push('?');
    }
}

fn ledger_entry_columns(alias: &str) -> String {
    format!(
        "{alias}.ledger_id, {alias}.transaction_id, {alias}.entry_id, \
         {alias}.sequence_no, {alias}.line_no, {alias}.business_date, \
         {alias}.transaction_kind, {alias}.status, {alias}.role, \
         {alias}.account_id, {alias}.account_name, {alias}.category_id, \
         {alias}.category_name, {alias}.signed_amount_minor, {alias}.currency_code, \
         {alias}.signed_base_amount_minor, {alias}.base_currency_code, \
         {alias}.theme, {alias}.description, {alias}.memo, {alias}.has_attachments, \
         COALESCE((SELECT json_group_array(tag_name) FROM ( \
             SELECT tg.name AS tag_name FROM transaction_tags tag_tt \
             JOIN tags tg ON tg.id = tag_tt.tag_id \
             WHERE tag_tt.transaction_id = {alias}.transaction_id ORDER BY tg.name \
         )), '[]')"
    )
}

fn query_ledger_entries(
    connection: &Connection,
    sql: &str,
    values: Vec<Value>,
    offset: usize,
) -> Result<Vec<LedgerEntryProjection>, ReportReadError> {
    let mut statement = connection.prepare(sql).map_err(report_storage_error)?;
    let rows = statement
        .query_map(params_from_iter(values.iter()), |row| {
            map_ledger_entry(row, offset)
        })
        .map_err(report_storage_error)?;
    rows.collect::<Result<Vec<_>, _>>()
        .map_err(report_storage_error)
}

fn map_ledger_entry(row: &Row<'_>, offset: usize) -> Result<LedgerEntryProjection, RusqliteError> {
    let tag_names_json: String = row.get(offset + 21)?;
    let tag_names = serde_json::from_str(&tag_names_json).map_err(|error| {
        RusqliteError::FromSqlConversionFailure(offset + 21, Type::Text, Box::new(error))
    })?;
    Ok(LedgerEntryProjection {
        ledger_id: row.get(offset)?,
        transaction_id: row.get(offset + 1)?,
        entry_id: row.get(offset + 2)?,
        sequence_no: row.get(offset + 3)?,
        line_no: row.get(offset + 4)?,
        business_date: row.get(offset + 5)?,
        transaction_kind: row.get(offset + 6)?,
        status: row.get(offset + 7)?,
        role: row.get(offset + 8)?,
        account_id: row.get(offset + 9)?,
        account_name: row.get(offset + 10)?,
        category_id: row.get(offset + 11)?,
        category_name: row.get(offset + 12)?,
        signed_amount_minor: row.get(offset + 13)?,
        currency_code: row.get(offset + 14)?,
        signed_base_amount_minor: row.get(offset + 15)?,
        base_currency_code: row.get(offset + 16)?,
        theme: row.get(offset + 17)?,
        description: row.get(offset + 18)?,
        memo: row.get(offset + 19)?,
        has_attachments: row.get::<_, i64>(offset + 20)? != 0,
        tag_names,
    })
}

fn read_scale(row: &Row<'_>, index: usize) -> Result<u8, RusqliteError> {
    let scale: i64 = row.get(index)?;
    scale_to_u8(scale, index)
}

fn scale_to_u8(scale: i64, index: usize) -> Result<u8, RusqliteError> {
    u8::try_from(scale).map_err(|error| {
        RusqliteError::FromSqlConversionFailure(index, Type::Integer, Box::new(error))
    })
}

fn storage_error(error: impl std::fmt::Display) -> SqliteLedgerError {
    SqliteLedgerError::Storage(error.to_string())
}

fn report_storage_error(error: RusqliteError) -> ReportReadError {
    ReportReadError::Storage(error.to_string())
}

fn transaction_storage_error(error: RusqliteError) -> TransactionWriteError {
    match &error {
        RusqliteError::SqliteFailure(details, _)
            if details.code == ErrorCode::ConstraintViolation =>
        {
            TransactionWriteError::Conflict("SQLite 约束冲突".to_owned())
        }
        _ => TransactionWriteError::Storage(error.to_string()),
    }
}

#[cfg(test)]
mod tests {
    use std::sync::atomic::{AtomicU64, Ordering};

    use crate::{
        app::{
            planning::{
                self, BudgetChanges, FinancialGoalChanges, NewBudget, NewBudgetItem,
                NewFinancialGoal, NewReminder, NewSchedule, PlanningRepository, ReminderChanges,
                ScheduleChanges,
            },
            reference_data::{
                self, AccountChanges, AccountGroupChanges, CategoryChanges, InitialAccount,
                InitializeLedgerRequest, NewAccount, NewAccountGroup, NewCategory, NewCurrency,
                NewParty, NewTag, PartyChanges, ReferenceDataRepository, TagChanges,
            },
            reporting::{InvestmentProjectionFilter, LedgerEntryFilter, ReportReadRepository},
            transactions,
        },
        domain::{
            money::MoneyAmount,
            planning::{
                BudgetPeriodKind, BudgetRolloverMode, BudgetStatus, FinancialGoalAccountScopeMode,
                FinancialGoalProgressMode, FinancialGoalStatus, ReminderDeliveryMode,
                ReminderStatus, ScheduleExecutionMode, ScheduleStatus,
            },
            reference_data::{
                BirthdayCalendar, CategoryDirection, PartyBirthday, PartyKind, PersonSex,
            },
            transactions::{
                EntryDirection, NewTransaction, NewTransactionEntry, NewTransactionStatus,
                TransactionEntryRole, TransactionKind,
            },
        },
    };

    use super::*;

    static TEST_FILE_COUNTER: AtomicU64 = AtomicU64::new(0);

    fn seeded_store() -> SqliteLedgerStore {
        let store = SqliteLedgerStore::create_in_memory().unwrap();
        store
            .connection
            .execute_batch(
                "INSERT INTO currencies(code, name, minor_unit) VALUES ('CNY', '人民币', 2);\
                 INSERT INTO ledgers(id, name, base_currency_code, created_at, updated_at)\
                 VALUES ('ledger-1', '测试账本', 'CNY', '2026-07-29T00:00:00Z', '2026-07-29T00:00:00Z');\
                 INSERT INTO accounts(id, ledger_id, name, kind, currency_code, is_asset, created_at)\
                 VALUES ('account-1', 'ledger-1', '现金', 'cash', 'CNY', 1, '2026-07-29T00:00:00Z');\
                 INSERT INTO categories(id, ledger_id, name, direction)\
                 VALUES ('category-income', 'ledger-1', '工资', 'income');\
                 INSERT INTO tags(id, ledger_id, name) VALUES ('tag-1', 'ledger-1', '日常,生活');",
            )
            .unwrap();
        store
    }

    fn valid_income() -> NewTransaction {
        NewTransaction {
            ledger_id: "ledger-1".to_owned(),
            business_date: "2026-07-29".to_owned(),
            occurred_at: "2026-07-29T09:00:00+08:00".to_owned(),
            kind: TransactionKind::Income,
            status: NewTransactionStatus::Posted,
            party_id: None,
            theme: Some("工资到账".to_owned()),
            description: None,
            entries: vec![NewTransactionEntry {
                account_id: "account-1".to_owned(),
                role: TransactionEntryRole::Primary,
                direction: EntryDirection::Inflow,
                amount: MoneyAmount::new(10_000, "CNY"),
                base_amount: Some(MoneyAmount::new(10_000, "CNY")),
                fx_snapshot_id: None,
                category_id: Some("category-income".to_owned()),
                memo: None,
            }],
            tag_ids: vec!["tag-1".to_owned()],
            attachment_ids: Vec::new(),
        }
    }

    fn test_ledger_path() -> PathBuf {
        let target = std::env::var_os("CARGO_TARGET_DIR")
            .map(PathBuf::from)
            .unwrap_or_else(|| PathBuf::from("target"));
        let directory = target.join("sqlite-ledger-tests");
        fs::create_dir_all(&directory).unwrap();
        let sequence = TEST_FILE_COUNTER.fetch_add(1, Ordering::Relaxed);
        directory.join(format!("ledger-{}-{sequence}.sqlite", std::process::id()))
    }

    fn ledger_request(currency_code: &str) -> InitializeLedgerRequest {
        InitializeLedgerRequest {
            name: "家庭账簿".to_owned(),
            base_currency: NewCurrency {
                code: currency_code.to_owned(),
                name: "人民币".to_owned(),
                minor_unit: 2,
            },
            initial_account: InitialAccount {
                name: "现金".to_owned(),
                kind: "cash".to_owned(),
                is_asset: true,
            },
            created_at: "2026-07-29T00:00:00+08:00".to_owned(),
        }
    }

    #[test]
    fn creates_and_reopens_current_schema_file() {
        let path = test_ledger_path();
        let _ = fs::remove_file(&path);
        let location = SqliteLedgerLocation::new(&path);
        let store = SqliteLedgerStore::create(location.clone()).unwrap();
        assert_eq!(store.schema_version().unwrap(), CURRENT_SCHEMA_VERSION);
        assert_eq!(store.application_id().unwrap(), EXPECTED_APPLICATION_ID);
        assert_eq!(store.location(), Some(&location));
        drop(store);

        let reopened = SqliteLedgerStore::open(location).unwrap();
        assert_eq!(reopened.schema_version().unwrap(), CURRENT_SCHEMA_VERSION);
        assert_eq!(reopened.application_id().unwrap(), EXPECTED_APPLICATION_ID);
        drop(reopened);
        fs::remove_file(path).unwrap();
    }

    #[test]
    fn financial_goal_schema_preserves_signed_baseline_and_rejects_reversed_period() {
        let mut store = SqliteLedgerStore::create_in_memory().unwrap();
        let initialized =
            reference_data::initialize_ledger(&mut store, &ledger_request("CNY")).unwrap();

        store
            .connection
            .execute(
                "INSERT INTO financial_goals (
                    id, ledger_id, name, target_amount_minor, currency_code,
                    target_date, progress_mode, status, created_at, updated_at,
                    start_date, initial_value_minor, initial_value_captured_at,
                    initial_inputs_json, account_scope_mode, progress_formula_version
                 ) VALUES (
                    ?1, ?2, ?3, ?4, ?5, ?6, ?7, 'active', ?8, ?8,
                    ?9, ?10, ?8, ?11, 'selected', ?12
                 )",
                params![
                    "goal-1",
                    initialized.ledger_id,
                    "受控目标",
                    100_000_i64,
                    "CNY",
                    "2026-10-29",
                    "balance",
                    "2026-07-29T00:00:00+08:00",
                    "2026-07-29",
                    -55_000_000_i64,
                    format!(
                        r#"{{"accounts":[{{"account_id":"{}","value_minor":-55000000}}]}}"#,
                        initialized.initial_account_id
                    ),
                    "pending-calibration-v1",
                ],
            )
            .unwrap();
        store
            .connection
            .execute(
                "INSERT INTO financial_goal_accounts (goal_id, account_id) VALUES (?1, ?2)",
                params!["goal-1", initialized.initial_account_id],
            )
            .unwrap();

        let baseline: (String, String, i64, String, String) = store
            .connection
            .query_row(
                "SELECT start_date, target_date, initial_value_minor,
                        account_scope_mode, progress_formula_version
                 FROM v_goal_progress_inputs
                 WHERE goal_id = 'goal-1'",
                [],
                |row| {
                    Ok((
                        row.get(0)?,
                        row.get(1)?,
                        row.get(2)?,
                        row.get(3)?,
                        row.get(4)?,
                    ))
                },
            )
            .unwrap();
        assert_eq!(
            baseline,
            (
                "2026-07-29".to_owned(),
                "2026-10-29".to_owned(),
                -55_000_000,
                "selected".to_owned(),
                "pending-calibration-v1".to_owned(),
            )
        );

        let reversed = store.connection.execute(
            "UPDATE financial_goals SET start_date = '2026-11-01' WHERE id = 'goal-1'",
            [],
        );
        assert!(reversed.is_err());
    }

    #[test]
    fn planning_repository_creates_and_replaces_budget_items() {
        let mut store = seeded_store();
        let budget = NewBudget {
            ledger_id: "ledger-1".to_owned(),
            name: "2026年8月预算".to_owned(),
            period_kind: BudgetPeriodKind::Monthly,
            start_date: "2026-08-01".to_owned(),
            end_date: "2026-08-31".to_owned(),
            status: BudgetStatus::Active,
            created_at: "2026-08-03T10:00:00+08:00".to_owned(),
            items: vec![NewBudgetItem {
                category_id: "category-income".to_owned(),
                period_start: "2026-08-01".to_owned(),
                period_end: "2026-08-31".to_owned(),
                amount_minor: 50_000,
                currency_code: "CNY".to_owned(),
                rollover_mode: BudgetRolloverMode::None,
                note: Some("首轮预算样例".to_owned()),
            }],
        };

        let budget_id = planning::create_budget(&mut store, &budget).unwrap();
        let budgets = store.list_budgets("ledger-1").unwrap();
        assert_eq!(budgets.len(), 1);
        assert_eq!(budgets[0].id, budget_id);
        assert_eq!(budgets[0].status, BudgetStatus::Active);

        let replacement = [NewBudgetItem {
            category_id: "category-income".to_owned(),
            period_start: "2026-08-01".to_owned(),
            period_end: "2026-08-31".to_owned(),
            amount_minor: 60_000,
            currency_code: "CNY".to_owned(),
            rollover_mode: BudgetRolloverMode::Positive,
            note: None,
        }];
        store
            .replace_budget_items("ledger-1", &budget_id, &replacement)
            .unwrap();
        let items = store.list_budget_items(&budget_id).unwrap();
        assert_eq!(items.len(), 1);
        assert_eq!(items[0].amount_minor, 60_000);
        assert_eq!(items[0].rollover_mode, BudgetRolloverMode::Positive);

        store
            .update_budget(&BudgetChanges {
                id: budget_id.clone(),
                ledger_id: "ledger-1".to_owned(),
                name: "2026年8月预算-关闭".to_owned(),
                period_kind: BudgetPeriodKind::Monthly,
                start_date: "2026-08-01".to_owned(),
                end_date: "2026-08-31".to_owned(),
                status: BudgetStatus::Closed,
                updated_at: "2026-08-04T10:00:00+08:00".to_owned(),
            })
            .unwrap();
        assert_eq!(
            store.list_budgets("ledger-1").unwrap()[0].status,
            BudgetStatus::Closed
        );
    }

    #[test]
    fn planning_repository_creates_goal_and_replaces_account_scope() {
        let mut store = seeded_store();
        let goal = NewFinancialGoal {
            ledger_id: "ledger-1".to_owned(),
            name: "买房首付".to_owned(),
            target_amount_minor: 1_000_000,
            currency_code: "CNY".to_owned(),
            start_date: Some("2026-08-01".to_owned()),
            target_date: Some("2027-08-01".to_owned()),
            progress_mode: FinancialGoalProgressMode::Balance,
            status: FinancialGoalStatus::Active,
            initial_value_minor: Some(10_000),
            initial_value_captured_at: Some("2026-08-03T10:00:00+08:00".to_owned()),
            initial_inputs_json: Some(r#"{"accounts":["account-1"]}"#.to_owned()),
            account_scope_mode: FinancialGoalAccountScopeMode::Selected,
            progress_formula_version: Some("balance-v1".to_owned()),
            account_ids: vec!["account-1".to_owned()],
            created_at: "2026-08-03T10:00:00+08:00".to_owned(),
        };

        let goal_id = planning::create_financial_goal(&mut store, &goal).unwrap();
        let goals = store.list_financial_goals("ledger-1").unwrap();
        assert_eq!(goals.len(), 1);
        assert_eq!(goals[0].id, goal_id);
        assert_eq!(goals[0].initial_value_minor, Some(10_000));

        let account_links: i64 = store
            .connection
            .query_row(
                "SELECT COUNT(*) FROM financial_goal_accounts WHERE goal_id = ?1",
                [&goal_id],
                |row| row.get(0),
            )
            .unwrap();
        assert_eq!(account_links, 1);

        store
            .replace_financial_goal_accounts("ledger-1", &goal_id, &[])
            .unwrap();
        let account_links_after_replace: i64 = store
            .connection
            .query_row(
                "SELECT COUNT(*) FROM financial_goal_accounts WHERE goal_id = ?1",
                [&goal_id],
                |row| row.get(0),
            )
            .unwrap();
        assert_eq!(account_links_after_replace, 0);

        store
            .update_financial_goal(&FinancialGoalChanges {
                id: goal_id.clone(),
                ledger_id: "ledger-1".to_owned(),
                name: "买房首付-完成".to_owned(),
                target_amount_minor: 1_000_000,
                currency_code: "CNY".to_owned(),
                start_date: Some("2026-08-01".to_owned()),
                target_date: Some("2027-08-01".to_owned()),
                progress_mode: FinancialGoalProgressMode::Balance,
                status: FinancialGoalStatus::Completed,
                account_scope_mode: FinancialGoalAccountScopeMode::All,
                progress_formula_version: Some("balance-v1".to_owned()),
                updated_at: "2026-08-04T10:00:00+08:00".to_owned(),
            })
            .unwrap();
        let updated = store.list_financial_goals("ledger-1").unwrap();
        assert_eq!(updated[0].status, FinancialGoalStatus::Completed);
        assert_eq!(
            updated[0].account_scope_mode,
            FinancialGoalAccountScopeMode::All
        );
    }

    #[test]
    fn planning_repository_creates_and_updates_schedule() {
        let mut store = seeded_store();
        store
            .connection
            .execute(
                "INSERT INTO transaction_templates(
                    id, ledger_id, name, transaction_kind, created_at, updated_at
                 ) VALUES ('template-1', 'ledger-1', '月度工资模板', 'income', ?1, ?1)",
                ["2026-08-03T10:00:00+08:00"],
            )
            .unwrap();
        let schedule = NewSchedule {
            ledger_id: "ledger-1".to_owned(),
            template_id: "template-1".to_owned(),
            name: "每月工资计划".to_owned(),
            recurrence_json: r#"{"kind":"monthly","day":3}"#.to_owned(),
            start_date: "2026-08-03".to_owned(),
            end_date: None,
            next_due_date: Some("2026-09-03".to_owned()),
            execution_mode: ScheduleExecutionMode::Manual,
            status: ScheduleStatus::Active,
            max_occurrences: Some(12),
            reminder_lead_days: 2,
            recurrence_version: 1,
            created_at: "2026-08-03T10:00:00+08:00".to_owned(),
        };

        let schedule_id = planning::create_schedule(&mut store, &schedule).unwrap();
        let schedules = store.list_schedules("ledger-1").unwrap();
        assert_eq!(schedules.len(), 1);
        assert_eq!(schedules[0].id, schedule_id);
        assert_eq!(schedules[0].execution_mode, ScheduleExecutionMode::Manual);

        store
            .update_schedule(&ScheduleChanges {
                id: schedule_id,
                ledger_id: "ledger-1".to_owned(),
                template_id: "template-1".to_owned(),
                name: "每月工资计划-暂停".to_owned(),
                recurrence_json: r#"{"kind":"monthly","day":5}"#.to_owned(),
                start_date: "2026-08-03".to_owned(),
                end_date: Some("2026-12-03".to_owned()),
                next_due_date: Some("2026-10-05".to_owned()),
                execution_mode: ScheduleExecutionMode::Automatic,
                status: ScheduleStatus::Paused,
                max_occurrences: Some(6),
                reminder_lead_days: 1,
                recurrence_version: 2,
                updated_at: "2026-08-04T10:00:00+08:00".to_owned(),
            })
            .unwrap();
        let updated = store.list_schedules("ledger-1").unwrap();
        assert_eq!(updated[0].status, ScheduleStatus::Paused);
        assert_eq!(updated[0].recurrence_version, 2);
    }

    #[test]
    fn planning_repository_creates_and_updates_reminder() {
        let mut store = seeded_store();
        let reminder = NewReminder {
            ledger_id: "ledger-1".to_owned(),
            name: "现金余额提醒".to_owned(),
            reminder_kind: "account_balance".to_owned(),
            target_kind: Some("account".to_owned()),
            target_id: Some("account-1".to_owned()),
            condition_json: r#"{"operator":"lt","amount_minor":1000}"#.to_owned(),
            remind_at: None,
            recurrence_json: None,
            next_trigger_at: Some("2026-08-05T09:00:00+08:00".to_owned()),
            status: ReminderStatus::Active,
            is_enabled: true,
            condition_version: 1,
            delivery_mode: ReminderDeliveryMode::InApp,
            created_at: "2026-08-03T10:00:00+08:00".to_owned(),
        };

        let reminder_id = planning::create_reminder(&mut store, &reminder).unwrap();
        let reminders = store.list_reminders("ledger-1").unwrap();
        assert_eq!(reminders.len(), 1);
        assert_eq!(reminders[0].id, reminder_id);
        assert!(reminders[0].is_enabled);

        store
            .update_reminder(&ReminderChanges {
                id: reminder_id,
                ledger_id: "ledger-1".to_owned(),
                name: "现金余额提醒-延后".to_owned(),
                reminder_kind: "account_balance".to_owned(),
                target_kind: Some("account".to_owned()),
                target_id: Some("account-1".to_owned()),
                condition_json: r#"{"operator":"lt","amount_minor":2000}"#.to_owned(),
                remind_at: None,
                recurrence_json: Some(r#"{"kind":"daily"}"#.to_owned()),
                next_trigger_at: Some("2026-08-06T09:00:00+08:00".to_owned()),
                last_triggered_at: Some("2026-08-05T09:00:00+08:00".to_owned()),
                status: ReminderStatus::Snoozed,
                is_enabled: false,
                condition_version: 2,
                delivery_mode: ReminderDeliveryMode::Both,
                updated_at: "2026-08-04T10:00:00+08:00".to_owned(),
            })
            .unwrap();
        let updated = store.list_reminders("ledger-1").unwrap();
        assert_eq!(updated[0].status, ReminderStatus::Snoozed);
        assert!(!updated[0].is_enabled);
        assert_eq!(updated[0].condition_version, 2);
    }

    #[test]
    fn plan_and_reminder_schema_preserves_occurrence_history_and_action_capabilities() {
        let mut store = SqliteLedgerStore::create_in_memory().unwrap();
        let initialized =
            reference_data::initialize_ledger(&mut store, &ledger_request("CNY")).unwrap();
        let now = "2026-08-03T04:30:00+08:00";

        store
            .connection
            .execute(
                "INSERT INTO transaction_templates (
                    id, ledger_id, name, transaction_kind, created_at, updated_at
                 ) VALUES (?1, ?2, ?3, 'expense', ?4, ?4)",
                params![
                    "template-plan-1",
                    initialized.ledger_id,
                    "受控收支计划",
                    now
                ],
            )
            .unwrap();
        store
            .connection
            .execute(
                "INSERT INTO schedules (
                    id, ledger_id, template_id, name, recurrence_json, start_date,
                    next_due_date, execution_mode, status, created_at, updated_at,
                    max_occurrences, reminder_lead_days, recurrence_version
                 ) VALUES (
                    ?1, ?2, ?3, ?4, ?5, '2026-08-03', '2026-08-03',
                    'manual', 'active', ?6, ?6, 3, 3, 1
                 )",
                params![
                    "schedule-1",
                    initialized.ledger_id,
                    "template-plan-1",
                    "每月受控计划",
                    r#"{"version":1,"frequency":"monthly","interval":1}"#,
                    now,
                ],
            )
            .unwrap();
        store
            .connection
            .execute(
                "INSERT INTO schedule_occurrences (
                    id, schedule_id, due_date, recurrence_version, execution_mode,
                    status, source_snapshot_json, idempotency_key, created_at, updated_at
                 ) VALUES (
                    'schedule-occurrence-1', 'schedule-1', '2026-08-03', 1, 'manual',
                    'pending', ?1, 'schedule-1:2026-08-03:v1', ?2, ?2
                 )",
                params![r#"{"amount_minor":1000,"currency_code":"CNY"}"#, now],
            )
            .unwrap();

        store
            .connection
            .execute(
                "INSERT INTO reminders (
                    id, ledger_id, name, reminder_kind, target_kind, target_id,
                    condition_json, next_trigger_at, status, is_enabled,
                    created_at, updated_at, condition_version, delivery_mode
                 ) VALUES (
                    'reminder-1', ?1, '现金低余额', 'account_balance',
                    'account', ?2, ?3, ?4, 'active', 1, ?5, ?5, 1, 'in_app'
                 )",
                params![
                    initialized.ledger_id,
                    initialized.initial_account_id,
                    r#"{"operator":"lt","amount_minor":1000,"currency_code":"CNY"}"#,
                    "2026-08-03T04:00:00+08:00",
                    now,
                ],
            )
            .unwrap();
        store
            .connection
            .execute(
                "INSERT INTO reminder_occurrences (
                    id, reminder_id, trigger_at, condition_version,
                    condition_snapshot_json, observed_value_json, status,
                    created_at, updated_at
                 ) VALUES (
                    'reminder-occurrence-1', 'reminder-1', ?1, 1, ?2, ?3,
                    'pending', ?4, ?4
                 )",
                params![
                    "2026-08-03T04:00:00+08:00",
                    r#"{"operator":"lt","amount_minor":1000,"currency_code":"CNY"}"#,
                    r#"{"balance_minor":500,"currency_code":"CNY"}"#,
                    now,
                ],
            )
            .unwrap();

        let inbox: Vec<(String, String, i64, i64)> = store
            .connection
            .prepare(
                "SELECT source_kind, title, can_execute, can_skip
                 FROM v_today_reminder_inbox ORDER BY source_kind",
            )
            .unwrap()
            .query_map([], |row| {
                Ok((row.get(0)?, row.get(1)?, row.get(2)?, row.get(3)?))
            })
            .unwrap()
            .collect::<Result<_, _>>()
            .unwrap();
        assert_eq!(
            inbox,
            vec![
                ("reminder".to_owned(), "现金低余额".to_owned(), 0, 0),
                ("schedule".to_owned(), "每月受控计划".to_owned(), 1, 1),
            ]
        );

        store
            .connection
            .execute(
                "INSERT INTO transactions (
                    id, ledger_id, sequence_no, business_date, occurred_at,
                    kind, status, theme, created_at, updated_at
                 ) VALUES (
                    'transaction-plan-1', ?1, 1, '2026-08-03', ?2,
                    'expense', 'posted', '计划执行', ?2, ?2
                 )",
                params![initialized.ledger_id, now],
            )
            .unwrap();
        store
            .connection
            .execute(
                "UPDATE schedule_occurrences
                 SET status = 'executed', transaction_id = 'transaction-plan-1',
                     actioned_at = ?1, updated_at = ?1
                 WHERE id = 'schedule-occurrence-1'",
                [now],
            )
            .unwrap();

        let lifecycle: (i64, i64, i64, Option<String>) = store
            .connection
            .query_row(
                "SELECT occurrence_count, executed_count, skipped_count, last_executed_at
                 FROM v_schedule_lifecycle WHERE schedule_id = 'schedule-1'",
                [],
                |row| Ok((row.get(0)?, row.get(1)?, row.get(2)?, row.get(3)?)),
            )
            .unwrap();
        assert_eq!(lifecycle, (1, 1, 0, Some(now.to_owned())));

        let invalid_execution = store.connection.execute(
            "INSERT INTO schedule_occurrences (
                id, schedule_id, due_date, recurrence_version, execution_mode,
                status, source_snapshot_json, idempotency_key, actioned_at,
                created_at, updated_at
             ) VALUES (
                'schedule-occurrence-invalid', 'schedule-1', '2026-09-03', 1,
                'manual', 'executed', '{}', 'schedule-1:2026-09-03:v1', ?1, ?1, ?1
             )",
            [now],
        );
        assert!(invalid_execution.is_err());

        let invalid_reminder_action = store.connection.execute(
            "UPDATE reminder_occurrences
             SET status = 'acknowledged', updated_at = ?1
             WHERE id = 'reminder-occurrence-1'",
            [now],
        );
        assert!(invalid_reminder_action.is_err());
    }

    #[test]
    fn upgrades_supported_versions_and_rejects_foreign_sqlite_identity() {
        let legacy_path = test_ledger_path();
        let _ = fs::remove_file(&legacy_path);
        let legacy_connection = Connection::open(&legacy_path).unwrap();
        for migration in &MIGRATIONS[..6] {
            legacy_connection.execute_batch(migration).unwrap();
        }
        assert_eq!(
            legacy_connection
                .query_row("PRAGMA user_version", [], |row| row.get::<_, i64>(0))
                .unwrap(),
            6
        );
        drop(legacy_connection);

        let upgraded = SqliteLedgerStore::open(SqliteLedgerLocation::new(&legacy_path)).unwrap();
        assert_eq!(upgraded.schema_version().unwrap(), CURRENT_SCHEMA_VERSION);
        assert_eq!(upgraded.application_id().unwrap(), EXPECTED_APPLICATION_ID);
        drop(upgraded);
        fs::remove_file(legacy_path).unwrap();

        let version_seven_path = test_ledger_path();
        let _ = fs::remove_file(&version_seven_path);
        let version_seven_connection = Connection::open(&version_seven_path).unwrap();
        for migration in &MIGRATIONS[..7] {
            version_seven_connection.execute_batch(migration).unwrap();
        }
        assert_eq!(
            version_seven_connection
                .query_row("PRAGMA user_version", [], |row| row.get::<_, i64>(0))
                .unwrap(),
            7
        );
        drop(version_seven_connection);

        let upgraded =
            SqliteLedgerStore::open(SqliteLedgerLocation::new(&version_seven_path)).unwrap();
        assert_eq!(upgraded.schema_version().unwrap(), CURRENT_SCHEMA_VERSION);
        assert_eq!(upgraded.application_id().unwrap(), EXPECTED_APPLICATION_ID);
        drop(upgraded);
        fs::remove_file(version_seven_path).unwrap();

        let version_eight_path = test_ledger_path();
        let _ = fs::remove_file(&version_eight_path);
        let version_eight_connection = Connection::open(&version_eight_path).unwrap();
        for migration in &MIGRATIONS[..8] {
            version_eight_connection.execute_batch(migration).unwrap();
        }
        assert_eq!(
            version_eight_connection
                .query_row("PRAGMA user_version", [], |row| row.get::<_, i64>(0))
                .unwrap(),
            8
        );
        drop(version_eight_connection);

        let upgraded =
            SqliteLedgerStore::open(SqliteLedgerLocation::new(&version_eight_path)).unwrap();
        assert_eq!(upgraded.schema_version().unwrap(), CURRENT_SCHEMA_VERSION);
        assert_eq!(upgraded.application_id().unwrap(), EXPECTED_APPLICATION_ID);
        drop(upgraded);
        fs::remove_file(version_eight_path).unwrap();

        let version_nine_path = test_ledger_path();
        let _ = fs::remove_file(&version_nine_path);
        let version_nine_connection = Connection::open(&version_nine_path).unwrap();
        for migration in &MIGRATIONS[..9] {
            version_nine_connection.execute_batch(migration).unwrap();
        }
        assert_eq!(
            version_nine_connection
                .query_row("PRAGMA user_version", [], |row| row.get::<_, i64>(0))
                .unwrap(),
            9
        );
        drop(version_nine_connection);

        let upgraded =
            SqliteLedgerStore::open(SqliteLedgerLocation::new(&version_nine_path)).unwrap();
        assert_eq!(upgraded.schema_version().unwrap(), CURRENT_SCHEMA_VERSION);
        assert_eq!(upgraded.application_id().unwrap(), EXPECTED_APPLICATION_ID);
        drop(upgraded);
        fs::remove_file(version_nine_path).unwrap();

        let version_ten_path = test_ledger_path();
        let _ = fs::remove_file(&version_ten_path);
        let version_ten_connection = Connection::open(&version_ten_path).unwrap();
        for migration in &MIGRATIONS[..10] {
            version_ten_connection.execute_batch(migration).unwrap();
        }
        assert_eq!(
            version_ten_connection
                .query_row("PRAGMA user_version", [], |row| row.get::<_, i64>(0))
                .unwrap(),
            10
        );
        drop(version_ten_connection);

        let upgraded =
            SqliteLedgerStore::open(SqliteLedgerLocation::new(&version_ten_path)).unwrap();
        assert_eq!(upgraded.schema_version().unwrap(), CURRENT_SCHEMA_VERSION);
        assert_eq!(upgraded.application_id().unwrap(), EXPECTED_APPLICATION_ID);
        drop(upgraded);
        fs::remove_file(version_ten_path).unwrap();

        let version_eleven_path = test_ledger_path();
        let _ = fs::remove_file(&version_eleven_path);
        let version_eleven_connection = Connection::open(&version_eleven_path).unwrap();
        for migration in &MIGRATIONS[..11] {
            version_eleven_connection.execute_batch(migration).unwrap();
        }
        assert_eq!(
            version_eleven_connection
                .query_row("PRAGMA user_version", [], |row| row.get::<_, i64>(0))
                .unwrap(),
            11
        );
        drop(version_eleven_connection);

        let upgraded =
            SqliteLedgerStore::open(SqliteLedgerLocation::new(&version_eleven_path)).unwrap();
        assert_eq!(upgraded.schema_version().unwrap(), CURRENT_SCHEMA_VERSION);
        assert_eq!(upgraded.application_id().unwrap(), EXPECTED_APPLICATION_ID);
        drop(upgraded);
        fs::remove_file(version_eleven_path).unwrap();

        let version_twelve_path = test_ledger_path();
        let _ = fs::remove_file(&version_twelve_path);
        let version_twelve_connection = Connection::open(&version_twelve_path).unwrap();
        for migration in &MIGRATIONS[..12] {
            version_twelve_connection.execute_batch(migration).unwrap();
        }
        assert_eq!(
            version_twelve_connection
                .query_row("PRAGMA user_version", [], |row| row.get::<_, i64>(0))
                .unwrap(),
            12
        );
        drop(version_twelve_connection);

        let upgraded =
            SqliteLedgerStore::open(SqliteLedgerLocation::new(&version_twelve_path)).unwrap();
        assert_eq!(upgraded.schema_version().unwrap(), CURRENT_SCHEMA_VERSION);
        assert_eq!(upgraded.application_id().unwrap(), EXPECTED_APPLICATION_ID);
        drop(upgraded);
        fs::remove_file(version_twelve_path).unwrap();

        let foreign_path = test_ledger_path();
        let _ = fs::remove_file(&foreign_path);
        let foreign_connection = Connection::open(&foreign_path).unwrap();
        foreign_connection
            .execute_batch("PRAGMA user_version = 7; PRAGMA application_id = 0;")
            .unwrap();
        drop(foreign_connection);

        let error = match SqliteLedgerStore::open(SqliteLedgerLocation::new(&foreign_path)) {
            Ok(_) => panic!("其它 SQLite 文件被误识别为 Finance Own 账簿"),
            Err(error) => error,
        };
        assert_eq!(
            error,
            SqliteLedgerError::InvalidApplicationId {
                found: 0,
                expected: EXPECTED_APPLICATION_ID,
            }
        );
        fs::remove_file(foreign_path).unwrap();
    }

    #[test]
    fn initializes_usable_ledger_and_rolls_back_duplicate_currency() {
        let mut store = SqliteLedgerStore::create_in_memory().unwrap();
        let initialized =
            reference_data::initialize_ledger(&mut store, &ledger_request("CNY")).unwrap();

        let ledger = store.get_ledger(&initialized.ledger_id).unwrap();
        assert_eq!(ledger.name, "家庭账簿");
        assert_eq!(ledger.base_currency_code, "CNY");
        let accounts = store.list_accounts(&initialized.ledger_id).unwrap();
        assert_eq!(accounts.len(), 1);
        assert_eq!(accounts[0].id, initialized.initial_account_id);
        assert_eq!(accounts[0].name, "现金");

        let duplicate = reference_data::initialize_ledger(
            &mut store,
            &InitializeLedgerRequest {
                name: "第二账簿".to_owned(),
                ..ledger_request("CNY")
            },
        )
        .unwrap_err();
        assert!(matches!(duplicate, ReferenceDataError::Conflict(_)));
        let counts: (i64, i64, i64) = store
            .connection
            .query_row(
                "SELECT\
                    (SELECT COUNT(*) FROM currencies),\
                    (SELECT COUNT(*) FROM ledgers),\
                    (SELECT COUNT(*) FROM accounts)",
                [],
                |row| Ok((row.get(0)?, row.get(1)?, row.get(2)?)),
            )
            .unwrap();
        assert_eq!(counts, (1, 1, 1));
    }

    #[test]
    fn maintains_account_category_tag_and_party_lifecycle() {
        let mut store = SqliteLedgerStore::create_in_memory().unwrap();
        let initialized =
            reference_data::initialize_ledger(&mut store, &ledger_request("CNY")).unwrap();

        let account_id = store
            .create_account(&NewAccount {
                ledger_id: initialized.ledger_id.clone(),
                group_id: None,
                name: "工资卡".to_owned(),
                kind: "debit_card".to_owned(),
                currency_code: "CNY".to_owned(),
                institution_name: Some("测试银行".to_owned()),
                account_number_masked: Some("****1234".to_owned()),
                is_asset: true,
                created_at: "2026-07-29T01:00:00+08:00".to_owned(),
            })
            .unwrap();
        store
            .update_account(&AccountChanges {
                id: account_id.clone(),
                ledger_id: initialized.ledger_id.clone(),
                group_id: None,
                name: "主工资卡".to_owned(),
                kind: "debit_card".to_owned(),
                institution_name: Some("测试银行".to_owned()),
                account_number_masked: Some("****1234".to_owned()),
                is_hidden: true,
                closed_on: Some("2026-07-29".to_owned()),
            })
            .unwrap();

        let category_id = store
            .create_category(&NewCategory {
                ledger_id: initialized.ledger_id.clone(),
                parent_id: None,
                name: "工资".to_owned(),
                direction: CategoryDirection::Income,
                sort_order: 10,
            })
            .unwrap();
        store
            .update_category(&CategoryChanges {
                id: category_id,
                ledger_id: initialized.ledger_id.clone(),
                parent_id: None,
                name: "薪资".to_owned(),
                direction: CategoryDirection::Income,
                sort_order: 5,
                is_archived: true,
            })
            .unwrap();

        let tag_id = store
            .create_tag(&NewTag {
                ledger_id: initialized.ledger_id.clone(),
                name: "固定收入".to_owned(),
                color: Some("#228B22".to_owned()),
            })
            .unwrap();
        store
            .update_tag(&TagChanges {
                id: tag_id,
                ledger_id: initialized.ledger_id.clone(),
                name: "稳定收入".to_owned(),
                color: Some("#006400".to_owned()),
                is_archived: true,
            })
            .unwrap();

        let party_id = store
            .create_party(&NewParty {
                ledger_id: initialized.ledger_id.clone(),
                name: "测试公司".to_owned(),
                kind: PartyKind::Institution,
                contact: Some("0755-12345678".to_owned()),
                address: Some("深圳".to_owned()),
                sex: None,
                birthday: None,
            })
            .unwrap();
        store
            .update_party(&PartyChanges {
                id: party_id,
                ledger_id: initialized.ledger_id.clone(),
                name: "测试集团".to_owned(),
                kind: PartyKind::Institution,
                contact: Some("0755-87654321".to_owned()),
                address: Some("深圳南山".to_owned()),
                sex: None,
                birthday: None,
                is_hidden: true,
            })
            .unwrap();

        let accounts = store.list_accounts(&initialized.ledger_id).unwrap();
        let updated_account = accounts
            .iter()
            .find(|account| account.id == account_id)
            .unwrap();
        assert_eq!(updated_account.name, "主工资卡");
        assert!(updated_account.is_hidden);
        assert_eq!(updated_account.closed_on.as_deref(), Some("2026-07-29"));
        assert_eq!(
            store.list_categories(&initialized.ledger_id).unwrap()[0].name,
            "薪资"
        );
        assert!(store.list_categories(&initialized.ledger_id).unwrap()[0].is_archived);
        assert_eq!(
            store.list_tags(&initialized.ledger_id).unwrap()[0].name,
            "稳定收入"
        );
        assert!(store.list_tags(&initialized.ledger_id).unwrap()[0].is_archived);
        assert_eq!(
            store.list_parties(&initialized.ledger_id).unwrap()[0].name,
            "测试集团"
        );
        assert!(store.list_parties(&initialized.ledger_id).unwrap()[0].is_hidden);
    }

    #[test]
    fn preserves_person_profile_and_rejects_organization_person_fields() {
        let mut store = SqliteLedgerStore::create_in_memory().unwrap();
        let initialized =
            reference_data::initialize_ledger(&mut store, &ledger_request("CNY")).unwrap();
        let birthday = PartyBirthday {
            calendar: BirthdayCalendar::Lunar,
            year: 1991,
            month: 6,
            day: 7,
        };

        let party_id = store
            .create_party(&NewParty {
                ledger_id: initialized.ledger_id.clone(),
                name: "家庭成员甲".to_owned(),
                kind: PartyKind::FamilyMember,
                contact: Some("13900139034".to_owned()),
                address: Some("深圳".to_owned()),
                sex: Some(PersonSex::Male),
                birthday: Some(birthday),
            })
            .unwrap();
        let party = store
            .list_parties(&initialized.ledger_id)
            .unwrap()
            .remove(0);
        assert_eq!(party.id, party_id);
        assert_eq!(party.kind, PartyKind::FamilyMember);
        assert_eq!(party.contact.as_deref(), Some("13900139034"));
        assert_eq!(party.address.as_deref(), Some("深圳"));
        assert_eq!(party.sex, Some(PersonSex::Male));
        assert_eq!(party.birthday, Some(birthday));

        let invalid = store
            .create_party(&NewParty {
                ledger_id: initialized.ledger_id,
                name: "错误机构".to_owned(),
                kind: PartyKind::Institution,
                contact: None,
                address: None,
                sex: Some(PersonSex::Female),
                birthday: None,
            })
            .unwrap_err();
        assert!(matches!(invalid, ReferenceDataError::InvalidInput(_)));
    }

    #[test]
    fn keeps_party_names_unique_across_categories_and_hidden_records() {
        let mut store = SqliteLedgerStore::create_in_memory().unwrap();
        let initialized =
            reference_data::initialize_ledger(&mut store, &ledger_request("CNY")).unwrap();
        let party_id = store
            .create_party(&NewParty {
                ledger_id: initialized.ledger_id.clone(),
                name: "共享名称".to_owned(),
                kind: PartyKind::ContactPerson,
                contact: None,
                address: None,
                sex: Some(PersonSex::Male),
                birthday: None,
            })
            .unwrap();

        let duplicate = store
            .create_party(&NewParty {
                ledger_id: initialized.ledger_id.clone(),
                name: "共享名称".to_owned(),
                kind: PartyKind::Institution,
                contact: None,
                address: None,
                sex: None,
                birthday: None,
            })
            .unwrap_err();
        assert!(matches!(duplicate, ReferenceDataError::Conflict(_)));

        store
            .update_party(&PartyChanges {
                id: party_id,
                ledger_id: initialized.ledger_id.clone(),
                name: "共享名称".to_owned(),
                kind: PartyKind::ContactPerson,
                contact: None,
                address: None,
                sex: Some(PersonSex::Male),
                birthday: None,
                is_hidden: true,
            })
            .unwrap();
        assert!(store.list_parties(&initialized.ledger_id).unwrap()[0].is_hidden);

        let hidden_duplicate = store
            .create_party(&NewParty {
                ledger_id: initialized.ledger_id,
                name: "共享名称".to_owned(),
                kind: PartyKind::Institution,
                contact: None,
                address: None,
                sex: None,
                birthday: None,
            })
            .unwrap_err();
        assert!(matches!(hidden_duplicate, ReferenceDataError::Conflict(_)));
    }

    #[test]
    fn maintains_account_tree_and_preserves_relations_when_deleting_group() {
        let mut store = SqliteLedgerStore::create_in_memory().unwrap();
        let first = reference_data::initialize_ledger(&mut store, &ledger_request("CNY")).unwrap();
        let second = reference_data::initialize_ledger(&mut store, &ledger_request("USD")).unwrap();
        let root_id = store
            .create_account_group(&NewAccountGroup {
                ledger_id: first.ledger_id.clone(),
                parent_id: None,
                name: "流动资产".to_owned(),
                kind: "asset".to_owned(),
                sort_order: 0,
            })
            .unwrap();
        let child_id = store
            .create_account_group(&NewAccountGroup {
                ledger_id: first.ledger_id.clone(),
                parent_id: Some(root_id.clone()),
                name: "银行账户".to_owned(),
                kind: "asset".to_owned(),
                sort_order: 10,
            })
            .unwrap();
        let grandchild_id = store
            .create_account_group(&NewAccountGroup {
                ledger_id: first.ledger_id.clone(),
                parent_id: Some(child_id.clone()),
                name: "工资账户".to_owned(),
                kind: "asset".to_owned(),
                sort_order: 20,
            })
            .unwrap();
        let account_id = store
            .create_account(&NewAccount {
                ledger_id: first.ledger_id.clone(),
                group_id: Some(child_id.clone()),
                name: "工资卡".to_owned(),
                kind: "debit_card".to_owned(),
                currency_code: "CNY".to_owned(),
                institution_name: None,
                account_number_masked: None,
                is_asset: true,
                created_at: "2026-07-29T02:00:00+08:00".to_owned(),
            })
            .unwrap();

        let cross_ledger = store
            .create_account(&NewAccount {
                ledger_id: second.ledger_id,
                group_id: Some(root_id.clone()),
                name: "错误分组账户".to_owned(),
                kind: "cash".to_owned(),
                currency_code: "USD".to_owned(),
                institution_name: None,
                account_number_masked: None,
                is_asset: true,
                created_at: "2026-07-29T02:00:00+08:00".to_owned(),
            })
            .unwrap_err();
        assert!(matches!(cross_ledger, ReferenceDataError::Conflict(_)));

        let cycle = store
            .update_account_group(&AccountGroupChanges {
                id: root_id.clone(),
                ledger_id: first.ledger_id.clone(),
                parent_id: Some(grandchild_id.clone()),
                name: "流动资产".to_owned(),
                kind: "asset".to_owned(),
                sort_order: 0,
            })
            .unwrap_err();
        assert!(matches!(cycle, ReferenceDataError::Conflict(_)));

        let deleted = store
            .delete_account_group(&first.ledger_id, &child_id)
            .unwrap();
        assert_eq!(deleted.reassigned_accounts, 1);
        assert_eq!(deleted.reassigned_child_groups, 1);
        let account = store
            .list_accounts(&first.ledger_id)
            .unwrap()
            .into_iter()
            .find(|account| account.id == account_id)
            .unwrap();
        assert_eq!(account.group_id.as_deref(), Some(root_id.as_str()));
        let groups = store.list_account_groups(&first.ledger_id).unwrap();
        assert_eq!(groups.len(), 2);
        let grandchild = groups
            .iter()
            .find(|group| group.id == grandchild_id)
            .unwrap();
        assert_eq!(grandchild.parent_id.as_deref(), Some(root_id.as_str()));
    }

    #[test]
    fn rolls_back_account_group_delete_when_reparenting_conflicts() {
        let mut store = SqliteLedgerStore::create_in_memory().unwrap();
        let initialized =
            reference_data::initialize_ledger(&mut store, &ledger_request("CNY")).unwrap();
        let root_id = store
            .create_account_group(&NewAccountGroup {
                ledger_id: initialized.ledger_id.clone(),
                parent_id: None,
                name: "资产".to_owned(),
                kind: "asset".to_owned(),
                sort_order: 0,
            })
            .unwrap();
        store
            .create_account_group(&NewAccountGroup {
                ledger_id: initialized.ledger_id.clone(),
                parent_id: Some(root_id.clone()),
                name: "重复名称".to_owned(),
                kind: "asset".to_owned(),
                sort_order: 0,
            })
            .unwrap();
        let deleting_id = store
            .create_account_group(&NewAccountGroup {
                ledger_id: initialized.ledger_id.clone(),
                parent_id: Some(root_id),
                name: "待删除".to_owned(),
                kind: "asset".to_owned(),
                sort_order: 10,
            })
            .unwrap();
        store
            .create_account_group(&NewAccountGroup {
                ledger_id: initialized.ledger_id.clone(),
                parent_id: Some(deleting_id.clone()),
                name: "重复名称".to_owned(),
                kind: "asset".to_owned(),
                sort_order: 0,
            })
            .unwrap();
        let account_id = store
            .create_account(&NewAccount {
                ledger_id: initialized.ledger_id.clone(),
                group_id: Some(deleting_id.clone()),
                name: "受保护账户".to_owned(),
                kind: "cash".to_owned(),
                currency_code: "CNY".to_owned(),
                institution_name: None,
                account_number_masked: None,
                is_asset: true,
                created_at: "2026-07-29T03:00:00+08:00".to_owned(),
            })
            .unwrap();

        let error = store
            .delete_account_group(&initialized.ledger_id, &deleting_id)
            .unwrap_err();
        assert!(matches!(error, ReferenceDataError::Conflict(_)));
        let account = store
            .list_accounts(&initialized.ledger_id)
            .unwrap()
            .into_iter()
            .find(|account| account.id == account_id)
            .unwrap();
        assert_eq!(account.group_id.as_deref(), Some(deleting_id.as_str()));
        assert!(store
            .list_account_groups(&initialized.ledger_id)
            .unwrap()
            .iter()
            .any(|group| group.id == deleting_id));
    }

    #[test]
    fn rejects_self_parent_and_unknown_cross_ledger_update() {
        let mut store = SqliteLedgerStore::create_in_memory().unwrap();
        let initialized =
            reference_data::initialize_ledger(&mut store, &ledger_request("CNY")).unwrap();
        let category_id = store
            .create_category(&NewCategory {
                ledger_id: initialized.ledger_id.clone(),
                parent_id: None,
                name: "日常".to_owned(),
                direction: CategoryDirection::Both,
                sort_order: 0,
            })
            .unwrap();

        let self_parent = store
            .update_category(&CategoryChanges {
                id: category_id.clone(),
                ledger_id: initialized.ledger_id.clone(),
                parent_id: Some(category_id.clone()),
                name: "日常".to_owned(),
                direction: CategoryDirection::Both,
                sort_order: 0,
                is_archived: false,
            })
            .unwrap_err();
        assert!(matches!(self_parent, ReferenceDataError::InvalidInput(_)));

        let second = reference_data::initialize_ledger(&mut store, &ledger_request("USD")).unwrap();
        let cross_ledger_parent = store
            .create_category(&NewCategory {
                ledger_id: second.ledger_id,
                parent_id: Some(category_id),
                name: "跨账簿分类".to_owned(),
                direction: CategoryDirection::Both,
                sort_order: 0,
            })
            .unwrap_err();
        assert!(matches!(
            cross_ledger_parent,
            ReferenceDataError::Conflict(_)
        ));

        let missing = store
            .update_tag(&TagChanges {
                id: "missing-tag".to_owned(),
                ledger_id: initialized.ledger_id,
                name: "不存在".to_owned(),
                color: None,
                is_archived: false,
            })
            .unwrap_err();
        assert!(matches!(missing, ReferenceDataError::NotFound(_)));
    }

    #[test]
    fn writes_income_and_reads_exact_tag_and_balance() {
        let mut store = seeded_store();
        let created = transactions::create_transaction(&mut store, &valid_income()).unwrap();
        assert_eq!(created.sequence_no, 1);

        let entries = store
            .list_ledger_entries(&LedgerEntryFilter {
                ledger_id: "ledger-1".to_owned(),
                date_range: None,
                account_ids: Vec::new(),
                category_ids: Vec::new(),
                tag_ids: Vec::new(),
                include_voided: false,
            })
            .unwrap();
        assert_eq!(entries.len(), 1);
        assert_eq!(entries[0].signed_amount_minor, 10_000);
        assert_eq!(entries[0].tag_names, vec!["日常,生活"]);

        let balances = store.list_account_balances("ledger-1").unwrap();
        assert_eq!(balances.len(), 1);
        assert_eq!(balances[0].balance_minor, 10_000);
    }

    #[test]
    fn rolls_back_header_when_related_tag_is_missing() {
        let mut store = seeded_store();
        let mut income = valid_income();
        income.tag_ids = vec!["missing-tag".to_owned()];

        let error = transactions::create_transaction(&mut store, &income).unwrap_err();
        assert!(matches!(error, TransactionWriteError::Conflict(_)));
        let transaction_count: i64 = store
            .connection
            .query_row("SELECT COUNT(*) FROM transactions", [], |row| row.get(0))
            .unwrap();
        assert_eq!(transaction_count, 0);
    }

    #[test]
    fn queries_running_tagged_and_investment_projections() {
        let mut store = seeded_store();
        transactions::create_transaction(&mut store, &valid_income()).unwrap();
        store
            .connection
            .execute_batch(
                "INSERT INTO account_tags(account_id, tag_id) VALUES ('account-1', 'tag-1');\
                 INSERT INTO investment_instruments(\
                     id, ledger_id, code, name, kind, quote_currency_code, quantity_scale, price_scale\
                 ) VALUES ('instrument-1', 'ledger-1', 'TEST', '测试证券', 'security', 'CNY', 3, 2);\
                 INSERT INTO transactions(\
                     id, ledger_id, sequence_no, business_date, occurred_at, kind, status, created_at, updated_at\
                 ) VALUES\
                     ('investment-transaction-1', 'ledger-1', 2, '2026-07-29',\
                      '2026-07-29T10:00:00+08:00', 'investment_buy', 'posted',\
                      '2026-07-29T10:00:00+08:00', '2026-07-29T10:00:00+08:00'),\
                     ('investment-transaction-2', 'ledger-1', 3, '2026-07-29',\
                      '2026-07-29T11:00:00+08:00', 'investment_sell', 'posted',\
                      '2026-07-29T11:00:00+08:00', '2026-07-29T11:00:00+08:00');\
                 INSERT INTO investment_trades(\
                     id, transaction_id, account_id, instrument_id, trade_kind, position_effect,\
                     quantity_units, price_units, price_scale\
                 ) VALUES\
                     ('trade-buy', 'investment-transaction-1', 'account-1', 'instrument-1',\
                      'buy', 1, 100, 1000, 2),\
                     ('trade-sell', 'investment-transaction-2', 'account-1', 'instrument-1',\
                      'sell', -1, 40, 1200, 2);\
                 INSERT INTO investment_lot_allocations(\
                     id, sell_trade_id, buy_trade_id, quantity_units,\
                     allocated_cost_minor, allocated_proceeds_minor\
                 ) VALUES ('allocation-1', 'trade-sell', 'trade-buy', 40, 40000, 48000);",
            )
            .unwrap();

        let ledger_filter = LedgerEntryFilter {
            ledger_id: "ledger-1".to_owned(),
            date_range: None,
            account_ids: Vec::new(),
            category_ids: Vec::new(),
            tag_ids: vec!["tag-1".to_owned()],
            include_voided: false,
        };
        let running = store.list_account_running_balances(&ledger_filter).unwrap();
        assert_eq!(running.len(), 1);
        assert_eq!(running[0].balance_minor, 10_000);

        let tagged_entries = store.list_tagged_entries(&ledger_filter).unwrap();
        assert_eq!(tagged_entries.len(), 1);
        assert_eq!(tagged_entries[0].tag_name, "日常,生活");
        let tagged_assets = store
            .list_tagged_assets("ledger-1", &["tag-1".to_owned()])
            .unwrap();
        assert_eq!(tagged_assets.len(), 1);
        assert_eq!(tagged_assets[0].account.balance_minor, 10_000);

        let investment_filter = InvestmentProjectionFilter {
            ledger_id: "ledger-1".to_owned(),
            account_ids: Vec::new(),
            instrument_ids: Vec::new(),
            date_range: None,
        };
        let positions = store
            .list_investment_position_inputs(&investment_filter)
            .unwrap();
        assert_eq!(positions.len(), 1);
        assert_eq!(positions[0].net_quantity, ScaledValue::new(60, 3));
        assert_eq!(positions[0].bought_quantity, ScaledValue::new(100, 3));
        assert_eq!(positions[0].sold_quantity, ScaledValue::new(40, 3));

        let realized = store
            .list_realized_profit_inputs(&investment_filter)
            .unwrap();
        assert_eq!(realized.len(), 1);
        assert_eq!(realized[0].sold_quantity, ScaledValue::new(40, 3));
        assert_eq!(realized[0].price, Some(ScaledValue::new(1200, 2)));
        assert_eq!(realized[0].allocated_quantity, ScaledValue::new(40, 3));
        assert_eq!(realized[0].allocated_cost_minor, 40_000);
        assert_eq!(realized[0].allocated_proceeds_minor, 48_000);
    }
}
