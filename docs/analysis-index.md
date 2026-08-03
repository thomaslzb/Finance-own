# MoneyHome8 分析索引

本文档是当前 `Finance-own/docs` 目录中分析产物的总索引，用于快速定位不同主题的结论、证据与待办。

## 1. 总览类

- [rebuild-prd.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\rebuild-prd.md)
  - 总体产品与技术 PRD
- [coverage-status.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\coverage-status.md)
  - 各功能域覆盖度与缺口状态
- [functional-audit-checklist.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\functional-audit-checklist.md)
  - 按功能域整理的审计清单
- [traceability-matrix.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\traceability-matrix.md)
  - 功能域/数据源/证据/缺口追溯矩阵
- [verified-vs-pending-index.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\verified-vs-pending-index.md)
  - 已确认 vs 待实测索引
- [feature-catalog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\feature-catalog.md)
  - 全量功能目录

## 2. UI 与页面观察

- [top-level-navigation-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\top-level-navigation-observations.md)
  - 顶层导航入口状态
- [data-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-page-observations.md)
  - 财务数据工作区
- [report-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\report-page-observations.md)
  - 财务报表工作区
- [analysis-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\analysis-page-observations.md)
  - 财务分析工作区
- [workspace-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\workspace-map.md)
  - 四大工作区结构图
- [bookkeeping-workspace-hypothesis.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\bookkeeping-workspace-hypothesis.md)
  - 记账工作区结构假设

## 3. 功能与资源窗体

- [function-matrix.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\function-matrix.md)
  - 按业务域整理的功能矩阵
- [feature-inventory.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\feature-inventory.md)
  - 初始功能清单与持续补充
- [resource-form-index.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\resource-form-index.md)
  - 资源窗体索引
- [resource-domain-summary.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\resource-domain-summary.md)
  - 资源窗体按域摘要
- [resource-form-family-index.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\resource-form-family-index.md)
  - 窗体家族归档
- [resource-forms.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\resource-forms.json)
  - 465 个 RCDATA 窗体结构化清单

## 4. 数据源、缓存与认证

- [data-source-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-source-map.md)
  - 主账本/参考库/内置库/缓存/认证上下文总图
- [mh8-storage-investigation.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\mh8-storage-investigation.md)
  - 主账本格式与认证排查
- [access-com-behavior.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\access-com-behavior.md)
  - Access COM 打开数据库后的行为对照
- [linked-table-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\linked-table-evidence.md)
  - 主账本与 `mhlink.mdb` 的外部依赖证据
- [provider-behavior-comparison.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\provider-behavior-comparison.md)
  - ODBC / ACE / ADOX / Access COM 的对照行为
- [field-semantic-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\field-semantic-evidence.md)
  - 主账本字段业务语义证据
- [object-type-enum-hints.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\object-type-enum-hints.md)
  - 主账本中文类型枚举线索
- [cache-and-package-investigation.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\cache-and-package-investigation.md)
  - `.data` / `.cache` 文件排查
- [cache-semantics.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\cache-semantics.md)
  - 缓存语义推断
- [code-type-mapping.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\code-type-mapping.md)
  - `ObjType / CurrType / _3/_4/_9` 类型码推断
- [migration-strategy.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\migration-strategy.md)
  - 旧数据迁移与双轨路线建议
- [auth-research-plan.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\auth-research-plan.md)
  - 主账本认证研究计划

## 5. 对象、实体与模式

- [moneyhome8-data-object-summary.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\moneyhome8-data-object-summary.md)
  - 解压后的内置库对象摘要
- [test-mh8-object-summary.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\test-mh8-object-summary.md)
  - 主账本对象摘要
- [mh8-structure-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\mh8-structure-evidence.md)
  - 主账本索引/主键/字段结构证据
- [table-evidence-matrix-summary.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\table-evidence-matrix-summary.md)
  - 主账本候选表证据矩阵摘要
- [table-cluster-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\table-cluster-evidence.md)
  - 主账本表簇分布证据
- [mh8-semantic-summary.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\mh8-semantic-summary.md)
  - 主账本中文语义线索摘要
- [shared-model-summary.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\shared-model-summary.md)
  - 主账本与内置库共享模型结论
- [entity-catalog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\entity-catalog.md)
  - 领域实体目录
- [entity-flow-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\entity-flow-map.md)
  - 实体关系草图
- [schema-hypothesis.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\schema-hypothesis.md)
  - 候选表/字段到实体的模式假设
- [domain-mapping-spec.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\domain-mapping-spec.md)
  - 领域映射规格
- [inner-table-field-map-summary.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\inner-table-field-map-summary.md)
  - 内置库表字段候选摘要
- [table-domain-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\table-domain-map.md)
  - 103 张共享表的业务域地图
- [table-domain-stats.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\table-domain-stats.md)
  - 共享表数量统计摘要

## 6. 过程与落地

- [scenario-data-flows.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\scenario-data-flows.md)
  - 典型用户场景数据流
- [ui-entity-source-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\ui-entity-source-map.md)
  - UI/窗体/实体/数据源映射
- [rust-module-plan.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\rust-module-plan.md)
  - Rust 模块拆分计划
- [implementation-backlog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\implementation-backlog.md)
  - 实施 backlog
- [roadmap.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\roadmap.md)
  - 初始三阶段路线
- [acceptance-criteria.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\acceptance-criteria.md)
  - 分阶段验收标准
- [decision-log.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\decision-log.md)
  - 关键判断与阶段性推断日志
- [open-gaps-register.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\open-gaps-register.md)
  - 未解缺口登记
- [local-database-selection.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\local-database-selection.md)
  - 新本地账本数据库选型结论
- [sqlite-schema-and-query-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-schema-and-query-contract.md)
  - SQLite 核心真相表、计划预算扩展、索引、视图、事务边界和查询 Repository 契约
- [sqlite-domain-coverage-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-domain-coverage-audit.md)
  - `53` 类运行时实体候选与当前 `53` 表、`15` 视图、`40` 索引及账簿外备份边界的逐项覆盖审计
- [similar-systems-benchmark.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\similar-systems-benchmark.md)
  - 类似系统对标与功能基线
- [functional-ledger.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\functional-ledger.md)
  - 面向开发与验收的功能点总台账
- [cross-domain-dataflow-catalog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\cross-domain-dataflow-catalog.md)
  - 面向模块拆分与仓储设计的数据流总表
- [resource-string-hints.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\resource-string-hints.md)
  - 资源二进制字符串提取的补充证据与可靠性边界
- [runtime-window-tree-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-window-tree-evidence.md)
  - 运行中主窗口的控件树直接证据
- [runtime-component-inventory.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-component-inventory.md)
  - 运行中已加载组件与隐藏页的清单
- [runtime-automation-boundaries.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-automation-boundaries.md)
  - 当前运行态自动化能做什么、不能做什么
- [auth-state-machine.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\auth-state-machine.md)
  - 主账本认证链的分阶段状态机总结
- [runtime-dfm-functional-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-dfm-functional-evidence.md)
  - `460` 个真实运行时 DFM 的功能、字段、命令和数据流结论
- [runtime-dfm-control-catalog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-dfm-control-catalog.md)
  - 全部运行时窗体的标题、可见文案、绑定字段和事件目录
- [runtime-form-coverage-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-coverage-audit.md)
  - `460/460` 个运行时窗体到业务域、交互角色、目标数据流和四层表面类型的无遗漏映射
- [runtime-form-composition-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-composition-evidence.md)
  - `107` 条逻辑直接组合关系，以及 `37/37` 个无文案嵌入视图的父窗体、最终宿主和实例路径
- [runtime-internal-surface-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-internal-surface-evidence.md)
  - AI、控制台和金额计算器宿主的控件、事件、快捷键线索、使用规模与产品范围边界
- [runtime-method-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-method-evidence.md)
  - 4 个特殊类、31 个 published 方法、19 个命名例程、VCL 跳转符号、25 个控制台命令类和 AI 外部接口常量
- [runtime-event-handler-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-event-handler-evidence.md)
  - 全部 `2332` 条事件绑定、`2000` 个按窗体去重处理器、VMT/父类代码入口、字符串引用、空实现和资源型无 VMT 边界
- [runtime-event-command-dataflow.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-event-command-dataflow.md)
  - `2000` 个旧事件到应用命令、数据方向、Rust 边界和实体候选的逐项映射，以及 `159` 条精确命名调用边
- [runtime-destructive-and-file-operation-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-destructive-and-file-operation-contract.md)
  - 账户/基础资料删除、批量删除、模板覆盖、`.mh8k` 备份、还原和导出文件的代码级开发合同
- [runtime-ai-console-calculator-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-ai-console-calculator-contract.md)
  - AI 外部数据边界、控制台命令/历史/快捷键和金额计算器关闭行为的 Rust 开发合同
- [runtime-shared-ui-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-shared-ui-contract.md)
  - 19 个共享 UI/技术支撑资源到金额筛选、日期、对话框、进度、统计、详情和 Web 内容宿主的收敛合同
- [runtime-ledger-lifecycle-and-settings-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-ledger-lifecycle-and-settings-contract.md)
  - B01 应用外壳、账簿新建/备份/还原/结算、密码、设置、快捷键和授权的 Rust 开发合同
- [runtime-accounts-and-master-data-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-accounts-and-master-data-contract.md)
  - B02 账户类型目录、开户向导、组合账户、期初资金、分类、人员、币种、汇率和存款利率的 Rust 开发合同
- [runtime-transactions-and-ledger-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-transactions-and-ledger-contract.md)
  - B03 单笔/批量交易、平衡分录、模板、分期、查找筛选、审计和图表一致性的 Rust 开发合同
- [runtime-debts-credit-and-amortization-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-debts-credit-and-amortization-contract.md)
  - B04 债权债务合同、还款计划、信用卡账单、分期、预付待摊和网贷关联的 Rust 开发合同
- [runtime-deposits-and-bank-wealth-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-deposits-and-bank-wealth-contract.md)
  - B05 定期账户、存单周期、续存/到期、银行理财产品、持仓本金和现金流事件的 Rust 开发合同
- [runtime-investment-shared-projections-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-investment-shared-projections-contract.md)
  - B07 持仓调整、投资现金事件、估值快照、成本/市值构成、历史盈亏和市值变动的 Rust 开发合同
- [runtime-securities-ledger-and-valuation-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-securities-ledger-and-valuation-contract.md)
  - B08 证券身份、账户资金来源、费率继承、交易与公司行为、持仓批次、行情和估值的 Rust 开发合同
- [runtime-open-and-money-market-funds-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-open-and-money-market-funds-contract.md)
  - B09 开放式基金与货币基金目录、账户、金额/份额、转换、认购、分红、拆分和估值的 Rust 开发合同
- [runtime-bonds-ledger-and-maturity-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-bonds-ledger-and-maturity-contract.md)
  - B10 债券目录、账户、净价/全价、应计利息、成本批次、估值、到期和提前兑取的 Rust 开发合同
- [runtime-calculation-and-report-projections.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-calculation-and-report-projections.md)
  - 计算字段、汇总规则、报表组件、交易/统计字段与 SQLite 查询投影规格
- [runtime-command-and-state-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-command-and-state-evidence.md)
  - `1407` 个交互控件、快捷键、默认选项和设计时命令状态
- [runtime-validation-scenarios.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-validation-scenarios.md)
  - 动态菜单、写入结果、计算公式和报表导出的最小验证场景
- [runtime-execution-queue.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-execution-queue.md)
  - `20` 个业务批次中的 `460` 个窗体、`1407` 个可交互控件、`2000` 个事件和 `502` 个高风险候选的逐项运行队列
- [runtime-observation-record-template.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-observation-record-template.md)
  - 单个窗体的入口、状态、命令结果、数据流、证据和 Rust 需求回填模板
- [target-ui-consolidation-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\target-ui-consolidation-map.md)
  - `460` 个旧窗体到 `11` 个 Rust 目标分区和 `40` 个页面族的全量归并，以及投资共享框架和逐窗体追溯
- [data-exchange-and-persistence-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-exchange-and-persistence-contract.md)
  - 21 类整账簿数据、交割单映射、备份还原、附件、同步和导出开发契约

## 7. 结构化 JSON 产物

- [resource-forms.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\resource-forms.json)
- [moneyhome8-data-object-map.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\moneyhome8-data-object-map.json)
- [test-mh8-object-map.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\test-mh8-object-map.json)
- [test-mh8-index-field-hints.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\test-mh8-index-field-hints.json)
- [table-evidence-matrix.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\table-evidence-matrix.json)
- [shared-model-core.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\shared-model-core.json)
- [shared-field-core.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\shared-field-core.json)
- [investment-cache-type-stats.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\investment-cache-type-stats.json)
- [cache-overlap-analysis.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\cache-overlap-analysis.json)
- [mh8-semantic-hints.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\mh8-semantic-hints.json)
- [table-semantic-map.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\table-semantic-map.json)
- [inner-table-field-map.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\inner-table-field-map.json)
- [runtime-dfm-all-forms.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-dfm-all-forms.json)
- [runtime-dfm-forms.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-dfm-forms.json)
- [runtime-calculation-evidence.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-calculation-evidence.json)
- [runtime-command-state-evidence.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-command-state-evidence.json)
- [runtime-data-exchange-evidence.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-data-exchange-evidence.json)
- [runtime-form-coverage-audit.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-coverage-audit.json)
- [runtime-form-composition-evidence.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-composition-evidence.json)
- [runtime-internal-surface-evidence.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-internal-surface-evidence.json)
- [runtime-method-evidence.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-method-evidence.json)
- [runtime-event-handler-evidence.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-event-handler-evidence.json)
- [runtime-event-command-dataflow.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-event-command-dataflow.json)
- [sqlite-domain-coverage-audit.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-domain-coverage-audit.json)
- [backup-manifest.schema.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\backup-manifest.schema.json)
- [backup-manifest-template.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\backup-manifest-template.json)
- [target-ui-consolidation-map.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\target-ui-consolidation-map.json)

## 8. 当前最重要的缺口

- `test.mh8` 正式表结构、真实样例和旧计算字段关系
- `记账` 动态下拉、页面跳转和代表性截图
- 财务诊断、规划、目标和投资收益率的精确公式与边界结果
- 专用报表的运行列、分组、小计、图表和空结果已由 B16 动态补证；仍缺精确 SQL、排序钻取、筛选边界、导出格式和打印结果
- 通用 XML 的完整导入语义、信用卡账单、备份压缩和附件目录；同步与行情页面已由 B18 动态确认，仍缺真实同步冲突/删除传播/断点续传、移动端结果和其余行情源协议
- AI 当前无用户入口，控制台只确认 `Ctrl+F12` 配置；金额计算器已通过 `F4` 动态唤起但仍缺回填/错误/焦点行为，以及 `37` 个已定位嵌入视图的空数据、有数据、筛选和交互结果
- 无 VMT 资源均已有产品范围决策；仍需验证取款资源与运行类字段完全对应，以及是否存在需要迁移的历史工具栏布局数据
