# MoneyHome8 实体目录

本文档将当前已识别的表名、字段名、参考库表、缓存语义和功能域统一整理为“实体目录”，用于指导 Rust 领域建模与实现顺序。

证据标记：

- `MH8`：来自 `test.mh8` 主账本字节流
- `INNER`：来自解压后的 `MoneyHome8.data` 内置 Jet 库字节流
- `REF`：来自 `mhlink.mdb` 可直接查询的表
- `CACHE`：来自 `MoneyHome8.cache` / `Investment.cache`
- `RC`：来自 Delphi 窗体资源

## 1. 核心账本实体

### `AccountGroup`

- 线索对象：
  - `TBAcctGroup`
  - `TBAcctGroupType`
  - `TBAcctRelation`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- 业务职责：
  - 组织账户树
  - 承载分组显示顺序与层级
- Rust 优先级：
  - `P0`

### `Account`

- 线索对象：
  - `TBAcctDetail`
  - `TBAcctType`
  - `TBCurrentAcct`
  - `TBDepositAcct`
  - `TBCreditCardAcct`
  - `TBAssetAcct`
  - `TBSecurityAcct`
  - `TBMarginAcct`
  - `TBInsureAcctInfo`
- 典型字段：
  - `AccountName`
  - `AccountType`
  - `AcctID`
  - `AcctType`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P0`

### `Category`

- 线索对象：
  - `TBCategory`
  - `TBCategoryStored`
- 典型字段：
  - `CategoryID`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P0`

### `Currency`

- 线索对象：
  - `TBCurrency`
- 典型字段：
  - `CurrencyID`
  - `CurrencyName`
  - `CurrType`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P0`

### `Person`

- 线索对象：
  - `TBPerson`
  - `TBPerson_1`
  - `TBPerson_2`
- 典型字段：
  - `PersonID`
  - `ChineseName`
  - `ForeignName`
  - `FullName`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P0`

## 2. 通用交易实体

### `Transaction`

- 线索对象：
  - `TBTransaction`
  - `TBTransactionB`
  - `TBStatement`
  - `TBStatement6`
  - `TBOldTransaction`
  - `TBOldStatement`
- 典型字段：
  - `TransID`
  - `TransDate`
  - `TransType`
  - `TransAmount`
  - `TransFee`
  - `TransObjID`
  - `ThemeID`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P0`

### `TransactionTheme`

- 线索对象：
  - `TBTransTheme`
  - `TBStateTheme`
  - `TBPlanTransTheme`
  - `TBLifeTheme`
- 证据：
  - `MH8`
  - `INNER`
- Rust 优先级：
  - `P1`

### `TransactionType`

- 线索对象：
  - `TBTransType`
- 典型字段：
  - `TypeID`
  - `TypeName`
- 证据：
  - `MH8`
  - `INNER`
- Rust 优先级：
  - `P0`

### `Template`

- 线索对象：
  - `TBTemplate`
- 典型字段：
  - `TemplateType`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P1`

## 3. 债权债务与信用实体

### `DebtAccount`

- 线索对象：
  - `TBDebtAcct`
  - `TBDebtCAcct`
  - `TBDebtInvestmentAcct`
- 典型字段：
  - `DebtAcctID`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P1`

### `DebtObject`

- 线索对象：
  - `TBDebtObject`
  - `TBDebtRate`
- 典型字段：
  - `DebtName`
  - `RateType`
- 证据：
  - `MH8`
  - `INNER`
- Rust 优先级：
  - `P1`

### `CreditCard`

- 线索对象：
  - `TBCreditCardAcct`
- 相关窗体：
  - `TCreditCardTransFm`
  - `TCreditCardStatisticFrame`
  - `TCreditRemindDlg`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P1`

### `PayModeHistory`

- 线索对象：
  - `TBPayModeHistory`
- 典型字段：
  - `ChangeDate`
  - `AcctID`
- 证据：
  - `MH8`
  - `INNER`
- Rust 优先级：
  - `P1`

## 4. 预算、提醒、计划、目标实体

### `Budget`

- 线索对象：
  - `TBBudget`
  - `TBBudgetItem`
- 典型字段：
  - `BudgetID`
  - `AmountBeginDate`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P1`

### `Reminder`

- 线索对象：
  - `TBRemindSetting`
  - `TBRemindTypeSet`
- 典型字段：
  - `RemindType`
  - `InformDate`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P1`

### `Plan`

- 线索对象：
  - `TBPlanInventory`
  - `TBPlanStatement`
  - `TBPlanTransaction`
  - `TBSchedule`
- 典型字段：
  - `PlanName`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P2`

### `FinancialPlanning`

- 线索对象：
  - `TBFPAssetPurchasePlan`
  - `TBFPExpensesInformation`
  - `TBFPKeyValue`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P2`

### `Goal`

- 线索对象：
  - `TBGoalSetting`
  - `TBGoalAcctRelation`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P2`

## 5. 投资与扩展资产实体

### `Security`

- 线索对象：
  - `TBSecurities`
  - `TBSecurityAcct`
  - `TBSecuType`
- 典型字段：
  - `SecuName`
  - `SecuType`
  - `SecuObjID`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P2`

### `Fund`

- 线索对象：
  - `TBOpenFund`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P2`

### `Asset`

- 线索对象：
  - `TBAssetAcct`
  - `TBAssetType`
- 典型字段：
  - `AssetID`
  - `AssetName`
  - `AssetTypeID`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P2`

### `Insurance`

- 线索对象：
  - `TBInsure`
  - `TBInsureAcctInfo`
- 典型字段：
  - `FirstInsuranceDate`
  - `InsureType`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P2`

### `PreciousMetals`

- 线索对象：
  - `TBPreciousMetals`
  - `TBPreciousMetalsTDGoods`
  - `TBPreciousMetalsTDContractObj`
- 典型字段：
  - `PreciousMetalsName`
  - `PreciousMetalsTDGoodsID`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P2`

### `Futures`

- 线索对象：
  - `TBFuturesGoods`
  - `TBFuturesContractObj`
- 典型字段：
  - `FuturesGoodsID`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P2`

### `Financing`

- 线索对象：
  - `TBFinancingContract`
  - `TBSecuritiesLendingContract`
  - `TBMarginAcct`
- 典型字段：
  - `FinancingRate`
  - `SecuritiesLendingRate`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P2`

## 6. 同步与系统实体

### `SyncRecord`

- 线索对象：
  - `TBSyncRecord`
  - `TBSyncDefaultData`
- 典型字段：
  - `LastDownloadDate`
  - `LastDownloadTransationDate`
- 证据：
  - `MH8`
  - `INNER`
  - `INI`
- Rust 优先级：
  - `P2`

### `ReportSettings`

- 线索对象：
  - `TBReportSettings`
- 证据：
  - `MH8`
  - `INNER`
  - `RC`
- Rust 优先级：
  - `P2`

### `SystemState`

- 线索对象：
  - `TBSystem`
  - `TBStateTheme`
  - `TBLifeTheme`
- 证据：
  - `MH8`
  - `INNER`
- Rust 优先级：
  - `P3`

## 7. 参考数据实体

### `RateRule`

- 来源：
  - `mhlink.mdb.HBRate`
- 字段：
  - `CurrType`
  - `DepoType`
  - `DepoTime`
  - `ARate`
- Rust 优先级：
  - `P1`

### `Quote`

- 来源：
  - `mhlink.mdb.TBSecuPrice`
- 字段：
  - `SecuCode`
  - `PriceDate`
  - `Price`
  - `CurrType`
  - `ObjType`
- Rust 优先级：
  - `P1`

### `FeeRule`

- 来源：
  - `mhlink.mdb.TBTransFee`
- 字段：
  - `Type`
  - `YJFL`
  - `YHSL`
  - `ZDYJ`
  - `GHF`
  - `FJF`
  - `JSFL`
- Rust 优先级：
  - `P1`

## 8. 缓存与检索实体

### `LookupIndex`

- 来源：
  - `MoneyHome8.cache`
- 语义：
  - 代码检索
  - 中文名检索
  - 拼音缩写检索
- Rust 优先级：
  - `P1`

### `InvestmentCatalog`

- 来源：
  - `Investment.cache`
- 语义：
  - 投资品列表
  - 类型码 `_3 / _4 / _9`
  - 投资对象名称索引
- Rust 优先级：
  - `P1`

## 9. 当前落地建议

### 最先建模

- `AccountGroup`
- `Account`
- `Category`
- `Currency`
- `Person`
- `Transaction`

### 第二批建模

- `Budget`
- `Reminder`
- `RateRule`
- `Quote`
- `FeeRule`
- `LookupIndex`
- `InvestmentCatalog`

### 第三批建模

- `Security`
- `Fund`
- `DebtAccount`
- `Insurance`
- `PreciousMetals`
- `Futures`
- `Goal`
- `FinancialPlanning`
- `SyncRecord`
