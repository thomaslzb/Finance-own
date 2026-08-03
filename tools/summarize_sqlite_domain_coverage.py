"""审计运行时实体候选与当前 SQLite 迁移的覆盖关系。"""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[1]
DOCS_DIR = WORKSPACE / "docs"
MIGRATIONS_DIR = WORKSPACE / "migrations"
EVENT_DATAFLOW_PATH = DOCS_DIR / "runtime-event-command-dataflow.json"
OUTPUT_JSON_PATH = DOCS_DIR / "sqlite-domain-coverage-audit.json"
OUTPUT_MD_PATH = DOCS_DIR / "sqlite-domain-coverage-audit.md"


def contract(
    status: str,
    current_objects: list[str],
    next_objects: list[str],
    rationale: str,
    adapter_artifacts: list[str] | None = None,
) -> dict[str, Any]:
    """创建单个实体候选的数据库覆盖合同。"""

    return {
        "status": status,
        "current_objects": current_objects,
        "next_objects": next_objects,
        "adapter_artifacts": adapter_artifacts or [],
        "rationale": rationale,
    }


COVERAGE_CONTRACTS = {
    "transaction": contract(
        "implemented_truth",
        [
            "transactions",
            "transaction_entries",
            "payroll_income_details",
            "payroll_category_components",
            "payroll_social_contributions",
            "v_payroll_income_reconciliation",
        ],
        [],
        "交易头和原子账户分录是真相来源；工资复合交易使用类型化扩展保存收入、扣款和社保组成。",
    ),
    "account": contract("implemented_truth", ["accounts"], [], "账户树与余额投影已落地。"),
    "position": contract("implemented_input_projection", ["v_investment_position_inputs"], [], "持仓输入已落地，成本和收益率等待动态校准。"),
    "investment_transaction": contract("implemented_generic_truth", ["transactions", "investment_trades"], [], "投资业务复用交易头并保存专属成交扩展。"),
    "quote": contract("implemented_truth", ["market_quotes"], [], "行情按标的、时点和来源保存。"),
    "application_setting": contract("implemented_truth", ["application_settings"], [], "应用级与账簿级设置使用带版本 JSON，并由作用域约束隔离。"),
    "attachment": contract("implemented_truth", ["attachments", "transaction_attachments"], [], "附件元数据与业务关系分离并受引用保护。"),
    "category": contract("implemented_truth", ["categories"], [], "分类树和方向已落地。"),
    "account_entry": contract("implemented_truth", ["transaction_entries"], [], "所有余额变化统一由原子分录表达。"),
    "category_split": contract("implemented_generic_truth", ["transaction_entries"], [], "分类拆分使用同一交易的多条稳定分录。"),
    "currency": contract("implemented_truth", ["currencies"], [], "币种精度与启用状态已落地。"),
    "tag": contract("implemented_truth", ["tags", "transaction_tags", "account_tags"], [], "标签同时关联流水和账户。"),
    "account_group": contract("implemented_truth", ["account_groups", "accounts"], [], "删除分组只解除账户关系。"),
    "person": contract("implemented_truth", ["parties"], [], "人员和机构使用统一参与方模型。"),
    "ledger": contract("implemented_truth", ["ledgers"], [], "SQLite 单文件账簿是真相边界。"),
    "debt": contract("implemented_contract_boundary", ["accounts", "transactions", "transaction_entries", "debt_contracts", "v_debt_contract_inputs"], [], "资金流由分录表达，借款期限、利率和状态由专属合同表承载。"),
    "backup_snapshot": contract(
        "adapter_boundary",
        [],
        [],
        "备份是文件适配器和校验清单，不进入活动账簿；Schema 明确快照、哈希、模式版本和附件相对路径。",
        ["backup-manifest.schema.json", "backup-manifest-template.json"],
    ),
    "reminder": contract("implemented_truth", ["schedules", "schedule_occurrences", "reminders", "reminder_occurrences", "v_schedule_lifecycle", "v_today_reminder_inbox"], [], "计划定义、逐次执行实例、提醒规则、触发实例和今日收件箱已分层落地。"),
    "financial_plan": contract("implemented_truth", ["financial_plan_scenarios", "financial_plan_inputs", "financial_plan_accounts"], [], "规划输入采用带版本 JSON，公式仍由 Rust 策略校准。"),
    "budget": contract("implemented_truth", ["budgets", "budget_items", "v_budget_consumption_inputs"], [], "预算期间、分类金额和消耗输入已落地。"),
    "fund": contract("implemented_generic_truth", ["investment_instruments", "investment_trades", "market_quotes"], [], "基金通过 kind 和类型化策略复用投资真相表。"),
    "credit_account": contract("implemented_contract_boundary", ["accounts", "transactions", "credit_account_terms"], [], "账户和流水是真相，账单日、还款日、额度和计息输入由专属条款承载。"),
    "repayment": contract("implemented_generic_truth", ["transactions", "transaction_entries"], [], "收款和还款均由平衡账户分录表达。"),
    "financial_goal": contract("implemented_truth", ["financial_goals", "financial_goal_accounts", "v_goal_account_balance_inputs", "v_goal_progress_inputs"], [], "目标金额、起止日期、账户范围、初始估值快照和进度输入已落地。"),
    "security": contract("implemented_generic_truth", ["investment_instruments", "investment_trades", "market_quotes"], [], "证券通过投资标的、成交和行情表达。"),
    "futures_contract": contract("implemented_contract_boundary", ["investment_instruments", "investment_trades", "market_quotes", "futures_contract_terms"], [], "成交和行情复用投资真相，合约乘数、保证金和交割输入由专属条款承载。"),
    "metal_position": contract("implemented_generic_truth", ["investment_instruments", "investment_trades", "market_quotes"], [], "黄金和贵金属持仓复用投资真相表。"),
    "tangible_asset": contract("implemented_contract_boundary", ["investment_instruments", "market_quotes", "tangible_asset_details"], [], "资产标识和估值复用投资真相，购置输入和专属属性由扩展表承载。"),
    "valuation": contract("implemented_generic_truth", ["market_quotes"], [], "市场与人工估值统一保存为带来源的时点价格。"),
    "tool_input": contract("transient_not_persisted", [], [], "工具输入属于临时页面状态。"),
    "tool_result": contract("transient_not_persisted", [], [], "计算器和辅助工具结果默认不进入账簿真相。"),
    "presentation_state": contract("transient_not_persisted", [], [], "选择、焦点、加载和展开状态属于展示层。"),
    "financing_transaction": contract("implemented_contract_boundary", ["transactions", "investment_trades", "margin_contracts"], [], "融资资金流和证券成交复用真相表，额度、期限和利率由合同扩展承载。"),
    "margin_account": contract("implemented_contract_boundary", ["accounts", "margin_account_terms"], [], "账户主体与融资融券风险条款已经分离落地。"),
    "export_projection": contract("transient_not_persisted", ["v_ledger_entries", "report_presets"], [], "导出消费查询 DTO，不单独保存复制数据。"),
    "field_mapping": contract("implemented_truth", ["import_field_mappings"], [], "导入列映射、重复规则和版本已可复用并审计。"),
    "import_batch": contract("implemented_truth", ["import_batches", "v_import_batch_audit"], [], "导入来源哈希、状态、计数和提交结果已形成批次真相。"),
    "raw_row": contract("implemented_truth", ["import_rows", "v_import_batch_audit"], [], "原始行、规范化结果、字段错误和最终对象标识可逐行追溯。"),
    "financial_product": contract("implemented_generic_truth", ["investment_instruments", "investment_trades", "market_quotes"], [], "银行理财和货币产品复用投资标的与成交模型。"),
    "bond": contract("implemented_generic_truth", ["investment_instruments", "investment_trades", "market_quotes"], [], "债券基础交易复用投资真相表，票息细则可由后续类型扩展补充。"),
    "insurance_policy": contract("implemented_contract_boundary", ["insurance_policies", "insurance_events", "insurance_cash_value_snapshots", "insurance_cash_value_history", "v_insurance_cash_value_effective_ranges", "transactions", "transaction_entries"], [], "保障条款、保险业务事件、可审计现金价值估值与可选资金交易分离；同日估值使用唯一键 upsert，当前值按显式查询日选择生效区间。"),
    "social_security_account": contract("implemented_contract_boundary", ["accounts", "transactions", "social_security_profiles"], [], "账户和缴费流水是真相，地区、基数和规则快照由专属输入表承载。"),
    "report_filter": contract("implemented_truth", ["report_presets"], [], "筛选和图表序列以校验 JSON 保存。"),
    "report_projection": contract("implemented_input_projection", ["v_ledger_entries", "v_account_balances", "v_investment_position_inputs"], [], "报表查询输入已落地，专用公式仍由 Rust 计算策略提供。"),
    "report_query": contract("implemented_input_projection", ["report_presets", "v_ledger_entries"], [], "保存条件与查询投影分离。"),
    "notification": contract("implemented_truth", ["reminders", "reminder_occurrences", "v_today_reminder_inbox", "notification_delivery_log"], [], "提醒规则、触发实例、统一收件箱与投递重试日志已经分离。"),
    "sync_batch": contract("implemented_truth", ["sync_batches", "sync_object_results", "sync_conflicts", "sync_tombstones", "v_open_sync_conflicts"], [], "同步批次、对象结果、冲突和删除传播已经形成审计真相。"),
    "user_identity": contract("adapter_boundary", ["sync_profiles"], [], "登录身份属于可选同步适配器；本地只保存非秘密配置，不阻塞本地账簿。"),
    "exchange_rate": contract("implemented_truth", ["exchange_rate_snapshots"], [], "历史折算使用不可变汇率快照。"),
    "fx_transaction": contract("implemented_generic_truth", ["transactions", "transaction_entries", "exchange_rate_snapshots"], [], "跨币种分录引用明确汇率快照。"),
    "fee_rule": contract("adapter_boundary", ["fee_rule_snapshots"], [], "旧参考费率以来源快照进入适配器边界，交易仍保存实际费用分录。"),
    "investment_object": contract("implemented_truth", ["investment_instruments"], [], "所有投资品使用稳定标的标识和 kind。"),
    "report": contract("implemented_input_projection", ["report_presets"], [], "报表定义由代码和预设组成，不复制结果真相。"),
}


def schema_objects() -> tuple[set[str], set[str], set[str]]:
    """执行全部迁移并读取最终模式，避免把已替换对象重复计数。"""

    connection = sqlite3.connect(":memory:")
    try:
        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            connection.executescript(path.read_text(encoding="utf-8"))

        def names(object_type: str) -> set[str]:
            return {
                str(row[0])
                for row in connection.execute(
                    """SELECT name FROM sqlite_schema
                       WHERE type = ? AND name NOT LIKE 'sqlite_%'""",
                    (object_type,),
                )
            }

        return names("table"), names("view"), names("index")
    finally:
        connection.close()


def build_audit() -> dict[str, Any]:
    """合并事件出现次数、当前对象和后续迁移建议。"""

    dataflow = json.loads(EVENT_DATAFLOW_PATH.read_text(encoding="utf-8"))
    occurrence_counts = Counter(
        entity
        for command in dataflow["commands"]
        for entity in command.get("entity_candidates", [])
    )
    candidates = set(occurrence_counts)
    missing_contracts = sorted(candidates - set(COVERAGE_CONTRACTS))
    stale_contracts = sorted(set(COVERAGE_CONTRACTS) - candidates)
    if missing_contracts or stale_contracts:
        raise SystemExit(
            f"实体覆盖合同不一致：缺少 {missing_contracts}，多余 {stale_contracts}"
        )

    tables, views, indexes = schema_objects()
    known_objects = tables | views | indexes
    rows = []
    for entity in sorted(candidates):
        item = dict(COVERAGE_CONTRACTS[entity])
        unresolved_current = sorted(set(item["current_objects"]) - known_objects)
        if unresolved_current:
            raise SystemExit(f"{entity} 引用了不存在的当前对象：{unresolved_current}")
        unresolved_artifacts = sorted(
            name
            for name in item["adapter_artifacts"]
            if not (DOCS_DIR / name).is_file()
        )
        if unresolved_artifacts:
            raise SystemExit(
                f"{entity} 引用了不存在的适配器产物：{unresolved_artifacts}"
            )
        rows.append(
            {
                "entity_candidate": entity,
                "event_occurrence_count": occurrence_counts[entity],
                **item,
            }
        )

    status_counts = Counter(row["status"] for row in rows)
    next_object_counts = Counter(
        next_object for row in rows for next_object in row["next_objects"]
    )
    adapter_artifacts = {
        artifact for row in rows for artifact in row["adapter_artifacts"]
    }
    return {
        "schema_version": 1,
        "sources": [
            EVENT_DATAFLOW_PATH.name,
            *[path.name for path in sorted(MIGRATIONS_DIR.glob("*.sql"))],
        ],
        "evidence_boundary": (
            "实体候选来自事件静态分类；覆盖状态是新 SQLite 设计审计。"
            "partial 或 missing 项不能在对应动态样例和迁移验证前标记为行为兼容。"
        ),
        "metrics": {
            "entity_candidate_count": len(rows),
            "table_count": len(tables),
            "view_count": len(views),
            "index_count": len(indexes),
            "adapter_artifact_count": len(adapter_artifacts),
            "status_counts": dict(status_counts),
            "recommended_next_object_count": len(next_object_counts),
        },
        "recommended_next_objects": [
            {"name": name, "referenced_by_entity_count": count}
            for name, count in sorted(next_object_counts.items())
        ],
        "entities": rows,
    }


def render_markdown(audit: dict[str, Any]) -> str:
    """生成数据库覆盖结论和后续迁移分组。"""

    metrics = audit["metrics"]
    status_labels = {
        "implemented_truth": "已落地真相表",
        "implemented_generic_truth": "由通用真相表承载",
        "implemented_input_projection": "已落地输入投影",
        "implemented_contract_boundary": "已落地专属合同边界",
        "partial_existing": "部分覆盖，需专属扩展",
        "planned_missing": "后续迁移缺口",
        "adapter_boundary": "适配器或文件边界",
        "transient_not_persisted": "临时状态，不持久化",
    }
    lines = [
        "# SQLite 领域覆盖审计",
        "",
        "本文档把 `2000` 个事件中出现的 `53` 类实体候选与当前 SQLite 迁移逐项对照。",
        "它用于防止核心交易表验证通过后，误以为预算、提醒、导入、同步和专属资产合同也已经完成。",
        "",
        "## 1. 当前规模",
        "",
        "| 项目 | 数量 |",
        "| --- | ---: |",
        f"| 实体候选 | {metrics['entity_candidate_count']} |",
        f"| SQLite 表 | {metrics['table_count']} |",
        f"| SQLite 视图 | {metrics['view_count']} |",
        f"| SQLite 索引 | {metrics['index_count']} |",
        f"| 适配器文件产物 | {metrics['adapter_artifact_count']} |",
        f"| 建议后续对象 | {metrics['recommended_next_object_count']} |",
        "",
        "状态分布：",
        "",
    ]
    for status, count in sorted(metrics["status_counts"].items()):
        lines.append(f"- `{status}`（{status_labels[status]}）：{count}")
    lines.extend(
        [
            "",
            "## 2. 实体逐项覆盖",
            "",
            "| 实体候选 | 事件出现 | 状态 | 当前 SQLite 对象 | 文件/适配器产物 | 后续对象 |",
            "| --- | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in audit["entities"]:
        lines.append(
            "| `{entity}` | {count} | `{status}` | {current} | {artifacts} | {next_objects} |".format(
                entity=row["entity_candidate"],
                count=row["event_occurrence_count"],
                status=row["status"],
                current=", ".join(f"`{name}`" for name in row["current_objects"]) or "-",
                artifacts=", ".join(f"`{name}`" for name in row["adapter_artifacts"]) or "-",
                next_objects=", ".join(f"`{name}`" for name in row["next_objects"]) or "-",
            )
        )
    lines.extend(
        [
            "",
            "## 3. 已落地边界与剩余外部对象",
            "",
            "### 3.1 债务、信用和专属资产合同",
            "",
            "- `debt_contracts`, `credit_account_terms`, `futures_contract_terms`",
            "- `margin_contracts`, `margin_account_terms`",
            "- `insurance_policies`, `social_security_profiles`, `tangible_asset_details`",
            "",
            "这些表已经落地，只保存通用交易模型不能表达的合同条款；资金变化仍必须进入 `transactions + transaction_entries`。",
            "",
            "### 3.2 导入审计",
            "",
            "- `import_batches`, `import_rows`, `import_field_mappings`",
            "",
            "来源显示名与哈希、映射版本、逐行错误、重复判断和最终提交对象已经可以追溯。",
            "",
            "### 3.3 同步与通知",
            "",
            "- `sync_profiles`, `sync_batches`, `sync_object_results`, `sync_conflicts`, `sync_tombstones`",
            "- `notification_delivery_log`",
            "",
            "同步批次、对象结果、冲突和墓碑已落地；本地账簿始终独立可用，网络秘密不进入核心领域表。",
            "",
            "### 3.4 设置与参考规则",
            "",
            "- `application_settings`",
            "- `fee_rule_snapshots`",
            "- `backup-manifest.schema.json` 与 `backup-manifest-template.json` 作为账簿外文件清单合同，不放入活动数据库",
            "",
            "### 3.5 工资收入扩展",
            "",
            "- `payroll_income_details`",
            "- `payroll_category_components`",
            "- `payroll_social_contributions`",
            "- `v_payroll_income_reconciliation`",
            "",
            "工资仍属于运行时 `transaction` 实体，但收入、扣款、个人缴费和公司缴费不能压缩成一条普通收入分录。第七版迁移增加类型化扩展，并把实收现金和社保权益与账户分录做确定性核对。",
            "",
            "### 3.6 待摊费用扩展",
            "",
            "- `prepaid_expenses`",
            "- `prepaid_expense_installments`",
            "- `v_prepaid_expense_overview`",
            "",
            "待摊费用账户、原始金额、人员、项目和摊销参数由专属表承载；每一期保存确定金额和幂等交易引用，资金变化仍必须进入 `transactions + transaction_entries`。",
            "",
            "## 4. 结论",
            "",
            "`0001_core.sql` 已覆盖账户、交易、标签、汇率、附件、投资输入和报表预设；",
            "`0002_planning_and_automation.sql` 已补模板计划、预算、提醒、目标和规划输入。",
            "`0003_contracts_exchange_and_sync.sql` 已补专属合同、导入审计、同步冲突、通知投递、设置和费率快照。",
            "`0007_payroll_income_and_application_identity.sql` 已补工资收入组成、账户投影核对和 Finance Own SQLite 文件标识。",
            "`0010_prepaid_expenses.sql` 已补待摊费用主体、分期计划和剩余金额查询投影。",
            "数据库与账簿外文件实体均已形成可执行或可验证合同，不需要复制旧 Jet 表结构。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    """生成 JSON 和 Markdown 数据库覆盖审计。"""

    audit = build_audit()
    OUTPUT_JSON_PATH.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    OUTPUT_MD_PATH.write_text(
        render_markdown(audit), encoding="utf-8", newline="\n"
    )
    metrics = audit["metrics"]
    print(
        "SQLite 领域覆盖审计完成："
        f"{metrics['entity_candidate_count']} 个实体候选，"
        f"{metrics['table_count']} 表 / {metrics['view_count']} 视图"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
