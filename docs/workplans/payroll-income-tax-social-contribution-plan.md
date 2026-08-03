# 工资收入、税务与社保缴费需求计划

本文档承接 `three-client-requirements-analysis.md`、`command-form-lifecycle-plan.md`、`master-data-lifecycle-plan.md`、`amount-currency-exchange-rate-plan.md`、`insurance-social-security-tangible-assets-plan.md` 和 `payroll-income-domain-contract.md`，定义 Finance Own 第一版工资收入、收入组成、普通扣款、个人社保缴费、公司社保缴费、个人所得税计算快照和原子提交边界。本文只定义新系统需求口径，不把旧 MoneyHome8 尚未校准的工资、税务或社保报表公式标记为已兼容。

## 1. 目标

1. 支持 PC/Web 创建、修改、删除和查询工资收入对象，保持工资头、组成明细、现金流入、社保权益、税务快照和审计事件一致。
2. 保证工资实收现金、普通扣款、个人社保、公司社保和社保权益按固定公式逐分守恒。
3. 明确税务计算器是草稿辅助能力，取消不回填，确认后保存可审计快照，但不能绕过工资提交直接入账。
4. 保证账户、分类、人员、社保账户和标签全部使用稳定 ID 与版本，不使用显示名称推断业务对象。
5. 保证旧 MoneyHome8 工资迁移证据、迁移审计、迁移报告、脱敏摘要、旧路径和旧原始行只保存在 PC 本地。

## 2. 非目标

1. 第一版不承诺完整复刻旧版个人所得税、地区社保、住房公积金和专项附加扣除公式。
2. 第一版不在手机端提供复杂工资组成、税务计算器或社保缴费编辑器。
3. 第一版不允许 Web 或手机读取旧 MoneyHome8 工资原始证据。
4. 第一版不允许公司社保缴费进入现金实收账户。
5. 第一版不使用显示文字、标题、控件可访问性名称或导入行文本作为已绑定对象。

## 3. 领域对象

### 3.1 `PayrollIncome`

| 字段 | 说明 |
| --- | --- |
| `payroll_id` | 工资对象稳定 ID |
| `ledger_id` | 账本 ID |
| `currency_code` | 原币币种 |
| `business_date` | 工资业务日期 |
| `cash_account_id` | 实收现金账户 ID |
| `person_id` | 可选人员 ID；存在社保缴费时必填 |
| `memo` | 备注 |
| `tag_ids` | 标签稳定 ID 列表 |
| `status` | 草稿、已过账、已冲正、已删除 |
| `version` | 对象版本 |
| `created_by_device_id` | 创建设备 ID |
| `source_type` | 手工、导入、迁移 |

### 3.2 `PayrollIncomeComponent`

| 字段 | 说明 |
| --- | --- |
| `component_id` | 收入组成稳定 ID |
| `payroll_id` | 工资对象 ID |
| `category_id` | 收入分类 ID |
| `amount_minor` | 原币最小单位金额 |
| `display_order` | 页面排序 |
| `memo` | 明细备注 |

### 3.3 `PayrollDeductionComponent`

| 字段 | 说明 |
| --- | --- |
| `component_id` | 扣款组成稳定 ID |
| `payroll_id` | 工资对象 ID |
| `category_id` | 扣款分类 ID |
| `amount_minor` | 原币最小单位金额 |
| `deduction_kind` | 普通扣款、个人所得税、其它扣款 |
| `memo` | 明细备注 |

### 3.4 `PayrollSocialContribution`

| 字段 | 说明 |
| --- | --- |
| `contribution_id` | 社保缴费组成稳定 ID |
| `payroll_id` | 工资对象 ID |
| `person_id` | 参保人员 ID |
| `social_security_account_id` | 社保账户 ID |
| `social_security_project` | 养老、医疗、失业、工伤、生育、住房公积金等项目 |
| `personal_amount_minor` | 个人缴费金额 |
| `company_amount_minor` | 公司缴费金额 |
| `memo` | 明细备注 |

### 3.5 `PayrollTaxCalculation`

| 字段 | 说明 |
| --- | --- |
| `tax_calculation_id` | 税务计算快照 ID |
| `payroll_id` | 工资对象 ID |
| `tax_rule_version` | 税制规则版本 |
| `input_snapshot_json` | 计算输入快照 |
| `rounding_mode` | 舍入规则 |
| `tax_amount_minor` | 计算结果中的个税金额 |
| `confirmed_at` | 用户确认回填时间 |
| `calibration_status` | 可用、受限、需公式校准 |

## 4. 计算口径

所有工资金额必须使用同一原币最小单位和受检整数运算：

```text
gross_income = sum(income_components)
ordinary_deductions = sum(deduction_components)
personal_social = sum(social_contributions.personal_amount)
company_social = sum(social_contributions.company_amount)
net_cash = gross_income - ordinary_deductions - personal_social
social_account_credit = personal_social + company_social
```

规则：

1. `net_cash` 不得为负。
2. `net_cash` 必须等于实收账户现金流入金额。
3. `social_account_credit` 必须等于社保账户权益增加金额。
4. 公司社保缴费不进入现金账户、收入合计或实收现金，只进入对应社保账户权益。
5. 税务扣款属于 `PayrollDeductionComponent`，税务计算快照只解释扣款来源，不单独形成现金分录。
6. 页脚汇总、报表投影和净资产投影必须从工资事实和分录重建，不能保存可手工编辑的独立汇总数。

## 5. 原子提交

一次工资确认必须在一个数据库事务中完成：

1. 校验账簿、币种、实收账户、收入分类、扣款分类、人员、社保账户、标签和预期版本。
2. 保存工资头、收入组成、扣款组成、社保缴费组成和可选税务计算快照。
3. 生成实收账户现金流入 posting。
4. 生成社保账户权益 posting。
5. 保存附件关系、标签关系和审计事件。
6. 从同一提交版本刷新账户流水、财务记录、收支报表、社保账户、预算、目标和净资产投影。

任一组成失败时整体回滚。不得先写实收现金，再异步补写扣款、社保权益或税务快照；也不得只保存实收金额而丢失工资组成。

## 6. 表单与命令生命周期

1. 工资入口必须是专用命令，不能由 `职业工资` 等分类名称自动推断。
2. 收入账户、收入分类、扣款分类、人员、社保账户和标签选择器必须返回稳定 ID 与对象版本。
3. 只写显示文字、标题或可访问性名称时，提交前必须返回字段错误。
4. 币种改变后必须重新过滤可选账户和分类；不兼容的旧选择保留在草稿中并标错，不能静默换绑。
5. 社保人员改变后必须按人员 ID 重新加载社保账户，仍有效的缴费行可保留，被移除的行必须明确提示。
6. 税务计算器取消不改变草稿；确认只把计算结果和输入快照回填到草稿。
7. 保存并继续必须先原子提交当前工资，再创建新草稿；字段保留策略按已校准规则执行。
8. 修改、删除、冲正和恢复必须检查对象版本，并返回影响预览。

## 7. 三端职责

| 能力 | PC | Web | 手机 |
| --- | --- | --- | --- |
| 新增工资收入 | 支持 | 支持 | 摘要后置 |
| 编辑工资组成 | 支持 | 支持 | 不支持 |
| 税务计算器 | 支持 | 支持 | 不支持 |
| 社保缴费组成 | 支持 | 支持 | 只读摘要 |
| 工资列表与详情 | 支持 | 支持 | 摘要 |
| 删除、冲正、恢复 | 支持 | 支持 | 不支持 |
| 旧工资迁移预览 | PC 本地支持 | 不支持 | 不支持 |

手机端第一版只显示工资摘要、同步状态和冲突摘要。手机可保留普通收入草稿，但不得在离线队列中伪造复杂工资组成。

## 8. 同步与冲突

1. 工资头、收入组成、扣款组成、社保缴费组成、税务快照、posting 链接、附件关系和审计摘要作为新系统对象同步。
2. 用户未开启同步时，PC 工资数据只保存在本地 SQLite。
3. 用户显式开启同步后，云端只接收新系统工资对象和对象版本，不接收旧 MoneyHome8 证据。
4. PC/Web 可处理字段级冲突；手机只显示冲突摘要并引导到 PC/Web。
5. 同一工资对象的组成明细冲突必须按稳定 ID 合并，不能用行号或显示文字匹配。
6. 税务计算快照冲突必须显示规则版本、输入摘要和结果差异。

## 9. 隐私与安全

1. 旧 MoneyHome8 工资迁移证据、迁移审计、迁移报告、脱敏摘要、旧路径、旧原始行和自动化诊断只保存在 PC 本地。
2. 云端日志、错误响应、支持包和诊断 ID 不得包含工资明细、个人身份证件、完整本地路径、旧原始行、令牌或密码。
3. Web 和手机不得展示旧工资来源路径或旧程序控件证据。
4. 工资导出必须经过账本权限校验，并按用户选择脱敏人员和敏感备注。
5. 税务计算输入快照不得保存非必要身份证件、银行卡号或账号秘密。

## 10. 错误模型

| 错误码 | 场景 | 处理 |
| --- | --- | --- |
| `payroll_income_component_required` | 缺少有效收入项目 | 阻止提交并定位收入明细 |
| `payroll_account_required` | 缺少实收账户稳定 ID | 阻止提交并定位账户字段 |
| `payroll_category_invalid` | 收入或扣款分类无效 | 阻止提交并刷新候选 |
| `payroll_net_cash_negative` | 实收现金为负 | 阻止提交并展示公式明细 |
| `payroll_social_person_required` | 存在社保缴费但缺少人员 | 阻止提交并定位人员字段 |
| `payroll_social_account_person_mismatch` | 社保账户与人员不匹配 | 阻止提交并刷新社保账户 |
| `payroll_tax_calibration_limited` | 税务公式处于受限校准状态 | 允许保存草稿，阻止标记为正式税务结论 |
| `payroll_version_conflict` | 对象版本冲突 | 进入 PC/Web 冲突解决 |
| `payroll_permission_denied` | 无账本写权限 | 阻止写入并保留草稿 |

## 11. 验收场景

1. 只写入“职业工资”显示文字但没有收入分类稳定 ID 时，提交必须被拒绝。
2. 工资收入、普通扣款、个人社保和公司社保同时存在时，`net_cash` 与实收账户 posting 逐分一致。
3. 公司社保缴费只增加社保账户权益，不进入现金账户。
4. 税务计算器取消不改变草稿；确认后保存税务规则版本、输入快照、舍入规则和结果。
5. 工资提交中任一组成保存失败时，工资头、posting、社保权益、附件和审计全部回滚。
6. Web 下载 PC 同步工资对象后，组成明细、公式版本和税务快照一致。
7. 手机只展示工资摘要和同步状态，不提供复杂编辑入口。
8. 旧工资迁移证据、迁移审计、迁移报告、脱敏摘要、旧路径和旧原始行只保存在 PC 本地。

## 12. 当前无需人工确认

本计划没有引入新的产品取舍；它细化的是已确认的三端架构、工资收入专用命令、稳定 ID、税务快照、社保权益、原子提交、同步冲突和旧迁移证据 PC 本地保存边界。
