# 顶层导航实测记录

本文档记录当前对 `财智8` 顶层导航入口的实际页面观察结果，用于区分“仅从资源/配置推断存在”与“已拿到真实页面证据”的差别。

## 1. 已确认的顶层入口

从界面与快捷键配置可确认存在以下顶层入口：

- 财务数据
- 财务报表
- 财务分析
- 记账

## 2. 已拿到真实页面证据的入口

### 2.1 财务数据

证据：

- [data-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-page-observations.md)

当前已实测：

- 顶部当前显示 `财务数据`
- 左侧导航至少包含：
  - 概况
  - 财务记录
  - 投资一览
  - 标签
  - 账户中心
- 当前已明确可见 `账户中心` 页面及其账户类型分区

### 2.2 财务报表

证据：

- [report-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\report-page-observations.md)

当前已实测：

- 顶部当前显示 `财务报表`
- 左侧导航至少包含：
  - 日常收支类
  - 资产负债类
  - 投资类
- 当前已明确可见的报表项包括：
  - 日常收支表
  - 日常收支明细表
  - 账户日常收支表
  - 标签日常收支表
  - 两段时间收支对比表
  - 收支统计表
  - 收支走势图
  - 月平均收支表
  - 现金流表
  - 资产负债表
  - 可用资金表
  - 债权债务表
  - 月资产走势图

### 2.3 财务分析

证据：

- [analysis-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\analysis-page-observations.md)
- [runtime-execution-queue.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-execution-queue.md) 中 `RT-15-001` 至 `RT-15-042` 的运行态记录

当前已实测：

- 顶部当前显示 `财务分析`
- 左侧导航至少包含：
  - 财务预算
  - 财务诊断
  - 财务规划
  - 财务目标
- 财务预算已确认新增、分类选择、十二个月金额设置、实际支出导入、周期切换、信息修改、年度复制、删除和刷新后空状态。
- 财务诊断已确认输入页、资产性质设置、结果页及部分指标公式。
- 财务规划已确认家庭资料、收入、支出、资产、债务、保险、通胀、退休、教育、重大支出、资产购置和年度余额图。
- 财务目标已确认名称、日期、金额、账户绑定、必填校验、进度展示、修改/删除入口和删除后空状态。
- `计划提醒` 主菜单已确认包含 `财务日历 / 计划与提醒 / 限额提醒`，并已到达四类计划和四类限额提醒编辑器。

## 3. 记账入口实测

顶部 `记账` 是下拉命令中心，不是独立页面。一级菜单已实测为：

- 日常收支 `F1`
- 批量记账
- 批量转账
- 工资收入
- 存款
- 取款
- 转账 `F2`
- 借入
- 借出
- 物品买入
- 更多交易活动

`更多交易活动` 按业务域继续分组，当前截图可见调整、收支、银行存款、支付宝/微信钱包、信用卡、上市证券、开放式基金、货币基金、债券、银行理财、贵金属、外汇交易、融资融券、网贷投资、期货、贵金属 TD、外汇兑换、重大资产、物品和保险等入口。`调整` 的三级菜单进一步包含余额调整和持仓调整。

已进一步动态确认：

- `调整`：余额调整、持仓调整；前者打开 `TNewRecTransDlgFm`，后者打开 `TAdjustHeldDlgFm`。
- `收支`：日常收支、分拆收支、待摊费用、工资收入。
- `银行存款`：存款、取款、转账、利息收入、货币兑换；利息收入打开标题为 `资金利息收入` 的 `TInvestFeeDlgFm`，货币兑换打开 `TCurrChgXferDlgFm`。
- `支付宝、微信钱包`：充值、提现，两个方向复用 `TRechargeDlgFm`，由发起命令决定资金方向。
- `信用卡`：信用卡取现、信用卡还款；分别打开 `TCashCardDlgFm` 和 `TDrawalCardDlgFm`。
- `上市证券`：证券买入、证券卖出、新股申购、新股申购确认、送股、缩股、配股配债、现金红利、权证行权、放弃行权、债券到期、债转股、兑付债券利息、其它费用、利息收入。
- 上市证券菜单中的送股/缩股复用 `TStockDividDlgFm`，其它费用/利息收入复用 `TInvestFeeDlgFm`；权证、债券和债转股命令会调用其它静态业务域的共享窗体。
- `开放式基金`：开放式基金申购、赎回、新基金认购、认购确认、基金拆分、基金现金红利、分红再投资、转为开放式基金、转为货币基金、其它费用、利息收入。
- `货币基金`：货币基金申购、赎回、红利再投资、转为开放式基金、转为货币基金、其它费用、利息收入。
- 两组基金菜单共用 `TInvestFeeDlgFm`；两个转换方向分别复用 `TFundConvertDlgFm` 或 `TCurrFundConvertFm`，目标产品类型决定动态字段和计算策略。
- `债券`：债券买入、债券卖出、债券到期、债券提前兑取、债券利息。
- `银行理财`：银行理财产品申购、赎回、分红、其它费用、利息收入。
- 银行理财产品分红复用 `TNMarketBondInterestDlgFm` 并动态替换账户/产品标签；其它费用和利息收入复用投资公共窗体。
- `外汇交易`：外汇买卖、转账、其它费用、利息收入；对应菜单命令 ID 为 `211`、`212`、`214`、`215`，其中外汇买卖打开 `TCurrExchangeDlgFm`，转账打开 `TCashXferDlgFm`，后两项复用 `TInvestFeeDlgFm`。
- `贵金属`：贵金属买入、贵金属卖出、其它费用、利息收入；对应菜单命令 ID 为 `205`、`206`、`208`、`209`，买卖分别打开 `TGoldBuyDlgFm` 和 `TGoldSellDlgFm`，后两项复用 `TInvestFeeDlgFm`。
- 贵金属买卖都包含投资账户、资金账户、产品、单价、数量、手续费、总金额、标签、日期和备注；买入还提供更新产品及新增产品入口。
- `财智8 -> 资料管理 -> 贵金属` 打开产品/价格双列表；产品操作含修改、删除、查找、获取价格、价格整理、导出、打印，价格操作含修改、删除、导出、打印。
- 贵金属账户工作区操作菜单包含余额调整、持仓调整、添加贵金属价格、查看账户资料、导出、打印和设为软件首页；空账户下添加价格、导出和打印禁用。
- `贵金属TD` 账户专用记账菜单包含开仓 `980`、平仓 `981`、递延费 `983`、超期费 `984`、其它费用 `986`、利息收入 `987` 和转账 `988`。
- TD 工作区顶部操作包含余额调整、添加贵金属价格、贵金属TD品种设置、查看账户资料、导出、打印和设为软件首页；空账户下添加价格、导出和打印禁用，未出现现货账户的持仓调整。
- TD 工作区下部只有交易明细和历史盈亏两个页签；持仓范围菜单为当前持仓合约和所有交易过的合约，品种设置入口打开独立品种列表与编辑器。
- `期货` 账户专用记账菜单包含开仓 `980`、平仓 `981`、其它费用 `983`、利息收入 `984` 和转账 `985`；后 3 项分别复用投资费用与现金转账窗体。
- 期货工作区顶部操作包含余额调整、添加合约价格、期货品种设置、查看账户资料、导出、打印和设为软件首页；空账户下添加价格、导出和打印禁用，同样未出现持仓调整。
- 期货工作区下部为交易明细和历史盈亏，持仓范围为当前持仓合约和所有交易过的合约；在线更新窗体明确默认选择期货价格。
- `财智8 -> 资料管理 -> 期货合约` 打开合约/价格双列表；空合约状态下新增、修改和删除价格等依赖选择的命令禁用。期货品种设置另有内置品种列表及新增、修改、删除、导出和打印入口。
- `融资融券` 账户专用记账菜单包含融资买入 `984`、融券卖出 `985`、卖券还款 `986`、买券还券 `987`、批量直接还款 `988`、批量直接还券 `989`、利息返还 `991`、融资权益 `993`、融券权益 `994`、担保物买入 `995`、担保物卖出 `996`、担保物划入 `997` 和担保物划出 `998`。
- 运行时确认顶部菜单第 4/5 个偿还入口打开批量直接还款/还券窗体；单笔直接还款、直接还券和融资融券合约编辑从工作区中选定的具体合同对象进入，不能按同名菜单项合并为一个命令。
- 融资融券记账菜单的 `更多` 子菜单包含新股申购、申购确认、送股、配股配债、现金红利、其它费用、利息收入、转账和货币兑换，复用证券与投资公共能力。
- 融资融券工作区顶部操作包含余额调整、持仓调整、融资融券费率设置、证券费率设置、查看账户资料、导出、打印和设为软件首页；空账户下代码变更、添加股票价格、导出和打印禁用。
- 融资融券工作区下部为交易明细和历史盈亏，持仓范围为当前持有证券和所有交易过的证券；在线更新窗体默认选择股票收盘价。
- 外汇账户工作区的操作菜单包含持有外汇调整 `604`、添加外汇牌价 `924`、查看账户资料 `912`、导出 `914`、打印 `915` 和设为软件首页 `917`；零余额空账户下导出和打印禁用。
- 账户中心外汇账户行操作包含余额调整 `284`、修改账户 `286`、删除账户 `287`、关闭账户 `289`、隐藏账户 `290`、指定账户组 `292`、添加标签 `296` 和查看附件 `297`；删除会显示关联收支、转账及债权债务计划等数据的级联警告。
- `债权`：借出、预付、收回、提前收回、垫付、报销、债权坏账、待摊费用。
- `债务`：借入、预收、返还、提前返还、债务坏账。
- 借入/借出复用 `TNewDebtBorrowDlgFm`，提前收回/提前返还复用 `TPrepaymentFm`，债权坏账/债务坏账复用 `TDebtAdjustDlgFm`；业务方向由菜单命令决定。
- `重大资产`：重大资产买入、重大资产卖出、追加投资、资产投资收益、资产投资费用。
- `物品`：物品买入、物品卖出、物品价值变更。
- 重大资产账户工作区提供交易明细、市值管理、成本市值构成和资产概况四个页签；范围菜单区分当前持有资产和所有记录过的资产，账户记账菜单与顶部重大资产分组一致。
- 物品账户工作区提供交易明细和成本市值构成，顶部统计列为分类/名称、购买均价、数量、购买成本和市值。账户中心按物品过滤可定位空账户并执行永久删除。
- `资料管理 -> 家居物品` 打开 `TPracListFm`，上半区管理分类和物品主档，下半区管理按日价格；新增菜单分为物品和物品分类。
- `保险`：缴纳保费、保费返还、退保、保险分红。
- 新增账户类型中 `商业保险` 与 `社保` 是独立入口。商业保险采用四步向导；社保采用两步向导，第一页必须从人员主数据绑定参保人，第二页至少选择养老、工伤、失业、医疗、生育或住房公积金之一并录入独立记账日余额。
- 商业保险共享工作区提供交易明细、现金价值和账户概况页签；三页均已真实切换，现金价值页提供按日价值表、趋势图和增改删，账户概况聚合账户、保单、人员关系及状态。账户操作菜单提供余额调整、修改、删除、关闭、隐藏、账户组、标签和附件。
- 零余额 `Lzb-养老` 已动态创建并进入同一 `TSocialSecurityTransFm`：现金价值页受保费收支统计开关限制，概况按社保模式显示参保人、社保编码和地区；删除子账户后空账户组需独立删除，清理后两个名称均不再出现。
- 分拆收支打开 `TSplitIncExpDlgFm`，待摊费用打开 `TPrepaidExpensesIncExpDlgFm`，工资收入打开 `TPayrollIncomeDlgFm`。
- 债权债务交易明细中的上下文 `记账` 菜单先分为债权和债务；债权子菜单包含借出、预付、收回、提前收回、垫付、报销、债权坏账和待摊费用，报销打开 `TExpenseDlgFm`。
- 选择具体债权款项后会出现 `查看未报销记录`，打开 `TCostDetailsDlgFm` 展示日期、收支项目、金额、标签和备注。

证据：[bookkeeping-menu-open.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-menu-open.png)、[bookkeeping-more-transactions-menu.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-more-transactions-menu.png)、[bookkeeping-adjustment-submenu.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-adjustment-submenu.png)、[bookkeeping-bank-deposit-submenu.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-bank-deposit-submenu.png)、[bookkeeping-credit-card-submenu.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-credit-card-submenu.png)、[bookkeeping-more-transactions-popup-group20-selected.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-more-transactions-popup-group20-selected.png)、[bookkeeping-securities-popup.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-securities-popup.png)、[bookkeeping-open-fund-popup.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-open-fund-popup.png)、[bookkeeping-money-fund-popup.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-money-fund-popup.png)、[bookkeeping-bonds-popup.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-bonds-popup.png)、[bookkeeping-bank-wealth-popup.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-bank-wealth-popup.png)、[bookkeeping-group20-popup.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-group20-popup.png)、[bookkeeping-debt-popup.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\bookkeeping-debt-popup.png)、[claims-bookkeeping-menu.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\claims-bookkeeping-menu.png)、[claims-bookkeeping-claims-submenu.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\claims-bookkeeping-claims-submenu.png)。

保险与社保证据：[b13-insurance-account-type-dialog.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-insurance-account-type-dialog.png)、[b13-commercial-insurance-wizard-page1.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-commercial-insurance-wizard-page1.png)、[b13-insurance-cash-value-tab-verified.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-insurance-cash-value-tab-verified.png)、[b13-insurance-account-overview-verified.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-insurance-account-overview-verified.png)、[b13-social-wizard-page2-pension.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-social-wizard-page2-pension.png)、[b13-social-workspace-transactions.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-social-workspace-transactions.png)、[b13-social-account-overview.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-social-account-overview.png)、[b13-account-center-after-social-cleanup.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-account-center-after-social-cleanup.png)。

重大资产与家居物品证据：[b14-major-asset-workspace-bmw.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b14-major-asset-workspace-bmw.png)、[b14-major-asset-value-management.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b14-major-asset-value-management.png)、[b14-major-asset-cost-market-constituent.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b14-major-asset-cost-market-constituent.png)、[b14-item-account-after-create.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b14-item-account-after-create.png)、[b14-item-master-list.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b14-item-master-list.png)、[b14-account-center-after-item-delete.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b14-account-center-after-item-delete.png)。

## 4. 当前顶层导航认知

截至 2026-07-29，当前最合理的 UI 结构判断是：

- `财务报表`
  - 偏查询与统计中心
- `财务分析`
  - 偏预算、规划、诊断、目标中心
- `财务数据`
  - 已确认偏日常业务主数据与业务浏览中心
- `记账`
  - 已确认是覆盖普通收支、批量、转账、工资、存取款、借贷及专项资产交易的跨域快捷命令中心

## 5. 对 Rust 重构的意义

- 顶层导航不应设计成单一路由平铺菜单。
- 至少应保留四个一层工作区：
  - 数据
  - 报表
  - 分析
  - 记账
- 每个工作区下再挂自己的左侧子导航或内容面板。
- `记账` 不应实现成固定页面路由；应作为可搜索、可按业务域分组的命令面板，调度各领域的专用编辑器。
