# Rust 模块拆分计划

本文档把当前已确认的功能矩阵映射为 Rust 重构时的代码模块，目标是让后续实现不再围绕“原窗体名”直接堆逻辑，而是围绕稳定的业务边界组织代码。

全量归并基线见 [target-ui-consolidation-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\target-ui-consolidation-map.md)：`460` 个旧窗体映射到 `11` 个目标分区和 `40` 个页面族，同时守恒 `1407` 个交互控件、`2000` 个事件和 `502` 个高风险候选。

## 1. 顶层模块

建议按以下顶层模块拆分：

- `ledger`
- `security`
- `master_data`
- `accounts`
- `transactions`
- `investments`
- `planning`
- `sync`
- `import_export`
- `reports`
- `ui`

## 2. 模块职责

### `ledger`

负责账本本体与持久化边界：

- 账本元信息
- 账本打开/关闭
- 账本备份/恢复
- `mh8` 读取适配器
- 未来的新格式仓储
- 数据迁移器

建议子模块：

- `ledger::model`
- `ledger::repository`
- `ledger::mh8`
- `ledger::backup`
- `ledger::migration`

### `security`

负责本地安全与授权：

- 账本密码校验
- 密码修改
- 权限上下文
- 未来的工作组/用户认证桥接

建议子模块：

- `security::auth`
- `security::password`
- `security::workgroup`

### `master_data`

负责基础资料：

- 币种
- 汇率
- 分类
- 标签
- 人员
- 主题模板

建议子模块：

- `master_data::currency`
- `master_data::rate`
- `master_data::category`
- `master_data::tag`
- `master_data::person`
- `master_data::theme`

### `accounts`

负责账户树与账户类型体系：

- 账户组
- 账户创建向导
- 账户详情
- 账户余额快照
- 账户筛选

建议子模块：

- `accounts::group`
- `accounts::account`
- `accounts::wizard`
- `accounts::balance`
- `accounts::filters`

### `transactions`

负责通用交易头与传统流水：

- 收入
- 支出
- 转账
- 现金/活期/第三方储值流水
- 流水账
- 附件
- 模板
- 计划交易

建议子模块：

- `transactions::core`
- `transactions::cash`
- `transactions::current`
- `transactions::third_party`
- `transactions::waste_book`
- `transactions::template`
- `transactions::schedule`
- `transactions::attachments`

### `investments`

负责扩展资产与投资品：

- 定期
- 债权债务
- 外汇
- 证券
- 开放式基金
- 债券/国债
- 黄金
- 标准贵金属
- 期货
- 融资融券
- 保险
- 社保
- 重大资产
- 预付/待摊
- 货币理财

建议子模块：

- `investments::fixed_deposit`
- `investments::debt`
- `investments::foreign_exchange`
- `investments::security`
- `investments::open_fund`
- `investments::bond`
- `investments::gold`
- `investments::precious_metal`
- `investments::futures`
- `investments::margin`
- `investments::insurance`
- `investments::social_security`
- `investments::asset`
- `investments::prepaid`
- `investments::money_product`

### `planning`

负责预算、提醒、财务规划、目标：

- 预算
- 财务提醒
- 限额提醒
- 远程通知开关
- 财务规划专题输入
- 财务诊断
- 目标中心

建议子模块：

- `planning::budget`
- `planning::reminder`
- `planning::notification`
- `planning::financial_planning`
- `planning::diagnosis`
- `planning::goal`

### `sync`

负责云端同步与行情：

- 用户登录/注册
- 同步参数获取
- 业务对象上传下载
- 行情更新
- 通知状态同步

建议子模块：

- `sync::auth`
- `sync::config`
- `sync::currency`
- `sync::person`
- `sync::tag`
- `sync::category`
- `sync::account`
- `sync::transaction`
- `sync::default_currency`
- `sync::balance`
- `sync::quotes`
- `sync::notification`

### `import_export`

负责外部数据接入：

- 导入分类
- 导入收支数据
- 导入交割单
- 导入预览
- 导出数据

建议子模块：

- `import_export::category_import`
- `import_export::data_import`
- `import_export::jiaogedan_import`
- `import_export::preview`
- `import_export::export`

### `reports`

负责报表与分析投影：

- 收支报表
- 账户报表
- 投资报表
- 分类报表
- 标签报表
- 趋势图
- 资产负债统计

建议子模块：

- `reports::query`
- `reports::projection`
- `reports::calculation_policy`
- `reports::income_expense`
- `reports::account`
- `reports::investment`
- `reports::category`
- `reports::tag`
- `reports::trend`
- `reports::balance_sheet`

### `ui`

负责桌面界面与交互编排：

- 主窗体
- 左导航
- 顶部入口
- 账户中心页
- 交易页
- 投资页
- 预算提醒页
- 报表分析页
- 导入导出页
- 登录同步页

建议子模块：

- `ui::shell`
- `ui::accounts`
- `ui::transactions`
- `ui::debts`
- `ui::investments`
- `ui::planning`
- `ui::reports`
- `ui::import_export`
- `ui::sync`
- `ui::tools`
- `ui::shared`

`ui::shared` 按 B20 合同至少拆分为：

- `amount_filter`
- `dialog_shell`
- `date_picker`
- `date_range`
- `tree_select`
- `workspace`
- `progress`
- `statistics`
- `detail_projection`
- `web_content_host`

这些模块只接收宿主模型、草稿和命令回调，不直接依赖 `rusqlite`；网格高级筛选按需启用，第三方工具栏定制器不迁移。

跨 Flutter 页面和 PC 本地 API 的命令状态规则先放在 `app::command_state`：

- 记录选择与批量模式
- 报表空、加载、筛选待刷新、就绪和失败状态
- 导入输入与预览选择状态
- 标签和关联记录选择状态

这样桌面控件只负责绑定 `Enabled / Disabled / Hidden`，不会在多个页面重复实现业务状态判断。

目标 UI 不按旧窗体一比一实现：

- `197` 个投资与扩展资产窗体使用 7 个共享页面族，资产类型通过字段定义、校验、费用和计算策略扩展
- `28` 个报表窗体作为报表定义挂载到同一报表工作区
- `37` 个嵌入视图并入已确认宿主，`21` 个技术窗体替换为共享组件
- 旧功能验收仍以 `execution_id` 为基线；页面合并不能删除命令、字段、状态或数据流

## 3. 首批实现顺序

### Phase A：底层摸清

- `ledger`
- `security`
- `master_data`
- `accounts`

目标：

- 能稳定打开账本
- 能读取账户树、分类、标签、币种、人员

### Phase B：核心记账可用

- `transactions`
- `planning::budget`
- `planning::reminder`
- `ui::shell`
- `ui::accounts`
- `ui::transactions`

目标：

- 能查看流水
- 能录入收入/支出/转账
- 能查看预算与提醒

### Phase C：投资与报表

- `investments`
- `reports`
- `ui::investments`
- `ui::reports`

目标：

- 能替代原软件的大部分投资与统计页面

### Phase D：外围增强

- `sync`
- `import_export`
- `planning::financial_planning`
- `planning::goal`
- `ui::sync`
- `ui::import_export`
- `ui::planning`

目标：

- 补齐同步、行情、导入导出、财务规划、目标

## 4. 设计原则

- 不要用“一个大 Transaction 枚举 + 所有字段全 nullable”硬撑全部业务。
- 统一交易头保留共性字段，各资产域保留专属扩展对象。
- 报表模块不直接耦合 UI，必须基于查询投影或聚合服务。
- 表格、图表、导出和打印必须复用 `ReportReadRepository` 返回的同一组 DTO。
- 旧程序尚未校准的投资成本与收益率只能进入 `calculation_policy`，不得藏在 SQL Repository 中。
- `mh8` 适配器先只读，再考虑写回；新格式仓储要和旧格式适配器解耦。
- 同步协议与本地领域模型之间要有映射层，不把远端字段直接污染核心模型。
