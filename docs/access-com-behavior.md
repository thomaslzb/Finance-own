# Access COM 行为对照

本文档记录在当前会话中，使用 `Access.Application` 打开不同数据库时表现出的差异。

## 1. 目标

通过同一套 `Access COM` 接口对比：

- `mhlink.mdb`
- `test.mh8`

看看问题究竟是：

1. COM 服务器本身不稳定
2. 某个数据库打不开
3. 数据库可打开但对象集合不可见

## 2. 当前观察结果

### 2.1 `mhlink.mdb`

当前会话表现：

- 在某些调用里 `Access.Application` 创建阶段直接失败：
  - `80080005 服务器运行失败`

当前解释：

- Access COM 服务器本身在当前环境里并不稳定。
- 因此不能简单把 `mhlink.mdb` 的 COM 失败解释成库本身有问题。

### 2.2 `test.mh8`

当前会话表现：

- `Access.Application` 可创建
- `OpenCurrentDatabase('test.mh8', ..., 'SystemDB=mh.mdw;...')` 返回：
  - `OPEN_OK`
- 但紧接着：
  - `CURRPROJECT_NAME = ""`
  - `CURRPROJECT_PATH = ""`
  - `CURRDB_NAME = ""`
  - `ALLTABLES = 0`
  - `ALLQUERIES = 0`
  - `TABLEDEFS = 0`
  - `QUERYDEFS = 0`

当前解释：

- 主账本在 Access COM 里至少已经通过了“打开文件”阶段。
- 但对象集合完全不可见。
- 这更像：
  - 打开了一个受限壳层
  - 或打开成功但当前上下文无对象访问权

## 3. 当前最重要的技术结论

### 结论 A：`test.mh8` 不再只是“打不开”

这是比 ODBC/ADO 更进一步的结论：

- 它在 Access COM 中已经能 `OPEN_OK`
- 所以问题已从“连接失败”推进为“对象不可见”

### 结论 B：`mhlink.mdb` 与 `test.mh8` 的问题层级不同

- `mhlink.mdb`
  - 在 ODBC 层可稳定读取
  - Access COM 层当前受服务器不稳定影响
- `test.mh8`
  - 在 ODBC 层卡认证
  - 在 Access COM 层可打开但对象不可见

### 结论 C：后续不要再把“文件可打开”和“对象可见”混为一谈

后续排查应区分三层：

1. 文件能否打开
2. 库是否被接受为当前数据库
3. 对象集合是否可见

## 4. 与 DAO 16.0 的互补关系

2026-07-28 补充实验后，可以把 Access COM 与 DAO 16.0 的角色区分得更清楚：

- `Access COM`
  - 已能达到：
    - `OPEN_OK`
  - 但对象集合：
    - 不可见
- `DAO.DBEngine.120`
  - 已确认可用
  - 但在：
    - 原始账本上先命中文件锁
    - 副本账本上先命中权限不足

这说明：

- Access COM 更像已经“跨过文件打开阶段”
- DAO 16.0 更像在更早层就被权限体系拦下
- DAO 默认工作区当前还直接暴露了：
  - `Workspace.UserName = admin`
- 两条路径互补后，当前问题已进一步收敛为：
  - 文件锁
  - 工作组/权限
  - 对象可见性

## 5. 对后续的直接建议

### 若继续打认证链

优先验证：

- 对象集合为何为 `0`
- 是否存在隐藏工作区或对象容器
- 是否存在“打开后需进一步登录”的状态

### 若继续做实现

当前可以安全采用的结论是：

- 不依赖主账本正式表结构，也可以先做 Phase 1/2 的 Rust 骨架
- 但不能宣称主账本读取器已经完成
