# Finance Own

这是 对标 `MoneyHome8` 的重构工程骨架。

当前阶段目标：

1. 以 SQLite 单文件账簿承载新系统真相数据，不复刻旧 Jet 表结构。
2. 通过只读 `legacy_import` 边界逐步接入 `test.mh8`，不直接污染原始账本。
3. 按已确认功能、查询投影和代表性样例逐步实现桌面 UI 与计算兼容。

当前目录说明：

- `src/main.rs`：程序入口。
- `src/app`：应用编排层。
- `src/domain`：领域模型与业务规则。
- `src/infrastructure`：文件格式、存储、适配器等基础设施代码。
- `migrations`：可执行的 SQLite 新账簿迁移。
- `docs`：重构设计与功能对照文档。

当前可执行验证：

```powershell
& .\tools\run-rust-checks.ps1 -Action all
python tools\validate_sqlite_schema.py
python tools\summarize_runtime_calculations.py
python tools\summarize_runtime_commands.py
python tools\summarize_runtime_event_handlers.py
python tools\summarize_event_dataflows.py
python tools\generate_runtime_execution_queue.py
python tools\generate_b01_system_shell_records.py
python tools\generate_b02_accounts_master_data_records.py
python tools\generate_b03_transactions_records.py
python tools\generate_b04_debts_credit_records.py
python tools\generate_b05_financial_products_records.py
python tools\generate_b07_investment_shared_records.py
python tools\generate_b08_securities_records.py
python tools\sanitize_b09_screenshots.py
python tools\generate_b09_open_funds_records.py
python tools\generate_target_ui_consolidation.py
python tools\summarize_sqlite_domain_coverage.py
python tools\refresh_analysis_package.py
```

MoneyHome8 动态场景不得复用历史 PID 或 HWND。启动并核对测试账簿基线后，先运行 `tools/moneyhome-session-context.ps1` 获取当前唯一进程、主窗和记账工具栏上下文；命令探针还必须指定预期 Delphi 对话框类名。

说明：

- `src/app/command_state.rs` 已定义选择、批量、报表加载、导入和标签命令状态。
- `src/domain/transactions.rs` 与 `src/app/transactions.rs` 已定义通用交易校验和原子写入仓储契约。
- `src/domain/reference_data.rs` 与 `src/app/reference_data.rs` 已定义账簿初始化、账户组、账户、分类、标签和往来方生命周期契约。
- `src/app/destructive_operations.rs` 已定义删除影响预览、业务阻断、确认修订标记和原子执行契约。
- `src/infrastructure/sqlite.rs` 已实现新账簿创建/打开、应用文件标识校验、可用账簿初始化、账户树和基础资料维护、十三版迁移、完整性检查、原子交易写入和七组报表查询端口。
- SQLite 验证已覆盖收入、支出、转账、手续费、余额投影、失败整体回滚、账户组解绑和附件引用保护。
- `docs/runtime-execution-queue.json` 已把全部窗体、交互控件、事件和宿主关系转换为逐项动态验证队列。
- B01 的 `15/15` 个系统外壳窗体已形成结构化部分观察记录；主窗口、菜单、新建、结算、备份、还原、密码、设置、快捷键、关于和授权入口均已有脱敏证据。
- `docs/runtime-ledger-lifecycle-and-settings-contract.md` 已固定账簿新建、备份、还原、结算、密码、设置作用域、快捷键和授权隔离规则。
- B02 的 `41/41` 个账户与基础资料资源已形成结构化部分观察记录；账户类型目录、代表性开户向导、分类、人员、币种、汇率和存款利率均已有脱敏证据。
- `docs/runtime-accounts-and-master-data-contract.md` 已固定组合账户原子创建、期初资金来源、基础资料引用保护、汇率方向和利率版本化规则。
- B03 的 `38/38` 个交易与流水资源已形成结构化部分观察记录；财务记录、账户流水、单笔/批量编辑器、查找筛选和概况图表已有运行证据，日常收入、日常支出、带来源手续费的取款、同币种转账、钱包零手续费双向流，以及充值/提现均由资金发出侧承担手续费的规则已完成真实保存与冷启动复核。
- `docs/runtime-transactions-and-ledger-contract.md` 已固定平衡分录、批次、模板、分期、审计和查询投影规则。
- B04 的 `54/54` 个债权债务、信用卡、分期与网贷资源已形成结构化部分观察记录；临时零余额信用卡已在指定测试账簿中创建并永久删除。
- `docs/runtime-debts-credit-and-amortization-contract.md` 已固定合同版本、本息费用拆分、还款计划、账单、分期和网贷关联规则。
- B05 的 `19/19` 个定期存款与银行理财资源已形成结构化部分观察记录；临时零余额银行理财账户已在指定测试账簿中创建并永久删除，未创建产品或持仓。
- `docs/runtime-deposits-and-bank-wealth-contract.md` 已固定定期账户、存单、续存周期、理财产品、持仓本金和到期事件的领域边界。
- B07 的 `6/6` 个投资公共资源已形成结构化部分观察记录；投资一览、成本/市值构成图、历史盈亏、市值变动及共享调整/现金事件已有运行证据。
- `docs/runtime-investment-shared-projections-contract.md` 已固定交易事实、持仓批次、估值快照和查询投影的分层规则。
- B08 的 `21/21` 个上市证券资源已形成结构化部分观察记录；证券账户、资料、行情、费率、交易明细、持仓估值、市值构成、历史盈亏及七类交易/公司行为表单已有运行或明确静态边界证据。
- `docs/runtime-securities-ledger-and-valuation-contract.md` 已固定证券身份、代码变更、账户费率继承、交易原子性、持仓批次、新股关系和估值快照规则。
- B09 的 `29/29` 个开放式基金与货币基金资源已形成结构化部分观察记录；账户、向导、资料目录、净值、持仓、交易、市值和历史盈亏均已有运行或明确组合证据。
- `docs/runtime-open-and-money-market-funds-contract.md` 已固定两类基金的差异化目录、账户、金额/份额换算、转换、认购、分红、拆分和估值规则。
- B10 的 `15/15` 个债券资源已形成结构化部分观察记录；债券资料、账户向导/编辑/概况、持仓、交易明细、成本市值构成、历史盈亏及买入、卖出、到期、提前兑取和利息表单均已有运行证据。
- `docs/runtime-bonds-ledger-and-maturity-contract.md` 已固定债券身份、账户资金来源、净价/全价、应计利息、成本批次、估值及到期与提前兑取事件边界。
- `docs/target-ui-consolidation-map.json` 已把 `460` 个旧窗体归并到现代 Rust 页面族，同时保留逐窗体追溯。
- `migrations/0002_planning_and_automation.sql` 已补模板计划、预算、提醒、目标和规划输入。
- `migrations/0003_contracts_exchange_and_sync.sql` 已补专属合同、导入审计、同步冲突、通知投递、设置和费率快照。
- `migrations/0004_insurance_cash_value.sql` 已补保险现金价值快照、变更审计和保险事件。
- `migrations/0005_insurance_cash_value_as_of.sql` 已补按查询基准日选择现金价值的生效区间视图。
- `migrations/0006_insurance_cash_value_amount_guard.sql` 已补现金价值非负数据库约束。
- `migrations/0007_payroll_income_and_application_identity.sql` 已补工资收入组成、账户投影核对和 SQLite 应用文件标识。
- `migrations/0008_party_profile.sql` 已补人员与机构精确分类、联系方式、地址、性别和带历法生日字段。
- `migrations/0009_party_list_lifecycle.sql` 已补三类共享的账簿级名称唯一性和类别/隐藏状态列表索引。
- `migrations/0010_prepaid_expenses.sql` 已补待摊费用主体、分期计划、幂等交易引用和剩余金额查询投影。
- `migrations/0011_deposit_rate_versions.sql` 已补存款利率更新批次、逐行校验、不可变版本和当前生效利率投影。
- `migrations/0012_financial_goal_progress_baseline.sql` 已补财务目标起始日期、允许负值的初始估值快照、账户范围、公式版本和进度输入投影。
- `migrations/0013_plan_and_reminder_occurrences.sql` 已补计划执行实例、提醒触发实例、生命周期统计和今日提醒统一投影。
- `docs/local-storage-and-ledger-architecture.md` 已固定 SQLite、本地备份、类型化扩展和分阶段双重记账升级方向。
- `docs/sqlite-domain-coverage-audit.json` 已对账全部 `53` 类运行时实体候选；当前迁移为 `63` 表、`21` 视图、`56` 个显式索引和 `2` 个账簿外备份清单产物，无建议缺失对象。
- 项目内 Rust GNU 工具链位于 `.tools`，不会修改系统 `PATH`；SQLite 运行库使用官网 x64 预编译包并通过 SHA3-256 校验。
- `tools/run-rust-checks.ps1` 会配置项目内 Cargo、`rust-lld` 和 SQLite DLL；当前 Rust 基线为 `67 passed, 0 failed`。
