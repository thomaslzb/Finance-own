# MoneyHome8 旧窗体到 Rust 目标 UI 归并图

本设计不按 Delphi 的 `460` 个窗体逐一复刻。新系统按稳定业务边界组织页面，
但通过 `execution_id` 保留每个旧窗体、命令、事件和动态验收结果的完整追溯。

## 1. 归并结果

| 项目 | 数量 |
| --- | ---: |
| 旧运行时窗体 | 460 |
| Rust 目标分区 | 11 |
| 目标页面族 | 40 |
| 可交互控件守恒 | 1407 |
| 事件处理器守恒 | 2000 |
| 高风险事件守恒 | 502 |
| 归入共享投资框架的旧子域 / 窗体 | 10 / 197 |

完整逐窗体映射见 [target-ui-consolidation-map.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\target-ui-consolidation-map.json)。

## 2. 设计原则

- 旧窗体是证据和验收来源，不是新架构的模块边界。
- 证券、基金、债券、外汇、期货、贵金属、保险和重大资产共享投资账户、交易、流水、统计和配置页面框架。
- 各投资子域通过资产类型、字段定义、校验策略、费用策略和计算策略表达差异，不复制整套 UI。
- `28` 个报表窗体归入报表工作区，继续保留独立报表定义、列、筛选、分组、图表和导出合同。
- 技术支撑窗体改为共享组件；嵌入视图并入已确认宿主；内部或实验入口单独作范围决策。
- 合并页面不能删除旧命令；每个 `execution_id` 都必须在动态队列中关闭。

## 3. 目标分区

| 分区 | 目标页面族 | 旧窗体 | 控件 | 事件 | 高风险 | Rust 模块 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 账簿与应用壳层 | 3 | 15 | 193 | 171 | 35 | `ledger`, `app::ledger`, `ui::shell` |
| 账户与基础资料 | 6 | 41 | 190 | 225 | 61 | `accounts`, `master_data`, `ui::accounts` |
| 通用交易 | 5 | 38 | 118 | 254 | 72 | `transactions`, `app::transactions`, `ui::transactions` |
| 债权债务与信用 | 5 | 54 | 78 | 156 | 31 | `investments::debt`, `transactions`, `ui::debts` |
| 投资与扩展资产 | 7 | 197 | 441 | 734 | 190 | `investments`, `reports`, `ui::investments` |
| 预算、提醒、规划与目标 | 3 | 42 | 141 | 153 | 60 | `planning`, `ui::planning` |
| 报表与分析 | 1 | 28 | 39 | 31 | 5 | `reports`, `app::reporting`, `ui::reports` |
| 导入导出 | 1 | 7 | 83 | 72 | 18 | `import_export`, `ui::import_export` |
| 同步与外部服务 | 1 | 5 | 22 | 26 | 7 | `sync`, `ui::sync` |
| 辅助工具 | 4 | 14 | 67 | 89 | 18 | `tools`, `ui::tools` |
| 共享 UI 组件 | 4 | 19 | 35 | 89 | 5 | `app::command_state`, `ui::shared` |

## 4. 目标页面族

| 目标页面族 | UI 形态 | 旧窗体 | 控件 / 事件 / 高风险 | 应用服务 |
| --- | --- | ---: | --- | --- |
| `ui.ledger_shell.ledger-workflow`<br>账簿与应用壳层 - 账簿生命周期 | `wizard_or_dialog`<br>`/ledger-workflow` | 4 | 10 / 11 / 4 | `LedgerLifecycleService` |
| `ui.ledger_shell.settings`<br>账簿与应用壳层 - 配置 | `settings_page_or_dialog`<br>`/settings` | 9 | 83 / 62 / 14 | `SettingsService` |
| `ui.ledger_shell.shell`<br>账簿与应用壳层 - 应用壳层 | `full_page_shell`<br>`/shell` | 2 | 100 / 98 / 17 | `ShellCoordinator` |
| `ui.accounts_master_data.account-workflow`<br>账户与基础资料 - 账户配置 | `wizard_or_drawer`<br>`/accounts/account-workflow` | 18 | 70 / 50 / 20 | `AccountCommandService` |
| `ui.accounts_master_data.catalog`<br>账户与基础资料 - 目录与基础资料 | `management_page`<br>`/accounts/catalog` | 8 | 72 / 70 / 20 | `CatalogService` |
| `ui.accounts_master_data.entry`<br>账户与基础资料 - 业务录入 | `form_drawer_or_dialog`<br>`/accounts/entry` | 1 | 0 / 6 / 2 | `TransactionCommandService` |
| `ui.accounts_master_data.overview`<br>账户与基础资料 - 概览与投影 | `page_or_embedded_panel`<br>`/accounts/overview` | 1 | 0 / 0 / 0 | `ProjectionQueryService` |
| `ui.accounts_master_data.selector`<br>账户与基础资料 - 选择器与筛选 | `shared_selector`<br>`/accounts/selector` | 5 | 10 / 39 / 6 | `SelectionQueryService` |
| `ui.accounts_master_data.settings`<br>账户与基础资料 - 配置 | `settings_page_or_dialog`<br>`/accounts/settings` | 8 | 38 / 60 / 13 | `SettingsService` |
| `ui.transactions.entry`<br>通用交易 - 业务录入 | `form_drawer_or_dialog`<br>`/transactions/entry` | 15 | 22 / 108 / 36 | `TransactionCommandService` |
| `ui.transactions.history`<br>通用交易 - 流水与历史 | `data_grid_page`<br>`/transactions/history` | 7 | 69 / 95 / 21 | `TransactionQueryService` |
| `ui.transactions.overview`<br>通用交易 - 概览与投影 | `page_or_embedded_panel`<br>`/transactions/overview` | 4 | 2 / 4 / 0 | `ProjectionQueryService` |
| `ui.transactions.selector`<br>通用交易 - 选择器与筛选 | `shared_selector`<br>`/transactions/selector` | 4 | 10 / 10 / 2 | `SelectionQueryService` |
| `ui.transactions.settings`<br>通用交易 - 配置 | `settings_page_or_dialog`<br>`/transactions/settings` | 8 | 15 / 37 / 13 | `SettingsService` |
| `ui.debts_credit.account-workflow`<br>债权债务与信用 - 账户配置 | `wizard_or_drawer`<br>`/debts/account-workflow` | 8 | 29 / 20 / 0 | `AccountCommandService` |
| `ui.debts_credit.entry`<br>债权债务与信用 - 业务录入 | `form_drawer_or_dialog`<br>`/debts/entry` | 17 | 20 / 81 / 20 | `TransactionCommandService` |
| `ui.debts_credit.history`<br>债权债务与信用 - 流水与历史 | `data_grid_page`<br>`/debts/history` | 6 | 3 / 9 / 1 | `TransactionQueryService` |
| `ui.debts_credit.overview`<br>债权债务与信用 - 概览与投影 | `page_or_embedded_panel`<br>`/debts/overview` | 15 | 18 / 21 / 4 | `ProjectionQueryService` |
| `ui.debts_credit.settings`<br>债权债务与信用 - 配置 | `settings_page_or_dialog`<br>`/debts/settings` | 8 | 8 / 25 / 6 | `SettingsService` |
| `ui.investments.account-workflow`<br>投资与扩展资产 - 账户配置 | `wizard_or_drawer`<br>`/investments/account-workflow` | 23 | 56 / 43 / 4 | `AccountCommandService` |
| `ui.investments.catalog`<br>投资与扩展资产 - 目录与基础资料 | `management_page`<br>`/investments/catalog` | 11 | 182 / 193 / 50 | `CatalogService` |
| `ui.investments.entry`<br>投资与扩展资产 - 业务录入 | `form_drawer_or_dialog`<br>`/investments/entry` | 64 | 47 / 296 / 67 | `TransactionCommandService` |
| `ui.investments.history`<br>投资与扩展资产 - 流水与历史 | `data_grid_page`<br>`/investments/history` | 28 | 14 / 23 / 1 | `TransactionQueryService` |
| `ui.investments.overview`<br>投资与扩展资产 - 概览与投影 | `page_or_embedded_panel`<br>`/investments/overview` | 39 | 74 / 68 / 20 | `ProjectionQueryService` |
| `ui.investments.selector`<br>投资与扩展资产 - 选择器与筛选 | `shared_selector`<br>`/investments/selector` | 1 | 2 / 2 / 2 | `SelectionQueryService` |
| `ui.investments.settings`<br>投资与扩展资产 - 配置 | `settings_page_or_dialog`<br>`/investments/settings` | 31 | 66 / 109 / 46 | `SettingsService` |
| `ui.planning.entry`<br>预算、提醒、规划与目标 - 业务录入 | `form_drawer_or_dialog`<br>`/planning/entry` | 10 | 13 / 22 / 9 | `TransactionCommandService` |
| `ui.planning.selector`<br>预算、提醒、规划与目标 - 选择器与筛选 | `shared_selector`<br>`/planning/selector` | 1 | 2 / 1 / 1 | `SelectionQueryService` |
| `ui.planning.workflow`<br>预算、提醒、规划与目标 - 规划工作流 | `guided_workflow`<br>`/planning/workflow` | 31 | 126 / 130 / 50 | `PlanningService` |
| `ui.reports.report-workspace`<br>报表与分析 - 报表工作区 | `report_definition`<br>`/reports/report-workspace` | 28 | 39 / 31 / 5 | `ReportQueryService` |
| `ui.data_exchange.exchange-workflow`<br>导入导出 - 数据交换 | `guided_workflow`<br>`/data-exchange/exchange-workflow` | 7 | 83 / 72 / 18 | `DataExchangeService` |
| `ui.sync.adapter-workspace`<br>同步与外部服务 - 外部适配器 | `settings_and_status_page`<br>`/sync/adapter-workspace` | 5 | 22 / 26 / 7 | `ExternalAdapterService` |
| `ui.tools.component`<br>辅助工具 - 共享组件 | `shared_component`<br>`/tools/component` | 1 | 0 / 5 / 0 | `SharedUiService` |
| `ui.tools.settings`<br>辅助工具 - 配置 | `settings_page_or_dialog`<br>`/tools/settings` | 3 | 9 / 9 / 5 | `SettingsService` |
| `ui.tools.shell`<br>辅助工具 - 应用壳层 | `full_page_shell`<br>`/tools/shell` | 1 | 17 / 23 / 2 | `ShellCoordinator` |
| `ui.tools.tool`<br>辅助工具 - 工具 | `tool_dialog`<br>`/tools/tool` | 9 | 41 / 52 / 11 | `ToolService` |
| `ui.shared_ui.component`<br>共享 UI 组件 - 共享组件 | `shared_component`<br>`component://shared/component` | 8 | 7 / 24 / 0 | `SharedUiService` |
| `ui.shared_ui.overview`<br>共享 UI 组件 - 概览与投影 | `page_or_embedded_panel`<br>`component://shared/overview` | 4 | 12 / 29 / 2 | `ProjectionQueryService` |
| `ui.shared_ui.selector`<br>共享 UI 组件 - 选择器与筛选 | `shared_selector`<br>`component://shared/selector` | 5 | 7 / 24 / 3 | `SelectionQueryService` |
| `ui.shared_ui.settings`<br>共享 UI 组件 - 配置 | `settings_page_or_dialog`<br>`component://shared/settings` | 2 | 9 / 12 / 0 | `SettingsService` |

## 5. 开发和验收约束

1. 每个目标页面族使用应用服务访问领域和仓储，UI 不直接写 SQLite。
2. 同一页面族中的资产类型差异通过类型化策略或专属扩展对象表达，不使用所有字段可空的大对象。
3. `legacy_form_mappings` 是功能一致性的追溯基线；合并页面完成时必须列出覆盖的全部 `execution_id`。
4. 动态执行记录未关闭前，目标页面族只能标记为结构覆盖，不能标记为行为兼容。
5. 页面族的 Rust 模块和应用服务是建议边界；动态结果可调整规则，但不能丢弃旧功能证据。
