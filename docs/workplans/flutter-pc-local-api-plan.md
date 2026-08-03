# Flutter PC 本地 API 需求计划

本文档承接 `three-client-requirements-analysis.md`，把 Flutter Desktop 与 Rust PC 本地核心之间的第一版 API 需求拆成可实施边界。本文属于进行中工作计划，后续 API 定稿后再回填到长期架构和接口文档。

## 1. 目标

第一版 PC 本地 API 必须让 Flutter Desktop 完成本地账本首屏、账户中心、最近流水、常用记账、同步入口和旧迁移入口，同时保持以下边界：

- Flutter 不直接访问 SQLite。
- Flutter 不拼接 SQL。
- Flutter 不读取旧 MoneyHome8 原始文件。
- Rust 可以改变 SQLite 内部结构，但必须保持 API 业务契约稳定。
- API 返回 DTO、结构化错误和命令结果，不返回数据库表行。
- API 错误不得包含完整敏感路径、密钥、旧原始行或未脱敏迁移诊断。

## 2. 当前 Rust 基础

| 能力 | 当前代码基础 | 缺口 |
| --- | --- | --- |
| 账本会话 | `app::workspace_shell` | 需要 FFI 友好的 DTO 和打开/关闭 API 包装 |
| 首页视图 | `app::ui::WorkspaceHomeViewModel` | 需要序列化边界、分页、筛选和错误码 |
| 账户中心 | `app::ui::AccountCenterViewModel` | 需要 Flutter 字段命名和空状态 |
| 基础资料 | `app::reference_data::ReferenceDataRepository` | 需要本地 API 查询入口 |
| 报表读取 | `app::reporting::ReportReadRepository` | 需要首屏最近流水和分页 |
| 交易写入 | `app::transactions::create_transaction` | 需要收入、支出、转账命令 DTO |
| 计划预算 | `app::planning::PlanningRepository` | 需要后续预算/提醒页面 API |
| 旧来源探测 | `domain::legacy_source`、`infrastructure::mh8`、`cache_file`、`reference_json` | 需要迁移预览和确认导入 API |

## 3. API 分组

### 3.1 LedgerSessionApi

| API | 输入 | 输出 |
| --- | --- | --- |
| `get_session` | 无 | `LocalLedgerSessionDto` |
| `create_local_ledger` | `CreateLocalLedgerRequestDto` | `LocalLedgerSessionDto` |
| `open_local_ledger` | `OpenLocalLedgerRequestDto` | `LocalLedgerSessionDto` |
| `close_local_ledger` | `CloseLocalLedgerRequestDto` | `LocalLedgerSessionDto` |

`LocalLedgerSessionDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `state` | `no_ledger`、`opening`、`opened`、`closing`、`failed` |
| `ledger_id` | 已打开账本 ID，未打开时为空 |
| `ledger_name` | 已打开账本名称 |
| `local_file_label` | 脱敏后的本地文件展示名 |
| `failure_code` | 失败错误码 |
| `failure_message` | 可展示错误说明 |

### 3.2 WorkspaceApi

| API | 输入 | 输出 |
| --- | --- | --- |
| `load_workspace_home` | `ledger_id`、最近流水数量 | `WorkspaceHomeDto` |
| `refresh_account_center` | `ledger_id` | `AccountCenterDto` |
| `list_recent_entries` | `LedgerEntryListRequestDto` | `PagedLedgerEntryDto` |

`WorkspaceHomeDto` 必须包含：

1. 账簿信息。
2. 工作区状态。
3. 账户中心。
4. 最近流水。
5. 同步入口摘要。

### 3.2.1 WorkspaceHomeDto 字段

| 字段 | 可为空 | 数据来源 | 说明 |
| --- | --- | --- | --- |
| `ledger` | 否 | `LedgerRecord` | 当前账簿基础信息，只暴露新系统账簿 ID、名称、默认币种和业务状态 |
| `shell` | 否 | `WorkspaceShellState` | 顶层会话、当前工作区和加载状态 |
| `account_center` | 否 | `AccountCenterViewModel` | 账户树、未分组账户、资产汇总和负债汇总 |
| `recent_entries` | 否 | `LedgerEntryProjection` | 首屏最近流水，默认不包含作废记录 |
| `sync_summary` | 否 | `LocalSyncStatusDto` | 同步入口摘要，未登录或未开启同步时也必须返回 |

### 3.2.2 ShellDto 字段

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `session_state` | 否 | `no_ledger`、`opening`、`opened`、`closing`、`failed` |
| `active_workspace` | 否 | `finance_data`、`bookkeeping`、`financial_reports`、`financial_analysis` |
| `load_state` | 否 | `empty`、`loading`、`ready`、`failed` |
| `failure` | 是 | 加载失败时返回 `LocalApiErrorDto`，必须脱敏 |

### 3.2.3 AccountCenterDto 字段

| 字段 | 可为空 | 数据来源 | 说明 |
| --- | --- | --- | --- |
| `groups` | 否 | `AccountGroupViewNode` | 有分组归属的账户树 |
| `ungrouped_accounts` | 否 | `AccountViewRow` | 没有关联账户组或原组已失效的账户 |
| `asset_totals` | 否 | `CurrencyBalanceSummary` | 按币种汇总的资产余额 |
| `liability_totals` | 否 | `CurrencyBalanceSummary` | 按币种汇总的负债余额 |

`AccountGroupDto` 字段：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `id` | 否 | 账户组稳定标识 |
| `name` | 否 | 账户组名称 |
| `kind` | 否 | 分组类型键，Flutter 用于图标和筛选 |
| `sort_order` | 否 | 同级排序值 |
| `accounts` | 否 | 当前组直属账户 |
| `children` | 否 | 当前组直属子组 |

`AccountRowDto` 字段：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `id` | 否 | 账户稳定标识 |
| `group_id` | 是 | 账户组标识；为空时归入未分组 |
| `name` | 否 | 账户名称 |
| `kind` | 否 | 账户类型键 |
| `currency_code` | 否 | ISO 4217 或本地约定币种代码 |
| `balance_minor` | 否 | 账户币种最小单位余额 |
| `is_asset` | 否 | `true` 为资产账户，`false` 为负债账户 |
| `is_hidden` | 否 | 隐藏账户仍可在管理视图显示 |
| `closed_on` | 是 | 账户关闭业务日期 |

### 3.2.4 RecentEntryDto 字段

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `transaction_id` | 否 | 交易稳定标识 |
| `sequence_no` | 否 | 账簿内单调序号，用于稳定排序和分页游标 |
| `business_date` | 否 | 业务日期，格式 `YYYY-MM-DD` |
| `occurred_at` | 否 | 实际发生时间，ISO 8601 文本 |
| `kind` | 否 | `income`、`expense`、`transfer`、`adjustment` 或扩展类型键 |
| `title` | 否 | 页面展示标题，由 Rust 侧按业务对象生成 |
| `amount_minor` | 否 | 主展示金额，最小单位整数 |
| `currency_code` | 否 | 主展示金额币种 |
| `account_labels` | 否 | 相关账户展示名，必须来自新系统账户对象 |
| `category_label` | 是 | 收支分类展示名 |
| `description` | 是 | 交易说明 |
| `status` | 否 | `draft`、`posted`、`voided`、`deleted_tombstone` 等页面状态 |
| `sync_state` | 否 | `local_only`、`pending_upload`、`synced`、`conflicted`、`failed` |

### 3.3 TransactionCommandApi

| API | 输入 | 输出 |
| --- | --- | --- |
| `create_income` | `CreateIncomeCommandDto` | `CreatedTransactionDto` |
| `create_expense` | `CreateExpenseCommandDto` | `CreatedTransactionDto` |
| `create_transfer` | `CreateTransferCommandDto` | `CreatedTransactionDto` |

命令 DTO 只表达用户业务输入，不要求 Flutter 构造原子分录。

| 命令 | Rust 本地核心责任 |
| --- | --- |
| 收入 | 生成收入交易和流入分录，校验分类方向、账户、币种和金额 |
| 支出 | 生成支出交易和流出分录，校验分类方向、账户、币种和金额 |
| 转账 | 生成转出、转入和可选手续费分录，确保同一事务提交 |

### 3.3.1 通用命令字段

收入、支出和转账命令都必须包含：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `client_command_id` | 否 | Flutter 生成的幂等命令 ID，用于避免重复点击或重试造成重复写入 |
| `ledger_id` | 否 | 目标账簿；不得从全局状态隐式推断 |
| `business_date` | 否 | 业务日期，格式 `YYYY-MM-DD` |
| `occurred_at` | 否 | 实际发生时间，ISO 8601 文本 |
| `amount_minor` | 否 | 主金额，最小单位整数且必须大于零 |
| `currency_code` | 否 | 主金额币种 |
| `party_id` | 是 | 人员或机构标识 |
| `description` | 是 | 交易说明 |
| `tag_ids` | 否 | 标签标识列表，同一命令不得重复 |
| `attachment_ids` | 否 | 已落盘的新系统附件标识 |

收入命令额外字段：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `account_id` | 否 | 收入流入账户 |
| `category_id` | 否 | 收入分类，Rust 必须校验分类方向 |

支出命令额外字段：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `account_id` | 否 | 支出流出账户 |
| `category_id` | 否 | 支出分类，Rust 必须校验分类方向 |

转账命令额外字段：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `from_account_id` | 否 | 转出账户 |
| `to_account_id` | 否 | 转入账户，不能与转出账户相同 |
| `fee_amount_minor` | 是 | 手续费金额；为空表示无手续费 |
| `fee_account_id` | 是 | 手续费承担账户；有手续费时必须明确 |
| `fee_category_id` | 是 | 手续费分类；第一版可为空，但 Rust 必须保留字段 |

`CreatedTransactionDto` 字段：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `transaction_id` | 否 | 新交易标识 |
| `sequence_no` | 否 | 同一 SQLite 事务中分配的账簿内单调序号 |
| `sync_state` | 否 | 创建后的本地同步状态 |
| `created_at` | 否 | 本地创建时间，ISO 8601 文本 |
| `affected_account_ids` | 否 | 受余额影响的账户 ID 列表 |

### 3.4 LocalSyncEntryApi

| API | 输入 | 输出 |
| --- | --- | --- |
| `get_local_sync_status` | `ledger_id` | `LocalSyncStatusDto` |
| `confirm_enable_sync` | `ledger_id`、用户确认摘要 | `LocalSyncStatusDto` |
| `list_local_conflicts` | `ledger_id`、分页 | `PagedConflictDto` |

第一版可以先返回本地同步入口状态，不要求完成真实联网同步。

### 3.5 LegacyMigrationApi

| API | 输入 | 输出 |
| --- | --- | --- |
| `inspect_legacy_source` | 旧文件选择结果 | `LegacySourceInspectionDto` |
| `preview_legacy_migration` | 旧来源和迁移选项 | `LegacyMigrationPreviewDto` |
| `confirm_legacy_import` | 迁移批次 ID、用户确认 | `LegacyImportResultDto` |

迁移 API 必须遵守：

1. 旧 MoneyHome8 原始文件不上传云端。
2. 迁移审计、迁移报告和脱敏摘要只保存在 PC 本地。
3. 迁移预览必须在写入 PC SQLite 前展示风险和阻塞项。
4. 导入失败必须可追溯并支持重新预览。

## 4. 错误码需求

| 错误码 | 场景 | Flutter 行为 |
| --- | --- | --- |
| `validation_failed` | 字段输入无效 | 标记字段或表单 |
| `ledger_not_open` | 没有打开账本 | 引导打开或创建 |
| `ledger_not_found` | 账本不存在 | 提示重新选择 |
| `foreign_sqlite_identity` | 非 Finance Own SQLite | 拒绝打开 |
| `unsupported_schema_version` | SQLite 版本不支持 | 提示升级或恢复 |
| `account_not_found` | 账户不存在或不属账本 | 刷新账户中心 |
| `currency_mismatch` | 账户币种和输入币种不匹配 | 标记币种字段 |
| `category_direction_mismatch` | 分类方向不允许 | 标记分类字段 |
| `transaction_conflict` | 本地版本或同步冲突 | 引导冲突处理 |
| `storage_failed` | 本地存储失败 | 展示脱敏诊断 |
| `legacy_invalid_format` | 旧来源格式不识别 | 展示迁移阻塞 |
| `legacy_auth_failed` | 旧来源认证失败 | 展示认证缺口 |
| `legacy_locked` | 旧来源被占用 | 提示关闭原程序或重试 |

### 4.1 LocalApiResult 包装

FFI 或本地桥接层必须使用统一结果包装，避免 Flutter 依赖 Rust 异常或字符串解析。

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `ok` | 否 | 成功为 `true`，失败为 `false` |
| `data` | 是 | 成功时返回具体 DTO |
| `error` | 是 | 失败时返回 `LocalApiErrorDto` |

`LocalApiErrorDto` 字段：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `code` | 否 | 稳定错误码 |
| `message` | 否 | 可展示的脱敏错误说明 |
| `field_errors` | 否 | 字段级错误列表；没有字段错误时为空数组 |
| `recoverable` | 否 | 是否允许用户修正输入或重试 |
| `diagnostic_id` | 是 | 本地诊断标识；不得包含完整路径、密钥、旧原始行或机器隐私 |

## 5. 验收口径

1. 每个 API 都必须有明确输入、输出和错误码。
2. 每个 DTO 字段都必须说明业务含义、是否可为空和数据来源。
3. 金额字段必须使用最小单位整数和币种代码。
4. 日期字段必须明确是业务日期还是发生时间。
5. 账本范围必须显式传入或由当前会话唯一确定。
6. Flutter 不需要知道 SQLite 表名、旧表名或迁移内部路径。
7. 迁移诊断、存储错误和路径信息必须脱敏。

## 6. 可直接实施的第一批任务

1. 为 `WorkspaceHomeViewModel` 增加 FFI/序列化友好的 DTO 映射层。
2. 为 `load_workspace_home` 增加最近流水数量限制。
3. 增加 `CreateIncomeCommandDto`、`CreateExpenseCommandDto`、`CreateTransferCommandDto` 到应用层。
4. 增加 PC 本地 API 错误码枚举，并映射现有 `ReferenceDataError`、`ReportReadError`、`TransactionWriteError` 和 `LegacySourceStatus`。
5. 增加本地同步入口 DTO，先表达未登录、已登录未开启同步、同步中、冲突待处理和失败状态。

## 7. 当前无需人工确认

本计划没有引入新的产品取舍；它只是把已确认的三端架构和 PC 本地边界拆成 API 需求。
