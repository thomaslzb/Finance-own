# 认证机制证据

本文档记录当前从可执行文件、依赖 DLL、配置文件和运行时现象中获得的“认证机制”相关证据，目的是缩小后续排查范围。

## 1. 来自主程序与 DLL 的直接证据

### 1.1 `MoneyHome8.exe`

当前能确认的导入/字符串线索：

- 导入 DLL：
  - `advapi32.dll`
  - `ole32.dll`
  - `oleaut32.dll`
  - `shell32.dll`
  - `wininet.dll`
  - `wsock32.dll`
- 可见字符串：
  - `Jet OLEDB`

当前判断：

- 主程序确实涉及：
  - 注册表访问
  - OLE / COM
  - 网络访问
- 但当前没有直接看到大量显式 `Crypt*` API 调用字符串

### 1.2 `mwSync.dll`

当前导入线索：

- `advapi32.dll`
- `oleaut32.dll`

当前判断：

- 同步模块至少涉及注册表与 OLE 自动化
- 当前未看到显式数据库认证字符串

### 1.3 `mwWebService.dll`

当前导入线索：

- `advapi32.dll`
- `oleaut32.dll`
- `wsock32.dll`

当前判断：

- Web 服务模块至少涉及注册表与网络发送
- 说明远程同步/通知逻辑并非完全在主程序里硬编码

## 2. 来自主账本与工作组的直接证据

### 2.1 主账本行为

- `test.mh8` 文件头：
  - `Standard Jet DB`
- `test.mh8` 不带 `SystemDB`：
  - 权限不足
- `test.mh8` 带 `SystemDB=mh.mdw`：
  - 用户名或密码无效

当前判断：

- 这是典型的“工作组数据库 + 用户认证”问题，而不是普通损坏文件或单纯锁文件问题。

### 2.2 内置库行为

- `MoneyHome8.data` 解压后同样是 Jet 数据库
- 解压库也受 `SystemDB=mh.mdw` 影响

当前判断：

- 主账本与内置库很可能共用一套认证/权限体系。

### 2.3 Access COM 行为

已确认：

- `Access.Application` COM 对象可创建
- `OpenCurrentDatabase('test.mh8', ..., 'SystemDB=mh.mdw;...')` 可返回成功
- 但随后：
  - `AllTables = 0`
  - `AllQueries = 0`
  - `TableDefs = 0`
  - `QueryDefs = 0`
  - `CurrentProject.AllForms = 0`
  - `CurrentProject.AllReports = 0`
  - `CurrentDb().Properties.Count = 0`

当前判断：

- Access 至少接受了该库并进入“已打开”状态
- 但当前上下文仍看不到任何业务对象集合
- 认证问题已经从“能否打开库”进一步收敛到“对象可见性/对象访问权限”

### 2.4 DAO 16.0 行为

已确认：

- `DAO.DBEngine.120`
  - 本机可创建
  - 版本：`16.0`
- `DAO.DBEngine.36`
  - 本机未注册

对默认工作区：

- `DBEngine.Workspaces.Count = 1`
- 默认工作区名：
  - `#Default Workspace#`
- `Workspace.UserName`：
  - `admin`
- `Workspace.Users.Count = 0`
- `Workspace.Groups.Count = 0`

当前判断：

- 本机 DAO 默认工作区当前用户名并非空，而是 `admin`
- 但默认工作区并没有直接暴露可枚举的 `Users / Groups` 集合内容

对原始账本：

- 当原程序正在打开 `test.mh8` 时：
  - DAO 16.0 稳定返回：
    - `文件已在使用中`

对 workspace 副本：

- 使用：
  - `SystemDB=mh.mdw`
  - 多组 `UID / PWD`
- 当前稳定返回：
  - `没有使用该对象的必要权限`

对 `CreateWorkspace(...)` 试探：

- `User=""`
  - 稳定返回：
    - `不是有效的账户名称或密码`
- `User=Admin, PWD=""`
  - 可创建工作区
  - `Workspace.UserName = Admin`
  - `Users.Count = 0`
  - `Groups.Count = 0`
- `User=admin, PWD=""`
  - 可创建工作区
  - `Workspace.UserName = admin`
  - `Users.Count = 0`
  - `Groups.Count = 0`
- `User=Admin/admin` 配合非空密码
  - 转而返回：
    - `无法启动应用程序。工作组信息文件丢失，或是已被其它用户以独占方式打开`

当前判断：

- DAO 16.0 是一个真实可用的补充入口
- 但它并没有绕过主账本权限体系
- 在“去掉文件锁”之后，它也没有进入可见对象层，而是落在“权限不足”层
- `Admin / admin` 作为账号名比空用户名更像有效候选
- 但目前仍没有得到可用的口令或用户/组枚举结果

## 3. 来自配置文件的直接证据

### 3.1 `mh.mdw`

- 当前直接可见字符串极少
- 但它能改变 `test.mh8` 的连接错误类型

当前判断：

- `mh.mdw` 不是可忽略的附属文件
- 它是 Access/Jet 工作组认证链的一部分

### 3.2 `user.cfg`

- 存在 Base64 风格载荷
- 其中一段 `Pz8t` 可解码为 `??-`
- 主要 `content=` 段解码后为高熵二进制

本轮补充结构分析：

- 文件大小：
  - `1834` 字节
- 最后修改时间：
  - `2025-12-01 23:07:16`
- 结构仅包含两段：
  - `key=...`
  - `content=...`
- `key=` 行当前表现为：
  - `Pz8t=Wswhdv6iv8A1ibGyLUhT2e78wK0fa`
- 其中：
  - `Pz8t`
    - 单独可解码为 `??-`
  - 其后拼接段当前不能按标准 Base64 直接整体解码
- `content`：
  - Base64 长度约 `1784`
  - 解码后长度约 `1336` 字节
  - 熵约 `7.7875`
  - 未发现 `admin / test / mh8 / MoneyWise / sync` 等直接明文命中
  - `16` 字节块无重复

当前判断：

- `user.cfg` 更像“较老的静态密文容器”
- `key=` 字段不像普通单段 Base64，更像：
  - 前缀标记
  - 加盐片段
  - 或应用自定义分隔格式
- 从当前结构看，它不像直接保存一个可抄出的明文口令
- 在 2026-07-28 本轮“关闭程序 -> 离线采样 -> 重新打开程序”对比中：
  - `user.cfg` 的：
    - 文件大小
    - 修改时间
    - SHA256
  都未发生变化

这进一步说明：

- 单纯打开 `MoneyHome8` 或打开 `test.mh8`
  - 当前不会刷新 `user.cfg`
- 它更像长期静态材料，而不是每次会话都会改写的运行态文件

### 3.3 `UseInformation.cfg`

- 存在 `key1` / `key2` / `key3` / `content` 四段 Base64 风格载荷
- `content` 解码后也是高熵二进制

本轮补充结构分析：

- 文件大小：
  - `3009` 字节
- 最后修改时间：
  - `2026-07-28 16:01:22`
- 说明它在今天当前会话中发生过更新
- `key1 / key2 / key3`
  - Base64 解码后长度分别约：
    - `25`
    - `13`
    - `12`
  - 熵约在：
    - `3.5 ~ 4.6`
- `content`
  - Base64 长度约 `2752`
  - 解码后长度约 `2064` 字节
  - 熵约 `7.8804`
  - `16` 字节块无重复
  - 未发现 `admin / test / mh8 / MoneyWise / sync` 等直接明文命中

当前判断：

- `UseInformation.cfg` 比 `user.cfg` 更像“运行时活跃材料”
- 它今天被更新过，这一点非常重要
- 从长度和高熵表现看，更像：
  - 会话态
  - 设备/授权信息
  - 认证上下文封装
  而不是简单配置项
- 但当前仍不能证明它直接等于数据库口令

本轮补充差分：

- 在 2026-07-28 本轮“关闭程序 -> 离线采样 -> 重新打开程序”对比中，必须区分两个采样时点：
  - 程序刚启动、尚未完全进入稳定响应前
    - `UseInformation.cfg` 暂未变化
  - 程序完成打开并进入 `test - 财智8` 稳定状态后
    - `UseInformation.cfg`
      - 文件大小：
        - `3009 -> 3011`
      - 修改时间：
        - `2026-07-28 16:01:22 -> 2026-07-28 16:44:48`
      - SHA256：
        - 由 `96698A...` 变为 `DF9AA5...`

这说明：

- `UseInformation.cfg` 确实会被“完成一次正常打开流程”触发改写
- 只是变化时机不是进程刚启动瞬间，而是更靠后
- 它因此更像：
  - 打开流程中的运行态材料
  - 会话/授权状态封装
  - 或与账本进入稳定状态相关的上下文文件

本轮补充时间序列：

- 启动监测基线时间：
  - `2026-07-28 16:49:05`
- 约 `+5s`
  - `Moneyhome.ini`
    - SHA256 发生变化
    - 修改时间变为：
      - 启动时对应新一轮写入
    - `UsedTimes`
      - `143 -> 144`
  - 同时 `UseInformation.cfg`
    - 仍保持上一轮稳定值
    - 文件长度：
      - `3011`
- 约 `+10s`
  - 进程主窗口标题开始出现：
    - `财智8`
  - 同时 `UseInformation.cfg`
    - SHA256 发生变化
    - 且当前已确认不是单一 `content` 变化，而是：
      - `key1`
      - `key2`
      - `key3`
      - `content`
      四段哈希同时变化
  - 启动 `+5s` 时的分段哈希仍为上一轮稳定值：
    - `key1 = DA955D...`
    - `key2 = F6DD4B...`
    - `key3 = 99BF16...`
    - `content = 3C3503...`
  - 启动 `+10s` 时的新分段哈希切换为：
    - `key1 = 4C1F2D...`
    - `key2 = 50CB2D...`
    - `key3 = 933BA4...`
    - `content = A55E36...`
- 约 `+37s`
  - 主窗口标题进一步稳定为：
    - `test - 财智8`
- 约 `+22s ~ +23s` 之后到账本稳定阶段
  - `mh.ldb`
    - 开始重新出现
  - `test.mh8`
    - 重新进入被锁定状态

这条时间线说明：

- `Moneyhome.ini`
  - 比 `UseInformation.cfg` 更早变化
- `UseInformation.cfg`
  - 变化时机位于：
    - `Moneyhome.ini` 之后
    - `test - 财智8` 稳定标题之前
  - 并且是整组分段一起翻新，而不是只替换 `content`
- `test.mh8` / `mh.ldb`
  - 更靠后才进入稳定占用状态

因此它们更可能对应不同层级：

- `Moneyhome.ini`
  - 本地使用态/程序状态
- `UseInformation.cfg`
  - 打开流程中的运行态上下文
- `test.mh8` / `mh.ldb`
  - 账本正式进入占用阶段

## 4. 当前没有看到的证据

截至目前，没有直接看到足够强的证据证明：

- 主程序显式调用 Windows DPAPI
- 主程序在字符串层直接保存明文数据库用户名/密码
- `mh.mdw` 可以被公开直接读取用户/组信息

这意味着：

- 认证可能通过：
  - 旧式 DAO/Jet 工作组机制
  - 本地自定义密文配置
  - 运行时派生上下文
  共同完成

同时也意味着：

- `UseInformation.cfg`
  - 当前比 `user.cfg` 更值得优先跟踪前后变化
- `user.cfg`
  - 更像长期持久化材料
- 而且“完成一次正常打开流程”本身已经足以触发 `UseInformation.cfg` 变化
- 并且最终稳定落盘后的 `UseInformation.cfg`
  - 不一定等于启动中途的瞬时内容
- 当前更强的判断是：
  - `UseInformation.cfg` 像一整组会话材料被重新生成
  - 而不是只更新单个数据载荷块

本轮补充跨启动稳定性：

- 在一次新的受控重启中，`UseInformation.cfg` 的分段变化呈现出更明确的两阶段特征：
  - 启动约 `+7s`
    - `key1 / key2 / key3 / content`
      仍保持上一轮稳定值：
      - `key1 = 4C1F2D...`
      - `key2 = 50CB2D...`
      - `key3 = 933BA4...`
      - `content = A55E36...`
  - 启动约 `+15s`
    - 主窗口标题出现：
      - `财智8`
    - `UseInformation.cfg` 四段同时切换为新值：
      - `key1 = 6BD5DB...`
      - `key2 = EEC2DD...`
      - `key3 = 7E1BAC...`
      - `content = E49FD6...`

随后又做了一轮受控重启，出现了更强的时序证据：

- 启动约 `+6s`
  - `Moneyhome.ini`
    - `UsedTimes = 146`
  - `UseInformation.cfg`
    - 仍保持上一轮稳定值：
      - `key1 = 6BD5DB...`
      - `key2 = EEC2DD...`
      - `key3 = 7E1BAC...`
      - `content = E49FD6...`
- 启动约 `+13s`
  - 主窗口标题出现：
    - `财智8`
  - `UseInformation.cfg` 四段再次整组切换为新的中间态：
    - `key1 = F10A23...`
    - `key2 = 7FED0E...`
    - `key3 = 7A5CB6...`
    - `content = 0B75E6...`
- 启动约 `+46s`
  - 主窗口标题稳定为：
    - `test - 财智8`
- 程序进入稳定态后再次采样：
  - `UseInformation.cfg` 最终文件 SHA256 回到：
    - `6A4734...`
  - 四段哈希也回到稳定值：
    - `key1 = 6BD5DB...`
    - `key2 = EEC2DD...`
    - `key3 = 7E1BAC...`
    - `content = E49FD6...`

这说明：

- `UseInformation.cfg` 的四段在跨启动时并不是固定不变
- 它们会在打开流程中段整组刷新
- 刷新之前会短暂保留上一轮的稳定值
- 并且在至少这一次样本里：
  - 启动中途出现的“新值”并不一定会成为最终稳定落盘值
  - 稳定态可能重新回落到上一轮的持久值

这比“只有 `content` 在变”更强，也比“只是某个时间戳更新了”更强。
- 因此后续更应做：
  - 启动早期 vs 稳定打开后的分阶段对比
  - 登录/同步前后对比
  - 设置变更前后对比

## 5. 对后续排查的直接约束

### 不要优先假设的路线

- 不要假设口令明文写在 `ini/cfg` 里
- 不要假设只要知道 `mh.mdw` 路径就能直接开库
- 不要假设认证只发生在主账本，内置库也受同类控制

### 应优先尝试的路线

- 32 位 DAO / ADO / ODBC 只读实验
- 配置密文相关性分析
- 运行时前后配置文件对比
- 主程序和同步模块的 COM/数据库调用链进一步定位

## 6. 当前最稳的结论

截至当前证据，最稳的认证机制结论是：

1. `test.mh8` 与内置库都属于受控 Jet 数据库。
2. `mh.mdw` 明确参与认证。
3. `user.cfg` / `UseInformation.cfg` 很可能参与认证上下文，但暂不能当作明文口令来源。
4. `Access COM` 已经能开主账本，但对象不可见，说明还存在对象层权限问题。
5. `DAO 16.0` 去掉文件锁后仍然只能走到“权限不足”，说明当前问题并不只是 Access 外壳行为异常。
6. `Admin / admin` 当前比空用户名更像有效账号候选，但尚未得到可用口令。
7. 真正的数据库认证很可能不是单一文件即可解决的问题，而是“工作组文件 + 本地密文配置 + 运行时上下文”的组合。
