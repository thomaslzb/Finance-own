# 运行态组件清单

本文档基于 2026-07-28 对 `MoneyHome8.exe` 运行中窗口树的递归枚举结果，整理当前已经在进程内实际加载出来的关键窗体、页签和组件。

这份清单的价值在于区分三类情况：

1. 只在资源里存在
2. 已在运行进程中实际加载
3. 已加载且当前可见

这样后续判断证据强度时会更稳。

依赖文档：

- [runtime-window-tree-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-window-tree-evidence.md)
- [resource-form-family-index.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\resource-form-family-index.md)
- [verified-vs-pending-index.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\verified-vs-pending-index.md)

## 1. 当前运行上下文

本轮命中的真实运行窗口：

- `TMoneyHome8`
  - 标题：`财智8`
  - 可见：`True`
- `TApplication`
  - 标题：`test - 财智8`
  - 可见：`True`

这说明：

- 测试账本 `test.mh8` 当前已在原程序中打开
- 以下组件都不是“静态资源存在”，而是运行中进程里可枚举到的对象

## 2. 已加载且当前可见的关键业务组件

### 主壳与页签

- `TMoneyHome8`
  - `财智8`
- `TRzPageControl`
- `TRzTabSheet`
  - `资产`
- `TRzTabSheet`
  - `分析`
  - 当前隐藏
- `TRzTabSheet`
  - `目标`
  - 当前隐藏

结论：

- `资产 / 分析 / 目标` 已不是纯推断，而是运行态主壳中的真实页签语义

### 当前可见业务页

- `TAccountManagerFm`
  - `账户中心`

### 当前可见账户中心操作组件

- `TRzMenuButton`
  - `所有账户类型`
- `TRzMenuButton`
  - `按账户类型查看`
- `TRzBitBtn`
  - `新增账户组`
- `TRzBitBtn`
  - `新增账户`
- `TRzMenuButton`
  - `操作`

### 当前可见账户类型组件

- `TmwAccountList`
  - `现金`
- `TmwAccountList`
  - `活期（卡折）`
- `TmwAccountList`
  - `定期`
- `TmwAccountList`
  - `第三方储值`
- `TmwAccountList`
  - `上市证券`
- `TmwAccountList`
  - `开放式基金`
- `TmwAccountList`
  - `外汇`
- `TmwAccountList`
  - `重大资产`
- `TmwAccountList`
  - `应付款`
- `TmwAccountList`
  - `预收款`
- `TmwAccountList`
  - `应收款`

## 3. 已加载但当前隐藏的关键业务组件

### 分析与目标页签容器

- `TRzTabSheet`
  - `分析`
  - 当前不可见
- `TRzTabSheet`
  - `目标`
  - 当前不可见

并且它们各自已经挂了子组件：

- `分析`
  - `TMWTreeView`
- `目标`
  - `TMWEntryView`

这说明：

- `分析` 和 `目标` 当前不仅仅是空名字
- 它们在运行中已有自己的容器与内容承载控件
- 只是本轮还没拿到子控件文本

补充边界：

- 本轮继续尝试对低风险菜单按钮做消息级点击
- 仍未能切换到 `分析` / `目标` 页签实际内容

因此当前只能把它们升级为：

- `运行态已加载`

而不能升级为：

- `页面内容已实测`

### 账户相关隐藏页

- `TAccountOverviewDlgFm`
  - 标题：`账户概况`
  - 当前隐藏

这是一条有价值的新证据：

- 账户体系中不仅有 `账户中心`
- 还存在运行态加载过的 `账户概况` 页/窗体

### 计算器相关隐藏页

- `TCalcuFm`
  - 标题：`CalcuFm`
  - 当前隐藏

这与之前从资源与功能目录看到的：

- 内置计算器

形成了运行态印证。

### 主题相关隐藏页

- `TThemeUIFm`
  - 标题：`ThemeUIFm`
  - 当前隐藏

配套还能看到隐藏分组框标题：

- `默认主题图片`
- `使用主题图片`

这说明：

- 程序内部存在主题/皮肤相关配置 UI
- 这属于系统与外观配置层，而不是纯资源残留

## 4. 已加载的基础技术组件

以下组件不是直接业务功能，但说明了当前 UI 技术栈：

- `TNodeForm`
  - `NODEWRAP`
- `TNodeWrapForm`
- `TWkeWebbrowser`
- `wkeWebWindow`

结论：

- 当前主界面里至少嵌入了一层 Web 容器/浏览器壳
- 后续如果要理解某些页面为什么标题少、文本抓不到，这可能是原因之一

## 5. 证据强度升级

与之前相比，这份清单让以下判断的证据等级上升：

### 从“高可信”上升到“运行态已加载”

- `资产 / 分析 / 目标` 主壳页签语义
- `账户概况`
- `计算器`
- `主题 UI`

### 仍然不能升级到“页面内容已实测”

虽然 `分析` 和 `目标` 页签已加载，但本轮还不能说：

- `财务诊断` 内容已实测
- `财务规划` 内容已实测
- `财务目标` 内容已实测

因为：

- 当前只看到隐藏容器
- 还没有读到这些页里的业务文本或字段

## 6. 对当前缺口的影响

本轮实质缩小的是“结构真实性”缺口，而不是“内容细节”缺口。

更具体地说：

### 已缩小

- `财务分析` / `财务目标` 属于主壳页签，而不是旁路猜测
- `账户概况`、`计算器` 等长尾功能不仅资源存在，运行时也被加载

### 尚未缩小

- `记账` 工作区真实页面
- `财务分析` 子页真实内容
- `财务报表` 投资类真实子项
- `test.mh8` 正式认证后的主表结构

## 7. 当前结论

截至 `2026-07-28`，可以更稳地说：

1. `MoneyHome8` 主壳是一个多页签、多容器结构，而不是单页容器。
2. `资产 / 分析 / 目标` 在运行态都已经是实际存在的页签语义。
3. `账户概况`、`计算器`、`主题 UI` 都已有运行态加载证据。
4. 这些运行态组件可以用来进一步校正哪些功能只是“资源存在”，哪些已经“真实挂进主程序”。

## 8. 后续运行时 DFM 补证

本文件记录的是窗口树阶段当时的证据边界。随后通过普通权限副本内存提取，已经完整解析 `460` 个真实 DFM：

- `记账` 的录入、转账、分拆、模板、计划和流水字段/命令已确认
- 财务诊断、规划、目标的静态结构和代表性动态页面均已确认
- `12` 张投资类子报表及趋势序列已确认

因此第 6 节“尚未缩小”中的三个 UI 项现已在结构层关闭；仍待的是截图、跳转和真实计算结果。详见 [runtime-dfm-functional-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-dfm-functional-evidence.md)。
