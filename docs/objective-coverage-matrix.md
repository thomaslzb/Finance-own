# 目标覆盖矩阵

本文档直接围绕当前总目标做覆盖审计：

目标：

`不要停，直到所有的功能点均记录下来，并理清相关的数据流转，落地开发的需求分析`

矩阵目的：

1. 检查“功能点记录”覆盖到什么程度
2. 检查“数据流转”覆盖到什么程度
3. 检查“开发需求分析”是否已具备落地条件

状态说明：

- `已覆盖`
  - 已有明确证据与文档落点
- `部分覆盖`
  - 已有较强证据，但仍有关键缺口
- `未覆盖`
  - 仍缺核心证据

## 1. 功能点记录

| 子目标 | 当前状态 | 主要证据 | 剩余缺口 |
| --- | --- | --- | --- |
| 顶层工作区已识别 | 已覆盖 | [top-level-navigation-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\top-level-navigation-observations.md), [runtime-dfm-functional-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-dfm-functional-evidence.md) | `记账` 多级菜单已截图；其余专用命令结果待校准 |
| 主功能域已归类 | 已覆盖 | [feature-catalog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\feature-catalog.md), [runtime-form-coverage-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-coverage-audit.md) | `460/460` 已分类且未分类为 `0`；仍缺真实计算结果与动态生成控件 |
| 命令、快捷键和初始状态已归档 | 已覆盖 | [runtime-command-and-state-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-command-and-state-evidence.md) | 已覆盖 `460` 个窗体、`1407` 个交互控件和 `36` 个快捷键；仍需真实点击结果校准 |
| DFM 事件与代码入口已归档 | 已覆盖 | [runtime-event-handler-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-event-handler-evidence.md) | `2000` 个去重处理器中 `1951` 个已定位代码；3 个无 VMT 资源已分别形成保留、运行类对应和技术排除决策 |
| 窗体家族与组合关系已系统归档 | 已覆盖 | [runtime-form-coverage-audit.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-coverage-audit.json), [runtime-form-composition-evidence.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-composition-evidence.json), [runtime-method-evidence.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-method-evidence.json) | 已分层为 `400 + 37 + 2 + 21`，`37/37` 个嵌入视图已定位父窗体，特殊表面方法合同已确认；仍缺动态结果和入口校准 |
| 全量动态执行范围已形成 | 已覆盖 | [runtime-execution-queue.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-execution-queue.md), [runtime-observation-record.schema.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-observation-record.schema.json) | 已形成 `20` 批、`460` 窗体、`1407` 控件、`2000` 事件的逐项队列；当前 `455` 条部分观察、`3` 条合同前置阻塞、`2` 条当前版本不可达，`pending` 为零 |
| 页面级实测已形成记录 | 部分覆盖 | [data-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-page-observations.md), [report-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\report-page-observations.md), [analysis-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\analysis-page-observations.md), [runtime-execution-queue.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-execution-queue.md) | 财务数据五页及 B01 至 B20 均已有结构化观察或明确范围决策；代表性成功写入、完整公式、在线更新与失败回滚仍待执行 |

## 2. 数据流转

| 子目标 | 当前状态 | 主要证据 | 剩余缺口 |
| --- | --- | --- | --- |
| 多数据源结构已厘清 | 已覆盖 | [data-source-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-source-map.md), [final-synthesis.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\final-synthesis.md) | 主账本正式读取仅影响旧数据迁移映射，不阻塞新系统功能设计 |
| 共享参考库职责已明确 | 已覆盖 | `mhlink.mdb` 已正式读取，见 [data-source-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-source-map.md), [code-type-mapping.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\code-type-mapping.md) | 关系/索引系统表权限受限 |
| 缓存语义已形成推断 | 已覆盖 | [cache-semantics.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\cache-semantics.md), [analysis-dashboard.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\analysis-dashboard.md) | 协议细节仍未完全逆向 |
| 关键业务场景流已梳理 | 已覆盖 | [scenario-data-flows.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\scenario-data-flows.md), [entity-flow-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\entity-flow-map.md) | 需待主账本正式表结构验证 |
| 主账本与参考库关系已收敛 | 部分覆盖 | [linked-table-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\linked-table-evidence.md) | 仍未正式证明是链接表还是本地镜像 |
| 新系统真相数据流已落地 | 已覆盖 | [sqlite-schema-and-query-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-schema-and-query-contract.md), [local-storage-and-ledger-architecture.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\local-storage-and-ledger-architecture.md), [0001_core.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0001_core.sql), [0002_planning_and_automation.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0002_planning_and_automation.sql), [0003_contracts_exchange_and_sync.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0003_contracts_exchange_and_sync.sql), [0004_insurance_cash_value.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0004_insurance_cash_value.sql), [0005_insurance_cash_value_as_of.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0005_insurance_cash_value_as_of.sql), [0006_insurance_cash_value_amount_guard.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0006_insurance_cash_value_amount_guard.sql), [0007_payroll_income_and_application_identity.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0007_payroll_income_and_application_identity.sql), [0008_party_profile.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0008_party_profile.sql), [0009_party_list_lifecycle.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0009_party_list_lifecycle.sql), [0010_prepaid_expenses.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0010_prepaid_expenses.sql), [0011_deposit_rate_versions.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0011_deposit_rate_versions.sql), [0012_financial_goal_progress_baseline.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0012_financial_goal_progress_baseline.sql), [0013_plan_and_reminder_occurrences.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0013_plan_and_reminder_occurrences.sql), [sqlite-domain-coverage-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-domain-coverage-audit.md), [backup-manifest.schema.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\backup-manifest.schema.json) | 十三版迁移、应用文件标识、工资组成核对、人员资料字段、人员列表生命周期、待摊费用主体与期次、存款利率批次与版本、财务目标进度基线、计划执行实例、提醒触发实例、今日提醒统一投影、可用账簿初始化、账户树、基础资料维护、原子交易写入和七组报表查询已形成 Rust 可运行闭环；平衡 posting 总账以及计划、预算和目标的应用服务与专属适配器仍待实现 |
| 数据交换与持久化边界已落地 | 已覆盖 | [data-exchange-and-persistence-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-exchange-and-persistence-contract.md), [runtime-data-exchange-evidence.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-data-exchange-evidence.json) | 旧 XML 格式和通用 CSV 预览已确认；成功回导、专用账单、附件目录行为和同步结果待验证 |
| 事件到应用命令的数据流已落地 | 已覆盖 | [runtime-event-command-dataflow.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-event-command-dataflow.md), [runtime-destructive-and-file-operation-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-destructive-and-file-operation-contract.md) | `2000` 个事件均有 Rust 边界候选；真实级联数量、失败回滚和文件结果仍需动态校准 |

## 3. 开发需求分析

| 子目标 | 当前状态 | 主要证据 | 剩余缺口 |
| --- | --- | --- | --- |
| 领域模型已成型 | 已覆盖 | [entity-catalog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\entity-catalog.md), [schema-hypothesis.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\schema-hypothesis.md), [domain-mapping-spec.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\domain-mapping-spec.md) | 主账本正式字段仍待校验 |
| Rust 模块拆分已形成 | 已覆盖 | [rust-module-plan.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\rust-module-plan.md) | 无阻塞，可直接用于 Phase 1/2 |
| 旧窗体到目标 UI 与模块边界已归并 | 已覆盖 | [target-ui-consolidation-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\target-ui-consolidation-map.md) | `460` 个旧窗体已映射到 `11` 个分区、`40` 个页面族；动态行为仍按执行队列逐项关闭 |
| 实施任务已形成 backlog | 已覆盖 | [implementation-backlog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\implementation-backlog.md) | 可继续细化到 issue 级别 |
| 迁移路线已形成 | 已覆盖 | [migration-strategy.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\migration-strategy.md) | 旧格式写回仍属后期议题 |
| 验收标准已形成 | 已覆盖 | [acceptance-criteria.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\acceptance-criteria.md) | 后续可按实现进展补测试清单 |
| 本地数据库已选型并形成可执行模式 | 已覆盖 | [local-database-selection.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\local-database-selection.md), [sqlite-schema-and-query-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-schema-and-query-contract.md), [sqlite-domain-coverage-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-domain-coverage-audit.md) | SQLite 主库已确定；`53` 类实体候选均有数据库契约，同步和分析副库保持可选 |
| 同类系统对标已转为产品决策 | 已覆盖 | [similar-systems-benchmark.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\similar-systems-benchmark.md) | 后续只需随重大产品决策复查，不需要持续扩充产品名单 |

## 4. 当前阶段总体判断

### 已经完成到什么程度

- “功能点均记录下来”：`高覆盖，静态范围已系统归档`
- “数据流转已理清”：`高覆盖，新系统主数据流已可执行验证`
- “开发需求分析已落地”：`已覆盖，可直接进入模块实现`
- “同类系统与数据库选型”：`已覆盖，并已转成明确取舍`

### 为什么还不能宣称完全完成

当前仍存在 7 个关键未闭环项：

1. `记账` 其余专用命令、字段联动和真实写入结果
2. 财务诊断、规划、目标和投资收益的精确计算口径
3. 报表精确 SQL、收益率公式、排序钻取、筛选边界、导出格式和打印结果
4. `test.mh8` 正式结构与样例数据到新 SQLite 模型的迁移映射
5. 旧 XML 成功回导、21 类节点映射、信用卡专用账单、备份压缩和附件目录；同步与行情页面已由 B18 动态确认，仍缺真实冲突/删除传播/断点续传、移动端结果和其余行情源协议
6. AI 动态入口、控制台命令语法与副作用、金额计算器动态回填，以及嵌入视图的空数据、有数据、筛选和交互结果；AI/控制台/计算器静态方法合同已确认
7. B20 共享组件的日期/金额边界、键盘焦点、统计快照一致性、任务取消和 WebView 隔离
8. B01 账簿真实新建、还原到新账簿、旧 `.mh8k` 的 Rust 解密迁移、结算日期/重复范围/跨域口径和失败回滚、密码 KDF/迁移失败恢复、设置持久化及许可协议
9. B02 账户与基础资料的成功/失败保存、引用保护、组合账户原子性、期初资金分录和费率历史
10. B03 交易与流水的单笔/批量提交、跨币种与手续费、分期、退款审计、附件和失败回滚
11. B04 债权债务、信用卡、分期与网贷的真实合同保存、本息费用分配、账单生成、还款核销、摊还公式和失败回滚
12. B05 定期存款与银行理财的续存/到期事件、产品生命周期、持仓本金、真实申购赎回、收益公式和失败回滚
13. B07 投资公共能力的真实持仓调整、成本批次、实现盈亏、跨币种估值、有数据输出和失败回滚
14. B08 上市证券的账户级费率、新股关系、证券选择、真实费用舍入、成本批次、代码迁移和失败回滚
15. B09 开放式基金与货币基金的真实金额/份额、费率、收益结转、成本、认购、拆分和失败回滚
16. B10 债券的真实净价/全价、应计利息、费用、成本批次、兑付损益、税务和失败回滚

新增的 B14 动态证据已经关闭重大资产和家居物品的主要页面级缺口；B15 关闭预算、提醒、诊断、规划和目标的独立页面与字段缺口；B16 完成 `25` 张业务报表逐页查询；B17 确认真实 XML、通用 CSV 预览、交割单和标签设置，并暴露回导崩溃与预览写文件缺陷；B18 确认同步设置、注册、手机快查、行情来源和中止路径；B19 完成辅助工具与长尾范围决策；B20 完成 19 个共享 UI/技术支撑资源的合并、保留和排除决策；B01 已补齐 15 个系统外壳资源的入口、初始/取消路径、正常关闭和脱敏边界，并完成真实备份、当前账簿覆盖还原、结算恢复点、余额调整算法和冷启动；B02 补齐 41 个账户与基础资料资源的类型目录、代表性向导、主数据页面和取消边界；B03 补齐 38 个交易与流水资源的列表、编辑、模板、查找筛选和图表结构；B04 补齐 54 个债权债务、信用卡、分期和网贷资源的工作区、筛选、账户、向导及编辑器结构；B05 补齐 19 个定期存款与银行理财资源的账户、向导、工作区、产品目录和编辑器结构；B07 补齐 6 个投资公共资源的调整、现金事件、持仓列表、构成图、历史盈亏和市值变动结构；B08 补齐 21 个上市证券资源的账户、资料、行情、费率、代码变更、持仓、交易、市值和公司行为结构；B09 补齐 29 个开放式基金与货币基金资源的账户、向导、资料、净值、持仓、交易、市值、历史盈亏和专项交易结构；B10 补齐 15 个债券资源的资料、账户、向导、持仓、交易、构成图、历史盈亏和五类专用交易结构。剩余风险已收敛到代表性成功写入、精确计算公式、成功回导、导出打印、真实远端协议、账簿生命周期剩余分支与失败回滚、账户与基础资料引用保护、交易、合同、产品生命周期与持仓成本原子性及审计、共享组件边界和旧库迁移映射。

这些缺口不影响现在开始 Rust Phase 1/2 编码，但会影响：

- 旧账本深兼容度
- 页面细节复刻度
- 最终“功能一致”口径的严谨程度

## 5. 后续最优先行动

1. 按 [runtime-execution-queue.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-execution-queue.md) 逐窗体执行，并用 [runtime-validation-scenarios.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-validation-scenarios.md) 的代表性数据校准跨页面结果
2. 将每次运行结果按统一 Schema 回填功能目录、数据流、PRD 和验收标准
3. 在已完成计划/提醒实例模式的基础上，实现计划定义、实例生成、执行/跳过、提醒确认，以及预算和目标 CRUD 的应用服务与 SQLite 适配器
4. 将 `test.mh8` 正式结构研究保留为迁移适配并行项，不再作为主线阻塞
