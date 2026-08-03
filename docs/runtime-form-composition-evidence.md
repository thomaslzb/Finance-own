# MoneyHome8 运行时窗体组合与嵌入视图证据

本文档由运行时 DFM 根类和组件类引用自动生成。它证明设计时父子装配关系，不把静态引用扩大解释为真实运行结果。

## 1. 完整性结论

- 运行时窗体：`460` 个
- DFM 序列化组合实例：`108` 条
- 去重后的逻辑直接组合关系：`107` 条
- 被其它窗体组合的资源：`86` 个
- 被多个父窗体复用的资源：`10` 个
- 无文案嵌入视图：`37` 个
- 已找到父窗体的嵌入视图：`37` 个
- 未解析嵌入视图：`0` 个
- 内部或实验入口：`2` 个，其中设计时父窗体引用 `0` 个

Delphi 会把嵌套 Frame 子树再次序列化到最终宿主中，因此本台账同时保留序列化实例数和去重后的逻辑直接组合边。`37/37` 个无文案嵌入视图都已找到直接父窗体，因此父窗体装配关系不再是缺口。仍需动态验证的是空数据、有数据、筛选、命令和计算结果。`2` 个内部或实验入口没有设计时父窗体引用，但仍可能由事件代码动态创建，不能据此判定为不可达。

## 2. 无文案嵌入视图

| 嵌入资源 | 业务域 | 交互角色 | 直接父窗体 | 最终宿主 | 实例路径 | 目标数据流 |
| --- | --- | --- | --- | --- | --- | --- |
| `TADVANCESVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | `TCLAIMSDEBTCONTAINER` | `TCLAIMSTRANSFM` | `ClaimsDebtContainer.PgControl.TabSheet5.AdvancesViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TALIPAYVIEWFRAME` | 通用交易、流水与模板 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.AlipayViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TASSETSCONSTITUTECHARTFRAME` | 重大资产与家居物品 | 统计/图表/嵌入视图 | `TSOFTINDEXCENTERFORM` | `TSOFTINDEXCENTERFORM` | `SoftIndexCenterForm.pnlChildClient.pnlChildClientArea.sb1.AssetsConstituteChartFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TASSETSMARKETCONSTITUTESFRAME` | 重大资产与家居物品 | 统计/图表/嵌入视图 | `TASSETTRANSFM`；`TPRACTRANSFM` | `TASSETTRANSFM`；`TPRACTRANSFM` | `AssetTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet3.AssetsMarketConstitutesFrame`；`PracTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.AssetsMarketConstitutesFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TASSETVIEWFRAME` | 重大资产与家居物品 | 统计/图表/嵌入视图 | `TASSETTRANSFM` | `TASSETTRANSFM` | `AssetTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet4.AssetViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TBONDSMARKETCONSTITUTESFRAME` | 债券 | 统计/图表/嵌入视图 | `TMARKETDEBTTRANSFM` | `TMARKETDEBTTRANSFM` | `MarketDebtTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.BondsMarketConstitutesFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TBONDSVIEWFRAME` | 债券 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.BondsViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TCARDVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.CardViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TCASHVIEWFRAME` | 通用交易、流水与模板 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.CashViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TCURRDEPOSITSVIEWFRAME` | 存款与银行理财产品 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.CurrDepositsViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TCURRFUNDMARKETCONSTITUTESFRAME` | 基金与货币基金 | 统计/图表/嵌入视图 | `TMONEYTRANSFM` | `TMONEYTRANSFM` | `MoneyTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.CurrFundMarketConstitutesFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TCURRFUNDVIEWFRAME` | 基金与货币基金 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.CurrFundViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TDEBTINVESTMENTACCTLISTFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | `TDEBTINVESTMENTTRANSFM` | `TDEBTINVESTMENTTRANSFM` | `DebtInvestmentTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.FDebtInvestmentAcctListFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TDEBTINVESTMENTTRANSFRAME` | 债权债务、信用与摊销 | 交易明细与历史 | `TDEBTINVESTMENTTRANSFM` | `TDEBTINVESTMENTTRANSFM` | `DebtInvestmentTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.FDebtInvestmentTransFrame` | 已提交交易 -> 查询投影 -> 明细操作与下游报表 |
| `TDEBTINVESTMENTVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.DebtInvestmentViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TDEFERREDVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | `TCLAIMSDEBTCONTAINER` | `TCLAIMSTRANSFM` | `ClaimsDebtContainer.PgControl.TabSheet3.DeferredViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TEXCHANGEMARKETCONSTITUTESFRAME` | 外汇 | 统计/图表/嵌入视图 | `TFOREIGNTRANSFM` | `TFOREIGNTRANSFM` | `ForeignTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.ExchangeMarketConstitutesFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TEXCHANGEVIEWFRAME` | 外汇 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.ExchangeViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TFIXDEPOSITSVIEWFRAME` | 存款与银行理财产品 | 统计/图表/嵌入视图 | `TFIXEDDEPOSITTRANSFM` | `TFIXEDDEPOSITTRANSFM` | `FixedDepositTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.FixDepositsViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TFUTURESVIEWFRAME` | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.FuturesViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TINSUREVIEWFRAME` | 保险与社会保障 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM`；`TSOCIALSECURITYTRANSFM` | `TACCOUNTOVERVIEWDLGFM`；`TSOCIALSECURITYTRANSFM` | `AccountOverviewDlgFm.pnlDlgClient.InsureViewFrame`；`SocialSecurityTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet3.InsureViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TMARGINVIEWFRAME` | 融资融券 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.MarginViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TMARKETCONSTITUTESFRAME` | 投资公共能力 | 统计/图表/嵌入视图 | `TGOLDTRANSFM`；`TOPENFUNDTRANSFM`；`TSECURITYTRANSFM` | `TGOLDTRANSFM`；`TOPENFUNDTRANSFM`；`TSECURITYTRANSFM` | `GoldTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.MarketConstitutesFrame`；`OpenFundTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.MarketConstitutesFrame`；`SecurityTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.MarketConstitutesFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TMONEYINFOVIEWFRAME` | 存款与银行理财产品 | 统计/图表/嵌入视图 | `TMONEYTRANSFM` | `TMONEYTRANSFM` | `MoneyTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet4.MoneyInfoViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TMONEYPRODUCTSVIEWFRAME` | 存款与银行理财产品 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.MoneyProductsViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TOPENFUNDVIEWFRAME` | 基金与货币基金 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.OpenFundViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TPAYABLESVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | `TCLAIMSDEBTCONTAINER` | `TCLAIMSTRANSFM` | `ClaimsDebtContainer.PgControl.TabSheet2.PayablesViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TPRACGROUPVIEWFRAME` | 重大资产与家居物品 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.PracGroupViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TPRACSTATISTICFRAME` | 重大资产与家居物品 | 统计/图表/嵌入视图 | `TPRACTRANSFM` | `TPRACTRANSFM` | `PracTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.PracStatisticFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TPRECIOUSMETALSTDVIEWFRAME` | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.PreciousMetalsTDViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TPRECIOUSVIEWFRAME` | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.PreciousViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TRECEIVABLESVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | `TCLAIMSDEBTCONTAINER` | `TCLAIMSTRANSFM` | `ClaimsDebtContainer.PgControl.TabSheet1.ReceivablesViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TSTOCKVIEWFRAME` | 证券 | 统计/图表/嵌入视图 | `TACCOUNTOVERVIEWDLGFM` | `TACCOUNTOVERVIEWDLGFM` | `AccountOverviewDlgFm.pnlDlgClient.StockViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TTRANSFERLISTTEMPLATEFRAME` | 通用交易、流水与模板 | 业务交易录入 | `TTRANSFERTEMPLATEDLGFM` | `TTRANSFERTEMPLATEDLGFM` | `TransferTemplateDlgFm.pnlDlgClient.FTransferListTemplateFrame` | 用户输入 -> 领域校验 -> 原子分录/专项扩展事务 |
| `TTRANSLISTTEMPLATEFRAME` | 通用交易、流水与模板 | 配置与调整 | `TTEMPLATEDLGFM` | `TTEMPLATEDLGFM` | `TemplateDlgFm.pnlDlgClient.FTransListTemplateFrame` | 配置/调整输入 -> 领域规则或显示状态持久化 |
| `TUNEARNEDVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | `TCLAIMSDEBTCONTAINER` | `TCLAIMSTRANSFM` | `ClaimsDebtContainer.PgControl.TabSheet4.UnearnedViewFrame` | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| `TUSABLEMONEYCHARTFRAME` | 报表与分析投影 | 报表查询投影 | `TSOFTINDEXCENTERFORM` | `TSOFTINDEXCENTERFORM` | `SoftIndexCenterForm.pnlChildClient.pnlChildClientArea.sb1.UsableMoneyChartFrame` | SQLite 真相 -> 参数化查询 -> 表格/图表/导出 |

## 3. 多父窗体复用组件

这类组件应在 Rust 版优先实现为共享视图或共享查询投影，避免复制业务规则。

| 资源 | 父窗体数 | 父窗体 | 角色 | 表面类型 |
| --- | ---: | --- | --- | --- |
| `TASSETSMARKETCONSTITUTESFRAME` | 2 | `TASSETTRANSFM`；`TPRACTRANSFM` | projection_view | embedded_indirect_surface |
| `TCASHTRANSFRAME` | 4 | `TCASHTRANSFM`；`TCURRENTTRANSFM`；`TFIXEDDEPOSITTRANSFM`；`TTHIRDDEPOSITSTRANSFM` | transaction_history | business_surface |
| `THISTORYPROFITFRAME` | 9 | `TCURRFUNDTRANSFM`；`TFUTURESTRANSFM`；`TGOLDTRANSFM`；`TMARGINTRANSFM`；`TMARKETDEBTTRANSFM`；`TMONEYTRANSFM`；`TOPENFUNDTRANSFM`；`TPRECIOUSMETALSTDTRANSFM`；`TSECURITYTRANSFM` | projection_view | business_surface |
| `TINCEXPEDITFRAME` | 2 | `TINCEXPDLGFM`；`TINCEXPINSTALLMENTWIZARDDLG` | transaction_editor | business_surface |
| `TINSTALLMENTEDITFRAME` | 3 | `TINCEXPINSTALLMENTWIZARDDLG`；`TINSTALLMENTEDITDLG`；`TPRACBUYINSTALLMENTWIZARDDLG` | configuration_editor | business_surface |
| `TINSURECASHVALUEFRAME` | 2 | `TMISCDIALOGFM`；`TSOCIALSECURITYTRANSFM` | configuration_editor | business_surface |
| `TINSURETRANSFRAME` | 2 | `TINSURETRANSFM`；`TSOCIALSECURITYTRANSFM` | transaction_history | business_surface |
| `TINSUREVIEWFRAME` | 2 | `TACCOUNTOVERVIEWDLGFM`；`TSOCIALSECURITYTRANSFM` | projection_view | embedded_indirect_surface |
| `TMARKETCONSTITUTESFRAME` | 3 | `TGOLDTRANSFM`；`TOPENFUNDTRANSFM`；`TSECURITYTRANSFM` | projection_view | embedded_indirect_surface |
| `TPRACBUYEDITFRAME` | 2 | `TPRACASSETBUYDLGFM`；`TPRACBUYINSTALLMENTWIZARDDLG` | transaction_editor | business_surface |

## 4. 内部或实验入口

| 资源 | 标题 | 设计时父窗体引用 | 静态状态 | 剩余验证 |
| --- | --- | ---: | --- | --- |
| `TAIPANELDLG` | AI | 0 | no_design_time_composition_reference | 没有设计时父窗体引用不等于不可达，仍可能由事件代码动态创建 |
| `TCONSOLEFM` | 控制台 | 0 | no_design_time_composition_reference | 没有设计时父窗体引用不等于不可达，仍可能由事件代码动态创建 |

## 5. 全部设计时组合关系

| 逻辑直接父级 | 父标题 | 子资源 | 实例名 | 代表对象路径 | 序列化次数 | 子角色 | 子表面类型 |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TALIPAYVIEWFRAME` | `AlipayViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.AlipayViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TBONDSVIEWFRAME` | `BondsViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.BondsViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TCARDVIEWFRAME` | `CardViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.CardViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TCASHVIEWFRAME` | `CashViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.CashViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TCURRDEPOSITSVIEWFRAME` | `CurrDepositsViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.CurrDepositsViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TCURRFUNDVIEWFRAME` | `CurrFundViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.CurrFundViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TDEBTINVESTMENTVIEWFRAME` | `DebtInvestmentViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.DebtInvestmentViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TEXCHANGEVIEWFRAME` | `ExchangeViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.ExchangeViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TFUTURESVIEWFRAME` | `FuturesViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.FuturesViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TINSUREVIEWFRAME` | `InsureViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.InsureViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TMARGINVIEWFRAME` | `MarginViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.MarginViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TMONEYPRODUCTSVIEWFRAME` | `MoneyProductsViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.MoneyProductsViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TOPENFUNDVIEWFRAME` | `OpenFundViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.OpenFundViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TPRACGROUPVIEWFRAME` | `PracGroupViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.PracGroupViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TPRECIOUSMETALSTDVIEWFRAME` | `PreciousMetalsTDViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.PreciousMetalsTDViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TPRECIOUSVIEWFRAME` | `PreciousViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.PreciousViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | `TSTOCKVIEWFRAME` | `StockViewFrame` | `AccountOverviewDlgFm.pnlDlgClient.StockViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TASSETTRANSFM` | 重大资产交易明细 | `TASSETSMARKETCONSTITUTESFRAME` | `AssetsMarketConstitutesFrame` | `AssetTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet3.AssetsMarketConstitutesFrame` | 1 | projection_view | embedded_indirect_surface |
| `TASSETTRANSFM` | 重大资产交易明细 | `TASSETSSTATISTICFRAME` | `AssetsStatisticFrame` | `AssetTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.AssetsStatisticFrame` | 1 | projection_view | business_surface |
| `TASSETTRANSFM` | 重大资产交易明细 | `TASSETSTRANSFRAME` | `AssetsTransFrame` | `AssetTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.AssetsTransFrame` | 1 | transaction_history | business_surface |
| `TASSETTRANSFM` | 重大资产交易明细 | `TASSETSVALUEMANAGEMENTFRAME` | `AssetsValueManagementFrame` | `AssetTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.AssetsValueManagementFrame` | 1 | configuration_editor | business_surface |
| `TASSETTRANSFM` | 重大资产交易明细 | `TASSETVIEWFRAME` | `AssetViewFrame` | `AssetTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet4.AssetViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TCASHTRANSFM` | 现金交易列表 | `TCASHTRANSFRAME` | `CashTransFrame` | `CashTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.CashTransFrame` | 1 | transaction_history | business_surface |
| `TCLAIMSDEBTCONTAINER` |  | `TADVANCESVIEWFRAME` | `AdvancesViewFrame` | `ClaimsDebtContainer.PgControl.TabSheet5.AdvancesViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TCLAIMSDEBTCONTAINER` |  | `TDEFERREDVIEWFRAME` | `DeferredViewFrame` | `ClaimsDebtContainer.PgControl.TabSheet3.DeferredViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TCLAIMSDEBTCONTAINER` |  | `TPAYABLESVIEWFRAME` | `PayablesViewFrame` | `ClaimsDebtContainer.PgControl.TabSheet2.PayablesViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TCLAIMSDEBTCONTAINER` |  | `TRECEIVABLESVIEWFRAME` | `ReceivablesViewFrame` | `ClaimsDebtContainer.PgControl.TabSheet1.ReceivablesViewFrame` | 2 | projection_view | embedded_indirect_surface |
| `TCLAIMSDEBTCONTAINER` |  | `TUNEARNEDVIEWFRAME` | `UnearnedViewFrame` | `ClaimsDebtContainer.PgControl.TabSheet4.UnearnedViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TCLAIMSTRANSFM` | 债权债务交易明细 | `TCLAIMSDEBTCONTAINER` | `ClaimsDebtContainer` | `ClaimsTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet4.ClaimsDebtContainer` | 1 | projection_view | business_surface |
| `TCLAIMSTRANSFM` | 债权债务交易明细 | `TCLAIMSDEBTSCONSTITUTESFRAME` | `ClaimsDebtsConstitutesFrame` | `ClaimsTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.ClaimsDebtsConstitutesFrame` | 1 | configuration_editor | business_surface |
| `TCLAIMSTRANSFM` | 债权债务交易明细 | `TCLAIMSDEBTSTATISTICFRAME` | `ClaimsDebtStatisticFrame` | `ClaimsTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.ClaimsDebtStatisticFrame` | 1 | projection_view | business_surface |
| `TCLAIMSTRANSFM` | 债权债务交易明细 | `TCLAIMSDEBTTRANSFRAME` | `ClaimsDebtTransFrame` | `ClaimsTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.ClaimsDebtTransFrame` | 1 | transaction_history | business_surface |
| `TCLAIMSTRANSFM` | 债权债务交易明细 | `TREPAYMENTTABLEFRAME` | `RepaymentTableFrame` | `ClaimsTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet3.RepaymentTableFrame` | 1 | transaction_editor | business_surface |
| `TCREDITCARDTRANSFM` | 信用卡交易明细 | `TCREDITCARDSTATISTICFRAME` | `CreditCardStatisticFrame` | `CreditCardTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.CreditCardStatisticFrame` | 1 | projection_view | business_surface |
| `TCREDITCARDTRANSFM` | 信用卡交易明细 | `TCREDITCARDTRANSFRAME` | `CreditCardTransFrame` | `CreditCardTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.CreditCardTransFrame` | 1 | transaction_history | business_surface |
| `TCREDITCARDTRANSFM` | 信用卡交易明细 | `TINSTALLMENTFRAME` | `InstallmentFrame` | `CreditCardTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.InstallmentFrame` | 1 | configuration_editor | business_surface |
| `TCURRENTTRANSFM` | 活期存款交易明细 | `TCASHTRANSFRAME` | `CurrTransFrame` | `CurrentTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.CurrTransFrame` | 1 | transaction_history | business_surface |
| `TCURRFUNDTRANSFM` | 货币基金交易明细 | `TCURRFUNDSTATISTICFRAME` | `CurrFundStatisticFrame` | `CurrFundTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.CurrFundStatisticFrame` | 1 | projection_view | business_surface |
| `TCURRFUNDTRANSFM` | 货币基金交易明细 | `TCURRFUNDTRANSFRAME` | `CurrFundTransFrame` | `CurrFundTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.CurrFundTransFrame` | 1 | transaction_history | business_surface |
| `TCURRFUNDTRANSFM` | 货币基金交易明细 | `THISTORYPROFITFRAME` | `HistoryProfitFrame` | `CurrFundTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.HistoryProfitFrame` | 1 | projection_view | business_surface |
| `TDEBTINVESTMENTTRANSFM` | 网贷账户交易明细 | `TDEBTINVESTMENTACCTLISTFRAME` | `FDebtInvestmentAcctListFrame` | `DebtInvestmentTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.FDebtInvestmentAcctListFrame` | 1 | projection_view | embedded_indirect_surface |
| `TDEBTINVESTMENTTRANSFM` | 网贷账户交易明细 | `TDEBTINVESTMENTPAYOBJECTFRAME` | `FDebtInvestmentPayObjectFrame` | `DebtInvestmentTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet3.FDebtInvestmentPayObjectFrame` | 1 | projection_view | business_surface |
| `TDEBTINVESTMENTTRANSFM` | 网贷账户交易明细 | `TDEBTINVESTMENTSTATISTICFRAME` | `FDebtInvestmentStatisticFrame` | `DebtInvestmentTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.FDebtInvestmentStatisticFrame` | 1 | projection_view | business_surface |
| `TDEBTINVESTMENTTRANSFM` | 网贷账户交易明细 | `TDEBTINVESTMENTTRANSFRAME` | `FDebtInvestmentTransFrame` | `DebtInvestmentTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.FDebtInvestmentTransFrame` | 1 | transaction_history | embedded_indirect_surface |
| `TFIXEDDEPOSITTRANSFM` | 定期存单 | `TCASHTRANSFRAME` | `FixedDepositTransFrame` | `FixedDepositTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.FixedDepositTransFrame` | 1 | transaction_history | business_surface |
| `TFIXEDDEPOSITTRANSFM` | 定期存单 | `TFIXDEPOSITSVIEWFRAME` | `FixDepositsViewFrame` | `FixedDepositTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.FixDepositsViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TFIXEDDEPOSITTRANSFM` | 定期存单 | `TFIXEDDEPOSITSTATISTICFRAME` | `FFixedDepositStatisticFrame` | `FixedDepositTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.FFixedDepositStatisticFrame` | 1 | projection_view | business_surface |
| `TFOREIGNTRANSFM` | 外汇交易明细 | `TEXCHANGEMARKETCONSTITUTESFRAME` | `ExchangeMarketConstitutesFrame` | `ForeignTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.ExchangeMarketConstitutesFrame` | 1 | projection_view | embedded_indirect_surface |
| `TFOREIGNTRANSFM` | 外汇交易明细 | `TFOREIGNSTATISTICFRAME` | `ForeignStatisticFrame` | `ForeignTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.ForeignStatisticFrame` | 1 | projection_view | business_surface |
| `TFOREIGNTRANSFM` | 外汇交易明细 | `TFOREIGNTRANSFRAME` | `ForeignTransFrame` | `ForeignTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.ForeignTransFrame` | 1 | transaction_history | business_surface |
| `TFUTURESTRANSFM` | 期货账户交易明细 | `TFUTURESSTATISTICFRAME` | `FFuturesStatisticFrame` | `FuturesTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.FFuturesStatisticFrame` | 1 | projection_view | business_surface |
| `TFUTURESTRANSFM` | 期货账户交易明细 | `TFUTURESTRANSFRAME` | `FFuturesTransFrame` | `FuturesTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.FFuturesTransFrame` | 1 | transaction_history | business_surface |
| `TFUTURESTRANSFM` | 期货账户交易明细 | `THISTORYPROFITFRAME` | `FHistoryProfitFrame` | `FuturesTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.FHistoryProfitFrame` | 1 | projection_view | business_surface |
| `TGOLDTRANSFM` | 贵金属交易明细 | `TGOLDSTATISTICFRAME` | `GoldStatisticFrame` | `GoldTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.GoldStatisticFrame` | 1 | projection_view | business_surface |
| `TGOLDTRANSFM` | 贵金属交易明细 | `TGOLDTRANSFRAME` | `GoldTransFrame` | `GoldTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.GoldTransFrame` | 1 | transaction_history | business_surface |
| `TGOLDTRANSFM` | 贵金属交易明细 | `THISTORYPROFITFRAME` | `HistoryProfitFrame` | `GoldTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet3.HistoryProfitFrame` | 1 | projection_view | business_surface |
| `TGOLDTRANSFM` | 贵金属交易明细 | `TMARKETCONSTITUTESFRAME` | `MarketConstitutesFrame` | `GoldTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.MarketConstitutesFrame` | 1 | projection_view | embedded_indirect_surface |
| `TINCEXPDLGFM` | 日常收支 | `TINCEXPEDITFRAME` | `FIncExpEditFrame` | `IncExpDlgFm.pnlDlgClient.RzPanel1.FIncExpEditFrame` | 1 | transaction_editor | business_surface |
| `TINCEXPINSTALLMENTWIZARDDLG` | 日常支出分期 | `TINCEXPEDITFRAME` | `FIncExpEditFrame` | `IncExpInstallmentWizardDlg.pnlDlgClient.pnl1.nbPage.gBoxIncExp.FIncExpEditFrame` | 1 | transaction_editor | business_surface |
| `TINCEXPINSTALLMENTWIZARDDLG` | 日常支出分期 | `TINSTALLMENTEDITFRAME` | `FInstallmentEditFrame` | `IncExpInstallmentWizardDlg.pnlDlgClient.pnl1.nbPage.gBoxInstallment.FInstallmentEditFrame` | 1 | configuration_editor | business_surface |
| `TINSTALLMENTEDITDLG` | 分期付款 | `TINSTALLMENTEDITFRAME` | `FInstallmentEditFrame` | `InstallmentEditDlg.pnlDlgClient.FInstallmentEditFrame` | 1 | configuration_editor | business_surface |
| `TINSURETRANSFM` | 保险交易明细 | `TINSURETRANSFRAME` | `InsureTransFrame` | `InsureTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.InsureTransFrame` | 1 | transaction_history | business_surface |
| `TMARGINTRANSFM` | 融资融券账户交易明细 | `THISTORYPROFITFRAME` | `FHistoryProfitFrame` | `MarginTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.FHistoryProfitFrame` | 1 | projection_view | business_surface |
| `TMARGINTRANSFM` | 融资融券账户交易明细 | `TMARGINSTATISTICFRAME` | `FMarginStatisticFrame` | `MarginTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.FMarginStatisticFrame` | 1 | projection_view | business_surface |
| `TMARGINTRANSFM` | 融资融券账户交易明细 | `TMARGINTRANSFRAME` | `FMarginTransFrame` | `MarginTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.FMarginTransFrame` | 1 | transaction_history | business_surface |
| `TMARKETDEBTTRANSFM` | 债券交易明细 | `TBONDSMARKETCONSTITUTESFRAME` | `BondsMarketConstitutesFrame` | `MarketDebtTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.BondsMarketConstitutesFrame` | 1 | projection_view | embedded_indirect_surface |
| `TMARKETDEBTTRANSFM` | 债券交易明细 | `THISTORYPROFITFRAME` | `HistoryProfitFrame` | `MarketDebtTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet3.HistoryProfitFrame` | 1 | projection_view | business_surface |
| `TMARKETDEBTTRANSFM` | 债券交易明细 | `TMARKETDEBTSTATISTICFRAME` | `MarketDebtStatisticFrame` | `MarketDebtTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.MarketDebtStatisticFrame` | 1 | projection_view | business_surface |
| `TMARKETDEBTTRANSFM` | 债券交易明细 | `TMARKETDEBTTRANSFRAME` | `MarketDebtTransFrame` | `MarketDebtTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.MarketDebtTransFrame` | 1 | transaction_history | business_surface |
| `TMISCDIALOGFM` | MiscDialog | `TDEBTINVESTMENTPAYTABLEFRAME` | `DebtInvestmentPayTableFrame` | `MiscDialogFm.pnlDlgClient.DebtInvestmentPayTableFrame` | 1 | projection_view | business_surface |
| `TMISCDIALOGFM` | MiscDialog | `TINSURECASHVALUEFRAME` | `InsureCashValueFrame` | `MiscDialogFm.pnlDlgClient.InsureCashValueFrame` | 1 | configuration_editor | business_surface |
| `TMONEYTRANSFM` | 银行理财产品交易明细 | `TCURRFUNDMARKETCONSTITUTESFRAME` | `CurrFundMarketConstitutesFrame` | `MoneyTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.CurrFundMarketConstitutesFrame` | 1 | projection_view | embedded_indirect_surface |
| `TMONEYTRANSFM` | 银行理财产品交易明细 | `THISTORYPROFITFRAME` | `HistoryProfitFrame` | `MoneyTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet3.HistoryProfitFrame` | 1 | projection_view | business_surface |
| `TMONEYTRANSFM` | 银行理财产品交易明细 | `TMONEYINFOVIEWFRAME` | `MoneyInfoViewFrame` | `MoneyTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet4.MoneyInfoViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TMONEYTRANSFM` | 银行理财产品交易明细 | `TMONEYSTATISTICFRAME` | `MoneyStatisticFrame` | `MoneyTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.MoneyStatisticFrame` | 1 | projection_view | business_surface |
| `TMONEYTRANSFM` | 银行理财产品交易明细 | `TMONEYTRANSFRAME` | `MoneyTransFrame` | `MoneyTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.MoneyTransFrame` | 1 | transaction_history | business_surface |
| `TOPENFUNDTRANSFM` | 开放式基金交易明细 | `THISTORYPROFITFRAME` | `HistoryProfitFrame` | `OpenFundTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet3.HistoryProfitFrame` | 1 | projection_view | business_surface |
| `TOPENFUNDTRANSFM` | 开放式基金交易明细 | `TMARKETCONSTITUTESFRAME` | `MarketConstitutesFrame` | `OpenFundTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.MarketConstitutesFrame` | 1 | projection_view | embedded_indirect_surface |
| `TOPENFUNDTRANSFM` | 开放式基金交易明细 | `TOPENFUNDSTATISTICFRAME` | `OpenFundStatisticFrame` | `OpenFundTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.OpenFundStatisticFrame` | 1 | projection_view | business_surface |
| `TOPENFUNDTRANSFM` | 开放式基金交易明细 | `TOPENFUNDTRANSFRAME` | `OpenFundTransFrame` | `OpenFundTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.OpenFundTransFrame` | 1 | transaction_history | business_surface |
| `TPRACASSETBUYDLGFM` | 物品买入 | `TPRACBUYEDITFRAME` | `FPracBuyEditFrame` | `PracAssetBuyDlgFm.pnlDlgClient.RzPanel1.FPracBuyEditFrame` | 1 | transaction_editor | business_surface |
| `TPRACBUYINSTALLMENTWIZARDDLG` | 物品买入分期 | `TINSTALLMENTEDITFRAME` | `FInstallmentEditFrame` | `PracBuyInstallmentWizardDlg.pnlDlgClient.pnl1.nbPage.gBoxInstallment.FInstallmentEditFrame` | 1 | configuration_editor | business_surface |
| `TPRACBUYINSTALLMENTWIZARDDLG` | 物品买入分期 | `TPRACBUYEDITFRAME` | `FPracBuyEditFrame` | `PracBuyInstallmentWizardDlg.pnlDlgClient.pnl1.nbPage.gBoxPracAsset.FPracBuyEditFrame` | 1 | transaction_editor | business_surface |
| `TPRACTRANSFM` | 物品交易明细 | `TASSETSMARKETCONSTITUTESFRAME` | `AssetsMarketConstitutesFrame` | `PracTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.AssetsMarketConstitutesFrame` | 1 | projection_view | embedded_indirect_surface |
| `TPRACTRANSFM` | 物品交易明细 | `TPRACSTATISTICFRAME` | `PracStatisticFrame` | `PracTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.PracStatisticFrame` | 1 | projection_view | embedded_indirect_surface |
| `TPRACTRANSFM` | 物品交易明细 | `TPRACTRANSFRAME` | `PracTransFrame` | `PracTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.PracTransFrame` | 1 | transaction_history | business_surface |
| `TPRECIOUSMETALSTDTRANSFM` | 贵金属TD账户交易明细 | `THISTORYPROFITFRAME` | `FHistoryProfitFrame` | `PreciousMetalsTDTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.FHistoryProfitFrame` | 1 | projection_view | business_surface |
| `TPRECIOUSMETALSTDTRANSFM` | 贵金属TD账户交易明细 | `TPRECIOUSMETALSTDSTATISTICFRAME` | `FPreciousMetalsTDStatisticFrame` | `PreciousMetalsTDTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.FPreciousMetalsTDStatisticFrame` | 1 | projection_view | business_surface |
| `TPRECIOUSMETALSTDTRANSFM` | 贵金属TD账户交易明细 | `TPRECIOUSMETALSTDTRANSFRAME` | `FPreciousMetalsTDTransFrame` | `PreciousMetalsTDTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.FPreciousMetalsTDTransFrame` | 1 | transaction_history | business_surface |
| `TREPORTOPTIONDLGFM` | 筛选 | `TAMOUNTSCREENINGFRAME` | `AmountScreeningFrame1` | `ReportOptionDlgFm.pnlDlgClient.mwPageControl1.tabSum.AmountScreeningFrame1` | 1 | selector_filter | technical_support |
| `TSECURITYTRANSFM` | 上市证券交易列表 | `THISTORYPROFITFRAME` | `HistoryProfitFrame` | `SecurityTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet3.HistoryProfitFrame` | 1 | projection_view | business_surface |
| `TSECURITYTRANSFM` | 上市证券交易列表 | `TMARKETCONSTITUTESFRAME` | `MarketConstitutesFrame` | `SecurityTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.MarketConstitutesFrame` | 1 | projection_view | embedded_indirect_surface |
| `TSECURITYTRANSFM` | 上市证券交易列表 | `TSECURITYSTATISTICFRAME` | `StatisticFrame` | `SecurityTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.StatisticFrame` | 1 | projection_view | business_surface |
| `TSECURITYTRANSFM` | 上市证券交易列表 | `TSECURITYTRANSFRAME` | `SecurityTransFrame` | `SecurityTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.SecurityTransFrame` | 1 | transaction_history | business_surface |
| `TSOCIALSECURITYTRANSFM` | 社会保险账户交易明细 | `TINSURECASHVALUEFRAME` | `InsureCashValueFrame` | `SocialSecurityTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet2.InsureCashValueFrame` | 1 | configuration_editor | business_surface |
| `TSOCIALSECURITYTRANSFM` | 社会保险账户交易明细 | `TINSURETRANSFRAME` | `InsureTransFrame` | `SocialSecurityTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet1.InsureTransFrame` | 1 | transaction_history | business_surface |
| `TSOCIALSECURITYTRANSFM` | 社会保险账户交易明细 | `TINSUREVIEWFRAME` | `InsureViewFrame` | `SocialSecurityTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageBottom.FPageContrl.TabSheet3.InsureViewFrame` | 1 | projection_view | embedded_indirect_surface |
| `TSOCIALSECURITYTRANSFM` | 社会保险账户交易明细 | `TSOCIALSECURITYSTATISTICFRAME` | `SocialSecurityStatisticFrame` | `SocialSecurityTransFm.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.SocialSecurityStatisticFrame` | 1 | projection_view | business_surface |
| `TSOFTINDEXCENTERFORM` | 概况 | `TASSETSCONSTITUTECHARTFRAME` | `AssetsConstituteChartFrame` | `SoftIndexCenterForm.pnlChildClient.pnlChildClientArea.sb1.AssetsConstituteChartFrame` | 1 | projection_view | embedded_indirect_surface |
| `TSOFTINDEXCENTERFORM` | 概况 | `TCLAIMSDEBTSCHARTFRAME` | `ClaimsDebtsChartFrame` | `SoftIndexCenterForm.pnlChildClient.pnlChildClientArea.sb1.ClaimsDebtsChartFrame` | 1 | projection_view | business_surface |
| `TSOFTINDEXCENTERFORM` | 概况 | `TCURRENTMONTHINCEXPPIECHARTFRAME` | `CurrentMonthIncExpPieChartFrame` | `SoftIndexCenterForm.pnlChildClient.pnlChildClientArea.sb1.CurrentMonthIncExpPieChartFrame` | 1 | projection_view | business_surface |
| `TSOFTINDEXCENTERFORM` | 概况 | `TINVESTMENTCHARTFRAME` | `InvestmentChartFrame` | `SoftIndexCenterForm.pnlChildClient.pnlChildClientArea.sb1.InvestmentChartFrame` | 1 | projection_view | business_surface |
| `TSOFTINDEXCENTERFORM` | 概况 | `TMONTHINCEXPCOLUMNCHARTFRAME` | `MonthIncExpColumnChartFrame` | `SoftIndexCenterForm.pnlChildClient.pnlChildClientArea.sb1.MonthIncExpColumnChartFrame` | 1 | projection_view | business_surface |
| `TSOFTINDEXCENTERFORM` | 概况 | `TUSABLEMONEYCHARTFRAME` | `UsableMoneyChartFrame` | `SoftIndexCenterForm.pnlChildClient.pnlChildClientArea.sb1.UsableMoneyChartFrame` | 1 | report_projection | embedded_indirect_surface |
| `TTEMPLATEDLGFM` | 批量记账 | `TTRANSLISTTEMPLATEFRAME` | `FTransListTemplateFrame` | `TemplateDlgFm.pnlDlgClient.FTransListTemplateFrame` | 1 | configuration_editor | embedded_indirect_surface |
| `TTHIRDDEPOSITSTRANSFM` | 支付宝交易明细 | `TCASHTRANSFRAME` | `CurrTransFrame` | `ThirdDepositsTransFM.pnlChildClient.pnlChildClientArea.RzSplitter1.PnlPageTop.CurrTransFrame` | 1 | transaction_history | business_surface |
| `TTRANSFERTEMPLATEDLGFM` | 批量转账 | `TTRANSFERLISTTEMPLATEFRAME` | `FTransferListTemplateFrame` | `TransferTemplateDlgFm.pnlDlgClient.FTransferListTemplateFrame` | 1 | transaction_editor | embedded_indirect_surface |
