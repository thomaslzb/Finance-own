# MoneyHome8 共享表域地图

本文档将当前已确认的 `103` 张主账本/内置库共享表，按业务域做系统性归类。

目的：

1. 让后续实现可以按域推进，而不是逐张表零散处理。
2. 明确哪些表属于核心账本，哪些属于扩展资产，哪些属于系统/同步/报表配置。

数据来源：

- [shared-model-core.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\shared-model-core.json)
- [shared-model-summary.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\shared-model-summary.md)

## 1. 账户与基础资料域

### 账户与账户组

- `TBAcctDetail`
- `TBAcctGroup`
- `TBAcctGroupType`
- `TBAcctRelation`
- `TBAcctTransFee`
- `TBAcctType`
- `TBCurrentAcct`
- `TBDepositAcct`
- `TBCreditCardAcct`
- `TBAssetAcct`
- `TBSecurityAcct`
- `TBMarginAcct`
- `TBInsureAcctInfo`
- `TBInsureAcctInfoCSTR`
- `TBStdAcct`

### 基础资料

- `TBCategory`
- `TBCategoryStored`
- `TBCurrency`
- `TBPerson`
- `TBPerson_1`
- `TBPerson_2`
- `TBObjectType`
- `TBSecuType`
- `TBStateTheme`
- `TBLifeTheme`

## 2. 通用交易与流水域

- `TBTransaction`
- `TBTransactionB`
- `TBStatement`
- `TBStatement6`
- `TBOldTransaction`
- `TBOldStatement`
- `TBTemplate`
- `TBTransTheme`
- `TBTransType`
- `TBSchedule`
- `TBHistory`
- `TBMemoTemp`
- `TBDiary`
- `TBInventory`
- `TBInstallment`

## 3. 债权债务与信用域

- `TBDebtAcct`
- `TBDebtCAcct`
- `TBDebtInvestmentAcct`
- `TBDebtObject`
- `TBDebtRate`
- `TBPayModeHistory`

## 4. 预算、提醒、计划、目标域

- `TBBudget`
- `TBBudgetI`
- `TBBudgetItem`
- `TBRemindSetting`
- `TBRemindTypeSet`
- `TBPlanInventory`
- `TBPlanStatement`
- `TBPlanStatement6`
- `TBPlanTransTheme`
- `TBPlanTransaction`
- `TBFPAssetPurchasePlan`
- `TBFPExpensesInformation`
- `TBFPKeyValue`
- `TBGoalAcctRelation`
- `TBGoalSetting`

## 5. 投资与扩展资产域

### 证券与基金

- `TBOpenFund`
- `TBSecurities`
- `TBSecuPrice`

### 重大资产与理财

- `TBAssetType`
- `TBBankFiscal`
- `TBMortgage_PK`
- `TBStdPrice`
- `TBStdPriceOther`
- `TBStdTransObject`
- `TBCustom`

### 贵金属 / 期货 / 融资融券

- `TBPreciousMetals`
- `TBPreciousMetalsTDAcct`
- `TBPreciousMetalsTDContractObj`
- `TBPreciousMetalsTDGoods`
- `TBFuturesContractObj`
- `TBFuturesGoods`
- `TBFinancingContract`
- `TBSecuritiesLendingContract`
- `TBPracObj`
- `TBPracType`

### 保险

- `TBInsure`
- `TBInsure_PK`

## 6. 同步与系统配置域

- `TBSyncDefaultData`
- `TBSyncRecord`
- `TBReportSettings`
- `TBSystem`
- `TBReportSettings_PK`
- `TBPlanStateTheme`
- `TBPracObj_PK`

## 7. 杂项与辅助结构

- `TBGoalSetting`
- `TBGoalAcctRelation`
- `TBFPAssetPurchasePlan_PK`
- `TBFPExpensesInformation_PK`
- `TBAcctGroup_PK`
- `TBBudgetItem_PK`
- `TBCategory_PK`
- `TBDebtObject_PK`
- `TBPayModeHistory_PK`
- `TBPerson_PK`
- `TBSecurityAcct_PK`
- `TBTransaction_PK`

说明：

- 这些对象多为 `*_PK` 或结构性辅助对象，更适合作为索引/约束线索，而不是单独领域实体。

## 8. 领域优先级排序

### P0：最先实现

- 账户与基础资料域
- 通用交易与流水域

### P1：第二批实现

- 债权债务与信用域
- 预算、提醒、计划域
- 共享参考库中的行情/利率/费率

### P2：第三批实现

- 证券与基金
- 重大资产与理财
- 贵金属 / 期货 / 融资融券
- 保险

### P3：第四批实现

- 同步与系统配置域
- 财务规划与目标

## 9. 当前最重要的实现启示

- 不要把 `103` 张表一口气平推实现。
- 先围绕：
  - 账户
  - 分类
  - 人员
  - 交易
  - 预算
  - 提醒
  - 行情/利率/费率
  这几条主链建立稳定的最小闭环。
