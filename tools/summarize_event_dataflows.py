"""把 MoneyHome8 全量事件处理器映射为应用命令和数据流候选。"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
DOCS_DIR = WORKSPACE / "docs"
DEFAULT_EVENT_INPUT = DOCS_DIR / "runtime-event-handler-evidence.json"
DEFAULT_DFM_INPUT = DOCS_DIR / "runtime-dfm-all-forms.json"
DEFAULT_METHOD_INPUT = DOCS_DIR / "runtime-method-evidence.json"
DEFAULT_JSON_OUTPUT = DOCS_DIR / "runtime-event-command-dataflow.json"
DEFAULT_MARKDOWN_OUTPUT = DOCS_DIR / "runtime-event-command-dataflow.md"


INTENT_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("backup_restore", ("backup", "restore", "备份", "还原", "恢复账簿")),
    ("sync_external", ("sync", "remote", "online", "http", "url", "同步", "远程", "在线")),
    ("import_data", ("import", "paste", "clipboard", "导入", "粘贴")),
    ("export_output", ("export", "print", "导出", "打印")),
    ("delete_data", ("delete", "remove", "cleardata", "clearall", "删除", "移出", "清除数据")),
    ("create_data", ("add", "new", "append", "insert", "新增", "新建", "添加")),
    (
        "transaction_action",
        (
            "refund",
            "transfer",
            "withdraw",
            "deposit",
            "borrow",
            "repay",
            "return",
            "buy",
            "sell",
            "dividend",
            "split",
            "convert",
            "交易",
            "转账",
            "退款",
            "取款",
            "存款",
            "买入",
            "卖出",
            "还款",
            "收款",
        ),
    ),
    (
        "update_data",
        (
            "edit",
            "modify",
            "save",
            "rename",
            "replace",
            "adjust",
            "update",
            "settag",
            "setdescription",
            "修改",
            "编辑",
            "保存",
            "替换",
            "调整",
            "更新",
            "确定",
        ),
    ),
    ("calculation", ("calc", "calculate", "recalc", "yield", "profit", "amount", "price", "rate", "计算", "金额", "收益", "价格", "费率")),
    ("query_read", ("find", "search", "filter", "query", "refresh", "load", "preview", "sort", "group", "查找", "查询", "筛选", "刷新", "预览", "排序", "分组")),
    ("navigation", ("back", "next", "page", "tab", "center", "expand", "collapse", "show", "hide", "information", "settings", "manage", "about", "help", "faq", "返回", "下一步", "展开", "收起", "显示", "隐藏", "设置", "管理", "帮助")),
    ("selection_input", ("select", "closeup", "editing", "edited", "keydown", "keypress", "change", "选择", "输入")),
    ("display_format", ("draw", "paint", "resize", "mousemove", "mouseenter", "mouseleave", "gettext", "alignment", "font", "绘制", "调整大小")),
    ("lifecycle", ("formcreate", "formdestroy", "formshow", "formclose", "formactivate", "formdeactivate", "timer", "创建窗体", "关闭窗体")),
]

INTENT_BOUNDARIES = {
    "backup_restore": ("snapshot_or_replace", "persistence_service"),
    "sync_external": ("bidirectional_external", "integration_adapter"),
    "import_data": ("external_to_write", "import_pipeline"),
    "export_output": ("read_to_external", "query_export_service"),
    "delete_data": ("delete", "command_handler"),
    "create_data": ("write", "command_handler"),
    "transaction_action": ("write", "domain_command_handler"),
    "update_data": ("write", "command_handler"),
    "calculation": ("read_or_derive", "domain_service"),
    "query_read": ("read", "query_handler"),
    "navigation": ("ui_state", "presentation_state"),
    "selection_input": ("ui_input", "presentation_state"),
    "display_format": ("ui_render", "presentation_state"),
    "lifecycle": ("lifecycle_unknown", "presentation_lifecycle"),
    "other": ("unknown", "manual_review"),
}

DOMAIN_ENTITIES = {
    "accounts_master_data": ["account", "account_group", "category", "tag", "person", "currency"],
    "auth_sync_external": ["sync_batch", "user_identity", "notification"],
    "bonds": ["bond", "investment_transaction", "position"],
    "debts_credit": ["debt", "credit_account", "repayment", "transaction"],
    "financial_products": ["financial_product", "position", "transaction"],
    "foreign_exchange": ["currency", "exchange_rate", "fx_transaction"],
    "funds": ["fund", "position", "investment_transaction", "quote"],
    "futures_metals": ["futures_contract", "metal_position", "investment_transaction"],
    "import_export": ["import_batch", "raw_row", "field_mapping", "export_projection"],
    "insurance_social": ["insurance_policy", "social_security_account", "transaction"],
    "investment_shared": ["investment_object", "position", "quote", "fee_rule"],
    "major_tangible_assets": ["tangible_asset", "valuation", "transaction"],
    "margin_financing": ["margin_account", "financing_transaction", "position"],
    "planning_budget_goal": ["budget", "reminder", "financial_plan", "financial_goal"],
    "reports": ["report_query", "report_projection", "report_filter"],
    "securities": ["security", "position", "investment_transaction", "quote"],
    "shared_infrastructure": ["application_setting", "presentation_state"],
    "system_shell": ["ledger", "application_setting", "backup_snapshot"],
    "tools_longtail": ["tool_input", "tool_result"],
    "transactions": ["transaction", "account_entry", "category_split", "attachment"],
}

ENTITY_TOKENS: list[tuple[str, tuple[str, ...]]] = [
    ("account", ("acct", "account", "账户")),
    ("transaction", ("trans", "wastebook", "流水", "交易")),
    ("category", ("category", "分类", "项目")),
    ("tag", ("tag", "标签")),
    ("budget", ("budget", "预算")),
    ("reminder", ("remind", "limit", "提醒", "限额")),
    ("report", ("report", "rpt", "报表")),
    ("security", ("security", "secu", "stock", "证券", "股票")),
    ("fund", ("fund", "基金")),
    ("debt", ("debt", "credit", "债", "信用")),
    ("financial_goal", ("goal", "目标")),
    ("financial_plan", ("plan", "规划", "计划")),
    ("attachment", ("attach", "附件")),
    ("quote", ("price", "rate", "quote", "行情", "汇率", "价格")),
    ("ledger", ("book", "ledger", "账簿")),
]


def iter_nodes(
    root: dict[str, Any], path: tuple[str, ...] = ()
) -> Iterable[tuple[dict[str, Any], str]]:
    """遍历 DFM 控件树并生成与事件证据一致的组件路径。"""
    current = path + (str(root.get("name", "")),)
    component_path = ".".join(item for item in current if item)
    yield root, component_path
    for child in root.get("children", []):
        yield from iter_nodes(child, current)


def text_property(value: Any) -> str:
    """把简单 DFM 属性压缩为可检索文本，跳过二进制和复杂对象。"""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return "；".join(value[:20])
    return ""


def component_metadata(dfm_form: dict[str, Any]) -> dict[str, dict[str, str]]:
    """提取事件解释需要的标题、提示、动作和字段绑定。"""
    result: dict[str, dict[str, str]] = {}
    selected_properties = (
        "Caption",
        "Text",
        "Hint",
        "Action",
        "DataField",
        "FieldName",
        "DataSource",
    )
    for node, path in iter_nodes(dfm_form):
        properties = node.get("properties", {})
        metadata = {
            "component": str(node.get("name", "")),
            "component_class": str(node.get("class", "")),
        }
        for name in selected_properties:
            value = text_property(properties.get(name))
            if value:
                metadata[name.lower()] = value
        result[path] = metadata
    return result


def normalize_search_text(parts: Iterable[str]) -> str:
    """统一空白并保留 CamelCase，比较阶段再执行大小写归一化。"""
    return " ".join(part for part in parts if part)


def identifier_words(text: str) -> set[str]:
    """按 CamelCase、数字和标点拆分英文标识符，避免短词子串误判。"""
    expanded = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", text)
    expanded = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", expanded)
    return {word.lower() for word in re.findall(r"[A-Za-z0-9]+", expanded)}


def token_matches(text: str, words: set[str], token: str) -> bool:
    """中文使用短语包含，英文优先使用词级匹配。"""
    token = token.lower()
    if any("\u4e00" <= char <= "\u9fff" for char in token):
        return token in text
    if token in words:
        return True
    compact = re.sub(r"[^a-z0-9]", "", text)
    return len(token) >= 6 and token in compact


def rule_matches(text: str, intent: str) -> bool:
    """判断一段事件文本是否命中指定意图规则。"""
    words = identifier_words(text)
    return any(
        token_matches(text.lower(), words, token)
        for rule_intent, tokens in INTENT_RULES
        if rule_intent == intent
        for token in tokens
    )


def matching_intents(
    handler: str,
    bindings: list[dict[str, Any]],
    component_text: str,
    form_context_text: str,
) -> tuple[list[str], str]:
    """返回意图和证据来源，输入/展示事件优先保持在展示层。"""
    event_properties = {binding["event_property"] for binding in bindings}
    component_classes = " ".join(
        str(binding.get("component_class", "")) for binding in bindings
    ).lower()
    if re.match(
        r"^Form(Create|Destroy|Show|Close|Activate|Deactivate)", handler
    ) or handler.lower().endswith("timertimer"):
        return ["lifecycle"], "event_semantics"
    display_events = {
        "OnResize",
        "OnPaint",
        "OnMouseMove",
        "OnMouseEnter",
        "OnMouseLeave",
        "OnCustomDrawCell",
        "OnGetText",
        "OnGetAlignment",
    }
    if event_properties and event_properties <= display_events:
        return ["display_format"], "event_semantics"

    handler_matches = [
        intent
        for intent, _ in INTENT_RULES
        if rule_matches(handler, intent)
    ]
    explicit_handler_matches = [
        intent
        for intent in handler_matches
        if intent not in {"selection_input", "display_format", "lifecycle"}
    ]
    input_events = {
        "OnChange",
        "OnCloseUp",
        "OnEditing",
        "OnEdited",
        "OnKeyDown",
        "OnKeyPress",
        "OnExit",
        "OnEnter",
    }
    input_component = any(
        token in component_classes
        for token in ("checkbox", "radiobutton", "combobox", "edit")
    )
    if not explicit_handler_matches and (
        (event_properties and event_properties <= input_events)
        or input_component
        or "checkbox" in handler.lower()
    ):
        return ["selection_input"], "event_semantics"
    handler_words = identifier_words(handler)
    if not explicit_handler_matches and handler_words & {
        "cancel",
        "close",
        "back",
        "next",
        "browse",
    }:
        return ["navigation"], "handler_name"
    if handler_matches:
        return handler_matches, "handler_name"

    commit_words = {"ok", "save", "enter", "start", "finish"}
    if handler_words & commit_words:
        context_matches = [
            intent
            for intent in (
                "backup_restore",
                "sync_external",
                "import_data",
                "export_output",
                "create_data",
                "calculation",
            )
            if rule_matches(form_context_text, intent)
        ]
        if context_matches:
            return context_matches, "form_context"

    matches = []
    for intent, tokens in INTENT_RULES:
        words = identifier_words(component_text)
        if any(
            token_matches(component_text.lower(), words, token) for token in tokens
        ):
            matches.append(intent)
    if matches:
        return matches, "component_text"
    if handler_words & {"ok", "save", "finish"}:
        return ["update_data"], "generic_commit"
    return ["other"], "manual_review"


def confidence_for(
    handler: str,
    bindings: list[dict[str, Any]],
    primary_intent: str,
    match_source: str,
) -> tuple[str, list[str]]:
    """根据处理器名称和命令型事件判断意图证据强度。"""
    handler_text = handler.lower()
    handler_match = rule_matches(handler, primary_intent)
    command_event = any(
        binding["event_property"] in {"OnClick", "OnExecute", "OnDblClick"}
        for binding in bindings
    )
    sources = []
    if handler_match or match_source == "handler_name":
        sources.append("handler_name")
    if command_event:
        sources.append("command_event")
    if any(binding.get("caption") or binding.get("hint") for binding in bindings):
        sources.append("component_text")
    if (handler_match or match_source == "handler_name") and command_event:
        return "high", sources
    if handler_match or match_source in {
        "handler_name",
        "component_text",
        "form_context",
        "generic_commit",
    } or command_event:
        return "medium", sources
    return "low", sources or ["event_semantics"]


def infer_entities(domain: str, action_text: str) -> list[str]:
    """结合业务域和事件名称生成实体候选，不声明旧库表结构。"""
    entities = set(DOMAIN_ENTITIES.get(domain, []))
    action_text = action_text.lower()
    for entity, tokens in ENTITY_TOKENS:
        if any(token.lower() in action_text for token in tokens):
            entities.add(entity)
    return sorted(entities)


def snake_case(value: str) -> str:
    """把 Delphi 标识符转换为稳定的小写命令片段。"""
    value = re.sub(r"^T", "", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    value = re.sub(r"[^A-Za-z0-9]+", "_", value)
    return value.strip("_").lower()


def build_code_name_map(event_data: dict[str, Any]) -> dict[int, list[dict[str, str]]]:
    """建立代码入口到 published 类方法的反向索引。"""
    result: dict[int, list[dict[str, str]]] = defaultdict(list)
    seen: set[tuple[int, str, str]] = set()
    for form in event_data["forms"]:
        for method in form["published_methods"]:
            key = (method["code_rva"], form["class_name"], method["name"])
            if key in seen:
                continue
            seen.add(key)
            result[method["code_rva"]].append(
                {"class_name": form["class_name"], "method": method["name"]}
            )
    return result


def build_named_routine_map(method_data: dict[str, Any]) -> dict[int, dict[str, str]]:
    """建立特殊方法证据中的命名例程索引。"""
    result = {
        item["analysis"]["code_rva"]: {"name": item["name"], "role": item["role"]}
        for item in method_data.get("named_routines", [])
    }
    for item in result.values():
        if item["name"] == "VclFormCloseThunk":
            item["role"] = "VCL TCustomForm.Close 跳转入口"
        elif item["name"] == "VclFormHideThunk":
            item["role"] = "VCL TCustomForm.Hide 跳转入口"
    return result


def handler_code_records(form: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """合并当前类、真实父类和未定位处理器的代码状态。"""
    records: dict[str, dict[str, Any]] = {}
    for item in form["direct_handlers"]:
        records[item["handler"]] = {
            "code_status": "current_class",
            "code_rva": item["code_rva"],
            "declaring_class": form["class_name"],
            "analysis": item["analysis"],
        }
    for item in form["inherited_handlers"]:
        records[item["handler"]] = {
            "code_status": "real_ancestor",
            "code_rva": item["code_rva"],
            "declaring_class": item["declaring_class"],
            "analysis": item["analysis"],
        }
    for item in form["unmatched_handler_resolutions"]:
        records[item["handler"]] = {
            "code_status": item["status"],
            "code_rva": None,
            "declaring_class": None,
            "analysis": None,
            "candidates": item["candidates"],
        }
    return records


def collect_dataflows(
    event_data: dict[str, Any],
    dfm_data: dict[str, Any],
    method_data: dict[str, Any],
) -> dict[str, Any]:
    """生成逐处理器命令目录、代码调用边和按域汇总。"""
    code_names = build_code_name_map(event_data)
    named_routines = build_named_routine_map(method_data)
    dfm_forms = dfm_data["forms"]
    commands = []
    call_edges = []
    call_edge_keys: set[tuple[Any, ...]] = set()
    for form in event_data["forms"]:
        metadata = component_metadata(dfm_forms[form["resource"]])
        bindings_by_handler: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for binding in form["event_bindings"]:
            component = metadata.get(binding["component_path"], {})
            bindings_by_handler[binding["handler"]].append(
                {**binding, **component}
            )
        code_records = handler_code_records(form)
        for handler in sorted(bindings_by_handler):
            bindings = bindings_by_handler[handler]
            record = code_records[handler]
            analysis = record.get("analysis") or {}
            strings = [
                item["text"] for item in analysis.get("string_references", [])
            ]
            component_text = [
                str(binding.get(key, ""))
                for binding in bindings
                for key in ("component", "caption", "hint", "action", "datafield", "fieldname")
            ]
            action_text = normalize_search_text([handler, *component_text])
            component_search_text = normalize_search_text(component_text)
            form_context_text = normalize_search_text(
                [form["class_name"], form["title"]]
            )
            intents, match_source = matching_intents(
                handler, bindings, component_search_text, form_context_text
            )
            primary_intent = intents[0]
            confidence, evidence_sources = confidence_for(
                handler, bindings, primary_intent, match_source
            )
            if strings:
                evidence_sources.append("code_strings")
            if match_source == "form_context":
                evidence_sources.append("form_context")
            data_direction, rust_boundary = INTENT_BOUNDARIES[primary_intent]
            known_calls = []
            for call in analysis.get("calls", []):
                target_rva = call.get("target_rva")
                if target_rva is None:
                    continue
                for target in code_names.get(target_rva, []):
                    edge = {
                        "source_resource": form["resource"],
                        "source_class": form["class_name"],
                        "source_handler": handler,
                        "source_code_rva": record.get("code_rva"),
                        "target_code_rva": target_rva,
                        **target,
                    }
                    edge_key = (
                        form["resource"],
                        handler,
                        target_rva,
                        target.get("class_name"),
                        target.get("method"),
                    )
                    if edge_key not in call_edge_keys:
                        call_edge_keys.add(edge_key)
                        known_calls.append(edge)
                        call_edges.append(edge)
                if target_rva in named_routines:
                    target = named_routines[target_rva]
                    edge = {
                        "source_resource": form["resource"],
                        "source_class": form["class_name"],
                        "source_handler": handler,
                        "source_code_rva": record.get("code_rva"),
                        "target_code_rva": target_rva,
                        "named_routine": target["name"],
                        "role": target["role"],
                    }
                    edge_key = (
                        form["resource"],
                        handler,
                        target_rva,
                        target["name"],
                    )
                    if edge_key not in call_edge_keys:
                        call_edge_keys.add(edge_key)
                        known_calls.append(edge)
                        call_edges.append(edge)
            command_id = ".".join(
                [form["domain"], snake_case(form["class_name"]), snake_case(handler)]
            )
            commands.append(
                {
                    "command_id": command_id,
                    "resource": form["resource"],
                    "class_name": form["class_name"],
                    "title": form["title"],
                    "domain": form["domain"],
                    "role": form["role"],
                    "surface_kind": form["surface_kind"],
                    "form_code_linkage_status": form["code_linkage_status"],
                    "handler": handler,
                    "bindings": bindings,
                    "primary_intent": primary_intent,
                    "all_intents": intents,
                    "data_direction": data_direction,
                    "rust_boundary": rust_boundary,
                    "confidence": confidence,
                    "evidence_sources": evidence_sources,
                    "entity_candidates": infer_entities(form["domain"], action_text),
                    "code_status": record["code_status"],
                    "declaring_class": record.get("declaring_class"),
                    "code_rva": record.get("code_rva"),
                    "is_noop": bool(analysis.get("is_noop")),
                    "instruction_count": analysis.get("instruction_count"),
                    "string_references": strings,
                    "known_call_edges": known_calls,
                    "same_name_candidates": record.get("candidates", []),
                }
            )

    domain_summary: dict[str, Counter[str]] = defaultdict(Counter)
    intent_summary: Counter[str] = Counter()
    boundary_summary: Counter[str] = Counter()
    confidence_summary: Counter[str] = Counter()
    code_status_summary: Counter[str] = Counter()
    for command in commands:
        row = domain_summary[command["domain"]]
        row["commands"] += 1
        row[command["primary_intent"]] += 1
        intent_summary[command["primary_intent"]] += 1
        boundary_summary[command["rust_boundary"]] += 1
        confidence_summary[command["confidence"]] += 1
        code_status_summary[command["code_status"]] += 1

    high_risk_boundaries = {
        "command_handler",
        "domain_command_handler",
        "import_pipeline",
        "integration_adapter",
        "persistence_service",
    }
    high_risk_commands = [
        command
        for command in commands
        if command["rust_boundary"] in high_risk_boundaries
        and command["confidence"] in {"high", "medium"}
        and not command["is_noop"]
    ]
    return {
        "source_event_evidence": str(DEFAULT_EVENT_INPUT),
        "source_dfm": str(DEFAULT_DFM_INPUT),
        "source_method_evidence": str(DEFAULT_METHOD_INPUT),
        "classification_contract": {
            "status": "heuristic_with_code_evidence",
            "rule": "处理器名称和命令型事件用于意图分类；代码入口、字符串和精确调用边用于增强证据，但动态副作用仍需运行校准。",
            "intent_priority": [intent for intent, _ in INTENT_RULES] + ["other"],
        },
        "metrics": {
            "command_count": len(commands),
            "high_risk_command_count": len(high_risk_commands),
            "known_call_edge_count": len(call_edges),
            "commands_with_strings": sum(bool(item["string_references"]) for item in commands),
            "noop_command_count": sum(item["is_noop"] for item in commands),
            "unlocated_code_command_count": sum(
                item["code_status"]
                in {"same_name_unique_candidate", "same_name_ambiguous_candidate", "unresolved"}
                for item in commands
            ),
            "resource_only_command_count": sum(
                item["form_code_linkage_status"] == "resource_only_no_vmt"
                for item in commands
            ),
        },
        "intent_summary": dict(sorted(intent_summary.items())),
        "boundary_summary": dict(sorted(boundary_summary.items())),
        "confidence_summary": dict(sorted(confidence_summary.items())),
        "code_status_summary": dict(sorted(code_status_summary.items())),
        "domain_summary": [
            {"domain": domain, **dict(sorted(row.items()))}
            for domain, row in sorted(domain_summary.items())
        ],
        "high_risk_commands": high_risk_commands,
        "known_call_edges": call_edges,
        "commands": commands,
    }


def escape_cell(value: Any) -> str:
    """转义 Markdown 表格单元格。"""
    if isinstance(value, list):
        value = "；".join(str(item) for item in value)
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(result: dict[str, Any]) -> str:
    """生成人工审阅用的事件命令和数据流摘要。"""
    metrics = result["metrics"]
    lines = [
        "# MoneyHome8 事件命令与数据流目录",
        "",
        "本文件把全量 DFM 事件绑定转换为 Rust 应用命令候选。分类用于需求拆分和动态验证排序，不替代真实运行副作用证据。",
        "",
        "## 1. 覆盖摘要",
        "",
        f"- 应用命令候选：`{metrics['command_count']}` 个",
        f"- 高风险写入/删除/导入/同步候选：`{metrics['high_risk_command_count']}` 个",
        f"- 精确命名调用边：`{metrics['known_call_edge_count']}` 条",
        f"- 含代码字符串证据：`{metrics['commands_with_strings']}` 个",
        f"- 空实现：`{metrics['noop_command_count']}` 个",
        f"- 无当前类或真实父类代码归属：`{metrics['unlocated_code_command_count']}` 个",
        f"- 其中资源型无 VMT 窗体处理器：`{metrics['resource_only_command_count']}` 个",
        "",
        "## 2. Rust 边界分布",
        "",
        "| Rust 边界 | 命令数 |",
        "|---|---:|",
    ]
    for boundary, count in result["boundary_summary"].items():
        lines.append(f"| `{boundary}` | {count} |")
    lines.extend(
        [
            "",
            "## 3. 按业务域与主意图",
            "",
            "| 业务域 | 命令 | 新增 | 修改 | 删除 | 交易 | 查询 | 导入 | 导出 | 同步 | 计算 |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in result["domain_summary"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["domain"],
                    str(row.get("commands", 0)),
                    str(row.get("create_data", 0)),
                    str(row.get("update_data", 0)),
                    str(row.get("delete_data", 0)),
                    str(row.get("transaction_action", 0)),
                    str(row.get("query_read", 0)),
                    str(row.get("import_data", 0)),
                    str(row.get("export_output", 0)),
                    str(row.get("sync_external", 0)),
                    str(row.get("calculation", 0)),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## 4. 高风险命令候选",
            "",
            "下表保留命令型事件中最需要动态校准的写入、删除、导入、同步和持久化路径。完整 `2000` 项见 JSON。",
            "",
            "| 命令 ID | 页面 | 处理器 | 意图 | 方向 | 置信度 | 实体候选 | 代码状态 | 字符串证据 |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
    )
    priority = {"high": 0, "medium": 1, "low": 2}
    high_risk = sorted(
        result["high_risk_commands"],
        key=lambda item: (
            priority[item["confidence"]],
            item["domain"],
            item["resource"],
            item["handler"],
        ),
    )
    for command in high_risk[:250]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{command['command_id']}`",
                    escape_cell(command["title"] or command["resource"]),
                    f"`{command['handler']}`",
                    f"`{command['primary_intent']}`",
                    f"`{command['data_direction']}`",
                    command["confidence"],
                    escape_cell(command["entity_candidates"]),
                    f"`{command['code_status']}`",
                    escape_cell(command["string_references"][:4]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## 5. 精确命名调用边",
            "",
            "调用边只在反汇编直接调用目标 RVA 与 published 方法或已命名例程入口完全相等时记录。",
            "",
            "| 来源 | 处理器 | 目标 | 目标 RVA |",
            "|---|---|---|---:|",
        ]
    )
    for edge in result["known_call_edges"][:200]:
        target = edge.get("named_routine") or (
            f"{edge.get('class_name', '')}.{edge.get('method', '')}"
        )
        lines.append(
            f"| `{edge['source_class']}` | `{edge['source_handler']}` | "
            f"`{target}` | `0x{edge['target_code_rva']:X}` |"
        )
    lines.extend(
        [
            "",
            "## 6. 开发与验收合同",
            "",
            "- `command_handler` 和 `domain_command_handler` 必须通过单一应用命令进入事务边界，UI 不直接写 SQLite。",
            "- `query_handler`、`query_export_service` 和报表投影共享查询 DTO，筛选变化后必须重新生成结果再导出。",
            "- `import_pipeline` 必须经过原始行、映射、预览、校验、幂等检查和单事务提交。",
            "- `integration_adapter` 默认不阻塞本地记账，并保留批次、冲突、取消、重试和删除墓碑。",
            "- `presentation_state` 和 `presentation_lifecycle` 只有在代码或动态结果证明副作用后，才升级为领域命令。",
            "- `same_name_*` 和 `unresolved` 不能证明代码归属；资源型无 VMT 窗体必须先验证可达性。",
            "",
        ]
    )
    return "\n".join(lines)


def workspace_output(path: Path) -> Path:
    """限制生成文件位于固定项目工作区。"""
    resolved = path.resolve()
    if WORKSPACE != resolved and WORKSPACE not in resolved.parents:
        raise SystemExit(f"输出必须位于固定工作区内：{WORKSPACE}")
    return resolved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成事件命令与数据流目录")
    parser.add_argument("--event-input", type=Path, default=DEFAULT_EVENT_INPUT)
    parser.add_argument("--dfm-input", type=Path, default=DEFAULT_DFM_INPUT)
    parser.add_argument("--method-input", type=Path, default=DEFAULT_METHOD_INPUT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for path in (args.event_input, args.dfm_input, args.method_input):
        if not path.is_file():
            raise SystemExit(f"输入文件不存在：{path}")
    result = collect_dataflows(
        json.loads(args.event_input.read_text(encoding="utf-8")),
        json.loads(args.dfm_input.read_text(encoding="utf-8")),
        json.loads(args.method_input.read_text(encoding="utf-8")),
    )
    json_output = workspace_output(args.json_output)
    markdown_output = workspace_output(args.markdown_output)
    json_output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    markdown_output.write_text(
        render_markdown(result), encoding="utf-8", newline="\n"
    )
    metrics = result["metrics"]
    print(
        "已生成事件命令与数据流目录："
        f"{metrics['command_count']} 个命令，"
        f"{metrics['high_risk_command_count']} 个高风险候选，"
        f"{metrics['known_call_edge_count']} 条命名调用边"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
