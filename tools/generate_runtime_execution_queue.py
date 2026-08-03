"""生成 MoneyHome8 全量动态页面与命令执行队列。"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[1]
DOCS_DIR = WORKSPACE / "docs"
FORM_COVERAGE_PATH = DOCS_DIR / "runtime-form-coverage-audit.json"
COMMAND_STATE_PATH = DOCS_DIR / "runtime-command-state-evidence.json"
EVENT_DATAFLOW_PATH = DOCS_DIR / "runtime-event-command-dataflow.json"
COMPOSITION_PATH = DOCS_DIR / "runtime-form-composition-evidence.json"
OUTPUT_JSON_PATH = DOCS_DIR / "runtime-execution-queue.json"
OUTPUT_MD_PATH = DOCS_DIR / "runtime-execution-queue.md"
RUNTIME_ARTIFACT_DIR = WORKSPACE / "artifacts" / "runtime-validation"


DOMAIN_ORDER = [
    "system_shell",
    "accounts_master_data",
    "transactions",
    "debts_credit",
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
    "planning_budget_goal",
    "reports",
    "import_export",
    "auth_sync_external",
    "tools_longtail",
    "shared_infrastructure",
]

ROLE_STATES = {
    "ledger_lifecycle": ["初始", "输入有效", "输入无效", "成功", "取消", "失败恢复"],
    "external_adapter": ["离线", "就绪", "执行中", "取消", "网络失败", "重试"],
    "data_exchange": ["未选择文件", "文件已加载", "预览", "部分错误", "提交成功", "回滚"],
    "report_projection": ["空数据", "有数据", "筛选已修改", "加载中", "结果", "导出或打印"],
    "projection_view": ["空数据", "有数据", "未选择", "单选", "多选", "筛选结果"],
    "transaction_editor": ["初始", "有效输入", "校验错误", "保存成功", "取消", "失败回滚"],
    "transaction_history": ["空数据", "有数据", "未选择", "单选", "多选", "筛选结果"],
    "account_editor": ["初始", "有效输入", "校验错误", "保存成功", "取消", "引用保护"],
    "catalog_editor": ["空数据", "有数据", "新增", "编辑", "引用保护", "停用或删除"],
    "planning_workflow": ["空数据", "有数据", "输入中", "计算结果", "校验错误", "清除前"],
    "selector_filter": ["空选项", "有选项", "未选择", "已选择", "已清除"],
    "configuration_editor": ["初始", "已修改", "校验错误", "保存成功", "取消"],
    "tool_window": ["初始", "有效输入", "无效输入", "结果", "取消"],
    "application_shell": ["初始", "菜单展开", "导航完成", "无账簿", "已打开账簿"],
    "shared_infrastructure": ["宿主调用", "正常返回", "取消", "失败"],
}

HIGH_PRIORITY_ROLES = {
    "ledger_lifecycle",
    "data_exchange",
    "report_projection",
    "transaction_editor",
    "account_editor",
    "planning_workflow",
}

COMPLETION_REQUIREMENTS = [
    "入口和导航路径已记录",
    "页面、字段、默认值和可见状态已记录",
    "命令初始状态、触发方式、提示和结果已记录",
    "写入前后数据、余额、关联对象和文件副作用已记录",
    "空数据、有数据、校验失败和取消路径按适用范围执行",
    "截图、导出、日志或文件证据已落到 runtime-validation 目录",
    "结果已回填功能目录、数据流、PRD 和验收标准",
]


def read_json(path: Path) -> dict[str, Any]:
    """读取生成队列所需的 UTF-8 JSON 证据。"""

    if not path.is_file():
        raise SystemExit(f"缺少输入证据：{path}")
    return json.loads(path.read_text(encoding="utf-8"))


def priority_for(form: dict[str, Any], high_risk_count: int) -> str:
    """根据业务副作用和表面类型确定动态执行优先级。"""

    if form["surface_kind"] == "internal_or_experimental":
        return "P0"
    if high_risk_count or form["role"] in HIGH_PRIORITY_ROLES:
        return "P0"
    if form["surface_kind"] in {"business_surface", "embedded_indirect_surface"}:
        return "P1"
    return "P2"


def entry_strategy_for(
    form: dict[str, Any], composition: dict[str, Any] | None
) -> str:
    """说明旧窗体应直接打开、通过宿主观察还是只做间接验证。"""

    surface_kind = form["surface_kind"]
    if surface_kind == "embedded_indirect_surface":
        hosts = (composition or {}).get("ultimate_hosts", [])
        return f"通过最终宿主打开：{', '.join(hosts) if hosts else '待确认宿主'}"
    if surface_kind == "internal_or_experimental":
        return "搜索菜单、快捷键和条件分支，验证真实可达性"
    if surface_kind == "technical_support":
        return "通过业务宿主间接触发，记录正常、取消和失败路径"
    return "从菜单、导航、上下文命令或所属业务流程直接进入"


def states_for(form: dict[str, Any], high_risk_count: int) -> list[str]:
    """为每类窗体给出最小但可复现的页面状态集合。"""

    states = list(ROLE_STATES.get(form["role"], ["初始", "正常", "失败", "取消"]))
    if high_risk_count:
        states.extend(["确认前", "取消确认", "确认后", "执行失败或回滚"])
    return list(dict.fromkeys(states))


def compact_event(event: dict[str, Any], high_risk_ids: set[str]) -> dict[str, Any]:
    """保留动态执行和 Rust 需求回填真正需要的事件字段。"""

    return {
        "command_id": event["command_id"],
        "handler": event["handler"],
        "primary_intent": event["primary_intent"],
        "all_intents": event["all_intents"],
        "data_direction": event["data_direction"],
        "rust_boundary": event["rust_boundary"],
        "confidence": event["confidence"],
        "code_status": event["code_status"],
        "is_noop": event["is_noop"],
        "high_risk": event["command_id"] in high_risk_ids,
    }


def load_observation_records() -> dict[str, dict[str, Any]]:
    """读取每个执行条目的最新结构化观察记录。"""

    latest: dict[str, dict[str, Any]] = {}
    if not RUNTIME_ARTIFACT_DIR.is_dir():
        return latest
    for path in sorted(RUNTIME_ARTIFACT_DIR.glob("RT-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        execution_id = record.get("execution_id")
        observed_at = record.get("observed_at")
        result = record.get("result", {})
        if not execution_id or not observed_at or not result.get("status"):
            raise SystemExit(f"动态观察记录缺少关键字段：{path}")
        current = latest.get(execution_id)
        if current is None or observed_at > current["observed_at"]:
            latest[execution_id] = {
                "path": str(path.relative_to(WORKSPACE)),
                "observed_at": observed_at,
                "status": result["status"],
                "summary": result.get("summary", ""),
                "resource": record.get("resource"),
            }
    return latest


def build_queue() -> dict[str, Any]:
    """合并窗体、命令状态、事件数据流和宿主关系。"""

    coverage = read_json(FORM_COVERAGE_PATH)
    command_state = read_json(COMMAND_STATE_PATH)
    event_dataflow = read_json(EVENT_DATAFLOW_PATH)
    composition = read_json(COMPOSITION_PATH)

    commands_by_resource = {
        item["resource"]: item for item in command_state["forms"]
    }
    events_by_resource: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in event_dataflow["commands"]:
        events_by_resource[event["resource"]].append(event)
    composition_by_resource = {
        item["resource"]: item for item in composition["embedded_views"]
    }
    high_risk_ids = {
        event["command_id"] for event in event_dataflow["high_risk_commands"]
    }
    observation_records = load_observation_records()
    domain_rank = {domain: index for index, domain in enumerate(DOMAIN_ORDER, start=1)}

    forms: list[dict[str, Any]] = []
    ordered_forms = sorted(
        coverage["forms"],
        key=lambda form: (
            domain_rank.get(form["domain"], 999),
            form["surface_kind"],
            form["resource"],
        ),
    )
    domain_sequence: Counter[str] = Counter()
    for form in ordered_forms:
        domain = form["domain"]
        domain_sequence[domain] += 1
        events = events_by_resource.get(form["resource"], [])
        high_risk_count = sum(event["command_id"] in high_risk_ids for event in events)
        command_form = commands_by_resource.get(
            form["resource"], {"commands": [], "option_lists": [], "stateful_controls": []}
        )
        handler_ids: dict[str, list[str]] = defaultdict(list)
        for event in events:
            handler_ids[event["handler"]].append(event["command_id"])

        actionable_commands = []
        for command in command_form["commands"]:
            related_handlers = list(
                dict.fromkeys(
                    handler_id
                    for handler in command["events"].values()
                    for handler_id in handler_ids.get(handler, [])
                )
            )
            actionable_commands.append(
                {
                    "component": command["component"],
                    "path": command["path"],
                    "component_class": command["class"],
                    "label": command["label"],
                    "events": command["events"],
                    "shortcut": command["shortcut"],
                    "initial_state": command["state"],
                    "related_event_ids": related_handlers,
                    "high_risk": any(item in high_risk_ids for item in related_handlers),
                }
            )

        composition_item = composition_by_resource.get(form["resource"])
        batch_number = domain_rank.get(domain, 99)
        execution_id = f"RT-{batch_number:02d}-{domain_sequence[domain]:03d}"
        observation_record = observation_records.get(execution_id)
        if observation_record and observation_record["resource"] != form["resource"]:
            raise SystemExit(
                f"动态观察记录资源不匹配：{execution_id} 应为 {form['resource']}，"
                f"实际为 {observation_record['resource']}"
            )
        forms.append(
            {
                "execution_id": execution_id,
                "batch_id": f"B{batch_number:02d}-{domain}",
                "priority": priority_for(form, high_risk_count),
                "status": (observation_record or {}).get("status", "pending"),
                "resource": form["resource"],
                "class_name": form["class"],
                "title": form["title"],
                "domain": domain,
                "domain_label": form["domain_label"],
                "role": form["role"],
                "role_label": form["role_label"],
                "surface_kind": form["surface_kind"],
                "structure_status": form["structure_status"],
                "existing_dynamic_status": form["dynamic_result_status"],
                "static_data_flow": form["data_flow"],
                "entry_strategy": entry_strategy_for(form, composition_item),
                "direct_parents": (composition_item or {}).get("direct_parents", []),
                "ultimate_hosts": (composition_item or {}).get("ultimate_hosts", []),
                "fields": form["fields"],
                "tabs": form["tabs"],
                "options": form["options"],
                "states_to_capture": states_for(form, high_risk_count),
                "actionable_commands": actionable_commands,
                "stateful_controls": command_form["stateful_controls"],
                "option_lists": command_form["option_lists"],
                "event_handlers": [
                    compact_event(event, high_risk_ids)
                    for event in sorted(events, key=lambda item: item["command_id"])
                ],
                "high_risk_event_count": high_risk_count,
                "completion_requirements": COMPLETION_REQUIREMENTS,
                "observation_record": observation_record,
            }
        )

    batch_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for form in forms:
        batch_groups[form["batch_id"]].append(form)
    batches = []
    for batch_id, batch_forms in batch_groups.items():
        first = batch_forms[0]
        batches.append(
            {
                "batch_id": batch_id,
                "order": domain_rank.get(first["domain"], 99),
                "domain": first["domain"],
                "domain_label": first["domain_label"],
                "form_count": len(batch_forms),
                "actionable_command_count": sum(
                    len(form["actionable_commands"]) for form in batch_forms
                ),
                "event_handler_count": sum(
                    len(form["event_handlers"]) for form in batch_forms
                ),
                "high_risk_event_count": sum(
                    form["high_risk_event_count"] for form in batch_forms
                ),
                "surface_counts": dict(
                    Counter(form["surface_kind"] for form in batch_forms)
                ),
                "priority_counts": dict(Counter(form["priority"] for form in batch_forms)),
            }
        )
    batches.sort(key=lambda item: item["order"])

    metrics = {
        "batch_count": len(batches),
        "form_count": len(forms),
        "actionable_command_count": sum(
            len(form["actionable_commands"]) for form in forms
        ),
        "event_handler_count": sum(len(form["event_handlers"]) for form in forms),
        "high_risk_event_count": sum(form["high_risk_event_count"] for form in forms),
        "forms_with_high_risk_events": sum(
            form["high_risk_event_count"] > 0 for form in forms
        ),
        "embedded_form_count": sum(
            form["surface_kind"] == "embedded_indirect_surface" for form in forms
        ),
        "embedded_forms_with_hosts": sum(
            form["surface_kind"] == "embedded_indirect_surface"
            and bool(form["ultimate_hosts"])
            for form in forms
        ),
        "status_counts": dict(Counter(form["status"] for form in forms)),
        "priority_counts": dict(Counter(form["priority"] for form in forms)),
    }
    expected_metrics = {
        "form_count": coverage["metrics"]["runtime_form_count"],
        "actionable_command_count": command_state["metrics"]["command_count"],
        "event_handler_count": event_dataflow["metrics"]["command_count"],
        "high_risk_event_count": event_dataflow["metrics"]["high_risk_command_count"],
        "embedded_form_count": composition["metrics"]["embedded_surface_count"],
        "embedded_forms_with_hosts": composition["metrics"][
            "embedded_surface_with_parent_count"
        ],
    }
    for metric, expected in expected_metrics.items():
        if metrics[metric] != expected:
            raise SystemExit(
                f"执行队列对账失败：{metric}={metrics[metric]}，期望 {expected}"
            )

    return {
        "schema_version": 1,
        "sources": [
            FORM_COVERAGE_PATH.name,
            COMMAND_STATE_PATH.name,
            EVENT_DATAFLOW_PATH.name,
            COMPOSITION_PATH.name,
        ],
        "evidence_boundary": (
            "该队列保证静态范围逐项可执行，不代表页面或副作用已经动态验证；"
            "只有 observation_record 完成并回填需求文档后才能关闭条目。"
        ),
        "artifact_directory": str(RUNTIME_ARTIFACT_DIR),
        "record_schema": "runtime-observation-record.schema.json",
        "record_template": "runtime-observation-record-template.md",
        "metrics": metrics,
        "batches": batches,
        "forms": forms,
    }


def render_markdown(queue: dict[str, Any]) -> str:
    """生成便于人工执行和审阅的批次摘要。"""

    metrics = queue["metrics"]
    lines = [
        "# MoneyHome8 全量动态执行队列",
        "",
        "本队列把静态证据转换为逐窗体可勾选的动态巡检工作。它不以代表性场景替代全量覆盖，",
        "并要求每次运行结果使用统一记录 Schema 保存到 `artifacts/runtime-validation/`。",
        "",
        "## 1. 覆盖对账",
        "",
        "| 项目 | 数量 |",
        "| --- | ---: |",
        f"| 执行批次 | {metrics['batch_count']} |",
        f"| 运行时窗体 | {metrics['form_count']} |",
        f"| 可交互控件 | {metrics['actionable_command_count']} |",
        f"| 事件处理器 | {metrics['event_handler_count']} |",
        f"| 高风险事件候选 | {metrics['high_risk_event_count']} |",
        f"| 含高风险事件的窗体 | {metrics['forms_with_high_risk_events']} |",
        f"| 嵌入视图及已解析宿主 | {metrics['embedded_form_count']} / {metrics['embedded_forms_with_hosts']} |",
        "",
        "机器可执行明细见 [runtime-execution-queue.json](C:\\DCG-SZ\\SZ-System-Docs\\CodexWorkSpace\\Finance-own\\docs\\runtime-execution-queue.json)。",
        "观察结果必须符合 [runtime-observation-record.schema.json](C:\\DCG-SZ\\SZ-System-Docs\\CodexWorkSpace\\Finance-own\\docs\\runtime-observation-record.schema.json)，",
        "人工记录格式见 [runtime-observation-record-template.md](C:\\DCG-SZ\\SZ-System-Docs\\CodexWorkSpace\\Finance-own\\docs\\runtime-observation-record-template.md)。",
        "",
        "## 2. 执行规则",
        "",
        "1. `P0` 先执行写入、删除、文件、报表、账户、规划和内部入口；`P1` 执行业务视图；`P2` 通过宿主间接验证技术组件。",
        "2. 每个窗体必须按 `states_to_capture` 建立空数据、有数据、选择、错误、取消或回滚状态；不适用状态要写明依据。",
        "3. 嵌入视图必须从 `ultimate_hosts` 指定的最终宿主进入，不把 Frame 当作独立窗口寻找。",
        "4. 每个命令记录初始启用状态、触发方式、提示、数据前后差异、文件副作用和 Rust 边界结论。",
        "5. 删除或清除操作必须在确认动作前保存证据；实际确认仍遵守当前桌面自动化的动作时确认要求。",
        "6. 单个条目只有满足 `completion_requirements` 并回填 PRD、数据流和验收标准后才能改为 `completed`。",
        "",
        "## 3. 批次摘要",
        "",
        "| 顺序 | 批次 | 业务域 | 窗体 | 可交互控件 | 事件 | 高风险事件 | P0/P1/P2 |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for batch in queue["batches"]:
        priorities = batch["priority_counts"]
        lines.append(
            "| {order} | `{batch_id}` | {label} | {forms} | {commands} | {events} | "
            "{risks} | {p0}/{p1}/{p2} |".format(
                order=batch["order"],
                batch_id=batch["batch_id"],
                label=batch["domain_label"],
                forms=batch["form_count"],
                commands=batch["actionable_command_count"],
                events=batch["event_handler_count"],
                risks=batch["high_risk_event_count"],
                p0=priorities.get("P0", 0),
                p1=priorities.get("P1", 0),
                p2=priorities.get("P2", 0),
            )
        )
    lines.extend(
        [
            "",
            "## 4. 关闭条件",
            "",
            *[f"- {item}" for item in COMPLETION_REQUIREMENTS],
            "",
            "当前状态分布："
            + "、".join(
                f"`{status}` {count} 条"
                for status, count in sorted(metrics["status_counts"].items())
            )
            + "。只有结构化观察记录可以推进状态，静态分析不能自动把页面标记为动态兼容。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    """生成并对账 JSON 队列和 Markdown 摘要。"""

    queue = build_queue()
    OUTPUT_JSON_PATH.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    OUTPUT_MD_PATH.write_text(
        render_markdown(queue), encoding="utf-8", newline="\n"
    )
    metrics = queue["metrics"]
    print(
        "动态执行队列生成完成："
        f"{metrics['batch_count']} 批、{metrics['form_count']} 窗体、"
        f"{metrics['actionable_command_count']} 控件、"
        f"{metrics['event_handler_count']} 事件"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
