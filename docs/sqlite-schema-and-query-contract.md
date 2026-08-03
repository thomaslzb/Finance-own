# SQLite 真相表与查询契约

本文档把运行时 DFM 已确认的流水、余额、标签、投资和报表字段转换为新系统的 SQLite 核心模式。它描述新库设计，不复刻旧 Jet 表名；旧字段只在迁移映射层保留。

可执行迁移：

- [0001_core.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0001_core.sql)
- [0002_planning_and_automation.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0002_planning_and_automation.sql)
- [0003_contracts_exchange_and_sync.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0003_contracts_exchange_and_sync.sql)
- [0004_insurance_cash_value.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0004_insurance_cash_value.sql)
- [0005_insurance_cash_value_as_of.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0005_insurance_cash_value_as_of.sql)
- [0006_insurance_cash_value_amount_guard.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0006_insurance_cash_value_amount_guard.sql)
- [0007_payroll_income_and_application_identity.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0007_payroll_income_and_application_identity.sql)
- [0008_party_profile.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0008_party_profile.sql)
- [0009_party_list_lifecycle.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0009_party_list_lifecycle.sql)
- [0010_prepaid_expenses.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0010_prepaid_expenses.sql)
- [0011_deposit_rate_versions.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0011_deposit_rate_versions.sql)
- [0012_financial_goal_progress_baseline.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0012_financial_goal_progress_baseline.sql)
- [0013_plan_and_reminder_occurrences.sql](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\migrations\0013_plan_and_reminder_occurrences.sql)

领域覆盖审计：

- [sqlite-domain-coverage-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-domain-coverage-audit.md)
- 当前 `53` 类运行时实体候选已全部获得明确契约；十三版迁移共创建 `63` 张表、`21` 个视图和 `56` 个显式索引

可重复验证：

```powershell
python tools\validate_sqlite_schema.py
```

## 1. 设计决定

### 1.1 交易真相

一笔业务由 `transactions` 记录业务日期、稳定序号、类型、状态和说明，由 `transaction_entries` 记录最终原子账户分录。

- 收入：至少一条 `inflow` 分录
- 支出：至少一条 `outflow` 分录
- 转账：转出账户 `outflow` + 转入账户 `inflow`
- 手续费：单独的 `role=fee` 分录
- 分类或账户拆分：拆成多条有稳定 `line_no` 的分录
- 作废：修改交易状态为 `voided`，不物理删除审计真相

该结构直接保护旧程序已确认的“转账、手续费、分类拆分、账户拆分必须原子提交”场景，同时避免交易头和多组拆分表产生笛卡尔组合。

### 1.2 金额与精度

- 普通金额：`INTEGER` 最小货币单位，币种的 `minor_unit` 明确小数位
- 数量：`quantity_units + quantity_scale`
- 价格：`price_units + price_scale`
- 汇率：`rate_units + rate_scale`
- 时间：ISO 8601 `TEXT`；业务日期单独保存为 `YYYY-MM-DD`

SQLite 不承担隐式浮点舍入。Rust 领域层必须使用定点值并统一舍入策略，不能将财务金额转换为 `f64` 后写回。

### 1.3 原币与本币

`transaction_entries` 同时允许保存：

- 原币金额与币种
- 本币折算金额与币种
- 使用的 `exchange_rate_snapshots` 标识

这使 `IncLocal / ExpLocal` 可重建且可审计。没有汇率快照时，本币金额必须为空，不能静默使用当前汇率补写历史交易。

### 1.4 删除与解除关系

删除动作必须先区分“删除业务对象”和“解除对象关系”，不能由 UI 直接拼接 SQL：

- 删除账户组使用 `accounts.group_id ON DELETE SET NULL`，只解除账户归属，保留账户、交易和余额。
- 删除仍有业务引用的账户、分类、币种或人员必须由引用保护规则拒绝，或先完成显式迁移/停用。
- 附件内容与交易关系分开管理；`transaction_attachments.attachment_id ON DELETE RESTRICT` 保证仍有引用时不能物理删除附件记录和受管文件。
- 账户、批量交易等级联影响较大的操作必须先返回影响数量和阻断原因，再用同一操作及修订标记原子提交。

### 1.5 模板、计划与规划输入

- `transaction_templates + transaction_template_entries` 只保存交易草稿；实际执行必须生成新的 `transactions + transaction_entries`，不能把模板当作交易真相。
- `schedules` 保存启停状态、下次执行时间、最大次数、提前提醒天数和版本化 `recurrence_json`；`schedule_occurrences` 固化每次应发生日期、规则版本、执行模式、状态、动作时间和最终交易。Rust 领域层负责校验周期规则、幂等生成实例，并在成功执行后推进下一次时间，不能只依赖 `last_generated_transaction_id` 表达全部历史。
- 计划金额规则至少允许精确值、近似值和区间值；匹配必须保存命中条件、候选交易、最终选择和时间窗口。预测只消费未完成计划实例，不把预测值写入账户余额或已过账分录。
- `budgets + budget_items` 保存预算边界，实际消耗由已过账分录投影，不回写累计值。
- `reminders` 使用 `target_kind + target_id` 连接多种业务对象，`condition_json` 只保存版本化条件；`reminder_occurrences` 固化每次触发时的条件快照、观测值、处理动作和时间，投递结果独立进入 `notification_delivery_log`。
- `financial_goals` 通过 `financial_goal_accounts` 绑定账户；账户仍被目标引用时禁止静默物理删除。
- `financial_plan_inputs` 使用版本化 JSON 保存尚待动态校准的专题参数，公式和年度结果未校准前不固化为数据库真相。

### 1.6 日记真相与日历投影

日记扩展生命周期已经动态确认，但尚未进入当前 v13 迁移。下一版迁移应新增等价于 `diary_entries` 的真相表，至少保存稳定 ID、账簿 ID、账簿本地自然日、版本化安全富文本、规范化纯文本、创建/更新时间、行版本和可审计删除状态。

- 不对 `ledger_id + diary_date` 添加唯一约束；同日是否允许多篇仍待动态验证。
- 月度列表使用 `ledger_id + diary_date + delete state` 范围索引；搜索使用纯文本索引或等价 FTS 投影，不匹配富文本控制标记。
- 保存正文、格式、纯文本投影和行版本必须同事务提交；修改使用稳定 ID 和乐观并发检查。
- 财务日历按 `ledger_id + diary_date` 只读聚合日记来源，不复制正文或删除状态。
- 导出读取冻结的列表查询快照并写入用户选择目录；文件格式和编码在成功路径校准前不得固化为兼容结论。

详细运行证据和待验证边界见 [runtime-diary-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-diary-contract.md)。

### 1.7 人物生日与日历发生实例

当前 v13 已在 `parties` 保存 `birthday_calendar + birth_year + birth_month + birth_day`，并由约束保证生日四列全空或完整存在。动态样例进一步确认生日仍属于人物真相，财务日历只读取人物字段生成摘要。

- 下一版日历查询应生成可重建的 `BirthdayOccurrence`，输出 `party_id`、人物版本、当前名称、原始历法分量、发生日期、规则版本、来源类型和命令能力；不得保存可独立漂移的姓名或生日副本。
- 公历历史年份周年、`2月29日`、农历换算、闰月、时区和账簿业务日策略尚未全部校准，必须由领域规则版本处理，不能直接写成 SQLite 日期字符串比较。
- 人物修改、隐藏和删除与日历查询通过提交版本保持一致；缓存发生实例时必须包含人物版本和规则版本，并能从 `parties` 全量重建。
- 日历按发生日期读取生日，与交易、计划实例、提醒和日记来源做只读并集；单一来源删除不能级联删除其它来源。

详细运行证据和待验证边界见 [runtime-birthday-calendar-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-birthday-calendar-contract.md)。

### 1.8 普通提醒与日历投影

动态样例确认普通提醒定义、待处理实例和财务日历投影是三个边界。一次性实例在 `pending` 时按应发生日进入日历；跳过后日历来源立即消失，但定义仍保留在已完成范围，真实动作必须是 `skipped` 而不是执行。

- 下一版日历查询应按 `ledger_id + occurrence_date + status` 读取普通提醒实例，并输出稳定 `occurrence_id`、定义与规则版本、摘要、来源类型和 `can_open`；不能用提醒名称作为关联键。
- 应发生日与提前提醒资格窗口必须分列或以等价的类型化结构保存。`v_today_reminder_inbox` 可按资格窗口读取，日历则按应发生日读取；未来实例的旧版日历规则尚未校准，不能把两个查询合并。
- 跳过命令原子写入实例状态、动作时间、操作者和幂等键；成功提交后今日提醒与日历从同一提交版本刷新，不生成交易、不删除定义，也不影响同日其它来源。
- `pending` 普通提醒进入当前兼容日历，`skipped` 不进入。`executed`、`dismissed`、`failed`、`archived`、重复实例和定义修改后的日历行为仍待动态验证。
- 查询索引至少覆盖 `ledger_id + occurrence_date + status`；历史审计查询仍按定义 ID 和状态读取全部实例，不能为当前投影性能物理删除已处理行。

详细运行证据和待验证边界见 [runtime-reminder-calendar-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-reminder-calendar-contract.md)。

## 2. 核心表

| 领域 | 真相表 | 保护的业务规则 |
| --- | --- | --- |
| 账簿与币种 | `ledgers`, `currencies` | 每个账簿明确本位币和金额精度 |
| 账户树 | `account_groups`, `accounts` | 余额由分录重算；删除分组只解绑账户，账户表不保存可漂移余额 |
| 基础资料 | `categories`, `tags`, `parties` | 分类、标签、人员/机构独立生命周期；三类人员共享账簿级名称空间 |
| 交易 | `transactions`, `transaction_entries` | 同一事务内提交收支、转账、拆分和手续费 |
| 标签 | `transaction_tags`, `account_tags` | 标签既可关联流水，也可关联资产账户 |
| 汇率 | `exchange_rate_snapshots` | 历史本币金额可追溯到具体汇率 |
| 附件 | `attachments`, `transaction_attachments` | 文件元数据与交易关系分离，可按哈希去重；仍有交易引用时禁止物理删除 |
| 投资 | `investment_instruments`, `investment_trades`, `investment_lot_allocations`, `market_quotes` | 成交、持仓增减方向、批次成本分配和行情各自可审计 |
| 报表设置 | `report_presets` | 筛选条件和图表序列不进入交易真相 |
| 模板与计划 | `transaction_templates`, `transaction_template_entries`, `schedules`, `schedule_occurrences` | 模板是可复用输入；计划定义与每次应发生实例分离，执行成功后实例关联独立交易真相。下一版还必须冻结实例的今日提醒可见性及执行/跳过能力 |
| 预算与提醒 | `budgets`, `budget_items`, `reminders`, `reminder_occurrences` | 预算消耗由分录重建；提醒规则与触发实例分离，条件、目标快照和触发时观测值保持版本化且不直接写财务结果。四类限额条件在 Rust 领域层使用类型化枚举 |
| 财务目标 | `financial_goals`, `financial_goal_accounts` | 目标金额与账户余额输入分离，账户关系受删除保护 |
| 财务规划 | `financial_plan_scenarios`, `financial_plan_inputs`, `financial_plan_accounts` | 保存方案与校准输入，不提前固化未知公式结果 |
| 专属合同 | `debt_contracts`, `credit_account_terms`, `futures_contract_terms`, `margin_account_terms`, `margin_contracts`, `tangible_asset_details`, `insurance_policies`, `social_security_profiles` | 只保存通用模型无法表达的条款，资金变化仍进入交易分录 |
| 保险估值 | `insurance_cash_value_snapshots`, `insurance_cash_value_history` | 当前快照按保单和估值日唯一；`value_minor` 为非负整数最小单位，负数由数据库触发器拒绝；同日 upsert、修改和删除均写入历史且不生成资金分录；查询显式携带 `as_of_date` 并从生效区间选择唯一快照，未来快照生效前不进入当前投影，无匹配快照的消费者投影为零 |
| 保险事件 | `insurance_events` | 开户调整、缴费、返还、分红、退保和迁移调整使用显式类型；资金交易可选关联，不能由金额方向推断业务；退保在 `details_json.finish_account` 保存提交时的终止选择，不能从当前保单状态反推历史意图 |
| 导入审计 | `import_field_mappings`, `import_batches`, `import_rows` | 来源哈希、映射版本、原始行、字段错误和提交结果可追溯 |
| 同步与通知 | `sync_profiles`, `sync_batches`, `sync_object_results`, `sync_conflicts`, `sync_tombstones`, `notification_delivery_log` | 本地账簿独立可写，远端结果、冲突和删除传播不静默覆盖真相 |
| 设置与费率输入 | `application_settings`, `fee_rule_snapshots` | 设置按作用域隔离；参考费率只保存来源快照，实际费用仍以分录为准 |
| 旧库迁移 | `legacy_id_map` | Jet 标识只存在于导入边界，不污染新领域主键 |
| 工资收入 | `payroll_income_details`, `payroll_category_components`, `payroll_social_contributions` | 收入、扣款、个人缴费和公司缴费分别保存，实收及社保权益由明细和账户分录共同核对 |

## 3. 已落地查询视图

| 视图 | 输出口径 | DFM 对应证据 |
| --- | --- | --- |
| `v_ledger_entries` | 每条原子账户分录、原币/本币金额、分类、标签、说明和附件状态 | 财务记录字段集合 |
| `v_account_transaction_running_balance` | 按业务日期、交易序号、分录序号累计的账户币种余额 | `Bala` 计算字段 |
| `v_account_balances` | 账户和币种当前余额 | 账户中心、目标、资产投影 |
| `v_life_theme_transactions` | 标签关联流水 | 标签页流入/流出汇总 |
| `v_life_theme_assets` | 标签关联账户余额 | 标签页资产金额合计 |
| `v_investment_position_inputs` | 持仓数量计算输入 | `38` 个交易/统计窗体中的持仓字段 |
| `v_investment_realized_profit_inputs` | 卖出与批次成本分配输入 | 历史盈亏字段和页脚绑定 |
| `v_budget_consumption_inputs` | 按预算项汇总已过账分类分录的消耗输入 | 预算跟踪与限额提醒 |
| `v_goal_account_balance_inputs` | 目标绑定账户的当前余额输入 | 财务目标进度 |
| `v_due_schedules` | 已启用且到期的计划执行输入 | 模板、计划和自动执行 |
| `v_pending_schedule_occurrences` | 按应发生日期读取待执行或失败待处理的计划实例 | 今日提醒中的计划执行、跳过和失败重试 |
| `v_schedule_lifecycle` | 按计划汇总待处理、执行、跳过、失败和取消实例数量 | 计划列表的执行状态、终止与恢复判断 |
| `v_today_reminder_inbox` | 合并计划实例与提醒触发实例，并给出可执行、可跳过能力；十三版仍把所有计划实例固定投影为 `1/1`，下一版须改为读取实例能力快照和收件箱可见性 | 今日提醒列表；保险仅提醒计划必须投影 `0/1`，固定账户自动计划不得因到期就进入今日提醒，预算偏差等提醒不可误用计划执行动作 |
| `v_debt_contract_inputs` | 债务合同、账户和参与方输入 | 借贷、负债和还款工作区 |
| `v_import_batch_audit` | 导入批次计数与逐行状态汇总 | 文件预览、错误修正和提交审计 |
| `v_open_sync_conflicts` | 尚未解决的本地/远端对象冲突 | 可选同步冲突处理 |
| `v_payroll_income_reconciliation` | 工资组成公式、实收账户和社保账户投影核对 | 工资收入复合提交与异常诊断 |
| `v_insurance_cash_value_effective_ranges` | 每份保单的现金价值快照及左闭右开生效区间；调用方用 `effective_from <= :as_of_date AND (effective_to_exclusive IS NULL OR :as_of_date < effective_to_exclusive)` 选择唯一值 | 保险账户余额、现金价值汇总、资产和报表；完整趋势图直接读取全部快照，禁止读取独立缓存旧值 |

投资视图刻意使用 `_inputs` 后缀：旧程序的成本法、费用归属、收益率分母和公司行动处理尚未用真实样例校准。校准前不得创建名称看似最终口径的 `v_investment_position` 或 `v_investment_realized_profit`。

十三版计划实例模式已能保存执行、跳过、失败和幂等交易关系，但能力模型仍不完整。保险动态样例确认至少存在三种组合：普通交易计划在今日提醒中可执行且可跳过；保险“仅做提醒”可跳过但不可执行；固定账户保险自动计划不进入今日提醒，但可从中央计划列表执行并在后台领取后无界面提交。下一版迁移应在实例上冻结 `show_in_today_inbox`、`can_execute`、`can_skip` 和执行策略版本或等价枚举，并让收件箱及执行器读取该快照；不能继续由 `source_kind='schedule'` 推断统一能力。计划修改还必须以版本替换未来未处理实例，领取和提交使用唯一幂等键。该迁移需提供 v13 到新版本的原子升级、三种能力组合、两缴费年度重算和自动执行后投影一致性测试。

限额提醒动态样例确认 `reminders` 的通用规则与 `reminder_occurrences` 的历史实例分层方向正确，但十三版仍缺目标快照版本和边界级幂等键。下一版迁移应增加等价于 `target_snapshot_version`、`boundary_kind`、`evaluation_version` 的字段或结构化快照，并保证相同 `reminder_id + condition_version + target_snapshot_version + boundary_kind` 唯一。`v_today_reminder_inbox` 对该来源固定投影 `can_execute=0`、`can_skip=0`；规则停用或删除可以移出当前兼容视图，但不可级联清除历史触发审计。跨类型目标引用当前由应用服务校验，删除目标前必须查询并预览受影响规则。

`investment_trades.position_effect` 明确记录本次业务对持仓数量的影响：`1` 增加、`-1` 减少、`0` 不改变。拆并股、转入转出和其它公司行动由业务命令显式给出方向，持仓视图不再根据活动名称猜测。

## 4. 索引与查询路径

| 查询路径 | 索引 | 目的 |
| --- | --- | --- |
| 账簿 + 状态 + 日期范围流水 | `idx_transactions_ledger_status_date` | 支持财务记录与绝大多数报表日期筛选 |
| 账户余额与流水 | `idx_entries_account_currency_transaction` | 支持账户/币种分区累计 |
| 分类收支 | `idx_entries_category_transaction` | 支持分类报表和预算消耗 |
| 标签流水/资产 | `idx_transaction_tags_tag_transaction`, `idx_account_tags_tag_account` | 支持标签页两类投影 |
| 汇率历史 | `idx_exchange_rates_pair_time` | 查找币种对最近或指定时点汇率 |
| 投资持仓 | `idx_investment_trades_position` | 按账户和标的聚合成交 |
| 最新行情 | `idx_market_quotes_latest` | 按标的读取最近行情 |
| 报表预设 | `idx_report_presets_lookup` | 按报表类型加载默认或命名预设 |
| 旧标识回查 | `idx_legacy_id_map_entity` | 迁移审计和重复导入检测 |
| 到期计划定义 | `idx_schedules_due` | 按启用状态和下次执行时间扫描需要生成实例的计划定义 |
| 计划实例 | `idx_schedule_occurrences_due_status`, `idx_schedule_occurrences_schedule_status` | 扫描待执行实例，并按计划回放执行、跳过和失败历史 |
| 预算周期 | `idx_budgets_period`, `idx_budget_items_category_period` | 按账簿、周期和分类投影预算消耗 |
| 提醒规则与实例 | `idx_reminders_due`, `idx_reminder_occurrences_trigger_status`, `idx_reminder_occurrences_rule_status` | 扫描提醒规则和待处理触发实例，并按规则回放历史 |
| 目标 | `idx_goals_status_date`, `idx_goal_accounts_account` | 目标列表和账户删除影响检查 |
| 财务规划 | `idx_financial_plan_scenarios_status`, `idx_financial_plan_accounts_account` | 方案状态查询和账户影响检查 |
| 专属合同 | `idx_debt_contracts_status_due`, `idx_margin_contracts_account_status`, `idx_insurance_policies_status_date` | 到期合同、账户风险和保单状态查询 |
| 保险现金价值审计 | `idx_insurance_cash_value_history_policy_date` | 按保单、估值日和版本回放同日 upsert、修改与删除历史 |
| 保险事件时间线 | `idx_insurance_events_policy_date` | 按保单、日期、事件类型和状态读取业务时间线 |
| 导入审计 | `idx_import_batches_status_created`, `idx_import_rows_batch_status` | 批次列表、预览和逐行错误筛选 |
| 同步冲突 | `idx_sync_batches_profile_started`, `idx_sync_object_results_status`, `idx_sync_conflicts_open`, `idx_sync_tombstones_pending` | 批次历史、失败重试、开放冲突和删除传播 |
| 通知与费率 | `idx_notification_delivery_retry`, `idx_fee_rule_snapshots_lookup` | 失败重试和有效期费率快照查找 |
| 人员名称唯一性 | `idx_parties_ledger_name_unique` | 阻止同一账簿的家庭成员、往来人员和机构出现完全同名记录 |
| 人员列表 | `idx_parties_ledger_category_hidden_name` | 按账簿、类别、隐藏状态和名称读取稳定列表 |
| 待摊费用列表 | `idx_prepaid_expenses_ledger_status_first_due`, `idx_prepaid_expenses_party_status` | 按账簿、状态、首次摊销日或人员读取待摊费用账户 |
| 待摊期次 | `idx_prepaid_installments_due_status` | 扫描到期且尚未入账的摊销期次 |
| 存款利率更新 | `idx_deposit_rate_batches_ledger_status_requested`, `idx_deposit_rate_items_batch_status_key`, `idx_deposit_rate_versions_lookup` | 查询更新批次、逐行校验状态和指定币种/期限的当前生效版本 |
| 财务目标进度 | `idx_goals_status_period`, `idx_goal_accounts_goal` | 按账簿、状态和目标期间读取目标，并关联创建时账户范围与当前余额输入 |

验证脚本通过 `EXPLAIN QUERY PLAN` 确认日期范围流水使用 `idx_transactions_ledger_status_date`，并执行 `PRAGMA foreign_key_check`。脚本还写入转出、转入和手续费三条分录，验证两侧余额；随后主动制造分录顺序冲突，确认交易头和已写分录会一起回滚。删除约束验证会实际删除测试账户组并确认账户仍存在且 `group_id` 置空，同时确认被交易引用的账户、分类、账簿币种和附件不能直接删除；解除附件关系后才允许删除附件记录。合同、同步与保险验证覆盖设置作用域、债务输入、期货条款、导入原始行与字段错误、开放同步冲突、通知投递、费率快照、保险事件、现金价值版本和非负金额保护。第七版验证 `application_id=1179604814`、工资实收 `100.00 - 10.00 - 10.00 = 80.00`、社保权益 `10.00 + 5.00 = 15.00` 和账户投影匹配；第八版验证人员精确分类、联系方式、地址、性别、带历法生日和机构字段约束；第九版验证三类人员名称账簿级唯一和隐藏记录仍受唯一索引约束；第十版验证待摊费用必填与期次边界、`100.01 CNY / 3` 期的目标尾差策略和剩余金额派生；第十一版验证存款利率批次按实际明细完整发布、未发布来源阻断、发布后不可原位改写、当前版本选择、负数与超过 `100%` 拒绝；第十二版验证财务目标起止日期、允许负值的完整初始估值快照、账户范围、公式版本和倒置期间拒绝；第十三版验证计划定义与执行实例、提醒规则与触发实例分层，已执行实例必须关联交易，已处理提醒必须记录动作和时间，并覆盖 v6/v7/v8/v9/v10/v11/v12 原子升级，最终 `user_version=13`。MoneyHome8 自动摊销旧公式、存款利率更多输入边界、目标标准进度公式和重复日历边界仍待动态验证，不作为已兼容结论。

## 5. 事务边界

Rust 契约已经落地：

- `src/domain/transactions.rs`：交易头、原子分录、方向、角色和保守业务校验
- `src/domain/reference_data.rs`：账簿、账户组、账户、分类、标签和往来方读取模型
- `src/app/transactions.rs`：原子写入仓储端口、写入结果和错误边界
- `src/app/reference_data.rs`：可用账簿初始化、账户树与基础资料生命周期端口
- `src/app/destructive_operations.rs`：删除影响预览、阻断原因、修订标记校验和原子执行端口
- `src/infrastructure/sqlite.rs`：文件账簿创建/打开、v6 核心表指纹确认与 v6/v7/v8/v9/v10/v11/v12 到 v13 原子升级、应用文件标识、币种/账簿/首账户原子初始化、账户组保留关系删除、基础资料维护、十三版迁移、`user_version`/完整性校验、原子交易写入和 `ReportReadRepository` 七组查询的具体适配器

可重复执行：

```powershell
& .\tools\run-rust-checks.ps1 -Action all
```

当前 Rust 测试会创建并重开版本 `13` 的文件账簿，同时校验 `application_id`，并验证具有核心表指纹的 v6 账簿和合法 v7/v8/v9/v10/v11/v12 账簿可原子升级、伪装成 v7 的其它 SQLite 文件会被拒绝。测试还覆盖账簿初始化、账户树、人员资料字段、跨类别及隐藏状态名称唯一性、基础资料生命周期、交易整体回滚、余额和投资查询，以及余额调整、工资、待摊费用、存款利率、财务目标基线、计划实例和提醒实例约束。当前结果为 `67 passed, 0 failed`。

一次业务命令应按以下顺序在单个 SQLite 事务中执行：

1. 分配账簿内单调递增的 `sequence_no`。
2. 写入 `transactions`。
3. 写入全部 `transaction_entries`，包括手续费和拆分行。
4. 写入标签、附件和投资成交扩展关系。
5. 校验账户、币种、分录方向和金额守恒规则。
6. 提交后再刷新余额、预算、目标和报表查询。

写入失败必须整体回滚。UI 不允许直接更新余额视图或投资统计结果。

破坏性操作在 UI 确认前只调用只读 `preview`。提交时应用层必须核对操作内容、阻断原因和 `revision_token`，仓储层在同一事务中重新校验修订标记并完成删除、作废或解除关系，防止预览后数据变化造成误删。

## 6. 当前覆盖与外部边界

当前 `53` 类实体候选中：`24` 类已有专属真相表，`10` 类由通用真相表承载，`8` 类已有专属合同边界，`4` 类已有输入投影，另有 `3` 类适配器边界和 `4` 类临时状态。数据库内不再有 `planned_missing` 或 `partial_existing` 项。

十三版迁移已经落地：

- 债务、信用、期货、融资融券、保险、社保和实物资产的专属合同条款
- 导入批次、原始行、字段映射、逐行错误和重复判断
- 同步身份、批次、对象结果、冲突、墓碑与通知投递日志
- 应用设置和费用规则快照
- 工资收入组成、账户投影核对和 Finance Own SQLite 文件标识
- 家庭成员、往来人员、机构分类，以及联系方式、地址、性别和带历法生日字段
- 三类共享的账簿级人员名称唯一索引和类别/隐藏状态列表索引
- 存款利率更新批次、逐行校验、不可变利率版本和当前生效投影
- 财务目标起止日期、允许负值的初始估值快照、账户范围、公式版本和进度输入投影
- 计划执行实例、提醒触发实例、实例生命周期统计和今日提醒统一投影
- 待摊费用主体、分期计划、幂等交易引用和剩余金额查询投影

资金变化仍必须进入 `transactions + transaction_entries`，专属表不得复制余额或交易真相。账簿外备份清单已由 [backup-manifest.schema.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\backup-manifest.schema.json) 与 [backup-manifest-template.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\backup-manifest-template.json) 定义，用于快照哈希、模式版本、完整性结果和附件相对路径，不放入活动数据库。逐实体结论见 [sqlite-domain-coverage-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-domain-coverage-audit.md)。

## 7. 待校准后再固化的规则

- 同一业务日期内旧程序使用的最终排序规则
- 跨币种转账的汇率方向、手续费币种和舍入时点
- 证券、基金、期货和贵金属的成本法
- 分红、拆并股、转入转出对成本的影响
- 已实现盈亏、浮动盈亏、含费盈亏和收益率分母
- 作废、隐藏账户和已关闭账户在 25 张报表中的纳入范围

这些缺口不阻止核心真相表实施，但阻止把投资最终公式标记为兼容原软件。
