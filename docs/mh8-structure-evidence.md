# 主账本结构证据

本文档汇总当前从 `test.mh8` 主账本字节流中直接抽出的结构证据，重点是：

- 表名候选
- 字段名候选
- 主键/索引/唯一键痕迹
- 这些线索对后续正式表枚举的价值

依赖文件：

- [test-mh8-object-map.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\test-mh8-object-map.json)
- [test-mh8-index-field-hints.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\test-mh8-index-field-hints.json)

## 1. 已确认的结构层级

当前证据显示，`test.mh8` 至少存在以下四层结构：

1. 业务表名
2. 业务字段名
3. 主键或唯一键命名
4. 索引命名

这说明主账本不是“简单存值文件”，而是带有明确关系型设计的数据库。

## 2. 主键/唯一键线索

当前已直接看到的典型主键或唯一键命名包括：

- `TBAcctGroup_PK`
- `TBBudgetItem_PK`
- `TBCategory_PK`
- `TBDebtObject_PK`
- `TBFPAssetPurchasePlan_PK`
- `TBFPExpensesInformation_PK`
- `TBInsure_PK`
- `TBMortgage_PK`
- `TBPayModeHistory_PK`
- `TBPerson_PK`
- `TBPracObj_PK`
- `TBReportSettings_PK`
- `TBSecurityAcct_PK`
- `TBTransaction_PK`

当前解释：

- 这些对象大概率至少都有独立主键。
- `TBTransaction_PK` 的存在非常重要，说明交易主表不是无主键堆叠。

## 3. 索引线索

当前可见的索引/索引片段包括：

- `TBBudgetItem_INDEX`
- `TBBudgetItem_INDEX_BudgetID_CategoryID_AmountBeginDate`
- `IDX_TBAcctDetail_AcctID`
- `IDX_TBPayModeHistory_AcctID`
- `IDX_TBPayModeHistory_ChangeDate`
- `IDX_TBInventory_TransDate`
- `IDX_TBStdTransObject_ObjName`
- `X_TBCurrency_EnglishAbbr2IDX_TBCurrency_TransObjID`
- `ID2IDX_TBCurrency_CashOrBill4IDX_TBCurrency_ChineseName4ID`
- `LIDX_TBPreciousMetalsTDContractObj_CodeNID`

当前解释：

- `TBBudgetItem` 至少有预算维度复合索引。
- `TBAcctDetail` 至少有按账户 ID 的索引。
- `TBPayModeHistory` 至少按账户和变更时间索引，说明有历史追踪需求。
- `TBInventory` 至少按交易日期索引，说明存在按时间序列聚合库存/持仓的查询需求。
- `TBStdTransObject` 至少按对象名称索引，说明存在名称检索需求。
- `TBCurrency` 存在多种索引片段，说明币种表被高频使用且承担转换/显示口径。

## 4. 字段线索中的高价值部分

### 4.1 主体标识类

- `AcctID`
- `AssetID`
- `CategoryID`
- `CurrencyID`
- `DebtAcctID`
- `ObjectID`
- `ObjectTypeID`
- `PersonID`
- `TransID`

### 4.2 时间类

- `BeginDate`
- `CreateDate`
- `ChangeDate`
- `FirstDate`
- `FirstInsuranceDate`
- `FirstPayDate`
- `FirstStagePayDate`
- `LastDate`
- `LastDownloadDate`
- `PriceDate`
- `InformDate`
- `OverDate`

### 4.3 金额/费率类

- `TransAmount`
- `TransFee`
- `TotalFee`
- `AnnualRate`
- `AnnualGrowthRate`
- `FinancingRate`
- `FiscalFee`
- `SecuritiesLendingRate`
- `DownPaymentAmount`
- `MonthlyRepaymentAmount`
- `TuitionFee`

### 4.4 业务语义类

- `AccountName`
- `AccountType`
- `AssetName`
- `DebtName`
- `ExpensesName`
- `SecuName`
- `SecuType`
- `SecuTypeName`
- `PaymentType`
- `TemplateType`
- `RemindType`
- `PlanName`

## 5. 当前最强的数据库设计推断

### 推断 A：主账本存在明确的标准主表

如：

- `TBTransaction`
- `TBAcctDetail`
- `TBCategory`
- `TBPerson`
- `TBBudgetItem`

### 推断 B：主账本存在按查询场景设计的索引

至少覆盖：

- 账户维度
- 日期维度
- 预算维度
- 支付方式历史维度
- 名称检索维度

### 推断 C：主账本不是只存“当前状态”

从以下对象可以看出存在历史或计划语义：

- `TBPayModeHistory`
- `TBOldTransaction`
- `TBOldStatement`
- `TBPlanTransaction`
- `TBSchedule`

## 6. 对 Rust 重构的直接意义

### 6.1 领域模型要接受“历史 + 当前 + 计划”三层并存

不能只建：

- 当前账户
- 当前交易

还要考虑：

- 历史流水
- 计划交易
- 历史支付方式

### 6.2 查询层要提前考虑索引对应的访问模式

即使新系统不复用旧索引名，也应保留同类查询优化方向：

- 按账户查
- 按日期范围查
- 按预算/分类查
- 按对象名称查

### 6.3 报表与预算统计最好不要从 UI 端做二次拼装

因为当前线索已经表明旧系统在数据库层就存在较强的查询设计。

## 7. 后续一旦认证打通，最先该验证什么

1. `TBTransaction_PK` 是否真为交易主键
2. `TBBudgetItem_INDEX_BudgetID_CategoryID_AmountBeginDate` 的真实列序
3. `IDX_TBPayModeHistory_AcctID` / `ChangeDate` 是否对应历史追踪
4. `IDX_TBStdTransObject_ObjName` 是否对应投资对象模糊检索
5. `TBCurrency` 上的多索引是否对应现金/票据/英文简称/对象映射
