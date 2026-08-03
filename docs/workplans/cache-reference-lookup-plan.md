# 缓存、参考库与候选检索需求计划

本文档承接 `cache-semantics.md`、`cache-and-package-investigation.md`、`code-type-mapping.md`、`cross-domain-dataflow-catalog.md`、`domain-mapping-spec.md`、`coverage-status.md`、`open-gaps-register.md`、`localization-accessibility-display-plan.md` 和 `phase1-execution-plan.md`，定义 Finance Own 第一版对旧缓存、参考库和候选检索的需求边界。

第一版必须把旧 `.cache` 文件视为 PC 本地只读候选来源，而不是账本事实源。Web 和手机不得直接读取旧缓存文件。

## 1. 目标

第一版必须支持：

1. PC 本地只读探测 `MoneyHome8.cache` 和 `Investment.cache`。
2. PC 本地按代码、名称候选、拼音或缩写查询旧缓存候选。
3. PC 本地区分 `_PY`、`_LIST`、`_3`、`_4` 和 `_9` 的已确认语义。
4. PC 本地把可靠候选映射到新系统投资品、基金或货币基金选择器。
5. 新系统选择器统一使用稳定对象 ID、候选版本、来源和校准状态。
6. 未确认的中文片段、长度前缀、字段布局和旧类别码诊断只保存在 PC 本地。
7. Web 和手机只使用同步后的新系统对象、云端候选或摘要缓存，不直接依赖旧缓存。

第一版不要求：

1. 完整复刻旧缓存二进制协议。
2. 旧缓存字段布局全部逆向完成后才启动三端开发。
3. 把旧缓存中的未确认中文片段直接写成新系统业务名称。

第一版不支持：

1. Web 或手机上传、保存、解析旧 `.cache` 文件。

第一版必须禁止：

1. 把 `MoneyHome8.cache`、`Investment.cache` 或旧缓存原始片段上传云端。
2. 把旧缓存解析诊断、旧路径、旧字段值、迁移审计、迁移报告或脱敏摘要保存到云端、Web、手机、日志、导出或支持包。
3. 把缓存候选当成账户、交易、持仓、行情、报表或余额的权威事实。

## 2. 数据来源分层

| 来源 | 第一版定位 | 可进入云端 | 说明 |
| --- | --- | --- | --- |
| PC SQLite | PC 本地账本事实源 | 用户开启同步后的新系统对象可进入 | 交易、账户、分录、版本和墓碑以新系统 DTO 同步 |
| `mhlink.mdb` | PC 本地参考库候选 | 可靠映射后的新系统参考对象可进入 | 价格、利率、费率等参考值必须带来源和版本 |
| `MoneyHome8.cache` | PC 本地综合检索候选 | 否 | `_PY`、`_LIST` 候选用于迁移和选择器辅助 |
| `Investment.cache` | PC 本地投资品目录候选 | 否 | `_3`、`_4`、`_9` 候选用于投资品分类辅助 |
| 云端候选服务 | Web/手机在线候选 | 是 | 只保存新系统对象和受控参考数据 |
| 手机摘要缓存 | 手机轻量使用 | 否，除本机草稿上传外 | 不保存完整账本，不保存旧缓存原文 |

## 3. 缓存候选 DTO

`LegacyCacheProbeDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `source_kind` | moneyhome_cache、investment_cache |
| `source_file_label` | 脱敏来源文件名 |
| `source_hash` | 来源文件哈希 |
| `header_state` | valid_moneyhome_cache、unknown、damaged |
| `marker_counts` | `_PY`、`_LIST`、`_3`、`_4`、`_9` 等标记计数 |
| `encoding_state` | ascii_only、gbk_candidate、length_prefix_pending、unsupported |
| `probe_errors` | 探测错误码集合 |

`LookupCandidateDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `candidate_id` | PC 本地候选 ID，不等同于新系统对象 ID |
| `source_kind` | moneyhome_cache、investment_cache、reference_store、cloud_catalog |
| `source_marker` | `_PY`、`_LIST`、`_3`、`_4`、`_9` 或参考库表名 |
| `raw_code` | 旧代码或候选代码摘要 |
| `display_name` | 可靠解析后的显示名；不可靠时为空 |
| `abbr_keys` | 拼音、缩写或英文别名候选 |
| `catalog_type` | market_tradable、fund、money_fund、unknown |
| `confidence` | reliable、inferred、pending_protocol、unsupported |
| `candidate_version` | 候选版本，用于提交防陈旧 |
| `diagnostic_ref` | PC 本地诊断引用；不得同步 |

## 4. 解析与映射规则

1. `MoneyHome8.cache` 文件头为 `MoneyHomeCache` 时才进入候选解析；文件头异常必须阻断并返回 `cache_header_invalid`。
2. `_PY` 第一版可作为代码、名称、拼音首字母或缩写检索候选；不能假定每条 `_PY` 都是可靠业务名称。
3. `_LIST` 第一版可作为展示记录候选；字段分隔规则未确认时只能返回可靠 token 和 `pending_protocol`。
4. `Investment.cache` 的 `_3` 高可信映射为交易型市场标的候选，覆盖股票、指数、ETF、LOF、REIT、新股和部分海外证券。
5. `Investment.cache` 的 `_4` 高可信映射为场外基金或公募基金产品候选。
6. `Investment.cache` 的 `_9` 高可信映射为货币基金或现金管理类产品候选。
7. `_3/_4/_9` 必须区分“真实类别记录”和“字节级偶发匹配”；无法区分时返回 `pending_protocol`，不得写入正式目录。
8. 中文名称只有在编码、长度前缀、字段边界和来源语义可靠时才能写入 `display_name`。
9. 用户从候选创建新系统对象时，必须展示来源、置信度和可编辑名称；用户确认后的新系统名称才可同步。
10. 候选被旧缓存重建、参考库更新或云端目录刷新后，提交必须携带 `candidate_version`；陈旧候选拒绝提交并保留草稿。
11. 候选查询不得改变 PC SQLite 真相表、旧缓存文件或参考库文件。
12. 候选诊断只允许 PC 本地研发和迁移工作区读取；Web、手机、导出和支持包不得包含旧缓存原文。

## 5. 三端边界

PC 必须支持：

1. 本地只读缓存探测和候选查询。
2. 使用缓存候选辅助迁移、证券/基金/货币基金选择和代码变更校准。
3. 标记候选来源、版本和校准状态。
4. 把可靠映射或用户确认后的新系统对象写入 PC SQLite。

Web 必须支持：

1. 查询云端新系统对象和受控候选目录。
2. 展示 PC 同步后的新系统投资品、基金和货币基金对象。
3. 拒绝旧缓存文件上传、旧缓存诊断展示和旧路径保存。

手机必须支持：

1. 使用云端同步下来的候选摘要和最近选择缓存。
2. 离线草稿引用缓存候选时展示缓存状态。
3. 候选失效、权限变化或版本陈旧时保留草稿并提示回到 PC/Web 处理。
4. 不保存完整旧缓存、旧字段原文或旧迁移诊断。

## 6. 缓存失效与多账本隔离

1. 每个候选结果必须带账本、账号、设备和来源边界；跨账本不得复用选择器状态。
2. PC 切换账本后必须清理页面候选、草稿上下文和缓存诊断引用。
3. 云端目录更新不得覆盖 PC 本地已确认的新系统对象，除非用户进入显式更新或合并流程。
4. 手机摘要缓存过期时只能提示刷新，不得把旧候选重新上传为正式对象。
5. 删除或归档新系统投资品后，旧缓存命中只能作为重新创建候选，不得复活已删除对象。

## 7. 错误码

| 错误码 | 触发条件 | 前端处理 |
| --- | --- | --- |
| `cache_header_invalid` | 缓存文件头无效或损坏 | 阻断解析 |
| `cache_marker_unsupported` | 标记类型不在已知集合 | 作为未知候选保留 PC 本地诊断 |
| `cache_encoding_pending` | 中文字段编码或长度前缀未确认 | 不写入业务名称 |
| `cache_candidate_stale` | 提交时候选版本已变化 | 保留草稿并要求重选 |
| `cache_candidate_ambiguous` | 同一代码或缩写命中多个候选 | 要求用户选择或编辑 |
| `cache_cross_ledger_scope` | 候选或草稿引用跨账本上下文 | 阻断提交并清理选择器 |
| `cache_diagnostic_forbidden` | Web、手机、导出或支持包请求旧诊断 | 拒绝并记录脱敏审计 |

## 8. 验收口径

1. PC 能识别 `MoneyHome8.cache` 和 `Investment.cache` 的有效文件头。
2. PC 能统计 `_PY`、`_LIST`、`_3`、`_4` 和 `_9` 候选标记。
3. PC 能按代码、缩写或可靠名称返回候选。
4. `_3`、`_4`、`_9` 能分别映射为交易型市场标的、基金和货币基金候选；无法确认的记录标记 `pending_protocol`。
5. 未确认中文片段不会写入新系统业务名称。
6. 用户确认后的新系统对象可以同步；旧缓存文件、旧路径、旧字段原文和解析诊断不上传云端。
7. Web 和手机不能上传、解析或展示旧 `.cache` 文件。
8. 候选版本陈旧时提交失败并保留草稿。
9. 切换账本后不能沿用上一个账本的候选、草稿或诊断引用。

## 9. 当前无需人工确认

本计划没有引入新的产品取舍；它把已确认的 PC 本地 Rust 只读缓存探测、三端候选来源隔离、旧缓存诊断 PC 本地保存和未确认中文协议不得写入业务名称的边界整理为实施需求。
