# MoneyHome8 运行时 DFM 控件目录

本文档由普通权限运行副本内存中的真实 `TPF0` 窗体资源生成，用于检索页面标题、可见文案、数据绑定字段和交互事件。

- 数据源：`C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-dfm-all-forms.json`
- 成功解析：`460` 个窗体
- 非窗体或解析失败：`40` 个资源
- 证据边界：控件和属性来自运行时 DFM；业务结果、动态菜单和代码生成控件仍需运行流程验证。

| 资源窗体 | 页面标题 | 可见文案 | 数据字段 | 交互事件 |
| --- | --- | --- | --- | --- |
| `TABOUTFORM` | 关于 | 关于；版权所有(C) 1999-#### 成都财智软件有限公司 保留所有权利；成都财智软件有限公司 |  | 成都财智软件有限公司 -> lblCompanyClick |
| `TACCESSORIESDLG` | 添加删除附件 | 添加删除附件；删除；打开附件；添加；您可将各类财务凭证（如发票、收银条、存折等）扫描存档，同时支持添加家庭成员照片、视频、网页截图及文档等附件。；建议您在添加附件后，避免修改账簿名称、附件文件夹名称及其存储路径，以免影响系统的正常调用。；打开附件文件夹 |  | FileViewList -> btnViewClick；FileViewList -> FileViewListChange；删除 -> btnDeleteClick；打开附件 -> btnViewClick；添加 -> btnAddClick；打开附件文件夹 -> btnOpenClick |
| `TACCOUNTDLGFM` | AccountDlgFm | 账户名称；备注；所有者；币种；日期；<无>；确 定；查看附件；添加删除附件 |  | 确 定 -> btnSaveClick；查看附件 -> btnAccessoriesClick；添加删除附件 -> miAccessoriesClick |
| `TACCOUNTFEESETFM` | 证券交易费率 | 证券交易费率；A股；证券类型；买入印花税(%)；卖出印花税(%)；买入佣金(%)；买入最低佣金(元)；卖出佣金(%)；卖出最低佣金(元)；附加费(元)；过户费(‰)；B股；结算费(%)；结算费上限(元)；交易规费(%)；确定 |  | 确定 -> btnOkClick |
| `TACCOUNTMANAGERFM` | 账户中心 | 账户中心；显示选项；新增账户；所有账户；新增账户组；操作；修改账户组；删除账户组；修改账户；删除账户；注销账户；隐藏账户；加入标签；显示到期账户；显示隐藏账户；显示注销账户；显示已结清的债权债务账户；按账户类型查看；按自定分组查看；添加账户；余额调整；属于账户组；查看附件；添加删除附件；设为软件首页 |  | 显示选项 -> btnGroupTypeClick；新增账户 -> btnNewClick；所有账户 -> btnFilterTypeClick；新增账户组 -> btnNewGroupClick；操作 -> btnOperateClick；修改账户组 -> actEditAccountGroupExecute；删除账户组 -> actDeleteAccountGroupExecute；修改账户 -> actEditAccountExecute；删除账户 -> actDeleteAccountExecute；注销账户 -> actDisableAccountExecute；隐藏账户 -> actHideAccountExecute；加入标签 -> actAddThemeExecute；显示到期账户 -> actShowFinishAccountExecute；显示隐藏账户 -> actShowHiddenAccountExecute；显示注销账户 -> actShowWriteOffAccountExecute；显示已结清的债权债务账户 -> actShowOverDebtAcctExecute；按账户类型查看 -> actGroupByAcctTypeExecute；按自定分组查看 -> actGroupByAcctGroupExecute；添加账户 -> actAddSelectAccountToGroupExecute；余额调整 -> miBalaClick；属于账户组 -> miAccountGroupClick；新增账户组 -> pmNewGroupClick；查看附件 -> miAccessoriesClick；添加删除附件 -> mmiAddAccessClick；设为软件首页 -> miSetDefaultPageClick |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | 账户概况 |  |  |
| `TACCTBALAREMINDDLG` | 账户余额提醒 | 账户余额提醒；余额小于；或大于；当账户；保存 |  | 保存 -> btnSaveNewClick |
| `TACCTDETAILDLG` | 账户详细资料 | 账户详细资料；托管银行；<无>；确定；账户名称；联网登录号；联网账号；联系电话；联系方式；密码；备注；卡号；利率(%) |  | 联网账号 -> lbOnlineNoClick |
| `TACCTGUIDEMAIN` | AcctGuideMain |  |  |  |
| `TADJUSTHELDDLGFM` | 持仓调整 | 持仓调整；持仓总成本；持仓数量；账户/资产；持有产品 |  |  |
| `TADVANCEACCTDLGFM` | 预收、预付 | 预收、预付；款项 |  |  |
| `TADVANCESVIEWFRAME` |  |  |  |  |
| `TADVANCETRANSDLGFM` | 预付 | 预付；债务人；款项；预付金额；币种；支付账户 |  | edKind -> edKindChange |
| `TAIPANELDLG` | AI |  |  |  |
| `TALIPAYVIEWFRAME` |  |  |  |  |
| `TALSOCOUPONSDIRECTLYDLGFM` | 直接还券 | 直接还券；返还数量；融资融券账户；融券合约；返还利息 |  |  |
| `TAMOUNTSCREENINGFRAME` |  | 到；之间；金额在；金额小于等于；金额大于等于；不筛选金额 |  | 金额在 -> rbtnClick；金额小于等于 -> rbtnClick；金额大于等于 -> rbtnClick；不筛选金额 -> rbtnClick |
| `TASSETBUYFM` | 重大资产买入 | 重大资产买入；有贷款；新增贷款；备注；主题；日期；币种；所有者；资产名称；总额；资产性质；支付账户；选择；债权人；款项；金额；确 定 |  | 有贷款 -> RzCheckClick；新增贷款 -> btnNewDebtClick；确 定 -> btnSaveClick |
| `TASSETENCASHDLGFM` | 重大资产卖出 | 重大资产卖出；卖出原始成本；资产名称；卖出所得金额；收入账户；按比例减少市值；新增欠款；有欠款；选择；债务人；款项；日期；金额 |  | 按比例减少市值 -> RzCheckClick；新增欠款 -> btnNewDebtClick；有欠款 -> RzCheckClick |
| `TASSETINCREMENTDLGFM` | 资产市值变更 | 资产市值变更；变更前价值；资产名称；变更后价值 |  | edTransDate -> edTransDateChange |
| `TASSETINVESTDLGFM` | 追加投资 | 追加投资；有贷款；新增贷款；资产名称；追加金额；支付账户；同时追加市值；选择；债权人；款项；日期；金额 |  | 有贷款 -> RzCheckClick；新增贷款 -> btnNewDebtClick；同时追加市值 -> RzCheckClick |
| `TASSETOTHERFEEDLGFM` | 资产投资费用 | 资产投资费用；资金账户；金额；支出项目；资产名称 |  |  |
| `TASSETPRICEFM` | 重大资产价格 | 重大资产价格；资产概况；新增价格；操作；资产名称；日期；价格；当前价格；修改价格；删除价格；导出；打印 | `AcctID`；`AssetName`；`PriceDate`；`Price` | 操作 -> RzMenuButton1Click；MHBPrice -> actEditExecute；操作 -> btn1Click；MHBAsset -> actAssetExecute；新增价格 -> actAddExecute；修改价格 -> actEditExecute；删除价格 -> actDelExecute；资产概况 -> actAssetExecute；导出 -> miExportPriceClick；打印 -> miPrintPriceClick；导出 -> miExportClick；打印 -> miPrintClick |
| `TASSETSCONSTITUTECHARTFRAME` |  |  |  |  |
| `TASSETSDLGFM` | 重大资产概况 | 重大资产概况；资产名称；创建日期；资产性质；投资；自用 |  |  |
| `TASSETSMARKETCONSTITUTESFRAME` |  |  |  |  |
| `TASSETSSTATISTICFRAME` |  | 资产名称；币种；当前成本；累计收益；资产市值；资产性质；删除；当前持有资产；所有记录过的资产 | `ObjName`；`CurrType`；`Cost`；`Scale`；`Market`；`IsInvestment` | 删除 -> miDeleteAssetClick |
| `TASSETSTRANSFRAME` |  | 发生金额；单个资产交易明细 | `AMT`；`CategoryName`；`Iterbala`；`AcctID`；`TotalFee`；`TransObjID` |  |
| `TASSETSVALUEMANAGEMENTFRAME` |  | 日期；市值；添加；修改；删除 | `PriceDate`；`Price` | mhbgData -> mhbgDataDblClick；添加 -> btnAddClick；修改 -> btnUpdateClick；删除 -> btnDeleteClick |
| `TASSETTRANSFM` | 重大资产交易明细 | 重大资产交易明细；交易明细；市值管理；成本市值构成；资产概况 |  |  |
| `TASSETVIEWFRAME` |  |  |  |  |
| `TBACKUPBOOKFM` | 备份账簿 | 备份账簿；当前账簿；备份到；备份名称；备份；更改；确定 |  | 备份 -> BtnOkClick；更改 -> BtnDBrowseClick；确定 -> BtnOkClick |
| `TBATCHALSOCOUPONSDIRECTLYDLGFM` | 批量直接还券 | 批量直接还券；融资融券账户；主题；日期；备注；确 定；融券合约；返还数量；利息 |  | 确 定 -> btnSaveExitClick |
| `TBATCHDIRECTPAYMENTSDLGFM` | 批量直接还款 | 批量直接还款；融资融券账户；主题；日期；备注；确 定；融资合约；还款金额；利息 |  | 确 定 -> btnSaveExitClick |
| `TBLOCKUPDLGFM` | 垫付 | 垫付；债务人；款项；金额；标签；币种；收支项目；资金账户；<无> |  | edKind -> edKindChange |
| `TBONDSMARKETCONSTITUTESFRAME` |  |  |  |  |
| `TBONDSVIEWFRAME` |  |  |  |  |
| `TBUDGETCOPYDLGFM` | 复制预算金额 | 复制预算金额；九月；十月；十一月；十二月；八月；七月；六月；五月；四月；三月；二月；一月；确定 |  | 确定 -> btnOkClick |
| `TBUDGETLISTFM` | 预算 | 预算；新增预算；预算设置；您可通过切换日期，为不同时间段设置相应的预算额。；知道了；修改预算收支项目；修改预算金额；修改预算信息；删除预算；导出文件；修改；删除 |  | 新增预算 -> btnNewClick；mwAdjustYear -> mwAdjustYearClick；mwAdjustMonth -> mwAdjustYearClick；mwAdjustSeason -> mwAdjustYearClick；预算设置 -> btnUpdateClick；btnDisplayType -> btnDisplayTypeClick；btnCloseTransList -> btnCloseTransListClick；知道了 -> btnKnowClick；修改预算收支项目 -> miEditBudgetCategoryClick；修改预算金额 -> miEditBudgetAmountClick；修改预算信息 -> miEditBudgetClick；删除预算 -> miDeleteBudgetClick；导出文件 -> miExportClick；修改 -> miModifyClick；删除 -> miDeleteClick |
| `TBUYFUNDPLANDLGFM` | 基金定投计划 | 基金定投计划；申购基金；资金账户；基金账户；更新基金；<无>；申购费率 %；基金申购定额；自动执行 |  | 更新基金 -> btnUpdateCodeClick；自动执行 -> chkAutoExecuteClick |
| `TCALCUFM` | CalcuFm |  |  |  |
| `TCALCULATORDLG` | 金融计算器 | 金融计算器 |  |  |
| `TCARDVIEWFRAME` |  |  |  |  |
| `TCASHACCTDLGFM` | 现金 | 现金 |  |  |
| `TCASHCARDDLGFM` | 信用卡取现 | 信用卡取现；取款信用卡；资金去向；金额；手续费 |  |  |
| `TCASHTRANSFM` | 现金交易列表 | 现金交易列表 |  |  |
| `TCASHTRANSFRAME` |  | 流入；流出；导入 | `Inc`；`Exp`；`CategoryName`；`Bala`；`Iterbala`；`FIID`；`Amount` | 导入 -> miImportClick |
| `TCASHVIEWFRAME` |  |  |  |  |
| `TCASHWITHDRAWDLGFM` | 取款 | 取款；取款账户；可用资金；资金去向；取款金额；手续费；支出账户；全部取完；选中此项后，取款金额及可大于可用资金，大于的金额将做为利息处理；到期 |  | edTransDate -> edTransDateChange；全部取完 -> chbAllClick；selDrawAcct -> selDrawAcctChange |
| `TCASHXFERDLGFM` | 转账 | 转账；交换转入转出账户；转出账户；转入账户；转账金额；转账币种；手续费；手续费账户；<无> |  | MHBmpButton1 -> MHBmpButton1Click |
| `TCATEGORYLISTFM` | 收支项目 | 收支项目；操作；新增项目；请输入要搜索的关键字...；收支项目名称；一级收支项目名称；隐藏的收支项目将不会在记账时的收支项目选择列表中显示。；系统预置的收支项目为固定项目，不支持修改或删除操作。；归属于；上次使用日期：；修改项目；删除项目；隐藏项目；显示隐藏类别；显示系统类别；往上移；往下移；按使用量排序；按自定义排序；调整收支项目顺序；导入；导出 |  | 操作 -> sbCustomClick；上次使用日期： -> miLastUsedClick；新增项目 -> actAddCategoryExecute；修改项目 -> actEditCategoryExecute；删除项目 -> actDeleteCategoryExecute；隐藏项目 -> actHideCategoryExecute；显示隐藏类别 -> actShowHideExecute；显示系统类别 -> actShowSysExecute；按使用量排序 -> miSortByFreqClick；按自定义排序 -> miSortByFreqClick；调整收支项目顺序 -> miEditCategoryOrderClick；导入 -> miImportClick；导出 -> miExportClick |
| `TCHANGEPAYMODEDLGFM` | 变更还款方式 | 变更还款方式；变更日期；新方式；每期还款额；保存 |  | 保存 -> btnSaveExitClick |
| `TCHECKBOOKDLG` | 结算账簿 | 结算账簿；账簿备份位置；结算截止日；更改；确定；当记录数量过多导致系统运行缓慢或需要进行到期结转时，您可以使用账簿结算功能。 结算操作将合并截止日期前的所有记录。如需查询历史明细，可通过账簿还原功能查看 完整记录。 |  | 更改 -> btnChangeClick；确定 -> RzButtonOkClick |
| `TCHILDFORM` | ChildForm |  |  | sbHelp -> sbHelpClick；sbCloseChild -> sbCloseChildClick |
| `TCLAIMSDEBTCONTAINER` |  | 应收款概况；应付款；待摊费用；预收款；预付款概况 |  |  |
| `TCLAIMSDEBTSCHARTFRAME` |  |  |  | btnUnit -> btnUnitClick |
| `TCLAIMSDEBTSCONSTITUTESFRAME` |  |  |  | btnShowType -> btnShowTypeClick |
| `TCLAIMSDEBTSTATISTICFRAME` |  | 债权和债务 \| 忽略已完成款项；债权人/债务人 款项；款项类型；还款方式；利率；剩余期数；待收/还本金；删除；显示债权和债务；仅债权；仅债务；忽略已完成的款项 |  | 债权和债务 \| 忽略已完成款项 -> btnDisplayTypeClick；删除 -> miDeleteAssetClick；忽略已完成的款项 -> miIgnoreCompletedClick |
| `TCLAIMSDEBTTRANSFRAME` |  | 查看未报销记录；增加；减少；利息；合计；待收/还金额 | `InCorpus`；`OutCorpus`；`AbsInterest`；`AMT`；`CategoryName`；`Bala`；`Iterbala`；`AcctID`；`AcctType` | 查看未报销记录 -> btnShowUnreimbursedRecordClick |
| `TCLAIMSTRANSFM` | 债权债务交易明细 | 债权债务交易明细；交易明细；债权债务构成；已收金额和收款表；债权债务概况 |  |  |
| `TCLEANPRICEFM` | 价格整理 | 价格整理；整理条件；到；之前的所有价格数据；之间的所有价格数据；删除日期；删除日期 从；删除所有未交易对象的价格数据；保留已交易过的金融产品的历史价格数据；整理范围；股票价格数据；基金价格数据；贵金属价格数据；币种汇率数据；确定；定期整理价格数据，清理无用价格，可提升系统处理效率与运行速度。建议您每两至三个月执行一次价格整理操作。 |  | 确定 -> RzBtnOkClick |
| `TCOLLATERALINDLGFM` | 担保物划入 | 担保物划入；划入融资融券账户；划出证券账户；划入证券代码；划入数量 |  |  |
| `TCONSOLEFM` | 控制台 | 控制台；网银插件与网络；清除控制台记录 |  | 清除控制台记录 -> miClearClick |
| `TCOSTDETAILSDLGFM` | 垫付明细 | 垫付明细；确定；反选(&I)；全选(&A)；日期；收支项目；金额；主题；备注 |  | 确定 -> btnOkClick；反选(&I) -> btnInvertClick；全选(&A) -> btnAllClick |
| `TCOUPONSALSOBUYCOUPONSDLGFM` | 买券还券 | 买券还券；费用小计；金额合计；买入数量；买入价格；融资融券账户；融券合约；证券代码；返还利息；印花税率 %；印花税费；佣金比例 %；佣金；过户费；附加费；显示费用详情 |  | 显示费用详情 -> chkvisibleClick |
| `TCREATEBUDGETDLGFM` | 预算 | 预算；预算名称；预算频率；到；标签；您可通过标签分类与自定义时间周期功能，创建装修、婚礼等特定场景的专项预算方案，实现重要事项的精细化财务规划。；预算周期；月度；季度；年度；自定义；确定；高级预算设置 |  | 月度 -> rbMonthClick；季度 -> rbMonthClick；年度 -> rbMonthClick；自定义 -> rbMonthClick；确定 -> btnSaveClick；pnlAdvanced -> pnlAdvancedClick；img1 -> pnlAdvancedClick；imgStatus -> pnlAdvancedClick；高级预算设置 -> pnlAdvancedClick |
| `TCREDITACCTDLGFM` | 信用卡账户 | 信用卡账户；启用日期；透支限额；开户银行；还款日；卡号；当透支额大于；时提醒；年费；最低还款比例(%)；预借现金额度；到期月年；年费减免规则；账单日当天交易；透支提醒；日；天；账单日之后；固定还款日，每月；计入下期；计入本期；次免年费；免年费；刷卡金额满；刷卡；不免年费；<无>；更多信息；账单日管理 |  | 透支提醒 -> cbIsAwakeClick；账单日之后 -> RBPayType0Click；固定还款日，每月 -> RBPayType1Click；刷卡金额满 -> rbAnnualFeeExemptType0Click；刷卡 -> rbAnnualFeeExemptType0Click；不免年费 -> rbAnnualFeeExemptType0Click；更多信息 -> btnMoreInfoClick；账单日管理 -> btnManageBillDateClick |
| `TCREDITCARDSTATISTICFRAME` |  | 账单记录时间段；账单日；还款日；流入金额；流出金额；账单金额；导入；显示最近3期已出账单；显示所有已出账单 | `BillDate`；`NBillDate`；`LastPayDate`；`Inc`；`Exp`；`BillAmount` | 导入 -> miImportClick |
| `TCREDITCARDTRANSFM` | 信用卡交易明细 | 信用卡交易明细；交易明细；分期付款管理 |  |  |
| `TCREDITCARDTRANSFRAME` |  | 流入；流出；导入；单个账单交易明细 | `Inc`；`Exp`；`CategoryName`；`Bala`；`Iterbala`；`FIID`；`AMT` | 导入 -> miImportClick |
| `TCREDITREMINDDLG` | 信用卡透支额提醒 | 信用卡透支额提醒；透支额为；当信用卡；保存 |  | 保存 -> btnSaveNewClick |
| `TCURRCHGXFERDLGFM` | 货币兑换 | 货币兑换；兑换报价方式说明：USD/RMB牌价为8.27，表示1美元兑换8.27元人民币。；换出账户；换入账户；换出金额；换入金额 |  |  |
| `TCURRDEPOSITSVIEWFRAME` |  |  |  |  |
| `TCURRDLG` | 货币 | 货币；钞汇；对人民币汇率；英文缩写；名称；保存；现汇；现钞 |  | 保存 -> btnSaveExitClick |
| `TCURRENTACCTDLGFM` | 活期存款 | 活期存款；开户日期；卡号；账户组；开户银行；<无>；更多信息 |  | 更多信息 -> btnMoreInfoClick |
| `TCURRENTMONTHINCEXPPIECHARTFRAME` |  |  |  | btnUnit -> btnUnitClick |
| `TCURRENTTRANSFM` | 活期存款交易明细 | 活期存款交易明细 |  |  |
| `TCURREXCHANGEDLGFM` | 外汇交易 | 外汇交易；报价方式说明：USD/RMB牌价为8.27，表示1美元兑换8.27元人民币。；交易账户；卖出货币；买入货币；卖出金额；买入金额；交易汇率 |  | lblRateDirection -> lblRateDirectionClick；edAmountIn -> edAmountOutChange；edAmountOut -> edAmountOutChange |
| `TCURRFUNDACCTDLGFM` | 货币基金账户 | 货币基金账户；创建日期；开户机构；账号；资产性质；默认资金账户；自身；其它；<无>；储蓄；投资 |  | 自身 -> rbSelfCapitalClick；其它 -> rbSelfCapitalClick |
| `TCURRFUNDBUYDLGFM` | 货币基金申购 | 货币基金申购；基金账户；基金名称；资金账户；申购金额；更新基金；<无> |  | 更新基金 -> btnUpdateCodeClick |
| `TCURRFUNDCONVERTFM` | 货币基金转换 | 货币基金转换；备注；主题；日期；转为基金；转入份额；转换费用；单位净值；转为收费模式；基金账户；更新基金；原有基金；转出份额；资金账户；<无>；确 定 |  | 更新基金 -> btnUpdateCodeClick；确 定 -> btnOKClick |
| `TCURRFUNDMARKETCONSTITUTESFRAME` |  |  |  |  |
| `TCURRFUNDREINVESTDLGFM` | 货币基金红利再投资 | 货币基金红利再投资；金额；基金名称；基金账户；份额 |  |  |
| `TCURRFUNDSELLDLGFM` | 货币基金赎回 | 货币基金赎回；资金账户；赎回金额；基金名称；基金账户；利息；赎回份额；<无> |  |  |
| `TCURRFUNDSLISTFM` | 货币基金列表 | 货币基金列表；新增基金；操作；请输入要搜索的关键字...；代码；名称；币种；修改基金；删除基金；代码转换；获取代码；查找；导出；打印 | `TransObjID`；`Code`；`FullName`；`ChineseName` | 操作 -> RzMenuButton1Click；MHBGSecurity -> actEditSecurityExecute；新增基金 -> actAddSecurityExecute；修改基金 -> actEditSecurityExecute；删除基金 -> actDeleteSecurityExecute；代码转换 -> actConvertCodeExecute；获取代码 -> ActGetCodeExecute；查找 -> N3Click；导出 -> miExportClick；打印 -> miPrintClick |
| `TCURRFUNDSTATISTICFRAME` |  | 获取代码；基金名称；累计金额；占比%；货币基金代码转换；当前持仓基金；所有交易过的基金 | `ObjName`；`Cost`；`scale` | 获取代码 -> btnUpdateDataClick；BrowseGrid -> BrowseGridDblClick；货币基金代码转换 -> ActChangeCodeExecute |
| `TCURRFUNDTRANSFM` | 货币基金交易明细 | 货币基金交易明细；交易明细；历史盈亏 |  |  |
| `TCURRFUNDTRANSFRAME` |  | 基金名称；交易金额；单只基金交易明细 | `CategoryName`；`TransObjID`；`AMT`；`Bala`；`Iterbala` |  |
| `TCURRFUNDVIEWFRAME` |  |  |  |  |
| `TCURRLISTFM` | 币种与汇率 | 币种与汇率；货币与汇率；操作；请输入要搜索的关键字...；本币；货币名称；英文缩写；对人民币牌价；日期；货币；比；报价方式；牌价/汇率；新增汇率；按日期显示全部汇率；修改；删除；查找；如何做；设置为本币；获取牌价；现汇；现钞；选项；所有；修改汇率；删除汇率；价格整理；分类显示；导出；打印 | `TransObjID`；`CHINESENAME`；`ENGLISHABBR`；`PriceDate`；`Curr1name`；`Curr2name`；`Abbr`；`Price`；`ID` | 币种与汇率 -> FormShow；操作 -> btnOptionClick；DBGRID -> DBGRIDDblClick；RateGrid -> actRateEditExecute；RzDTEDate -> RzDTEDateChange；按日期显示全部汇率 -> RzCBOnlyDateClick；操作 -> btn1Click；修改 -> actEditExecute；删除 -> actDelExecute；设置为本币 -> actLocalCurrExecute；获取牌价 -> actDownloadExecute；现汇 -> actOptionBillExecute；现钞 -> actOptionCashExecute；所有 -> actOptionAllExecute；新增汇率 -> actRateAddExecute；修改汇率 -> actRateEditExecute；删除汇率 -> actRateDelExecute；价格整理 -> actCheckPriceExecute；导出 -> miExportClick；打印 -> miPrintClick；导出 -> miExportPriceClick；打印 -> miPrintPriceClick |
| `TCUSTCOLUMNFM` | CustColumnFm |  |  |  |
| `TCUSTOMERDLGFM` | 客户服务 | 客户服务；官网：；微信：；周一到周五，9点到18点在线；电邮：；微博：；常见问题 |  | imgQQTechnicalSupport -> imgQQTechnicalSupportClick；imgQQBuy -> imgQQTechnicalSupportClick；imgSinaWeibo -> imgSinaWeiboClick；http://www.moneywise.com.cn/ -> lblWebsiteClick；常见问题 -> btnFAQClick |
| `TCUSTOMNAVIGATIONACCTDLGFM` | 设置[自定义]显示 | 设置[自定义]显示；下移；全选；反选；确定；上移 |  | 下移 -> btnDownClick；全选 -> btnSelectAllClick；反选 -> btnInverseClick；确定 -> btnSaveClick；上移 -> btnUpClick；chkTreeAcct -> chkTreeAcctChange |
| `TDCURRCREDITACCTDLGFM` | 双币信用卡 | 双币信用卡；信用卡别名；币种一；账单日；开户银行；信用卡账号；更多资料...；当前余额；透支限额；币种二；还款日；限额提醒；日；每月；每月最后一天是账单日；固定账单日；天；账单日之后；固定还款日；<无> |  | 更多资料... -> lblMoreInfoClick；每月最后一天是账单日 -> RBBillType1Click；固定账单日 -> RBBillType0Click；账单日之后 -> RBPayType0Click；固定还款日 -> RBPayType1Click |
| `TDEBTADJUSTDLGFM` | 坏账 | 坏账；债务人；款项；金额 |  |  |
| `TDEBTBORROWDLGFM` | 借入 | 借入；借入金额；债权人；款项；收入账户；保存 |  |  |
| `TDEBTEQUITYSWAPTRANSDLGFM` | 债转股 | 债转股；证券账户；资金账户；可转债代码；证券代码；转债数量(张)；转股数量；转股价格；返还本息；<无> |  | edtDebtQuantity -> edtDebtQuantityChange；edtStockPrice -> edtDebtQuantityChange |
| `TDEBTINVESTMENTACCTDLGFM` | 网贷 | 网贷；平台名称；平台网址 |  |  |
| `TDEBTINVESTMENTACCTLISTFRAME` |  | 账户名称；预期年化收益率；实现盈亏；待收利息；待收本金；可用资金；资产值 | `AcctName`；`YearRate`；`PL`；`LessInterest`；`LessCost`；`Cash`；`AssetValue`；`AcctID` |  |
| `TDEBTINVESTMENTBADTRANSDLGFM` | 网贷坏账 | 网贷坏账；损失金额；网贷账户；投资名称 |  |  |
| `TDEBTINVESTMENTLOANDLGFM` | 网贷借出 | 网贷借出；投资计息日；网贷账户；资金账户；投资名称；借出金额；年利率(%)；收款方式；首次收款日；借出期限；收款间隔；收款总期数；已收款期数；每期收款额；剩余本金；管理费率(%)；计息方式；回款日期；标满付息日；收款计划到期自动执行 |  | edTransDate -> edTransDateChange；edtAmount -> edtAmountChange；edtRate -> edtAmountChange；edtPeriod -> edtPeriodChange；edtPayFreq -> edtPeriodChange；edtPayCount -> edtAmountChange；edtPayedCount -> edtAmountChange；edtManagementFeeRate -> edtAmountChange；edtTakebackDate -> edtTakebackDateChange；edtRateDate -> edtRateDateChange |
| `TDEBTINVESTMENTPAYOBJECTFRAME` |  | 网贷收回；收款日期；账户；投资名称；应收本金；应收利息；应收合计；剩余期数；当前账户 | `NextPayDate`；`AcctName`；`ObjName`；`PayCost`；`PayInterest`；`PayAmount`；`UnPayCount` | 网贷收回 -> btnWithDrawClick；BrowseGrid -> BrowseGridDblClick |
| `TDEBTINVESTMENTPAYTABLEFRAME` |  | 打印；期次；日期；月收款本息；本期收款；本金；利息；剩余本金 |  | 打印 -> btnPrintClick |
| `TDEBTINVESTMENTREWARDTRANSDLGFM` | 网贷投资奖励 | 网贷投资奖励；奖励金额；网贷账户；收入账户；投资名称 |  |  |
| `TDEBTINVESTMENTSELLTRANSDLGFM` | 网贷转让 | 网贷转让；转让本金；成交金额；手续费；网贷账户；投资名称；收入账户 |  | edTransDate -> selDebtInvestmentObjCloseUp |
| `TDEBTINVESTMENTSTATISTICFRAME` |  | 收款表；名称；投资日期；期限；收款方式；收款间隔；剩余期数；年利率；待收本金；当前持有网贷；已完成网贷 | `ObjName`；`InvestmentDate`；`Period`；`PayMode`；`PayFreq`；`UnpayCount`；`Rate`；`UnpayAmount` | 收款表 -> btnPayTableClick；BrowseGrid -> BrowseGridDblClick |
| `TDEBTINVESTMENTTRANSFM` | 网贷账户交易明细 | 网贷账户交易明细；交易明细；投资列表；待收明细 |  |  |
| `TDEBTINVESTMENTTRANSFRAME` |  | 投资名称；本金；利息；发生金额 | `TransObjID`；`Corpus`；`Interest`；`AMT`；`CategoryName`；`Bala`；`Iterbala` |  |
| `TDEBTINVESTMENTVIEWFRAME` |  |  |  |  |
| `TDEBTINVESTMENTWITHDRAWTRANSDLGFM` | 网贷收回 | 网贷收回；本金；利息；本息合计；网贷账户；收入账户；投资名称 |  |  |
| `TDEBTLENDDLGFM` | 借出 | 借出；债务人；款项；借出金额；支出账户；保存 |  |  |
| `TDEBTRATESETDLG` | 借贷款账户利率调整 | 借贷款账户利率调整；日期；利率(%)；确定 |  | 确定 -> RzBitBtn1Click |
| `TDEBTRECDLGFM` | 收回 | 收回；债务人；款项；本金；利息；本息合计；收入账户 |  |  |
| `TDEBTRETURNDLGFM` | 返还 | 返还；利息；款项；债权人；本金；本息合计；支出账户 |  |  |
| `TDEBTSACCTDLGFM` | 应收、应付 | 应收、应付；款项名称；人员；借贷发生日；首次还款日；金额；利率；还款方式；还款总期数；已还款期数；约定还款额；剩余本金；贷款期限；还款频率；最低还款额；年；季度；月；不定 |  |  |
| `TDEFERREDVIEWFRAME` |  |  |  |  |
| `TDIALOGFORM` | DialogForm | 关闭；帮助；最小化；对话框标题 |  | DialogForm -> FormShow；btnCaptionClose -> btnCaptionCloseClick；btnCaptionHelp -> btnCaptionHelpClick；对话框标题 -> lbCaptionDblClick |
| `TDIARYDLGFM` | 日记 | 日记；日期；加粗；倾斜；下划线；左对齐；居中；右对齐；项目符号；字体颜色；字体；字号；选择字体颜色；保存；撤销；剪切；复制；粘贴；全选 |  | RzDTEDate -> RzDTEDateChange；BoldButton -> BoldButtonClick；ItalicButton -> ItalicButtonClick；UnderlineButton -> UnderlineButtonClick；LeftAlign -> LeftAlignClick；CenterAlign -> LeftAlignClick；RightAlign -> LeftAlignClick；BulletsButton -> BulletsButtonClick；ColorButton -> ColorButtonClick；保存 -> RzBtnSaveClick；撤销 -> N4Click；剪切 -> N3Click；复制 -> N1Click；粘贴 -> N2Click；全选 -> N8Click |
| `TDIARYUNTFM` | 日记 | 日记；操作；写日记；修改日记；删除日记；查看所有日记；搜索；导出列表中的日记 |  | 操作 -> btnOperateClick；tlDiary -> tlDiaryDblClick；写日记 -> ActAddExecute；修改日记 -> ActModifyExecute；删除日记 -> ActDeleteExecute；查看所有日记 -> actViewExecute；搜索 -> actSearchExecute；导出列表中的日记 -> actExprotExecute |
| `TDIRECTPAYMENTSDLGFM` | 直接还款 | 直接还款；还款金额；融资融券账户；融资合约；返还利息 |  |  |
| `TDRAWALCARDDLGFM` | 信用卡还款 | 信用卡还款；信用卡；资金来源；还款金额；利息；还款总额；还款总额=账单金额+利息 |  | edAmount -> edAmountChange；edtInterest -> edAmountChange |
| `TDROPDOWNDATE` | Dropdowndate |  |  | mwCalendarPanel1 -> mwCalendarPanel1Change |
| `TDROPFM` | DropFM |  |  | DropFM -> FormShow |
| `TEDITACCOUNTGROUPFM` | 账户组 | 账户组；账户组名；账户组功能可帮助您管理具有相似属性或用途的账户集合。例如，您可以将银行定期一本通下的多个存单整合为一个账户组进行统一管理。此外，您还可以根据实际需求，灵活创建不同的账户组分类，如按家庭成员、资金用途等维度进行分组管理，让您的财务管理更加清晰有序。；详细资料... |  | 详细资料... -> btnShowDetailClick |
| `TEDITASSETBUYDLGFM` | 重大资产买入 | 重大资产买入；有贷款；新增贷款；资产名称；金额；支付账户；选择；债权人；款项；日期 |  | 有贷款 -> RzCheckClick；新增贷款 -> btnNewDebtClick |
| `TEDITBANKMONEYPRODUCTDLGFM` | 银行理财产品 | 银行理财产品；币种；产品代码；发行机构；委托期；收益终止日；预期年收益率(%)；产品名称；收益起始日；保存；是否保本；<无>；是否注销 |  | 保存 -> RzButtonOKClick；edtBeginDate -> edtBeginDateChange；edtTerm -> edtTermChange |
| `TEDITBUDGETAMOUNTDLGFM` | 预算金额设置 | 预算金额设置；确定；复制预算金额；导入最近12个月的收支金额；收支项目；一月；二月；三月；四月；五月；六月；七月；八月；九月；十月；十一月；十二月；一季度；二季度；三季度；四季度；全年；预算金额；从其它年份复制预算金额；复制选中单元格金额到其它列；复制选中列金额到其它列 |  | 确定 -> btnSaveClick；mwAdjustYear -> mwAdjustYearClick；复制预算金额 -> btnCopyAmountClick；导入最近12个月的收支金额 -> btnImportAmountClick；从其它年份复制预算金额 -> miCopyAmountFromYearClick；复制选中单元格金额到其它列 -> miCopyCellAmountClick；复制选中列金额到其它列 -> miCopyColumnAmountClick |
| `TEDITBUDGETCATEGORYDLGFM` | 选择预算收支项目 | 选择预算收支项目；支出；收入；以红色标识的项目表示已设置预算额度；确定；新增收支项目；全选；反选 |  | 确定 -> btnSaveClick；新增收支项目 -> btnCreateCategoryClick；全选 -> btnSeletAllClick；反选 -> btnSelectContraryClick |
| `TEDITCATEGORYFM` | 收支项目 | 收支项目；名称；归属于；支出；收入；保存；保存并新添；<无> |  | 支出 -> rbExpenseClick；收入 -> rbExpenseClick；保存 -> RzBtnSaveExitClick；保存并新添 -> btnSaveNewClick |
| `TEDITCATGORYORDERDLGFM` | 调整收支项目顺序 | 调整收支项目顺序；确定 |  | mwSortCategoryList -> mwSortCategoryListChange；确定 -> btnOverClick |
| `TEDITCURRFUNDFM` | 货币基金 | 货币基金；名称；代码；币种；保存；锁定名称 |  | RzEditName -> RzEditNameChange；保存 -> RzButtonOKClick；锁定名称 -> cbLockNameClick |
| `TEDITFUTURESGOODSFM` | 期货品种 | 期货品种；品种名称；保证金比例(%)；品种代码；品种类型；报价单位；交易单位；每手数量；手续费；交易所；保存 |  | 保存 -> RzButtonOKClick |
| `TEDITGOLDFM` | 贵金属 | 贵金属；产品名称；币种；保存 |  | 保存 -> RzButtonOKClick |
| `TEDITMARGINCONTRACTDLGFM` | 编辑融资融券 | 编辑融资融券；类型；年利率%；合同号；对应证券；更新代码；保存 |  | 更新代码 -> btnUpdateCodeClick；保存 -> btnOKClick |
| `TEDITNMARKETBONDFM` | 债券 | 债券；币种；债券名称；发行日期；年利率(%)；到期日期；月；债券类型；付息日期2；付息日期1；日；面值；发行单位；债券代码；保存；免税；<无>；目前只提供面值100的债券。 |  | 保存 -> RzButtonOKClick |
| `TEDITOPENFUNDFM` | 开放式基金 | 开放式基金；代码；币种；名称；申购费率(%)；赎回费率(%)；保存；锁定名称 |  | RzEditName -> RzEditNameChange；保存 -> RzButtonOKClick；锁定名称 -> cbLockNameClick |
| `TEDITPRECIOUSMETALSTDGOODSFM` | 贵金属TD品种 | 贵金属TD品种；品种名称；保证金比例(%)；品种代码；报价单位；交易单位；每手数量；保存 |  | 保存 -> RzButtonOKClick |
| `TEDITSECURITYFM` | 股票 | 股票；代码；名称；类型；币种；保存；锁定名称 |  | RzEditName -> RzEditNameChange；保存 -> RzButtonOKClick；锁定名称 -> cbLockNameClick |
| `TEDITSECURITYPRICEFM` | EditSecurityPriceFm | 日期；价格；代码；保存 |  | 保存 -> RzButtonOkClick |
| `TEDITTAGORDERDLGFM` | 调整标签顺序 | 调整标签顺序；确定 |  | mwSortTagList -> mwSortTagListChange；确定 -> btnOverClick |
| `TEDTACCTGRPDLGFM` | 修改所属账户组 | 修改所属账户组；请选择账户组；确定；<无> |  | 确定 -> btnSaveClick |
| `TEQUITYFINANCINGDLGFM` | 融资权益 | 融资权益；融资融券账户；融资年利率%；融资合同号；融资金额；附加权益 融券合约 |  |  |
| `TEQUITYSECURITIESLENDINGDLGFM` | 融券权益 | 融券权益；融资融券账户；融券年利率%；融券合同号；附加权益 融券合约；融券单价；融券数量 |  |  |
| `TEXCHANGEACCTFM` | 外汇交易账户 | 外汇交易账户；创建日期；开户银行；账号 |  |  |
| `TEXCHANGEMARKETCONSTITUTESFRAME` |  |  |  |  |
| `TEXCHANGERATEDLG` | 外汇汇率 | 外汇汇率；日期；比；汇率；报价方式；货币；保存 |  | 保存 -> btnSaveExitClick |
| `TEXCHANGEVIEWFRAME` |  |  |  |  |
| `TEXERTIONRIGHTSDLGFM` | 行权 | 行权；证券账户；权证代码；行权价格；行权数量；行权对象；行权比例；行权费用；资金账户；<无> |  |  |
| `TEXPENSEDLGFM` | 报销 | 报销；借款款项；垫付款项；本次报销金额；本次报销抵扣借款；选择垫付记录…；账户名称；实收金额；<无> |  | 选择垫付记录… -> btnSelectExpenseClick |
| `TEXPORTDATAFM` | 数据导出 | 数据导出；确定；基本选项；导入时间段内数据：；到；导出数据起止日期：；导出数据账户：；导出文件名称：；浏览...；导入时更新账户余额；增加；删除并覆盖；数据选项；双击此处全选/取消全选；账户信息；交易信息；交易费率；记账模板；证券列表；提醒设置；物品历史价格；物品信息；计划日记；人员机构；贵金属；生活主题；理财目标；基金列表；历史汇率；债券列表；货币基金；货币信息；收支项目；收支预算；理财产品 |  | BtnOk -> BtnOkClick；确定 -> BtnOkClick；浏览... -> btnBrowserClick；数据选项 -> tsOptionsDblClick |
| `TFEESETFORM` | 证券交易费率 | 证券交易费率；此处设置为全局费率设置，新建证券账户将自动继承当前全局费率。请注意，修改全局费率仅对新账户生效，已建立的证券账户费率将保持不变。请点击表格进行费率调整。；操作；证券类型；买入印花税(%)；卖出印花税(%)；买入佣金(%)；买入最低佣金(元)；卖出佣金(%)；卖出最低佣金(元)；附加费(元)；过户费(‰)；结算费(%)；结算费上限(元)；交易规费(%)；更新费率；导出；打印 |  | 操作 -> btnOperateClick；操作 -> btnOperate2Click；更新费率 -> actUpFeeExecute；导出 -> miExportClick；打印 -> miPrintClick；导出 -> miExport2Click；打印 -> miPrint2Click |
| `TFILTERDLGFM` | 筛选 | 筛选；活动类型；资产；关键字；收支项目；<无>；主题；日期；确定；清空条件；到；不筛选金额；金额大于等于；金额小于等于；金额从 |  | 确定 -> btnOKClick；清空条件 -> btnDefaultClick；不筛选金额 -> RB1Click；金额大于等于 -> RB1Click；金额小于等于 -> RB1Click；金额从 -> RB1Click |
| `TFILTERTRANSFRAME` |  | 所有明细；当前交易明细；所有交易明细 |  | 所有明细 -> btnAllOrPartTransListClick |
| `TFINANCIALCALENDARDLG` | 财务日历 | 财务日历；日期；事务描述 |  | mwCalendar -> mwCalendarChange |
| `TFINANCIALDIAGNOSISFM` | 财务诊断 | 财务诊断；新增账户；资产性质设置；开始诊断；调整财务数据；定期；流动资产；投资资产；货币基金 |  | 新增账户 -> btnCreateAccountClick；btnInputDataType -> btnInputDataTypeClick；资产性质设置 -> btnAssetPropertySettingsClick；开始诊断 -> btnBeginClick；调整财务数据 -> btnReturnClick；流动资产 -> miFixedDeposit_LiquidAssetClick；投资资产 -> miFixedDeposit_InvestmentAssetClick；流动资产 -> miCurrFund_LiquidAssetClick；投资资产 -> miCurrFund_InvestmentAssetClick |
| `TFINANCIALPLANNINGCENTERFM` | 财务规划 | 财务规划；清除数据；未来重大事件；当前财务情况；家庭资料 |  | 清除数据 -> btnClearDataClick |
| `TFINANCINGBIDDLGFM` | 融资买入 | 融资买入；融资融券账户；融资年利率%；融资合同号；买入证券；买入价格；买入数量；费用小计；金额合计；更新代码；显示费用详情；印花税率 %；印花税费；佣金比例 %；佣金；过户费；附加费 |  | 更新代码 -> btnUpdateCodeClick；显示费用详情 -> chkvisibleClick |
| `TFINDDLGFM` | 查找 | 查找；查找项目；查找内容；查找下一个；重新开始 |  | Edit1 -> Edit1Change；查找下一个 -> RzButtonOkClick；重新开始 -> RzButton1Click |
| `TFINDFORM` | 查找 | 查找 |  | 查找 -> RzBitBtn1Click |
| `TFIXDEPMATUREDLGFM` | 续存 | 续存；存单；存期；存款类型；年利率(%)；可用资金；续存金额 |  |  |
| `TFIXDEPOSITSVIEWFRAME` |  |  |  |  |
| `TFIXEDACCTDLGFM` | 定期存款 | 定期存款；起存日期；存单号；存款类型；资金来源；主题；到期自动续存；存款金额；当前余额；存期；年利率(%)；加入账户组；开户银行；<无>；起存金额；<不考虑资金来源> |  | edAmount -> edAmountChange；edtMoney -> edAmountChange |
| `TFIXEDDEPOSITSTATISTICFRAME` |  | 所有；新增存单；账户组 \| 存单名称；存单类型；存期；起存日；到期日；年利率；余额；到期本息；删除 | `AcctName`；`DepositType`；`Term`；`BeginDate`；`EndDate`；`Rate`；`Balance`；`MatureSum` | 所有 -> btnAcctGroupClick；新增存单 -> btnCreateAcctClick；删除 -> miDeleteAssetClick |
| `TFIXEDDEPOSITTRANSFM` | 定期存单 | 定期存单；交易明细；账户概况 |  |  |
| `TFMCUSTOMDIALOG` | Custom AutoFilter | Custom AutoFilter；Show rows where:；Use ? to represent any single character；Use * to represent any series of characters |  |  |
| `TFMINCEXPCAPTIONFORM` | 管理常用备注 | 管理常用备注；新增；操作；修改；删除；导出；打印 |  | 新增 -> btnNewClick；操作 -> btnOptionClick；TreeList -> TreeListDblClick；修改 -> miEditClick；删除 -> miDeleteClick；导出 -> miExportClick；打印 -> miPrintClick |
| `TFOREIGNSTATISTICFRAME` |  | 获取牌价；币种；当前余额；当前牌价；折算金额；持有外汇调整；添加外汇牌价；当前持有外汇；所有交易过的外汇 | `CurrType`；`Amount`；`Price`；`LoaclAmount` | 获取牌价 -> btnUpdateDataClick；添加外汇牌价 -> ActAddPriceExecute |
| `TFOREIGNTRANSFM` | 外汇交易明细 | 外汇交易明细；交易明细；外汇构成 |  |  |
| `TFOREIGNTRANSFRAME` |  | 卖出金额；卖出币种；买入金额；买入币种；报价方式；成交汇率；当前选中币种交易明细 | `OutSum`；`OutCurr`；`InSum`；`InCurr`；`BuySellType`；`absPrice`；`TransType`；`AssetID1`；`AssetID2`；`Price` |  |
| `TFPANNUALSALARYINFODLGFM` | 工资 | 工资；确定；您的工资；年工资；元；结束年份；年；年增长率；配偶工资 |  | 确定 -> btnOKClick |
| `TFPASSETEXPENSESINFODLGFM` | 资产带来的支出 | 资产带来的支出；元；名称；来自资产账户；年；开始年份；年增长率；结束年份；年支出；持续；确定 |  | 确定 -> btnOKClick |
| `TFPASSETGROWTHINFODLGFM` | 资产增长 | 资产增长；您的资产（现金、投资、存款）预计年增长率；除此之外，当每年有现金盈余时，还可以拿出；的盈余来进行追加投资，以获得更多的现金资产；确定 |  | 确定 -> btnOKClick |
| `TFPASSETINCOMEINFODLGFM` | 资产带来的收入 | 资产带来的收入；名称；来自资产账户；年收入；元；年；结束年份；年增长率；开始年份；持续；确定 |  | 确定 -> btnOKClick |
| `TFPASSETPURCHASEPLANINFOFM` | 资产购置 | 资产购置；确定；元；名称；首付；年；购置年份；年利率；期数；月；购置金额；月供；分期付款；一次性付款；带来的收入；年增长率；持续；资产购置后每年带来的收入；带来的支出；资产购置后每年带来的支出 |  | 确定 -> btnOKClick；edtInstallmentsNumber -> edtAmountChange；edtAnnualRate -> edtAmountChange；分期付款 -> rbOneOffClick；一次性付款 -> rbOneOffClick；edtAmount -> edtAmountChange；edtDownPaymentAmount -> edtAmountChange |
| `TFPBASEDLGFM` | FPBaseDlgFm |  |  |  |
| `TFPBASEINFODLGFM` | 家庭资料 | 家庭资料；确定；您的资料；出生年份；年；预计寿命；岁；有配偶；配偶资料 |  | 确定 -> btnOKClick；edtMyBirthdayYear -> edtMyBirthdayYearChange；edtMyLifeExpectancy -> edtMyBirthdayYearChange；有配偶 -> chkSpouseClick；edtSpouseBirthdayYear -> edtSpouseBirthdayYearChange；edtSpouseLifeExpectancy -> edtSpouseBirthdayYearChange |
| `TFPDAILYEXPENSESINFODLGFM` | 日常支出 | 日常支出；家庭每年日常支出；元；日常支出指家庭维持基本生活所需的经常性开支，但不包含未来计划性支出。；确定 |  | 确定 -> btnOKClick |
| `TFPEDUCATIONEXPENSESINFODLGFM` | 教育计划 | 教育计划；元；名称；年；持续；开始年份；每年生活费；结束年份；每年学费；每年其它费用；合计；确定 |  | 确定 -> btnOKClick；edtLivingExpenses -> edtTuitionFeeChange；edtTuitionFee -> edtTuitionFeeChange；edtOtherExpenses -> edtTuitionFeeChange |
| `TFPEXPENSESADJUSTMENTINFODLGFM` | 支出调整 | 支出调整；名称；开始年份；结束年份；年日常支出增加；元；年；减少请填写负数；持续；确定 |  | 确定 -> btnOKClick |
| `TFPINFLATIONRATEINFODLGFM` | 通货膨胀率 | 通货膨胀率；通货膨胀率将作为您家庭日常支出的年增长率参考值，用于预测未来生活成本的变化趋势；确定 |  | 确定 -> btnOKClick |
| `TFPOTHEREXPENSESINFODLGFM` | 其它支出 | 其它支出；元；名称；年；开始年份；年增长率；结束年份；年支出；持续；确定 |  | 确定 -> btnOKClick |
| `TFPOTHERINCOMEINFODLGFM` | 其它收入 | 其它收入；年收入；年；结束年份；年增长率；开始年份；名称；元；持续；确定 |  | 确定 -> btnOKClick |
| `TFPRETIREMENTINFODLGFM` | 养老计划 | 养老计划；您；退休年龄；岁；退休金年收入；元；退休金年增长；退休后的家庭年支出；鉴于退休后将减少工作相关支出（如通勤费用等）且不再有工作收入，通常情况下，退休后的年支出/年收入水平都将低于当前工作期间的水平。；确定；配偶 |  | edtMyRetirementAge -> edtMyRetirementAgeChange；确定 -> btnOKClick；edtSpouseRetirementAge -> edtSpouseRetirementAgeChange |
| `TFPSELECTASSETSDLGFM` | 选择资产 | 选择资产；账户名称；余额；确定；新增账户 |  | 确定 -> btnOKClick；新增账户 -> btnCreateAssetClick |
| `TFPYEARDATAINFODLGFM` | 年度情况 | 年度情况；上一年；下一年 |  | 上一年 -> actPrevYearExecute；下一年 -> actNextYearExecute |
| `TFUNDBUYDLGFM` | 开放式基金申购 | 开放式基金申购；单位净值；申购份数；基金名称；申购费率 %；申购金额；资金账户；收费模式；申购费用；基金账户；更新基金；<无> |  | edTransDate -> edTransDateChange；edPrice -> edPriceChange；edFeeRate -> edPriceChange；edAmount -> edPriceChange；更新基金 -> btnUpdateCodeClick |
| `TFUNDCONVERTDLGFM` | 开放式基金转换 | 开放式基金转换；转为基金；转入份额；基金账户；更新基金；转换费用；单位净值；转为收费模式；资金账户；原有基金；申购费率；赎回费用；申购费用；转出份额；原有收费模式；<无>；主题；日期；备注；确 定 |  | 更新基金 -> btnUpdateCodeClick；edBuyFee -> edPriceChange；edNewQuantity -> edPriceChange；edNewPrice -> edPriceChange；edPrice -> edPriceChange；edQuantity -> edPriceChange；edFee -> edPriceChange；edSellFee -> edPriceChange；edTransDate -> edTransDateChange；确 定 -> btnOKClick |
| `TFUNDINTERESTDLGFM` | 基金现金红利 | 基金现金红利；金额；基金名称；资金账户；基金账户；本次收入记为；<无> |  |  |
| `TFUNDMARKBUYDLGFM` | 新基金认购确认 | 新基金认购确认；认购基金；资金账户；认购返款；认购金；认购金利息；认购金本息合计；日期；备注；基金账户；主题；中签；中签数量；购买金额合计；基金名称；中签价格；认购费用；<无>；确 定 |  | 中签 -> cbSignClick；确 定 -> btnSaveExitClick |
| `TFUNDORDERBUYDLGFM` | 新基金认购 | 新基金认购；单位净值；认购份数；基金名称；认购费率 %；认购金额；资金账户；基金账户；更新基金；<无> |  | 更新基金 -> btnUpdateCodeClick |
| `TFUNDREINVESTDLGFM` | 分红再投资 | 分红再投资；分红金额；单位净值；分红数量；基金名称；基金账户；本次收入记为 |  | edPrice -> edAmountChange；edAmount -> edAmountChange |
| `TFUNDSELLDLGFM` | 开放式基金赎回 | 开放式基金赎回；基金账户；本次盈亏记为；赎回费率 %；赎回金额；单位净值；赎回份额；基金名称；资金账户；申购费率 %；收费模式；赎回费用；<无> |  | edTransDate -> edTransDateChange；edPrice -> edPriceChange；edQuantity -> edPriceChange；edFeeRate -> edPriceChange；edFeeRateBuy -> edPriceChange |
| `TFUNDSPLITDLGFM` | 基金拆分 | 基金拆分；基金名称；拆分比例；原有份额；基金账户；拆分后份额 |  |  |
| `TFUTURESACCTDLGFM` | 期货账户 | 期货账户；创建日期；开户机构；<无> |  |  |
| `TFUTURESBUYDLGFM` | 期货开仓 | 期货开仓；期货账户；期货品种；到期年月；成交单价；成交数量；成交金额；手续费；保证金比例；保证金 |  |  |
| `TFUTURESCONTRACTLISTFM` | 期货合约列表 | 期货合约列表；操作；请输入要搜索的关键字...；代码；名称；日期；新增价格；显示单日所有价格；只显示持仓产品价格；产品名称；价格；新增；修改；删除；修改价格；删除价格；获取价格；查找；价格整理；导出；打印 | `TransObjID`；`Code`；`Name`；`PriceDate`；`ObjName`；`MessureQuant` | 期货合约列表 -> FormShow；操作 -> RzMenuButton1Click；RzDate -> RzDateChange；显示单日所有价格 -> RzCBOnlyDateClick；只显示持仓产品价格 -> RzCBOnlyHaveClick；操作 -> btn1Click；DBGridPrice -> ActModifyPriceExecute；删除 -> ActDeleteExecute；新增价格 -> ActAddPriceExecute；修改价格 -> ActModifyPriceExecute；删除价格 -> ActDeletePriceExecute；获取价格 -> ActGetPriceExecute；查找 -> N4Click；导出 -> miExportClick；打印 -> miPrintClick；导出 -> miExportPriceClick；打印 -> miPrintPriceClick |
| `TFUTURESGOODSLISTFM` | 期货品种列表 | 期货品种列表；新增期货；操作；请输入要搜索的关键字...；代码名称；报价单位；每手数量；交易单位；手续费；保证金比例(%)；交易所；修改期货；删除期货；导出；打印 | `TransObjID`；`FeeType`；`Name`；`QuotationUnit`；`Quantity`；`TradingUnit`；`Fee`；`MarginRatio`；`ExchangeName`；`ID`；`CnName`；`IsStockIndex`；`FeeRate`；`Exchangename` | 期货品种列表 -> FormShow；操作 -> RzMenuButton1Click；MHBGSecurity -> MHBGSecurityDblClick；新增期货 -> actAddSecurityExecute；修改期货 -> actEditSecurityExecute；删除期货 -> actDeleteSecurityExecute；导出 -> miExportClick；打印 -> miPrintClick |
| `TFUTURESSELLDLGFM` | 期货平仓 | 期货平仓；期货账户；期货合约；成交单价；成交数量；成交金额；手续费；收回保证金；收回金额 |  | edTransDate -> edTransDateChange |
| `TFUTURESSTATISTICFRAME` |  | 获取合约价格；期货合约；数量(手)；保证金；市值；占比%；浮动盈亏；均价；收盘价；浮动收益率%；添加合约价格；证券代码变更；期货品种设置；当前持仓合约；所有交易过的合约 | `ObjName`；`Amount`；`MarginCost`；`TheValue`；`Scale`；`PAL`；`Price`；`MarketPrice`；`ProfitRate` | 获取合约价格 -> btnUpdateDataClick；BrowseGrid -> BrowseGridDblClick；添加合约价格 -> ActAddPriceExecute；期货品种设置 -> mmiFuturesGoodsClick |
| `TFUTURESTRANSFM` | 期货账户交易明细 | 期货账户交易明细；交易明细；历史盈亏 |  |  |
| `TFUTURESTRANSFRAME` |  | 期货合约；价格；数量；总费用；交易金额；单个合约交易明细 | `CategoryName`；`ObjName`；`Price`；`Quantity`；`TotalFee`；`AMT`；`Bala`；`Iterbala`；`Commission`；`TransObjID` |  |
| `TFUTURESVIEWFRAME` |  |  |  |  |
| `TGOALACCTLISTDLG` | 财务目标账户余额列表 | 财务目标账户余额列表；账户；余额/市值；合计 |  |  |
| `TGOALCENTERFM` | 财务目标 | 财务目标；新增目标；设置；显示已过期目标；修改；删除 |  | 新增目标 -> BtnAddClick；设置 -> btnSettingClick；显示已过期目标 -> miShowExpiredClick；修改 -> miModifyClick；删除 -> miDeleteClick |
| `TGOALSAVEFM` | 财务目标 | 财务目标；目标金额；目标名称；结束日期；开始日期；保存；全部账户 |  | 保存 -> btnSaveClick；全部账户 -> RCAllClick |
| `TGOLDACCTDLGFM` | 贵金属账户 | 贵金属账户；创建日期；开户机构；默认资金账户；自身；其它；<无> |  | 自身 -> rbSelfCapitalClick；其它 -> rbSelfCapitalClick |
| `TGOLDBUYDLGFM` | 贵金属买入 | 贵金属买入；单价；数量；手续费；总金额；资金账户；投资账户；产品；更新产品；<无> |  | 更新产品 -> btnUpdateCodeClick |
| `TGOLDLISTFM` | 贵金属产品列表 | 贵金属产品列表；新增产品；操作；请输入要搜索的关键字...；名称；币种；日期；新增价格；显示单日所有价格；只显示持仓产品价格；产品名称；价格；修改产品；删除产品；修改价格；删除价格；获取价格；价格整理；查找；导出；打印 | `TransObjID`；`PreciousMetalsName`；`CurrType`；`PriceDate`；`ObjName`；`MessureQuant` | 贵金属产品列表 -> FormShow；操作 -> RzMenuButton1Click；DBGridList -> ActModifyExecute；RzDate -> RzDateChange；显示单日所有价格 -> RzCBOnlyDateClick；只显示持仓产品价格 -> RzCBOnlyHaveClick；操作 -> btn1Click；DBGridPrice -> ActModifyPriceExecute；新增产品 -> ActAddExecute；修改产品 -> ActModifyExecute；删除产品 -> ActDeleteExecute；新增价格 -> ActAddPriceExecute；修改价格 -> ActModifyPriceExecute；删除价格 -> ActDeletePriceExecute；获取价格 -> ActGetPriceExecute；价格整理 -> ActConvertCodeExecute；查找 -> N4Click；导出 -> miExportClick；打印 -> miPrintClick；导出 -> miExportPriceClick；打印 -> miPrintPriceClick |
| `TGOLDSELLDLGFM` | 贵金属卖出 | 贵金属卖出；单价；数量；手续费；总金额；资金账户；投资账户；产品；<无> |  |  |
| `TGOLDSTATISTICFRAME` |  | 获取价格；产品；持仓数量；买入均价；持仓成本；市值；占比%；浮动盈亏；浮动收益率%；最新行情；添加贵金属价格；当前持仓贵金属；所有交易过的贵金属 | `ObjName`；`Amount`；`Price`；`Cost`；`TheValue`；`Scale`；`PAL`；`ProfitRate`；`MarketPrice` | 获取价格 -> btnUpdateDataClick；BrowseGrid -> BrowseGridDblClick；添加贵金属价格 -> ActAddPriceExecute |
| `TGOLDTRANSFM` | 贵金属交易明细 | 贵金属交易明细；交易明细；市值构成和变动；历史盈亏 |  |  |
| `TGOLDTRANSFRAME` |  | 产品名称；单价；数量；交易金额；单只贵金属交易明细 | `CategoryName`；`TransObjID`；`Price`；`Quantity`；`AMT`；`Bala`；`Iterbala` |  |
| `TGUIDEDLG` | GuideDlg |  |  |  |
| `THISTORYPROFITFRAME` |  | 操作；交易日期；名称；活动类型；价格；数量；交易金额；实现盈亏；盈亏比例；导出；打印 | `TDate`；`ObjName`；`Name`；`Price`；`Quantity`；`AMT`；`PLAmount`；`YKRate`；`TransID`；`TransObjectID`；`YLAmount`；`KSAmount`；`ObjectTypeID` | btnShowType -> btnShowTypeClick；操作 -> btnOperateClick；导出 -> miExportClick；打印 -> miPrintClick |
| `TIMPORTCATEGORYDLGFM` | 替换收支项目 | 替换收支项目；查询记录；将选中记录的收支项目替换为；确定替换；日期；收支项目；流入金额；流出金额；币种；资金账户/款项；主题；备注 | `transid`；`Transdate`；`CName`；`inc`；`exp`；`sObjName`；`AcctName`；`Theme`；`Description`；`id`；`TransDate`；`CType`；`TransObjectID`；`Amount`；`AcctNo1`；`Inc`；`Exp`；`TransID`；`FID`；`TransType`；`NID`；`StateID` | 查询记录 -> btnFilterClick；确定替换 -> btnSaveExitClick |
| `TIMPORTDATAFM` | 导入数据 | 导入数据；导入文件名；导入数据选项；浏览...；双击此处全选/取消全选；账户信息；人员机构；货币信息；收支项目；收支预算；计划日记；证券列表；基金列表；债券列表；交易信息；物品信息；交易费率；提醒设置；记账模板；生活主题；理财产品；贵金属；货币基金；历史汇率；物品历史价格；理财目标；确定 |  | BtnOk -> BtnOkClick；浏览... -> btnBrowserClick；OptionsGroup -> OptionsGroupDblClick；确定 -> BtnOkClick |
| `TIMPORTJIAOGEDANDLGFM` | 导入股票交割单 | 导入股票交割单；粘贴；匹配方案；删除方案；方案另存为；显示方案详细内容；各列之间分隔符；单个半角字符；制表符Tab；空格；其它；自动识别；匹配交易类型；证券买入；证券卖出；新股申购；申购中签；申购返款；送股；配股；红利；利息收入；其它费用；资金转入；资金转出；匹配交易数据项；日期；证券代码；证券名称；价格；数量；金额；印花税；佣金；过户费；以“列头文字”匹配；以“列序号(第几列)”匹配；金额已包含后面的费用项；下一步；行号；交易类型；标签；申购关联标记；确认导入；上一步；批量修改；关联新股申购；卖出和红利盈亏记为；导入到证券账户；交易资金账户；转账资金账户；<无>；修改交易类型；修改证券代码；修改标签；取消关联 |  | 粘贴 -> btnPasteDataClick；删除方案 -> btnProgramDeleteClick；方案另存为 -> btnProgramSaveClick；显示方案详细内容 -> chkShowProgramDetailedClick；制表符Tab -> rbOnClick；空格 -> rbOnClick；其它 -> rbOnClick；自动识别 -> btnAutoDiscernClick；下一步 -> btnBeginClick；确认导入 -> btnImportClick；上一步 -> btnBackClick；批量修改 -> btnUpdateClick；关联新股申购 -> btnSignClick；修改交易类型 -> miUpdateTransTypeClick；修改证券代码 -> miUpdateCodeClick；修改标签 -> miUpdateTagClick；关联新股申购 -> miSignClick；取消关联 -> miCancelSignClick |
| `TIMPORTPREVIEWFM` | 导入预览 | 导入预览；原始数据；准备导入的记录；导入选中的记录 |  | pcPreview -> pcPreviewChange；导入选中的记录 -> btnImportClick |
| `TIMPORTSELECTDLGFM` | 导入数据 | 导入数据；从文件导入；从剪贴板导入 |  | mwIconList -> mwIconListClick；从文件导入 -> btnImportClick；从剪贴板导入 -> btnImportFromClipboardClick |
| `TIMPORTTHEMEDLGFM` | 主题数据设置 | 主题数据设置；将选中记录加入；设置；查询记录；日期；活动类型；流入金额；流出金额；币种；资金账户/款项；主题；备注 | `transid`；`CateID`；`Transdate`；`CategoryName`；`inc`；`exp`；`ObjName`；`AcctID`；`TransTheme`；`sDesc`；`Description`；`cacct`；`acctno1`；`acctno2`；`CategoryID`；`transtype`；`sum1`；`sum2`；`XX`；`TransObjId`；`Theme`；`id`；`AcctName`；`Inc`；`Exp`；`StateID`；`CType` | 设置 -> btnSaveExitClick；查询记录 -> btnFilterClick |
| `TINCEXPCAPIONDLGFM` | 备选说明 | 备选说明；常用备注；保存 |  | 保存 -> RzBtnSaveClick |
| `TINCEXPDLGFM` | 日常收支 | 日常收支 |  |  |
| `TINCEXPEDITFRAME` |  | 主题；备注；日期；金额；收支账户；收支项目；分期付款 |  | 分期付款 -> btnInstallmentClick |
| `TINCEXPINSTALLMENTWIZARDDLG` | 日常支出分期 | 日常支出分期；支出信息；分期信息；确认信息；完成后，软件将生成以下内容 |  |  |
| `TINCEXPPLANDLGFM` | 收支计划 | 收支计划；资金账户；收支项目；金额；主题；自动执行；您可通过系统设定财务计划，例如每月工资入账、固定周期缴费等事项。 |  | 自动执行 -> chkAutoExecuteClick |
| `TINFORMATIONDLGFM` | 资料管理 | 资料管理 |  |  |
| `TINPUTTEXTDLGFM` | InputTextDlgFm | 确定 |  | 确定 -> btnOKClick |
| `TINSTALLMENTEDITDLG` | 分期付款 | 分期付款；保存 |  | 保存 -> btnSaveExitClick |
| `TINSTALLMENTEDITFRAME` |  | 利息支付方式；手续费率(%)；手续费；手续费支付方式；每期还款总计；首次记账日期；利率(%)；利息；申请日期；总期数；已入账期数；备注；信用卡账户；以后每期还款；申请分期金额；关联收支项目；到达还款日后自动减少未还期数 |  | 关联收支项目 -> lblCategoryClick；edtAmount -> edtAmountChange；edtCount -> edtAmountChange；edtFeeAmount -> edtAmountChange；edtRateAmount -> edtAmountChange |
| `TINSTALLMENTFRAME` |  | 新增；操作；申请日期；总期数；分期总额；总手续费；总利息；每期偿还本金；每期手续费；每期利息；未还期数；未还总额；备注；修改；删除 | `CreateDate`；`StagesCount`；`TransAmount`；`FeeAll`；`RateAll`；`StagesAmount`；`FeeStages`；`RateStages`；`WHCount`；`WHAmount`；`Description`；`ID`；`CompletedCount`；`FeeType`；`RateType` | 新增 -> btnAddClick；操作 -> btnOperateClick；btnShowType -> btnShowTypeClick；mhbgData -> miEditClick；修改 -> miEditClick；删除 -> miDeleteClick |
| `TINSUREACCTDLGFM` | 保险账户 | 保险账户；保单号；保险机构；投保金额；缴费年限；生效日期；终止日期；投保人；受益人；被保险人；保险种类；终生有效；<无>；社保编码；城市；参保人；将保费做为收支统计 |  | 终生有效 -> ckbIsForLife0Click |
| `TINSUREBALAINDLGFM` | 保险价值增加 | 保险价值增加；金额；保险账户 |  |  |
| `TINSUREBALAOUTDLGFM` | 保险价值减少 | 保险价值减少；金额；保险账户 |  |  |
| `TINSURECASHVALUEEDITDLGFM` | 保险现金价值 | 保险现金价值；日期；现金价值；确定 |  | 确定 -> btnSaveClick |
| `TINSURECASHVALUEFRAME` |  | 只有将保费作为收支统计，才能单独管理保险的现金价值。 可以在账户概况中修改。；日期；现金价值；添加；修改；删除 | `PriceDate`；`Price` | mhbgData -> mhbgDataDblClick；添加 -> btnAddClick；修改 -> btnUpdateClick；删除 -> btnDeleteClick |
| `TINSUREDIVIDENDFM` | 保险分红 | 保险分红；保险账户；领取账户；金额 |  |  |
| `TINSUREGETFEEDLGFM` | 保费返还 | 保费返还；领取账户；金额；保险账户；<无> |  |  |
| `TINSUREOVERDLGFM` | 退保 | 退保；退保到账户；金额；保险账户；同时终止保险账户；<无> |  |  |
| `TINSUREPAYFEEDLGFM` | 缴纳保费 | 缴纳保费；支付账户；金额；保险账户；<无> |  |  |
| `TINSURETRANSFM` | 保险交易明细 | 保险交易明细 |  |  |
| `TINSURETRANSFRAME` |  | 缴费；领取；管理现金价值；修改缴费计划 | `CategoryName`；`Inc`；`Exp`；`Iterbala`；`Amount` | 管理现金价值 -> miCashValueClick；修改缴费计划 -> miModifyPlanClick |
| `TINSUREVIEWFRAME` |  |  |  |  |
| `TINVESTFEEDLGFM` | 其它费用或利息 | 其它费用或利息；金额；资金账户；币种；费用；利息收入 |  | selInvestAcct -> selInvestAcctChange |
| `TINVESTMENTCHARTFRAME` |  |  |  | btnType -> btnTypeClick |
| `TINVESTMENTLISTFM` | 投资一览 | 投资一览；操作；更新行情数据；设为软件首页 |  | 操作 -> btnMoreClick；btnDataChange -> btnDataChangeClick；更新行情数据 -> btnUpdateDataClick；设为软件首页 -> N6Click |
| `TLIFETHEMEFM` | 标签 | 标签；查找；批量操作；其它；查看交易记录；日期；活动类型；流入；流出；资金账户/款项；主题；备注；币种；查看资产；账户名称；资金余额/资产总值；交易记录；资产账户；新增标签；操作；名称；从当前主题中移出；从所有主题中移出；从当前主题转移到...；从所有主题转移到...；快速加入主题；修改主题；删除主题；隐藏主题；新增主题；标签排序；显示隐藏标签；批量设置标签；设为软件首页；导出；筛选；放弃筛选；移出主题；转移到；打印 | `FakeTransDate`；`CategoryName`；`IncAmount`；`ExpAmount`；`AcctName`；`TransTheme`；`sDesc`；`ObjName`；`TransID`；`CateID`；`TransType`；`TransDate`；`UserMark`；`Name`；`Amount`；`CurrType`；`ID`；`CType`；`AcctNo1`；`AcctNo2`；`StateID`；`TransAmount`；`IncCurrency`；`ExpCurrency`；`CreateTime` | 查找 -> btnFindClick；批量操作 -> btnBulkActionClick；其它 -> btnOtherClick；DBGrid -> DBGridDblClick；操作 -> btnSettingClick；myTagList -> myTagListClick；从当前主题中移出 -> actDeleteTagExecute；从所有主题中移出 -> actDeleteAllExecute；从当前主题转移到... -> actMoveTagExecute；从所有主题转移到... -> actMoveAllTagExecute；快速加入主题 -> actAddTagExecute；修改主题 -> actModifyExecute；删除主题 -> actDeleteExecute；隐藏主题 -> actHideExecute；新增主题 -> actAddExecute；标签排序 -> miEditTagsOrderClick；查找 -> miFindClick；显示隐藏标签 -> mmiViewClick；批量设置标签 -> mmiBatchTagsClick；设为软件首页 -> miSetHomePageClick；导出 -> miExportTagClick；查找 -> mmiFindClick；筛选 -> mmiFilterClick；放弃筛选 -> miClearFilterClick；导出 -> N11Click；打印 -> N12Click |
| `TLIMITREMINDDLG` | 限额提醒 | 限额提醒；新增提醒；操作；类别；提醒条件；生效；新增账户余额提醒；新增信用卡透支额提醒；新增证券市价提醒；新增开放式基金价格提醒；修改；删除 |  | 操作 -> btnCustomClick；TreeList -> TreeListDblClick；新增账户余额提醒 -> N1Click；新增信用卡透支额提醒 -> N2Click；新增证券市价提醒 -> N3Click；新增开放式基金价格提醒 -> N4Click；修改 -> miModifyClick；删除 -> miDeleteClick |
| `TLOGINDIALOG` | Database Login | Database Login；&User Name: |  | Database Login -> FormShow |
| `TLZCASHDEPDLGFM` | 存款 | 存款；资金来源；存款账户；金额 |  |  |
| `TMAINFORM` | MainForm | 财智8；资产；分析；目标；激活高级功能；全部收起；全部展开；按[类型]显示；按[自定义]显示；设置[自定义]显示；显示金额；显示到期账户；显示隐藏账户；财务数据；财务报表；财务分析；同步数据；今日提醒；打开财智8；账簿；新建账簿；打开账簿；结算账簿；设置账簿密码；关闭当前打开的账簿；备份账簿；还原账簿；导入账簿数据；导出账簿数据；资料管理；收支项目；人员与机构；上市证券；开放式基金；货币基金；债券；贵金属；银行理财产品；期货合约；期货品种；贵金属TD品种；重大资产；家居物品；证券交易费率；其它金融产品；币种与汇率；存款利率；常用备注；计划提醒；财务日历；计划与提醒；限额提醒；财务工具；更新行情数据；导入股票交割单；日记；金融计算器；Windows计算器；设置；系统设置；快捷键设置；同步设置；手机提醒设置；修改同步账号密码；删除同步账号密码；帮助；财智8常见问题解答；客户服务；检查软件更新；软件许可；最近使用的序列号；访问财智在线理财；访问财智公司官网；关于；退出 |  | MainForm -> FormShow；pnlToolsBar -> pnlToolsBarDblClick；btnMainPopupMenuCenter -> btnMainPopupMenuCenterClick；btnMainPopupMenuRight -> btnMainPopupMenuCenterClick；sbClose -> sbCloseClick；sbStoreMax -> pnlToolsBarDblClick；sbMin -> sbMinClick；sbMax -> pnlToolsBarDblClick；btnCustomerService -> btnCustomerServiceClick；imgTitle -> btnMainPopupMenuCenterClick；btnBack -> btnBackClick；btnNext -> btnNextClick；btnCenter -> btnCenterClick；btnAddTrans -> btnAddTransClick；btnSync -> btnSyncClick；btnRemind -> btnRemindClick；btnTheme -> btnThemeClick；btnFinancialTools -> btnFinancialToolsClick；财智8 -> btnMainPopupMenuCenterClick；btnHideNavigation2 -> btnHideNavigation2Click；bmpbtnRegister -> bmpbtnRegisterClick；imgReg -> bmpbtnRegisterClick；激活高级功能 -> bmpbtnRegisterClick；pnlLeftBar -> pnlLeftBarDblClick；btnAddAcct -> btnAddAcctClick；btnHideNavigation -> btnHideNavigationClick；ActEscCloseForm -> ActEscCloseFormExecute；全部收起 -> mmiAcctListAllNotExpandedClick；全部展开 -> mmiAcctListAllExpandedClick；按[类型]显示 -> mmiAcctOrderByTypeClick；按[自定义]显示 -> mmiAcctOrderByCustomClick；设置[自定义]显示 -> mmiCustomAcctClick；显示金额 -> mmiShowAcctTreeAmountClick；显示到期账户 -> mmiShowFinishedAcctClick；显示隐藏账户 -> mmiShowHideAcctClick；财务数据 -> miFinanceDataClick；财务报表 -> miFinanceReportClick；财务分析 -> miFinanceAnalysisClick；同步数据 -> btnSyncClick；今日提醒 -> btnRemindClick；打开财智8 -> miShowWindowClick；账簿 -> miBookClick；新建账簿 -> mmiNewbookClick；打开账簿 -> mmiOpen_NewClick；结算账簿 -> mmiRecalcClick；设置账簿密码 -> mmiSetBookPasswordClick；关闭当前打开的账簿 -> mmiCloseBookClick；备份账簿 -> mmiBackupClick；还原账簿 -> mmiRestoreClick；导入账簿数据 -> mmiImportClick；导出账簿数据 -> mmiExportClick；收支项目 -> miInformationClick；人员与机构 -> miInformationClick；上市证券 -> miInformationClick；开放式基金 -> miInformationClick；货币基金 -> miInformationClick；债券 -> miInformationClick；贵金属 -> miInformationClick；银行理财产品 -> miInformationClick；期货合约 -> miInformationClick；期货品种 -> miInformationClick；贵金属TD品种 -> miInformationClick；重大资产 -> miInformationClick；家居物品 -> miInformationClick；证券交易费率 -> miInformationClick；其它金融产品 -> miInformationClick；币种与汇率 -> miInformationClick；存款利率 -> miInformationClick；常用备注 -> miInformationClick；财务日历 -> mmiFinancialCalendarClick；计划与提醒 -> mmiPlanClick；限额提醒 -> mmiLimitRemindClick；更新行情数据 -> mmiUpdateRateClick；导入股票交割单 -> mmiImportJGDClick；日记 -> mmiDirayClick；金融计算器 -> mmiJRCalculatorClick；Windows计算器 -> mmiCalculatorClick；系统设置 -> miSystemSettingsClick；快捷键设置 -> miTransShortcutManagnClick；同步设置 -> mmiSyncClick；手机提醒设置 -> mmiRemoteNotificationSettingClick；修改同步账号密码 -> miModifySyncUserPasswordClick；删除同步账号密码 -> miDeleteSyncUserPasswordClick；财智8常见问题解答 -> miFAQClick；客户服务 -> mmiHelpClick；检查软件更新 -> mmiSoftUpdateClick；软件许可 -> mmiRegisterClick；最近使用的序列号 -> mmiLastUseSerialNumberClick；访问财智在线理财 -> mmiMHOnlineURLClick；访问财智公司官网 -> mmiSoftWareURLClick；关于 -> mmiAboutClick；退出 -> miCloseClick |
| `TMANAGEBILLDATEDLGFM` | 账单日管理 | 账单日管理；设置；删除；设置日期；账单日 |  | 设置 -> btnModifyClick；删除 -> btnDeleteClick；treeList -> treeListDblClick |
| `TMARGINACCTDLGFM` | 融资融券账户 | 融资融券账户；创建日期；开户机构；融资年利率(%)；融券年利率(%)；<无> |  |  |
| `TMARGININTERESTREPAYMENTSDLGFM` | 利息返还 | 利息返还；融资融券账户；融资融券合约；返还利息 |  |  |
| `TMARGINSTATISTICFRAME` |  | 获取收盘价；证券/合约；持仓数量；持仓成本；市值；占比%；浮动盈亏；交易盈亏；均价；保本价；收盘价；浮动收益率%；添加股票价格；证券代码变更；融资融券费率设置；证券费率设置；当前持仓证券；所有交易过的证券 | `ObjName`；`Amount`；`Cost`；`TheValue`；`Scale`；`PAL`；`PALWithFee`；`Price`；`LowPrice`；`MarketPrice`；`ProfitRate` | 获取收盘价 -> btnUpdateDataClick；BrowseGrid -> BrowseGridDblClick；添加股票价格 -> ActAddPriceExecute；证券代码变更 -> ActChangeCodeExecute；融资融券费率设置 -> miMarginFeeSetClick；证券费率设置 -> mmiFeeSetClick |
| `TMARGINTRANSFM` | 融资融券账户交易明细 | 融资融券账户交易明细；交易明细；历史盈亏 |  |  |
| `TMARGINTRANSFRAME` |  | 证券/合约；价格；数量；佣金；总费用；交易金额；单只证券交易明细 | `ObjName`；`Price`；`Quantity`；`Commission`；`TotalFee`；`AMT`；`CategoryName`；`Bala`；`Iterbala`；`SID`；`TransObjID` |  |
| `TMARGINVIEWFRAME` |  |  |  |  |
| `TMARKETCONSTITUTESFRAME` |  | 名称；今日市值；昨日市值；涨跌额；涨跌幅 | `Name`；`NewValue`；`UpValue`；`ZDE`；`ZF` |  |
| `TMARKETDEBTSTATISTICFRAME` |  | 债券代码名称；数量；投资金额；面值；年利率%；年限；到期日；当前持仓债券；所有交易过的债券 | `ObjName`；`Quantity`；`Cost`；`ParValue`；`Rate`；`Scale`；`MatureDate` | BrowseGrid -> BrowseGridDblClick |
| `TMARKETDEBTTRANSFM` | 债券交易明细 | 债券交易明细；交易明细；成本市值构成；历史盈亏 |  |  |
| `TMARKETDEBTTRANSFRAME` |  | 债券代码名称；净价；应计利息；数量；费用；交易金额；单只债券交易明细 | `CategoryName`；`TransObjID`；`Price`；`Commission`；`Quantity`；`TotalFee`；`AMT`；`Bala`；`Iterbala` |  |
| `TMHFRAME` |  |  |  |  |
| `TMISCDIALOGFM` | MiscDialog |  |  |  |
| `TMODIFYBILLDATEDLGFM` | 设置账单日 | 设置账单日；设置日期；日；固定账单日，每月；每月最后一天是账单日；确 定 |  | 固定账单日，每月 -> RBBillType0Click；每月最后一天是账单日 -> RBBillType0Click；确 定 -> btnSaveExitClick |
| `TMONEYACCTDLGFM` | 银行理财产品账户 | 银行理财产品账户；创建日期；默认资金账户；开户机构；自身；其它；<无> |  | 自身 -> rbSelfCapitalClick；其它 -> rbSelfCapitalClick |
| `TMONEYBUYDLGFM` | 银行理财产品申购 | 银行理财产品申购；理财账户；资金账户；申购金额；产品名称；<无> |  |  |
| `TMONEYINFOVIEWFRAME` |  |  |  |  |
| `TMONEYLISTFM` | 银行理财产品列表 | 银行理财产品列表；新增产品；操作；请输入要搜索的关键字...；代码；产品名称；币种；收益起始日；委托期；收益终止日；预期年收益率(%)；已注销；修改产品；删除产品；注销产品/取消注销；查找；显示已注销的理财产品；导出；打印 | `TransObjID`；`ProductNo`；`Name`；`CurrType`；`BeginDate`；`Term`；`EndDate`；`YRate`；`id`；`IsWriteOff`；`DateType`；`InstitutionID`；`IsPreservation` | 操作 -> RzMenuButton1Click；MHBGSecurity -> MHBGSecurityDblClick；新增产品 -> actAddSecurityExecute；修改产品 -> actEditSecurityExecute；删除产品 -> actDeleteSecurityExecute；注销产品/取消注销 -> actWirteOffExecute；查找 -> N1Click；显示已注销的理财产品 -> miShowAllClick；导出 -> miExportClick；打印 -> miPrintClick |
| `TMONEYMATUREDLGFM` | 银行理财产品到期 | 银行理财产品到期；理财账户；到期本金；资金账户；收益；<无> |  |  |
| `TMONEYPRODUCTSVIEWFRAME` |  |  |  |  |
| `TMONEYREDEEMDLGFM` | 银行理财产品赎回 | 银行理财产品赎回；赎回日期；理财账户；实际收回金额；资金账户；赎回损益；赎回本金；产品名称；大于0为收益，小于0为损失；<无> |  |  |
| `TMONEYSTATISTICFRAME` |  | 产品名称；机构；累计金额；占比%；购买日；到期日；预计年收益率%；当前持仓产品；所有交易过的产品 | `ObjName`；`Organ`；`Cost`；`Scale`；`BeginDate`；`EndDate`；`ProfitRate` | BrowseGrid -> BrowseGridDblClick |
| `TMONEYTRANSFM` | 银行理财产品交易明细 | 银行理财产品交易明细；交易明细；市值构成；历史盈亏；产品资料 |  |  |
| `TMONEYTRANSFRAME` |  | 产品名称；交易金额；单个产品交易明细 | `CategoryName`；`TransObjID`；`AMT`；`Bala`；`Iterbala` |  |
| `TMONTHDAYFM` | 日历 | 日历 |  | mwCalendarPanel -> mwCalendarPanelChange |
| `TMONTHINCEXPCOLUMNCHARTFRAME` |  |  |  | btnUnit -> btnUnitClick |
| `TMWADJUSTBUTTONDROP` | mwAdjustButtonDrop | 年；月；确 定 |  | mwAdjustButtonDrop -> FormShow；确 定 -> btnOKClick |
| `TMWSELECTACCOUNTDROP` |  | 单账户；没有可用账户，请点击下方“新增账户”；多账户；搜索；[新增账户]；确 定 |  | mwSelectAccountDrop -> FormShow；pgAccount -> pgAccountChange；[新增账户] -> btnNewAccountClick；确 定 -> btnOKClick |
| `TMWSELECTCATEGORYDROP` |  | 支出；收入；搜索；[新增]；[收支项目管理] |  | mwSelectCategoryDrop -> FormShow；pgCategory -> pgCategoryChange；[新增] -> btnNewCategoryClick；[收支项目管理] -> btnManageCategoryClick |
| `TMWSELECTTAGDROP` |  | 标签；确 定；[新增标签] |  | mwSelectTagDrop -> FormShow；pgTag -> pgTagChange；确 定 -> btnOKClick；[新增标签] -> btnNewTagClick |
| `TNEWACCTTYPEDLGFM` | 新增资产账户 | 新增资产账户；账户作为财务管理的基础单元，支持多账户分类管理体系。您可根据资金用途、账户类型等维度创建账户，构建清晰的账户架构，实现财务数据的系统化管理。；现金储蓄；金融投资；重大资产；债权债务；保险；信用卡；储蓄卡；第三方储值；基金；预收/预付；垫付/待摊；融资融券；网贷；贵金属；现金；上市证券；银行理财产品；债券；房产；汽车；家居物品；其它重大资产；借入；借出；社保；商业保险；期货；外汇；单币信用卡；双币信用卡；活期(卡/折)；定期；活期一本通；定期一本通；一卡通；支付宝；微信钱包；财付通；其它储值账户；开放式基金；货币基金；预收款；预付款；垫付款；待摊费用；现货贵金属；贵金属TD |  |  |
| `TNEWACCTWIZARDCASHDLGFM` | 现金账户 | 现金账户；您可通过创建独立的现金账户，为每位家庭成员建立专属的现金管理单元，完整记录日常收支明细，包括工资收入、日常消费等各类资金流动情况，实现家庭财务的精细化管理。；所有者；备注；账户名称；币种；属于账户组；<无>；日期；账户余额 |  |  |
| `TNEWACCTWIZARDCREDITCARDDLGFM` | 信用卡账户 | 信用卡账户；您可为每位家庭成员分别创建独立的信用卡账户，精准记录每张信用卡的消费明细、还款周期及信用额度使用情况，实现家庭信用卡消费的全面管理和风险控制。；备注；所有者；币种；账户名称；属于账户组；<无>；启用日期；账单日；还款日；已透支金额；当透支额大于；时提醒；日；每月；每月最后一天是账单日；固定账单日；天；账单日之后；固定还款日；透支提醒 |  | 每月最后一天是账单日 -> RBBillType0Click；固定账单日 -> RBBillType0Click；账单日之后 -> RBPayType0Click；固定还款日 -> RBPayType0Click；透支提醒 -> cbIsAwakeClick |
| `TNEWACCTWIZARDCURRENCYONECARDDLGFM` | 活期一本通 | 活期一本通；您可根据需求，创建多个活期存款账户组。每个账户组可整合多个活期子账户，实现资金的分类管理和统一监控，满足多样化的财务管理需求。；一本通账户组名称；所有者；子账户名称；币种；备注；开户日期；账户金额；资金来源；属于一本/卡通；当活期存折、银行卡是某个一卡通或者活期一本通的子账户时，可以选择此项，方便归类管理。；<不考虑资金来源> |  |  |
| `TNEWACCTWIZARDCURRENTDLGFM` | 活期存折银行卡 | 活期存折银行卡；您可通过创建活期账户，统一管理存折、银行卡等资金载体，完整记录存取款、转账汇款、消费支付等资金流动。该账户既可独立使用，也可作为一卡通或活期一本通的子账户，实现资金的灵活管理和统筹调配。；所有者；备注；币种；账户名称；属于账户组；<无>；资金来源；账户余额；开户日期；<不考虑资金来源> |  |  |
| `TNEWACCTWIZARDCURRFUNDDLGFM` | 货币基金账户 | 货币基金账户；您可创建多个货币基金账户，专业管理在不同基金公司开立的货币基金投资。完整记录申购、赎回及收益结转等交易明细，监控资金流动性和收益率，为您提供便捷的现金管理工具。；账户名称；备注；所有者；币种；属于账户组；<无>；资金来源；日期；资产性质；余额；其它账户；账户自身；投资；储蓄 |  | 其它账户 -> rbCAcctSelfClick；账户自身 -> rbCAcctSelfClick |
| `TNEWACCTWIZARDDEBTINVESTMENTDLGFM` | 网贷 | 网贷；您可按P2P平台创建独立的网贷账户，实现对各投资平台的精细化管控。该功能支持全面记录债权明细、资金流动及收益情况，助您掌握网贷投资组合表现，有效管控投资风险。；所有者；备注；账户名称；币种；属于账户组；<无>；日期；账户余额；平台名称；平台网址；同时添加此平台到机构中 |  | edtPlatformName -> edtPlatformNameChange |
| `TNEWACCTWIZARDDEPOSITONECARDDLGFM` | 定期一本通 | 定期一本通；您可创建多个定期存款账户组，每个账户组可集中管理多个定期子账户。通过分组管理，您可以清晰掌握不同期限、不同用途的定期存款分布，实现定期存款的精细化管理和收益优化。；一本通账户组名称；所有者；子账户名称；备注；币种；起存日期；存期；年利率(%)；存款类型；到期自动续存；属于一本通；当活期存折、银行卡是某个一卡通或者活期一本通的子账户时，可以选择此项，方便归类管理；取款去向；月取金额；<不考虑取款去向>；已存金额；存款来源；存款金额；<不考虑存款来源> |  | edtTerm -> edtTermChange |
| `TNEWACCTWIZARDDLGFM` | NewAcctWizardDlgFm |  |  |  |
| `TNEWACCTWIZARDEXCHANGEDLGFM` | 外汇交易账户 | 外汇交易账户；您可创建外汇交易账户，专业管理在银行及金融机构开立的外汇投资账户。支持多币种管理，完整记录外汇买卖、汇率转换及利息收支等交易明细，监控汇率波动风险，为您提供专业的外汇投资管理工具。；所有者；备注；币种；账户名称；属于账户组；<无>；账户余额；日期；资金来源；增加其它币种；金额 |  |  |
| `TNEWACCTWIZARDFIXEDDEPOSITDLGFM` | 定期存款 | 定期存款；您可通过创建定期存款账户，专业管理在银行办理的定期存款业务。支持完整记录存款开户、到期支取等关键业务，每个账户对应单笔定期存款，确保资金管理的精准性和可追溯性。；所有者；备注；币种；账户名称；属于账户组；<无>；存款类型；起存日期；存期；年利率(%)；到期自动续存；存款来源；存款金额；<不考虑存款来源>；已存金额；取款去向；月取金额；<不考虑取款去向> |  | edtTerm -> edtTermChange |
| `TNEWACCTWIZARDFUTURESDLGFM` | 期货 | 期货；您可创建期货交易账户，专业管理各类期货合约投资。完整记录开仓、平仓、保证金变动等交易明细，监控持仓盈亏和风险指标，为您提供专业的期货投资风险管理解决方案。；所有者；备注；账户名称；币种；属于账户组；<无>；日期；账户余额；开户机构 |  |  |
| `TNEWACCTWIZARDGOLDDLGFM` | 贵金属账户 | 贵金属账户；您可创建多个贵金属交易账户，专业管理银行纸黄金及贵金属交易所的黄金、白银、铂族等贵金属投资。每个账户支持记录多品种同币种贵金属的买卖交易、持仓变动及盈亏情况，实现贵金属投资的多元化管理。；账户名称；备注；所有者；币种；属于账户组；<无>；资金来源；日期；余额；其它账户；账户自身 |  | 其它账户 -> rbCAcctSelfClick；账户自身 -> rbCAcctSelfClick |
| `TNEWACCTWIZARDINSURECOMMERCEDLGFM` | 商业保险账户 | 商业保险账户；商业保险是由保险企业市场化运营、投保人自主选择的保障体系，主要涵盖人寿保险、财产保险及投资连结保险等多元化产品类型，为客户提供个性化的风险保障和财富管理解决方案。；人身保险；财产保险；投资分红险；所有人；币种；备注；账户名称；将保费做为收支统计；<无>；缴费年限；保险机构；保险种类；终止日期；生效日期；受益人；被保险人；投保人；投保金额；保单号；终生有效；缴费账户；缴费金额；缴费频率；已缴保费；固定账户定期扣款；仅做提醒；不提醒 |  | 人身保险 -> rbTypeClass1Click；财产保险 -> rbTypeClass1Click；投资分红险 -> rbTypeClass1Click；将保费做为收支统计 -> chkIncExpStatisticsClick；edtBeginDate -> edtYearsChange；终生有效 -> ckbIsForLifeClick；edtYears -> edtYearsChange；固定账户定期扣款 -> rbRemindType1Click；仅做提醒 -> rbRemindType1Click；不提醒 -> rbRemindType1Click |
| `TNEWACCTWIZARDINSURESOCIALDLGFM` | 社保账户 | 社保账户；国家立法规定的强制性社会保险体系，包含养老保险、工伤保险、失业保险、医疗保险、生育保险及住房公积金六大类别，共同构建起全面的社会保障网络。；城市；社保编码；参保人；将保费做为收支统计；<无>；记账日期；下面至少选择一项；记账日余额；住房公积金；生育；医疗；失业；工伤；养老 |  | 将保费做为收支统计 -> chkIncExpStatisticsClick；住房公积金 -> chk16Click；生育 -> chk15Click；医疗 -> chk14Click；失业 -> chk13Click；工伤 -> chk12Click；养老 -> chk11Click |
| `TNEWACCTWIZARDMARGINDLGFM` | 融资融券 | 融资融券；您可创建融资融券交易账户，专业管理在证券公司开立的信用交易账户。完整记录融资买入、融券卖出、担保品划转及利息费用等交易明细，监控信用额度使用率和风险指标，为您提供专业的投资风险管理解决方案。；所有者；备注；账户名称；币种；属于账户组；<无>；日期；账户余额；融资年利率(%)；融券年利率(%) |  |  |
| `TNEWACCTWIZARDMONEYDLGFM` | 银行理财产品账户 | 银行理财产品账户；您可创建多个银行理财账户，专业管理不同币种的理财产品投资。每个账户支持记录多款同币种理财产品的申购、赎回、收益分配等完整交易流程，实现银行理财产品的精细化管理和收益分析。；账户名称；备注；所有者；币种；属于账户组；<无>；资金来源；日期；余额；其它账户；账户自身 |  | 其它账户 -> rbCAcctSelfClick；账户自身 -> rbCAcctSelfClick |
| `TNEWACCTWIZARDNMARKETDEBTDLGFM` | 债券账户 | 债券账户；您可创建多个债券交易账户，专业管理不同币种的债券投资。每个账户支持记录多支同币种债券的买卖交易、利息收入及到期兑付等完整生命周期，实现债券投资的专业化管理和收益跟踪。；账户名称；备注；所有者；币种；属于账户组；<无>；资金来源；日期；余额；其它账户；账户自身 |  | 其它账户 -> rbCAcctSelfClick；账户自身 -> rbCAcctSelfClick |
| `TNEWACCTWIZARDONECARDDLGFM` | 一卡通 | 一卡通；您可将活期、定期存款子账户灵活组合，创建与银行卡一一对应的账户组。每个账户组集中管理关联卡片下的所有存款账户，实现资金的全方位监控和统一调配，提升财务管理效率。；一卡通账户组名称；备注；至少选择一个子账户；创建活期子账户；创建定期子账户；子账户；余额 |  | 创建活期子账户 -> btnNewCurrentClick；创建定期子账户 -> btnNewFixedDepositClick |
| `TNEWACCTWIZARDOPENFUNDDLGFM` | 开放式基金账户 | 开放式基金账户；您可创建多个开放式基金账户，专业管理在不同基金公司开立的投资账户。完整记录基金申购、赎回、转换及分红等交易明细，跟踪基金持仓收益，为您提供全面的基金投资管理解决方案。；账户名称；备注；所有者；币种；属于账户组；<无>；资金来源；日期；余额；其它账户；账户自身 |  | 其它账户 -> rbCAcctSelfClick；账户自身 -> rbCAcctSelfClick |
| `TNEWACCTWIZARDPRACDLGFM` | 家居物品账户 | 家居物品账户；您可创建家庭物品管理账户，系统化分类管理各类资产。支持记录物品购置、使用、维护及处置等信息，提供统计分析，助您实现家庭资产的智能化管理，提升物品使用效率。；所有者；备注；币种；账户名称；资产性质；属于账户组；投资；自用；<无> |  |  |
| `TNEWACCTWIZARDPRECIOUSMETALSTDDLGFM` | 贵金属TD账户 | 贵金属TD账户；您可创建贵金属递延交易账户，专业管理在银行开立的贵金属延期交收合约投资。完整记录开仓、平仓、递延费结算等交易明细，监控保证金状况和持仓盈亏，为您提供专业的贵金属投资管理工具。；所有者；备注；币种；账户名称；属于账户组；<无>；开户日期；资金来源；交易手续费；每万元；余额；其它账户；账户自身 |  | 其它账户 -> rbCAcctSelfClick；账户自身 -> rbCAcctSelfClick |
| `TNEWACCTWIZARDSECURITYDLGFM` | 上市证券账户 | 上市证券账户；您可创建证券交易账户，专业管理在证券公司开立的股票、权证、上市基金及债券等投资账户。完整记录买卖委托、成交明细、持仓变动等交易活动，实时跟踪投资组合表现，为您提供专业的投资管理解决方案。；所有者；备注；类型；账户名称；属于账户组；<无>；日期；资金来源；余额；其它账户；账户自身 |  | 其它账户 -> rbCAcctSelfClick；账户自身 -> rbCAcctSelfClick |
| `TNEWACCTWIZARDTHIRDDEPOSITSDLGFM` | 支付宝、微信钱包 | 支付宝、微信钱包；您可创建第三方支付账户，统一管理支付宝、微信支付等主流电子钱包。完整记录在线消费、账户充值、转账汇款等资金流动，实时掌握网络支付动态，实现线上线下资金的统筹管理。；所有者；备注；币种；账户名称；属于账户组；<无>；创建日期；账户余额；资金来源；<不考虑资金来源> |  |  |
| `TNEWACCTWIZARDTWOCURRCREDITDLGFM` | 双币信用卡账户 | 双币信用卡账户；您可为每位家庭成员分别创建独立的双币种信用卡账户，精准记录人民币和外币的消费明细、汇率转换、还款周期及信用额度使用情况，实现家庭跨境消费的全面管理和汇率风险控制。；所有者；备注；账户名称；启用日期；还款日；账单日；日；每月；每月最后一天是账单日；固定账单日；天；账单日之后；固定还款日；已透支金额；币种1；币种2；当透支额大于；时提醒；透支提醒 |  | 每月最后一天是账单日 -> RBBillType0Click；固定账单日 -> RBBillType0Click；账单日之后 -> RBPayType0Click；固定还款日 -> RBPayType0Click；透支提醒 -> chkIsAwake1Click；透支提醒 -> chkIsAwake2Click |
| `TNEWBLOCKUPDLG` | 垫付 | 垫付；债务人；款项；金额；日期；备注；币种；收支项目；资金账户；标签；<无>；保存；保存并继续 |  | edKind -> edKindChange；保存 -> btnSaveExitClick；保存并继续 -> btnSaveNewClick |
| `TNEWBOOKFM` | 新建账簿 | 新建账簿；新账簿名称；保存位置；建好后立即设置账簿密码；确定；建议将账簿文件存储于非系统分区，以避免系统重装时造成数据丢失。；更改 |  | 建好后立即设置账簿密码 -> CheckPawClick；确定 -> BtnOKClick；更改 -> btnChangeClick |
| `TNEWDEBTBORROWDLGFM` | 借入、借出 | 借入、借出；还款总期数；已还款期数；每期还款额；剩余本金；贷款期限；还款频率；首次还款日；债权人；币种；还款方式；年利率(%)；借入金额；款项；收入账户；主题；借贷发生日；备注；保存并新添；保存 |  | edKind -> edKindChange；保存并新添 -> btnSaveNewClick；保存 -> btnSaveExitClick |
| `TNEWRECTRANSDLGFM` | 余额调整 | 余额调整；账户；账面余额；真实余额；币种；差额记为 |  | edTransDate -> edTransDateChange |
| `TNEWREMINDDLGFM` | 今日提醒 | 今日提醒；说明；提醒ID；提醒类型；执行；跳过；关闭；今日不再提醒；打开账簿时自动弹出今日提醒；提醒设置；不再提醒；详情 |  | 关闭 -> RzBitBtn1Click；今日不再提醒 -> chkNoRemindTodayClick；打开账簿时自动弹出今日提醒 -> chkAutoShowRemindTodayClick；执行 -> actExecuteExecute；跳过 -> actJumpExecute |
| `TNEWTHEMEDLGFM` | 标签 | 标签；请输入%s名称，如需新增多个%s，请用分号（;）隔开：；为记录和资产添加标记，便于进行分类管理，并可用于报表统计。；保存 |  | 保存 -> btnOKClick |
| `TNMARKETBONDBUYDLGFM` | 债券买入 | 债券买入；资金账户；债券名称；应计利息；金额；债券账户；净价；总费用；数量(张)；<无> |  | edInterest -> edPriceChange；edPrice -> edPriceChange；edFee -> edPriceChange；edQuantity -> edPriceChange |
| `TNMARKETBONDCASHAHEADDLGFM` | 债券提前兑取 | 债券提前兑取；资金账户；债券名称；数量(张)；金额；债券账户；净价；应计利息；<无> |  | edQuantity -> edPriceChange；edPrice -> edPriceChange；edInterest -> edPriceChange |
| `TNMARKETBONDINTERESTDLGFM` | 债券利息 | 债券利息；资金账户；债券名称；金额；债券账户；<无> |  |  |
| `TNMARKETBONDLISTFM` | 债券列表 | 债券列表；新增债券；操作；请输入要搜索的关键字...；代码；名称；币种；发行日；到期日；付息日1；付息日2；年利率(%)；面值；价格历史；修改债券；删除债券；查找；导出；打印 | `TransObjID`；`BondCode`；`DebtName`；`ChineseName`；`PubDate`；`EndDate`；`PayDate1`；`PayDate2`；`Rate`；`ParValue` | 债券列表 -> FormShow；操作 -> RzMenuButton1Click；MHBGSecurity -> MHBGSecurityDblClick；新增债券 -> actAddSecurityExecute；修改债券 -> actEditSecurityExecute；删除债券 -> actDeleteSecurityExecute；查找 -> N1Click；导出 -> miExportClick；打印 -> miPrintClick |
| `TNMARKETBONDMATUREDLGFM` | 债券到期 | 债券到期；资金账户；债券名称；数量(张)；债券账户；全价；金额；<无> |  | edQuantity -> edPriceChange；edPrice -> edPriceChange |
| `TNMARKETBONDSELLDLGFM` | 债券卖出 | 债券卖出；资金账户；债券名称；数量(张)；金额；债券账户；净价；总费用；应计利息；<无> |  | edQuantity -> edPriceChange；edPrice -> edPriceChange；edFee -> edPriceChange；edInterest -> edPriceChange |
| `TNMARKETDEBTACCTDLGFM` | 债券账户 | 债券账户；创建日期；开户机构；默认资金账户；账号；自身；其它；<无> |  | 自身 -> rbSelfCapitalClick；其它 -> rbSelfCapitalClick |
| `TNODEWRAPFORM` |  |  |  |  |
| `TNORMALPLANDLGFM` | 提醒 | 提醒；提醒名称 |  |  |
| `TOKCANCELDIALOGFM` | OkCancelDialogFm | 取消；帮助；确定 |  | 取消 -> BtnCancelClick |
| `TONLINEGETDATAFM` | 更新行情数据 | 更新行情数据；更新；中止；完成；获取最新行情数据；数据项；上次更新时间；仅获取当前持仓的；获取全部；获取持仓和历史交易过的；获取历史行情数据；开始日期；结束日期 |  | 更新 -> RzButtonUpdateClick；中止 -> RzButtonAbortClick；完成 -> btnCompleteClick；仅获取当前持仓的 -> R1Click；获取全部 -> R1Click；获取持仓和历史交易过的 -> R1Click；仅获取当前持仓的 -> R4Click；获取全部 -> R4Click；获取持仓和历史交易过的 -> R4Click |
| `TOPENFUNDACCTDLGFM` | 开放式基金账户 | 开放式基金账户；创建日期；账号；开户机构；默认资金账户；自身；其它；<无> |  | 自身 -> rbSelfCapitalClick；其它 -> rbSelfCapitalClick |
| `TOPENFUNDREMINDDLG` | 开放式基金价格提醒 | 开放式基金价格提醒；价格小于；或大于；当基金；保存；更新基金 |  | 保存 -> btnSaveNewClick；更新基金 -> btnUpdateCodeClick |
| `TOPENFUNDSLISTFM` | 开放式基金列表 | 开放式基金列表；新增基金；操作；请输入要搜索的关键字...；代码；名称；币种；申购费率(%)；赎回费率(%)；日期；新增价格；显示单日所有价格；只显示持仓基金净值；净值；修改基金；删除基金；修改价格；删除价格；代码转换；获取净值；价格整理；查找；导出；打印 | `TransObjID`；`Code`；`FullName`；`ChineseName`；`SGRate`；`SHRate`；`PriceDate`；`MessureQuant` | 操作 -> RzMenuButton1Click；DBGridList -> ActModifyExecute；RzDate -> RzDateChange；显示单日所有价格 -> RzCBOnlyDateClick；只显示持仓基金净值 -> RzCBOnlyHaveClick；操作 -> btn1Click；DBGridPrice -> ActModifyPriceExecute；新增基金 -> ActAddExecute；修改基金 -> ActModifyExecute；删除基金 -> ActDeleteExecute；新增价格 -> ActAddPriceExecute；修改价格 -> ActModifyPriceExecute；删除价格 -> ActDeletePriceExecute；代码转换 -> actConvertCodeExecute；获取净值 -> ActGetPriceExecute；价格整理 -> ActCheckPriceExecute；查找 -> N6Click；导出 -> miExportClick；打印 -> miPrintClick；导出 -> miExportPriceClick；打印 -> miPrintPriceClick |
| `TOPENFUNDSTATISTICFRAME` |  | 获取净值；基金名称；持仓数量；持仓成本；市值；占比%；浮动盈亏；均价；基金净值；浮动收益率%；添加基金净值；开放式基金代码变更；当前持仓基金；所有交易过的基金 | `ObjName`；`Amount`；`Cost`；`TheValue`；`Scale`；`PAL`；`Price`；`MarketPrice`；`ProfitRate` | 获取净值 -> btnUpdateDataClick；BrowseGrid -> BrowseGridDblClick；添加基金净值 -> ActAddPriceExecute；开放式基金代码变更 -> ActChangCodeExecute |
| `TOPENFUNDTRANSFM` | 开放式基金交易明细 | 开放式基金交易明细；交易明细；市值构成和变动；历史盈亏 |  |  |
| `TOPENFUNDTRANSFRAME` |  | 基金名称；价格；数量；费率；交易金额；单只基金交易明细 | `CategoryName`；`TransObjID`；`Price`；`Quantity`；`Commission`；`AMT`；`Bala`；`Iterbala`；`TotalFee` |  |
| `TOPENFUNDVIEWFRAME` |  |  |  |  |
| `TPAGECONTRLFM` | PageContrlFM |  |  | PageContrlFM -> FormShow |
| `TPARENTPLANDLGFM` | ParentPlanDlgFm | 确定；已执行次数；计划名称；开始日期；重复；重复次数；提醒 |  | 确定 -> btnSaveClick |
| `TPASSWORDDIALOG` | Enter password | Enter password；Re&move all |  | &OK -> OKButtonClick；Edit -> EditChange；&Add -> AddButtonClick；&Remove -> RemoveButtonClick；Re&move all -> RemoveAllButtonClick |
| `TPAYABLEADVANCEDLGFM` | 预收、预付 | 预收、预付；债权人；金额；款项；日期；备注；币种；主题；收入账户；保存；保存并继续 |  | edKind -> edKindChange；保存 -> btnSaveExitClick；保存并继续 -> btnSaveNewClick |
| `TPAYABLEMONEYTRANSDLGFM` | 预收 | 预收；债权人；预收金额；款项；币种；收入账户 |  | edKind -> edKindChange |
| `TPAYABLESVIEWFRAME` |  |  |  |  |
| `TPAYROLLINCOMEDLGFM` | 工资收入 | 工资收入；个人所得税计算器；收入账户；社保人员；币种；收入项目；金额；扣款项目；社保账户；个人缴费金额；公司缴费金额 |  | 个人所得税计算器 -> lblTaxCalcClick |
| `TPERSONDLG` | 人员与机构 | 人员与机构；类型；名称；性别；男；女；联系方式；地址；年；生日；保存 |  | 生日 -> CKBirthClick；保存 -> btnSaveExitClick |
| `TPERSONLISTFM` | 人员与机构 | 人员与机构；人员与机构列表；名称；类型；性别；生日类型；出生日期；联系方式；地址；新增；操作；请输入要搜索的关键字...；修改；删除；隐藏；显示隐藏人员和机构；导出；打印 | `PName`；`TypeName`；`sexname`；`BirthdayType`；`Birth`；`connect`；`Address`；`Sex`；`type`；`HideFlag` | DBGRID -> actEditExecute；操作 -> sbCustomClick；新增 -> actAddExecute；修改 -> actEditExecute；删除 -> actDelExecute；隐藏 -> actHideExecute；显示隐藏人员和机构 -> miVisibleClick；导出 -> miExportClick；打印 -> miPrintClick |
| `TPLANINSUREPAYFEEDLGFM` | 缴费计划 | 缴费计划；缴费频率；缴费金额；缴费账户；确 定；<无> |  | 确 定 -> btnSaveExitClick |
| `TPLANLISTDLG` | 财务计划和提醒 | 财务计划和提醒；类型；计划名称；发生频率；开始日期；结束日期；下次执行日期；执行状态；执行；新增计划；操作；跳过；新添计划；修改；删除；终止；恢复；提醒；收支计划；转账计划；基金申购/定投计划；显示已完成的计划和提醒 |  | PlanTreeList -> PlanTreeListDblClick；操作 -> btnCustomClick；执行 -> actExecuteExecute；跳过 -> actCancelExecute；修改 -> actEditExecute；删除 -> actDelExecute；终止 -> actEndExecute；恢复 -> actResumeExecute；提醒 -> N2Click；收支计划 -> N3Click；转账计划 -> N4Click；基金申购/定投计划 -> N5Click；显示已完成的计划和提醒 -> miIncludFinishClick |
| `TPRACACCTDLGFM` | 物品账户 | 物品账户；创建日期；资金账户；资产性质；投资；自用；<无> |  |  |
| `TPRACASSETBUYDLGFM` | 物品买入 | 物品买入 |  |  |
| `TPRACASSETSELLDLGFM` | 物品卖出 | 物品卖出；物品名称；数量；单价；总金额；资金账户；物品分类；物品账户；收支项目；<无> |  | edQuantity -> EdPriceChange；EdPrice -> EdPriceChange |
| `TPRACBUYEDITFRAME` |  | 物品名称；数量；资金账户；金额；单价；物品分类；备注；主题；物品账户；日期；收支项目；分期付款；<无> |  | edPrice -> edPriceChange；分期付款 -> btnInstallmentClick；SelObject -> SelObjectChange；edQuantity -> edPriceChange |
| `TPRACBUYINSTALLMENTWIZARDDLG` | 物品买入分期 | 物品买入分期；物品买入信息；分期信息；确认信息；完成后，软件将生成以下内容 |  |  |
| `TPRACCHANGEVALUEDLGFM` | 物品价值变更 | 物品价值变更；物品分类；物品名称；重估前价值；重估后价值；物品账户 |  | edTransDate -> edTransDateChange |
| `TPRACDLG` | 家居物品 | 家居物品；备注；现价；物品分类；物品名称；币种；保存；保存并继续 |  | 保存 -> btnSaveExitClick；保存并继续 -> btnSaveNewClick |
| `TPRACGROUPVIEWFRAME` |  |  |  |  |
| `TPRACINCDLGFM` | 资产投资收益 | 资产投资收益；金额；资产名称；资金账户；收入项目 |  |  |
| `TPRACLISTFM` | 家居物品资料和价格 | 家居物品资料和价格；家居物品现价表；日期；新增价格；只显示持有物品价格；按日期显示全部价格；操作；物品名称；价格；新增；分类/名称；币种；备注；物品分类；物品；修改物品；删除物品；修改价格；删除价格；隐藏物品；修改分类；删除分类；显示隐藏物品；导出；打印 | `TransObjID`；`PracName`；`PriceDate`；`Price` | RzDTEDate -> RzDTEDateChange；只显示持有物品价格 -> RzCBOnlyHaveClick；按日期显示全部价格 -> RzCBOnlyDateClick；操作 -> RzMenuButton3Click；PracPrice -> actEditPriceExecute；操作 -> RzMenuButton2Click；PracTreeList -> PracTreeListDblClick；物品分类 -> actAddGroupExecute；物品 -> actAddExecute；修改物品 -> actEditExecute；删除物品 -> actDelExecute；新增价格 -> actAddPriceExecute；修改价格 -> actEditPriceExecute；删除价格 -> actDeletePriceExecute；隐藏物品 -> actHideExecute；修改分类 -> actEditGroupExecute；删除分类 -> actDelGroupExecute；显示隐藏物品 -> mmiViewClick；导出 -> miExportClick；打印 -> miPrintClick；导出 -> miExportPriceClick；打印 -> miPrintPriceClick |
| `TPRACSTATISTICFRAME` |  | 物品分类/名称；购买均价；数量；购买成本；市值 |  |  |
| `TPRACTRANSFM` | 物品交易明细 | 物品交易明细；交易明细；成本市值构成 |  |  |
| `TPRACTRANSFRAME` |  | 物品分类/名称；单价；数量；金额；单个物品交易明细 | `TransObjID`；`Price`；`Quantity`；`sum2`；`CategoryName`；`Iterbala`；`TotalFee`；`TransObjType` |  |
| `TPRACTYPEDLG` | 家居物品分类 | 家居物品分类；分类名称；保存 |  | 保存 -> btnSaveExitClick |
| `TPRECIOUSMETALSTDACCTDLGFM` | 贵金属TD账户 | 贵金属TD账户；开户日期；默认资金账户；交易手续费；每万元；自身；其它；<无> |  | 自身 -> rbSelfCapitalClick；其它 -> rbSelfCapitalClick |
| `TPRECIOUSMETALSTDBUYDLGFM` | 贵金属TD开仓 | 贵金属TD开仓；资金账户；贵金属TD账户；TD品种；成交单价；成交数量；成交金额；手续费；保证金比例；保证金；<无> |  |  |
| `TPRECIOUSMETALSTDGOODSLISTFM` | 贵金属TD品种列表 | 贵金属TD品种列表；新增贵金属；操作；请输入要搜索的关键字...；代码名称；报价单位；每手数量；交易单位；保证金比例(%)；修改贵金属；删除贵金属；导出；打印 | `TransObjID`；`FeeType`；`Name`；`QuotationUnit`；`Quantity`；`TradingUnit`；`MarginRatio`；`ID`；`CnName` | 贵金属TD品种列表 -> FormShow；操作 -> RzMenuButton1Click；MHBGSecurity -> MHBGSecurityDblClick；新增贵金属 -> actAddSecurityExecute；修改贵金属 -> actEditSecurityExecute；删除贵金属 -> actDeleteSecurityExecute；导出 -> miExportClick；打印 -> miPrintClick |
| `TPRECIOUSMETALSTDSELLDLGFM` | 贵金属TD平仓 | 贵金属TD平仓；资金账户；贵金属TD账户；TD合约；成交单价；成交数量；成交金额；手续费；收回保证金；收回金额；<无> |  | edTransDate -> edTransDateChange |
| `TPRECIOUSMETALSTDSTATISTICFRAME` |  | 获取最新价格；合约；数量(手)；保证金；市值；占比%；浮动盈亏；均价；收盘价；浮动收益率%；添加贵金属价格；证券代码变更；贵金属TD品种设置；当前持仓合约；所有交易过的合约 | `ObjName`；`Amount`；`MarginCost`；`TheValue`；`Scale`；`PAL`；`Price`；`MarketPrice`；`ProfitRate` | 获取最新价格 -> btnUpdateDataClick；BrowseGrid -> BrowseGridDblClick；添加贵金属价格 -> ActAddPriceExecute；贵金属TD品种设置 -> mmiPreciousMetalsTDGoodsClick |
| `TPRECIOUSMETALSTDTRANSFM` | 贵金属TD账户交易明细 | 贵金属TD账户交易明细；交易明细；历史盈亏 |  |  |
| `TPRECIOUSMETALSTDTRANSFRAME` |  | 期货合约；价格；数量；总费用；交易金额；单个合约交易明细 | `CategoryName`；`ObjName`；`Price`；`Quantity`；`TotalFee`；`AMT`；`Bala`；`Iterbala`；`Commission`；`TransObjID` |  |
| `TPRECIOUSMETALSTDVIEWFRAME` |  |  |  |  |
| `TPRECIOUSVIEWFRAME` |  |  |  |  |
| `TPREPAIDEXPENSESDLGFM` | 待摊费用 | 待摊费用；日期；备注；收支项目；待摊金额；款项；摊销频率；月/次；人员；总摊销次数；主题；首次摊销日期；已摊销次数；币种；支出账户；保存；保存并继续 |  | edtHasPaidTimes -> edtHasPaidTimesChange；保存 -> btnSaveExitClick；保存并继续 -> btnSaveNewClick |
| `TPREPAIDEXPENSESINCEXPDLGFM` | 待摊费用 | 待摊费用；支出项目；待摊金额；款项名称；摊销频率；月/次；人员；总摊销次数；首次摊销日期；已摊销次数；币种；支出账户 |  |  |
| `TPREPAYMENTFM` | 提前返还 | 提前返还；款项；处理方式；归还本金；支付利息；本息合计；剩余本金；剩余期数；每期金额；支出账户 |  | edTransDate -> edTransDateChange |
| `TPREPEXPEACCTDLGFM` | 待摊费用概况 | 待摊费用概况；款项；人员；收支项目；收支金额；摊销频率；月/次；首次摊销日期；已摊销次数；总摊销次数 |  |  |
| `TPROGRESSFORM` | ProgressFM | 正在处理数据...；取消 |  | 取消 -> btnCancelClick |
| `TPWDCHANGEFM` | 密码设置 | 密码设置；旧密码；新密码；再次输入；确定 |  | BtnOk -> BtnOkClick；edNew1 -> edNew1Change；确定 -> BtnOkClick |
| `TPWDCHECKFM` | 密码输入 | 密码输入；账簿；密码；确定 |  | 确定 -> RzButtonOkClick |
| `TQUITEXERTIONRIGHTFM` | 放弃行权 | 放弃行权；权证；数量 |  |  |
| `TRATEFM` | 存款利率 | 存款利率；操作；人民币；储蓄类型；储蓄期间；年利率(%)；外币储蓄；币种；活期；一个月；三个月；半年；一年；两年；七天通知存款；更新利率；导出；打印 |  | 操作 -> btnOperateClick；更新利率 -> miUpdateClick；导出 -> miExportClick；打印 -> miPrintClick |
| `TRECEIVABLESVIEWFRAME` |  |  |  |  |
| `TRECHARGEDLGFM` | 充值 | 充值；充值账户；资金来源；金额；手续费 |  |  |
| `TREGISTERFORM` | 软件联网注册 | 软件联网注册；已有高级功能序列号；了解高级功能；激活高级功能；试用期已结束，软件将切换为免费版本运行；购买高级功能；使用免费功能；去广告；远离广告打扰；所有财务报表；财务报表轻松看并支持自定义报表；财务诊断、目标、规划；规划人生财富实现理财目标；三端数据同步；电脑、手机、在线理财三端数据同步；免费试用高级功能；序列号；重新激活；购买序列号继续使用；下一步；上一步；序列号由四组数字和“-”组成， 请完整输入（例如：1234-5678-8701-6666）。；序列号保护信息；请牢记并妥善保管您的保护信息，后续激活需要填写此信息。；请确保保护信息不超过16位字符（数字或字母）或8个汉字。；忘记保护信息？点击这里找回...；确定；请仔细填写以下信息，这些信息将帮助您找回序列号并享受我们的售后服务。；姓名；电子邮箱；电话；例：02887016666；详细地址；所在省市；使用地点；当您在多台电脑上激活时，可随时取消对其他电脑的授权， 方便您灵活管理授权设备（如公司、家、台式机、笔记本等）。；北京；辽宁；广东；浙江；江苏；山东；四川；黑龙江；湖南；湖北；上海；福建；陕西；河南；安徽；重庆；河北；吉林；江西；天津；广西；山西；内蒙古；甘肃；贵州；新疆；云南；宁夏；海南；青海；西藏；港澳台；海外；其它；很抱歉，由于网络连接问题或其他原因，本次激活未能成功。；离线激活；保存用户信息；离线激活操作指南；去掉并激活；请在下表中选择要去掉的部分历史激活记录，继续本次激活。如无法成功，请联系客服（QQ：854978390）。；最近使用时间；注册日期；地点；省市；联系方式；查看注册资料；开始使用；请妥善保存您的序列号，凭借此序列号，您将享有正版软件的优质售后服务。；确认密码；昵 称；密 码；昵称是否可用？；邮箱是否可用？；已有财智通行证（原蜗牛谷、财智在线理财、财智快账等账号均可使用）；没有财智通行证？立即注册 |  | 了解高级功能 -> lblGNDBClick；激活高级功能 -> btnFirstUse_RegisterClick；购买高级功能 -> btnFirstUse_BuyClick；使用免费功能 -> btnFirstUse_FreeUseClick；免费试用高级功能 -> btnFreeUse_TryClick；edtIndex_SerialNo -> edtSerialChange；重新激活 -> btnIndex_SerialNoRegisterClick；购买序列号继续使用 -> btnFirstUse_BuyClick；下一步 -> btnSerialNo_NextClick；上一步 -> btnWoniugu_BackClick；edtSerial -> edtSerialChange；忘记保护信息？点击这里找回... -> lblResultVerifyCodeClick；确定 -> btnUserInfo_ActivationClick；离线激活 -> btnOvertime_NextClick；保存用户信息 -> btnOfflineReg_SaveUserInfoClick；去掉并激活 -> btnDisableInfoSign_ActivationClick；查看注册资料 -> btnShowUserInfo1Click；开始使用 -> btnSuccess_CloseClick；edtSuccess_SerialNo -> edtSerialChange；开始使用 -> btnCaizhiPass_SubmitClick；昵称是否可用？ -> lblNicknameExistsClick；邮箱是否可用？ -> lblEmailExistsClick；已有财智通行证（原蜗牛谷、财智在线理财、财智快账等账号均可使用） -> rbHaveClick；没有财智通行证？立即注册 -> rbHaveClick |
| `TRELATIONNEWSTOCKRECORDSDLGFM` | 关联新股申购记录 | 关联新股申购记录；申购记录行号；中签记录行号；返款记录行号；确定 |  | 确定 -> btnOkClick |
| `TREMOTENOTIFICATIONDLGFM` | 手机快查设置 | 手机快查设置；电子邮箱；密码；启用“手机快查”功能；您可通过财智快账App的“快查”功能，接收财务提醒并便捷查看投资、预算等财务数据。；注册账号 |  | edtEMail -> edtEMailChange；edtPassword -> edtPasswordChange；启用“手机快查”功能 -> chkEnableClick；注册账号 -> btnRegisterClick |
| `TREPAYMENTTABLEFRAME` |  | 还款方式：；该账户类型不能进行利率调整，也没有收/还款表。；添加；修改；删除；日期；利率(%)；还款频率：；还款总期数：；已还本金：；已还利息：；剩余利息：；打印；期次；本期还款；本金；利息；剩余本金 |  | 添加 -> btnAddClick；修改 -> btnUpdateClick；删除 -> btnDeleteClick；tlRateChange -> tlRateChangeDblClick；打印 -> btnPrintClick |
| `TREPORTFM` | ReportFm | 筛选\|已更改；图表；操作；报表数据已更新，请按F5键刷新报表。；修改；删除；导出到文件；报表另存为；删除报表；导出报表；打印预览 |  | 筛选\|已更改 -> sbOptionClick；图表 -> btnReportOrChartClick；操作 -> btnOtherClick；btnCloseTransList -> btnCloseTransListClick；修改 -> miModifyClick；删除 -> miDeleteClick；导出到文件 -> miExportToFileClick；报表另存为 -> miRptSaveClick；删除报表 -> miRptDeleteClick；导出报表 -> ActionExportRpt；打印预览 -> ActionPrintRpt |
| `TREPORTOPTIONDLGFM` | 筛选 | 筛选；确定；恢复默认条件；相关资产；反选；全选；人员、机构；活动类型；收支项目；标签；币种、对象；金额范围 |  | 确定 -> btnOkClick；恢复默认条件 -> btnDefaultClick；反选 -> btnInvert_AcctClick；全选 -> btnAllClick |
| `TRESTOREBOOKFM` | 还原账簿 | 还原账簿；备份账簿；还原到；关闭；选择；确定；还原操作将覆盖当前账簿数据，请谨慎操作。建议选择还原至新建的账簿。 |  | 选择 -> btnOtherClick；确定 -> RzButtonOkClick |
| `TRPTACCOUNTINCOMESTATFRM` | 账户日常收支表 | 账户日常收支表 |  |  |
| `TRPTBSSTATFRM` | 资产负债表 | 资产负债表；统计方式；统计到 |  | 统计到 -> btnDateClick |
| `TRPTCASHWASTEFM` | 现金流表 | 现金流表 |  |  |
| `TRPTCREDITDEBTSTATFM` | 债权债务表 | 债权债务表 |  |  |
| `TRPTDEBTINVESTMENTINVESTYKFORM` | 网贷盈亏一览表 | 网贷盈亏一览表 |  |  |
| `TRPTEXCHANGE6FM` | 外汇交易一览表 | 外汇交易一览表 |  |  |
| `TRPTFINANCIALPRODUCTSFM` | 银行理财产品收益率表 | 银行理财产品收益率表 |  |  |
| `TRPTFUNDSAVAILABLEFM` | 可用资金表 | 可用资金表 |  |  |
| `TRPTFUNDTRENDFM` | 开放式基金市值大势图 | 开放式基金市值大势图；资产总值；基金市值；资金余额 |  | 资产总值 -> chbAssetClick；基金市值 -> chbAssetClick；资金余额 -> chbAssetClick |
| `TRPTINCEXPCOMPAREFM` | 两段时间收支对比表 | 两段时间收支对比表；时间段2；时间段1 |  |  |
| `TRPTINCEXPZSTOVFM` | 收支走势图 | 收支走势图 |  |  |
| `TRPTINCOMELISTFM` | 日常收支明细表 | 日常收支明细表 |  |  |
| `TRPTINCOMESTATFRM` | 日常收支表 | 日常收支表 |  |  |
| `TRPTINVESTINCOMEFM` | 投资收益一览表 | 投资收益一览表 |  |  |
| `TRPTINVESTMENTPERFORMANCESTATFM` | 投资收益率统计表 | 投资收益率统计表 |  |  |
| `TRPTINVESTVIEWFM` | 投资一览表 | 投资一览表 |  |  |
| `TRPTMONTHASSETFM` | 月资产走势图 | 月资产走势图 |  |  |
| `TRPTMONTHAVERAGEINCEXPFM` | 月平均收支表 | 月平均收支表 |  |  |
| `TRPTOPENFUNDINVESTFM` | 开放式基金投资一览表 | 开放式基金投资一览表 |  |  |
| `TRPTOPENFUNDINVESTLOSSFM` | 开放式基金费用及盈亏一览表 | 开放式基金费用及盈亏一览表 |  |  |
| `TRPTSECURITINVESTFM` | 证券投资一览表 | 证券投资一览表 |  |  |
| `TRPTSECURITINVESTLOSSFM` | 证券费用及盈亏一览表 | 证券费用及盈亏一览表 |  |  |
| `TRPTSTOCKTRENDFM` | 证券市值大势图 | 证券市值大势图；资产总值；证券市值；资金余额；上证指数；深证成指 |  | 资产总值 -> chbAssetClick；证券市值 -> chbAssetClick；资金余额 -> chbAssetClick；上证指数 -> chbAssetClick；深证成指 -> chbAssetClick |
| `TRPTTAGINCOMESTATFRM` | 标签日常收支表 | 标签日常收支表 |  |  |
| `TRPTYEARINCEXPFORM` | 收支统计表 | 收支统计表 |  |  |
| `TRZFRMCUSTOMIZETOOLBAR` | Customize Toolbar | Customize Toolbar；Add a Spacer；Add a Grooved Spacer |  | LstControls -> LstControlsClick；LstControls -> LstControlsChange；CbxTextOptions -> CbxTextOptionsClick；MoveUp -> BtnMoveUpClick；MoveDown -> BtnMoveDownClick |
| `TSECURITYACCTDLGFM` | 证券账户 | 证券账户；创建日期；类型；股东代码(深)；股东代码(沪)；默认资金账户；开户机构；股东代码(北)；自身；其它；<无> |  | 自身 -> rbSelfCapitalClick；其它 -> rbSelfCapitalClick |
| `TSECURITYCODECONVERTFM` | 代码变更 | 代码变更；申购股代码；上市后代码；帮助；确定 |  | 确定 -> RzButtonOKClick |
| `TSECURITYLISTFM` | 证券资料 | 证券资料；新增股票；操作；请输入要搜索的关键字...；代码；名称；类型；日期；新增价格；显示单日所有价格；只显示持仓股票价格；价格；新增证券；修改证券；删除证券；修改价格；删除价格；代码转换；获取价格；价格整理；修改股票；删除股票；查找；分类显示；所有股票；沪市股票；深市股票；沪市基金；深市基金；深市债券；沪市债券；深市B股；沪市B股；京市股票；香港H股；NASDAQ股；其它股票；导出；打印 | `TransObjID`；`SecuCode`；`SecuName`；`SecuType`；`PriceDate`；`MessureQuant` | 操作 -> RzMenuButton1Click；DBGridList -> ActModifyExecute；RzDate -> RzDateChange；显示单日所有价格 -> RzCBOnlyDateClick；只显示持仓股票价格 -> RzCBOnlyHaveClick；操作 -> btn1Click；DBGridPrice -> ActModifyPriceExecute；新增证券 -> ActAddExecute；修改证券 -> ActModifyExecute；删除证券 -> ActDeleteExecute；新增价格 -> ActAddPriceExecute；修改价格 -> ActModifyPriceExecute；删除价格 -> ActDeletePriceExecute；代码转换 -> ActConvertCodeExecute；获取价格 -> actGetPriceExecute；价格整理 -> ActCheckPriceExecute；查找 -> N5Click；所有股票 -> miAllClick；沪市股票 -> miAllClick；深市股票 -> miAllClick；沪市基金 -> miAllClick；深市基金 -> miAllClick；深市债券 -> miAllClick；沪市债券 -> miAllClick；深市B股 -> miAllClick；沪市B股 -> miAllClick；京市股票 -> miAllClick；香港H股 -> miAllClick；NASDAQ股 -> miAllClick；其它股票 -> miAllClick；导出 -> miExportClick；打印 -> miPrintClick；导出 -> miExportPriceClick；打印 -> miPrintPriceClick |
| `TSECURITYREMINDDLG` | 证券市价提醒 | 证券市价提醒；价格小于；或大于；当证券；保存；更新证券 |  | 保存 -> btnSaveNewClick；更新证券 -> btnUpdateCodeClick |
| `TSECURITYSTATISTICFRAME` |  | 获取收盘价；证券名称；持仓数量；持仓成本；市值；占比%；浮动盈亏；交易盈亏；均价；保本价；收盘价；浮动收益率%；添加股票价格；证券代码变更；导入股票交割单；费率设置；当前持仓证券；所有交易过的证券 | `ObjName`；`Amount`；`Cost`；`TheValue`；`Scale`；`PAL`；`PALWithFee`；`Price`；`LowPrice`；`MarketPrice`；`ProfitRate` | 获取收盘价 -> btnUpdateDataClick；BrowseGrid -> BrowseGridDblClick；添加股票价格 -> ActAddPriceExecute；证券代码变更 -> ActChangeCodeExecute；导入股票交割单 -> mmijgdClick；费率设置 -> mmiFeeSetClick |
| `TSECURITYTRANSFM` | 上市证券交易列表 | 上市证券交易列表；交易明细；市值构成和变动；历史盈亏 |  |  |
| `TSECURITYTRANSFRAME` |  | 证券名称；价格；数量；佣金；总费用；交易金额；单只证券交易明细 | `TransObjID`；`Price`；`Quantity`；`Commission`；`TotalFee`；`AMT`；`CategoryName`；`Bala`；`Iterbala` |  |
| `TSELECTDATERANGEDLGFM` | 自定义日期 | 自定义日期；到；确定 |  | 确定 -> btnOkClick |
| `TSELECTREPETITIONFREQUENCYDLGFM` | SelectRepetitionFrequencyDlgFm | 每；重复；确定 |  | 确定 -> btnSaveClick |
| `TSELECTSECURITIESCODEDLGFM` | 选择证券 | 选择证券；确定；更新证券 |  | 确定 -> btnOkClick；更新证券 -> btnUpdateCodeClick |
| `TSELECTTAGDLGFM` | 选择标签 | 选择标签；确定 |  | 确定 -> btnOkClick |
| `TSELECTTHEMEDLGFM` | SelectThemeDlgFm |  |  |  |
| `TSELECTTRANSTYPEDLGFM` | 选择交易类型 | 选择交易类型；确定 |  | 确定 -> btnOkClick |
| `TSELLCOUPONSREPAYMENTDLGFM` | 卖券还款 | 卖券还款；费用小计；金额合计；卖出数量；卖出价格；融资融券账户；融资合约；证券代码；返还利息；印花税率 %；印花税费；佣金比例 %；佣金；过户费；附加费；显示费用详情 |  | 显示费用详情 -> chkvisibleClick |
| `TSHORTCUTMANAGEDLGFM` | 快捷键设置 | 快捷键设置；记账快捷键设置；菜单项快捷键设置；控制台；确定；启用老板键；菜单项；快捷键；保存快捷键；删除 |  | 确定 -> btnSaveExitClick；btnF1 -> MenuButtonClick；btnF2 -> MenuButtonClick；启用老板键 -> cbBossKeyClick；tlMenuShortCut -> tlMenuShortCutDblClick；保存快捷键 -> btnNewShortCutClick；删除 -> miDeleteClick |
| `TSHORTSELLINGDLGFM` | 融券卖出 | 融券卖出；费用小计；金额合计；卖出数量；卖出价格；融资融券账户；证券代码；融券年利率%；融券合同号；印花税率 %；印花税费；佣金比例 %；佣金；过户费；附加费；显示费用详情；更新代码 |  | 显示费用详情 -> chkvisibleClick |
| `TSOCIALSECURITYSTATISTICFRAME` |  | 名称；余额；备注；删除 | `Name`；`Value`；`Description` | 删除 -> miDeleteAcctClick |
| `TSOCIALSECURITYTRANSFM` | 社会保险账户交易明细 | 社会保险账户交易明细；交易明细；现金价值；账户概况 |  |  |
| `TSOFTINDEXCENTERFORM` | 概况 | 概况；操作；更新行情；诊断；统计数据；统计图表；投资一览；投资详情；名称；数量；成本；市值；浮动盈亏；盈亏比例；财务预算；预算详情；新增预算；可用预算额；实际发生额；预算额；信用卡一览；当前免息期；账单；还款日；未还金额；设为软件首页；调整显示顺序；显示统计图表；显示信用卡一览；显示投资一览；显示财务预算 |  | 概况 -> FormShow；llTitle -> llTitleDblClick；操作 -> btnOperateClick；更新行情 -> btnUpdatePriceClick；诊断 -> btnGotoFinancialDiagnosisClick；pnlFinancialDiagnosis_Close -> pnlFinancialDiagnosis_CloseClick；imgClose -> pnlFinancialDiagnosis_CloseClick；lblDataNumber -> lblDataNumberClick；投资详情 -> btnGotoInvestmentClick；预算详情 -> btnGotoBudgetClick；新增预算 -> btnNewBudgetClick；tlCreditCard -> tlCreditCardDblClick；设为软件首页 -> N1Click；调整显示顺序 -> miSortClick；显示统计图表 -> pmChartClick；显示信用卡一览 -> pmCreditCardClick；显示投资一览 -> pmInvestClick；显示财务预算 -> pmBudgetClick |
| `TSORTSOFTINDEXCENTERDLGFM` | 调整概况显示顺序 | 调整概况显示顺序；确定 |  | mwSortList -> mwSortListChange；确定 -> btnOverClick |
| `TSPLASHFORM` |  |  |  |  |
| `TSPLITINCEXPDLGFM` | 分拆收支 | 分拆收支；收支项目选择<无>，则删除该条收支记录。；注意：第一行[收支项目]的类型，将决定此次交易的类型；注意：第一行[收支账户]的币种，将决定此次交易的币种；收支项目；收入；支出；主题；备注；收支账户；金额 |  | 收入 -> ColInChange；支出 -> ColOutChange |
| `TSTATISTICFRAME` |  | 操作；所有；余额调整；持仓调整；查看账户资料；导出；打印；设为软件首页；当前持仓 |  | 操作 -> btnOperateClick；所有 -> btnAllOrPartObjectListClick；余额调整 -> ActAdjustBalaExecute；持仓调整 -> ActAdjustStaticExecute；查看账户资料 -> actOverviewExecute；导出 -> actExportExecute；打印 -> actPrintExecute；设为软件首页 -> miHomePageClick |
| `TSTATISTICGRIDFRAME` |  |  |  |  |
| `TSTATISTICTREEFRMAE` |  | 全部展开；全部折叠 |  | 全部展开 -> miExpandClick；全部折叠 -> miCollapseClick |
| `TSTOCKBONDMATUREDLGFM` | 债券到期 | 债券到期；资金账户；证券代码；价格/债券全价；数量；金额；证券账户；<无> |  | edPrice -> edPriceChange；edQuantity -> edPriceChange |
| `TSTOCKBUYDLGFM` | 证券买入 | 证券买入；资金账户；证券账户；证券代码；价格；数量；金额合计；费用小计；资金到账日；到期金额；结算汇率；印花税率 %；印花税费；佣金比例 %；佣金；过户费；附加费；显示费用详情；更新代码；<无> |  | edTransDate -> edTransDateChange；edPrice -> edPriceChange；edQuantity -> edPriceChange；显示费用详情 -> chkvisibleClick；更新代码 -> btnUpdateCodeClick；edtEndDate -> edtEndDateChange；edtSettlementRate -> edPriceChange |
| `TSTOCKDIVIDDLGFM` | 送股/缩股 | 送股/缩股；证券代码；数量；证券账户 |  |  |
| `TSTOCKINTERESTDLGFM` | 现金红利 | 现金红利；资金账户；证券代码；金额；证券账户；本次收入记为；<无> |  |  |
| `TSTOCKMARKBUYDLGFM` | 中签确认 | 中签确认；资金账户；申购金；申购返款；申购证券；日期；备注；证券账户；主题；证券代码；中签价格；申购费用；权证代码；权证数量；金额合计；中签数量；申购证券为可分离债；中签；<无>；确 定 |  | 申购证券为可分离债 -> chkKFLZClick；中签 -> cbSignClick；确 定 -> btnSaveExitClick |
| `TSTOCKORDERBUYDLGFM` | 新股申购 | 新股申购；资金账户；证券账户；证券代码；价格；数量；费用；总金额；更新代码；<无> |  | 更新代码 -> btnUpdateCodeClick |
| `TSTOCKQUOTADLGFM` | 配股 | 配股；资金账户；证券代码；价格/债券全价；数量；金额；证券账户；(配债数量按张数计)；<无> |  | edPrice -> edPriceChange；edQuantity -> edPriceChange |
| `TSTOCKSELLDLGFM` | 证券卖出 | 证券卖出；资金账户；证券代码；价格；金额合计；数量；证券账户；费用小计；本次盈亏记为；结算汇率；印花税率 %；印花税费；佣金比例 %；佣金；过户费；附加费；显示费用详情；<无> |  | 显示费用详情 -> chkvisibleClick |
| `TSTOCKVIEWFRAME` |  |  |  |  |
| `TSYNCUSERDATAFM` | 同步 | 同步；密码；电子邮箱；同步条款；上次同步时间；同步方式；(将合并本地账簿与财智在线理财的数据)；(以当前本地账簿数据为准，覆盖财智在线理财的数据)；我同意；注册账号；双向同步；单向上传；开始同步；取消同步；关闭账簿时自动同步 |  | 同步条款 -> lblProvisionClick；我同意 -> chkAgreeClick；注册账号 -> btnRegisterClick；开始同步 -> btnSyncStartClick；取消同步 -> btnSyncCancelClick；关闭账簿时自动同步 -> chkSyncByCloseBookClick |
| `TSYNCUSERREGISTERFM` | 注册同步账号 | 注册同步账号；电子邮箱；密码；确认密码；昵称；注册 |  | 注册 -> btnRegisterClick |
| `TSYSTEMSETTINGSFM` | 系统设置 | 系统设置；系统；软件启动后:；只允许运行一个财智8实例；启动时检查软件更新；启用软件音效；强制网银插件使用Internet Explorer 11；显示在任务栏；显示在系统托盘；启用最小化保护；当软件从最小化状态恢复时，系统将要求重新验证账簿密码。；网络；代理服务器IP；代理服务器端口；网络离线模式；同步时压缩传输数据；账簿备份；默认保存备份账簿到此文件夹中:；保留最近；的账簿备份文件；更改目录；恢复默认；备份账簿前优化账簿；优化账簿将执行完整性校验，建议保持该选项处于启用状态。；备份账簿时压缩账簿；启用压缩可有效缩减账簿备份文件体积，显著降低磁盘存储空间的占用。；打开文件夹；授权；序列号:；请妥善保管您的序列号，这是您享受正版软件售后服务的凭证。\|双击复制序列号到剪贴板；查看注册资料；修改序列号保护信息；找回序列号保护信息；合并序列号使用期；高级；启用显示缓存；如遇界面显示乱码问题，可尝试通过重置系统界面缓存修复。；交易记录高亮；高亮记录以标记特定的交易记录，高亮快捷键为空格键。；双击隐藏统计金额；打开报表时自动查询；双击定制报表单元格；选择高亮颜色；重置显示缓存；设置非 Unicode 程序的语言；异步刷新模式 |  | tvSection -> tvSectionDblClick；更改目录 -> btnChangeDirClick；恢复默认 -> btnResetDirClick；打开文件夹 -> btnOpenDirClick；edtSerialNo -> edtSerialNoDblClick；查看注册资料 -> btnRegisterInfoClick；修改序列号保护信息 -> btnChangeSerialPassClick；找回序列号保护信息 -> btnForgotSerialPassClick；合并序列号使用期 -> btnMergeSerialNoClick；重置显示缓存 -> btnResetCacheClick；设置非 Unicode 程序的语言 -> btnSetLanguageClick |
| `TTEMPLATEDLGFM` | 批量记账 | 批量记账；在批量处理收支记录时，金额为零的记录将不会被生成。；生成收支记录；删除模板；存为模板 |  | 生成收支记录 -> btnSaveTransClick；删除模板 -> btnDeleteTemplateClick；存为模板 -> btnSaveTemplateClick |
| `TTHEMEUIFM` | ThemeUIFm | 使用主题图片；启动画面；对话框图片；主窗口图片；主窗口工具栏图片；功能区图片；其他；默认主题图片；避免内存出错 |  |  |
| `TTHIRDDEPOSITSACCTDLGFM` | 第三方储值 | 第三方储值；账户别名；创建日期；联网登录号；联网账号 |  |  |
| `TTHIRDDEPOSITSTRANSFM` | 支付宝交易明细 | 支付宝交易明细 |  |  |
| `TTRANSACTIONPLANDLGFM` | 交易计划 | 交易计划 |  |  |
| `TTRANSDLGFM` | TransDlgFm | 日期；备注；主题；保存并新添；确定；查看附件；添加删除附件 |  | 保存并新添 -> btnSaveNewClick；确定 -> btnSaveExitClick；查看附件 -> btnAccessoriesClick；添加删除附件 -> miAccessoriesClick |
| `TTRANSFERLISTTEMPLATEFRAME` |  | 日期；转出账户；转入账户；转账金额；手续费；标签；备注 |  |  |
| `TTRANSFERTEMPLATEDLGFM` | 批量转账 | 批量转账；系统仅生成转账金额不为零的有效记录，相关手续费将从转出账户中扣除。；生成转账记录；删除模板；存为模板 |  | 生成转账记录 -> btnSaveTransClick；删除模板 -> btnDeleteTemplateClick；存为模板 -> btnSaveTemplateClick |
| `TTRANSFRAME` |  | 操作；查找；记账；批量操作；日期；活动类型；主题；备注；附件；批量操作模式；复制记录；粘贴记录；粘贴记录到今天；同日期记录上移；同日期记录下移；退款；转为计划；活动类型更改为；查看附件；添加删除附件；修改；删除；余额调整；导出；打印；查看账户资料；设为软件首页；设置标签；设置备注；退出批量操作模式 | `TransCheck`；`TransType`；`id`；`FIID`；`Transdate`；`FakeTransDate`；`Theme`；`Description`；`AccessoriesID`；`UserMark`；`_Amount`；`Bala`；`TransName`；`XX`；`CreateTime` | 操作 -> btnOperateClick；记账 -> btnNewTransClick；DBGrid -> actModifyExecute；批量操作模式 -> miBatchModeClick；复制记录 -> miCopyRecClick；粘贴记录 -> miPasteRecClick；粘贴记录到今天 -> miPasteTodayClick；同日期记录上移 -> miUpTransClick；同日期记录下移 -> miDownTransClick；退款 -> miRefundClick；转为计划 -> miIntoPlanClick；活动类型更改为 -> miChangeTransClick；查看附件 -> miAccessoriesClick；添加删除附件 -> mmiAddAccessClick；修改 -> actModifyExecute；删除 -> actDeleteExecute；查找 -> actFindExecute；余额调整 -> actAdjustExecute；导出 -> actExportExecute；打印 -> actPrintExecute；查看账户资料 -> actOverviewExecute；设为软件首页 -> N7Click；删除 -> miBatchDeleteClick；设置标签 -> miSetTagClick；设置备注 -> miSetDescriptionClick；退出批量操作模式 -> miQuitBatchModeClick |
| `TTRANSLISTTEMPLATEFRAME` |  | 日期；收支项目；资金账户；金额；标签；备注 |  |  |
| `TUNEARNEDVIEWFRAME` |  |  |  |  |
| `TUPDATEVERIFYCODEFM` | 修改序列号保护信息 | 修改序列号保护信息；序列号；保护信息；新保护信息；确定 |  | 确定 -> btnEnterClick |
| `TUSABLEMONEYCHARTFRAME` |  |  |  |  |
| `TVIEWFRAME` |  |  |  |  |
| `TWASTEBOOKFM` | 财务记录 | 财务记录；查找；操作；收支\|流水；批量操作；真日期；日期；活动类型；流入；流出；资产账户；标签；备注；币种；附件；批量操作模式；复制记录；粘贴记录；粘贴记录到今天；同日期记录上移；同日期记录下移；退款；转为计划；活动类型更改为；查看附件；添加删除附件；修改；删除；导出到文件；打印；筛选；放弃筛选；替换收支项目；记录分组显示；设为软件首页；设置标签；设置备注；退出批量操作模式 | `TransID`；`TransType`；`TransCheck`；`TransDate`；`FakeTransDate`；`CategoryName`；`IncAmount`；`ExpAmount`；`AcctName`；`TransTheme`；`sDesc`；`ObjName`；`AccessoriesID`；`IncLocal`；`ExpLocal`；`TransAmount`；`UserMark`；`CateID`；`CType`；`AcctNo1`；`AcctNo2`；`StateID`；`TransObjectID`；`IncCurrency`；`ExpCurrency`；`CreateTime` | 财务记录 -> FormShow；查找 -> btnFindClick；操作 -> btnActionClick；收支\|流水 -> btnDataTypeClick；Grid -> actModifyExecute；批量操作模式 -> miBatchModeClick；复制记录 -> miCopyRecClick；粘贴记录 -> miPasteRecClick；粘贴记录到今天 -> miPasteTodayClick；同日期记录上移 -> miUpTransClick；同日期记录下移 -> miDownTransClick；退款 -> miRefundClick；转为计划 -> miIntoPlanClick；活动类型更改为 -> miChangeTransClick；查看附件 -> miAccessoriesClick；添加删除附件 -> mmiAddAccessClick；修改 -> actModifyExecute；删除 -> actDeleteExecute；查找 -> actFindExecute；导出到文件 -> actExportExecute；打印 -> actPrintExecute；筛选 -> actFilterExecute；放弃筛选 -> actClearFilterExecute；替换收支项目 -> miReplaceCategoryClick；记录分组显示 -> miGroupClick；设为软件首页 -> N7Click；设置标签 -> miSetTagClick；设置备注 -> miSetDescriptionClick；退出批量操作模式 -> miQuitBatchModeClick |
| `TXFERPLANDLGFM` | 转账计划 | 转账计划；转出账户；转入账户；金额；主题；手续费；手续费账户；自动执行；<无> |  | 自动执行 -> chkAutoExecuteClick |

## 非窗体资源

以下项目保留在 PE 的 RCDATA 清单中，但运行时载荷不是 DFM：

- `CATEGORYADD`：不是运行时 DFM：签名为 b'\x89PNG'
- `CATEGORYHIDE`：不是运行时 DFM：签名为 b'\x89PNG'
- `CATEGORYHIDEHIGHLIGHT`：不是运行时 DFM：签名为 b'\x89PNG'
- `CATEGORYSYSTEM`：不是运行时 DFM：签名为 b'\x89PNG'
- `DOTLINE`：不是运行时 DFM：签名为 b'\x89PNG'
- `DVCLAL`：不是运行时 DFM：签名为 b'&=O8'
- `FRAME`：不是运行时 DFM：签名为 b'\x89PNG'
- `HINT`：不是运行时 DFM：签名为 b'\x89PNG'
- `HINTACTIVE`：不是运行时 DFM：签名为 b'\x89PNG'
- `INFOPANELICON`：不是运行时 DFM：签名为 b'\x89PNG'
- `INFOPANELLINE`：不是运行时 DFM：签名为 b'\x89PNG'
- `LISTCOLLAPSE`：不是运行时 DFM：签名为 b'\x89PNG'
- `LISTCOLLAPSEACTIVE`：不是运行时 DFM：签名为 b'\x89PNG'
- `LISTEXPAND`：不是运行时 DFM：签名为 b'\x89PNG'
- `LISTEXPANDACTIVE`：不是运行时 DFM：签名为 b'\x89PNG'
- `LISTVIEW_BUTTOM_IMAGE`：不是运行时 DFM：签名为 b'\x89PNG'
- `MENUICON_1`：不是运行时 DFM：签名为 b'\x89PNG'
- `MENUICON_2`：不是运行时 DFM：签名为 b'\x89PNG'
- `MENUICON_3`：不是运行时 DFM：签名为 b'\x89PNG'
- `MENUICON_4`：不是运行时 DFM：签名为 b'\x89PNG'
- `MENUICON_5`：不是运行时 DFM：签名为 b'\x89PNG'
- `MENUICON_6`：不是运行时 DFM：签名为 b'\x89PNG'
- `MENUICON_7`：不是运行时 DFM：签名为 b'\x89PNG'
- `MENUICON_8`：不是运行时 DFM：签名为 b'\x89PNG'
- `NOTSAFE`：不是运行时 DFM：签名为 b'\x89PNG'
- `PACKAGEINFO`：不是运行时 DFM：签名为 b'\x00\x00\x00\xcc'
- `PNG_TREEVIEW_COLLAPSE`：不是运行时 DFM：签名为 b'\x89PNG'
- `PNG_TREEVIEW_EXPAND`：不是运行时 DFM：签名为 b'\x89PNG'
- `PNG_TREEVIEW_STRIP_HOVER_LEFT`：不是运行时 DFM：签名为 b'\x89PNG'
- `PNG_TREEVIEW_STRIP_HOVER_MIDDLE`：不是运行时 DFM：签名为 b'\x89PNG'
- `PNG_TREEVIEW_STRIP_HOVER_RIGHT`：不是运行时 DFM：签名为 b'\x89PNG'
- `PNG_TREEVIEW_STRIP_SELECTED_LEFT`：不是运行时 DFM：签名为 b'\x89PNG'
- `PNG_TREEVIEW_STRIP_SELECTED_MIDDLE`：不是运行时 DFM：签名为 b'\x89PNG'
- `PNG_TREEVIEW_STRIP_SELECTED_RIGHT`：不是运行时 DFM：签名为 b'\x89PNG'
- `SAFE`：不是运行时 DFM：签名为 b'\x89PNG'
- `TAGACTIVE`：不是运行时 DFM：签名为 b'\x89PNG'
- `TAGFOCUSEDDARK`：不是运行时 DFM：签名为 b'\x89PNG'
- `TAGFOCUSEDGREY`：不是运行时 DFM：签名为 b'\x89PNG'
- `TAGNORMAL`：不是运行时 DFM：签名为 b'\x89PNG'
- `TAGSELECTED`：不是运行时 DFM：签名为 b'\x89PNG'
