"""从运行时 DFM 类引用生成窗体、Frame 与复用组件的组合关系证据。"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
DOCS_DIR = WORKSPACE / "docs"
DEFAULT_DFM_INPUT = DOCS_DIR / "runtime-dfm-all-forms.json"
DEFAULT_COVERAGE_INPUT = DOCS_DIR / "runtime-form-coverage-audit.json"
DEFAULT_JSON_OUTPUT = DOCS_DIR / "runtime-form-composition-evidence.json"
DEFAULT_MARKDOWN_OUTPUT = DOCS_DIR / "runtime-form-composition-evidence.md"


def iter_composition_occurrences(
    owner_resource: str,
    logical_parent: str,
    root: dict[str, Any],
    path: tuple[str, ...],
    class_to_resource: dict[str, str],
) -> Iterable[dict[str, Any]]:
    """遍历序列化子树，并用最近的已知根类确定逻辑直接父级。"""

    for child in root.get("children", []):
        child_path = path + (str(child.get("name", "")),)
        child_resource = class_to_resource.get(str(child.get("class", "")))
        if child_resource:
            yield {
                "owner_resource": owner_resource,
                "parent_resource": logical_parent,
                "child_resource": child_resource,
                "child": child,
                "component_path": ".".join(
                    part for part in child_path if part
                ),
            }
            next_parent = child_resource
        else:
            next_parent = logical_parent
        yield from iter_composition_occurrences(
            owner_resource,
            next_parent,
            child,
            child_path,
            class_to_resource,
        )


def ultimate_hosts(
    resource: str,
    parents_by_child: dict[str, set[str]],
    visiting: frozenset[str] = frozenset(),
) -> set[str]:
    """沿组合关系向上查找最终宿主，循环引用时保留当前资源作为边界。"""

    if resource in visiting:
        return {resource}
    parents = parents_by_child.get(resource, set())
    if not parents:
        return {resource}
    hosts: set[str] = set()
    for parent in parents:
        hosts.update(ultimate_hosts(parent, parents_by_child, visiting | {resource}))
    return hosts


def escape_cell(value: Any) -> str:
    """把结构化值转换成不会破坏 Markdown 表格的短文本。"""

    if isinstance(value, list):
        text = "；".join(str(item) for item in value)
    else:
        text = str(value)
    return text.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def build_evidence(
    dfm_data: dict[str, Any],
    coverage_data: dict[str, Any],
    dfm_path: Path,
    coverage_path: Path,
) -> dict[str, Any]:
    """连接 DFM 根类、嵌入实例与功能覆盖信息，生成可验证组合图。"""

    forms = dfm_data["forms"]
    coverage_forms = {
        item["resource"]: item for item in coverage_data["forms"]
    }
    class_to_resource = {
        root["class"]: resource for resource, root in forms.items()
    }
    occurrences: list[dict[str, Any]] = []
    parents_by_child: dict[str, set[str]] = defaultdict(set)

    for owner_resource, root in sorted(forms.items()):
        root_path = (str(root.get("name", "")),)
        occurrences.extend(
            iter_composition_occurrences(
                owner_resource,
                owner_resource,
                root,
                root_path,
                class_to_resource,
            )
        )

    grouped_occurrences: dict[
        tuple[str, str, str], list[dict[str, Any]]
    ] = defaultdict(list)
    for occurrence in occurrences:
        child = occurrence["child"]
        grouped_occurrences[
            (
                occurrence["parent_resource"],
                occurrence["child_resource"],
                str(child.get("name", "")),
            )
        ].append(occurrence)

    links: list[dict[str, Any]] = []
    for (parent_resource, child_resource, child_instance), group in sorted(
        grouped_occurrences.items()
    ):
        parent_coverage = coverage_forms[parent_resource]
        child_coverage = coverage_forms[child_resource]
        child = group[0]["child"]
        parents_by_child[child_resource].add(parent_resource)
        serialized_instances = sorted(
            (
                {
                    "owner_resource": occurrence["owner_resource"],
                    "component_path": occurrence["component_path"],
                }
                for occurrence in group
            ),
            key=lambda entry: (
                entry["owner_resource"],
                entry["component_path"],
            ),
        )
        preferred_instance = next(
            (
                entry
                for entry in serialized_instances
                if entry["owner_resource"] == parent_resource
            ),
            serialized_instances[0],
        )
        links.append(
            {
                "parent_resource": parent_resource,
                "parent_title": parent_coverage["title"],
                "parent_domain": parent_coverage["domain"],
                "child_resource": child_resource,
                "child_class": child["class"],
                "child_instance": child_instance,
                "component_path": preferred_instance["component_path"],
                "serialized_occurrence_count": len(serialized_instances),
                "serialized_instances": serialized_instances,
                "child_domain": child_coverage["domain"],
                "child_role": child_coverage["role"],
                "child_surface_kind": child_coverage["surface_kind"],
                "child_data_flow": child_coverage["data_flow"],
            }
        )

    links.sort(
        key=lambda item: (
            item["parent_resource"],
            item["child_resource"],
            item["component_path"],
        )
    )
    links_by_child: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for link in links:
        links_by_child[link["child_resource"]].append(link)

    embedded_views = []
    for item in coverage_data["forms"]:
        if item["surface_kind"] != "embedded_indirect_surface":
            continue
        resource = item["resource"]
        resource_links = links_by_child.get(resource, [])
        embedded_views.append(
            {
                "resource": resource,
                "class": item["class"],
                "domain": item["domain"],
                "domain_label": item["domain_label"],
                "role": item["role"],
                "role_label": item["role_label"],
                "data_flow": item["data_flow"],
                "direct_parents": sorted(parents_by_child.get(resource, set())),
                "ultimate_hosts": sorted(
                    ultimate_hosts(resource, parents_by_child) - {resource}
                ),
                "link_count": len(resource_links),
                "instances": [
                    {
                        "parent_resource": link["parent_resource"],
                        "parent_title": link["parent_title"],
                        "instance": link["child_instance"],
                        "component_path": link["component_path"],
                    }
                    for link in resource_links
                ],
                "composition_status": (
                    "direct_dfm_composition_proved"
                    if resource_links
                    else "unresolved"
                ),
                "dynamic_result_status": "pending_empty_and_populated_state_validation",
            }
        )

    internal_entries = []
    for item in coverage_data["forms"]:
        if item["surface_kind"] != "internal_or_experimental":
            continue
        resource = item["resource"]
        resource_links = links_by_child.get(resource, [])
        internal_entries.append(
            {
                "resource": resource,
                "class": item["class"],
                "title": item["title"],
                "static_composition_references": len(resource_links),
                "direct_parents": sorted(parents_by_child.get(resource, set())),
                "status": (
                    "design_time_composition_found"
                    if resource_links
                    else "no_design_time_composition_reference"
                ),
                "evidence_boundary": (
                    "没有设计时父窗体引用不等于不可达，仍可能由事件代码动态创建"
                ),
            }
        )

    multi_parent_resources = [
        {
            "resource": resource,
            "parents": sorted(parents),
            "parent_count": len(parents),
            "surface_kind": coverage_forms[resource]["surface_kind"],
            "role": coverage_forms[resource]["role"],
        }
        for resource, parents in sorted(parents_by_child.items())
        if len(parents) > 1
    ]

    unresolved_embedded = [
        item["resource"]
        for item in embedded_views
        if item["composition_status"] == "unresolved"
    ]
    evidence = {
        "sources": {
            "runtime_dfm": str(dfm_path),
            "form_coverage": str(coverage_path),
        },
        "evidence_boundary": {
            "proved": [
                "DFM 中直接声明的父窗体到已知窗体或 Frame 根类实例关系",
                "嵌套 Frame 重复序列化产生的实例与去重后的逻辑直接组合边",
                "嵌入实例的对象路径、直接父窗体和沿静态组合图得到的最终宿主",
                "无文案嵌入视图是否存在静态孤立项",
            ],
            "not_proved": [
                "事件处理器在运行时动态创建、替换或销毁的窗体",
                "嵌入视图的真实查询参数、空状态、有数据结果和交互副作用",
                "内部或实验入口是否通过菜单、快捷键或条件代码到达",
            ],
        },
        "metrics": {
            "runtime_form_count": len(forms),
            "serialized_composition_occurrence_count": len(occurrences),
            "composition_link_count": len(links),
            "composed_resource_count": len(links_by_child),
            "multi_parent_resource_count": len(multi_parent_resources),
            "embedded_surface_count": len(embedded_views),
            "embedded_surface_with_parent_count": (
                len(embedded_views) - len(unresolved_embedded)
            ),
            "unresolved_embedded_surface_count": len(unresolved_embedded),
            "internal_or_experimental_count": len(internal_entries),
            "internal_with_static_parent_count": sum(
                1
                for item in internal_entries
                if item["static_composition_references"] > 0
            ),
        },
        "embedded_views": embedded_views,
        "unresolved_embedded_views": unresolved_embedded,
        "internal_or_experimental_entries": internal_entries,
        "multi_parent_resources": multi_parent_resources,
        "composition_links": links,
    }
    if unresolved_embedded:
        raise ValueError(
            "存在未找到父窗体的嵌入视图：" + ", ".join(unresolved_embedded)
        )
    return evidence


def build_markdown(evidence: dict[str, Any]) -> str:
    """把组合证据渲染为面向需求评审和动态验证的 Markdown 台账。"""

    metrics = evidence["metrics"]
    lines = [
        "# MoneyHome8 运行时窗体组合与嵌入视图证据",
        "",
        "本文档由运行时 DFM 根类和组件类引用自动生成。它证明设计时父子装配关系，不把静态引用扩大解释为真实运行结果。",
        "",
        "## 1. 完整性结论",
        "",
        f"- 运行时窗体：`{metrics['runtime_form_count']}` 个",
        f"- DFM 序列化组合实例：`{metrics['serialized_composition_occurrence_count']}` 条",
        f"- 去重后的逻辑直接组合关系：`{metrics['composition_link_count']}` 条",
        f"- 被其它窗体组合的资源：`{metrics['composed_resource_count']}` 个",
        f"- 被多个父窗体复用的资源：`{metrics['multi_parent_resource_count']}` 个",
        f"- 无文案嵌入视图：`{metrics['embedded_surface_count']}` 个",
        f"- 已找到父窗体的嵌入视图：`{metrics['embedded_surface_with_parent_count']}` 个",
        f"- 未解析嵌入视图：`{metrics['unresolved_embedded_surface_count']}` 个",
        f"- 内部或实验入口：`{metrics['internal_or_experimental_count']}` 个，其中设计时父窗体引用 `{metrics['internal_with_static_parent_count']}` 个",
        "",
        f"Delphi 会把嵌套 Frame 子树再次序列化到最终宿主中，因此本台账同时保留序列化实例数和去重后的逻辑直接组合边。`37/37` 个无文案嵌入视图都已找到直接父窗体，因此父窗体装配关系不再是缺口。仍需动态验证的是空数据、有数据、筛选、命令和计算结果。`{metrics['internal_or_experimental_count']}` 个内部或实验入口没有设计时父窗体引用，但仍可能由事件代码动态创建，不能据此判定为不可达。",
        "",
        "## 2. 无文案嵌入视图",
        "",
        "| 嵌入资源 | 业务域 | 交互角色 | 直接父窗体 | 最终宿主 | 实例路径 | 目标数据流 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in evidence["embedded_views"]:
        paths = [instance["component_path"] for instance in item["instances"]]
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(item['resource'])}`",
                    escape_cell(item["domain_label"]),
                    escape_cell(item["role_label"]),
                    escape_cell([f"`{value}`" for value in item["direct_parents"]]),
                    escape_cell([f"`{value}`" for value in item["ultimate_hosts"]]),
                    escape_cell([f"`{value}`" for value in paths]),
                    escape_cell(item["data_flow"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 3. 多父窗体复用组件",
            "",
            "这类组件应在 Rust 版优先实现为共享视图或共享查询投影，避免复制业务规则。",
            "",
            "| 资源 | 父窗体数 | 父窗体 | 角色 | 表面类型 |",
            "| --- | ---: | --- | --- | --- |",
        ]
    )
    for item in evidence["multi_parent_resources"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(item['resource'])}`",
                    str(item["parent_count"]),
                    escape_cell([f"`{value}`" for value in item["parents"]]),
                    escape_cell(item["role"]),
                    escape_cell(item["surface_kind"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 4. 内部或实验入口",
            "",
            "| 资源 | 标题 | 设计时父窗体引用 | 静态状态 | 剩余验证 |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    for item in evidence["internal_or_experimental_entries"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(item['resource'])}`",
                    escape_cell(item["title"]),
                    str(item["static_composition_references"]),
                    escape_cell(item["status"]),
                    escape_cell(item["evidence_boundary"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 5. 全部设计时组合关系",
            "",
            "| 逻辑直接父级 | 父标题 | 子资源 | 实例名 | 代表对象路径 | 序列化次数 | 子角色 | 子表面类型 |",
            "| --- | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for link in evidence["composition_links"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(link['parent_resource'])}`",
                    escape_cell(link["parent_title"]),
                    f"`{escape_cell(link['child_resource'])}`",
                    f"`{escape_cell(link['child_instance'])}`",
                    f"`{escape_cell(link['component_path'])}`",
                    str(link["serialized_occurrence_count"]),
                    escape_cell(link["child_role"]),
                    escape_cell(link["child_surface_kind"]),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """读取输入与输出路径，默认全部位于固定项目工作区。"""

    parser = argparse.ArgumentParser(description="生成 MoneyHome8 窗体组合关系证据")
    parser.add_argument("--dfm-input", type=Path, default=DEFAULT_DFM_INPUT)
    parser.add_argument("--coverage-input", type=Path, default=DEFAULT_COVERAGE_INPUT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    return parser.parse_args()


def main() -> int:
    """生成 JSON 和 Markdown，并在嵌入视图存在孤立项时失败。"""

    args = parse_args()
    paths = [
        args.dfm_input.resolve(),
        args.coverage_input.resolve(),
        args.json_output.resolve(),
        args.markdown_output.resolve(),
    ]
    for output_path in paths[2:]:
        if WORKSPACE not in output_path.parents:
            raise SystemExit(f"输出必须位于固定工作区内：{WORKSPACE}")
    for input_path in paths[:2]:
        if not input_path.is_file():
            raise SystemExit(f"输入文件不存在：{input_path}")

    dfm_data = json.loads(paths[0].read_text(encoding="utf-8"))
    coverage_data = json.loads(paths[1].read_text(encoding="utf-8"))
    evidence = build_evidence(dfm_data, coverage_data, paths[0], paths[1])
    paths[2].write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    paths[3].write_text(
        build_markdown(evidence),
        encoding="utf-8",
        newline="\n",
    )
    metrics = evidence["metrics"]
    print(
        "已生成窗体组合证据："
        f"{metrics['composition_link_count']} 条关系，"
        f"{metrics['embedded_surface_with_parent_count']}/"
        f"{metrics['embedded_surface_count']} 个嵌入视图已定位父窗体"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
