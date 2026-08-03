# MoneyHome8 重构分析包说明

本文档是 `docs/` 目录的入口说明，告诉后续阅读者：

1. 先看什么
2. 各文档分别回答什么问题
3. 当前最关键的未完成项是什么

当前日期基线：`2026-07-28`

## 1. 如果你只看 3 份文档

优先看：

1. [rebuild-prd.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\rebuild-prd.md)
2. [feature-catalog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\feature-catalog.md)
3. [data-source-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-source-map.md)

这三份分别回答：

- 产品/技术总目标是什么
- 目前都确认了哪些功能
- 当前到底有几层数据源

## 2. 如果你要继续逆向排查

优先看：

1. [analysis-index.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\analysis-index.md)
2. [mh8-storage-investigation.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\mh8-storage-investigation.md)
3. [linked-table-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\linked-table-evidence.md)
4. [mh8-structure-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\mh8-structure-evidence.md)
5. [field-semantic-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\field-semantic-evidence.md)
6. [auth-research-plan.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\auth-research-plan.md)

这组文档主要针对：

- `test.mh8` 旧数据迁移研究；该组不是新系统开发主线
- 主账本与 `mhlink.mdb` 的关系
- 主账本里已经能看到哪些对象、字段、索引线索
- 主账本里少量字段已经能看出哪些业务语义
- 主账本里的候选表分域与表簇分布
- 如何在不阻塞新系统的前提下继续建立旧字段迁移映射

## 3. 如果你要直接开始写 Rust

优先看：

1. [phase1-requirements-analysis.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\phase1-requirements-analysis.md)
2. [workplans/phase1-execution-plan.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\workplans\phase1-execution-plan.md)
3. [workplans/phase1-domain-contract-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\workplans\phase1-domain-contract-audit.md)
4. [domain-mapping-spec.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\domain-mapping-spec.md)
5. [entity-catalog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\entity-catalog.md)
6. [schema-hypothesis.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\schema-hypothesis.md)
7. [rust-module-plan.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\rust-module-plan.md)
8. [implementation-backlog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\implementation-backlog.md)
9. [migration-strategy.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\migration-strategy.md)
10. [runtime-calculation-and-report-projections.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-calculation-and-report-projections.md)
11. [sqlite-schema-and-query-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-schema-and-query-contract.md)
12. [runtime-command-and-state-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-command-and-state-evidence.md)
13. [runtime-validation-scenarios.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-validation-scenarios.md)
14. [data-exchange-and-persistence-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-exchange-and-persistence-contract.md)
15. [runtime-form-coverage-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-coverage-audit.md)
16. [runtime-form-composition-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-composition-evidence.md)
17. [runtime-internal-surface-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-internal-surface-evidence.md)
18. [runtime-event-handler-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-event-handler-evidence.md)
19. [runtime-event-command-dataflow.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-event-command-dataflow.md)
20. [runtime-destructive-and-file-operation-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-destructive-and-file-operation-contract.md)
21. [runtime-accounts-and-master-data-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-accounts-and-master-data-contract.md)
22. [runtime-transactions-and-ledger-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-transactions-and-ledger-contract.md)
23. [runtime-debts-credit-and-amortization-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-debts-credit-and-amortization-contract.md)
24. [runtime-open-and-money-market-funds-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-open-and-money-market-funds-contract.md)

这组文档主要回答：

- 领域实体怎么拆
- 候选表和字段怎么映射
- 哪些字段候选更值得优先信任
- 哪些表更适合先实现、哪些只是结构线索
- Rust 模块怎么组织
- 先做哪些任务
- 旧账本怎么迁移最稳
- 旧程序计算字段、汇总规则和 SQLite 查询投影怎么落地
- 新 SQLite 真相表、索引和 Rust 只读查询端口如何对应
- `53` 类运行时实体候选如何落到真相表、通用模型、专属合同、输入投影或适配器边界
- 旧程序命令、快捷键、初始禁用/隐藏/选中状态如何建模
- 代表性数据和 `25` 张报表应按什么步骤做运行态校准
- 全部 `460` 个窗体、`1407` 个交互控件和 `2000` 个事件应按什么批次逐页执行、记录和关闭
- `460` 个 Delphi 窗体如何归并为 `11` 个 Rust 目标分区和 `40` 个页面族，并保持功能追溯不丢失
- 导入导出、交割单、备份还原、附件和同步应如何形成可审计 Rust + SQLite 边界
- 全部 `460` 个旧运行时窗体如何映射到业务域、交互角色、目标数据流和新 UI 去留决策
- `37` 个嵌入视图如何装配到父窗体，以及哪些 Frame 在多个业务页面中复用
- AI、控制台和金额计算器宿主分别属于实验能力、内部诊断还是共享技术组件，以及它们的方法级代码合同和外部数据边界
- `2000` 个旧事件处理器中哪些已定位真实代码、哪些只是同名候选，以及哪些属于资源型无 VMT 边界
- 每个旧事件建议落到哪个 Rust 应用边界，以及账户删除、备份还原、导入导出和模板覆盖应遵守什么事务规则

## 4. 如果你要补 UI 证据

优先看：

1. [top-level-navigation-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\top-level-navigation-observations.md)
2. [data-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-page-observations.md)
3. [report-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\report-page-observations.md)
4. [analysis-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\analysis-page-observations.md)
5. [ui-verification-plan.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\ui-verification-plan.md)
6. [runtime-command-and-state-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-command-and-state-evidence.md)
7. [runtime-validation-scenarios.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-validation-scenarios.md)
8. [runtime-execution-queue.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-execution-queue.md)
9. [runtime-observation-record-template.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-observation-record-template.md)
10. [target-ui-consolidation-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\target-ui-consolidation-map.md)

当前 UI 状态：

- `财务数据`：已有页面证据
- `财务报表`：已有页面证据
- `财务分析`：已有页面证据
- `记账`：B03/B06 已覆盖日常收支、取款、转账、工资、分拆、批量模板、查找筛选、账户流水和概况图表；日常收入/支出、带来源手续费的取款、同币种转账与来源手续费、跨币种货币兑换均已真实保存并冷启动校准，货币兑换还已确认稳定账户 ID 绑定、两侧账户/币种/金额校验及确认与保存并继续的共享校验链；保存并继续成功态、附件、全部取完、分期、其它提交和剩余换汇边界仍待验证
- `债权债务/信用`：B04 已覆盖债权债务明细、构成、还款表、概况、信用卡交易/分期/账户/还款和单双币/网贷向导；合同保存、账单与摊还公式仍待校准
- `定期存款/银行理财`：B05 已覆盖定期账户编辑、工作区、开户向导，以及银行理财账户、产品目录、产品编辑和持仓工作区；续存、到期、产品生命周期和真实交易仍待校准
- `投资公共能力`：B07 已覆盖投资一览、成本/市值构成图、历史盈亏、市值构成与变动、持仓调整及共享费用/利息编辑器，并真实验证银行 CNY 利息收入与外汇 CNY 其它费用；其它产品域费用/利息、真实成本批次、实现盈亏和跨币种边界仍待校准
- `上市证券`：B08 已覆盖证券账户向导/编辑/概况、证券与价格目录、全局费率、代码变更、持仓统计、交易明细、市值构成、历史盈亏和七类交易表单；账户级费率、新股关系、证券选择及真实费用/成本公式仍待校准
- `开放式基金/货币基金`：B09 已覆盖两类账户向导/编辑/概况、基金目录、净值、持仓统计、交易明细、市值、历史盈亏和 12 类交易表单；真实金额/份额、费率、收益结转、成本和拆分公式仍待校准
- `债券`：B10 已覆盖债券资料目录/编辑器、账户向导/编辑/概况、持仓统计、交易明细、成本市值构成、历史盈亏和买入、卖出、到期、提前兑取、利息表单；真实成交、应计利息、成本、兑付和税务公式仍待校准
- `融资融券`：B12 已覆盖开户、账户、持仓/交易、融资融券交易、担保物、批量偿还和费率；真实临时融资/融券合同已确认单笔直接还款、直接还券与合同编辑的合同绑定、默认值和取消路径。批量直接还款又复现未结合同跨重启存在但候选为空、空行提交被阻断，成功偿还与公式仍待校准
- `保险/社保`：B13 已覆盖商业保险与社保开户、共享工作区、交易、现金价值和概况；非零开户确认已缴保费生成独立“余额调整”，现金价值同日新增执行覆盖更新且修改后跨页一致。旧保险价值增加/减少资源在当前版本无用户入口并由现金价值快照替代，标记为 `unreachable`
- `重大资产/家居物品`：B14 已覆盖账户、主数据、交易、估值和成本市值构成；物品买入分期向导第一页及必填校验已动态确认，后续页与真实分期写入仍待校准
- 命令状态：已确认 `1407` 个交互控件、`36` 个快捷键和初始禁用/隐藏/选中状态，仍缺真实点击后的结果校准
- 事件代码：`2000` 个去重处理器中 `1951` 个已定位当前类或真实父类代码；3 个资源型无 VMT 窗体中交割单已证明可达，剩余 2 个待确认
- 动态队列：已形成 `20` 个批次并覆盖全部 `460` 个窗体；当前为 `448 partial + 1 parent + 9 pass + 2 unreachable`，`blocked` 与 `pending` 均为零

## 5. 如果你要看功能面到底有多宽

优先看：

1. [function-matrix.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\function-matrix.md)
2. [resource-form-family-index.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\resource-form-family-index.md)
3. [feature-catalog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\feature-catalog.md)
4. [runtime-form-coverage-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-coverage-audit.md)
5. [runtime-form-composition-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-composition-evidence.md)
6. [runtime-internal-surface-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-internal-surface-evidence.md)
7. [runtime-event-handler-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-event-handler-evidence.md)
8. [runtime-event-command-dataflow.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-event-command-dataflow.md)

这里能看到：

- 顶层工作区
- 账户体系
- 通用收支
- 债权债务/信用
- 外汇/证券/基金/债券/期货/黄金/贵金属/融资融券/保险/社保/重大资产
- 预算/提醒/规划/目标
- 导入导出
- 报表分析
- 长尾辅助工具
- `460/460` 个窗体的逐项覆盖，以及 `400 + 37 + 2 + 21` 四层表面分类
- `107` 条逻辑直接组合关系和全部嵌入视图的父窗体/最终宿主
- `2332` 条事件绑定到 `1951` 个已定位代码处理器的全量追溯，以及 3 个资源型遗留窗体的范围边界

## 6. 如果你要看数据流

优先看：

1. [scenario-data-flows.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\scenario-data-flows.md)
2. [entity-flow-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\entity-flow-map.md)
3. [workspace-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\workspace-map.md)
4. [cross-domain-dataflow-catalog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\cross-domain-dataflow-catalog.md)
5. [runtime-calculation-and-report-projections.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-calculation-and-report-projections.md)
6. [data-exchange-and-persistence-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-exchange-and-persistence-contract.md)
7. [runtime-ai-console-calculator-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-ai-console-calculator-contract.md)
8. [runtime-event-command-dataflow.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-event-command-dataflow.md)
9. [runtime-destructive-and-file-operation-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-destructive-and-file-operation-contract.md)

## 7. 如果你要做产品和架构决策

优先看：

1. [rebuild-prd.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\rebuild-prd.md)
2. [local-database-selection.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\local-database-selection.md)
3. [sqlite-domain-coverage-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-domain-coverage-audit.md)
4. [similar-systems-benchmark.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\similar-systems-benchmark.md)
5. [objective-coverage-matrix.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\objective-coverage-matrix.md)

这组文档明确区分原程序功能等价、内部架构现代化和竞品可选增强，避免数据库结构复刻或竞品功能扩张偏离主目标。

## 8. 当前最关键的未完成项

### P1

- 按 [runtime-validation-scenarios.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-validation-scenarios.md) 校准交易提交、批量模板、分期、投资、预算、提醒、目标和报表的真实结果
- 确认诊断、规划、投资收益和报表动态列的精确计算口径

### 并行迁移线

- 打通 `test.mh8` 的正式认证
- 获取主账本正式表结构和样例数据
- 建立旧字段到 SQLite 新模型的可追溯迁移映射

### P2

- 验证 `记账` 除已完成日常收入/支出、带来源手续费的取款、同币种转账、银行 CNY 利息收入、外汇 CNY 其它费用和最小货币兑换外的单笔/批量真实写入，以及全部取完、费用/利息、货币兑换保存并继续成功态、同账户/同币种动态提示与其它换汇边界、分拆尾差、分期生成、审计和失败回滚

### P3

- 进一步细化缓存协议
- 动态确认通用 XML 的完整导入语义、信用卡账单、备份压缩和报表导出的实际格式
- 动态确认交割单边界值与最终落库、旧附件目录行为、真实同步冲突/删除传播/断点续传、移动端结果和其余行情源协议

## 9. 当前阶段的总判断

- 功能面：静态范围已完成 `460/460` 无遗漏分类，动态结果仍需校准
- 数据源分层：已经较清晰
- 领域模型：已经足够开始正式实现
- 最大不确定性：旧库迁移映射、动态交互与计算结果口径
