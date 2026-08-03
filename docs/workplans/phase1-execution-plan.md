# 第一期执行计划

本文档承接 `phase1-requirements-analysis.md`，把第一期需求拆成可执行、可验证的工作队列。当前计划优先保证 PC 本地 SQLite、Rust 本地核心和只读数据源边界稳定，再进入 Flutter PC 本地 API、.NET 云端同步和三端业务闭环。

## 1. 当前基线

截至 `2026-08-03`，第一期可用基线如下：

- SQLite 迁移文件共 `13` 个，范围为 `0001_core.sql` 到 `0013_plan_and_reminder_occurrences.sql`。
- `tools/validate_sqlite_schema.py` 已覆盖表、视图、索引、触发器、应用文件标识、`user_version=13` 和代表性投影。
- `tools/run-rust-checks.ps1` 使用项目内 Rust 工具链、`rust-lld` 和 SQLite 运行库，不依赖系统 `PATH`。
- 当前 Rust 测试覆盖账簿创建/重开、外来 SQLite 标识拒绝、账户树、基础资料、交易写入、余额与标签查询、预算/计划/提醒/财务目标 CRUD、计划提醒实例、财务目标基线、待摊费用、存款利率、保险现金价值、参考库 JSON 映射、缓存候选读取、旧数据源静态识别、工作区壳层状态和原子回滚等基础能力。

本轮已执行验证：

```powershell
python .\tools\validate_sqlite_schema.py
& .\tools\run-rust-checks.ps1 -Action all
```

验证结果：

- `SQLite schema validation: PASS`
- Rust：`67 passed, 0 failed`

## 2. 第一期开工顺序

### P1-01 账簿与 SQLite 基线

状态：`已验证，可进入细化实现`

目标：

- 固化 SQLite 新账簿作为第一期真相源。
- 明确账簿创建、打开、迁移、完整性检查和错误状态。
- 把当前脚本验证结果纳入后续交付检查。

已满足：

- 13 版迁移可在内存 SQLite 中完整执行。
- `PRAGMA application_id` 和 `PRAGMA user_version` 已验证。
- Rust 全量检查通过。

后续任务：

1. 检查 `src/infrastructure/sqlite.rs` 中公开接口是否完整表达 `create/open/integrity_check/foreign_identity_reject` 需求。
2. 梳理账簿状态 DTO：无账簿、打开中、已打开、关闭中、失败恢复。
3. 若已有接口满足需求，在文档中标记为第一期基线完成；若缺接口，补最小应用层契约。

验收：

- 保持 `tools/validate_sqlite_schema.py` 通过。
- 保持 `tools/run-rust-checks.ps1 -Action all` 通过。
- 新增或确认的账簿状态接口有单元测试或等价验证。

### P1-02 共享参考库读取

状态：`契约、文件级探测、ACE 只读表行探测、受控 JSON 样本和 JSON Repository 已完成`

目标：

- 接入 `mhlink.mdb` 的只读读取能力。
- 将 `HBRate`、`TBSecuPrice`、`TBTransFee` 映射到 `RateRule`、`Quote`、`FeeRule`。

已完成：

1. 新增 `src/domain/reference_store.rs`，定义 `RateRule`、`Quote`、`FeeRule`、`ReferenceStoreError` 和 `ReferenceStoreRepository`。
2. 新增 `src/infrastructure/reference_mdb.rs`，对 `artifacts/mhlink-copy.mdb` 做只读文件级探测。
3. 已验证 `mhlink-copy.mdb` 能识别为 Jet/Access 数据库，并明确当前尚未具备表行读取适配器。
4. 缺失文件会返回结构化 `FileNotFound`，不会崩溃。
5. 新增 `tools/probe_mhlink_reference.ps1`，使用 `Microsoft.ACE.OLEDB.16.0` 以 `Mode=Read` 读取三张参考表的行数、字段和首行样例。
6. 已确认 `HBRate` 为 `113` 行，`TBSecuPrice` 为 `12207` 行，`TBTransFee` 为 `11` 行。
7. `tools/probe_mhlink_reference.ps1 -IncludeRows` 可输出三张表的全量行 JSON，行数与表计数一致。
8. 新增 `src/infrastructure/reference_json.rs`，通过受控 JSON 中间层实现 `ReferenceStoreRepository`，完成 `HBRate -> RateRule`、`TBSecuPrice -> Quote`、`TBTransFee -> FeeRule` 的基础映射。
9. `HBRate.ARate` 在 `RateRule` 中保存为 `legacy_rate_value` 原始定点值，比例单位校准前不直接转成账簿内年利率百分数。
10. 新增 `tools/export_mhlink_reference_json.ps1`，把只读探测结果导出到 `artifacts/reference/mhlink-reference.json`，使用 UTF-8 无 BOM。
11. 新增 `tools/validate_mhlink_reference_json.ps1`，校验受控 JSON 样本的三表字段、行数和全量 `rows`。
12. `ReferenceJsonRepository::from_path` 已能读取受控全量 JSON 样本，并通过行数与代表性代码查询测试。

任务：

1. 生成项目内受控 JSON 样本时，必须确认其来自 `artifacts/mhlink-copy.mdb` 或明确指定的只读参考库副本，避免把程序目录原始文件作为默认写入目标。
2. 进一步校准 `HBRate.ARate` 的真实比例单位、`TBSecuPrice.ObjectQuant` 的业务用途，以及 `TBTransFee.YHSL/YHSL_SELL`、`YJFL/YJFL_SELL` 的买卖方向优先级。
3. 根据 UI 或计算场景决定是否需要 Rust 直接 COM/ODBC 适配；在此之前，核心 Rust 代码通过 JSON 中间层读取。
4. 为真实全量 JSON 样本增加校验脚本或测试夹具，覆盖三表行数、关键字段和代表性映射。

验收：

- 能读取或明确报告 `mhlink.mdb` 不可访问原因。
- 三类表都有结构化结果类型。
- 读取过程不修改 `mhlink.mdb`。
- `tools/run-rust-checks.ps1 -Action all` 保持通过。

本轮验证：

- `python .\tools\validate_sqlite_schema.py`：`SQLite schema validation: PASS`
- `& .\tools\run-rust-checks.ps1 -Action all`：`47 passed, 0 failed`
- `& .\tools\probe_mhlink_reference.ps1`：三张参考表只读探测成功，行数为 `113 / 12207 / 11`
- `& .\tools\probe_mhlink_reference.ps1 -IncludeRows`：三张参考表全量 JSON 行数为 `113 / 12207 / 11`
- `& .\tools\export_mhlink_reference_json.ps1`：生成 `artifacts/reference/mhlink-reference.json`
- `& .\tools\validate_mhlink_reference_json.ps1`：`PASS`

### P1-03 缓存读取

状态：`领域契约、文件头探测、ASCII 标记统计和候选读取已完成；中文字段协议待继续逆向`

目标：

- 接入 `MoneyHome8.cache` 和 `Investment.cache`。
- 固化 `_PY`、`_LIST`、`_3`、`_4`、`_9` 的已确认语义。

已完成：

1. 已阅读现有缓存语义文档和调查记录，确认 `MoneyHome8.cache`、`Investment.cache` 是第一期只读候选数据源。
2. 新增 `src/domain/cache_store.rs`，定义 `LookupIndexEntry`、`LookupIndexSuffix`、`InvestmentCatalogEntry`、`InvestmentCatalogTypeCode`、`CacheStoreError` 和 `CacheStoreRepository`。
3. 新增 `src/infrastructure/cache_file.rs`，提供只读 `CacheFile`，能识别 `MoneyHomeCache` 文件头、统计 `_PY/_LIST/_3/_4/_9` 标记，并按 ASCII 可见 token 抽取候选。
4. `CacheFile` 已实现 `CacheStoreRepository`，领域层可通过仓储端口调用 `search_lookup`、`search_lookup_by_code`、`search_lookup_by_abbr` 和 `list_investment_catalog_by_type`。
5. 新增 `tools/probe_moneyhome_cache.ps1`，用字节级方式探测两个缓存样本，避免把二进制缓存误判成 UTF-16 文本。
6. 已确认 `MoneyHome8.cache` 文件头有效，`_PY` 标记 `154034` 次，`_LIST` 标记 `84265` 次。
7. 已确认 `Investment.cache` 文件头有效，候选 `_3` 标记 `83832` 次、`_4` 标记 `24314` 次、`_9` 标记 `286` 次。
8. 缓存中的中文名称更像 GBK/ANSI 长度前缀片段，目前不把未确认字段写成业务含义；`InvestmentCatalogEntry.name` 在协议未确认前保持为空。

任务：

1. 继续逆向 GBK/ANSI 长度前缀字符串记录，确认代码、名称、拼音、类别和原始值之间的分隔规则。
2. 区分真实 `_3/_4/_9` 类别记录和字节级偶发匹配，形成比“标记计数”更稳定的目录行数。
3. 将可靠中文名称映射到 `InvestmentCatalogEntry.name`，并保留无法识别片段的诊断信息。
4. 为按代码、名称或缩写查询补充更贴近真实缓存样本的断言。

验收：

- 能按代码、名称或缩写返回候选。
- 能按 `_3/_4/_9` 区分投资品目录候选。
- 未识别记录不导致解析中断。

本轮验证：

- `& .\tools\probe_moneyhome_cache.ps1`：`PASS`
- `python .\tools\validate_sqlite_schema.py`：`SQLite schema validation: PASS`
- `& .\tools\validate_mhlink_reference_json.ps1`：`PASS`
- `& .\tools\run-rust-checks.ps1 -Action all`：`51 passed, 0 failed`

### P1-04 旧账本与内置库只读状态

状态：`状态模型、静态检查和 ACE 只读连接分类已完成；认证参数和封装解密仍待突破`

目标：

- 为 `test.mh8` 与 `MoneyHome8.data` 建立结构化检查结果。
- 不把认证未打通误判为读取成功，也不让它阻塞新主库。

已完成：

1. 新增 `src/domain/legacy_source.rs`，定义统一 `LegacySourceStatus`：
   - `success`
   - `file_not_found`
   - `locked`
   - `permission_denied`
   - `auth_failed`
   - `object_invisible`
   - `not_implemented`
   - `invalid_format`
2. 扩展 `src/infrastructure/mh8.rs`，提供 `Mh8Library::inspect_read_only()` 和 `inspect_legacy_file()`，只读取文件元数据、头部字节和锁文件线索。
3. 新增 `tools/probe_legacy_sources.ps1`，默认使用 `C:\DCG-SZ\IT Manage\Private\Personal-Docs\test001.mh8`，输出文件大小、SHA-256、Jet 头、锁线索、MoneyHome8 进程 ID 和 ACE 只读连接分类。
4. 已确认 `test001.mh8` 文件存在，大小 `18661376` 字节，SHA-256 为 `8E40928F98A687D82CF671138E0000B740A5E6AEA7913EC179819BEA28BF23F8`。
5. `test001.mh8` 前 256 字节未识别 `Standard Jet DB`，ACE 只读打开返回“不可识别的数据库格式”，因此当前分类为 `invalid_format`，不是 `locked`。
6. `tools/moneyhome8-runtime/MoneyHome8.data` 原包大小 `2770980` 字节，ACE 只读打开同样返回 `invalid_format`；它应先走已知解压流程，不应直接当 Jet 库打开。
7. `artifacts/MoneyHome8.data.decompressed.mdb` 大小 `4583424` 字节，SHA-256 为 `9E7328BB2C408DD824CFC5B692EB413C8F8896F53A738B5C8EF14F3B96F2ACE7`，可识别 Jet 头，但 ACE 只读打开返回 `auth_failed`。
8. 探针记录 MoneyHome8 进程 ID 和 `mh.ldb` 锁线索，但只有文件级锁或读失败才提升为 `locked`，避免把“旧程序正在运行”误判为所有样本都被锁。
9. 新增 `tools/extract_moneyhome_data.ps1`，从 `MoneyHome8.data` 偏移 `125` 处识别 zlib 头 `78DA`，跳过 zlib 头后使用 `DeflateStream` 重建 `artifacts/MoneyHome8.data.decompressed.mdb`。
10. 已验证解压脚本输出 `4583424` 字节，SHA-256 与现有解压副本一致，且包含 `Standard Jet DB` 头。

任务：

1. 继续确认 `test001.mh8` 外层封装、加密或压缩格式；当前不能把它当作裸 Jet 库。
2. 针对 `artifacts/test-copy.mh8` 这类裸 Jet 账簿副本，继续尝试工作组 `mh.mdw`、用户名和口令来源，但不得写回原账簿。
3. 认证打通后再补对象枚举；如果连接成功但对象为 0，应分类为 `object_invisible`。

验收：

- 不存在文件、格式错误和当前测试账簿都有可区分结果。
- 旧账本检查不修改文件指纹。

本轮验证：

- `& .\tools\probe_legacy_sources.ps1`：`WARN`，原因是 `test001.mh8` 与 `MoneyHome8.data` 原包当前为 `invalid_format`，解压内置库为 `auth_failed`。
- `& .\tools\extract_moneyhome_data.ps1`：`PASS`，输出 SHA-256 为 `9E7328BB2C408DD824CFC5B692EB413C8F8896F53A738B5C8EF14F3B96F2ACE7`
- `& .\tools\run-rust-checks.ps1 -Action all`：`54 passed, 0 failed`

### P1-05 核心领域模型和仓储契约

状态：`第一轮审计完成，公开契约注释完整，后续随业务阶段补应用服务`

目标：

- 对齐 `domain-mapping-spec.md` 与代码中的领域类型。
- 补齐第一期 DTO、Repository 和错误类型的中文业务注释。

已完成：

1. 已审查 `docs/domain-mapping-spec.md`、`docs/sqlite-domain-coverage-audit.md`、账簿生命周期合同和交易合同。
2. 已扫描 `src/domain`、`src/app`、`src/infrastructure` 中公开 `struct`、`enum`、`trait` 和 `fn`，当前均有 Rust 文档注释。
3. 新增 `docs/workplans/phase1-domain-contract-audit.md`，记录第一期领域契约、仓储端口和 SQLite 覆盖关系。
4. 已确认当前没有用全字段可空大对象承载投资、账户或交易；专属业务通过专属表、扩展模型或输入投影表达。

任务：

1. 后续新增应用服务或 UI DTO 时继续按本审计口径补中文业务注释。
2. 投资、预算、提醒、同步、授权和备份恢复进入具体实现阶段时，继续按文档实体补应用层命令和仓储契约。

验收：

- 第一批模型都能对应到文档条目。
- 公共类型和跨层 DTO 有中文业务说明。
- Rust 检查保持通过。

本轮验证：

- 公开契约注释扫描：无缺失项
- `& .\tools\run-rust-checks.ps1 -Action all`：`54 passed, 0 failed`

### P1-06 PC 本地应用壳层与 Flutter DTO

状态：`Rust 本地核心壳层状态已完成；Flutter PC 首屏 DTO 已开始`

目标：

- 建立四大工作区和子导航空状态，并作为 Flutter PC 本地 API 的首屏 DTO 基础。

已完成：

1. 当前仓库是 Rust PC 本地核心库，后续由 Flutter Desktop 通过本地 API/FFI 消费其 DTO 和命令。
2. 新增 `src/app/workspace_shell.rs`，定义 `LedgerSessionState`、`WorkspaceKind`、`WorkspaceLoadState` 和 `WorkspaceShellState`。
3. 已建立四个顶层工作区枚举：
   - `FinanceData`
   - `Bookkeeping`
   - `FinancialReports`
   - `FinancialAnalysis`
4. 已建立无账簿、打开中、已打开、关闭中、失败恢复，以及工作区空、加载、就绪、失败状态。
5. `switch_workspace` 在无账簿或失败状态只切换目标工作区并保持 `Empty`，避免 UI 误触发 SQLite 或旧数据源读取。
6. `src/app/mod.rs` 已导出 `workspace_shell`。
7. 新增 `src/app/ui.rs`，以 Flutter 可消费 DTO 聚合工作区壳层、账户树、账户余额汇总和最近财务记录。
8. `src/app/mod.rs` 已导出 `ui`，后续 Flutter PC 本地 API 应消费同一套 ViewModel。

任务：

1. 继续补齐首屏 ViewModel、命令状态和 PC 本地 API 边界。
2. Flutter 页面只调用本地 API 或云端 API，不直接读取 SQLite、`mhlink.mdb`、`.cache` 或旧账簿。

验收：

- 四大工作区可切换。
- 子导航可见。
- 无账簿和打开失败状态可展示。

本轮验证：

- `& .\tools\run-rust-checks.ps1 -Action all`：`67 passed, 0 failed`
- `python .\tools\validate_sqlite_schema.py`：`SQLite schema validation: PASS`

## 3. 下一次实际开工建议

下一轮建议进入 Phase 2 的下一条主线：`Flutter PC 首屏与 Rust 本地 API 契约实现准备`。

1. 按 `docs/workplans/flutter-pc-local-api-plan.md` 细化 Rust 本地 API DTO 映射、错误码和 FFI 边界。
2. 优先接入应用层已有的 `WorkspaceShellState`、基础资料、交易报表和计划预算仓储端口。
3. 按 `docs/workplans/dotnet-sync-api-plan.md`、`mobile-offline-queue-plan.md`、`flutter-web-online-plan.md`、`conflict-resolution-plan.md` 和 `attachment-privacy-plan.md` 分拆 .NET、手机端、Web 端、冲突解决和附件隐私任务。

选择这个顺序的原因：

- P1-01 到 P1-06 已经完成第一层边界，Phase 2 计划、预算、提醒与财务目标 CRUD、Flutter 可消费首屏 ViewModel 和三端需求计划已落地，Rust 全量检查为 `67 passed, 0 failed`。
- 旧账簿和内置库边界已经结构化，不再阻塞 PC 本地核心、Flutter 三端和云同步开发。
- Backlog 下一项是 Flutter PC 首屏；当前 Rust 仓库应先稳定本地 API 契约，避免 Flutter 页面直接依赖 SQLite 或旧格式。

## 4. 持续验证命令

每轮修改后至少运行：

```powershell
python .\tools\validate_sqlite_schema.py
& .\tools\run-rust-checks.ps1 -Action all
```

当修改涉及外部只读数据源时，还应增加对应读取探测脚本或单元测试，并在交付说明中列出读取样本、返回状态和未验证缺口。
