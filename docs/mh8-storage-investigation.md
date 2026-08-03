# mh8 存储与权限排查记录

本文档专门记录 `test.mh8` 的格式、权限与连接实验，避免这部分证据散落在总需求分析里。

## 1. 当前样本

- 文件：`C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8`
- 大小：约 `18.67 MB`
- 测试日期：`2026-07-28`

## 2. 已确认事实

### 2.1 文件与程序共现线索

- 程序目录存在 `mh.mdw`
- 程序目录曾出现 `mh.ldb`
- 程序清单声明 `requireAdministrator`
- 程序二进制中可检出 `Jet OLEDB`、`DBQ`、`PWD`、`User`、`Admin` 等连接相关痕迹
- `user.cfg` 与 `UseInformation.cfg` 中存在明显的 Base64 段，且解码后并非直接明文，说明本地还存在一层应用自定义加密配置
- `MoneyHome8.data` 在偏移 `125` 处可 `zlib` 解压出一份 `Standard Jet DB` 数据库

### 2.2 访问行为线索

- 当 `MoneyHome8.exe` 正在打开 `test.mh8` 时：
  - ODBC 报错为“文件已在使用中”
- 当关闭主程序后：
  - 直接 ODBC 打开 `test.mh8` 报错为“没有必要权限”
- 当在连接串中加入：
  - `SystemDB=C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\mh.mdw`
  - 错误进一步收敛为“不是有效的账户名称或密码”
- 对 `MoneyHome8.data` 解压得到的 `artifacts\MoneyHome8.data.decompressed.mdb`：
  - 不带 `SystemDB` 时返回“没有必要权限”
  - 带 `SystemDB` 后同样收敛为“不是有效的账户名称或密码”

这说明：

1. `mh8` 并非普通自由访问文件。
2. `mh.mdw` 不是无关文件，而是参与访问控制的工作组数据库。
3. `MoneyHome8.data` 内部也不是普通静态资源，而是受同类认证控制的 Jet 内置库。
4. 当前卡点已经进入“认证参数”层，而不是“文件格式是否可识别”层。

### 2.3 本地加密配置线索

- `user.cfg`
  - `content=` 后是长度约 `1784` 的 Base64 字符串
  - 解码后得到约 `1336` 字节的高熵二进制数据
  - 其中未直接出现可见账号、域名或数据库连接明文
- `UseInformation.cfg`
  - `key1`、`key2`、`key3`、`content` 均为 CDATA 包裹的 Base64 风格载荷
  - 其中 `content` 解码后约 `2064` 字节，也表现为高熵数据
- `user.cfg` 的 `key=` 值中，前段 `Pz8t` 可解码为 `??-`，后段仍不像可直接使用的明文口令

当前解释：

- 本地配置里很可能保存了应用自己的加密凭证、设备绑定信息、登录态或派生密钥材料
- 它们不是直接可读的 Access 账号口令文本

## 3. 已尝试连接路径

### 3.1 64 位 ODBC Access Driver

已验证本机存在：

- `Microsoft Access Driver (*.mdb, *.accdb)` 64-bit

实验结果：

- 不带 `SystemDB`：无权限
- 带 `SystemDB` 且使用 `Admin/admin/User/user` 空密码：账号或密码无效

### 3.2 64 位 OLEDB Jet Provider

实验结果：

- `Microsoft.Jet.OLEDB.4.0` 在当前 64 位宿主未注册

### 3.2A 64 位 ACE OLEDB Provider

实验结果：

- 对 `mhlink-copy.mdb`
  - `OPEN_OK`
  - 可枚举系统表与业务表
- 对原始 `mhlink.mdb`
  - 报 `不能锁定文件`
- 对 `test-copy.mh8`
  - 不带 `SystemDB`：无权限
  - 带 `SystemDB=mh.mdw`：账号或口令无效

当前解释：

- `ACE OLEDB 16.0` 在本机可用
- `mhlink.mdb` 的 ACE 失败更像文件锁问题
- `test.mh8` 的核心问题仍然是认证，而不是 Provider 可用性

### 3.3 32 位 PowerShell + ADO COM

实验结果：

- 可以创建 `ADODB.Connection` COM 对象
- 说明 32 位 Jet 通路在本机不是完全缺失
- 但对 `test.mh8` 调用 `Open(...)` 时尚未得到可公开使用的表结构结果

当前解释：

- 32 位 Provider 存在，但仍受工作组认证与权限约束

### 3.4 运行时自动化约束

实验线索：

- 主程序清单声明 `requireAdministrator`
- 后续从普通命令上下文重新拉起主程序时，未稳定拿到可继续自动化枚举的进程窗口

当前解释：

- 很可能存在 UAC 提权弹窗或提升桌面切换
- 这会影响：
  - 自动化启动原程序
  - 自动化点击顶部菜单
  - 后续批量截图与控件树抓取

### 3.5 Access COM 对象枚举行为

实验结果：

- `Access.Application.OpenCurrentDatabase(...)` 可成功打开 `test.mh8`
- 但打开后：
  - `CurrentProject.AllForms = 0`
  - `CurrentProject.AllReports = 0`
  - `CurrentProject.AllTables = 0`
  - `CurrentProject.AllQueries = 0`
  - `CurrentDb().Properties.Count = 0`

当前解释：

- 主账本在当前上下文下更像“空壳已打开，但对象全部不可见”
- 这进一步说明卡点不是文件路径，而是对象级访问权限

## 4. 当前最合理判断

截至目前，最合理的技术判断是：

- `test.mh8` 很可能建立在 Access/Jet 数据库体系之上
- 访问它需要：
  - 正确的数据源路径
  - 正确的 `SystemDB` 工作组文件
  - 正确的用户标识
  - 正确的口令或等价认证上下文

因此，“Rust 直接读取二进制结构”并不是当前唯一方向，甚至未必是最优先方向。更高优先级是：

1. 继续找到正确的工作组认证参数
2. 或从运行时进程/界面动作中旁路验证表结构
3. 或转向“通过原程序导出/中转”的迁移通道
4. 或在提升权限的受控环境中做一次性结构提取

## 5. 对重构方案的影响

### 5.1 短期

- 先以“只读导入旧账本”为目标
- 不承诺早期版本原位写回 `mh8`
- Rust 核心模型与旧格式访问层必须解耦
- 需要为“主账本 Jet 库”和“压缩封装的内置 Jet 库”预留独立读取器

### 5.2 中期

- 若拿到认证参数，可继续：
  - 枚举表结构
  - 提取真实字段
  - 建立表到领域模型映射
  - 分别厘清 `test.mh8`、解压后的 `MoneyHome8.data`、`mhlink.mdb` 三者边界

### 5.3 长期

若最终无法稳定复用旧账本认证体系，则建议方案改为：

- 原账本只读导入
- 新版使用自有存储格式
- 提供迁移器与导出器

## 6. 待验证问题

- 工作组默认用户到底是什么
- 口令是否来自：
  - 本地配置文件
  - 远程登录态
  - 程序内部加密配置
  - 首次建账时写入的库内权限
- `user.cfg` / `UseInformation.cfg` 中的密文与 `mh8` 工作组认证之间是否存在直接映射
- `mh8` 是否完全等价于 `.mdb`，还是在外层又包了一层自定义容器
- 原程序是否有“导出明细 / 导出账本 / 修复账本”这类可用于旁路取数的能力
