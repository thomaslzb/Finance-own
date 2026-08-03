# 共享表证据矩阵摘要

本文档基于 [table-evidence-matrix.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\table-evidence-matrix.json) 对主账本候选表做摘要，重点关注：

- 每张表属于哪个业务域
- 是否已出现在共享模型核心中
- 是否也出现在内置库中
- 它第一次出现的大致位置

## 1. 总体规模

- 当前纳入矩阵的主账本候选表：`119`
- 其中属于共享模型核心的表：`103`
- 当前仅在主账本线索中出现、未进入共享核心的对象：`16`

## 2. 按业务域计数

- 账户域：`18`
- 基础资料域：`16`
- 通用交易域：`16`
- 债权债务/信用域：`11`
- 规划/预算/提醒/目标域：`20`
- 投资与扩展资产域：`30`
- 同步/系统域：`5`
- 其它：`3`

## 3. 当前最重要的主账本候选域

### 账户域

首批候选表：

- `TBAcctDetail`
- `TBAcctGroup`
- `TBAcctGroupType`
- `TBAcctRelation`
- `TBAcctType`
- `TBCurrentAcct`
- `TBDepositAcct`
- `TBCreditCardAcct`
- `TBAssetAcct`

### 交易域

首批候选表：

- `TBTransaction`
- `TBTransactionB`
- `TBStatement`
- `TBStatement6`
- `TBOldTransaction`
- `TBOldStatement`
- `TBTemplate`
- `TBSchedule`

### 规划域

首批候选表：

- `TBBudget`
- `TBBudgetItem`
- `TBRemindSetting`
- `TBPlanTransaction`
- `TBGoalSetting`
- `TBFPAssetPurchasePlan`
- `TBFPExpensesInformation`

### 投资域

首批候选表：

- `TBSecurities`
- `TBOpenFund`
- `TBSecuPrice`
- `TBPreciousMetals`
- `TBFuturesGoods`
- `TBFinancingContract`
- `TBMarginAcct`

## 4. 主账本独有的额外结构线索

当前未进入共享核心、但在主账本中可见的对象多为：

- 主键/索引片段
- 名称索引
- 交易对象映射索引
- 特定查询加速结构

例如：

- `TBAcctDetail_AcctID`
- `TBBudgetItem_INDEX_BudgetID_CategoryID_AmountBeginDate`
- `TBCurrency_CashOrBill...`
- `TBCurrency_TransObjID`
- `TBCurrency_uuid`
- `TBInventory_TransDate`
- `TBPayModeHistory_AcctID`
- `TBPayModeHistory_ChangeDate`
- `TBStdTransObject_ObjName`

## 5. 当前意义

- 这份矩阵证明主账本并不是“只和内置库部分重叠”，而是大范围复用同一套业务模型。
- 同时，主账本还带有自己的查询/索引增强结构。
- 后续认证打通后，优先验证这些“独有结构”是否真为索引或关系对象，将有助于恢复原系统的查询口径。
