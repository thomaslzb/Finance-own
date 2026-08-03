# 运行态窗口树证据

本文档记录 2026-07-28 直接对正在运行的 `MoneyHome8.exe` 主窗口进行 Win32 子控件枚举时得到的证据。

这份证据的重要性高于：

- 资源字符串弱提示
- 文件名推断
- 误命名截图

因为它来自当前真实运行进程的窗口树，而不是静态猜测。

## 1. 方法说明

本轮没有使用截图识别，而是直接对运行中进程执行：

- `Get-Process`
- `EnumWindows`
- `EnumChildWindows`
- `pywinauto` 的 `win32` 只读连接

说明：

- 当前 Python 环境为 `64-bit`
- 目标程序为 `32-bit`
- 当前脚本未以管理员权限运行

因此本轮能力边界是：

- `可读取` 窗口与子控件树
- `可读取` 标题、类名、矩形位置
- `不稳定/不适合` 直接发起页面切换操作

## 2. 命中的主窗口

本轮稳定命中的关键窗口：

- `TMoneyHome8`
  - 标题：`财智8`
  - 可见：`True`
- `TApplication`
  - 标题：`test - 财智8`
  - 可见：`True`

这说明：

- 当前测试账本 `test.mh8` 已在原软件中打开
- 程序主壳和账本容器都处于真实运行状态

## 3. 当前主壳中直接抓到的关键控件

以下控件来自 `TMoneyHome8` 主窗口的直接子孙树：

### 3.1 工作区页签级结构

- `TRzPageControl`
- `TRzTabSheet`
  - `资产`
- `TRzTabSheet`
  - `分析`
- `TRzTabSheet`
  - `目标`

这是一个非常强的运行态证据，说明主壳内部确实存在至少三个页签语义：

- 资产
- 分析
- 目标

它们与我们之前从截图和功能分析形成的判断是相互印证的：

- `财务数据`
  - 对应资产/账户浏览中心
- `财务分析`
  - 对应分析中心
- `财务目标`
  - 在主壳内部拥有独立页签位置，而不是普通弹窗

### 3.2 当前激活业务页

- `TAccountManagerFm`
  - 标题：`账户中心`
  - 矩形：`(L290, T51, R1920, B1032)`

这证明：

- 当前主壳右侧主内容区确实承载 `账户中心`
- 之前截图中的 `账户中心` 不是一次性弹窗，而是运行中主工作区内容页

### 3.3 当前账户中心操作区

本轮直接抓到以下真实控件文本：

- `所有账户类型`
- `按账户类型查看`
- `新增账户组`
- `新增账户`
- `操作`

这与：

- [data-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-page-observations.md)
- 账户中心截图

完全一致，属于运行态再次确认。

### 3.4 当前账户类型列表

本轮直接抓到以下列表项文本：

- `现金`
- `活期（卡折）`
- `定期`
- `第三方储值`
- `上市证券`
- `开放式基金`
- `外汇`
- `重大资产`
- `应付款`
- `预收款`
- `应收款`

这说明这些类型并不是 OCR 误识别，而是当前运行控件里真实存在的文本项。

## 4. 直接意义

## 4.1 对 `财务数据` 工作区的意义

当前可以把以下判断升级得更硬：

- `账户中心` 为真实运行页
- 顶部操作按钮为真实运行控件
- 账户类型列表为真实运行控件文本

因此：

- `财务数据 -> 账户中心`
  - 已经不只是截图级证据
  - 还是运行态控件树级证据

## 4.2 对总信息架构的意义

当前最有价值的新证据，不是又确认了一次 `账户中心`，而是运行态主壳里直接暴露了：

- `资产`
- `分析`
- `目标`

三个 `TRzTabSheet`

这使我们对整体结构的判断更稳：

- 主壳内部不是简单单页
- 至少包含多页签/多容器结构
- 资产、分析、目标在运行时就是主导航级别的概念

## 4.3 对当前缺口的影响

本轮没有直接补到：

- `记账` 工作区真实页面
- `财务分析` 下诊断/规划/目标子页具体内容
- `财务报表` 投资类具体子项

但本轮显著强化了：

- `财务数据` 工作区的运行态真实性
- 主壳内部页签式结构

## 5. 当前边界与限制

本轮日志里同时出现两条工具层警告：

- `32-bit application should be automated using 32-bit Python`
- `Python process has no rights to make changes in the target GUI (run the script as Administrator)`

这意味着：

- 当前最适合做只读枚举
- 不适合在这套环境里直接承诺稳定点击切页

所以本轮最稳妥的使用方式是：

- 把它作为“运行态结构确认工具”
- 暂不把它当成完整 UI 自动化回放工具

补充说明：

- 2026-07-28 继续对：
  - `所有账户类型`
  - `按账户类型查看`
  - `操作`
  这类低风险按钮做了消息级点击探测
- 已尝试：
  - `BM_CLICK`
  - `WM_LBUTTONDOWN / WM_LBUTTONUP`
- 当前都没有稳定弹出新的可见下拉菜单

因此本轮再次确认：

- 当前环境适合只读枚举
- 不适合把消息级点击当作稳定切页手段

## 6. 与现有文档的关系

这份文档应与以下文档配合阅读：

- [data-page-observations.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\data-page-observations.md)
- [workspace-map.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\workspace-map.md)
- [functional-ledger.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\functional-ledger.md)
- [verified-vs-pending-index.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\verified-vs-pending-index.md)

## 7. 当前结论

截至 `2026-07-28`，可以确认：

1. `test.mh8` 已在原程序中实际打开。
2. 运行中主壳 `财智8` 可以被直接枚举到真实子控件树。
3. `账户中心`、其操作区按钮、以及账户类型文本都已被运行态控件树直接证实。
4. 主壳内部至少存在 `资产 / 分析 / 目标` 三个页签语义。

这已经是对现有 UI 结构分析的一次明显加固。

## 8. 后续运行时 DFM 补证

本文件第 4.3 节保留的是窗口树探测当时的结论。随后从普通权限副本内存中完整解析了 `460` 个真实 DFM，已补齐：

- 记账公共录入、转账、分拆、模板、计划和流水操作
- 财务诊断、规划、目标的静态控件与字段
- `25` 张报表及 `12` 张投资类报表标题

这些内容现在属于运行时直接结构证据，但页面截图和真实计算结果仍待验证。详见 [runtime-dfm-functional-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-dfm-functional-evidence.md)。
