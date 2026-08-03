# MoneyHome8 重构实施 Backlog

本文档将当前阶段的功能分析、数据源排查和领域模型结论转化为可执行的实施任务清单，供后续逐步实现。

当前已拍板的主系统技术路线：

- 三端 UI：`Flutter Desktop` / `Flutter Mobile` / `Flutter Web`
- PC 本地核心：`Rust` 内置模块，通过稳定本地 API/FFI 供 Flutter PC 调用
- PC 本地账本：`SQLite`
- 云端服务：`.NET API`
- 云端数据库：`PostgreSQL`
- 旧格式与迁移：Rust PC 本地只读迁移，旧 MoneyHome8 原始文件不上传云端
- 同步：对象级多主同步，云端保存完整新系统财务对象副本并协调冲突

## Epic 1：旧数据源接入

### Task 1.1 主账本读取器骨架

- 目标：
  - 建立旧 `.mh8` 读取入口
  - 抽象主账本 repository 接口
- 输入证据：
  - `artifacts/test-copy.mh8` 为裸 `Standard Jet DB`，但 ACE 只读打开仍受权限/认证约束
  - `C:\DCG-SZ\IT Manage\Private\Personal-Docs\test001.mh8` 当前不是裸 Jet 文件头，ACE 只读打开返回 `invalid_format`
  - 解压后的 `MoneyHome8.data` 为受控 Jet 库，ACE 只读打开返回 `auth_failed`
- 产出：
  - `domain::legacy_source`
  - `infrastructure::mh8`
  - `tools/probe_legacy_sources.ps1`
- 验收：
  - 能返回“尝试连接主账本”的结构化结果
  - 能区分“文件不存在 / 文件占用 / 无权限 / 账号口令无效 / 不可识别格式 / 对象不可见”

### Task 1.2 共享参考库读取器

- 目标：
  - 接入 `mhlink.mdb`
- 已知表：
  - `HBRate`
  - `TBSecuPrice`
  - `TBTransFee`
- 产出：
  - `reference_store`
  - 利率/行情/费率查询接口
- 验收：
  - 能读取 `HBRate` 全量
  - 能按 `SecuCode` 查询行情
  - 能按 `Type` 查询费率规则

### Task 1.3 内置库解压与读取骨架

- 目标：
  - 解析 `MoneyHome8.data`
  - 在偏移 `125` 处完成 `zlib` 解压
- 产出：
  - `tools/extract_moneyhome_data.ps1`
  - `domain::legacy_source`
  - `infrastructure::mh8`
- 验收：
  - 能稳定产出解压文件
  - 能识别其为受控 Jet 库

### Task 1.4 缓存读取器

- 目标：
  - 读取 `MoneyHome8.cache`
  - 读取 `Investment.cache`
- 产出：
  - `cache_store`
  - `infrastructure::cache_file`
  - `tools/probe_moneyhome_cache.ps1`
- 验收：
  - 能按代码查名称
  - 能按名称查拼音缩写
  - 能按投资品分类码 `_3/_4/_9` 查询对象

## Epic 2：核心领域模型

### Task 2.1 基础资料模型

- 实体：
  - `Category`
  - `Tag`
  - `Currency`
  - `Person`
  - `ObjectType`
- 验收：
  - 模型字段能覆盖当前已识别字段
  - 模型命名与 `TB*` 对象一致或有映射说明

### Task 2.2 账户模型

- 实体：
  - `AccountGroup`
  - `Account`
  - `AccountType`
- 验收：
  - 能表达树结构
  - 能表达多账户类型
  - 能表达显示名、币种、账号/卡号、余额等核心信息

### Task 2.3 通用交易模型

- 实体：
  - `Transaction`
  - `TransactionType`
  - `TransactionTheme`
  - `Template`
- 验收：
  - 能表达日期、金额、主题、对象、费用、提醒关联

### Task 2.4 投资扩展模型

- 实体：
  - `Security`
  - `Fund`
  - `DebtAccount`
  - `Insurance`
  - `PreciousMetals`
  - `Futures`
  - `Financing`
  - `Asset`
- 验收：
  - 能覆盖 `ObjType` / 缓存类别码推断下的主要投资对象

### Task 2.5 预算与提醒模型

- 实体：
  - `Budget`
  - `Reminder`
  - `Plan`
  - `FinancialPlanning`
  - `Goal`
- 验收：
  - 能覆盖预算、提醒、财务规划专题输入、目标储蓄
  - `0002_planning_and_automation.sql` 可执行，预算、目标和到期计划输入视图可重建
  - `domain::planning` 已定义预算、预算项、财务目标、计划模板、提醒及其状态、周期和执行口径记录
  - `app::planning::PlanningRepository` 已覆盖预算、财务目标、计划模板和提醒的创建、更新、列表和关系替换
  - `SqliteLedgerStore` 已实现预算、财务目标、计划模板和提醒 CRUD，Rust 测试覆盖预算项替换、目标账户范围替换、计划更新和提醒更新
  - 待实现下一版实例能力迁移：冻结 `show_in_today_inbox`、`can_execute`、`can_skip` 和执行策略版本或等价枚举，修正十三版把全部计划固定投影为可执行/可跳过；至少测试普通计划 `1/1`、保险仅提醒 `0/1`、固定账户自动计划不进入今日提醒、两缴费年度修改只重算未来实例，以及自动入账后账户/保险/计划投影同版本刷新

### Task 2.6 SQLite 核心真相表

- 目标：
  - 用新模式表达账户、交易、原子分录、标签、汇率、附件、投资成交、模板计划、预算、提醒、目标和规划输入
  - 不复刻旧 Jet 表结构
- 已落地产物：
  - `migrations/0001_core.sql`
  - `migrations/0002_planning_and_automation.sql`
  - `migrations/0003_contracts_exchange_and_sync.sql`
  - `tools/validate_sqlite_schema.py`
  - `tools/summarize_sqlite_domain_coverage.py`
  - `docs/sqlite-domain-coverage-audit.json`
  - `src/domain/transactions.rs`
  - `src/app/transactions.rs`
  - `src/infrastructure/sqlite.rs`
  - `tools/run-rust-checks.ps1`
- 验收：
  - 内存 SQLite 可执行完整迁移
  - 外键检查通过
  - 同日流水余额、流入/流出/差额和标签两类投影通过样例验证
  - 转账、转入和手续费三分录余额通过样例验证
  - 写入中途约束失败时交易头和已写分录一起回滚
  - 日期范围查询命中复合索引
  - `53` 类运行时实体候选全部有唯一契约，所有“已实现”对象均真实存在于迁移
  - Rust 文件账簿创建/重开、原子交易写入、余额/标签查询和约束失败整体回滚测试通过

## Epic 3：核心读取能力

### Task 3.1 共享参考库 -> Rust 实体映射

- 验收：
  - `HBRate` -> `RateRule`
  - `TBSecuPrice` -> `Quote`
  - `TBTransFee` -> `FeeRule`

### Task 3.2 缓存 -> 检索索引映射

- 验收：
  - `MoneyHome8.cache` -> `LookupIndex`
  - `Investment.cache` -> `InvestmentCatalog`
  - `_PY` / `_LIST` / `_3/_4/_9` 映射被固化到代码注释或枚举

### Task 3.3 主账本对象优先读取清单

- 优先表：
  - `TBAcctGroup`
  - `TBAcctDetail`
  - `TBCategory`
  - `TBCurrency`
  - `TBPerson`
  - `TBTransaction`
  - `TBBudget`
  - `TBRemindSetting`
  - `TBSyncRecord`
- 验收：
  - 每张表都有“读取成功 / 权限阻塞 / 字段待映射”的明确状态

## Epic 4：Flutter PC 壳层与本地 API

目标结构不是复刻 `460` 个 Delphi 窗体，而是实现 [target-ui-consolidation-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\target-ui-consolidation-map.md) 中的 `11` 个分区、`40` 个页面族。每个页面族完成时必须列出覆盖的全部旧 `execution_id`。

### Task 4.1 Flutter PC 主壳层

- 页面：
  - 左导航
  - 顶部入口
  - 状态栏
- 已落地产物：
  - `src/app/workspace_shell.rs` 提供四大工作区、账簿会话和加载状态
  - `src/app/ui.rs` 提供首屏 Flutter 可消费的 `WorkspaceHomeViewModel`
  - `docs/workplans/flutter-pc-local-api-plan.md` 已定义 PC 本地 API 第一版需求
- 验收：
  - 可容纳账户中心、财务记录、投资一览、标签页
  - Flutter 页面只调用 PC 本地 API，不直接访问 SQLite 或旧账本文件

### Task 4.2 账户中心页

- 功能：
  - 账户树
  - 按类型筛选
  - 账户余额汇总
- 已落地产物：
  - `src/app/ui.rs` 已聚合账户组树、未分组账户、资产/负债币种汇总和账户余额
- 验收：
  - 结构与现有截图口径匹配

### Task 4.3 流水与记账页

- 功能：
  - 收入录入
  - 支出录入
  - 转账录入
  - 流水浏览
- 验收：
  - 可用通用交易模型驱动

### Task 4.4 投资页

- 功能：
  - 投资品选择
  - 价格展示
  - 基础交易录入
- 验收：
  - 支持按代码、中文名、拼音缩写检索
  - 证券、基金、债券、外汇、期货、贵金属、保险和重大资产复用账户、目录、录入、流水、概览、选择器和配置 7 个页面族
  - 资产类型差异通过专属扩展对象与策略表达，不复制页面或使用全字段可空模型

### Task 4.5 全量旧页面追溯

- 目标：
  - 维护 `460 -> 40` 的旧窗体到目标页面族映射
  - 把动态观察记录回填到目标页面族验收
- 验收：
  - `460` 个 `execution_id` 唯一且全部有目标页面族
  - `1407` 个可交互控件、`2000` 个事件和 `502` 个高风险候选计数守恒
  - 合并、共享组件替代、宿主合并和内部范围决策分别有明确状态

## Epic 5：报表、分析与提醒

### Task 5.1 报表引擎骨架

- 报表：
  - 收支
  - 资产
  - 投资
  - 标签
  - 账户
- 验收：
  - 查询与 UI 解耦
  - 表格、图表、导出和打印复用同一结果 DTO
  - `ReportReadRepository` 覆盖流水、余额、标签流水、标签资产和投资输入投影
  - 未校准的投资成本与收益率不在 SQL 层隐式计算

### Task 5.2 投资分析

- 指标：
  - 市值
  - 成本
  - 浮盈浮亏
  - 收益率
- 验收：
  - 依赖 `Quote` 与投资对象计算
  - 使用 `investment_lot_allocations` 保存可审计成本分配
  - 通过买入、部分卖出、分红、费用和转入转出样例后再固化最终公式

### Task 5.3 提醒与预算

- 功能：
  - 提醒列表
  - 限额提醒
  - 预算跟踪
- 验收：
  - 本地模型闭环
  - 将四类限额条件实现为 Rust 类型化枚举，校验账户/价格 `lower < upper`，金额和行情价格使用定点数并保留证券四位精度
  - 实现规则默认启用、原子启停、条件版本递增、目标快照版本和边界级幂等评估；停用规则不参与评估
  - 今日提醒对限额告警固定禁用执行和跳过；规则删除只移除当前告警，不删除历史触发审计
  - 目标账户或投资品删除/关闭前预览引用规则，明确 restrict、停用或确认级联策略并记录审计
  - 补齐等于边界、信用卡真实透支、基金越界、无行情、冷启动去重、并发及失败回滚测试

## Epic 6：同步、导入导出与迁移

### Task 6.1 .NET 同步协议骨架

- 对象：
  - 币种
  - 人员
  - 标签
  - 分类
  - 账户
  - 交易
  - 默认币种
  - 余额
- 验收：
  - 先完成 .NET API 合同、PostgreSQL 对象副本和 PC 本地映射，不要求首轮全量联机闭环
  - `docs/workplans/dotnet-sync-api-plan.md` 已定义 .NET 同步 API、PostgreSQL 对象副本和错误模型需求
  - `docs/workplans/conflict-resolution-plan.md` 已定义 PC/Web 冲突解决需求
  - `sync_profiles`, `sync_batches`, `sync_object_results`, `sync_conflicts`, `sync_tombstones` 已由第三版迁移落地
  - 本地账簿断网可写，凭据和令牌不进入核心领域表
  - 同步按对象和批次传输，不上传整个 SQLite 文件
  - PC/Web 支持完整冲突解决，手机端只提示冲突并延后处理

### Task 6.2 导入导出

- 功能：
  - 数据导入
  - 分类导入
  - 交割单导入
  - 数据导出
- 验收：
  - 文件格式和 UI 路径形成明确合同
  - `import_field_mappings`, `import_batches`, `import_rows` 支持来源哈希、预览、字段错误、重复判断和提交追溯

### Task 6.3 旧格式迁移

- 验收：
  - 明确旧 MoneyHome8 原始文件只在 PC 端本地迁移
  - 明确 PC 迁移审计、迁移报告和脱敏摘要只保存在 PC 本地，不上传云端
  - 明确迁移结果写入 PC SQLite，经用户确认后再同步新系统对象到云端
  - 对认证未打通情形给出降级方案

### Task 6.4 Flutter Mobile 轻量同步

- 功能：
  - 随手记账
  - 离线草稿
  - 待同步队列
  - 最近查询缓存
- 验收：
  - 手机端可上传本端记录并同步下载其它端数据
  - 手机端不保存完整本地账本，不承担旧账本迁移或复杂冲突处理
  - `docs/workplans/mobile-offline-queue-plan.md` 已定义离线队列、幂等键、重试和附件临时缓存需求

### Task 6.5 Flutter Web 在线端

- 功能：
  - 在线记账
  - 在线查询
  - 账本选择
  - 冲突解决
- 验收：
  - Web 端必须登录后使用
  - Web 端通过 .NET API 写入云端对象副本
  - Web 端不承担离线主账本写入
  - `docs/workplans/flutter-web-online-plan.md` 已定义在线记账、查询、删除确认和冲突解决需求

### Task 6.6 附件与隐私

- 功能：
  - PC 本地附件
  - 手机临时附件
  - Web 上传附件
  - 云端附件权限
  - 旧迁移附件隐私边界
- 验收：
  - `docs/workplans/attachment-privacy-plan.md` 已定义三端附件、票据/支票簿类凭证、云端附件、旧迁移附件和隐私边界
  - 旧 MoneyHome8 原始文件、迁移审计、迁移报告、脱敏摘要和完整本地路径不上传云端
  - 附件下载必须经过账本权限校验或短期授权

## 当前最高优先级

1. 按 `docs/workplans/flutter-pc-local-api-plan.md` 把当前 Rust `app`/`infrastructure` 能力收敛为 PC 本地 API 契约
2. 按 `docs/workplans/dotnet-sync-api-plan.md` 进入 .NET API / PostgreSQL 云端对象副本的接口细化
3. 按 `docs/workplans/mobile-offline-queue-plan.md`、`flutter-web-online-plan.md` 和 `conflict-resolution-plan.md` 细化三端同步页面任务
4. 使用 `docs/workplans/three-client-implementation-slices.md` 作为三端实施顺序和端到端验收链路索引
5. 使用 `docs/workplans/three-client-acceptance-scenarios.md` 作为三端需求验收和隐私边界检查索引
6. 使用 `docs/workplans/security-audit-error-handling-plan.md` 作为三端安全、审计、日志脱敏和错误恢复检查索引
7. 使用 `docs/workplans/backup-import-export-plan.md` 作为 PC 备份恢复、旧 XML/CSV、专用账单、回导预览、导入导出和 Web 恢复入口需求索引
8. 使用 `docs/workplans/reporting-planning-plan.md` 作为基础报表、预算、提醒、计划和目标需求索引
9. 使用 `docs/workplans/three-client-ui-navigation-plan.md` 作为三端 UI 信息架构、导航、概况布局、图表摘要、页面状态和旧页面族追溯需求索引
10. 使用 `docs/workplans/account-device-ledger-membership-plan.md` 作为账号、设备、账本成员、角色变化和权限错误需求索引
11. 使用 `docs/workplans/amount-currency-exchange-rate-plan.md` 作为金额、币种、汇率、本币折算和余额展示需求索引
12. 使用 `docs/workplans/list-query-filter-pagination-plan.md` 作为列表查询、筛选、排序、查找、分页、缓存和导出打印状态需求索引
13. 使用 `docs/workplans/settings-preferences-notification-plan.md` 作为设置、偏好、通知状态、手机快查、外围入口、快捷入口和设备状态需求索引
14. 使用 `docs/workplans/command-form-lifecycle-plan.md` 作为命令、表单草稿、批量操作、模板、复制粘贴、导入预览、幂等和审计需求索引
15. 使用 `docs/workplans/master-data-lifecycle-plan.md` 作为账户组、账户、分类、标签、往来方、币种和汇率快照生命周期需求索引
16. 使用 `docs/workplans/ledger-lifecycle-storage-plan.md` 作为账本创建、打开、关闭、删除、云端绑定和本地存储边界需求索引
17. 使用 `docs/workplans/investment-advanced-assets-calibration-plan.md` 作为投资、高级资产、公式校准状态和旧迁移隐私边界需求索引
18. 使用 `docs/workplans/data-retention-deletion-recovery-plan.md` 作为删除、归档、保留、恢复、物理清理和墓碑同步需求索引
19. 使用 `docs/workplans/date-time-period-semantics-plan.md` 作为业务日期、发生时间、审计时间、账本时区、账期、预算周期和提醒周期需求索引
20. 使用 `docs/workplans/domain-validation-invariants-plan.md` 作为三端输入、Rust 本地核心、.NET API、手机队列、导入迁移和存储约束的领域校验需求索引
21. 使用 `docs/workplans/localization-accessibility-display-plan.md` 作为金额日期显示、本地化消息、稳定命令键、字段错误、基础可访问性和旧中文字段解析边界需求索引
22. 使用 `docs/workplans/auth-session-secret-storage-plan.md` 作为账号登录、会话、访问令牌、刷新令牌、退出登录、设备撤销和秘密存储需求索引
23. 使用 `docs/workplans/operations-observability-support-plan.md` 作为云端运行监控、诊断 ID、告警、客户服务入口、支持入口、数据修复和运维隐私边界需求索引
24. 使用 `docs/workplans/testing-acceptance-release-gates-plan.md` 作为三端测试、验收证据、隐私安全门禁、财务数据门禁、运维门禁和发布说明边界需求索引
25. 使用 `docs/workplans/schedule-reminder-occurrence-plan.md` 作为计划模板、提醒、发生实例、今日待办、财务日历待处理投影、执行/跳过能力标志和自动入账后置需求索引
26. 使用 `docs/workplans/financial-goals-planning-input-plan.md` 作为财务目标、规划输入、进度公式版本、引用影响预览和旧迁移证据 PC 本地保存需求索引
27. 使用 `docs/workplans/limit-alert-budget-rule-evaluation-plan.md` 作为限额提醒、预算提示、条件版本、幂等评估、今日提醒投影和引用影响预览需求索引
28. 使用 `docs/workplans/deposits-debts-credit-amortization-plan.md` 作为存款、银行理财、债权债务、信用卡账单、账单日规则、分期摊还、分录平衡和敏感信息保护需求索引
29. 使用 `docs/workplans/insurance-social-security-tangible-assets-plan.md` 作为保险、社保、现金价值、重大资产、家居物品、估值、分期和敏感信息保护需求索引
30. 使用 `docs/workplans/market-instruments-trading-valuation-plan.md` 作为证券、基金、债券、融资融券、证券代码转换、新股关联、行情更新批次、费率快照、行情净值、估值批次、成本批次和合同偿还需求索引
31. 使用 `docs/workplans/shared-ui-ai-diagnostics-automation-plan.md` 作为共享 UI、金额计算器、Web 内容宿主、AI 适配器默认关闭、内部诊断控制台隔离和旧程序自动化证据本地化需求索引
32. 使用 `docs/workplans/payroll-income-tax-social-contribution-plan.md` 作为工资收入、税务计算快照、社保缴费组成、原子提交和旧迁移证据 PC 本地保存需求索引
33. 使用 `docs/workplans/source-document-traceability-plan.md` 作为根目录 PRD、架构、同步草案、验收标准、覆盖矩阵和证据文档到 workplans 的承接索引
34. 使用 `docs/workplans/diary-calendar-richtext-plan.md` 作为日记、富文本正文、搜索、导出、财务日历投影、人员生日投影和旧迁移证据 PC 本地保存需求索引
35. 使用 `docs/workplans/financial-calculators-price-maintenance-plan.md` 作为财务计算器、净价/清洁价格计算、公式版本、结果回填、价格整理预览和旧证据 PC 本地保存需求索引
36. 使用 `docs/workplans/wallet-recharge-withdrawal-plan.md` 作为第三方钱包充值、提现、本金手续费组成、保存并继续和旧验证证据 PC 本地保存需求索引
37. 使用 `docs/workplans/prepaid-expenses-amortization-plan.md` 作为待摊费用主体、初始资金事实、确定金额期次、幂等摊销、计划重算和旧验证证据 PC 本地保存需求索引
38. 继续运行原程序页面并用最小样例校准余额、本币折算和投资公式
39. 将 `test001.mh8` 外层封装、裸 Jet 副本认证与结构枚举保留为 PC 本地只读迁移工作，不阻塞 Flutter 三端与云同步主线
40. 使用 `docs/workplans/ledger-lifecycle-storage-plan.md` 的账簿结算补充规则作为 PC 本地恢复点、结算预览、失败回滚和旧结算证据 PC 本地保存需求索引
41. 使用 `docs/workplans/auth-session-secret-storage-plan.md` 的 PC 本地密码/KDF 补充规则作为失败冷却、换密钥中断恢复和密钥材料不入云需求索引
42. 使用 `docs/workplans/reporting-planning-plan.md` 与 `docs/workplans/list-query-filter-pagination-plan.md` 作为报表/列表导出打印快照、查询追溯和旧报表证据 PC 本地保存需求索引
43. 使用 `docs/workplans/settings-preferences-notification-plan.md` 作为旧设置、窗口状态、快捷键、最近账簿和授权协议证据 PC 本地保存需求索引
44. 使用 `docs/workplans/master-data-lifecycle-plan.md` 作为标签设为首页、拖放排序、批量关系、选择器候选版本失效和旧标签校准证据 PC 本地保存需求索引
45. 使用 `docs/workplans/master-data-lifecycle-plan.md` 作为组合账户、一本通、多成员账户、账户组迁移、期初资金分录和资料入口草稿策略需求索引
46. 使用 `docs/workplans/amount-currency-exchange-rate-plan.md` 作为本位币切换、自定义币种、在线牌价更新批次、汇率重复键和旧牌价诊断证据 PC 本地保存需求索引
47. 使用 `docs/workplans/command-form-lifecycle-plan.md` 作为保存并继续、批量模板逐行策略、复制粘贴、改变类型、转计划、退款、冲销、分期和陈旧草稿保护需求索引
48. 使用 `docs/workplans/deposits-debts-credit-amortization-plan.md` 作为银行理财产品生命周期、持仓本金/实际现金流/收益同快照一致、还款分配、网贷流转和旧证据 PC 本地保存需求索引
49. 使用 `docs/workplans/market-instruments-trading-valuation-plan.md` 作为基金确认/收费/资金在途/拆分、债券兑付/利息/税务、融资融券候选筛选/超额偿还/担保物划转需求索引
50. 使用 `docs/workplans/insurance-social-security-tangible-assets-plan.md` 作为保险返还、分红、退保保留/终止、现金价值输入边界、重大资产多贷款、部分出售、估值删除和家居物品成本公式状态需求索引
51. 使用 `docs/workplans/financial-goals-planning-input-plan.md` 作为规划推演起始余额组成、通胀/退休/资产增长/分期展开公式版本、清空确认、多币种错误状态和旧规划证据 PC 本地保存需求索引
52. 使用 `docs/workplans/reporting-planning-plan.md` 作为预算期间、退款冲销、多币种预算、滚动导入、财务诊断指标边界和目标进度多账户估值需求索引
53. 使用 `docs/workplans/reporting-planning-plan.md` 与 `docs/workplans/list-query-filter-pagination-plan.md` 作为报表排序、分组小计、趋势图、概况可用资金图表、钻取版本和旧 SQL/旧查询证据 PC 本地保存需求索引
54. 使用 `docs/workplans/attachment-privacy-plan.md` 作为多附件引用、最后引用待清理、物理清理幂等、哈希校验、扫描/配额/大文件错误和票据凭证生命周期需求索引
55. 使用 `docs/workplans/dotnet-sync-api-plan.md`、`docs/workplans/mobile-offline-queue-plan.md` 和 `docs/workplans/settings-preferences-notification-plan.md` 作为同步断点续传、取消、墓碑传播、下载续拉、手机快查失败和远程通知幂等需求索引
