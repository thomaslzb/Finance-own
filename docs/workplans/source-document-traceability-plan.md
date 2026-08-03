# 来源文档承接与需求追溯计划

本文档承接 `three-client-requirements-analysis.md`、`technical-architecture-proposal.md`、`rebuild-prd.md`、`requirements-analysis.md`、`acceptance-criteria.md`、`flutter-dotnet-interface-architecture.md`、`sync-protocol-draft.md`、`local-storage-and-ledger-architecture.md`、`coverage-status.md`、`objective-coverage-matrix.md`、`requirement-audit-matrix.md`、`traceability-matrix.md` 和 `ui-verification-plan.md`，用于把 `docs` 根目录中的历史分析、证据、PRD、架构和验收材料承接到 `docs/workplans` 的进行中需求计划。本文不引入新的产品取舍，只定义文档追溯边界。

## 1. 目标

1. 明确 `docs/workplans` 是当前需求分析、实施计划和验收链路的工作目录。
2. 明确 `docs` 根目录中的旧 PRD、旧 Rust 分析、运行证据、覆盖矩阵和验收标准是来源材料，不直接作为当前三端实施任务清单。
3. 防止 Flutter 三端、.NET 云端、Rust PC 本地核心的已确认架构被旧文档中的过期技术栈表述覆盖。
4. 保证旧 MoneyHome8 迁移证据、自动化证据、旧路径、旧原始行、迁移审计、迁移报告和脱敏摘要仍只保存在 PC 本地。
5. 为后续需求分析提供“发现来源 -> 承接 workplan -> 验收场景”的最短路径。

## 2. 文档分层

| 层级 | 目录或文档 | 当前职责 |
| --- | --- | --- |
| 当前工作计划 | `docs/workplans/*.md` | 三端需求分析、实施切片、验收场景和待开发计划 |
| 正式架构来源 | `technical-architecture-proposal.md`、`docs/adr/*.md` | Flutter + .NET + Rust PC 本地核心的决策来源 |
| 历史 PRD 与总览 | `rebuild-prd.md`、`requirements-analysis.md`、`phase1-requirements-analysis.md` | 功能域、旧程序行为和迁移边界来源 |
| 验收来源 | `acceptance-criteria.md`、`runtime-validation-scenarios.md`、`ui-verification-plan.md` | 旧功能等价、动态验证和 UI 验收口径来源 |
| 覆盖和追溯来源 | `coverage-status.md`、`objective-coverage-matrix.md`、`requirement-audit-matrix.md`、`traceability-matrix.md` | 需求覆盖、缺口和证据矩阵来源 |
| 证据和目录 | `runtime-*evidence*`、`*-catalog.*`、`*-inventory.*`、`*-observations.md` | 旧程序页面、控件、事件、数据流和运行结果证据 |

## 3. 当前架构承接规则

1. 当前第一版架构以 `technical-architecture-proposal.md`、ADR 和 `three-client-requirements-analysis.md` 为准。
2. Flutter 是 PC、Web 和手机三端 UI 的统一开发语言和框架。
3. .NET API 与 PostgreSQL 承担云端账号、账本成员、对象副本、同步、冲突、附件元数据和审计。
4. Rust 只作为 PC 客户端内置本地核心，不要求新用户安装 Rust，不进入 Web 或手机端。
5. PC 本地 SQLite 是 PC 离线账本真相源；Web 在线为主；手机保存草稿、队列、缓存和摘要，不保存完整本地账本。
6. 旧 MoneyHome8 原始文件和旧证据只进入 PC 本地迁移流程。
7. 根目录旧文档中“手机端本地完整 SQLite”“Rust 主系统”“旧同步协议兼容完成”等过期或未校准表述，不得覆盖当前 workplans。

## 4. 来源到 workplan 的承接矩阵

| 来源文档 | 已承接 workplan | 承接口径 |
| --- | --- | --- |
| `technical-architecture-proposal.md` | `three-client-requirements-analysis.md`、`flutter-pc-local-api-plan.md`、`dotnet-sync-api-plan.md`、`mobile-offline-queue-plan.md`、`flutter-web-online-plan.md` | 三端架构、技术栈、端职责 |
| `flutter-dotnet-interface-architecture.md` | `dotnet-sync-api-plan.md`、`flutter-web-online-plan.md`、`account-device-ledger-membership-plan.md` | Flutter 与 .NET API 分层、DTO、权限入口 |
| `sync-protocol-draft.md` | `dotnet-sync-api-plan.md`、`conflict-resolution-plan.md`、`mobile-offline-queue-plan.md`、`data-retention-deletion-recovery-plan.md` | 对象同步、游标、墓碑、冲突；过期手机完整本地库表述按当前架构修正 |
| `local-storage-and-ledger-architecture.md` | `ledger-lifecycle-storage-plan.md`、`domain-validation-invariants-plan.md`、`amount-currency-exchange-rate-plan.md`、`payroll-income-tax-social-contribution-plan.md` | PC SQLite、分录守恒、投影重建和工资公式 |
| `runtime-diary-contract.md` | `diary-calendar-richtext-plan.md` | 日记、富文本、搜索、导出和财务日历投影 |
| `runtime-birthday-calendar-contract.md` | `diary-calendar-richtext-plan.md`、`master-data-lifecycle-plan.md` | 人员生日真相、公历/农历生日字段、财务日历生日只读投影和旧证据 PC 本地保存 |
| `runtime-reminder-calendar-contract.md` | `schedule-reminder-occurrence-plan.md` | 普通提醒定义与实例分层、待处理日历投影、跳过动作、提前资格窗口和旧证据 PC 本地保存 |
| `feature-catalog.md`、`acceptance-criteria.md` 中的财务计算器和价格整理条目 | `financial-calculators-price-maintenance-plan.md` | 19 类财务计算器、公式状态和价格整理高风险删除 |
| `feature-catalog.md`、`runtime-bonds-ledger-and-maturity-contract.md` 中的净价/清洁价格计算条目 | `financial-calculators-price-maintenance-plan.md`、`market-instruments-trading-valuation-plan.md` | 净价、全价和应计利息计算只回填债券交易草稿，不直接入账 |
| `runtime-validation-scenarios.md`、`functional-ledger.md` 中的钱包充值/提现条目 | `wallet-recharge-withdrawal-plan.md` | 第三方钱包双边资金流、本金手续费组成和保存并继续 |
| `runtime-accounts-and-master-data-contract.md`、`runtime-debts-credit-and-amortization-contract.md`、`acceptance-criteria.md`、`functional-ledger.md`、`sqlite-schema-and-query-contract.md` 中的待摊费用条目 | `prepaid-expenses-amortization-plan.md` | 待摊费用主体、初始资金事实、确定金额期次、幂等摊销、计划重算和删除影响 |
| `feature-catalog.md`、`function-matrix.md`、`requirement-audit-matrix.md` 中的支票簿/票据条目 | `attachment-privacy-plan.md` | 票据、支票簿和银行凭证作为受管凭证或附件引用，不直接改变账务事实 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的附件生命周期条目 | `attachment-privacy-plan.md`、`data-retention-deletion-recovery-plan.md` | 多附件引用、最后引用待清理、物理清理幂等、哈希校验、扫描/配额/大文件错误和旧来源路径本地化 |
| `data-exchange-and-persistence-contract.md`、`runtime-securities-ledger-and-valuation-contract.md`、`runtime-command-and-state-evidence.md` 中的证券代码转换和新股关联条目 | `market-instruments-trading-valuation-plan.md` | 稳定工具 ID、代码历史、新股申购流程 ID、交割单导入关联 |
| `feature-catalog.md`、`runtime-dfm-functional-evidence.md` 中的客户服务条目 | `operations-observability-support-plan.md` | FAQ、官网、服务时间、联系方式和脱敏诊断 ID 支持入口 |
| `feature-catalog.md`、`coverage-status.md` 中的概况布局条目 | `three-client-ui-navigation-plan.md` | 工作台概况区块、图表摘要、显示偏好和拖动排序只作为 UI 偏好 |
| `feature-catalog.md`、`data-exchange-and-persistence-contract.md` 中的 XML、CSV、专用账单和回导条目 | `backup-import-export-plan.md` | 编码、版本、列顺序、来源适配器、21 类数据集选择、分区预览、覆盖/去重策略、预览错误和导出格式记录 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的旧 `.mh8k`、恢复为新账本、备份损坏和失败回滚条目 | `backup-import-export-plan.md` | 旧 `.mh8k` PC 本地隔离探测、解密校验、内容对比、恢复为新账本、失败回滚和旧迁移证据 PC 本地保存 |
| `cache-semantics.md`、`cache-and-package-investigation.md`、`code-type-mapping.md`、`domain-mapping-spec.md`、`coverage-status.md`、`open-gaps-register.md` 中的旧缓存和候选检索条目 | `cache-reference-lookup-plan.md` | `MoneyHome8.cache`、`Investment.cache` 只读候选、`_PY/_LIST/_3/_4/_9` 语义、候选版本、未确认中文片段保护和三端旧缓存隔离 |
| `feature-catalog.md`、`deposits-debts-credit-amortization-plan.md`、`coverage-status.md`、`open-gaps-register.md` 中的账单日管理条目 | `deposits-debts-credit-amortization-plan.md`、`date-time-period-semantics-plan.md` | 固定日、月末模式、相对偏移、短月份策略、账单生成幂等、历史账单规则冻结和领域层标准化 |
| `feature-catalog.md`、`coverage-status.md` 中的手机快查、远程通知、关于、许可、更新和验证码条目 | `settings-preferences-notification-plan.md`、`auth-session-secret-storage-plan.md`、`operations-observability-support-plan.md` | 外围入口、授权级设置、安全挑战、通知摘要和旧证据 PC 本地保存 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的同步、手机快查和远程通知条目 | `dotnet-sync-api-plan.md`、`mobile-offline-queue-plan.md`、`settings-preferences-notification-plan.md`、`conflict-resolution-plan.md` | 批次幂等、分片断点续传、取消、墓碑传播、下载续拉、手机快查失败分类和远程通知幂等 |
| `feature-catalog.md`、`coverage-status.md`、`open-gaps-register.md` 中的行情更新条目 | `market-instruments-trading-valuation-plan.md` | 行情、净值、汇率、存款利率、交易费率和历史价格更新批次；供应商适配器版本、行级失败、幂等重试、历史无数据、版本发布和旧协议证据 PC 本地保存 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的账簿结算、恢复点和失败回滚条目 | `ledger-lifecycle-storage-plan.md` | PC 本地结算预览、截止日、恢复点、幂等、防半写和旧结算校准证据 PC 本地保存 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的旧密码、KDF、换密钥和连续失败条目 | `auth-session-secret-storage-plan.md` | PC 本地账本密码/KDF、安全失败冷却、换密钥中断恢复和密钥材料不入云 |
| `coverage-status.md`、`functional-audit-checklist.md` 中的报表导出、打印、排序和筛选边界条目 | `reporting-planning-plan.md`、`list-query-filter-pagination-plan.md` | 报表/列表快照、查询参数、排序、对象版本、公式状态和旧报表证据 PC 本地保存 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的系统设置、快捷键、窗口状态、最近账簿和授权协议条目 | `settings-preferences-notification-plan.md` | 旧设置迁移预览、快捷键冲突、窗口边界校验、授权级设置和旧配置证据 PC 本地保存 |
| `coverage-status.md`、`functional-audit-checklist.md` 中的标签设为首页、拖放排序、批量关系和选择器候选失效条目 | `master-data-lifecycle-plan.md`、`command-form-lifecycle-plan.md` | 标签显示偏好、排序版本、批量关系影响预览、选择器候选版本和失败回滚 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的组合账户、账户组迁移、期初分录和资料入口草稿条目 | `master-data-lifecycle-plan.md`、`command-form-lifecycle-plan.md` | 组合账户原子提交、组成员版本、期初来源类型、无账本状态和跨类型未保存草稿 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的本位币切换、自定义币种、在线牌价和汇率边界条目 | `amount-currency-exchange-rate-plan.md`、`master-data-lifecycle-plan.md` | 本位币影响预览、自定义币种规范化、汇率暂存批次、重复业务键和旧牌价诊断 PC 本地保存 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的保存并继续、批量模板、复制粘贴、改变类型、转计划、退款、冲销和分期条目 | `command-form-lifecycle-plan.md`、`domain-validation-invariants-plan.md` | 新草稿/新幂等键、批量逐行策略、转换影响预览、退款冲销引用原事实、分期计划和已入账保护 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的定期、银行理财、债权债务和网贷条目 | `deposits-debts-credit-amortization-plan.md` | 理财产品生命周期、持仓本金/现金流/收益同快照、还款组成分配、网贷稳定身份和状态流转 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的开放式基金、货币基金、债券和融资融券条目 | `market-instruments-trading-valuation-plan.md`、`investment-advanced-assets-calibration-plan.md` | 基金确认/收费/资金在途/拆分、债券兑付/利息/税务、融资融券候选筛选/担保物和风险状态 |
| `coverage-status.md`、`feature-catalog.md`、`open-gaps-register.md` 中的保险、现金价值、退保、重大资产、家居物品和分期条目 | `insurance-social-security-tangible-assets-plan.md` | 保险返还/分红/退保事件边界、现金价值输入边界、重大资产多贷款、部分出售、估值删除和家居物品成本状态 |
| `coverage-status.md`、`feature-catalog.md`、`open-gaps-register.md` 中的财务诊断、目标和规划推演条目 | `financial-goals-planning-input-plan.md`、`reporting-planning-plan.md` | 起始余额组成、通胀/退休/资产增长/分期展开顺序、清空确认、多币种边界和公式状态 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的预算、诊断和目标进度条目 | `reporting-planning-plan.md`、`financial-goals-planning-input-plan.md` | 预算期间、退款/冲销、多币种、滚动导入、诊断零分母/阈值/缺估值和目标多账户估值进度 |
| `coverage-status.md`、`functional-audit-checklist.md`、`open-gaps-register.md` 中的报表、投资类子报表、趋势图和概况可用资金图表条目 | `reporting-planning-plan.md`、`list-query-filter-pagination-plan.md`、`three-client-ui-navigation-plan.md` | 报表排序、分组小计、趋势图、钻取版本、导出打印快照和概况图表数据口径 |
| `rebuild-prd.md` | `three-client-ui-navigation-plan.md`、`reporting-planning-plan.md`、`investment-advanced-assets-calibration-plan.md`、`shared-ui-ai-diagnostics-automation-plan.md` | 目标工作区、功能范围、旧页面收敛和共享组件 |
| `requirements-analysis.md` | 全部领域类 workplan | 旧程序行为、动态校准、迁移和缺口来源 |
| `acceptance-criteria.md` | `three-client-acceptance-scenarios.md`、`testing-acceptance-release-gates-plan.md` | 阶段验收、功能等价和发布门禁 |
| `coverage-status.md` | `testing-acceptance-release-gates-plan.md`、`three-client-implementation-slices.md` | 覆盖等级、验证缺口和发布风险 |
| `objective-coverage-matrix.md` | `testing-acceptance-release-gates-plan.md`、`domain-validation-invariants-plan.md` | 目标覆盖、SQLite 覆盖和剩余实现缺口 |
| `requirement-audit-matrix.md` | `testing-acceptance-release-gates-plan.md`、`source-document-traceability-plan.md` | 需求审计和来源追溯 |
| `traceability-matrix.md` | 各领域 workplan、`source-document-traceability-plan.md` | 旧窗体、动态记录和目标模型追溯 |
| `ui-verification-plan.md` | `three-client-ui-navigation-plan.md`、`testing-acceptance-release-gates-plan.md` | UI 验收、页面状态和截图验证来源 |

## 5. 证据类文档处理规则

1. `runtime-dfm-control-catalog.md`、`runtime-dfm-functional-evidence.md`、`runtime-event-handler-evidence.json`、`runtime-window-tree-evidence.md` 等证据目录不需要各自建立需求计划。
2. 当证据目录暴露新的用户可见能力、业务字段、命令、错误或隐私风险时，必须补到对应领域 workplan。
3. 当证据仅描述控件树、窗体组合、事件绑定或自动化运行过程时，只作为追溯来源，不进入产品需求清单。
4. 旧程序自动化证据涉及的完整路径、旧原始行、迁移审计、迁移报告、脱敏摘要和诊断输出只保存在 PC 本地。
5. 任何从证据文档提炼出的云端对象必须先转为新系统 DTO、对象版本和脱敏审计，不能上传旧证据本身。

## 6. 需求分析继续规则

后续继续做需求分析时按以下顺序处理：

1. 先在 `docs/workplans` 查是否已有对应计划。
2. 如果已有计划，只补引用、字段、验收或隐私规则。
3. 如果是新业务域或横切能力，再在 `docs/workplans` 新建独立计划。
4. 同步更新 `three-client-requirements-analysis.md`、`three-client-implementation-slices.md` 和 `implementation-backlog.md`。
5. 涉及端到端行为时，同步更新 `three-client-acceptance-scenarios.md`。
6. 每轮结束前复扫待人工确认标记、过期技术栈表述和 PC 本地隐私边界。

## 7. 验收

1. 所有 `*contract*.md` 都必须被至少一个 `docs/workplans` 文档引用或明确说明为证据类来源。
2. 三端架构文档不得出现互相矛盾的当前决策；过期草案必须被标记为历史或按当前架构降级。
3. 根目录 PRD、验收、覆盖和追溯文档中的需求必须能在 workplans 中找到承接口径，或被明确归为证据/历史来源。
4. 旧 MoneyHome8 证据、旧路径、旧原始行、迁移审计、迁移报告和脱敏摘要不得出现在云端同步、Web、手机、日志、导出或支持包中。
5. `docs/workplans` 中不得保留会阻塞继续分析的待人工确认标记。

## 8. 当前无需人工确认

本计划只是把已有来源文档纳入 `docs/workplans` 的追溯体系，没有改变 Flutter 三端、.NET 云端、Rust PC 本地核心、对象级同步、多账本隔离、冲突解决或旧迁移证据 PC 本地保存的已确认边界。
