# MoneyHome8 计算口径与报表查询投影

本文档由 `runtime-dfm-all-forms.json` 自动生成，记录旧程序能从运行时 DFM 直接确认的计算字段、汇总规则、报表组件与字段投影，并给出 Rust + SQLite 的落地边界。

## 1. 证据结论

- 扫描窗体：`460` 个
- 计算字段：`20` 个
- 明确汇总规则：`6` 条
- 汇总页脚绑定：`2` 条
- 计算相关事件：`17` 个
- 报表窗体：`25` 个
- 报表图表组件：`30` 个
- DFM 内含非空静态 SQL 的数据集：`0` 个

`FieldKind=fkCalculated`、`SummaryGroups`、字段绑定、显示格式和事件名属于本次静态扫描的直接证据。事件处理器公式和运行时 SQL 不在 DFM 中，必须通过代表性数据校准；动态报表列及真实结果后来已由 B16 对全部 `25` 张业务报表逐页补证，但不反向改变本文的静态证据边界。

## 2. 已确认计算字段

| 窗体 | 字段 | 数据集 | 计算事件 | 显示格式 | 证据边界 |
| --- | --- | --- | --- | --- | --- |
|  (`TCASHTRANSFRAME`) | `Amount` | `GridDBQuery` | `` | `` | 确认由旧程序计算；公式待校准 |
|  (`TFOREIGNTRANSFRAME`) | `BuySellType` | `GridDBQuery` | `` | `` | 确认由旧程序计算；公式待校准 |
| 期货品种列表 (`TFUTURESGOODSLISTFM`) | `Fee` | `qry1` | `qry1CalcFields` | `` | 确认由旧程序计算；公式待校准 |
|  (`THISTORYPROFITFRAME`) | `ObjName` | `qryData` | `` | `` | 确认由旧程序计算；公式待校准 |
|  (`THISTORYPROFITFRAME`) | `YKRate` | `qryData` | `` | `,0.00%;-,0.00%` | 确认由旧程序计算；公式待校准 |
| 替换收支项目 (`TIMPORTCATEGORYDLGFM`) | `Inc` | `GridDBQuery` | `GridDBQueryCalcFields` | `,0.00;-,0.00` | 确认由旧程序计算；公式待校准 |
| 替换收支项目 (`TIMPORTCATEGORYDLGFM`) | `Exp` | `GridDBQuery` | `GridDBQueryCalcFields` | `,0.00;-,0.00` | 确认由旧程序计算；公式待校准 |
|  (`TINSTALLMENTFRAME`) | `WHAmount` | `qryData` | `qryDataCalcFields` | `,0.00;-,0.00` | 确认由旧程序计算；公式待校准 |
|  (`TINSURETRANSFRAME`) | `Amount` | `GridDBQuery` | `` | `` | 确认由旧程序计算；公式待校准 |
| 标签 (`TLIFETHEMEFM`) | `FakeTransDate` | `GridDBQuery` | `GridDBQueryCalcFields` | `` | 确认由旧程序计算；公式待校准 |
|  (`TPRACTRANSFRAME`) | `TransObjType` | `GridDBQuery` | `` | `` | 确认由旧程序计算；公式待校准 |
|  (`TTRANSFRAME`) | 余额 (`Bala`) | `GridDBQuery` | `GridDBQueryCalcFields` | `,0.00;-,0.00` | 确认由旧程序计算；公式待校准 |
|  (`TTRANSFRAME`) | `AccessoriesID` | `GridDBQuery` | `GridDBQueryCalcFields` | `` | 确认由旧程序计算；公式待校准 |
|  (`TTRANSFRAME`) | `FakeTransDate` | `GridDBQuery` | `GridDBQueryCalcFields` | `` | 确认由旧程序计算；公式待校准 |
|  (`TTRANSFRAME`) | `TransCheck` | `GridDBQuery` | `GridDBQueryCalcFields` | `` | 确认由旧程序计算；公式待校准 |
| 财务记录 (`TWASTEBOOKFM`) | `AccessoriesID` | `GridDBQuery` | `GridDBQueryCalcFields` | `` | 确认由旧程序计算；公式待校准 |
| 财务记录 (`TWASTEBOOKFM`) | `FakeTransDate` | `GridDBQuery` | `GridDBQueryCalcFields` | `` | 确认由旧程序计算；公式待校准 |
| 财务记录 (`TWASTEBOOKFM`) | `IncLocal` | `GridDBQuery` | `GridDBQueryCalcFields` | `` | 确认由旧程序计算；公式待校准 |
| 财务记录 (`TWASTEBOOKFM`) | `ExpLocal` | `GridDBQuery` | `GridDBQueryCalcFields` | `` | 确认由旧程序计算；公式待校准 |
| 财务记录 (`TWASTEBOOKFM`) | `TransCheck` | `GridDBQuery` | `GridDBQueryCalcFields` | `` | 确认由旧程序计算；公式待校准 |

## 3. 已确认汇总规则

| 窗体 | 组件 | 聚合 | 字段 | 格式 |
| --- | --- | --- | --- | --- |
| 标签 (`TLIFETHEMEFM`) | `DBGrid` | `cstSum` | `Inc` | `(流入=,0.00)` |
| 标签 (`TLIFETHEMEFM`) | `DBGrid` | `cstSum` | `Exp` | `(流出=,0.00)` |
| 标签 (`TLIFETHEMEFM`) | `AssetGrid` | `cstSum` | `AmountSum` | `(合计=,0.00)` |
| 财务记录 (`TWASTEBOOKFM`) | `Grid` | `cstSum` | `IncLocal` | `` |
| 财务记录 (`TWASTEBOOKFM`) | `Grid` | `cstSum` | `ExpLocal` | `` |
| 财务记录 (`TWASTEBOOKFM`) | `Grid` | `cstSum` | `TransAmount` | `差额=,0.00;差额=-,0.00` |
|  (`THISTORYPROFITFRAME`) | `gColQuantity` | 页脚字段绑定 | `Quantity -> YLAmount` |  |
|  (`THISTORYPROFITFRAME`) | `gColAmount` | 页脚字段绑定 | `AMT -> KSAmount` |  |

## 4. 报表组件架构

| 报表 | 页签 | 图表组件 | 静态序列/选项 | 静态字段列 |
| --- | --- | --- | --- | --- |
| 账户日常收支表 (`TRPTACCOUNTINCOMESTATFRM`) |  |  |  |  |
| 资产负债表 (`TRPTBSSTATFRM`) |  | Bar:TWkeWebbrowser；pieAsset:TWkeWebbrowser；pieDebt:TWkeWebbrowser |  |  |
| 现金流表 (`TRPTCASHWASTEFM`) |  | Bar:TWkeWebbrowser；pieInc:TWkeWebbrowser；pieExp:TWkeWebbrowser |  |  |
| 债权债务表 (`TRPTCREDITDEBTSTATFM`) |  | pieTop:TWkeWebbrowser；pieBottom:TWkeWebbrowser |  |  |
| 网贷盈亏一览表 (`TRPTDEBTINVESTMENTINVESTYKFORM`) |  |  |  |  |
| 外汇交易一览表 (`TRPTEXCHANGE6FM`) |  |  |  |  |
| 银行理财产品收益率表 (`TRPTFINANCIALPRODUCTSFM`) |  |  |  |  |
| 可用资金表 (`TRPTFUNDSAVAILABLEFM`) |  | Bar:TWkeWebbrowser；Pie:TWkeWebbrowser |  |  |
| 开放式基金市值大势图 (`TRPTFUNDTRENDFM`) |  | cht:TWkeWebbrowser | 资产总值；基金市值；资金余额 |  |
| 两段时间收支对比表 (`TRPTINCEXPCOMPAREFM`) |  | Bar:TWkeWebbrowser |  |  |
| 收支走势图 (`TRPTINCEXPZSTOVFM`) |  | mwVerticalChart:TmwVerticalChart |  |  |
| 日常收支明细表 (`TRPTINCOMELISTFM`) |  |  |  |  |
| 日常收支表 (`TRPTINCOMESTATFRM`) |  | Bar:TWkeWebbrowser；pieInc:TWkeWebbrowser；pieExp:TWkeWebbrowser |  |  |
| 投资收益一览表 (`TRPTINVESTINCOMEFM`) |  |  |  |  |
| 投资收益率统计表 (`TRPTINVESTMENTPERFORMANCESTATFM`) |  |  |  |  |
| 投资一览表 (`TRPTINVESTVIEWFM`) |  | pieTop:TWkeWebbrowser；pieBottom:TWkeWebbrowser |  |  |
| 月资产走势图 (`TRPTMONTHASSETFM`) |  | cht:TWkeWebbrowser |  |  |
| 月平均收支表 (`TRPTMONTHAVERAGEINCEXPFM`) |  | Bar:TWkeWebbrowser；pieInc:TWkeWebbrowser；pieExp:TWkeWebbrowser |  |  |
| 开放式基金投资一览表 (`TRPTOPENFUNDINVESTFM`) |  | Bar:TWkeWebbrowser；Pie:TWkeWebbrowser |  |  |
| 开放式基金费用及盈亏一览表 (`TRPTOPENFUNDINVESTLOSSFM`) |  |  |  |  |
| 证券投资一览表 (`TRPTSECURITINVESTFM`) |  | Bar:TWkeWebbrowser；Pie:TWkeWebbrowser |  |  |
| 证券费用及盈亏一览表 (`TRPTSECURITINVESTLOSSFM`) |  |  |  |  |
| 证券市值大势图 (`TRPTSTOCKTRENDFM`) |  | cht:TWkeWebbrowser | 资产总值；证券市值；资金余额；上证指数；深证成指 |  |
| 标签日常收支表 (`TRPTTAGINCOMESTATFRM`) |  |  |  |  |
| 收支统计表 (`TRPTYEARINCEXPFORM`) |  | Bar:TWkeWebbrowser；pieInc:TWkeWebbrowser；pieExp:TWkeWebbrowser |  |  |

## 5. 交易与统计投影字段

下表只列出运行时网格绑定字段；字段名和中文列标题属于直接证据，字段之间的公式关系仍按待校准处理。

| 窗体 | 网格投影字段 |
| --- | --- |
| TASSETSSTATISTICFRAME (`TASSETSSTATISTICFRAME`) | 资产名称 (`ObjName`)；币种 (`CurrType`)；当前成本 (`Cost`) `,0.00;-,0.00`；累计收益 (`Scale`) `,0.00;-,0.00`；资产市值 (`Market`) `,0.00;-,0.00`；资产性质 (`IsInvestment`) |
| TASSETSTRANSFRAME (`TASSETSTRANSFRAME`) | 发生金额 (`AMT`) `,0.00;-,0.00`；`CategoryName`；`Iterbala` |
| TCASHTRANSFRAME (`TCASHTRANSFRAME`) | 流入 (`Inc`) `,0.00;-,0.00`；流出 (`Exp`) `,0.00;-,0.00`；`CategoryName`；`Bala` `,0.00;-,0.00`；`Iterbala` |
| TCLAIMSDEBTTRANSFRAME (`TCLAIMSDEBTTRANSFRAME`) | 增加 (`InCorpus`) `,0.00;-,0.00`；减少 (`OutCorpus`) `,0.00;-,0.00`；利息 (`AbsInterest`) `,0.00;,0.00`；合计 (`AMT`) `,0.00;-,0.00`；`CategoryName`；待收/还金额 (`Bala`) `,0.00;-,0.00`；`Iterbala` |
| TCREDITCARDSTATISTICFRAME (`TCREDITCARDSTATISTICFRAME`) | 账单记录时间段 (`BillDate`)；账单日 (`NBillDate`)；还款日 (`LastPayDate`)；流入金额 (`Inc`) `,0.00;-,0.00`；流出金额 (`Exp`) `,0.00;-,0.00`；账单金额 (`BillAmount`) `,0.00;-,0.00` |
| TCREDITCARDTRANSFRAME (`TCREDITCARDTRANSFRAME`) | 流入 (`Inc`) `,0.00;-,0.00`；流出 (`Exp`) `,0.00;-,0.00`；`CategoryName`；`Bala` `,0.00;-,0.00`；`Iterbala` |
| TCURRFUNDSTATISTICFRAME (`TCURRFUNDSTATISTICFRAME`) | 基金名称 (`ObjName`)；累计金额 (`Cost`) `,0.00;-,0.00`；占比% (`scale`) `,0.00;-,0.00` |
| TCURRFUNDTRANSFRAME (`TCURRFUNDTRANSFRAME`) | `CategoryName`；基金名称 (`TransObjID`)；交易金额 (`AMT`) `,0.00;-,0.00`；`Bala` `,0.00;-,0.00`；`Iterbala` |
| TDEBTINVESTMENTACCTLISTFRAME (`TDEBTINVESTMENTACCTLISTFRAME`) | 账户名称 (`AcctName`)；预期年化收益率 (`YearRate`) `,0.00##%;-,0.00##%`；实现盈亏 (`PL`) `,0.00;-,0.00`；待收利息 (`LessInterest`) `,0.00;-,0.00`；待收本金 (`LessCost`) `,0.00;-,0.00`；可用资金 (`Cash`) `,0.00;-,0.00`；资产值 (`AssetValue`) `,0.00;-,0.00`；`AcctID` |
| TDEBTINVESTMENTPAYOBJECTFRAME (`TDEBTINVESTMENTPAYOBJECTFRAME`) | 收款日期 (`NextPayDate`)；账户 (`AcctName`)；投资名称 (`ObjName`)；应收本金 (`PayCost`) `,0.00;-,0.00`；应收利息 (`PayInterest`) `,0.00;-,0.00`；应收合计 (`PayAmount`) `,0.00;-,0.00`；剩余期数 (`UnPayCount`) `,0;-,0` |
| TDEBTINVESTMENTSTATISTICFRAME (`TDEBTINVESTMENTSTATISTICFRAME`) | 名称 (`ObjName`)；投资日期 (`InvestmentDate`)；期限 (`Period`)；收款方式 (`PayMode`)；收款间隔 (`PayFreq`)；剩余期数 (`UnpayCount`)；年利率 (`Rate`) `,0.00##%;-,0.00##%`；待收本金 (`UnpayAmount`) `,0.00;-,0.00` |
| TDEBTINVESTMENTTRANSFRAME (`TDEBTINVESTMENTTRANSFRAME`) | 投资名称 (`TransObjID`)；本金 (`Corpus`) `,0.00;-,0.00`；利息 (`Interest`) `,0.00;-,0.00`；发生金额 (`AMT`) `,0.00;-,0.00`；`CategoryName`；`Bala` `,0.00;-,0.00` |
| TFIXEDDEPOSITSTATISTICFRAME (`TFIXEDDEPOSITSTATISTICFRAME`) | 账户组 \| 存单名称 (`AcctName`)；存单类型 (`DepositType`)；存期 (`Term`)；起存日 (`BeginDate`)；到期日 (`EndDate`)；年利率 (`Rate`) `,0.00##%;-,0.00##%`；余额 (`Balance`) `,0.00;-,0.00`；到期本息 (`MatureSum`) `,0.00;-,0.00` |
| TFOREIGNSTATISTICFRAME (`TFOREIGNSTATISTICFRAME`) | 币种 (`CurrType`)；当前余额 (`Amount`) `,0.00;-,0.00`；当前牌价 (`Price`) `,0.0000;-,0.0000`；折算金额 (`LoaclAmount`) `,0.00;-,0.00` |
| TFOREIGNTRANSFRAME (`TFOREIGNTRANSFRAME`) | 卖出金额 (`OutSum`) `,0.00;-,0.00`；卖出币种 (`OutCurr`)；买入金额 (`InSum`) `,0.00;-,0.00`；买入币种 (`InCurr`)；报价方式 (`BuySellType`)；成交汇率 (`absPrice`) `,0.0000;-,0.0000`；`TransType` |
| TFUTURESSTATISTICFRAME (`TFUTURESSTATISTICFRAME`) | 期货合约 (`ObjName`)；数量(手) (`Amount`) `,0;-,0`；保证金 (`MarginCost`) `,0.00;-,0.00`；市值 (`TheValue`) `,0.00;-,0.00`；占比% (`Scale`) `,0.00;-,0.00`；浮动盈亏 (`PAL`) `,0.00;-,0.00`；均价 (`Price`) `,0.000;-,0.000`；收盘价 (`MarketPrice`) `,0.000;-,0.000`；浮动收益率% (`ProfitRate`) `,0.00##;-,0.00##` |
| TFUTURESTRANSFRAME (`TFUTURESTRANSFRAME`) | `CategoryName`；期货合约 (`ObjName`)；价格 (`Price`) `,0.000;-,0.000`；数量 (`Quantity`) `,0;-,0`；总费用 (`TotalFee`) `,0.00;-,0.00`；交易金额 (`AMT`) `,0.00;-,0.00`；`Bala` `,0.00;-,0.00`；`Iterbala` |
| TGOLDSTATISTICFRAME (`TGOLDSTATISTICFRAME`) | 产品 (`ObjName`)；持仓数量 (`Amount`) `,0.0000;-,0.0000`；买入均价 (`Price`) `,0.0000;-,0.0000`；持仓成本 (`Cost`) `,0.0000;-,0.0000`；市值 (`TheValue`) `,0.00;-,0.00`；占比% (`Scale`) `,0.00;-,0.00`；浮动盈亏 (`PAL`) `,0.00;-,0.00`；浮动收益率% (`ProfitRate`) `,0.00##;-,0.00##`；最新行情 (`MarketPrice`) `,0.0000;-,0.0000` |
| TGOLDTRANSFRAME (`TGOLDTRANSFRAME`) | `CategoryName`；产品名称 (`TransObjID`)；单价 (`Price`) `,0.0000;-,0.0000`；数量 (`Quantity`) `,0.0000;-,0.0000`；交易金额 (`AMT`) `,0.0000;-,0.0000`；`Bala` `,0.00;-,0.00`；`Iterbala` |
| THISTORYPROFITFRAME (`THISTORYPROFITFRAME`) | 交易日期 (`TDate`)；名称 (`ObjName`)；活动类型 (`Name`)；价格 (`Price`)；数量 (`Quantity`)；交易金额 (`AMT`) `,0.00;-,0.00`；实现盈亏 (`PLAmount`) `,0.00;-,0.00`；盈亏比例 (`YKRate`) `,0.00%;-,0.00%` |
| TINSURETRANSFRAME (`TINSURETRANSFRAME`) | `CategoryName`；缴费 (`Inc`) `,0.00;-,0.00`；领取 (`Exp`) `,0.00;-,0.00`；`Iterbala` |
| 标签 (`TLIFETHEMEFM`) | 日期 (`FakeTransDate`)；活动类型 (`CategoryName`)；流入 (`IncAmount`) `,0.00;-,0.00`；流出 (`ExpAmount`) `,0.00;-,0.00`；资金账户/款项 (`AcctName`)；主题 (`TransTheme`)；备注 (`sDesc`)；币种 (`ObjName`)；`TransID`；`CateID`；`TransType`；`TransDate`；`UserMark`；账户名称 (`Name`)；资金余额/资产总值 (`Amount`) `,0.00;-,0.00.`；币种 (`CurrType`)；`ID`；名称 (`Name`) |
| TMARGINSTATISTICFRAME (`TMARGINSTATISTICFRAME`) | 证券/合约 (`ObjName`)；持仓数量 (`Amount`) `,0;-,0`；持仓成本 (`Cost`) `,0.00;-,0.00`；市值 (`TheValue`) `,0.00;-,0.00`；占比% (`Scale`) `,0.00;-,0.00`；浮动盈亏 (`PAL`) `,0.00;-,0.00`；交易盈亏 (`PALWithFee`) `,0.00;-,0.00`；均价 (`Price`) `,0.000;-,0.000`；保本价 (`LowPrice`) `,0.000;-,0.000`；收盘价 (`MarketPrice`) `,0.000;-,0.000`；浮动收益率% (`ProfitRate`) `,0.00##;-,0.00##` |
| TMARGINTRANSFRAME (`TMARGINTRANSFRAME`) | 证券/合约 (`ObjName`)；价格 (`Price`) `,0.000;-,0.000`；数量 (`Quantity`) `,0;-,0`；佣金 (`Commission`) `,0.00;-,0.00`；总费用 (`TotalFee`) `,0.00;-,0.00`；交易金额 (`AMT`) `,0.00;-,0.00`；`CategoryName`；`Bala` `,0.00;-,0.00`；`Iterbala`；`SID` |
| TMARKETDEBTSTATISTICFRAME (`TMARKETDEBTSTATISTICFRAME`) | 债券代码名称 (`ObjName`)；数量 (`Quantity`) `,0.00;-,0.00`；投资金额 (`Cost`) `,0.00;-,0.00`；面值 (`ParValue`) `,0.00;-,0.00`；年利率% (`Rate`) `,0.00##;-,0.00##`；年限 (`Scale`)；到期日 (`MatureDate`) |
| TMARKETDEBTTRANSFRAME (`TMARKETDEBTTRANSFRAME`) | `CategoryName`；债券代码名称 (`TransObjID`)；净价 (`Price`) `,0.00;-,0.00`；应计利息 (`Commission`) `,0.00;-,0.00`；数量 (`Quantity`) `,0.00;-,0.00`；费用 (`TotalFee`) `,0.00;-,0.00`；交易金额 (`AMT`) `,0.00;-,0.00`；`Bala` `,0.00;-,0.00`；`Iterbala` |
| TMONEYSTATISTICFRAME (`TMONEYSTATISTICFRAME`) | 产品名称 (`ObjName`)；机构 (`Organ`)；累计金额 (`Cost`) `,0.00;-,0.00`；占比% (`Scale`) `,0.00;-,0.00`；购买日 (`BeginDate`)；到期日 (`EndDate`)；预计年收益率% (`ProfitRate`) `,0.0000##;-,0.0000##` |
| TMONEYTRANSFRAME (`TMONEYTRANSFRAME`) | `CategoryName`；产品名称 (`TransObjID`)；交易金额 (`AMT`) `,0.00;-,0.00`；`Bala` `,0.00;-,0.00`；`Iterbala` |
| TOPENFUNDSTATISTICFRAME (`TOPENFUNDSTATISTICFRAME`) | 基金名称 (`ObjName`)；持仓数量 (`Amount`) `,0.00;-,0.00`；持仓成本 (`Cost`) `,0.00;-,0.00`；市值 (`TheValue`) `,0.00;-,0.00`；占比% (`Scale`) `,0.00;-,0.00`；浮动盈亏 (`PAL`) `,0.00;-,0.00`；均价 (`Price`) `,0.0000;-,0.0000`；基金净值 (`MarketPrice`) `,0.0000;-,0.0000`；浮动收益率% (`ProfitRate`) `,0.00##;-,0.00##` |
| TOPENFUNDTRANSFRAME (`TOPENFUNDTRANSFRAME`) | `CategoryName`；基金名称 (`TransObjID`)；价格 (`Price`) `,0.0000;-,0.0000`；数量 (`Quantity`) `,0.00;-,0.00`；费率 (`Commission`) `,0.00##;-,0.00##`；交易金额 (`AMT`) `,0.00;-,0.00`；`Bala` `,0.00;-,0.00`；`Iterbala` |
| TPRACTRANSFRAME (`TPRACTRANSFRAME`) | 物品分类/名称 (`TransObjID`)；单价 (`Price`) `,0.00;-,0.00`；数量 (`Quantity`) `,0;-,0`；金额 (`sum2`) `,0.00;-,0.00`；`CategoryName`；`Iterbala` |
| TPRECIOUSMETALSTDSTATISTICFRAME (`TPRECIOUSMETALSTDSTATISTICFRAME`) | 合约 (`ObjName`)；数量(手) (`Amount`) `,0;-,0`；保证金 (`MarginCost`) `,0.00;-,0.00`；市值 (`TheValue`) `,0.00;-,0.00`；占比% (`Scale`) `,0.00;-,0.00`；浮动盈亏 (`PAL`) `,0.00;-,0.00`；均价 (`Price`) `,0.000;-,0.000`；收盘价 (`MarketPrice`) `,0.000;-,0.000`；浮动收益率% (`ProfitRate`) `,0.00##;-,0.00##` |
| TPRECIOUSMETALSTDTRANSFRAME (`TPRECIOUSMETALSTDTRANSFRAME`) | `CategoryName`；期货合约 (`ObjName`)；价格 (`Price`) `,0.000;-,0.000`；数量 (`Quantity`) `,0;-,0`；总费用 (`TotalFee`) `,0.00;-,0.00`；交易金额 (`AMT`) `,0.00;-,0.00`；`Bala` `,0.00;-,0.00`；`Iterbala` |
| TSECURITYSTATISTICFRAME (`TSECURITYSTATISTICFRAME`) | 证券名称 (`ObjName`)；持仓数量 (`Amount`) `,0;-,0`；持仓成本 (`Cost`) `,0.00;-,0.00`；市值 (`TheValue`) `,0.00;-,0.00`；占比% (`Scale`) `,0.00;-,0.00`；浮动盈亏 (`PAL`) `,0.00;-,0.00`；交易盈亏 (`PALWithFee`) `,0.00;-,0.00`；均价 (`Price`) `,0.000;-,0.000`；保本价 (`LowPrice`) `,0.000;-,0.000`；收盘价 (`MarketPrice`) `,0.000;-,0.000`；浮动收益率% (`ProfitRate`) `,0.00##;-,0.00##` |
| TSECURITYTRANSFRAME (`TSECURITYTRANSFRAME`) | 证券名称 (`TransObjID`)；价格 (`Price`) `,0.000;-,0.000`；数量 (`Quantity`) `,0;-,0`；佣金 (`Commission`) `,0.00;-,0.00`；总费用 (`TotalFee`) `,0.00;-,0.00`；交易金额 (`AMT`) `,0.00;-,0.00`；`CategoryName`；`Bala` `,0.00;-,0.00`；`Iterbala` |
| TSOCIALSECURITYSTATISTICFRAME (`TSOCIALSECURITYSTATISTICFRAME`) | 名称 (`Name`)；余额 (`Value`) `,0.00;-,0.00`；备注 (`Description`) |
| TTRANSFRAME (`TTRANSFRAME`) | `TransCheck`；`TransType`；`id`；`FIID`；`Transdate`；日期 (`FakeTransDate`)；主题 (`Theme`)；备注 (`Description`)；附件 (`AccessoriesID`)；`UserMark`；`_Amount` |
| 财务记录 (`TWASTEBOOKFM`) | `TransID`；`TransType`；`TransCheck`；真日期 (`TransDate`)；日期 (`FakeTransDate`)；活动类型 (`CategoryName`)；流入 (`IncAmount`) `,0.00;-,0.00`；流出 (`ExpAmount`) `,0.00;-,0.00`；资产账户 (`AcctName`)；标签 (`TransTheme`)；备注 (`sDesc`)；币种 (`ObjName`)；附件 (`AccessoriesID`)；`IncLocal`；`ExpLocal`；`TransAmount`；`UserMark` |

## 6. 未解析计算事件

下列事件确认旧程序存在动态计算或自定义页脚，但 DFM 不包含处理器代码：

- `OnCalcFields`：6 处；处理器：`qry1CalcFields`、`GridDBQueryCalcFields`、`qryDataCalcFields`
- `OnGetFooterCellText`：3 处；处理器：`tlCategoryIncListGetFooterCellText`
- `OnGroupCalc`：2 处；处理器：`gridGroupCalc`
- `OnIsExistFooterCell`：6 处；处理器：`tlContractIsExistFooterCell`、`dxTreeListIsExistFooterCell`、`tlCategoryIncListIsExistFooterCell`

## 7. SQLite 查询投影规格

### 7.1 真相层与投影层

- 交易、账户分录、投资成交、费用、汇率快照和附件关系是可审计真相，写入规范化表。
- `FakeTransDate`、`Bala`、`IncLocal`、`ExpLocal`、`TransCheck`、`ProfitRate` 等展示或计算字段不得反向覆盖真相表；应由查询、窗口函数或应用层计算生成。
- 金额使用整数最小货币单位；数量、价格、汇率和比例使用明确精度的定点值，并在 Rust 领域层统一舍入口径。
- 报表筛选必须显式携带账簿、日期、账户、币种、标签和对象范围，不能依赖全局可变 SQL。

### 7.2 第一批稳定投影

| 投影 | 必要输出 | 用途 | 验证状态 |
| --- | --- | --- | --- |
| `v_ledger_entries` | 交易标识、实际/显示日期、类型、分类、账户、流入、流出、本币折算、标签、备注、对象、附件状态 | 财务记录、标签明细、账户收支 | 字段集合和三项求和已确认；折算公式待样例校准 |
| `v_account_transaction_running_balance` | 账户、交易顺序、发生额、手续费、余额 | 所有账户交易明细 | `Bala` 为计算字段已确认；同日排序和期初口径待校准 |
| `v_investment_position` | 对象、持仓量、成本、市值、仓位、行情价、盈亏、含费盈亏、收益率 | 证券、基金、贵金属、投资一览 | 字段和显示精度已确认；成本法与费用口径待校准 |
| `v_investment_realized_profit` | 日期、对象、交易类型、价格、数量、金额、盈亏、收益率、盈利合计、亏损合计 | 投资收益和历史盈亏 | 字段及页脚绑定已确认；收益率分母待校准 |
| `v_life_theme_transactions` | 标签、交易、流入、流出、账户、币种、备注 | 标签日常收支 | 流入/流出汇总已确认 |
| `v_life_theme_assets` | 标签、资产名称、金额、币种、本币金额 | 标签资产 | 合计汇总已确认；跨币种折算待校准 |

### 7.3 查询实现约束

1. 账户余额使用按稳定业务顺序执行的 SQLite 窗口函数；排序键至少包含业务日期、创建顺序和交易标识。
2. 转账、拆分行、手续费和对应账户分录在一个事务内提交，报表只读取已提交分录。
3. 本币折算必须读取交易时或报告基准日的汇率快照，并在投影结果中保留使用的汇率标识。
4. 投资成本、已实现盈亏、未实现盈亏和含费盈亏分别输出，不能只保留一个模糊的 `PAL` 字段。
5. 图表与表格共享同一查询结果 DTO，避免旧程序式的 Web 图表和网格各自重复计算。
6. 25 张报表先实现参数化仓储查询；只有稳定、复用且可测试的口径才固化为 SQLite 视图。

## 8. 验收样例要求

下一阶段应在 `test.mh8` 的可控副本中建立最小数据集，逐项记录旧程序结果：

- 同日多笔收支、转账和手续费后的余额顺序
- 两币种交易在交易日与报告日汇率下的本币金额
- 股票/基金买入、部分卖出、分红和费用后的成本及盈亏
- 标签同时关联流水与资产时的两类合计
- 空数据、跨年、隐藏账户和已删除/作废记录的报表边界

每个样例保存输入、筛选条件、表格结果、图表系列、页脚合计和导出结果；只有结果匹配后，相关公式才可从“待校准”升级为“已验证”。
