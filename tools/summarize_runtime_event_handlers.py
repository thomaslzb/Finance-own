"""生成全部 MoneyHome8 运行时窗体的 Delphi 事件处理器代码索引。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
DOCS_DIR = WORKSPACE / "docs"
DEFAULT_EXE = WORKSPACE / "tools" / "moneyhome8-runtime" / "MoneyHome8.exe"
DEFAULT_DFM = DOCS_DIR / "runtime-dfm-all-forms.json"
DEFAULT_COVERAGE = DOCS_DIR / "runtime-form-coverage-audit.json"
DEFAULT_JSON = DOCS_DIR / "runtime-event-handler-evidence.json"
DEFAULT_MARKDOWN = DOCS_DIR / "runtime-event-handler-evidence.md"

sys.path.insert(0, str(WORKSPACE / "tools"))

from extract_runtime_dfm import (  # noqa: E402
    ProcessMemoryReader,
    iter_rcdata_resources,
    wait_until_unpacked,
)
from summarize_runtime_methods import (  # noqa: E402
    disassemble_routine,
    find_pascal_string_occurrences,
    import_address_map,
    parse_method_table_before_class,
    read_image_bytes,
    read_runtime_sections,
)


HIGH_VALUE_PATTERN = (
    "TRANS",
    "REPORT",
    "RPT",
    "FINANCIAL",
    "GOAL",
    "BUDGET",
    "PLAN",
    "IMPORT",
    "EXPORT",
    "BACKUP",
    "RESTORE",
    "SYNC",
    "CREDIT",
    "DEBT",
    "SECUR",
    "FUND",
    "FOREX",
)


def iter_nodes(
    root: dict[str, Any], path: tuple[str, ...] = ()
) -> Iterable[tuple[dict[str, Any], tuple[str, ...]]]:
    """遍历 DFM 控件树并返回稳定组件路径。"""
    current = path + (str(root.get("name", "")),)
    yield root, current
    for child in root.get("children", []):
        yield from iter_nodes(child, current)


def collect_event_bindings(root: dict[str, Any]) -> list[dict[str, str]]:
    """提取所有 `On*` 属性及其处理器，保留重复绑定关系。"""
    bindings: list[dict[str, str]] = []
    for node, path in iter_nodes(root):
        for property_name, value in node.get("properties", {}).items():
            if not property_name.startswith("On") or not isinstance(value, str) or not value:
                continue
            bindings.append(
                {
                    "component": str(node.get("name", "")),
                    "component_class": str(node.get("class", "")),
                    "component_path": ".".join(item for item in path if item),
                    "event_property": property_name,
                    "handler": value,
                }
            )
    return bindings


def summarize_analysis(analysis: dict[str, Any]) -> dict[str, Any]:
    """压缩单个方法证据，保留需求追踪需要的控制流信号。"""
    instructions = analysis["instructions"]
    calls = []
    for call in analysis["calls"]:
        calls.append(
            {
                key: value
                for key, value in call.items()
                if key in {"instruction_rva", "target_rva", "import"}
            }
        )
    return {
        "instruction_count": analysis["instruction_count"],
        "is_noop": len(instructions) == 1
        and instructions[0]["mnemonic"].startswith("ret"),
        "calls": calls,
        "string_references": analysis["string_references"],
    }


def choose_method_table(
    sections: list[Any],
    class_name: str,
    expected_handlers: set[str],
    base_address: int,
    image_size: int,
) -> dict[str, Any] | None:
    """优先通过 VMT 指针读取方法表，无法定位时再使用类名邻接回退。"""
    vmt_rva = find_class_vmt_rva(sections, class_name, base_address)
    if vmt_rva is not None:
        method_table_pointer = read_image_bytes(sections, vmt_rva - 52, 4)
        if method_table_pointer is not None:
            method_table_va = struct.unpack("<I", method_table_pointer)[0]
            if base_address <= method_table_va < base_address + image_size:
                table = parse_method_table_at_rva(
                    sections,
                    method_table_va - base_address,
                    base_address,
                    image_size,
                )
                if table is not None:
                    names = {method["name"] for method in table["methods"]}
                    return {
                        "class_rva": vmt_rva,
                        "vmt_rva": vmt_rva,
                        "source": "vmt_method_table",
                        "handler_overlap": len(names & expected_handlers),
                        **table,
                    }

    candidates = []
    for class_rva in find_pascal_string_occurrences(sections, class_name):
        table = parse_method_table_before_class(
            sections, class_rva, base_address, image_size
        )
        if table is None:
            continue
        names = {method["name"] for method in table["methods"]}
        candidates.append(
            {
                "class_rva": class_rva,
                "vmt_rva": vmt_rva,
                "source": "class_name_adjacency",
                "handler_overlap": len(names & expected_handlers),
                **table,
            }
        )
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda item: (item["handler_overlap"], item["method_count"]),
    )


def parse_method_table_at_rva(
    sections: list[Any],
    table_rva: int,
    base_address: int,
    image_size: int,
) -> dict[str, Any] | None:
    """按 Delphi 7 published 方法表结构解析 VMT 指针指向的数据。"""
    count_bytes = read_image_bytes(sections, table_rva, 2)
    if count_bytes is None:
        return None
    count = struct.unpack("<H", count_bytes)[0]
    if not 1 <= count <= 4096:
        return None

    position = table_rva + 2
    methods: list[dict[str, Any]] = []
    for _ in range(count):
        header = read_image_bytes(sections, position, 7)
        if header is None:
            return None
        entry_length = struct.unpack_from("<H", header, 0)[0]
        code_va = struct.unpack_from("<I", header, 2)[0]
        name_length = header[6]
        if entry_length != 7 + name_length:
            return None
        raw_name = read_image_bytes(sections, position + 7, name_length)
        if raw_name is None:
            return None
        try:
            name = raw_name.decode("ascii")
        except UnicodeDecodeError:
            return None
        if not name or not all(ch.isalnum() or ch == "_" for ch in name):
            return None
        if not base_address <= code_va < base_address + image_size:
            return None
        methods.append(
            {
                "name": name,
                "entry_length": entry_length,
                "code_va": code_va,
                "code_rva": code_va - base_address,
            }
        )
        position += entry_length
    return {
        "table_rva": table_rva,
        "method_count": count,
        "methods": methods,
    }


def find_class_vmt_rva(
    sections: list[Any], class_name: str, base_address: int
) -> int | None:
    """通过 `vmtClassName` 和 `vmtSelfPtr` 定位主模块内的 Delphi VMT。"""
    for name_rva in find_pascal_string_occurrences(sections, class_name):
        pointer = struct.pack("<I", base_address + name_rva)
        for section in sections:
            start = 0
            while True:
                offset = section.data.find(pointer, start)
                if offset < 0:
                    break
                vmt_rva = section.rva + offset + 44
                self_pointer = read_image_bytes(sections, vmt_rva - 76, 4)
                instance_size_bytes = read_image_bytes(sections, vmt_rva - 40, 4)
                if self_pointer is not None and instance_size_bytes is not None:
                    self_va = struct.unpack("<I", self_pointer)[0]
                    instance_size = struct.unpack("<I", instance_size_bytes)[0]
                    if self_va == base_address + vmt_rva and 4 <= instance_size < 0x100000:
                        return vmt_rva
                start = offset + 1
    return None


def read_u32(memory: ProcessMemoryReader, address: int) -> int | None:
    """读取绝对地址中的无符号 32 位值，地址不可读时返回空。"""
    try:
        return struct.unpack("<I", memory.read_address(address, 4))[0]
    except OSError:
        return None


def read_short_string(memory: ProcessMemoryReader, address: int) -> str | None:
    """读取 Delphi ShortString 类名。"""
    try:
        length = memory.read_address(address, 1)[0]
        if not 1 <= length <= 200:
            return None
        return memory.read_address(address + 1, length).decode("ascii")
    except (OSError, UnicodeDecodeError):
        return None


def class_name_from_vmt(memory: ProcessMemoryReader, vmt_va: int) -> str | None:
    """从 VMT 的 `vmtClassName` 槽读取类名。"""
    name_va = read_u32(memory, vmt_va - 44)
    return None if name_va is None else read_short_string(memory, name_va)


def resolve_class_hierarchy(
    memory: ProcessMemoryReader,
    sections: list[Any],
    class_name: str,
    base_address: int,
    image_size: int,
) -> list[dict[str, Any]]:
    """沿 `vmtParent` 恢复当前类到 VCL 基类的真实继承链。"""
    vmt_rva = find_class_vmt_rva(sections, class_name, base_address)
    if vmt_rva is None:
        return []
    current_vmt = base_address + vmt_rva
    seen: set[int] = set()
    hierarchy: list[dict[str, Any]] = []
    while current_vmt and current_vmt not in seen and len(hierarchy) < 64:
        seen.add(current_vmt)
        current_name = class_name_from_vmt(memory, current_vmt)
        if current_name is None:
            break
        in_main_image = base_address <= current_vmt < base_address + image_size
        hierarchy.append(
            {
                "class_name": current_name,
                "vmt_va": current_vmt,
                "vmt_rva": current_vmt - base_address if in_main_image else None,
                "in_main_image": in_main_image,
            }
        )
        parent_reference = read_u32(memory, current_vmt - 36)
        if not parent_reference:
            break
        parent_vmt = read_u32(memory, parent_reference)
        if not parent_vmt:
            break
        current_vmt = parent_vmt
    return hierarchy


def is_high_value(resource: str, class_name: str, title: str) -> bool:
    """标记交易、报表、规划、交换和投资等高价值业务窗体。"""
    haystack = f"{resource} {class_name} {title}".upper()
    return any(token in haystack for token in HIGH_VALUE_PATTERN)


def collect_runtime_evidence(
    exe_path: Path,
    dfm_data: dict[str, Any],
    coverage_data: dict[str, Any],
) -> dict[str, Any]:
    """从隔离运行副本匹配全部窗体的 DFM 事件和 published 方法。"""
    forms = dfm_data["forms"]
    coverage_by_resource = {
        item["resource"]: item for item in coverage_data["forms"]
    }
    environment = os.environ.copy()
    environment["__COMPAT_LAYER"] = "RunAsInvoker"
    process = subprocess.Popen([str(exe_path)], cwd=str(exe_path.parent), env=environment)
    try:
        import pefile

        pe = pefile.PE(str(exe_path), fast_load=False)
        resources = iter_rcdata_resources(pe)
        memory: ProcessMemoryReader | None = None
        deadline = time.monotonic() + 5.0
        while memory is None and time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(f"MoneyHome8 隔离副本提前退出：{process.returncode}")
            try:
                memory = ProcessMemoryReader(process.pid)
            except OSError:
                time.sleep(0.1)
        if memory is None:
            raise TimeoutError("无法在限定时间内读取 MoneyHome8 隔离副本")

        with memory:
            wait_until_unpacked(memory, resources, timeout_seconds=5.0)
            sections = read_runtime_sections(pe, memory)
            base_address = memory.base_address
            image_size = int(pe.OPTIONAL_HEADER.SizeOfImage)
            imports = import_address_map(pe, base_address)
            form_records: list[dict[str, Any]] = []
            global_method_sources: dict[str, list[dict[str, Any]]] = defaultdict(list)
            disassembly_cache: dict[int, dict[str, Any]] = {}
            ancestor_table_cache: dict[str, dict[str, Any] | None] = {}
            hierarchy_cache: dict[str, list[dict[str, Any]]] = {}

            for resource, root in forms.items():
                class_name = str(root.get("class", ""))
                title = str(root.get("properties", {}).get("Caption", ""))
                bindings = collect_event_bindings(root)
                handlers = sorted({item["handler"] for item in bindings})
                table = choose_method_table(
                    sections,
                    class_name,
                    set(handlers),
                    base_address,
                    image_size,
                )
                methods = [] if table is None else table["methods"]
                method_by_name = {method["name"]: method for method in methods}
                for method in methods:
                    global_method_sources[method["name"]].append(
                        {
                            "resource": resource,
                            "class_name": class_name,
                            "code_rva": method["code_rva"],
                        }
                    )
                direct_handlers = []
                for handler in handlers:
                    method = method_by_name.get(handler)
                    if method is None:
                        continue
                    code_rva = method["code_rva"]
                    if code_rva not in disassembly_cache:
                        disassembly_cache[code_rva] = summarize_analysis(
                            disassemble_routine(
                                sections,
                                code_rva,
                                base_address,
                                image_size,
                                imports,
                            )
                        )
                    direct_handlers.append(
                        {
                            "handler": handler,
                            "code_rva": code_rva,
                            "analysis": disassembly_cache[code_rva],
                        }
                    )
                coverage = coverage_by_resource.get(resource, {})
                if class_name not in hierarchy_cache:
                    hierarchy_cache[class_name] = resolve_class_hierarchy(
                        memory,
                        sections,
                        class_name,
                        base_address,
                        image_size,
                    )
                form_records.append(
                    {
                        "resource": resource,
                        "class_name": class_name,
                        "title": title,
                        "domain": coverage.get("domain", "未归类"),
                        "role": coverage.get("role", "unknown"),
                        "surface_kind": coverage.get("surface_kind", "unknown"),
                        "high_value": is_high_value(resource, class_name, title),
                        "event_binding_count": len(bindings),
                        "unique_handler_count": len(handlers),
                        "event_bindings": bindings,
                        "method_table": None
                        if table is None
                        else {
                            "class_rva": table["class_rva"],
                            "vmt_rva": table.get("vmt_rva"),
                            "table_rva": table["table_rva"],
                            "source": table["source"],
                            "published_method_count": table["method_count"],
                            "handler_overlap": table["handler_overlap"],
                        },
                        "published_methods": methods,
                        "direct_handlers": direct_handlers,
                        "class_hierarchy": hierarchy_cache[class_name],
                        "inherited_handlers": [],
                        "unmatched_handlers": sorted(set(handlers) - set(method_by_name)),
                    }
                )

            for form in form_records:
                remaining = set(form["unmatched_handlers"])
                for ancestor in form["class_hierarchy"][1:]:
                    if not remaining or not ancestor["in_main_image"]:
                        continue
                    ancestor_name = ancestor["class_name"]
                    if ancestor_name not in ancestor_table_cache:
                        ancestor_table_cache[ancestor_name] = choose_method_table(
                            sections,
                            ancestor_name,
                            remaining,
                            base_address,
                            image_size,
                        )
                    table = ancestor_table_cache[ancestor_name]
                    if table is None:
                        continue
                    method_by_name = {
                        method["name"]: method for method in table["methods"]
                    }
                    for method in table["methods"]:
                        source = {
                            "resource": None,
                            "class_name": ancestor_name,
                            "code_rva": method["code_rva"],
                        }
                        if source not in global_method_sources[method["name"]]:
                            global_method_sources[method["name"]].append(source)
                    for handler in sorted(remaining & set(method_by_name)):
                        method = method_by_name[handler]
                        code_rva = method["code_rva"]
                        if code_rva not in disassembly_cache:
                            disassembly_cache[code_rva] = summarize_analysis(
                                disassemble_routine(
                                    sections,
                                    code_rva,
                                    base_address,
                                    image_size,
                                    imports,
                                )
                            )
                        form["inherited_handlers"].append(
                            {
                                "handler": handler,
                                "declaring_class": ancestor_name,
                                "code_rva": code_rva,
                                "analysis": disassembly_cache[code_rva],
                            }
                        )
                        remaining.remove(handler)
                form["unmatched_handlers"] = sorted(remaining)

            for form in form_records:
                resolutions = []
                for handler in form["unmatched_handlers"]:
                    candidates = [
                        item
                        for item in global_method_sources.get(handler, [])
                        if item["resource"] != form["resource"]
                    ]
                    candidates = list(
                        {
                            (item["class_name"], item["code_rva"]): item
                            for item in candidates
                        }.values()
                    )
                    if len(candidates) == 1:
                        status = "same_name_unique_candidate"
                    elif candidates:
                        status = "same_name_ambiguous_candidate"
                    else:
                        status = "unresolved"
                    resolutions.append(
                        {
                            "handler": handler,
                            "status": status,
                            "candidate_count": len(candidates),
                            "candidates": candidates[:20],
                        }
                    )
                form["unmatched_handler_resolutions"] = resolutions
                if form["method_table"] is not None:
                    form["code_linkage_status"] = "current_class_method_table"
                elif form["class_hierarchy"]:
                    form["code_linkage_status"] = "ancestor_vmt_only"
                else:
                    form["code_linkage_status"] = "resource_only_no_vmt"

            return build_result(
                exe_path,
                form_records,
                base_address,
                image_size,
                disassembly_cache,
            )
    finally:
        # 只回收本工具启动的无账本副本，不影响用户其它 MoneyHome8 实例。
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2.0)


def build_result(
    exe_path: Path,
    forms: list[dict[str, Any]],
    base_address: int,
    image_size: int,
    disassembly_cache: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    """计算全局与按业务域汇总指标。"""
    domain_rows: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    status_counts: Counter[str] = Counter()
    for form in forms:
        row = domain_rows[form["domain"]]
        row["forms"] += 1
        row["event_bindings"] += form["event_binding_count"]
        row["unique_handlers"] += form["unique_handler_count"]
        row["direct_handlers"] += len(form["direct_handlers"])
        row["inherited_handlers"] += len(form["inherited_handlers"])
        for resolution in form["unmatched_handler_resolutions"]:
            status_counts[resolution["status"]] += 1
            row[resolution["status"]] += 1
    published_methods = {
        (form["class_name"], method["name"], method["code_rva"])
        for form in forms
        for method in form["published_methods"]
    }
    direct_handler_keys = {
        (form["resource"], handler["handler"])
        for form in forms
        for handler in form["direct_handlers"]
    }
    inherited_handler_keys = {
        (form["resource"], handler["handler"])
        for form in forms
        for handler in form["inherited_handlers"]
    }
    resource_only_forms = [
        form
        for form in forms
        if form.get("code_linkage_status") == "resource_only_no_vmt"
        and form["event_binding_count"] > 0
    ]
    noop_handlers = [
        {
            "resource": form["resource"],
            "class_name": form["class_name"],
            "title": form["title"],
            "handler": handler["handler"],
            "code_rva": handler["code_rva"],
        }
        for form in forms
        for handler in form["direct_handlers"]
        if handler["analysis"]["is_noop"]
    ]
    return {
        "source_exe": str(exe_path),
        "source_sha256": hashlib.sha256(exe_path.read_bytes()).hexdigest(),
        "image_base": base_address,
        "image_size": image_size,
        "metrics": {
            "runtime_form_count": len(forms),
            "forms_with_events": sum(form["event_binding_count"] > 0 for form in forms),
            "event_binding_count": sum(form["event_binding_count"] for form in forms),
            "unique_form_handler_count": sum(form["unique_handler_count"] for form in forms),
            "classes_with_method_table": sum(form["method_table"] is not None for form in forms),
            "classes_without_method_table": sum(form["method_table"] is None for form in forms),
            "published_method_count": len(published_methods),
            "direct_handler_count": len(direct_handler_keys),
            "inherited_handler_count": len(inherited_handler_keys),
            "located_handler_count": len(direct_handler_keys)
            + len(inherited_handler_keys),
            "same_name_unique_candidate_count": status_counts[
                "same_name_unique_candidate"
            ],
            "same_name_ambiguous_candidate_count": status_counts[
                "same_name_ambiguous_candidate"
            ],
            "unresolved_handler_count": status_counts["unresolved"],
            "resource_only_form_count": len(resource_only_forms),
            "resource_only_handler_count": sum(
                form["unique_handler_count"] for form in resource_only_forms
            ),
            "disassembled_code_entry_count": len(disassembly_cache),
            "handlers_with_strings": sum(
                bool(analysis["string_references"])
                for analysis in disassembly_cache.values()
            ),
            "noop_handler_count": len(noop_handlers),
            "high_value_form_count": sum(form["high_value"] for form in forms),
        },
        "domain_summary": [
            {"domain": domain, **dict(values)}
            for domain, values in sorted(domain_rows.items())
        ],
        "forms": forms,
        "noop_handlers": noop_handlers,
    }


def escape_cell(value: Any) -> str:
    """转义 Markdown 表格单元格。"""
    if isinstance(value, list):
        text = "；".join(str(item) for item in value)
    else:
        text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def render_markdown(evidence: dict[str, Any]) -> str:
    """生成人工审阅用的全量事件处理器覆盖摘要。"""
    metrics = evidence["metrics"]
    lines = [
        "# MoneyHome8 全量运行时事件处理器证据",
        "",
        "本文件由 `tools/summarize_runtime_event_handlers.py` 从隔离运行副本的 Delphi published RTTI 和全部运行时 DFM 生成。",
        "",
        "## 1. 覆盖摘要",
        "",
        f"- 运行时窗体：`{metrics['runtime_form_count']}` 个",
        f"- 含事件窗体：`{metrics['forms_with_events']}` 个",
        f"- DFM 事件绑定：`{metrics['event_binding_count']}` 条",
        f"- 按窗体去重处理器：`{metrics['unique_form_handler_count']}` 个",
        f"- 直接定位到当前类代码：`{metrics['direct_handler_count']}` 个",
        f"- 沿真实父类链定位：`{metrics['inherited_handler_count']}` 个",
        f"- 已定位代码合计：`{metrics['located_handler_count']}` 个",
        f"- 唯一同名候选：`{metrics['same_name_unique_candidate_count']}` 个",
        f"- 多个同名候选：`{metrics['same_name_ambiguous_candidate_count']}` 个",
        f"- 完全未定位：`{metrics['unresolved_handler_count']}` 个",
        f"- 有事件但无可执行 VMT 的资源窗体：`{metrics['resource_only_form_count']}` 个，涉及 `{metrics['resource_only_handler_count']}` 个处理器",
        f"- published 方法：`{metrics['published_method_count']}` 个",
        f"- 已反汇编代码入口：`{metrics['disassembled_code_entry_count']}` 个",
        f"- 含字符串引用处理器：`{metrics['handlers_with_strings']}` 个",
        f"- 空实现处理器：`{metrics['noop_handler_count']}` 个",
        "",
        "## 2. 按业务域覆盖",
        "",
        "| 业务域 | 窗体 | 事件绑定 | 去重处理器 | 当前类 | 父类链 | 唯一同名 | 多同名 | 未定位 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in evidence["domain_summary"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(row["domain"]),
                    str(row.get("forms", 0)),
                    str(row.get("event_bindings", 0)),
                    str(row.get("unique_handlers", 0)),
                    str(row.get("direct_handlers", 0)),
                    str(row.get("inherited_handlers", 0)),
                    str(row.get("same_name_unique_candidate", 0)),
                    str(row.get("same_name_ambiguous_candidate", 0)),
                    str(row.get("unresolved", 0)),
                ]
            )
            + " |"
        )

    unresolved_forms = [
        form
        for form in evidence["forms"]
        if any(
            item["status"] == "unresolved"
            for item in form["unmatched_handler_resolutions"]
        )
    ]
    lines.extend(
        [
            "",
            "## 3. 完全未定位处理器",
            "",
            "| 资源 | 类 | 标题 | 未定位处理器 |",
            "|---|---|---|---|",
        ]
    )
    for form in unresolved_forms:
        names = [
            item["handler"]
            for item in form["unmatched_handler_resolutions"]
            if item["status"] == "unresolved"
        ]
        lines.append(
            f"| `{form['resource']}` | `{form['class_name']}` | "
            f"{escape_cell(form['title'])} | {escape_cell(names)} |"
        )
    if not unresolved_forms:
        lines.append("| - | - | - | 无 |")

    high_value = [form for form in evidence["forms"] if form["high_value"]]
    high_value.sort(
        key=lambda item: (len(item["direct_handlers"]), item["event_binding_count"]),
        reverse=True,
    )
    lines.extend(
        [
            "",
            "## 4. 高价值业务窗体代码覆盖",
            "",
            "| 资源 | 标题 | 业务域 | 绑定 | 当前类 | 父类链 | 未匹配 |",
            "|---|---|---|---:|---:|---:|---:|",
        ]
    )
    for form in high_value:
        lines.append(
            f"| `{form['resource']}` | {escape_cell(form['title'])} | "
            f"{escape_cell(form['domain'])} | {form['event_binding_count']} | "
            f"{len(form['direct_handlers'])} | {len(form['inherited_handlers'])} | "
            f"{len(form['unmatched_handlers'])} |"
        )

    lines.extend(
        [
            "",
            "## 5. 空实现处理器",
            "",
            "| 资源 | 标题 | 处理器 | 代码 RVA |",
            "|---|---|---|---:|",
        ]
    )
    for item in evidence["noop_handlers"]:
        lines.append(
            f"| `{item['resource']}` | {escape_cell(item['title'])} | "
            f"`{item['handler']}` | `0x{item['code_rva']:x}` |"
        )
    if not evidence["noop_handlers"]:
        lines.append("| - | - | 无 | - |")

    lines.extend(
        [
            "",
            "## 6. 证据边界",
            "",
            "- `直接命中` 表示处理器名称存在于当前窗体类的 Delphi published 方法表，代码地址可直接证明。",
            "- `父类链` 表示通过当前类 VMT 的 `vmtParent` 逐级定位到真实祖先类方法表。",
            "- `同名候选` 是父类链仍未覆盖时在其它类中发现的同名方法，只用于检索，不能证明继承或实现归属。",
            "- `resource_only_no_vmt` 表示资源中存在窗体和事件绑定，但当前主程序映像没有该类的可执行 VMT；应按未链接、未启用或历史资源候选处理，并由动态验证决定是否进入重构范围。",
            "- 字符串和调用引用可用于定位校验、提示、文件、网络和数据访问路径，但不能单独证明运行时分支一定执行。",
            "- 动态页面、真实输入输出和数据副作用仍按 `runtime-validation-scenarios.md` 校准。",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 MoneyHome8 全量事件处理器证据")
    parser.add_argument("--exe", type=Path, default=DEFAULT_EXE)
    parser.add_argument("--dfm", type=Path, default=DEFAULT_DFM)
    parser.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    return parser.parse_args()


def workspace_output(path: Path) -> Path:
    """限制生成文件位于固定项目工作区。"""
    resolved = path.resolve()
    if WORKSPACE != resolved and WORKSPACE not in resolved.parents:
        raise SystemExit(f"输出必须位于固定工作区内：{WORKSPACE}")
    return resolved


def main() -> int:
    args = parse_args()
    exe_path = args.exe.resolve()
    dfm_path = args.dfm.resolve()
    coverage_path = args.coverage.resolve()
    json_path = workspace_output(args.json)
    markdown_path = workspace_output(args.markdown)
    for path in (exe_path, dfm_path, coverage_path):
        if not path.is_file():
            raise SystemExit(f"输入文件不存在：{path}")
    evidence = collect_runtime_evidence(
        exe_path,
        json.loads(dfm_path.read_text(encoding="utf-8")),
        json.loads(coverage_path.read_text(encoding="utf-8")),
    )
    json_path.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    markdown_path.write_text(
        render_markdown(evidence), encoding="utf-8", newline="\n"
    )
    metrics = evidence["metrics"]
    print(
        "已生成全量事件处理器证据："
        f"{metrics['direct_handler_count']} 当前类 + "
        f"{metrics['inherited_handler_count']} 父类 / "
        f"{metrics['unique_form_handler_count']} 个处理器总计，"
        f"{metrics['unresolved_handler_count']} 个未定位"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
