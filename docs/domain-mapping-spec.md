# MoneyHome8 领域映射规格

本文档把当前已确认的功能页、候选表、字段线索、参考库表、缓存依赖整理成按业务域划分的实现规格，用于直接指导 Rust 代码落地。

说明：

- `状态` 只表示当前证据成熟度：
  - `confirmed`
    - 已有强证据，通常来自多源
  - `inferred`
    - 已有较强推断，但仍缺正式表结构或页面细节
- `来源` 可能包括：
  - `MH8`
  - `INNER`
  - `REF`
  - `CACHE`
  - `RC`
  - `UI`

## 1. 账户域

### 1.1 账户组

- 实体：
  - `AccountGroup`
- 状态：
  - `confirmed`
- 页面：
  - `财务数据 -> 账户中心`
- 候选表：
  - `TBAcctGroup`
  - `TBAcctGroupType`
  - `TBAcctRelation`
- 关键字段：
  - `GroupID`
  - `TypeID`
  - `ParentIdName`
  - `CreateDate`
  - `ChangeDate`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`
  - `UI`
- 依赖：
  - `Account`

### 1.2 账户

- 实体：
  - `Account`
- 状态：
  - `confirmed`
- 页面：
  - `财务数据 -> 账户中心`
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
- 关键字段：
  - `AcctID`
  - `AcctType`
  - `AccountName`
  - `AccountType`
  - `CurrencyID`
  - `InstitutionID`
  - `ObjectID`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`
  - `UI`
- 依赖：
  - `Currency`
  - `AccountGroup`

## 2. 基础资料域

### 2.1 分类

- 实体：
  - `Category`
- 状态：
  - `confirmed`
- 页面：
  - `财务数据 -> 标签/分类相关页`
- 候选表：
  - `TBCategory`
  - `TBCategoryStored`
- 关键字段：
  - `CategoryID`
  - `TypeID`
  - `TypeName`
  - `ChineseName`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`

### 2.2 标签

- 实体：
  - `Tag`
- 状态：
  - `inferred`
- 页面：
  - `财务数据 -> 标签`
- 候选来源：
  - `TBObjectType`
  - `TBStateTheme`
  - 资源窗体中的 Tag 相关控件
- 来源：
  - `RC`
  - `UI`
  - `INNER`

### 2.3 币种

- 实体：
  - `Currency`
- 状态：
  - `confirmed`
- 页面：
  - 基础资料 / 投资 / 账户
- 候选表：
  - `TBCurrency`
- 关键字段：
  - `CurrencyID`
  - `CurrencyName`
  - `CurrType`
  - `ChineseName`
  - `ForeignName`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`

### 2.4 人员

- 实体：
  - `Person`
- 状态：
  - `confirmed`
- 页面：
  - 人员资料、债权债务、提醒关联
- 候选表：
  - `TBPerson`
  - `TBPerson_1`
  - `TBPerson_2`
- 关键字段：
  - `PersonID`
  - `ChineseName`
  - `ForeignName`
  - `FullName`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`

## 3. 通用交易域

### 3.1 通用流水

- 实体：
  - `Transaction`
- 状态：
  - `confirmed`
- 页面：
  - `财务数据 -> 财务记录`
  - `记账`
  - `流水账`
- 候选表：
  - `TBTransaction`
  - `TBTransactionB`
  - `TBStatement`
  - `TBStatement6`
  - `TBOldTransaction`
  - `TBOldStatement`
- 关键字段：
  - `TransID`
  - `TransDate`
  - `TransType`
  - `TransAmount`
  - `TransFee`
  - `TotalFee`
  - `TransObjID`
  - `CategoryID`
  - `PersonID`
  - `CurrencyID`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`

### 3.2 模板与计划

- 实体：
  - `Template`
  - `Schedule`
  - `PlannedTransaction`
- 状态：
  - `confirmed`
- 页面：
  - 模板、计划、重复性交易
- 候选表：
  - `TBTemplate`
  - `TBSchedule`
  - `TBPlanTransaction`
  - `TBPlanStatement`
- 关键字段：
  - `TemplateType`
  - `PlanName`
  - `FirstDate`
  - `LastDate`
  - `StagesCount`
  - `StagesAmount`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`

## 4. 债权债务与信用域

### 4.1 债权债务

- 实体：
  - `DebtAccount`
  - `DebtObject`
  - `DebtRate`
- 状态：
  - `confirmed`
- 页面：
  - 债权债务页
- 候选表：
  - `TBDebtAcct`
  - `TBDebtCAcct`
  - `TBDebtInvestmentAcct`
  - `TBDebtObject`
  - `TBDebtRate`
- 关键字段：
  - `DebtAcctID`
  - `DebtName`
  - `RateType`
  - `AnnualRate`
  - `BorrowingDate`
  - `OverDate`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`

### 4.2 信用卡

- 实体：
  - `CreditCard`
- 状态：
  - `confirmed`
- 页面：
  - 信用卡流水 / 账单日 / 提醒
- 候选表：
  - `TBCreditCardAcct`
- 关键字段：
  - `AcctID`
  - `AccountType`
  - `PaymentType`
  - `NewBillDate`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`

### 4.3 应收应付/预付待摊

- 实体：
  - `Receivable`
  - `Payable`
  - `PrepaidExpense`
- 状态：
  - `inferred`
- 页面：
  - 应收款 / 应付款 / 预付费用
- 候选表：
  - `TBPayModeHistory`
  - `TBDebt*`
  - `TBPrepaid*` 相关对象线索
- 来源：
  - `RC`
  - `MH8`
  - `INNER`

## 5. 投资与扩展资产域

### 5.1 证券

- 实体：
  - `Security`
- 状态：
  - `confirmed`
- 页面：
  - 证券列表、证券交易、投资一览
- 候选表：
  - `TBSecurities`
  - `TBSecurityAcct`
  - `TBSecuType`
- 关键字段：
  - `SecuObjID`
  - `SecuName`
  - `SecuType`
  - `SecuTypeName`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`

### 5.2 基金

- 实体：
  - `Fund`
- 状态：
  - `confirmed`
- 页面：
  - 开放式基金、投资一览
- 候选表：
  - `TBOpenFund`
- 关键字段：
  - `ObjectID`
  - `ObjectTypeID`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`

### 5.3 行情

- 实体：
  - `Quote`
- 状态：
  - `confirmed`
- 来源表：
  - `mhlink.mdb.TBSecuPrice`
- 字段：
  - `SecuCode`
  - `PriceDate`
  - `Price`
  - `CurrType`
  - `ObjType`
- 依赖：
  - `Security`
  - `Fund`

### 5.4 费率

- 实体：
  - `FeeRule`
- 状态：
  - `confirmed`
- 来源表：
  - `mhlink.mdb.TBTransFee`
- 字段：
  - `Type`
  - `YJFL`
  - `YHSL`
  - `ZDYJ`
  - `GHF`
  - `FJF`
  - `JSFL`
- 依赖：
  - `TransactionType`

### 5.5 利率

- 实体：
  - `RateRule`
- 状态：
  - `confirmed`
- 来源表：
  - `mhlink.mdb.HBRate`
- 字段：
  - `CurrType`
  - `DepoType`
  - `DepoTime`
  - `ARate`

### 5.6 其他扩展资产

- 实体：
  - `Asset`
  - `InsurancePolicy`
  - `PreciousMetal`
  - `FuturesContract`
  - `FinancingContract`
- 状态：
  - `confirmed`
- 候选表：
  - `TBAssetAcct`
  - `TBAssetType`
  - `TBInsure`
  - `TBInsureAcctInfo`
  - `TBPreciousMetals`
  - `TBPreciousMetalsTDGoods`
  - `TBFuturesGoods`
  - `TBFinancingContract`
  - `TBSecuritiesLendingContract`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`

## 6. 预算、提醒、规划、目标域

### 6.1 预算

- 实体：
  - `Budget`
  - `BudgetItem`
- 状态：
  - `confirmed`
- 页面：
  - 财务分析 -> 财务预算
- 候选表：
  - `TBBudget`
  - `TBBudgetItem`
- 字段：
  - `BudgetID`
  - `AmountBeginDate`
  - `CategoryID`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`
  - `UI`

### 6.2 提醒

- 实体：
  - `Reminder`
  - `ReminderType`
- 状态：
  - `confirmed`
- 页面：
  - 计划与提醒 / 今日提醒 / 限额提醒
- 候选表：
  - `TBRemindSetting`
  - `TBRemindTypeSet`
- 字段：
  - `RemindType`
  - `InformDate`
  - `IsRemind`
- 来源：
  - `MH8`
  - `INNER`
  - `INI`
  - `RC`

### 6.3 财务规划与目标

- 实体：
  - `FinancialPlanning`
  - `Goal`
- 状态：
  - `confirmed`
- 页面：
  - 财务分析 -> 财务规划
  - 财务分析 -> 财务目标
- 候选表：
  - `TBFPAssetPurchasePlan`
  - `TBFPExpensesInformation`
  - `TBFPKeyValue`
  - `TBGoalSetting`
  - `TBGoalAcctRelation`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`
  - `UI`

## 7. 同步与系统域

### 7.1 同步

- 实体：
  - `SyncRecord`
  - `SyncDefaultData`
  - `SyncProfile`
- 状态：
  - `confirmed`
- 页面：
  - 登录/注册/同步数据
- 候选表：
  - `TBSyncRecord`
  - `TBSyncDefaultData`
- 配置来源：
  - `mwSync.ini`
  - `Notification.ini`
- 来源：
  - `MH8`
  - `INNER`
  - `INI`
  - `RC`

### 7.2 报表设置

- 实体：
  - `ReportSettings`
- 状态：
  - `confirmed`
- 页面：
  - 财务报表
- 候选表：
  - `TBReportSettings`
- 来源：
  - `MH8`
  - `INNER`
  - `RC`

## 8. 缓存与检索域

### 8.1 综合检索缓存

- 实体：
  - `LookupIndex`
- 状态：
  - `confirmed`
- 来源：
  - `MoneyHome8.cache`
- 当前语义：
  - 代码
  - 中文名
  - 拼音/缩写

### 8.2 投资品目录缓存

- 实体：
  - `InvestmentCatalog`
- 状态：
  - `confirmed`
- 来源：
  - `Investment.cache`
- 当前语义：
  - 类型码 `_3 / _4 / _9`
  - 投资品名称
  - 分类检索

## 9. 当前最重要的实施与验证顺序

### 第一优先级：新系统闭环

- 执行 SQLite 核心迁移并实现账簿创建
- 实现账户、交易头、原子账户分录和基础资料写入
- 实现 `ReportReadRepository` 的流水、余额和标签查询
- 用最小样例验证事务回滚、稳定排序和本币折算

### 第二优先级：运行结果校准

- 投资买入、部分卖出、分红、费用和转入转出
- 财务记录本币流入、本币流出与差额
- 25 张报表的动态列、分组、小计和导出
- 财务诊断、规划和目标结果

### 并行优先级：旧库迁移映射

- `TBAcctGroup`
- `TBAcctDetail`
- `TBTransaction`
- `TBCategory`
- `TBCurrency`
- `TBPerson`

### 旧库第二批验证

- `TBBudget`
- `TBRemindSetting`
- `TBOpenFund`
- `TBSecurities`
- `TBSyncRecord`

### 旧库第三批验证

- `TBGoalSetting`
- `TBFPExpensesInformation`
- `TBReportSettings`
- `TBPreciousMetals`
- `TBFuturesGoods`
- `TBFinancingContract`
