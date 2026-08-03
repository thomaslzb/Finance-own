# MoneyHome8.data 内置库对象摘要

本文档基于解压后的 `artifacts/MoneyHome8.data.decompressed.mdb` 进行底层字符串提取，记录当前已发现的表名候选与字段名候选。

说明：

- 这些对象名来自 Jet 数据库字节流中的可见字符串。
- 它们不是通过正式认证后的表枚举结果，但足以作为高价值结构线索。

## 1. 表名候选规模

- 当前提取到的 `TB*` 表名候选约：`110` 个

## 2. 已识别的核心对象族

### 账户与分组

- `TBAcctDetail`
- `TBAcctGroup`
- `TBAcctGroupType`
- `TBAcctRelation`
- `TBAcctType`
- `TBCurrentAcct`
- `TBDepositAcct`
- `TBCreditCardAcct`
- `TBAssetAcct`
- `TBSecurityAcct`
- `TBMarginAcct`
- `TBInsureAcctInfo`

### 交易与流水

- `TBTransaction`
- `TBTransactionB`
- `TBStatement`
- `TBStatement6`
- `TBOldTransaction`
- `TBOldStatement`
- `TBSchedule`
- `TBTemplate`
- `TBTransTheme`
- `TBTransType`
- `TBAcctTransFee`
- `TBTransFee`

### 分类、标签、人员、币种

- `TBCategory`
- `TBCategoryStored`
- `TBCurrency`
- `TBPerson`
- `TBPerson_1`
- `TBPerson_2`
- `TBObjectType`

### 债权债务与付款历史

- `TBDebtAcct`
- `TBDebtCAcct`
- `TBDebtInvestmentAcct`
- `TBDebtObject`
- `TBDebtRate`
- `TBPayModeHistory`

### 预算、提醒、报表

- `TBBudget`
- `TBBudgetItem`
- `TBRemindSetting`
- `TBRemindTypeSet`
- `TBReportSettings`

### 财务规划与目标

- `TBFPAssetPurchasePlan`
- `TBFPExpensesInformation`
- `TBFPKeyValue`
- `TBGoalAcctRelation`
- `TBGoalSetting`

### 投资扩展域

- `TBOpenFund`
- `TBSecurities`
- `TBSecuPrice`
- `TBSecuType`
- `TBPreciousMetals`
- `TBPreciousMetalsTDGoods`
- `TBPreciousMetalsTDContractObj`
- `TBFuturesGoods`
- `TBFuturesContractObj`
- `TBFinancingContract`
- `TBSecuritiesLendingContract`
- `TBStdPrice`
- `TBStdPriceOther`
- `TBStdTransObject`

### 系统与同步

- `TBSystem`
- `TBSyncDefaultData`
- `TBSyncRecord`
- `TBLifeTheme`
- `TBStateTheme`
- `TBPlanStateTheme`
- `TBPlanTransTheme`
- `TBPlanTransaction`

## 3. 字段名候选信号

当前已发现字段名候选约：`130` 个，以下是最能说明业务结构的一批：

### 主键、外键与对象关联

- `AccountID`
- `AssetAcctID`
- `AssetID`
- `AssetObjID`
- `AssetTransObjID`
- `BudgetID`
- `CategoryID`
- `CurrencyID`
- `DebtAcctID`
- `FuturesGoodsID`
- `InstitutionID`
- `ObjectID`
- `ObjectTypeID`
- `PersonID`

### 日期与计划

- `BeginDate`
- `CreateDate`
- `FirstDate`
- `FirstPayDate`
- `FirstStagePayDate`
- `LastDate`
- `LastDownloadDate`
- `LastDownloadTransationDate`
- `OverDate`
- `PriceDate`
- `InformDate`

### 金额、费率、利率

- `AnnualRate`
- `AnnualGrowthRate`
- `FinancingRate`
- `ManagementFeeRate`
- `FiscalFee`
- `FeeRate`
- `TransAmount`
- `TotalFee`
- `RateType`

### 主题、提醒、名称

- `Theme`
- `ThemeID`
- `RemindType`
- `PlanName`
- `AssetName`
- `DebtName`
- `ExpensesName`
- `SecuName`
- `PreciousMetalsName`

## 4. 当前结构判断

这批表名与字段名说明：

1. `MoneyHome8.data` 解压后的内置库绝不是一张小字典表。
2. 它至少覆盖：
   - 账户与账户组
   - 交易流水
   - 分类、人员、币种
   - 债权债务
   - 预算与提醒
   - 财务规划与目标
   - 证券、基金、期货、贵金属、融资融券等扩展投资域
   - 同步与系统主题
3. 这进一步支持一个判断：
   - 原软件内部存在“主业务数据库模型”，而不是仅靠 UI 逻辑拼装功能。

## 5. 对 Rust 重构的直接意义

- 后续 Rust 领域模型不需要从零拍脑袋命名。
- 可以优先对齐这批表名中的业务实体，减少术语漂移。
- 等认证打通后，优先验证以下表：
  - `TBTransaction`
  - `TBAcctGroup`
  - `TBCategory`
  - `TBPerson`
  - `TBBudget`
  - `TBRemindSetting`
  - `TBOpenFund`
  - `TBSecurities`
  - `TBPlanTransaction`
  - `TBSyncRecord`
