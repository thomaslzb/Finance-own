# 财务数据页面实测记录

本文档记录对 `财务数据` 工作区的实际截图观察结果。

证据截图：

- [moneyhome-current.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\screenshots\moneyhome-current.png)

运行态补充证据：

- [runtime-window-tree-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-window-tree-evidence.md)

## 1. 页面顶部

- 顶部入口当前显示：`财务数据`
- 右侧当前可见操作：
  - 所有账户类型
  - 按账户类型查看
  - 新增账户组
  - 新增账户
  - 操作

## 2. 左侧数据导航

当前截图可直接确认以下左侧入口：

- 概况
- 财务记录
- 投资一览
- 标签
- 账户中心

## 3. 五个页面的运行态结果

### 3.1 概况

- 窗体：`TSoftIndexCenterForm`。
- 7 月收入 `24,228.50`、支出 `10,991.94`、结余 `13,236.56`。
- 资产数量 `5`、总负债 `1,444,074.57`、净资产 `7,091,459.48`。
- 收支对比区域提供收支、可用资金、债权债务、投资和资产构成入口；信用卡区域显示 `没有信用卡数据`。
- 证据：[B01-overview-current-state.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\B01-overview-current-state.png)。

### 3.2 财务记录

- 窗体：`TWasteBookFm`。
- 默认范围为 `全部记录`，日期为 `最近1月: 2026-06-29到2026-07-29`。
- 当前结果 `23` 条；流入 `249,277.84`、流出 `240,556.08`、差额 `8,721.76`。
- 列表可见日期、活动类型、流入、流出、资产账户、标签、备注、币种和附件状态。
- 记录范围可切换为 `仅收支记录`；切换后排除转账等非收支活动，列标题变为收入/支出，结果由 `23` 条变为 `13` 条，底部汇总同步重算。
- 查找支持日期、活动类型、流入、流出、资产账户、标签和备注；`查找下一个` 只移动当前选中行，`重新开始` 保留条件并重置查找游标。
- 筛选支持资产、活动类型、关键字、标签及金额的大于等于、小于等于和区间条件；条件会保留供再次编辑，`清空条件` 可一次恢复默认查询。
- 使用关键字 `Council Tax` 后只剩一条 `GBP 242.00` 支出，但底部流出为 `2,185.16`，说明行金额保留原币而汇总使用账本本位币折算。
- 清空筛选恢复同一 `23` 条记录后，流出从 `240,556.08` 变为 `240,556.07`，差额从 `8,721.76` 变为 `8,721.77`；原程序存在同查询重算的 `0.01` 漂移。
- `记录分组显示` 会增加列标题拖放区；`批量操作模式` 会增加逐行复选框，未选择时删除、设置标签和设置备注保持禁用。
- 选中转账后执行修改会打开专用 `TCashXferDlgFm`，加载转出/转入账户、金额、币种、手续费、标签、备注、日期和附件入口；关闭取消后账簿不写入。
- 2026-07-31 已真实保存 `Cash-CNY -> 顺德农行` 的 `50.00 CNY` 转账和来源账户 `1.00 CNY` 手续费。保存及冷启动后，来源余额为 `557.00`、目标余额为 `150.00`；来源流水显示流出 `51.00`，全局财务记录显示同一转账流入 `50.00`、流出 `51.00`，净资产减少 `1.00`。
- 2026-07-31 已真实保存 `顺德农行 -> Cash-CNY` 的 `4.00 CNY` 取款和来源账户 `1.00 CNY` 手续费。保存及冷启动后，来源余额为 `95.00`、目标余额为 `612.00`；全局财务记录显示同一取款流入 `4.00`、流出 `5.00`，净资产只减少手续费 `1.00`。
- 2026-07-31 已分别真实保存第三方钱包零手续费双向资金流：充值 `Cash-CNY 608.00 -> 606.00`、`微信钱包 2,986.44 -> 2,988.44`；提现 `微信钱包 2,986.44 -> 2,985.44`、`Cash-CNY 608.00 -> 609.00`。两个方向的全局记录都同时显示等额流入和流出，净资产不变且冷启动保持。同日本金 `1.00`、手续费 `0.10` 的双向样例确认：充值由 `Cash-CNY` 总减少 `1.10`、钱包只增加 `1.00`；提现由钱包总减少 `1.10`、Cash-CNY 只增加 `1.00`；两个方向净资产均减少 `0.10`，全局流入/流出均为 `1.00/1.10`。统一规则是资金发出侧承担手续费，接收侧只取得本金。充值手续费随后验证修改与删除：费用 `0.10 -> 0.20` 时钱包本金保持，Cash-CNY、CASH 分组和净资产只再减少 `0.10`；删除确认后测试行消失，钱包、来源账户、分组和净资产全部恢复基线，两个状态均通过冷启动。证据：[rt03-wallet-recharge-fee-wallet-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-wallet-recharge-fee-wallet-after-restart-sanitized.png)、[rt03-wallet-fee-lifecycle-cold-restart-modified-balances-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-wallet-fee-lifecycle-cold-restart-modified-balances-sanitized.png)、[rt03-wallet-fee-lifecycle-delete-confirmation-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-wallet-fee-lifecycle-delete-confirmation-sanitized.png)。
- 转入账户控件只写显示文本而未选定真实账户对象时提示 `请选择转入账户` 且不写入，证明账户选择必须保存稳定对象身份，不能把名称文本当作外键。
- 选中 `职业工资` 收入后执行修改会打开 `TIncExpDlgFm` 的 `日常收入` 变体，而不是工资专用窗体；字段为收支项目、金额、收支账户、标签、日期、备注和附件。
- 选中 `教育培训` 支出后执行修改会打开同一 `TIncExpDlgFm` 的 `日常支出` 变体，内部复用 `TIncExpEditFrame`；两次标题栏关闭均取消草稿，账簿长度和最后写入时间不变。
- 从空白 `日常收支` 草稿选择 `其它收入` 后标题切换为 `日常收入`；保存 `Cash-CNY +3.00 CNY` 后余额为 `611.00`、CASH 分组为 `9,498.70`，全局记录只有流入 `3.00`，冷启动后保持。
- 从相同基线选择 `教育培训` 后标题切换为 `日常支出`；保存 `Cash-CNY 2.00 CNY` 后余额为 `606.00`、CASH 分组为 `9,493.70`，全局记录只有流出 `2.00`，冷启动后保持。两个方向都输入正金额。
- `替换收支项目` 打开 `TImportCategoryDlgFm`，流程为查询候选、选择记录、选择目标项目和确定替换；本轮只验证初始与取消。
- 导出格式实际提供网页和 Excel。取消导出后旧程序错误提示 `导出成功`，但未生成对应文件；打印进入系统打印对话框并可正常取消。
- 证据：[RT-03-034-financial-records-current-state.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-03-034-financial-records-current-state.png)。
- 菜单与模式证据：[financial-records-actions-menu.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\financial-records-actions-menu.png)、[financial-records-batch-actions-menu.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\financial-records-batch-actions-menu.png)。
- 查找与筛选证据：[RT-03-012-find-field-options-f4.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-03-012-find-field-options-f4.png)、[RT-03-010-filter-keyword-result.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-03-010-filter-keyword-result.png)。
- 同币种转账证据：[b03-transfer-balances-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\b03-transfer-balances-after-restart-sanitized.png)、[b03-transfer-source-ledger-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\b03-transfer-source-ledger-after-restart-sanitized.png)、[b03-transfer-financial-record-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\b03-transfer-financial-record-after-restart-sanitized.png)。
- 取款证据：[rt03-withdraw-balances-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-withdraw-balances-after-restart-sanitized.png)、[rt03-withdraw-global-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-withdraw-global-after-restart-sanitized.png)。
- 货币兑换已真实保存 `Cash-CNY 9.00 CNY -> Cash-GBP 1.00 GBP`：余额分别从 `608.00 / 908.30` 变为 `599.00 / 909.30`，账户组人民币折算值从 `9,495.70` 变为 `9,495.74`，冷启动后保持。全局记录为单条流入 `1.00`、流出 `9.00`，币种列为空；旧页脚直接累加不同币种名义金额。失败校验复测进一步确认，换出和换入账户必须绑定稳定账户 ID，仅向选择器写入 `Cash-GBP` 显示文字仍会提示 `请选择换入账户`；确认与保存并继续共用同一校验链，依次约束两侧账户存在、账户不同、币种不同以及两侧金额大于零。旧版同币种提示文案含义错误，Rust 版应保留拒绝规则并改为明确的“换出与换入账户币种必须不同”。证据：[b06-balances-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\b06-balances-after-restart-sanitized.png)、[b06-financial-record-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\b06-financial-record-after-restart-sanitized.png)、[RT-06-001-20260802T091603+0800.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-06-001-20260802T091603+0800.json)。
- 银行资金利息收入已真实保存 `Cash-CNY +2.00 CNY`：余额和 CASH 分组人民币折算值均增加 `2.00`，全局记录为单条“利息收入”流入且冷启动保持。新增 CNY 行币种列为空，而同页 GBP 利息行显示 `英镑 GBP`，说明本位币文字可隐藏但领域事实不能丢失币种。证据：[rt07-bank-interest-balances-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt07-bank-interest-balances-after-restart-sanitized.png)、[rt07-bank-interest-financial-record-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt07-bank-interest-financial-record-after-restart-sanitized.png)。
- 外汇入口其它费用已真实保存 `Cash-CNY -1.25 CNY`：余额和 CASH 分组人民币折算值均减少 `1.25`，全局记录为单条“其它费用”流出且冷启动保持。该行币种显示为空且没有可见外汇来源，证明交易事实必须独立保存币种和来源上下文。证据：[rt07-foreign-expense-balances-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt07-foreign-expense-balances-after-restart-sanitized.png)、[rt07-foreign-expense-financial-record-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt07-foreign-expense-financial-record-after-restart-sanitized.png)。
- 外汇账户 `CodexFX-1706` 的有数据工作区已补充实测：持仓统计显示美元 `0.88 / 6.7894 / 5.97 CNY`、人民币 `94.00 / 1.0000 / 94.00 CNY` 和合计 `99.97 CNY`；构成圆环图图例直接复用 `美元 5.97 / 人民币 94.00`。交易明细显示 `2026-08-01 / 100.00 CNY / 余额调整` 与 `2026-08-02 / 6.00 CNY -> 0.88 USD / 0.1473 / 外汇买卖`，并确认当前币种/所有交易、12 类日期范围、四类记账入口和修改删除/导出打印菜单。证据：[RT06-foreign-workspace-populated-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT06-foreign-workspace-populated-notes.md)、[rt06-workspace-wide-transaction-detail-20260802.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt06-workspace-wide-transaction-detail-20260802.png)、[rt06-workspace-wide-fx-composition-20260802.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt06-workspace-wide-fx-composition-20260802.png)。
- 收支编辑证据：[RT-03-016-daily-income-dialog.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-03-016-daily-income-dialog.png)、[RT-03-016-daily-expense-dialog.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-03-016-daily-expense-dialog.png)。
- 日常收支真实保存证据：[rt03-daily-income-balances-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-daily-income-balances-after-restart-sanitized.png)、[rt03-daily-income-global-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-daily-income-global-after-restart-sanitized.png)、[rt03-daily-expense-balances-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-daily-expense-balances-after-restart-sanitized.png)、[rt03-daily-expense-global-after-restart-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-daily-expense-global-after-restart-sanitized.png)。

### 3.2.0 资料管理统一宿主

- 窗体 `TInformationDlgFm` 是基础资料编辑器的统一路由宿主，不直接维护业务实体。运行时主菜单可见 `11` 个入口：收支项目、人员与机构、上市证券、开放式基金、重大资产、家居物品、证券交易费率、其它金融产品、币种与汇率、存款利率、常用备注；菜单中另有 `4` 个分隔符。
- 金融产品宿主左侧实际提供 `10` 类内部路由：上市证券、开放式基金、货币基金、债券、贵金属、银行理财产品、期货合约、期货品种、贵金属 TD 品种和证券交易费率。即使部分类型没有独立显示在主菜单，仍必须作为可到达的资料类型建模。
- 收支项目默认进入支出分类，可切换收入分类；人员与机构默认进入家庭成员，可切换往来人员和机构；存款利率提供人民币与外币分组。左侧切换会替换或刷新当前子编辑器，而不是在宿主内复制一套表单。
- “其它金融产品”当前运行时默认打开 `TCurrFundsListFm / 货币基金列表`。该入口应记录为旧版兼容路由别名，Rust 版必须用明确的资料类型 ID 和路由表表达，不能从菜单文字推断实体类型。
- 收支项目切换到收入后，同会话关闭再打开仍回到支出；完全退出并冷启动后同样回到支出。说明宿主临时选中类型不持久化，默认类型由入口命令决定。
- 宿主关闭立即返回账户中心，没有宿主级保存按钮或隐式业务写入。新增、修改、删除、引用保护和事务边界均属于当前装载的子编辑器；宿主只负责入口解析、类型选择、子页面生命周期和返回导航。
- 验证结束后已关闭 MoneyHome8、归档两次退出产生的恢复文件并精确还原 `test.mh8`；最终长度 `18,669,568`，SHA-256 为 `D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC`。
- 证据：[RT02-information-host-routing-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-information-host-routing-notes.md)、[RT-02-017-20260801T124926+0800.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-02-017-20260801T124926+0800.json)、[rt02-information-host-main-menu-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-information-host-main-menu-20260801.png)、[rt02-information-host-security-10425994-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-information-host-security-10425994-20260801.png)、[rt02-information-host-category-cold-restart-default-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-information-host-category-cold-restart-default-20260801.png)。

### 3.2.0.1 账户选择器

- `TmwSelectAccountDrop` 是工资、转账、钱包、保险和其它业务编辑器共享的账户引用组件。工资收款账户配置显示单账户、多账户、搜索、过滤和 `[新增账户]`；转账的转出/转入账户只显示单账户列表，手续费账户额外提供 `<无>`。
- 工资单账户页从真实候选选择 `Cash-CNY` 后，下拉立即关闭并回填外层字段。显示文字只用于呈现，提交仍必须携带稳定账户 ID 和候选版本。
- 多账户页点击 `Cash-CNY` 后动态出现账户金额编辑器和行级确定，底部还有选择器级确定；金额为 `0.00` 时提示 `请输入账户金额`。目标模型应返回 `AccountAllocation` 明细，而不是无金额的账户 ID 集合。
- 过滤输入会自动切换到搜索页；输入 `Cash` 只显示 `Cash-CNY`，无匹配文本显示空结果。点击外层控件会关闭下拉且不改外层已选值，再次打开恢复单账户初态。
- 转出和转入候选集合相同，均包含 `Cash-CNY`、`Cash-USD`、`Cash-GBP` 和银行账户，没有自动排除当前来源或按 CNY 过滤外币。选择 `Cash-USD` 后目标账户回填，但转账币种仍为 CNY，说明跨字段业务规则属于外层命令。
- 转入账户的 `[新增账户]` 打开 `TNewAcctTypeDlgFm / 新增资产账户`，取消后回到原选择器并保留转账草稿；手续费账户允许 `<无>` 且当前配置不显示内联新增。
- 验证结束后关闭应用、归档会话期间创建的恢复副本，最终 `test.mh8` 已恢复长度 `18,669,568` 和 SHA-256 `D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC`。
- 证据：[RT02-account-selector-runtime-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-account-selector-runtime-notes.md)、[RT-02-019-20260801T132229+0800.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-02-019-20260801T132229+0800.json)、[rt02-account-selector-payroll-multi-zero-validation-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-account-selector-payroll-multi-zero-validation-20260801.png)、[rt02-account-selector-payroll-search-cash-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-account-selector-payroll-search-cash-20260801.png)、[rt02-account-selector-transfer-target-usd-selected-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-account-selector-transfer-target-usd-selected-20260801.png)。

### 3.2.0.2 收支项目选择器

- `TmwSelectCategoryDrop` 在 `TIncExpDlgFm / 日常收支` 的收支项目字段中真实到达。空白草稿默认打开支出页；支出页创建 `22` 个候选控件，首行把父项 `交通` 与子项 `公共交通`、`汽车` 并排显示。收入页创建 `12` 个候选控件。
- 输入 `工资` 自动切到搜索页，只返回 `职业工资 / 收入`；输入 `其它` 同时返回 `其它收入 / 收入` 和 `其它支出 / 支出`；输入不存在分类返回空结果。搜索跨方向执行，结果必须携带稳定 ID、方向和层级信息。
- 选择 `其它收入` 后父窗切换为 `日常收入`，选择 `其它支出` 后切换为 `日常支出`。重新打开选择器会按当前分类方向进入对应页并清空过滤文字。
- 在收入选择器中切到支出页但不选择，再点击外层金额字段，下拉关闭且原 `其它收入` 草稿保持。页签、搜索和高亮属于选择器临时状态，不得提前提交宿主变化。
- 从收入页点击 `[新增]` 打开 `TEditCategoryFm`，旧窗却仍默认勾选支出；取消后返回收入页并保留原选择。这是方向上下文丢失缺陷，Rust 版必须继承当前方向或显式确认变化。
- `[收支项目管理]` 在该宿主中隐藏，隐藏句柄点击无导航效果；可见宿主、返回状态、键盘和真实自绘层级项选择仍待验证。
- 本轮没有保存交易或分类。会话恢复副本已归档，最终 `test.mh8` 精确恢复到长度 `18,669,568` 和 SHA-256 `D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC`。
- 证据：[RT02-category-selector-runtime-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-category-selector-runtime-notes.md)、[RT-02-020-20260801T135226+0800.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-02-020-20260801T135226+0800.json)、[rt02-category-selector-search-other-both-directions-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-category-selector-search-other-both-directions-20260801.png)、[rt02-category-selector-inline-new-income-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-category-selector-inline-new-income-20260801.png)、[rt02-category-selector-search-expense-selected-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-category-selector-search-expense-selected-20260801.png)。

### 3.2.0.3 标签选择器

- `TmwSelectTagDrop` 已在 `TIncExpDlgFm / 日常收支` 的标签字段真实到达，并与账户中心外层 `TSelectTagDlgFm` 的既有证据交叉校准。
- 无标签基线显示“没有标签，请点击下方新增标签”，只提供受控新增和确定；有数据时每个标签以独立 `TmwTagControl` 候选显示，支持多选。
- 过滤 `TagB` 只显示匹配候选，清空后恢复全部且原选择保持；`NoSuchTag` 返回空候选区，不回退全部标签或创建占位对象。
- 两个标签同时选中后，确定把 `CodexSelTagA-1409;CodexSelTagB-1409` 回填父级草稿；取消全部选中并确定可返回明确空集合。旧分号文本只是显示格式，目标数据应是有序稳定标签引用集合。
- 取消第二项后点击父级其它字段，旧下拉在失焦时自动提交剩余单标签到父级草稿，但不保存交易。合成 Escape 不关闭下拉，真实键盘仍待补测。
- 内联新增空名称提示 `请输入标签名称`。分号输入一次创建两个标签主数据，但父级只自动回填批次第一项；第二项已存在于候选，需要再次显式选中。目标实现必须明确批量创建后的默认选择策略。
- 内联新增草稿标题栏关闭不写入，并返回原候选。关闭整个日常收支父窗后重新打开，已成功创建的两个标签仍存在，证明标签主数据提交独立于交易或账户关系提交。
- 旧程序退出后的业务副本和恢复文件均已归档；最终 `test.mh8` 精确恢复到长度 `18,669,568` 和 SHA-256 `D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC`，源恢复文件和进程均为 `0`。
- 证据：[RT02-tag-selector-runtime-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-tag-selector-runtime-notes.md)、[RT-02-021-20260801T142902+0800.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-02-021-20260801T142902+0800.json)、[rt02-021-multiselect-two-tags-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-021-multiselect-two-tags-20260801.png)、[rt02-021-daily-host-after-inline-create-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-021-daily-host-after-inline-create-20260801.png)、[rt02-021-reopen-after-parent-cancel-master-persists-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-021-reopen-after-parent-cancel-master-persists-20260801.png)。

### 3.2.0.4 第三方储值账户

- 第三方储值子菜单包含支付宝、微信钱包、财付通和其它储值账户；其它储值仍复用 `TNewAcctWizardThirdDepositsDlgFm`，旧窗体标题不能代表真实提供方类型。
- 两页向导先维护名称、币种、所有者、备注和账户组，再维护创建日期、余额和可选资金来源。空名称提示 `请输入账户名称`，返回和前进保持完整草稿。
- `CodexRT41Wallet / 12.34 CNY / 资金来源<无>` 保存后旧客户端报 `Cannot perform this operation on a closed dataset` 并退出，但冷启动确认账户和一条余额调整已持久化；财务记录 `2189 -> 2190`，资产和净资产各增加 `12.34`，负债不变。
- `TThirdDepositsAcctDlgFm` 可编辑名称、所有者、备注和创建日期，币种只读且不提供余额直接编辑。标题栏关闭丢弃草稿；保存 `CodexRT41WalletM / RT41M` 后金额仍为 `12.34`，没有新增财务记录。
- 本轮退出后已归档创建崩溃态与资料修改态，并把 `test.mh8` 和 `~$test` 恢复到操作前长度及 SHA256，MoneyHome8 进程为 `0`。
- 证据：[RT02-third-party-stored-value-lifecycle-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-third-party-stored-value-lifecycle-notes.md)、[RT-02-041-20260802T053900+0800.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-02-041-20260802T053900+0800.json)、[rt41-cold-start-after-create.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt41-cold-start-after-create.png)、[rt41-third-party-editor-initial.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt41-third-party-editor-initial.png)。

### 3.2.1 收支项目基础资料

- 窗体：列表 `TCategoryListFm`，编辑器 `TEditCategoryFm`。
- 列表默认显示支出项目，可切换收入项目并搜索；一级项目行提供“新增二级项目”，二级项目与父项在同一行分栏展示。
- 编辑器默认支出方向。空名称保存提示 `请输入收支项目名称`；输入已有支出项目 `交通` 提示 `已有相同名称的收支项目存在，请重新输入收支项目名称`，两种失败均未形成有效新项目。
- 切换到收入方向后，父级候选只包含收入项目，如 `投资收益`、`利息收入`、`职业工资`，没有混入支出项目。
- 通过真实字符输入创建一级支出项目 `CodexParent0801`，再从筛选候选绑定该父级并创建 `CodexChild0801`；列表立即显示父子层级。
- `保存并新添` 保存 `CodexBatchA0801` 后编辑器保持打开、名称清空且方向仍为支出；随后普通保存 `CodexBatchB0801`。冷启动搜索 `Codex` 可见四个项目及父子关系。
- 操作菜单默认勾选“按使用量排序”，此时“调整收支项目顺序”禁用；切换“按自定义排序”后两个排序模式互斥，顺序命令启用。将 `CodexLifeB0801` 跨越多个一级项目拖动并确定后，冷启动仍保持 `CodexLifeA0801、旅游费用、食物、餐费、CodexLifeB0801` 的顺序和自定义模式。
- 打开“显示系统类别”后，支出方向自绘分类控件由 `46` 增至 `57`，新增 `投资亏损、报销支出、保险支出、债务利息支出、资产费用、投资杂费、购物费用、坏账支出、对账支出、利息支出、手续费`；关闭后恢复 `46`。当前基线无隐藏支出项目，“显示隐藏类别”开关前后均为 `46`，因此具体隐藏/恢复仍待独立样例。
- 成功冷启动账簿副本 SHA-256 为 `77DE1782E62DA230FF49EBE9529534EC73F34AD3E9A120F88EC313B025E8AAF4`；验证结束后 `test.mh8` 已恢复运行前长度 `18,669,568` 和 SHA-256 `D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC`。
- 证据：[RT02-category-crud-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-category-crud-notes.md)、[RT02-category-lifecycle-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-category-lifecycle-notes.md)、[rt02-category-parent-child-batch-cold-restart-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-category-parent-child-batch-cold-restart-20260801.png)、[rt02-category-lifecycle-cold-restart-custom-order-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-category-lifecycle-cold-restart-custom-order-20260801.png)。

### 3.2.2 常用备注

- 窗体：列表 `TFmIncExpCaptionForm`，编辑器 `TIncExpCapionDlgFm / 备选说明`。
- 列表使用 `TMHTreeList` 展示备注文本，提供新增、修改、删除、导出和打印；编辑器只有多行备注内容和保存。
- 空内容保存提示 `请输入常用备注`。真实保存 `CodexMemo0801` 后列表立即追加，修改为 `CodexMemoEdited0801` 后原行更新。
- 删除提示 `您确定删除此备注吗？`；选择否记录保持，选择是后删除，冷启动仍为原有五条记录。
- 常用备注属于交易输入辅助主数据，不产生余额或分录；历史交易必须保存备注快照，不能随主档修改或删除变化。
- 证据：[RT03-common-caption-lifecycle-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT03-common-caption-lifecycle-notes.md)、[rt03-common-caption-after-save-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-common-caption-after-save-20260801.png)、[rt03-common-caption-delete-confirmation-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-common-caption-delete-confirmation-20260801.png)、[rt03-common-caption-cold-restart-after-delete-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt03-common-caption-cold-restart-after-delete-20260801.png)。

### 3.2.3 币种与汇率

- 窗体：`TCurrListFm / 币种与汇率`，嵌入 `TInformationDlgFm / 资料管理`；入口菜单命令 ID 为 `56`。
- 上半区展示本币标记、货币名称、英文缩写和对人民币牌价；当前可见 `CNY、USD、HKD、CAD、EUR、JPY、CHF`，人民币为本币且牌价为 `1.0000`。
- 选择美元后，下半区显示日期化 `USD/CNY` 历史，列为日期、两个币种、比较符、报价方式和四位汇率。首条原值为 `2026-07-29 / 6.7894`。
- 修改窗口预载日期、美元、人民币、`USD/CNY` 和原汇率；改为 `6.7895` 保存后，上半区美元当前牌价和下半区历史行即时同步，冷启动后仍保持。
- 删除提示 `您确定删除该外汇汇率吗？`；选择否保持记录，选择是后 `2026-07-29` 行消失，`2026-07-28 / 6.7829` 成为首条历史，上半区美元当前牌价同步回退为 `6.7829`。
- 勾选 `按日期显示全部汇率` 后显示独立日期控件和指定日期的跨币种列表；默认 `2026-08-01` 当前为空。取消后恢复选中币种的完整时间序列。
- 新增汇率对话框默认当天，要求两个币种和汇率；币种选择器没有形成动态绑定，因此关闭且未保存。运行时处理器补充确认汇率格式实际为 `0.0000`、最大长度 `12`，“报价方式”只读标签由有序币种 ID 对派生；保存依次校验日期、两侧币种、币种不同和正汇率，并按 `rate * 10000` 写入整数。上半区菜单精确顺序为修改、删除、设置为本币、获取牌价、价格整理、分类显示、导出、打印，分类显示子项依次为所有、现钞、现汇；静态 `查找` 动作未绑定到当前菜单。
- 当前页面没有新增币种入口。初始 CNY 和选中 CHF 时，币种修改、删除均禁用；`TCurrDlg / 货币` 仅有静态编辑器证据，真实可编辑币种来源仍待确认。
- 选择 CHF 执行设置为本币后没有确认框或独立保存步骤，CHF 立即获得本币勾选；正常退出并冷启动后仍保持。列标题和数值继续使用“对人民币牌价”，证明账簿本币与人民币报价锚点相互独立。本轮未验证账户、报表、预算、规划或历史估值的重算影响。
- 修改关闭态 SHA-256 为 `2F3FD6E2E1AC66BBC2C4CF79F4EF39ACD83E6A06C302CD5E9B03F6F71FA0D9A8`，删除关闭态为 `A96736760B26C468DE4B7CE7C34B437ACB6CC82C5EF9BC04A599A0AC0C3F4EA2`；最终 `test.mh8` 恢复运行前长度和 SHA-256。
- 证据：[RT02-currency-rate-lifecycle-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-currency-rate-lifecycle-notes.md)、[RT02-currency-master-local-currency-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-currency-master-local-currency-notes.md)、[rt02-currency-master-after-set-local-command-20260802.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-currency-master-after-set-local-command-20260802.png)、[rt02-currency-master-cold-restart-chf-local-20260802.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-currency-master-cold-restart-chf-local-20260802.png)、[rt02-currency-usd-rate-after-modify-67895-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-currency-usd-rate-after-modify-67895-20260801.png)、[rt02-currency-after-delete-confirmed-rate-fallback-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-currency-after-delete-confirmed-rate-fallback-20260801.png)。

### 3.2.4 存款利率

- 窗体：`TRateFm / 存款利率`，嵌入 `TInformationDlgFm / 资料管理`；入口菜单命令 ID 为 `57`。
- 人民币表按储蓄类型、储蓄期间和年利率展示，只有年利率可编辑；外币表按币种和活期、一个月、三个月、半年、一年、两年、七天通知存款展示。
- 人民币活期年利率从 `0.35` 提交为 `0.36` 后列表即时刷新，无独立保存步骤，冷启动仍保持 `0.36`。
- “更新利率”打开 `TOnlineGetDataFm` 并只选择存款利率；任务完成后记录批次计数与 `2026-08-01` 更新时间，返回页后人民币活期刷新为 `0.10`，当前可见外币矩阵未变化。
- 历史行情页只覆盖股票、港股、美股、开放式基金、贵金属、期货和外汇，不提供存款利率或证券交易费率历史下载。
- 运行时反汇编确认：编辑变化只设置脏标记；校验只判断文本能否解析为数字，失败静默恢复旧值；提交把浮点输入乘 `10000` 后取整写入。该证据没有证明负数、零和超大值的真实页面结果，仍需后续动态输入校准。
- 证据：[RT02-deposit-rate-lifecycle-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-deposit-rate-lifecycle-notes.md)、[rt02-deposit-rate-rmb-after-clean-036-commit-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-deposit-rate-rmb-after-clean-036-commit-20260801.png)、[rt02-deposit-rate-rmb-cold-restart-036-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-deposit-rate-rmb-cold-restart-036-20260801.png)、[rt02-deposit-rate-update-result-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-deposit-rate-update-result-20260801.png)、[rt02-deposit-rate-history-update-tab-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt02-deposit-rate-history-update-tab-20260801.png)。
- 静态补强证据：[RT02-deposit-rate-validation-static-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-deposit-rate-validation-static-notes.md)、[RT-02-037-20260802T060300+0800.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-02-037-20260802T060300+0800.json)。

### 3.2.5 证券交易费率

- 窗体：`TFeeSetForm / 证券交易费率`，嵌入管理金融产品工作区；A 股和 B 股各有独立表格及更新、导出、打印菜单。
- A 股按九类市场/证券模板维护买卖印花税、佣金、最低佣金、附加费和过户费；B 股按沪市/深市维护印花税、佣金、最低佣金、结算费、结算费上限和交易规费。列标题明确区分 `%`、`‰` 和固定金额。
- 沪市股票卖出印花税从 `0.1` 改为 `0.11`、沪市 B 股结算费从 `0.05` 改为 `0.06` 后均即时提交，正常关闭并冷启动后保持。
- 在线更新默认只选择证券交易费率，日志显示成功更新 `11` 条；返回页面后两个手工值被覆盖回 `0.1` 和 `0.05`，深市 B 股买卖最低佣金从 `0.05` 更新为 `5`。
- 页面声明全局模板只由新建账户继承，不修改已有账户。安装目录 `mhlink.mdb` 的写入时间在更新窗口内变化，恢复 `test.mh8` 后更新时间仍保留，说明全局参考数据或更新元数据至少部分位于账簿之外。
- 证据：[RT08-security-fee-lifecycle-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT08-security-fee-lifecycle-notes.md)、[rt08-security-fee-cold-restart-manual-values-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt08-security-fee-cold-restart-manual-values-20260801.png)、[rt08-security-fee-update-result-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt08-security-fee-update-result-20260801.png)、[rt08-security-fee-page-after-online-update-20260801.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt08-security-fee-page-after-online-update-20260801.png)。

### 3.2.6 人员与机构基础资料

- 窗体：列表 `TPersonListFm`，编辑器 `TPersonDlg`；默认进入家庭成员，可切换往来人员和机构。
- 编辑器默认男、生日未启用。类型菜单固定为家庭成员、往来人员、机构；机构模式隐藏性别和生日，只保留名称、联系方式和地址。
- 生日启用后可选公历或农历。公历默认当前日期；农历使用年份、12 个月份和 30 个日期。生日类型和原始年月日必须同时保存。
- 空名称提示 `请输入名称`；标题栏关闭唯一草稿零写入；同一家庭成员的完全同名新增提示 `该名称已存在，请重新输入`。
- `CodexRT34Person` 已真实新增并修改：女性、农历 `1990-05-06` 保存后，再更新为男性、联系方式 `13900139034`、地址 `Shenzhen RT34 Updated`、农历 `1991-06-07`；列表即时刷新，冷启动后完整保持。
- 三类列表已分别取证：家庭成员和往来人员显示名称、性别、生日类型、出生日期、联系方式、地址，机构只显示名称、联系方式、地址；新增按钮文案随类别变化，切换类别会清空搜索。
- 搜索按当前显示字段即时做子串匹配，名称 `Shaw`、联系方式 `esavings` 和地址 `Hornchurc` 均可命中机构；空结果仍可新增，但操作按钮不产生依赖当前行的菜单。
- 新增机构 `CodexRT35Shared` 后，再新增同名往来人员被提示 `该名称已存在，请重新输入`，证明三类共享账簿级名称空间；改名 `CodexRT35Contact` 后保存成功。
- 隐藏记录默认从列表排除；开启“显示隐藏人员和机构”后名称显示 `已隐藏 | ...`，菜单变为“取消隐藏”。未引用往来人员删除前按类型确认并可物理删除；已引用机构 `Halifax` 在确认前直接提示 `该人员或机构已被使用，无法删除`。
- 导出默认 `机构列表.htm` 和网页类型，但取消保存后旧程序仍误报 `导出成功`，且未发现新 HTML 文件；打印进入系统打印对话框，取消后无打印作业。
- 运行结束后业务副本已归档，`test.mh8` 恢复长度 `18,669,568` 和 SHA256 `D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC`；既有 `~$test` 保留未删除。
- 证据：[RT02-person-editor-lifecycle-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-person-editor-lifecycle-notes.md)、[RT02-person-list-lifecycle-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-person-list-lifecycle-notes.md)、[rt34-person-type-menu-popup.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt34-person-type-menu-popup.png)、[rt34-person-create-filled-lunar.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt34-person-create-filled-lunar.png)、[rt35-person-cross-type-duplicate-validation.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt35-person-cross-type-duplicate-validation.png)、[rt35-person-show-hidden-contact.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt35-person-show-hidden-contact.png)、[rt35-person-reference-delete-confirmation.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\rt35-person-reference-delete-confirmation.png)。

### 3.3 投资一览

- 窗体：`TInvestmentListFm`。
- 当前按投资账户分组，至少可见 `Trading212 - ISA`、`Trading212-Invest`、`国泰君安`。
- 投入成本 `4,775,044.14`、当前市值 `6,993,903.35`、浮动盈亏 `2,218,859.21`，三者算术关系一致。
- 页面提供 `投资构成图`、`更新行情数据` 和 `操作` 入口。
- 证据：[RT-07-005-investment-list-current-state.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-07-005-investment-list-current-state.png)。

### 3.4 标签

- 窗体：`TLifeThemeFm`。
- 当前显示 `没有标签`，并说明标签用于按项目归类财务记录。
- 空状态中央和顶部均提供 `新增标签` 入口。
- 点击新增后打开 `TNewThemeDlgFm` 模态对话框；输入框支持用半角分号分隔多个标签，示例为 `标签1;标签2;标签3`。
- 对话框没有独立取消按钮；标题栏关闭可取消，父页面恢复空状态，`test.mh8` 大小和最后写入时间不变。
- `RT-02-018` 已补充完整主数据生命周期：空名称提示 `请输入标签名称`，精确重复提示 `标签名称已存在，请重新输入`；单标签保存、改名取消/保存、无引用删除否/是均已实测。
- 一次输入 `CodexTagMultiA0801;CodexTagMultiB0801` 会创建两个独立标签。隐藏标签后默认返回空态，开启 `显示隐藏标签` 后以禁止图标显示，菜单动态变为 `取消隐藏`；标签状态和查看偏好均通过冷启动。
- 有数据态固定 `<无>` 位于首项，下方有 `交易记录`、`资产账户` 两个页签。查找与筛选支持资产、活动类型、关键词、日期、金额和标签条件；筛选激活后提供 `放弃筛选`。
- 批量菜单包含快速加入、移除和转移；无选择时提示 `请选择记录`。`导入记录到标签` 页面先查询交易，再选择目标标签执行设置，本轮未提交既有交易关系。
- 标签交易导出默认 `标签_2026-08-01.htm`，标签列表导出默认 `标签列表.htm`；两个保存对话框取消后旧程序仍误报 `导出成功`。打印进入系统打印对话框并已取消。
- 完整证据见 [RT02-tag-page-lifecycle-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-tag-page-lifecycle-notes.md)。
- 为验证排序，在指定测试账簿中临时创建 `CodexTagOrderA0801`、`CodexTagOrderC0801`、`CodexTagOrderB0801`。标签页显示 `<无>、A、C、B`，`调整标签顺序` 对话框只列真实标签，初始顺序为 `A -> C -> B`。
- 拖动视觉预览可形成 `C -> B -> A`，标题栏关闭并重开恢复 `A -> C -> B`；`确定` 无二次确认且可关闭窗口。2026-08-02 又对首个 `TmwTagControl` 发送完整按下、连续移动和释放消息链，视觉顺序再次变为 `C -> B -> A`，但确定后标签页、同会话重开和冷启动均为 `A -> C -> B`。说明组件位置与内部排序草稿是不同状态，不能把视觉移动当作持久化成功。
- 当前活动桌面为 `LockApp`，受保护物理拖动在输入前发现坐标未命中 MoneyHome8 并拒绝，因此仍不能据此判定真实鼠标拖放保存失败。三个临时标签只保存在归档会话态，验证结束后 `test.mh8` 和 `~$test` 均精确恢复。完整证据见 [RT02-tag-order-lifecycle-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-tag-order-lifecycle-notes.md) 和 [RT02-tag-order-message-drag-boundary-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-tag-order-message-drag-boundary-notes.md)。
- 证据：[RT-02-018-tags-current-state.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-02-018-tags-current-state.png)。
- 对话框证据：[RT-02-018-new-tag-dialog-initial.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-02-018-new-tag-dialog-initial.png)。

### 3.5 账户中心

- 窗体：`TAccountManagerFm`。
- 当前筛选为 `所有账户类型`，分组为 `按账户类型查看`。
- 现金组小计 `9,487.88`，活期（卡折）组小计 `978,715.76`。
- 资产 `8,535,534.04`、负债 `1,444,074.57`、净资产 `7,091,459.47`，资产减负债与净资产一致。
- `新增账户组` 打开 `TEditAccountGroupFm`；父窗包含账户组名、`详细资料...` 和 `确定`，空名称时确定按钮仍为启用状态。
- `详细资料...` 打开 `TAcctDetailDlg` 二级模态窗；账户组模式显示联系电话、联系方式、密码和备注，父窗名称为空时只读名称显示为 `未命名`。
- 空名称点击确定会弹出 `请输入账户组名称`，关闭警告后保留编辑器，不会自动创建名为 `未命名` 的账户组。
- 有效名称与详细资料可成功保存；密码输入后以星号遮罩。二级详细资料窗确定时文件不写入，父账户组确定后 `test.mh8` 才发生写入。
- 精确输入既有组名 `CASH` 会提示 `已有相同名称的账户组存在，请重新输入账户组名称`，并保持零写入；前后带空格的 ` CASH ` 却能保存，重新打开时显示为 `CASH`，证明旧程序缺少名称规范化并会产生视觉重名。
- 把空格组修改为 `Codex-Group-Edit-20260801` 后，联系电话、联系方式、遮罩密码和备注在同会话及冷启动均完整回填；父级提交点和二级草稿边界保持不变。
- 查看方式菜单支持 `按账户类型查看`、`按自定义分组查看`，并提供已结清债权债务、到期、隐藏和注销账户显示开关。
- 自定义分组视图显示组级汇总，空账户组为 `0.00`；组选中后提供修改账户组、删除账户组和添加账户。
- 左侧账户树右键的 `设置[自定义]显示` 打开 `TCustomNavigationAcctDlgFm`。树支持组/账户层级复选、半选、全选、反选、上移、下移和确定；首项上移禁用，移动到第二位后可上移恢复。
- 真实取消勾选 `Halifax / H-Current` 并把 `Halifax` 下移后，确定无二次确认，左侧导航立即变为 `Other UK Bank -> Halifax` 且隐藏 `H-Current`；资产、负债、净资产仍为 `8,540,196.43 / 1,444,589.25 / 7,095,607.18`。冷启动保持；重新勾选并上移后再次冷启动恢复。
- 反选和全选只修改对话框草稿，标题栏关闭不提交。修改态副本 SHA-256 为 `B6A44CD5A1F24F1529F40336574C37F1BBA94B2D769ECC56833FE28CCAA9779D`；最终测试账簿已精确恢复基线。证据：[RT02-custom-navigation-lifecycle-notes.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT02-custom-navigation-lifecycle-notes.md)。
- “添加账户”打开名称/余额多选表。把 `Cash-CNY 608.00` 加入新组后，新组为 `608.00`，原 `CASH` 从 `9,495.70` 变为 `8,887.70`，全局资产、负债和净资产不变，冷启动后关系保持。
- 删除账户组前明确确认永久删除组；若组内有账户，只解除账户与组的关联，不删除账户。
- 本轮创建的 `Codex验证组_20260729_0901` 已在验证后删除，页面不再显示该组。
- 新增账户类型中的贵金属分为 `现货贵金属` 和 `贵金属TD`；两类均已完成账户创建、页面观察和临时账户删除。
- 现货贵金属两步向导包含账户资料、固定币种、账户组、日期以及账户自身余额或其它资金账户来源；零余额临时账户创建后自动进入贵金属工作区。
- 贵金属账户工作区显示持仓统计和交易明细、市值构成和变动、历史盈亏三个页签；空账户下添加价格、导出和打印禁用。
- 查看账户资料展示账户、资金来源、账户组、标签、附件及开户联系资料；修改编辑器出现完整账户名称被读取为 `zi` 的异常，本轮未保存。
- 临时账户删除确认明确覆盖相关收支、转账和理财计划，确认后账户中心及侧栏不再显示该账户；Jet 文件长度增长不能替代业务清理验证。
- 既有非零账户 `Cash-CNY 608.00` 的永久删除已补充完整前后对账：选择否零写入；确认后全历史记录从 `2,189` 降至 `2,180`，移除流入 `26,845.50`、流出 `30,708.00`，对手账户和资产负债汇总同步重算，净资产增加 `3,862.50` 并通过冷启动。删除影响不能用目标账户当前余额或其列表内 9 行合计推导。
- 现金开户两步向导已完成独立动态闭环。第一页默认 `我的现金 / 人民币 CNY / 所有者<无> / 账户组<无>`，第二页默认当前业务日和 `0.00`；空名称和既有 `Cash-CNY` 都在下一步前阻断。`CodexCashCancel-1509 / 12.34` 在上一步往返中保持，标题栏关闭后同名可重新使用。直接提交 `CodexCashDirect-1512 / 12.34` 后旧程序先报 `closed dataset`，再报 `C0000025` 并退出；冷启动仍回读账户、备注和余额，资产与净资产各增加 `12.34`，负债不变，证明故障发生在提交后的刷新或生命周期阶段而非业务回滚。
- 活期一本通三页向导已完成组合提交。空组名、既有 `CASH`、空子账户名和既有 `Cash-CNY` 均在对应步骤阻断；第三页关闭后组名可重新使用。成功提交后冷启动显示 `CodexCurrentPass-1537` 组及 `CodexCurrentSub-1537` 子账户，小计和余额均为 `7.89`；子账户流水只有一条 `余额调整` 流入 `7.89`，记录数 `1`，资产和净资产各增加 `7.89`。旧程序仍在提交后刷新阶段报 `closed dataset` 与 `C0000025`，目标组合命令必须原子且幂等。
- 普通活期两页向导已完成独立提交。第一页默认 `我的活期 / 人民币 CNY / 所有者<无> / 备注空 / 账户组<无>`，第二页默认当前业务日、`0.00` 和资金来源 `<无>`；空名称和既有 `Cash-CNY` 均在下一步前阻断，草稿往返保持，第二页关闭后名称可重新使用。`CodexCurrent-1604 / 23.45` 提交后立即进入无账户组投影且没有崩溃；冷启动后只有一条 `余额调整` 流入 `23.45`，余额 `23.45`、记录数 `1`，资产和净资产各增加 `23.45`、负债不变。
- 定期一本通四页向导已完成默认整存整取分支提交。默认条款为 `1个月 / 0.25%`，存期改为 `3个月` 后自动建议 `0.80%`，存期单位菜单提供年/月，自动续存可勾选。成功提交 `CodexDepositPass-1625 / CodexDepositSub-1627 / 1200.00 CNY` 后，组小计和子账户余额均为 `1200.00`；存单列表显示起存日 `2026-08-01`、到期日 `2026-11-01`、到期本息 `1202.40`，交易明细只有一条余额调整流入 `1200.00`。冷启动后全部条款和计算投影保持，资产和净资产各增加 `1200.00`、负债不变。
- `Cash-CNY` 账户附件已完成全生命周期：空态管理窗、标准文件选择、文本预览、受管副本 `test\Account\23\account-attachment-probe.txt`、系统打开、打开目录、动态附件文件菜单、添加冷启动、删除确认否/是和删除冷启动。源文件与副本 SHA-256 一致；删除最后附件会清理整个空 `test` 受管目录。旧版同一会话账户行仍显示 `1个附件`，重启才修正。
- `Cash-CNY` 修改编辑器已验证名称、日期、只读币种、所有者、备注和附件入口。空名称提示 `请输入账户名称`，改为 `Cash-GBP` 提示 `已有相同名称账户`，均不写入。保存 `Codex-Cash-CNY-Edit` 和备注后账户按名称重新排序，余额、组小计和资产负债汇总不变；同会话和冷启动重新打开均完整回填。
- 贵金属 TD 两步向导在账户资料外配置每万元交易手续费和资金来源；零余额账户创建后仍停留账户中心，点击账户行进入专用工作区。
- TD 工作区上部显示合约手数、保证金、市值、占比、浮动盈亏、均价、收盘价和收益率，下部只有交易明细与历史盈亏；范围可切换当前持仓合约和所有交易过的合约。
- TD 记账菜单包含开仓、平仓、递延费、超期费、其它费用、利息收入和转账；所有编辑器均已到达并以取消结束。
- TD 品种设置默认列出 `Ag`、`Au` 和 `mAu`，展示报价/交易单位、每手数量和保证金比例，并提供新增、修改、删除、导出和打印。
- TD 账户概况不显示现货开户机构和联系人区，账户编辑器正确加载完整临时账户名称；共享行情窗口仍默认选择贵金属价格，实际 TD 行情映射尚待验证。
- TD 临时账户删除后主窗口恢复启用、账户中心不再显示该名称；删除后账簿长度为 `18,743,296` 字节，仍只作为写入证据而非逻辑清理证明。
- 期货两步向导包含固定人民币账户资料，以及日期、账户余额和开户机构；没有 TD 的每万元手续费与独立资金来源账户字段。
- 期货工作区上部按合约显示手数、保证金、市值、占比、浮动盈亏、均价、收盘价和收益率，下部为交易明细与历史盈亏；范围可切换当前持仓合约和所有交易过的合约。
- 期货记账菜单包含开仓、平仓、其它费用、利息收入和转账；开仓按品种、方向和到期年月录入，平仓选择已有合约，本轮所有表单均以取消结束。
- 期货品种列表已有内置数据，字段包括合约乘数、手续费数值与单位、保证金比例和交易所；期货合约页将合约目录与日价格分为上下两张表，当前账簿为空。
- 期货账户顶部操作包含余额调整、添加合约价格、期货品种设置、查看账户资料、导出、打印和设为软件首页；空持仓下添加价格、导出和打印禁用。
- 期货共享行情窗口明确默认勾选 `期货价格`；账户概况与编辑器正确往返完整临时账户名称。
- 期货临时账户永久删除后主窗口恢复启用、账户中心名称匹配数为零；删除后账簿长度为 `18,767,872` 字节，仍不能用物理长度代替业务清理与关系校验。
- 融资融券两步向导固定人民币，并分别录入融资年利率与融券年利率；零余额临时账户创建后可进入专用工作区，账户概况与编辑器正确往返完整名称。
- 融资融券工作区按证券或合同展示持仓数量、持仓成本、市值、占比、浮动/交易盈亏、均价、保本价、收盘价和收益率，并汇总担保物市值、融资负债、融券负债、可用资金和资产总值。
- 融资融券记账菜单已打开融资买入、融券卖出、卖券还款、买券还券、批量直接还款、批量直接还券、利息还款、融资权益、融券权益、担保物买入/卖出/划入/划出，以及其它费用、利息收入、转账和货币兑换；本轮均以取消结束。
- 融资与融券交易表单分别保存合同号、合同年利率和分项费用；偿还表单选择具体合同并显示偿还本金或数量与利息，批量表单按合同逐行录入。
- 担保物买卖使用信用账户内证券交易字段，担保物划入/划出则同时选择融资融券账户与普通证券账户、证券和数量，证明两者的数据流不同。
- 顶部操作包含余额调整、持仓调整、融资融券费率设置、证券费率设置、账户资料、导出、打印和设为首页；当前两个费率命令都打开同一按市场与证券类型维护分项费率的表格。
- 持仓范围可切换当前持有证券与所有交易过的证券；历史盈亏页显示日期、名称、活动类型、价格、数量、交易金额、已实现盈亏和盈亏比例，在线更新默认选择股票收盘价。
- 使用最小融资合同 `FM-CODEX-20260730-1` 和融券合同 `SM-CODEX-20260730-1` 已动态打开直接还款、直接还券与合同编辑：默认还款金额为未还金额 `1.00`，默认还券数量为未还数量 `1`，返还利息均为 `0.00`，合同编辑加载年利率 `1.00` 和证券 `002594 比亚迪`；三窗均关闭未保存。临时账户删除后保存退出状态副本，并将 `test.mh8` 恢复为运行前长度 `18,669,568` 字节和 SHA-256 `D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC`。
- 批量直接还款复测重新保存未结融资合同 `FM-BATCH-20260731-1`，工作区和重启后均显示融资负债 `-1.00`；但批量窗体在重启前后都没有列出该合同。`F2` 可激活空白合同行，空行提交提示“请选择合约并输入还款金额”且不写入。该路径证明旧版候选解析与工作区合同投影不一致，Rust 必须按稳定账户和合同状态查询候选；本轮没有伪造成功还款，账簿最终恢复原始 SHA-256。
- 账户类型选择窗明确提供 `商业保险` 与 `社保` 两个独立入口。商业保险使用四步向导，依次录入保险类别、账户资料、保单条款与投保关系、缴费计划与提醒策略。
- 零金额商业保险临时账户创建后进入 `TSocialSecurityTransFm` 共享工作区：上部列表显示名称、余额和备注，下部包含交易明细、现金价值、账户概况三个页签，底部汇总现金价值、累计保费、累计返还和记录数。
- 商业保险账户操作菜单包含余额调整、修改、删除、关闭、隐藏、账户组、标签和附件；账户编辑器正确加载完整名称、保单条款、投保关系、保险期间和统计口径，取消后不写入账簿。
- 现金价值页已通过真实 `TmwPageControlTabs` 切换到达：左侧按日期显示现金价值，右侧显示价值趋势图，新账户有开户日 `0.00` 初始快照，添加/修改/删除均可见且选中初始行时启用。
- 现金价值的添加命令打开 `TInsureCashValueEditDlgFm`，字段为日期和现金价值；在已有开户日 `0.00` 行时同日添加 `8.00`，未提示重复且仍只有一行，证明同日新增采用覆盖更新。修改为 `9.00` 后，快照表、上部账户余额和趋势图同步刷新。
- 删除唯一的 `2026-07-30 / 11.00` 快照时没有确认框，行立即消失且图表归零，但账户余额和交易页现金价值汇总在当前会话错误显示 `1.00`；正常退出并重开后快照仍为空、图表仍为零，余额和现金价值汇总却回到 `11.00`。保险交易、缴费 `10.00`、领取 `0.00` 和记录数 `1` 始终未变。脱敏截图与删除前后副本指纹已保存在 B13 证据目录，现有 `~$test` 恢复文件未触碰，因此只确认跨读模型缺陷，不臆测具体数据库根因。
- 多日期复测新增 `2026-07-31 / 13.00` 后，列表按日期降序显示 `13.00`、`11.00`。删除最新值的当前会话正确回退到 `2026-07-30 / 11.00`，余额、交易页汇总和图表一致；重开后被删行仍未恢复，表格和图表仍为 `11.00`，但账户余额和交易页汇总错误回到 `13.00`。这进一步确认故障位于重启投影重建，而非快照行删除失败。
- 同一两日期样例删除较早的 `2026-07-30 / 11.00` 时也没有确认框；当前会话及重启后都只保留 `2026-07-31 / 13.00`，账户余额、交易页汇总和图表稳定为 `13.00`，保险交易及缴费/领取统计不变。旧程序删除缺陷因此集中在被删行参与当前值时。
- 历史/未来日期样例新增 `2026-07-29 / 7.00` 和 `2026-08-01 / 15.00` 后，列表按日期降序展示且趋势图包含全部数据点；在 `2026-07-31` 当前会话中，余额和交易页现金价值汇总仍为最近已生效的 `11.00`。重开后三条明细继续存在，但旧程序余额和汇总错误归零，证明完整历史序列与按查询日投影是不同读模型。
- 金额边界样例确认负数 `-1` 和空值都会被旧程序无提示保存为 `0.00`；人民币 `1.234` 保存为 `1.23`、`1.235` 保存为 `1.24`。十一位整数金额发生控件截断和浮点进位，而 `9,999,999,999.99` 能在现金价值页、交易汇总、账户中心及重启后保持精确；保险交易和缴费/领取统计始终不变。
- 非零开户样例填写投保金额 `100.00`、已缴保费 `10.00`、年缴 `10.00`、无缴费账户和仅提醒；完成后生成一条缴费 `10.00` 的“余额调整”，现金价值初始为 `0.00`。现金价值改为 `9.00` 后，交易行、缴费总额 `10.00`、领取总额 `0.00` 和记录数 `1` 保持不变。
- 独立缴费样例创建零已缴保费保单 `B13Policy0730`，再从支付账户选择器内联创建期初 `100.00` 的现金账户 `B13PayCash`。保存保费 `10.00` 后，保险侧活动为 `缴纳保费 | B13PayCash`、缴费总额 `10.00`、现金价值 `0.00`；现金侧活动为 `缴纳保费 | B13Policy0730`，余额由 `100.00` 变为 `90.00`。正常关闭并重新打开后结果仍存在，随后已恢复测试库基线。
- 同一保单返还 `4.00` 后，保险侧活动为 `保费返还 | 我的现金`，缴费总额仍为 `10.00`、领取总额变为 `4.00`、记录数为 `2`、现金价值和保单余额仍为 `0.00`；零期初的“我的现金”新增 `4.00` 流入，活动为 `保费返还 | B13Policy0730`，余额为 `4.00`。正常关闭后保留成功账簿副本，并已恢复测试库基线。
- 同一保单分红 `2.00` 后，保险侧活动为 `保险分红 | B13DividendCash`，缴费总额仍为 `10.00`、领取总额变为 `2.00`、记录数为 `2`、现金价值和保单余额仍为 `0.00`；零期初领取账户新增 `2.00` 流入，财务记录也投影活动类型“保险分红”和账户关系 `B13Policy0730 -> B13DividendCash`。正常关闭后保留成功账簿副本，并已恢复测试库基线。
- 同一保单退保 `5.00` 且保持“同时终止保险账户”勾选后，编辑器无二次确认直接保存；零期初 `B13SurrenderCash` 收到 `5.00`，`B13PayCash` 保持 `90.00`，财务记录投影“退保”和 `B13Policy0730 -> B13SurrenderCash`。保单从活动账户列表移除，但终止后的保险工作区下方仍短暂显示保存前缴费行和旧汇总，证明旧程序存在跨组件刷新缺陷；活动 UI 不能证明旧库内部是否保留终止记录。
- 同额对照取消“同时终止保险账户”后，退保 `5.00` 仍新增 `退保 | B13SurrenderKeepCash` 领取行，缴费总额保持 `10.00`、领取总额变为 `5.00`、记录数变为 `2`、现金价值保持 `0.00`；`B13Policy0730` 继续显示并保持选中，交易和汇总立即刷新。因保存后桌面进入系统锁屏，本轮未重新拍摄到账账户余额和财务记录页，不将这两个交叉投影标记为独立通过。
- 账户概况页已真实到达，聚合账户名称、类型、币种、所有者、备注、保险机构、保单号、险种、三类保险关系人、投保金额、保险期间、账户组、标签、附件、终止状态和保费统计口径。
- 第二个临时商业保险账户永久删除后名称从账户中心消失，主窗口恢复启用；账簿长度从 `18,837,504` 增至 `18,862,080` 字节，说明 Jet 物理长度仍不能代替逻辑清理证明。
- 社保开户第一页包含参保人、社会保障号码、城市和“保费计入收支统计”；直接写入文本仍触发 `请选择参保人`，人员下拉则真实列出 `LHM`、`Lzb`、`Qrd`，选择 `Lzb` 后通过校验，证明必须绑定人员对象而不是仅保存显示名称。
- 社保第二页已动态到达：包含记账日期，以及养老、工伤、失业、医疗、生育和住房公积金六类独立选择，且至少选择一项；勾选养老后出现独立“记账日余额 0.00”。完成后创建 `Lzb的社保账户组` 和 `Lzb-养老`，组与子账户余额均为 `0.00`。
- `Lzb-养老` 进入同一个 `TSocialSecurityTransFm` 共享工作区，上部按项目展示名称、余额和备注，下部提供交易明细、现金价值和账户概况；交易空状态汇总现金价值、缴费总额、领取总额和记录数均为零。
- 社保现金价值页提示只有将保费作为收支统计时才能单独管理现金价值；账户概况显示保险种类“养老（社保）”、参保人、社保编码、地区、账户组和统计口径，修改入口打开按社保字段裁剪的 `TInsureAcctDlgFm`，取消后不写入账簿。
- 商业保险缴费计划已完成代表性动态校准：仅提醒计划进入今日提醒，执行禁用、跳过启用，跳过单期实例不生成交易；绑定 `Cash-CNY` 的 `1.00` 固定账户计划生成可执行自动计划但创建时不扣款，手工执行打开类型化缴费草稿，入账后现金余额 `608.00 -> 607.00`、资金记录数 `9 -> 10`，保险侧新增缴费 `1.00`、累计保费 `1.00`、记录数 `1`、现金价值保持 `0.00`。中央列表对保单派生计划禁用直接修改和删除；保单工作区独立修改窗已把两缴费年度的年缴 `1.00` 改为半年缴 `1.01`，列表重算为每 `6` 月、`2026-08-03..2028-02-03`，执行草稿同步为 `1.01`。关闭未入账草稿并重启后首期已自动入账，`Cash-CNY=606.99`、保险累计保费 `1.01`、下次日期 `2027-02-03`，但账户中心短暂仍显示旧余额 `608.00`。
- 四类限额提醒已完成真实动态校准：统一列表列为类别、提醒条件和生效，新建默认生效且信用卡规则停用跨冷启动保持。`Cash-CNY=608.00` 对下限 `609.00` 显示低 `1.00` 元；证券 `000001 平安银行` 对下限 `0.0100` 触发，基金未越界不触发。限额告警的执行和跳过均禁用；证券规则删除后当前告警立即消失并跨冷启动保持。证券编辑器/告警保留四位小数而列表显示两位，目标数据模型必须保留领域精度。
- 社保工作区记账菜单仍复用缴纳保费、保费返还、退保和保险分红四项。删除 `Lzb-养老` 会级联提示相关收支、转账和财务计划，但最后一个子账户删除后空账户组不会自动清理；独立删除空组后两个名称在账户中心匹配数均为零。
- `H-Current` 的账户概况已真实打开 `TEdtAcctGrpDlgFm / 修改所属账户组`。初始所属组为 `Halifax`；选择 `CASH` 后关闭，概况仍为 `Halifax`。重新选择并确定后，概况与左侧账户树立即显示 `CASH`，同会话重开和冷启动保持；余额 `795.57`、交易数 `558`、开户银行和资产/负债/净资产不变。证据：[rt02-account-group-dialog-initial.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\rt02-account-group-dialog-initial.png)、[rt02-account-group-overview-after-cancel.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\rt02-account-group-overview-after-cancel.png)、[rt02-account-group-overview-after-save.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\rt02-account-group-overview-after-save.png)、[rt02-account-group-cold-start-shell.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\rt02-account-group-cold-start-shell.png)。
- 依次关闭详细资料窗和账户组窗后，父页面恢复，`test.mh8` 大小和最后写入时间不变。
- 证据：[RT-02-002-account-center-current-state.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\RT-02-002-account-center-current-state.png)。
- 账户组证据：[account-group-detail-dialog-initial.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\account-group-detail-dialog-initial.png)。
- 贵金属账户证据：[b11-account-center-gold-created.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-account-center-gold-created.png)、[b11-gold-account-workspace.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-gold-account-workspace.png)、[b11-gold-account-delete-confirmation.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-gold-account-delete-confirmation.png)。
- 贵金属 TD 证据：[b11-td-wizard-page1.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-td-wizard-page1.png)、[b11-td-account-workspace2.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-td-account-workspace2.png)、[b11-td-bookkeeping-menu.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-td-bookkeeping-menu.png)、[b11-td-goods-list.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-td-goods-list.png)、[b11-td-account-delete-confirmation.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-td-account-delete-confirmation.png)。
- 期货证据：[b11-futures-wizard.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-futures-wizard.png)、[b11-futures-account-workspace.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-futures-account-workspace.png)、[b11-futures-open-dialog.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-futures-open-dialog.png)、[b11-futures-goods-list.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-futures-goods-list.png)、[b11-futures-contract-list.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-futures-contract-list.png)、[b11-futures-account-delete-confirmation.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b11-futures-account-delete-confirmation.png)。
- 融资融券证据：[b12-margin-wizard-page2.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b12-margin-wizard-page2.png)、[b12-margin-account-workspace.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b12-margin-account-workspace.png)、[b12-margin-financing-buy-dialog.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b12-margin-financing-buy-dialog.png)、[b12-margin-short-selling-dialog.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b12-margin-short-selling-dialog.png)、[b12-margin-collateral-in-dialog.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b12-margin-collateral-in-dialog.png)、[b12-margin-account-delete-confirmation.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b12-margin-account-delete-confirmation.png)。
- 保险与社保证据：[b13-insurance-account-type-dialog.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-insurance-account-type-dialog.png)、[b13-commercial-insurance-wizard-page1.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-commercial-insurance-wizard-page1.png)、[b13-insurance-account-editor.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-insurance-account-editor.png)、[b13-insurance-cash-value-tab-verified.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-insurance-cash-value-tab-verified.png)、[b13-insurance-account-overview-verified.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-insurance-account-overview-verified.png)、[b13-social-person-selector.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-social-person-selector.png)、[b13-social-wizard-page2-pension.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-social-wizard-page2-pension.png)、[b13-social-workspace-transactions.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-social-workspace-transactions.png)、[b13-social-account-overview.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-social-account-overview.png)、[b13-account-center-after-social-cleanup.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\b13-account-center-after-social-cleanup.png)。

- 现金价值真实写入证据：[b13-cash-calibration-value-after-same-day-add-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\b13-cash-calibration-value-after-same-day-add-sanitized.png)、[b13-cash-calibration-value-after-modify-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\b13-cash-calibration-value-after-modify-sanitized.png)、[b13-cash-calibration-transaction-after-value-modify-sanitized.png](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\artifacts\runtime-validation\screenshots\b13-cash-calibration-transaction-after-value-modify-sanitized.png)。

## 4. 当前可确认结论

- `财务数据` 不是单页，而是一个以左侧导航切换业务数据页面的工作区。
- 目前至少可以确认，它覆盖：
  - 概况
  - 财务记录
  - 投资一览
  - 标签
  - 账户中心
- 这说明在产品信息架构上，`财务数据` 更接近“日常业务浏览中心”，而不是报表或分析中心。
- 2026-07-29 已通过左侧导航实际进入全部五个页面，并由真实 Delphi 内容窗体、UI 自动化树和 `PrintWindow` 截图交叉确认。
- 五个页面均可从同一工作区原位切换；旧窗体实例会保留在自动化树中，因此运行态工具必须以当前可见内容区为准，不能仅按根节点名称取第一个匹配项。
- 只执行页面导航时，`test.mh8` 大小保持 `18,669,568` 字节，但最后写入时间推进到 `2026-07-29 02:14:21`；这只能证明原程序存在会话或界面状态写入，不能解释为业务数据改变。
- 概况净资产 `7,091,459.48` 与账户中心净资产 `7,091,459.47` 相差 `0.01`，原程序存在跨页面舍入或聚合路径差异。

## 5. 对 Rust 重构的意义

- `财务数据` 应作为单独的一层工作区存在。
- 其内部至少需要以下二级页面容器：
  - Overview
  - Transactions
  - InvestmentOverview
  - Tags
  - AccountCenter
- 五个页面都可以作为首批只读查询投影实现，其中账户中心和财务记录优先提供可复用查询 DTO。
- 概况、账户中心、投资一览和财务记录不得各自在 UI 中重复计算金额；应共享领域查询服务、估值快照和金额舍入策略。
- 标签需要作为交易关系实体处理，删除前必须检查历史引用，不能只实现为可任意物理删除的字典项。
- 一次输入多个标签时，分隔、裁剪、重复校验和写入必须作为一个领域命令处理，并在单事务中全部成功或全部回滚。
- 账户组和详细资料应组成同一个编辑草稿；二级窗确认只更新草稿，最终由父窗一次事务提交，任意层取消都不得留下部分写入。
- 账户组名称必填校验必须在业务写入前执行；校验失败后保留完整草稿供原位修正。
- 详细资料窗必须按账户或账户组上下文切换字段；密码等敏感字段需要遮罩展示、受保护存储和日志脱敏。
- 删除账户组必须删除组及其专属详细资料、清除账户关联，但保留账户；这些写入需要在单事务中完成。
- 永久删除账户必须先读取完整关系图形成影响快照，再原子处理关联事实和对手关系，并从剩余事实重建账户、分组、资产负债和全历史投影；隐藏和注销不得复用该命令。
- 附件元数据、业务关系和受管文件是三个一致性边界；添加采用暂存复制与哈希校验，删除采用最后引用检查，账户行计数、动态菜单、预览、备份和启动审计必须读取同一附件提交版本。
- 账户普通资料修改使用稳定账户 ID 和乐观版本原位更新；规范化名称唯一索引与领域校验共同阻止空值和重名，成功后跨页面刷新但不得触碰余额事实与历史关系。
- 账户类型投影和自定义分组投影必须共享同一余额查询、估值快照与底部总计服务。
- 财务记录的范围、筛选、查找、分组、批量模式、导出和打印必须共享同一不可变查询快照；查找只维护游标，不得暗中改变筛选集合。
- 普通收入和普通支出应复用同一收支编辑组件，由明确的交易方向上下文切换标题、金额语义和余额影响；不能仅根据 `职业工资` 等收支项目名称选择专用编辑器。
- 收支字段组件只编辑父级草稿，最终由父窗口统一校验并原子提交交易头、账户分录、项目、标签、备注和附件关系；父窗取消时整体丢弃。
- 交易行需要同时承载原币金额和本位币折算金额；汇总采用本位币时必须保留汇率快照并在 UI 或明细中可追踪。
- 同一查询 DTO 和汇率快照必须产生确定可复现的列表与汇总，筛选往返不得改变相同记录集合的金额结果。
- 批量删除、设置标签和设置备注必须显式进入批量模式，并按选择状态控制命令；批量写入必须单事务提交。
- 导出取消必须返回明确的 `cancelled` 结果，不得复刻旧程序“未生成文件却提示成功”的行为。
- 商业保险开户应以一个草稿聚合账户资料、保单条款、投保关系和缴费计划；最终确认时原子提交，取消或任一步校验失败不得留下半成品账户。已缴保费必须保存为来源明确的开户保险事件，不能等同于现金价值；无资金账户时不得虚构资金分录。
- 保险工作区可复用统一页面外壳，但交易、现金价值和账户概况必须读取同一保单与估值快照；现金价值跨日期保留历史，同一账户同一日期执行可审计 upsert，且不得改变保险交易和缴费/领取汇总。
- 选择资金账户缴纳保费时，保险事件和资金账户流出必须原子提交并以稳定 ID 关联；累计保费增加不能自动改变现金价值，保险侧和资金侧应能互相导航到关联对象。
- 社保参保关系必须引用人员 ID，并把养老、工伤、失业、医疗、生育和住房公积金保存为可独立记账、查询和汇总的子账户。
- 社保开户应原子创建自动账户组、选中子账户和期初余额；删除最后一个子账户后是保留还是删除空组必须成为明确产品规则，不能留下不可见或不可管理的孤立组。
- 账户中心的账户类型过滤已实测可直接筛选 `物品`。空物品账户会显示在 `无账户组` 下，行操作提供余额调整、修改、永久删除、注销、隐藏、账户组、标签和附件；永久删除前明确警告关联收支、转账和财务计划也会被删除。
- 重大资产工作区把持仓统计、交易明细、市值历史、成本/市值构成和账户概况组合在同一选择上下文中；物品工作区复用持仓统计、交易明细和构成图，但使用独立主档、分类、数量和价格历史。
- `RT-14-001` 的 `1.00 CNY` 无支付账户买入已确认：当前成本和市值均为 `1.00`、累计收益为 `0.00`，交易明细与同日初始市值自动生成，资产和净资产各增加 `1.00`、负债不变。零金额买入也能保存，账户中心可见且冷启动保留，但“当前持有资产”不显示该对象。
- `RT-14-001` 的支付账户买入已确认：`CodexAssetCash-0802 / 10.00 CNY` 稳定绑定 `Cash-CNY` 后，现金从 `608.00` 降至 `598.00`，资产成本和市值均为 `10.00`，全账簿资产、负债和净资产不变。选择器默认“单账户”页虽显示没有可用账户，但搜索 `Cash` 可返回并绑定 `Cash-CNY`。
- `RT-14-002` 的全额卖出已确认：`1.50` 所得结转 `1.00` 成本后，当前成本和市值均为 `0.00`、累计收益为 `0.50`；当前持有范围排除该资产，所有记录范围和冷启动仍保留资产及两条交易。同日市值从买入初始 `1.00` 覆盖为单个当前有效 `0.00`；零金额和清仓资产仍显示在构成图例中但不贡献扇区。
- `RT-14-002` 的绑定账户部分卖出已确认：从成本/市值 `10.00/10.00` 的资产结转成本 `4.00`、取得 `6.00`，收入账户稳定绑定 `Cash-CNY` 且按比例减少市值后，剩余成本/市值均为 `6.00`，现金从 `598.00` 增至 `604.00`，全账簿资产和净资产各增加 `2.00`，负债不变；财务记录显示重大资产卖出流入 `6.00`，冷启动保持。
- `RT-14-004` 的追加投资已确认：工作区当前选中行决定资产绑定；`0.00` 无校验保存为零值交易；`2.00` 勾选同时追加市值后成本和市值均增至 `3.00`，资产和净资产各增加 `2.00`；再追加 `3.00` 并取消市值联动后成本增至 `6.00`，市值历史、账户中心余额、资产和净资产保持不变。无支付账户时 `Cash-CNY` 不变。另一归档态绑定 `Cash-CNY` 追加 `5.00` 后，资产成本/市值 `6.00 -> 11.00`、现金 `604.00 -> 599.00`，全账簿资产、负债和净资产不变。随后新增贷款融资 `2.00`，资产成本/市值 `11.00 -> 13.00`、全账簿资产和负债各增加 `2.00`、现金与净资产不变，并创建 `Lzb的普通应付款` 及资产关系，冷启动保持。另一个受控样例先独立借入 `1.00` 创建未关联的 `Lzb的普通应付款`，再用于顺德房产追加投资；成本和市值各增加 `1.00`，贷款本金及全账簿负债不重复增加，现金不变，且顺德房产原有顺德房贷仍保留。现金加贷款组合样例把 `3.00` 总额拆为 `Cash-CNY 2.00 + 新贷款1.00`：资产成本和市值各增加 `3.00`，现金只扣差额 `2.00`，负债增加 `1.00`，全局记录保留 `3.00` 业务总额，冷启动保持。选择已关联顺德房产的既有顺德房贷后仍会无提示返回且无写入。工作区菜单数字 ID 在会话间变化，稳定合同是当前资产 ID、菜单语义和位置而非数字 ID。
- `RT-14-005` 的投资费用已确认：`0.00` 提交静默停留在编辑器；支出项目默认 `资产费用` 但可选择完整支出类别树。`0.50` 外部支付使累计收益变为 `-0.50`，成本、市值和资产负债表不变；再绑定 `Cash-CNY` 支付 `0.25` 后累计收益变为 `-0.75`，`Cash-CNY`、全账簿资产和净资产各减少 `0.25`，资产页、现金账户页和全局财务记录显示同一业务关联。
- `RT-14-020` 的投资收益已确认：顶部全局入口不继承账户中心选择，重大资产工作区入口会稳定回填当前资产；`0.00` 提交静默停留在编辑器，收入项目默认 `投资收益` 但可选择完整收入类别列表。`0.50` 外部收益使累计收益变为 `0.50`，成本、市值和资产负债表不变；再绑定 `Cash-CNY` 收入 `0.25` 后累计收益变为 `0.75`，`Cash-CNY`、全账簿资产和净资产各增加 `0.25`。资产页、现金账户页、账户中心和全局财务记录显示同一业务关联，冷启动页面保持。
- `RT-14-003` 已纠正旧记录误分类：旧截图属于物品价值变更 `TPracChangeValueDlgFm`，静态 `TAssetIncrementDlgFM / 资产市值变更` 在当前版本无用户入口；现行重大资产估值由 `TEditSecurityPriceFm` 和市值管理页完成。
- `RT-14-006/010` 已确认市值快照生命周期：允许 `0.00`；跨日期新增形成新行；修改锁定资产和日期；同日“添加”按资产与日期 upsert；删除最新值无确认并回退上一日期。目标资产从 `1.00` 估值为 `2.50` 后，成本与累计收益不变，`Cash-CNY` 和负债不变，资产与净资产各增加 `1.50`，冷启动后历史和汇总保持。
- 重大资产构成图已观察到英镑资产折算为人民币后的成本和市值，与工作区总额一致；Rust 版必须让统计表、构成图和净资产共享同一估值时点与汇率快照。
- B15 已确认预算实际支出、财务诊断、规划资产选择和目标进度都会读取财务数据工作区的账户、交易与估值投影；这些分析页面不能维护第二套余额或支出真相。
- `RT-15-003/005/007` 已真实创建并冷启动月度预算 `RT15-Budget-20260802`。创建流程先保存名称和频率，再必须确认分类范围；目标实现应原子保存预算头和分类关系，或使用不进入有效列表的显式草稿。
- 2026 年 8 月“食物”预算 `23.45` 保存后，页面显示实际总支出 `12,322.99`、预算 `23.45` 和 `52,550%`；比例按 `actual / budget * 100` 四舍五入为整数且不封顶。预算为零时，实际为零显示 `0%`，实际大于零显示 `100%`。支出金额网格单元格使用正数，页脚使用负方向。
- “导入最近12个月的收支金额”无确认覆盖手工值。2026-08-02 执行时读取 `2025-08` 至 `2026-07` 的 12 个完整月份，再按月份编号写入 2026 年 1 至 12 月列；2026 年 7 月导入值和实际值均为 `10,834.72`，2026 年 8 月导入 `47,536.21` 与 2025 年 8 月实际支出及各分类逐分相等。目标导入必须记录来源区间、目标期间和覆盖版本，并在提交前返回差异预览。

## 6. 尚待继续实测

- 概况页的行情、预算、图表切换和显示选项。
- 财务记录的空结果、选择态、新增、除已验证同币种转账、银行 CNY 利息收入和货币兑换外的修改保存、删除、退款、复制粘贴、批量操作、附件、导出和打印；普通收支仍需验证候选列表、校验失败、保存并继续和事务回滚。
- 投资一览的行情更新、离线失败、取消重试、空持仓、多币种估值和图表一致性。
- 标签的新增、修改、排序、隐藏、删除、引用保护、批量设置、导出和打印。
- 账户中心的筛选切换、账户与账户组 CRUD、分组迁移、余额调整、附件以及失败回滚。
- 重大资产追加投资的多贷款分摊、已关联贷款候选与额度规则、非人民币汇率、成本不等于市值时的部分卖出比例和舍入、收益/费用非默认类别、标签、保存并继续、并发和失败回滚；无支付账户与绑定支付账户买入、零金额对象的所有记录范围、无账户全额卖出、绑定收入账户部分卖出、同日市值调整、追加投资零金额/联动/不联动/绑定 `Cash-CNY`/新增贷款融资/未关联既有贷款成功复用/现金加贷款组合、已关联既有贷款静默无操作、投资收益和投资费用的外部/绑定现金账户双路径，以及市值跨日新增、同日 upsert、修改、删除回退、工作区、构成图、概况和冷启动页面复核已到达。市值唯一快照删除、日期/金额/币种边界、收益率、撤销和审计导出仍待校准。
- 物品真实买入/卖出/重估、数量成本算法、分期买入、主档引用保护和失败回滚；账户创建、工作区、资料管理、价格编辑、三类交易编辑和永久删除已到达。
- 商业保险现金价值业务日期来源、跨月/跨年/时区、读模型缺陷根因、其它币种精度、精确上限、聚合溢出和失败回滚，保费计划修改，缴费异常路径，返还/分红边界、候选账户和异常回滚，以及未终止退保后的后续命令、精确损益、计划处理、重复提交和失败回滚；代表性缴费、保费返还、保险分红、退保保留/终止两条路径、同日现金价值新增覆盖、修改、唯一快照删除、两日期删除最新值/非最新值、历史/未来日期、负数/空值、人民币舍入、大额金额和跨页/重启复核已验证，旧 `TInsureBalaIn/OutDlgFm` 保持当前版本不可达结论。
- 使用六类并存和非零余额样例验证社保总额、缴费/待遇交易、统计刷新、异常校验和失败回滚；单个养老子账户创建、共享工作区、删除级联和空组清理已完成。
- 正常关闭原程序后补充 `test.mh8` 的操作后 SHA-256，并区分会话写入与业务写入。
- 用代表性收入、退款、分类迁移、多币种和其它预算周期继续校准预算投影；月度支出预算、滚动导入和冷启动已完成。继续校准诊断指标、规划年度结果与目标进度的跨工作区一致性。
