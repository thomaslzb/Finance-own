# MoneyHome8 全量动态执行队列

本队列把静态证据转换为逐窗体可勾选的动态巡检工作。它不以代表性场景替代全量覆盖，
并要求每次运行结果使用统一记录 Schema 保存到 `artifacts/runtime-validation/`。

## 1. 覆盖对账

| 项目 | 数量 |
| --- | ---: |
| 执行批次 | 20 |
| 运行时窗体 | 460 |
| 可交互控件 | 1407 |
| 事件处理器 | 2000 |
| 高风险事件候选 | 502 |
| 含高风险事件的窗体 | 225 |
| 嵌入视图及已解析宿主 | 37 / 37 |

机器可执行明细见 [runtime-execution-queue.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-execution-queue.json)。
观察结果必须符合 [runtime-observation-record.schema.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-observation-record.schema.json)，
人工记录格式见 [runtime-observation-record-template.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-observation-record-template.md)。

## 2. 执行规则

1. `P0` 先执行写入、删除、文件、报表、账户、规划和内部入口；`P1` 执行业务视图；`P2` 通过宿主间接验证技术组件。
2. 每个窗体必须按 `states_to_capture` 建立空数据、有数据、选择、错误、取消或回滚状态；不适用状态要写明依据。
3. 嵌入视图必须从 `ultimate_hosts` 指定的最终宿主进入，不把 Frame 当作独立窗口寻找。
4. 每个命令记录初始启用状态、触发方式、提示、数据前后差异、文件副作用和 Rust 边界结论。
5. 删除或清除操作必须在确认动作前保存证据；实际确认仍遵守当前桌面自动化的动作时确认要求。
6. 单个条目只有满足 `completion_requirements` 并回填 PRD、数据流和验收标准后才能改为 `completed`。

## 3. 批次摘要

| 顺序 | 批次 | 业务域 | 窗体 | 可交互控件 | 事件 | 高风险事件 | P0/P1/P2 |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `B01-system_shell` | 账簿生命周期与系统壳层 | 15 | 193 | 171 | 35 | 11/3/1 |
| 2 | `B02-accounts_master_data` | 账户与基础资料 | 41 | 190 | 225 | 61 | 36/5/0 |
| 3 | `B03-transactions` | 通用交易、流水与模板 | 38 | 118 | 254 | 72 | 25/13/0 |
| 4 | `B04-debts_credit` | 债权债务、信用与摊销 | 54 | 78 | 156 | 31 | 34/20/0 |
| 5 | `B05-financial_products` | 存款与银行理财产品 | 19 | 29 | 55 | 17 | 11/8/0 |
| 6 | `B06-foreign_exchange` | 外汇 | 9 | 9 | 22 | 6 | 5/4/0 |
| 7 | `B07-investment_shared` | 投资公共能力 | 6 | 13 | 18 | 1 | 3/3/0 |
| 8 | `B08-securities` | 证券 | 21 | 77 | 106 | 33 | 17/4/0 |
| 9 | `B09-funds` | 基金与货币基金 | 29 | 81 | 128 | 40 | 19/10/0 |
| 10 | `B10-bonds` | 债券 | 15 | 21 | 49 | 11 | 10/5/0 |
| 11 | `B11-futures_metals` | 期货、黄金与贵金属 | 31 | 97 | 129 | 33 | 22/9/0 |
| 12 | `B12-margin_financing` | 融资融券 | 22 | 21 | 82 | 10 | 18/4/0 |
| 13 | `B13-insurance_social` | 保险与社会保障 | 16 | 27 | 34 | 10 | 13/3/0 |
| 14 | `B14-major_tangible_assets` | 重大资产与家居物品 | 29 | 66 | 111 | 29 | 18/11/0 |
| 15 | `B15-planning_budget_goal` | 预算、提醒、规划与目标 | 42 | 141 | 153 | 60 | 42/0/0 |
| 16 | `B16-reports` | 报表与分析投影 | 28 | 39 | 31 | 5 | 28/0/0 |
| 17 | `B17-import_export` | 导入导出 | 7 | 83 | 72 | 18 | 7/0/0 |
| 18 | `B18-auth_sync_external` | 登录、同步与外部服务 | 5 | 22 | 26 | 7 | 2/3/0 |
| 19 | `B19-tools_longtail` | 辅助工具与长尾能力 | 14 | 67 | 89 | 18 | 10/3/1 |
| 20 | `B20-shared_infrastructure` | 共享 UI 与技术支撑 | 19 | 35 | 89 | 5 | 3/0/16 |

## 4. 关闭条件

- 入口和导航路径已记录
- 页面、字段、默认值和可见状态已记录
- 命令初始状态、触发方式、提示和结果已记录
- 写入前后数据、余额、关联对象和文件副作用已记录
- 空数据、有数据、校验失败和取消路径按适用范围执行
- 截图、导出、日志或文件证据已落到 runtime-validation 目录
- 结果已回填功能目录、数据流、PRD 和验收标准

当前状态分布：`parent_driven_structure_only` 1 条、`partial` 437 条、`pass` 16 条、`unreachable` 6 条。只有结构化观察记录可以推进状态，静态分析不能自动把页面标记为动态兼容。
