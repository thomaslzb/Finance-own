# MoneyHome8 AI、控制台与金额计算器代码合同

本文档基于隔离运行副本的 Delphi published RTTI、运行时解包代码、VCL/BPL 导出符号和 DFM 控件树形成。逐方法地址、反汇编、字符串引用和源程序哈希见 [runtime-method-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-method-evidence.md) 与 [runtime-method-evidence.json](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-method-evidence.json)。

## 1. 结论

| 表面 | 原程序性质 | 已证明合同 | Rust 版范围决策 |
|---|---|---|---|
| `TAIPanelDlg` | 实验性、置顶 WebView AI 面板 | 本地 HTML、JavaScript 桥、三类外部 HTTP 接口、MD5 签名和响应协议 | 独立可选适配器，默认关闭；禁止照搬明文 HTTP 和内置秘密 |
| `TConsoleFm` | 内部诊断控制台 | `Ctrl+F12`、三页控制台、最近 10 条历史、25 个命令类、回调协议和窗口状态 | 仅开发/诊断构建启用，与普通财务功能和用户数据权限隔离 |
| `TCalcuFm` | 共享金额计算器宿主 | 结果、错误、`Esc`、方向上键均关闭弹窗；错误单独置位 | 作为金额输入控件共享弹层保留，动态补齐回填、错误文案和焦点结果 |

## 2. 金额计算器合同

### 2.1 已证明行为

- `TCalcuFm.FormCreate` 同步内部计算器面板与宿主窗体尺寸，初始化计算器组件，并把错误标志清零。
- `dxCalculatorError` 先把错误标志置为 `1`，再调用 `vcl70.bpl!TCustomForm.Close`。
- `dxCalculatorResult` 直接调用同一个 `TCustomForm.Close`。
- `FormKeyDown` 识别 `VK_ESCAPE (0x1B)` 和 `VK_UP (0x26)`；命中后把按键值清零并关闭窗体，避免按键继续传给原金额输入框。
- `FormDestroy` 释放计算器组件资源。
- 该宿主由 `160` 个窗体中的 `429` 个 `TMHCalcuEdit` 复用，不是独立业务页面。

### 2.2 Rust 实现要求

- 金额编辑器以共享弹层打开计算器，不复制 429 套计算逻辑。
- 有效结果只有在明确完成时回填；取消或键盘关闭不得改变原值。
- 计算错误必须与取消区分，保留原值并展示可理解的错误原因。
- `Esc` 和方向上键关闭弹层并消费按键；关闭后焦点回到原金额输入框。
- 金额解析、精度和四舍五入必须由统一金额类型处理，不能使用二进制浮点作为账务真相。

B19 已确认在日常收支 `TMHCalcuEdit` 聚焦后按 `F4` 可打开共享计算器，并动态观察到完整按键布局。尚待确认：除零或非法表达式文案、错误标志如何影响调用方、结果回填时机、键盘关闭结果与焦点选择范围。

## 3. 内部控制台合同

### 3.1 入口与生命周期

- 快捷键设置页在 `FormCreate` 中把 `edtConsole` 写为 `0x407B`，即 `Ctrl+F12`。
- 老板键从配置对象读取；值为空时回退为 `0x4031`，即 `Ctrl+1`。老板键不是控制台键。
- 标题栏关闭按钮调用 `vcl70.bpl!TCustomForm.Hide`，因此关闭后保留控制台实例、页面与命令历史。
- 窗体销毁前把 `Width / Height / Left / Top` 保存到 `ConsoleFm` 配置节。

### 3.2 页面与历史

- 三个页签分别为主控制台、网银插件与网络、SQL，三者加载同一个 `Console.htm` 本地页面。
- 主控制台执行 `console.setOptions({"readOnly": 0, "commandHistory": ...})`，允许输入命令并恢复历史。
- 网络页和 SQL 页执行 `console.setOptions({"readOnly": 1})`，只显示诊断消息。
- 历史从配置键 `Moneyhome / cmdHistory` 读取；定时器把最后 `10` 条命令序列化后交给 `system.saveHistory(...)`。
- 日志进入页面前会处理反斜杠、引号、回车和换行，再通过 `console.message(...)` 注入对应 WebView。
- `WebBrowserAlertBox` 接收 JSON 回调；字段 `id` 减 `1000` 后映射到内部回调列表。无法匹配时记录“命令错误”。
- 菜单项“清除控制台记录”的 Delphi 事件处理器只有 `ret`，静态上没有清空副作用；需动态确认是否由网页上下文菜单处理。
- B19 快捷键设置页动态显示控制台为只读 `Ctrl+F12`，但当前自动化会话未打开可见 `TConsoleFm`；可达前置条件仍未闭环。

### 3.3 已注册命令

页面就绪后注册下列 `25` 个命令类：

| 注册范围 | 命令类 |
|---|---|
| 基础诊断 | `THelpCommand`、`TSaveConsoleSettingsCommand`、`TMoneyHomeIniCommand`、`THashCommand`、`TSystemInfoCommand`、`TClearSyncAccountCommand` |
| 特定运行模式 | `TShowFormClassNameCommand`、`TSystemEncryptCommand`、`TBase64Command`、`TExecuteSQLCommand`、`TGenDataScriptCommand`、`TTestCommand` |
| 条件网络诊断 | `TNetworkDebugCommand` |
| 高风险维护 | `TFixCurrencyCommand`、`TFixCodeCommand`、`TFixPriceCommand`、`TFixADOCommand`、`TSetVarCommand`、`TRemoteCommand`、`TSQLCommand`、`TQuickIncExpCommand`、`TServerCheckCommand`、`TReactivationCommand`、`THttpServerLogCommand`、`TRenameBookCommand` |

类名直接证明命令能力存在，但命令语法、参数、返回格式和真实副作用仍需通过 `help` 输出和隔离测试库动态校准。

### 3.4 Rust 实现边界

- 控制台不得进入普通用户默认导航，只能由显式开发/诊断开关启用。
- SQL、远程、修复、重命名和重新激活命令必须使用结构化命令接口；不得把任意字符串直接交给 SQLite 或系统 Shell。
- 诊断日志必须脱敏，不记录账本密码、同步凭据、AI key、完整账户号或可识别的财务明细。
- 主控制台命令历史单独存储，最多保留数量可配置；默认不进入账本备份和同步。
- “隐藏窗口”与“销毁窗口”保持不同语义，避免每次关闭丢失诊断上下文。

## 4. AI 外部服务合同

### 4.1 本地页面与 JavaScript 桥

- `FormShow` 加载 `data/AIPanel.html`。
- 页面就绪后调用 JavaScript `init`；内容准备调用 `prepare`；结果展示调用 `showContent`。
- 通用桥接格式为 `o.%s(\`%s\`, \`%s\`);`，参数在注入前进行转义。
- WebView 控制台消息按 `%s - %s, Line: %d` 格式转发到内部控制台；网页 alert 由桌面警告框显示。

### 4.2 外部端点与请求字段

原程序包含三个明文 HTTP 端点：

- `http://ai.smallisfine.com/v1/consult?question=%s&key=%s&_=%s&sign=%s`
- `http://ai.smallisfine.com/v1/explanation?terminology=%s&key=%s&_=%s&sign=%s`
- `http://ai.smallisfine.com/v1/faq?subject=%s&key=%s&_=%s&sign=%s`

请求数据包括用户输入、`key`、时间值 `_` 和 `sign`。咨询使用问题输入，术语解释使用术语输入；FAQ 是否启用由运行状态决定。

### 4.3 key 与签名

- 请求 key 要求长度为 `16`；不满足时走清空或固定值回退路径。
- 程序内存在两个 16 字符常量：`3141592653589793` 和 `1234567812345678`。
- 签名输入按 `%s%s%s%s` 拼接：编码后的用户输入、key、时间值和固定秘密。
- 哈希算法字符串为 `md5`。
- 最终 URL 由输入、派生 key、时间值和签名格式化，当前 URL 保存到面板实例，随后创建异步请求对象。

### 4.4 响应协议

- 响应先去除可选 UTF-8 BOM，再转换为内部字符串。
- 短响应会检查 `:::` 分隔符并提取状态码；程序常量包含成功码 `200` 和无内容/更新中码 `204`。
- 异常状态按 `内容获取出错（%s: %s）` 记录当前 URL 和状态信息。
- 无可用内容时调用页面 `prepare` 显示“内容正在更新中，请稍后再试。”。
- 有内容时进入 `showContent` 页面注入路径。

### 4.5 Rust 安全要求

- AI 必须是财务核心之外的 `ExternalAiAdapter`，默认禁用；离线记账、查询、报表和备份不能依赖它。
- 不兼容原明文 HTTP。只有配置 HTTPS 端点、通过证书校验并明确取得用户同意后才能发送请求。
- 默认只发送用户在 AI 面板中主动输入的文本，禁止自动附带账户、交易、预算、负债、投资持仓或报表数据。
- key 和签名秘密不得硬编码在客户端；使用系统凭据存储或用户自管配置，并对日志做脱敏。
- 请求必须支持超时、取消、重试上限、响应大小上限和内容类型校验。
- 旧端点、MD5 和旧状态协议只属于迁移证据，不是新实现的安全设计依据。
- B19 未发现 AI 用户入口，且没有向旧明文 HTTP 端点发送请求；在安全替代端点和明确同意机制完成前维持默认关闭。

## 5. 动态补证清单

1. 用 `Ctrl+F12` 验证控制台真实可达条件，执行 `help` 并记录 25 个命令的名称、参数和输出。
2. 切换三个页签，确认主控制台可输入、网络和 SQL 页只读，并验证最近 10 条历史的保存与恢复。
3. 测试“清除控制台记录”是否由网页层实现，以及隐藏再打开后页面和历史是否保留。
4. 在 `TMHCalcuEdit` 中验证计算器唤起、结果回填、错误提示、`Esc`、方向上键和焦点恢复。
5. 只在明确同意和隔离网络环境下验证 AI 页面；记录实际发送字段，不向旧 HTTP 端点发送真实财务数据。
