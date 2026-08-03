# 主账本字段语义证据

本文档整理当前从 `test.mh8` 字节流片段中直接观察到的少量高价值字段语义线索。

说明：

- 原始片段中存在大量编码噪音。
- 这里只保留已经能稳定看出业务含义的部分，不强行解释噪音内容。
- 这些线索仍然属于“认证未打通前的结构语义证据”，不是最终数据库事实。

## 1. `TBPerson`

从 `TBPerson` 附近可稳定看到以下字段名：

- `ID`
- `Name`
- `Type`
- `Birth`
- `BirthType`
- `Sex`
- `Address`
- `Connect`
- `Icon`
- `HideFlag`
- `uuid`

同时可见的中文提示包括：

- `唯一标识符 标识 人员/机构表`
- `类型 属于 人员/机构表`
- `性别 属于 人员/机构表`
- `人员/机构表名`

当前高可信结论：

- `TBPerson` 并非只保存自然人，还可能保存“人员/机构”混合对象。
- 这与先前从样本中抽出的银行、保险公司名称是相互印证的。
- `Person` 实体在 Rust 中不应只按“联系人”建模，更像：
  - 人
  - 机构
  - 往来方

## 2. `TBTransType`

从 `TBTransType` 附近可稳定看到：

- 字段：
  - `ID`
  - `Name`
- 中文提示：
  - `Name 属于 交易类型表 资产的占有户头`

同时周边可见：

- `在设计视图中创建查询`
- `在设计视图中创建窗体`
- `在设计视图中创建报表`
- `在设计视图中创建数据访问页`

当前高可信结论：

- `TBTransType` 是交易类型基础字典表。
- 旧库内部保留了 Access 设计器级元数据，说明主账本并不是被完全“去结构化”封装。

## 3. `TBRemindSetting`

从 `TBRemindSetting` 附近可稳定看到：

- 字段：
  - `ID`
  - `RemindType`
  - `ObjectID`
  - `MinValue`
  - `MaxValue`
  - `IsRemind`

可见中文提示包括：

- `最大值`

当前高可信结论：

- `TBRemindSetting` 很可能支持阈值型提醒，而不只是日期提醒。
- 结合 `MinValue / MaxValue / IsRemind`，推断其至少能表达：
  - 上限提醒
  - 下限提醒
  - 是否启用

## 4. `TBPreciousMetals`

从 `TBPreciousMetals` 附近可稳定看到：

- 字段：
  - `PreciousMetalsName`
  - `CurrType`
  - `TransObjID`
  - `ID`

当前高可信结论：

- 贵金属对象本身具有独立名称、计价币种和交易对象关联。
- Rust 中不应把贵金属当成普通证券代码直接复用证券实体，应保留独立实体或独立扩展字段。

## 5. `TBCurrency`

从 `TBCurrency` 相关索引片段可稳定看到：

- `IDX_TBCurrency_CashOrBill4...`
- `IDX_TBCurrency_ChineseName4...`
- `IDX_TBCurrency_EnglishAbbr2...`
- `IDX_TBCurrency_TransObjID`

当前高可信结论：

- 币种表不仅仅是显示名称表，还承担：
  - 中文名称检索
  - 英文缩写检索
  - 现金/票据口径区分
  - 与交易对象的映射

## 6. 对 Rust 重构的直接意义

### `Person`

- 应建模为“人员/机构/往来方”统一抽象，而不是只做自然人。

### `Reminder`

- 应保留阈值型提醒字段，例如：
  - `min_value`
  - `max_value`
  - `enabled`

### `PreciousMetal`

- 应保留独立实体或独立扩展结构，不建议仅复用 `Security`。

### `Currency`

- 应至少保留：
  - 中文名
  - 英文缩写
  - 与交易对象的关联键

## 7. 当前价值

虽然这些语义证据还不足以替代表结构枚举，但它们已经足以：

1. 收窄实体定义方向
2. 收窄字段命名方向
3. 避免后续 Rust 领域模型严重偏离原业务口径
