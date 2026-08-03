# 第一期领域契约审计

本文档记录 P1-05 对当前 Rust 领域模型、应用端口和基础设施边界的审计结果。审计目标不是扩大实现范围，而是确认第一期已经落地的契约可读、可验证，并且没有把旧 Jet 表结构直接复制进新账簿模型。

## 1. 审计输入

- `docs/domain-mapping-spec.md`
- `docs/sqlite-domain-coverage-audit.md`
- `docs/runtime-ledger-lifecycle-and-settings-contract.md`
- `docs/runtime-transactions-and-ledger-contract.md`
- `src/domain`
- `src/app`
- `src/infrastructure`

## 2. 当前结论

状态：`通过，第一期领域契约边界清晰`

- 公开 `struct`、`enum`、`trait` 和 `fn` 均已有 Rust 文档注释。
- 账户、基础资料、交易、报表输入、存款利率、工资、待摊费用、参考库、缓存和旧源状态均有独立领域类型或应用端口。
- 共享参考库使用 `ReferenceStoreRepository`，旧格式只读检查使用 `LegacySourceInspection`，缓存候选读取使用 `CacheStoreRepository`；三者没有混入 SQLite 真相源。
- `docs/sqlite-domain-coverage-audit.md` 显示当前 SQLite 覆盖 `53` 类实体候选，不需要复制旧 Jet 表结构。
- 当前模型没有新增“全字段可空大对象”来承载投资、账户或交易；专属业务通过专属表、扩展模型或输入投影表达。

## 3. 已对齐模型

| 文档实体 | 当前 Rust/SQLite 边界 | 状态 |
| --- | --- | --- |
| `Ledger` | `domain::ledger::LedgerProfile`、`sqlite::SqliteLedgerStore`、`ledgers` | 已落地 |
| `AccountGroup` / `Account` | `domain::reference_data::*Record`、`app::reference_data::*`、`account_groups`、`accounts` | 已落地 |
| `Currency` / `Category` / `Tag` / `Person` | `domain::reference_data`、`app::reference_data`、`currencies`、`categories`、`tags`、`parties` | 已落地 |
| `Transaction` / `Entry` | `domain::transactions`、`app::transactions`、`transactions`、`transaction_entries` | 已落地 |
| `ReportProjection` | `domain::reporting`、`app::reporting`、`v_ledger_entries`、`v_account_balances`、`v_investment_position_inputs` | 已落地 |
| `RateRule` / `Quote` / `FeeRule` | `domain::reference_store`、`infrastructure::reference_json`、`artifacts/reference/mhlink-reference.json` | 已落地 |
| `LookupIndex` / `InvestmentCatalog` | `domain::cache_store`、`infrastructure::cache_file` | 阶段性落地 |
| 旧账簿与内置库状态 | `domain::legacy_source`、`infrastructure::mh8`、`tools/probe_legacy_sources.ps1` | 阶段性落地 |
| 工资 / 待摊费用 / 余额调整 | `domain::payroll`、`domain::prepaid_expenses`、`domain::balance_adjustments` | 已落地 |

## 4. 后续缺口

- `test001.mh8` 当前是 `invalid_format`，需要继续确认外层封装、加密或压缩格式。
- `MoneyHome8.data.decompressed.mdb` 可识别 Jet 头，但 ACE 只读打开仍为 `auth_failed`，需要认证参数或等价认证上下文。
- 缓存中文名称仍待解析 GBK/ANSI 长度前缀协议；当前只把 ASCII token 作为候选。
- 投资、预算、提醒、同步、授权和备份恢复虽已有 SQLite 合同，仍需按后续阶段补应用服务和 UI 工作流。

## 5. 验证

```powershell
python .\tools\validate_sqlite_schema.py
& .\tools\run-rust-checks.ps1 -Action all
& .\tools\probe_moneyhome_cache.ps1
& .\tools\probe_legacy_sources.ps1
& .\tools\extract_moneyhome_data.ps1
```

本轮结果：

- SQLite schema validation: `PASS`
- Rust：`54 passed, 0 failed`
- 缓存探针：`PASS`
- 旧源探针：`WARN`，分类原因已写入 `docs/workplans/phase1-execution-plan.md`
- 内置库解压：`PASS`
