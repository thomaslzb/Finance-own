# 内置库表字段候选摘要

本文档基于 [inner-table-field-map.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\inner-table-field-map.json) 做人工收敛，提取其中相对可信、对实现最有价值的字段候选。

说明：

- 这是启发式抽取结果，存在噪音。
- 其中同时出现于主账本和内置库，并且业务含义清晰的字段，可信度更高。
- 出现明显跨表串扰的候选字段，在本摘要中会被剔除或标记为“待验证”。

## 1. 相对可信的表字段候选

### `TBBankFiscal`

相对可信字段：

- `TransObjID`
- `Name`
- `ContractNo`
- `ProductNo`
- `CurrType`
- `BeginDate`
- `DateType`
- `EndDate`
- `YRate`
- `InstitutionID`

当前判断：

- 更像银行理财/金融产品合约信息表。

### `TBFinancingContract`

相对可信字段：

- `TransObjID`
- `Name`
- `Rate`
- `SecuObjID`
- `TheDate`
- `SID`
- `CnName`
- `EnName`
- `FeeType`
- `FeeRate`
- `ExchangeName`

当前判断：

- 更像融资合约或证券化融资对象表。

### `TBHistory`

相对可信字段：

- `Name`
- `BeginDate`
- `EndDate`
- `GoalValue`
- `AcctID`
- `CreateDate`
- `FirstDate`
- `TransAmount`
- `StagesCount`
- `StagesAmount`
- `FeeType`
- `Fee`
- `RateType`
- `Rate`
- `CompletedCount`
- `AutoCompletedCount`

当前判断：

- 很可能承载历史计划、阶段任务或历史统计对象，而非普通流水表。

### `TBMarginAcct`

相对可信字段：

- `AcctID`
- `FinancingRate`
- `SecuritiesLendingRate`
- `TransObjID`
- `FullName`
- `SGRate`
- `SHRate`
- `ShortName`
- `CurrType`
- `AutoUpdateName`

当前判断：

- 这些字段与融资融券保证金账户的语义匹配度较高。

### `TBOpenFund`

相对可信字段：

- `TransObjID`
- `FullName`
- `SGRate`
- `SHRate`
- `ShortName`
- `CurrType`
- `AutoUpdateName`
- `AcctID`

待验证字段：

- `ThemeID`
- `TransID`
- `TransObjectID`

当前判断：

- 基金对象至少包含名称、代码关联、币种和行情更新名。

### `TBPlanStateTheme`

相对可信字段：

- `StateID`
- `ThemeID`
- `TransID`
- `TransDate`
- `AssetTypeID`
- `AcctID`
- `TransObjectID`
- `CategoryID`
- `Amount`
- `Theme`
- `TransType`
- `ItemID`
- `PersonID`
- `Price`
- `TotalFee`
- `FIID`
- `TDate`
- `UpdateTime`
- `TransBID`
- `ChargeMode`
- `FiscalFee`
- `TransFee`
- `TackFee`

当前判断：

- 这组字段强烈说明该表更像“计划状态 / 主题 / 交易引用”混合表。

### `TBRemindSetting`

相对可信字段：

- `RemindType`
- `ObjectID`
- `MinValue`
- `MaxValue`

待验证字段：

- `PreciousMetalsName`
- `CurrType`
- `TransObjID`
- `SecuType`
- `SecuName`
- `AutoUpdateName`

当前判断：

- 阈值提醒语义可信，但后半段字段很可能混入了相邻表串扰。

## 2. 明显存在串扰的表

以下表目前只抽到了极少量、且明显来自相邻表的字段，不建议直接据此建模：

- `TBAcctType`
- `TBAssetAcct`
- `TBAssetType`
- `TBBudget`
- `TBCategory`
- `TBCreditCardAcct`
- `TBCurrency`
- `TBCurrentAcct`
- `TBCustom`
- `TBDebtCAcct`
- `TBDebtInvestmentAcct`
- `TBDebtObject`
- `TBDebtRate`

当前建议：

- 这些表仍应以 [schema-hypothesis.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\schema-hypothesis.md) 和主账本/内置库对象摘要为主，不要直接依赖这份启发式结果。

## 3. 对后续实现的使用原则

### 可以直接参考的

- 表是否存在
- 某些强语义字段是否出现
- 某个对象大致属于哪类业务表

### 不应直接当成最终事实的

- 完整字段列表
- 字段顺序
- 字段类型
- 相邻表间是否发生字段串扰

## 4. 当前价值

尽管启发式结果有噪音，但它至少帮我们确认：

1. 某些复杂表确实携带了比“表名”更多的业务语义
2. 融资、基金、银行理财、计划状态、历史记录等对象不是空壳
3. 一旦后续认证打通，应优先回头正式验证这些高价值表
