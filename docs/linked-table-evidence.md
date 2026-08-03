# 主账本外部链接表证据

本文档记录 `test.mh8` 中与外部参考库 `mhlink.mdb` 相关的字节流证据，用于支撑“主账本可能通过链接表或等价机制引用共享参考数据”的判断。

## 1. `mhlink.mdb` 路径痕迹

在 `test.mh8` 的 UTF-16 字节流中，已多次发现以下完整路径：

`C:\Program Files (x86)\MoneyWise\MoneyHome8\Data\mhlink.mdb`

当前已见：

- 至少 `6` 次出现

这说明：

- 主账本内部不只是“知道有这个文件”，而是确实保存了与 `mhlink.mdb` 的明确路径关系。

## 2. 与系统表/连接字段同现的证据

在 `test.mh8` 和解压后的内置库中，`mhlink.mdb` 路径附近还出现了以下明显结构词：

- `Connect`
- `Database`
- `Tables`
- `MSysRelationships`
- `MSysQueries`
- `MSysACEs`
- `MSysObjects`

这类词在 Access/Jet 体系里通常与：

- 链接表
- 系统关系
- 查询定义
- 连接元数据

有强关联。

## 3. 与参考表名同现的证据

在 `test.mh8` 的 UTF-16 字节流中，以下共享参考表名都能被直接检出：

- `HBRate`
- `TBSecuPrice`
- `TBTransFee`
- `TBSecuType`
- `TBSecurityAcct`
- `TBSecurities`
- `TBReportSettings`
- `TBRemindTypeSet`

其中，在部分片段中可以看到如下连续表目录式序列：

- `HBRate`
- `TBSecuPrice`
- `TBSecuType`
- `TBSecurityAcct`
- `TBSecurities`
- `TBReportSettings`
- `TBRemindTypeSet`

这说明：

- `test.mh8` 并非只在孤立位置保留了这些名字
- 它更像持有一段完整的对象目录或对象描述结构

## 4. 当前最合理判断

截至 2026-07-28，当前最合理的技术判断是：

1. `test.mh8` 主账本内部显式保存了到 `mhlink.mdb` 的路径。
2. 主账本内部同时保存了与外部表/系统连接相关的元数据词汇。
3. 主账本中还直接出现了一批与 `mhlink.mdb` 一致的共享参考表名。

因此，以下结论具有较高可信度：

- `test.mh8` 很可能通过 Access 链接表、系统关系定义或等价外部连接机制使用 `mhlink.mdb` 中的共享数据。

## 5. 对重构的意义

### 5.1 参考库不应被视作孤立附件

在 Rust 重构中，`mhlink.mdb` 应被视为主账本生态的一部分，而不是一个无关辅助库。

### 5.2 主账本读取器需要考虑外部依赖

当未来正式读取 `test.mh8` 时，需要准备处理：

- 链接表
- 外部引用
- 连接失效时的降级逻辑

### 5.3 迁移器需要同时处理主账本与参考库

若后续做旧账本导入，不应只导入 `mh8` 单文件，还要考虑：

- 行情
- 费率
- 利率规则
- 对象分类

## 6. 后续优先验证点

1. `test.mh8` 正式认证打通后，优先验证是否存在链接表或外部表属性
2. 验证 `HBRate`、`TBSecuPrice`、`TBTransFee` 在主账本中的访问方式是：
   - 真正的链接表
   - 本地缓存镜像
   - 查询中引用
   - 其它访问层封装
3. 验证 `TBObjectType` / `TBSecuType` 等对象是否也依赖共享参考库
