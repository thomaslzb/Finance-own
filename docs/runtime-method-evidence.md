# MoneyHome8 特殊窗体运行时方法证据

本文件由 `tools/summarize_runtime_methods.py` 从隔离运行副本的已解包内存生成；工具不打开或修改账本。

## 覆盖摘要

- 目标类：4 个
- Delphi published 方法：31 个
- 额外命名例程：19 个
- 控制台命令类：25 个
- 源程序 SHA-256：`11e6197f3205a2a5d1b8252da32e859f76cc31b4edf1b0bebfac87ff5011d956`

## 类与方法

### `TAIPanelDlg`：实验性 AI 面板

类元数据 RVA `0x3dcdfc`，方法表 RVA `0x3dcd7a`。

| 方法 | 代码 RVA | 指令数 | 字符串引用 |
|---|---:|---:|---|
| `WebBrowserConsoleMessage` | `0x3ddd24` | 43 | `%s - %s, Line: %d` |
| `FormShow` | `0x3dddd0` | 9 | `data/AIPanel.html` |
| `WebBrowserDocumentReady` | `0x3dde08` | 37 | `init` |
| `WebBrowserAlertBox` | `0x3dde98` | 24 | - |
| `btnCaptionCloseClick` | `0x3ddf98` | 2 | - |

### `TCalcuFm`：共享金额计算器宿主

类元数据 RVA `0xfaa30`，方法表 RVA `0xfa9c8`。

| 方法 | 代码 RVA | 指令数 | 字符串引用 |
|---|---:|---:|---|
| `FormCreate` | `0xfaae8` | 22 | - |
| `FormDestroy` | `0xfab44` | 4 | - |
| `dxCalculatorError` | `0xfab54` | 3 | - |
| `dxCalculatorResult` | `0xfab64` | 2 | - |
| `FormKeyDown` | `0xfab6c` | 11 | - |

### `TConsoleFm`：内部诊断控制台

类元数据 RVA `0x45a64d`，方法表 RVA `0x45a53e`。

| 方法 | 代码 RVA | 指令数 | 字符串引用 |
|---|---:|---:|---|
| `btnCaptionCloseClick` | `0x45a78c` | 8 | - |
| `FormCreate` | `0x45a7b0` | 29 | - |
| `FormDestroy` | `0x45b0d8` | 31 | - |
| `miClearClick` | `0x45adbc` | 1 | - |
| `TimerTimer` | `0x45b130` | 4 | `system.saveHistory(console.obj2Json(cmdHistory.slice(cmdHistory.length - 10, cmdHistory.length)));` |
| `WebBrowserDocumentReady` | `0x45b32c` | 134 | `财智8`；`8.50`；`%s [版本 %s.%s]%s(C) 版权所有 1999-%s 成都财智软件有限公司`；`cmdHistory`；`Moneyhome`；`console.setOptions({"readOnly": 0, "commandHistory": %s});` |
| `NetworkWebBrowserDocumentReady` | `0x45b5d4` | 4 | `console.setOptions({"readOnly": 1});` |
| `SQLWebBrowserDocumentReady` | `0x45b618` | 4 | `console.setOptions({"readOnly": 1});` |
| `WebBrowserConsoleMessage` | `0x45b65c` | 6 | - |
| `WebBrowserAlertBox` | `0x45b66c` | 103 | `id`；`命令错误` |
| `FormShow` | `0x45b7e0` | 60 | `Console.htm`；`Loaded` |

### `TShortcutManageDlgFm`：快捷键设置页

类元数据 RVA `0x43a9f3`，方法表 RVA `0x43a916`。

| 方法 | 代码 RVA | 指令数 | 字符串引用 |
|---|---:|---:|---|
| `FormCreate` | `0x43b168` | 109 | `97`；`<无>` |
| `FormDestroy` | `0x43b2ec` | 12 | - |
| `MenuButtonClick` | `0x43aad4` | 7 | - |
| `btnSaveExitClick` | `0x43aaec` | 143 | `ShortCut` |
| `cbBossKeyClick` | `0x43b528` | 14 | - |
| `tlMenuShortCutMouseUp` | `0x43b558` | 33 | - |
| `miDeleteClick` | `0x43b5c0` | 7 | - |
| `btnNewShortCutClick` | `0x43b7dc` | 178 | `请选择菜单项`；`请输入快捷键`；`Ctrl`；`Shift`；`Alt`；`快捷键需为组合键，请重新输入`；`,F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11,F12,Ctrl+F12,Shift+Ctrl+F12,Ctrl+C,Ctrl+V,Ctrl+M,`；`此快捷键不可用，请重新输入` |
| `tlMenuShortCutDblClick` | `0x43bb64` | 60 | - |
| `FormShow` | `0x43bcc0` | 16 | - |

## 已解析跳转桩

- `VclFormCloseThunk` -> `vcl70.bpl!@Forms@TCustomForm@Close$qqrv`：计算器结果、错误和键盘关闭共用的 VCL 窗体关闭入口
- `VclFormHideThunk` -> `vcl70.bpl!@Forms@TCustomForm@Hide$qqrv`：控制台标题栏关闭按钮使用的 VCL 窗体隐藏入口

## 控制台命令类

- `THelpCommand`：控制台页面就绪后注册；全局槽位 RVA `0x4433f0`
- `TSaveConsoleSettingsCommand`：控制台页面就绪后注册；全局槽位 RVA `0x443378`
- `TMoneyHomeIniCommand`：控制台页面就绪后注册；全局槽位 RVA `0x4434d4`
- `THashCommand`：控制台页面就绪后注册；全局槽位 RVA `0x4435bc`
- `TSystemInfoCommand`：控制台页面就绪后注册；全局槽位 RVA `0x443778`
- `TClearSyncAccountCommand`：控制台页面就绪后注册；全局槽位 RVA `0x4437e8`
- `TShowFormClassNameCommand`：仅特定运行模式注册；全局槽位 RVA `0x44345c`
- `TSystemEncryptCommand`：仅特定运行模式注册；全局槽位 RVA `0x443548`
- `TBase64Command`：仅特定运行模式注册；全局槽位 RVA `0x443628`
- `TExecuteSQLCommand`：仅特定运行模式注册；全局槽位 RVA `0x443694`
- `TGenDataScriptCommand`：仅特定运行模式注册；全局槽位 RVA `0x443d18`
- `TTestCommand`：仅特定运行模式注册；全局槽位 RVA `0x443860`
- `TNetworkDebugCommand`：非特定模式且网络调试未禁用时注册；全局槽位 RVA `0x443704`
- `TFixCurrencyCommand`：控制台页面就绪后注册；全局槽位 RVA `0x4438cc`
- `TFixCodeCommand`：控制台页面就绪后注册；全局槽位 RVA `0x44393c`
- `TFixPriceCommand`：控制台页面就绪后注册；全局槽位 RVA `0x4439a8`
- `TFixADOCommand`：控制台页面就绪后注册；全局槽位 RVA `0x443a18`
- `TSetVarCommand`：控制台页面就绪后注册；全局槽位 RVA `0x443a84`
- `TRemoteCommand`：控制台页面就绪后注册；全局槽位 RVA `0x443af0`
- `TSQLCommand`：控制台页面就绪后注册；全局槽位 RVA `0x443b5c`
- `TQuickIncExpCommand`：控制台页面就绪后注册；全局槽位 RVA `0x443bc4`
- `TServerCheckCommand`：控制台页面就绪后注册；全局槽位 RVA `0x443c34`
- `TReactivationCommand`：控制台页面就绪后注册；全局槽位 RVA `0x443ca4`
- `THttpServerLogCommand`：控制台页面就绪后注册；全局槽位 RVA `0x443d8c`
- `TRenameBookCommand`：控制台页面就绪后注册；全局槽位 RVA `0x443e00`

## 高价值常量

| 常量 | RVA | 代码引用 RVA |
|---|---:|---|
| `data/AIPanel.html` | `0x3dddf4` | 0x3ddddb |
| `Console.htm` | `0x45b8dc` | 0x45b80a |
| `http://ai.smallisfine.com/v1/consult?question=%s&key=%s&_=%s&sign=%s` | `0x3ddc80` | 0x3ddb3a |
| `http://ai.smallisfine.com/v1/consult?question=%s&key=%s&_=%s&sign=%s` | `0x3de174` | 0x3de0bc |
| `http://ai.smallisfine.com/v1/explanation?terminology=%s&key=%s&_=%s&sign=%s` | `0x3de1c4` | 0x3de0e0 |
| `http://ai.smallisfine.com/v1/faq?subject=%s&key=%s&_=%s&sign=%s` | `0x3de218` | 0x3de0fd |
| `o.%s(`%s`, `%s`);` | `0x3dd8c0` | 0x3dd865 |
| `prepare` | `0x3de080` | 0x3de046 |
| `init` | `0x3dde90` | 0x3dde35 |
| `showContent` | `0x3de014` | 0x3ddfd5 |
| `内容正在更新中，请稍后再试。` | `0x3de848` | 0x3de78d |
| `内容获取出错（%s: %s）` | `0x3de6a8` | 0x3de61f |
| `%s - %s, Line: %d` | `0x376810` | 0x3767c6 |
| `%s - %s, Line: %d` | `0x3dddbc` | 0x3ddd72 |
| `md5` | `0x3de340` | 0x3de2e1 |
| `3141592653589793` | `0x3dce44` | 0x60a054 |
| `1234567812345678` | `0x3dce60` | 0x60a058 |
| `200` | `0x3dce7c` | 0x60a05c |
| `204` | `0x3dce88` | 0x60a060 |

## 使用边界

- 方法名来自 Delphi published RTTI，地址来自同一运行副本，不依赖磁盘壳内占位代码。
- 反汇编仅用于证明控制流、常量引用和外部调用边界；业务语义仍需结合 DFM、动态操作和账本结果交叉验证。
- 旧 AI 接口使用明文 HTTP。Rust 重构不得照搬该传输方式，也不得在未明确配置和同意时上传财务数据。
