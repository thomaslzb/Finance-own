# MoneyHome8 事件命令与数据流目录

本文件把全量 DFM 事件绑定转换为 Rust 应用命令候选。分类用于需求拆分和动态验证排序，不替代真实运行副作用证据。

## 1. 覆盖摘要

- 应用命令候选：`2000` 个
- 高风险写入/删除/导入/同步候选：`502` 个
- 精确命名调用边：`159` 条
- 含代码字符串证据：`436` 个
- 空实现：`8` 个
- 无当前类或真实父类代码归属：`49` 个
- 其中资源型无 VMT 窗体处理器：`48` 个

## 2. Rust 边界分布

| Rust 边界 | 命令数 |
|---|---:|
| `command_handler` | 451 |
| `domain_command_handler` | 16 |
| `domain_service` | 111 |
| `import_pipeline` | 19 |
| `integration_adapter` | 13 |
| `manual_review` | 354 |
| `persistence_service` | 4 |
| `presentation_lifecycle` | 67 |
| `presentation_state` | 848 |
| `query_export_service` | 70 |
| `query_handler` | 47 |

## 3. 按业务域与主意图

| 业务域 | 命令 | 新增 | 修改 | 删除 | 交易 | 查询 | 导入 | 导出 | 同步 | 计算 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| accounts_master_data | 225 | 22 | 28 | 9 | 0 | 19 | 1 | 13 | 1 | 5 |
| auth_sync_external | 26 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| bonds | 49 | 8 | 2 | 1 | 0 | 1 | 0 | 2 | 0 | 10 |
| debts_credit | 156 | 17 | 8 | 2 | 2 | 0 | 2 | 2 | 0 | 8 |
| financial_products | 55 | 11 | 4 | 2 | 0 | 2 | 0 | 2 | 0 | 3 |
| foreign_exchange | 22 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| funds | 128 | 15 | 19 | 3 | 3 | 2 | 0 | 6 | 0 | 16 |
| futures_metals | 129 | 14 | 12 | 6 | 1 | 2 | 0 | 12 | 0 | 13 |
| import_export | 72 | 1 | 10 | 1 | 0 | 4 | 6 | 1 | 0 | 2 |
| insurance_social | 34 | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| investment_shared | 18 | 0 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| major_tangible_assets | 111 | 15 | 9 | 5 | 0 | 1 | 0 | 8 | 0 | 8 |
| margin_financing | 82 | 4 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| planning_budget_goal | 153 | 17 | 33 | 6 | 4 | 0 | 1 | 1 | 0 | 7 |
| reports | 31 | 0 | 3 | 2 | 0 | 1 | 0 | 3 | 0 | 0 |
| securities | 106 | 14 | 14 | 2 | 2 | 1 | 1 | 8 | 0 | 13 |
| shared_infrastructure | 89 | 0 | 5 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| system_shell | 171 | 7 | 11 | 3 | 1 | 1 | 2 | 1 | 7 | 5 |
| tools_longtail | 89 | 3 | 9 | 3 | 1 | 3 | 1 | 1 | 1 | 1 |
| transactions | 254 | 20 | 37 | 8 | 2 | 10 | 5 | 6 | 0 | 8 |

## 4. 高风险命令候选

下表保留命令型事件中最需要动态校准的写入、删除、导入、同步和持久化路径。完整 `2000` 项见 JSON。

| 命令 ID | 页面 | 处理器 | 意图 | 方向 | 置信度 | 实体候选 | 代码状态 | 字符串证据 |
|---|---|---|---|---|---|---|---|---|
| `accounts_master_data.account_dlg_fm.btn_save_click` | AccountDlgFm | `btnSaveClick` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` | 썛 |
| `accounts_master_data.account_manager_fm.act_add_select_account_to_group_execute` | 账户中心 | `actAddSelectAccountToGroupExecute` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` | 请选择要添加到“%s”的账户；-100 |
| `accounts_master_data.account_manager_fm.act_add_theme_execute` | 账户中心 | `actAddThemeExecute` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` | 请选择标签；加入标签 |
| `accounts_master_data.account_manager_fm.act_delete_account_execute` | 账户中心 | `actDeleteAccountExecute` | `delete_data` | `delete` | high | account；account_group；category；currency；person；tag | `current_class` | 账户“；”将被永久删除！；删除操作将移除该账户及其所有相关数据，包括：；相关的收支记录、与其它账户的转账记录、关联的财务计划等。 |
| `accounts_master_data.account_manager_fm.act_delete_account_group_execute` | 账户中心 | `actDeleteAccountGroupExecute` | `delete_data` | `delete` | high | account；account_group；category；currency；person；tag | `current_class` | 账户组“；”将被永久删除！；如果该账户组包含下挂账户，删除后将清除账户组与下挂账户的关联关系，；确定删除此账户组吗？ |
| `accounts_master_data.account_manager_fm.act_edit_account_execute` | 账户中心 | `actEditAccountExecute` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.account_manager_fm.act_edit_account_group_execute` | 账户中心 | `actEditAccountGroupExecute` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.account_manager_fm.btn_new_click` | 账户中心 | `btnNewClick` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.account_manager_fm.btn_new_group_click` | 账户中心 | `btnNewGroupClick` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.account_manager_fm.mmi_add_access_click` | 账户中心 | `mmiAddAccessClick` | `create_data` | `write` | high | account；account_group；attachment；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.account_manager_fm.pm_new_group_click` | 账户中心 | `pmNewGroupClick` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.acct_detail_dlg.lb_online_no_click` | 账户详细资料 | `lbOnlineNoClick` | `sync_external` | `bidirectional_external` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.category_list_fm.act_add_category_execute` | 收支项目 | `actAddCategoryExecute` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.category_list_fm.act_delete_category_execute` | 收支项目 | `actDeleteCategoryExecute` | `delete_data` | `delete` | high | account；account_group；category；currency；person；tag | `current_class` | 子收支项目“；”已被使用，无法删除。；您确定删除“；”吗？ |
| `accounts_master_data.category_list_fm.act_edit_category_execute` | 收支项目 | `actEditCategoryExecute` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.category_list_fm.mi_edit_category_order_click` | 收支项目 | `miEditCategoryOrderClick` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.category_list_fm.mi_import_click` | 收支项目 | `miImportClick` | `import_data` | `external_to_write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.curr_dlg.btn_save_exit_click` | 货币 | `btnSaveExitClick` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` | 保存失败 |
| `accounts_master_data.curr_list_fm.act_edit_execute` | 币种与汇率 | `actEditExecute` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.curr_list_fm.act_rate_add_execute` | 币种与汇率 | `actRateAddExecute` | `create_data` | `write` | high | account；account_group；category；currency；person；quote；tag | `current_class` | 譕맬 |
| `accounts_master_data.curr_list_fm.act_rate_edit_execute` | 币种与汇率 | `actRateEditExecute` | `update_data` | `write` | high | account；account_group；category；currency；person；quote；tag | `current_class` | 譕맬 |
| `accounts_master_data.custom_navigation_acct_dlg_fm.btn_save_click` | 设置[自定义]显示 | `btnSaveClick` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` | UPDATE TBStdAcct SET NavigationOrder=NULL；UPDATE TBStdAcct SET NavigationOrder=%d,NavigationShow=%s WHERE ID=%d |
| `accounts_master_data.edit_category_fm.rz_btn_save_exit_click` | 收支项目 | `RzBtnSaveExitClick` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.edit_category_fm.btn_save_new_click` | 收支项目 | `btnSaveNewClick` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.edt_acct_grp_dlg_fm.btn_save_click` | 修改所属账户组 | `btnSaveClick` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` | 3 |
| `accounts_master_data.life_theme_fm.act_add_execute` | 标签 | `actAddExecute` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.life_theme_fm.act_add_tag_execute` | 标签 | `actAddTagExecute` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` | 请选择记录 |
| `accounts_master_data.life_theme_fm.act_delete_all_execute` | 标签 | `actDeleteAllExecute` | `delete_data` | `delete` | high | account；account_group；category；currency；person；tag | `current_class` | 请选择记录 |
| `accounts_master_data.life_theme_fm.act_delete_execute` | 标签 | `actDeleteExecute` | `delete_data` | `delete` | high | account；account_group；category；currency；person；tag | `current_class` | 您确定删除%s“；”吗？ |
| `accounts_master_data.life_theme_fm.act_delete_tag_execute` | 标签 | `actDeleteTagExecute` | `delete_data` | `delete` | high | account；account_group；category；currency；person；tag | `current_class` | 请选择记录 |
| `accounts_master_data.life_theme_fm.act_modify_execute` | 标签 | `actModifyExecute` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.life_theme_fm.mi_edit_tags_order_click` | 标签 | `miEditTagsOrderClick` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.mw_select_account_drop.btn_new_account_click` | TMWSELECTACCOUNTDROP | `btnNewAccountClick` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.mw_select_category_drop.btn_new_category_click` | TMWSELECTCATEGORYDROP | `btnNewCategoryClick` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.mw_select_tag_drop.btn_new_tag_click` | TMWSELECTTAGDROP | `btnNewTagClick` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.new_acct_wizard_one_card_dlg_fm.btn_new_current_click` | 一卡通 | `btnNewCurrentClick` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.new_acct_wizard_one_card_dlg_fm.btn_new_fixed_deposit_click` | 一卡通 | `btnNewFixedDepositClick` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.person_dlg.btn_save_exit_click` | 人员与机构 | `btnSaveExitClick` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` | 保存失败 |
| `accounts_master_data.person_list_fm.act_add_execute` | 人员与机构 | `actAddExecute` | `create_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `accounts_master_data.person_list_fm.act_edit_execute` | 人员与机构 | `actEditExecute` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` | ID |
| `accounts_master_data.rate_fm.mi_update_click` | 存款利率 | `miUpdateClick` | `update_data` | `write` | high | account；account_group；category；currency；person；tag | `current_class` |  |
| `auth_sync_external.online_get_data_fm.rz_button_update_click` | 更新行情数据 | `RzButtonUpdateClick` | `update_data` | `write` | high | notification；sync_batch；user_identity | `current_class` |  |
| `auth_sync_external.sync_user_data_fm.btn_sync_cancel_click` | 同步 | `btnSyncCancelClick` | `sync_external` | `bidirectional_external` | high | notification；sync_batch；user_identity | `current_class` |  |
| `auth_sync_external.sync_user_data_fm.btn_sync_start_click` | 同步 | `btnSyncStartClick` | `sync_external` | `bidirectional_external` | high | notification；sync_batch；user_identity | `current_class` |  |
| `auth_sync_external.sync_user_data_fm.chk_sync_by_close_book_click` | 同步 | `chkSyncByCloseBookClick` | `sync_external` | `bidirectional_external` | high | ledger；notification；sync_batch；user_identity | `current_class` |  |
| `bonds.nmarket_bond_list_fm.act_add_security_execute` | 债券列表 | `actAddSecurityExecute` | `create_data` | `write` | high | bond；debt；investment_transaction；position；security | `current_class` |  |
| `bonds.nmarket_bond_list_fm.act_delete_security_execute` | 债券列表 | `actDeleteSecurityExecute` | `delete_data` | `delete` | high | bond；debt；investment_transaction；position；security | `current_class` |  |
| `bonds.nmarket_bond_list_fm.act_edit_security_execute` | 债券列表 | `actEditSecurityExecute` | `update_data` | `write` | high | bond；debt；investment_transaction；position；security | `current_class` |  |
| `debts_credit.change_pay_mode_dlg_fm.btn_save_exit_click` | 变更还款方式 | `btnSaveExitClick` | `update_data` | `write` | high | credit_account；debt；repayment；transaction | `current_class` | 3；“%s”必须在最近一次变更日期%s之后；“%s”必须在今天%s之前 |
| `debts_credit.claims_debt_statistic_frame.mi_delete_asset_click` | TCLAIMSDEBTSTATISTICFRAME | `miDeleteAssetClick` | `delete_data` | `delete` | high | credit_account；debt；repayment；transaction | `current_class` |  |
| `debts_credit.credit_card_statistic_frame.mi_import_click` | TCREDITCARDSTATISTICFRAME | `miImportClick` | `import_data` | `external_to_write` | high | credit_account；debt；repayment；transaction | `current_class` |  |
| `debts_credit.credit_card_trans_frame.mi_import_click` | TCREDITCARDTRANSFRAME | `miImportClick` | `import_data` | `external_to_write` | high | credit_account；debt；repayment；transaction | `current_class` |  |
| `debts_credit.debt_investment_pay_object_frame.btn_with_draw_click` | TDEBTINVESTMENTPAYOBJECTFRAME | `btnWithDrawClick` | `transaction_action` | `write` | high | credit_account；debt；repayment；transaction | `current_class` | AcctID |
| `debts_credit.new_blockup_dlg.btn_save_exit_click` | 垫付 | `btnSaveExitClick` | `update_data` | `write` | high | credit_account；debt；repayment；transaction | `current_class` | 썛 |
| `debts_credit.new_blockup_dlg.btn_save_new_click` | 垫付 | `btnSaveNewClick` | `create_data` | `write` | high | credit_account；debt；repayment；transaction | `current_class` |  |
| `debts_credit.new_debt_borrow_dlg_fm.btn_save_exit_click` | 借入、借出 | `btnSaveExitClick` | `update_data` | `write` | high | credit_account；debt；repayment；transaction | `current_class` | 썛 |
| `debts_credit.new_debt_borrow_dlg_fm.btn_save_new_click` | 借入、借出 | `btnSaveNewClick` | `create_data` | `write` | high | credit_account；debt；repayment；transaction | `current_class` |  |
| `debts_credit.payable_advance_dlg_fm.btn_save_exit_click` | 预收、预付 | `btnSaveExitClick` | `update_data` | `write` | high | credit_account；debt；repayment；transaction | `current_class` |  |
| `debts_credit.payable_advance_dlg_fm.btn_save_new_click` | 预收、预付 | `btnSaveNewClick` | `create_data` | `write` | high | credit_account；debt；repayment；transaction | `current_class` |  |
| `debts_credit.prepaid_expenses_dlg_fm.btn_save_exit_click` | 待摊费用 | `btnSaveExitClick` | `update_data` | `write` | high | credit_account；debt；repayment；transaction | `current_class` |  |
| `debts_credit.prepaid_expenses_dlg_fm.btn_save_new_click` | 待摊费用 | `btnSaveNewClick` | `create_data` | `write` | high | credit_account；debt；repayment；transaction | `current_class` |  |
| `debts_credit.repayment_table_frame.btn_add_click` | TREPAYMENTTABLEFRAME | `btnAddClick` | `create_data` | `write` | high | credit_account；debt；repayment；transaction | `current_class` |  |
| `debts_credit.repayment_table_frame.btn_delete_click` | TREPAYMENTTABLEFRAME | `btnDeleteClick` | `delete_data` | `delete` | high | credit_account；debt；repayment；transaction | `current_class` | 借贷款账户需设置至少一个利率 |
| `debts_credit.repayment_table_frame.btn_update_click` | TREPAYMENTTABLEFRAME | `btnUpdateClick` | `update_data` | `write` | high | credit_account；debt；repayment；transaction | `current_class` |  |
| `financial_products.fixed_deposit_statistic_frame.mi_delete_asset_click` | TFIXEDDEPOSITSTATISTICFRAME | `miDeleteAssetClick` | `delete_data` | `delete` | high | financial_product；position；transaction | `current_class` | AcctName；将被永久删除！；删除操作将移除该账户及其所有相关数据，包括：；相关的收支记录，与其它账户的转账记录、关联的财务计划等。 |
| `financial_products.money_list_fm.act_add_security_execute` | 银行理财产品列表 | `actAddSecurityExecute` | `create_data` | `write` | high | financial_product；position；security；transaction | `current_class` |  |
| `financial_products.money_list_fm.act_delete_security_execute` | 银行理财产品列表 | `actDeleteSecurityExecute` | `delete_data` | `delete` | high | financial_product；position；security；transaction | `current_class` |  |
| `financial_products.money_list_fm.act_edit_security_execute` | 银行理财产品列表 | `actEditSecurityExecute` | `update_data` | `write` | high | financial_product；position；security；transaction | `current_class` |  |
| `foreign_exchange.exchange_rate_dlg.btn_save_exit_click` | 外汇汇率 | `btnSaveExitClick` | `update_data` | `write` | high | currency；exchange_rate；fx_transaction | `current_class` | 썛 |
| `foreign_exchange.foreign_statistic_frame.act_add_price_execute` | TFOREIGNSTATISTICFRAME | `ActAddPriceExecute` | `create_data` | `write` | high | currency；exchange_rate；fx_transaction；quote | `current_class` |  |
| `foreign_exchange.foreign_statistic_frame.btn_update_data_click` | TFOREIGNSTATISTICFRAME | `btnUpdateDataClick` | `update_data` | `write` | high | currency；exchange_rate；fx_transaction | `current_class` |  |
| `funds.curr_fund_buy_dlg_fm.btn_update_code_click` | 货币基金申购 | `btnUpdateCodeClick` | `update_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `funds.curr_fund_convert_fm.btn_update_code_click` | 货币基金转换 | `btnUpdateCodeClick` | `update_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `funds.curr_funds_list_fm.act_add_security_execute` | 货币基金列表 | `actAddSecurityExecute` | `create_data` | `write` | high | fund；investment_transaction；position；quote；security | `current_class` |  |
| `funds.curr_funds_list_fm.act_convert_code_execute` | 货币基金列表 | `actConvertCodeExecute` | `transaction_action` | `write` | high | fund；investment_transaction；position；quote | `current_class` | TransObjID |
| `funds.curr_funds_list_fm.act_delete_security_execute` | 货币基金列表 | `actDeleteSecurityExecute` | `delete_data` | `delete` | high | fund；investment_transaction；position；quote；security | `current_class` |  |
| `funds.curr_funds_list_fm.act_edit_security_execute` | 货币基金列表 | `actEditSecurityExecute` | `update_data` | `write` | high | fund；investment_transaction；position；quote；security | `current_class` |  |
| `funds.curr_fund_statistic_frame.btn_update_data_click` | TCURRFUNDSTATISTICFRAME | `btnUpdateDataClick` | `update_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `funds.fund_buy_dlg_fm.btn_update_code_click` | 开放式基金申购 | `btnUpdateCodeClick` | `update_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `funds.fund_convert_dlg_fm.btn_update_code_click` | 开放式基金转换 | `btnUpdateCodeClick` | `update_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `funds.fund_mark_buy_dlg_fm.btn_save_exit_click` | 新基金认购确认 | `btnSaveExitClick` | `update_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` | 썛 |
| `funds.fund_order_buy_dlg_fm.btn_update_code_click` | 新基金认购 | `btnUpdateCodeClick` | `update_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `funds.open_funds_list_fm.act_add_execute` | 开放式基金列表 | `ActAddExecute` | `create_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `funds.open_funds_list_fm.act_add_price_execute` | 开放式基金列表 | `ActAddPriceExecute` | `create_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` | TransObjID；净值 |
| `funds.open_funds_list_fm.act_delete_execute` | 开放式基金列表 | `ActDeleteExecute` | `delete_data` | `delete` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `funds.open_funds_list_fm.act_delete_price_execute` | 开放式基金列表 | `ActDeletePriceExecute` | `delete_data` | `delete` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `funds.open_funds_list_fm.act_modify_execute` | 开放式基金列表 | `ActModifyExecute` | `update_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `funds.open_funds_list_fm.act_modify_price_execute` | 开放式基金列表 | `ActModifyPriceExecute` | `update_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `funds.open_funds_list_fm.act_convert_code_execute` | 开放式基金列表 | `actConvertCodeExecute` | `transaction_action` | `write` | high | fund；investment_transaction；position；quote | `same_name_unique_candidate` |  |
| `funds.open_fund_statistic_frame.act_add_price_execute` | TOPENFUNDSTATISTICFRAME | `ActAddPriceExecute` | `create_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` | ObjID；净值 |
| `funds.open_fund_statistic_frame.btn_update_data_click` | TOPENFUNDSTATISTICFRAME | `btnUpdateDataClick` | `update_data` | `write` | high | fund；investment_transaction；position；quote | `current_class` |  |
| `futures_metals.futures_contract_list_fm.act_add_price_execute` | 期货合约列表 | `ActAddPriceExecute` | `create_data` | `write` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` | TransObjID；价格 |
| `futures_metals.futures_contract_list_fm.act_delete_execute` | 期货合约列表 | `ActDeleteExecute` | `delete_data` | `delete` | high | futures_contract；investment_transaction；metal_position | `current_class` |  |
| `futures_metals.futures_contract_list_fm.act_delete_price_execute` | 期货合约列表 | `ActDeletePriceExecute` | `delete_data` | `delete` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` |  |
| `futures_metals.futures_contract_list_fm.act_modify_price_execute` | 期货合约列表 | `ActModifyPriceExecute` | `update_data` | `write` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` |  |
| `futures_metals.futures_goods_list_fm.act_add_security_execute` | 期货品种列表 | `actAddSecurityExecute` | `create_data` | `write` | high | futures_contract；investment_transaction；metal_position；security | `current_class` |  |
| `futures_metals.futures_goods_list_fm.act_delete_security_execute` | 期货品种列表 | `actDeleteSecurityExecute` | `delete_data` | `delete` | high | futures_contract；investment_transaction；metal_position；security | `current_class` |  |
| `futures_metals.futures_goods_list_fm.act_edit_security_execute` | 期货品种列表 | `actEditSecurityExecute` | `update_data` | `write` | high | futures_contract；investment_transaction；metal_position；security | `current_class` |  |
| `futures_metals.futures_statistic_frame.act_add_price_execute` | TFUTURESSTATISTICFRAME | `ActAddPriceExecute` | `create_data` | `write` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` | 价格；ObjID |
| `futures_metals.futures_statistic_frame.btn_update_data_click` | TFUTURESSTATISTICFRAME | `btnUpdateDataClick` | `update_data` | `write` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` |  |
| `futures_metals.gold_buy_dlg_fm.btn_update_code_click` | 贵金属买入 | `btnUpdateCodeClick` | `update_data` | `write` | high | futures_contract；investment_transaction；metal_position | `current_class` |  |
| `futures_metals.gold_list_fm.act_add_execute` | 贵金属产品列表 | `ActAddExecute` | `create_data` | `write` | high | futures_contract；investment_transaction；metal_position | `current_class` |  |
| `futures_metals.gold_list_fm.act_add_price_execute` | 贵金属产品列表 | `ActAddPriceExecute` | `create_data` | `write` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` | TransObjID；价格 |
| `futures_metals.gold_list_fm.act_convert_code_execute` | 贵金属产品列表 | `ActConvertCodeExecute` | `transaction_action` | `write` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` |  |
| `futures_metals.gold_list_fm.act_delete_execute` | 贵金属产品列表 | `ActDeleteExecute` | `delete_data` | `delete` | high | futures_contract；investment_transaction；metal_position | `current_class` |  |
| `futures_metals.gold_list_fm.act_delete_price_execute` | 贵金属产品列表 | `ActDeletePriceExecute` | `delete_data` | `delete` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` |  |
| `futures_metals.gold_list_fm.act_modify_execute` | 贵金属产品列表 | `ActModifyExecute` | `update_data` | `write` | high | futures_contract；investment_transaction；metal_position | `current_class` |  |
| `futures_metals.gold_list_fm.act_modify_price_execute` | 贵金属产品列表 | `ActModifyPriceExecute` | `update_data` | `write` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` |  |
| `futures_metals.gold_statistic_frame.act_add_price_execute` | TGOLDSTATISTICFRAME | `ActAddPriceExecute` | `create_data` | `write` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` | 价格；ObjID |
| `futures_metals.gold_statistic_frame.btn_update_data_click` | TGOLDSTATISTICFRAME | `btnUpdateDataClick` | `update_data` | `write` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` |  |
| `futures_metals.precious_metals_tdgoods_list_fm.act_add_security_execute` | 贵金属TD品种列表 | `actAddSecurityExecute` | `create_data` | `write` | high | futures_contract；investment_transaction；metal_position；security | `current_class` |  |
| `futures_metals.precious_metals_tdgoods_list_fm.act_delete_security_execute` | 贵金属TD品种列表 | `actDeleteSecurityExecute` | `delete_data` | `delete` | high | futures_contract；investment_transaction；metal_position；security | `current_class` |  |
| `futures_metals.precious_metals_tdgoods_list_fm.act_edit_security_execute` | 贵金属TD品种列表 | `actEditSecurityExecute` | `update_data` | `write` | high | futures_contract；investment_transaction；metal_position；security | `current_class` |  |
| `futures_metals.precious_metals_tdstatistic_frame.act_add_price_execute` | TPRECIOUSMETALSTDSTATISTICFRAME | `ActAddPriceExecute` | `create_data` | `write` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` | 价格；ObjID |
| `futures_metals.precious_metals_tdstatistic_frame.btn_update_data_click` | TPRECIOUSMETALSTDSTATISTICFRAME | `btnUpdateDataClick` | `update_data` | `write` | high | futures_contract；investment_transaction；metal_position；quote | `current_class` |  |
| `import_export.import_category_dlg_fm.btn_save_exit_click` | 替换收支项目 | `btnSaveExitClick` | `update_data` | `write` | high | export_projection；field_mapping；import_batch；raw_row | `current_class` |  |
| `import_export.import_jiao_gedan_dlg_fm.btn_import_click` | 导入股票交割单 | `btnImportClick` | `import_data` | `external_to_write` | high | export_projection；field_mapping；import_batch；raw_row | `same_name_ambiguous_candidate` |  |
| `import_export.import_jiao_gedan_dlg_fm.btn_paste_data_click` | 导入股票交割单 | `btnPasteDataClick` | `import_data` | `external_to_write` | high | export_projection；field_mapping；import_batch；raw_row | `unresolved` |  |
| `import_export.import_jiao_gedan_dlg_fm.btn_program_delete_click` | 导入股票交割单 | `btnProgramDeleteClick` | `delete_data` | `delete` | high | export_projection；field_mapping；import_batch；raw_row | `unresolved` |  |
| `import_export.import_jiao_gedan_dlg_fm.btn_program_save_click` | 导入股票交割单 | `btnProgramSaveClick` | `update_data` | `write` | high | export_projection；field_mapping；import_batch；raw_row | `unresolved` |  |
| `import_export.import_jiao_gedan_dlg_fm.btn_update_click` | 导入股票交割单 | `btnUpdateClick` | `update_data` | `write` | high | export_projection；field_mapping；import_batch；raw_row | `same_name_ambiguous_candidate` |  |
| `import_export.import_jiao_gedan_dlg_fm.mi_update_code_click` | 导入股票交割单 | `miUpdateCodeClick` | `update_data` | `write` | high | export_projection；field_mapping；import_batch；raw_row；security | `unresolved` |  |
| `import_export.import_jiao_gedan_dlg_fm.mi_update_tag_click` | 导入股票交割单 | `miUpdateTagClick` | `update_data` | `write` | high | export_projection；field_mapping；import_batch；raw_row；tag | `unresolved` |  |
| `import_export.import_jiao_gedan_dlg_fm.mi_update_trans_type_click` | 导入股票交割单 | `miUpdateTransTypeClick` | `update_data` | `write` | high | export_projection；field_mapping；import_batch；raw_row；transaction | `unresolved` |  |
| `import_export.import_preview_fm.btn_import_click` | 导入预览 | `btnImportClick` | `import_data` | `external_to_write` | high | export_projection；field_mapping；import_batch；raw_row | `current_class` |  |
| `import_export.import_select_dlg_fm.btn_import_click` | 导入数据 | `btnImportClick` | `import_data` | `external_to_write` | high | export_projection；field_mapping；import_batch；raw_row | `current_class` |  |
| `import_export.import_select_dlg_fm.btn_import_from_clipboard_click` | 导入数据 | `btnImportFromClipboardClick` | `import_data` | `external_to_write` | high | export_projection；field_mapping；import_batch；raw_row | `current_class` | .html；.csv；._clip |
| `import_export.import_theme_dlg_fm.btn_save_exit_click` | 主题数据设置 | `btnSaveExitClick` | `update_data` | `write` | high | export_projection；field_mapping；import_batch；raw_row | `current_class` |  |
| `insurance_social.insure_cash_value_edit_dlg_fm.btn_save_click` | 保险现金价值 | `btnSaveClick` | `update_data` | `write` | high | insurance_policy；social_security_account；transaction | `current_class` | 请输入正确的日期 |
| `insurance_social.insure_cash_value_frame.btn_add_click` | TINSURECASHVALUEFRAME | `btnAddClick` | `create_data` | `write` | high | insurance_policy；social_security_account；transaction | `current_class` |  |
| `insurance_social.insure_cash_value_frame.btn_delete_click` | TINSURECASHVALUEFRAME | `btnDeleteClick` | `delete_data` | `delete` | high | insurance_policy；social_security_account；transaction | `current_class` | PriceDate；删除失败 |
| `insurance_social.insure_cash_value_frame.btn_update_click` | TINSURECASHVALUEFRAME | `btnUpdateClick` | `update_data` | `write` | high | insurance_policy；social_security_account；transaction | `current_class` | PriceDate |
| `insurance_social.insure_trans_frame.mi_modify_plan_click` | TINSURETRANSFRAME | `miModifyPlanClick` | `update_data` | `write` | high | financial_plan；insurance_policy；social_security_account；transaction | `current_class` |  |
| `insurance_social.social_security_statistic_frame.mi_delete_acct_click` | TSOCIALSECURITYSTATISTICFRAME | `miDeleteAcctClick` | `delete_data` | `delete` | high | account；insurance_policy；social_security_account；transaction | `current_class` | 将被永久删除！；删除操作将永久移除该账户及其所有相关数据，包括：；相关的收支接记录，与其它账户的转账记录、关联的财务计划等。；确定删除此账户吗？ |
| `investment_shared.investment_list_fm.btn_update_data_click` | 投资一览 | `btnUpdateDataClick` | `update_data` | `write` | high | fee_rule；investment_object；position；quote | `current_class` |  |
| `major_tangible_assets.asset_buy_fm.btn_new_debt_click` | 重大资产买入 | `btnNewDebtClick` | `create_data` | `write` | high | debt；tangible_asset；transaction；valuation | `current_class` |  |
| `major_tangible_assets.asset_buy_fm.btn_save_click` | 重大资产买入 | `btnSaveClick` | `update_data` | `write` | high | tangible_asset；transaction；valuation | `current_class` | 썛 |
| `major_tangible_assets.asset_encash_dlg_fm.btn_new_debt_click` | 重大资产卖出 | `btnNewDebtClick` | `create_data` | `write` | high | debt；tangible_asset；transaction；valuation | `current_class` |  |
| `major_tangible_assets.asset_invest_dlg_fm.btn_new_debt_click` | 追加投资 | `btnNewDebtClick` | `create_data` | `write` | high | debt；tangible_asset；transaction；valuation | `current_class` |  |
| `major_tangible_assets.asset_price_fm.act_add_execute` | 重大资产价格 | `actAddExecute` | `create_data` | `write` | high | quote；tangible_asset；transaction；valuation | `current_class` | 价格 |
| `major_tangible_assets.asset_price_fm.act_edit_execute` | 重大资产价格 | `actEditExecute` | `update_data` | `write` | high | quote；tangible_asset；transaction；valuation | `current_class` | AssetObjID；PriceDate；价格；AssetName |
| `major_tangible_assets.assets_statistic_frame.mi_delete_asset_click` | TASSETSSTATISTICFRAME | `miDeleteAssetClick` | `delete_data` | `delete` | high | tangible_asset；transaction；valuation | `current_class` | AcctID；ObjID；该资产将被永久删除！ 删除操作将移除该资产及其所有相关数据，包括： 相关的收支记录，与其它账户的转账记录、关联的财务计划等。 确定删除此资产吗？ |
| `major_tangible_assets.assets_value_management_frame.btn_add_click` | TASSETSVALUEMANAGEMENTFRAME | `btnAddClick` | `create_data` | `write` | high | tangible_asset；transaction；valuation | `current_class` | 市值 |
| `major_tangible_assets.assets_value_management_frame.btn_delete_click` | TASSETSVALUEMANAGEMENTFRAME | `btnDeleteClick` | `delete_data` | `delete` | high | tangible_asset；transaction；valuation | `current_class` | PriceDate |
| `major_tangible_assets.assets_value_management_frame.btn_update_click` | TASSETSVALUEMANAGEMENTFRAME | `btnUpdateClick` | `update_data` | `write` | high | tangible_asset；transaction；valuation | `current_class` | PriceDate；市值 |
| `major_tangible_assets.edit_asset_buy_dlg_fm.btn_new_debt_click` | 重大资产买入 | `btnNewDebtClick` | `create_data` | `write` | high | debt；tangible_asset；transaction；valuation | `current_class` |  |
| `major_tangible_assets.prac_dlg.btn_save_exit_click` | 家居物品 | `btnSaveExitClick` | `update_data` | `write` | high | tangible_asset；transaction；valuation | `current_class` | 保存失败 |
| `major_tangible_assets.prac_dlg.btn_save_new_click` | 家居物品 | `btnSaveNewClick` | `create_data` | `write` | high | tangible_asset；transaction；valuation | `current_class` | 保存失败 |
| `major_tangible_assets.prac_list_fm.act_add_execute` | 家居物品资料和价格 | `actAddExecute` | `create_data` | `write` | high | tangible_asset；transaction；valuation | `current_class` |  |
| `major_tangible_assets.prac_list_fm.act_add_group_execute` | 家居物品资料和价格 | `actAddGroupExecute` | `create_data` | `write` | high | category；tangible_asset；transaction；valuation | `current_class` |  |
| `major_tangible_assets.prac_list_fm.act_add_price_execute` | 家居物品资料和价格 | `actAddPriceExecute` | `create_data` | `write` | high | quote；tangible_asset；transaction；valuation | `current_class` | 譕㏬；价格 |
| `major_tangible_assets.prac_list_fm.act_delete_price_execute` | 家居物品资料和价格 | `actDeletePriceExecute` | `delete_data` | `delete` | high | quote；tangible_asset；transaction；valuation | `current_class` | 譕㏬；您确定删除此物品的价格吗？；TransObjID；PriceDate |
| `major_tangible_assets.prac_list_fm.act_edit_execute` | 家居物品资料和价格 | `actEditExecute` | `update_data` | `write` | high | tangible_asset；transaction；valuation | `current_class` |  |
| `major_tangible_assets.prac_list_fm.act_edit_group_execute` | 家居物品资料和价格 | `actEditGroupExecute` | `update_data` | `write` | high | category；tangible_asset；transaction；valuation | `current_class` |  |
| `major_tangible_assets.prac_list_fm.act_edit_price_execute` | 家居物品资料和价格 | `actEditPriceExecute` | `update_data` | `write` | high | quote；tangible_asset；transaction；valuation | `current_class` | 譕㏬；TransObjID；PriceDate；价格 |
| `major_tangible_assets.prac_type_dlg.btn_save_exit_click` | 家居物品分类 | `btnSaveExitClick` | `update_data` | `write` | high | tangible_asset；transaction；valuation | `current_class` | 保存失败 |
| `margin_financing.batch_also_coupons_directly_dlg_fm.btn_save_exit_click` | 批量直接还券 | `btnSaveExitClick` | `update_data` | `write` | high | financing_transaction；margin_account；position | `current_class` | 3；,；保存失败 |
| `margin_financing.batch_direct_payments_dlg_fm.btn_save_exit_click` | 批量直接还款 | `btnSaveExitClick` | `update_data` | `write` | high | financing_transaction；margin_account；position | `current_class` | 3；,；保存失败 |
| `margin_financing.edit_margin_contract_dlg_fm.btn_update_code_click` | 编辑融资融券 | `btnUpdateCodeClick` | `update_data` | `write` | high | financing_transaction；margin_account；position | `current_class` |  |
| `margin_financing.financing_bid_dlg_fm.btn_update_code_click` | 融资买入 | `btnUpdateCodeClick` | `update_data` | `write` | high | financing_transaction；margin_account；position | `current_class` |  |
| `margin_financing.margin_statistic_frame.act_add_price_execute` | TMARGINSTATISTICFRAME | `ActAddPriceExecute` | `create_data` | `write` | high | financing_transaction；margin_account；position；quote；security | `current_class` | 价格；ObjID |
| `margin_financing.margin_statistic_frame.btn_update_data_click` | TMARGINSTATISTICFRAME | `btnUpdateDataClick` | `update_data` | `write` | high | financing_transaction；margin_account；position | `current_class` |  |
| `planning_budget_goal.acct_bala_remind_dlg.btn_save_new_click` | 账户余额提醒 | `btnSaveNewClick` | `create_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` | 孞 |
| `planning_budget_goal.budget_list_fm.btn_new_click` | 预算 | `btnNewClick` | `create_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.budget_list_fm.btn_update_click` | 预算 | `btnUpdateClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.budget_list_fm.mi_delete_budget_click` | 预算 | `miDeleteBudgetClick` | `delete_data` | `delete` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.budget_list_fm.mi_delete_click` | 预算 | `miDeleteClick` | `delete_data` | `delete` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.budget_list_fm.mi_edit_budget_amount_click` | 预算 | `miEditBudgetAmountClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.budget_list_fm.mi_edit_budget_category_click` | 预算 | `miEditBudgetCategoryClick` | `update_data` | `write` | high | budget；category；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.budget_list_fm.mi_edit_budget_click` | 预算 | `miEditBudgetClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.budget_list_fm.mi_modify_click` | 预算 | `miModifyClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.budget_list_fm.mw_adjust_year_click` | 预算 | `mwAdjustYearClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.buy_fund_plan_dlg_fm.btn_update_code_click` | 基金定投计划 | `btnUpdateCodeClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；fund；reminder | `current_class` |  |
| `planning_budget_goal.create_budget_dlg_fm.btn_save_click` | 预算 | `btnSaveClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` | 3 |
| `planning_budget_goal.credit_remind_dlg.btn_save_new_click` | 信用卡透支额提醒 | `btnSaveNewClick` | `create_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` | 孞 |
| `planning_budget_goal.edit_budget_amount_dlg_fm.btn_import_amount_click` | 预算金额设置 | `btnImportAmountClick` | `import_data` | `external_to_write` | high | budget；financial_goal；financial_plan；reminder | `current_class` | ID；total；c%d%.2d |
| `planning_budget_goal.edit_budget_amount_dlg_fm.btn_save_click` | 预算金额设置 | `btnSaveClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.edit_budget_amount_dlg_fm.mw_adjust_year_click` | 预算金额设置 | `mwAdjustYearClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.edit_budget_category_dlg_fm.btn_save_click` | 选择预算收支项目 | `btnSaveClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.financial_diagnosis_fm.btn_return_click` | 财务诊断 | `btnReturnClick` | `transaction_action` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.financial_diagnosis_fm.mi_fixed_deposit_investment_asset_click` | 财务诊断 | `miFixedDeposit_InvestmentAssetClick` | `transaction_action` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.financial_diagnosis_fm.mi_fixed_deposit_liquid_asset_click` | 财务诊断 | `miFixedDeposit_LiquidAssetClick` | `transaction_action` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.financial_planning_center_fm.btn_clear_data_click` | 财务规划 | `btnClearDataClick` | `delete_data` | `delete` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.goal_center_fm.btn_add_click` | 财务目标 | `BtnAddClick` | `create_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.goal_center_fm.mi_delete_click` | 财务目标 | `miDeleteClick` | `delete_data` | `delete` | high | budget；financial_goal；financial_plan；reminder | `current_class` | 您确定删除财务目标“；”吗？ |
| `planning_budget_goal.goal_center_fm.mi_modify_click` | 财务目标 | `miModifyClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.goal_save_fm.btn_save_click` | 财务目标 | `btnSaveClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` | 썛 |
| `planning_budget_goal.limit_remind_dlg.mi_delete_click` | 限额提醒 | `miDeleteClick` | `delete_data` | `delete` | high | budget；financial_goal；financial_plan；reminder | `current_class` | 您确定删除该提醒吗？ |
| `planning_budget_goal.limit_remind_dlg.mi_modify_click` | 限额提醒 | `miModifyClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.open_fund_remind_dlg.btn_save_new_click` | 开放式基金价格提醒 | `btnSaveNewClick` | `create_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` | 孞 |
| `planning_budget_goal.open_fund_remind_dlg.btn_update_code_click` | 开放式基金价格提醒 | `btnUpdateCodeClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；fund；reminder | `current_class` |  |
| `planning_budget_goal.plan_insure_pay_fee_dlg_fm.btn_save_exit_click` | 缴费计划 | `btnSaveExitClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` | 保存失败 |
| `planning_budget_goal.plan_list_dlg.act_edit_execute` | 财务计划和提醒 | `actEditExecute` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `planning_budget_goal.security_remind_dlg.btn_save_new_click` | 证券市价提醒 | `btnSaveNewClick` | `create_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` | 孞 |
| `planning_budget_goal.security_remind_dlg.btn_update_code_click` | 证券市价提醒 | `btnUpdateCodeClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder；security | `current_class` |  |
| `planning_budget_goal.select_repetition_frequency_dlg_fm.btn_save_click` | SelectRepetitionFrequencyDlgFm | `btnSaveClick` | `update_data` | `write` | high | budget；financial_goal；financial_plan；reminder | `current_class` |  |
| `reports.report_fm.mi_delete_click` | ReportFm | `miDeleteClick` | `delete_data` | `delete` | high | report_filter；report_projection；report_query | `current_class` |  |
| `reports.report_fm.mi_modify_click` | ReportFm | `miModifyClick` | `update_data` | `write` | high | report_filter；report_projection；report_query | `current_class` |  |
| `reports.report_fm.mi_rpt_delete_click` | ReportFm | `miRptDeleteClick` | `delete_data` | `delete` | high | report；report_filter；report_projection；report_query | `current_class` |  |
| `reports.report_fm.mi_rpt_save_click` | ReportFm | `miRptSaveClick` | `update_data` | `write` | high | report；report_filter；report_projection；report_query | `current_class` | 报表名称；保存自定义报表 |
| `securities.security_list_fm.act_add_execute` | 证券资料 | `ActAddExecute` | `create_data` | `write` | high | investment_transaction；position；quote；security | `current_class` | 譕맬 |
| `securities.security_list_fm.act_add_price_execute` | 证券资料 | `ActAddPriceExecute` | `create_data` | `write` | high | investment_transaction；position；quote；security | `current_class` | TransObjID；价格 |
| `securities.security_list_fm.act_convert_code_execute` | 证券资料 | `ActConvertCodeExecute` | `transaction_action` | `write` | high | investment_transaction；position；quote；security | `current_class` | 譕맬；TransObjID |
| `securities.security_list_fm.act_delete_execute` | 证券资料 | `ActDeleteExecute` | `delete_data` | `delete` | high | investment_transaction；position；quote；security | `current_class` | 譕맬 |
| `securities.security_list_fm.act_delete_price_execute` | 证券资料 | `ActDeletePriceExecute` | `delete_data` | `delete` | high | investment_transaction；position；quote；security | `current_class` |  |
| `securities.security_list_fm.act_modify_execute` | 证券资料 | `ActModifyExecute` | `update_data` | `write` | high | investment_transaction；position；quote；security | `current_class` |  |
| `securities.security_list_fm.act_modify_price_execute` | 证券资料 | `ActModifyPriceExecute` | `update_data` | `write` | high | investment_transaction；position；quote；security | `current_class` |  |
| `securities.security_statistic_frame.act_add_price_execute` | TSECURITYSTATISTICFRAME | `ActAddPriceExecute` | `create_data` | `write` | high | investment_transaction；position；quote；security | `current_class` | ObjID；价格 |
| `securities.security_statistic_frame.btn_update_data_click` | TSECURITYSTATISTICFRAME | `btnUpdateDataClick` | `update_data` | `write` | high | investment_transaction；position；quote；security | `current_class` |  |
| `securities.select_securities_code_dlg_fm.btn_update_code_click` | 选择证券 | `btnUpdateCodeClick` | `update_data` | `write` | high | investment_transaction；position；quote；security | `current_class` |  |
| `securities.stock_buy_dlg_fm.btn_update_code_click` | 证券买入 | `btnUpdateCodeClick` | `update_data` | `write` | high | investment_transaction；position；quote；security | `current_class` |  |
| `securities.stock_mark_buy_dlg_fm.btn_save_exit_click` | 中签确认 | `btnSaveExitClick` | `update_data` | `write` | high | investment_transaction；position；quote；security | `current_class` | 썛 |
| `securities.stock_order_buy_dlg_fm.btn_update_code_click` | 新股申购 | `btnUpdateCodeClick` | `update_data` | `write` | high | investment_transaction；position；quote；security | `current_class` |  |
| `shared_infrastructure.statistic_frame.act_adjust_bala_execute` | TSTATISTICFRAME | `ActAdjustBalaExecute` | `update_data` | `write` | high | application_setting；presentation_state | `current_class` |  |
| `shared_infrastructure.statistic_frame.act_adjust_static_execute` | TSTATISTICFRAME | `ActAdjustStaticExecute` | `update_data` | `write` | high | application_setting；presentation_state | `current_class` |  |
| `system_shell.main_form.btn_add_acct_click` | MainForm | `btnAddAcctClick` | `create_data` | `write` | high | account；application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.main_form.btn_add_trans_click` | MainForm | `btnAddTransClick` | `create_data` | `write` | high | application_setting；backup_snapshot；ledger；transaction | `current_class` |  |
| `system_shell.main_form.btn_sync_click` | MainForm | `btnSyncClick` | `sync_external` | `bidirectional_external` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.main_form.mi_delete_sync_user_password_click` | MainForm | `miDeleteSyncUserPasswordClick` | `sync_external` | `bidirectional_external` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.main_form.mi_modify_sync_user_password_click` | MainForm | `miModifySyncUserPasswordClick` | `sync_external` | `bidirectional_external` | high | application_setting；backup_snapshot；ledger | `current_class` | http://o.imoney.com.cn/Settings/Password.aspx |
| `system_shell.main_form.mmi_backup_click` | MainForm | `mmiBackupClick` | `backup_restore` | `snapshot_or_replace` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.main_form.mmi_import_click` | MainForm | `mmiImportClick` | `import_data` | `external_to_write` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.main_form.mmi_import_jgdclick` | MainForm | `mmiImportJGDClick` | `import_data` | `external_to_write` | high | application_setting；backup_snapshot；ledger；security | `current_class` |  |
| `system_shell.main_form.mmi_mhonline_urlclick` | MainForm | `mmiMHOnlineURLClick` | `sync_external` | `bidirectional_external` | high | application_setting；backup_snapshot；ledger | `current_class` | http://o.imoney.com.cn/?utm_source=Moneywise_View&utm_medium=MH8&utm_campaign=MH8_OnlineIndex_ |
| `system_shell.main_form.mmi_open_new_click` | MainForm | `mmiOpen_NewClick` | `create_data` | `write` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.main_form.mmi_remote_notification_setting_click` | MainForm | `mmiRemoteNotificationSettingClick` | `sync_external` | `bidirectional_external` | high | application_setting；backup_snapshot；ledger；reminder | `current_class` |  |
| `system_shell.main_form.mmi_restore_click` | MainForm | `mmiRestoreClick` | `backup_restore` | `snapshot_or_replace` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.main_form.mmi_soft_update_click` | MainForm | `mmiSoftUpdateClick` | `update_data` | `write` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.main_form.mmi_soft_ware_urlclick` | MainForm | `mmiSoftWareURLClick` | `sync_external` | `bidirectional_external` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.main_form.mmi_sync_click` | MainForm | `mmiSyncClick` | `sync_external` | `bidirectional_external` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.main_form.mmi_update_rate_click` | MainForm | `mmiUpdateRateClick` | `update_data` | `write` | high | application_setting；backup_snapshot；ledger；quote | `current_class` |  |
| `system_shell.password_dialog.add_button_click` | Enter password | `AddButtonClick` | `create_data` | `write` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.password_dialog.remove_all_button_click` | Enter password | `RemoveAllButtonClick` | `delete_data` | `delete` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.password_dialog.remove_button_click` | Enter password | `RemoveButtonClick` | `delete_data` | `delete` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.register_form.btn_first_use_buy_click` | 软件联网注册 | `btnFirstUse_BuyClick` | `transaction_action` | `write` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `system_shell.register_form.btn_offline_reg_save_user_info_click` | 软件联网注册 | `btnOfflineReg_SaveUserInfoClick` | `update_data` | `write` | high | application_setting；backup_snapshot；ledger | `current_class` | 保存用户信息；*.cfg；.cfg；用户信息.cfg |
| `system_shell.shortcut_manage_dlg_fm.btn_new_short_cut_click` | 快捷键设置 | `btnNewShortCutClick` | `create_data` | `write` | high | application_setting；backup_snapshot；ledger | `current_class` | 请选择菜单项；请输入快捷键；Ctrl；Shift |
| `system_shell.shortcut_manage_dlg_fm.btn_save_exit_click` | 快捷键设置 | `btnSaveExitClick` | `update_data` | `write` | high | application_setting；backup_snapshot；ledger | `current_class` | ShortCut |
| `system_shell.shortcut_manage_dlg_fm.mi_delete_click` | 快捷键设置 | `miDeleteClick` | `delete_data` | `delete` | high | application_setting；backup_snapshot；ledger | `current_class` |  |
| `tools_longtail.accessories_dlg.btn_add_click` | 添加删除附件 | `btnAddClick` | `create_data` | `write` | high | tool_input；tool_result | `current_class` | ⸪*譕 |
| `tools_longtail.accessories_dlg.btn_delete_click` | 添加删除附件 | `btnDeleteClick` | `delete_data` | `delete` | high | tool_input；tool_result | `current_class` | 您确定删除选中的附件吗？ |
| `tools_longtail.diary_dlg_fm.rz_btn_save_click` | 日记 | `RzBtnSaveClick` | `update_data` | `write` | high | tool_input；tool_result | `current_class` | 3；请输入正确的日期 |
| `tools_longtail.diary_unt_fm.act_add_execute` | 日记 | `ActAddExecute` | `create_data` | `write` | high | tool_input；tool_result | `current_class` |  |
| `tools_longtail.diary_unt_fm.act_delete_execute` | 日记 | `ActDeleteExecute` | `delete_data` | `delete` | high | tool_input；tool_result | `current_class` | 您确定删除该日记吗？ |
| `tools_longtail.diary_unt_fm.act_modify_execute` | 日记 | `ActModifyExecute` | `update_data` | `write` | high | tool_input；tool_result | `current_class` |  |
| `tools_longtail.manage_bill_date_dlg_fm.btn_delete_click` | 账单日管理 | `btnDeleteClick` | `delete_data` | `delete` | high | tool_input；tool_result | `current_class` |  |
| `tools_longtail.manage_bill_date_dlg_fm.btn_modify_click` | 账单日管理 | `btnModifyClick` | `update_data` | `write` | high | tool_input；tool_result | `current_class` |  |
| `tools_longtail.modify_bill_date_dlg_fm.btn_save_exit_click` | 设置账单日 | `btnSaveExitClick` | `update_data` | `write` | high | tool_input；tool_result | `current_class` |  |
| `tools_longtail.soft_index_center_form.btn_new_budget_click` | 概况 | `btnNewBudgetClick` | `create_data` | `write` | high | budget；tool_input；tool_result | `current_class` |  |
| `tools_longtail.soft_index_center_form.btn_update_price_click` | 概况 | `btnUpdatePriceClick` | `update_data` | `write` | high | quote；tool_input；tool_result | `current_class` |  |

## 5. 精确命名调用边

调用边只在反汇编直接调用目标 RVA 与 published 方法或已命名例程入口完全相等时记录。

| 来源 | 处理器 | 目标 | 目标 RVA |
|---|---|---|---:|
| `TAccountFeeSetFm` | `btnOkClick` | `VclFormCloseThunk` | `0x8B60` |
| `TAdvanceTransDlgFm` | `selPersonCloseUp` | `TAdvanceTransDlgFm.edKindCloseUp` | `0x4DA188` |
| `TAIPanelDlg` | `WebBrowserDocumentReady` | `AIExecuteJavaScript` | `0x3DD7E4` |
| `TAIPanelDlg` | `WebBrowserDocumentReady` | `AIPreparePageContent` | `0x3DE020` |
| `TAIPanelDlg` | `WebBrowserDocumentReady` | `AISelectEndpoint` | `0x3DE088` |
| `TAlipayViewFrame` | `GridAdditionCheckBoxClick` | `TAlipayViewFrame.GridAdditionClickCell` | `0x346D24` |
| `TBatchAlsoCouponsDirectlyDlgFm` | `tlContractKeyDown` | `TBatchAlsoCouponsDirectlyDlgFm.tlContractKeyPress` | `0x5D23E4` |
| `TBatchDirectPaymentsDlgFm` | `tlContractKeyDown` | `TBatchDirectPaymentsDlgFm.tlContractKeyPress` | `0x5D0F60` |
| `TBuyFundPlanDlgFm` | `btnUpdateCodeClick` | `TBuyFundPlanDlgFm.SelFundAccountCloseUp` | `0x2BA9BC` |
| `TCalcuFm` | `FormKeyDown` | `VclFormCloseThunk` | `0x8B60` |
| `TCalcuFm` | `dxCalculatorError` | `VclFormCloseThunk` | `0x8B60` |
| `TCalcuFm` | `dxCalculatorResult` | `VclFormCloseThunk` | `0x8B60` |
| `TCardViewFrame` | `GridAdditionCheckBoxClick` | `TCardViewFrame.GridAdditionClickCell` | `0x342A0C` |
| `TChildForm` | `sbCloseChildClick` | `VclFormCloseThunk` | `0x8B60` |
| `TCollateralInDlgFm` | `selMarginAcctCloseUp` | `TCollateralInDlgFm.selStockAcctCloseUp` | `0x4F4228` |
| `TConsoleFm` | `NetworkWebBrowserDocumentReady` | `ConsoleExecuteScript` | `0x45ADC0` |
| `TConsoleFm` | `SQLWebBrowserDocumentReady` | `ConsoleExecuteScript` | `0x45ADC0` |
| `TConsoleFm` | `TimerTimer` | `ConsoleExecuteScript` | `0x45ADC0` |
| `TConsoleFm` | `WebBrowserAlertBox` | `ConsoleAppendMessage` | `0x45AD54` |
| `TConsoleFm` | `WebBrowserConsoleMessage` | `ConsoleAppendMessage` | `0x45AD54` |
| `TConsoleFm` | `WebBrowserDocumentReady` | `ConsoleFormatAndExecuteScript` | `0x45AE00` |
| `TConsoleFm` | `WebBrowserDocumentReady` | `ConsolePostDocumentInitialization` | `0x45B1AC` |
| `TConsoleFm` | `WebBrowserDocumentReady` | `ConsoleAppendHistoryEntry` | `0x45A818` |
| `TCostDetailsDlgFm` | `btnOkClick` | `VclFormCloseThunk` | `0x8B60` |
| `TCouponsAlsoBuyCouponsDlgFm` | `SelContractCloseUp` | `TCouponsAlsoBuyCouponsDlgFm.selCodeCloseUp` | `0x4ECF94` |
| `TCouponsAlsoBuyCouponsDlgFm` | `edFiscalExit` | `TCouponsAlsoBuyCouponsDlgFm.edFiscalFeeChange` | `0x4EC56C` |
| `TCouponsAlsoBuyCouponsDlgFm` | `edFiscalFeeChange` | `TCouponsAlsoBuyCouponsDlgFm.edFeeChange` | `0x4EC464` |
| `TCouponsAlsoBuyCouponsDlgFm` | `edPriceExit` | `TCouponsAlsoBuyCouponsDlgFm.edFiscalFeeChange` | `0x4EC56C` |
| `TCouponsAlsoBuyCouponsDlgFm` | `selInvestAcctCloseUp` | `TCouponsAlsoBuyCouponsDlgFm.edPriceExit` | `0x4EC5F0` |
| `TCreateBudgetDlgFm` | `btnSaveClick` | `VclFormHideThunk` | `0x8B70` |
| `TCurrDepositsViewFrame` | `GridAdditionCheckBoxClick` | `TCurrDepositsViewFrame.GridAdditionClickCell` | `0x341CA4` |
| `TCurrExchangeDlgFm` | `edRateExit` | `TCurrExchangeDlgFm.edAmountOutExit` | `0x4A51BC` |
| `TCurrFundBuyDlgFm` | `btnUpdateCodeClick` | `TCurrFundBuyDlgFm.SelInAcctCloseUp` | `0x4D3E0C` |
| `TCurrFundConvertFm` | `btnUpdateCodeClick` | `TCurrFundConvertFm.selAcctCloseUp` | `0x5C9010` |
| `TCurrListFm` | `DBGRIDDblClick` | `TCurrListFm.actEditExecute` | `0x315DB8` |
| `TDebtInvestmentBadTransDlgFm` | `selInvestmentAcctCloseUp` | `TDebtInvestmentBadTransDlgFm.selDebtInvestmentObjCloseUp` | `0x4FC7B4` |
| `TDebtInvestmentLoanDlgFm` | `edtAmountExit` | `TDebtInvestmentLoanDlgFm.edTransDateChange` | `0x4F6504` |
| `TDebtInvestmentLoanDlgFm` | `edtPeriodExit` | `TDebtInvestmentLoanDlgFm.edTransDateChange` | `0x4F6504` |
| `TDebtInvestmentLoanDlgFm` | `edtRateExit` | `TDebtInvestmentLoanDlgFm.edtAmountExit` | `0x4F5D70` |
| `TDebtInvestmentLoanDlgFm` | `edtTakebackDateChange` | `TDebtInvestmentLoanDlgFm.edtPeriodExit` | `0x4F6308` |
| `TDebtInvestmentPayObjectFrame` | `BrowseGridDblClick` | `TDebtInvestmentPayObjectFrame.btnWithDrawClick` | `0x439958` |
| `TDebtInvestmentSellTransDlgFm` | `selInvestmentAcctCloseUp` | `TDebtInvestmentSellTransDlgFm.selDebtInvestmentObjCloseUp` | `0x4F8F48` |
| `TDebtInvestmentStatisticFrame` | `BrowseGridDblClick` | `TDebtInvestmentStatisticFrame.btnPayTableClick` | `0x437030` |
| `TDebtInvestmentWithdrawTransDlgFm` | `selDebtInvestmentObjCloseUp` | `TDebtInvestmentWithdrawTransDlgFm.edtCashSumChange` | `0x4F815C` |
| `TDebtInvestmentWithdrawTransDlgFm` | `selInvestmentAcctCloseUp` | `TDebtInvestmentWithdrawTransDlgFm.selDebtInvestmentObjCloseUp` | `0x4F8290` |
| `TDropFM` | `FormDeactivate` | `VclFormHideThunk` | `0x8B70` |
| `TDropFM` | `FormDeactivate` | `VclFormCloseThunk` | `0x8B60` |
| `TDropFM` | `FormKeyPress` | `TDropFM.FormDeactivate` | `0x1E6220` |
| `TDropFM` | `FormShortCut` | `TDropFM.FormDeactivate` | `0x1E6220` |
| `TDropFM` | `dxTreeListKeyPress` | `TDropFM.FormDeactivate` | `0x1E6220` |
| `TDropFM` | `dxTreeListMouseUp` | `TDropFM.FormDeactivate` | `0x1E6220` |
| `TEditCategoryFm` | `RzBtnSaveExitClick` | `VclFormCloseThunk` | `0x8B60` |
| `TEditCurrFundFm` | `RzButtonOKClick` | `VclFormCloseThunk` | `0x8B60` |
| `TEditFuturesGoodsFm` | `RzButtonOKClick` | `VclFormCloseThunk` | `0x8B60` |
| `TEditGoldFm` | `RzButtonOKClick` | `VclFormCloseThunk` | `0x8B60` |
| `TEditNMarketBondFm` | `RzButtonOKClick` | `VclFormCloseThunk` | `0x8B60` |
| `TEditOpenFundFm` | `RzButtonOKClick` | `VclFormCloseThunk` | `0x8B60` |
| `TEditPreciousMetalsTDGoodsFm` | `RzButtonOKClick` | `VclFormCloseThunk` | `0x8B60` |
| `TEditSecurityFm` | `RzButtonOKClick` | `VclFormCloseThunk` | `0x8B60` |
| `TExpenseDlgFm` | `AcctTreeListKeyDown` | `TExpenseDlgFm.AcctTreeListKeyPress` | `0x4DC79C` |
| `TFinancingBidDlgFm` | `btnUpdateCodeClick` | `TFinancingBidDlgFm.selInvestAcctCloseUp` | `0x4E8FA0` |
| `TFinancingBidDlgFm` | `edCommPercentExit` | `TFinancingBidDlgFm.edFiscalFeeChange` | `0x4E8164` |
| `TFinancingBidDlgFm` | `edFiscalExit` | `TFinancingBidDlgFm.edFiscalFeeChange` | `0x4E8164` |
| `TFinancingBidDlgFm` | `edFiscalFeeChange` | `TFinancingBidDlgFm.edFeeChange` | `0x4E805C` |
| `TFinancingBidDlgFm` | `edPriceExit` | `TFinancingBidDlgFm.edFiscalFeeChange` | `0x4E8164` |
| `TFinancingBidDlgFm` | `selInvestAcctCloseUp` | `TFinancingBidDlgFm.edPriceExit` | `0x4E81E8` |
| `TFixDepositsViewFrame` | `GridAdditionCheckBoxClick` | `TFixDepositsViewFrame.GridAdditionClickCell` | `0x3E3734` |
| `TFmIncExpCaptionForm` | `TreeListDblClick` | `TFmIncExpCaptionForm.miEditClick` | `0x31F440` |
| `TFundBuyDlgFm` | `btnUpdateCodeClick` | `TFundBuyDlgFm.selAcctCloseUp` | `0x4AA34C` |
| `TFundConvertDlgFm` | `btnUpdateCodeClick` | `TFundConvertDlgFm.SelCurrAcctCloseUp` | `0x5C83F4` |
| `TFundMarkBuyDlgFm` | `cbSignClick` | `TFundMarkBuyDlgFm.edPriceExit` | `0x4F1CB4` |
| `TFundMarkBuyDlgFm` | `edInterestExit` | `TFundMarkBuyDlgFm.edPriceExit` | `0x4F1CB4` |
| `TFundOrderBuyDlgFm` | `btnUpdateCodeClick` | `TFundOrderBuyDlgFm.selAcctCloseUp` | `0x4CF34C` |
| `TFuturesBuyDlgFm` | `edtAmountChange` | `TFuturesBuyDlgFm.edtMarginRatioChange` | `0x4FA81C` |
| `TFuturesBuyDlgFm` | `edtQuantityChange` | `TFuturesBuyDlgFm.edtAmountChange` | `0x4FA7C4` |
| `TFuturesBuyDlgFm` | `selFuturesGoodsCloseUp` | `TFuturesBuyDlgFm.edtQuantityChange` | `0x4FA86C` |
| `TFuturesBuyDlgFm` | `selFuturesGoodsCloseUp` | `TFuturesBuyDlgFm.edtMarginRatioChange` | `0x4FA81C` |
| `TFuturesGoodsListFm` | `MHBGSecurityDblClick` | `TFuturesGoodsListFm.actEditSecurityExecute` | `0x332BE0` |
| `TFuturesSellDlgFm` | `selFuturesContractCloseUp` | `TFuturesSellDlgFm.edtQuantityChange` | `0x4FB7E0` |
| `TFuturesSellDlgFm` | `selInvestAcctCloseUp` | `TFuturesSellDlgFm.selFuturesContractCloseUp` | `0x4FBCA4` |
| `TGoldBuyDlgFm` | `btnUpdateCodeClick` | `TGoldBuyDlgFm.edtGoldAcctCloseUp` | `0x4CB01C` |
| `TImportPreviewFm` | `pcPreviewChange` | `TImportPreviewFm.FormResize` | `0x33B97C` |
| `TImportSelectDlgFm` | `btnImportClick` | `TImportSelectDlgFm.mwIconListClick` | `0x3E5A9C` |
| `TImportSelectDlgFm` | `btnImportFromClipboardClick` | `TImportSelectDlgFm.mwIconListClick` | `0x3E5A9C` |
| `TImportSelectDlgFm` | `mwIconListClick` | `VclFormHideThunk` | `0x8B70` |
| `TInsureViewFrame` | `GridAdditionCheckBoxClick` | `TInsureViewFrame.GridAdditionClickCell` | `0x3459A0` |
| `TMainForm` | `ActEscCloseFormExecute` | `TMainForm.FormKeyPress` | `0x451D74` |
| `TMainForm` | `FormKeyPress` | `VclFormCloseThunk` | `0x8B60` |
| `TMainForm` | `miBookClick` | `TMainForm.pmBookPopup` | `0x45380C` |
| `TMainForm` | `sbCloseClick` | `VclFormCloseThunk` | `0x8B60` |
| `TMoneyListFm` | `MHBGSecurityDblClick` | `TMoneyListFm.actEditSecurityExecute` | `0x32B428` |
| `TmwAdjustButtonDrop` | `edtKeyPress` | `TmwAdjustButtonDrop.btnOKClick` | `0x210AA0` |
| `TmwSelectAccountDrop` | `FormDeactivate` | `VclFormCloseThunk` | `0x8B60` |
| `TmwSelectAccountDrop` | `FormKeyPress` | `TmwSelectAccountDrop.FormDeactivate` | `0x1DD2CC` |
| `TmwSelectAccountDrop` | `FormShortCut` | `TmwSelectAccountDrop.FormDeactivate` | `0x1DD2CC` |
| `TmwSelectCategoryDrop` | `FormDeactivate` | `VclFormCloseThunk` | `0x8B60` |
| `TmwSelectCategoryDrop` | `FormKeyPress` | `TmwSelectCategoryDrop.FormDeactivate` | `0x1E2E30` |
| `TmwSelectCategoryDrop` | `FormShortCut` | `TmwSelectCategoryDrop.FormDeactivate` | `0x1E2E30` |
| `TmwSelectTagDrop` | `FormDeactivate` | `TmwSelectTagDrop.btnOKClick` | `0x1E09F0` |
| `TmwSelectTagDrop` | `FormKeyPress` | `TmwSelectTagDrop.FormDeactivate` | `0x1E01CC` |
| `TmwSelectTagDrop` | `FormShortCut` | `TmwSelectTagDrop.FormDeactivate` | `0x1E01CC` |
| `TmwSelectTagDrop` | `btnNewTagClick` | `VclFormCloseThunk` | `0x8B60` |
| `TmwSelectTagDrop` | `btnOKClick` | `VclFormCloseThunk` | `0x8B60` |
| `TNewAcctWizardDlgFm` | `WizardCtrl1CancelClick` | `VclFormCloseThunk` | `0x8B60` |
| `TNewAcctWizardExchangeDlgFm` | `dxTreeListKeyDown` | `TNewAcctWizardExchangeDlgFm.dxTreeListKeyPress` | `0x400318` |
| `TNewAcctWizardInsureCommerceDlgFm` | `ckbIsForLifeClick` | `TNewAcctWizardInsureCommerceDlgFm.edtYearsChange` | `0x3E8708` |
| `TNewDebtBorrowDlgFm` | `edKindNewAccountClick` | `TNewDebtBorrowDlgFm.edKindChange` | `0x3F0514` |
| `TNewDebtBorrowDlgFm` | `edPersonCloseUp` | `TNewDebtBorrowDlgFm.edKindChange` | `0x3F0514` |
| `TNewDebtBorrowDlgFm` | `edPersonCloseUp` | `TNewDebtBorrowDlgFm.edKindCloseUp` | `0x3EFEBC` |
| `TNewRemindDlgFm` | `RzBitBtn1Click` | `VclFormCloseThunk` | `0x8B60` |
| `TNMarketBondListFm` | `MHBGSecurityDblClick` | `TNMarketBondListFm.actEditSecurityExecute` | `0x329208` |
| `TOkCancelDialogFm` | `BtnCancelClick` | `VclFormCloseThunk` | `0x8B60` |
| `TOnlineGetDataFm` | `btnCompleteClick` | `VclFormCloseThunk` | `0x8B60` |
| `TPayableAdvanceDlgFm` | `selPersonCloseUp` | `TPayableAdvanceDlgFm.edKindCloseUp` | `0x3FD01C` |
| `TPayrollIncomeDlgFm` | `tlCategoryExpListKeyDown` | `TPayrollIncomeDlgFm.tlCategoryExpListKeyPress` | `0x5016C4` |
| `TPayrollIncomeDlgFm` | `tlCategoryIncListKeyDown` | `TPayrollIncomeDlgFm.tlCategoryIncListKeyPress` | `0x501914` |
| `TPracAssetSellDlgFm` | `SelPracAcctCloseUp` | `TPracAssetSellDlgFm.SelObjectClassCloseUp` | `0x4B7CF0` |
| `TPracListFm` | `PracTreeListDblClick` | `TPracListFm.actEditExecute` | `0x31B7E8` |
| `TPreciousMetalsTDBuyDlgFm` | `edtAmountChange` | `TPreciousMetalsTDBuyDlgFm.edtMarginRatioChange` | `0x4FD594` |
| `TPreciousMetalsTDBuyDlgFm` | `edtQuantityChange` | `TPreciousMetalsTDBuyDlgFm.edtAmountChange` | `0x4FD54C` |
| `TPreciousMetalsTDBuyDlgFm` | `selGoodsCloseUp` | `TPreciousMetalsTDBuyDlgFm.edtQuantityChange` | `0x4FD5E4` |
| `TPreciousMetalsTDGoodsListFm` | `MHBGSecurityDblClick` | `TPreciousMetalsTDGoodsListFm.actEditSecurityExecute` | `0x330F9C` |
| `TPreciousMetalsTDSellDlgFm` | `edtQuantityChange` | `TPreciousMetalsTDSellDlgFm.edtAmountChange` | `0x4FE55C` |
| `TPreciousMetalsTDSellDlgFm` | `selContractCloseUp` | `TPreciousMetalsTDSellDlgFm.edtQuantityChange` | `0x4FE5B0` |
| `TPreciousMetalsTDSellDlgFm` | `selInvestAcctCloseUp` | `TPreciousMetalsTDSellDlgFm.selContractCloseUp` | `0x4FEAA4` |
| `TPwdChangeFm` | `BtnOkClick` | `VclFormCloseThunk` | `0x8B60` |
| `TRegisterForm` | `btnFirstUse_FreeUseClick` | `TRegisterForm.btnSuccess_CloseClick` | `0x2A1058` |
| `TRemoteNotificationDlgFm` | `btnRegisterClick` | `VclFormHideThunk` | `0x8B70` |
| `TReportFm` | `miRptDeleteClick` | `VclFormCloseThunk` | `0x8B60` |
| `TRestoreBookFm` | `RzButtonOkClick` | `VclFormHideThunk` | `0x8B70` |
| `TRestoreBookFm` | `RzButtonOkClick` | `VclFormCloseThunk` | `0x8B60` |
| `TSellCouponsRepaymentDlgFm` | `edCommPercentExit` | `TSellCouponsRepaymentDlgFm.edFiscalFeeChange` | `0x4E5A8C` |
| `TSellCouponsRepaymentDlgFm` | `edFiscalExit` | `TSellCouponsRepaymentDlgFm.edFiscalFeeChange` | `0x4E5A8C` |
| `TSellCouponsRepaymentDlgFm` | `edPriceChange` | `TSellCouponsRepaymentDlgFm.edFiscalFeeChange` | `0x4E5A8C` |
| `TSellCouponsRepaymentDlgFm` | `selInvestAcctCloseUp` | `TSellCouponsRepaymentDlgFm.edPriceChange` | `0x4E5B04` |
| `TShortSellingDlgFm` | `edCommPercentExit` | `TShortSellingDlgFm.edFiscalFeeChange` | `0x4EA5DC` |
| `TShortSellingDlgFm` | `edFiscalExit` | `TShortSellingDlgFm.edFiscalFeeChange` | `0x4EA5DC` |
| `TShortSellingDlgFm` | `edFiscalFeeChange` | `TShortSellingDlgFm.edFeeChange` | `0x4EA4D4` |
| `TShortSellingDlgFm` | `edPriceChange` | `TShortSellingDlgFm.edFiscalFeeChange` | `0x4EA5DC` |
| `TShortSellingDlgFm` | `selCodeCloseUp` | `TShortSellingDlgFm.edFiscalFeeChange` | `0x4EA5DC` |
| `TShortSellingDlgFm` | `selInvestAcctCloseUp` | `TShortSellingDlgFm.edPriceChange` | `0x4EA660` |
| `TSplitIncExpDlgFm` | `DTLAcctKeyDown` | `TSplitIncExpDlgFm.DTLAcctKeyPress` | `0x4CA1C8` |
| `TSplitIncExpDlgFm` | `dxTreeListKeyDown` | `TSplitIncExpDlgFm.dxTreeListKeyPress` | `0x4C9DB4` |
| `TStockBuyDlgFm` | `edCommPercentExit` | `TStockBuyDlgFm.edFiscalFeeChange` | `0x4C2590` |
| `TStockBuyDlgFm` | `edFiscalExit` | `TStockBuyDlgFm.edFiscalFeeChange` | `0x4C2590` |
| `TStockBuyDlgFm` | `edFiscalFeeChange` | `TStockBuyDlgFm.edFeeChange` | `0x4C2748` |
| `TStockBuyDlgFm` | `edPriceExit` | `TStockBuyDlgFm.edFiscalFeeChange` | `0x4C2590` |
| `TStockBuyDlgFm` | `edTransDateChange` | `TStockBuyDlgFm.edPriceExit` | `0x4C14DC` |
| `TStockBuyDlgFm` | `edtEndDateChange` | `TStockBuyDlgFm.edPriceExit` | `0x4C14DC` |
| `TStockBuyDlgFm` | `selInvestAcctCloseUp` | `TStockBuyDlgFm.edPriceExit` | `0x4C14DC` |
| `TStockMarkBuyDlgFm` | `cbSignClick` | `TStockMarkBuyDlgFm.edPriceExit` | `0x4F2FEC` |
| `TStockOrderBuyDlgFm` | `btnUpdateCodeClick` | `TStockOrderBuyDlgFm.selInvestAcctCloseUp` | `0x4D00C8` |
| `TStockSellDlgFm` | `edCommPercentExit` | `TStockSellDlgFm.edFiscalFeeChange` | `0x4BF2F8` |
| `TStockSellDlgFm` | `edFiscalExit` | `TStockSellDlgFm.edFiscalFeeChange` | `0x4BF2F8` |
| `TStockSellDlgFm` | `edFiscalFeeChange` | `TStockSellDlgFm.edFeeChange` | `0x4BF4B0` |
| `TStockSellDlgFm` | `edPriceChange` | `TStockSellDlgFm.edFiscalFeeChange` | `0x4BF2F8` |
| `TSyncUserDataFm` | `btnRegisterClick` | `VclFormHideThunk` | `0x8B70` |
| `TTransferListTemplateFrame` | `tlTransListKeyDown` | `TTransferListTemplateFrame.tlTransListKeyPress` | `0x5CE690` |
| `TTransListTemplateFrame` | `tlTransListKeyDown` | `TTransListTemplateFrame.tlTransListKeyPress` | `0x5CB910` |

## 6. 开发与验收合同

- `command_handler` 和 `domain_command_handler` 必须通过单一应用命令进入事务边界，UI 不直接写 SQLite。
- `query_handler`、`query_export_service` 和报表投影共享查询 DTO，筛选变化后必须重新生成结果再导出。
- `import_pipeline` 必须经过原始行、映射、预览、校验、幂等检查和单事务提交。
- `integration_adapter` 默认不阻塞本地记账，并保留批次、冲突、取消、重试和删除墓碑。
- `presentation_state` 和 `presentation_lifecycle` 只有在代码或动态结果证明副作用后，才升级为领域命令。
- `same_name_*` 和 `unresolved` 不能证明代码归属；资源型无 VMT 窗体必须先验证可达性。
