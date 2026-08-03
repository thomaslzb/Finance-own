# 资源二进制特征证据

本文档记录对若干关键 Delphi 资源二进制块的格式特征观察，目的是判断：

- 它们是否是标准明文 DFM
- 是否存在二次封装、压缩或高熵存储

## 0. 结论修正

本文件第 1 至第 3 节保留的是早期“直接从磁盘映像导出资源”的历史观察。2026-07-28 的运行时内存取证已经证明：

- PE 资源目录中的大量 DFM RVA 指向磁盘没有原始数据的虚拟区段
- 早期高熵/全零 `.bin` 是错误读取磁盘占位区或无关原始偏移的结果
- 普通权限副本完成解包后，这些 RVA 上的真实载荷以标准 `TPF0` 开头
- `460` 个真实 DFM 已全部解析成功，另 `5` 个 `T...` 资源为 PNG

因此“关键资源不是标准 DFM”“`TACCOUNTMANAGERFM` 是空占位资源”等旧推断均已失效。当前权威结论见：

- [runtime-dfm-functional-evidence.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-dfm-functional-evidence.md)
- [runtime-dfm-control-catalog.md](C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own\docs\runtime-dfm-control-catalog.md)

## 1. 已取样资源

当前已单独导出的资源二进制：

- `TMAINFORM.bin`
- `TTRANSDLGFM.bin`
- `TACCOUNTMANAGERFM.bin`
- `TREPORTFM.bin`
- `TFINANCIALPLANNINGCENTERFM.bin`

## 2. 关键观察

### 2.1 不是标准明文 DFM 头

标准 Delphi 二进制 DFM 通常会出现可识别的签名或较明显的属性头部。

当前取样中：

- `TMAINFORM.bin`
- `TTRANSDLGFM.bin`
- `TREPORTFM.bin`
- `TFINANCIALPLANNINGCENTERFM.bin`

头部都呈现高熵二进制，而不是可直接识别的明文结构。

当前结论：

- 主窗体与关键业务窗体资源很可能经过二次封装、压缩或自定义序列化。

### 2.2 `TACCOUNTMANAGERFM.bin` 异常全零

当前观察：

- 文件长度：`6919`
- 前缀零字节长度：`6919`
- 熵：接近 `0`

当前结论：

- 该资源不是普通有效窗体载荷。
- 可能是：
  - 空占位资源
  - 运行时动态加载占位符
  - 外部载荷索引

### 2.3 关键资源高熵明显

当前观察：

- `TFINANCIALPLANNINGCENTERFM.bin`
  - 熵约 `7.806`
- `TMAINFORM.bin`
  - 熵约 `7.828`
- `TREPORTFM.bin`
  - 熵约 `7.753`
- `TTRANSDLGFM.bin`
  - 熵约 `7.487`

当前结论：

- 这些资源明显不像未经处理的普通文本/表单流。
- 更像：
  - 压缩块
  - 加密/混淆块
  - 运行时解包资源

### 2.4 当前未发现直接 zlib 解压成功

对取样资源在前 `512` 字节范围内尝试以 `0x78` 为起点做 `zlib` 解压：

- 当前均未直接成功

当前结论：

- 资源块如果被压缩，也不是和 `MoneyHome8.data` 一样的“简单偏移 + zlib”模式。

## 3. 对后续逆向的意义

### 3.1 不要优先假设“资源 = 直接可解析 DFM”

当前更稳妥的判断是：

- 页面和窗体能力的确认，短期仍应以：
  - 资源窗体名
  - 运行时页面截图
  - 数据表/字段
  为主

### 3.2 资源二进制更适合做“辅助证据”

在当前阶段，资源二进制更适合用于：

- 判断是否存在二次封装
- 判断资源是否可能运行时加载
- 为未来深逆向保留样本

而不适合当前就作为主要页面语义来源。

## 4. 当前最稳的结论（已更新）

1. 磁盘原始映像不能直接代表运行时窗体载荷。
2. 运行时资源是可解析的标准 Delphi `TPF0` 对象流。
3. 资源层的功能、控件、字段和事件已经完成全量结构化提取。
4. 后续重点应转向真实数据、计算公式、动态菜单与页面跳转验证。
