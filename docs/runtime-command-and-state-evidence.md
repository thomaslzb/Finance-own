# MoneyHome8 运行时命令与状态证据

本文档由 `runtime-dfm-all-forms.json` 自动生成，记录旧程序的命令、事件、快捷键、静态选项和设计时初始状态。

## 1. 证据边界

- 扫描窗体：`460` 个
- 命令/交互控件：`1407` 个
- 包含命令证据的重点业务窗体：`142` 个
- Markdown 摘要窗体：`52` 个
- 快捷键：`36` 个
- 明确初始禁用命令：`82` 个
- 明确初始隐藏命令：`42` 个
- 明确默认选中命令：`74` 个

事件名和设计时属性属于直接证据。`Enabled=False` 只能证明初始禁用，不能单独证明具体启用条件；动态菜单、点击结果和错误提示仍需运行验证。

## 2. 关键状态规则

- 财务记录的修改、删除、查找动作在 DFM 中初始禁用；Rust 版应在存在有效选中记录或可查询数据时再启用。具体条件需运行校准。
- 通用报表的导出报表、打印预览初始禁用；Rust 版应在报表结果成功生成后启用。
- 证券趋势图默认选中资产总值、证券市值、资金余额、上证指数和深证成指。
- 基金趋势图默认选中资产总值、基金市值和资金余额。
- 复制预算金额对一月至十二月全部默认选中，允许用户按月份取消复制范围。
- 导入预览的“导入选中的记录”和从剪贴板导入动作初始禁用，必须由有效输入或选择状态驱动启用。
- 标签页的移出、转移、快速加入、修改、删除和隐藏动作初始禁用，说明它们依赖当前标签或记录选择。
- 今日提醒直接提供执行、跳过、今日不再提醒和打开账簿时自动弹出四类状态动作。

## 3. 重点窗体命令目录

| 窗体 | 命令、事件与初始状态 | 静态选项 |
| --- | --- | --- |
| 账户中心 (`TACCOUNTMANAGERFM`) | 显示选项 [OnClick=btnGroupTypeClick]；新增账户 [OnClick=btnNewClick]；所有账户 [OnClick=btnFilterTypeClick]；新增账户组 [OnClick=btnNewGroupClick]；操作 [OnClick=btnOperateClick]；修改账户组 [OnExecute=actEditAccountGroupExecute]；删除账户组 [OnExecute=actDeleteAccountGroupExecute]；修改账户 [OnExecute=actEditAccountExecute]；删除账户 [OnExecute=actDeleteAccountExecute]；注销账户 [OnExecute=actDisableAccountExecute]；隐藏账户 [OnExecute=actHideAccountExecute]；加入标签 [OnExecute=actAddThemeExecute]；显示到期账户 [OnExecute=actShowFinishAccountExecute]；显示隐藏账户 [OnExecute=actShowHiddenAccountExecute]；显示注销账户 [OnExecute=actShowWriteOffAccountExecute]；显示已结清的债权债务账户 [OnExecute=actShowOverDebtAcctExecute]；按账户类型查看 [OnExecute=actGroupByAcctTypeExecute]；按自定分组查看 [OnExecute=actGroupByAcctGroupExecute]；添加账户 [OnExecute=actAddSelectAccountToGroupExecute]；pmAccount [OnPopup=pmAccountPopup]；余额调整 [OnClick=miBalaClick]；属于账户组 [OnClick=miAccountGroupClick]；新增账户组 [OnClick=pmNewGroupClick]；查看附件 [OnClick=miAccessoriesClick]；添加删除附件 [OnClick=mmiAddAccessClick]；pmGroup [OnPopup=pmGroupPopup]；设为软件首页 [OnClick=miSetDefaultPageClick] |  |
| 账户余额提醒 (`TACCTBALAREMINDDLG`) | 保存 [OnClick=btnSaveNewClick] |  |
| TASSETSSTATISTICFRAME (`TASSETSSTATISTICFRAME`) | 删除 [OnClick=miDeleteAssetClick]；当前持有资产；所有记录过的资产 |  |
| 复制预算金额 (`TBUDGETCOPYDLGFM`) | 九月 [默认选中]；十月 [默认选中]；十一月 [默认选中]；十二月 [默认选中]；八月 [默认选中]；七月 [默认选中]；六月 [默认选中]；五月 [默认选中]；四月 [默认选中]；三月 [默认选中]；二月 [默认选中]；一月 [默认选中]；确定 [OnClick=btnOkClick] |  |
| 预算 (`TBUDGETLISTFM`) | 新增预算 [OnClick=btnNewClick]；mwAdjustYear [OnClick=mwAdjustYearClick]；mwAdjustMonth [OnClick=mwAdjustYearClick]；mwAdjustSeason [OnClick=mwAdjustYearClick]；预算设置 [OnClick=btnUpdateClick]；btnDisplayType [OnClick=btnDisplayTypeClick]；btnCloseTransList [OnClick=btnCloseTransListClick]；知道了 [OnClick=btnKnowClick]；修改预算收支项目 [OnClick=miEditBudgetCategoryClick]；修改预算金额 [OnClick=miEditBudgetAmountClick]；修改预算信息 [OnClick=miEditBudgetClick]；删除预算 [OnClick=miDeleteBudgetClick]；导出文件 [OnClick=miExportClick]；修改 [OnClick=miModifyClick]；删除 [OnClick=miDeleteClick] |  |
| TCLAIMSDEBTSTATISTICFRAME (`TCLAIMSDEBTSTATISTICFRAME`) | 债权和债务 \| 忽略已完成款项 [OnClick=btnDisplayTypeClick]；删除 [OnClick=miDeleteAssetClick]；显示债权和债务；仅债权；仅债务；忽略已完成的款项 [OnClick=miIgnoreCompletedClick] |  |
| 预算 (`TCREATEBUDGETDLGFM`) | 月度 [OnClick=rbMonthClick]；季度 [OnClick=rbMonthClick]；年度 [OnClick=rbMonthClick]；自定义 [OnClick=rbMonthClick]；确定 [OnClick=btnSaveClick]；pnlAdvanced [OnClick=pnlAdvancedClick]；img1 [OnClick=pnlAdvancedClick]；imgStatus [OnClick=pnlAdvancedClick]；高级预算设置 [OnClick=pnlAdvancedClick] |  |
| TCREDITCARDSTATISTICFRAME (`TCREDITCARDSTATISTICFRAME`) | 导入 [OnClick=miImportClick]；显示最近3期已出账单；显示所有已出账单 |  |
| 信用卡透支额提醒 (`TCREDITREMINDDLG`) | 保存 [OnClick=btnSaveNewClick] |  |
| TCURRFUNDSTATISTICFRAME (`TCURRFUNDSTATISTICFRAME`) | 获取代码 [OnClick=btnUpdateDataClick]；BrowseGrid [OnDblClick=BrowseGridDblClick]；货币基金代码转换 [OnExecute=ActChangeCodeExecute]；当前持仓基金；所有交易过的基金 |  |
| TDEBTINVESTMENTSTATISTICFRAME (`TDEBTINVESTMENTSTATISTICFRAME`) | 收款表 [OnClick=btnPayTableClick]；BrowseGrid [OnDblClick=BrowseGridDblClick]；当前持有网贷；已完成网贷 |  |
| 预算金额设置 (`TEDITBUDGETAMOUNTDLGFM`) | 确定 [OnClick=btnSaveClick]；mwAdjustYear [OnClick=mwAdjustYearClick]；复制预算金额 [OnClick=btnCopyAmountClick]；导入最近12个月的收支金额 [OnClick=btnImportAmountClick]；pm1 [OnPopup=pm1Popup]；从其它年份复制预算金额 [OnClick=miCopyAmountFromYearClick]；复制选中单元格金额到其它列 [OnClick=miCopyCellAmountClick]；复制选中列金额到其它列 [OnClick=miCopyColumnAmountClick] |  |
| 选择预算收支项目 (`TEDITBUDGETCATEGORYDLGFM`) | 确定 [OnClick=btnSaveClick]；新增收支项目 [OnClick=btnCreateCategoryClick]；全选 [OnClick=btnSeletAllClick]；反选 [OnClick=btnSelectContraryClick] |  |
| 数据导出 (`TEXPORTDATAFM`) | BtnOk [OnClick=BtnOkClick]；确定 [OnClick=BtnOkClick]；浏览... [OnClick=btnBrowserClick]；导入时更新账户余额 [初始隐藏]；增加；删除并覆盖；数据选项 [OnDblClick=tsOptionsDblClick]；账户信息；交易信息；交易费率；记账模板；证券列表；提醒设置；物品历史价格；物品信息；计划日记；人员机构；贵金属；生活主题；理财目标；基金列表；历史汇率；债券列表；货币基金；货币信息；收支项目；收支预算；理财产品 |  |
| 财务诊断 (`TFINANCIALDIAGNOSISFM`) | 新增账户 [OnClick=btnCreateAccountClick]；btnInputDataType [OnClick=btnInputDataTypeClick]；资产性质设置 [OnClick=btnAssetPropertySettingsClick]；开始诊断 [OnClick=btnBeginClick]；调整财务数据 [OnClick=btnReturnClick]；定期；流动资产 [OnClick=miFixedDeposit_LiquidAssetClick]；投资资产 [OnClick=miFixedDeposit_InvestmentAssetClick]；货币基金；流动资产 [OnClick=miCurrFund_LiquidAssetClick]；投资资产 [OnClick=miCurrFund_InvestmentAssetClick] |  |
| 财务规划 (`TFINANCIALPLANNINGCENTERFM`) | 清除数据 [OnClick=btnClearDataClick] |  |
| TFIXEDDEPOSITSTATISTICFRAME (`TFIXEDDEPOSITSTATISTICFRAME`) | 所有 [OnClick=btnAcctGroupClick]；新增存单 [OnClick=btnCreateAcctClick]；删除 [OnClick=miDeleteAssetClick] |  |
| TFOREIGNSTATISTICFRAME (`TFOREIGNSTATISTICFRAME`) | 获取牌价 [OnClick=btnUpdateDataClick]；持有外汇调整；添加外汇牌价 [OnExecute=ActAddPriceExecute]；持有外汇调整；当前持有外汇；所有交易过的外汇 |  |
| TFUTURESSTATISTICFRAME (`TFUTURESSTATISTICFRAME`) | 获取合约价格 [OnClick=btnUpdateDataClick]；BrowseGrid [OnDblClick=BrowseGridDblClick]；添加合约价格 [OnExecute=ActAddPriceExecute]；证券代码变更 [初始隐藏]；期货品种设置 [OnClick=mmiFuturesGoodsClick]；当前持仓合约；所有交易过的合约 |  |
| 财务目标 (`TGOALCENTERFM`) | 新增目标 [OnClick=BtnAddClick]；设置 [OnClick=btnSettingClick]；显示已过期目标 [OnClick=miShowExpiredClick]；pmOperate [OnPopup=pmOperatePopup]；修改 [OnClick=miModifyClick]；删除 [OnClick=miDeleteClick] |  |
| 财务目标 (`TGOALSAVEFM`) | 保存 [OnClick=btnSaveClick]；全部账户 [OnClick=RCAllClick] |  |
| TGOLDSTATISTICFRAME (`TGOLDSTATISTICFRAME`) | 获取价格 [OnClick=btnUpdateDataClick]；BrowseGrid [OnDblClick=BrowseGridDblClick]；添加贵金属价格 [OnExecute=ActAddPriceExecute]；pmOperate [OnPopup=pmOperatePopup]；当前持仓贵金属；所有交易过的贵金属 |  |
| 替换收支项目 (`TIMPORTCATEGORYDLGFM`) | 查询记录 [OnClick=btnFilterClick]；确定替换 [OnClick=btnSaveExitClick] |  |
| 导入数据 (`TIMPORTDATAFM`) | BtnOk [OnClick=BtnOkClick]；浏览... [OnClick=btnBrowserClick]；双击此处全选/取消全选 [OnDblClick=OptionsGroupDblClick]；账户信息；人员机构；货币信息；收支项目；收支预算；计划日记；证券列表；基金列表；债券列表；交易信息；物品信息；交易费率；提醒设置；记账模板；生活主题；理财产品；贵金属；货币基金；历史汇率；物品历史价格；理财目标；确定 [OnClick=BtnOkClick] |  |
| 导入股票交割单 (`TIMPORTJIAOGEDANDLGFM`) | 粘贴 [OnClick=btnPasteDataClick]；删除方案 [OnClick=btnProgramDeleteClick]；方案另存为 [OnClick=btnProgramSaveClick]；显示方案详细内容 [OnClick=chkShowProgramDetailedClick]；制表符Tab [OnClick=rbOnClick; 默认选中]；空格 [OnClick=rbOnClick]；其它 [OnClick=rbOnClick]；自动识别 [OnClick=btnAutoDiscernClick]；以“列头文字”匹配 [默认选中]；以“列序号(第几列)”匹配；金额已包含后面的费用项；下一步 [OnClick=btnBeginClick]；确认导入 [OnClick=btnImportClick]；上一步 [OnClick=btnBackClick]；批量修改 [OnClick=btnUpdateClick]；关联新股申购 [OnClick=btnSignClick]；btnGainsLossesType；修改交易类型 [OnClick=miUpdateTransTypeClick]；修改证券代码 [OnClick=miUpdateCodeClick]；修改标签 [OnClick=miUpdateTagClick]；关联新股申购 [OnClick=miSignClick]；取消关联 [OnClick=miCancelSignClick] |  |
| 导入预览 (`TIMPORTPREVIEWFM`) | 导入选中的记录 [OnClick=btnImportClick; 初始禁用] |  |
| 导入数据 (`TIMPORTSELECTDLGFM`) | mwIconList [OnClick=mwIconListClick]；从文件导入 [OnClick=btnImportClick]；从剪贴板导入 [OnClick=btnImportFromClipboardClick; 初始禁用] |  |
| 主题数据设置 (`TIMPORTTHEMEDLGFM`) | 设置 [OnClick=btnSaveExitClick]；查询记录 [OnClick=btnFilterClick] |  |
| 标签 (`TLIFETHEMEFM`) | 查找 [OnClick=btnFindClick]；批量操作 [OnClick=btnBulkActionClick]；其它 [OnClick=btnOtherClick]；DBGrid [OnDblClick=DBGridDblClick]；操作 [OnClick=btnSettingClick]；myTagList [OnClick=myTagListClick]；从当前主题中移出 [OnExecute=actDeleteTagExecute; 初始禁用]；从所有主题中移出 [OnExecute=actDeleteAllExecute; 初始禁用]；从当前主题转移到... [OnExecute=actMoveTagExecute; 初始禁用]；从所有主题转移到... [OnExecute=actMoveAllTagExecute; 初始禁用]；快速加入主题 [OnExecute=actAddTagExecute; 初始禁用]；修改主题 [OnExecute=actModifyExecute; 初始禁用]；删除主题 [OnExecute=actDeleteExecute; 初始禁用]；隐藏主题 [OnExecute=actHideExecute; 初始禁用]；新增主题 [OnExecute=actAddExecute]；pmSetting [OnPopup=pmSettingPopup]；标签排序 [OnClick=miEditTagsOrderClick]；查找 [OnClick=miFindClick]；显示隐藏标签 [OnClick=mmiViewClick]；批量设置标签 [OnClick=mmiBatchTagsClick]；设为软件首页 [OnClick=miSetHomePageClick]；导出 [OnClick=miExportTagClick]；查找 [OnClick=mmiFindClick]；筛选 [OnClick=mmiFilterClick]；放弃筛选 [OnClick=miClearFilterClick; 初始隐藏]；移出主题；转移到；pmExport [OnPopup=pmExportPopup]；导出 [OnClick=N11Click]；打印 [OnClick=N12Click] |  |
| 限额提醒 (`TLIMITREMINDDLG`) | 新增提醒；操作 [OnClick=btnCustomClick]；TreeList [OnDblClick=TreeListDblClick]；新增账户余额提醒 [OnClick=N1Click]；新增信用卡透支额提醒 [OnClick=N2Click]；新增证券市价提醒 [OnClick=N3Click]；新增开放式基金价格提醒 [OnClick=N4Click]；修改 [OnClick=miModifyClick]；删除 [OnClick=miDeleteClick; 快捷键=Delete] |  |
| MainForm (`TMAINFORM`) | MainForm [OnShortCut=FormShortCut]；pnlToolsBar [OnDblClick=pnlToolsBarDblClick]；btnMainPopupMenuCenter [OnClick=btnMainPopupMenuCenterClick]；btnMainPopupMenuRight [OnClick=btnMainPopupMenuCenterClick]；sbClose [OnClick=sbCloseClick]；sbStoreMax [OnClick=pnlToolsBarDblClick]；sbMin [OnClick=sbMinClick]；sbMax [OnClick=pnlToolsBarDblClick]；btnCustomerService [OnClick=btnCustomerServiceClick]；imgTitle [OnClick=btnMainPopupMenuCenterClick]；btnBack [OnClick=btnBackClick]；btnNext [OnClick=btnNextClick]；btnCenter [OnClick=btnCenterClick]；btnAddTrans [OnClick=btnAddTransClick]；btnSync [OnClick=btnSyncClick]；btnRemind [OnClick=btnRemindClick]；btnTheme [OnClick=btnThemeClick]；btnFinancialTools [OnClick=btnFinancialToolsClick]；财智8 [OnClick=btnMainPopupMenuCenterClick]；btnHideNavigation2 [OnClick=btnHideNavigation2Click]；bmpbtnRegister [OnClick=bmpbtnRegisterClick]；imgReg [OnClick=bmpbtnRegisterClick]；激活高级功能 [OnClick=bmpbtnRegisterClick]；pnlLeftBar [OnDblClick=pnlLeftBarDblClick]；btnAddAcct [OnClick=btnAddAcctClick]；btnHideNavigation [OnClick=btnHideNavigationClick]；ActEscCloseForm [OnExecute=ActEscCloseFormExecute; 快捷键=Esc]；全部收起 [OnClick=mmiAcctListAllNotExpandedClick]；全部展开 [OnClick=mmiAcctListAllExpandedClick]；按[类型]显示 [OnClick=mmiAcctOrderByTypeClick]；按[自定义]显示 [OnClick=mmiAcctOrderByCustomClick]；设置[自定义]显示 [OnClick=mmiCustomAcctClick]；显示金额 [OnClick=mmiShowAcctTreeAmountClick]；显示到期账户 [OnClick=mmiShowFinishedAcctClick]；显示隐藏账户 [OnClick=mmiShowHideAcctClick]；ApplicationEvents [OnShortCut=ApplicationEventsShortCut]；财务数据 [OnClick=miFinanceDataClick]；财务报表 [OnClick=miFinanceReportClick]；财务分析 [OnClick=miFinanceAnalysisClick]；同步数据 [OnClick=btnSyncClick; 初始隐藏]；今日提醒 [OnClick=btnRemindClick; 初始隐藏]；pmMainPopupMenu [OnPopup=pmMainPopupMenuPopup]；打开财智8 [OnClick=miShowWindowClick; 初始隐藏]；账簿 [OnClick=miBookClick]；新建账簿 [OnClick=mmiNewbookClick]；打开账簿 [OnClick=mmiOpen_NewClick]；结算账簿 [OnClick=mmiRecalcClick]；设置账簿密码 [OnClick=mmiSetBookPasswordClick]；关闭当前打开的账簿 [OnClick=mmiCloseBookClick; 初始隐藏]；备份账簿 [OnClick=mmiBackupClick]；还原账簿 [OnClick=mmiRestoreClick]；导入账簿数据 [OnClick=mmiImportClick]；导出账簿数据 [OnClick=mmiExportClick]；资料管理；收支项目 [OnClick=miInformationClick]；人员与机构 [OnClick=miInformationClick]；上市证券 [OnClick=miInformationClick]；开放式基金 [OnClick=miInformationClick; 初始隐藏]；货币基金 [OnClick=miInformationClick; 初始隐藏]；债券 [OnClick=miInformationClick; 初始隐藏]；贵金属 [OnClick=miInformationClick; 初始隐藏]；银行理财产品 [OnClick=miInformationClick; 初始隐藏]；期货合约 [OnClick=miInformationClick; 初始隐藏]；期货品种 [OnClick=miInformationClick; 初始隐藏]；贵金属TD品种 [OnClick=miInformationClick; 初始隐藏]；重大资产 [OnClick=miInformationClick]；家居物品 [OnClick=miInformationClick]；证券交易费率 [OnClick=miInformationClick; 初始隐藏]；其它金融产品 [OnClick=miInformationClick]；币种与汇率 [OnClick=miInformationClick]；存款利率 [OnClick=miInformationClick]；常用备注 [OnClick=miInformationClick]；计划提醒；财务日历 [OnClick=mmiFinancialCalendarClick]；计划与提醒 [OnClick=mmiPlanClick]；限额提醒 [OnClick=mmiLimitRemindClick]；财务工具；更新行情数据 [OnClick=mmiUpdateRateClick]；导入股票交割单 [OnClick=mmiImportJGDClick]；日记 [OnClick=mmiDirayClick]；金融计算器 [OnClick=mmiJRCalculatorClick]；Windows计算器 [OnClick=mmiCalculatorClick]；设置；系统设置 [OnClick=miSystemSettingsClick]；快捷键设置 [OnClick=miTransShortcutManagnClick]；同步设置 [OnClick=mmiSyncClick]；手机提醒设置 [OnClick=mmiRemoteNotificationSettingClick]；修改同步账号密码 [OnClick=miModifySyncUserPasswordClick]；删除同步账号密码 [OnClick=miDeleteSyncUserPasswordClick]；帮助；财智8常见问题解答 [OnClick=miFAQClick]；客户服务 [OnClick=mmiHelpClick]；检查软件更新 [OnClick=mmiSoftUpdateClick]；软件许可 [OnClick=mmiRegisterClick]；最近使用的序列号 [OnClick=mmiLastUseSerialNumberClick]；访问财智在线理财 [OnClick=mmiMHOnlineURLClick]；访问财智公司官网 [OnClick=mmiSoftWareURLClick]；关于 [OnClick=mmiAboutClick]；退出 [OnClick=miCloseClick] |  |
| TMARGINSTATISTICFRAME (`TMARGINSTATISTICFRAME`) | 获取收盘价 [OnClick=btnUpdateDataClick]；BrowseGrid [OnDblClick=BrowseGridDblClick]；添加股票价格 [OnExecute=ActAddPriceExecute]；证券代码变更 [OnExecute=ActChangeCodeExecute]；融资融券费率设置 [OnClick=miMarginFeeSetClick]；证券费率设置 [OnClick=mmiFeeSetClick]；当前持仓证券；所有交易过的证券 |  |
| TMARKETDEBTSTATISTICFRAME (`TMARKETDEBTSTATISTICFRAME`) | BrowseGrid [OnDblClick=BrowseGridDblClick]；当前持仓债券；所有交易过的债券 |  |
| TMONEYSTATISTICFRAME (`TMONEYSTATISTICFRAME`) | BrowseGrid [OnDblClick=BrowseGridDblClick]；当前持仓产品；所有交易过的产品 |  |
| 今日提醒 (`TNEWREMINDDLGFM`) | 关闭 [OnClick=RzBitBtn1Click]；今日不再提醒 [OnClick=chkNoRemindTodayClick]；打开账簿时自动弹出今日提醒 [OnClick=chkAutoShowRemindTodayClick]；提醒设置；不再提醒；执行 [OnExecute=actExecuteExecute]；详情；跳过 [OnExecute=actJumpExecute] |  |
| 开放式基金价格提醒 (`TOPENFUNDREMINDDLG`) | 保存 [OnClick=btnSaveNewClick]；更新基金 [OnClick=btnUpdateCodeClick] |  |
| TOPENFUNDSTATISTICFRAME (`TOPENFUNDSTATISTICFRAME`) | 获取净值 [OnClick=btnUpdateDataClick]；BrowseGrid [OnDblClick=BrowseGridDblClick]；添加基金净值 [OnExecute=ActAddPriceExecute]；开放式基金代码变更 [OnExecute=ActChangCodeExecute]；当前持仓基金；所有交易过的基金 |  |
| TPRECIOUSMETALSTDSTATISTICFRAME (`TPRECIOUSMETALSTDSTATISTICFRAME`) | 获取最新价格 [OnClick=btnUpdateDataClick]；BrowseGrid [OnDblClick=BrowseGridDblClick]；添加贵金属价格 [OnExecute=ActAddPriceExecute]；证券代码变更 [初始隐藏]；贵金属TD品种设置 [OnClick=mmiPreciousMetalsTDGoodsClick]；当前持仓合约；所有交易过的合约 |  |
| ReportFm (`TREPORTFM`) | 筛选\|已更改 [OnClick=sbOptionClick]；图表 [OnClick=btnReportOrChartClick]；操作 [OnClick=btnOtherClick]；btnCloseTransList [OnClick=btnCloseTransListClick]；pmRightbtn [OnPopup=pmRightbtnPopup]；修改 [OnClick=miModifyClick]；删除 [OnClick=miDeleteClick]；导出到文件 [OnClick=miExportToFileClick]；报表另存为 [OnClick=miRptSaveClick]；删除报表 [OnClick=miRptDeleteClick]；导出报表 [OnClick=ActionExportRpt; 初始禁用]；打印预览 [OnClick=ActionPrintRpt; 初始禁用] |  |
| 资产负债表 (`TRPTBSSTATFRM`) | 统计方式；统计到 [OnClick=btnDateClick] |  |
| 开放式基金市值大势图 (`TRPTFUNDTRENDFM`) | 资产总值 [OnClick=chbAssetClick; 默认选中]；基金市值 [OnClick=chbAssetClick; 默认选中]；资金余额 [OnClick=chbAssetClick; 默认选中] |  |
| 收支走势图 (`TRPTINCEXPZSTOVFM`) | btnDateType |  |
| 投资收益率统计表 (`TRPTINVESTMENTPERFORMANCESTATFM`) | btnMode |  |
| 证券市值大势图 (`TRPTSTOCKTRENDFM`) | 资产总值 [OnClick=chbAssetClick; 默认选中]；证券市值 [OnClick=chbAssetClick; 默认选中]；资金余额 [OnClick=chbAssetClick; 默认选中]；上证指数 [OnClick=chbAssetClick; 默认选中]；深证成指 [OnClick=chbAssetClick; 默认选中] |  |
| 收支统计表 (`TRPTYEARINCEXPFORM`) | btnDateType |  |
| 证券市价提醒 (`TSECURITYREMINDDLG`) | 保存 [OnClick=btnSaveNewClick]；更新证券 [OnClick=btnUpdateCodeClick] |  |
| TSECURITYSTATISTICFRAME (`TSECURITYSTATISTICFRAME`) | 获取收盘价 [OnClick=btnUpdateDataClick]；BrowseGrid [OnDblClick=BrowseGridDblClick]；添加股票价格 [OnExecute=ActAddPriceExecute]；证券代码变更 [OnExecute=ActChangeCodeExecute]；导入股票交割单 [OnClick=mmijgdClick]；费率设置 [OnClick=mmiFeeSetClick]；当前持仓证券；所有交易过的证券 |  |
| TSOCIALSECURITYSTATISTICFRAME (`TSOCIALSECURITYSTATISTICFRAME`) | 删除 [OnClick=miDeleteAcctClick] |  |
| TSTATISTICFRAME (`TSTATISTICFRAME`) | 操作 [OnClick=btnOperateClick]；所有 [OnClick=btnAllOrPartObjectListClick]；余额调整 [OnExecute=ActAdjustBalaExecute]；持仓调整 [OnExecute=ActAdjustStaticExecute]；查看账户资料 [OnExecute=actOverviewExecute]；导出 [OnExecute=actExportExecute]；打印 [OnExecute=actPrintExecute]；设为软件首页 [OnClick=miHomePageClick]；当前持仓；所有 |  |
| 批量记账 (`TTEMPLATEDLGFM`) | 生成收支记录 [OnClick=btnSaveTransClick]；删除模板 [OnClick=btnDeleteTemplateClick]；存为模板 [OnClick=btnSaveTemplateClick] |  |
| 批量转账 (`TTRANSFERTEMPLATEDLGFM`) | 生成转账记录 [OnClick=btnSaveTransClick]；删除模板 [OnClick=btnDeleteTemplateClick]；存为模板 [OnClick=btnSaveTemplateClick] |  |
| 财务记录 (`TWASTEBOOKFM`) | 查找 [OnClick=btnFindClick]；操作 [OnClick=btnActionClick]；收支\|流水 [OnClick=btnDataTypeClick]；批量操作；Grid [OnDblClick=actModifyExecute]；pmRightbtn [OnPopup=pmRightbtnPopup]；批量操作模式 [OnClick=miBatchModeClick]；复制记录 [OnClick=miCopyRecClick; 快捷键=Ctrl+C]；粘贴记录 [OnClick=miPasteRecClick; 快捷键=Ctrl+V]；粘贴记录到今天 [OnClick=miPasteTodayClick]；同日期记录上移 [OnClick=miUpTransClick; 快捷键=Ctrl+Up]；同日期记录下移 [OnClick=miDownTransClick; 快捷键=Ctrl+Down]；退款 [OnClick=miRefundClick]；转为计划 [OnClick=miIntoPlanClick]；活动类型更改为 [OnClick=miChangeTransClick]；查看附件 [OnClick=miAccessoriesClick]；添加删除附件 [OnClick=mmiAddAccessClick]；修改 [OnExecute=actModifyExecute; 初始禁用]；删除 [OnExecute=actDeleteExecute; 快捷键=Delete; 初始禁用]；查找 [OnExecute=actFindExecute; 初始禁用]；导出到文件 [OnExecute=actExportExecute]；打印 [OnExecute=actPrintExecute]；筛选 [OnExecute=actFilterExecute]；放弃筛选 [OnExecute=actClearFilterExecute]；pmFind [OnPopup=pmFindPopup]；pmActive [OnPopup=pmActivePopup]；替换收支项目 [OnClick=miReplaceCategoryClick]；记录分组显示 [OnClick=miGroupClick]；批量操作模式 [OnClick=miBatchModeClick]；设为软件首页 [OnClick=N7Click]；pmBatchOperation [OnPopup=pmBatchOperationPopup]；设置标签 [OnClick=miSetTagClick]；设置备注 [OnClick=miSetDescriptionClick]；退出批量操作模式 [OnClick=miQuitBatchModeClick] |  |

## 4. 对 Rust 交互状态机的要求

1. 命令可用性必须由当前选择、数据加载状态、编辑权限和计算结果显式决定，不能散落在 UI 控件事件中。
2. 删除、批量修改、退款、转计划和清除规划数据属于有副作用命令，应用服务必须返回结构化确认信息和结果。
3. 报表筛选变化后进入 `dirty` 状态，刷新成功后进入 `ready`，导出和打印只在 `ready` 状态可用。
4. 批量操作模式应是明确状态，进入后显示选择列与批量标签/备注命令，退出后恢复普通选择行为。
5. 趋势图序列是报表预设的一部分，默认值按 DFM 直接证据初始化，但用户修改后应持久化。
6. 快捷键调用与菜单点击必须进入同一个应用命令，避免产生两套校验和副作用逻辑。

## 5. 仍需运行验证

- 财务记录修改/删除/查找的精确启用条件
- 报表结果生成前后导出和打印的启用时点
- 顶部记账动态下拉的项目、排序和快捷键
- 退款、转为计划、活动类型更改和批量操作的确认提示及结果
- 删除预算、目标、提醒和模板时的级联与恢复行为
- 清除规划数据的影响范围和确认文案
