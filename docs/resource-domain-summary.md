# Resource Domain Summary

本文档基于 [resource-forms.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\resource-forms.json) 对 `MoneyHome8.exe` 的 Delphi 资源窗体做域级摘要，帮助快速判断功能覆盖面与实现优先级。

## 1. 总量

- 已抽取 `RT_RCDATA` 窗体资源：`465` 个

## 2. 主要分组

### 账户体系

- 数量：`48`
- 代表窗体：
  - `TAccountManagerFm`
  - `TAccountDlgFm`
  - `TAccountOverviewDlgFm`
  - `TNewAcctWizard*`
  - 各类账户 `*AcctDlgFm`

说明：

- 原软件并非只有“新增账户”一个入口，而是包含大量账户类型专用向导和配置页。

### 通用交易与流水

- 数量：`20`
- 代表窗体：
  - `TCashTransFm`
  - `TCurrentTransFm`
  - `TWasteBookFm`
  - `TExpenseDlgFm`
  - `TCashXferDlgFm`
  - `TTmpl*` / `TTransfer*` / `TTransactionPlan*`

说明：

- 原软件具备“交易录入 + 流水浏览 + 模板 + 计划”组合能力。

### 债权债务与信用类

- 数量：`36`
- 代表窗体：
  - `TClaimsTransFm`
  - `TDebt*`
  - `TCreditCardTransFm`
  - `TPayable*`
  - `TReceivablesViewFrame`
  - `TPrepaid*`

说明：

- 应收、应付、借贷、信用卡、预付待摊属于同一组“负债/债权/信用”能力，不宜在重构时拆散成彼此无关的孤立页面。

### 投资与扩展资产

- 数量：`105`
- 代表窗体：
  - `TForeign*`
  - `TSecurity*`
  - `TOpenFund*`
  - `TNMarketBond*`
  - `TFutures*`
  - `TGold*`
  - `TPreciousMetalStd*`
  - `TMargin*`
  - `TMoney*`
  - `TAsset*`
  - `TInsure*`
  - `TSocialSecurity*`

说明：

- 这是产品最宽的业务域，也是 Rust 重构时最容易低估工作量的一块。

### 预算、提醒、规划、目标

- 数量：`28`
- 代表窗体：
  - `TBudget*`
  - `TNewRemindDlgFm`
  - `TLimitRemindDlg`
  - `TRemoteNotificationDlgFm`
  - `TFinancialPlanningCenterFm`
  - `TFP*`
  - `TGoal*`

说明：

- 财务规划是一个专题输入系统，不是单报表页。

### 报表

- 数量：`27`
- 代表窗体：
  - `TReportFm`
  - `TReportOptionDlgFm`
  - `TRpt*`

说明：

- 报表覆盖收支、资产、投资、趋势、标签、账户多口径。

### 系统与同步

- 数量：`12`
- 代表窗体：
  - `TLoginDialog`
  - `TRegisterForm`
  - `TSyncUserDataFm`
  - `TOnlineGetDataFm`
  - `TSystemSettingsFm`
  - `TPasswordDialog`

说明：

- 同步与用户体系是明确存在的，不应在早期设计里忽略。

## 3. 长尾但重要的功能信号

以下窗体虽然不一定属于前述主分组，但都是重构时容易漏掉的功能点：

- `TAccessoriesDlg`
  - 说明存在附件/附属信息能力
- `TCheckBookDlg`
  - 说明存在支票簿或票据相关能力
- `TManageBillDateDlgFm` / `TModifyBillDateDlgFm`
  - 说明存在账单日管理
- `TRechargeDlgFm`
  - 说明存在充值场景
- `TPayrollIncomeDlgFm`
  - 说明存在工资收入专门录入页
- `TAlsoCouponsDirectlyDlgFm` / `TCouponsAlsoBuyCouponsDlgFm`
  - 说明存在票息、优惠券或类似金融细分场景
- `TRelationNewStockRecordsDlgFm`
  - 说明存在新股关联记录
- `TSecurityCodeConvertFm`
  - 说明存在证券代码转换
- `TCleanPriceFm`
  - 说明存在净价/清洁价格相关金融计算
- `TCalculatorDlg`
  - 说明内置辅助计算器

## 4. 对重构排期的影响

### 低估风险最高的域

- 投资与扩展资产
- 财务规划
- 导入交割单与模板
- 同步、通知、行情

### 适合作为 Phase 1 的域

- 账本打开/备份/恢复
- 分类/标签/人员/币种
- 账户中心
- 通用收支与流水

### 适合作为 Phase 2/3 的域

- 证券/基金/债券/期货/黄金/保险
- 财务规划与目标
- 云同步与行情
- 批量导入导出与交割单
