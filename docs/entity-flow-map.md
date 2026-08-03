# 实体与数据流映射

本文档将当前已发现的表名候选、参考库表、缓存语义与功能域组合起来，形成一个面向开发的实体关系草图。

## 1. 账户与基础资料主链

```mermaid
flowchart TD
  A["TBAcctGroup / TBAcctType"] --> B["AccountGroup / Account"]
  C["TBCurrency"] --> B
  D["TBCategory"] --> E["Transaction / Budget"]
  F["TBPerson"] --> G["Debt / Remind / Related Party"]
  H["TBObjectType"] --> I["Investment Object"]
```

## 2. 交易主链

```mermaid
flowchart TD
  A["TBTransaction / TBStatement / TBOldTransaction"] --> B["现金/活期/第三方储值/通用流水"]
  C["TBTransType / TBTransTheme / TBTemplate"] --> B
  D["TBPayModeHistory"] --> B
  E["TBRemindSetting"] --> B
```

## 3. 债权债务与信用链

```mermaid
flowchart TD
  A["TBDebtAcct / TBDebtObject / TBDebtRate"] --> B["债权债务流水与统计"]
  C["TBCreditCardAcct"] --> D["信用卡流水/账单/提醒"]
  E["TPayable* / TReceivable* 相关窗体"] --> F["应付款 / 应收款页面"]
```

## 4. 投资与扩展资产链

```mermaid
flowchart TD
  A["TBSecurities / TBSecurityAcct"] --> B["证券交易"]
  C["TBOpenFund"] --> D["开放式基金交易"]
  E["TBPreciousMetals / TBFuturesGoods / TBFinancingContract"] --> F["贵金属/期货/融资融券"]
  G["TBAssetAcct / TBAssetType"] --> H["重大资产 / 实物资产"]
  I["TBInsure / TBInsureAcctInfo"] --> J["保险 / 社保"]
```

## 5. 预算、提醒、规划、目标链

```mermaid
flowchart TD
  A["TBBudget / TBBudgetItem"] --> B["预算页面"]
  C["TBRemindSetting / TBRemindTypeSet"] --> D["提醒页面"]
  E["TBFP*"] --> F["财务规划专题输入"]
  G["TBGoalSetting / TBGoalAcctRelation"] --> H["目标中心 / 目标储蓄"]
```

## 6. 同步与系统链

```mermaid
flowchart TD
  A["TBSyncDefaultData / TBSyncRecord"] --> B["同步状态与默认同步数据"]
  C["TBReportSettings"] --> D["报表配置"]
  E["TBStateTheme / TBPlanStateTheme / TBLifeTheme"] --> F["主题/状态/UI 配置"]
```

## 7. 参考库与缓存链

```mermaid
flowchart LR
  A["mhlink.mdb: HBRate"] --> B["定期/理财利率"]
  C["mhlink.mdb: TBSecuPrice"] --> D["证券/基金/债券行情"]
  E["mhlink.mdb: TBTransFee"] --> F["交易费率"]
  G["MoneyHome8.cache"] --> H["名称 + 拼音/缩写检索"]
  I["Investment.cache"] --> J["投资品分类字典"]
```

## 8. 当前最重要的实现优先级

### P0：一切都依赖的对象

- `TBAcctGroup`
- `TBAcctType`
- `TBTransaction`
- `TBCategory`
- `TBCurrency`
- `TBPerson`

### P1：财务实用功能

- `TBBudget`
- `TBRemindSetting`
- `TBTemplate`
- `TBPayModeHistory`

### P2：投资重度功能

- `TBSecurities`
- `TBOpenFund`
- `TBPreciousMetals`
- `TBFuturesGoods`
- `TBFinancingContract`

### P3：计划与同步

- `TBFP*`
- `TBGoal*`
- `TBSync*`
- `TBReportSettings`

## 9. 对 Rust 代码的直接映射

- `accounts` 模块：
  - 对齐 `TBAcct*`
- `transactions` 模块：
  - 对齐 `TBTransaction`、`TBStatement`、`TBTemplate`
- `investments` 模块：
  - 对齐 `TBSecurities`、`TBOpenFund`、`TBPreciousMetals`、`TBFutures*`
- `planning` 模块：
  - 对齐 `TBBudget`、`TBRemind*`、`TBFP*`、`TBGoal*`
- `sync` 模块：
  - 对齐 `TBSync*`
- `reports` 模块：
  - 对齐 `TBReportSettings` 与 `TRpt*` 窗体资源
