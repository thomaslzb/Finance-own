# 财务目标与规划输入需求计划

本文档承接 `three-client-requirements-analysis.md`、`reporting-planning-plan.md`、`amount-currency-exchange-rate-plan.md`、`date-time-period-semantics-plan.md`、`schedule-reminder-occurrence-plan.md`、`investment-advanced-assets-calibration-plan.md` 和 `data-retention-deletion-recovery-plan.md`，定义 Finance Own 第一版财务目标、规划输入、进度计算、引用对象处理和三端同步边界。本文只定义需求口径，不固化尚未校准的投资成本、收益率或旧程序公式。

## 1. 目标

1. 支持 PC/Web 创建、修改、停用、归档和查看财务目标。
2. 支持目标账户范围、目标金额、目标日期、币种和进度摘要。
3. 支持规划输入作为预测和提醒的输入对象，而不是把所有预测值写成事实流水。
4. 支持目标进度公式版本、输入版本和结果版本，避免三端展示口径漂移。
5. 支持手机端查看目标摘要、进度状态和同步状态。
6. 支持账户、投资品或预算规则删除/关闭前的引用影响预览。
7. 明确旧 MoneyHome8 目标或规划迁移证据只保存在 PC 本地。

## 2. 非目标

1. 第一版不承诺完整个人理财规划引擎。
2. 第一版不自动给出投资建议、资产配置建议或收益预测承诺。
3. 第一版不把未校准投资收益率、成本批次或保险现金价值公式作为正式目标进度。
4. 第一版不要求手机端承担复杂目标配置、批量重算或冲突解决。
5. 第一版不把旧 MoneyHome8 原始规划数据、迁移审计、迁移报告、脱敏摘要、旧路径或旧原始行上传云端。

## 3. 对象边界

### 3.1 财务目标

`FinancialGoalDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `goal_id` | 目标 ID |
| `ledger_id` | 所属账本；用于多账本隔离 |
| `name` | 目标名称 |
| `description` | 可选说明 |
| `target_amount_minor` | 目标金额，使用最小货币单位 |
| `currency_code` | 目标币种 |
| `target_date` | 目标日期，按账本业务日期解释 |
| `account_scope_mode` | `all`、`selected`、`none` |
| `account_ids` | 参与进度计算的账户范围 |
| `asset_scope_mode` | `none`、`selected_investments`、`selected_assets` |
| `asset_ids` | 参与进度摘要的投资品或高级资产 ID |
| `baseline_amount_minor` | 起始快照金额 |
| `baseline_at` | 起始快照生成时间 |
| `progress_formula_version` | 进度公式版本 |
| `progress_status` | `calculated`、`partial`、`input_only`、`pending_calibration` |
| `status` | `active`、`paused`、`completed`、`archived` |
| `version` | 对象版本 |
| `updated_at` | 最后修改审计时间 |

规则：

1. 目标必须属于明确账本，不允许跨账本引用账户、投资品或预算。
2. 目标金额必须使用整数最小货币单位和明确币种。
3. 目标日期必须是业务日期，不得用同步接收时间替代。
4. 目标进度必须带 `progress_formula_version` 和 `progress_status`。
5. 账户范围为空时只能保存为未开始配置或输入型目标，不能显示为完成。
6. Viewer 只读；Editor 和 Owner 可维护目标基础信息。

### 3.2 规划输入

规划输入用于保存用户明确录入的假设、目标分摊、周期性预算输入和预测参数。

`PlanningInputDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `planning_input_id` | 规划输入 ID |
| `ledger_id` | 所属账本 |
| `source_type` | `manual_assumption`、`budget_link`、`schedule_link`、`goal_allocation`、`legacy_migration` |
| `source_id` | 来源对象 ID |
| `business_period` | 适用账期或日期范围 |
| `currency_code` | 输入币种 |
| `amount_minor` | 输入金额 |
| `calculation_role` | `input_only`、`projection_seed`、`progress_adjustment` |
| `formula_version` | 使用该输入的公式版本 |
| `status` | `active`、`superseded`、`archived` |
| `version` | 对象版本 |

规则：

1. 规划输入不是财务事实，不直接影响账户余额。
2. 规划输入可以参与目标进度、预算预测或提醒摘要，但结果必须标记公式版本。
3. 旧迁移产生的规划输入只写入新系统对象；旧原始证据仍只保存在 PC 本地。
4. 被替代的输入使用 `superseded`，不静默删除历史。
5. 手机端可查看摘要，不承担复杂输入矩阵编辑。

## 4. 进度计算口径

第一版目标进度优先支持可解释、可追溯的简单口径。

| 口径 | 说明 | 结果状态 |
| --- | --- | --- |
| 账户余额汇总 | 选定账户按同一币种或可用汇率快照折算 | `calculated` |
| 起始快照差额 | 当前可计算金额减起始快照 | `calculated` |
| 用户手工输入 | 用户录入当前进度或调整值 | `input_only` |
| 投资输入摘要 | 只展示已校准输入或持仓摘要 | `partial` |
| 未校准投资公式 | 成本、收益率、复杂公司行动未校准 | `pending_calibration` |

规则：

1. 目标进度不能隐式调用未校准投资公式。
2. 多币种目标必须显示汇率快照来源和缺汇率状态。
3. 目标进度结果应保存计算时间、输入版本和公式版本，便于三端一致展示。
4. 目标完成状态不能只靠前端展示推断，必须由本地核心或云端 API 返回明确状态。
5. 进度重算失败不得覆盖上一次成功结果；页面应显示结果时间和错误状态。

## 5. 规划推演口径

`PlanningProjectionScenarioDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `projection_scenario_id` | 推演场景 ID |
| `ledger_id` | 所属账本 |
| `scenario_name` | 场景名称 |
| `base_period` | 起始账期或业务日期 |
| `currency_code` | 推演主币种 |
| `starting_balance_source` | `account_scope`、`manual_input`、`migration_input`、`mixed` |
| `starting_balance_minor` | 起始余额，使用最小货币单位 |
| `inflation_rate_snapshot_id` | 通胀率输入快照 |
| `retirement_rule_snapshot_id` | 退休或收入停止规则快照 |
| `asset_growth_formula_version` | 资产增长公式版本 |
| `installment_expansion_version` | 分期购买展开版本 |
| `projection_status` | `calculated`、`partial`、`input_only`、`pending_calibration`、`overflow` |
| `version` | 场景版本 |

规则：

1. 起始余额必须说明组成来源，至少区分账户范围汇总、手工输入、旧迁移输入和混合输入；混合输入必须展示来源组成。
2. 推演结果不是财务事实，不直接写入账户余额、预算执行额或真实流水。
3. 通胀、退休或收入停止、资产增长、目标投入、分期购买展开和周期费用的计算顺序必须保存为公式版本。
4. 复利、退休年份、资产增长和通胀顺序尚未校准时，推演结果只能标记为 `pending_calibration` 或 `partial`，不能作为正式理财结论。
5. 分期购买跨年份展开时必须区分已入账事实、未来计划期次和纯推演期次；清空或重算推演不得删除真实分期协议和已入账流水。
6. 多币种推演必须保存原币、汇率快照、折算方向和缺汇率状态；缺汇率时不得混合成一个本位币结论。
7. 负值、零分母、极大金额、聚合溢出和小数精度必须返回结构化状态，不得回退为静默零值。
8. 清空规划输入、重置场景或覆盖起始余额必须有明确确认和影响预览；取消、失败或冲突时不得半清空。
9. 旧规划公式、旧原始行、迁移审计、迁移报告、脱敏摘要和旧路径只保存在 PC 本地，不能作为云端推演附件或诊断材料。

## 6. 三端职责

| 能力 | PC | Web | 手机 |
| --- | --- | --- | --- |
| 创建和维护目标 | 支持 | 支持 | 后置 |
| 目标摘要查看 | 支持 | 支持 | 支持 |
| 规划输入维护 | 支持 | 支持 | 后置 |
| 规划推演场景维护 | 支持 | 支持 | 摘要 |
| 目标进度重算 | 支持 | 支持 | 查看云端或本地缓存结果 |
| 复杂引用影响预览 | 支持 | 支持 | 摘要提示 |
| 冲突解决 | 支持 | 支持 | 摘要和稍后处理 |
| 旧目标迁移 | PC 本地支持 | 不支持 | 不支持 |

PC 未登录时可完整使用本地目标和规划输入。Web 必须登录在线使用。手机第一版以摘要、缓存和同步状态为主，不承载复杂配置。

## 7. 引用对象删除与关闭

目标和规划输入可能引用账户、投资品、预算、计划或提醒。第一版必须在删除、关闭、归档或停用被引用对象前返回影响预览。

影响预览字段：

| 字段 | 说明 |
| --- | --- |
| `object_type` | 被处理对象类型 |
| `object_id` | 被处理对象 ID |
| `referenced_by_goals` | 引用该对象的目标列表摘要 |
| `referenced_by_planning_inputs` | 引用该对象的规划输入摘要 |
| `impact_level` | `none`、`display_only`、`calculation_changes`、`blocking` |
| `allowed_actions` | 可选动作列表 |
| `audit_reason_required` | 是否需要操作原因 |

允许动作：

| 动作 | 适用场景 |
| --- | --- |
| `restrict` | 删除会破坏历史或进度计算，阻止该操作 |
| `close_keep_reference` | 关闭账户或资产但保留历史引用 |
| `archive_goal_reference` | 归档目标或输入引用，历史结果保留 |
| `detach_future_projection` | 只解除未来预测引用，不修改历史快照 |
| `cascade_with_review` | 用户审阅影响范围后执行受控级联 |

规则：

1. 有历史流水引用的账户不因目标配置被物理删除。
2. 投资品或高级资产关闭后，历史目标进度继续可追溯；未来进度按引用策略展示缺口或排除。
3. 预算、提醒或计划停用不删除已生成的目标历史快照。
4. 受控级联必须记录操作者、对象、版本、动作和影响摘要。
5. 删除与其它端修改并发时进入冲突解决。

## 8. 同步与冲突

同步规则：

1. 目标、目标账户范围、规划输入、进度快照和引用状态都是新系统对象，可以在用户开启同步后进入云端。
2. 云端保存新系统对象副本和版本，不保存旧 MoneyHome8 原始证据、旧路径、迁移审计、迁移报告、脱敏摘要或 PC 机器环境诊断。
3. PC/Web 并发修改同一目标字段时进入字段级冲突。
4. 一端删除或归档目标，另一端修改目标金额、日期或范围时进入删除修改冲突。
5. 手机离线期间只允许保留摘要缓存或本机草稿；上传失败不得丢弃用户输入。
6. 多账本之间不共享目标、规划输入、进度快照或同步游标。

冲突摘要必须说明对进度、预算、提醒和报表的影响，不得只展示字段差异。

## 9. 审计、隐私与本地保存

审计范围：

1. 创建、修改、停用、归档和恢复目标。
2. 修改目标金额、目标日期、币种、账户范围或公式版本。
3. 新增、替代和归档规划输入。
4. 执行引用对象关闭、删除、归档或受控级联。
5. 发生同步冲突、重算失败或权限阻止。
6. 创建、修改、重算、清空和恢复规划推演场景。

隐私规则：

1. 旧 MoneyHome8 目标、规划或公式迁移证据只保存在 PC 本地。
2. 云端、Web 和手机不得保存或请求旧原始文件、旧路径、旧原始行、旧字段值、迁移审计、迁移报告、脱敏摘要或 PC 机器环境诊断。
3. 目标审计、错误响应和诊断 ID 不得包含完整 PC 本地路径、令牌、密码或旧迁移证据。
4. 导出目标或规划报表时，只能导出新系统对象和可展示的公式状态。

## 10. 错误码

| 错误码 | 含义 | 行为 |
| --- | --- | --- |
| `goal_scope_empty` | 目标范围为空且不能计算 | 保存配置或提示补充范围 |
| `goal_currency_missing_rate` | 多币种目标缺汇率 | 显示缺汇率状态 |
| `goal_formula_pending_calibration` | 公式未校准 | 标记 `pending_calibration` |
| `planning_input_superseded` | 输入已被新版本替代 | 阻止旧版本覆盖 |
| `planning_projection_order_pending` | 推演公式顺序未校准 | 标记 `pending_calibration` |
| `planning_clear_confirmation_required` | 清空规划或覆盖起始余额缺少确认 | 阻止提交并返回影响预览 |
| `planning_projection_overflow` | 推演金额、比例、期数或聚合结果溢出 | 阻止保存或标记 `overflow` |
| `goal_reference_blocking` | 引用关系阻止删除或关闭 | 返回影响预览 |
| `goal_version_conflict` | 目标版本冲突 | 进入冲突解决 |
| `goal_permission_denied` | 当前角色无权修改 | 保留本地草稿或只读展示 |

错误响应不得包含 PC 完整本地路径、旧 MoneyHome8 原始路径、旧原始行、旧字段值、迁移审计、迁移报告、脱敏摘要、令牌或密码。

## 11. 验收场景

1. PC 未登录创建本地目标，选择两个账户后可查看进度摘要。
2. PC 登录并显式开启同步后，目标对象和规划输入作为新系统对象上传云端。
3. Web 登录后查看同一目标，进度公式版本、结果状态和账本币种一致。
4. 手机查看目标摘要，不能进入复杂规划输入维护。
5. 账户关闭前返回目标引用影响预览，历史进度快照保留。
6. 投资品参与目标但公式未校准时，结果显示 `pending_calibration`，不显示正式收益结论。
7. PC/Web 并发修改目标金额和账户范围时进入冲突解决。
8. 删除或归档目标生成对象版本、墓碑或归档状态，并同步到三端。
9. 创建规划推演场景时必须展示起始余额组成、通胀/退休/资产增长/分期展开公式版本和结果状态。
10. 清空规划输入或覆盖起始余额必须二次确认；取消、失败或冲突不得删除真实流水、分期协议或已入账期次。
11. 多币种、负值、零分母、极大金额和缺汇率推演返回结构化状态，不输出静默零值或正式结论。
12. 旧迁移相关审计、报告、脱敏摘要、旧路径和旧原始行只保存在 PC 本地，云端、Web 和手机不得保存或请求。

## 12. 当前无需人工确认

本计划没有引入新的产品取舍；它细化的是已确认的财务目标、规划输入、规划推演、三端同步、多账本隔离、公式校准状态、引用影响预览和旧迁移证据只保存在 PC 本地的边界。
