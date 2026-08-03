# 报表、预算与提醒需求计划

本文档承接 `three-client-requirements-analysis.md`、`phase2-build-spec.md`、`coverage-status.md`、`open-gaps-register.md` 和当前 Rust 侧 `ReportReadRepository`、`PlanningRepository` 能力，定义 Finance Own 第一版基础报表、预算、提醒、计划、财务诊断和财务目标边界。

## 1. 目标

第一版必须支持：

1. PC 完整基础报表。
2. Web 基础报表和列表型查询。
3. 手机摘要报表、预算和提醒轻量查看。
4. PC/Web 管理预算、提醒和财务目标基础对象。
5. 报表表格、图表、导出和打印复用同一结果 DTO。
6. 报表筛选、加载、待刷新、失败和空状态。
7. 未校准投资公式不固化为正式结果。
8. 财务诊断和目标进度必须保存输入版本、公式版本、结果状态和边界错误。

第一版不要求：

1. 手机端复杂报表和高级导出。
2. 复杂投资收益率、成本批次和全部费用公式一次性闭环。
3. 自动计划执行后台任务完整闭环。
4. 高级报表设计器。

第一版不得：

1. 云端、Web 或手机保存 PC 本地报表缓存、旧迁移审计、旧报表校准证据、旧诊断公式证据、旧路径、旧原始行、迁移报告或脱敏摘要。

## 2. 基础报表范围

第一版报表族：

| 报表族 | PC | Web | 手机 |
| --- | --- | --- | --- |
| 收支流水 | 完整筛选、列表、汇总 | 列表和汇总 | 最近摘要 |
| 账户余额 | 账户树、资产负债汇总 | 账户树和余额摘要 | 常用账户摘要 |
| 标签流水 | 标签筛选和列表 | 标签筛选和列表 | 标签摘要后置 |
| 标签资产 | 标签资产汇总 | 基础汇总 | 后置 |
| 基础预算执行 | 预算定义、执行摘要 | 预算列表和摘要 | 当前预算摘要 |
| 财务诊断摘要 | 指标、公式版本和边界状态 | 指标摘要 | 摘要后置 |
| 提醒列表 | 今日提醒、限额提醒、状态 | 提醒列表和状态 | 提醒提示 |
| 投资输入投影 | 已校准输入列表和基础持仓 | 基础列表 | 后置 |

复杂投资成本、收益率和未验证公式不得作为第一版正式报表结论。

## 3. 报表请求与结果

`ReportRequestDto` 字段：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `ledger_id` | 否 | 目标账本 |
| `report_type` | 否 | income_expense、account_balance、tag_entries、tag_assets、budget_summary、reminder_list、investment_inputs |
| `date_from` | 是 | 业务日期起点 |
| `date_to` | 是 | 业务日期终点 |
| `account_ids` | 否 | 账户筛选；为空表示全部有权限账户 |
| `category_ids` | 否 | 分类筛选 |
| `tag_ids` | 否 | 标签筛选 |
| `currency_code` | 是 | 展示币种；为空时按对象原币展示 |
| `limit` | 否 | 列表型报表分页数量 |
| `cursor` | 是 | 列表型报表游标 |

`ReportResultDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `report_id` | 本次报表结果 ID 或请求哈希 |
| `ledger_id` | 目标账本 |
| `report_type` | 报表类型 |
| `filters` | 实际生效筛选 |
| `columns` | 表格列定义 |
| `rows` | 表格行 |
| `summaries` | 汇总数据 |
| `chart_series` | 图表序列；没有时为空 |
| `next_cursor` | 下一页游标 |
| `generated_at` | 生成时间 |
| `formula_status` | verified、input_only、pending_calibration |
| `diagnostic_warnings` | 可选边界提示，例如缺汇率、缺估值、零分母 |
| `drill_targets` | 可选钻取目标，指向新系统对象查询参数 |
| `group_summaries` | 分组小计、页脚合计和趋势汇总 |
| `sort_snapshot` | 实际排序字段、方向和稳定兜底键 |

报表规则：

1. 金额使用最小单位整数和币种代码。
2. 报表必须限定 `ledger_id` 和成员权限。
3. 筛选变化后结果进入 `Dirty`，导出和打印禁用，直到刷新。
4. 报表加载失败返回结构化错误和诊断 ID。
5. 报表结果不得包含旧迁移审计、迁移报告、脱敏摘要、旧路径或旧原始行。
6. 排序必须保存主排序、次排序和稳定兜底键；分页、导出、打印和钻取不得出现重复行或漏行。
7. 分组小计、页脚合计、趋势图和表格行必须来自同一 `ReportResultDto` 快照，不允许图表另走未版本化查询。
8. 报表钻取只能生成新系统查询参数，例如日期范围、账户、分类、标签、投资品或资产 ID；不得把旧 SQL、旧窗体名或旧证据路径作为钻取目标。
9. 精确 SQL、旧报表查询和旧公式样例只能作为 PC 本地校准证据；产品合同只固化可解释的业务口径、输入版本和公式状态。
10. 概况页可用资金图表、资产摘要和预算提醒图表都必须绑定同一账本、业务日期、对象版本和公式状态；布局偏好不能改变图表数据口径。

## 4. 报表页面状态

| 状态 | 说明 | 可用操作 |
| --- | --- | --- |
| `Empty` | 尚未加载或无账本 | 选择账本或筛选 |
| `Loading` | 正在读取 | 取消或等待 |
| `Dirty` | 筛选变化但未刷新 | 刷新 |
| `Ready` | 有结果 | 查看、导出、打印 |
| `ReadyEmpty` | 查询成功但无数据 | 修改筛选 |
| `Failed` | 查询失败 | 重试、查看诊断 |

导出和打印要求：

1. 仅 `Ready` 且有行时启用。
2. `Dirty`、`Loading`、`Failed`、`ReadyEmpty` 状态禁用。
3. 导出、打印和图表使用同一个 `ReportResultDto`。
4. 导出失败不能误报成功。
5. 导出文件必须记录报表类型、筛选快照、排序、数据版本、生成时间、币种口径和公式状态。
6. 打印预览和实际打印必须绑定同一 `ReportResultDto` 快照；筛选或数据版本变化后必须重新生成。
7. PC 本地基于旧程序校准的报表对照证据、旧 SQL 样例、旧打印输出、旧导出样例和脱敏摘要只保存在 PC 本地。
8. Web 导出只能使用 .NET API 返回的新系统报表对象，不读取或保存 PC 本地报表缓存。
9. 手机第一版只展示摘要，不提供完整报表导出或旧格式打印。

报表结果追溯要求：

1. 报表服务必须保留本次查询的逻辑查询 ID、筛选快照和对象版本集合摘要，便于解释导出和打印结果。
2. 报表 SQL、Rust 查询或 .NET 查询实现可以在代码和本地诊断中追溯，但不得把旧库 SQL、旧证据路径或旧原始行写入云端报表结果。
3. 报表公式为 `pending_calibration` 或 `input_only` 时，导出和打印必须显示同等状态，不能在导出中转成正式结论。
4. 钻取打开的列表必须继承来源报表的账本、权限、业务日期范围和对象版本；若数据版本已变化，页面提示刷新后再钻取。
5. 投资收益率、年化收益率、持仓盈亏和可用资金趋势在公式未校准时只能展示 `pending_calibration`、`input_only` 或 `unsupported`。

## 5. 预算需求

第一版预算由 PC/Web 管理，手机展示摘要。

`BudgetDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `budget_id` | 预算 ID |
| `ledger_id` | 所属账本 |
| `name` | 预算名称 |
| `period_kind` | monthly、quarterly、yearly、custom |
| `start_date` | 起始业务日期 |
| `end_date` | 结束业务日期 |
| `status` | draft、active、archived |
| `items` | 预算项 |
| `created_at` | 创建时间 |
| `updated_at` | 更新时间 |

`BudgetItemDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `item_id` | 预算项 ID |
| `category_id` | 分类 |
| `amount_minor` | 预算金额 |
| `currency_code` | 币种 |
| `rollover_mode` | none、carry_remaining、carry_overrun |
| `actual_source_mode` | transaction_facts、manual_adjustment、none |
| `formula_version` | 预算执行率和滚动导入公式版本 |

预算规则：

1. 预算必须属于明确账本。
2. 预算项引用的分类必须属于同一账本。
3. Editor/Owner 可维护预算，Viewer 只读。
4. 手机端只展示当前预算摘要和超支提示，不承担复杂预算配置。
5. 月度、季度、年度和自定义期间必须保存闭区间业务日期、账本时区和期间版本；不能只按页面显示月份推断。
6. 预算实际金额必须从交易事实按分类、业务日期、方向和退款/冲销规则重建，不得直接由前端输入覆盖。
7. 收入执行率、支出执行率和净额执行率必须分开保存公式版本；非零实际收入、零预算、负数和零分母必须返回结构化状态。
8. 父子分类迁移、分类移除、重新加入和父级取消必须返回影响预览，取消零写入，已保存历史预算快照保留。
9. 多币种预算必须保存原币、汇率快照和折算状态；缺汇率时不得把不同币种名义金额相加。
10. 从最近 12 个月导入、复制预算或批量调整额度时必须记录来源期间、选择快照、覆盖策略和逐项错误；失败整体回滚或只提交用户明确选择的有效项。
11. 预算导出使用已刷新报表快照，包含期间、分类范围、公式状态和对象版本；旧预算校准证据只保存在 PC 本地。

## 6. 财务诊断需求

`FinancialDiagnosisRequestDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `ledger_id` | 所属账本 |
| `diagnosis_period` | 诊断业务日期范围 |
| `source_mode` | `auto_statistics`、`manual_input`、`mixed` |
| `account_scope` | 参与资产、负债和现金流统计的账户范围 |
| `valuation_policy` | 投资、保险和重大资产估值口径 |
| `formula_version` | 指标公式版本 |
| `input_version` | 手工输入或自动统计输入版本 |

`FinancialDiagnosisResultDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `diagnosis_result_id` | 诊断结果 ID |
| `ledger_id` | 所属账本 |
| `period_snapshot` | 实际生效日期范围 |
| `metrics` | 指标列表，包含分子、分母、单位、参考区间和结果状态 |
| `warnings` | 缺汇率、缺估值、零分母、负值、阈值端点等提示 |
| `formula_status` | `verified`、`input_only`、`partial`、`pending_calibration` |
| `generated_at` | 生成时间 |

诊断规则：

1. 自动统计日期范围必须明确起止业务日期、账本时区和是否包含当日未结事项；不能由页面当前日期隐式决定。
2. 退款、冲销、转账、内部换汇和资产重分类必须按事实类型进入指标分子或分母，不得只按金额正负推断。
3. 投资、保险、社保、重大资产和外币账户缺估值或缺汇率时，诊断结果标记为 `partial` 或 `pending_calibration`。
4. 零分母、负数、阈值等于边界、极大金额和舍入必须返回可展示状态，不得用异常、NaN 或静默零值进入报表。
5. 手工输入与自动统计混合时必须保存输入来源和版本；重新统计不得覆盖用户手工输入历史。
6. 并发修改账户、交易、估值或手工输入时，诊断结果必须绑定对象版本集合摘要；版本变化后结果进入待刷新。
7. 诊断导出只能包含新系统指标、公式状态和脱敏结果，不得包含旧诊断样例、旧路径、旧原始行、迁移审计、迁移报告或脱敏摘要。

## 7. 提醒与计划需求

第一版提醒和计划先支持基础定义、列表和状态展示；自动执行任务完整闭环后置。

`ReminderDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `reminder_id` | 提醒 ID |
| `ledger_id` | 所属账本 |
| `name` | 提醒名称 |
| `reminder_kind` | due_date、limit、schedule、custom |
| `target_kind` | account、transaction、budget、schedule、manual |
| `target_id` | 目标对象 ID |
| `is_enabled` | 是否启用 |
| `status` | pending、triggered、dismissed、archived |
| `last_triggered_at` | 最近触发时间 |
| `delivery_mode` | in_app、system_notification、none |

`ScheduleDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `schedule_id` | 计划 ID |
| `ledger_id` | 所属账本 |
| `template_id` | 交易模板 ID |
| `name` | 计划名称 |
| `recurrence_json` | 周期定义 |
| `start_date` | 起始日期 |
| `end_date` | 结束日期 |
| `is_auto_post` | 是否自动入账 |
| `status` | active、paused、archived |

提醒和计划规则：

1. PC/Web 可创建、修改、停用和归档提醒。
2. 手机端查看提醒摘要和本机提示。
3. 自动计划执行第一版可以展示配置和待办，但完整后台执行、幂等、重试和失败补偿后置。
4. 已产生实例必须保留审计，不因规则修改而静默删除历史。

## 8. 财务目标需求

第一版财务目标支持基础定义、账户范围和进度摘要。

`FinancialGoalDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `goal_id` | 目标 ID |
| `ledger_id` | 所属账本 |
| `name` | 目标名称 |
| `target_amount_minor` | 目标金额 |
| `currency_code` | 币种 |
| `target_date` | 目标日期 |
| `account_scope_mode` | all、selected |
| `account_ids` | 参与目标的账户 |
| `progress_formula_version` | 进度公式版本 |
| `status` | active、completed、archived |

目标规则：

1. PC/Web 可维护目标。
2. 手机端可查看目标摘要。
3. 目标进度必须说明公式版本，不能隐式使用未校准公式。
4. 标准进度、实际进度和剩余差额必须保存目标金额、当前金额、账户范围、估值策略、汇率快照和舍入规则。
5. 多账户目标必须固定账户选择快照和对象版本；账户关闭、移权、跨账本失效或估值缺失时进入 `partial` 或影响预览。
6. 投资、保险现金价值和重大资产参与目标时，只允许使用已校准估值快照；未校准收益率、损益或现金价值公式不得作为正式完成率。
7. 目标进度达到、超过或低于阈值边界时必须按公式版本返回状态，不能只由 Flutter 前端判断。
8. 删除、归档或修改目标账户范围时必须保留历史进度快照和审计。

## 9. 错误码

| 错误码 | 含义 | 行为 |
| --- | --- | --- |
| `budget_period_invalid` | 预算期间不是有效闭区间 | 阻止保存 |
| `budget_actual_formula_pending` | 预算实际金额或执行率公式未校准 | 标记结果状态 |
| `budget_category_impact_required` | 分类迁移、移除或父级取消需要影响预览 | 返回影响预览 |
| `diagnosis_denominator_zero` | 诊断指标分母为零 | 返回结构化状态 |
| `diagnosis_valuation_missing` | 诊断缺估值或缺汇率 | 标记 `partial` |
| `diagnosis_threshold_boundary` | 指标命中参考区间边界 | 返回明确边界状态 |
| `goal_progress_scope_stale` | 目标账户或估值范围版本过期 | 进入待刷新或冲突解决 |
| `report_drill_version_stale` | 报表钻取时来源结果版本已过期 | 提示刷新后重试 |
| `report_sort_unsupported` | 排序字段不在该报表允许范围 | 返回字段错误 |
| `report_formula_pending` | 报表公式或图表序列未校准 | 标记公式状态 |

错误响应不得包含 PC 完整本地路径、旧 MoneyHome8 原始路径、旧 SQL、旧诊断样例、旧原始行、迁移审计、迁移报告、脱敏摘要、令牌或密码。

## 10. 三端验收

1. PC 能加载至少一页基础列表型报表。
2. Web 能查询账户、流水、预算和提醒基础列表。
3. 手机能查看最近流水、当前预算或提醒摘要。
4. 报表筛选变化后导出和打印不可使用旧结果。
5. Viewer 只能查看报表、预算和提醒，不能修改。
6. 投资复杂公式未校准时结果标记为 `pending_calibration` 或 `input_only`。
7. 自动计划执行完整闭环不作为第一版阻塞项，但对象模型必须保留状态和审计字段。
8. PC/Web 导出和打印必须使用同一个已刷新报表快照，筛选变化后不能复用旧结果。
9. 旧报表校准证据、旧 SQL 样例、旧打印输出、旧导出样例、旧路径和迁移摘要只保存在 PC 本地。
10. 月度、季度、年度和自定义预算都按闭区间业务日期、分类范围、退款/冲销规则和多币种状态计算。
11. 财务诊断自动统计、手工输入和混合输入都返回公式版本、输入版本、边界状态和对象版本集合摘要。
12. 财务目标标准进度、实际进度、舍入和多账户估值口径在 PC/Web 一致；手机只展示摘要。
13. 排序、分组小计、页脚合计、趋势图、导出、打印和钻取都使用同一报表结果快照。
14. 概况页可用资金图表与报表图表共享数据口径、对象版本和公式状态；旧概况图表证据只保存在 PC 本地。

## 11. 当前无需人工确认

本计划没有引入新的产品取舍；它把已确认的基础报表、预算、提醒、计划、财务诊断、财务目标和复杂投资公式后置边界整理成实施需求。
