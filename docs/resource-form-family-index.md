# Resource Form Family Index

本文档按“窗体家族”整理 `MoneyHome8.exe` 的 Delphi 资源。磁盘资源目录共有 `465` 项，其中 `460` 项是真实运行时 DFM 窗体，另 `5` 项为主题或非窗体资源。本页使用通配符聚合家族，只作为人工导航；逐窗体、无遗漏的权威映射见 [runtime-form-coverage-audit.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-coverage-audit.md) 和 [runtime-form-coverage-audit.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-form-coverage-audit.json)。

## 1. 账本与系统家族

- `TNewBookFm`
- `TBackupBookFm`
- `TRestoreBookFm`
- `TAboutForm`
- `TSystemSettingsFm`
- `TShortcutManageDlgFm`
- `TPasswordDialog`
- `TPwdCheckFm`
- `TPwdChangeFm`
- `TGuideDlg`

## 2. 登录、注册、同步家族

- `TLoginDialog`
- `TRegisterForm`
- `TSyncUserDataFm`
- `TSyncUserRegisterFm`
- `TRemoteNotificationDlgFm`
- `TOnlineGetDataFm`
- `TUpdateVerifyCodeFm`

## 3. 账户与开户向导家族

- `TAccountManagerFm`
- `TAccountDlgFm`
- `TAccountOverviewDlgFm`
- `TAccountFeeSetFm`
- `TEditAccountGroupFm`
- `TNewAcctTypeDlgFm`
- `TNewAcctWizard*`
  - Cash
  - Current
  - FixedDeposit
  - ThirdDeposits
  - Exchange
  - Security
  - OpenFund
  - DebtInvestment
  - NMarketDebt
  - Money
  - Margin
  - Futures
  - Gold
  - PreciousMetalStd
  - CreditCard
  - TwoCurrCredit
  - InsureCommerce
  - InsureSocial

## 4. 基础资料家族

- `TCategoryListFm`
- `TEditCategoryFm`
- `TEditCatgoryOrderDlgFm`
- `TPersonListFm`
- `TPersonDlg`
- `TCurrListFm`
- `TCurrDlg`
- `TRateFm`
- `TExchangeRateDlg`
- `TSelectTagDlgFm`
- `TEditTagOrderDlgFm`

## 5. 通用收支与流水家族

- `TTransDlgFm`
- `TCashTransFm`
- `TCurrentTransFm`
- `TThirdDepositsTransFm`
- `TWasteBookFm`
- `TExpenseDlgFm`
- `TCashWithdrawDlgFm`
- `TCashXferDlgFm`
- `TSplitIncExpDlgFm`
- `TIncExpEditFrame`
- `TIncExpInstallmentWizardDlg`
- `TInstallmentEditDlg`
- `TInstallmentEditFrame`
- `TInstallmentFrame`
- `TTemplateDlgFm`
- `TTransferTemplateDlgFm`
- `TTransactionPlanDlgFm`
- `TXferPlanDlgFm`
- `TFilterDlgFm`
- `TFilterTransFrame`
- `TFindDlgFm`
- `TFindForm`
- `TCustColumnFm`

## 6. 债权债务、信用、应收应付家族

- `TClaimsTransFm`
- `TClaimsDebt*`
- `TDebtBorrowDlgFm`
- `TDebtLendDlgFm`
- `TDebtRecDlgFm`
- `TDebtReturnDlgFm`
- `TDebtAdjustDlgFm`
- `TDebtRateSetDlg`
- `TDebtInvestment*`
- `TCreditCardTransFm`
- `TCreditCardStatisticFrame`
- `TCreditRemindDlg`
- `TPayable*`
- `TReceivablesViewFrame`
- `TPrepaidExpenses*`
- `TPrePaymentFm`

## 7. 定期、理财、货币产品家族

- `TFixedDepositTransFm`
- `TFixedDepositStatisticFrame`
- `TFixDepMatureDlgFm`
- `TMoneyListFm`
- `TMoneyTransFm`
- `TMoneyBuyDlgFm`
- `TMoneyRedeemDlgFm`
- `TMoneyMatureDlgFm`
- `TMoneyStatisticFrame`
- `TMoneyProductsViewFrame`
- `TMoneyInfoViewFrame`

## 8. 外汇家族

- `TForeignTransFm`
- `TForeignTransFrame`
- `TForeignStatisticFrame`
- `TCurrExchangeDlgFm`
- `TCurrChgXferDlgFm`
- `TExchangeAcctFm`
- `TExchangeViewFrame`
- `TExchangeMarketConstitutesFrame`

## 9. 证券家族

- `TSecurityListFm`
- `TSecurityTransFm`
- `TSecurityTransFrame`
- `TSecurityStatisticFrame`
- `TStockBuyDlgFm`
- `TStockMarkBuyDlgFm`
- `TStockOrderBuyDlgFm`
- `TStockSellDlgFm`
- `TStockDividDlgFm`
- `TStockInterestDlgFm`
- `TStockQuotaDlgFm`
- `TSecurityRemindDlg`
- `TSecurityCodeConvertFm`
- `TRelationNewStockRecordsDlgFm`

## 10. 开放式基金家族

- `TOpenFundsListFm`
- `TOpenFundTransFm`
- `TOpenFundTransFrame`
- `TOpenFundStatisticFrame`
- `TFundBuyDlgFm`
- `TFundMarkBuyDlgFm`
- `TFundOrderBuyDlgFm`
- `TFundSellDlgFm`
- `TFundConvertDlgFm`
- `TFundReinvestDlgFm`
- `TFundInterestDlgFm`
- `TOpenFundRemindDlg`

## 11. 债券、国债、债券市场家族

- `TNMarketBondListFm`
- `TNMarketBondBuyDlgFm`
- `TNMarketBondSellDlgFm`
- `TNMarketBondMatureDlgFm`
- `TNMarketBondCashAheadDlgFm`
- `TNMarketBondInterestDlgFm`
- `TBondsMarketConstitutesFrame`
- `TBondsViewFrame`
- `TMarketDebt*`

## 12. 期货、黄金、贵金属家族

- `TFuturesGoodsListFm`
- `TFuturesContractListFm`
- `TFuturesBuyDlgFm`
- `TFuturesSellDlgFm`
- `TFuturesStatisticFrame`
- `TGOLD*`
- `TPreciousMetalStd*`

## 13. 融资融券、保证金家族

- `TMarginAcctDlgFm`
- `TMarginTransFm`
- `TMarginTransFrame`
- `TMarginStatisticFrame`
- `TMarginInterestRepaymentsDlgFm`
- `TEquityFinancingDlgFm`
- `TEquitySecuritiesLendingDlgFm`
- `TFinancingBidDlgFm`
- `TExertionRightsDlgFm`
- `TQuitExertionRightFm`

## 14. 保险与社保家族

- `TInsureTransFm`
- `TInsureTransFrame`
- `TInsurePayFeeDlgFm`
- `TInsureGetFeeDlgFm`
- `TInsureDividendFm`
- `TInsureOverDlgFm`
- `TInsureBalaInDlgFm`
- `TInsureBalaOutDlgFm`
- `TInsureCashValueEditDlgFm`
- `TSocialSecurityTransFm`
- `TSocialSecurityStatisticFrame`

## 15. 重大资产与实物资产家族

- `TAssetBuyFm`
- `TAssetEncashDlgFm`
- `TAssetIncrementDlgFm`
- `TAssetInvestDlgFm`
- `TAssetOtherFeeDlgFm`
- `TAssetPriceFm`
- `TAssetsStatisticFrame`
- `TAssetsValueManagementFrame`
- `TAssetViewFrame`

## 16. 预算、提醒、规划、目标家族

- `TBudgetListFm`
- `TBudgetCopyDlgFm`
- `TCreateBudgetDlgFm`
- `TEditBudgetAmountDlgFm`
- `TEditBudgetCategoryDlgFm`
- `TNewRemindDlgFm`
- `TLimitRemindDlg`
- `TFinancialDiagnosisFm`
- `TFinancialPlanningCenterFm`
- `TFP*`
  - AnnualSalaryInfo
  - AssetIncomeInfo
  - AssetExpensesInfo
  - AssetGrowthInfo
  - AssetPurchasePlanInfo
  - DailyExpensesInfo
  - EducationExpensesInfo
  - OtherIncomeInfo
  - OtherExpensesInfo
  - ExpensesAdjustmentInfo
  - InflationRateInfo
  - RetirementInfo
  - YearDataInfo
  - SelectAssets
- `TGoalCenterFm`
- `TGoalSaveFm`
- `TGoalAcctListDlg`

## 17. 导入导出家族

- `TImportDataFm`
- `TImportCategoryDlgFm`
- `TImportPreviewFm`
- `TImportSelectDlgFm`
- `TImportThemeDlgFm`
- `TImportJiaogeDanDlgFm`
- `TExportDataFm`

## 18. 报表与分析家族

- `TReportFm`
- `TReportOptionDlgFm`
- `TRpt*`
  - CashWaste
  - IncomeList
  - IncomeStat
  - IncExpCompare
  - YearIncExp
  - MonthAsset
  - MonthAverageIncExp
  - BalanceSheet
  - CreditDebtStat
  - InvestIncome
  - InvestmentPerformanceStat
  - SecuritiesInvest / Loss
  - OpenFundInvest / Loss
  - StockTrend
  - FundTrend
  - TagIncomeStat
  - AccountIncomeStat

## 19. 辅助工具与长尾家族

- `TAccessoriesDlg`
- `TCheckBookDlg`
- `TDiaryDlgFm`
- `TDiaryUntFm`
- `TCalculatorDlg`
- `TCleanPriceFm`
- `TManageBillDateDlgFm`
- `TModifyBillDateDlgFm`
- `TRechargeDlgFm`
- `TPayrollIncomeDlgFm`
- `TAlsoCouponsDirectlyDlgFm`
- `TCouponsAlsoBuyCouponsDlgFm`
- `TDirectPaymentsDlgFm`
- `TBatchDirectPaymentsDlgFm`
- `TCollateralInDlgFm`
- `TBlockUpDlgFm`
- `TEditBankMoneyProductDlgFm`

## 20. UI 壳层与主题家族

- `TMainForm`
- `TMHFrame`
- `TChildForm`
- `TPageContrlFm`
- `TDropFm`
- `TSplashForm`
- `TTHEMEUIFM`
- `TRzFrmCustomizeToolbar`
- `TAIPanelDlg`
- `TAGACTIVE`
- `TAGFOCUSEDDARK`
- `TAGFOCUSEDGREY`
- `TAGNORMAL`
- `TAGSELECTED`

## 21. 视图框架与统计框架家族

- `TAdvanceSViewFrame`
- `TAlipayViewFrame`
- `TCardViewFrame`
- `TCashViewFrame`
- `TDeferredViewFrame`
- `TFixDepositsViewFrame`
- `TFixedDepositStatisticFrame`
- `THistoryProfitFrame`
- `TInvestmentChartFrame`
- `TMarketConstitutesFrame`
- `TMoneyInfoViewFrame`
- `TMoneyProductsViewFrame`
- `TMoneyStatisticFrame`
- `TMonthIncExpColumnChartFrame`
- `TPracStatisticFrame`
- `TStatisticFrame`
- `TStatisticGridFrame`
- `TStatisticTreeFrmae`
- `TUnearnedViewFrame`
- `TUsableMoneyChartFrame`
- `TViewFrame`

## 22. 选择器、日期与筛选辅助家族

- `TDropdownDate`
- `TSelectDateRangeDlgFm`
- `TSelectRepetitionFrequencyDlgFm`
- `TSelectSecuritiesCodeDlgFm`
- `TSelectThemeDlgFm`
- `TSelectTransTypeDlgFm`
- `TAmountScreeningFrame`

## 23. 编辑、调整与特殊对话框家族

- `TAdjustHeldDlgFm`
- `TChangePayModeDlgFm`
- `TEditAccountGroupFm`
- `TEditAssetBuyDlgFm`
- `TEditBudgetAmountDlgFm`
- `TEditBudgetCategoryDlgFm`
- `TEditCatgoryOrderDlgFm`
- `TEditCurrFundFm`
- `TEditFuturesGoodsFm`
- `TEditGoldFm`
- `TEditMarginContractDlgFm`
- `TEditNMarketBondFm`
- `TEditOpenFundFm`
- `TEditPreciousMetalStdGoodsFm`
- `TEditSecurityFm`
- `TEditSecurityPriceFm`
- `TEdtAcctGrpDlgFm`
- `TFixDepMatureDlgFm`
- `TMoneyMatureDlgFm`
- `TPRacBuyEditFrame`

## 24. 货币产品、理财与实盘/练习家族

- `TAdvanceAcctDlgFm`
- `TAdvanceTransDlgFm`
- `TLZCashDepDlgFm`
- `TMoneyBuyDlgFm`
- `TMoneyListFm`
- `TMoneyRedeemDlgFm`
- `TMoneyTransFm`
- `TMoneyTransFrame`
- `TPRacBuyInstallmentWizardDlg`
- `TPRacDlg`
- `TPRacListFm`
- `TPRacTransFm`
- `TPRacTransFrame`
- `TPRacTypeDlg`

## 25. 其它长尾支撑家族

- `TBatchAlsoCouponsDirectlyDlgFm`
- `TBuyFundPlanDlgFm`
- `TCalcuFm`
- `TCashCardDlgFm`
- `TConsoleFm`
- `TCreateBudgetDlgFm`
- `TCustomerDlgFm`
- `TCustomNavigationAcctDlgFm`
- `TDrawalCardDlgFm`
- `TFeeSetForm`
- `TFixedDepositTransFm`
- `TFMCustomDialog`
- `TFMIncExpCaptionForm`
- `TInformationDlgFm`
- `TInvestFeeDlgFm`
- `TInvestmentListFm`
- `TLifeThemeFm`
- `TNewAcctTypeDlgFm`
- `TNewBlockUpDlg`
- `TNewDebtBorrowDlgFm`
- `TNewRecTransDlgFm`
- `TNewThemeDlgFm`
- `TNormalPlanDlgFm`
- `TParentPlanDlgFm`
- `TPrepExpeAcctDlgFm`
- `TRepaymentTableFrame`
- `TShortSellingDlgFm`
- `TSoftIndexCenterForm`
- `TSortSoftIndexCenterDlgFm`
- `TTransFrame`
- `TTransListTemplateFrame`

## 26. 当前意义

这份家族索引说明：

- 原软件的功能面已经远超“个人记账”最小集。
- 任何 Rust 重构若要达到“功能一致”，都必须至少保留：
  - 通用收支
  - 账户体系
  - 投资扩展域
  - 报表分析中心
  - 预算/提醒/规划/目标
  - 同步与导入导出
