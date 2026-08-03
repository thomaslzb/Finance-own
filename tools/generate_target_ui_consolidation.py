"""生成旧 MoneyHome8 窗体到 Rust 目标页面族的全量归并映射。"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[1]
DOCS_DIR = WORKSPACE / "docs"
EXECUTION_QUEUE_PATH = DOCS_DIR / "runtime-execution-queue.json"
EVENT_DATAFLOW_PATH = DOCS_DIR / "runtime-event-command-dataflow.json"
OUTPUT_JSON_PATH = DOCS_DIR / "target-ui-consolidation-map.json"
OUTPUT_MD_PATH = DOCS_DIR / "target-ui-consolidation-map.md"


INVESTMENT_DOMAINS = {
    "financial_products",
    "foreign_exchange",
    "investment_shared",
    "securities",
    "funds",
    "bonds",
    "futures_metals",
    "margin_financing",
    "insurance_social",
    "major_tangible_assets",
}

SECTION_BY_DOMAIN = {
    "system_shell": "ledger_shell",
    "accounts_master_data": "accounts_master_data",
    "transactions": "transactions",
    "debts_credit": "debts_credit",
    "planning_budget_goal": "planning",
    "reports": "reports",
    "import_export": "data_exchange",
    "auth_sync_external": "sync",
    "tools_longtail": "tools",
    "shared_infrastructure": "shared_ui",
}

SECTION_ORDER = [
    "ledger_shell",
    "accounts_master_data",
    "transactions",
    "debts_credit",
    "investments",
    "planning",
    "reports",
    "data_exchange",
    "sync",
    "tools",
    "shared_ui",
]

SECTION_LABELS = {
    "ledger_shell": "账簿与应用壳层",
    "accounts_master_data": "账户与基础资料",
    "transactions": "通用交易",
    "debts_credit": "债权债务与信用",
    "investments": "投资与扩展资产",
    "planning": "预算、提醒、规划与目标",
    "reports": "报表与分析",
    "data_exchange": "导入导出",
    "sync": "同步与外部服务",
    "tools": "辅助工具",
    "shared_ui": "共享 UI 组件",
}

SECTION_ROUTES = {
    "ledger_shell": "/",
    "accounts_master_data": "/accounts",
    "transactions": "/transactions",
    "debts_credit": "/debts",
    "investments": "/investments",
    "planning": "/planning",
    "reports": "/reports",
    "data_exchange": "/data-exchange",
    "sync": "/sync",
    "tools": "/tools",
    "shared_ui": "component://shared",
}

SECTION_MODULES = {
    "ledger_shell": ["ledger", "app::ledger", "ui::shell"],
    "accounts_master_data": ["accounts", "master_data", "ui::accounts"],
    "transactions": ["transactions", "app::transactions", "ui::transactions"],
    "debts_credit": ["investments::debt", "transactions", "ui::debts"],
    "investments": ["investments", "reports", "ui::investments"],
    "planning": ["planning", "ui::planning"],
    "reports": ["reports", "app::reporting", "ui::reports"],
    "data_exchange": ["import_export", "ui::import_export"],
    "sync": ["sync", "ui::sync"],
    "tools": ["tools", "ui::tools"],
    "shared_ui": ["app::command_state", "ui::shared"],
}

ROLE_TARGETS = {
    "application_shell": ("shell", "应用壳层", "full_page_shell", "ShellCoordinator"),
    "ledger_lifecycle": ("ledger-workflow", "账簿生命周期", "wizard_or_dialog", "LedgerLifecycleService"),
    "external_adapter": ("adapter-workspace", "外部适配器", "settings_and_status_page", "ExternalAdapterService"),
    "data_exchange": ("exchange-workflow", "数据交换", "guided_workflow", "DataExchangeService"),
    "report_projection": ("report-workspace", "报表工作区", "report_definition", "ReportQueryService"),
    "projection_view": ("overview", "概览与投影", "page_or_embedded_panel", "ProjectionQueryService"),
    "transaction_editor": ("entry", "业务录入", "form_drawer_or_dialog", "TransactionCommandService"),
    "transaction_history": ("history", "流水与历史", "data_grid_page", "TransactionQueryService"),
    "account_editor": ("account-workflow", "账户配置", "wizard_or_drawer", "AccountCommandService"),
    "catalog_editor": ("catalog", "目录与基础资料", "management_page", "CatalogService"),
    "planning_workflow": ("workflow", "规划工作流", "guided_workflow", "PlanningService"),
    "selector_filter": ("selector", "选择器与筛选", "shared_selector", "SelectionQueryService"),
    "configuration_editor": ("settings", "配置", "settings_page_or_dialog", "SettingsService"),
    "tool_window": ("tool", "工具", "tool_dialog", "ToolService"),
    "shared_infrastructure": ("component", "共享组件", "shared_component", "SharedUiService"),
}


def read_json(path: Path) -> dict[str, Any]:
    """读取 UTF-8 JSON 输入证据。"""

    if not path.is_file():
        raise SystemExit(f"缺少输入证据：{path}")
    return json.loads(path.read_text(encoding="utf-8"))


def section_for(domain: str) -> str:
    """把投资子域归并到共享投资工作区，其余域保持稳定边界。"""

    if domain in INVESTMENT_DOMAINS:
        return "investments"
    try:
        return SECTION_BY_DOMAIN[domain]
    except KeyError as error:
        raise SystemExit(f"缺少目标 UI 分区映射：{domain}") from error


def target_for(form: dict[str, Any]) -> dict[str, str]:
    """计算单个旧窗体对应的目标页面族和 Rust 应用服务。"""

    section = section_for(form["domain"])
    try:
        role_slug, role_label, ui_pattern, app_service = ROLE_TARGETS[form["role"]]
    except KeyError as error:
        raise SystemExit(f"缺少目标 UI 角色映射：{form['role']}") from error
    route_root = SECTION_ROUTES[section]
    route = (
        f"{route_root}/{role_slug}"
        if route_root != "/" and not route_root.startswith("component://")
        else f"{route_root.rstrip('/')}/{role_slug}"
    )
    return {
        "target_surface_id": f"ui.{section}.{role_slug}",
        "section": section,
        "section_label": SECTION_LABELS[section],
        "target_name": f"{SECTION_LABELS[section]} - {role_label}",
        "route_or_component": route,
        "ui_pattern": ui_pattern,
        "application_service": app_service,
    }


def migration_decision(form: dict[str, Any]) -> str:
    """说明旧窗体在新 UI 中是合并、嵌入、保留还是范围化处理。"""

    surface_kind = form["surface_kind"]
    if surface_kind == "embedded_indirect_surface":
        return "merge_into_host_surface"
    if surface_kind == "technical_support":
        return "replace_with_shared_component"
    if surface_kind == "internal_or_experimental":
        return "diagnostic_or_optional_adapter_scope"
    return "merge_into_target_surface_family"


def merge_rationale(role: str) -> str:
    """给出按交互角色合并而非逐窗体复刻的设计原因。"""

    rationales = {
        "application_shell": "统一导航、当前账簿上下文和全局命令状态。",
        "ledger_lifecycle": "新建、打开、备份和还原共享文件选择、校验、进度和失败恢复。",
        "external_adapter": "登录、同步和行情属于可选适配器，不能阻塞本地财务功能。",
        "data_exchange": "导入导出共享来源、映射、预览、错误和批次提交状态机。",
        "report_projection": "旧报表保留为报表定义，表格、图表、导出和打印复用同一查询 DTO。",
        "projection_view": "列表、统计和图表共享查询投影，并按业务域参数化。",
        "transaction_editor": "收入、支出和各投资活动共享命令壳层，领域规则由资产类型策略提供。",
        "transaction_history": "流水页共享日期、筛选、选择、批量操作和稳定排序。",
        "account_editor": "账户向导共享步骤框架，账户类型只提供字段与规则差异。",
        "catalog_editor": "基础资料和投资品目录共享搜索、新增、编辑、引用保护和停用行为。",
        "planning_workflow": "预算、诊断、规划和目标共享分步输入、计算、保存和结果展示。",
        "selector_filter": "选择器不保存业务真相，只返回稳定标识和筛选条件。",
        "configuration_editor": "配置统一处理脏状态、校验、保存、取消和默认值恢复。",
        "tool_window": "长尾工具保持独立命令但复用统一对话框与输入输出边界。",
        "shared_infrastructure": "技术窗体不作为业务页面复刻，由可测试共享组件替代。",
    }
    return rationales[role]


def build_mapping() -> dict[str, Any]:
    """构建目标页面族和逐窗体追溯映射。"""

    queue = read_json(EXECUTION_QUEUE_PATH)
    dataflow = read_json(EVENT_DATAFLOW_PATH)
    events_by_resource: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in dataflow["commands"]:
        events_by_resource[event["resource"]].append(event)

    mappings: list[dict[str, Any]] = []
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for form in queue["forms"]:
        target = target_for(form)
        events = events_by_resource.get(form["resource"], [])
        entity_candidates = sorted(
            {
                entity
                for event in events
                for entity in event.get("entity_candidates", [])
            }
        )
        mapping = {
            "execution_id": form["execution_id"],
            "resource": form["resource"],
            "class_name": form["class_name"],
            "title": form["title"],
            "source_domain": form["domain"],
            "source_domain_label": form["domain_label"],
            "source_role": form["role"],
            "surface_kind": form["surface_kind"],
            "target_surface_id": target["target_surface_id"],
            "route_or_component": target["route_or_component"],
            "ui_pattern": target["ui_pattern"],
            "rust_modules": SECTION_MODULES[target["section"]],
            "application_service": target["application_service"],
            "migration_decision": migration_decision(form),
            "actionable_command_count": len(form["actionable_commands"]),
            "event_handler_count": len(form["event_handlers"]),
            "high_risk_event_count": form["high_risk_event_count"],
            "entity_candidates": entity_candidates,
            "dynamic_execution_status": form["status"],
        }
        mappings.append(mapping)
        groups[target["target_surface_id"]].append(
            {"form": form, "events": events, "mapping": mapping, "target": target}
        )

    targets = []
    for target_surface_id, items in groups.items():
        first = items[0]
        target = first["target"]
        forms = [item["form"] for item in items]
        events = [event for item in items for event in item["events"]]
        source_domains = sorted({form["domain"] for form in forms})
        targets.append(
            {
                "target_surface_id": target_surface_id,
                "section": target["section"],
                "section_label": target["section_label"],
                "target_name": target["target_name"],
                "route_or_component": target["route_or_component"],
                "ui_pattern": target["ui_pattern"],
                "source_role": forms[0]["role"],
                "rust_modules": SECTION_MODULES[target["section"]],
                "application_service": target["application_service"],
                "merge_rationale": merge_rationale(forms[0]["role"]),
                "source_domains": source_domains,
                "source_domain_labels": sorted({form["domain_label"] for form in forms}),
                "old_form_count": len(forms),
                "actionable_command_count": sum(
                    len(form["actionable_commands"]) for form in forms
                ),
                "event_handler_count": sum(len(form["event_handlers"]) for form in forms),
                "high_risk_event_count": sum(
                    form["high_risk_event_count"] for form in forms
                ),
                "surface_kind_counts": dict(
                    Counter(form["surface_kind"] for form in forms)
                ),
                "data_direction_counts": dict(
                    Counter(event["data_direction"] for event in events)
                ),
                "rust_boundary_counts": dict(
                    Counter(event["rust_boundary"] for event in events)
                ),
                "entity_candidates": sorted(
                    {
                        entity
                        for event in events
                        for entity in event.get("entity_candidates", [])
                    }
                ),
                "states_to_capture": list(
                    dict.fromkeys(
                        state for form in forms for state in form["states_to_capture"]
                    )
                ),
                "execution_ids": [form["execution_id"] for form in forms],
                "old_resources": [form["resource"] for form in forms],
            }
        )

    section_rank = {section: index for index, section in enumerate(SECTION_ORDER)}
    targets.sort(key=lambda item: (section_rank[item["section"]], item["target_surface_id"]))
    mappings.sort(key=lambda item: item["execution_id"])

    section_summaries = []
    for section in SECTION_ORDER:
        section_targets = [target for target in targets if target["section"] == section]
        if not section_targets:
            continue
        section_summaries.append(
            {
                "section": section,
                "section_label": SECTION_LABELS[section],
                "target_surface_count": len(section_targets),
                "old_form_count": sum(item["old_form_count"] for item in section_targets),
                "actionable_command_count": sum(
                    item["actionable_command_count"] for item in section_targets
                ),
                "event_handler_count": sum(
                    item["event_handler_count"] for item in section_targets
                ),
                "high_risk_event_count": sum(
                    item["high_risk_event_count"] for item in section_targets
                ),
                "rust_modules": SECTION_MODULES[section],
            }
        )

    metrics = {
        "source_form_count": len(mappings),
        "target_section_count": len(section_summaries),
        "target_surface_family_count": len(targets),
        "actionable_command_count": sum(
            item["actionable_command_count"] for item in targets
        ),
        "event_handler_count": sum(item["event_handler_count"] for item in targets),
        "high_risk_event_count": sum(item["high_risk_event_count"] for item in targets),
        "investment_source_domain_count": len(INVESTMENT_DOMAINS),
        "investment_source_form_count": sum(
            mapping["source_domain"] in INVESTMENT_DOMAINS for mapping in mappings
        ),
        "mapping_decision_counts": dict(
            Counter(mapping["migration_decision"] for mapping in mappings)
        ),
    }
    expected = queue["metrics"]
    reconciliations = {
        "source_form_count": expected["form_count"],
        "actionable_command_count": expected["actionable_command_count"],
        "event_handler_count": expected["event_handler_count"],
        "high_risk_event_count": expected["high_risk_event_count"],
    }
    for metric, value in reconciliations.items():
        if metrics[metric] != value:
            raise SystemExit(
                f"目标 UI 映射对账失败：{metric}={metrics[metric]}，期望 {value}"
            )
    if len({mapping["execution_id"] for mapping in mappings}) != len(mappings):
        raise SystemExit("目标 UI 映射存在重复 execution_id")

    return {
        "schema_version": 1,
        "sources": [EXECUTION_QUEUE_PATH.name, EVENT_DATAFLOW_PATH.name],
        "design_status": "proposed_modern_consolidation_with_full_legacy_traceability",
        "design_boundary": (
            "目标页面族是 Rust 产品设计决策，不是旧程序运行事实。旧窗体可以合并，"
            "但命令、字段、状态、数据流和动态验收条目必须全部追溯。"
        ),
        "metrics": metrics,
        "sections": section_summaries,
        "target_surfaces": targets,
        "legacy_form_mappings": mappings,
    }


def render_markdown(mapping: dict[str, Any]) -> str:
    """输出面向产品、设计和 Rust 开发的归并摘要。"""

    metrics = mapping["metrics"]
    lines = [
        "# MoneyHome8 旧窗体到 Rust 目标 UI 归并图",
        "",
        "本设计不按 Delphi 的 `460` 个窗体逐一复刻。新系统按稳定业务边界组织页面，",
        "但通过 `execution_id` 保留每个旧窗体、命令、事件和动态验收结果的完整追溯。",
        "",
        "## 1. 归并结果",
        "",
        "| 项目 | 数量 |",
        "| --- | ---: |",
        f"| 旧运行时窗体 | {metrics['source_form_count']} |",
        f"| Rust 目标分区 | {metrics['target_section_count']} |",
        f"| 目标页面族 | {metrics['target_surface_family_count']} |",
        f"| 可交互控件守恒 | {metrics['actionable_command_count']} |",
        f"| 事件处理器守恒 | {metrics['event_handler_count']} |",
        f"| 高风险事件守恒 | {metrics['high_risk_event_count']} |",
        f"| 归入共享投资框架的旧子域 / 窗体 | {metrics['investment_source_domain_count']} / {metrics['investment_source_form_count']} |",
        "",
        "完整逐窗体映射见 [target-ui-consolidation-map.json](C:\\DCG-SZ\\SZ-System-Docs\\CodexWorkSpace\\Finance-own\\docs\\target-ui-consolidation-map.json)。",
        "",
        "## 2. 设计原则",
        "",
        "- 旧窗体是证据和验收来源，不是新架构的模块边界。",
        "- 证券、基金、债券、外汇、期货、贵金属、保险和重大资产共享投资账户、交易、流水、统计和配置页面框架。",
        "- 各投资子域通过资产类型、字段定义、校验策略、费用策略和计算策略表达差异，不复制整套 UI。",
        "- `28` 个报表窗体归入报表工作区，继续保留独立报表定义、列、筛选、分组、图表和导出合同。",
        "- 技术支撑窗体改为共享组件；嵌入视图并入已确认宿主；内部或实验入口单独作范围决策。",
        "- 合并页面不能删除旧命令；每个 `execution_id` 都必须在动态队列中关闭。",
        "",
        "## 3. 目标分区",
        "",
        "| 分区 | 目标页面族 | 旧窗体 | 控件 | 事件 | 高风险 | Rust 模块 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for section in mapping["sections"]:
        lines.append(
            "| {label} | {targets} | {forms} | {commands} | {events} | {risks} | `{modules}` |".format(
                label=section["section_label"],
                targets=section["target_surface_count"],
                forms=section["old_form_count"],
                commands=section["actionable_command_count"],
                events=section["event_handler_count"],
                risks=section["high_risk_event_count"],
                modules="`, `".join(section["rust_modules"]),
            )
        )
    lines.extend(
        [
            "",
            "## 4. 目标页面族",
            "",
            "| 目标页面族 | UI 形态 | 旧窗体 | 控件 / 事件 / 高风险 | 应用服务 |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    for target in mapping["target_surfaces"]:
        lines.append(
            "| `{surface}`<br>{name} | `{pattern}`<br>`{route}` | {forms} | {commands} / {events} / {risks} | `{service}` |".format(
                surface=target["target_surface_id"],
                name=target["target_name"],
                pattern=target["ui_pattern"],
                route=target["route_or_component"],
                forms=target["old_form_count"],
                commands=target["actionable_command_count"],
                events=target["event_handler_count"],
                risks=target["high_risk_event_count"],
                service=target["application_service"],
            )
        )
    lines.extend(
        [
            "",
            "## 5. 开发和验收约束",
            "",
            "1. 每个目标页面族使用应用服务访问领域和仓储，UI 不直接写 SQLite。",
            "2. 同一页面族中的资产类型差异通过类型化策略或专属扩展对象表达，不使用所有字段可空的大对象。",
            "3. `legacy_form_mappings` 是功能一致性的追溯基线；合并页面完成时必须列出覆盖的全部 `execution_id`。",
            "4. 动态执行记录未关闭前，目标页面族只能标记为结构覆盖，不能标记为行为兼容。",
            "5. 页面族的 Rust 模块和应用服务是建议边界；动态结果可调整规则，但不能丢弃旧功能证据。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    """生成 JSON 追溯图和 Markdown 产品设计摘要。"""

    mapping = build_mapping()
    OUTPUT_JSON_PATH.write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    OUTPUT_MD_PATH.write_text(
        render_markdown(mapping), encoding="utf-8", newline="\n"
    )
    metrics = mapping["metrics"]
    print(
        "目标 UI 归并完成："
        f"{metrics['source_form_count']} 个旧窗体 -> "
        f"{metrics['target_surface_family_count']} 个页面族 / "
        f"{metrics['target_section_count']} 个分区"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
