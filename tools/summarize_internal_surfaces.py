"""汇总 AI 面板、计算器宿主和控制台的结构、方法与产品范围证据。"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
DOCS_DIR = WORKSPACE / "docs"
DEFAULT_DFM_INPUT = DOCS_DIR / "runtime-dfm-all-forms.json"
DEFAULT_COVERAGE_INPUT = DOCS_DIR / "runtime-form-coverage-audit.json"
DEFAULT_COMPOSITION_INPUT = DOCS_DIR / "runtime-form-composition-evidence.json"
DEFAULT_METHOD_INPUT = DOCS_DIR / "runtime-method-evidence.json"
DEFAULT_JSON_OUTPUT = DOCS_DIR / "runtime-internal-surface-evidence.json"
DEFAULT_MARKDOWN_OUTPUT = DOCS_DIR / "runtime-internal-surface-evidence.md"
TARGET_RESOURCES = ("TAIPANELDLG", "TCALCUFM", "TCONSOLEFM")
TEXT_PROPERTIES = ("Caption", "Hint", "Title", "Text", "Items.Strings")


def iter_nodes(
    root: dict[str, Any],
    path: tuple[str, ...] = (),
) -> Iterable[tuple[dict[str, Any], tuple[str, ...]]]:
    """遍历 DFM 控件树并返回稳定的对象路径。"""

    current_path = path + (str(root.get("name", "")),)
    yield root, current_path
    for child in root.get("children", []):
        yield from iter_nodes(child, current_path)


def flatten_strings(value: Any) -> Iterable[str]:
    """展开 DFM 属性里的字符串或字符串列表。"""

    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from flatten_strings(item)


def unique(values: Iterable[str]) -> list[str]:
    """按首次出现顺序去重文本。"""

    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = " ".join(value.replace("\r", " ").replace("\n", " ").split())
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def find_component(root: dict[str, Any], name: str) -> dict[str, Any] | None:
    """按设计时组件名查找单个节点。"""

    for node, _ in iter_nodes(root):
        if node.get("name") == name:
            return node
    return None


def summarize_target(
    resource: str,
    root: dict[str, Any],
    coverage: dict[str, Any],
    static_parent_count: int,
    external_references: list[dict[str, str]],
) -> dict[str, Any]:
    """提取目标窗体的组件、事件、文案和静态引用。"""

    nodes = list(iter_nodes(root))
    class_counts = Counter(str(node.get("class", "")) for node, _ in nodes)
    labels: list[str] = []
    events: list[dict[str, str]] = []
    for node, path in nodes:
        properties = node.get("properties", {})
        for property_name in TEXT_PROPERTIES:
            labels.extend(flatten_strings(properties.get(property_name)))
        for property_name, value in properties.items():
            if property_name.startswith("On") and isinstance(value, str):
                events.append(
                    {
                        "component": str(node.get("name", "")),
                        "component_class": str(node.get("class", "")),
                        "path": ".".join(part for part in path if part),
                        "event_property": property_name,
                        "handler": value,
                    }
                )

    assessments = {
        "TAIPANELDLG": {
            "static_semantic": "置顶 WebView AI 面板",
            "product_classification": "experimental_web_panel",
            "development_decision": "保留为默认关闭的外部 AI 适配器；禁止复制旧明文 HTTP 和客户端内置秘密",
            "remaining_validation": "菜单、快捷键或条件代码入口；实际发送字段需在不使用真实财务数据时校准",
        },
        "TCALCUFM": {
            "static_semantic": "金额输入控件使用的无边框计算器宿主",
            "product_classification": "shared_numeric_calculator_host",
            "development_decision": "作为共享技术组件实现，不作为独立业务页面复刻",
            "remaining_validation": "从金额输入框唤起、回填结果、错误文案和焦点恢复",
        },
        "TCONSOLEFM": {
            "static_semantic": "包含 SQL、网银插件与网络、控制台页签的置顶诊断窗口",
            "product_classification": "internal_diagnostic_console",
            "development_decision": "仅在开发或诊断构建中启用，不进入普通用户默认导航",
            "remaining_validation": "动态可达前置条件、25 个命令的语法、输出和真实副作用",
        },
    }
    assessment = assessments[resource]
    return {
        "resource": resource,
        "class": root["class"],
        "title": str(root.get("properties", {}).get("Caption", "")),
        "surface_kind": coverage["surface_kind"],
        "role": coverage["role"],
        "control_count": len(nodes),
        "class_counts": dict(sorted(class_counts.items())),
        "labels": unique(labels),
        "events": events,
        "static_composition_parent_count": static_parent_count,
        "external_dfm_references": external_references,
        **assessment,
    }


def build_evidence(
    dfm_data: dict[str, Any],
    coverage_data: dict[str, Any],
    composition_data: dict[str, Any],
    method_data: dict[str, Any],
    paths: dict[str, Path],
) -> dict[str, Any]:
    """生成三个特殊窗体及其跨窗体支持线索。"""

    forms = dfm_data["forms"]
    missing = [resource for resource in TARGET_RESOURCES if resource not in forms]
    if missing:
        raise ValueError("缺少目标窗体：" + ", ".join(missing))
    coverage_by_resource = {
        item["resource"]: item for item in coverage_data["forms"]
    }
    parent_counts = Counter(
        link["child_resource"] for link in composition_data["composition_links"]
    )

    titles = {
        resource: str(forms[resource].get("properties", {}).get("Caption", ""))
        for resource in TARGET_RESOURCES
    }
    external_references: dict[str, list[dict[str, str]]] = {
        resource: [] for resource in TARGET_RESOURCES
    }
    for source_resource, root in forms.items():
        if source_resource in TARGET_RESOURCES:
            continue
        for node, node_path in iter_nodes(root):
            properties = node.get("properties", {})
            for property_name in TEXT_PROPERTIES:
                for value in flatten_strings(properties.get(property_name)):
                    for target_resource, title in titles.items():
                        if value == title:
                            external_references[target_resource].append(
                                {
                                    "source_resource": source_resource,
                                    "component": str(node.get("name", "")),
                                    "component_class": str(node.get("class", "")),
                                    "path": ".".join(
                                        part for part in node_path if part
                                    ),
                                    "property": property_name,
                                    "value": value,
                                }
                            )

    targets = [
        summarize_target(
            resource,
            forms[resource],
            coverage_by_resource[resource],
            parent_counts[resource],
            external_references[resource],
        )
        for resource in TARGET_RESOURCES
    ]
    target_by_resource = {item["resource"]: item for item in targets}
    target_by_resource["TAIPANELDLG"].update(
        {
            "development_decision": "保留为默认关闭的外部 AI 适配器；禁止复制旧明文 HTTP 和客户端内置秘密",
            "remaining_validation": "动态入口和实际发送字段；不得使用真实财务数据测试旧服务",
        }
    )
    target_by_resource["TCALCUFM"].update(
        {
            "remaining_validation": "从金额输入框唤起、结果回填、错误文案和焦点恢复；关闭键和 VCL Close 路径已确认",
        }
    )
    target_by_resource["TCONSOLEFM"].update(
        {
            "development_decision": "仅在开发或诊断构建中启用，不进入普通用户默认导航",
            "remaining_validation": "动态可达前置条件、25 个命令的语法、输出和真实副作用",
        }
    )

    calculator_edit_forms: set[str] = set()
    calculator_edit_count = 0
    web_browser_forms: set[str] = set()
    web_browser_count = 0
    for resource, root in forms.items():
        for node, _ in iter_nodes(root):
            component_class = node.get("class")
            if component_class == "TMHCalcuEdit":
                calculator_edit_count += 1
                calculator_edit_forms.add(resource)
            elif component_class == "TWkeWebbrowser":
                web_browser_count += 1
                web_browser_forms.add(resource)

    shortcut_form = forms["TSHORTCUTMANAGEDLGFM"]
    console_label = find_component(shortcut_form, "lblConsole")
    console_hotkey = find_component(shortcut_form, "edtConsole")
    if not console_label or not console_hotkey:
        raise ValueError("快捷键设置中缺少控制台标签或热键控件")
    console_shortcut_clue = {
        "source_resource": "TSHORTCUTMANAGEDLGFM",
        "source_title": str(
            shortcut_form.get("properties", {}).get("Caption", "")
        ),
        "label_component": console_label["name"],
        "label": console_label.get("properties", {}).get("Caption", ""),
        "hotkey_component": console_hotkey["name"],
        "hotkey_class": console_hotkey["class"],
        "hotkey_enabled_at_design_time": console_hotkey.get("properties", {}).get(
            "Enabled", True
        ),
        "runtime_hotkey": "Ctrl+F12",
        "runtime_shortcut_value": "0x407B",
        "interpretation": "方法级代码把 edtConsole 固定写为 Ctrl+F12；设计时禁用只表示用户不能在该页编辑",
    }

    return {
        "sources": {name: str(path) for name, path in paths.items()},
        "evidence_boundary": {
            "proved": [
                "三个目标窗体的控件类、页签、事件、窗口样式和设计时状态",
                "控制台热键为 Ctrl+F12，包含三个页签、最近 10 条历史和 25 个命令类",
                "金额计算输入控件和 WebView 控件在全部运行时窗体中的使用规模",
                "AI 外部 HTTP 端点、发送字段、MD5 签名和响应码；计算器结果/错误/关闭键的 VCL Close 路径",
            ],
            "inferred_design": [
                "TCalcuFm 是 TMHCalcuEdit 的共享弹出计算器宿主",
                "控制台主要用于诊断和支持，不属于日常财务业务页面",
                "AI 面板属于实验 WebView 能力，应隔离为默认关闭的外部适配器",
            ],
            "not_proved": [
                "AI 面板的真实菜单、快捷键或条件触发路径",
                "控制台 Ctrl+F12 的前置条件及命令语法和副作用",
                "TCalcuFm 与 TMHCalcuEdit 之间的调用方回填和焦点恢复关系",
            ],
        },
        "metrics": {
            "target_surface_count": len(targets),
            "experimental_surface_count": 1,
            "internal_diagnostic_count": 1,
            "technical_helper_count": 1,
            "target_with_static_composition_parent_count": sum(
                item["static_composition_parent_count"] > 0 for item in targets
            ),
            "target_with_external_dfm_reference_count": sum(
                bool(item["external_dfm_references"]) for item in targets
            ),
            "calculator_edit_count": calculator_edit_count,
            "calculator_edit_form_count": len(calculator_edit_forms),
            "web_browser_count": web_browser_count,
            "web_browser_form_count": len(web_browser_forms),
            "published_method_count": method_data["metrics"][
                "published_method_count"
            ],
            "console_command_class_count": method_data["metrics"][
                "console_command_class_count"
            ],
        },
        "targets": targets,
        "calculator_support_evidence": {
            "calculator_edit_class": "TMHCalcuEdit",
            "calculator_edit_count": calculator_edit_count,
            "calculator_edit_form_count": len(calculator_edit_forms),
            "calculator_edit_forms": sorted(calculator_edit_forms),
            "popup_calculator_class": "TdxCalculator",
            "popup_calculator_resource": "TCALCUFM",
        },
        "console_shortcut_clue": console_shortcut_clue,
        "webview_usage": {
            "component_class": "TWkeWebbrowser",
            "count": web_browser_count,
            "form_count": len(web_browser_forms),
            "forms": sorted(web_browser_forms),
        },
    }


def escape_cell(value: Any) -> str:
    """把值转换成 Markdown 表格文本。"""

    if isinstance(value, list):
        text = "；".join(str(item) for item in value)
    else:
        text = str(value)
    return text.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def build_markdown(evidence: dict[str, Any]) -> str:
    """渲染内部表面的产品范围和验证边界。"""

    metrics = evidence["metrics"]
    lines = [
        "# MoneyHome8 内部与实验表面专项证据",
        "",
        "本文档区分实验入口、内部诊断窗口和共享技术组件，避免把所有特殊窗体都误算成独立业务功能。",
        "",
        "## 1. 结论",
        "",
        f"- 专项目标：`{metrics['target_surface_count']}` 个",
        f"- 实验表面：`{metrics['experimental_surface_count']}` 个",
        f"- 内部诊断：`{metrics['internal_diagnostic_count']}` 个",
        f"- 技术辅助组件：`{metrics['technical_helper_count']}` 个",
        f"- `TMHCalcuEdit`：`{metrics['calculator_edit_count']}` 个，分布于 `{metrics['calculator_edit_form_count']}` 个窗体",
        f"- `TWkeWebbrowser`：`{metrics['web_browser_count']}` 个，分布于 `{metrics['web_browser_form_count']}` 个窗体",
        "",
        "`TCalcuFm` 已归入技术支撑；关闭键和错误/结果关闭路径已确认。`TConsoleFm` 热键为 `Ctrl+F12`，包含 `25` 个命令类；`TAIPanelDlg` 外部数据边界已确认，但仍未发现动态入口。",
        "",
        "## 2. 专项表面",
        "",
        "| 资源 | 标题 | 控件 | 核心结构 | 外部 DFM 引用 | 静态语义 | 产品决策 | 剩余验证 |",
        "| --- | --- | ---: | --- | ---: | --- | --- | --- |",
    ]
    for item in evidence["targets"]:
        core_classes = [
            f"`{name}` x{count}"
            for name, count in item["class_counts"].items()
            if name in {"TdxCalculator", "TMHCalcuEdit", "TWkeWebbrowser", "TRzTabSheet", "TTimer"}
        ]
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(item['resource'])}`",
                    escape_cell(item["title"]),
                    str(item["control_count"]),
                    escape_cell(core_classes),
                    str(len(item["external_dfm_references"])),
                    escape_cell(item["static_semantic"]),
                    escape_cell(item["development_decision"]),
                    escape_cell(item["remaining_validation"]),
                ]
            )
            + " |"
        )

    shortcut = evidence["console_shortcut_clue"]
    calculator = evidence["calculator_support_evidence"]
    lines.extend(
        [
            "",
            "## 3. 控制台入口线索",
            "",
            f"- 来源窗体：`{shortcut['source_resource']}`（{shortcut['source_title']}）",
            f"- 标签：`{shortcut['label_component']}` = `{shortcut['label']}`",
            f"- 热键控件：`{shortcut['hotkey_component']}` / `{shortcut['hotkey_class']}`",
            f"- 设计时启用：`{str(shortcut['hotkey_enabled_at_design_time']).lower()}`",
            f"- 运行时键值：`{shortcut['runtime_hotkey']}` / `{shortcut['runtime_shortcut_value']}`",
            f"- 解释：{shortcut['interpretation']}",
            "",
            "方法级证据证明具体键值；动态验证只需确认触发前置条件、窗口可达性和命令副作用。",
            "",
            "## 4. 金额计算器支撑范围",
            "",
            f"- 金额输入控件：`{calculator['calculator_edit_class']}`",
            f"- 实例数：`{calculator['calculator_edit_count']}`",
            f"- 覆盖窗体：`{calculator['calculator_edit_form_count']}` 个",
            f"- 弹出计算器：`{calculator['popup_calculator_resource']}` / `{calculator['popup_calculator_class']}`",
            "",
            "Rust 版应把它实现为金额输入控件的共享计算器弹层；结果、错误、Esc 和方向上键均关闭弹层，仍需动态验收回填、错误文案和焦点恢复。",
            "",
            "## 5. 产品范围边界",
            "",
            "- `AI`：记录为实验外部能力；默认关闭，不得复制旧明文 HTTP、内置秘密或无同意上传行为。",
            "- `控制台`：记录为内部诊断能力；仅开发/诊断构建启用，不进入普通用户默认导航。",
            "- `CalcuFm`：属于金额输入共享技术组件，进入实现范围，但不计为独立业务功能页。",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """读取固定工作区内的证据输入和输出路径。"""

    parser = argparse.ArgumentParser(description="生成 MoneyHome8 内部表面专项证据")
    parser.add_argument("--dfm-input", type=Path, default=DEFAULT_DFM_INPUT)
    parser.add_argument("--coverage-input", type=Path, default=DEFAULT_COVERAGE_INPUT)
    parser.add_argument("--composition-input", type=Path, default=DEFAULT_COMPOSITION_INPUT)
    parser.add_argument("--method-input", type=Path, default=DEFAULT_METHOD_INPUT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    return parser.parse_args()


def main() -> int:
    """生成 JSON 和 Markdown 专项证据。"""

    args = parse_args()
    input_paths = {
        "runtime_dfm": args.dfm_input.resolve(),
        "form_coverage": args.coverage_input.resolve(),
        "form_composition": args.composition_input.resolve(),
        "runtime_methods": args.method_input.resolve(),
    }
    output_paths = [args.json_output.resolve(), args.markdown_output.resolve()]
    for input_path in input_paths.values():
        if not input_path.is_file():
            raise SystemExit(f"输入文件不存在：{input_path}")
    for output_path in output_paths:
        if WORKSPACE not in output_path.parents:
            raise SystemExit(f"输出必须位于固定工作区内：{WORKSPACE}")

    evidence = build_evidence(
        json.loads(input_paths["runtime_dfm"].read_text(encoding="utf-8")),
        json.loads(input_paths["form_coverage"].read_text(encoding="utf-8")),
        json.loads(input_paths["form_composition"].read_text(encoding="utf-8")),
        json.loads(input_paths["runtime_methods"].read_text(encoding="utf-8")),
        input_paths,
    )
    output_paths[0].write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    output_paths[1].write_text(
        build_markdown(evidence),
        encoding="utf-8",
        newline="\n",
    )
    metrics = evidence["metrics"]
    print(
        "已生成内部表面证据："
        f"{metrics['calculator_edit_count']} 个金额计算输入控件，"
        "控制台 Ctrl+F12 和方法级边界已确认"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
