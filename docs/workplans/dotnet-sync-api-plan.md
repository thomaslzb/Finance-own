# .NET 同步 API 需求计划

本文档承接 `three-client-requirements-analysis.md`，把 .NET 云端服务、PostgreSQL 对象副本和三端同步 API 的第一版需求拆成可实施边界。本文属于进行中工作计划。

## 1. 目标

.NET API 第一版必须支撑：

- Flutter Web 在线记账和查询。
- Flutter PC 上传/下载同步数据。
- Flutter Mobile 上传离线队列并下载其它端变更。
- PostgreSQL 保存完整新系统财务对象副本。
- 对象级多主同步、版本、墓碑、冲突和审计。
- PC/Web 完整冲突解决，手机端冲突摘要提示。

.NET API 第一版不得：

- 解析旧 MoneyHome8 原始文件。
- 保存旧 MoneyHome8 原始文件。
- 保存任何 PC 迁移审计、迁移报告、脱敏摘要或旧库诊断。
- 要求 PC 登录后才能本地记账。
- 用云端静默覆盖 PC 本地对象。

## 2. API 分组

### 2.1 AuthApi

| API | 路径草案 | 说明 |
| --- | --- | --- |
| 登录 | `POST /auth/login` | 邮箱、密码登录 |
| 刷新令牌 | `POST /auth/refresh` | 使用刷新令牌获取新访问令牌 |
| 退出登录 | `POST /auth/logout` | 当前设备令牌失效 |
| 当前用户 | `GET /me` | 用户资料和默认设置 |
| 设备列表 | `GET /me/devices` | 登录设备、最后同步时间和撤销状态 |
| 撤销设备 | `POST /me/devices/{device_id}/revoke` | 撤销指定设备 |

第一版账号优先支持邮箱、密码和昵称；手机号、第三方登录和企业 SSO 后置。

登录请求字段：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `email` | 否 | 用户邮箱，第一版主登录标识 |
| `password` | 否 | 用户密码，只通过 HTTPS 传输，不进入日志 |
| `device_name` | 否 | 当前设备展示名 |
| `device_type` | 否 | pc、web、mobile |
| `client_instance_id` | 否 | 客户端安装或浏览器会话生成的设备幂等标识 |

登录响应字段：

| 字段 | 说明 |
| --- | --- |
| `access_token` | 短期访问令牌 |
| `refresh_token` | 刷新令牌；客户端必须使用安全存储 |
| `expires_at` | 访问令牌过期时间 |
| `user` | `UserProfileDto` |
| `device` | `DeviceDto` |

`UserProfileDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `user_id` | 用户稳定标识 |
| `email` | 登录邮箱 |
| `nickname` | 展示昵称 |
| `phone_reserved` | 手机号预留字段；第一版可以为空，不作为登录阻塞 |
| `created_at` | 账号创建时间 |

`DeviceDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `device_id` | 云端设备稳定标识 |
| `device_name` | 用户可识别的设备名 |
| `device_type` | pc、web、mobile |
| `client_instance_id` | 客户端实例标识 |
| `last_seen_at` | 最近活跃时间 |
| `last_sync_at` | 最近成功同步时间 |
| `revoked_at` | 被撤销时间；未撤销时为空 |

设备撤销规则：

1. 撤销设备会使该设备刷新令牌失效。
2. 撤销设备不删除 PC 本地账本文件。
3. 被撤销设备继续上传同步批次时，API 返回 `device_revoked`。
4. Web 浏览器设备撤销后必须重新登录。

### 2.2 LedgerApi

| API | 路径草案 | 说明 |
| --- | --- | --- |
| 账本列表 | `GET /ledgers` | 返回当前用户可访问账本 |
| 创建云端账本 | `POST /ledgers` | Web 创建或 PC 开启同步时创建 |
| 账本详情 | `GET /ledgers/{ledger_id}` | 基础信息、角色、同步摘要 |
| 更新账本 | `PATCH /ledgers/{ledger_id}` | 名称、设置等基础信息 |
| 成员列表 | `GET /ledgers/{ledger_id}/members` | Owner/Editor/Viewer |
| 邀请成员 | `POST /ledgers/{ledger_id}/members/invitations` | 第一版 PC/Web |
| 修改成员角色 | `PATCH /ledgers/{ledger_id}/members/{member_id}` | Owner 操作 |
| 移除成员 | `DELETE /ledgers/{ledger_id}/members/{member_id}` | Owner 操作 |

账本删除第一版必须高风险处理：二次确认、审计、墓碑和设备同步。具体路径可在后续接口设计中细化，但不能做无审计硬删除。

`LedgerSummaryDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `ledger_id` | 云端账本稳定标识 |
| `name` | 账本名称 |
| `base_currency_code` | 本位币 |
| `current_user_role` | Owner、Editor、Viewer |
| `sync_summary` | 账本同步摘要 |
| `member_count` | 成员数量 |
| `created_at` | 创建时间 |
| `updated_at` | 最近更新时间 |
| `is_archived` | 是否归档 |

创建云端账本请求字段：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `name` | 否 | 账本名称 |
| `base_currency_code` | 否 | 本位币 |
| `source` | 否 | web_created、pc_sync_enable |
| `client_request_id` | 否 | 幂等请求 ID |
| `pc_local_ledger_id` | 是 | PC 开启同步时传入的新系统本地账本 ID；Web 创建时为空 |

`LedgerMemberDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `member_id` | 成员记录 ID |
| `ledger_id` | 所属账本 |
| `user_id` | 用户 ID |
| `email` | 成员邮箱 |
| `nickname` | 成员昵称 |
| `role` | Owner、Editor、Viewer |
| `status` | active、invited、removed |
| `invited_by` | 邀请人 |
| `joined_at` | 加入时间 |
| `updated_at` | 最近更新时间 |

邀请成员请求字段：

| 字段 | 可为空 | 说明 |
| --- | --- | --- |
| `email` | 否 | 被邀请邮箱 |
| `role` | 否 | Editor 或 Viewer；第一版不允许邀请直接成为 Owner |
| `message` | 是 | 邀请备注 |
| `client_request_id` | 否 | 幂等请求 ID |

成员权限矩阵：

| 操作 | Owner | Editor | Viewer |
| --- | --- | --- | --- |
| 查看账本和基础报表 | 是 | 是 | 是 |
| 新增/修改常规财务对象 | 是 | 是 | 否 |
| 删除或归档常规财务对象 | 是 | 是 | 否 |
| 上传附件 | 是 | 是 | 否 |
| 下载附件 | 是 | 是 | 是 |
| 查看同步状态 | 是 | 是 | 是 |
| 解决冲突 | 是 | 是 | 否 |
| 邀请成员 | 是 | 否 | 否 |
| 修改成员角色 | 是 | 否 | 否 |
| 移除成员 | 是 | 否 | 否 |
| 删除或归档账本 | 是 | 否 | 否 |

成员规则：

1. 每个账本必须至少有一个 Owner。
2. Owner 不能把最后一个 Owner 移除或降级。
3. Editor/Viewer 被移除后，后续 API 访问返回 `ledger_forbidden`。
4. Editor 降级为 Viewer 后，未上传的 PC/手机变更必须失败或进入冲突提示，不能静默上传。
5. PC 本地未开启同步的账本没有云端成员概念；云端成员变化不得自动删除 PC 本地文件。
6. 账本、对象、附件、同步批次和报表缓存都必须按 `ledger_id` 隔离。

### 2.3 SyncApi

| API | 路径草案 | 说明 |
| --- | --- | --- |
| 拉取变更 | `GET /ledgers/{ledger_id}/sync/changes` | 按游标和对象类型拉取 |
| 上传批次 | `POST /ledgers/{ledger_id}/sync/batches` | 上传客户端对象变更 |
| 查询批次 | `GET /ledgers/{ledger_id}/sync/batches/{batch_id}` | 查看处理结果 |
| 同步摘要 | `GET /ledgers/{ledger_id}/sync/status` | 待拉取、冲突数、最近同步 |
| 取消批次 | `POST /ledgers/{ledger_id}/sync/batches/{batch_id}/cancel` | 取消尚未进入不可取消阶段的同步批次 |

上传批次必须包含：

| 字段 | 说明 |
| --- | --- |
| `client_batch_id` | 批次幂等键 |
| `device_id` | 来源设备 |
| `base_cursor` | 客户端上传前已知游标 |
| `changes` | 对象变更列表 |
| `created_at` | 客户端批次时间 |
| `upload_mode` | `full`、`chunked`、`resume` |
| `chunk_info` | 分片上传信息；非分片时为空 |
| `checkpoint_token` | 断点续传令牌；首次上传可为空 |

对象变更必须包含：

| 字段 | 说明 |
| --- | --- |
| `client_change_id` | 对象变更幂等键 |
| `object_type` | 账本、账户、交易等对象类型 |
| `object_id` | 稳定对象 ID |
| `operation` | create、update、delete |
| `base_version` | 客户端编辑时看到的版本 |
| `payload` | 业务字段 |
| `tombstone` | 删除操作的墓碑信息 |

`changes` 响应必须包含：

| 字段 | 说明 |
| --- | --- |
| `ledger_id` | 账本范围，必须和路径一致 |
| `server_cursor` | 本次响应结束后的服务端游标 |
| `has_more` | 是否还有后续变更 |
| `objects` | 云端对象版本列表 |
| `conflict_summary` | 当前账本冲突摘要 |

`CloudObjectVersionDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `object_type` | 对象类型 |
| `object_id` | 稳定对象 ID |
| `version` | 云端对象版本 |
| `operation` | create、update、delete |
| `payload` | 新系统对象字段，不包含旧 MoneyHome8 原始字段 |
| `tombstone` | 删除墓碑，非删除时为空 |
| `updated_at` | 云端提交时间 |
| `updated_by_user_id` | 修改用户 |
| `updated_device_id` | 修改设备 |

上传批次响应必须包含：

| 字段 | 说明 |
| --- | --- |
| `batch_id` | 云端批次 ID |
| `client_batch_id` | 客户端批次幂等键 |
| `status` | accepted、partial_success、failed、conflict_created |
| `new_server_cursor` | 批次处理后的服务端游标 |
| `results` | 每个对象变更的处理结果 |
| `conflict_ids` | 本批次创建或关联的冲突 ID |
| `resume_token` | 批次未完成时的续传令牌 |
| `cancel_allowed` | 是否仍允许取消 |
| `checkpoint` | 服务端已处理到的分片、变更序号和游标 |

`SyncObjectResultDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `client_change_id` | 客户端对象变更幂等键 |
| `object_type` | 对象类型 |
| `object_id` | 稳定对象 ID |
| `result` | applied、replayed、rejected、conflict_created |
| `server_version` | 成功应用或幂等重放后的云端版本 |
| `error` | 拒绝时返回结构化错误 |

`SyncChunkInfoDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `chunk_index` | 当前分片序号，从 0 开始 |
| `chunk_count` | 总分片数 |
| `chunk_hash` | 当前分片内容哈希 |
| `total_payload_hash` | 整个批次 payload 哈希 |
| `previous_checkpoint_token` | 上一次成功检查点令牌 |

同步批次规则：

1. 小批次可以一次提交，大批次必须支持 `chunked` 上传和 `resume` 续传。
2. 服务端必须按 `client_batch_id + device_id + ledger_id` 幂等识别批次，重复提交返回原批次状态和逐项结果。
3. 分片上传必须校验分片序号、分片哈希、总 payload 哈希和上一检查点令牌；错序、缺片或哈希不匹配时拒绝当前分片。
4. 批次取消只允许在 `accepted`、`receiving`、`validating` 等未写入对象版本阶段；进入写入或冲突创建阶段后返回 `sync_cancel_not_allowed`。
5. 批次失败不得发布半批新对象版本；已应用的对象必须在逐项结果中可追溯，未应用对象保留可重试状态。
6. 删除操作必须生成墓碑对象版本，并在后续拉取中传播到 PC/Web/手机；客户端不得把缺失对象误判为本地缓存损坏后复活。
7. 拉取变更支持按对象类型、游标和 `has_more` 分页；断点续拉必须返回稳定顺序和最后成功游标。
8. 查询批次接口必须能返回真实对象结果、冲突 ID、拒绝原因、续传状态、取消状态和脱敏诊断 ID。

### 2.4 ObjectQueryApi

Web 在线端需要按对象查询云端副本。第一版不要求把所有报表都做成复杂服务端分析，但必须支持基础页面查询。

| API | 路径草案 | 说明 |
| --- | --- | --- |
| 账户树 | `GET /ledgers/{ledger_id}/accounts/tree` | 账户组、账户和余额摘要 |
| 流水列表 | `GET /ledgers/{ledger_id}/entries` | 日期、账户、分类、标签筛选 |
| 分类列表 | `GET /ledgers/{ledger_id}/categories` | 包含归档状态 |
| 标签列表 | `GET /ledgers/{ledger_id}/tags` | 包含归档状态 |
| 预算列表 | `GET /ledgers/{ledger_id}/budgets` | 预算定义和摘要 |
| 提醒列表 | `GET /ledgers/{ledger_id}/reminders` | 提醒状态 |

列表必须使用 `limit + cursor`，不能依赖大 offset。

### 2.5 ConflictApi

| API | 路径草案 | 说明 |
| --- | --- | --- |
| 冲突摘要 | `GET /ledgers/{ledger_id}/sync/conflicts/summary` | 手机端可用 |
| 冲突列表 | `GET /ledgers/{ledger_id}/sync/conflicts` | PC/Web 完整列表 |
| 冲突详情 | `GET /ledgers/{ledger_id}/sync/conflicts/{conflict_id}` | 字段级差异 |
| 解决冲突 | `POST /ledgers/{ledger_id}/sync/conflicts/{conflict_id}/resolve` | 生成解决版本 |

解决方式：

1. `keep_local`
2. `keep_cloud`
3. `merge_fields`
4. `save_as_copy`
5. `defer`

`ConflictSummaryDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `ledger_id` | 所属账本 |
| `total_count` | 未解决冲突总数 |
| `high_risk_count` | 账户、交易、账本设置等高风险冲突数量 |
| `last_conflict_at` | 最近冲突时间 |

`ConflictDetailDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `conflict_id` | 冲突稳定标识 |
| `ledger_id` | 所属账本 |
| `object_type` | 冲突对象类型 |
| `object_id` | 冲突对象 ID |
| `base_version` | 两端共同基线版本 |
| `local_version` | 上传端或本端版本 |
| `cloud_version` | 云端当前版本 |
| `field_diffs` | 字段级差异列表 |
| `allowed_resolutions` | 当前用户和对象类型允许的解决方式 |
| `created_at` | 冲突创建时间 |

`FieldDiffDto` 字段：

| 字段 | 说明 |
| --- | --- |
| `field_path` | 对象字段路径 |
| `label` | 可展示字段名 |
| `base_value` | 基线值，敏感字段必须脱敏 |
| `local_value` | 上传端或本端值，敏感字段必须脱敏 |
| `cloud_value` | 云端当前值，敏感字段必须脱敏 |
| `mergeable` | 是否允许字段级合并 |

解决冲突请求必须包含：

| 字段 | 说明 |
| --- | --- |
| `resolution` | `keep_local`、`keep_cloud`、`merge_fields`、`save_as_copy` 或 `defer` |
| `merged_payload` | 字段级合并后的对象；仅 `merge_fields` 时必填 |
| `reason` | 用户可选说明，高风险对象建议必填 |
| `client_resolution_id` | 幂等键，避免重复提交 |

### 2.6 AttachmentApi

| API | 路径草案 | 说明 |
| --- | --- | --- |
| 上传附件 | `POST /ledgers/{ledger_id}/attachments` | 内容和元数据 |
| 附件元数据 | `GET /ledgers/{ledger_id}/attachments/{attachment_id}` | 权限校验后返回 |
| 下载附件 | `GET /ledgers/{ledger_id}/attachments/{attachment_id}/content` | 短期授权或流式下载 |
| 删除附件引用 | `DELETE /ledgers/{ledger_id}/attachments/{attachment_id}/references/{object_id}` | 解除引用，不立即物理删除 |

## 3. PostgreSQL 对象副本需求

PostgreSQL 不逐表复刻 PC SQLite，但必须支持对象版本、游标、冲突和审计。

建议对象族：

1. `cloud_ledgers`
2. `cloud_ledger_members`
3. `cloud_objects`
4. `cloud_object_versions`
5. `cloud_sync_batches`
6. `cloud_sync_results`
7. `cloud_conflicts`
8. `cloud_tombstones`
9. `cloud_attachments`
10. `cloud_audit_events`

`cloud_objects` 需要至少表达：

| 字段 | 说明 |
| --- | --- |
| `ledger_id` | 账本范围 |
| `object_type` | 对象族 |
| `object_id` | 稳定对象 ID |
| `current_version` | 当前版本 |
| `is_deleted` | 是否墓碑删除 |
| `updated_at` | 云端更新时间 |
| `updated_by` | 用户 |
| `updated_device_id` | 设备 |

`cloud_object_versions` 需要至少表达：

| 字段 | 说明 |
| --- | --- |
| `ledger_id` | 账本范围 |
| `object_type` | 对象族 |
| `object_id` | 稳定对象 ID |
| `version` | 对象版本，按对象单调递增 |
| `payload_json` | 新系统对象快照 |
| `payload_hash` | 用于幂等和冲突判断的内容哈希 |
| `created_at` | 版本创建时间 |
| `created_by` | 用户 |
| `device_id` | 来源设备 |

`cloud_sync_batches` 需要至少表达：

| 字段 | 说明 |
| --- | --- |
| `batch_id` | 云端批次 ID |
| `ledger_id` | 账本范围 |
| `client_batch_id` | 客户端幂等键 |
| `device_id` | 来源设备 |
| `base_cursor` | 客户端上传前已知游标 |
| `status` | 批次处理状态 |
| `created_at` | 云端接收时间 |
| `upload_mode` | full、chunked、resume |
| `checkpoint_json` | 断点续传检查点 |
| `cancel_requested_at` | 用户请求取消时间 |
| `cancelled_at` | 实际取消时间 |
| `resume_token_hash` | 续传令牌哈希 |

`cloud_conflicts` 需要至少表达：

| 字段 | 说明 |
| --- | --- |
| `conflict_id` | 冲突稳定标识 |
| `ledger_id` | 账本范围 |
| `object_type` | 对象族 |
| `object_id` | 稳定对象 ID |
| `base_version` | 基线版本 |
| `local_version` | 上传端版本 |
| `cloud_version` | 云端版本 |
| `status` | open、resolved、deferred |
| `resolution` | 解决方式 |
| `resolved_by` | 解决用户 |
| `resolved_at` | 解决时间 |

云端 PostgreSQL 表名可以在技术设计阶段调整，但上述字段语义必须保留。

## 4. 错误模型

| 错误码 | 场景 |
| --- | --- |
| `unauthenticated` | 未登录或令牌无效 |
| `token_expired` | 访问令牌过期 |
| `ledger_forbidden` | 无账本权限 |
| `ledger_readonly` | 当前角色只读 |
| `object_not_found` | 对象不存在或不可见 |
| `version_conflict` | 对象版本冲突 |
| `sync_conflict_created` | 已创建显式冲突 |
| `idempotency_replay` | 幂等重放，返回原处理结果 |
| `validation_failed` | 字段校验失败 |
| `attachment_too_large` | 附件超出大小限制 |
| `storage_failed` | 云端存储失败 |
| `sync_chunk_invalid` | 分片序号、哈希或检查点不匹配 |
| `sync_resume_invalid` | 续传令牌无效或不属于当前设备/账本 |
| `sync_cancel_not_allowed` | 批次已进入不可取消阶段 |
| `sync_batch_cancelled` | 批次已取消 |
| `sync_tombstone_required` | 删除操作缺少墓碑或版本 |

错误响应必须包含：

1. 错误码。
2. 可展示消息。
3. 诊断 ID。
4. 字段错误列表。
5. 可选冲突 ID 或批次 ID。

## 5. 安全和隐私

1. 所有 API 必须走 HTTPS。
2. 服务端保存静态加密数据和密钥管理策略。
3. 所有读写必须校验 `ledger_id` 和成员角色。
4. 附件下载必须经过权限校验或短期授权。
5. 响应不得包含旧 MoneyHome8 原始路径、迁移审计、迁移报告、脱敏摘要或 PC 机器环境诊断。
6. 诊断日志必须避免记录密码、令牌、完整附件内容和旧账本原始行。

## 6. 验收口径

1. 同一 `client_batch_id` 重复上传返回原批次和逐项结果，不重复创建对象。
2. 分片上传中断后使用续传令牌继续，服务端从最后检查点恢复。
3. 分片哈希不匹配、错序或续传令牌跨账本使用时被拒绝。
4. 批次进入不可取消阶段前可取消，取消后不发布未完成对象版本。
5. Web 删除对象后生成墓碑，PC 和手机拉取后按墓碑删除或隐藏本地投影，不复活旧对象。
6. 查询批次能返回 applied、replayed、rejected、conflict_created、cancelled 和 failed 的真实对象结果。
7. 同步错误、批次状态和诊断 ID 不包含旧迁移证据、PC 完整本地路径或旧原始行。

## 7. 当前无需人工确认

本计划没有引入新的产品取舍；它细化的是已经确认的 .NET、PostgreSQL、对象级同步和三端写入边界。
