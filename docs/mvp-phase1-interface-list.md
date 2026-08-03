# Phase 1 MVP 前后端接口清单

> 状态：当前实施参考。当前 Phase 1/2 由 Rust PC 本地核心、SQLite 仓储、Flutter PC 本地 API 和 .NET 云端 API 共同驱动。

本文档定义 `Finance Own` 第一阶段 MVP 建议实现的前后端接口清单，目标是支撑：

1. Flutter PC 端优先落地
2. PC 本地 `SQLite` 离线可用
3. `.NET` 后端具备最小同步和 Web 在线能力
4. 为手机端轻量离线队列和 Web 在线端留好边界

## 1. Phase 1 MVP 范围

第一阶段只覆盖最小可用闭环：

- 账本启动与当前账本会话
- 账户树查看
- 分类 / 币种 / 人员基础资料读取
- 收入 / 支出 / 转账录入
- 流水列表查看
- 预算列表与新增预算入口
- 基础同步接口骨架
- 一张基础报表：`收支统计`

不进入第一阶段强交付范围：

- 旧 `mh8` 正式认证读取
- 全量投资交易录入
- 高级报表
- 高风险同步修复
- 交割单导入

## 2. 接口设计原则

- Flutter 页面层不直接碰本地 SQL 和旧格式
- 先定义统一业务 DTO，再决定本地/远端分别怎么落
- 第一阶段同时保留：
  - `Local Use Case`
  - `Remote API`
- 即使桌面端第一阶段主要依赖本地库，也要先把远端接口合同固定下来

## 3. 接口分组

### 3.1 App / Ledger

- 当前账本状态
- 当前用户会话
- 应用健康状态

### 3.2 Master Data

- 分类
- 币种
- 人员
- 标签

### 3.3 Accounts

- 账户树
- 账户详情
- 账户余额概况

### 3.4 Transactions

- 流水查询
- 新增收入
- 新增支出
- 新增转账

### 3.5 Budgets

- 预算列表
- 创建预算

### 3.6 Reports

- 收支统计报表

### 3.7 Sync

- 同步状态
- Push / Pull 骨架

## 4. 详细接口清单

## 4.1 App / Ledger

### `GET /api/app/bootstrap`

用途：

- Flutter 启动后拉取当前应用初始上下文

返回：

```json
{
  "appVersion": "0.1.0",
  "mode": "local",
  "hasLedgerOpened": true,
  "currentLedger": {
    "id": "uuid",
    "name": "test",
    "storageType": "sqlite"
  },
  "syncStatus": {
    "enabled": true,
    "lastSyncAt": null,
    "hasPendingChanges": false
  }
}
```

验收：

- 桌面端启动时能拿到初始化状态
- 没有账本时返回空状态，而不是异常

### `GET /api/ledger/current`

用途：

- 获取当前账本元信息

返回字段建议：

- `id`
- `name`
- `currencyId`
- `openedAt`
- `storageType`

## 4.2 Master Data

### `GET /api/master/categories`

用途：

- 获取分类树

查询参数：

- `includeHidden`

返回：

```json
[
  {
    "id": "uuid",
    "parentId": null,
    "name": "餐饮",
    "type": "expense",
    "children": []
  }
]
```

### `GET /api/master/currencies`

用途：

- 获取币种列表

返回字段建议：

- `id`
- `code`
- `name`
- `symbol`
- `isDefault`

### `GET /api/master/persons`

用途：

- 获取人员列表

返回字段建议：

- `id`
- `name`
- `fullName`
- `isArchived`

### `GET /api/master/tags`

用途：

- 获取标签列表

返回字段建议：

- `id`
- `name`
- `color`

## 4.3 Accounts

### `GET /api/accounts/tree`

用途：

- 获取账户树，用于账户中心

返回：

```json
[
  {
    "groupId": "uuid",
    "groupName": "现金",
    "children": [
      {
        "accountId": "uuid",
        "accountName": "Cash-CNY",
        "accountType": "cash",
        "currencyCode": "CNY",
        "balance": "9487.88"
      }
    ]
  }
]
```

验收：

- 能支持桌面端左树展示
- 返回顺序稳定

### `GET /api/accounts/{accountId}`

用途：

- 获取单账户详情

### `GET /api/accounts/summary`

用途：

- 获取账户页底部汇总

返回字段建议：

- `totalAssets`
- `totalLiabilities`
- `netAssets`

## 4.4 Transactions

### `GET /api/transactions`

用途：

- 分页查询流水

查询参数建议：

- `dateFrom`
- `dateTo`
- `accountId`
- `categoryId`
- `transactionType`
- `keyword`
- `page`
- `pageSize`

返回：

```json
{
  "items": [
    {
      "id": "uuid",
      "transactionType": "expense",
      "accountId": "uuid",
      "accountName": "Cash-CNY",
      "categoryId": "uuid",
      "categoryName": "餐饮",
      "amount": "32.50",
      "currencyCode": "CNY",
      "transactedAt": "2026-07-30T12:00:00Z",
      "note": "午餐"
    }
  ],
  "page": 1,
  "pageSize": 50,
  "total": 1
}
```

### `POST /api/transactions/income`

用途：

- 新增收入

请求：

```json
{
  "accountId": "uuid",
  "categoryId": "uuid",
  "amount": "1000.00",
  "currencyId": "uuid",
  "transactedAt": "2026-07-30T12:00:00Z",
  "note": "工资"
}
```

### `POST /api/transactions/expense`

用途：

- 新增支出

### `POST /api/transactions/transfer`

用途：

- 新增转账

请求：

```json
{
  "fromAccountId": "uuid",
  "toAccountId": "uuid",
  "amount": "500.00",
  "currencyId": "uuid",
  "feeAmount": "2.00",
  "feeAccountId": "uuid",
  "transactedAt": "2026-07-30T12:00:00Z",
  "note": "银行卡转账"
}
```

共同验收：

- 事务写入成功后能立即反映到账户余额与流水列表
- 非法金额、缺失账户、缺失分类返回字段级错误

## 4.5 Budgets

### `GET /api/budgets`

用途：

- 获取预算列表

返回字段建议：

- `id`
- `name`
- `periodType`
- `startDate`
- `endDate`
- `plannedAmount`
- `actualAmount`

### `POST /api/budgets`

用途：

- 新增预算

请求：

```json
{
  "name": "2026-08 月预算",
  "periodType": "monthly",
  "startDate": "2026-08-01",
  "endDate": "2026-08-31",
  "items": [
    {
      "categoryId": "uuid",
      "amount": "2000.00"
    }
  ]
}
```

## 4.6 Reports

### `GET /api/reports/income-expense`

用途：

- 获取第一张 MVP 报表：收支统计

查询参数：

- `dateFrom`
- `dateTo`
- `groupBy`
  - `day`
  - `month`
  - `category`

返回：

```json
{
  "summary": {
    "income": "12000.00",
    "expense": "8300.00",
    "net": "3700.00"
  },
  "series": [
    {
      "label": "2026-07",
      "income": "12000.00",
      "expense": "8300.00"
    }
  ]
}
```

## 4.7 Sync

### `GET /api/sync/status`

用途：

- 获取同步状态

返回字段建议：

- `enabled`
- `lastSyncAt`
- `hasPendingChanges`
- `lastCursor`

### `POST /api/sync/push`

用途：

- 上传本地变更批次

### `POST /api/sync/pull`

用途：

- 拉取远端变更批次

第一阶段验收：

- 接口合同存在
- 基础请求/响应可以走通
- 允许先返回空批次，不要求完整冲突解决已上线

## 5. Flutter 侧对应能力

### 第一阶段真正要接的页面

- App Bootstrap
- 账户中心
- 收入录入
- 支出录入
- 转账录入
- 流水列表
- 预算列表
- 收支统计报表

## 6. 第一阶段建议返回错误码

- `VALIDATION_FAILED`
- `ACCOUNT_NOT_FOUND`
- `CATEGORY_NOT_FOUND`
- `LEDGER_NOT_OPENED`
- `SYNC_DISABLED`
- `SYNC_CONFLICT`
- `UNAUTHORIZED`

## 7. 本地模式与云端模式兼容要求

同一套 Flutter 页面应支持：

1. `Local only`
2. `Local + Sync`
3. `Web online`

所以请求模型与返回模型尽量统一，不要让前端为三种模式维护三套页面 DTO。

## 8. 第一阶段接口优先级

### P0

- `GET /api/app/bootstrap`
- `GET /api/accounts/tree`
- `GET /api/master/categories`
- `GET /api/master/currencies`
- `GET /api/transactions`
- `POST /api/transactions/income`
- `POST /api/transactions/expense`
- `POST /api/transactions/transfer`

### P1

- `GET /api/accounts/summary`
- `GET /api/budgets`
- `POST /api/budgets`
- `GET /api/reports/income-expense`

### P2

- `GET /api/sync/status`
- `POST /api/sync/push`
- `POST /api/sync/pull`

## 9. 当前建议结论

如果现在开始第一阶段 MVP，我建议直接按这份接口清单开工。

这样 Flutter 桌面端能最先闭环，而后端接口又不会和后续手机端、Web 端、同步能力冲突。*** End Patch
"]} to=functions.apply_patch code
