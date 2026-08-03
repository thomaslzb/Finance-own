# 类似系统对标结论

本文档用于回答两个问题：

1. 市面上类似的个人财务系统，通常把哪些能力做成“标配”。
2. `MoneyHome8` Rust 重构时，哪些能力必须保留，哪些能力可以用更现代的方式重做。

对标对象选择原则：

- 必须是个人财务或家用账本领域
- 尽量覆盖不同产品形态：
  - 本地优先
  - Web/同步型
  - 桌面会计型
  - 轻量桌面型

本次选取的参考对象如下，初次于 `2026-07-28` 查看，并于 `2026-08-02` 复核官方资料：

- `Actual Budget`
- `Firefly III`
- `GnuCash`
- `HomeBank`

证据使用原则：

- 产品能力只采用官网、官方文档或官方源码仓库
- “强/中/弱”仅用于相对比较，不作为需求证据
- 真正进入开发范围的内容必须落到第 4 节的产品决策
- Firefly III 文档站对当前自动化请求返回 Cloudflare 验证页，相关能力改用其官方 GitHub 仓库、文档源码和应用源码交叉确认

## 1. 总体观察

四个系统虽然侧重点不同，但都反复出现了几类共性能力：

- 账户体系
- 分类/标签/预算
- 交易录入与转账
- 周期性交易或计划交易
- 报表与趋势分析
- 导入导出

而 `MoneyHome8` 相比这四类产品，明显更重的能力在于：

- 投资品种更丰富
- 资产类型更复杂
- 财务规划/目标/诊断更重
- 本地参考库、行情、费率、提醒联动更多

所以我们的重构目标不应只是“做一个普通记账软件”，而应是：

- 以现代本地架构，重做一个覆盖 `MoneyHome8` 业务广度的个人财务工作台

## 2. 逐个系统看可借鉴点

### 2.1 Actual Budget

官方资料显示，`Actual Budget` 当前强调：

- 账户统一视图
- 转账
- 预算
- 报表
- 同步
- 银行同步

它的强项：

- 本地优先和多端同步思路很清晰
- 预算系统很成熟
- 报表与自定义分析能力强
- 账户分为预算内/预算外，这对现金流与投资分层很有参考价值
- 账户关闭会要求处理现有余额，同时保留关闭账户的历史入口并支持重新打开
- 计划交易支持一次性或周期、自动入账或人工批准、多日期、周末前后移动，以及精确值、近似值和金额区间
- 计划可从历史交易创建、主动寻找匹配交易或从历史中识别周期模式，并与规则联动补充分类和备注
- 报表支持多个自定义仪表盘、保存筛选和动态/固定日期范围；现金流与净资产采用不同账户范围
- 同步明确区分本地真相、服务器副本、同步重置、同步代际和冲突恢复，并允许可选端到端加密

它对我们的启发：

- `MoneyHome8` 重构后可以借鉴“预算账户”和“投资账户”分层思路
- 预算不应只是一个列表页，而应能直接联动现金流与分类
- 报表应该支持：
  - 默认报表
  - 可扩展报表
  - 未来自定义查询
- 计划不能只保存“下次执行时间”，还要保存发生实例、人工批准状态、匹配结果和跳过原因
- 账户关闭必须是生命周期命令，不等于删除；余额转移、关闭标记和历史可查必须原子完成

需要明确保留的差异：

- Actual 的预算外账户交易不能分类，适合轻量余额跟踪
- MoneyHome8 的投资、重大资产和债权债务仍需要分类、标签、人员和专项交易语义
- 因此新系统可以借鉴“是否参与预算”的账户属性，但不能照搬“预算外账户禁止分类”的限制

它不覆盖或较弱的地方：

- `MoneyHome8` 那种多投资品种、多资产子域深度并不是其主战场

### 2.2 Firefly III

官方资料显示，`Firefly III` 当前强调：

- 账户
- 交易
- 预算
- 分类
- 标签
- 周期性交易
- 规则
- 附件

它的强项：

- 交易组织能力很强
- 周期性交易和自动化思路清楚
- 预算、分类、标签、规则之间边界明确
- 附件能力成熟
- REST JSON API 覆盖其大部分产品能力，适合作为模块边界和自动化接口参考
- 官方仓库明确把复式记账、周期交易、规则、目标储蓄、多币种和收支报表列为核心能力

它对我们的启发：

- `MoneyHome8` 重构时，交易系统应保留：
  - 分类
  - 标签
  - 周期计划
  - 规则/模板
- 附件不应再停留在“可能有”层面，应该作为正式能力建模
- 规则引擎可以成为后续增强点：
  - 自动分类
  - 自动标签
  - 自动提醒

它不完全适合直接照搬的地方：

- 它的预算和对象组织方式与 `MoneyHome8` 的“投资 + 规划 + 提醒”混合场景不完全一致
- 它是自托管 Web 应用；我们的首版仍应是无需常驻服务器的本地桌面应用

### 2.3 GnuCash

官方资料显示，`GnuCash` 当前强调：

- 复式记账
- 股票/债券/基金账户
- 多币种
- 计划交易
- 30+ 报表
- 投资组合估值
- SQLite/MySQL/PostgreSQL 等存储支持

官方同时明确提示 SQL 数据库存储仍带有实验性说明，并提到部分边界场景存在数据丢失报告。该事实只能证明 GnuCash 支持多种存储后端，不能据此推导本项目也需要多数据库支持。

它的强项：

- 投资账户、证券、基金、币种严谨
- 报表体系成熟
- 财务口径强
- 计划交易与对账成熟

它对我们的启发：

- 投资域不能只做“买卖记录”，必须有：
  - 持仓
  - 成本
  - 市值
  - 盈亏
  - 收益率
- 多币种、汇率、资产负债必须从一开始就在模型上站稳
- 报表层要支持资产负债、投资估值、预算相关视图
- 贷款必须能表达本金取得、利息和本金拆分还款、计划、提前结清及资产关系；投资必须保留批次与资本利得关系

它不适合完全照搬的地方：

- `GnuCash` 的复式记账导向更强
- `MoneyHome8` 是更偏家庭财务运营工具，而不是纯会计软件

所以更合适的路线是：

- 保留复式/平衡思想的可审计性
- 但不要把 UI 和业务交互做得像专业会计账套
- 保持单一 SQLite 主账本，先把事务、备份和迁移验证做扎实，不增加无实际需求的数据库方言

### 2.4 HomeBank

官方资料显示，`HomeBank` 当前强调：

- 预算
- 计划交易
- 现金流预测
- 动态图表和过滤报表
- 自动化辅助

它的强项：

- 桌面场景轻快
- 录入效率和报表可读性好
- 对普通个人用户更友好
- 官方列出的模板、分类拆分、内部转账、多币种、导入导出和错误预防能力，说明桌面效率不仅是视觉问题，还依赖高频命令的完整闭环
- 导入支持 QIF、OFX、QFX 和 CSV，并在提交前识别重复交易
- 计划交易既可自动化内部转账，也可作为现金流预测输入
- 交易支持批量编辑、标签、提醒状态、模板复用和分类拆分

它对我们的启发：

- `MoneyHome8` 重构后的桌面交互不应过重
- 要保留“快速录入 + 快速查账 + 快速看图”的节奏
- 现金流预测、计划与提醒可以先做成实用型页面，而不是复杂的金融建模入口

它不覆盖的地方：

- 投资深度明显不如 `MoneyHome8`
- 财务规划和目标模块也没有原软件那么重

## 3. 对标矩阵

| 维度 | MoneyHome8 现状 | Actual Budget | Firefly III | GnuCash | HomeBank | 对我们最有价值的借鉴 |
| --- | --- | --- | --- | --- | --- | --- |
| 账户体系 | 很强，类型繁多 | 强 | 强 | 很强 | 中 | `GnuCash` 严谨度 + `Actual` 分层思路 |
| 收支/转账 | 强 | 强 | 强 | 强 | 强 | `Firefly` 规则化交易组织 |
| 预算 | 强 | 很强 | 强 | 中高 | 强 | `Actual` |
| 周期交易/计划 | 强 | 中高 | 很强 | 强 | 强 | `Firefly` + `HomeBank` |
| 标签/分类/人员 | 强 | 中高 | 很强 | 中 | 中 | `Firefly` |
| 报表 | 很强 | 强 | 中高 | 很强 | 强 | `GnuCash` + `Actual` |
| 投资域 | 很强 | 中 | 弱到中 | 很强 | 弱 | `GnuCash` |
| 财务规划/目标 | 很强 | 中 | 中 | 弱 | 弱 | 原软件自身最有特色，需保留 |
| 本地优先 | 强 | 很强 | 中 | 强 | 强 | `Actual` + `HomeBank` |
| 同步 | 有 | 很强 | 中 | 弱 | 弱 | `Actual` |
| 附件/自动化 | 有线索 | 中 | 很强 | 中 | 中 | `Firefly` |

## 4. 对 Rust 重构的直接影响

### 4.1 官方证据到产品决策

| 官方事实 | 对本项目的直接决策 | 明确不照搬的部分 |
| --- | --- | --- |
| Actual 本地优先、离线可用、后台同步、可选端到端加密 | 本地 SQLite 始终是可独立工作的真相源；同步只能作为适配器增强 | 不让登录或网络状态阻塞本地记账 |
| Actual 区分预算内/预算外账户 | 账户增加“是否参与预算”规则，预算投影只消费纳入范围 | 不禁止投资或预算外账户使用分类、标签和专项交易 |
| Actual 自定义报表支持表格和多类图表、动态/固定日期筛选 | `report_presets` 保存筛选和图表序列；表格、图表、导出共享查询 DTO | 不在 UI 层复制三套计算逻辑 |
| Firefly 支持预算、分类、标签、周期交易和规则处理 | 模板、计划、提醒和未来规则引擎共享交易命令入口 | 不把规则执行结果直接写成不可追溯余额 |
| Firefly 提供广覆盖 REST API，并把附件作为正式模型 | 应用服务保持可调用边界；附件采用独立元数据和关联表 | 首版不要求自托管服务器或 Web 化部署 |
| GnuCash 使用平衡分录、多币种、投资组合和计划交易 | 交易采用原子账户分录，投资拆分成交、持仓输入、批次和行情 | 不把专业复式会计术语强加给普通用户界面 |
| GnuCash SQL 后端仍带实验性风险提示 | 首版只支持经过完整验证的 SQLite 单文件账本 | 不为“看起来灵活”提前支持 MySQL/PostgreSQL |
| HomeBank 支持模板、拆分、转账、多币种、计划、预测和动态报表 | 桌面端优先优化录入、查账、筛选、预测和快捷命令 | 不以简化投资域换取表面上的轻量化 |
| Actual 计划支持精确/近似/区间金额、自动/人工执行、历史匹配和跳过 | 计划定义、发生实例、匹配关系和实际交易分离；预测只读取未完成实例 | 不把计划本身或预测值当作已过账财务事实 |
| Actual 账户关闭保留历史并可重开，HomeBank 导入先识别重复 | 账户关闭使用生命周期状态和显式余额处理；导入逐行保存重复判定与用户决策 | 不用物理删除模拟关闭，不用文件哈希替代逐笔重复检测 |
| Actual 同步重置指定某个本地副本为新真相 | 同步配置增加代际/重置语义，旧设备必须显式回退到新代际 | 不让同步重置删除当前设备的本地账簿或静默覆盖未同步修改 |

### 4.2 已进入当前设计的借鉴项

- `transactions + transaction_entries`：吸收 GnuCash 可审计分录思想，但保持家庭财务语义
- `report_presets + 查询投影`：吸收 Actual 的保存筛选和自定义分析思路
- `templates / schedules / rules` 边界：吸收 Firefly 和 HomeBank 的自动化组织方式
- `attachments + transaction_attachments`：把附件从长尾线索升级为正式模型
- `account.is_budgeted` 候选规则：借鉴 Actual 的预算范围分层，具体字段在预算模式迁移中落地
- `SQLite 本地真相 + 可选同步适配器`：结合 Actual 本地优先和 Firefly 自托管隐私取向
- `schedule occurrences + transaction links` 候选边界：计划定义、每次应发生实例、自动/人工批准、匹配和最终交易必须可分别审计
- `account lifecycle command`：关闭、重开、隐藏、注销和永久删除使用不同命令，不依赖单个布尔字段混用
- `import row decisions`：重复、接受、拒绝和人工覆盖逐行留痕，批次统计由明细重建
- `cash-flow forecast projection`：从当前余额、未完成计划和明确假设即时计算，不保存不可追溯的预测余额

### 4.3 必须保留的“行业标配”

如果缺了下面这些，重构后就会明显落后于类似系统：

- 账户体系
- 分类/标签
- 收支和转账
- 周期性交易或计划交易
- 预算
- 基础报表
- 导入导出

### 4.4 必须保留的 `MoneyHome8` 差异化能力

如果缺了下面这些，就不再是原软件的等价替代：

- 复杂账户类型
- 投资多子域
  - 证券
  - 基金
  - 外汇
  - 债券
  - 期货
  - 黄金/贵金属
  - 保险/社保
- 财务规划
- 财务目标
- 提醒与限额联动
- 行情/费率/汇率参考数据

### 4.5 可以用更现代方式重做的能力

这些不需要按原样复刻：

- 旧 `mh8` 表结构
- Jet/工作组权限体系
- 原有同步协议细节
- 原窗体组织细节

更推荐的重做方式：

- 用 `SQLite` 重建本地账本
- 用统一领域模型整合各类交易
- 用规则/模板机制取代部分旧式散乱窗体
- 用可扩展报表层取代部分硬编码报表窗体

## 5. 实现优先级再校准

结合原软件和对标系统，建议重新强调以下优先级：

### P0

- 账户中心
- 通用记账
- 转账
- 分类/标签/人员
- 预算
- 基础报表
- 附件正式模型
- 导入预览和可追溯映射

### P1

- 周期交易/计划交易
- 提醒
- 投资一览
- 证券/基金/外汇基础交易
- 交易规则基础设施，但首版只启用可解释的模板和计划规则

### P2

- 债券/期货/黄金/保险/社保
- 财务规划
- 财务目标
- 复杂投资报表

### P3

- 同步增强
- 云备份
- 自定义报表设计器
- 智能规则推荐

## 6. 最终对标结论

截至 `2026-08-02`，这四个类似系统给出的最重要结论是：

1. `Actual Budget` 证明了“本地优先 + 同步增强”是非常适合现代个人财务软件的路线。
2. `Firefly III` 证明了“交易规则、周期交易、附件、标签分类体系”是成熟产品的重要骨架。
3. `GnuCash` 证明了“投资、多币种、资产负债、报表严谨性”必须认真建模，不能只做 UI。
4. `HomeBank` 证明了“桌面场景里的轻快录入和动态报表”依然很重要。
5. `MoneyHome8` 自身最独特的价值，仍然在于“复杂资产域 + 财务规划/目标 + 本地参考数据联动”。

因此，Rust 重构的正确方向不是抄某一个竞品，而是：

- 用 `Actual` 的本地优先思路
- 用 `Firefly` 的交易组织能力
- 用 `GnuCash` 的财务严谨度
- 用 `HomeBank` 的桌面效率
- 去承接 `MoneyHome8` 自己更广的功能深度

## 7. 参考来源

以下资料于 `2026-07-28` 初次查阅，并于 `2026-08-02` 复核：

- [Actual Budget Website](https://actualbudget.org/)
- [Actual Budget Accounts Docs](https://actualbudget.org/docs/accounts/)
- [Actual Budgeting Docs](https://actualbudget.org/docs/budgeting/)
- [Actual Budget Release Notes](https://actualbudget.org/docs/releases/)
- [Actual Budget Reports Dashboard](https://actualbudget.org/docs/reports/)
- [Actual Budget Custom Reports](https://actualbudget.org/docs/reports/custom-reports)
- [Actual Budget Schedules](https://actualbudget.org/docs/schedules)
- [Actual Budget Sync](https://actualbudget.org/docs/getting-started/sync)
- [Firefly III Introduction and Features](https://docs.firefly-iii.org/explanation/firefly-iii/about/introduction/)
- [Firefly III Budgets](https://docs.firefly-iii.org/explanation/financial-concepts/budgets/)
- [Firefly III Recurring Transactions](https://docs.firefly-iii.org/how-to/firefly-iii/finances/recurring/)
- [Firefly III Official Repository](https://github.com/firefly-iii/firefly-iii)
- [Firefly III Repository README](https://github.com/firefly-iii/firefly-iii/blob/main/readme.md)
- [Firefly III Official Documentation Source](https://github.com/firefly-iii/docs)
- [Firefly III Attachment Model Source](https://github.com/firefly-iii/firefly-iii/tree/main/app/Models)
- [GnuCash Home](https://www.gnucash.org/)
- [GnuCash Features](https://www.gnucash.org/features.phtml)
- [GnuCash Guide - Features](https://www.gnucash.org/docs/v5/C/gnucash-guide/oview-features1.html)
- [GnuCash Guide - Accounts](https://www.gnucash.org/docs/v5/C/gnucash-guide/chapter_accts.html)
- [HomeBank Official Site](https://www.gethomebank.org/)
- [HomeBank Feature List](https://www.gethomebank.org/en/features.php)
