# UI / 窗体 / 实体 / 数据源映射

本文档将当前已识别的 UI 入口、Delphi 窗体资源、领域实体和底层数据源串起来，便于后续实现与测试对照。

## 1. 账户中心

### UI 入口

- 左侧导航：`账户中心`

### 相关窗体

- `TAccountManagerFm`
- `TAccountDlgFm`
- `TAccountOverviewDlgFm`
- `TNewAcctWizard*`

### 相关实体

- `AccountGroup`
- `Account`
- `AccountType`
- `Currency`

### 主要数据源

- 主账本：
  - `TBAcctGroup`
  - `TBAcctDetail`
  - `TBAcctType`
  - `TBCurrency`

## 2. 财务记录 / 记账

### UI 入口

- 左侧导航：`财务记录`
- 顶部入口：`记账`

### 相关窗体

- `TTransDlgFm`
- `TCashTransFm`
- `TCurrentTransFm`
- `TWasteBookFm`
- `TExpenseDlgFm`
- `TCashXferDlgFm`

### 相关实体

- `Transaction`
- `TransactionType`
- `TransactionTheme`
- `Template`
- `Category`
- `Person`

### 主要数据源

- 主账本：
  - `TBTransaction`
  - `TBStatement`
  - `TBTransType`
  - `TBTransTheme`
  - `TBTemplate`
  - `TBCategory`
  - `TBPerson`

## 3. 债权债务 / 信用卡 / 应收应付

### UI 入口

- 账户中心下的应收款、应付款、信用类账户

### 相关窗体

- `TClaimsTransFm`
- `TCreditCardTransFm`
- `TCreditCardStatisticFrame`
- `TCreditRemindDlg`
- `TPayable*`
- `TReceivablesViewFrame`

### 相关实体

- `DebtAccount`
- `DebtObject`
- `CreditCard`
- `PayModeHistory`

### 主要数据源

- 主账本：
  - `TBDebtAcct`
  - `TBDebtObject`
  - `TBDebtRate`
  - `TBCreditCardAcct`
  - `TBPayModeHistory`

## 4. 投资一览

### UI 入口

- 左侧导航：`投资一览`

### 相关窗体

- `TInvestmentListFm`
- `TSecurity*`
- `TOpenFund*`
- `TForeign*`
- `TNMarketBond*`
- `TFutures*`
- `TGold*`
- `TPrecious*`
- `TMargin*`

### 相关实体

- `Security`
- `Fund`
- `Quote`
- `FeeRule`
- `LookupIndex`
- `InvestmentCatalog`

### 主要数据源

- 主账本：
  - `TBSecurities`
  - `TBOpenFund`
- 共享参考库：
  - `TBSecuPrice`
  - `TBTransFee`
- 缓存：
  - `MoneyHome8.cache`
  - `Investment.cache`

## 5. 定期 / 理财 / 货币类产品

### UI 入口

- 账户中心中的定期、理财、货币类账户

### 相关窗体

- `TFixedDepositTransFm`
- `TMoney*`

### 相关实体

- `Account`
- `RateRule`
- `Transaction`

### 主要数据源

- 主账本：
  - `TBDepositAcct`
- 共享参考库：
  - `HBRate`

## 6. 预算 / 提醒 / 财务规划 / 目标

### UI 入口

- `计划与提醒`
- `限额提醒`
- 目标相关页

### 相关窗体

- `TBudget*`
- `TNewRemindDlgFm`
- `TLimitRemindDlg`
- `TFinancialPlanningCenterFm`
- `TFP*`
- `TGoal*`

### 相关实体

- `Budget`
- `Reminder`
- `FinancialPlanning`
- `Goal`

### 主要数据源

- 主账本：
  - `TBBudget`
  - `TBRemindSetting`
  - `TBFP*`
  - `TBGoal*`

## 7. 同步 / 登录 / 远程通知

### UI 入口

- `同步数据`
- 登录/注册相关页

### 相关窗体

- `TLoginDialog`
- `TRegisterForm`
- `TSyncUserDataFm`
- `TSyncUserRegisterFm`
- `TRemoteNotificationDlgFm`
- `TOnlineGetDataFm`

### 相关实体

- `SyncRecord`
- `SyncProfile`
- `Reminder`
- `Budget`

### 主要数据源

- 主账本：
  - `TBSyncRecord`
  - `TBSyncDefaultData`
- 本地配置：
  - `user.cfg`
  - `UseInformation.cfg`
- 远端协议：
  - `mwSync.ini`
  - `Notification.ini`

## 8. 报表与分析

### UI 入口

- 顶部：`财务报表`
- 顶部：`财务分析`

### 相关窗体

- `TReportFm`
- `TReportOptionDlgFm`
- `TRpt*`

### 相关实体

- `Transaction`
- `Account`
- `Quote`
- `Budget`
- `ReportSettings`

### 主要数据源

- 主账本：
  - `TBReportSettings`
  - `TBTransaction`
  - `TBAcct*`
- 共享参考库：
  - `TBSecuPrice`
  - `HBRate`
  - `TBTransFee`

## 9. 导入导出

### UI 入口

- 导入数据、导入交割单、导出数据

### 相关窗体

- `TImportDataFm`
- `TImportCategoryDlgFm`
- `TImportJiaogeDanDlgFm`
- `TImportPreviewFm`
- `TExportDataFm`

### 相关实体

- `Transaction`
- `Category`
- `Security`
- `Fund`

### 主要数据源

- 主账本：
  - `TBTransaction`
  - `TBCategory`
- 缓存与参考库：
  - `Investment.cache`
  - `TBSecuPrice`
