"""提取运行时 DFM 中的计算、汇总、报表与查询投影证据。"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = WORKSPACE / "docs" / "runtime-dfm-all-forms.json"
DEFAULT_JSON_OUTPUT = WORKSPACE / "docs" / "runtime-calculation-evidence.json"
DEFAULT_MARKDOWN_OUTPUT = (
    WORKSPACE / "docs" / "runtime-calculation-and-report-projections.md"
)
CALCULATION_EVENT_PROPERTIES = (
    "OnCalcFields",
    "OnGroupCalc",
    "OnGetFooterCellText",
    "OnIsExistFooterCell",
)
CHART_CLASS_PATTERN = re.compile(r"(?:chart|webbrowser)", re.IGNORECASE)
PROJECTION_FORM_PATTERN = re.compile(
    r"(?:STATISTIC|PROFIT|INVEST|TRANSFRAME|VIEWFRAME|WASTEBOOK|LIFETHEME)",
    re.IGNORECASE,
)
OPTION_CLASSES = {
    "TCheckBox",
    "TRadioButton",
    "TRzCheckBox",
    "TRzRadioButton",
}


def iter_nodes(
    root: dict[str, Any],
    ancestors: tuple[dict[str, Any], ...] = (),
) -> Iterable[tuple[dict[str, Any], tuple[dict[str, Any], ...]]]:
    """深度优先遍历控件树，并保留父级链以定位字段所属数据集。"""

    yield root, ancestors
    next_ancestors = (*ancestors, root)
    for child in root.get("children", []):
        yield from iter_nodes(child, next_ancestors)


def node_path(
    node: dict[str, Any], ancestors: tuple[dict[str, Any], ...]
) -> str:
    parts = [ancestor.get("name", "") for ancestor in ancestors]
    parts.append(node.get("name", ""))
    return "/".join(part for part in parts if part)


def form_title(root: dict[str, Any]) -> str:
    return str(root.get("properties", {}).get("Caption", ""))


def nearest_dataset(
    ancestors: tuple[dict[str, Any], ...]
) -> dict[str, Any] | None:
    for ancestor in reversed(ancestors):
        class_name = str(ancestor.get("class", ""))
        if class_name.endswith(("Query", "Table", "DataSet")):
            return ancestor
    return None


def unique_strings(values: Iterable[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = " ".join(str(value).replace("\r", " ").replace("\n", " ").split())
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def extract_summary_rules(
    resource_name: str,
    title: str,
    node: dict[str, Any],
    ancestors: tuple[dict[str, Any], ...],
) -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    properties = node.get("properties", {})
    for group in properties.get("SummaryGroups", []):
        for item in group.get("SummaryItems", []):
            summary_field = item.get("SummaryField")
            summary_type = item.get("SummaryType")
            # 空项只表示设计器预留的汇总槽位，不构成业务规则证据。
            if not summary_field and not summary_type:
                continue
            rules.append(
                {
                    "resource": resource_name,
                    "title": title,
                    "component": node.get("name", ""),
                    "path": node_path(node, ancestors),
                    "group": group.get("Name", ""),
                    "default_group": bool(group.get("DefaultGroup", False)),
                    "field": summary_field or "",
                    "summary_type": summary_type or "",
                    "format": item.get("SummaryFormat", ""),
                    "evidence_status": "direct_dfm_rule",
                }
            )
    return rules


def extract_form(resource_name: str, root: dict[str, Any]) -> dict[str, Any]:
    title = form_title(root)
    calculated_fields: list[dict[str, Any]] = []
    summary_rules: list[dict[str, Any]] = []
    summary_footers: list[dict[str, Any]] = []
    calculation_events: list[dict[str, Any]] = []
    field_bindings: list[dict[str, Any]] = []
    charts: list[dict[str, Any]] = []
    options: list[dict[str, Any]] = []
    tabs: list[str] = []
    datasets: list[dict[str, Any]] = []

    for node, ancestors in iter_nodes(root):
        properties = node.get("properties", {})
        class_name = str(node.get("class", ""))
        path = node_path(node, ancestors)

        field_name = properties.get("FieldName")
        if field_name:
            binding = {
                "resource": resource_name,
                "title": title,
                "component": node.get("name", ""),
                "path": path,
                "class": class_name,
                "field": str(field_name),
                "caption": str(
                    properties.get("Caption") or properties.get("DisplayLabel") or ""
                ),
                "display_format": str(properties.get("DisplayFormat", "")),
                "is_grid_column": "Grid" in class_name and "Column" in class_name,
                "is_calculated": bool(properties.get("Calculated"))
                or properties.get("FieldKind") == "fkCalculated",
            }
            field_bindings.append(binding)
            if binding["is_calculated"]:
                dataset = nearest_dataset(ancestors)
                dataset_properties = dataset.get("properties", {}) if dataset else {}
                calculated_fields.append(
                    {
                        **binding,
                        "dataset": dataset.get("name", "") if dataset else "",
                        "calculation_event": dataset_properties.get("OnCalcFields", ""),
                        "formula_status": "handler_not_present_in_dfm",
                    }
                )

        summary_rules.extend(
            extract_summary_rules(resource_name, title, node, ancestors)
        )

        if properties.get("SummaryFooterField"):
            summary_footers.append(
                {
                    "resource": resource_name,
                    "title": title,
                    "component": node.get("name", ""),
                    "path": path,
                    "field": str(field_name or ""),
                    "footer_field": str(properties["SummaryFooterField"]),
                    "evidence_status": "direct_dfm_binding",
                }
            )

        for event_property in CALCULATION_EVENT_PROPERTIES:
            event_name = properties.get(event_property)
            if event_name:
                calculation_events.append(
                    {
                        "resource": resource_name,
                        "title": title,
                        "component": node.get("name", ""),
                        "path": path,
                        "event_property": event_property,
                        "handler": str(event_name),
                        "formula_status": "handler_not_present_in_dfm",
                    }
                )

        sql_strings = properties.get("SQL.Strings")
        if sql_strings is not None or class_name.endswith(("Query", "Table", "DataSet")):
            sql_values = unique_strings(sql_strings or [])
            datasets.append(
                {
                    "resource": resource_name,
                    "title": title,
                    "component": node.get("name", ""),
                    "path": path,
                    "class": class_name,
                    "on_calc_fields": str(properties.get("OnCalcFields", "")),
                    "sql_strings": sql_values,
                    "sql_status": (
                        "static_sql_present" if sql_values else "empty_or_runtime_generated"
                    ),
                }
            )

        if CHART_CLASS_PATTERN.search(class_name):
            charts.append(
                {
                    "resource": resource_name,
                    "title": title,
                    "component": node.get("name", ""),
                    "path": path,
                    "class": class_name,
                    "caption": str(properties.get("Caption", "")),
                }
            )

        if class_name in OPTION_CLASSES and properties.get("Caption"):
            options.append(
                {
                    "component": node.get("name", ""),
                    "caption": str(properties["Caption"]),
                    "checked": bool(properties.get("Checked", False)),
                }
            )

        if class_name.endswith("TabSheet") and properties.get("Caption"):
            tabs.append(str(properties["Caption"]))

    grid_fields = [binding for binding in field_bindings if binding["is_grid_column"]]
    return {
        "resource": resource_name,
        "title": title,
        "calculated_fields": calculated_fields,
        "summary_rules": summary_rules,
        "summary_footers": summary_footers,
        "calculation_events": calculation_events,
        "field_bindings": field_bindings,
        "grid_fields": grid_fields,
        "charts": charts,
        "options": options,
        "tabs": unique_strings(tabs),
        "datasets": datasets,
    }


def build_evidence(data: dict[str, Any], source_path: Path) -> dict[str, Any]:
    forms = [
        extract_form(resource_name, root)
        for resource_name, root in sorted(data["forms"].items())
    ]
    calculated_fields = [item for form in forms for item in form["calculated_fields"]]
    summary_rules = [item for form in forms for item in form["summary_rules"]]
    summary_footers = [item for form in forms for item in form["summary_footers"]]
    calculation_events = [item for form in forms for item in form["calculation_events"]]
    datasets = [item for form in forms for item in form["datasets"]]
    reports = [
        {
            "resource": form["resource"],
            "title": form["title"],
            "tabs": form["tabs"],
            "charts": form["charts"],
            "options": form["options"],
            "grid_fields": form["grid_fields"],
            "datasets": form["datasets"],
        }
        for form in forms
        if form["resource"].startswith("TRPT")
    ]
    projection_forms = [
        {
            "resource": form["resource"],
            "title": form["title"],
            "grid_fields": form["grid_fields"],
        }
        for form in forms
        if PROJECTION_FORM_PATTERN.search(form["resource"]) and form["grid_fields"]
    ]
    return {
        "source": str(source_path),
        "evidence_scope": {
            "direct": [
                "field bindings and display formats",
                "calculated-field markers",
                "summary fields, types and formats",
                "event handler names",
                "report chart components and static options",
            ],
            "not_recovered": [
                "compiled event-handler formulas",
                "runtime-generated SQL",
                "runtime-generated report columns",
                "calculation results for representative ledger data",
            ],
        },
        "metrics": {
            "form_count": len(forms),
            "calculated_field_count": len(calculated_fields),
            "summary_rule_count": len(summary_rules),
            "summary_footer_binding_count": len(summary_footers),
            "calculation_event_count": len(calculation_events),
            "dataset_count": len(datasets),
            "dataset_with_static_sql_count": sum(
                item["sql_status"] == "static_sql_present" for item in datasets
            ),
            "report_form_count": len(reports),
            "report_chart_count": sum(len(report["charts"]) for report in reports),
            "projection_form_count": len(projection_forms),
        },
        "calculated_fields": calculated_fields,
        "summary_rules": summary_rules,
        "summary_footers": summary_footers,
        "calculation_events": calculation_events,
        "reports": reports,
        "projection_forms": projection_forms,
        "forms": forms,
    }


def escape_cell(value: Any) -> str:
    if isinstance(value, list):
        text = "；".join(str(item) for item in value)
    else:
        text = str(value or "")
    return text.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def format_field(binding: dict[str, Any]) -> str:
    label = binding.get("caption") or binding["field"]
    if label == binding["field"]:
        return f"`{binding['field']}`"
    return f"{escape_cell(label)} (`{binding['field']}`)"


def build_markdown(evidence: dict[str, Any]) -> str:
    metrics = evidence["metrics"]
    lines = [
        "# MoneyHome8 计算口径与报表查询投影",
        "",
        "本文档由 `runtime-dfm-all-forms.json` 自动生成，记录旧程序能从运行时 DFM 直接确认的计算字段、汇总规则、报表组件与字段投影，并给出 Rust + SQLite 的落地边界。",
        "",
        "## 1. 证据结论",
        "",
        f"- 扫描窗体：`{metrics['form_count']}` 个",
        f"- 计算字段：`{metrics['calculated_field_count']}` 个",
        f"- 明确汇总规则：`{metrics['summary_rule_count']}` 条",
        f"- 汇总页脚绑定：`{metrics['summary_footer_binding_count']}` 条",
        f"- 计算相关事件：`{metrics['calculation_event_count']}` 个",
        f"- 报表窗体：`{metrics['report_form_count']}` 个",
        f"- 报表图表组件：`{metrics['report_chart_count']}` 个",
        f"- DFM 内含非空静态 SQL 的数据集：`{metrics['dataset_with_static_sql_count']}` 个",
        "",
        "`FieldKind=fkCalculated`、`SummaryGroups`、字段绑定、显示格式和事件名属于直接证据。事件处理器公式、运行时 SQL、动态报表列及真实结果不在 DFM 中，必须通过代表性数据校准；本文不会把它们标为已验证。",
        "",
        "## 2. 已确认计算字段",
        "",
        "| 窗体 | 字段 | 数据集 | 计算事件 | 显示格式 | 证据边界 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in evidence["calculated_fields"]:
        lines.append(
            "| "
            + " | ".join(
                (
                    f"{escape_cell(item['title'])} (`{item['resource']}`)",
                    format_field(item),
                    f"`{escape_cell(item['dataset'])}`",
                    f"`{escape_cell(item['calculation_event'])}`",
                    f"`{escape_cell(item['display_format'])}`",
                    "确认由旧程序计算；公式待校准",
                )
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 3. 已确认汇总规则",
            "",
            "| 窗体 | 组件 | 聚合 | 字段 | 格式 |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in evidence["summary_rules"]:
        lines.append(
            "| "
            + " | ".join(
                (
                    f"{escape_cell(item['title'])} (`{item['resource']}`)",
                    f"`{escape_cell(item['component'])}`",
                    f"`{escape_cell(item['summary_type'])}`",
                    f"`{escape_cell(item['field'])}`",
                    f"`{escape_cell(item['format'])}`",
                )
            )
            + " |"
        )
    for item in evidence["summary_footers"]:
        lines.append(
            f"| {escape_cell(item['title'])} (`{item['resource']}`) | "
            f"`{escape_cell(item['component'])}` | 页脚字段绑定 | "
            f"`{escape_cell(item['field'])} -> {escape_cell(item['footer_field'])}` |  |"
        )

    lines.extend(
        [
            "",
            "## 4. 报表组件架构",
            "",
            "| 报表 | 页签 | 图表组件 | 静态序列/选项 | 静态字段列 |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for report in evidence["reports"]:
        charts = [
            f"{chart['component']}:{chart['class']}" for chart in report["charts"]
        ]
        options = [option["caption"] for option in report["options"]]
        fields = [format_field(field) for field in report["grid_fields"]]
        lines.append(
            "| "
            + " | ".join(
                (
                    f"{escape_cell(report['title'])} (`{report['resource']}`)",
                    escape_cell(report["tabs"]),
                    escape_cell(charts),
                    escape_cell(options),
                    "；".join(fields),
                )
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 5. 交易与统计投影字段",
            "",
            "下表只列出运行时网格绑定字段；字段名和中文列标题属于直接证据，字段之间的公式关系仍按待校准处理。",
            "",
            "| 窗体 | 网格投影字段 |",
            "| --- | --- |",
        ]
    )
    for projection in evidence["projection_forms"]:
        fields: list[str] = []
        seen_fields: set[tuple[str, str, str]] = set()
        for binding in projection["grid_fields"]:
            identity = (
                binding["field"],
                binding.get("caption", ""),
                binding.get("display_format", ""),
            )
            if identity in seen_fields:
                continue
            seen_fields.add(identity)
            text = format_field(binding)
            if binding.get("display_format"):
                text += f" `{escape_cell(binding['display_format'])}`"
            fields.append(text)
        label = projection["title"] or projection["resource"]
        lines.append(
            f"| {escape_cell(label)} (`{projection['resource']}`) | "
            + "；".join(fields)
            + " |"
        )

    event_counter = Counter(
        event["event_property"] for event in evidence["calculation_events"]
    )
    lines.extend(
        [
            "",
            "## 6. 未解析计算事件",
            "",
            "下列事件确认旧程序存在动态计算或自定义页脚，但 DFM 不包含处理器代码：",
            "",
        ]
    )
    for event_property, count in sorted(event_counter.items()):
        handlers = unique_strings(
            event["handler"]
            for event in evidence["calculation_events"]
            if event["event_property"] == event_property
        )
        lines.append(
            f"- `{event_property}`：{count} 处；处理器："
            + "、".join(f"`{handler}`" for handler in handlers)
        )

    lines.extend(
        [
            "",
            "## 7. SQLite 查询投影规格",
            "",
            "### 7.1 真相层与投影层",
            "",
            "- 交易、账户分录、投资成交、费用、汇率快照和附件关系是可审计真相，写入规范化表。",
            "- `FakeTransDate`、`Bala`、`IncLocal`、`ExpLocal`、`TransCheck`、`ProfitRate` 等展示或计算字段不得反向覆盖真相表；应由查询、窗口函数或应用层计算生成。",
            "- 金额使用整数最小货币单位；数量、价格、汇率和比例使用明确精度的定点值，并在 Rust 领域层统一舍入口径。",
            "- 报表筛选必须显式携带账簿、日期、账户、币种、标签和对象范围，不能依赖全局可变 SQL。",
            "",
            "### 7.2 第一批稳定投影",
            "",
            "| 投影 | 必要输出 | 用途 | 验证状态 |",
            "| --- | --- | --- | --- |",
            "| `v_ledger_entries` | 交易标识、实际/显示日期、类型、分类、账户、流入、流出、本币折算、标签、备注、对象、附件状态 | 财务记录、标签明细、账户收支 | 字段集合和三项求和已确认；折算公式待样例校准 |",
            "| `v_account_transaction_running_balance` | 账户、交易顺序、发生额、手续费、余额 | 所有账户交易明细 | `Bala` 为计算字段已确认；同日排序和期初口径待校准 |",
            "| `v_investment_position` | 对象、持仓量、成本、市值、仓位、行情价、盈亏、含费盈亏、收益率 | 证券、基金、贵金属、投资一览 | 字段和显示精度已确认；成本法与费用口径待校准 |",
            "| `v_investment_realized_profit` | 日期、对象、交易类型、价格、数量、金额、盈亏、收益率、盈利合计、亏损合计 | 投资收益和历史盈亏 | 字段及页脚绑定已确认；收益率分母待校准 |",
            "| `v_life_theme_transactions` | 标签、交易、流入、流出、账户、币种、备注 | 标签日常收支 | 流入/流出汇总已确认 |",
            "| `v_life_theme_assets` | 标签、资产名称、金额、币种、本币金额 | 标签资产 | 合计汇总已确认；跨币种折算待校准 |",
            "",
            "### 7.3 查询实现约束",
            "",
            "1. 账户余额使用按稳定业务顺序执行的 SQLite 窗口函数；排序键至少包含业务日期、创建顺序和交易标识。",
            "2. 转账、拆分行、手续费和对应账户分录在一个事务内提交，报表只读取已提交分录。",
            "3. 本币折算必须读取交易时或报告基准日的汇率快照，并在投影结果中保留使用的汇率标识。",
            "4. 投资成本、已实现盈亏、未实现盈亏和含费盈亏分别输出，不能只保留一个模糊的 `PAL` 字段。",
            "5. 图表与表格共享同一查询结果 DTO，避免旧程序式的 Web 图表和网格各自重复计算。",
            "6. 25 张报表先实现参数化仓储查询；只有稳定、复用且可测试的口径才固化为 SQLite 视图。",
            "",
            "## 8. 验收样例要求",
            "",
            "下一阶段应在 `test.mh8` 的可控副本中建立最小数据集，逐项记录旧程序结果：",
            "",
            "- 同日多笔收支、转账和手续费后的余额顺序",
            "- 两币种交易在交易日与报告日汇率下的本币金额",
            "- 股票/基金买入、部分卖出、分红和费用后的成本及盈亏",
            "- 标签同时关联流水与资产时的两类合计",
            "- 空数据、跨年、隐藏账户和已删除/作废记录的报表边界",
            "",
            "每个样例保存输入、筛选条件、表格结果、图表系列、页脚合计和导出结果；只有结果匹配后，相关公式才可从“待校准”升级为“已验证”。",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 MoneyHome8 计算与报表投影证据")
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
    json_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    markdown_output.write_text(
        build_markdown(evidence),
        encoding="utf-8",
        newline="\n",
    )
    print(
        "已生成计算证据："
        f"{evidence['metrics']['calculated_field_count']} 个计算字段，"
        f"{evidence['metrics']['summary_rule_count']} 条汇总规则，"
        f"{evidence['metrics']['report_form_count']} 张报表"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
