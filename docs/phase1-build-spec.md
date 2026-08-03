# Phase 1 实施规格

本文档定义 Rust 重构的 Phase 1 交付边界，目标是在不依赖主账本认证完全打通的前提下，尽快建立一个“旧数据可读、结构可扩展”的可运行基础版本。

## 1. Phase 1 目标

Phase 1 不追求“完整替代财智8”，而追求三个最小结果：

1. 有一个稳定的 Rust 工作区与模块骨架。
2. 能读取并使用当前已确认可访问的数据源。
3. 能展示最小可用的账户/参考数据/投资品检索壳层。

## 2. 明确不在 Phase 1 内承诺的内容

- 不承诺 `test.mh8` 原位写回
- 不承诺主账本正式表结构已完全恢复
- 不承诺 `记账` 工作区完整复刻
- 不承诺同步/通知真正联网成功
- 不承诺所有投资子域页面齐全

## 3. Phase 1 数据源范围

### 3.1 必须接入

- `mhlink.mdb`
  - 利率
  - 行情
  - 费率
- `MoneyHome8.cache`
  - 名称/拼音缩写检索
- `Investment.cache`
  - 投资品分类字典

### 3.2 必须建立接口但允许返回“未完成”

- `test.mh8`
- `MoneyHome8.data` 解压内置库

接口层必须能明确区分：

- `success`
- `locked`
- `permission_denied`
- `auth_failed`
- `object_invisible`
- `not_implemented`

## 4. Phase 1 领域模型范围

### 4.1 必须建模

- `AccountGroup`
- `Account`
- `Category`
- `Currency`
- `Person`
- `Quote`
- `RateRule`
- `FeeRule`
- `LookupIndex`
- `InvestmentCatalog`

### 4.2 建最小骨架即可

- `Transaction`
- `Budget`
- `Reminder`
- `Security`
- `Fund`
- `SyncRecord`

## 5. Phase 1 仓储层范围

### 5.1 `reference_repository`

必须提供：

- `list_rate_rules()`
- `list_fee_rules()`
- `find_quotes_by_code(code)`
- `list_quotes(limit, filters)`

### 5.2 `cache_repository`

必须提供：

- `search_lookup(keyword)`
- `search_lookup_by_code(code)`
- `search_lookup_by_abbr(abbr)`
- `list_investment_catalog_by_type(type_code)`

### 5.3 `ledger_repository`

Phase 1 允许只提供：

- `open_legacy_ledger(path) -> LedgerOpenResult`
- `inspect_legacy_ledger(path) -> LedgerInspection`

其中：

- `LedgerOpenResult`
  - 返回文件是否可访问
  - 返回认证/对象可见性状态
- `LedgerInspection`
  - 返回当前已知的主账本结构线索

### 5.4 `builtin_repository`

Phase 1 允许只提供：

- `decompress_builtin_db()`
- `inspect_builtin_db()`

## 6. Phase 1 UI 范围

### 6.1 必须有的工作区壳层

- 财务数据
- 财务报表
- 财务分析
- 记账

### 6.2 必须有的可见内容

#### 财务数据

- 账户中心占位页
- 左侧导航骨架：
  - 概况
  - 财务记录
  - 投资一览
  - 标签
  - 账户中心

#### 财务报表

- 左侧分组骨架：
  - 日常收支类
  - 资产负债类
  - 投资类
- 一个可见空状态或占位报表页

#### 财务分析

- 左侧分组骨架：
  - 财务预算
  - 财务诊断
  - 财务规划
  - 财务目标
- 预算空状态页

#### 记账

- 工作区占位页
- 至少展示：
  - 收入录入
  - 支出录入
  - 转账录入
  - 流水账
  的导航骨架

## 7. Phase 1 代码组织建议

建议最小目录：

```text
src/
  app/
  domain/
    accounts/
    master_data/
    investments/
    shared/
  infrastructure/
    legacy/
    reference/
    cache/
  ui/
    shell/
    workspace_data/
    workspace_reports/
    workspace_analysis/
    workspace_bookkeeping/
```

## 8. Phase 1 关键输出物

### 代码输出

- Rust 工程骨架
- 读取器骨架
- 领域模型骨架
- 工作区壳层

### 文档输出

- 若实现时发现模型偏差
  - 必须同步修正：
    - `schema-hypothesis.md`
    - `domain-mapping-spec.md`
    - `rebuild-prd.md`

## 9. Phase 1 验收口径

### 必须通过

- 能读取 `mhlink.mdb`
- 能读取两个 `.cache`
- 能返回 `test.mh8` 的结构化打开状态
- 有四大工作区 UI 壳层
- 有账户/参考数据/缓存检索模型

### 可接受未完成

- 主账本真实表枚举
- 旧库写回
- `记账` 完整交互
- 投资域完整交易录入

## 10. Phase 1 完成后的下一步

Phase 1 完成后，最优先推进：

1. `test.mh8` 正式认证研究继续深入
2. 账户中心真实数据读取
3. 通用交易读取与流水展示
4. 预算与提醒基础闭环
