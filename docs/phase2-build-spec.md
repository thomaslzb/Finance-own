# Phase 2 实施规格

本文档定义 Rust 重构的 Phase 2 交付边界。Phase 2 的目标是在 Phase 1 的“可读可查”基础上，进入“核心可用”的阶段。

## 1. Phase 2 目标

Phase 2 重点不是“所有功能都能用”，而是先把最常用的核心闭环做起来：

1. 账户中心可展示真实数据。
2. 通用记账能力可用。
3. 预算与提醒有最小闭环。
4. 财务报表和财务分析至少有基础可用页。

## 2. Phase 2 明确范围

### 2.1 必须完成的工作区

- 财务数据
  - 账户中心
  - 财务记录最小列表
- 记账
  - 收入
  - 支出
  - 转账
  - 流水账
- 财务报表
  - 日常收支类基础页
  - 资产负债类基础页
- 财务分析
  - 财务预算
  - 基础提醒

### 2.2 可以保留为占位或只读的工作区

- 投资类子报表
- 财务诊断
- 财务规划
- 财务目标
- 同步/通知真实联机
- 导入导出

## 3. Phase 2 数据源策略

### 3.1 允许直接依赖

- `mhlink.mdb`
- `MoneyHome8.cache`
- `Investment.cache`

### 3.2 允许只读兼容

- `test.mh8`
- `MoneyHome8.data` 解压内置库

### 3.3 仍不要求

- `test.mh8` 原位写回
- 主账本完整对象可见性恢复

## 4. Phase 2 领域模型必需项

### 4.1 账户与基础资料

- `AccountGroup`
- `Account`
- `Category`
- `Currency`
- `Person`

### 4.2 通用交易

- `Transaction`
- `TransactionType`
- `TransactionTheme`
- `Template`
- `Schedule`

### 4.3 预算提醒

- `Budget`
- `BudgetItem`
- `Reminder`
- `ReminderType`

### 4.4 参考数据

- `Quote`
- `RateRule`
- `FeeRule`
- `LookupIndex`
- `InvestmentCatalog`

## 5. Phase 2 最小功能闭环

### 闭环 A：账户中心

输入：

- 主账本只读数据
- 基础资料

输出：

- 账户组树
- 账户列表
- 汇总口径：
  - 资产
  - 负债
  - 净资产

验收：

- 至少能展示一批真实账户数据
- 能按账户类型筛选

### 闭环 B：通用记账

输入：

- 账户
- 分类
- 人员
- 交易类型

输出：

- 收入录入
- 支出录入
- 转账录入
- 流水展示

验收：

- 至少有一个可运行的本地新格式写入通路
- 至少能在 Rust 界面中看到录入后的流水

### 闭环 C：预算

输入：

- 分类
- 预算项
- 交易聚合

输出：

- 预算列表
- 新增预算
- 已用/剩余展示

验收：

- 预算页不再只是空状态
- 能看到最小预算明细

### 闭环 D：提醒

输入：

- 提醒项
- 阈值字段
- 日期字段

输出：

- 提醒列表
- 启用/禁用
- 到期/阈值提示

验收：

- 能展示一组最小提醒数据

### 闭环 E：基础报表

输入：

- 交易流水
- 账户汇总

输出：

- 日常收支类基础结果
- 资产负债类基础结果

验收：

- 至少能生成一页基础列表型报表

## 6. Phase 2 仓储接口建议

### 6.1 `ledger_repository`

新增：

- `list_accounts()`
- `list_account_groups()`
- `list_categories()`
- `list_people()`
- `list_transactions(filters)`

### 6.2 `app_write_repository`

已落地通用交易写入接口 `src/app/transactions.rs::TransactionWriteRepository`：

- `create_transaction(input)`

后续仍需新增：

- `create_budget(input)`
- `create_reminder(input)`

交易写入必须把 `transactions`、全部 `transaction_entries`、手续费、标签和附件关系放在同一个 SQLite 事务中；余额字段不允许直接写入账户表。

### 6.3 `report_read_repository`

已落地 Rust trait：`src/app/reporting.rs::ReportReadRepository`。

- `list_ledger_entries(filter)`
- `list_account_running_balances(filter)`
- `list_account_balances(ledger_id)`
- `list_tagged_entries(filter)`
- `list_tagged_assets(ledger_id, tag_ids)`
- `list_investment_position_inputs(filter)`
- `list_realized_profit_inputs(filter)`

投资接口只返回计算输入；成本法、费用归属和收益率分母必须在代表性样例校准后由独立策略实现。

## 7. Phase 2 UI 交付建议

通用命令状态由 `src/app/command_state.rs` 提供，Flutter PC 本地 API 和页面必须消费同一套状态结果：

- 无记录选择时禁用修改、删除和查找
- 批量命令仅在批量模式显示，并由批量选择决定是否可写
- 报表加载完成前禁用导出和打印；筛选变化后进入待刷新状态
- 导入和标签操作必须等待有效输入或对应选择

### 财务数据

- 左侧导航仍保留：
  - 概况
  - 财务记录
  - 投资一览
  - 标签
  - 账户中心
- 至少先让：
  - 账户中心
  - 财务记录
  可用

### 记账

- 左侧或上方分组至少有：
  - 收入
  - 支出
  - 转账
  - 流水账

### 财务报表

- 左侧分组保留：
  - 日常收支类
  - 资产负债类
  - 投资类
- Phase 2 至少做前两组的基础页

### 财务分析

- 左侧分组保留：
  - 财务预算
  - 财务诊断
  - 财务规划
  - 财务目标
- Phase 2 至少做预算页与提醒相关页

## 8. Phase 2 不要求解决的问题

- 主账本所有表都可见
- 投资子域完整录入
- 旧库写回
- 同步联网成功
- 导入导出完整通路

## 9. Phase 2 验收标准

必须通过：

1. 账户中心能展示真实账户数据
2. 至少能录入并展示一条新交易
3. 预算页不再只是空状态
4. 提醒页至少能展示一批提醒
5. 报表页至少有一页列表型结果
6. `python tools\validate_sqlite_schema.py` 通过

可接受未完成：

1. 投资交易录入
2. 导入交割单
3. 同步登录
4. 旧库写回

## 10. Phase 2 完成后最优先继续推进

1. `test.mh8` 对象可见性继续研究
2. 投资域真实交易闭环
3. 财务诊断 / 财务规划 / 财务目标页
4. 投资类报表
