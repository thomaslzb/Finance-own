# 主账本与内置库共享模型摘要

本文档基于：

- `docs/test-mh8-object-map.json`
- `docs/moneyhome8-data-object-map.json`
- `docs/shared-model-core.json`

对 `test.mh8` 主账本与解压后的 `MoneyHome8.data.decompressed.mdb` 进行对象级重合分析。

## 1. 重合规模

- 当前识别到的共享表名约：`103` 个

这意味着：

- 主账本与内置库不是两套完全独立的对象体系
- 更像是“同一业务模型在不同数据源中的两种载体”

## 2. 共享核心对象

### 账户与基础资料

- `TBAcctDetail`
- `TBAcctGroup`
- `TBAcctGroupType`
- `TBAcctRelation`
- `TBAcctType`
- `TBCategory`
- `TBCurrency`
- `TBPerson`
- `TBObjectType`

### 交易与流水

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

### 债权债务、信用与支付

- `TBDebtAcct`
- `TBDebtCAcct`
- `TBDebtInvestmentAcct`
- `TBDebtObject`
- `TBDebtRate`
- `TBPayModeHistory`
- `TBCreditCardAcct`

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
- `TBPlanInventory`
- `TBPlanStatement`
- `TBPlanTransTheme`
- `TBPlanTransaction`
- `TBSyncDefaultData`
- `TBSyncRecord`

### 投资与扩展资产

- `TBOpenFund`
- `TBSecurities`
- `TBSecuPrice`
- `TBSecuType`
- `TBPreciousMetals`
- `TBFuturesGoods`
- `TBFinancingContract`
- `TBMarginAcct`
- `TBStdPrice`
- `TBStdTransObject`
- `TBInsure`

## 3. 当前最合理解释

### 解释 A：共享模式定义

内置库保存：

- 表结构定义
- 系统初始数据
- 默认字典
- 主题/状态/类型等基础对象

主账本保存：

- 用户实际业务数据
- 用户定制配置
- 用户投资、预算、提醒、同步记录

### 解释 B：同构业务模型

即便主账本与内置库不共享同一物理文件，它们也明显复用了高度相近的业务模型。

这对 Rust 重构意味着：

- 领域层应只建一套稳定模型
- 不同数据源通过不同 repository 适配器接入

## 4. 对重构实现的直接影响

### 4.1 领域模型优先级更清晰

可以优先围绕共享核心对象落地：

- `Account`
- `AccountGroup`
- `Transaction`
- `Category`
- `Currency`
- `Person`
- `Budget`
- `Reminder`
- `Security`
- `Fund`
- `SyncRecord`

### 4.2 数据访问层建议

- `ledger_repository`
  - 面向主账本 `test.mh8`
- `builtin_repository`
  - 面向 `MoneyHome8.data` 解压内置库
- `reference_repository`
  - 面向 `mhlink.mdb`

### 4.3 迁移策略建议

如果后续无法稳定复用旧权限链，至少仍可利用这套共享模型完成：

- 旧账本只读导入
- 内置字典迁移
- 新格式落地

## 5. 当前仍待确认

- 103 个重合表在两个库中的字段是否完全一致
- 哪些表只在内置库中存在、哪些只在主账本中存在
- 主账本是否通过链接表或初始化复制方式继承内置库结构
