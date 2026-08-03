# 财务计算器与价格整理需求计划

本文档承接 `three-client-requirements-analysis.md`、`shared-ui-ai-diagnostics-automation-plan.md`、`amount-currency-exchange-rate-plan.md`、`market-instruments-trading-valuation-plan.md`、`deposits-debts-credit-amortization-plan.md`、`data-retention-deletion-recovery-plan.md`、`runtime-ai-console-calculator-contract.md`、`runtime-shared-ui-contract.md`、`feature-catalog.md` 和 `acceptance-criteria.md`，定义 Finance Own 第一版财务计算器、公式版本、计算结果回填、价格整理预览和高风险删除边界。本文只定义新系统需求口径，不把尚未校准的旧版 19 类财务计算公式、价格删除边界或账单日短月份规则标记为已兼容。

## 1. 目标

1. 支持 PC/Web 使用财务计算器进行存款、贷款、证券和其它辅助计算。
2. 保证计算器结果默认只作为预览或草稿输入，不直接生成账务分录。
3. 为每类公式保存公式标识、公式版本、输入快照、舍入规则、输出结果和校准状态。
4. 支持价格整理前展示价格类型、对象数、记录数、日期范围和影响预览。
5. 支持净价/清洁价格计算作为证券类或债券类计算器结果回填债券交易草稿。
6. 保证旧 MoneyHome8 计算器、价格整理和自动化证据只保存在 PC 本地。

## 2. 非目标

1. 第一版不承诺旧版 19 类财务计算器公式全部完全兼容。
2. 第一版不允许计算器直接提交交易、计划、投资持仓或账单。
3. 第一版不允许价格整理无预览批量删除。
4. 第一版不在手机端提供完整财务计算器和价格整理。
5. 第一版不上传旧公式校准样例、旧路径、旧原始行、迁移审计、迁移报告或脱敏摘要。

## 3. 财务计算器范围

旧版已确认四大类共 19 类财务计算器：

| 类别 | 第一版处理 |
| --- | --- |
| 存款类 | PC/Web 提供输入、预览和公式状态 |
| 贷款类 | PC/Web 提供输入、预览和公式状态 |
| 证券类 | PC/Web 提供输入、预览、净价/清洁价格计算和公式状态 |
| 其它类 | PC/Web 提供输入、预览和公式状态 |

规则：

1. 每个计算器必须有稳定 `calculator_type`。
2. 每次计算必须产生 `calculation_session_id`，用于草稿回填和审计追溯。
3. 公式未校准时，结果标记为 `pending_calibration` 或 `input_only`，不能作为正式报表结论。
4. 金额使用定点十进制或最小单位整数，不使用二进制浮点作为财务结果。
5. 结果回填到业务草稿时，必须由宿主页面明确接收，不能绕过宿主校验直接入账。

### 3.1 净价/清洁价格计算

净价/清洁价格计算作为 `calculator_type=bond_clean_dirty_price` 或等价稳定类型处理。

输入字段至少包括：

| 字段 | 说明 |
| --- | --- |
| `bond_id` | 可选债券稳定 ID，用于带入票面规则 |
| `trade_date` | 成交业务日期 |
| `settlement_date` | 结算业务日期 |
| `face_value_minor` | 面值 |
| `coupon_rate` | 票面利率定点值 |
| `clean_price` | 净价，可为空 |
| `dirty_price` | 全价，可为空 |
| `accrued_interest_minor` | 应计利息，可为空 |
| `quantity` | 数量 |
| `rounding_mode` | 舍入规则 |

规则：

1. 净价、全价和应计利息至少应能在给定足够输入时互相推导，但公式未校准时结果标记为 `pending_calibration`。
2. 计算结果只能回填债券买入、卖出、到期或提前兑取草稿的价格字段。
3. 回填后仍由债券交易命令校验资金账户、费用、数量、币种和分录平衡。
4. 取消计算器不改变宿主草稿。
5. 旧净价计算样例、旧路径、旧原始行、迁移审计、迁移报告和脱敏摘要只保存在 PC 本地。

## 4. 计算会话对象

`FinancialCalculationSessionDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `calculation_session_id` | 计算会话 ID |
| `ledger_id` | 可选账本 ID |
| `calculator_type` | 计算器类型 |
| `formula_id` | 公式 ID |
| `formula_version` | 公式版本 |
| `input_snapshot_json` | 输入快照 |
| `rounding_mode` | 舍入规则 |
| `result_json` | 输出结果 |
| `calibration_status` | `verified`、`input_only`、`pending_calibration`、`unsupported` |
| `created_at` | 计算时间 |
| `accepted_by_command_id` | 被业务草稿接收时的命令 ID |

隐私规则：

1. 输入快照不得包含密码、令牌、完整 PC 本地路径、旧原始行或敏感证件号。
2. 云端只同步用户确认保存的新系统计算快照；旧公式校准证据只保存在 PC 本地。
3. 未被业务对象接收的临时计算会话可按设备本地缓存策略清理。

## 5. 价格整理范围

价格整理涉及股票、基金、贵金属和币种汇率等价格数据。

`PriceMaintenancePreviewDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `preview_id` | 预览 ID |
| `ledger_id` | 账本 ID |
| `price_kinds` | 股票、基金、贵金属、币种汇率 |
| `date_mode` | 指定日期前、日期区间、未交易对象 |
| `date_from` | 起始日期 |
| `date_to` | 结束日期 |
| `object_count` | 受影响对象数 |
| `price_record_count` | 受影响价格记录数 |
| `protected_record_count` | 被交易、持仓、报表快照或同步版本保护的记录数 |
| `can_execute` | 是否可执行 |
| `blocked_reasons` | 阻断原因 |

规则：

1. 执行前必须生成预览，列出价格类型、对象数、记录数和保护原因。
2. 用户确认后才允许进入删除事务。
3. 删除必须单事务执行，失败整体回滚。
4. 被交易、持仓、估值快照、报表冻结或同步版本引用的价格不得被无提示物理删除。
5. 删除结果必须刷新价格列表、持仓估值、报表状态和审计记录。
6. 大范围价格整理属于高风险命令，必须二次确认。

## 6. 三端职责

| 能力 | PC | Web | 手机 |
| --- | --- | --- | --- |
| 财务计算器目录 | 支持 | 支持 | 摘要后置 |
| 公式输入和预览 | 支持 | 支持 | 后置 |
| 结果回填业务草稿 | 支持 | 支持 | 后置 |
| 价格整理预览 | 支持 | 支持受限 |
| 价格整理执行 | 支持 | Owner/Editor 受控执行 | 不支持 |
| 旧公式校准证据 | PC 本地支持 | 不支持 | 不支持 |

## 7. 同步与冲突

1. 已被业务对象接收的计算快照作为新系统对象的一部分同步。
2. 未被接收的临时计算会话默认不进入云端。
3. 价格整理命令同步为新系统审计、价格墓碑或版本结果，不同步旧自动化证据。
4. PC/Web 可处理价格整理与新价格录入、行情导入之间的版本冲突。
5. 手机只显示价格数据状态，不执行价格整理。

## 8. 错误模型

| 错误码 | 场景 | 处理 |
| --- | --- | --- |
| `financial_calculator_unsupported` | 计算器类型未支持 | 显示不可用 |
| `financial_formula_pending_calibration` | 公式未校准 | 返回结果但标记状态 |
| `financial_calculation_input_invalid` | 输入不合法 | 保留草稿并定位字段 |
| `financial_calculation_not_posting` | 尝试直接入账 | 阻止并提示必须回到宿主命令 |
| `price_cleanup_preview_required` | 未预览直接执行 | 阻止执行 |
| `price_cleanup_protected_records` | 存在受保护价格记录 | 阻止或要求缩小范围 |
| `price_cleanup_version_conflict` | 价格版本冲突 | 重新生成预览 |
| `price_cleanup_permission_denied` | 权限不足 | 阻止执行 |

## 9. 验收场景

1. 打开任一财务计算器，输入合法值后返回公式版本、输入快照、舍入规则、结果和校准状态。
2. 公式未校准时，结果可展示但不能作为正式报表结论。
3. 计算结果只有用户明确接受时才回填宿主草稿；取消不改变宿主草稿。
4. 计算器不得直接生成交易、计划、投资持仓、信用账单或报表冻结结果。
5. 净价/清洁价格计算只回填债券交易草稿的净价、全价或应计利息字段，不能直接生成债券交易或资金分录。
6. 执行价格整理前必须展示价格类型、对象数、记录数、保护记录数和二次确认。
7. 取消价格整理不改变价格记录、持仓估值或报表。
8. 删除执行失败时整体回滚，价格列表、持仓估值和报表状态保持旧版本。
9. 旧公式校准证据、旧净价计算证据、旧价格整理证据、迁移审计、迁移报告、脱敏摘要、旧路径和旧原始行只保存在 PC 本地。

## 10. 当前无需人工确认

本计划没有引入新的产品取舍；它细化的是已确认的财务计算器、公式校准状态、价格整理预览、高风险删除、三端职责、同步冲突和旧迁移证据 PC 本地保存边界。
