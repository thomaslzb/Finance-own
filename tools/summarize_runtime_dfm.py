"""把运行时 DFM 控件树整理成便于检索的功能证据目录。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = WORKSPACE / "docs" / "runtime-dfm-all-forms.json"
DEFAULT_OUTPUT = WORKSPACE / "docs" / "runtime-dfm-control-catalog.md"
LABEL_PROPERTIES = ("Caption", "Hint", "Title", "Text", "Items.Strings")
EVENT_PROPERTIES = ("OnClick", "OnDblClick", "OnShow", "OnChange", "OnExecute")
CHINESE_PATTERN = re.compile(r"[\u3400-\u9fff]")
INTERNAL_LABEL_PATTERN = re.compile(
    r"^(?:btn|lbl|lb|pnl|ts|tab|mi|mmi|grid|col|edt|ed|rc|rb|chb|cbx|"
    r"frame|form|dlg|fm)\w*$",
    re.IGNORECASE,
)


def iter_nodes(root: dict[str, Any]) -> Iterable[dict[str, Any]]:
    yield root
    for child in root.get("children", []):
        yield from iter_nodes(child)


def flatten_text(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from flatten_text(item)


def unique(values: Iterable[str]) -> list[str]:
    result = []
    seen = set()
    for value in values:
        normalized = " ".join(value.replace("\r", " ").replace("\n", " ").split())
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def is_user_facing_label(value: str, object_name: str) -> bool:
    normalized = value.strip()
    if not normalized or normalized == "-" or normalized == object_name:
        return False
    if INTERNAL_LABEL_PATTERN.fullmatch(normalized):
        return False
    # 中文标签直接保留；纯英文仅保留包含空格的说明性文本。
    return bool(CHINESE_PATTERN.search(normalized) or " " in normalized)


def collect_labels(root: dict[str, Any]) -> list[str]:
    labels = []
    for node in iter_nodes(root):
        properties = node.get("properties", {})
        for property_name in LABEL_PROPERTIES:
            for value in flatten_text(properties.get(property_name)):
                if is_user_facing_label(value, node.get("name", "")):
                    labels.append(value)
    return unique(labels)


def collect_fields(root: dict[str, Any]) -> list[str]:
    return unique(
        str(node.get("properties", {}).get("FieldName", ""))
        for node in iter_nodes(root)
        if node.get("properties", {}).get("FieldName")
    )


def collect_events(root: dict[str, Any]) -> list[str]:
    events = []
    for node in iter_nodes(root):
        properties = node.get("properties", {})
        label = next(
            (
                value
                for value in flatten_text(properties.get("Caption"))
                if value.strip() and value.strip() != "-"
            ),
            node.get("name", ""),
        )
        for event_property in EVENT_PROPERTIES:
            event_name = properties.get(event_property)
            if event_name:
                events.append(f"{label} -> {event_name}")
    return unique(events)


def escape_cell(values: Iterable[str] | str) -> str:
    if isinstance(values, str):
        text = values
    else:
        text = "；".join(values)
    return text.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def build_markdown(data: dict[str, Any], source_path: Path) -> str:
    lines = [
        "# MoneyHome8 运行时 DFM 控件目录",
        "",
        "本文档由普通权限运行副本内存中的真实 `TPF0` 窗体资源生成，用于检索页面标题、可见文案、数据绑定字段和交互事件。",
        "",
        f"- 数据源：`{source_path}`",
        f"- 成功解析：`{data['form_count']}` 个窗体",
        f"- 非窗体或解析失败：`{data['error_count']}` 个资源",
        "- 证据边界：控件和属性来自运行时 DFM；业务结果、动态菜单和代码生成控件仍需运行流程验证。",
        "",
        "| 资源窗体 | 页面标题 | 可见文案 | 数据字段 | 交互事件 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for resource_name, root in sorted(data["forms"].items()):
        title = str(root.get("properties", {}).get("Caption", ""))
        lines.append(
            "| "
            + " | ".join(
                (
                    f"`{escape_cell(resource_name)}`",
                    escape_cell(title),
                    escape_cell(collect_labels(root)),
                    escape_cell(f"`{field}`" for field in collect_fields(root)),
                    escape_cell(collect_events(root)),
                )
            )
            + " |"
        )

    if data.get("errors"):
        lines.extend(
            [
                "",
                "## 非窗体资源",
                "",
                "以下项目保留在 PE 的 RCDATA 清单中，但运行时载荷不是 DFM：",
                "",
            ]
        )
        for name, error in sorted(data["errors"].items()):
            lines.append(f"- `{name}`：{error}")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 MoneyHome8 运行时 DFM 控件目录")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = args.input.resolve()
    output_path = args.output.resolve()
    if not input_path.is_file():
        raise SystemExit(f"DFM JSON 不存在：{input_path}")
    if WORKSPACE not in output_path.parents:
        raise SystemExit(f"输出必须位于固定工作区内：{WORKSPACE}")

    data = json.loads(input_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_markdown(data, input_path),
        encoding="utf-8",
        newline="\n",
    )
    print(f"已生成 {data['form_count']} 个窗体的控件目录：{output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
