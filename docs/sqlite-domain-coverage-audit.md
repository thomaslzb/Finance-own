# SQLite 领域覆盖审计

本文档把 `2000` 个事件中出现的 `53` 类实体候选与当前 SQLite 迁移逐项对照。
它用于防止核心交易表验证通过后，误以为预算、提醒、导入、同步和专属资产合同也已经完成。

## 1. 当前规模

| 项目 | 数量 |
| --- | ---: |
| 实体候选 | 53 |
| SQLite 表 | 63 |
| SQLite 视图 | 21 |
| SQLite 索引 | 56 |
| 适配器文件产物 | 2 |
| 建议后续对象 | 0 |

状态分布：

- `adapter_boundary`（适配器或文件边界）：3
- `implemented_contract_boundary`（已落地专属合同边界）：8
- `implemented_generic_truth`（由通用真相表承载）：10
- `implemented_input_projection`（已落地输入投影）：4
- `implemented_truth`（已落地真相表）：24
- `transient_not_persisted`（临时状态，不持久化）：4

## 2. 实体逐项覆盖

| 实体候选 | 事件出现 | 状态 | 当前 SQLite 对象 | 文件/适配器产物 | 后续对象 |
| --- | ---: | --- | --- | --- | --- |
| `account` | 448 | `implemented_truth` | `accounts` | - | - |
| `account_entry` | 254 | `implemented_truth` | `transaction_entries` | - | - |
| `account_group` | 225 | `implemented_truth` | `account_groups`, `accounts` | - | - |
| `application_setting` | 260 | `implemented_truth` | `application_settings` | - | - |
| `attachment` | 260 | `implemented_truth` | `attachments`, `transaction_attachments` | - | - |
| `backup_snapshot` | 171 | `adapter_boundary` | - | `backup-manifest.schema.json`, `backup-manifest-template.json` | - |
| `bond` | 49 | `implemented_generic_truth` | `investment_instruments`, `investment_trades`, `market_quotes` | - | - |
| `budget` | 157 | `implemented_truth` | `budgets`, `budget_items`, `v_budget_consumption_inputs` | - | - |
| `category` | 256 | `implemented_truth` | `categories` | - | - |
| `category_split` | 254 | `implemented_generic_truth` | `transaction_entries` | - | - |
| `credit_account` | 156 | `implemented_contract_boundary` | `accounts`, `transactions`, `credit_account_terms` | - | - |
| `currency` | 247 | `implemented_truth` | `currencies` | - | - |
| `debt` | 174 | `implemented_contract_boundary` | `accounts`, `transactions`, `transaction_entries`, `debt_contracts`, `v_debt_contract_inputs` | - | - |
| `exchange_rate` | 22 | `implemented_truth` | `exchange_rate_snapshots` | - | - |
| `export_projection` | 72 | `transient_not_persisted` | `v_ledger_entries`, `report_presets` | - | - |
| `fee_rule` | 18 | `adapter_boundary` | `fee_rule_snapshots` | - | - |
| `field_mapping` | 72 | `implemented_truth` | `import_field_mappings` | - | - |
| `financial_goal` | 154 | `implemented_truth` | `financial_goals`, `financial_goal_accounts`, `v_goal_account_balance_inputs`, `v_goal_progress_inputs` | - | - |
| `financial_plan` | 158 | `implemented_truth` | `financial_plan_scenarios`, `financial_plan_inputs`, `financial_plan_accounts` | - | - |
| `financial_product` | 55 | `implemented_generic_truth` | `investment_instruments`, `investment_trades`, `market_quotes` | - | - |
| `financing_transaction` | 82 | `implemented_contract_boundary` | `transactions`, `investment_trades`, `margin_contracts` | - | - |
| `fund` | 157 | `implemented_generic_truth` | `investment_instruments`, `investment_trades`, `market_quotes` | - | - |
| `futures_contract` | 129 | `implemented_contract_boundary` | `investment_instruments`, `investment_trades`, `market_quotes`, `futures_contract_terms` | - | - |
| `fx_transaction` | 22 | `implemented_generic_truth` | `transactions`, `transaction_entries`, `exchange_rate_snapshots` | - | - |
| `import_batch` | 72 | `implemented_truth` | `import_batches`, `v_import_batch_audit` | - | - |
| `insurance_policy` | 34 | `implemented_contract_boundary` | `insurance_policies`, `insurance_events`, `insurance_cash_value_snapshots`, `insurance_cash_value_history`, `v_insurance_cash_value_effective_ranges`, `transactions`, `transaction_entries` | - | - |
| `investment_object` | 18 | `implemented_truth` | `investment_instruments` | - | - |
| `investment_transaction` | 412 | `implemented_generic_truth` | `transactions`, `investment_trades` | - | - |
| `ledger` | 174 | `implemented_truth` | `ledgers` | - | - |
| `margin_account` | 82 | `implemented_contract_boundary` | `accounts`, `margin_account_terms` | - | - |
| `metal_position` | 129 | `implemented_generic_truth` | `investment_instruments`, `investment_trades`, `market_quotes` | - | - |
| `notification` | 26 | `implemented_truth` | `reminders`, `reminder_occurrences`, `v_today_reminder_inbox`, `notification_delivery_log` | - | - |
| `person` | 225 | `implemented_truth` | `parties` | - | - |
| `position` | 438 | `implemented_input_projection` | `v_investment_position_inputs` | - | - |
| `presentation_state` | 89 | `transient_not_persisted` | - | - | - |
| `quote` | 368 | `implemented_truth` | `market_quotes` | - | - |
| `raw_row` | 72 | `implemented_truth` | `import_rows`, `v_import_batch_audit` | - | - |
| `reminder` | 162 | `implemented_truth` | `schedules`, `schedule_occurrences`, `reminders`, `reminder_occurrences`, `v_schedule_lifecycle`, `v_today_reminder_inbox` | - | - |
| `repayment` | 156 | `implemented_generic_truth` | `transactions`, `transaction_entries` | - | - |
| `report` | 7 | `implemented_input_projection` | `report_presets` | - | - |
| `report_filter` | 31 | `implemented_truth` | `report_presets` | - | - |
| `report_projection` | 31 | `implemented_input_projection` | `v_ledger_entries`, `v_account_balances`, `v_investment_position_inputs` | - | - |
| `report_query` | 31 | `implemented_input_projection` | `report_presets`, `v_ledger_entries` | - | - |
| `security` | 151 | `implemented_generic_truth` | `investment_instruments`, `investment_trades`, `market_quotes` | - | - |
| `social_security_account` | 34 | `implemented_contract_boundary` | `accounts`, `transactions`, `social_security_profiles` | - | - |
| `sync_batch` | 26 | `implemented_truth` | `sync_batches`, `sync_object_results`, `sync_conflicts`, `sync_tombstones`, `v_open_sync_conflicts` | - | - |
| `tag` | 240 | `implemented_truth` | `tags`, `transaction_tags`, `account_tags` | - | - |
| `tangible_asset` | 111 | `implemented_contract_boundary` | `investment_instruments`, `market_quotes`, `tangible_asset_details` | - | - |
| `tool_input` | 89 | `transient_not_persisted` | - | - | - |
| `tool_result` | 89 | `transient_not_persisted` | - | - | - |
| `transaction` | 642 | `implemented_truth` | `transactions`, `transaction_entries`, `payroll_income_details`, `payroll_category_components`, `payroll_social_contributions`, `v_payroll_income_reconciliation` | - | - |
| `user_identity` | 26 | `adapter_boundary` | `sync_profiles` | - | - |
| `valuation` | 111 | `implemented_generic_truth` | `market_quotes` | - | - |

## 3. 已落地边界与剩余外部对象

### 3.1 债务、信用和专属资产合同

- `debt_contracts`, `credit_account_terms`, `futures_contract_terms`
- `margin_contracts`, `margin_account_terms`
- `insurance_policies`, `social_security_profiles`, `tangible_asset_details`

这些表已经落地，只保存通用交易模型不能表达的合同条款；资金变化仍必须进入 `transactions + transaction_entries`。

### 3.2 导入审计

- `import_batches`, `import_rows`, `import_field_mappings`

来源显示名与哈希、映射版本、逐行错误、重复判断和最终提交对象已经可以追溯。

### 3.3 同步与通知

- `sync_profiles`, `sync_batches`, `sync_object_results`, `sync_conflicts`, `sync_tombstones`
- `notification_delivery_log`

同步批次、对象结果、冲突和墓碑已落地；本地账簿始终独立可用，网络秘密不进入核心领域表。

### 3.4 设置与参考规则

- `application_settings`
- `fee_rule_snapshots`
- `backup-manifest.schema.json` 与 `backup-manifest-template.json` 作为账簿外文件清单合同，不放入活动数据库

### 3.5 工资收入扩展

- `payroll_income_details`
- `payroll_category_components`
- `payroll_social_contributions`
- `v_payroll_income_reconciliation`

工资仍属于运行时 `transaction` 实体，但收入、扣款、个人缴费和公司缴费不能压缩成一条普通收入分录。第七版迁移增加类型化扩展，并把实收现金和社保权益与账户分录做确定性核对。

### 3.6 待摊费用扩展

- `prepaid_expenses`
- `prepaid_expense_installments`
- `v_prepaid_expense_overview`

待摊费用账户、原始金额、人员、项目和摊销参数由专属表承载；每一期保存确定金额和幂等交易引用，资金变化仍必须进入 `transactions + transaction_entries`。

## 4. 结论

`0001_core.sql` 已覆盖账户、交易、标签、汇率、附件、投资输入和报表预设；
`0002_planning_and_automation.sql` 已补模板计划、预算、提醒、目标和规划输入。
`0003_contracts_exchange_and_sync.sql` 已补专属合同、导入审计、同步冲突、通知投递、设置和费率快照。
`0007_payroll_income_and_application_identity.sql` 已补工资收入组成、账户投影核对和 Finance Own SQLite 文件标识。
`0010_prepaid_expenses.sql` 已补待摊费用主体、分期计划和剩余金额查询投影。
数据库与账簿外文件实体均已形成可执行或可验证合同，不需要复制旧 Jet 表结构。
