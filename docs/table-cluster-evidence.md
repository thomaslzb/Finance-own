# 主账本表簇证据

本文档基于 `test.mh8` 中表名在 UTF-16 字节流里的出现顺序，对主账本的表簇分布做当前阶段的技术观察。

## 1. 当前现象

主账本中的表名并非零散随机出现，而是能明显看到若干“簇”。

这通常意味着：

- 某些位置更像对象目录区
- 某些位置更像索引/键定义区
- 某些位置更像另一套结构描述或镜像定义区

## 2. 第一簇：账户与基础业务起始簇

较早位置连续出现：

- `TBTransFee`
- `TBDebtRate`
- `TBDebtObject`
- `TBDebtInvestmentAcct`
- `TBDebtCAcct`
- `TBCustom`
- `TBCurrentAcct`
- `TBCurrency`
- `TBCreditCardAcct`
- `TBCategory`
- `TBBudget`
- `TBAssetType`
- `TBAssetAcct`
- `TBAcctType`
- `TBAcctRelation`
- `TBAcctGroup`
- `TBAcctDetail`

当前判断：

- 这是一个高度业务化的对象目录区。
- 其顺序很像“先基础账务，再账户，再扩展对象”。

## 3. 第二簇：索引/主键增强簇

随后出现：

- `TBAcctDetail_AcctID`
- `TBAcctGroup_PK`
- `TBMortgage_PK`
- `TBBudgetItem_INDEX_BudgetID_CategoryID_AmountBeginDate`
- `TBBudgetItem_PK`
- `TBCategory_PK`
- `TBCurrency_uuid`
- `TBDebtObject_PK`

当前判断：

- 这一段更像索引/主键定义区。

## 4. 第三簇：参考与对象类型簇

随后出现：

- `TBSecuPrice`
- `TBSecuType`
- `TBSecurityAcct`
- `TBSecurities`
- `TBReportSettings`
- `TBRemindTypeSet`
- `TBPreciousMetalsTDGoods`
- `TBPreciousMetalsTDContractObj`
- `TBPreciousMetals`

当前判断：

- 这一段把证券、提醒、报表、贵金属等对象拉到一起，像一个“扩展对象目录区”。

## 5. 第四簇：计划与目标簇

随后出现：

- `TBPlanTransTheme`
- `TBPlanTransaction`
- `TBPlanStatement6`
- `TBPlanInventory`
- `TBPayModeHistory`
- `TBObjectType`
- `TBMemoTemp`
- `TBLifeTheme`
- `TBInventory`
- `TBInsure`
- `TBInstallment`
- `TBGoalSetting`
- `TBGoalAcctRelation`
- `TBFuturesContractObj`
- `TBFPKeyValue`
- `TBFPExpensesInformation`
- `TBFPAssetPurchasePlan`
- `TBDiary`

当前判断：

- 这段明显聚合了：
  - 计划
  - 提醒相关
  - 目标
  - 财务规划
  - 保险/期货/库存/日记

## 6. 后段重复簇

在更靠后的位置，许多表再次出现，例如：

- `TBSystem`
- `TBAcctDetail`
- `TBAcctGroup`
- `TBCategory`
- `TBCurrency`
- `TBPerson`
- `TBPlanStatement`
- `TBPlanTransaction`
- `TBOpenFund`
- `TBSecuPrice`
- `TBSecurities`
- `TBTransaction`
- `TBTransType`

当前判断：

- 主账本内部很可能不止一处保存对象定义。
- 可能是：
  - 表目录镜像
  - 数据访问页/对象定义区
  - 查询/设计器相关元数据区

## 7. 当前最重要的技术意义

### 7.1 主账本内部不是单层目录

它更像至少包含：

- 主业务对象目录
- 主键/索引区
- 扩展对象目录
- 计划与目标目录
- 后段镜像或设计器对象区

### 7.2 认证打通后应优先验证两件事

1. 这些簇是否分别对应：
   - 真正表
   - 索引
   - 关系
   - 设计器对象
2. 后段重复表是否为：
   - 链接表
   - 系统视图
   - 设计元对象

### 7.3 对 Rust 重构的意义

- 读取器设计不能假设“每张表只出现一次定义”。
- 后续正式解析时，要准备区分：
  - 数据表
  - 索引对象
  - 设计器元数据
  - 链接表/外部表
