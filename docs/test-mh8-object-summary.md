# test.mh8 主账本对象摘要

本文档基于 `C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8` 的 UTF-16 字节流字符串提取，整理当前已经看见的主账本对象线索。

说明：

- 这些对象名尚不是通过正式认证后的 `SELECT` / `GetSchema` 拿到的结果。
- 但它们直接来自主账本字节流，比“只从程序资源猜表结构”更接近真实账本模型。

## 1. 当前规模

- 表名候选（UTF-16）：约 `119` 个
- 字段名候选（UTF-16）：约 `146` 个

## 2. 与内置库高度重合的对象族

主账本字节流中已可直接看到以下核心对象，说明这些实体并非只存在于内置库 `MoneyHome8.data`：

### 账户与账户组

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

### 基础资料

- `TBCategory`
- `TBCategoryStored`
- `TBCurrency`
- `TBPerson`
- `TBObjectType`

### 债权债务与信用

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

### 规划、目标、同步

- `TBFPAssetPurchasePlan`
- `TBFPExpensesInformation`
- `TBFPKeyValue`
- `TBGoalAcctRelation`
- `TBGoalSetting`
- `TBPlanStateTheme`
- `TBPlanTransaction`
- `TBSyncDefaultData`
- `TBSyncRecord`

### 投资扩展域

- `TBOpenFund`
- `TBSecurities`
- `TBSecuPrice`
- `TBSecuType`
- `TBPreciousMetals`
- `TBFuturesGoods`
- `TBFinancingContract`
- `TBStdPrice`
- `TBStdTransObject`

## 3. 主账本中特别值得注意的索引与结构线索

主账本里出现的不只是表名，还有一些明显的索引/唯一键痕迹：

- `TBAcctDetail_AcctID`
- `TBBudgetItem_INDEX_BudgetID_CategoryID_AmountBeginDate`
- `TBPayModeHistory_AcctID`
- `TBPayModeHistory_ChangeDate`
- `TBInventory_TransDate`
- `TBStdTransObject_ObjName`
- `TBFuturesContractObj_Code`
- `TBPreciousMetalsTDContractObj_CodeNIDX`

这说明：

1. 主账本不是平铺结构，而是存在明确索引设计。
2. 账本内的查询重点至少覆盖：
   - 账户维度
   - 预算维度
   - 付款方式变更历史
   - 交易日期
   - 标的名称/代码

## 4. 主账本字段线索

### 账户与对象

- `AccountName`
- `AccountType`
- `AcctID`
- `AcctType`
- `AssetID`
- `AssetName`
- `AssetType`
- `AssetTypeID`
- `ObjectID`
- `ObjectTypeID`

### 基础资料

- `CategoryID`
- `CurrencyID`
- `CurrencyName`
- `ChineseName`
- `ForeignName`
- `FullName`
- `InstitutionID`
- `PersonID`

### 时间类

- `BeginDate`
- `CreateDate`
- `ChangeDate`
- `PriceDate`
- `FirstDate`
- `FirstPayDate`
- `FirstStagePayDate`
- `LastDate`
- `LastDownloadDate`
- `OverDate`
- `InformDate`

### 金额、费率、利率

- `AnnualRate`
- `AnnualGrowthRate`
- `FinancingRate`
- `FiscalFee`
- `TransAmount`
- `TransFee`
- `TotalFee`
- `DownPaymentAmount`
- `SecuritiesLendingRate`

### 主题、提醒、模板

- `ThemeID`
- `TransType`
- `RemindType`
- `TemplateType`
- `PlanName`

## 5. 当前判断

这批主账本对象说明：

1. `test.mh8` 的真实业务模型已经和内置库 `MoneyHome8.data` 出现大范围重叠。
2. 这更像“同一业务模型在主账本与内置库中分别承载不同数据”，而不是两个完全不同的数据库世界。
3. 主账本极大概率承载：
   - 用户账户与流水
   - 用户预算与提醒
   - 用户规划与目标
   - 用户投资持仓与交易
   - 用户同步记录

## 6. 对下一步的价值

即使还没拿到工作组认证参数，我们也已经能更有把握地优先锁定以下关键表：

- `TBTransaction`
- `TBAcctGroup`
- `TBAcctDetail`
- `TBCategory`
- `TBCurrency`
- `TBPerson`
- `TBBudget`
- `TBRemindSetting`
- `TBOpenFund`
- `TBSecurities`
- `TBSyncRecord`

后续一旦认证打通，应优先对这些表做正式枚举、样例抽取和关系确认。
