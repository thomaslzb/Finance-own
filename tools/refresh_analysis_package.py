"""刷新分析包的文档清单，保留既有功能统计和证据条目。"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
DOCS_DIR = WORKSPACE / "docs"
PACKAGE_PATH = DOCS_DIR / "analysis-package.json"
COVERAGE_PATH = DOCS_DIR / "runtime-form-coverage-audit.json"
COMPOSITION_PATH = DOCS_DIR / "runtime-form-composition-evidence.json"
INTERNAL_SURFACE_PATH = DOCS_DIR / "runtime-internal-surface-evidence.json"
METHOD_EVIDENCE_PATH = DOCS_DIR / "runtime-method-evidence.json"
EVENT_HANDLER_EVIDENCE_PATH = DOCS_DIR / "runtime-event-handler-evidence.json"
EVENT_DATAFLOW_PATH = DOCS_DIR / "runtime-event-command-dataflow.json"
RUNTIME_EXECUTION_QUEUE_PATH = DOCS_DIR / "runtime-execution-queue.json"
TARGET_UI_CONSOLIDATION_PATH = DOCS_DIR / "target-ui-consolidation-map.json"
SQLITE_DOMAIN_COVERAGE_PATH = DOCS_DIR / "sqlite-domain-coverage-audit.json"


def main() -> int:
    if not PACKAGE_PATH.is_file():
        raise SystemExit(f"分析包不存在：{PACKAGE_PATH}")

    package = json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))
    package["generated_on"] = date.today().isoformat()
    renamed_features = {
        "`财务报表` 真实列、聚合口径和导出格式": "`财务报表` 精确公式、排序钻取、筛选边界、导出和打印结果",
        "`财务报表` 动态列、事件公式和导出格式": "`财务报表` 精确公式、排序钻取、筛选边界、导出和打印结果",
        "导入交割单、模板、远程通知等页面的细字段与流程": "通用 XML 的完整导入语义、信用卡账单、备份压缩、附件目录、真实同步冲突/删除传播/断点续传、移动端结果和其余行情源协议",
        "通用交换文件、信用卡账单、备份压缩、附件目录和旧同步协议的动态结果": "通用 XML 的完整导入语义、信用卡账单、备份压缩、附件目录、真实同步冲突/删除传播/断点续传、移动端结果和其余行情源协议",
        "通用 XML 的完整导入语义、信用卡账单、备份压缩、附件目录和旧同步协议的动态结果": "通用 XML 的完整导入语义、信用卡账单、备份压缩、附件目录、真实同步冲突/删除传播/断点续传、移动端结果和其余行情源协议",
    }
    for feature in package.get("features", []):
        name = feature.get("name")
        if name in renamed_features:
            feature["name"] = renamed_features[name]
    renamed_gaps = {
        "财务分析诊断/规划/目标公式与真实结果": "财务分析诊断完整公式、规划逐年算法、目标边界值与失败回滚",
    }
    package["critical_open_gaps"] = [
        renamed_gaps.get(gap, gap) for gap in package.get("critical_open_gaps", [])
    ]
    # 排除清单文件自身，避免写入后文件大小再次变化导致清单立即过期。
    manifest = [
        {"name": path.name, "size": path.stat().st_size}
        for path in sorted(DOCS_DIR.iterdir(), key=lambda item: item.name.lower())
        if path.is_file() and path != PACKAGE_PATH
    ]
    package["summary"]["documents"] = len(manifest)
    if COVERAGE_PATH.is_file():
        coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
        metrics = coverage["metrics"]
        # 分析包只保留验收所需的稳定汇总，逐窗体细节仍由覆盖审计文件承载。
        package["summary"]["runtime_form_coverage"] = {
            "runtime_forms": metrics["runtime_form_count"],
            "classified_forms": metrics["classified_form_count"],
            "unclassified_forms": metrics["unclassified_form_count"],
            "business_surfaces": metrics["business_surface_count"],
            "embedded_indirect_surfaces": metrics["embedded_indirect_surface_count"],
            "internal_or_experimental": metrics["internal_or_experimental_count"],
            "technical_support": metrics["technical_support_count"],
            "commands": metrics["command_count"],
            "capability_signals": metrics["capability_signal_count"],
        }
    if COMPOSITION_PATH.is_file():
        composition = json.loads(COMPOSITION_PATH.read_text(encoding="utf-8"))
        metrics = composition["metrics"]
        package["summary"]["runtime_form_composition"] = {
            "serialized_occurrences": metrics[
                "serialized_composition_occurrence_count"
            ],
            "logical_composition_links": metrics["composition_link_count"],
            "composed_resources": metrics["composed_resource_count"],
            "multi_parent_resources": metrics["multi_parent_resource_count"],
            "embedded_surfaces": metrics["embedded_surface_count"],
            "embedded_surfaces_with_parent": metrics[
                "embedded_surface_with_parent_count"
            ],
            "unresolved_embedded_surfaces": metrics[
                "unresolved_embedded_surface_count"
            ],
        }
    if INTERNAL_SURFACE_PATH.is_file():
        internal = json.loads(INTERNAL_SURFACE_PATH.read_text(encoding="utf-8"))
        metrics = internal["metrics"]
        package["summary"]["runtime_internal_surfaces"] = {
            "experimental_surfaces": metrics["experimental_surface_count"],
            "internal_diagnostics": metrics["internal_diagnostic_count"],
            "technical_helpers": metrics["technical_helper_count"],
            "calculator_edits": metrics["calculator_edit_count"],
            "calculator_edit_forms": metrics["calculator_edit_form_count"],
            "web_browsers": metrics["web_browser_count"],
            "web_browser_forms": metrics["web_browser_form_count"],
            "external_dfm_entry_clues": metrics[
                "target_with_external_dfm_reference_count"
            ],
        }
    if METHOD_EVIDENCE_PATH.is_file():
        methods = json.loads(METHOD_EVIDENCE_PATH.read_text(encoding="utf-8"))
        metrics = methods["metrics"]
        package["summary"]["runtime_method_evidence"] = {
            "target_classes": metrics["target_class_count"],
            "published_methods": metrics["published_method_count"],
            "named_routines": metrics["named_routine_count"],
            "console_command_classes": metrics["console_command_class_count"],
            "focused_strings": len(methods["focused_strings"]),
        }
    if EVENT_HANDLER_EVIDENCE_PATH.is_file():
        handlers = json.loads(
            EVENT_HANDLER_EVIDENCE_PATH.read_text(encoding="utf-8")
        )
        metrics = handlers["metrics"]
        package["summary"]["runtime_event_handler_evidence"] = {
            "event_bindings": metrics["event_binding_count"],
            "unique_form_handlers": metrics["unique_form_handler_count"],
            "located_handlers": metrics["located_handler_count"],
            "same_name_candidates": metrics["same_name_unique_candidate_count"]
            + metrics["same_name_ambiguous_candidate_count"],
            "unresolved_handlers": metrics["unresolved_handler_count"],
            "resource_only_forms": metrics["resource_only_form_count"],
            "resource_only_handlers": metrics["resource_only_handler_count"],
            "noop_handlers": metrics["noop_handler_count"],
        }
    if EVENT_DATAFLOW_PATH.is_file():
        dataflows = json.loads(EVENT_DATAFLOW_PATH.read_text(encoding="utf-8"))
        metrics = dataflows["metrics"]
        package["summary"]["runtime_event_command_dataflow"] = {
            "commands": metrics["command_count"],
            "high_risk_candidates": metrics["high_risk_command_count"],
            "known_call_edges": metrics["known_call_edge_count"],
            "commands_with_strings": metrics["commands_with_strings"],
            "unlocated_code_commands": metrics["unlocated_code_command_count"],
            "resource_only_commands": metrics["resource_only_command_count"],
        }
    if RUNTIME_EXECUTION_QUEUE_PATH.is_file():
        queue = json.loads(RUNTIME_EXECUTION_QUEUE_PATH.read_text(encoding="utf-8"))
        metrics = queue["metrics"]
        package["summary"]["runtime_execution_queue"] = {
            "batches": metrics["batch_count"],
            "forms": metrics["form_count"],
            "actionable_commands": metrics["actionable_command_count"],
            "event_handlers": metrics["event_handler_count"],
            "high_risk_events": metrics["high_risk_event_count"],
            "embedded_forms_with_hosts": metrics["embedded_forms_with_hosts"],
            "pending_forms": metrics["status_counts"].get("pending", 0),
            "partial_forms": metrics["status_counts"].get("partial", 0),
            "blocked_forms": metrics["status_counts"].get("blocked", 0),
            "unreachable_forms": metrics["status_counts"].get("unreachable", 0),
        }
    if TARGET_UI_CONSOLIDATION_PATH.is_file():
        target_ui = json.loads(
            TARGET_UI_CONSOLIDATION_PATH.read_text(encoding="utf-8")
        )
        metrics = target_ui["metrics"]
        package["summary"]["target_ui_consolidation"] = {
            "legacy_forms": metrics["source_form_count"],
            "target_sections": metrics["target_section_count"],
            "target_surface_families": metrics["target_surface_family_count"],
            "actionable_commands": metrics["actionable_command_count"],
            "event_handlers": metrics["event_handler_count"],
            "high_risk_events": metrics["high_risk_event_count"],
            "investment_source_forms": metrics["investment_source_form_count"],
        }
    if SQLITE_DOMAIN_COVERAGE_PATH.is_file():
        sqlite_coverage = json.loads(
            SQLITE_DOMAIN_COVERAGE_PATH.read_text(encoding="utf-8")
        )
        metrics = sqlite_coverage["metrics"]
        package["summary"]["sqlite_domain_coverage"] = {
            "entity_candidates": metrics["entity_candidate_count"],
            "tables": metrics["table_count"],
            "views": metrics["view_count"],
            "indexes": metrics["index_count"],
            "adapter_artifacts": metrics["adapter_artifact_count"],
            "status_counts": metrics["status_counts"],
            "recommended_next_objects": metrics["recommended_next_object_count"],
        }
    package["docs_manifest"] = manifest
    package["critical_open_gaps"] = [
        "主账本正式表结构与样例数据",
        "通用记账、债权债务、信用卡账单、分期摊还、网贷、定期续存和银行理财生命周期的真实写入、精确公式、并发保护与失败回滚",
        "投资持仓调整、成本批次分配、实现盈亏、跨币种估值、市值变动和有数据输出的精确口径与失败回滚",
        "上市证券账户级费率、新股记录关系、证券选择、费用舍入、成本批次、代码迁移和失败回滚",
        "开放式基金与货币基金的金额/份额换算、申赎费率、收益结转、成本分配、认购、拆分和失败回滚",
        "债券净价/全价、应计利息、费用舍入、成本批次、到期/提前兑取损益、税务和失败回滚",
        "融资融券真实合同形成、单笔直接还款/还券、合同编辑、计息、偿还分配、风险指标和失败回滚",
        "保险现金价值删除/多日期、缴费/返还/分红异常、退保边界/损益/回滚、六类社保写入及旧价值增减事实迁移",
        "重大资产与家居物品的有持仓估值、卖出成本、分期完成、成本市值构成和失败回滚",
        "财务分析诊断完整公式、规划逐年算法、目标边界值与失败回滚",
        "报表精确 SQL、收益率公式、排序钻取、筛选边界、导出格式和打印结果",
        "通用 XML 的完整导入语义、信用卡账单、备份压缩、附件目录、真实同步冲突/删除传播/断点续传、移动端结果和其余行情源协议",
        "AI 动态入口、控制台命令语法与副作用、金额计算器回填行为，以及嵌入视图的空数据、有数据、筛选和交互结果；特殊表面方法合同已确认",
        "共享 UI 的日期/金额边界、键盘焦点、统计快照一致性、任务取消和 WebView 隔离；无 VMT 资源均已有范围决策",
    ]
    PACKAGE_PATH.write_text(
        json.dumps(package, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"已刷新分析包文档清单：{len(manifest)} 个文件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
