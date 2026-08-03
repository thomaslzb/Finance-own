"""在内存 SQLite 中验证全部迁移、索引和已确认查询投影。"""

from __future__ import annotations

import sqlite3
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
MIGRATIONS_DIR = WORKSPACE / "migrations"


def migration_paths() -> list[Path]:
    """按文件名顺序返回全部 SQLite 迁移。"""

    paths = sorted(MIGRATIONS_DIR.glob("*.sql"))
    if not paths:
        raise SystemExit(f"迁移目录中没有 SQL 文件：{MIGRATIONS_DIR}")
    return paths


def fetch_names(connection: sqlite3.Connection, object_type: str) -> set[str]:
    rows = connection.execute(
        "SELECT name FROM sqlite_schema WHERE type = ?", (object_type,)
    )
    return {str(row[0]) for row in rows}


def insurance_cash_value_as_of(
    connection: sqlite3.Connection, policy_id: str, as_of_date: str
) -> tuple[int, int] | None:
    """按显式查询时点返回有效现金价值及版本，未来快照不提前生效。"""

    return connection.execute(
        """SELECT value_minor, version
           FROM v_insurance_cash_value_effective_ranges
           WHERE policy_id = ?
             AND effective_from <= ?
             AND (effective_to_exclusive IS NULL OR ? < effective_to_exclusive)""",
        (policy_id, as_of_date, as_of_date),
    ).fetchone()


def seed_minimal_ledger(connection: sqlite3.Connection) -> None:
    connection.execute(
        "INSERT INTO currencies(code, name, minor_unit) VALUES ('CNY', '人民币', 2)"
    )
    connection.execute(
        """INSERT INTO ledgers(id, name, base_currency_code, created_at, updated_at)
           VALUES ('ledger-1', '校验账本', 'CNY', '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z')"""
    )
    connection.execute(
        """INSERT INTO accounts(
               id, ledger_id, name, kind, currency_code, is_asset, created_at
           ) VALUES ('account-1', 'ledger-1', '现金', 'cash', 'CNY', 1, '2026-07-28T00:00:00Z')"""
    )
    connection.execute(
        """INSERT INTO categories(id, ledger_id, name, direction)
           VALUES ('category-income', 'ledger-1', '工资', 'income'),
                  ('category-expense', 'ledger-1', '餐饮', 'expense')"""
    )
    connection.execute(
        "INSERT INTO tags(id, ledger_id, name) VALUES ('tag-1', 'ledger-1', '日常')"
    )
    connection.execute(
        "INSERT INTO account_tags(account_id, tag_id) VALUES ('account-1', 'tag-1')"
    )
    connection.execute(
        """INSERT INTO transactions(
               id, ledger_id, sequence_no, business_date, occurred_at, kind,
               theme, created_at, updated_at
           ) VALUES
               ('transaction-1', 'ledger-1', 1, '2026-07-28', '2026-07-28T09:00:00Z',
                'income', '工资到账', '2026-07-28T09:00:00Z', '2026-07-28T09:00:00Z'),
               ('transaction-2', 'ledger-1', 2, '2026-07-28', '2026-07-28T12:00:00Z',
                'expense', '午餐', '2026-07-28T12:00:00Z', '2026-07-28T12:00:00Z')"""
    )
    connection.execute(
        """INSERT INTO transaction_entries(
               id, transaction_id, account_id, line_no, role, direction,
               amount_minor, currency_code, base_amount_minor, base_currency_code, category_id
           ) VALUES
               ('entry-1', 'transaction-1', 'account-1', 1, 'primary', 'inflow',
                10000, 'CNY', 10000, 'CNY', 'category-income'),
               ('entry-2', 'transaction-2', 'account-1', 1, 'primary', 'outflow',
                2500, 'CNY', 2500, 'CNY', 'category-expense')"""
    )
    connection.execute(
        "INSERT INTO transaction_tags(transaction_id, tag_id) VALUES ('transaction-2', 'tag-1')"
    )


def validate_schema(connection: sqlite3.Connection) -> None:
    required_tables = {
        "currencies",
        "ledgers",
        "accounts",
        "transactions",
        "transaction_entries",
        "transaction_tags",
        "investment_instruments",
        "investment_trades",
        "investment_lot_allocations",
        "market_quotes",
        "report_presets",
        "legacy_id_map",
        "transaction_templates",
        "transaction_template_entries",
        "schedules",
        "schedule_occurrences",
        "budgets",
        "budget_items",
        "reminders",
        "reminder_occurrences",
        "financial_goals",
        "financial_goal_accounts",
        "financial_plan_scenarios",
        "financial_plan_inputs",
        "financial_plan_accounts",
        "application_settings",
        "debt_contracts",
        "credit_account_terms",
        "futures_contract_terms",
        "margin_account_terms",
        "margin_contracts",
        "tangible_asset_details",
        "insurance_policies",
        "insurance_cash_value_snapshots",
        "insurance_cash_value_history",
        "insurance_events",
        "social_security_profiles",
        "import_field_mappings",
        "import_batches",
        "import_rows",
        "sync_profiles",
        "sync_batches",
        "sync_object_results",
        "sync_conflicts",
        "sync_tombstones",
        "notification_delivery_log",
        "fee_rule_snapshots",
        "payroll_income_details",
        "payroll_category_components",
        "payroll_social_contributions",
        "prepaid_expenses",
        "prepaid_expense_installments",
        "deposit_rate_update_batches",
        "deposit_rate_update_items",
        "deposit_rate_versions",
    }
    required_views = {
        "v_ledger_entries",
        "v_account_transaction_running_balance",
        "v_account_balances",
        "v_life_theme_transactions",
        "v_life_theme_assets",
        "v_investment_position_inputs",
        "v_investment_realized_profit_inputs",
        "v_budget_consumption_inputs",
        "v_goal_account_balance_inputs",
        "v_goal_progress_inputs",
        "v_due_schedules",
        "v_pending_schedule_occurrences",
        "v_schedule_lifecycle",
        "v_today_reminder_inbox",
        "v_debt_contract_inputs",
        "v_import_batch_audit",
        "v_open_sync_conflicts",
        "v_insurance_cash_value_effective_ranges",
        "v_payroll_income_reconciliation",
        "v_prepaid_expense_overview",
        "v_current_deposit_rates",
    }
    required_indexes = {
        "idx_transactions_ledger_status_date",
        "idx_entries_account_currency_transaction",
        "idx_entries_category_transaction",
        "idx_transaction_tags_tag_transaction",
        "idx_investment_trades_position",
        "idx_market_quotes_latest",
        "ux_account_groups_sibling_name",
        "ux_categories_sibling_name_direction",
        "idx_schedules_due",
        "idx_schedule_occurrences_due_status",
        "idx_schedule_occurrences_schedule_status",
        "idx_budgets_period",
        "idx_reminders_due",
        "idx_reminder_occurrences_trigger_status",
        "idx_reminder_occurrences_rule_status",
        "idx_goals_status_date",
        "idx_goals_status_period",
        "ux_application_settings_scope_key",
        "idx_debt_contracts_status_due",
        "idx_import_batches_status_created",
        "idx_import_rows_batch_status",
        "idx_sync_batches_profile_started",
        "idx_sync_conflicts_open",
        "idx_notification_delivery_retry",
        "idx_fee_rule_snapshots_lookup",
        "idx_insurance_cash_value_history_policy_date",
        "idx_insurance_events_policy_date",
        "idx_payroll_income_details_person",
        "idx_payroll_category_components_transaction",
        "idx_payroll_social_contributions_transaction",
        "idx_parties_ledger_name_unique",
        "idx_parties_ledger_category_hidden_name",
        "idx_prepaid_expenses_ledger_status_first_due",
        "idx_prepaid_expenses_party_status",
        "idx_prepaid_installments_due_status",
        "idx_deposit_rate_batches_ledger_status_requested",
        "idx_deposit_rate_items_batch_status_key",
        "idx_deposit_rate_versions_lookup",
    }
    required_triggers = {
        "trg_deposit_rate_batches_publish_validate",
        "trg_deposit_rate_batches_published_immutable",
        "trg_deposit_rate_items_published_immutable",
        "trg_deposit_rate_versions_source_guard",
        "trg_deposit_rate_versions_immutable",
        "trg_financial_goals_period_validate_insert",
        "trg_financial_goals_period_validate_update",
        "trg_financial_goals_baseline_validate_insert",
        "trg_financial_goals_baseline_validate_update",
    }
    assert required_tables <= fetch_names(connection, "table")
    assert required_views <= fetch_names(connection, "view")
    assert required_indexes <= fetch_names(connection, "index")
    assert required_triggers <= fetch_names(connection, "trigger")
    assert connection.execute("PRAGMA application_id").fetchone() == (1179604814,)
    assert connection.execute("PRAGMA user_version").fetchone() == (13,)


def validate_party_list_lifecycle(connection: sqlite3.Connection) -> None:
    """验证三类共享名称空间，且隐藏记录不会释放名称。"""

    connection.execute(
        """INSERT INTO parties(id, ledger_id, name, kind, category)
           VALUES ('party-list-1', 'ledger-1', '共享名称', 'person', 'contact_person')"""
    )
    for category, kind in (("institution", "institution"), ("family_member", "person")):
        if category == "family_member":
            connection.execute(
                "UPDATE parties SET is_archived = 1 WHERE id = 'party-list-1'"
            )
        try:
            connection.execute(
                """INSERT INTO parties(id, ledger_id, name, kind, category)
                   VALUES (?, 'ledger-1', '共享名称', ?, ?)""",
                (f"party-list-{category}", kind, category),
            )
        except sqlite3.IntegrityError:
            continue
        raise AssertionError(f"人员名称唯一约束未阻止类别 {category} 的重复名称")


def validate_prepaid_expenses(connection: sqlite3.Connection) -> None:
    """验证待摊主体、期次状态约束和概况剩余金额投影。"""

    connection.execute(
        """INSERT INTO accounts(
               id, ledger_id, name, kind, currency_code, is_asset, created_at
           ) VALUES (
               'prepaid-account-1', 'ledger-1', '年度服务费', 'prepaid_expense',
               'CNY', 1, '2026-08-02T00:00:00Z'
           )"""
    )
    connection.executemany(
        """INSERT INTO transactions(
               id, ledger_id, sequence_no, business_date, occurred_at, kind,
               party_id, theme, created_at, updated_at
           ) VALUES (?, 'ledger-1', ?, ?, ?, ?, 'party-list-1', ?, ?, ?)""",
        [
            (
                "prepaid-opening-1",
                900,
                "2026-08-02",
                "2026-08-02T00:00:00Z",
                "balance_adjustment",
                "待摊费用期初余额",
                "2026-08-02T00:00:00Z",
                "2026-08-02T00:00:00Z",
            ),
            (
                "prepaid-posting-1",
                901,
                "2026-08-02",
                "2026-08-02T00:01:00Z",
                "expense",
                "待摊费用第一期",
                "2026-08-02T00:01:00Z",
                "2026-08-02T00:01:00Z",
            ),
        ],
    )
    connection.execute(
        """INSERT INTO prepaid_expenses(
               id, ledger_id, account_id, party_id, expense_category_id,
               funding_account_id, initial_transaction_id, original_amount_minor,
               currency_code, business_date, first_amortization_date,
               frequency_months, total_installments, posted_installments,
               note, created_at, updated_at
           ) VALUES (
               'prepaid-1', 'ledger-1', 'prepaid-account-1', 'party-list-1',
               'category-expense', NULL, 'prepaid-opening-1', 10001, 'CNY',
               '2026-08-02', '2026-08-02', 1, 3, 1, '模式验证',
               '2026-08-02T00:00:00Z', '2026-08-02T00:00:00Z'
           )"""
    )
    connection.executemany(
        """INSERT INTO prepaid_expense_installments(
               id, prepaid_expense_id, installment_no, due_date, amount_minor,
               status, transaction_id, posted_at, created_at, updated_at
           ) VALUES (?, 'prepaid-1', ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            (
                "prepaid-installment-1",
                1,
                "2026-08-02",
                3333,
                "posted",
                "prepaid-posting-1",
                "2026-08-02T00:01:00Z",
                "2026-08-02T00:00:00Z",
                "2026-08-02T00:01:00Z",
            ),
            (
                "prepaid-installment-2",
                2,
                "2026-09-02",
                3333,
                "pending",
                None,
                None,
                "2026-08-02T00:00:00Z",
                "2026-08-02T00:00:00Z",
            ),
            (
                "prepaid-installment-3",
                3,
                "2026-10-02",
                3335,
                "pending",
                None,
                None,
                "2026-08-02T00:00:00Z",
                "2026-08-02T00:00:00Z",
            ),
        ],
    )
    overview = connection.execute(
        """SELECT original_amount_minor, remaining_amount_minor,
                  total_installments, posted_installments
           FROM v_prepaid_expense_overview
           WHERE prepaid_expense_id = 'prepaid-1'"""
    ).fetchone()
    assert overview == (10001, 6668, 3, 1), overview

    try:
        connection.execute(
            "UPDATE prepaid_expenses SET posted_installments = 4 WHERE id = 'prepaid-1'"
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("待摊费用已摊期次不得超过总期次")

    try:
        connection.execute(
            """INSERT INTO prepaid_expense_installments(
                   id, prepaid_expense_id, installment_no, due_date, amount_minor,
                   status, created_at, updated_at
               ) VALUES (
                   'prepaid-invalid-posted', 'prepaid-1', 4, '2026-11-02', 1,
                   'posted', '2026-08-02T00:00:00Z', '2026-08-02T00:00:00Z'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("已入账待摊期次必须关联交易和入账时间")


def validate_deposit_rates(connection: sqlite3.Connection) -> None:
    """验证在线批次整批发布、不可变版本和当前有效利率投影。"""

    connection.execute(
        """INSERT INTO deposit_rate_update_batches(
               id, ledger_id, source, status, requested_at,
               received_count, valid_count, published_count, created_at, updated_at
           ) VALUES (
               'rate-batch-1', 'ledger-1', 'online', 'staged',
               '2026-08-02T06:00:00+08:00', 1, 1, 0,
               '2026-08-02T06:00:00+08:00', '2026-08-02T06:00:00+08:00'
           )"""
    )
    connection.execute(
        """INSERT INTO deposit_rate_update_items(
               id, batch_id, line_no, currency_code, deposit_type, term_code,
               raw_rate_text, annual_rate_units, annual_rate_scale,
               validation_status, created_at
           ) VALUES (
               'rate-item-1', 'rate-batch-1', 1, 'CNY', 'demand', 'demand',
               '0.36', 36, 2, 'valid', '2026-08-02T06:00:00+08:00'
           )"""
    )
    try:
        connection.execute(
            """INSERT INTO deposit_rate_versions(
                   id, ledger_id, currency_code, deposit_type, term_code,
                   annual_rate_units, annual_rate_scale, effective_at, source,
                   batch_id, source_item_id, version, created_at
               ) VALUES (
                   'rate-version-staged', 'ledger-1', 'CNY', 'demand', 'demand',
                   36, 2, '2026-08-02T06:00:30+08:00', 'online',
                   'rate-batch-1', 'rate-item-1', 1, '2026-08-02T06:00:30+08:00'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("未发布批次错误地产生了在线利率版本")

    connection.execute(
        """UPDATE deposit_rate_update_batches
           SET status = 'published', completed_at = '2026-08-02T06:01:00+08:00',
               published_count = 1, updated_at = '2026-08-02T06:01:00+08:00'
           WHERE id = 'rate-batch-1'"""
    )
    connection.execute(
        """INSERT INTO deposit_rate_versions(
               id, ledger_id, currency_code, deposit_type, term_code,
               annual_rate_units, annual_rate_scale, effective_at, source,
               batch_id, source_item_id, version, created_at
           ) VALUES (
               'rate-version-1', 'ledger-1', 'CNY', 'demand', 'demand',
               36, 2, '2026-08-02T06:01:00+08:00', 'online',
               'rate-batch-1', 'rate-item-1', 1, '2026-08-02T06:01:00+08:00'
           )"""
    )
    connection.execute(
        """INSERT INTO deposit_rate_versions(
               id, ledger_id, currency_code, deposit_type, term_code,
               annual_rate_units, annual_rate_scale, effective_at, source,
               version, supersedes_id, created_at
           ) VALUES (
               'rate-version-2', 'ledger-1', 'CNY', 'demand', 'demand',
               10, 2, '2026-08-03T00:00:00+08:00', 'manual',
               2, 'rate-version-1', '2026-08-03T00:00:00+08:00'
           )"""
    )

    current = connection.execute(
        """SELECT deposit_rate_version_id, annual_rate_units,
                  annual_rate_scale, source, version
           FROM v_current_deposit_rates
           WHERE ledger_id = 'ledger-1' AND currency_code = 'CNY'
             AND deposit_type = 'demand' AND term_code = 'demand'"""
    ).fetchone()
    assert current == ("rate-version-2", 10, 2, "manual", 2), current

    try:
        connection.execute(
            """UPDATE deposit_rate_versions
               SET annual_rate_units = 11
               WHERE id = 'rate-version-2'"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("已发布存款利率版本仍可原位覆盖")

    try:
        connection.execute(
            """UPDATE deposit_rate_update_items
               SET raw_rate_text = '0.37'
               WHERE id = 'rate-item-1'"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("已发布存款利率明细仍可原位覆盖")

    try:
        connection.execute(
            """INSERT INTO deposit_rate_versions(
                   id, ledger_id, currency_code, deposit_type, term_code,
                   annual_rate_units, annual_rate_scale, effective_at, source,
                   version, created_at
               ) VALUES (
                   'rate-negative', 'ledger-1', 'CNY', 'demand', 'demand',
                   -1, 2, '2026-08-04T00:00:00+08:00', 'manual',
                   3, '2026-08-04T00:00:00+08:00'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("负存款利率未被目标模式阻止")

    try:
        connection.execute(
            """INSERT INTO deposit_rate_versions(
                   id, ledger_id, currency_code, deposit_type, term_code,
                   annual_rate_units, annual_rate_scale, effective_at, source,
                   version, created_at
               ) VALUES (
                   'rate-over-limit', 'ledger-1', 'CNY', 'demand', 'demand',
                   10001, 2, '2026-08-03T00:00:00+08:00', 'manual',
                   3, '2026-08-03T00:00:00+08:00'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("超过 100% 的存款利率未被目标模式阻止")

    connection.execute(
        """INSERT INTO deposit_rate_update_batches(
               id, ledger_id, source, status, requested_at,
               received_count, valid_count, published_count, created_at, updated_at
           ) VALUES (
               'rate-batch-partial', 'ledger-1', 'online', 'staged',
               '2026-08-04T00:00:00+08:00', 2, 1, 0,
               '2026-08-04T00:00:00+08:00', '2026-08-04T00:00:00+08:00'
           )"""
    )
    try:
        connection.execute(
            """UPDATE deposit_rate_update_batches
               SET status = 'published', completed_at = '2026-08-04T00:01:00+08:00',
                   published_count = 1, updated_at = '2026-08-04T00:01:00+08:00'
               WHERE id = 'rate-batch-partial'"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("不完整在线批次被错误地部分发布")


def validate_projections(connection: sqlite3.Connection) -> None:
    balances = [
        int(row[0])
        for row in connection.execute(
            """SELECT balance_minor
               FROM v_account_transaction_running_balance
               WHERE account_id = 'account-1'
               ORDER BY sequence_no"""
        )
    ]
    assert balances == [10000, 7500], balances

    flow = connection.execute(
        """SELECT
               SUM(CASE WHEN direction = 'inflow' THEN amount_minor ELSE 0 END),
               SUM(CASE WHEN direction = 'outflow' THEN amount_minor ELSE 0 END),
               SUM(signed_amount_minor)
           FROM v_ledger_entries
           WHERE ledger_id = 'ledger-1' AND status = 'posted'"""
    ).fetchone()
    assert flow == (10000, 2500, 7500), flow

    tagged_transaction = connection.execute(
        "SELECT COUNT(*) FROM v_life_theme_transactions WHERE tag_id = 'tag-1'"
    ).fetchone()
    assert tagged_transaction == (1,), tagged_transaction

    tagged_asset = connection.execute(
        """SELECT balance_minor FROM v_life_theme_assets
           WHERE tag_id = 'tag-1' AND account_id = 'account-1'"""
    ).fetchone()
    assert tagged_asset == (7500,), tagged_asset

    query_plan = " ".join(
        str(row[3])
        for row in connection.execute(
            """EXPLAIN QUERY PLAN
               SELECT id FROM transactions
               WHERE ledger_id = ? AND status = ?
                 AND business_date BETWEEN ? AND ?
               ORDER BY business_date, sequence_no""",
            ("ledger-1", "posted", "2026-01-01", "2026-12-31"),
        )
    )
    assert "idx_transactions_ledger_status_date" in query_plan, query_plan
    assert connection.execute("PRAGMA foreign_key_check").fetchall() == []


def validate_payroll_income(connection: sqlite3.Connection) -> None:
    """验证工资组成公式、账户投影和跨实体作用域约束。"""

    connection.execute(
        """INSERT INTO accounts(
               id, ledger_id, name, kind, currency_code, is_asset, created_at
           ) VALUES (
               'social-account-1', 'ledger-1', '社保权益', 'social_security',
               'CNY', 1, '2026-07-31T00:00:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO parties(id, ledger_id, name, kind)
           VALUES ('person-payroll-1', 'ledger-1', '工资人员', 'person')"""
    )
    connection.execute(
        """INSERT INTO categories(id, ledger_id, name, direction)
           VALUES ('category-payroll-tax', 'ledger-1', '工资扣款', 'expense')"""
    )
    connection.execute(
        """INSERT INTO transactions(
               id, ledger_id, sequence_no, business_date, occurred_at, kind,
               theme, created_at, updated_at
           ) VALUES (
               'payroll-transaction-1', 'ledger-1', 200, '2026-07-31',
               '2026-07-31T09:00:00Z', 'payroll_income', '工资收入',
               '2026-07-31T09:00:00Z', '2026-07-31T09:00:00Z'
           )"""
    )
    connection.executemany(
        """INSERT INTO transaction_entries(
               id, transaction_id, account_id, line_no, role, direction,
               amount_minor, currency_code, base_amount_minor, base_currency_code
           ) VALUES (?, 'payroll-transaction-1', ?, ?, ?, 'inflow', ?, 'CNY', ?, 'CNY')""",
        [
            ("payroll-cash-entry-1", "account-1", 1, "primary", 8000, 8000),
            ("payroll-social-entry-1", "social-account-1", 2, "split", 1500, 1500),
        ],
    )
    connection.execute(
        """INSERT INTO payroll_income_details(
               transaction_id, receiving_account_id, person_id, currency_code,
               calculation_version, created_at, updated_at
           ) VALUES (
               'payroll-transaction-1', 'account-1', 'person-payroll-1', 'CNY', 1,
               '2026-07-31T09:00:00Z', '2026-07-31T09:00:00Z'
           )"""
    )
    connection.executemany(
        """INSERT INTO payroll_category_components(
               id, transaction_id, line_no, component_kind, category_id,
               amount_minor, currency_code
           ) VALUES (?, 'payroll-transaction-1', ?, ?, ?, ?, 'CNY')""",
        [
            ("payroll-income-component-1", 1, "income", "category-income", 10000),
            (
                "payroll-deduction-component-1",
                1,
                "deduction",
                "category-payroll-tax",
                1000,
            ),
        ],
    )
    connection.execute(
        """INSERT INTO payroll_social_contributions(
               id, transaction_id, line_no, social_account_id,
               personal_amount_minor, company_amount_minor, currency_code
           ) VALUES (
               'payroll-social-component-1', 'payroll-transaction-1', 1,
               'social-account-1', 1000, 500, 'CNY'
           )"""
    )

    reconciliation = connection.execute(
        """SELECT gross_income_minor, deduction_minor,
                  personal_contribution_minor, company_contribution_minor,
                  net_cash_minor, social_account_credit_minor,
                  receiving_account_movement_minor, social_account_movement_minor,
                  is_component_formula_valid, is_cash_projection_matched,
                  is_social_projection_matched
           FROM v_payroll_income_reconciliation
           WHERE transaction_id = 'payroll-transaction-1'"""
    ).fetchone()
    assert reconciliation == (
        10000,
        1000,
        1000,
        500,
        8000,
        1500,
        8000,
        1500,
        1,
        1,
        1,
    ), reconciliation

    try:
        connection.execute(
            """INSERT INTO payroll_category_components(
                   id, transaction_id, line_no, component_kind, category_id,
                   amount_minor, currency_code
               ) VALUES (
                   'payroll-income-component-duplicate', 'payroll-transaction-1', 2,
                   'income', 'category-income', 1, 'CNY'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("工资收入允许重复分类明细")

    connection.execute(
        """INSERT INTO transactions(
               id, ledger_id, sequence_no, business_date, occurred_at, kind,
               created_at, updated_at
           ) VALUES (
               'payroll-invalid-kind', 'ledger-1', 201, '2026-07-31',
               '2026-07-31T10:00:00Z', 'income',
               '2026-07-31T10:00:00Z', '2026-07-31T10:00:00Z'
           )"""
    )
    try:
        connection.execute(
            """INSERT INTO payroll_income_details(
                   transaction_id, receiving_account_id, person_id, currency_code,
                   created_at, updated_at
               ) VALUES (
                   'payroll-invalid-kind', 'account-1', 'person-payroll-1', 'CNY',
                   '2026-07-31T10:00:00Z', '2026-07-31T10:00:00Z'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("普通收入交易允许附加工资专属明细")


def validate_transfer_and_atomic_rollback(connection: sqlite3.Connection) -> None:
    connection.execute(
        """INSERT INTO accounts(
               id, ledger_id, name, kind, currency_code, is_asset, created_at
           ) VALUES ('account-2', 'ledger-1', '银行卡', 'current', 'CNY', 1,
                     '2026-07-28T00:00:00Z')"""
    )
    connection.execute(
        """INSERT INTO transactions(
               id, ledger_id, sequence_no, business_date, occurred_at, kind,
               theme, created_at, updated_at
           ) VALUES (
               'transaction-3', 'ledger-1', 3, '2026-07-28', '2026-07-28T15:00:00Z',
               'transfer', '账户转账', '2026-07-28T15:00:00Z', '2026-07-28T15:00:00Z'
           )"""
    )
    connection.executemany(
        """INSERT INTO transaction_entries(
               id, transaction_id, account_id, line_no, role, direction,
               amount_minor, currency_code, base_amount_minor, base_currency_code
           ) VALUES (?, 'transaction-3', ?, ?, ?, ?, ?, 'CNY', ?, 'CNY')""",
        [
            ("entry-3-out", "account-1", 1, "primary", "outflow", 5000, 5000),
            (
                "entry-3-in",
                "account-2",
                2,
                "counterparty",
                "inflow",
                5000,
                5000,
            ),
            ("entry-3-fee", "account-1", 3, "fee", "outflow", 100, 100),
        ],
    )

    balances = dict(
        connection.execute(
            """SELECT account_id, balance_minor
               FROM v_account_balances
               WHERE ledger_id = 'ledger-1'
                 AND account_id IN ('account-1', 'account-2')"""
        )
    )
    assert balances == {"account-1": 2400, "account-2": 5000}, balances

    connection.execute("SAVEPOINT failed_transaction_write")
    try:
        connection.execute(
            """INSERT INTO transactions(
                   id, ledger_id, sequence_no, business_date, occurred_at, kind,
                   created_at, updated_at
               ) VALUES (
                   'transaction-rollback', 'ledger-1', 4, '2026-07-28',
                   '2026-07-28T16:00:00Z', 'expense',
                   '2026-07-28T16:00:00Z', '2026-07-28T16:00:00Z'
               )"""
        )
        connection.execute(
            """INSERT INTO transaction_entries(
                   id, transaction_id, account_id, line_no, role, direction,
                   amount_minor, currency_code
               ) VALUES (
                   'entry-rollback-1', 'transaction-rollback', 'account-1', 1,
                   'primary', 'outflow', 100, 'CNY'
               )"""
        )
        connection.execute(
            """INSERT INTO transaction_entries(
                   id, transaction_id, account_id, line_no, role, direction,
                   amount_minor, currency_code
               ) VALUES (
                   'entry-rollback-2', 'transaction-rollback', 'account-1', 1,
                   'fee', 'outflow', 10, 'CNY'
               )"""
        )
    except sqlite3.IntegrityError:
        connection.execute("ROLLBACK TO failed_transaction_write")
        connection.execute("RELEASE failed_transaction_write")
    else:
        raise AssertionError("预期的交易内分录顺序冲突未发生")

    rolled_back_header = connection.execute(
        "SELECT COUNT(*) FROM transactions WHERE id = 'transaction-rollback'"
    ).fetchone()
    rolled_back_entries = connection.execute(
        "SELECT COUNT(*) FROM transaction_entries WHERE transaction_id = 'transaction-rollback'"
    ).fetchone()
    assert rolled_back_header == (0,), rolled_back_header
    assert rolled_back_entries == (0,), rolled_back_entries


def validate_constraints(connection: sqlite3.Connection) -> None:
    connection.execute(
        """INSERT INTO account_groups(id, ledger_id, name, kind)
           VALUES ('group-1', 'ledger-1', '资金账户', 'asset')"""
    )
    try:
        connection.execute(
            """INSERT INTO account_groups(id, ledger_id, name, kind)
               VALUES ('group-2', 'ledger-1', '资金账户', 'asset')"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("根账户组重名约束未生效")

    try:
        connection.execute(
            """INSERT INTO report_presets(
                   id, ledger_id, report_key, name, filter_json, created_at, updated_at
               ) VALUES (
                   'preset-1', 'ledger-1', 'income', '无效筛选', '{invalid',
                   '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("报表筛选 JSON 约束未生效")


def validate_destructive_operation_constraints(connection: sqlite3.Connection) -> None:
    """验证删除账户组、受引用主数据和附件内容的数据库保护边界。"""
    connection.execute(
        """INSERT INTO account_groups(id, ledger_id, name, kind)
           VALUES ('group-delete', 'ledger-1', '待删除账户组', 'asset')"""
    )
    connection.execute(
        "UPDATE accounts SET group_id = 'group-delete' WHERE id = 'account-2'"
    )
    connection.execute("DELETE FROM account_groups WHERE id = 'group-delete'")
    detached_account = connection.execute(
        "SELECT group_id FROM accounts WHERE id = 'account-2'"
    ).fetchone()
    assert detached_account == (None,), detached_account

    for sql, message in (
        ("DELETE FROM accounts WHERE id = 'account-1'", "受交易引用账户允许删除"),
        (
            "DELETE FROM categories WHERE id = 'category-income'",
            "受交易引用分类允许删除",
        ),
        ("DELETE FROM currencies WHERE code = 'CNY'", "账簿本币允许删除"),
    ):
        try:
            connection.execute(sql)
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError(message)

    connection.execute(
        """INSERT INTO attachments(
               id, ledger_id, file_name, relative_path, byte_size, sha256, created_at
           ) VALUES (
               'attachment-1', 'ledger-1', 'receipt.png', 'attachments/receipt.png',
               100, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
               '2026-07-28T00:00:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO transaction_attachments(transaction_id, attachment_id)
           VALUES ('transaction-1', 'attachment-1')"""
    )
    try:
        connection.execute("DELETE FROM attachments WHERE id = 'attachment-1'")
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("仍被交易引用的附件允许物理删除")
    connection.execute(
        "DELETE FROM transaction_attachments WHERE attachment_id = 'attachment-1'"
    )
    connection.execute("DELETE FROM attachments WHERE id = 'attachment-1'")
    assert connection.execute(
        "SELECT COUNT(*) FROM attachments WHERE id = 'attachment-1'"
    ).fetchone() == (0,)


def validate_planning_and_automation(connection: sqlite3.Connection) -> None:
    """验证模板计划、预算、提醒、目标和规划的真相表与输入投影。"""

    connection.execute(
        """INSERT INTO transaction_templates(
               id, ledger_id, name, transaction_kind, created_at, updated_at
           ) VALUES (
               'template-1', 'ledger-1', '月度餐饮', 'expense',
               '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO transaction_template_entries(
               id, template_id, line_no, role, direction, account_id,
               category_id, amount_minor, currency_code
           ) VALUES (
               'template-entry-1', 'template-1', 1, 'primary', 'outflow',
               'account-1', 'category-expense', 3000, 'CNY'
           )"""
    )
    connection.execute(
        """INSERT INTO schedules(
               id, ledger_id, template_id, name, recurrence_json, start_date,
               next_due_date, execution_mode, created_at, updated_at
           ) VALUES (
               'schedule-1', 'ledger-1', 'template-1', '每月餐饮计划',
               '{"frequency":"monthly","interval":1}', '2026-07-01',
               '2026-08-01', 'manual',
               '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z'
           )"""
    )
    assert connection.execute(
        "SELECT id, next_due_date FROM v_due_schedules WHERE id = 'schedule-1'"
    ).fetchone() == ("schedule-1", "2026-08-01")
    connection.execute(
        """INSERT INTO schedule_occurrences(
               id, schedule_id, due_date, recurrence_version, execution_mode,
               status, source_snapshot_json, idempotency_key, created_at, updated_at
           ) VALUES (
               'schedule-occurrence-1', 'schedule-1', '2026-08-01', 1, 'manual',
               'pending', '{"amount_minor":3000,"currency_code":"CNY"}',
               'schedule-1:2026-08-01:v1',
               '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z'
           )"""
    )
    assert connection.execute(
        """SELECT schedule_id, due_date, execution_mode, reminder_lead_days
           FROM v_pending_schedule_occurrences
           WHERE occurrence_id = 'schedule-occurrence-1'"""
    ).fetchone() == ("schedule-1", "2026-08-01", "manual", 0)

    try:
        connection.execute(
            """INSERT INTO schedules(
                   id, ledger_id, template_id, name, recurrence_json, start_date,
                   execution_mode, created_at, updated_at
               ) VALUES (
                   'schedule-invalid', 'ledger-1', 'template-1', '无效计划',
                   '{invalid', '2026-07-01', 'manual',
                   '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("计划允许写入无效 recurrence_json")

    connection.execute(
        """INSERT INTO budgets(
               id, ledger_id, name, period_kind, start_date, end_date, status,
               created_at, updated_at
           ) VALUES (
               'budget-1', 'ledger-1', '七月预算', 'monthly',
               '2026-07-01', '2026-07-31', 'active',
               '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO budget_items(
               id, budget_id, category_id, period_start, period_end,
               amount_minor, currency_code
           ) VALUES (
               'budget-item-1', 'budget-1', 'category-expense',
               '2026-07-01', '2026-07-31', 5000, 'CNY'
           )"""
    )
    budget_result = connection.execute(
        """SELECT budget_amount_minor, outflow_minor, inflow_minor
           FROM v_budget_consumption_inputs WHERE budget_item_id = 'budget-item-1'"""
    ).fetchone()
    assert budget_result == (5000, 2500, 0), budget_result

    connection.execute(
        """INSERT INTO reminders(
               id, ledger_id, name, reminder_kind, target_kind, target_id,
               condition_json, next_trigger_at, created_at, updated_at
           ) VALUES (
               'reminder-1', 'ledger-1', '现金低余额', 'account_balance',
               'account', 'account-1', '{"operator":"lt","amount_minor":1000}',
               '2026-08-01T09:00:00Z',
               '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO reminder_occurrences(
               id, reminder_id, trigger_at, condition_version,
               condition_snapshot_json, observed_value_json, status,
               created_at, updated_at
           ) VALUES (
               'reminder-occurrence-1', 'reminder-1', '2026-08-01T09:00:00Z', 1,
               '{"operator":"lt","amount_minor":1000}',
               '{"balance_minor":500,"currency_code":"CNY"}', 'pending',
               '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z'
           )"""
    )
    inbox = connection.execute(
        """SELECT source_kind, title, can_execute, can_skip
           FROM v_today_reminder_inbox ORDER BY source_kind"""
    ).fetchall()
    assert inbox == [
        ("reminder", "现金低余额", 0, 0),
        ("schedule", "每月餐饮计划", 1, 1),
    ], inbox

    connection.execute(
        """UPDATE schedule_occurrences
           SET status = 'executed', transaction_id = 'transaction-1',
               actioned_at = '2026-08-01T09:00:00Z',
               updated_at = '2026-08-01T09:00:00Z'
           WHERE id = 'schedule-occurrence-1'"""
    )
    assert connection.execute(
        """SELECT occurrence_count, executed_count, skipped_count, last_executed_at
           FROM v_schedule_lifecycle WHERE schedule_id = 'schedule-1'"""
    ).fetchone() == (1, 1, 0, "2026-08-01T09:00:00Z")

    try:
        connection.execute(
            """INSERT INTO schedule_occurrences(
                   id, schedule_id, due_date, recurrence_version, execution_mode,
                   status, source_snapshot_json, idempotency_key, actioned_at,
                   created_at, updated_at
               ) VALUES (
                   'schedule-occurrence-invalid', 'schedule-1', '2026-09-01', 1,
                   'manual', 'executed', '{}', 'schedule-1:2026-09-01:v1',
                   '2026-09-01T09:00:00Z',
                   '2026-08-01T00:00:00Z', '2026-08-01T00:00:00Z'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("已执行计划实例允许缺少关联交易")

    try:
        connection.execute(
            """UPDATE reminder_occurrences
               SET status = 'acknowledged', updated_at = '2026-08-01T09:00:00Z'
               WHERE id = 'reminder-occurrence-1'"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("已处理提醒实例允许缺少动作和处理时间")

    connection.execute(
        """INSERT INTO financial_goals(
               id, ledger_id, name, target_amount_minor, currency_code,
               target_date, progress_mode, created_at, updated_at,
               start_date, initial_value_minor, initial_value_captured_at,
               initial_inputs_json, account_scope_mode, progress_formula_version
           ) VALUES (
               'goal-1', 'ledger-1', '应急金', 100000, 'CNY',
               '2026-12-31', 'balance',
               '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z',
               '2026-07-28', 7500, '2026-07-28T00:00:00Z',
               '{"accounts":[{"account_id":"account-1","value_minor":7500}]}',
               'selected', 'pending-calibration-v1'
           )"""
    )
    connection.execute(
        """INSERT INTO financial_goal_accounts(goal_id, account_id)
           VALUES ('goal-1', 'account-1')"""
    )
    goal_result = connection.execute(
        """SELECT goal_id, start_date, target_date, initial_value_minor,
                  account_scope_mode, account_id, balance_minor
           FROM v_goal_progress_inputs WHERE goal_id = 'goal-1'"""
    ).fetchone()
    assert goal_result == (
        "goal-1",
        "2026-07-28",
        "2026-12-31",
        7500,
        "selected",
        "account-1",
        7500,
    ), goal_result

    try:
        connection.execute(
            "UPDATE financial_goals SET start_date = '2027-01-01' WHERE id = 'goal-1'"
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("财务目标不应接受晚于结束日期的开始日期")

    connection.execute(
        """INSERT INTO financial_plan_scenarios(
               id, ledger_id, name, base_year, schema_version, assumptions_json,
               created_at, updated_at
           ) VALUES (
               'plan-1', 'ledger-1', '家庭规划', 2026, 1,
               '{"inflation_rate_bps":250}',
               '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO financial_plan_inputs(
               id, scenario_id, topic, input_year, values_json, created_at, updated_at
           ) VALUES (
               'plan-input-1', 'plan-1', 'salary_income', 2026,
               '{"amount_minor":12000000,"currency":"CNY"}',
               '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO financial_plan_accounts(scenario_id, account_id, role)
           VALUES ('plan-1', 'account-1', 'included')"""
    )


def validate_contracts_exchange_and_sync(connection: sqlite3.Connection) -> None:
    """验证专属合同、导入审计、同步冲突和外部适配器边界。"""

    connection.execute(
        """INSERT INTO application_settings(
               id, scope_kind, ledger_id, setting_key, value_json, updated_at
           ) VALUES (
               'setting-1', 'ledger', 'ledger-1', 'ui.default_workspace',
               '{"workspace":"records"}', '2026-07-29T00:00:00Z'
           )"""
    )
    try:
        connection.execute(
            """INSERT INTO application_settings(
                   id, scope_kind, ledger_id, setting_key, value_json, updated_at
               ) VALUES (
                   'setting-invalid', 'application', 'ledger-1', 'invalid.scope',
                   '{}', '2026-07-29T00:00:00Z'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("应用级设置允许错误绑定账簿")

    connection.execute(
        """INSERT INTO debt_contracts(
               id, ledger_id, account_id, contract_kind, principal_minor,
               currency_code, annual_rate_units, annual_rate_scale,
               started_on, due_on, created_at, updated_at
           ) VALUES (
               'debt-1', 'ledger-1', 'account-1', 'personal_loan', 500000,
               'CNY', 450, 4, '2026-01-01', '2027-01-01',
               '2026-07-29T00:00:00Z', '2026-07-29T00:00:00Z'
           )"""
    )
    debt_input = connection.execute(
        """SELECT debt_contract_id, account_name, principal_minor, status
           FROM v_debt_contract_inputs WHERE debt_contract_id = 'debt-1'"""
    ).fetchone()
    assert debt_input == ("debt-1", "现金", 500000, "active"), debt_input

    try:
        connection.execute(
            """INSERT INTO credit_account_terms(
                   account_id, statement_day, due_day, updated_at
               ) VALUES ('account-1', 32, 20, '2026-07-29T00:00:00Z')"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("信用账户允许写入无效账单日")

    connection.execute(
        """INSERT INTO investment_instruments(
               id, ledger_id, code, name, kind, quote_currency_code,
               quantity_scale, price_scale
           ) VALUES (
               'instrument-future', 'ledger-1', 'IF2609', '股指期货测试',
               'future', 'CNY', 0, 2
           )"""
    )
    connection.execute(
        """INSERT INTO futures_contract_terms(
               instrument_id, contract_multiplier_units, contract_multiplier_scale,
               tick_size_units, tick_size_scale, settlement_kind, updated_at
           ) VALUES (
               'instrument-future', 300, 0, 20, 2, 'cash',
               '2026-07-29T00:00:00Z'
           )"""
    )

    connection.execute(
        """INSERT INTO import_field_mappings(
               id, ledger_id, source_kind, name, mapping_json,
               duplicate_rule_json, created_at, updated_at
           ) VALUES (
               'mapping-1', 'ledger-1', 'csv', '银行流水映射',
               '{"date":"交易日期","amount":"金额"}',
               '{"keys":["date","amount","memo"]}',
               '2026-07-29T00:00:00Z', '2026-07-29T00:00:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO import_batches(
               id, ledger_id, mapping_id, source_kind, source_display_name,
               source_sha256, total_rows, accepted_rows, rejected_rows,
               duplicate_rows, created_at
           ) VALUES (
               'import-1', 'ledger-1', 'mapping-1', 'csv', 'bank.csv',
               'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
               2, 1, 1, 0, '2026-07-29T00:00:00Z'
           )"""
    )
    connection.executemany(
        """INSERT INTO import_rows(
               id, batch_id, row_no, raw_json, normalized_json, error_json, row_status
           ) VALUES (?, 'import-1', ?, ?, ?, ?, ?)""",
        [
            (
                "import-row-1",
                1,
                '{"交易日期":"2026-07-01","金额":"100.00"}',
                '{"business_date":"2026-07-01","amount_minor":10000}',
                None,
                "accepted",
            ),
            (
                "import-row-2",
                2,
                '{"交易日期":"bad","金额":"x"}',
                None,
                '{"fields":{"business_date":"invalid","amount":"invalid"}}',
                "rejected",
            ),
        ],
    )
    import_audit = connection.execute(
        """SELECT total_rows, accepted_rows, rejected_rows, staged_row_count
           FROM v_import_batch_audit WHERE batch_id = 'import-1'"""
    ).fetchone()
    assert import_audit == (2, 1, 1, 2), import_audit

    try:
        connection.execute(
            """INSERT INTO import_rows(
                   id, batch_id, row_no, raw_json, row_status
               ) VALUES ('import-row-invalid', 'import-1', 3, '{invalid', 'pending')"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("导入行允许写入无效 raw_json")

    connection.execute(
        """INSERT INTO sync_profiles(
               id, ledger_id, provider_kind, display_name, device_id,
               config_json, status, created_at, updated_at
           ) VALUES (
               'sync-profile-1', 'ledger-1', 'test_adapter', '测试同步',
               'device-1', '{"endpoint_alias":"test"}', 'active',
               '2026-07-29T00:00:00Z', '2026-07-29T00:00:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO sync_batches(
               id, profile_id, direction, attempted_objects, succeeded_objects,
               failed_objects, conflict_objects, started_at
           ) VALUES (
               'sync-batch-1', 'sync-profile-1', 'bidirectional',
               1, 0, 0, 1, '2026-07-29T00:00:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO sync_conflicts(
               id, profile_id, entity_kind, entity_id, local_revision,
               remote_revision, local_json, remote_json, detected_at
           ) VALUES (
               'conflict-1', 'sync-profile-1', 'transaction', 'transaction-1',
               'local-1', 'remote-2', '{"theme":"本地"}', '{"theme":"远端"}',
               '2026-07-29T00:00:00Z'
           )"""
    )
    open_conflict = connection.execute(
        """SELECT conflict_id, ledger_id, entity_kind
           FROM v_open_sync_conflicts WHERE conflict_id = 'conflict-1'"""
    ).fetchone()
    assert open_conflict == ("conflict-1", "ledger-1", "transaction"), open_conflict

    connection.execute(
        """INSERT INTO notification_delivery_log(
               id, ledger_id, reminder_id, channel, delivery_status,
               requested_at, error_json
           ) VALUES (
               'delivery-1', 'ledger-1', 'reminder-1', 'in_app', 'sent',
               '2026-07-29T00:00:00Z', NULL
           )"""
    )
    connection.execute(
        """INSERT INTO fee_rule_snapshots(
               id, ledger_id, source_name, rule_kind, rate_units, rate_scale,
               parameters_json, captured_at
           ) VALUES (
               'fee-rule-1', 'ledger-1', 'mhlink.mdb', 'trade_commission',
               3, 4, '{"minimum_minor":500}', '2026-07-29T00:00:00Z'
           )"""
    )
    assert connection.execute("PRAGMA user_version").fetchone() == (13,)


def validate_insurance_cash_value(connection: sqlite3.Connection) -> None:
    """验证保险资金事件关联、失败回滚和现金价值独立性。"""

    connection.execute(
        """INSERT INTO accounts(
               id, ledger_id, name, kind, currency_code, is_asset, created_at
           ) VALUES
               ('insurance-policy-account', 'ledger-1', '测试保单', 'insurance',
                'CNY', 1, '2026-07-30T00:00:00Z'),
               ('insurance-cash-account', 'ledger-1', '保费现金', 'cash',
                'CNY', 1, '2026-07-30T00:00:00Z'),
               ('insurance-dividend-cash-account', 'ledger-1', '分红现金', 'cash',
                'CNY', 1, '2026-07-30T00:00:00Z'),
               ('insurance-surrender-keep-cash-account', 'ledger-1', '保留保单退保现金', 'cash',
                'CNY', 1, '2026-07-30T00:00:00Z'),
               ('insurance-surrender-cash-account', 'ledger-1', '退保现金', 'cash',
                'CNY', 1, '2026-07-30T00:00:00Z')"""
    )

    connection.execute(
        """INSERT INTO insurance_policies(
               id, ledger_id, account_id, policy_kind, currency_code,
               coverage_amount_minor, premium_amount_minor, started_on,
               created_at, updated_at
           ) VALUES (
               'policy-1', 'ledger-1', 'insurance-policy-account', 'whole_life', 'CNY',
               10000, 1000, '2026-07-30',
               '2026-07-30T00:00:00Z', '2026-07-30T00:00:00Z'
           )"""
    )
    transaction_count = connection.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()
    connection.execute(
        """INSERT INTO insurance_events(
               id, policy_id, event_kind, event_date, amount_minor,
               currency_code, source, created_at, updated_at
           ) VALUES (
               'insurance-event-opening', 'policy-1',
               'initial_premium_adjustment', '2026-07-30', 1000,
               'CNY', 'opening_wizard',
               '2026-07-30T00:00:00Z', '2026-07-30T00:00:00Z'
           )"""
    )
    assert connection.execute(
        """SELECT amount_minor, funding_transaction_id
           FROM insurance_events WHERE id = 'insurance-event-opening'"""
    ).fetchone() == (1000, None)
    connection.execute(
        """INSERT INTO insurance_cash_value_snapshots(
               policy_id, valuation_date, value_minor, source,
               version, created_at, updated_at
           ) VALUES (
               'policy-1', '2026-07-30', 0, 'opening', 1,
               '2026-07-30T00:00:00Z', '2026-07-30T00:00:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO transactions(
               id, ledger_id, sequence_no, business_date, occurred_at, kind,
               theme, created_at, updated_at
           ) VALUES
               ('insurance-cash-opening', 'ledger-1', 100, '2026-07-30',
                '2026-07-30T08:00:00Z', 'balance_adjustment', '现金期初余额',
                '2026-07-30T08:00:00Z', '2026-07-30T08:00:00Z'),
               ('insurance-premium-payment', 'ledger-1', 101, '2026-07-30',
                '2026-07-30T09:00:00Z', 'insurance_premium', '缴纳保费',
                '2026-07-30T09:00:00Z', '2026-07-30T09:00:00Z')"""
    )
    connection.executemany(
        """INSERT INTO transaction_entries(
               id, transaction_id, account_id, line_no, role, direction,
               amount_minor, currency_code, base_amount_minor, base_currency_code
           ) VALUES (?, ?, 'insurance-cash-account', 1, ?, ?, ?, 'CNY', ?, 'CNY')""",
        [
            (
                "insurance-cash-opening-entry",
                "insurance-cash-opening",
                "opening",
                "inflow",
                10000,
                10000,
            ),
            (
                "insurance-premium-payment-entry",
                "insurance-premium-payment",
                "primary",
                "outflow",
                1000,
                1000,
            ),
        ],
    )
    connection.execute(
        """INSERT INTO insurance_events(
               id, policy_id, funding_transaction_id, event_kind, event_date,
               amount_minor, currency_code, source, created_at, updated_at
           ) VALUES (
               'insurance-event-payment', 'policy-1', 'insurance-premium-payment',
               'premium_payment', '2026-07-30', 1000, 'CNY', 'manual',
               '2026-07-30T09:00:00Z', '2026-07-30T09:00:00Z'
           )"""
    )
    payment_projection = connection.execute(
        """SELECT e.amount_minor, e.funding_transaction_id, b.balance_minor,
                  (SELECT c.value_minor
                   FROM v_insurance_cash_value_effective_ranges c
                   WHERE c.policy_id = e.policy_id
                     AND c.effective_from <= '2026-07-31'
                     AND (c.effective_to_exclusive IS NULL
                          OR '2026-07-31' < c.effective_to_exclusive))
           FROM insurance_events e
           JOIN v_account_balances b
             ON b.account_id = 'insurance-cash-account'
           WHERE e.id = 'insurance-event-payment'"""
    ).fetchone()
    assert payment_projection == (
        1000,
        "insurance-premium-payment",
        9000,
        0,
    ), payment_projection

    # 返还是独立领取事件：增加资金账户余额和累计领取，不反向改写累计缴费或现金价值。
    connection.execute(
        """INSERT INTO transactions(
               id, ledger_id, sequence_no, business_date, occurred_at, kind,
               theme, created_at, updated_at
           ) VALUES (
               'insurance-premium-return', 'ledger-1', 102, '2026-07-30',
               '2026-07-30T09:30:00Z', 'insurance_premium', '保费返还',
               '2026-07-30T09:30:00Z', '2026-07-30T09:30:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO transaction_entries(
               id, transaction_id, account_id, line_no, role, direction,
               amount_minor, currency_code, base_amount_minor, base_currency_code
           ) VALUES (
               'insurance-premium-return-entry', 'insurance-premium-return',
               'insurance-cash-account', 1, 'primary', 'inflow',
               400, 'CNY', 400, 'CNY'
           )"""
    )
    connection.execute(
        """INSERT INTO insurance_events(
               id, policy_id, funding_transaction_id, event_kind, event_date,
               amount_minor, currency_code, source, created_at, updated_at
           ) VALUES (
               'insurance-event-return', 'policy-1', 'insurance-premium-return',
               'premium_return', '2026-07-30', 400, 'CNY', 'manual',
               '2026-07-30T09:30:00Z', '2026-07-30T09:30:00Z'
           )"""
    )
    return_projection = connection.execute(
        """SELECT
               SUM(CASE WHEN e.event_kind = 'premium_payment' THEN e.amount_minor ELSE 0 END),
               SUM(CASE WHEN e.event_kind = 'premium_return' THEN e.amount_minor ELSE 0 END),
               COUNT(*),
               (SELECT c.value_minor
                FROM v_insurance_cash_value_effective_ranges c
                WHERE c.policy_id = e.policy_id
                  AND c.effective_from <= '2026-07-31'
                  AND (c.effective_to_exclusive IS NULL
                       OR '2026-07-31' < c.effective_to_exclusive)),
               b.balance_minor
           FROM insurance_events e
           JOIN v_account_balances b ON b.account_id = 'insurance-cash-account'
           WHERE e.policy_id = 'policy-1'
             AND e.event_kind IN ('premium_payment', 'premium_return')"""
    ).fetchone()
    assert return_projection == (1000, 400, 2, 0, 9400), return_projection

    # 分红进入累计领取和通用资金流入，但必须保留 dividend 类型供收益报表单独聚合。
    connection.execute(
        """INSERT INTO transactions(
               id, ledger_id, sequence_no, business_date, occurred_at, kind,
               theme, created_at, updated_at
           ) VALUES (
               'insurance-dividend', 'ledger-1', 103, '2026-07-30',
               '2026-07-30T09:45:00Z', 'insurance_dividend', '保险分红',
               '2026-07-30T09:45:00Z', '2026-07-30T09:45:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO transaction_entries(
               id, transaction_id, account_id, line_no, role, direction,
               amount_minor, currency_code, base_amount_minor, base_currency_code
           ) VALUES (
               'insurance-dividend-entry', 'insurance-dividend',
               'insurance-dividend-cash-account', 1, 'primary', 'inflow',
               200, 'CNY', 200, 'CNY'
           )"""
    )
    connection.execute(
        """INSERT INTO insurance_events(
               id, policy_id, funding_transaction_id, event_kind, event_date,
               amount_minor, currency_code, source, created_at, updated_at
           ) VALUES (
               'insurance-event-dividend', 'policy-1', 'insurance-dividend',
               'dividend', '2026-07-30', 200, 'CNY', 'manual',
               '2026-07-30T09:45:00Z', '2026-07-30T09:45:00Z'
           )"""
    )
    dividend_projection = connection.execute(
        """SELECT
               SUM(CASE WHEN e.event_kind = 'premium_payment' THEN e.amount_minor ELSE 0 END),
               SUM(CASE WHEN e.event_kind IN ('premium_return', 'dividend')
                        THEN e.amount_minor ELSE 0 END),
               SUM(CASE WHEN e.event_kind = 'dividend' THEN e.amount_minor ELSE 0 END),
               COUNT(*),
               (SELECT c.value_minor
                FROM v_insurance_cash_value_effective_ranges c
                WHERE c.policy_id = e.policy_id
                  AND c.effective_from <= '2026-07-31'
                  AND (c.effective_to_exclusive IS NULL
                       OR '2026-07-31' < c.effective_to_exclusive)),
               b.balance_minor
           FROM insurance_events e
           JOIN v_account_balances b
             ON b.account_id = 'insurance-dividend-cash-account'
           WHERE e.policy_id = 'policy-1'
             AND e.event_kind IN ('premium_payment', 'premium_return', 'dividend')"""
    ).fetchone()
    assert dividend_projection == (1000, 600, 200, 3, 0, 200), dividend_projection

    # 退保资金事实和保单生命周期是两个动作：未勾选终止时仍需保留活动保单。
    connection.execute(
        """INSERT INTO transactions(
               id, ledger_id, sequence_no, business_date, occurred_at, kind,
               theme, created_at, updated_at
           ) VALUES (
               'insurance-surrender-keep-active', 'ledger-1', 104, '2026-07-31',
               '2026-07-31T00:10:00Z', 'insurance_surrender', '退保',
               '2026-07-31T00:10:00Z', '2026-07-31T00:10:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO transaction_entries(
               id, transaction_id, account_id, line_no, role, direction,
               amount_minor, currency_code, base_amount_minor, base_currency_code
           ) VALUES (
               'insurance-surrender-keep-entry', 'insurance-surrender-keep-active',
               'insurance-surrender-keep-cash-account', 1, 'primary', 'inflow',
               500, 'CNY', 500, 'CNY'
           )"""
    )
    connection.execute(
        """INSERT INTO insurance_events(
               id, policy_id, funding_transaction_id, event_kind, event_date,
               amount_minor, currency_code, source, details_json, created_at, updated_at
           ) VALUES (
               'insurance-event-surrender-keep', 'policy-1', 'insurance-surrender-keep-active',
               'surrender', '2026-07-31', 500, 'CNY', 'manual',
               '{"finish_account":false}',
               '2026-07-31T00:10:00Z', '2026-07-31T00:10:00Z'
           )"""
    )
    keep_active_projection = connection.execute(
        """SELECT e.amount_minor, e.funding_transaction_id,
                  json_extract(e.details_json, '$.finish_account'), p.status,
                  a.is_hidden, a.closed_on, b.balance_minor
           FROM insurance_events e
           JOIN insurance_policies p ON p.id = e.policy_id
           JOIN accounts a ON a.id = p.account_id
           JOIN v_account_balances b
             ON b.account_id = 'insurance-surrender-keep-cash-account'
           WHERE e.id = 'insurance-event-surrender-keep'"""
    ).fetchone()
    assert keep_active_projection == (
        500,
        "insurance-surrender-keep-active",
        0,
        "active",
        0,
        None,
        500,
    ), keep_active_projection

    # 只有显式勾选终止时才关闭账户；事件和选择必须保留，不能从当前状态反推历史意图。
    connection.execute(
        """INSERT INTO transactions(
               id, ledger_id, sequence_no, business_date, occurred_at, kind,
               theme, created_at, updated_at
           ) VALUES (
               'insurance-surrender', 'ledger-1', 105, '2026-07-31',
               '2026-07-31T00:20:00Z', 'insurance_surrender', '退保',
               '2026-07-31T00:20:00Z', '2026-07-31T00:20:00Z'
           )"""
    )
    connection.execute(
        """INSERT INTO transaction_entries(
               id, transaction_id, account_id, line_no, role, direction,
               amount_minor, currency_code, base_amount_minor, base_currency_code
           ) VALUES (
               'insurance-surrender-entry', 'insurance-surrender',
               'insurance-surrender-cash-account', 1, 'primary', 'inflow',
               500, 'CNY', 500, 'CNY'
           )"""
    )
    connection.execute(
        """INSERT INTO insurance_events(
               id, policy_id, funding_transaction_id, event_kind, event_date,
               amount_minor, currency_code, source, details_json, created_at, updated_at
           ) VALUES (
               'insurance-event-surrender', 'policy-1', 'insurance-surrender',
               'surrender', '2026-07-31', 500, 'CNY', 'manual',
               '{"finish_account":true}',
               '2026-07-31T00:20:00Z', '2026-07-31T00:20:00Z'
           )"""
    )
    connection.execute(
        """UPDATE insurance_policies
           SET status = 'surrendered', updated_at = '2026-07-31T00:20:00Z'
           WHERE id = 'policy-1'"""
    )
    connection.execute(
        """UPDATE accounts
           SET is_hidden = 1, closed_on = '2026-07-31'
           WHERE id = 'insurance-policy-account'"""
    )
    surrender_projection = connection.execute(
        """SELECT e.amount_minor, e.funding_transaction_id,
                  json_extract(e.details_json, '$.finish_account'), p.status,
                  a.is_hidden, a.closed_on, b.balance_minor
           FROM insurance_events e
           JOIN insurance_policies p ON p.id = e.policy_id
           JOIN accounts a ON a.id = p.account_id
           JOIN v_account_balances b
             ON b.account_id = 'insurance-surrender-cash-account'
           WHERE e.id = 'insurance-event-surrender'"""
    ).fetchone()
    assert surrender_projection == (
        500,
        "insurance-surrender",
        1,
        "surrendered",
        1,
        "2026-07-31",
        500,
    ), surrender_projection
    assert connection.execute(
        """SELECT COUNT(*) FROM insurance_policies p
           JOIN accounts a ON a.id = p.account_id
           WHERE p.id = 'policy-1'
             AND p.status = 'active'
             AND a.is_hidden = 0
             AND a.closed_on IS NULL"""
    ).fetchone() == (0,)
    assert connection.execute(
        """SELECT COUNT(*) FROM insurance_events
           WHERE policy_id = 'policy-1'"""
    ).fetchone() == (6,)

    # 保费交易和保险事件必须由应用层包在同一事务中，事件校验失败不能留下资金流水。
    connection.execute("SAVEPOINT insurance_payment_failure")
    try:
        connection.execute(
            """INSERT INTO transactions(
                   id, ledger_id, sequence_no, business_date, occurred_at, kind,
                   theme, created_at, updated_at
               ) VALUES (
                   'insurance-premium-rollback', 'ledger-1', 106, '2026-07-30',
                   '2026-07-30T10:00:00Z', 'insurance_premium', '失败保费',
                   '2026-07-30T10:00:00Z', '2026-07-30T10:00:00Z'
               )"""
        )
        connection.execute(
            """INSERT INTO transaction_entries(
                   id, transaction_id, account_id, line_no, role, direction,
                   amount_minor, currency_code, base_amount_minor, base_currency_code
               ) VALUES (
                   'insurance-premium-rollback-entry', 'insurance-premium-rollback',
                   'insurance-cash-account', 1, 'primary', 'outflow',
                   1000, 'CNY', 1000, 'CNY'
               )"""
        )
        connection.execute(
            """INSERT INTO insurance_events(
                   id, policy_id, funding_transaction_id, event_kind, event_date,
                   amount_minor, currency_code, created_at, updated_at
               ) VALUES (
                   'insurance-event-rollback', 'policy-1',
                   'insurance-premium-rollback', 'unknown', '2026-07-30',
                   1000, 'CNY', '2026-07-30T10:00:00Z', '2026-07-30T10:00:00Z'
               )"""
        )
    except sqlite3.IntegrityError:
        connection.execute("ROLLBACK TO insurance_payment_failure")
        connection.execute("RELEASE insurance_payment_failure")
    else:
        connection.execute("RELEASE insurance_payment_failure")
        raise AssertionError("保险事件校验失败后仍提交了资金交易")
    assert connection.execute(
        """SELECT COUNT(*) FROM transactions
           WHERE id = 'insurance-premium-rollback'"""
    ).fetchone() == (0,)
    assert connection.execute(
        """SELECT balance_minor FROM v_account_balances
           WHERE account_id = 'insurance-cash-account'"""
    ).fetchone() == (9400,)

    connection.execute(
        """INSERT INTO insurance_cash_value_snapshots(
               policy_id, valuation_date, value_minor, source,
               version, created_at, updated_at
           ) VALUES (
               'policy-1', '2026-07-30', 800, 'manual', 1,
               '2026-07-30T00:00:00Z', '2026-07-30T01:00:00Z'
           )
           ON CONFLICT(policy_id, valuation_date) DO UPDATE SET
               value_minor = excluded.value_minor,
               source = excluded.source,
               version = insurance_cash_value_snapshots.version + 1,
               updated_at = excluded.updated_at"""
    )
    connection.execute(
        """UPDATE insurance_cash_value_snapshots
           SET value_minor = 900, version = version + 1,
               updated_at = '2026-07-30T02:00:00Z'
           WHERE policy_id = 'policy-1' AND valuation_date = '2026-07-30'"""
    )
    current = insurance_cash_value_as_of(connection, "policy-1", "2026-07-31")
    assert current == (900, 3), current
    assert connection.execute(
        "SELECT COUNT(*) FROM insurance_cash_value_snapshots WHERE policy_id = 'policy-1'"
    ).fetchone() == (1,)
    history = connection.execute(
        """SELECT operation, value_minor, previous_value_minor, version
           FROM insurance_cash_value_history
           WHERE policy_id = 'policy-1' ORDER BY version"""
    ).fetchall()
    assert history == [
        ("insert", 0, None, 1),
        ("update", 800, 0, 2),
        ("update", 900, 800, 3),
    ], history
    assert connection.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone() == (transaction_count[0] + 6,)

    # 现金价值为非负估值；目标库拒绝旧程序把负数静默转换成零的行为。
    try:
        connection.execute(
            """INSERT INTO insurance_cash_value_snapshots(
                   policy_id, valuation_date, value_minor, source,
                   version, created_at, updated_at
               ) VALUES (
                   'policy-1', '2026-07-28', -100, 'manual', 1,
                   '2026-07-28T00:00:00Z', '2026-07-28T00:00:00Z'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("现金价值允许写入负数")
    assert connection.execute(
        """SELECT COUNT(*) FROM insurance_cash_value_snapshots
           WHERE policy_id = 'policy-1' AND valuation_date = '2026-07-28'"""
    ).fetchone() == (0,)

    try:
        connection.execute(
            """UPDATE insurance_cash_value_snapshots
               SET value_minor = -1, version = version + 1,
                   updated_at = '2026-07-30T02:30:00Z'
               WHERE policy_id = 'policy-1' AND valuation_date = '2026-07-30'"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("现金价值允许修改为负数")
    assert insurance_cash_value_as_of(connection, "policy-1", "2026-07-31") == (
        900,
        3,
    )

    try:
        connection.execute(
            """INSERT INTO insurance_events(
                   id, policy_id, event_kind, event_date, amount_minor,
                   currency_code, created_at, updated_at
               ) VALUES (
                   'insurance-event-invalid', 'policy-1', 'unknown',
                   '2026-07-30', 100, 'CNY',
                   '2026-07-30T00:00:00Z', '2026-07-30T00:00:00Z'
               )"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("保险事件允许未知业务类型")

    try:
        connection.execute(
            """UPDATE insurance_cash_value_snapshots
               SET value_minor = 1000, updated_at = '2026-07-30T03:00:00Z'
               WHERE policy_id = 'policy-1' AND valuation_date = '2026-07-30'"""
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("现金价值修改允许跳过版本递增")

    # 删除最新日期必须从剩余事实确定性回退，不能保留独立的当前值缓存。
    connection.execute(
        """INSERT INTO insurance_cash_value_snapshots(
               policy_id, valuation_date, value_minor, source,
               version, created_at, updated_at
           ) VALUES (
               'policy-1', '2026-07-31', 1300, 'manual', 1,
               '2026-07-31T00:00:00Z', '2026-07-31T00:00:00Z'
           )"""
    )
    assert insurance_cash_value_as_of(connection, "policy-1", "2026-07-31") == (
        1300,
        1,
    )

    # 删除任意非最新日期只移除历史点，当前现金价值仍由最大估值日快照决定。
    connection.execute(
        """INSERT INTO insurance_cash_value_snapshots(
               policy_id, valuation_date, value_minor, source,
               version, created_at, updated_at
           ) VALUES (
               'policy-1', '2026-07-29', 700, 'manual', 1,
               '2026-07-29T00:00:00Z', '2026-07-29T00:00:00Z'
           )"""
    )
    connection.execute(
        """DELETE FROM insurance_cash_value_snapshots
           WHERE policy_id = 'policy-1' AND valuation_date = '2026-07-29'"""
    )
    assert insurance_cash_value_as_of(connection, "policy-1", "2026-07-31") == (
        1300,
        1,
    )
    nonlatest_delete_history = connection.execute(
        """SELECT operation, value_minor, previous_value_minor, version
           FROM insurance_cash_value_history
           WHERE policy_id = 'policy-1' AND valuation_date = '2026-07-29'
           ORDER BY id DESC LIMIT 1"""
    ).fetchone()
    assert nonlatest_delete_history == ("delete", None, 700, 2), nonlatest_delete_history

    # 未来快照进入时间序列但不提前影响查询时点；到达估值日后才成为有效值。
    connection.execute(
        """INSERT INTO insurance_cash_value_snapshots(
               policy_id, valuation_date, value_minor, source,
               version, created_at, updated_at
           ) VALUES (
               'policy-1', '2026-08-01', 1500, 'manual', 1,
               '2026-08-01T00:00:00Z', '2026-08-01T00:00:00Z'
           )"""
    )
    assert insurance_cash_value_as_of(connection, "policy-1", "2026-07-31") == (
        1300,
        1,
    )
    assert insurance_cash_value_as_of(connection, "policy-1", "2026-08-01") == (
        1500,
        1,
    )
    connection.execute(
        """DELETE FROM insurance_cash_value_snapshots
           WHERE policy_id = 'policy-1' AND valuation_date = '2026-08-01'"""
    )
    future_delete_history = connection.execute(
        """SELECT operation, value_minor, previous_value_minor, version
           FROM insurance_cash_value_history
           WHERE policy_id = 'policy-1' AND valuation_date = '2026-08-01'
           ORDER BY id DESC LIMIT 1"""
    ).fetchone()
    assert future_delete_history == ("delete", None, 1500, 2), future_delete_history

    # 大额金额仍以整数最小单位精确保存，不能复制旧程序十一位整数发生分币进位的缺陷。
    exact_large_minor = 9_999_999_999_999
    connection.execute(
        """INSERT INTO insurance_cash_value_snapshots(
               policy_id, valuation_date, value_minor, source,
               version, created_at, updated_at
           ) VALUES (
               'policy-1', '2026-08-02', ?, 'manual', 1,
               '2026-08-02T00:00:00Z', '2026-08-02T00:00:00Z'
           )""",
        (exact_large_minor,),
    )
    assert insurance_cash_value_as_of(connection, "policy-1", "2026-08-02") == (
        exact_large_minor,
        1,
    )
    connection.execute(
        """DELETE FROM insurance_cash_value_snapshots
           WHERE policy_id = 'policy-1' AND valuation_date = '2026-08-02'"""
    )
    assert connection.execute(
        """SELECT previous_value_minor
           FROM insurance_cash_value_history
           WHERE policy_id = 'policy-1' AND valuation_date = '2026-08-02'
             AND operation = 'delete'"""
    ).fetchone() == (exact_large_minor,)

    connection.execute(
        """DELETE FROM insurance_cash_value_snapshots
           WHERE policy_id = 'policy-1' AND valuation_date = '2026-07-31'"""
    )
    assert insurance_cash_value_as_of(connection, "policy-1", "2026-07-31") == (
        900,
        3,
    )
    latest_date_delete_history = connection.execute(
        """SELECT operation, value_minor, previous_value_minor, version
           FROM insurance_cash_value_history
           WHERE policy_id = 'policy-1' AND valuation_date = '2026-07-31'
           ORDER BY id DESC LIMIT 1"""
    ).fetchone()
    assert latest_date_delete_history == ("delete", None, 1300, 2), latest_date_delete_history
    assert connection.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone() == (transaction_count[0] + 6,)

    # 旧程序删除唯一快照后出现表格为零、余额跨重启漂移的缺陷；目标库只从剩余快照重建所有投影。
    connection.execute(
        """DELETE FROM insurance_cash_value_snapshots
           WHERE policy_id = 'policy-1' AND valuation_date = '2026-07-30'"""
    )
    assert connection.execute(
        "SELECT COUNT(*) FROM insurance_cash_value_snapshots WHERE policy_id = 'policy-1'"
    ).fetchone() == (0,)
    assert insurance_cash_value_as_of(connection, "policy-1", "2026-07-31") is None
    assert connection.execute(
        """SELECT COALESCE((SELECT value_minor
                            FROM v_insurance_cash_value_effective_ranges
                            WHERE policy_id = 'policy-1'
                              AND effective_from <= '2026-07-31'
                              AND (effective_to_exclusive IS NULL
                                   OR '2026-07-31' < effective_to_exclusive)), 0)"""
    ).fetchone() == (0,)

    # 删除估值事实不能改写保险事件或资金交易，缴费和领取口径由各自事件独立聚合。
    assert connection.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone() == (transaction_count[0] + 6,)
    delete_history = connection.execute(
        """SELECT operation, value_minor, previous_value_minor, version
           FROM insurance_cash_value_history
           WHERE policy_id = 'policy-1' ORDER BY id DESC LIMIT 1"""
    ).fetchone()
    assert delete_history == ("delete", None, 900, 4), delete_history


def main() -> int:
    connection = sqlite3.connect(":memory:")
    try:
        for migration in migration_paths():
            connection.executescript(migration.read_text(encoding="utf-8"))
        validate_schema(connection)
        seed_minimal_ledger(connection)
        validate_party_list_lifecycle(connection)
        validate_prepaid_expenses(connection)
        validate_deposit_rates(connection)
        validate_projections(connection)
        validate_planning_and_automation(connection)
        validate_contracts_exchange_and_sync(connection)
        validate_insurance_cash_value(connection)
        validate_transfer_and_atomic_rollback(connection)
        validate_constraints(connection)
        validate_destructive_operation_constraints(connection)
        validate_payroll_income(connection)
    finally:
        connection.close()
    print("SQLite schema validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
