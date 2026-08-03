# Finance Own 技术架构方案

本文档是当前项目的正式技术架构决策。Finance Own 第一版采用 `Flutter + .NET + Rust PC 本地核心`：Flutter 统一 PC、手机和 Web 三端 UI，.NET 承载云端服务，Rust 作为 PC 客户端内置本地核心负责旧账本迁移、本地 SQLite 账本、导入导出和高风险财务处理。

本方案替代早期“Rust 主系统 / Rust 桌面 UI 框架待定”的路线。已完成的 Rust 领域模型、SQLite 迁移、只读旧数据源探测和应用端口继续保留，但定位调整为 PC 本地核心与 Flutter 本地 API 的基础。

## 1. 目标与约束

- 功能范围以 MoneyHome8 已验证页面、命令、状态和数据流为基线。
- 第一版必须覆盖 PC 端、手机端和 Web 端三端使用。
- PC 端必须支持完全离线可写，本地账本采用 SQLite。
- Web 端第一版在线为主，必须登录后通过云端 API 使用。
- 手机端支持记账、同步、离线草稿和待同步队列，但不保存完整本地账本。
- 三端都可以产生财务记录，并通过云端上传、下载和同步数据。
- 新系统不复刻旧 Jet 表结构，旧 MoneyHome8 原始文件只作为 PC 本地只读迁移来源。
- 交易、余额、持仓、预算和报表必须由同一组可审计事实重建。
- 未通过真实样例校准的投资公式和旧协议不得标记为兼容。

## 2. 当前技术栈

- 三端 UI：Flutter Desktop、Flutter Mobile、Flutter Web
- PC 本地核心：Rust 内置模块
- PC 本地账本：SQLite，当前 Rust 侧使用 rusqlite
- PC 本地 API：Flutter 通过稳定本地 API/FFI 调用 Rust，不直接访问 SQLite
- 云端服务：.NET API
- 云端数据库：PostgreSQL
- 同步：对象级多主同步，云端是协调中心并保存完整新系统财务对象副本
- 旧格式迁移：Rust PC 本地只读迁移，不上传旧 MoneyHome8 原始文件

Flutter 页面只绑定 DTO、结构化错误和命令回调，不拼接 SQL、不读取旧账本文件。Rust 本地核心可以改变 SQLite 内部结构，但必须保持 Flutter 本地 API 的业务契约稳定。

## 3. 架构总览

~~~mermaid
flowchart LR
  PCUI["Flutter Desktop"] --> LOCALAPI["PC Local API / FFI"]
  LOCALAPI --> RUST["Rust PC Local Core"]
  RUST --> SQLITE["PC SQLite Ledger"]
  RUST --> LEGACY["MoneyHome8 Legacy Migration"]

  MOBILE["Flutter Mobile"] --> CLOUD[".NET API"]
  WEB["Flutter Web"] --> CLOUD
  PCUI --> CLOUD
  RUST --> CLOUD

  CLOUD --> PG["PostgreSQL Cloud Replica"]
  CLOUD --> FILES["Attachment Storage"]
  CLOUD --> SYNC["Sync Batches / Versions / Conflicts"]
~~~

## 4. Flutter 三端边界

### PC 端

- 使用 Flutter Desktop 实现主界面、账户中心、记账、报表、分析、导入导出和冲突解决。
- 可以未登录创建和使用本地账本；登录后必须显式确认才开启云同步。
- 通过 Rust 本地核心读写 SQLite、执行旧账本迁移、导入导出和高风险财务处理。
- 支持完整冲突解决。

### 手机端

- 使用 Flutter Mobile 实现随手记账、查询、同步状态和轻量管理。
- 可保存离线记账草稿、本地待同步队列、最近查询缓存和附件临时缓存。
- 不保存完整本地账本，不承担旧账本迁移、批量治理或复杂冲突处理。
- 只提示冲突并允许延后到 PC 或 Web 处理。

### Web 端

- 使用 Flutter Web，第一版在线为主。
- 必须登录后使用，可在线记录财务数据并直接写入云端。
- 支持完整冲突解决和云端账本查询。
- 不承担浏览器离线主账本写入。

## 5. Rust PC 本地核心

Rust 负责 PC 端本地正确性和旧格式边界：

- 账簿创建、打开、完整性检查和本地 SQLite 写入。
- 账户、基础资料、交易、预算、计划、提醒、目标和基础报表的本地核心能力。
- MoneyHome8 `.mh8`、`mhlink.mdb`、`MoneyHome8.data`、缓存和 XML 等旧来源的只读迁移。
- 导入、导出、备份、附件散列和原子文件替换等高风险文件处理。
- 金额精度、交易分录、余额重建和同步前本地校验。

Rust 不作为第一版云端服务端主技术，也不要求手机端或 Web 端内置。

## 6. .NET 云端服务

.NET API 负责：

- 自有账号、会话、刷新令牌和设备列表。
- Web 在线记账和查询。
- PC、手机和 Web 三端同步 push/pull。
- PostgreSQL 中的新系统财务对象副本。
- 同步批次、对象版本、墓碑、冲突记录和审计。
- 附件上传、下载、权限校验和后台任务。

第一版不做完整端到端加密；云端必须提供 HTTPS、静态加密、密钥管理、账本级权限隔离和敏感字段保护。

## 7. 数据架构

### PC SQLite

SQLite 是 PC 本地账本真相源。当前十三版迁移创建 63 张表、21 个视图和 56 个显式索引，`PRAGMA user_version=13`，文件头 `application_id=1179604814`。

核心规则：

- 金额使用币种最小单位整数，禁止使用 REAL 或 f64 保存财务事实。
- 一笔业务由 transactions 和 transaction_entries 原子提交。
- 手续费、利息、调整和期初余额使用显式分录角色。
- 余额、预算消耗、目标进度和报表由查询投影重建。
- 投资产品使用通用成交与持仓事实，专属合同表只保存通用模型无法表达的条款。
- 附件内容使用受管相对路径和 SHA-256，数据库保存元数据及引用关系。
- 旧 Jet 标识只进入 legacy_id_map，不能成为新领域主键。

### PostgreSQL

PostgreSQL 是云端数据库，保存完整新系统财务对象副本、同步版本、冲突记录、附件元数据和审计日志。云端保存的是新系统对象，不保存旧 MoneyHome8 原始文件。

### 多账本隔离

第一版支持多账本。数据模型、同步、权限、附件、缓存和报表都必须按账本隔离，财务对象必须属于明确 `ledger_id`。数据模型预留账本成员能力，至少区分所有者、可编辑成员和只读成员；复杂细粒度权限后置。

## 8. 同步策略

同步采用对象级多主同步，云端是协调中心，不是覆盖 PC 本地账本的唯一真相源。

- PC 离线写入先在本地成立，联网后上传对象变更。
- 手机端离线草稿和待同步队列联网后上传。
- Web 在线写入直接进入云端版本，再同步给 PC 和手机。
- 不冲突的对象变更自动双向合并。
- 同一对象同一字段编辑、删除与修改并发等真正冲突进入显式解决流程。
- PC 和 Web 支持完整冲突解决；手机端只提示冲突并允许延后处理。
- 同步按对象和变更批次传输，不同步整个 SQLite 文件。

## 9. 旧格式与迁移

- 旧 MoneyHome8 原始文件迁移第一版仅在 PC 端本地执行。
- `test001.mh8`、裸 Jet 副本、`mhlink.mdb`、`MoneyHome8.data` 和缓存均只读。
- 迁移采用“提取、规范化、校验、预览、原子导入”流程。
- 旧字段映射、原始行、错误和目标 ID 都必须可审计。
- 旧库认证和结构枚举继续并行研究，但不阻塞新 SQLite 模式、Flutter 三端和云同步开发。
- 首版不写回旧 mh8。
- 迁移结果写入 PC 本地 SQLite，经用户确认后再按新系统对象同步到云端和其它端。

## 10. 分阶段路线

### Phase 1：PC 本地核心与迁移基线

- Rust SQLite 迁移、应用文件标识和完整性检查。
- 账户、基础资料、交易、预算、计划、提醒、目标和基础查询。
- 旧账本只读导入边界。
- Flutter PC 本地 API 契约草案。

### Phase 2：Flutter PC 可用闭环

- Flutter Desktop 壳层和账户中心。
- PC 端通过 Rust 本地 API 打开/创建账本。
- 日常收入、支出、取款和转账。
- 财务记录、账户流水、基础报表。
- 备份、恢复、附件基础能力。

### Phase 3：.NET 云端与三端同步

- 自有账号、设备、会话和账本成员。
- PostgreSQL 云端对象副本。
- PC、手机、Web 三端同步 push/pull。
- 显式开启同步、冲突记录和 PC/Web 冲突解决。

### Phase 4：Flutter Mobile 与 Flutter Web

- 手机端轻量记账、查询、离线草稿和待同步队列。
- Web 在线记账、查询和冲突解决。
- 三端统一 DTO、错误模型和权限边界。

### Phase 5：投资、合同、导入导出与高级分析

- 债权债务、信用卡、定期、理财。
- 证券、基金、债券、外汇、期货、贵金属和保险。
- 成本批次、估值、盈亏和报表。
- 旧 XML、交割单和专项导入。

## 11. 当前验证基线

- 53 类运行时实体候选均有数据库或适配器契约。
- 当前迁移规模为 63 表、21 视图、56 个显式索引。
- SQLite 验证目标版本为 `user_version=13`，应用文件标识为 `1179604814`。
- Rust 当前基线为 `67 passed, 0 failed`。
- 原程序 460/460 个窗体已分类并进入动态验证队列。

后续技术决策必须遵守本文件和 `docs/adr/` 中已接受的架构边界。
