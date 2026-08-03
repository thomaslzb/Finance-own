# MoneyHome8 全量运行时窗体覆盖审计

本文档由运行时 DFM 和命令证据自动生成，用于证明每一个已恢复窗体都进入功能与数据流台账。分类是重构需求映射，不要求新 SQLite 沿用旧数据库结构。

## 1. 完整性结论

- 运行时窗体：`460` 个
- 已分类窗体：`460` 个
- 未分类窗体：`0` 个
- 业务功能表面：`400` 个
- 父窗体驱动的无文案嵌入视图：`37` 个
- 内部或实验入口：`2` 个
- 共享 UI / 技术支撑：`21` 个
- 命令与交互控件：`1407` 个
- 去重字段绑定：`514` 个
- 标题、命令、页签和选项功能信号：`1822` 条
- 已有代表性运行证据：`29` 个

生成器在出现未分类窗体时直接失败，因此 `未分类窗体=0` 是分析包的硬门槛。无文案嵌入视图必须通过父窗体和调用方验证；`AI`、控制台和内部计算窗体先列为内部/实验入口，不能未经运行证据就纳入正式产品范围。这里证明的是静态结构与需求归属完整，不等于 460 个窗体的动态结果已经逐一实测。

## 2. 业务域覆盖

| 业务域 | 窗体数 | 主要数据流 |
| --- | ---: | --- |
| 账簿生命周期与系统壳层 (`system_shell`) | 15 | 导航/命令状态 -> 应用服务 -> 业务窗体与当前上下文；账簿文件/SQLite -> 打开、备份、还原、结算 -> 账簿上下文；配置/调整输入 -> 领域规则或显示状态持久化 |
| 登录、同步与外部服务 (`auth_sync_external`) | 5 | 本地领域对象 <-> DTO/协议适配 -> 远端服务或通知 |
| 账户与基础资料 (`accounts_master_data`) | 41 | 账户配置 -> 账户真相 -> 余额、估值与导航投影；领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；配置/调整输入 -> 领域规则或显示状态持久化；基础资料 -> 业务引用 -> 交易、预算、报表与同步；候选数据 -> 用户范围选择 -> 上游命令或查询参数；用户输入 -> 领域校验 -> 原子分录/专项扩展事务 |
| 通用交易、流水与模板 (`transactions`) | 38 | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；配置/调整输入 -> 领域规则或显示状态持久化；已提交交易 -> 查询投影 -> 明细操作与下游报表；用户输入 -> 领域校验 -> 原子分录/专项扩展事务；候选数据 -> 用户范围选择 -> 上游命令或查询参数 |
| 债权债务、信用与摊销 (`debts_credit`) | 54 | 账户配置 -> 账户真相 -> 余额、估值与导航投影；领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；用户输入 -> 领域校验 -> 原子分录/专项扩展事务；配置/调整输入 -> 领域规则或显示状态持久化；已提交交易 -> 查询投影 -> 明细操作与下游报表 |
| 存款与银行理财产品 (`financial_products`) | 19 | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；配置/调整输入 -> 领域规则或显示状态持久化；用户输入 -> 领域校验 -> 原子分录/专项扩展事务；账户配置 -> 账户真相 -> 余额、估值与导航投影；已提交交易 -> 查询投影 -> 明细操作与下游报表；基础资料 -> 业务引用 -> 交易、预算、报表与同步 |
| 外汇 (`foreign_exchange`) | 9 | 用户输入 -> 领域校验 -> 原子分录/专项扩展事务；领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；已提交交易 -> 查询投影 -> 明细操作与下游报表 |
| 投资公共能力 (`investment_shared`) | 6 | 用户输入 -> 领域校验 -> 原子分录/专项扩展事务；领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；基础资料 -> 业务引用 -> 交易、预算、报表与同步 |
| 证券 (`securities`) | 21 | 配置/调整输入 -> 领域规则或显示状态持久化；账户配置 -> 账户真相 -> 余额、估值与导航投影；基础资料 -> 业务引用 -> 交易、预算、报表与同步；领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；已提交交易 -> 查询投影 -> 明细操作与下游报表；候选数据 -> 用户范围选择 -> 上游命令或查询参数；用户输入 -> 领域校验 -> 原子分录/专项扩展事务 |
| 基金与货币基金 (`funds`) | 29 | 账户配置 -> 账户真相 -> 余额、估值与导航投影；用户输入 -> 领域校验 -> 原子分录/专项扩展事务；配置/调整输入 -> 领域规则或显示状态持久化；领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；基础资料 -> 业务引用 -> 交易、预算、报表与同步；已提交交易 -> 查询投影 -> 明细操作与下游报表 |
| 债券 (`bonds`) | 15 | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；配置/调整输入 -> 领域规则或显示状态持久化；已提交交易 -> 查询投影 -> 明细操作与下游报表；账户配置 -> 账户真相 -> 余额、估值与导航投影；用户输入 -> 领域校验 -> 原子分录/专项扩展事务；基础资料 -> 业务引用 -> 交易、预算、报表与同步 |
| 期货、黄金与贵金属 (`futures_metals`) | 31 | 配置/调整输入 -> 领域规则或显示状态持久化；账户配置 -> 账户真相 -> 余额、估值与导航投影；用户输入 -> 领域校验 -> 原子分录/专项扩展事务；基础资料 -> 业务引用 -> 交易、预算、报表与同步；领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；已提交交易 -> 查询投影 -> 明细操作与下游报表 |
| 融资融券 (`margin_financing`) | 22 | 用户输入 -> 领域校验 -> 原子分录/专项扩展事务；配置/调整输入 -> 领域规则或显示状态持久化；账户配置 -> 账户真相 -> 余额、估值与导航投影；领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；已提交交易 -> 查询投影 -> 明细操作与下游报表 |
| 保险与社会保障 (`insurance_social`) | 16 | 账户配置 -> 账户真相 -> 余额、估值与导航投影；用户输入 -> 领域校验 -> 原子分录/专项扩展事务；配置/调整输入 -> 领域规则或显示状态持久化；已提交交易 -> 查询投影 -> 明细操作与下游报表；领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| 重大资产与家居物品 (`major_tangible_assets`) | 29 | 用户输入 -> 领域校验 -> 原子分录/专项扩展事务；配置/调整输入 -> 领域规则或显示状态持久化；领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表；已提交交易 -> 查询投影 -> 明细操作与下游报表；账户配置 -> 账户真相 -> 余额、估值与导航投影；基础资料 -> 业务引用 -> 交易、预算、报表与同步 |
| 预算、提醒、规划与目标 (`planning_budget_goal`) | 42 | 规则/专题输入 + 真相投影 -> 计划、提醒、目标或预测结果；用户输入 -> 领域校验 -> 原子分录/专项扩展事务；候选数据 -> 用户范围选择 -> 上游命令或查询参数 |
| 导入导出 (`import_export`) | 7 | 外部来源 -> 暂存/映射/预览 -> 领域命令或导出投影 |
| 报表与分析投影 (`reports`) | 28 | SQLite 真相 -> 参数化查询 -> 表格/图表/导出 |
| 辅助工具与长尾能力 (`tools_longtail`) | 14 | 辅助输入或计算 -> 领域命令、参考数据或外部程序；父窗体状态 -> 复用控件 -> 选择、展示或交互反馈；配置/调整输入 -> 领域规则或显示状态持久化；导航/命令状态 -> 应用服务 -> 业务窗体与当前上下文 |
| 共享 UI 与技术支撑 (`shared_infrastructure`) | 19 | 候选数据 -> 用户范围选择 -> 上游命令或查询参数；父窗体状态 -> 复用控件 -> 选择、展示或交互反馈；配置/调整输入 -> 领域规则或显示状态持久化；领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |

## 3. 交互角色覆盖

| 角色 | 窗体数 | 数据流合同 |
| --- | ---: | --- |
| 账簿生命周期命令 (`ledger_lifecycle`) | 4 | 账簿文件/SQLite -> 打开、备份、还原、结算 -> 账簿上下文 |
| 外部服务与同步 (`external_adapter`) | 5 | 本地领域对象 <-> DTO/协议适配 -> 远端服务或通知 |
| 数据交换 (`data_exchange`) | 7 | 外部来源 -> 暂存/映射/预览 -> 领域命令或导出投影 |
| 报表查询投影 (`report_projection`) | 28 | SQLite 真相 -> 参数化查询 -> 表格/图表/导出 |
| 统计/图表/嵌入视图 (`projection_view`) | 63 | 领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表 |
| 业务交易录入 (`transaction_editor`) | 107 | 用户输入 -> 领域校验 -> 原子分录/专项扩展事务 |
| 交易明细与历史 (`transaction_history`) | 41 | 已提交交易 -> 查询投影 -> 明细操作与下游报表 |
| 账户配置 (`account_editor`) | 49 | 账户配置 -> 账户真相 -> 余额、估值与导航投影 |
| 基础资料维护 (`catalog_editor`) | 19 | 基础资料 -> 业务引用 -> 交易、预算、报表与同步 |
| 预算/提醒/规划工作流 (`planning_workflow`) | 31 | 规则/专题输入 + 真相投影 -> 计划、提醒、目标或预测结果 |
| 选择、筛选与查找 (`selector_filter`) | 16 | 候选数据 -> 用户范围选择 -> 上游命令或查询参数 |
| 配置与调整 (`configuration_editor`) | 69 | 配置/调整输入 -> 领域规则或显示状态持久化 |
| 辅助工具 (`tool_window`) | 9 | 辅助输入或计算 -> 领域命令、参考数据或外部程序 |
| 应用壳层与导航 (`application_shell`) | 3 | 导航/命令状态 -> 应用服务 -> 业务窗体与当前上下文 |
| 共享技术组件 (`shared_infrastructure`) | 9 | 父窗体状态 -> 复用控件 -> 选择、展示或交互反馈 |

## 4. 逐窗体覆盖矩阵

| 资源 | 标题 | 业务域 | 角色 | 命令 | 字段 | 功能信号 | 动态状态 |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| `TABOUTFORM` | 关于 | 账簿生命周期与系统壳层 | 应用壳层与导航 | 1 | 0 | 关于；成都财智软件有限公司 | pending_representative_runtime_validation |
| `TACCESSORIESDLG` | 添加删除附件 | 辅助工具与长尾能力 | 辅助工具 | 5 | 0 | 添加删除附件；FileViewList；删除；打开附件；添加；打开附件文件夹 | pending_representative_runtime_validation |
| `TACCOUNTDLGFM` | AccountDlgFm | 账户与基础资料 | 账户配置 | 3 | 0 | AccountDlgFm；确 定；查看附件；添加删除附件 | pending_representative_runtime_validation |
| `TACCOUNTFEESETFM` | 证券交易费率 | 证券 | 配置与调整 | 1 | 0 | 证券交易费率；A股；B股；确定 | pending_representative_runtime_validation |
| `TACCOUNTMANAGERFM` | 账户中心 | 账户与基础资料 | 账户配置 | 27 | 0 | 账户中心；显示选项；新增账户；所有账户；新增账户组；操作；另 21 项 | pending_representative_runtime_validation |
| `TACCOUNTOVERVIEWDLGFM` | 账户概况 | 账户与基础资料 | 统计/图表/嵌入视图 | 0 | 0 | 账户概况 | pending_representative_runtime_validation |
| `TACCTBALAREMINDDLG` | 账户余额提醒 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 1 | 0 | 账户余额提醒；保存 | pending_representative_runtime_validation |
| `TACCTDETAILDLG` | 账户详细资料 | 账户与基础资料 | 配置与调整 | 2 | 0 | 账户详细资料；确定；联网账号 | pending_representative_runtime_validation |
| `TACCTGUIDEMAIN` | AcctGuideMain | 账户与基础资料 | 账户配置 | 0 | 0 | AcctGuideMain | pending_representative_runtime_validation |
| `TADJUSTHELDDLGFM` | 持仓调整 | 投资公共能力 | 业务交易录入 | 0 | 0 | 持仓调整 | pending_representative_runtime_validation |
| `TADVANCEACCTDLGFM` | 预收、预付 | 债权债务、信用与摊销 | 账户配置 | 0 | 0 | 预收、预付 | pending_representative_runtime_validation |
| `TADVANCESVIEWFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TADVANCETRANSDLGFM` | 预付 | 债权债务、信用与摊销 | 业务交易录入 | 0 | 0 | 预付 | pending_representative_runtime_validation |
| `TAIPANELDLG` | AI | 辅助工具与长尾能力 | 辅助工具 | 0 | 0 | AI | pending_reachability_and_product_scope_decision |
| `TALIPAYVIEWFRAME` |  | 通用交易、流水与模板 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TALSOCOUPONSDIRECTLYDLGFM` | 直接还券 | 融资融券 | 业务交易录入 | 0 | 0 | 直接还券 | pending_representative_runtime_validation |
| `TAMOUNTSCREENINGFRAME` |  | 共享 UI 与技术支撑 | 选择、筛选与查找 | 4 | 0 | 金额在；金额小于等于；金额大于等于；不筛选金额 | pending_representative_runtime_validation |
| `TASSETBUYFM` | 重大资产买入 | 重大资产与家居物品 | 业务交易录入 | 4 | 0 | 重大资产买入；有贷款；新增贷款；btnType；确 定 | pending_representative_runtime_validation |
| `TASSETENCASHDLGFM` | 重大资产卖出 | 重大资产与家居物品 | 业务交易录入 | 3 | 0 | 重大资产卖出；按比例减少市值；有欠款；新增欠款 | pending_representative_runtime_validation |
| `TASSETINCREMENTDLGFM` | 资产市值变更 | 重大资产与家居物品 | 业务交易录入 | 0 | 0 | 资产市值变更 | pending_representative_runtime_validation |
| `TASSETINVESTDLGFM` | 追加投资 | 重大资产与家居物品 | 业务交易录入 | 3 | 0 | 追加投资；有贷款；同时追加市值；新增贷款 | pending_representative_runtime_validation |
| `TASSETOTHERFEEDLGFM` | 资产投资费用 | 重大资产与家居物品 | 业务交易录入 | 0 | 0 | 资产投资费用 | pending_representative_runtime_validation |
| `TASSETPRICEFM` | 重大资产价格 | 重大资产与家居物品 | 配置与调整 | 13 | 4 | 重大资产价格；操作；MHBPrice；MHBAsset；新增价格；修改价格；另 5 项 | pending_representative_runtime_validation |
| `TASSETSCONSTITUTECHARTFRAME` |  | 重大资产与家居物品 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TASSETSDLGFM` | 重大资产概况 | 重大资产与家居物品 | 统计/图表/嵌入视图 | 2 | 0 | 重大资产概况；投资；自用 | pending_representative_runtime_validation |
| `TASSETSMARKETCONSTITUTESFRAME` |  | 重大资产与家居物品 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TASSETSSTATISTICFRAME` |  | 重大资产与家居物品 | 统计/图表/嵌入视图 | 3 | 6 | 删除；当前持有资产；所有记录过的资产 | pending_representative_runtime_validation |
| `TASSETSTRANSFRAME` |  | 重大资产与家居物品 | 交易明细与历史 | 1 | 6 | 单个资产交易明细 | pending_representative_runtime_validation |
| `TASSETSVALUEMANAGEMENTFRAME` |  | 重大资产与家居物品 | 配置与调整 | 4 | 2 | mhbgData；添加；修改；删除 | pending_representative_runtime_validation |
| `TASSETTRANSFM` | 重大资产交易明细 | 重大资产与家居物品 | 交易明细与历史 | 0 | 0 | 重大资产交易明细；交易明细；市值管理；成本市值构成；资产概况 | pending_representative_runtime_validation |
| `TASSETVIEWFRAME` |  | 重大资产与家居物品 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TBACKUPBOOKFM` | 备份账簿 | 账簿生命周期与系统壳层 | 账簿生命周期命令 | 3 | 0 | 备份账簿；备份；更改；确定 | pending_representative_runtime_validation |
| `TBATCHALSOCOUPONSDIRECTLYDLGFM` | 批量直接还券 | 融资融券 | 业务交易录入 | 1 | 0 | 批量直接还券；确 定 | pending_representative_runtime_validation |
| `TBATCHDIRECTPAYMENTSDLGFM` | 批量直接还款 | 融资融券 | 业务交易录入 | 1 | 0 | 批量直接还款；确 定 | pending_representative_runtime_validation |
| `TBLOCKUPDLGFM` | 垫付 | 债权债务、信用与摊销 | 业务交易录入 | 0 | 0 | 垫付 | pending_representative_runtime_validation |
| `TBONDSMARKETCONSTITUTESFRAME` |  | 债券 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TBONDSVIEWFRAME` |  | 债券 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TBUDGETCOPYDLGFM` | 复制预算金额 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 13 | 0 | 复制预算金额；九月；十月；十一月；十二月；八月；另 8 项 | pending_representative_runtime_validation |
| `TBUDGETLISTFM` | 预算 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 15 | 0 | 预算；新增预算；mwAdjustYear；mwAdjustMonth；mwAdjustSeason；预算设置；另 10 项 | pending_representative_runtime_validation |
| `TBUYFUNDPLANDLGFM` | 基金定投计划 | 预算、提醒、规划与目标 | 业务交易录入 | 2 | 0 | 基金定投计划；自动执行；更新基金 | representative_runtime_validation_observed |
| `TCALCUFM` | CalcuFm | 辅助工具与长尾能力 | 共享技术组件 | 0 | 0 | CalcuFm | not_applicable_or_parent_driven |
| `TCALCULATORDLG` | 金融计算器 | 辅助工具与长尾能力 | 辅助工具 | 0 | 0 | 金融计算器 | pending_representative_runtime_validation |
| `TCARDVIEWFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TCASHACCTDLGFM` | 现金 | 账户与基础资料 | 账户配置 | 0 | 0 | 现金 | pending_representative_runtime_validation |
| `TCASHCARDDLGFM` | 信用卡取现 | 通用交易、流水与模板 | 配置与调整 | 0 | 0 | 信用卡取现 | pending_representative_runtime_validation |
| `TCASHTRANSFM` | 现金交易列表 | 通用交易、流水与模板 | 交易明细与历史 | 0 | 0 | 现金交易列表 | pending_representative_runtime_validation |
| `TCASHTRANSFRAME` |  | 通用交易、流水与模板 | 交易明细与历史 | 1 | 7 | 导入 | pending_representative_runtime_validation |
| `TCASHVIEWFRAME` |  | 通用交易、流水与模板 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TCASHWITHDRAWDLGFM` | 取款 | 通用交易、流水与模板 | 业务交易录入 | 2 | 0 | 取款；全部取完；到期 | pending_representative_runtime_validation |
| `TCASHXFERDLGFM` | 转账 | 通用交易、流水与模板 | 业务交易录入 | 1 | 0 | 转账；交换转入转出账户 | pending_representative_runtime_validation |
| `TCATEGORYLISTFM` | 收支项目 | 账户与基础资料 | 基础资料维护 | 17 | 0 | 收支项目；操作；pmCategory；归属于；上次使用日期：；新增项目；另 12 项 | pending_representative_runtime_validation |
| `TCHANGEPAYMODEDLGFM` | 变更还款方式 | 债权债务、信用与摊销 | 配置与调整 | 1 | 0 | 变更还款方式；保存 | pending_representative_runtime_validation |
| `TCHECKBOOKDLG` | 结算账簿 | 账簿生命周期与系统壳层 | 账簿生命周期命令 | 2 | 0 | 结算账簿；更改；确定 | pending_representative_runtime_validation |
| `TCHILDFORM` | ChildForm | 共享 UI 与技术支撑 | 共享技术组件 | 2 | 0 | ChildForm；sbHelp；sbCloseChild | pending_representative_runtime_validation |
| `TCLAIMSDEBTCONTAINER` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 | 0 | 应收款概况；应付款；待摊费用；预收款；预付款概况 | pending_representative_runtime_validation |
| `TCLAIMSDEBTSCHARTFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 1 | 0 | btnUnit | pending_representative_runtime_validation |
| `TCLAIMSDEBTSCONSTITUTESFRAME` |  | 债权债务、信用与摊销 | 配置与调整 | 1 | 0 | btnShowType | pending_representative_runtime_validation |
| `TCLAIMSDEBTSTATISTICFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 6 | 0 | 债权和债务 \| 忽略已完成款项；删除；显示债权和债务；仅债权；仅债务；忽略已完成的款项 | pending_representative_runtime_validation |
| `TCLAIMSDEBTTRANSFRAME` |  | 债权债务、信用与摊销 | 交易明细与历史 | 1 | 9 | 查看未报销记录 | pending_representative_runtime_validation |
| `TCLAIMSTRANSFM` | 债权债务交易明细 | 债权债务、信用与摊销 | 交易明细与历史 | 0 | 0 | 债权债务交易明细；交易明细；债权债务构成；已收金额和收款表；债权债务概况 | pending_representative_runtime_validation |
| `TCLEANPRICEFM` | 价格整理 | 辅助工具与长尾能力 | 辅助工具 | 9 | 0 | 价格整理；删除日期；删除日期 从；删除所有未交易对象的价格数据；保留已交易过的金融产品的历史价格数据；股票价格数据；另 4 项 | pending_representative_runtime_validation |
| `TCOLLATERALINDLGFM` | 担保物划入 | 融资融券 | 配置与调整 | 0 | 0 | 担保物划入 | pending_representative_runtime_validation |
| `TCONSOLEFM` | 控制台 | 辅助工具与长尾能力 | 辅助工具 | 1 | 0 | 控制台；SQL；网银插件与网络；清除控制台记录 | pending_reachability_and_product_scope_decision |
| `TCOSTDETAILSDLGFM` | 垫付明细 | 债权债务、信用与摊销 | 配置与调整 | 3 | 0 | 垫付明细；确定；反选(&I)；全选(&A) | pending_representative_runtime_validation |
| `TCOUPONSALSOBUYCOUPONSDLGFM` | 买券还券 | 融资融券 | 业务交易录入 | 1 | 0 | 买券还券；显示费用详情 | pending_representative_runtime_validation |
| `TCREATEBUDGETDLGFM` | 预算 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 9 | 0 | 预算；月度；季度；年度；自定义；确定；另 4 项 | pending_representative_runtime_validation |
| `TCREDITACCTDLGFM` | 信用卡账户 | 债权债务、信用与摊销 | 账户配置 | 10 | 0 | 信用卡账户；透支提醒；账单日之后；固定还款日，每月；计入下期；计入本期；另 5 项 | pending_representative_runtime_validation |
| `TCREDITCARDSTATISTICFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 3 | 6 | 导入；显示最近3期已出账单；显示所有已出账单 | pending_representative_runtime_validation |
| `TCREDITCARDTRANSFM` | 信用卡交易明细 | 债权债务、信用与摊销 | 交易明细与历史 | 0 | 0 | 信用卡交易明细；交易明细；分期付款管理 | pending_representative_runtime_validation |
| `TCREDITCARDTRANSFRAME` |  | 债权债务、信用与摊销 | 交易明细与历史 | 2 | 7 | 导入；单个账单交易明细 | pending_representative_runtime_validation |
| `TCREDITREMINDDLG` | 信用卡透支额提醒 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 1 | 0 | 信用卡透支额提醒；保存 | pending_representative_runtime_validation |
| `TCURRCHGXFERDLGFM` | 货币兑换 | 外汇 | 业务交易录入 | 0 | 0 | 货币兑换 | pending_representative_runtime_validation |
| `TCURRDEPOSITSVIEWFRAME` |  | 存款与银行理财产品 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TCURRDLG` | 货币 | 账户与基础资料 | 基础资料维护 | 3 | 0 | 货币；现汇；现钞；保存 | pending_representative_runtime_validation |
| `TCURRENTACCTDLGFM` | 活期存款 | 账户与基础资料 | 账户配置 | 1 | 0 | 活期存款；更多信息 | pending_representative_runtime_validation |
| `TCURRENTMONTHINCEXPPIECHARTFRAME` |  | 通用交易、流水与模板 | 统计/图表/嵌入视图 | 1 | 0 | btnUnit | pending_representative_runtime_validation |
| `TCURRENTTRANSFM` | 活期存款交易明细 | 通用交易、流水与模板 | 交易明细与历史 | 0 | 0 | 活期存款交易明细 | pending_representative_runtime_validation |
| `TCURREXCHANGEDLGFM` | 外汇交易 | 外汇 | 业务交易录入 | 1 | 0 | 外汇交易；lblRateDirection | pending_representative_runtime_validation |
| `TCURRFUNDACCTDLGFM` | 货币基金账户 | 基金与货币基金 | 账户配置 | 4 | 0 | 货币基金账户；自身；其它；储蓄；投资 | pending_representative_runtime_validation |
| `TCURRFUNDBUYDLGFM` | 货币基金申购 | 基金与货币基金 | 业务交易录入 | 1 | 0 | 货币基金申购；更新基金 | pending_representative_runtime_validation |
| `TCURRFUNDCONVERTFM` | 货币基金转换 | 基金与货币基金 | 配置与调整 | 3 | 0 | 货币基金转换；btnFeeType；更新基金；确 定 | pending_representative_runtime_validation |
| `TCURRFUNDMARKETCONSTITUTESFRAME` |  | 基金与货币基金 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TCURRFUNDREINVESTDLGFM` | 货币基金红利再投资 | 基金与货币基金 | 配置与调整 | 0 | 0 | 货币基金红利再投资 | pending_representative_runtime_validation |
| `TCURRFUNDSELLDLGFM` | 货币基金赎回 | 基金与货币基金 | 业务交易录入 | 0 | 0 | 货币基金赎回 | pending_representative_runtime_validation |
| `TCURRFUNDSLISTFM` | 货币基金列表 | 基金与货币基金 | 基础资料维护 | 12 | 4 | 货币基金列表；操作；MHBGSecurity；新增基金；修改基金；删除基金；另 7 项 | pending_representative_runtime_validation |
| `TCURRFUNDSTATISTICFRAME` |  | 基金与货币基金 | 统计/图表/嵌入视图 | 5 | 3 | 获取代码；BrowseGrid；货币基金代码转换；当前持仓基金；所有交易过的基金 | pending_representative_runtime_validation |
| `TCURRFUNDTRANSFM` | 货币基金交易明细 | 基金与货币基金 | 交易明细与历史 | 0 | 0 | 货币基金交易明细；交易明细；历史盈亏 | pending_representative_runtime_validation |
| `TCURRFUNDTRANSFRAME` |  | 基金与货币基金 | 交易明细与历史 | 1 | 5 | 单只基金交易明细 | pending_representative_runtime_validation |
| `TCURRFUNDVIEWFRAME` |  | 基金与货币基金 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TCURRLISTFM` | 币种与汇率 | 账户与基础资料 | 基础资料维护 | 26 | 9 | 币种与汇率；按日期显示全部汇率；操作；DBGRID；RateGrid；miDeleteCategory；另 18 项 | pending_representative_runtime_validation |
| `TCUSTCOLUMNFM` | CustColumnFm | 通用交易、流水与模板 | 配置与调整 | 0 | 0 | CustColumnFm | pending_representative_runtime_validation |
| `TCUSTOMERDLGFM` | 客户服务 | 辅助工具与长尾能力 | 配置与调整 | 5 | 0 | 客户服务；imgQQTechnicalSupport；imgQQBuy；imgSinaWeibo；http://www.moneywise.com.cn/；常见问题 | pending_representative_runtime_validation |
| `TCUSTOMNAVIGATIONACCTDLGFM` | 设置[自定义]显示 | 账户与基础资料 | 账户配置 | 5 | 0 | 设置[自定义]显示；下移；全选；反选；确定；上移 | representative_runtime_validation_observed |
| `TDCURRCREDITACCTDLGFM` | 双币信用卡 | 债权债务、信用与摊销 | 账户配置 | 7 | 0 | 双币信用卡；限额提醒；每月最后一天是账单日；固定账单日；账单日之后；固定还款日；另 1 项 | pending_representative_runtime_validation |
| `TDEBTADJUSTDLGFM` | 坏账 | 债权债务、信用与摊销 | 配置与调整 | 0 | 0 | 坏账 | pending_representative_runtime_validation |
| `TDEBTBORROWDLGFM` | 借入 | 债权债务、信用与摊销 | 业务交易录入 | 0 | 0 | 借入 | pending_representative_runtime_validation |
| `TDEBTEQUITYSWAPTRANSDLGFM` | 债转股 | 融资融券 | 业务交易录入 | 0 | 0 | 债转股 | pending_representative_runtime_validation |
| `TDEBTINVESTMENTACCTDLGFM` | 网贷 | 债权债务、信用与摊销 | 账户配置 | 0 | 0 | 网贷 | pending_representative_runtime_validation |
| `TDEBTINVESTMENTACCTLISTFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 | 8 |  | parent_driven_structure_only |
| `TDEBTINVESTMENTBADTRANSDLGFM` | 网贷坏账 | 债权债务、信用与摊销 | 业务交易录入 | 0 | 0 | 网贷坏账 | pending_representative_runtime_validation |
| `TDEBTINVESTMENTLOANDLGFM` | 网贷借出 | 债权债务、信用与摊销 | 业务交易录入 | 5 | 0 | 网贷借出；收款计划到期自动执行；btnPayMode；btnPeriodMode；btnPayFreqMode；btnInterestCalcMode | pending_representative_runtime_validation |
| `TDEBTINVESTMENTPAYOBJECTFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 3 | 7 | 网贷收回；BrowseGrid；当前账户 | pending_representative_runtime_validation |
| `TDEBTINVESTMENTPAYTABLEFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 1 | 0 | 打印 | pending_representative_runtime_validation |
| `TDEBTINVESTMENTREWARDTRANSDLGFM` | 网贷投资奖励 | 债权债务、信用与摊销 | 业务交易录入 | 0 | 0 | 网贷投资奖励 | pending_representative_runtime_validation |
| `TDEBTINVESTMENTSELLTRANSDLGFM` | 网贷转让 | 债权债务、信用与摊销 | 业务交易录入 | 0 | 0 | 网贷转让 | pending_representative_runtime_validation |
| `TDEBTINVESTMENTSTATISTICFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 4 | 8 | 收款表；BrowseGrid；当前持有网贷；已完成网贷 | pending_representative_runtime_validation |
| `TDEBTINVESTMENTTRANSFM` | 网贷账户交易明细 | 债权债务、信用与摊销 | 交易明细与历史 | 0 | 0 | 网贷账户交易明细；交易明细；投资列表；待收明细 | pending_representative_runtime_validation |
| `TDEBTINVESTMENTTRANSFRAME` |  | 债权债务、信用与摊销 | 交易明细与历史 | 0 | 7 |  | parent_driven_structure_only |
| `TDEBTINVESTMENTVIEWFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TDEBTINVESTMENTWITHDRAWTRANSDLGFM` | 网贷收回 | 债权债务、信用与摊销 | 业务交易录入 | 0 | 0 | 网贷收回 | pending_representative_runtime_validation |
| `TDEBTLENDDLGFM` | 借出 | 债权债务、信用与摊销 | 业务交易录入 | 0 | 0 | 借出 | pending_representative_runtime_validation |
| `TDEBTRATESETDLG` | 借贷款账户利率调整 | 债权债务、信用与摊销 | 配置与调整 | 1 | 0 | 借贷款账户利率调整；确定 | pending_representative_runtime_validation |
| `TDEBTRECDLGFM` | 收回 | 债权债务、信用与摊销 | 配置与调整 | 0 | 0 | 收回 | pending_representative_runtime_validation |
| `TDEBTRETURNDLGFM` | 返还 | 债权债务、信用与摊销 | 业务交易录入 | 0 | 0 | 返还 | pending_representative_runtime_validation |
| `TDEBTSACCTDLGFM` | 应收、应付 | 债权债务、信用与摊销 | 账户配置 | 0 | 0 | 应收、应付 | pending_representative_runtime_validation |
| `TDEFERREDVIEWFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TDIALOGFORM` | DialogForm | 共享 UI 与技术支撑 | 共享技术组件 | 3 | 0 | DialogForm；关闭；帮助；对话框标题 | pending_representative_runtime_validation |
| `TDIARYDLGFM` | 日记 | 辅助工具与长尾能力 | 辅助工具 | 15 | 0 | 日记；加粗；倾斜；下划线；左对齐；居中；另 10 项 | pending_representative_runtime_validation |
| `TDIARYUNTFM` | 日记 | 辅助工具与长尾能力 | 辅助工具 | 8 | 0 | 日记；操作；tlDiary；写日记；修改日记；删除日记；另 3 项 | pending_representative_runtime_validation |
| `TDIRECTPAYMENTSDLGFM` | 直接还款 | 融资融券 | 业务交易录入 | 0 | 0 | 直接还款 | pending_representative_runtime_validation |
| `TDRAWALCARDDLGFM` | 信用卡还款 | 债权债务、信用与摊销 | 配置与调整 | 0 | 0 | 信用卡还款 | pending_representative_runtime_validation |
| `TDROPDOWNDATE` | Dropdowndate | 共享 UI 与技术支撑 | 选择、筛选与查找 | 0 | 0 | Dropdowndate | not_applicable_or_parent_driven |
| `TDROPFM` | DropFM | 共享 UI 与技术支撑 | 选择、筛选与查找 | 1 | 0 | DropFM | pending_representative_runtime_validation |
| `TEDITACCOUNTGROUPFM` | 账户组 | 账户与基础资料 | 配置与调整 | 1 | 0 | 账户组；详细资料... | representative_runtime_validation_observed |
| `TEDITASSETBUYDLGFM` | 重大资产买入 | 重大资产与家居物品 | 业务交易录入 | 2 | 0 | 重大资产买入；有贷款；新增贷款 | pending_representative_runtime_validation |
| `TEDITBANKMONEYPRODUCTDLGFM` | 银行理财产品 | 存款与银行理财产品 | 配置与调整 | 4 | 0 | 银行理财产品；是否保本；是否注销；保存；btnTermType | pending_representative_runtime_validation |
| `TEDITBUDGETAMOUNTDLGFM` | 预算金额设置 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 8 | 0 | 预算金额设置；确定；mwAdjustYear；复制预算金额；导入最近12个月的收支金额；pm1；另 3 项 | pending_representative_runtime_validation |
| `TEDITBUDGETCATEGORYDLGFM` | 选择预算收支项目 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 4 | 0 | 选择预算收支项目；支出；收入；确定；新增收支项目；全选；另 1 项 | pending_representative_runtime_validation |
| `TEDITCATEGORYFM` | 收支项目 | 账户与基础资料 | 基础资料维护 | 4 | 0 | 收支项目；支出；收入；保存；保存并新添 | representative_runtime_validation_observed |
| `TEDITCATGORYORDERDLGFM` | 调整收支项目顺序 | 账户与基础资料 | 配置与调整 | 1 | 0 | 调整收支项目顺序；确定 | representative_runtime_validation_observed |
| `TEDITCURRFUNDFM` | 货币基金 | 基金与货币基金 | 配置与调整 | 2 | 0 | 货币基金；锁定名称；保存 | pending_representative_runtime_validation |
| `TEDITFUTURESGOODSFM` | 期货品种 | 期货、黄金与贵金属 | 配置与调整 | 3 | 0 | 期货品种；保存；btnType；btnFeeType | pending_representative_runtime_validation |
| `TEDITGOLDFM` | 贵金属 | 期货、黄金与贵金属 | 配置与调整 | 1 | 0 | 贵金属；保存 | pending_representative_runtime_validation |
| `TEDITMARGINCONTRACTDLGFM` | 编辑融资融券 | 融资融券 | 配置与调整 | 3 | 0 | 编辑融资融券；btnType；更新代码；保存 | pending_representative_runtime_validation |
| `TEDITNMARKETBONDFM` | 债券 | 债券 | 配置与调整 | 2 | 0 | 债券；免税；保存 | pending_representative_runtime_validation |
| `TEDITOPENFUNDFM` | 开放式基金 | 基金与货币基金 | 配置与调整 | 2 | 0 | 开放式基金；锁定名称；保存 | pending_representative_runtime_validation |
| `TEDITPRECIOUSMETALSTDGOODSFM` | 贵金属TD品种 | 期货、黄金与贵金属 | 配置与调整 | 1 | 0 | 贵金属TD品种；保存 | pending_representative_runtime_validation |
| `TEDITSECURITYFM` | 股票 | 证券 | 配置与调整 | 2 | 0 | 股票；锁定名称；保存 | pending_representative_runtime_validation |
| `TEDITSECURITYPRICEFM` | EditSecurityPriceFm | 证券 | 配置与调整 | 1 | 0 | EditSecurityPriceFm；保存 | pending_representative_runtime_validation |
| `TEDITTAGORDERDLGFM` | 调整标签顺序 | 账户与基础资料 | 配置与调整 | 1 | 0 | 调整标签顺序；确定 | representative_runtime_validation_observed |
| `TEDTACCTGRPDLGFM` | 修改所属账户组 | 账户与基础资料 | 配置与调整 | 1 | 0 | 修改所属账户组；确定 | representative_runtime_validation_observed |
| `TEQUITYFINANCINGDLGFM` | 融资权益 | 融资融券 | 业务交易录入 | 0 | 0 | 融资权益 | pending_representative_runtime_validation |
| `TEQUITYSECURITIESLENDINGDLGFM` | 融券权益 | 融资融券 | 业务交易录入 | 0 | 0 | 融券权益 | pending_representative_runtime_validation |
| `TEXCHANGEACCTFM` | 外汇交易账户 | 外汇 | 业务交易录入 | 0 | 0 | 外汇交易账户 | pending_representative_runtime_validation |
| `TEXCHANGEMARKETCONSTITUTESFRAME` |  | 外汇 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TEXCHANGERATEDLG` | 外汇汇率 | 外汇 | 业务交易录入 | 1 | 0 | 外汇汇率；保存 | pending_representative_runtime_validation |
| `TEXCHANGEVIEWFRAME` |  | 外汇 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TEXERTIONRIGHTSDLGFM` | 行权 | 融资融券 | 业务交易录入 | 0 | 0 | 行权 | pending_representative_runtime_validation |
| `TEXPENSEDLGFM` | 报销 | 通用交易、流水与模板 | 业务交易录入 | 1 | 0 | 报销；选择垫付记录… | pending_representative_runtime_validation |
| `TEXPORTDATAFM` | 数据导出 | 导入导出 | 数据交换 | 28 | 0 | 数据导出；基本选项；数据选项；导入时更新账户余额；增加；删除并覆盖；另 24 项 | pending_representative_runtime_validation |
| `TFEESETFORM` | 证券交易费率 | 证券 | 配置与调整 | 7 | 0 | 证券交易费率；操作；更新费率；导出；打印 | pending_representative_runtime_validation |
| `TFILTERDLGFM` | 筛选 | 通用交易、流水与模板 | 选择、筛选与查找 | 6 | 0 | 筛选；不筛选金额；金额大于等于；金额小于等于；金额从；确定；另 1 项 | pending_representative_runtime_validation |
| `TFILTERTRANSFRAME` |  | 通用交易、流水与模板 | 交易明细与历史 | 3 | 0 | 所有明细；当前交易明细；所有交易明细 | pending_representative_runtime_validation |
| `TFINANCIALCALENDARDLG` | 财务日历 | 预算、提醒、规划与目标 | 业务交易录入 | 2 | 0 | 财务日历；btnYear；btnMonth | pending_representative_runtime_validation |
| `TFINANCIALDIAGNOSISFM` | 财务诊断 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 11 | 0 | 财务诊断；tsInputData；tsIndicators；新增账户；btnInputDataType；资产性质设置；另 6 项 | pending_representative_runtime_validation |
| `TFINANCIALPLANNINGCENTERFM` | 财务规划 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 1 | 0 | 财务规划；未来重大事件；当前财务情况；家庭资料；清除数据 | pending_representative_runtime_validation |
| `TFINANCINGBIDDLGFM` | 融资买入 | 融资融券 | 业务交易录入 | 3 | 0 | 融资买入；显示费用详情；更新代码；btnFeeType | pending_representative_runtime_validation |
| `TFINDDLGFM` | 查找 | 通用交易、流水与模板 | 选择、筛选与查找 | 2 | 0 | 查找；查找下一个；重新开始 | pending_representative_runtime_validation |
| `TFINDFORM` | 查找 | 通用交易、流水与模板 | 选择、筛选与查找 | 1 | 0 | 查找 | pending_representative_runtime_validation |
| `TFIXDEPMATUREDLGFM` | 续存 | 存款与银行理财产品 | 业务交易录入 | 0 | 0 | 续存 | pending_representative_runtime_validation |
| `TFIXDEPOSITSVIEWFRAME` |  | 存款与银行理财产品 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TFIXEDACCTDLGFM` | 定期存款 | 存款与银行理财产品 | 账户配置 | 2 | 0 | 定期存款；到期自动续存；btnTermType | pending_representative_runtime_validation |
| `TFIXEDDEPOSITSTATISTICFRAME` |  | 存款与银行理财产品 | 统计/图表/嵌入视图 | 3 | 8 | 所有；新增存单；删除 | pending_representative_runtime_validation |
| `TFIXEDDEPOSITTRANSFM` | 定期存单 | 存款与银行理财产品 | 交易明细与历史 | 0 | 0 | 定期存单；交易明细；账户概况 | pending_representative_runtime_validation |
| `TFMCUSTOMDIALOG` | Custom AutoFilter | 共享 UI 与技术支撑 | 配置与调整 | 4 | 0 | Custom AutoFilter；&And；&Or；OK；Cancel | pending_representative_runtime_validation |
| `TFMINCEXPCAPTIONFORM` | 管理常用备注 | 通用交易、流水与模板 | 业务交易录入 | 7 | 0 | 管理常用备注；新增；操作；TreeList；修改；删除；另 2 项 | pending_representative_runtime_validation |
| `TFOREIGNSTATISTICFRAME` |  | 外汇 | 统计/图表/嵌入视图 | 6 | 4 | 获取牌价；持有外汇调整；添加外汇牌价；当前持有外汇；所有交易过的外汇 | pending_representative_runtime_validation |
| `TFOREIGNTRANSFM` | 外汇交易明细 | 外汇 | 交易明细与历史 | 0 | 0 | 外汇交易明细；交易明细；外汇构成 | pending_representative_runtime_validation |
| `TFOREIGNTRANSFRAME` |  | 外汇 | 交易明细与历史 | 1 | 10 | 当前选中币种交易明细 | pending_representative_runtime_validation |
| `TFPANNUALSALARYINFODLGFM` | 工资 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 1 | 0 | 工资；确定 | pending_representative_runtime_validation |
| `TFPASSETEXPENSESINFODLGFM` | 资产带来的支出 | 预算、提醒、规划与目标 | 业务交易录入 | 1 | 0 | 资产带来的支出；确定 | pending_representative_runtime_validation |
| `TFPASSETGROWTHINFODLGFM` | 资产增长 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 1 | 0 | 资产增长；确定 | pending_representative_runtime_validation |
| `TFPASSETINCOMEINFODLGFM` | 资产带来的收入 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 1 | 0 | 资产带来的收入；确定 | pending_representative_runtime_validation |
| `TFPASSETPURCHASEPLANINFOFM` | 资产购置 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 3 | 0 | 资产购置；带来的收入；带来的支出；分期付款；一次性付款；确定 | pending_representative_runtime_validation |
| `TFPBASEDLGFM` | FPBaseDlgFm | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 0 | 0 | FPBaseDlgFm | pending_representative_runtime_validation |
| `TFPBASEINFODLGFM` | 家庭资料 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 2 | 0 | 家庭资料；有配偶；确定 | pending_representative_runtime_validation |
| `TFPDAILYEXPENSESINFODLGFM` | 日常支出 | 预算、提醒、规划与目标 | 业务交易录入 | 1 | 0 | 日常支出；确定 | pending_representative_runtime_validation |
| `TFPEDUCATIONEXPENSESINFODLGFM` | 教育计划 | 预算、提醒、规划与目标 | 业务交易录入 | 1 | 0 | 教育计划；确定 | pending_representative_runtime_validation |
| `TFPEXPENSESADJUSTMENTINFODLGFM` | 支出调整 | 预算、提醒、规划与目标 | 业务交易录入 | 1 | 0 | 支出调整；确定 | pending_representative_runtime_validation |
| `TFPINFLATIONRATEINFODLGFM` | 通货膨胀率 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 1 | 0 | 通货膨胀率；确定 | pending_representative_runtime_validation |
| `TFPOTHEREXPENSESINFODLGFM` | 其它支出 | 预算、提醒、规划与目标 | 业务交易录入 | 1 | 0 | 其它支出；确定 | pending_representative_runtime_validation |
| `TFPOTHERINCOMEINFODLGFM` | 其它收入 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 1 | 0 | 其它收入；确定 | pending_representative_runtime_validation |
| `TFPRETIREMENTINFODLGFM` | 养老计划 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 1 | 0 | 养老计划；确定 | pending_representative_runtime_validation |
| `TFPSELECTASSETSDLGFM` | 选择资产 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 2 | 0 | 选择资产；确定；新增账户 | pending_representative_runtime_validation |
| `TFPYEARDATAINFODLGFM` | 年度情况 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 2 | 0 | 年度情况；上一年；下一年 | pending_representative_runtime_validation |
| `TFUNDBUYDLGFM` | 开放式基金申购 | 基金与货币基金 | 业务交易录入 | 2 | 0 | 开放式基金申购；更新基金；btnFeeMode | representative_runtime_validation_observed |
| `TFUNDCONVERTDLGFM` | 开放式基金转换 | 基金与货币基金 | 配置与调整 | 5 | 0 | 开放式基金转换；更新基金；btnNewFeeMode；btnOldFeeMode；确 定 | pending_representative_runtime_validation |
| `TFUNDINTERESTDLGFM` | 基金现金红利 | 基金与货币基金 | 业务交易录入 | 1 | 0 | 基金现金红利；btnType | pending_representative_runtime_validation |
| `TFUNDMARKBUYDLGFM` | 新基金认购确认 | 基金与货币基金 | 业务交易录入 | 2 | 0 | 新基金认购确认；中签；确 定 | pending_representative_runtime_validation |
| `TFUNDORDERBUYDLGFM` | 新基金认购 | 基金与货币基金 | 业务交易录入 | 1 | 0 | 新基金认购；更新基金 | pending_representative_runtime_validation |
| `TFUNDREINVESTDLGFM` | 分红再投资 | 基金与货币基金 | 配置与调整 | 1 | 0 | 分红再投资；btnType | pending_representative_runtime_validation |
| `TFUNDSELLDLGFM` | 开放式基金赎回 | 基金与货币基金 | 业务交易录入 | 2 | 0 | 开放式基金赎回；btnFeeMode；btnType | pending_representative_runtime_validation |
| `TFUNDSPLITDLGFM` | 基金拆分 | 基金与货币基金 | 配置与调整 | 0 | 0 | 基金拆分 | pending_representative_runtime_validation |
| `TFUTURESACCTDLGFM` | 期货账户 | 期货、黄金与贵金属 | 账户配置 | 0 | 0 | 期货账户 | pending_representative_runtime_validation |
| `TFUTURESBUYDLGFM` | 期货开仓 | 期货、黄金与贵金属 | 业务交易录入 | 1 | 0 | 期货开仓；btnType | pending_representative_runtime_validation |
| `TFUTURESCONTRACTLISTFM` | 期货合约列表 | 期货、黄金与贵金属 | 基础资料维护 | 19 | 6 | 期货合约列表；显示单日所有价格；只显示持仓产品价格；操作；DBGridPrice；新增；另 11 项 | pending_representative_runtime_validation |
| `TFUTURESGOODSLISTFM` | 期货品种列表 | 期货、黄金与贵金属 | 基础资料维护 | 9 | 14 | 期货品种列表；操作；MHBGSecurity；pmSecurity；miDeleteSecurity；新增期货；另 4 项 | pending_representative_runtime_validation |
| `TFUTURESSELLDLGFM` | 期货平仓 | 期货、黄金与贵金属 | 业务交易录入 | 0 | 0 | 期货平仓 | pending_representative_runtime_validation |
| `TFUTURESSTATISTICFRAME` |  | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | 7 | 9 | 获取合约价格；BrowseGrid；添加合约价格；证券代码变更；期货品种设置；当前持仓合约；另 1 项 | pending_representative_runtime_validation |
| `TFUTURESTRANSFM` | 期货账户交易明细 | 期货、黄金与贵金属 | 交易明细与历史 | 0 | 0 | 期货账户交易明细；交易明细；历史盈亏 | pending_representative_runtime_validation |
| `TFUTURESTRANSFRAME` |  | 期货、黄金与贵金属 | 交易明细与历史 | 1 | 10 | 单个合约交易明细 | pending_representative_runtime_validation |
| `TFUTURESVIEWFRAME` |  | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TGOALACCTLISTDLG` | 财务目标账户余额列表 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 0 | 0 | 财务目标账户余额列表 | pending_representative_runtime_validation |
| `TGOALCENTERFM` | 财务目标 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 6 | 0 | 财务目标；新增目标；设置；显示已过期目标；pmOperate；修改；另 1 项 | pending_representative_runtime_validation |
| `TGOALSAVEFM` | 财务目标 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 2 | 0 | 财务目标；全部账户；保存 | pending_representative_runtime_validation |
| `TGOLDACCTDLGFM` | 贵金属账户 | 期货、黄金与贵金属 | 账户配置 | 2 | 0 | 贵金属账户；自身；其它 | pending_representative_runtime_validation |
| `TGOLDBUYDLGFM` | 贵金属买入 | 期货、黄金与贵金属 | 业务交易录入 | 1 | 0 | 贵金属买入；更新产品 | pending_representative_runtime_validation |
| `TGOLDLISTFM` | 贵金属产品列表 | 期货、黄金与贵金属 | 基础资料维护 | 21 | 6 | 贵金属产品列表；显示单日所有价格；只显示持仓产品价格；操作；DBGridList；DBGridPrice；另 13 项 | pending_representative_runtime_validation |
| `TGOLDSELLDLGFM` | 贵金属卖出 | 期货、黄金与贵金属 | 业务交易录入 | 0 | 0 | 贵金属卖出 | pending_representative_runtime_validation |
| `TGOLDSTATISTICFRAME` |  | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | 6 | 9 | 获取价格；BrowseGrid；添加贵金属价格；pmOperate；当前持仓贵金属；所有交易过的贵金属 | pending_representative_runtime_validation |
| `TGOLDTRANSFM` | 贵金属交易明细 | 期货、黄金与贵金属 | 交易明细与历史 | 0 | 0 | 贵金属交易明细；交易明细；市值构成和变动；历史盈亏 | pending_representative_runtime_validation |
| `TGOLDTRANSFRAME` |  | 期货、黄金与贵金属 | 交易明细与历史 | 1 | 7 | 单只贵金属交易明细 | pending_representative_runtime_validation |
| `TGUIDEDLG` | GuideDlg | 账簿生命周期与系统壳层 | 配置与调整 | 0 | 0 | GuideDlg | pending_representative_runtime_validation |
| `THISTORYPROFITFRAME` |  | 投资公共能力 | 统计/图表/嵌入视图 | 5 | 13 | btnShowType；操作；pmOperate；导出；打印 | pending_representative_runtime_validation |
| `TIMPORTCATEGORYDLGFM` | 替换收支项目 | 导入导出 | 数据交换 | 2 | 22 | 替换收支项目；查询记录；确定替换 | pending_representative_runtime_validation |
| `TIMPORTDATAFM` | 导入数据 | 导入导出 | 数据交换 | 25 | 0 | 导入数据；账户信息；人员机构；货币信息；收支项目；收支预算；另 20 项 | pending_representative_runtime_validation |
| `TIMPORTJIAOGEDANDLGFM` | 导入股票交割单 | 导入导出 | 数据交换 | 22 | 0 | 导入股票交割单；ts1；ts2；显示方案详细内容；制表符Tab；空格；另 18 项 | pending_representative_runtime_validation |
| `TIMPORTPREVIEWFM` | 导入预览 | 导入导出 | 数据交换 | 1 | 0 | 导入预览；原始数据；准备导入的记录；导入选中的记录 | pending_representative_runtime_validation |
| `TIMPORTSELECTDLGFM` | 导入数据 | 导入导出 | 数据交换 | 3 | 0 | 导入数据；mwIconList；从文件导入；从剪贴板导入 | pending_representative_runtime_validation |
| `TIMPORTTHEMEDLGFM` | 主题数据设置 | 导入导出 | 数据交换 | 2 | 27 | 主题数据设置；设置；查询记录 | pending_representative_runtime_validation |
| `TINCEXPCAPIONDLGFM` | 备选说明 | 通用交易、流水与模板 | 业务交易录入 | 1 | 0 | 备选说明；保存 | pending_representative_runtime_validation |
| `TINCEXPDLGFM` | 日常收支 | 通用交易、流水与模板 | 业务交易录入 | 0 | 0 | 日常收支 | pending_representative_runtime_validation |
| `TINCEXPEDITFRAME` |  | 通用交易、流水与模板 | 业务交易录入 | 1 | 0 | 分期付款 | pending_representative_runtime_validation |
| `TINCEXPINSTALLMENTWIZARDDLG` | 日常支出分期 | 通用交易、流水与模板 | 业务交易录入 | 0 | 0 | 日常支出分期 | pending_representative_runtime_validation |
| `TINCEXPPLANDLGFM` | 收支计划 | 预算、提醒、规划与目标 | 业务交易录入 | 1 | 0 | 收支计划；自动执行 | pending_representative_runtime_validation |
| `TINFORMATIONDLGFM` | 资料管理 | 账户与基础资料 | 基础资料维护 | 0 | 0 | 资料管理 | representative_runtime_validation_observed |
| `TINPUTTEXTDLGFM` | InputTextDlgFm | 通用交易、流水与模板 | 配置与调整 | 1 | 0 | InputTextDlgFm；确定 | pending_representative_runtime_validation |
| `TINSTALLMENTEDITDLG` | 分期付款 | 通用交易、流水与模板 | 配置与调整 | 1 | 0 | 分期付款；保存 | pending_representative_runtime_validation |
| `TINSTALLMENTEDITFRAME` |  | 通用交易、流水与模板 | 配置与调整 | 4 | 0 | 到达还款日后自动减少未还期数；关联收支项目；btnFeeType；btnRateType | pending_representative_runtime_validation |
| `TINSTALLMENTFRAME` |  | 通用交易、流水与模板 | 配置与调整 | 6 | 15 | 新增；操作；btnShowType；mhbgData；修改；删除 | pending_representative_runtime_validation |
| `TINSUREACCTDLGFM` | 保险账户 | 保险与社会保障 | 账户配置 | 2 | 0 | 保险账户；终生有效；将保费做为收支统计 | pending_representative_runtime_validation |
| `TINSUREBALAINDLGFM` | 保险价值增加 | 保险与社会保障 | 业务交易录入 | 0 | 0 | 保险价值增加 | pending_representative_runtime_validation |
| `TINSUREBALAOUTDLGFM` | 保险价值减少 | 保险与社会保障 | 业务交易录入 | 0 | 0 | 保险价值减少 | pending_representative_runtime_validation |
| `TINSURECASHVALUEEDITDLGFM` | 保险现金价值 | 保险与社会保障 | 配置与调整 | 1 | 0 | 保险现金价值；确定 | pending_representative_runtime_validation |
| `TINSURECASHVALUEFRAME` |  | 保险与社会保障 | 配置与调整 | 4 | 2 | tsDisabled；tsEnabled；mhbgData；添加；修改；删除 | pending_representative_runtime_validation |
| `TINSUREDIVIDENDFM` | 保险分红 | 保险与社会保障 | 业务交易录入 | 0 | 0 | 保险分红 | pending_representative_runtime_validation |
| `TINSUREGETFEEDLGFM` | 保费返还 | 保险与社会保障 | 业务交易录入 | 0 | 0 | 保费返还 | pending_representative_runtime_validation |
| `TINSUREOVERDLGFM` | 退保 | 保险与社会保障 | 配置与调整 | 1 | 0 | 退保；同时终止保险账户 | pending_representative_runtime_validation |
| `TINSUREPAYFEEDLGFM` | 缴纳保费 | 保险与社会保障 | 业务交易录入 | 0 | 0 | 缴纳保费 | pending_representative_runtime_validation |
| `TINSURETRANSFM` | 保险交易明细 | 保险与社会保障 | 交易明细与历史 | 0 | 0 | 保险交易明细 | pending_representative_runtime_validation |
| `TINSURETRANSFRAME` |  | 保险与社会保障 | 交易明细与历史 | 2 | 5 | 管理现金价值；修改缴费计划 | pending_representative_runtime_validation |
| `TINSUREVIEWFRAME` |  | 保险与社会保障 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TINVESTFEEDLGFM` | 其它费用或利息 | 投资公共能力 | 业务交易录入 | 2 | 0 | 其它费用或利息；费用；利息收入 | pending_representative_runtime_validation |
| `TINVESTMENTCHARTFRAME` |  | 投资公共能力 | 统计/图表/嵌入视图 | 1 | 0 | btnType | pending_representative_runtime_validation |
| `TINVESTMENTLISTFM` | 投资一览 | 投资公共能力 | 基础资料维护 | 5 | 0 | 投资一览；tsList；tsChart；操作；btnDataChange；更新行情数据；另 2 项 | pending_representative_runtime_validation |
| `TLIFETHEMEFM` | 标签 | 账户与基础资料 | 配置与调整 | 30 | 25 | 标签；查看交易记录；查看资产；交易记录；资产账户；查找；另 26 项 | representative_runtime_validation_observed |
| `TLIMITREMINDDLG` | 限额提醒 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 9 | 0 | 限额提醒；新增提醒；操作；TreeList；新增账户余额提醒；新增信用卡透支额提醒；另 4 项 | pending_representative_runtime_validation |
| `TLOGINDIALOG` | Database Login | 登录、同步与外部服务 | 外部服务与同步 | 2 | 0 | Database Login；&OK；Cancel | pending_representative_runtime_validation |
| `TLZCASHDEPDLGFM` | 存款 | 存款与银行理财产品 | 配置与调整 | 0 | 0 | 存款 | pending_representative_runtime_validation |
| `TMAINFORM` | MainForm | 账簿生命周期与系统壳层 | 应用壳层与导航 | 99 | 0 | MainForm；资产；分析；目标；pnlToolsBar；btnMainPopupMenuCenter；另 96 项 | pending_representative_runtime_validation |
| `TMANAGEBILLDATEDLGFM` | 账单日管理 | 辅助工具与长尾能力 | 配置与调整 | 3 | 0 | 账单日管理；设置；删除；treeList | pending_representative_runtime_validation |
| `TMARGINACCTDLGFM` | 融资融券账户 | 融资融券 | 账户配置 | 0 | 0 | 融资融券账户 | pending_representative_runtime_validation |
| `TMARGININTERESTREPAYMENTSDLGFM` | 利息返还 | 融资融券 | 业务交易录入 | 0 | 0 | 利息返还 | pending_representative_runtime_validation |
| `TMARGINSTATISTICFRAME` |  | 融资融券 | 统计/图表/嵌入视图 | 8 | 11 | 获取收盘价；BrowseGrid；添加股票价格；证券代码变更；融资融券费率设置；证券费率设置；另 2 项 | pending_representative_runtime_validation |
| `TMARGINTRANSFM` | 融资融券账户交易明细 | 融资融券 | 交易明细与历史 | 0 | 0 | 融资融券账户交易明细；交易明细；历史盈亏 | pending_representative_runtime_validation |
| `TMARGINTRANSFRAME` |  | 融资融券 | 交易明细与历史 | 1 | 11 | 单只证券交易明细 | pending_representative_runtime_validation |
| `TMARGINVIEWFRAME` |  | 融资融券 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TMARKETCONSTITUTESFRAME` |  | 投资公共能力 | 统计/图表/嵌入视图 | 0 | 5 |  | parent_driven_structure_only |
| `TMARKETDEBTSTATISTICFRAME` |  | 债券 | 统计/图表/嵌入视图 | 3 | 7 | BrowseGrid；当前持仓债券；所有交易过的债券 | pending_representative_runtime_validation |
| `TMARKETDEBTTRANSFM` | 债券交易明细 | 债券 | 交易明细与历史 | 0 | 0 | 债券交易明细；交易明细；成本市值构成；历史盈亏 | pending_representative_runtime_validation |
| `TMARKETDEBTTRANSFRAME` |  | 债券 | 交易明细与历史 | 1 | 9 | 单只债券交易明细 | pending_representative_runtime_validation |
| `TMHFRAME` |  | 共享 UI 与技术支撑 | 共享技术组件 | 0 | 0 |  | not_applicable_or_parent_driven |
| `TMISCDIALOGFM` | MiscDialog | 共享 UI 与技术支撑 | 共享技术组件 | 0 | 0 | MiscDialog | not_applicable_or_parent_driven |
| `TMODIFYBILLDATEDLGFM` | 设置账单日 | 辅助工具与长尾能力 | 辅助工具 | 3 | 0 | 设置账单日；固定账单日，每月；每月最后一天是账单日；确 定 | pending_representative_runtime_validation |
| `TMONEYACCTDLGFM` | 银行理财产品账户 | 存款与银行理财产品 | 账户配置 | 2 | 0 | 银行理财产品账户；自身；其它 | pending_representative_runtime_validation |
| `TMONEYBUYDLGFM` | 银行理财产品申购 | 存款与银行理财产品 | 业务交易录入 | 0 | 0 | 银行理财产品申购 | pending_representative_runtime_validation |
| `TMONEYINFOVIEWFRAME` |  | 存款与银行理财产品 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TMONEYLISTFM` | 银行理财产品列表 | 存款与银行理财产品 | 基础资料维护 | 12 | 13 | 银行理财产品列表；操作；MHBGSecurity；新增产品；修改产品；删除产品；另 7 项 | pending_representative_runtime_validation |
| `TMONEYMATUREDLGFM` | 银行理财产品到期 | 存款与银行理财产品 | 业务交易录入 | 0 | 0 | 银行理财产品到期 | pending_representative_runtime_validation |
| `TMONEYPRODUCTSVIEWFRAME` |  | 存款与银行理财产品 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TMONEYREDEEMDLGFM` | 银行理财产品赎回 | 存款与银行理财产品 | 业务交易录入 | 0 | 0 | 银行理财产品赎回 | pending_representative_runtime_validation |
| `TMONEYSTATISTICFRAME` |  | 存款与银行理财产品 | 统计/图表/嵌入视图 | 3 | 7 | BrowseGrid；当前持仓产品；所有交易过的产品 | pending_representative_runtime_validation |
| `TMONEYTRANSFM` | 银行理财产品交易明细 | 存款与银行理财产品 | 交易明细与历史 | 0 | 0 | 银行理财产品交易明细；交易明细；市值构成；历史盈亏；产品资料 | pending_representative_runtime_validation |
| `TMONEYTRANSFRAME` |  | 存款与银行理财产品 | 交易明细与历史 | 1 | 5 | 单个产品交易明细 | pending_representative_runtime_validation |
| `TMONTHDAYFM` | 日历 | 辅助工具与长尾能力 | 辅助工具 | 0 | 0 | 日历 | pending_representative_runtime_validation |
| `TMONTHINCEXPCOLUMNCHARTFRAME` |  | 通用交易、流水与模板 | 统计/图表/嵌入视图 | 1 | 0 | btnUnit | pending_representative_runtime_validation |
| `TMWADJUSTBUTTONDROP` | mwAdjustButtonDrop | 共享 UI 与技术支撑 | 选择、筛选与查找 | 1 | 0 | mwAdjustButtonDrop；确 定 | pending_representative_runtime_validation |
| `TMWSELECTACCOUNTDROP` |  | 账户与基础资料 | 选择、筛选与查找 | 3 | 0 | 单账户；多账户；搜索；mwSelectAccountDrop；[新增账户]；确 定 | representative_runtime_validation_observed |
| `TMWSELECTCATEGORYDROP` |  | 账户与基础资料 | 选择、筛选与查找 | 3 | 0 | 支出；收入；搜索；mwSelectCategoryDrop；[新增]；[收支项目管理] | representative_runtime_validation_observed |
| `TMWSELECTTAGDROP` |  | 账户与基础资料 | 选择、筛选与查找 | 3 | 0 | 标签；mwSelectTagDrop；确 定；[新增标签] | representative_runtime_validation_observed |
| `TNEWACCTTYPEDLGFM` | 新增资产账户 | 账户与基础资料 | 账户配置 | 26 | 0 | 新增资产账户；信用卡；储蓄卡；第三方储值；基金；预收/预付；另 21 项 | representative_runtime_validation_observed |
| `TNEWACCTWIZARDCASHDLGFM` | 现金账户 | 账户与基础资料 | 账户配置 | 0 | 0 | 现金账户 | representative_runtime_validation_observed |
| `TNEWACCTWIZARDCREDITCARDDLGFM` | 信用卡账户 | 债权债务、信用与摊销 | 账户配置 | 5 | 0 | 信用卡账户；每月最后一天是账单日；固定账单日；账单日之后；固定还款日；透支提醒 | pending_representative_runtime_validation |
| `TNEWACCTWIZARDCURRENCYONECARDDLGFM` | 活期一本通 | 账户与基础资料 | 账户配置 | 0 | 0 | 活期一本通 | representative_runtime_validation_observed |
| `TNEWACCTWIZARDCURRENTDLGFM` | 活期存折银行卡 | 账户与基础资料 | 账户配置 | 0 | 0 | 活期存折银行卡 | representative_runtime_validation_observed |
| `TNEWACCTWIZARDCURRFUNDDLGFM` | 货币基金账户 | 基金与货币基金 | 账户配置 | 4 | 0 | 货币基金账户；其它账户；账户自身；投资；储蓄 | pending_representative_runtime_validation |
| `TNEWACCTWIZARDDEBTINVESTMENTDLGFM` | 网贷 | 债权债务、信用与摊销 | 账户配置 | 1 | 0 | 网贷；同时添加此平台到机构中 | pending_representative_runtime_validation |
| `TNEWACCTWIZARDDEPOSITONECARDDLGFM` | 定期一本通 | 账户与基础资料 | 账户配置 | 2 | 0 | 定期一本通；到期自动续存；btnTermType | representative_runtime_validation_observed |
| `TNEWACCTWIZARDDLGFM` | NewAcctWizardDlgFm | 账户与基础资料 | 账户配置 | 0 | 0 | NewAcctWizardDlgFm | pending_representative_runtime_validation |
| `TNEWACCTWIZARDEXCHANGEDLGFM` | 外汇交易账户 | 账户与基础资料 | 业务交易录入 | 0 | 0 | 外汇交易账户 | representative_runtime_validation_observed |
| `TNEWACCTWIZARDFIXEDDEPOSITDLGFM` | 定期存款 | 存款与银行理财产品 | 账户配置 | 2 | 0 | 定期存款；到期自动续存；btnTermType | pending_representative_runtime_validation |
| `TNEWACCTWIZARDFUTURESDLGFM` | 期货 | 期货、黄金与贵金属 | 账户配置 | 0 | 0 | 期货 | pending_representative_runtime_validation |
| `TNEWACCTWIZARDGOLDDLGFM` | 贵金属账户 | 期货、黄金与贵金属 | 账户配置 | 2 | 0 | 贵金属账户；其它账户；账户自身 | pending_representative_runtime_validation |
| `TNEWACCTWIZARDINSURECOMMERCEDLGFM` | 商业保险账户 | 保险与社会保障 | 账户配置 | 9 | 0 | 商业保险账户；人身保险；财产保险；投资分红险；将保费做为收支统计；终生有效；另 4 项 | pending_representative_runtime_validation |
| `TNEWACCTWIZARDINSURESOCIALDLGFM` | 社保账户 | 保险与社会保障 | 账户配置 | 7 | 0 | 社保账户；将保费做为收支统计；住房公积金；生育；医疗；失业；另 2 项 | pending_representative_runtime_validation |
| `TNEWACCTWIZARDMARGINDLGFM` | 融资融券 | 融资融券 | 账户配置 | 0 | 0 | 融资融券 | pending_representative_runtime_validation |
| `TNEWACCTWIZARDMONEYDLGFM` | 银行理财产品账户 | 账户与基础资料 | 账户配置 | 2 | 0 | 银行理财产品账户；其它账户；账户自身 | representative_runtime_validation_observed |
| `TNEWACCTWIZARDNMARKETDEBTDLGFM` | 债券账户 | 债券 | 账户配置 | 2 | 0 | 债券账户；其它账户；账户自身 | pending_representative_runtime_validation |
| `TNEWACCTWIZARDONECARDDLGFM` | 一卡通 | 账户与基础资料 | 账户配置 | 2 | 0 | 一卡通；创建活期子账户；创建定期子账户 | representative_runtime_validation_observed |
| `TNEWACCTWIZARDOPENFUNDDLGFM` | 开放式基金账户 | 基金与货币基金 | 账户配置 | 2 | 0 | 开放式基金账户；其它账户；账户自身 | pending_representative_runtime_validation |
| `TNEWACCTWIZARDPRACDLGFM` | 家居物品账户 | 账户与基础资料 | 账户配置 | 2 | 0 | 家居物品账户；投资；自用 | representative_runtime_validation_observed |
| `TNEWACCTWIZARDPRECIOUSMETALSTDDLGFM` | 贵金属TD账户 | 期货、黄金与贵金属 | 账户配置 | 2 | 0 | 贵金属TD账户；其它账户；账户自身 | pending_representative_runtime_validation |
| `TNEWACCTWIZARDSECURITYDLGFM` | 上市证券账户 | 证券 | 账户配置 | 3 | 0 | 上市证券账户；其它账户；账户自身；btnSecuType | pending_representative_runtime_validation |
| `TNEWACCTWIZARDTHIRDDEPOSITSDLGFM` | 支付宝、微信钱包 | 账户与基础资料 | 账户配置 | 0 | 0 | 支付宝、微信钱包 | representative_runtime_validation_observed |
| `TNEWACCTWIZARDTWOCURRCREDITDLGFM` | 双币信用卡账户 | 债权债务、信用与摊销 | 账户配置 | 6 | 0 | 双币信用卡账户；每月最后一天是账单日；固定账单日；账单日之后；固定还款日；透支提醒 | pending_representative_runtime_validation |
| `TNEWBLOCKUPDLG` | 垫付 | 债权债务、信用与摊销 | 业务交易录入 | 2 | 0 | 垫付；保存；保存并继续 | pending_representative_runtime_validation |
| `TNEWBOOKFM` | 新建账簿 | 账簿生命周期与系统壳层 | 账簿生命周期命令 | 3 | 0 | 新建账簿；建好后立即设置账簿密码；确定；更改 | pending_representative_runtime_validation |
| `TNEWDEBTBORROWDLGFM` | 借入、借出 | 债权债务、信用与摊销 | 业务交易录入 | 5 | 0 | 借入、借出；btnDeadline；btnFrequency；btnPayMode；保存并新添；保存 | pending_representative_runtime_validation |
| `TNEWRECTRANSDLGFM` | 余额调整 | 通用交易、流水与模板 | 业务交易录入 | 1 | 0 | 余额调整；btnType | pending_representative_runtime_validation |
| `TNEWREMINDDLGFM` | 今日提醒 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 8 | 0 | 今日提醒；今日不再提醒；打开账簿时自动弹出今日提醒；关闭；提醒设置；不再提醒；另 3 项 | pending_representative_runtime_validation |
| `TNEWTHEMEDLGFM` | 标签 | 账户与基础资料 | 配置与调整 | 1 | 0 | 标签；保存 | representative_runtime_validation_observed |
| `TNMARKETBONDBUYDLGFM` | 债券买入 | 债券 | 业务交易录入 | 0 | 0 | 债券买入 | pending_representative_runtime_validation |
| `TNMARKETBONDCASHAHEADDLGFM` | 债券提前兑取 | 债券 | 业务交易录入 | 0 | 0 | 债券提前兑取 | pending_representative_runtime_validation |
| `TNMARKETBONDINTERESTDLGFM` | 债券利息 | 债券 | 业务交易录入 | 0 | 0 | 债券利息 | pending_representative_runtime_validation |
| `TNMARKETBONDLISTFM` | 债券列表 | 债券 | 基础资料维护 | 11 | 10 | 债券列表；操作；MHBGSecurity；pmSecurity；miDeleteSecurity；价格历史；另 6 项 | pending_representative_runtime_validation |
| `TNMARKETBONDMATUREDLGFM` | 债券到期 | 债券 | 业务交易录入 | 0 | 0 | 债券到期 | pending_representative_runtime_validation |
| `TNMARKETBONDSELLDLGFM` | 债券卖出 | 债券 | 业务交易录入 | 0 | 0 | 债券卖出 | pending_representative_runtime_validation |
| `TNMARKETDEBTACCTDLGFM` | 债券账户 | 债券 | 账户配置 | 2 | 0 | 债券账户；自身；其它 | pending_representative_runtime_validation |
| `TNODEWRAPFORM` |  | 共享 UI 与技术支撑 | 共享技术组件 | 0 | 0 |  | not_applicable_or_parent_driven |
| `TNORMALPLANDLGFM` | 提醒 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 0 | 0 | 提醒 | pending_representative_runtime_validation |
| `TOKCANCELDIALOGFM` | OkCancelDialogFm | 共享 UI 与技术支撑 | 共享技术组件 | 1 | 0 | OkCancelDialogFm；取消 | pending_representative_runtime_validation |
| `TONLINEGETDATAFM` | 更新行情数据 | 登录、同步与外部服务 | 外部服务与同步 | 9 | 0 | 更新行情数据；获取最新行情数据；获取历史行情数据；仅获取当前持仓的；获取全部；获取持仓和历史交易过的；另 3 项 | pending_representative_runtime_validation |
| `TOPENFUNDACCTDLGFM` | 开放式基金账户 | 基金与货币基金 | 账户配置 | 2 | 0 | 开放式基金账户；自身；其它 | pending_representative_runtime_validation |
| `TOPENFUNDREMINDDLG` | 开放式基金价格提醒 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 2 | 0 | 开放式基金价格提醒；保存；更新基金 | pending_representative_runtime_validation |
| `TOPENFUNDSLISTFM` | 开放式基金列表 | 基金与货币基金 | 基础资料维护 | 22 | 8 | 开放式基金列表；显示单日所有价格；只显示持仓基金净值；操作；DBGridList；DBGridPrice；另 14 项 | pending_representative_runtime_validation |
| `TOPENFUNDSTATISTICFRAME` |  | 基金与货币基金 | 统计/图表/嵌入视图 | 6 | 9 | 获取净值；BrowseGrid；添加基金净值；开放式基金代码变更；当前持仓基金；所有交易过的基金 | pending_representative_runtime_validation |
| `TOPENFUNDTRANSFM` | 开放式基金交易明细 | 基金与货币基金 | 交易明细与历史 | 0 | 0 | 开放式基金交易明细；交易明细；市值构成和变动；历史盈亏 | pending_representative_runtime_validation |
| `TOPENFUNDTRANSFRAME` |  | 基金与货币基金 | 交易明细与历史 | 1 | 9 | 单只基金交易明细 | pending_representative_runtime_validation |
| `TOPENFUNDVIEWFRAME` |  | 基金与货币基金 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TPAGECONTRLFM` | PageContrlFM | 共享 UI 与技术支撑 | 共享技术组件 | 0 | 0 | PageContrlFM | not_applicable_or_parent_driven |
| `TPARENTPLANDLGFM` | ParentPlanDlgFm | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 3 | 0 | ParentPlanDlgFm；确定；btnRepeat；btnRemind | pending_representative_runtime_validation |
| `TPASSWORDDIALOG` | Enter password | 账簿生命周期与系统壳层 | 配置与调整 | 5 | 0 | Enter password；&OK；Cancel；&Add；&Remove；Re&move all | pending_representative_runtime_validation |
| `TPAYABLEADVANCEDLGFM` | 预收、预付 | 债权债务、信用与摊销 | 配置与调整 | 2 | 0 | 预收、预付；保存；保存并继续 | pending_representative_runtime_validation |
| `TPAYABLEMONEYTRANSDLGFM` | 预收 | 债权债务、信用与摊销 | 业务交易录入 | 0 | 0 | 预收 | pending_representative_runtime_validation |
| `TPAYABLESVIEWFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TPAYROLLINCOMEDLGFM` | 工资收入 | 通用交易、流水与模板 | 业务交易录入 | 1 | 0 | 工资收入；个人所得税计算器 | pending_representative_runtime_validation |
| `TPERSONDLG` | 人员与机构 | 账户与基础资料 | 基础资料维护 | 8 | 0 | 人员与机构；男；女；生日；btnType；btnBrithType；另 3 项 | representative_runtime_validation_observed |
| `TPERSONLISTFM` | 人员与机构 | 账户与基础资料 | 基础资料维护 | 10 | 10 | 人员与机构；DBGRID；操作；miDeleteCategory；新增；修改；另 5 项 | representative_runtime_validation_observed |
| `TPLANINSUREPAYFEEDLGFM` | 缴费计划 | 预算、提醒、规划与目标 | 业务交易录入 | 2 | 0 | 缴费计划；btnPlanFreq；确 定 | pending_representative_runtime_validation |
| `TPLANLISTDLG` | 财务计划和提醒 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 16 | 0 | 财务计划和提醒；PlanTreeList；新增计划；操作；miDeleteCategory；执行；另 11 项 | pending_representative_runtime_validation |
| `TPRACACCTDLGFM` | 物品账户 | 重大资产与家居物品 | 账户配置 | 2 | 0 | 物品账户；投资；自用 | pending_representative_runtime_validation |
| `TPRACASSETBUYDLGFM` | 物品买入 | 重大资产与家居物品 | 业务交易录入 | 0 | 0 | 物品买入 | pending_representative_runtime_validation |
| `TPRACASSETSELLDLGFM` | 物品卖出 | 重大资产与家居物品 | 业务交易录入 | 0 | 0 | 物品卖出 | pending_representative_runtime_validation |
| `TPRACBUYEDITFRAME` |  | 重大资产与家居物品 | 业务交易录入 | 1 | 0 | 分期付款 | pending_representative_runtime_validation |
| `TPRACBUYINSTALLMENTWIZARDDLG` | 物品买入分期 | 重大资产与家居物品 | 业务交易录入 | 0 | 0 | 物品买入分期 | pending_representative_runtime_validation |
| `TPRACCHANGEVALUEDLGFM` | 物品价值变更 | 重大资产与家居物品 | 配置与调整 | 0 | 0 | 物品价值变更 | pending_representative_runtime_validation |
| `TPRACDLG` | 家居物品 | 重大资产与家居物品 | 配置与调整 | 2 | 0 | 家居物品；保存；保存并继续 | pending_representative_runtime_validation |
| `TPRACGROUPVIEWFRAME` |  | 重大资产与家居物品 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TPRACINCDLGFM` | 资产投资收益 | 重大资产与家居物品 | 配置与调整 | 0 | 0 | 资产投资收益 | pending_representative_runtime_validation |
| `TPRACLISTFM` | 家居物品资料和价格 | 重大资产与家居物品 | 基础资料维护 | 24 | 4 | 家居物品资料和价格；只显示持有物品价格；按日期显示全部价格；操作；PracPrice；新增；另 16 项 | pending_representative_runtime_validation |
| `TPRACSTATISTICFRAME` |  | 重大资产与家居物品 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TPRACTRANSFM` | 物品交易明细 | 重大资产与家居物品 | 交易明细与历史 | 0 | 0 | 物品交易明细；交易明细；成本市值构成 | pending_representative_runtime_validation |
| `TPRACTRANSFRAME` |  | 重大资产与家居物品 | 交易明细与历史 | 1 | 8 | 单个物品交易明细 | pending_representative_runtime_validation |
| `TPRACTYPEDLG` | 家居物品分类 | 重大资产与家居物品 | 配置与调整 | 1 | 0 | 家居物品分类；保存 | pending_representative_runtime_validation |
| `TPRECIOUSMETALSTDACCTDLGFM` | 贵金属TD账户 | 期货、黄金与贵金属 | 账户配置 | 2 | 0 | 贵金属TD账户；自身；其它 | pending_representative_runtime_validation |
| `TPRECIOUSMETALSTDBUYDLGFM` | 贵金属TD开仓 | 期货、黄金与贵金属 | 业务交易录入 | 1 | 0 | 贵金属TD开仓；btnType | pending_representative_runtime_validation |
| `TPRECIOUSMETALSTDGOODSLISTFM` | 贵金属TD品种列表 | 期货、黄金与贵金属 | 基础资料维护 | 9 | 9 | 贵金属TD品种列表；操作；MHBGSecurity；pmSecurity；miDeleteSecurity；新增贵金属；另 4 项 | pending_representative_runtime_validation |
| `TPRECIOUSMETALSTDSELLDLGFM` | 贵金属TD平仓 | 期货、黄金与贵金属 | 业务交易录入 | 0 | 0 | 贵金属TD平仓 | pending_representative_runtime_validation |
| `TPRECIOUSMETALSTDSTATISTICFRAME` |  | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | 7 | 9 | 获取最新价格；BrowseGrid；添加贵金属价格；证券代码变更；贵金属TD品种设置；当前持仓合约；另 1 项 | pending_representative_runtime_validation |
| `TPRECIOUSMETALSTDTRANSFM` | 贵金属TD账户交易明细 | 期货、黄金与贵金属 | 交易明细与历史 | 0 | 0 | 贵金属TD账户交易明细；交易明细；历史盈亏 | pending_representative_runtime_validation |
| `TPRECIOUSMETALSTDTRANSFRAME` |  | 期货、黄金与贵金属 | 交易明细与历史 | 1 | 10 | 单个合约交易明细 | pending_representative_runtime_validation |
| `TPRECIOUSMETALSTDVIEWFRAME` |  | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TPRECIOUSVIEWFRAME` |  | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TPREPAIDEXPENSESDLGFM` | 待摊费用 | 债权债务、信用与摊销 | 业务交易录入 | 2 | 0 | 待摊费用；保存；保存并继续 | pending_representative_runtime_validation |
| `TPREPAIDEXPENSESINCEXPDLGFM` | 待摊费用 | 债权债务、信用与摊销 | 业务交易录入 | 0 | 0 | 待摊费用 | pending_representative_runtime_validation |
| `TPREPAYMENTFM` | 提前返还 | 债权债务、信用与摊销 | 业务交易录入 | 1 | 0 | 提前返还；btnType | pending_representative_runtime_validation |
| `TPREPEXPEACCTDLGFM` | 待摊费用概况 | 账户与基础资料 | 账户配置 | 0 | 0 | 待摊费用概况 | representative_runtime_validation_observed |
| `TPROGRESSFORM` | ProgressFM | 共享 UI 与技术支撑 | 共享技术组件 | 1 | 0 | ProgressFM；取消 | pending_representative_runtime_validation |
| `TPWDCHANGEFM` | 密码设置 | 账簿生命周期与系统壳层 | 配置与调整 | 2 | 0 | 密码设置；BtnOk；确定 | pending_representative_runtime_validation |
| `TPWDCHECKFM` | 密码输入 | 账簿生命周期与系统壳层 | 配置与调整 | 1 | 0 | 密码输入；确定 | pending_representative_runtime_validation |
| `TQUITEXERTIONRIGHTFM` | 放弃行权 | 融资融券 | 业务交易录入 | 0 | 0 | 放弃行权 | pending_representative_runtime_validation |
| `TRATEFM` | 存款利率 | 账户与基础资料 | 基础资料维护 | 4 | 0 | 存款利率；人民币；外币储蓄；操作；更新利率；导出；另 1 项 | pending_representative_runtime_validation |
| `TRECEIVABLESVIEWFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TRECHARGEDLGFM` | 充值 | 通用交易、流水与模板 | 业务交易录入 | 0 | 0 | 充值 | pending_representative_runtime_validation |
| `TREGISTERFORM` | 软件联网注册 | 账簿生命周期与系统壳层 | 配置与调整 | 29 | 0 | 软件联网注册；tsFirstUse；tsFreeUse；tsIndex；tsSerialNo；tsUserInfo；另 25 项 | pending_representative_runtime_validation |
| `TRELATIONNEWSTOCKRECORDSDLGFM` | 关联新股申购记录 | 证券 | 配置与调整 | 1 | 0 | 关联新股申购记录；确定 | pending_representative_runtime_validation |
| `TREMOTENOTIFICATIONDLGFM` | 手机快查设置 | 登录、同步与外部服务 | 外部服务与同步 | 2 | 0 | 手机快查设置；启用“手机快查”功能；注册账号 | pending_representative_runtime_validation |
| `TREPAYMENTTABLEFRAME` |  | 债权债务、信用与摊销 | 业务交易录入 | 5 | 0 | tsDisabled；tsEnabled；添加；修改；删除；tlRateChange；另 1 项 | pending_representative_runtime_validation |
| `TREPORTFM` | ReportFm | 报表与分析投影 | 报表查询投影 | 12 | 0 | ReportFm；tsReport；tsChart；筛选\|已更改；图表；操作；另 9 项 | pending_representative_runtime_validation |
| `TREPORTOPTIONDLGFM` | 筛选 | 报表与分析投影 | 报表查询投影 | 14 | 0 | 筛选；相关资产；人员、机构；活动类型；收支项目；标签；另 7 项 | pending_representative_runtime_validation |
| `TRESTOREBOOKFM` | 还原账簿 | 账簿生命周期与系统壳层 | 账簿生命周期命令 | 2 | 0 | 还原账簿；选择；确定 | pending_representative_runtime_validation |
| `TRPTACCOUNTINCOMESTATFRM` | 账户日常收支表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 账户日常收支表 | pending_representative_runtime_validation |
| `TRPTBSSTATFRM` | 资产负债表 | 报表与分析投影 | 报表查询投影 | 2 | 0 | 资产负债表；统计方式；统计到 | pending_representative_runtime_validation |
| `TRPTCASHWASTEFM` | 现金流表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 现金流表 | pending_representative_runtime_validation |
| `TRPTCREDITDEBTSTATFM` | 债权债务表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 债权债务表 | pending_representative_runtime_validation |
| `TRPTDEBTINVESTMENTINVESTYKFORM` | 网贷盈亏一览表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 网贷盈亏一览表 | pending_representative_runtime_validation |
| `TRPTEXCHANGE6FM` | 外汇交易一览表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 外汇交易一览表 | pending_representative_runtime_validation |
| `TRPTFINANCIALPRODUCTSFM` | 银行理财产品收益率表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 银行理财产品收益率表 | pending_representative_runtime_validation |
| `TRPTFUNDSAVAILABLEFM` | 可用资金表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 可用资金表 | pending_representative_runtime_validation |
| `TRPTFUNDTRENDFM` | 开放式基金市值大势图 | 报表与分析投影 | 报表查询投影 | 3 | 0 | 开放式基金市值大势图；资产总值；基金市值；资金余额 | pending_representative_runtime_validation |
| `TRPTINCEXPCOMPAREFM` | 两段时间收支对比表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 两段时间收支对比表 | pending_representative_runtime_validation |
| `TRPTINCEXPZSTOVFM` | 收支走势图 | 报表与分析投影 | 报表查询投影 | 1 | 0 | 收支走势图；btnDateType | pending_representative_runtime_validation |
| `TRPTINCOMELISTFM` | 日常收支明细表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 日常收支明细表 | pending_representative_runtime_validation |
| `TRPTINCOMESTATFRM` | 日常收支表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 日常收支表 | pending_representative_runtime_validation |
| `TRPTINVESTINCOMEFM` | 投资收益一览表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 投资收益一览表 | pending_representative_runtime_validation |
| `TRPTINVESTMENTPERFORMANCESTATFM` | 投资收益率统计表 | 报表与分析投影 | 报表查询投影 | 1 | 0 | 投资收益率统计表；btnMode | pending_representative_runtime_validation |
| `TRPTINVESTVIEWFM` | 投资一览表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 投资一览表 | pending_representative_runtime_validation |
| `TRPTMONTHASSETFM` | 月资产走势图 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 月资产走势图 | pending_representative_runtime_validation |
| `TRPTMONTHAVERAGEINCEXPFM` | 月平均收支表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 月平均收支表 | pending_representative_runtime_validation |
| `TRPTOPENFUNDINVESTFM` | 开放式基金投资一览表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 开放式基金投资一览表 | pending_representative_runtime_validation |
| `TRPTOPENFUNDINVESTLOSSFM` | 开放式基金费用及盈亏一览表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 开放式基金费用及盈亏一览表 | pending_representative_runtime_validation |
| `TRPTSECURITINVESTFM` | 证券投资一览表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 证券投资一览表 | pending_representative_runtime_validation |
| `TRPTSECURITINVESTLOSSFM` | 证券费用及盈亏一览表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 证券费用及盈亏一览表 | pending_representative_runtime_validation |
| `TRPTSTOCKTRENDFM` | 证券市值大势图 | 报表与分析投影 | 报表查询投影 | 5 | 0 | 证券市值大势图；资产总值；证券市值；资金余额；上证指数；深证成指 | pending_representative_runtime_validation |
| `TRPTTAGINCOMESTATFRM` | 标签日常收支表 | 报表与分析投影 | 报表查询投影 | 0 | 0 | 标签日常收支表 | pending_representative_runtime_validation |
| `TRPTYEARINCEXPFORM` | 收支统计表 | 报表与分析投影 | 报表查询投影 | 1 | 0 | 收支统计表；btnDateType | pending_representative_runtime_validation |
| `TRZFRMCUSTOMIZETOOLBAR` | Customize Toolbar | 共享 UI 与技术支撑 | 配置与调整 | 5 | 0 | Customize Toolbar；Close；LstControls；CbxTextOptions；MoveUp；MoveDown | pending_representative_runtime_validation |
| `TSECURITYACCTDLGFM` | 证券账户 | 证券 | 账户配置 | 3 | 0 | 证券账户；自身；其它；btnSecuType | pending_representative_runtime_validation |
| `TSECURITYCODECONVERTFM` | 代码变更 | 证券 | 配置与调整 | 1 | 0 | 代码变更；确定 | pending_representative_runtime_validation |
| `TSECURITYLISTFM` | 证券资料 | 证券 | 基础资料维护 | 38 | 6 | 证券资料；显示单日所有价格；只显示持仓股票价格；操作；DBGridList；DBGridPrice；另 30 项 | pending_representative_runtime_validation |
| `TSECURITYREMINDDLG` | 证券市价提醒 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 2 | 0 | 证券市价提醒；保存；更新证券 | pending_representative_runtime_validation |
| `TSECURITYSTATISTICFRAME` |  | 证券 | 统计/图表/嵌入视图 | 8 | 11 | 获取收盘价；BrowseGrid；添加股票价格；证券代码变更；导入股票交割单；费率设置；另 2 项 | pending_representative_runtime_validation |
| `TSECURITYTRANSFM` | 上市证券交易列表 | 证券 | 交易明细与历史 | 0 | 0 | 上市证券交易列表；交易明细；市值构成和变动；历史盈亏 | pending_representative_runtime_validation |
| `TSECURITYTRANSFRAME` |  | 证券 | 交易明细与历史 | 1 | 9 | 单只证券交易明细 | pending_representative_runtime_validation |
| `TSELECTDATERANGEDLGFM` | 自定义日期 | 共享 UI 与技术支撑 | 选择、筛选与查找 | 1 | 0 | 自定义日期；tsDay；tsMonth；tsQuarter；tsYear；确定 | pending_representative_runtime_validation |
| `TSELECTREPETITIONFREQUENCYDLGFM` | SelectRepetitionFrequencyDlgFm | 预算、提醒、规划与目标 | 选择、筛选与查找 | 2 | 0 | SelectRepetitionFrequencyDlgFm；btnType；确定 | pending_representative_runtime_validation |
| `TSELECTSECURITIESCODEDLGFM` | 选择证券 | 证券 | 选择、筛选与查找 | 2 | 0 | 选择证券；确定；更新证券 | pending_representative_runtime_validation |
| `TSELECTTAGDLGFM` | 选择标签 | 账户与基础资料 | 选择、筛选与查找 | 1 | 0 | 选择标签；确定 | representative_runtime_validation_observed |
| `TSELECTTHEMEDLGFM` | SelectThemeDlgFm | 账户与基础资料 | 选择、筛选与查找 | 0 | 0 | SelectThemeDlgFm | pending_representative_runtime_validation |
| `TSELECTTRANSTYPEDLGFM` | 选择交易类型 | 通用交易、流水与模板 | 选择、筛选与查找 | 1 | 0 | 选择交易类型；确定 | pending_representative_runtime_validation |
| `TSELLCOUPONSREPAYMENTDLGFM` | 卖券还款 | 融资融券 | 业务交易录入 | 1 | 0 | 卖券还款；显示费用详情 | pending_representative_runtime_validation |
| `TSHORTCUTMANAGEDLGFM` | 快捷键设置 | 账簿生命周期与系统壳层 | 配置与调整 | 17 | 0 | 快捷键设置；启用老板键；确定；btnF1；btnF2；tlMenuShortCut；另 2 项 | pending_representative_runtime_validation |
| `TSHORTSELLINGDLGFM` | 融券卖出 | 融资融券 | 业务交易录入 | 2 | 0 | 融券卖出；显示费用详情；更新代码 | pending_representative_runtime_validation |
| `TSOCIALSECURITYSTATISTICFRAME` |  | 保险与社会保障 | 统计/图表/嵌入视图 | 1 | 3 | 删除 | pending_representative_runtime_validation |
| `TSOCIALSECURITYTRANSFM` | 社会保险账户交易明细 | 保险与社会保障 | 交易明细与历史 | 0 | 0 | 社会保险账户交易明细；交易明细；现金价值；账户概况 | pending_representative_runtime_validation |
| `TSOFTINDEXCENTERFORM` | 概况 | 辅助工具与长尾能力 | 应用壳层与导航 | 17 | 0 | 概况；llTitle；操作；更新行情；诊断；pnlFinancialDiagnosis_Close；另 12 项 | pending_representative_runtime_validation |
| `TSORTSOFTINDEXCENTERDLGFM` | 调整概况显示顺序 | 辅助工具与长尾能力 | 配置与调整 | 1 | 0 | 调整概况显示顺序；确定 | pending_representative_runtime_validation |
| `TSPLASHFORM` |  | 账簿生命周期与系统壳层 | 配置与调整 | 0 | 0 |  | not_applicable_or_parent_driven |
| `TSPLITINCEXPDLGFM` | 分拆收支 | 通用交易、流水与模板 | 业务交易录入 | 0 | 0 | 分拆收支 | pending_representative_runtime_validation |
| `TSTATISTICFRAME` |  | 共享 UI 与技术支撑 | 统计/图表/嵌入视图 | 10 | 0 | 操作；所有；余额调整；持仓调整；查看账户资料；导出；另 3 项 | pending_representative_runtime_validation |
| `TSTATISTICGRIDFRAME` |  | 共享 UI 与技术支撑 | 统计/图表/嵌入视图 | 0 | 0 |  | not_applicable_or_parent_driven |
| `TSTATISTICTREEFRMAE` |  | 共享 UI 与技术支撑 | 统计/图表/嵌入视图 | 2 | 0 | 全部展开；全部折叠 | pending_representative_runtime_validation |
| `TSTOCKBONDMATUREDLGFM` | 债券到期 | 债券 | 业务交易录入 | 0 | 0 | 债券到期 | pending_representative_runtime_validation |
| `TSTOCKBUYDLGFM` | 证券买入 | 证券 | 业务交易录入 | 2 | 0 | 证券买入；显示费用详情；更新代码 | pending_representative_runtime_validation |
| `TSTOCKDIVIDDLGFM` | 送股/缩股 | 证券 | 业务交易录入 | 0 | 0 | 送股/缩股 | pending_representative_runtime_validation |
| `TSTOCKINTERESTDLGFM` | 现金红利 | 证券 | 业务交易录入 | 1 | 0 | 现金红利；btnType | pending_representative_runtime_validation |
| `TSTOCKMARKBUYDLGFM` | 中签确认 | 证券 | 业务交易录入 | 3 | 0 | 中签确认；申购证券为可分离债；中签；确 定 | pending_representative_runtime_validation |
| `TSTOCKORDERBUYDLGFM` | 新股申购 | 证券 | 业务交易录入 | 1 | 0 | 新股申购；更新代码 | pending_representative_runtime_validation |
| `TSTOCKQUOTADLGFM` | 配股 | 证券 | 配置与调整 | 0 | 0 | 配股 | pending_representative_runtime_validation |
| `TSTOCKSELLDLGFM` | 证券卖出 | 证券 | 业务交易录入 | 2 | 0 | 证券卖出；显示费用详情；btnType | pending_representative_runtime_validation |
| `TSTOCKVIEWFRAME` |  | 证券 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TSYNCUSERDATAFM` | 同步 | 登录、同步与外部服务 | 外部服务与同步 | 8 | 0 | 同步；我同意；双向同步；单向上传；关闭账簿时自动同步；同步条款；另 3 项 | pending_representative_runtime_validation |
| `TSYNCUSERREGISTERFM` | 注册同步账号 | 登录、同步与外部服务 | 外部服务与同步 | 1 | 0 | 注册同步账号；注册 | pending_representative_runtime_validation |
| `TSYSTEMSETTINGSFM` | 系统设置 | 账簿生命周期与系统壳层 | 配置与调整 | 28 | 0 | 系统设置；系统；网络；账簿备份；授权；高级；另 28 项 | pending_representative_runtime_validation |
| `TTEMPLATEDLGFM` | 批量记账 | 通用交易、流水与模板 | 配置与调整 | 3 | 0 | 批量记账；生成收支记录；删除模板；存为模板 | pending_representative_runtime_validation |
| `TTHEMEUIFM` | ThemeUIFm | 账户与基础资料 | 配置与调整 | 1 | 0 | ThemeUIFm；启动画面；对话框图片；主窗口图片；主窗口工具栏图片；功能区图片；另 2 项 | pending_representative_runtime_validation |
| `TTHIRDDEPOSITSACCTDLGFM` | 第三方储值 | 账户与基础资料 | 账户配置 | 0 | 0 | 第三方储值 | representative_runtime_validation_observed |
| `TTHIRDDEPOSITSTRANSFM` | 支付宝交易明细 | 通用交易、流水与模板 | 交易明细与历史 | 0 | 0 | 支付宝交易明细 | pending_representative_runtime_validation |
| `TTRANSACTIONPLANDLGFM` | 交易计划 | 预算、提醒、规划与目标 | 预算/提醒/规划工作流 | 0 | 0 | 交易计划 | pending_representative_runtime_validation |
| `TTRANSDLGFM` | TransDlgFm | 通用交易、流水与模板 | 业务交易录入 | 4 | 0 | TransDlgFm；保存并新添；确定；查看附件；添加删除附件 | pending_representative_runtime_validation |
| `TTRANSFERLISTTEMPLATEFRAME` |  | 通用交易、流水与模板 | 业务交易录入 | 0 | 0 |  | parent_driven_structure_only |
| `TTRANSFERTEMPLATEDLGFM` | 批量转账 | 通用交易、流水与模板 | 业务交易录入 | 3 | 0 | 批量转账；生成转账记录；删除模板；存为模板 | pending_representative_runtime_validation |
| `TTRANSFRAME` |  | 通用交易、流水与模板 | 交易明细与历史 | 31 | 15 | 操作；记账；批量操作；DBGrid；pmRightbtn；批量操作模式；另 23 项 | pending_representative_runtime_validation |
| `TTRANSLISTTEMPLATEFRAME` |  | 通用交易、流水与模板 | 配置与调整 | 0 | 0 |  | parent_driven_structure_only |
| `TUNEARNEDVIEWFRAME` |  | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 | 0 |  | parent_driven_structure_only |
| `TUPDATEVERIFYCODEFM` | 修改序列号保护信息 | 账簿生命周期与系统壳层 | 配置与调整 | 1 | 0 | 修改序列号保护信息；确定 | pending_representative_runtime_validation |
| `TUSABLEMONEYCHARTFRAME` |  | 报表与分析投影 | 报表查询投影 | 0 | 0 |  | parent_driven_structure_only |
| `TVIEWFRAME` |  | 共享 UI 与技术支撑 | 统计/图表/嵌入视图 | 0 | 0 |  | not_applicable_or_parent_driven |
| `TWASTEBOOKFM` | 财务记录 | 通用交易、流水与模板 | 交易明细与历史 | 34 | 26 | 财务记录；查找；操作；收支\|流水；批量操作；Grid；另 27 项 | pending_representative_runtime_validation |
| `TXFERPLANDLGFM` | 转账计划 | 预算、提醒、规划与目标 | 业务交易录入 | 1 | 0 | 转账计划；自动执行 | pending_representative_runtime_validation |

## 5. 特殊覆盖状态

### 5.1 内部或实验入口

| 资源 | 标题 | 当前处理 |
| --- | --- | --- |
| `TAIPANELDLG` | AI | 保留资源与命令证据；动态确认可达性和业务价值后再决定是否进入正式产品范围 |
| `TCONSOLEFM` | 控制台 | 保留资源与命令证据；动态确认可达性和业务价值后再决定是否进入正式产品范围 |

### 5.2 父窗体驱动的无文案嵌入视图

这些框架本身没有标题、命令或静态选项，功能语义来自父窗体装配、字段绑定或运行时数据源。不能把它们当成独立页面，也不能因无文案而删除。

| 资源 | 业务域 | 角色 | 字段数 |
| --- | --- | --- | ---: |
| `TADVANCESVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 |
| `TALIPAYVIEWFRAME` | 通用交易、流水与模板 | 统计/图表/嵌入视图 | 0 |
| `TASSETSCONSTITUTECHARTFRAME` | 重大资产与家居物品 | 统计/图表/嵌入视图 | 0 |
| `TASSETSMARKETCONSTITUTESFRAME` | 重大资产与家居物品 | 统计/图表/嵌入视图 | 0 |
| `TASSETVIEWFRAME` | 重大资产与家居物品 | 统计/图表/嵌入视图 | 0 |
| `TBONDSMARKETCONSTITUTESFRAME` | 债券 | 统计/图表/嵌入视图 | 0 |
| `TBONDSVIEWFRAME` | 债券 | 统计/图表/嵌入视图 | 0 |
| `TCARDVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 |
| `TCASHVIEWFRAME` | 通用交易、流水与模板 | 统计/图表/嵌入视图 | 0 |
| `TCURRDEPOSITSVIEWFRAME` | 存款与银行理财产品 | 统计/图表/嵌入视图 | 0 |
| `TCURRFUNDMARKETCONSTITUTESFRAME` | 基金与货币基金 | 统计/图表/嵌入视图 | 0 |
| `TCURRFUNDVIEWFRAME` | 基金与货币基金 | 统计/图表/嵌入视图 | 0 |
| `TDEBTINVESTMENTACCTLISTFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 8 |
| `TDEBTINVESTMENTTRANSFRAME` | 债权债务、信用与摊销 | 交易明细与历史 | 7 |
| `TDEBTINVESTMENTVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 |
| `TDEFERREDVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 |
| `TEXCHANGEMARKETCONSTITUTESFRAME` | 外汇 | 统计/图表/嵌入视图 | 0 |
| `TEXCHANGEVIEWFRAME` | 外汇 | 统计/图表/嵌入视图 | 0 |
| `TFIXDEPOSITSVIEWFRAME` | 存款与银行理财产品 | 统计/图表/嵌入视图 | 0 |
| `TFUTURESVIEWFRAME` | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | 0 |
| `TINSUREVIEWFRAME` | 保险与社会保障 | 统计/图表/嵌入视图 | 0 |
| `TMARGINVIEWFRAME` | 融资融券 | 统计/图表/嵌入视图 | 0 |
| `TMARKETCONSTITUTESFRAME` | 投资公共能力 | 统计/图表/嵌入视图 | 5 |
| `TMONEYINFOVIEWFRAME` | 存款与银行理财产品 | 统计/图表/嵌入视图 | 0 |
| `TMONEYPRODUCTSVIEWFRAME` | 存款与银行理财产品 | 统计/图表/嵌入视图 | 0 |
| `TOPENFUNDVIEWFRAME` | 基金与货币基金 | 统计/图表/嵌入视图 | 0 |
| `TPAYABLESVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 |
| `TPRACGROUPVIEWFRAME` | 重大资产与家居物品 | 统计/图表/嵌入视图 | 0 |
| `TPRACSTATISTICFRAME` | 重大资产与家居物品 | 统计/图表/嵌入视图 | 0 |
| `TPRECIOUSMETALSTDVIEWFRAME` | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | 0 |
| `TPRECIOUSVIEWFRAME` | 期货、黄金与贵金属 | 统计/图表/嵌入视图 | 0 |
| `TRECEIVABLESVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 |
| `TSTOCKVIEWFRAME` | 证券 | 统计/图表/嵌入视图 | 0 |
| `TTRANSFERLISTTEMPLATEFRAME` | 通用交易、流水与模板 | 业务交易录入 | 0 |
| `TTRANSLISTTEMPLATEFRAME` | 通用交易、流水与模板 | 配置与调整 | 0 |
| `TUNEARNEDVIEWFRAME` | 债权债务、信用与摊销 | 统计/图表/嵌入视图 | 0 |
| `TUSABLEMONEYCHARTFRAME` | 报表与分析投影 | 报表查询投影 | 0 |

## 6. 对开发需求的约束

1. 每个业务窗体必须对应应用命令、查询端口或配置端口，UI 不得直接访问 SQLite 表。
2. 同一业务域中的录入窗体、交易明细、统计视图和报表共享领域对象及金额/数量/汇率口径。
3. 技术支撑窗体不单独形成业务模块，但其筛选、选择、日期、进度和命令状态能力必须由共享组件承接。
4. 旧窗体名仅用于追溯；新系统可以合并重复页面，但合并后必须保留矩阵中的功能信号和数据流结果。
5. 删除旧功能或将多个窗体合并为一个工作流时，验收记录必须回指本矩阵中的全部相关资源。
6. 代表性动态验证优先覆盖有命令的业务表面，再覆盖父窗体驱动的嵌入式统计和技术组件。

## 7. 尚未证明的部分

- 菜单可达性、动态启用条件和窗口跳转
- 每个事件处理器的校验、确认、级联与持久化副作用
- 交易、投资、预算、规划和报表的真实计算结果
- 导入导出、备份还原、附件和同步的真实格式与协议结果

这些项目继续由 `runtime-validation-scenarios.md` 管理；不得因为静态覆盖率达到 100% 就宣称动态功能完全兼容。
