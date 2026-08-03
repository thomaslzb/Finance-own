# 证券、基金、债券与融资融券需求计划

本文档承接 `three-client-requirements-analysis.md`、`investment-advanced-assets-calibration-plan.md`、`amount-currency-exchange-rate-plan.md`、`limit-alert-budget-rule-evaluation-plan.md`、`runtime-investment-shared-projections-contract.md`、`runtime-securities-ledger-and-valuation-contract.md`、`runtime-open-and-money-market-funds-contract.md`、`runtime-bonds-ledger-and-maturity-contract.md` 和 `runtime-margin-financing-contract.md`，定义 Finance Own 第一版上市证券、开放式基金、货币基金、债券、融资融券、费率、净值、估值、成本批次、合同和风险投影的需求边界。本文只定义需求口径，不把未校准的费用、份额、净价、全价、应计利息、保证金或风险公式标记为已兼容。

## 1. 目标

1. 支持证券、基金、债券和融资融券对象使用稳定身份，不用当前代码或名称作为长期主键。
2. 支持交易事实、费用快照、资金分录、份额或数量批次、成本批次、估值批次和审计分离。
3. 支持 PC/Web 完整维护基础输入、查询和冲突解决，手机端摘要查看。
4. 支持未校准公式用 `input_only`、`pending_calibration` 或 `unsupported` 状态表达。
5. 支持旧迁移证据只保存在 PC 本地，云端只接收新系统对象和校准状态。

## 2. 非目标

1. 第一版不承诺自动券商、基金公司、银行、行情或融资融券接口完整闭环。
2. 第一版不承诺全部费用、税费、份额、成本、收益率、净价全价、票息、保证金和强平公式兼容旧版。
3. 第一版不在手机端提供复杂证券、基金、债券或融资融券交易录入。
4. 第一版不把行情、净值、费率或风险指标缺失时的结果静默按零处理。
5. 第一版不上传旧 MoneyHome8 原始交易、旧路径、旧原始行、迁移审计、迁移报告或脱敏摘要。

## 3. 统一对象边界

统一对象族：

| 对象族 | 用途 |
| --- | --- |
| `TradableInstrument` | 证券、基金、债券等稳定工具身份 |
| `InstrumentCodeHistory` | 代码、市场、有效期和变更审计 |
| `TradingAccount` | 证券、基金、债券或融资融券账户 |
| `TradeInput` | 买入、卖出、申购、赎回、转换、到期、偿还等交易输入 |
| `FeeSnapshot` | 每笔交易实际采用的费率、来源、单位和版本 |
| `LotAllocation` | 数量、份额或成本批次分配 |
| `QuoteOrNavInput` | 行情、净值、债券价格和批次 |
| `ValuationSnapshot` | 同一估值边界下的市值、成本和盈亏投影 |
| `IpoApplicationFlow` | 新股申购、冻结资金、中签、返款和结清状态机 |
| `MarketDataUpdateBatch` | 行情、净值、汇率或历史价格更新批次 |
| `LegacyInstrumentMap` | 旧 ID、旧代码和迁移诊断映射，仅 PC 本地 |

规则：

1. 证券、基金和债券代码不是主键；代码变更必须保留有效期和审计。
2. 交易保存时冻结实际采用的费率、净值、价格、汇率和规则版本。
3. 交易事实、资金分录、数量或份额变化、成本批次和审计必须同事务提交。
4. 查询投影可重建，不作为唯一业务事实。
5. 删除被历史交易、行情、持仓或计划引用的工具时，优先停用、归档或保留版本，不做物理删除。
6. 证券、基金或货币基金代码转换只能追加代码历史和迁移映射，不得重写稳定工具 ID。

## 4. 上市证券

`SecurityTradeDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `trade_id` | 交易 ID |
| `ledger_id` | 所属账本 |
| `security_id` | 稳定证券 ID |
| `account_id` | 证券账户 |
| `trade_type` | `buy`、`sell`、`ipo_apply`、`ipo_allot`、`refund`、`rights_issue`、`bonus_share`、`cash_dividend`、`adjustment` |
| `trade_date` | 成交业务日期 |
| `quantity` | 数量定点值 |
| `price` | 成交价格定点值 |
| `currency_code` | 币种 |
| `fee_snapshot_id` | 费用快照 |
| `cash_flow_minor` | 资金流金额 |
| `calibration_status` | 校准状态 |
| `version` | 对象版本 |

规则：

1. 全局费率是新账户模板，不是所有账户的实时引用。
2. 创建账户时复制版本化账户费率；后续修改全局模板不改变已有账户。
3. 每笔证券交易保存计算输入、分项费用、舍入规则、币种和费率快照。
4. 买入创建数量、成本批次和资金流；卖出关闭可用数量并分配成本。
5. 送股、缩股、现金红利、配股、新股申购、中签和退款使用独立事件类型和稳定关系 ID。
6. 缺行情、停牌、零价格、跨币种或昨日价格缺失必须显示明确状态。

### 4.1 证券代码转换和新股关联

`InstrumentCodeConversionDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `conversion_id` | 代码转换记录 ID |
| `ledger_id` | 所属账本 |
| `instrument_id` | 稳定工具 ID |
| `old_code` | 原代码 |
| `new_code` | 新代码 |
| `market` | 市场 |
| `effective_date` | 生效业务日期 |
| `reason` | 变更原因 |
| `affected_trade_count` | 影响的历史交易数量 |
| `version` | 版本 |

代码转换规则：

1. 历史交易、持仓、行情和成本批次继续引用 `instrument_id`。
2. 新代码只改变后续展示、检索和导入匹配优先级。
3. 同一市场同一生效区间内不能出现冲突代码。
4. 导入交割单批量修改证券代码时，必须生成预览并保留原始导入行的 PC 本地来源映射。
5. 旧代码转换证据、旧路径、旧原始行、迁移审计、迁移报告和脱敏摘要只保存在 PC 本地。

`IpoApplicationFlowDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `ipo_flow_id` | 新股流程稳定 ID |
| `ledger_id` | 所属账本 |
| `security_id` | 申购证券稳定 ID |
| `cash_account_id` | 冻结或返款资金账户 |
| `securities_account_id` | 证券账户 |
| `apply_trade_id` | 申购交易 ID |
| `allot_trade_id` | 中签交易 ID，可为空 |
| `refund_trade_id` | 返款交易 ID，可为空 |
| `status` | applied、not_allotted、partially_allotted、allotted、refunded、settled |
| `version` | 流程版本 |

新股流程规则：

1. 新股申购、中签确认和返款必须引用同一 `ipo_flow_id`。
2. 未中签、普通中签、部分中签、可分离债中签和结清是流程状态，不是孤立备注。
3. 冻结资金、返款、证券持仓和费用必须原子提交或可幂等恢复。
4. 导入交割单关联新股申购时，必须引用已存在或同批创建的申购记录；无法匹配时保留为导入行处理状态，不伪造关联。
5. 取消关联只影响导入预览或未提交关系，不能删除已入账交易事实。

## 5. 开放式基金与货币基金

`FundTradeDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `fund_trade_id` | 基金交易 ID |
| `ledger_id` | 所属账本 |
| `fund_id` | 稳定基金 ID |
| `fund_kind` | `open_ended`、`money_market` |
| `account_id` | 基金账户 |
| `trade_type` | 申购、赎回、转换、现金红利、分红再投资、认购、确认、拆分 |
| `trade_date` | 业务日期 |
| `gross_amount_minor` | 申购或赎回毛额 |
| `fee_minor` | 费用 |
| `confirmed_nav` | 确认净值，可为空 |
| `confirmed_units` | 确认份额 |
| `cost_minor` | 成本输入或结果 |
| `calibration_status` | 校准状态 |
| `version` | 对象版本 |

规则：

1. 开放式基金和货币基金可共享账户基础设施，但必须使用不同产品策略。
2. 开放式基金成交快照和当前估值快照必须分开保存。
3. 货币基金不得被强迫使用开放式基金净值字段猜测份额或收益。
4. 基金转换是原子复合命令，来源扣减、目标增加、费用、收益和审计同事务提交。
5. 认购、中签、返款、分红与再投资通过稳定关系 ID 关联，不依赖行号或备注文本。
6. 缺净值、净值日期落后、跨币种、零份额、负份额和并发更新必须显示明确状态。
7. 开放式基金必须区分前端收费、后端收费、申购费、赎回费、转换费和销售服务费来源；费用快照保存费率来源、适用规则和舍入口径。
8. 申购、赎回和转换必须保存真实金额、确认份额、确认净值、确认日期、资金账户、费用和在途状态；未确认份额不得进入正式持仓。
9. 货币基金面值、收益结转、赎回利息、资金在途和未结转收益必须使用货币基金策略，不得套用开放式基金净值公式。
10. 基金拆分必须保存拆分比例方向、零碎份额处理、成本重分配和历史净值调整范围；取消或失败不得改写原份额批次。

## 6. 债券

`BondTradeDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `bond_trade_id` | 债券交易 ID |
| `ledger_id` | 所属账本 |
| `bond_id` | 稳定债券 ID |
| `account_id` | 债券账户或证券账户 |
| `trade_type` | `buy`、`sell`、`coupon`、`maturity`、`early_redemption`、`adjustment` |
| `price_basis` | `clean`、`dirty` |
| `clean_price` | 净价 |
| `accrued_interest_minor` | 应计利息 |
| `quantity` | 数量 |
| `face_value_minor` | 面值 |
| `fee_minor` | 费用 |
| `cash_flow_minor` | 资金流金额 |
| `calibration_status` | 校准状态 |
| `version` | 对象版本 |

规则：

1. 债券目录保存发行人、发行日、到期日、票面利率、付息日、面值和免税状态。
2. 买入、卖出、到期和提前兑取必须明确净价、全价、应计利息、费用和资金账户。
3. 购入应计利息、卖出应计利息、票息收入和税费必须分开记账。
4. 正常到期、提前兑取和市场卖出是不同终止事件。
5. 净价/清洁价格计算器结果只能回填债券交易草稿，最终入账仍由债券交易命令校验。
6. 缺行情、过期行情、到期未处理、负持仓、零面值、跨币种和部分兑付必须显示明确状态。
7. 正常到期和提前兑取必须拆分本金、票息、溢折价、费用、税务、免税标志和状态迁移；净额不能替代分项事实。
8. 债券利息支付是独立事件，必须引用债券、持仓批次、付息日和免税状态；失败回滚不得改变持仓本金或成本批次。
9. 债券资料被交易引用后，发行人、票面、付息日、到期日和免税规则修改必须进入版本化或影响预览，不能原位覆盖历史交易口径。

## 7. 融资融券

`MarginContractDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `margin_contract_id` | 融资或融券合同 ID |
| `ledger_id` | 所属账本 |
| `margin_account_id` | 融资融券账户 |
| `contract_type` | `financing`、`securities_lending` |
| `contract_no` | 外部合同号 |
| `instrument_id` | 相关证券 |
| `principal_minor` | 融资本金，融资合同使用 |
| `quantity` | 融券数量，融券合同使用 |
| `remaining_principal_minor` | 未偿本金 |
| `remaining_quantity` | 未偿数量 |
| `annual_rate` | 年利率 |
| `effective_date` | 生效日期 |
| `maturity_date` | 到期日期 |
| `status` | `open`、`partially_repaid`、`closed`、`archived` |
| `version` | 对象版本 |

规则：

1. 融资买入和融券卖出完成时原子创建交易、合同、现金或证券分录。
2. 融资合同使用货币金额，融券合同使用证券数量，不能用无单位数值统一处理。
3. 单合同偿还和批量偿还是不同命令；二者必须有不同入口、参数和审计。
4. 偿还本金或数量、利息和费用分别保存；净额不能替代分项事实。
5. 担保物市值、融资负债、融券负债、可用资金和风险指标必须来自同一估值时点。
6. 风险指标和强平条件在公式校准前保持 `pending_calibration` 或 `unsupported`。
7. 融资买入、融券卖出、卖券还款、买券还券、直接偿还、批量偿还和担保物划转必须使用不同命令类型和审计口径。
8. 批量偿还候选必须按账户、合同状态、剩余本金或剩余数量、证券身份、权限和估值日期筛选；候选为空时只返回阻断原因，不生成空批次交易。
9. 超额偿还、超量还券、资金不足、可用数量不足和合同版本冲突必须拒绝并保留草稿；幂等重试不得重复减少合同余额。
10. 担保物划转必须保存担保物身份、数量、估值快照、转入/转出方向和风险投影影响；风险公式未校准时只展示结构化状态。

## 8. 估值与查询

估值引用字段：

| 字段 | 说明 |
| --- | --- |
| `ledger_revision` | 账本修订 |
| `price_batch_id` | 价格或行情批次 |
| `nav_batch_id` | 基金净值批次 |
| `fx_batch_id` | 汇率批次 |
| `valued_at` | 估值时间 |
| `reporting_currency` | 展示币种 |

规则：

1. 同一估值引用驱动持仓列表、页脚、市值构成、历史盈亏、导出和打印。
2. 行情、净值或债券价格先进入暂存批次，整批校验成功后发布。
3. 估值失败不得覆盖上一次成功结果；页面展示失败原因和结果时间。
4. 查询筛选、列表、页脚、图表、导出和打印必须共享同一查询快照。
5. 查询组件不得直接修改交易、持仓、合同或行情事实。

### 8.1 行情更新批次

行情更新包含证券、基金、贵金属、外汇汇率和历史价格来源。第一版只定义安全批次边界，不承诺旧版全部行情源协议兼容。

`MarketDataUpdateBatchDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `market_data_batch_id` | 更新批次 ID |
| `ledger_id` | 所属账本 |
| `source_kind` | quote、nav、fx_rate、precious_metal、history_price |
| `source_provider_id` | 受控来源 ID |
| `scope` | 当前持仓、全部交易过对象、指定列表或日期范围 |
| `date_from` | 历史价格起始日期，可为空 |
| `date_to` | 历史价格结束日期，可为空 |
| `state` | previewed、fetching、validated、publishing、published、partial_failed、failed、cancelled |
| `success_count` | 成功记录数 |
| `failed_count` | 失败记录数 |
| `skipped_count` | 因无权限、无标的、重复或已是最新而跳过的记录数 |
| `retry_count` | 批次级重试次数 |
| `provider_protocol_version` | 受控供应商适配器版本 |
| `challenge_state` | none、required、resolved、failed、unsupported |
| `publish_policy` | all_or_nothing、valid_records_only、preview_only |
| `rollback_snapshot_id` | 发布前快照或恢复引用 |
| `version` | 批次版本 |

`MarketDataUpdateItemDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `item_id` | 批次内记录 ID |
| `instrument_id` | 新系统稳定工具 ID |
| `quote_date` | 行情、净值、汇率或历史价格日期 |
| `price_kind` | latest_quote、history_quote、nav、fx_rate、fee_rate、deposit_rate |
| `raw_value_state` | parsed、missing、invalid、out_of_range、stale、duplicate |
| `normalized_price` | 定点价格或净值；无效时为空 |
| `currency_code` | 标的币种 |
| `source_timestamp` | 来源返回时间；无则为空 |
| `item_state` | valid、skipped、failed、published |
| `failure_code` | 行级失败原因 |

规则：

1. 行情更新必须先进入暂存批次，整批校验成功后发布。
2. 用户中止或网络失败不得发布半批次，也不得覆盖上一次成功估值。
3. 来源协议、供应商凭据和验证码挑战不得进入财务对象、导出、普通日志或支持包。
4. 外汇牌价、证券行情、基金净值和历史价格使用同一批次审计结构，但各自校验规则独立。
5. 旧行情更新页面证据、旧来源协议诊断、旧路径、旧原始行、迁移审计、迁移报告和脱敏摘要只保存在 PC 本地。
6. 九类最新来源和七类历史来源必须作为受控 `source_provider_id + provider_protocol_version` 管理；旧 HTTP、旧签名、验证码挑战和供应商凭据不得硬编码进 Flutter、.NET 或 Rust 领域层。
7. 历史区间必须校验闭区间日期、账本时区、最大跨度、节假日或无交易日结果；无数据不是成功价格，也不是零价格。
8. 部分失败批次默认不得发布；若用户选择 `valid_records_only`，必须展示失败项、跳过项、将发布项和对估值/报表的影响。
9. 重试必须复用同一批次或显式创建重试批次，保留来源、范围、失败项和幂等键；重复重试不得生成重复价格。
10. 批次发布后，持仓列表、趋势图、限额提醒、财务诊断、报表导出和打印必须引用同一发布版本。
11. 旧参考库或旧程序缓存只能作为 PC 本地校准输入；不得把新系统成功批次回写到旧参考库或旧缓存文件。
12. 存款利率、交易费率和行情价格都必须记录来源、单位、scale、适用日期和发布版本；来源缺失时显示 `pending_source`，不得猜测供应商。

## 9. 三端职责

| 能力 | PC | Web | 手机 |
| --- | --- | --- | --- |
| 证券基础输入 | 支持 | 支持 | 摘要 |
| 基金基础输入 | 支持 | 支持 | 摘要 |
| 债券基础输入 | 支持 | 支持 | 摘要 |
| 融资融券输入 | 支持 | 支持 | 摘要 |
| 行情、净值和费率维护 | 支持 | 支持 | 后置或摘要 |
| 复杂交易录入 | 支持 | 部分支持 | 后置 |
| 冲突解决 | 支持 | 支持 | 摘要和稍后处理 |
| 旧数据迁移 | PC 本地支持 | 不支持 | 不支持 |

PC 未登录时可完整维护本地对象。Web 在线使用云端对象副本。手机只展示摘要、校准状态、通知和同步状态。

## 10. 同步、冲突与审计

同步规则：

1. 稳定工具身份、账户、交易输入、费率快照、净值行情批次、估值结果、成本批次和融资合同作为新系统对象同步。
2. 云端不保存旧 MoneyHome8 原始交易、旧路径、旧原始行、旧字段值、迁移审计、迁移报告或脱敏摘要。
3. 并发修改同一交易、费率模板、行情批次、净值批次、债券主数据或融资合同进入冲突解决。
4. 手机离线只保留摘要缓存或本机草稿；上传失败不得丢弃用户输入。

审计必须覆盖：

1. 创建、修改、删除、停用和归档工具、账户和交易。
2. 费率模板编辑、在线发布、覆盖和回滚。
3. 行情、净值和债券价格批次导入、发布和失败。
4. 证券公司行为、基金转换、债券到期、提前兑取、融资融券偿还和批量命令。
5. 冲突解决、权限阻止、引用影响预览和迁移导入。

审计不得包含密码、令牌、PC 完整本地路径、旧 MoneyHome8 原始行、旧字段值、迁移审计、迁移报告、脱敏摘要或 PC 机器环境诊断。

## 11. 错误码

| 错误码 | 含义 | 行为 |
| --- | --- | --- |
| `instrument_code_conflict` | 代码或有效期冲突 | 阻止保存 |
| `fee_snapshot_missing` | 缺少费用快照 | 阻止交易或标记状态 |
| `quote_batch_invalid` | 行情或净值批次无效 | 阻止发布 |
| `quote_provider_unsupported` | 来源适配器不可用或版本不支持 | 阻断拉取并提示更换来源 |
| `quote_challenge_required` | 来源要求验证码或安全挑战 | 进入受控挑战，不写入财务对象 |
| `quote_partial_publish_required` | 批次有失败项但未选择发布策略 | 要求用户确认或取消 |
| `quote_retry_duplicate` | 同一批次或同一来源重复重试 | 返回原批次结果 |
| `quote_history_range_invalid` | 历史价格日期范围非法或跨度超限 | 阻断拉取 |
| `quote_no_market_data` | 来源返回无交易日或无价格 | 标记缺数据，不按零发布 |
| `lot_quantity_insufficient` | 可用数量或份额不足 | 阻止卖出或赎回 |
| `bond_price_basis_invalid` | 债券价格口径不合法 | 阻止保存 |
| `bond_accrual_pending_calibration` | 应计利息公式未校准 | 标记结果状态 |
| `fund_policy_mismatch` | 基金类型与交易策略不匹配 | 阻止保存 |
| `margin_contract_unit_mismatch` | 融资金额和融券数量单位混用 | 阻止保存 |
| `margin_repayment_replay` | 偿还幂等重放 | 返回原结果 |
| `market_instrument_version_conflict` | 对象版本冲突 | 进入冲突解决 |
| `fund_confirmation_pending` | 基金份额或净值尚未确认 | 保留在途状态，不进正式持仓 |
| `fund_split_ratio_invalid` | 基金拆分比例或方向无效 | 阻止保存 |
| `bond_redemption_allocation_invalid` | 债券兑付组成不平衡 | 阻止提交 |
| `margin_repayment_candidate_empty` | 融资融券偿还候选为空 | 返回阻断原因，不生成批次 |
| `margin_repayment_exceeds_remaining` | 偿还本金或数量超过剩余合同 | 阻止提交 |

错误响应不得包含 PC 完整本地路径、旧 MoneyHome8 原始路径、旧原始行、旧字段值、迁移审计、迁移报告、脱敏摘要、令牌或密码。

## 12. 验收场景

1. 证券代码变更后，历史交易、持仓和行情仍引用稳定证券 ID。
2. 创建证券账户时复制费率模板；修改全局模板不改变已有账户费率。
3. 证券买入保存交易事实、费用快照、资金分录和成本批次。
4. 开放式基金申购保存成交净值和当前估值净值为不同快照。
5. 货币基金交易不能调用开放式基金净值策略生成隐藏净值。
6. 债券买卖必须区分净价、全价和应计利息；到期、提前兑取和市场卖出是不同终止事件。
7. 融资合同和融券合同分别使用金额和数量单位；直接偿还和批量偿还是不同命令。
8. 缺行情、缺净值、缺债券价格或风险公式未校准时显示结构化状态，不生成正式收益结论。
9. 手机只展示持仓、估值和同步摘要，不显示复杂交易入口。
10. 旧迁移相关证券、基金、债券、融资融券证据、迁移审计、迁移报告、脱敏摘要、旧路径和旧原始行只保存在 PC 本地。
11. 证券代码转换后历史交易、持仓、行情和成本批次仍引用同一稳定工具 ID。
12. 新股申购、中签和返款通过同一流程 ID 关联，重复确认或重复返款不得产生孤立交易。
13. 行情更新中止或失败不得发布半批次；成功批次必须可追溯来源、范围、日期和记录数。
14. 行情更新重试必须幂等；历史区间无数据不得发布零价格，旧来源协议诊断只保存在 PC 本地。
15. 成功发布的行情、净值、汇率、存款利率和交易费率必须触发相关投影使用同一版本，不回写旧参考库或旧缓存文件。
16. 基金申购、赎回、转换、认购、确认、收益结转和拆分必须保存费用来源、确认净值/份额、资金在途和成本重分配状态，失败整体回滚。
17. 债券正常到期、提前兑取和利息支付必须拆分本金、票息、溢折价、费用、税务和免税标志，公式未校准时标记状态。
18. 融资融券批量偿还候选为空时不得生成空批次；超额偿还、超量还券、资金不足、版本冲突和重复提交必须可解释且不半写入。

## 13. 当前无需人工确认

本计划没有引入新的产品取舍；它细化的是已确认的证券、基金、债券、融资融券、费率快照、行情净值、估值批次、成本批次、合同偿还、三端职责、校准状态和旧迁移证据 PC 本地保存边界。
