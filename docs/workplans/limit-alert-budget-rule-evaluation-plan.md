# 限额提醒与预算规则评估需求计划

本文档承接 `reporting-planning-plan.md`、`schedule-reminder-occurrence-plan.md`、`financial-goals-planning-input-plan.md`、`amount-currency-exchange-rate-plan.md`、`runtime-limit-reminder-contract.md` 和 `runtime-budget-contract.md`，定义 Finance Own 第一版限额提醒、预算规则、条件评估、当前告警投影、审计和三端同步边界。本文只定义需求口径，不把旧版未验证的边界语义标记为已兼容。

## 1. 目标

1. 支持账户余额、信用卡透支、证券市价和开放式基金价格四类限额规则。
2. 使用类型化条件表达规则，避免用任意 JSON 解释核心财务边界。
3. 金额和行情价格使用定点数；证券价格保留领域精度，不复制旧列表两位显示造成的数据损失。
4. 规则默认启用，启停、修改、删除和告警重算必须保持版本一致。
5. 当前告警进入今日提醒时固定不可执行、不可跳过。
6. 历史触发审计不可变；删除规则只移除当前告警投影，不删除历史审计。
7. 支持预算引用、目标引用和导出任务引用的影响预览。

## 2. 非目标

1. 第一版不承诺完整行情订阅、实时推送或自动轮询策略。
2. 第一版不承诺所有旧版边界行为完全复刻，例如等于阈值、单侧阈值、停牌、无行情和真实信用卡透支方向。
3. 第一版不把限额告警当作自动入账计划处理。
4. 第一版不让手机端承担复杂规则配置或冲突解决。
5. 第一版不上传旧 MoneyHome8 规则验证过程、迁移审计、迁移报告、脱敏摘要、旧路径或旧原始行。

## 3. 规则对象

`LimitAlertRuleDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `rule_id` | 稳定规则 ID |
| `ledger_id` | 所属账本 |
| `rule_type` | `account_balance`、`credit_overdraft`、`security_price`、`open_fund_price` |
| `target_object_type` | `account`、`security`、`fund` 等目标对象类型 |
| `target_object_id` | 目标对象 ID |
| `condition` | 类型化条件 |
| `condition_version` | 条件版本，修改条件时递增 |
| `enabled` | 是否参与评估 |
| `status` | `active`、`paused`、`archived` |
| `created_at` | 创建审计时间 |
| `updated_at` | 最后修改审计时间 |
| `version` | 对象版本 |

类型化条件：

| 条件 | 字段 | 规则 |
| --- | --- | --- |
| 账户余额 | `currency_code`、`lower_minor`、`upper_minor` | 账户必选；`lower_minor < upper_minor` |
| 信用卡透支 | `currency_code`、`threshold_minor` | 阈值为正数；真实触发方向标记验证状态 |
| 证券市价 | `quote_currency_code`、`lower_price`、`upper_price`、`scale` | `lower_price < upper_price`；保留证券四位或领域要求精度 |
| 开放式基金价格 | `quote_currency_code`、`lower_price`、`upper_price`、`scale` | `lower_price < upper_price`；无行情返回可解释状态 |

规则：

1. 新建规则默认启用。
2. 启停只改变评估资格，不删除规则。
3. 修改条件必须产生新的 `condition_version`。
4. 删除或归档规则必须先处理当前告警投影，并留下审计。
5. 规则目标对象必须属于同一账本。
6. Viewer 只读；Editor 和 Owner 可维护规则。

## 4. 评估输入与快照

`LimitAlertEvaluationInputDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `rule_id` | 规则 ID |
| `condition_version` | 条件版本 |
| `target_snapshot_version` | 账户余额、行情或预算目标快照版本 |
| `observed_value` | 观测金额或价格 |
| `observed_scale` | 观测值精度 |
| `source_status` | `available`、`missing_quote`、`stale_quote`、`account_closed`、`unsupported` |
| `evaluated_at` | 评估时间 |
| `business_date` | 评估归属业务日期 |

规则：

1. 评估器只读取启用规则和同一版本范围内的目标快照。
2. 金额使用最小货币单位；行情价格使用十进制定点值，不使用二进制浮点数。
3. 缺行情、停牌、账户关闭或快照不可用时返回结构化状态，不制造错误告警。
4. 冷启动重建当前告警时必须使用同一规则版本和快照版本。
5. 评估调度策略必须显式配置为冷启动、保存后即时评估、手动刷新或后台任务之一；未实现的策略不得写入发布说明。

## 5. 告警投影

`LimitAlertOccurrenceDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `alert_id` | 告警实例 ID |
| `rule_id` | 来源规则 |
| `ledger_id` | 所属账本 |
| `trigger_key` | 幂等触发键 |
| `condition_snapshot` | 条件快照 |
| `observed_value` | 触发时观测值 |
| `delta_value` | 与边界的差额 |
| `boundary_kind` | `lower`、`upper`、`threshold` |
| `show_in_today_inbox` | 是否进入今日提醒 |
| `can_execute` | 固定为 `false` |
| `can_skip` | 固定为 `false` |
| `status` | `current`、`resolved`、`suppressed`、`archived` |
| `evaluated_at` | 评估时间 |

触发键至少包含：

```text
rule_id + condition_version + target_snapshot_version + boundary_kind
```

规则：

1. 页面刷新、冷启动或重试不能重复生成同一当前告警。
2. 当前告警视图只展示仍有效且当前越界的规则。
3. 停用或删除规则后，当前告警从今日提醒移除。
4. 历史触发审计不能因规则停用、修改或删除被改写。
5. 限额告警不是可执行计划，不能出现执行、跳过或自动入账能力。

## 6. 预算规则交互

预算相关规则用于提示预算执行状态，不直接修改预算额度或交易事实。

第一版预算规则边界：

1. 预算实际金额必须由交易事实按账本、业务期间、分类、方向、币种和汇率快照重建。
2. 预算超支、接近上限或无预算发生额可以生成提示，但提示结果必须引用预算版本和查询期间。
3. 修改预算分类范围、十二个月额度、导入结果或复制结果时，应递增预算版本。
4. 删除或修改被提醒、规划、导出任务引用的预算时必须返回影响预览。
5. 预算实际支出缓存不得成为第二套财务事实。

预算提示进入今日提醒时也固定 `can_execute=false`、`can_skip=false`，只能查看详情、调整预算或停用提示规则。

## 7. 引用与删除

限额规则可能引用账户、信用卡、证券、基金、预算、目标或规划输入。处理被引用对象前必须返回影响预览。

影响预览字段：

| 字段 | 说明 |
| --- | --- |
| `object_type` | 被处理对象类型 |
| `object_id` | 被处理对象 ID |
| `referenced_by_rules` | 引用该对象的限额规则摘要 |
| `referenced_by_budgets` | 预算或预算提示引用摘要 |
| `referenced_by_goals` | 目标引用摘要 |
| `current_alert_count` | 当前告警数量 |
| `allowed_actions` | 可执行动作 |
| `impact_level` | `none`、`display_only`、`calculation_changes`、`blocking` |

允许动作：

| 动作 | 适用场景 |
| --- | --- |
| `restrict` | 删除会造成孤儿规则或不可解释历史 |
| `close_keep_history` | 关闭对象并保留历史规则与审计 |
| `pause_related_rules` | 停用相关规则并保留审计 |
| `archive_related_rules` | 归档相关规则 |
| `cascade_with_review` | 用户审阅影响范围后执行受控级联 |

规则：

1. 不得留下孤儿规则。
2. 账户或投资品关闭不删除历史触发审计。
3. 受控级联必须在一个命令内处理规则、当前告警和审计。
4. 删除与其它端修改并发时进入冲突解决。

## 8. 三端职责

| 能力 | PC | Web | 手机 |
| --- | --- | --- | --- |
| 创建和维护限额规则 | 支持 | 支持 | 后置 |
| 当前告警列表 | 支持 | 支持 | 摘要提示 |
| 今日提醒投影 | 支持 | 支持 | 摘要提示 |
| 规则评估 | 本地核心支持 | 云端 API 支持 | 读取云端或缓存结果 |
| 引用影响预览 | 支持 | 支持 | 摘要提示 |
| 冲突解决 | 支持 | 支持 | 摘要和稍后处理 |
| 旧规则迁移验证 | PC 本地支持 | 不支持 | 不支持 |

PC 未登录时可完整维护本地限额规则。Web 在线使用云端对象副本。手机只展示摘要、通知和同步状态，不承担复杂条件编辑。

## 9. 同步、冲突与审计

同步规则：

1. 限额规则、当前告警投影、历史触发审计和预算提示状态都是新系统对象或派生投影。
2. 云端只保存新系统对象副本，不保存旧 MoneyHome8 原始验证证据。
3. 规则条件并发修改进入字段级冲突。
4. 一端停用或删除规则，另一端修改条件或目标对象时进入删除修改冲突。
5. 手机离线只保留摘要缓存或本机草稿；上传失败不得丢弃用户输入。

审计必须记录：

1. 创建、修改、启用、停用、删除和归档规则。
2. 触发、解除、抑制和归档当前告警。
3. 预算提示规则的版本、期间和来源快照。
4. 引用对象关闭、删除、归档或受控级联。
5. 评估失败、重试、冲突和权限阻止。

审计不得包含密码、令牌、PC 完整本地路径、旧 MoneyHome8 原始行、旧字段值、迁移审计、迁移报告、脱敏摘要或 PC 机器环境诊断。

## 10. 错误码

| 错误码 | 含义 | 行为 |
| --- | --- | --- |
| `limit_condition_invalid_range` | 下限不小于上限 | 阻止保存并映射字段错误 |
| `limit_condition_missing_target` | 缺少目标账户、证券或基金 | 阻止保存 |
| `limit_quote_missing` | 行情缺失 | 显示缺行情状态，不生成错误告警 |
| `limit_snapshot_stale` | 快照版本过旧 | 要求刷新或重新评估 |
| `limit_trigger_replay` | 幂等触发重放 | 返回原告警结果 |
| `limit_rule_reference_blocking` | 引用关系阻止删除或关闭 | 返回影响预览 |
| `budget_projection_incomplete` | 预算实际投影不完整 | 标记结果不完整 |
| `limit_rule_version_conflict` | 规则版本冲突 | 进入冲突解决 |

错误响应不得包含 PC 完整本地路径、旧 MoneyHome8 原始路径、旧原始行、旧字段值、迁移审计、迁移报告、脱敏摘要、令牌或密码。

## 11. 验收场景

1. PC 创建账户余额规则，`lower < upper` 校验通过后默认启用。
2. 输入下限不小于上限时，PC/Web 返回字段错误，不保存规则。
3. 证券价格规则保存四位或领域要求精度，列表两位显示不造成数据截断。
4. 冷启动评估同一规则和快照不会重复生成告警。
5. 限额告警进入今日提醒后，`can_execute=false` 且 `can_skip=false`。
6. 停用规则后当前告警消失，历史触发审计仍可追溯。
7. 删除证券或账户前返回限额规则、目标和预算引用影响预览。
8. Web 修改规则条件、PC 同时停用规则时进入冲突解决。
9. 手机仅展示限额提醒摘要和同步状态，不显示复杂条件编辑入口。
10. 旧迁移相关验证证据、迁移审计、迁移报告、脱敏摘要、旧路径和旧原始行只保存在 PC 本地。

## 12. 当前无需人工确认

本计划没有引入新的产品取舍；它细化的是已确认的限额提醒、预算提示、今日提醒投影、定点金额与行情价格、幂等评估、引用影响预览、三端职责和旧迁移证据 PC 本地保存边界。
