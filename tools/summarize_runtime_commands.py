"""提取运行时 DFM 中的命令、快捷键、选项和设计时初始状态。"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = WORKSPACE / "docs" / "runtime-dfm-all-forms.json"
DEFAULT_JSON_OUTPUT = WORKSPACE / "docs" / "runtime-command-state-evidence.json"
DEFAULT_MARKDOWN_OUTPUT = WORKSPACE / "docs" / "runtime-command-and-state-evidence.md"
COMMAND_EVENTS = ("OnClick", "OnExecute", "OnDblClick", "OnPopup", "OnShortCut")
STATE_PROPERTIES = (
    "Enabled",
    "Visible",
    "Checked",
    "AutoCheck",
    "RadioItem",
    "GroupIndex",
    "Default",
    "Cancel",
    "ModalResult",
    "ReadOnly",
)
COMMAND_CLASS_PATTERN = re.compile(
    r"(?:Button|MenuItem|Action|CheckBox|RadioButton|ToolButton)$", re.IGNORECASE
)
FOCUS_FORM_PATTERN = re.compile(
    r"(?:MAINFORM|WASTEBOOK|TEMPLATE|BUDGET|REMIND|GOAL|FINANCIAL|FP[A-Z]|"
    r"REPORTFM|^TRPT|TRANSFM|TRANSDLG|TRANSFRAME|STATISTICFRAME|LIFETHEME|"
    r"ACCOUNT|ACCT|IMPORT|EXPORT|SYNC)",
    re.IGNORECASE,
)
SUMMARY_FORM_PATTERN = re.compile(
    r"^(?:TMAINFORM|TACCOUNTMANAGERFM|TWASTEBOOKFM|TTEMPLATEDLGFM|"
    r"TTRANSFERTEMPLATEDLGFM|TBUDGET.*|TCREATEBUDGET.*|TEDITBUDGET.*|"
    r"T(?:LIMIT|NEW|ACCTBALA|CREDIT|SECURITY|OPENFUND)REMINDDLG(?:FM)?|"
    r"TFINANCIALDIAGNOSISFM|TFINANCIALPLANNINGCENTERFM|TGOAL.*|"
    r"TREPORTFM|TRPT.*|T.*STATISTICFRAME|TIMPORT.*|TEXPORT.*|TLIFETHEMEFM)$",
    re.IGNORECASE,
)


def iter_nodes(
    root: dict[str, Any],
    ancestors: tuple[dict[str, Any], ...] = (),
) -> Iterable[tuple[dict[str, Any], tuple[dict[str, Any], ...]]]:
    yield root, ancestors
    next_ancestors = (*ancestors, root)
    for child in root.get("children", []):
        yield from iter_nodes(child, next_ancestors)


def node_path(
    node: dict[str, Any], ancestors: tuple[dict[str, Any], ...]
) -> str:
    names = [ancestor.get("name", "") for ancestor in ancestors]
    names.append(node.get("name", ""))
    return "/".join(name for name in names if name)


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(flatten_strings(item))
        return result
    return []


def decode_shortcut(value: Any) -> str:
    if not isinstance(value, int) or value <= 0:
        return ""
    key_code = value & 0xFF
    modifiers = []
    if value & 0x4000:
        modifiers.append("Ctrl")
    if value & 0x2000:
        modifiers.append("Shift")
    if value & 0x8000:
        modifiers.append("Alt")
    key_names = {
        8: "Backspace",
        9: "Tab",
        13: "Enter",
        27: "Esc",
        32: "Space",
        33: "PageUp",
        34: "PageDown",
        35: "End",
        36: "Home",
        37: "Left",
        38: "Up",
        39: "Right",
        40: "Down",
        45: "Insert",
        46: "Delete",
    }
    if 65 <= key_code <= 90 or 48 <= key_code <= 57:
        key_name = chr(key_code)
    elif 112 <= key_code <= 123:
        key_name = f"F{key_code - 111}"
    else:
        key_name = key_names.get(key_code, f"VK_{key_code}")
    return "+".join((*modifiers, key_name))


def command_label(node: dict[str, Any]) -> str:
    properties = node.get("properties", {})
    for property_name in ("Caption", "Hint", "Text"):
        values = flatten_strings(properties.get(property_name))
        if values and values[0].strip():
            return " ".join(values[0].replace("\r", " ").replace("\n", " ").split())
    return str(node.get("name", ""))


def is_command(node: dict[str, Any]) -> bool:
    properties = node.get("properties", {})
    class_name = str(node.get("class", ""))
    if (
        any(properties.get(event_name) for event_name in COMMAND_EVENTS)
        or properties.get("ShortCut")
        or properties.get("ModalResult")
    ):
        return True
    caption = str(properties.get("Caption", "")).strip()
    return bool(
        caption
        and caption != "-"
        and COMMAND_CLASS_PATTERN.search(class_name)
    )


def extract_command(
    resource_name: str,
    title: str,
    node: dict[str, Any],
    ancestors: tuple[dict[str, Any], ...],
) -> dict[str, Any]:
    properties = node.get("properties", {})
    events = {
        event_name: str(properties[event_name])
        for event_name in COMMAND_EVENTS
        if properties.get(event_name)
    }
    state = {
        property_name: properties[property_name]
        for property_name in STATE_PROPERTIES
        if property_name in properties
    }
    shortcut_value = properties.get("ShortCut")
    return {
        "resource": resource_name,
        "title": title,
        "component": node.get("name", ""),
        "path": node_path(node, ancestors),
        "class": node.get("class", ""),
        "label": command_label(node),
        "events": events,
        "shortcut_value": shortcut_value if isinstance(shortcut_value, int) else None,
        "shortcut": decode_shortcut(shortcut_value),
        "state": state,
    }


def extract_form(resource_name: str, root: dict[str, Any]) -> dict[str, Any]:
    title = str(root.get("properties", {}).get("Caption", ""))
    commands = []
    option_lists = []
    stateful_controls = []
    for node, ancestors in iter_nodes(root):
        properties = node.get("properties", {})
        if is_command(node):
            commands.append(extract_command(resource_name, title, node, ancestors))

        items = flatten_strings(properties.get("Items.Strings"))
        if items:
            option_lists.append(
                {
                    "component": node.get("name", ""),
                    "path": node_path(node, ancestors),
                    "class": node.get("class", ""),
                    "label": command_label(node),
                    "items": items,
                }
            )

        explicit_state = {
            property_name: properties[property_name]
            for property_name in STATE_PROPERTIES
            if property_name in properties
            and (
                properties[property_name] is True
                or property_name in {"Enabled", "Visible"}
                and properties[property_name] is False
            )
        }
        if explicit_state and (
            is_command(node)
            or properties.get("Caption")
            or properties.get("Hint")
            or properties.get("FieldName")
        ):
            stateful_controls.append(
                {
                    "component": node.get("name", ""),
                    "path": node_path(node, ancestors),
                    "class": node.get("class", ""),
                    "label": command_label(node),
                    "field": str(properties.get("FieldName", "")),
                    "state": explicit_state,
                }
            )
    return {
        "resource": resource_name,
        "title": title,
        "commands": commands,
        "option_lists": option_lists,
        "stateful_controls": stateful_controls,
    }


def build_evidence(data: dict[str, Any], source: Path) -> dict[str, Any]:
    forms = [
        extract_form(resource_name, root)
        for resource_name, root in sorted(data["forms"].items())
    ]
    commands = [command for form in forms for command in form["commands"]]
    focused_forms = [
        form
        for form in forms
        if FOCUS_FORM_PATTERN.search(form["resource"])
        and (form["commands"] or form["option_lists"] or form["stateful_controls"])
    ]
    summary_forms = [
        form
        for form in focused_forms
        if SUMMARY_FORM_PATTERN.search(form["resource"])
    ]
    event_counts = Counter(
        event_name for command in commands for event_name in command["events"]
    )
    class_counts = Counter(command["class"] for command in commands)
    return {
        "source": str(source),
        "evidence_scope": {
            "direct": [
                "command captions and component names",
                "event handler names",
                "shortcuts",
                "design-time enabled, visible, checked and read-only states",
                "static option lists",
            ],
            "not_recovered": [
                "runtime enablement conditions",
                "runtime-generated menu items",
                "event-handler side effects",
                "post-click navigation and validation messages",
            ],
        },
        "metrics": {
            "form_count": len(forms),
            "command_count": len(commands),
            "focused_form_count": len(focused_forms),
            "summary_form_count": len(summary_forms),
            "shortcut_count": sum(bool(command["shortcut"]) for command in commands),
            "explicit_disabled_count": sum(
                command["state"].get("Enabled") is False for command in commands
            ),
            "explicit_hidden_count": sum(
                command["state"].get("Visible") is False for command in commands
            ),
            "explicit_checked_count": sum(
                command["state"].get("Checked") is True for command in commands
            ),
            "event_counts": dict(sorted(event_counts.items())),
            "command_class_counts": dict(class_counts.most_common()),
        },
        "focused_forms": focused_forms,
        "summary_forms": summary_forms,
        "forms": forms,
    }


def escape_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def command_text(command: dict[str, Any]) -> str:
    handlers = ", ".join(f"{key}={value}" for key, value in command["events"].items())
    details = []
    if handlers:
        details.append(handlers)
    if command["shortcut"]:
        details.append(f"快捷键={command['shortcut']}")
    state = command["state"]
    if state.get("Enabled") is False:
        details.append("初始禁用")
    if state.get("Visible") is False:
        details.append("初始隐藏")
    if state.get("Checked") is True:
        details.append("默认选中")
    if state.get("AutoCheck") is True:
        details.append("自动切换勾选")
    suffix = f" [{'; '.join(details)}]" if details else ""
    return f"{escape_cell(command['label'])}{suffix}"


def build_markdown(evidence: dict[str, Any]) -> str:
    metrics = evidence["metrics"]
    lines = [
        "# MoneyHome8 运行时命令与状态证据",
        "",
        "本文档由 `runtime-dfm-all-forms.json` 自动生成，记录旧程序的命令、事件、快捷键、静态选项和设计时初始状态。",
        "",
        "## 1. 证据边界",
        "",
        f"- 扫描窗体：`{metrics['form_count']}` 个",
        f"- 命令/交互控件：`{metrics['command_count']}` 个",
        f"- 包含命令证据的重点业务窗体：`{metrics['focused_form_count']}` 个",
        f"- Markdown 摘要窗体：`{metrics['summary_form_count']}` 个",
        f"- 快捷键：`{metrics['shortcut_count']}` 个",
        f"- 明确初始禁用命令：`{metrics['explicit_disabled_count']}` 个",
        f"- 明确初始隐藏命令：`{metrics['explicit_hidden_count']}` 个",
        f"- 明确默认选中命令：`{metrics['explicit_checked_count']}` 个",
        "",
        "事件名和设计时属性属于直接证据。`Enabled=False` 只能证明初始禁用，不能单独证明具体启用条件；动态菜单、点击结果和错误提示仍需运行验证。",
        "",
        "## 2. 关键状态规则",
        "",
        "- 财务记录的修改、删除、查找动作在 DFM 中初始禁用；Rust 版应在存在有效选中记录或可查询数据时再启用。具体条件需运行校准。",
        "- 通用报表的导出报表、打印预览初始禁用；Rust 版应在报表结果成功生成后启用。",
        "- 证券趋势图默认选中资产总值、证券市值、资金余额、上证指数和深证成指。",
        "- 基金趋势图默认选中资产总值、基金市值和资金余额。",
        "- 复制预算金额对一月至十二月全部默认选中，允许用户按月份取消复制范围。",
        "- 导入预览的“导入选中的记录”和从剪贴板导入动作初始禁用，必须由有效输入或选择状态驱动启用。",
        "- 标签页的移出、转移、快速加入、修改、删除和隐藏动作初始禁用，说明它们依赖当前标签或记录选择。",
        "- 今日提醒直接提供执行、跳过、今日不再提醒和打开账簿时自动弹出四类状态动作。",
        "",
        "## 3. 重点窗体命令目录",
        "",
        "| 窗体 | 命令、事件与初始状态 | 静态选项 |",
        "| --- | --- | --- |",
    ]
    for form in evidence["summary_forms"]:
        commands = "；".join(command_text(command) for command in form["commands"])
        option_lists = "；".join(
            f"{escape_cell(options['label'])}: "
            + ", ".join(escape_cell(item) for item in options["items"])
            for options in form["option_lists"]
        )
        title = form["title"] or form["resource"]
        lines.append(
            f"| {escape_cell(title)} (`{form['resource']}`) | {commands} | {option_lists} |"
        )

    lines.extend(
        [
            "",
            "## 4. 对 Rust 交互状态机的要求",
            "",
            "1. 命令可用性必须由当前选择、数据加载状态、编辑权限和计算结果显式决定，不能散落在 UI 控件事件中。",
            "2. 删除、批量修改、退款、转计划和清除规划数据属于有副作用命令，应用服务必须返回结构化确认信息和结果。",
            "3. 报表筛选变化后进入 `dirty` 状态，刷新成功后进入 `ready`，导出和打印只在 `ready` 状态可用。",
            "4. 批量操作模式应是明确状态，进入后显示选择列与批量标签/备注命令，退出后恢复普通选择行为。",
            "5. 趋势图序列是报表预设的一部分，默认值按 DFM 直接证据初始化，但用户修改后应持久化。",
            "6. 快捷键调用与菜单点击必须进入同一个应用命令，避免产生两套校验和副作用逻辑。",
            "",
            "## 5. 仍需运行验证",
            "",
            "- 财务记录修改/删除/查找的精确启用条件",
            "- 报表结果生成前后导出和打印的启用时点",
            "- 顶部记账动态下拉的项目、排序和快捷键",
            "- 退款、转为计划、活动类型更改和批量操作的确认提示及结果",
            "- 删除预算、目标、提醒和模板时的级联与恢复行为",
            "- 清除规划数据的影响范围和确认文案",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 MoneyHome8 运行时命令与状态证据")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    return parser.parse_args()


def ensure_workspace_path(path: Path) -> Path:
    resolved = path.resolve()
    if WORKSPACE != resolved and WORKSPACE not in resolved.parents:
        raise SystemExit(f"输出必须位于固定工作区内：{WORKSPACE}")
    return resolved


def main() -> int:
    args = parse_args()
    input_path = args.input.resolve()
    json_output = ensure_workspace_path(args.json_output)
    markdown_output = ensure_workspace_path(args.markdown_output)
    if not input_path.is_file():
        raise SystemExit(f"DFM JSON 不存在：{input_path}")
    data = json.loads(input_path.read_text(encoding="utf-8"))
    evidence = build_evidence(data, input_path)
    json_output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    markdown_output.write_text(
        build_markdown(evidence), encoding="utf-8", newline="\n"
    )
    print(
        f"已生成命令证据：{evidence['metrics']['command_count']} 个交互控件，"
        f"{evidence['metrics']['focused_form_count']} 个重点窗体"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
