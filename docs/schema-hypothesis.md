# MoneyHome8 模式假设

本文档在尚未完全拿到 `test.mh8` 正式表结构前，根据当前已掌握的：

- `test.mh8` 主账本对象/字段候选
- `MoneyHome8.data` 解压内置库对象/字段候选
- `mhlink.mdb` 共享参考库正式字段

为 Rust 重构提供“候选表 -> 候选字段 -> 领域实体”的假设映射。

说明：

- 本文是结构假设，不等于最终事实。
- 其价值在于为代码实现和后续验证提供一个稳定起点。
- 本文只描述旧 Jet 候选结构；新系统不按这些表复刻，正式新库模式见 [sqlite-schema-and-query-contract.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\sqlite-schema-and-query-contract.md)。

## 1. 账户域

### 1.1 账户组

- 候选表：
  - `TBAcctGroup`
  - `TBAcctGroupType`
  - `TBAcctRelation`

候选字段：

- `GroupID`
- `TypeID`
- `TypeName`
- `ParentIdName`
- `CreateDate`
- `ChangeDate`

Rust 实体：

- `AccountGroup`
- `AccountGroupType`

### 1.2 账户明细

- 候选表：
  - `TBAcctDetail`
  - `TBAcctType`
  - `TBCurrentAcct`
  - `TBDepositAcct`
  - `TBCreditCardAcct`
  - `TBAssetAcct`
  - `TBSecurityAcct`
  - `TBMarginAcct`
  - `TBInsureAcctInfo`

候选字段：

- `AcctID`
- `AcctType`
- `AccountName`
- `AccountType`
- `CurrencyID`
- `CurrencyName`
- `AssetAcctID`
- `SecuAcctType`
- `InstitutionID`
- `ObjectID`

Rust 实体：

- `Account`
- `AccountKind`

## 2. 基础资料域

### 2.1 分类

- 候选表：
  - `TBCategory`
  - `TBCategoryStored`

候选字段：

- `CategoryID`
- `TypeID`
- `TypeName`
- `ChineseName`
- `ShortName`

Rust 实体：

- `Category`

### 2.2 币种

- 候选表：
  - `TBCurrency`

候选字段：

- `CurrencyID`
- `CurrencyName`
- `CurrType`
- `ChineseName`
- `ForeignName`
- `FullName`
- `ObjectID`

Rust 实体：

- `Currency`

### 2.3 人员

- 候选表：
  - `TBPerson`
  - `TBPerson_1`
  - `TBPerson_2`

候选字段：

- `PersonID`
- `ChineseName`
- `ForeignName`
- `FullName`
- `TypeID`

Rust 实体：

- `Person`

### 2.4 对象类型

- 候选表：
  - `TBObjectType`
  - `TBSecuType`

候选字段：

- `ObjectTypeID`
- `SecuType`
- `SecuTypeName`
- `TypeID`
- `TypeName`

Rust 实体：

- `ObjectType`
- `SecurityType`

## 3. 通用交易域

### 3.1 交易头

- 候选表：
  - `TBTransaction`
  - `TBTransactionB`
  - `TBStatement`
  - `TBStatement6`
  - `TBOldTransaction`
  - `TBOldStatement`

候选字段：

- `TransID`
- `TransDate`
- `TransType`
- `TransAmount`
- `TransFee`
- `TotalFee`
- `TransObjID`
- `TransObjectID`
- `TransBID`
- `ThemeID`
- `CategoryID`
- `PersonID`
- `CurrencyID`
- `AccountID`

Rust 实体：

- `Transaction`

### 3.2 交易主题与类型

- 候选表：
  - `TBTransTheme`
  - `TBStateTheme`
  - `TBPlanTransTheme`
  - `TBLifeTheme`
  - `TBTransType`

候选字段：

- `ThemeID`
- `TypeID`
- `TypeName`
- `PlanName`

Rust 实体：

- `TransactionTheme`
- `TransactionType`

### 3.3 模板与计划

- 候选表：
  - `TBTemplate`
  - `TBSchedule`
  - `TBPlanTransaction`
  - `TBPlanStatement`
  - `TBPlanInventory`

候选字段：

- `TemplateType`
- `PlanName`
- `FirstDate`
- `LastDate`
- `StagesCount`
- `StagesAmount`
- `AutoCompletedCount`
- `CompletedCount`

Rust 实体：

- `Template`
- `Schedule`
- `PlannedTransaction`

## 4. 债权债务与支付域

### 4.1 债权债务

- 候选表：
  - `TBDebtAcct`
  - `TBDebtCAcct`
  - `TBDebtInvestmentAcct`
  - `TBDebtObject`
  - `TBDebtRate`

候选字段：

- `DebtAcctID`
- `DebtName`
- `RateType`
- `AnnualRate`
- `BorrowingDate`
- `OverDate`
- `PaymentType`

Rust 实体：

- `DebtAccount`
- `DebtObject`
- `DebtRate`

### 4.2 支付方式历史

- 候选表：
  - `TBPayModeHistory`

候选字段：

- `AcctID`
- `ChangeDate`
- `PaymentType`

Rust 实体：

- `PayModeHistory`

## 5. 预算、提醒、目标、规划域

### 5.1 预算

- 候选表：
  - `TBBudget`
  - `TBBudgetItem`

候选字段：

- `BudgetID`
- `CategoryID`
- `AmountBeginDate`
- `Amount`
- `BeginDate`
- `EndDate`

Rust 实体：

- `Budget`
- `BudgetItem`

### 5.2 提醒

- 候选表：
  - `TBRemindSetting`
  - `TBRemindTypeSet`

候选字段：

- `RemindType`
- `InformDate`
- `IsRemind`
- `FirstDate`

Rust 实体：

- `Reminder`
- `ReminderType`

### 5.3 目标与财务规划

- 候选表：
  - `TBGoalSetting`
  - `TBGoalAcctRelation`
  - `TBFPAssetPurchasePlan`
  - `TBFPExpensesInformation`
  - `TBFPKeyValue`

候选字段：

- `PlanName`
- `AssetID`
- `AssetName`
- `ExpensesName`
- `ExpensesType`
- `IncomeAnnualGrowthRate`
- `AnnualGrowthRate`
- `AnnualFeeExemptType`
- `MonthlyRepaymentAmount`
- `TuitionFee`

Rust 实体：

- `Goal`
- `GoalAccountRelation`
- `FinancialPlanning`
- `FinancialPlanningInput`

## 6. 投资与扩展资产域

### 6.1 证券

- 候选表：
  - `TBSecurities`
  - `TBSecurityAcct`

候选字段：

- `SecuObjID`
- `SecuName`
- `SecuType`
- `SecuTypeName`
- `SecuAcctType`

Rust 实体：

- `Security`

### 6.2 基金

- 候选表：
  - `TBOpenFund`

候选字段：

- `ObjectID`
- `ObjectTypeID`
- `PriceDate`

Rust 实体：

- `Fund`

### 6.3 重大资产

- 候选表：
  - `TBAssetAcct`
  - `TBAssetType`

候选字段：

- `AssetID`
- `AssetName`
- `AssetType`
- `AssetTypeID`
- `AssetValue`
- `AssetValue2`

Rust 实体：

- `Asset`

### 6.4 保险

- 候选表：
  - `TBInsure`
  - `TBInsureAcctInfo`
  - `TBInsureAcctInfoCSTR`

候选字段：

- `InsureType`
- `FirstInsuranceDate`
- `FirstPayDate`
- `FirstStagePayDate`
- `InsureTransObjID`

Rust 实体：

- `InsurancePolicy`
- `InsuranceEvent`：显式保存开户保费调整、缴费、返还、分红、退保和迁移调整；资金交易为可选稳定关联，不能用金额方向反推事件类型。退保事件保存 `finish_account` 命令快照，`false` 时保单保持活动，`true` 时才执行终止状态转换。
- `InsuranceCashValueSnapshot`：以保单和估值日为唯一键保存当前有效值；同日新增执行版本化 upsert。
- `InsuranceCashValueHistory`：追加记录插入、修改和删除前后值；不参与资金余额和缴费汇总。

动态样例已确认投保金额、开户已缴保费和现金价值是三种独立口径。保险账户余额取查询基准日之前最新生效的现金价值快照；同日把 `0.00` 添加为 `8.00` 后仍只有一行，再修改为 `9.00` 时交易记录和缴费总额不变。删除唯一 `11.00` 后旧程序出现 `1.00/11.00/0.00` 分裂；两日期删除最新 `13.00` 后重开明细仍为 `11.00`、余额却回填 `13.00`；反向删除较早 `11.00` 时，当前会话及重启均稳定保留最新 `13.00`。历史 `7.00`、当前 `11.00` 和未来 `15.00` 可同时存在，以 `2026-07-31` 查询仍为 `11.00`，但旧程序重启后错误归零。目标库必须通过快照生效区间和显式 `as_of_date` 重建全部消费者，无匹配快照时统一投影零。普通账户分录、投保金额或脱离查询日的缓存都不能代替现金价值。

金额边界样例进一步证明 `InsuranceCashValueSnapshot.value_minor` 必须是非负整数最小单位：旧程序把负数和空值静默写为零，人民币三位小数按两位四舍五入，十一位整数金额出现分币丢失和进位，十位整数金额则可跨页和重启保持精确。目标库用触发器拒绝负数，应用层拒绝空值并执行币种精度舍入；输入、聚合和格式化都不得经过二进制浮点账本事实。

独立缴费样例确认 `InsuranceEvent.funding_transaction_id` 的设计边界：选择资金账户支付 `10.00` 时，保险事件与资金流出必须一对一稳定关联，支付账户余额从 `100.00` 变为 `90.00`；累计保费增加但现金价值仍为 `0.00`。开户保费调整仍允许该关联为空，两种来源不得混写。

### 6.5 贵金属 / 期货 / 融资融券

- 候选表：
  - `TBPreciousMetals`
  - `TBPreciousMetalsTDGoods`
  - `TBPreciousMetalsTDContractObj`
  - `TBFuturesGoods`
  - `TBFuturesContractObj`
  - `TBFinancingContract`
  - `TBSecuritiesLendingContract`
  - `TBMarginAcct`

候选字段：

- `PreciousMetalsName`
- `PreciousMetalsTDGoodsID`
- `FuturesGoodsID`
- `FinancingRate`
- `SecuritiesLendingRate`
- `ObjectTypeID`

Rust 实体：

- `PreciousMetal`
- `FuturesContract`
- `FinancingContract`
- `SecuritiesLendingContract`

## 7. 同步与系统域

### 7.1 同步记录

- 候选表：
  - `TBSyncRecord`
  - `TBSyncDefaultData`

候选字段：

- `LastDownloadDate`
- `LastDownloadTransationDate`
- `Note4LastDownloadTransationDate`
- `AutoUpdateName`

Rust 实体：

- `SyncRecord`
- `SyncDefaultData`

### 7.2 报表设置

- 候选表：
  - `TBReportSettings`

Rust 实体：

- `ReportSettings`

## 8. 参考库正式已读对象

### `HBRate`

字段：

- `ID`
- `CurrType`
- `DepoType`
- `DepoTime`
- `ARate`

Rust 实体：

- `RateRule`

### `TBSecuPrice`

字段：

- `ID`
- `SecuCode`
- `PriceDate`
- `Price`
- `ObjectQuant`
- `CurrType`
- `ObjType`

Rust 实体：

- `Quote`

### `TBTransFee`

字段：

- `ID`
- `Type`
- `YJFL`
- `YHSL`
- `YHSL_SELL`
- `ZDYJ`
- `GHF`
- `FJF`
- `JSFL`
- `JSFSX`
- `JYGF`
- `YJFL_SELL`
- `ZDYJ_SELL`

Rust 实体：

- `FeeRule`

## 9. 当前最值得优先验证的表

### 主账本认证打通后优先验证

- `TBAcctGroup`
- `TBAcctDetail`
- `TBCategory`
- `TBCurrency`
- `TBPerson`
- `TBTransaction`
- `TBBudget`
- `TBRemindSetting`
- `TBOpenFund`
- `TBSecurities`
- `TBSyncRecord`

### 主账本认证打通后第二批验证

- `TBTemplate`
- `TBPayModeHistory`
- `TBGoalSetting`
- `TBFPExpensesInformation`
- `TBReportSettings`
- `TBPreciousMetals`
- `TBFuturesGoods`
- `TBFinancingContract`
