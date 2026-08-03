# Provider 行为对照

本文档记录当前对不同数据库访问路径的对照行为，重点区分：

- 文件锁问题
- Provider 可用性问题
- 主账本认证问题

## 1. 路径对照

### 1.1 ODBC + `mhlink.mdb`

结果：

- 可直接只读打开
- 可读表、字段、样例、行数

结论：

- ODBC 对共享参考库稳定可用

### 1.2 ODBC + `test.mh8`

结果：

- 不带 `SystemDB`：
  - 无权限
- 带 `SystemDB=mh.mdw`：
  - 账号或口令无效

结论：

- ODBC 路径已明确进入认证层

### 1.3 ACE OLEDB + 原始 `mhlink.mdb`

结果：

- 当前会话里会报：
  - `不能锁定文件`

结论：

- 这更像文件锁或文件占用问题
- 不足以说明 ACE Provider 本身不可用

### 1.4 ACE OLEDB + `mhlink-copy.mdb`

结果：

- `OPEN_OK`
- 能枚举：
  - `HBRate`
  - `MSysAccessObjects`
  - `MSysACEs`
  - `MSysObjects`
  - `MSysQueries`
  - `MSysRelationships`
  - `TBSecuPrice`
  - `TBTransFee`

结论：

- `ACE OLEDB 16.0` 在本机是可用的
- 原始 `mhlink.mdb` 的失败应归因为文件锁，而不是 Provider 缺失

### 1.5 ADOX + `mhlink-copy.mdb`

结果：

- `OPEN_OK`
- 能枚举与 ACE OLEDB 一致的表名

结论：

- ADOX 对可访问的 Access 库也可用

### 1.6 ACE OLEDB + `test-copy.mh8`

结果：

- 不带 `SystemDB`：
  - 无权限
- 带 `SystemDB=mh.mdw`：
  - 账号或口令无效

结论：

- 即使把主账本复制到 workspace，认证问题依旧存在
- 说明问题并非原路径文件锁，而是库本身权限/认证机制

### 1.7 DAO 16.0 + 原始 `test.mh8`

结果：

- `DAO.DBEngine.120`
  - `OPEN_OK` 不成立
  - 在原程序已打开账本的前提下，始终返回：
    - `文件已在使用中`
- `DAO.DBEngine.36`
  - 本机未注册
  - `80040154 没有注册类`

结论：

- 本机存在可用的 DAO 16.0 通路
- 但旧式 `DAO.DBEngine.36` 不可用
- 当原程序正在占用原始账本时，DAO 会首先卡在文件占用层

### 1.8 DAO 16.0 + `test-copy.mh8`

结果：

- 对 workspace 副本执行：
  - `SystemDB=mh.mdw`
  - 以及多组 `UID / PWD` 试探
- 不再报“文件已在使用中”
- 统一报：
  - `没有使用该对象的必要权限`

结论：

- 一旦文件锁影响移除，DAO 16.0 会稳定落到“权限不足”层
- 当前并没有通过简单的 `UID / PWD` 组合直接进入对象枚举层
- 这说明 DAO 路径与 ACE/ODBC 一样，也被主账本权限体系拦住

补充观察：

- `UID=Admin` / `UID=admin`
  - 当前并不会把错误从“权限不足”推进为“对象可见”
- 这说明：
  - 用户名候选虽然更像有效
  - 但距离可见对象层仍有明显鸿沟

### 1.9 ACE OLEDB + `test-copy.mh8` 本轮补充

结果：

- 本轮基于 `ADODB.Connection` 重新尝试 `test-copy.mh8`
- 返回为：
  - `不能使用 ''；文件已在使用中`

当前判断：

- 该错误表现与此前基于连接串的实验不完全一致
- 更像当前 `ADODB.Connection` 调用方式或 Provider 状态不稳定
- 现阶段不应把这一条新结果单独视为推翻之前“副本主要卡认证”的结论

## 2. 当前最稳的对照结论

1. `ACE OLEDB 16.0` 在本机可用。
2. `mhlink.mdb` 原始文件失败，更像文件锁问题。
3. `test.mh8` 无论原始文件还是副本，认证问题都保持不变。
4. 主账本问题的本质已收敛为：
   - 账号/口令
   - 工作组上下文
   - 对象可见性
5. `DAO.DBEngine.120` 也是可用入口，但它在：
   - 原始账本上先体现文件锁
   - 副本账本上先体现权限不足
   这进一步说明主问题层级并未偏离认证/权限体系
6. `admin / Admin` 当前是较强的用户名候选，但尚未形成可用认证组合

## 3. 对后续的直接意义

- 后续再研究 `test.mh8` 时，可以把：
  - “Provider 是否可用”
  - “文件锁是否导致失败”
  这两件事视为已基本排除。
- 主精力应继续集中在：
  - `mh.mdw`
  - `user.cfg` / `UseInformation.cfg`
  - Access/DAO/COM 对象可见性
