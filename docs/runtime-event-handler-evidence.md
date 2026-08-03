# MoneyHome8 全量运行时事件处理器证据

本文件由 `tools/summarize_runtime_event_handlers.py` 从隔离运行副本的 Delphi published RTTI 和全部运行时 DFM 生成。

## 1. 覆盖摘要

- 运行时窗体：`460` 个
- 含事件窗体：`380` 个
- DFM 事件绑定：`2332` 条
- 按窗体去重处理器：`2000` 个
- 直接定位到当前类代码：`1944` 个
- 沿真实父类链定位：`7` 个
- 已定位代码合计：`1951` 个
- 唯一同名候选：`3` 个
- 多个同名候选：`5` 个
- 完全未定位：`41` 个
- 有事件但无可执行 VMT 的资源窗体：`3` 个，涉及 `48` 个处理器
- published 方法：`2761` 个
- 已反汇编代码入口：`1944` 个
- 含字符串引用处理器：`431` 个
- 空实现处理器：`8` 个

## 2. 按业务域覆盖

| 业务域 | 窗体 | 事件绑定 | 去重处理器 | 当前类 | 父类链 | 唯一同名 | 多同名 | 未定位 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| accounts_master_data | 41 | 233 | 225 | 225 | 0 | 0 | 0 | 0 |
| auth_sync_external | 5 | 30 | 26 | 26 | 0 | 0 | 0 | 0 |
| bonds | 15 | 70 | 49 | 49 | 0 | 0 | 0 | 0 |
| debts_credit | 54 | 187 | 156 | 154 | 2 | 0 | 0 | 0 |
| financial_products | 19 | 58 | 55 | 54 | 1 | 0 | 0 | 0 |
| foreign_exchange | 9 | 23 | 22 | 21 | 1 | 0 | 0 | 0 |
| funds | 29 | 170 | 128 | 125 | 2 | 1 | 0 | 0 |
| futures_metals | 31 | 144 | 129 | 129 | 0 | 0 | 0 | 0 |
| import_export | 7 | 77 | 72 | 43 | 0 | 2 | 3 | 24 |
| insurance_social | 16 | 39 | 34 | 34 | 0 | 0 | 0 | 0 |
| investment_shared | 6 | 18 | 18 | 18 | 0 | 0 | 0 | 0 |
| major_tangible_assets | 29 | 120 | 111 | 111 | 0 | 0 | 0 | 0 |
| margin_financing | 22 | 100 | 82 | 82 | 0 | 0 | 0 | 0 |
| planning_budget_goal | 42 | 171 | 153 | 153 | 0 | 0 | 0 | 0 |
| reports | 28 | 46 | 31 | 31 | 0 | 0 | 0 | 0 |
| securities | 21 | 146 | 106 | 105 | 1 | 0 | 0 | 0 |
| shared_infrastructure | 19 | 101 | 89 | 78 | 0 | 0 | 0 | 11 |
| system_shell | 15 | 226 | 171 | 171 | 0 | 0 | 0 | 0 |
| tools_longtail | 14 | 101 | 89 | 89 | 0 | 0 | 0 | 0 |
| transactions | 38 | 272 | 254 | 246 | 0 | 0 | 2 | 6 |

## 3. 完全未定位处理器

| 资源 | 类 | 标题 | 未定位处理器 |
|---|---|---|---|
| `TCASHWITHDRAWDLGFM` | `TCashWithDrawDlgFm` | 取款 | chbAllClick；edtDrawAmountExit；selDrawAcctChange；selDrawAcctCloseUp；selDrawAcctNewAccountClick；selFeeAcctNewAccountClick |
| `TIMPORTJIAOGEDANDLGFM` | `TImportJiaoGedanDlgFm` | 导入股票交割单 | btnAutoDiscernClick；btnPasteDataClick；btnProgramDeleteClick；btnProgramSaveClick；btnSignClick；chkShowProgramDetailedClick；ddlProgramListCloseUp；ddlSecuAcctCloseUp；ddlSecuAcctNewAccountClick；miCancelSignClick；miSignClick；miUpdateCodeClick；miUpdateTagClick；miUpdateTransTypeClick；pnlStep2Resize；rbOnClick；tl1ColumnDateEditButtonClick；tl1ColumnSecuCodeEditButtonClick；tl1ColumnTagButtonClick；tl1ColumnTransTypeEditButtonClick；tl1Edited；tl1Editing；tl1KeyDown；tl1KeyPress |
| `TRZFRMCUSTOMIZETOOLBAR` | `TRzFrmCustomizeToolbar` | Customize Toolbar | BtnMoveDownClick；BtnMoveUpClick；CbxTextOptionsClick；ListBoxDrawItem；LstControlsChange；LstControlsClick；LstControlsDragDrop；LstControlsDragOver；LstControlsEndDrag；LstControlsMouseDown；Timer1Timer |

## 4. 高价值业务窗体代码覆盖

| 资源 | 标题 | 业务域 | 绑定 | 当前类 | 父类链 | 未匹配 |
|---|---|---|---:|---:|---:|---:|
| `TTRANSFRAME` |  | transactions | 43 | 41 | 0 | 0 |
| `TSECURITYLISTFM` | 证券资料 | securities | 40 | 26 | 0 | 0 |
| `TOPENFUNDSLISTFM` | 开放式基金列表 | funds | 28 | 24 | 0 | 1 |
| `TIMPORTPREVIEWFM` | 导入预览 | import_export | 18 | 17 | 0 | 0 |
| `TTRANSFERLISTTEMPLATEFRAME` |  | transactions | 16 | 16 | 0 | 0 |
| `TPLANLISTDLG` | 财务计划和提醒 | planning_budget_goal | 15 | 15 | 0 | 0 |
| `TTRANSLISTTEMPLATEFRAME` |  | transactions | 15 | 15 | 0 | 0 |
| `TBUDGETLISTFM` | 预算 | planning_budget_goal | 16 | 14 | 0 | 0 |
| `TEDITBUDGETAMOUNTDLGFM` | 预算金额设置 | planning_budget_goal | 14 | 14 | 0 | 0 |
| `TFUNDCONVERTDLGFM` | 开放式基金转换 | funds | 25 | 13 | 0 | 0 |
| `TREPORTFM` | ReportFm | reports | 13 | 13 | 0 | 0 |
| `TDEBTINVESTMENTLOANDLGFM` | 网贷借出 | debts_credit | 20 | 11 | 0 | 0 |
| `TCURRFUNDSLISTFM` | 货币基金列表 | funds | 12 | 11 | 0 | 0 |
| `TNEWDEBTBORROWDLGFM` | 借入、借出 | debts_credit | 12 | 11 | 0 | 0 |
| `TFINANCIALDIAGNOSISFM` | 财务诊断 | planning_budget_goal | 11 | 11 | 0 | 0 |
| `TFUNDBUYDLGFM` | 开放式基金申购 | funds | 14 | 10 | 0 | 0 |
| `TFUNDSELLDLGFM` | 开放式基金赎回 | funds | 15 | 9 | 0 | 0 |
| `TFINANCIALPLANNINGCENTERFM` | 财务规划 | planning_budget_goal | 10 | 8 | 0 | 0 |
| `TIMPORTCATEGORYDLGFM` | 替换收支项目 | import_export | 8 | 8 | 0 | 0 |
| `TIMPORTTHEMEDLGFM` | 主题数据设置 | import_export | 8 | 8 | 0 | 0 |
| `TSYNCUSERDATAFM` | 同步 | auth_sync_external | 8 | 8 | 0 | 0 |
| `TCREDITACCTDLGFM` | 信用卡账户 | debts_credit | 9 | 7 | 0 | 0 |
| `TGOALCENTERFM` | 财务目标 | planning_budget_goal | 7 | 7 | 0 | 0 |
| `TFUNDMARKBUYDLGFM` | 新基金认购确认 | funds | 9 | 6 | 0 | 0 |
| `TINSURETRANSFRAME` |  | insurance_social | 6 | 6 | 0 | 0 |
| `TSECURITYSTATISTICFRAME` |  | securities | 6 | 6 | 0 | 0 |
| `TFUNDORDERBUYDLGFM` | 新基金认购 | funds | 8 | 5 | 0 | 0 |
| `TCURRFUNDCONVERTFM` | 货币基金转换 | funds | 7 | 5 | 0 | 0 |
| `TADVANCETRANSDLGFM` | 预付 | debts_credit | 5 | 5 | 0 | 0 |
| `TBUYFUNDPLANDLGFM` | 基金定投计划 | planning_budget_goal | 5 | 5 | 0 | 0 |
| `TCASHTRANSFRAME` |  | transactions | 5 | 5 | 0 | 0 |
| `TCREDITCARDTRANSFRAME` |  | debts_credit | 5 | 5 | 0 | 0 |
| `TDCURRCREDITACCTDLGFM` | 双币信用卡 | debts_credit | 5 | 5 | 0 | 0 |
| `TEDITSECURITYFM` | 股票 | securities | 5 | 5 | 0 | 0 |
| `TFINANCIALCALENDARDLG` | 财务日历 | planning_budget_goal | 5 | 5 | 0 | 0 |
| `TPAYABLEMONEYTRANSDLGFM` | 预收 | debts_credit | 5 | 5 | 0 | 0 |
| `TTRANSFERTEMPLATEDLGFM` | 批量转账 | transactions | 5 | 5 | 0 | 0 |
| `TREPORTOPTIONDLGFM` | 筛选 | reports | 13 | 4 | 0 | 0 |
| `TCREATEBUDGETDLGFM` | 预算 | planning_budget_goal | 10 | 4 | 0 | 0 |
| `TDEBTEQUITYSWAPTRANSDLGFM` | 债转股 | margin_financing | 6 | 4 | 0 | 0 |
| `TNEWACCTWIZARDTWOCURRCREDITDLGFM` | 双币信用卡账户 | debts_credit | 6 | 4 | 0 | 0 |
| `TEXPORTDATAFM` | 数据导出 | import_export | 5 | 4 | 0 | 0 |
| `TCLAIMSDEBTSTATISTICFRAME` |  | debts_credit | 4 | 4 | 0 | 0 |
| `TCURRFUNDBUYDLGFM` | 货币基金申购 | funds | 4 | 4 | 0 | 0 |
| `TDEBTRECDLGFM` | 收回 | debts_credit | 4 | 4 | 0 | 0 |
| `TDEBTRETURNDLGFM` | 返还 | debts_credit | 4 | 4 | 0 | 0 |
| `TEDITBUDGETCATEGORYDLGFM` | 选择预算收支项目 | planning_budget_goal | 4 | 4 | 0 | 0 |
| `TEDITCURRFUNDFM` | 货币基金 | funds | 4 | 4 | 0 | 0 |
| `TEDITOPENFUNDFM` | 开放式基金 | funds | 4 | 4 | 0 | 0 |
| `TFOREIGNTRANSFRAME` |  | foreign_exchange | 4 | 4 | 0 | 0 |
| `TOPENFUNDSTATISTICFRAME` |  | funds | 4 | 4 | 0 | 0 |
| `TTRANSDLGFM` | TransDlgFm | transactions | 4 | 4 | 0 | 0 |
| `TFPASSETPURCHASEPLANINFOFM` | 资产购置 | planning_budget_goal | 7 | 3 | 0 | 0 |
| `TFUNDREINVESTDLGFM` | 分红再投资 | funds | 5 | 3 | 0 | 0 |
| `TFUNDSPLITDLGFM` | 基金拆分 | funds | 5 | 3 | 0 | 0 |
| `TNEWACCTWIZARDCREDITCARDDLGFM` | 信用卡账户 | debts_credit | 5 | 3 | 0 | 0 |
| `TBACKUPBOOKFM` | 备份账簿 | system_shell | 4 | 3 | 0 | 0 |
| `TDEBTINVESTMENTSELLTRANSDLGFM` | 网贷转让 | debts_credit | 4 | 3 | 0 | 0 |
| `TDEBTINVESTMENTWITHDRAWTRANSDLGFM` | 网贷收回 | debts_credit | 4 | 3 | 0 | 0 |
| `TIMPORTDATAFM` | 导入数据 | import_export | 4 | 3 | 0 | 0 |
| `TCURRFUNDSELLDLGFM` | 货币基金赎回 | funds | 3 | 3 | 0 | 0 |
| `TCURRFUNDSTATISTICFRAME` |  | funds | 3 | 3 | 0 | 0 |
| `TDEBTINVESTMENTSTATISTICFRAME` |  | debts_credit | 3 | 3 | 0 | 0 |
| `TEDITSECURITYPRICEFM` | EditSecurityPriceFm | securities | 3 | 3 | 0 | 0 |
| `TGOALSAVEFM` | 财务目标 | planning_budget_goal | 3 | 3 | 0 | 0 |
| `TIMPORTSELECTDLGFM` | 导入数据 | import_export | 3 | 3 | 0 | 0 |
| `TNEWRECTRANSDLGFM` | 余额调整 | transactions | 3 | 3 | 0 | 0 |
| `TXFERPLANDLGFM` | 转账计划 | planning_budget_goal | 3 | 3 | 0 | 0 |
| `TCLAIMSDEBTTRANSFRAME` |  | debts_credit | 4 | 2 | 0 | 0 |
| `TCURRFUNDACCTDLGFM` | 货币基金账户 | funds | 3 | 2 | 0 | 0 |
| `TNMARKETDEBTACCTDLGFM` | 债券账户 | bonds | 3 | 2 | 0 | 0 |
| `TOPENFUNDACCTDLGFM` | 开放式基金账户 | funds | 3 | 2 | 0 | 0 |
| `TSECURITYACCTDLGFM` | 证券账户 | securities | 3 | 2 | 0 | 0 |
| `TASSETSTRANSFRAME` |  | major_tangible_assets | 2 | 2 | 0 | 0 |
| `TCLAIMSDEBTSCHARTFRAME` |  | debts_credit | 2 | 2 | 0 | 0 |
| `TCLAIMSDEBTSCONSTITUTESFRAME` |  | debts_credit | 2 | 2 | 0 | 0 |
| `TCREDITCARDSTATISTICFRAME` |  | debts_credit | 2 | 2 | 0 | 0 |
| `TCURRFUNDREINVESTDLGFM` | 货币基金红利再投资 | funds | 2 | 2 | 0 | 0 |
| `TDEBTADJUSTDLGFM` | 坏账 | debts_credit | 2 | 2 | 0 | 0 |
| `TDEBTBORROWDLGFM` | 借入 | debts_credit | 2 | 2 | 0 | 0 |
| `TDEBTINVESTMENTBADTRANSDLGFM` | 网贷坏账 | debts_credit | 2 | 2 | 0 | 0 |
| `TDEBTINVESTMENTPAYOBJECTFRAME` |  | debts_credit | 2 | 2 | 0 | 0 |
| `TDEBTINVESTMENTPAYTABLEFRAME` |  | debts_credit | 2 | 2 | 0 | 0 |
| `TDEBTINVESTMENTREWARDTRANSDLGFM` | 网贷投资奖励 | debts_credit | 2 | 2 | 0 | 0 |
| `TDEBTINVESTMENTTRANSFRAME` |  | debts_credit | 2 | 2 | 0 | 0 |
| `TDEBTLENDDLGFM` | 借出 | debts_credit | 2 | 2 | 0 | 0 |
| `TEQUITYSECURITIESLENDINGDLGFM` | 融券权益 | margin_financing | 2 | 2 | 0 | 0 |
| `TFUNDINTERESTDLGFM` | 基金现金红利 | funds | 2 | 2 | 0 | 0 |
| `TOPENFUNDREMINDDLG` | 开放式基金价格提醒 | planning_budget_goal | 2 | 2 | 0 | 0 |
| `TPRACTRANSFRAME` |  | major_tangible_assets | 2 | 2 | 0 | 0 |
| `TRESTOREBOOKFM` | 还原账簿 | system_shell | 2 | 2 | 0 | 0 |
| `TRPTBSSTATFRM` | 资产负债表 | reports | 2 | 2 | 0 | 0 |
| `TSECURITYCODECONVERTFM` | 代码变更 | securities | 2 | 2 | 0 | 0 |
| `TSECURITYREMINDDLG` | 证券市价提醒 | planning_budget_goal | 2 | 2 | 0 | 0 |
| `TSELECTSECURITIESCODEDLGFM` | 选择证券 | securities | 2 | 2 | 0 | 0 |
| `TRPTSTOCKTRENDFM` | 证券市值大势图 | reports | 5 | 1 | 0 | 0 |
| `TRPTFUNDTRENDFM` | 开放式基金市值大势图 | reports | 3 | 1 | 0 | 0 |
| `TCURRFUNDVIEWFRAME` |  | funds | 2 | 1 | 1 | 0 |
| `TNEWACCTWIZARDCURRFUNDDLGFM` | 货币基金账户 | funds | 2 | 1 | 0 | 0 |
| `TNEWACCTWIZARDNMARKETDEBTDLGFM` | 债券账户 | bonds | 2 | 1 | 0 | 0 |
| `TNEWACCTWIZARDOPENFUNDDLGFM` | 开放式基金账户 | funds | 2 | 1 | 0 | 0 |
| `TNEWACCTWIZARDSECURITYDLGFM` | 上市证券账户 | securities | 2 | 1 | 0 | 0 |
| `TOPENFUNDVIEWFRAME` |  | funds | 2 | 1 | 1 | 0 |
| `TBUDGETCOPYDLGFM` | 复制预算金额 | planning_budget_goal | 1 | 1 | 0 | 0 |
| `TCREDITREMINDDLG` | 信用卡透支额提醒 | planning_budget_goal | 1 | 1 | 0 | 0 |
| `TCURRFUNDTRANSFRAME` |  | funds | 1 | 1 | 0 | 0 |
| `TDEBTINVESTMENTVIEWFRAME` |  | debts_credit | 1 | 1 | 0 | 0 |
| `TDEBTRATESETDLG` | 借贷款账户利率调整 | debts_credit | 1 | 1 | 0 | 0 |
| `TFILTERTRANSFRAME` |  | transactions | 1 | 1 | 0 | 0 |
| `TFUTURESTRANSFRAME` |  | futures_metals | 1 | 1 | 0 | 0 |
| `TGOALACCTLISTDLG` | 财务目标账户余额列表 | planning_budget_goal | 1 | 1 | 0 | 0 |
| `TGOLDTRANSFRAME` |  | futures_metals | 1 | 1 | 0 | 0 |
| `TINCEXPPLANDLGFM` | 收支计划 | planning_budget_goal | 1 | 1 | 0 | 0 |
| `TMARGINTRANSFRAME` |  | margin_financing | 1 | 1 | 0 | 0 |
| `TMARKETDEBTSTATISTICFRAME` |  | bonds | 1 | 1 | 0 | 0 |
| `TMARKETDEBTTRANSFRAME` |  | bonds | 1 | 1 | 0 | 0 |
| `TMONEYTRANSFRAME` |  | financial_products | 1 | 1 | 0 | 0 |
| `TNEWACCTWIZARDDEBTINVESTMENTDLGFM` | 网贷 | debts_credit | 1 | 1 | 0 | 0 |
| `TOPENFUNDTRANSFRAME` |  | funds | 1 | 1 | 0 | 0 |
| `TPARENTPLANDLGFM` | ParentPlanDlgFm | planning_budget_goal | 1 | 1 | 0 | 0 |
| `TPLANINSUREPAYFEEDLGFM` | 缴费计划 | planning_budget_goal | 1 | 1 | 0 | 0 |
| `TPRECIOUSMETALSTDTRANSFRAME` |  | futures_metals | 1 | 1 | 0 | 0 |
| `TRPTCASHWASTEFM` | 现金流表 | reports | 1 | 1 | 0 | 0 |
| `TRPTCREDITDEBTSTATFM` | 债权债务表 | reports | 1 | 1 | 0 | 0 |
| `TRPTFUNDSAVAILABLEFM` | 可用资金表 | reports | 1 | 1 | 0 | 0 |
| `TRPTINCEXPZSTOVFM` | 收支走势图 | reports | 1 | 1 | 0 | 0 |
| `TRPTINCOMESTATFRM` | 日常收支表 | reports | 1 | 1 | 0 | 0 |
| `TRPTINVESTVIEWFM` | 投资一览表 | reports | 1 | 1 | 0 | 0 |
| `TRPTMONTHAVERAGEINCEXPFM` | 月平均收支表 | reports | 1 | 1 | 0 | 0 |
| `TRPTOPENFUNDINVESTFM` | 开放式基金投资一览表 | reports | 1 | 1 | 0 | 0 |
| `TRPTSECURITINVESTFM` | 证券投资一览表 | reports | 1 | 1 | 0 | 0 |
| `TRPTYEARINCEXPFORM` | 收支统计表 | reports | 1 | 1 | 0 | 0 |
| `TSECURITYTRANSFRAME` |  | securities | 1 | 1 | 0 | 0 |
| `TSELECTTRANSTYPEDLGFM` | 选择交易类型 | transactions | 1 | 1 | 0 | 0 |
| `TSOCIALSECURITYSTATISTICFRAME` |  | insurance_social | 1 | 1 | 0 | 0 |
| `TSYNCUSERREGISTERFM` | 注册同步账号 | auth_sync_external | 1 | 1 | 0 | 0 |
| `TIMPORTJIAOGEDANDLGFM` | 导入股票交割单 | import_export | 31 | 0 | 0 | 29 |
| `TCLAIMSDEBTCONTAINER` |  | debts_credit | 10 | 0 | 2 | 0 |
| `TASSETTRANSFM` | 重大资产交易明细 | major_tangible_assets | 0 | 0 | 0 | 0 |
| `TCASHTRANSFM` | 现金交易列表 | transactions | 0 | 0 | 0 | 0 |
| `TCLAIMSTRANSFM` | 债权债务交易明细 | debts_credit | 0 | 0 | 0 | 0 |
| `TCREDITCARDTRANSFM` | 信用卡交易明细 | debts_credit | 0 | 0 | 0 | 0 |
| `TCURRENTTRANSFM` | 活期存款交易明细 | transactions | 0 | 0 | 0 | 0 |
| `TCURRFUNDMARKETCONSTITUTESFRAME` |  | funds | 0 | 0 | 0 | 0 |
| `TCURRFUNDTRANSFM` | 货币基金交易明细 | funds | 0 | 0 | 0 | 0 |
| `TDEBTINVESTMENTACCTDLGFM` | 网贷 | debts_credit | 0 | 0 | 0 | 0 |
| `TDEBTINVESTMENTACCTLISTFRAME` |  | debts_credit | 0 | 0 | 0 | 0 |
| `TDEBTINVESTMENTTRANSFM` | 网贷账户交易明细 | debts_credit | 0 | 0 | 0 | 0 |
| `TDEBTSACCTDLGFM` | 应收、应付 | debts_credit | 0 | 0 | 0 | 0 |
| `TFIXEDDEPOSITTRANSFM` | 定期存单 | financial_products | 0 | 0 | 0 | 0 |
| `TFOREIGNTRANSFM` | 外汇交易明细 | foreign_exchange | 0 | 0 | 0 | 0 |
| `TFUTURESTRANSFM` | 期货账户交易明细 | futures_metals | 0 | 0 | 0 | 0 |
| `TGOLDTRANSFM` | 贵金属交易明细 | futures_metals | 0 | 0 | 0 | 0 |
| `TINSURETRANSFM` | 保险交易明细 | insurance_social | 0 | 0 | 0 | 0 |
| `TMARGINTRANSFM` | 融资融券账户交易明细 | margin_financing | 0 | 0 | 0 | 0 |
| `TMARKETDEBTTRANSFM` | 债券交易明细 | bonds | 0 | 0 | 0 | 0 |
| `TMONEYTRANSFM` | 银行理财产品交易明细 | financial_products | 0 | 0 | 0 | 0 |
| `TNORMALPLANDLGFM` | 提醒 | planning_budget_goal | 0 | 0 | 0 | 0 |
| `TOPENFUNDTRANSFM` | 开放式基金交易明细 | funds | 0 | 0 | 0 | 0 |
| `TPRACTRANSFM` | 物品交易明细 | major_tangible_assets | 0 | 0 | 0 | 0 |
| `TPRECIOUSMETALSTDTRANSFM` | 贵金属TD账户交易明细 | futures_metals | 0 | 0 | 0 | 0 |
| `TRPTACCOUNTINCOMESTATFRM` | 账户日常收支表 | reports | 0 | 0 | 0 | 0 |
| `TRPTDEBTINVESTMENTINVESTYKFORM` | 网贷盈亏一览表 | reports | 0 | 0 | 0 | 0 |
| `TRPTEXCHANGE6FM` | 外汇交易一览表 | reports | 0 | 0 | 0 | 0 |
| `TRPTFINANCIALPRODUCTSFM` | 银行理财产品收益率表 | reports | 0 | 0 | 0 | 0 |
| `TRPTINCEXPCOMPAREFM` | 两段时间收支对比表 | reports | 0 | 0 | 0 | 0 |
| `TRPTINCOMELISTFM` | 日常收支明细表 | reports | 0 | 0 | 0 | 0 |
| `TRPTINVESTINCOMEFM` | 投资收益一览表 | reports | 0 | 0 | 0 | 0 |
| `TRPTINVESTMENTPERFORMANCESTATFM` | 投资收益率统计表 | reports | 0 | 0 | 0 | 0 |
| `TRPTMONTHASSETFM` | 月资产走势图 | reports | 0 | 0 | 0 | 0 |
| `TRPTOPENFUNDINVESTLOSSFM` | 开放式基金费用及盈亏一览表 | reports | 0 | 0 | 0 | 0 |
| `TRPTSECURITINVESTLOSSFM` | 证券费用及盈亏一览表 | reports | 0 | 0 | 0 | 0 |
| `TRPTTAGINCOMESTATFRM` | 标签日常收支表 | reports | 0 | 0 | 0 | 0 |
| `TSECURITYTRANSFM` | 上市证券交易列表 | securities | 0 | 0 | 0 | 0 |
| `TSOCIALSECURITYTRANSFM` | 社会保险账户交易明细 | insurance_social | 0 | 0 | 0 | 0 |
| `TTHIRDDEPOSITSTRANSFM` | 支付宝交易明细 | transactions | 0 | 0 | 0 | 0 |
| `TTRANSACTIONPLANDLGFM` | 交易计划 | planning_budget_goal | 0 | 0 | 0 | 0 |

## 5. 空实现处理器

| 资源 | 标题 | 处理器 | 代码 RVA |
|---|---|---|---:|
| `TCONSOLEFM` | 控制台 | `miClearClick` | `0x45adbc` |
| `TDIALOGFORM` | DialogForm | `FormPaint` | `0x513d40` |
| `TDIALOGFORM` | DialogForm | `FormShow` | `0x513d44` |
| `TFUTURESCONTRACTLISTFM` | 期货合约列表 | `FormShow` | `0x334b5c` |
| `TMAINFORM` | MainForm | `pnlLeftBarDblClick` | `0x459890` |
| `TPARENTPLANDLGFM` | ParentPlanDlgFm | `btnSaveClick` | `0x2bcb8c` |
| `TSTATISTICFRAME` |  | `actExportExecute` | `0x349694` |
| `TSTATISTICFRAME` |  | `actPrintExecute` | `0x349698` |

## 6. 证据边界

- `直接命中` 表示处理器名称存在于当前窗体类的 Delphi published 方法表，代码地址可直接证明。
- `父类链` 表示通过当前类 VMT 的 `vmtParent` 逐级定位到真实祖先类方法表。
- `同名候选` 是父类链仍未覆盖时在其它类中发现的同名方法，只用于检索，不能证明继承或实现归属。
- `resource_only_no_vmt` 表示资源中存在窗体和事件绑定，但当前主程序映像没有该类的可执行 VMT；应按未链接、未启用或历史资源候选处理，并由动态验证决定是否进入重构范围。
- 字符串和调用引用可用于定位校验、提示、文件、网络和数据访问路径，但不能单独证明运行时分支一定执行。
- 动态页面、真实输入输出和数据副作用仍按 `runtime-validation-scenarios.md` 校准。
