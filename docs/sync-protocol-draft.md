# Finance Own 同步协议字段草案

> 状态：历史草案，仅保留对象级同步概念。当前实施以 `technical-architecture-proposal.md` 和 `docs/workplans/three-client-requirements-analysis.md` 为准：Flutter 负责 PC/Web/手机三端 UI，.NET + PostgreSQL 负责云端对象副本与同步协调，Rust 只作为 PC 本地核心。

本文档定义 `Flutter` 三端与 `.NET` 后端之间的对象级同步协议草案，用于支撑：

1. PC 端本地 `SQLite` 完整账本。
2. 手机端离线草稿、待同步队列、最近查询缓存和附件临时缓存。
3. Web 端在线访问 `.NET API + PostgreSQL` 云端对象副本。
4. 对象级双向同步、冲突协调和用户确认覆盖策略。
5. PC 端高级同步修复和旧 MoneyHome8 本地迁移边界。

## 1. 设计目标

同步协议必须满足：

- PC 离线优先，手机端支持轻量离线草稿和待同步队列
- 对象级同步，不做文件级同步
- 支持：
  - 双向同步
  - 从云端恢复到本机
  - 用本机覆盖云端
- 支持软删除
- 支持冲突检测
- 支持批次审计
- 不直接传输旧 `mh8` / `mdb` / `cache` 文件

## 2. 同步单位

同步单位统一定义为 `SyncItem`。

每个 `SyncItem` 对应一个业务对象，例如：

- `account_group`
- `account`
- `category`
- `tag`
- `person`
- `transaction`
- `budget`
- `budget_item`
- `reminder`
- `goal`
- `goal_account_relation`
- `plan`
- `investment_position_snapshot`
- `sync_setting`

## 3. 基础字段

每个同步对象至少必须包含：

```json
{
  "entityType": "transaction",
  "entityId": "uuid",
  "operation": "upsert",
  "version": 12,
  "updatedAt": "2026-07-30T12:00:00Z",
  "deletedAt": null,
  "deviceId": "desktop-001",
  "payload": {}
}
```

### 字段定义

- `entityType`
  - 对象类型
- `entityId`
  - 全局唯一 ID，建议 `UUID`
- `operation`
  - `upsert` / `delete`
- `version`
  - 对象版本号，整数递增
- `updatedAt`
  - 最后修改时间，UTC
- `deletedAt`
  - 软删除时间；未删除则为 `null`
- `deviceId`
  - 最后写入来源设备
- `payload`
  - 业务对象正文

## 4. 批次模型

一次同步不是单对象提交，而是一个批次。

### 4.1 Push Batch

```json
{
  "batchId": "uuid",
  "deviceId": "desktop-001",
  "userId": "uuid",
  "mode": "bidirectional",
  "clientClock": "2026-07-30T12:05:00Z",
  "baseCursor": "sync-cursor-123",
  "items": []
}
```

字段：

- `batchId`
  - 同步批次 ID
- `deviceId`
  - 设备 ID
- `userId`
  - 用户 ID
- `mode`
  - `bidirectional`
  - `cloud_to_local_recovery`
  - `local_to_cloud_override`
- `clientClock`
  - 客户端发起时间
- `baseCursor`
  - 客户端认为自己基于的远端游标
- `items`
  - 本次推送对象列表

### 4.2 Pull Request

```json
{
  "deviceId": "desktop-001",
  "userId": "uuid",
  "sinceCursor": "sync-cursor-123",
  "entityTypes": [
    "account",
    "transaction",
    "budget",
    "reminder"
  ]
}
```

字段：

- `sinceCursor`
  - 上次同步成功后的游标
- `entityTypes`
  - 可选拉取范围

## 5. 服务端响应模型

### 5.1 Push Response

```json
{
  "batchId": "uuid",
  "status": "partial_conflict",
  "serverCursor": "sync-cursor-124",
  "accepted": [],
  "conflicts": [],
  "rejected": []
}
```

字段：

- `status`
  - `success`
  - `partial_conflict`
  - `rejected`
- `serverCursor`
  - 服务端最新游标
- `accepted`
  - 接受的对象结果
- `conflicts`
  - 冲突对象结果
- `rejected`
  - 拒绝对象结果

### 5.2 Pull Response

```json
{
  "serverCursor": "sync-cursor-124",
  "items": []
}
```

## 6. 接受结果字段

```json
{
  "entityType": "transaction",
  "entityId": "uuid",
  "status": "accepted",
  "serverVersion": 13,
  "serverUpdatedAt": "2026-07-30T12:05:03Z"
}
```

## 7. 冲突结果字段

```json
{
  "entityType": "transaction",
  "entityId": "uuid",
  "status": "conflict",
  "clientVersion": 12,
  "serverVersion": 14,
  "clientUpdatedAt": "2026-07-30T12:00:00Z",
  "serverUpdatedAt": "2026-07-30T12:02:00Z",
  "serverPayload": {},
  "conflictReason": "version_mismatch"
}
```

### `conflictReason` 建议值

- `version_mismatch`
- `deleted_on_server`
- `deleted_on_client`
- `payload_incompatible`
- `forbidden_override`

## 8. 拒绝结果字段

```json
{
  "entityType": "account",
  "entityId": "uuid",
  "status": "rejected",
  "reason": "validation_failed",
  "message": "账户名称不能为空。"
}
```

## 9. 同步模式定义

## 9.1 正常双向同步

模式值：

```text
bidirectional
```

策略：

- 上传本地增量
- 下载远端增量
- 冲突时进入冲突队列

适用：

- 桌面端日常使用
- 手机端日常使用
- Web 在线模式

## 9.2 从云端恢复到本机

模式值：

```text
cloud_to_local_recovery
```

策略：

- 以云端对象为主
- 本地未同步的新对象可选保留或备份
- 不允许静默覆盖服务端更高版本

适用：

- 新设备初始化
- 本地库损坏后恢复

## 9.3 用本机覆盖云端

模式值：

```text
local_to_cloud_override
```

策略：

- 仅桌面端允许
- 必须先做云端备份快照
- 必须二次确认
- 服务端应返回影响对象数量摘要

适用：

- 用户明确知道本地账本才是正确来源

## 10. 版本与冲突规则

### 10.1 版本推进

- 本地对象每次修改：
  - `version += 1`
- 服务端接受后：
  - 返回 `serverVersion`

### 10.2 双向同步冲突

冲突条件：

- 客户端上传的 `version` 小于服务端当前版本
- 或 `baseCursor` 已过旧，且同一对象在两端都改过

默认策略：

- 不自动丢弃任何一方
- 放入 `conflicts`

### 10.3 删除规则

删除不做物理删除同步，而是：

- 写入 `deletedAt`
- 服务端保留 tombstone

建议 tombstone 字段：

```json
{
  "entityType": "transaction",
  "entityId": "uuid",
  "deletedAt": "2026-07-30T12:03:00Z",
  "version": 15
}
```

## 11. 对象负载建议

### 11.1 账户

```json
{
  "id": "uuid",
  "groupId": "uuid",
  "name": "现金-CNY",
  "accountType": "cash",
  "currencyId": "uuid",
  "isArchived": false
}
```

### 11.2 交易

```json
{
  "id": "uuid",
  "transactionType": "expense",
  "accountId": "uuid",
  "categoryId": "uuid",
  "personId": null,
  "amount": "128.50",
  "currencyId": "uuid",
  "transactedAt": "2026-07-30T09:30:00Z",
  "note": "午餐"
}
```

### 11.3 预算

```json
{
  "id": "uuid",
  "name": "2026-08 月预算",
  "periodType": "monthly",
  "startDate": "2026-08-01",
  "endDate": "2026-08-31"
}
```

### 11.4 提醒

```json
{
  "id": "uuid",
  "remindType": "balance_limit",
  "targetId": "uuid",
  "triggerAt": "2026-08-05T00:00:00Z",
  "enabled": true
}
```

## 12. 设备与会话字段

建议单独维护设备表：

```json
{
  "deviceId": "desktop-001",
  "deviceType": "desktop",
  "platform": "windows",
  "appVersion": "0.1.0",
  "lastSeenAt": "2026-07-30T12:05:00Z"
}
```

### `deviceType` 建议值

- `desktop`
- `mobile`
- `web`

## 13. 审计与可观测性

服务端至少记录：

- `sync_batch`
- `sync_item_result`
- `sync_conflict`
- `sync_tombstone`

建议最少字段：

### `sync_batch`

- `batch_id`
- `user_id`
- `device_id`
- `mode`
- `base_cursor`
- `server_cursor`
- `status`
- `created_at`

### `sync_item_result`

- `batch_id`
- `entity_type`
- `entity_id`
- `result_status`
- `client_version`
- `server_version`

## 14. 安全边界

- 手机端与 Web 端不允许：
  - `local_to_cloud_override`
- 服务端不接受客户端直接上传旧 `mh8`
- 敏感操作必须带：
  - 用户身份
  - 设备身份
  - 批次 ID

## 15. 推荐的第一版 API

```text
POST /api/sync/push
POST /api/sync/pull
GET  /api/sync/status
POST /api/sync/resolve
POST /api/sync/recover-from-cloud
POST /api/sync/override-cloud
```

## 16. 当前建议结论

第一版同步协议建议：

1. 以对象级同步为核心
2. 默认双向同步
3. 高风险模式仅桌面端开放
4. `SQLite` 本地先写，`.NET + PostgreSQL` 云端统一合并
