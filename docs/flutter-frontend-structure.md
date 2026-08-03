# Flutter 三端前端目录结构设计

> 状态：当前实施参考。第一版三端 UI 统一采用 Flutter；PC 端通过 Rust 本地 API 访问本地账本，手机端使用轻量队列和缓存，Web 端在线访问 .NET API。

本文档给出 `Finance Own` 项目的 Flutter 前端建议目录结构，目标是：

1. 桌面、手机、Web 最大程度共用一套 UI 代码
2. 保留按端裁剪能力
3. 与 `.NET` 后端、自有同步层和 PC 端 Rust 旧格式迁移模块解耦

## 1. 设计原则

- 三端共用：
  - 设计系统
  - 路由结构
  - 页面组件
  - 表单与校验
  - 状态管理
  - API Client
  - PC 本地 API 抽象
  - 手机端队列与缓存抽象
- 平台差异只放在：
  - 文件选择
  - 附件打开
  - 窗口管理
  - 快捷键
  - 高级桌面工具

## 2. 推荐目录结构

```text
flutter_app/
1. pubspec.yaml
2. analysis_options.yaml
3. lib/
   3.1 app/
   3.2 bootstrap/
   3.3 core/
   3.4 design_system/
   3.5 infrastructure/
   3.6 features/
   3.7 platforms/
   3.8 routing/
   3.9 l10n/
4. test/
5. integration_test/
6. assets/
7. web/
8. windows/
9. macos/
10. linux/
11. android/
12. ios/
```

## 3. `lib/` 细分建议

### 3.1 `app/`

放应用总装配：

```text
lib/app/
1. app.dart
2. app_config.dart
3. app_environment.dart
4. app_providers.dart
5. app_lifecycle.dart
```

职责：

- 创建根 `MaterialApp`
- 注入全局 provider / service
- 区分桌面、手机、Web 环境

### 3.2 `bootstrap/`

放启动逻辑：

```text
lib/bootstrap/
1. bootstrap.dart
2. bootstrap_desktop.dart
3. bootstrap_mobile.dart
4. bootstrap_web.dart
```

职责：

- 初始化日志
- 初始化本地数据库
- 初始化 API 配置
- 初始化同步服务
- 初始化平台差异能力

### 3.3 `core/`

放前端核心无业务依赖层：

```text
lib/core/
1. constants/
2. enums/
3. errors/
4. utils/
5. extensions/
6. types/
7. services/
8. storage/
9. sync/
10. auth/
```

建议内容：

- 通用常量
- 通用错误模型
- 时间、金额、格式化工具
- 鉴权会话对象
- 同步状态对象
- 本地存储抽象

### 3.4 `design_system/`

放三端统一设计系统：

```text
lib/design_system/
1. theme/
2. tokens/
3. widgets/
4. layouts/
5. icons/
6. charts/
```

建议组件：

- 顶部导航栏
- 左侧树状导航
- 表格容器
- 筛选栏
- 空状态页
- 金额输入框
- 日期范围选择器
- 图表卡片
- 状态徽标
- 对话框

### 3.5 `infrastructure/`

放和外部依赖耦合的实现：

```text
lib/infrastructure/
1. api/
2. database/
3. repositories/
4. dto/
5. mappers/
6. local_cache/
7. attachments/
```

职责：

- HTTP client
- SQLite adapter
- DTO 与领域 ViewModel 映射
- 附件处理
- 本地缓存/草稿

### 3.6 `features/`

按业务域拆分：

```text
lib/features/
1. shell/
2. ledger/
3. accounts/
4. master_data/
5. transactions/
6. debts_credit/
7. investments/
8. budget/
9. reminders/
10. planning/
11. goals/
12. reports/
13. sync_center/
14. import_export/
15. settings/
```

每个 feature 再按统一结构拆：

```text
feature_name/
1. application/
2. domain/
3. presentation/
4. widgets/
5. state/
```

### 3.7 `platforms/`

放真正的平台差异实现：

```text
lib/platforms/
1. desktop/
2. mobile/
3. web/
```

建议内容：

- 文件选择器
- 文件打开器
- 导入入口能力判断
- 快捷键支持
- 窗口行为
- Web 特有限制处理

### 3.8 `routing/`

放统一路由：

```text
lib/routing/
1. app_router.dart
2. route_names.dart
3. guards/
4. route_groups/
```

建议路由分区：

- shell
- accounts
- transactions
- investments
- reports
- planning
- settings

### 3.9 `l10n/`

放国际化：

```text
lib/l10n/
1. app_zh.arb
2. app_en.arb
```

建议：

- 先以中文为主
- 保留英文扩展位

## 4. 每个 Feature 的推荐模板

以 `transactions` 为例：

```text
lib/features/transactions/
1. application/
   1.1 transaction_service.dart
   1.2 transaction_commands.dart
2. domain/
   2.1 transaction_vm.dart
   2.2 transaction_filter.dart
3. presentation/
   3.1 pages/
   3.2 dialogs/
   3.3 sections/
4. widgets/
   4.1 transaction_list.dart
   4.2 transaction_form.dart
5. state/
   5.1 transaction_list_controller.dart
   5.2 transaction_edit_controller.dart
```

说明：

- `application/`
  - 组织前端业务流程，不直接写数据库 SQL
- `domain/`
  - 放前端需要的页面模型、筛选模型、表单模型
- `presentation/`
  - 页面和弹窗
- `widgets/`
  - 可复用子组件
- `state/`
  - 页面状态与控制器

## 5. 三端共享与差异边界

### 完全共用

- 页面结构
- 列表与表单
- 报表展示
- 筛选交互
- 预算/提醒/规划/目标页面
- 登录和同步状态

### 桌面特有

- 旧账本导入入口
- 高级同步修复
- 高风险设置
- 文件级导出/恢复
- 更强快捷键

建议放在：

```text
lib/features/import_export/presentation/desktop/
lib/features/sync_center/presentation/desktop/
lib/features/settings/presentation/desktop/
```

### 手机特有

- 快速记账页
- 极简投资录入页
- 小屏专用组件

建议放在：

```text
lib/features/transactions/presentation/mobile/
lib/features/investments/presentation/mobile/
```

### Web 特有

- 限制本地文件能力
- 减少高风险入口

建议放在：

```text
lib/platforms/web/
```

## 6. 页面分区建议

建议围绕我们已经确认的顶层导航来建壳：

### `shell`

- 顶部入口：
  - 财务数据
  - 财务报表
  - 财务分析
  - 记账
- 左侧导航按当前工作区切换

### `accounts`

- 账户中心
- 账户组/账户详情
- 余额汇总

### `transactions`

- 财务记录
- 收入/支出/转账
- 债权债务
- 信用卡
- 模板/计划

### `investments`

- 投资一览
- 证券
- 基金
- 外汇
- 债券
- 黄金/贵金属
- 期货
- 融资融券

### `reports`

- 日常收支类
- 资产负债类
- 投资类

### `planning`

- 财务预算
- 财务诊断
- 财务规划
- 财务目标

## 7. 状态管理建议

推荐：

- `Riverpod`

原因：

- Flutter 三端通用
- 依赖注入和异步状态清晰
- 适合大项目
- 比传统全局单例更可控

建议结构：

```text
state/
1. *_provider.dart
2. *_controller.dart
3. *_state.dart
```

## 8. 本地数据库接入建议

前端侧不要直接暴露 SQL 到页面层。

建议：

```text
presentation -> controller -> application service -> repository -> sqlite adapter
```

这样后续：

- SQLite
- Mock repository
- Server-backed repository

都可以替换。

## 9. 与 .NET 后端的接口边界

Flutter 前端只依赖三类接口：

### 认证接口

- 登录
- 刷新 token
- 登出

### 同步接口

- 拉取变更
- 推送变更
- 冲突处理
- 同步状态查询

### 查询接口

- Web 端在线查询
- 报表聚合
- 行情获取

## 10. 目录结构最终建议

```text
flutter_app/
1. lib/
   1.1 app/
   1.2 bootstrap/
   1.3 core/
   1.4 design_system/
   1.5 infrastructure/
   1.6 features/
       1.6.1 shell/
       1.6.2 ledger/
       1.6.3 accounts/
       1.6.4 master_data/
       1.6.5 transactions/
       1.6.6 debts_credit/
       1.6.7 investments/
       1.6.8 budget/
       1.6.9 reminders/
       1.6.10 planning/
       1.6.11 goals/
       1.6.12 reports/
       1.6.13 sync_center/
       1.6.14 import_export/
       1.6.15 settings/
   1.7 platforms/
   1.8 routing/
   1.9 l10n/
2. test/
3. integration_test/
4. assets/
5. web/
6. windows/
7. macos/
8. linux/
9. android/
10. ios/
```

## 11. 当前建议结论

如果现在正式开始前端工程，我建议：

1. 直接按这份目录结构建 Flutter 主工程
2. 先做：
   - `shell`
   - `accounts`
   - `transactions`
   - `budget`
3. 暂时把：
   - 旧账本导入
   - 高级同步修复
   - 高风险设置
   放在桌面专属目录里
