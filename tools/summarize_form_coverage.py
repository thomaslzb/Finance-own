"""生成 MoneyHome8 全量运行时窗体的功能覆盖与数据流审计。"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
DEFAULT_DFM_INPUT = WORKSPACE / "docs" / "runtime-dfm-all-forms.json"
DEFAULT_COMMAND_INPUT = WORKSPACE / "docs" / "runtime-command-state-evidence.json"
DEFAULT_JSON_OUTPUT = WORKSPACE / "docs" / "runtime-form-coverage-audit.json"
DEFAULT_MARKDOWN_OUTPUT = WORKSPACE / "docs" / "runtime-form-coverage-audit.md"
RUNTIME_ARTIFACT_DIR = WORKSPACE / "artifacts" / "runtime-validation"

OBSERVED_DYNAMIC_STATUS = "representative_runtime_validation_observed"

DOMAIN_LABELS = {
    "system_shell": "账簿生命周期与系统壳层",
    "auth_sync_external": "登录、同步与外部服务",
    "accounts_master_data": "账户与基础资料",
    "transactions": "通用交易、流水与模板",
    "debts_credit": "债权债务、信用与摊销",
    "financial_products": "存款与银行理财产品",
    "foreign_exchange": "外汇",
    "investment_shared": "投资公共能力",
    "securities": "证券",
    "funds": "基金与货币基金",
    "bonds": "债券",
    "futures_metals": "期货、黄金与贵金属",
    "margin_financing": "融资融券",
    "insurance_social": "保险与社会保障",
    "major_tangible_assets": "重大资产与家居物品",
    "planning_budget_goal": "预算、提醒、规划与目标",
    "import_export": "导入导出",
    "reports": "报表与分析投影",
    "tools_longtail": "辅助工具与长尾能力",
    "shared_infrastructure": "共享 UI 与技术支撑",
}

EXPLICIT_DOMAINS = {
    "TADJUSTHELDDLGFM": "investment_shared",
    "TALIPAYVIEWFRAME": "transactions",
    "TAMOUNTSCREENINGFRAME": "shared_infrastructure",
    "TCARDVIEWFRAME": "debts_credit",
    "TCURRDEPOSITSVIEWFRAME": "financial_products",
    "TDEFERREDVIEWFRAME": "debts_credit",
    "TEDITASSETBUYDLGFM": "major_tangible_assets",
    "TEDITBANKMONEYPRODUCTDLGFM": "financial_products",
    "TEDITCATGORYORDERDLGFM": "accounts_master_data",
    "THISTORYPROFITFRAME": "investment_shared",
    "TINVESTFEEDLGFM": "investment_shared",
    "TINVESTMENTCHARTFRAME": "investment_shared",
    "TINVESTMENTLISTFM": "investment_shared",
    "TMARKETCONSTITUTESFRAME": "investment_shared",
    "TSELECTREPETITIONFREQUENCYDLGFM": "planning_budget_goal",
    "TSELECTSECURITIESCODEDLGFM": "securities",
    "TUNEARNEDVIEWFRAME": "debts_credit",
    "TUSABLEMONEYCHARTFRAME": "reports",
}

DOMAIN_RULES = (
    (
        "system_shell",
        r"ABOUT|BACKUPBOOK|CHECKBOOK|NEWBOOK|RESTOREBOOK|SYSTEMSETTINGS|"
        r"SHORTCUTMANAGE|PASSWORD|PWDCHECK|PWDCHANGE|MAINFORM|GUIDEDLG|"
        r"SPLASHFORM|REGISTERFORM|UPDATEVERIFYCODE",
    ),
    (
        "auth_sync_external",
        r"LOGINDIALOG|SYNCUSER|REMOTENOTIFICATION|ONLINEGETDATA",
    ),
    (
        "planning_budget_goal",
        r"BUDGET|REMIND|FINANCIALDIAGNOSIS|FINANCIALPLANNING|^TFP|GOAL|"
        r"FINANCIALCALENDAR|PLANLIST|NORMALPLAN|PARENTPLAN|PLANINSURE|"
        r"BUYFUNDPLAN|TRANSACTIONPLAN|XFERPLAN|INCEXPPLAN",
    ),
    ("import_export", r"IMPORT|EXPORT"),
    ("reports", r"^TRPT|^TREPORT"),
    ("insurance_social", r"INSURE|SOCIALSECURITY"),
    (
        "margin_financing",
        r"MARGIN|EQUITY|FINANCING|SHORTSELL|EXERTION|QUITEXERTION|"
        r"COLLATERAL|COUPONS|DIRECTPAYMENT|BATCHDIRECT|SELLCOUPONS",
    ),
    ("futures_metals", r"FUTURES|GOLD|PRECIOUS"),
    ("bonds", r"NMARKETBOND|MARKETDEBT|BONDS|STOCKBONDMATURE"),
    ("funds", r"OPENFUND|^TFUND|CURRFUND"),
    (
        "securities",
        r"SECURITY|^TSTOCK|RELATIONNEWSTOCK|FEESET|ACCOUNTFEE",
    ),
    ("foreign_exchange", r"FOREIGN|CURREXCHANGE|CURRCHGXFER|^TEXCHANGE"),
    ("financial_products", r"FIXED|FIXDEP|^TMONEY|LZCASHDEP"),
    ("major_tangible_assets", r"^TASSET|^TPRAC"),
    (
        "debts_credit",
        r"CLAIMS|DEBT|CREDIT|PAYABLE|RECEIVABLE|PREPAID|PREPAYMENT|"
        r"ADVANCE|BLOCKUP|DRAWALCARD|COSTDETAILS|CHANGEPAYMODE|"
        r"REPAYMENT|NEWBLOCK",
    ),
    (
        "accounts_master_data",
        r"ACCOUNT|ACCT|CATEGORY|PERSON|^TCURR(?:DLG|LIST)|^TRATEFM|"
        r"INFORMATION|TAG|THEME|CUSTOMNAVIGATION",
    ),
    (
        "transactions",
        r"TRANS|INCEXP|CASH|CURRENT|THIRDDEPOSIT|WASTEBOOK|EXPENSE|"
        r"INSTALLMENT|TEMPLATE|FIND|FILTER|CUSTCOLUMN|NEWREC|INPUTTEXT|"
        r"PAYROLL|RECHARGE",
    ),
    (
        "tools_longtail",
        r"ACCESSORIES|DIARY|CALCULATOR|CALCU|CLEANPRICE|MANAGEBILL|"
        r"MODIFYBILL|SOFTINDEX|CUSTOMER|AIPANEL|CONSOLE|MONTHDAY",
    ),
    (
        "shared_infrastructure",
        r"CHILDFORM|DIALOGFORM|DROPDOWNDATE|DROPFM|FMCUSTOMDIALOG|"
        r"MHFRAME|MISCDIALOG|MWADJUSTBUTTONDROP|MWSELECT|NODEWRAPFORM|"
        r"OKCANCELDIALOG|PAGECONTRL|PROGRESSFORM|RZFRMCUSTOMIZE|"
        r"SELECTDATERANGE|STATISTICFRAME|STATISTICGRIDFRAME|"
        r"STATISTICTREE|THEMEUIFM|VIEWFRAME",
    ),
)

ROLE_LABELS = {
    "ledger_lifecycle": "账簿生命周期命令",
    "external_adapter": "外部服务与同步",
    "data_exchange": "数据交换",
    "report_projection": "报表查询投影",
    "projection_view": "统计/图表/嵌入视图",
    "transaction_editor": "业务交易录入",
    "transaction_history": "交易明细与历史",
    "account_editor": "账户配置",
    "catalog_editor": "基础资料维护",
    "planning_workflow": "预算/提醒/规划工作流",
    "selector_filter": "选择、筛选与查找",
    "configuration_editor": "配置与调整",
    "tool_window": "辅助工具",
    "application_shell": "应用壳层与导航",
    "shared_infrastructure": "共享技术组件",
}

EXPLICIT_ROLES = {
    "TABOUTFORM": "application_shell",
    "TACCOUNTOVERVIEWDLGFM": "projection_view",
    "TACCTGUIDEMAIN": "account_editor",
    "TASSETINVESTDLGFM": "transaction_editor",
    "TASSETSDLGFM": "projection_view",
    "TDEBTINVESTMENTACCTLISTFRAME": "projection_view",
    "TDEBTINVESTMENTPAYOBJECTFRAME": "projection_view",
    "TDEBTINVESTMENTPAYTABLEFRAME": "projection_view",
    "THISTORYPROFITFRAME": "projection_view",
    "TINVESTFEEDLGFM": "transaction_editor",
    "TCALCUFM": "shared_infrastructure",
}

INTERNAL_OR_EXPERIMENTAL = {
    "TAIPANELDLG",
    "TCONSOLEFM",
}

TECHNICAL_RESOURCES = {"TCALCUFM", "TSPLASHFORM"}

FLOW_BY_ROLE = {
    "ledger_lifecycle": "账簿文件/SQLite -> 打开、备份、还原、结算 -> 账簿上下文",
    "external_adapter": "本地领域对象 <-> DTO/协议适配 -> 远端服务或通知",
    "data_exchange": "外部来源 -> 暂存/映射/预览 -> 领域命令或导出投影",
    "report_projection": "SQLite 真相 -> 参数化查询 -> 表格/图表/导出",
    "projection_view": "领域查询 -> 聚合/估值 -> 嵌入式列表、统计或图表",
    "transaction_editor": "用户输入 -> 领域校验 -> 原子分录/专项扩展事务",
    "transaction_history": "已提交交易 -> 查询投影 -> 明细操作与下游报表",
    "account_editor": "账户配置 -> 账户真相 -> 余额、估值与导航投影",
    "catalog_editor": "基础资料 -> 业务引用 -> 交易、预算、报表与同步",
    "planning_workflow": "规则/专题输入 + 真相投影 -> 计划、提醒、目标或预测结果",
    "selector_filter": "候选数据 -> 用户范围选择 -> 上游命令或查询参数",
    "configuration_editor": "配置/调整输入 -> 领域规则或显示状态持久化",
    "tool_window": "辅助输入或计算 -> 领域命令、参考数据或外部程序",
    "application_shell": "导航/命令状态 -> 应用服务 -> 业务窗体与当前上下文",
    "shared_infrastructure": "父窗体状态 -> 复用控件 -> 选择、展示或交互反馈",
}

EVENT_PROPERTIES = ("OnClick", "OnExecute", "OnDblClick", "OnPopup", "OnShortCut")
COMMAND_CLASS_PATTERN = re.compile(
    r"(?:Button|MenuItem|Action|CheckBox|RadioButton|ToolButton)$", re.IGNORECASE
)


def iter_nodes(root: dict[str, Any]) -> Iterable[dict[str, Any]]:
    yield root
    for child in root.get("children", []):
        yield from iter_nodes(child)


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(flatten_strings(item))
        return result
    return []


def unique_strings(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = " ".join(value.replace("\r", " ").replace("\n", " ").split())
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def classify_domain(resource: str) -> tuple[str, str]:
    if resource in EXPLICIT_DOMAINS:
        return EXPLICIT_DOMAINS[resource], "explicit_override"
    for domain, pattern in DOMAIN_RULES:
        if re.search(pattern, resource, re.IGNORECASE):
            return domain, "ordered_name_rule"
    raise ValueError(f"未分类运行时窗体：{resource}")


def infer_role(resource: str, domain: str) -> str:
    if resource in EXPLICIT_ROLES:
        return EXPLICIT_ROLES[resource]
    if re.search(r"BACKUPBOOK|RESTOREBOOK|CHECKBOOK|NEWBOOK", resource):
        return "ledger_lifecycle"
    if domain == "auth_sync_external":
        return "external_adapter"
    if domain == "import_export":
        return "data_exchange"
    if domain == "reports":
        return "report_projection"
    if resource == "TMAINFORM" or re.search(r"SOFTINDEXCENTERFORM", resource):
        return "application_shell"
    if re.search(r"STATISTIC|CHART|MARKETCONSTITUTES|VIEWFRAME|CONTAINER", resource):
        return "projection_view"
    if re.search(r"TRANSFM$|TRANSFRAME$|TRANSACTIONLIST|WASTEBOOK", resource):
        return "transaction_history"
    if re.search(
        r"BUY|SELL|REDEEM|MATURE|WITHDRAW|BORROW|LEND|RETURN|REPAY|"
        r"DIVID|INTEREST|XFER|EXCHANGE|PAYFEE|GETFEE|BALA(?:IN|OUT)|"
        r"ENCASH|INCREMENT|RECHARGE|PAYROLL|EXPENSE|INCEXP|"
        r"TRANS(?:DLG|FER)|ADJUSTHELD|EXERTION|SHORTSELL|FINANCING|"
        r"DIRECTPAYMENT|COUPON|BLOCKUP|OTHERFEE|CASHAHEAD|REWARD|"
        r"BADTRANS|LOAN",
        resource,
    ):
        return "transaction_editor"
    if re.search(r"NEWACCT|ACCTDLG|ACCOUNTDLG|ACCOUNTMANAGER", resource):
        return "account_editor"
    if re.search(r"BUDGET|REMIND|FINANCIAL|^TFP|GOAL|PLAN", resource):
        return "planning_workflow"
    if re.search(r"SELECT|FILTER|FIND|DROP|AMOUNTSCREENING", resource):
        return "selector_filter"
    if re.search(r"LISTFM$|CATEGORY|PERSON|CURRDLG|RATEFM|INFORMATION", resource):
        return "catalog_editor"
    if re.search(r"EDIT|SET|CUSTOM|SORT|CHANGE|MANAGE", resource):
        return "configuration_editor"
    if domain == "tools_longtail":
        return "tool_window"
    if domain == "shared_infrastructure":
        return "shared_infrastructure"
    return "configuration_editor"


def is_command(node: dict[str, Any]) -> bool:
    properties = node.get("properties", {})
    class_name = str(node.get("class", ""))
    if (
        any(properties.get(event_name) for event_name in EVENT_PROPERTIES)
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


def extract_form(
    resource: str,
    root: dict[str, Any],
    command_form: dict[str, Any],
) -> dict[str, Any]:
    domain, classification_source = classify_domain(resource)
    role = infer_role(resource, domain)
    title = str(root.get("properties", {}).get("Caption", ""))
    nodes = list(iter_nodes(root))
    fields = unique_strings(
        str(node.get("properties", {}).get(property_name, ""))
        for node in nodes
        for property_name in ("FieldName", "DataField")
        if node.get("properties", {}).get(property_name)
    )
    tabs = unique_strings(
        str(node.get("properties", {}).get("Caption", ""))
        for node in nodes
        if str(node.get("class", "")).endswith("TabSheet")
    )
    options = unique_strings(
        str(node.get("properties", {}).get("Caption", ""))
        for node in nodes
        if str(node.get("class", "")).endswith(("CheckBox", "RadioButton"))
        and node.get("properties", {}).get("Caption")
    )
    command_labels = unique_strings(
        str(command.get("label", "")) for command in command_form.get("commands", [])
    )
    capability_signals = unique_strings((title, *tabs, *options, *command_labels))
    if resource in INTERNAL_OR_EXPERIMENTAL:
        surface_kind = "internal_or_experimental"
    elif domain == "shared_infrastructure" or resource in TECHNICAL_RESOURCES:
        surface_kind = "technical_support"
    elif not capability_signals:
        surface_kind = "embedded_indirect_surface"
    else:
        surface_kind = "business_surface"
    if surface_kind == "technical_support" and not command_form.get("commands"):
        dynamic_result_status = "not_applicable_or_parent_driven"
    elif surface_kind == "embedded_indirect_surface":
        dynamic_result_status = "parent_driven_structure_only"
    elif surface_kind == "internal_or_experimental":
        dynamic_result_status = "pending_reachability_and_product_scope_decision"
    else:
        dynamic_result_status = "pending_representative_runtime_validation"
    return {
        "resource": resource,
        "class": root.get("class", ""),
        "title": title,
        "domain": domain,
        "domain_label": DOMAIN_LABELS[domain],
        "classification_source": classification_source,
        "role": role,
        "role_label": ROLE_LABELS[role],
        "data_flow": FLOW_BY_ROLE[role],
        "surface_kind": surface_kind,
        "structure_status": "direct_runtime_dfm",
        "dynamic_result_status": dynamic_result_status,
        "control_count": len(nodes),
        "command_count": len(command_form.get("commands", [])),
        "field_count": len(fields),
        "fields": fields,
        "tabs": tabs,
        "options": options,
        "command_labels": command_labels,
        "capability_signals": capability_signals,
    }


def build_evidence(
    dfm_data: dict[str, Any],
    command_data: dict[str, Any],
    dfm_source: Path,
    command_source: Path,
    preserved_dynamic_statuses: dict[str, str],
    passed_resources: set[str],
) -> dict[str, Any]:
    command_forms = {form["resource"]: form for form in command_data["forms"]}
    forms = [
        extract_form(
            resource,
            root,
            command_forms.get(resource, {"commands": []}),
        )
        for resource, root in sorted(dfm_data["forms"].items())
    ]
    for form in forms:
        resource = form["resource"]
        if resource in passed_resources:
            form["dynamic_result_status"] = OBSERVED_DYNAMIC_STATUS
        elif resource in preserved_dynamic_statuses:
            form["dynamic_result_status"] = preserved_dynamic_statuses[resource]
    if len(forms) != dfm_data["form_count"]:
        raise ValueError("窗体数量与 DFM 汇总不一致")
    classified_resources = {form["resource"] for form in forms}
    missing = sorted(set(dfm_data["forms"]) - classified_resources)
    if missing:
        raise ValueError(f"存在未覆盖窗体：{', '.join(missing)}")

    domain_counts = Counter(form["domain"] for form in forms)
    role_counts = Counter(form["role"] for form in forms)
    dynamic_status_counts = Counter(form["dynamic_result_status"] for form in forms)
    return {
        "sources": {
            "runtime_dfm": str(dfm_source),
            "command_evidence": str(command_source),
        },
        "evidence_boundary": {
            "proved": [
                "全部运行时 DFM 资源均已分类",
                "窗体标题、字段绑定、页签、静态选项、命令标题和事件数量",
                "每个窗体到业务域、交互角色和建议数据流的可追溯映射",
            ],
            "inferred_design": [
                "业务域由有序名称规则和少量显式消歧映射确定",
                "数据流描述是 Rust + SQLite 的目标边界，不要求复刻旧表结构",
            ],
            "not_proved": [
                "每个窗体在真实菜单中的可达条件和视觉布局",
                "事件处理器内部公式、校验、级联和副作用",
                "代表性数据写入、计算、导入导出和同步结果",
            ],
        },
        "metrics": {
            "runtime_form_count": len(forms),
            "classified_form_count": len(classified_resources),
            "unclassified_form_count": len(missing),
            "business_surface_count": sum(
                form["surface_kind"] == "business_surface" for form in forms
            ),
            "embedded_indirect_surface_count": sum(
                form["surface_kind"] == "embedded_indirect_surface"
                for form in forms
            ),
            "internal_or_experimental_count": sum(
                form["surface_kind"] == "internal_or_experimental"
                for form in forms
            ),
            "technical_support_count": sum(
                form["surface_kind"] == "technical_support" for form in forms
            ),
            "command_count": sum(form["command_count"] for form in forms),
            "field_binding_count": sum(form["field_count"] for form in forms),
            "capability_signal_count": sum(
                len(form["capability_signals"]) for form in forms
            ),
            "domain_counts": {
                domain: domain_counts.get(domain, 0) for domain in DOMAIN_LABELS
            },
            "role_counts": {
                role: role_counts.get(role, 0) for role in ROLE_LABELS
            },
            "dynamic_status_counts": dict(sorted(dynamic_status_counts.items())),
        },
        "forms": forms,
    }


def load_preserved_dynamic_statuses(path: Path) -> dict[str, str]:
    """保留人工确认的动态状态，避免静态审计刷新时回退历史进度。"""

    if not path.is_file():
        return {}
    previous = json.loads(path.read_text(encoding="utf-8"))
    return {
        form["resource"]: form["dynamic_result_status"]
        for form in previous.get("forms", [])
        if form.get("dynamic_result_status") == OBSERVED_DYNAMIC_STATUS
    }


def load_passed_resources() -> set[str]:
    """从每个执行条目的最新运行记录中提取已经通过的资源。"""

    latest: dict[str, tuple[str, str]] = {}
    if not RUNTIME_ARTIFACT_DIR.is_dir():
        return set()
    for path in sorted(RUNTIME_ARTIFACT_DIR.glob("RT-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        execution_id = record.get("execution_id")
        observed_at = record.get("observed_at")
        resource = record.get("resource")
        status = record.get("result", {}).get("status")
        if not execution_id or not observed_at or not resource or not status:
            raise SystemExit(f"动态观察记录缺少关键字段：{path}")
        current = latest.get(execution_id)
        if current is None or observed_at > current[0]:
            latest[execution_id] = (observed_at, resource if status == "pass" else "")
    return {resource for _, resource in latest.values() if resource}


def escape_cell(value: Any) -> str:
    if isinstance(value, list):
        value = "；".join(str(item) for item in value)
    return str(value or "").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def compact_signals(form: dict[str, Any], limit: int = 6) -> str:
    signals = form["capability_signals"]
    shown = signals[:limit]
    suffix = f"；另 {len(signals) - limit} 项" if len(signals) > limit else ""
    return "；".join(shown) + suffix


def build_markdown(evidence: dict[str, Any]) -> str:
    metrics = evidence["metrics"]
    forms = evidence["forms"]
    lines = [
        "# MoneyHome8 全量运行时窗体覆盖审计",
        "",
        "本文档由运行时 DFM 和命令证据自动生成，用于证明每一个已恢复窗体都进入功能与数据流台账。分类是重构需求映射，不要求新 SQLite 沿用旧数据库结构。",
        "",
        "## 1. 完整性结论",
        "",
        f"- 运行时窗体：`{metrics['runtime_form_count']}` 个",
        f"- 已分类窗体：`{metrics['classified_form_count']}` 个",
        f"- 未分类窗体：`{metrics['unclassified_form_count']}` 个",
        f"- 业务功能表面：`{metrics['business_surface_count']}` 个",
        f"- 父窗体驱动的无文案嵌入视图：`{metrics['embedded_indirect_surface_count']}` 个",
        f"- 内部或实验入口：`{metrics['internal_or_experimental_count']}` 个",
        f"- 共享 UI / 技术支撑：`{metrics['technical_support_count']}` 个",
        f"- 命令与交互控件：`{metrics['command_count']}` 个",
        f"- 去重字段绑定：`{metrics['field_binding_count']}` 个",
        f"- 标题、命令、页签和选项功能信号：`{metrics['capability_signal_count']}` 条",
        f"- 已有代表性运行证据：`{metrics['dynamic_status_counts'].get(OBSERVED_DYNAMIC_STATUS, 0)}` 个",
        "",
        "生成器在出现未分类窗体时直接失败，因此 `未分类窗体=0` 是分析包的硬门槛。无文案嵌入视图必须通过父窗体和调用方验证；`AI`、控制台和内部计算窗体先列为内部/实验入口，不能未经运行证据就纳入正式产品范围。这里证明的是静态结构与需求归属完整，不等于 460 个窗体的动态结果已经逐一实测。",
        "",
        "## 2. 业务域覆盖",
        "",
        "| 业务域 | 窗体数 | 主要数据流 |",
        "| --- | ---: | --- |",
    ]
    for domain, label in DOMAIN_LABELS.items():
        domain_forms = [form for form in forms if form["domain"] == domain]
        flows = unique_strings(form["data_flow"] for form in domain_forms)
        lines.append(
            f"| {label} (`{domain}`) | {len(domain_forms)} | {escape_cell(flows)} |"
        )

    lines.extend(
        [
            "",
            "## 3. 交互角色覆盖",
            "",
            "| 角色 | 窗体数 | 数据流合同 |",
            "| --- | ---: | --- |",
        ]
    )
    for role, label in ROLE_LABELS.items():
        lines.append(
            f"| {label} (`{role}`) | {metrics['role_counts'][role]} | "
            f"{escape_cell(FLOW_BY_ROLE[role])} |"
        )

    lines.extend(
        [
            "",
            "## 4. 逐窗体覆盖矩阵",
            "",
            "| 资源 | 标题 | 业务域 | 角色 | 命令 | 字段 | 功能信号 | 动态状态 |",
            "| --- | --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for form in forms:
        lines.append(
            "| "
            + " | ".join(
                (
                    f"`{form['resource']}`",
                    escape_cell(form["title"]),
                    escape_cell(form["domain_label"]),
                    escape_cell(form["role_label"]),
                    str(form["command_count"]),
                    str(form["field_count"]),
                    escape_cell(compact_signals(form)),
                    escape_cell(form["dynamic_result_status"]),
                )
            )
            + " |"
        )

    internal_forms = [
        form for form in forms if form["surface_kind"] == "internal_or_experimental"
    ]
    embedded_forms = [
        form
        for form in forms
        if form["surface_kind"] == "embedded_indirect_surface"
    ]
    lines.extend(
        [
            "",
            "## 5. 特殊覆盖状态",
            "",
            "### 5.1 内部或实验入口",
            "",
            "| 资源 | 标题 | 当前处理 |",
            "| --- | --- | --- |",
        ]
    )
    for form in internal_forms:
        lines.append(
            f"| `{form['resource']}` | {escape_cell(form['title'])} | "
            "保留资源与命令证据；动态确认可达性和业务价值后再决定是否进入正式产品范围 |"
        )
    lines.extend(
        [
            "",
            "### 5.2 父窗体驱动的无文案嵌入视图",
            "",
            "这些框架本身没有标题、命令或静态选项，功能语义来自父窗体装配、字段绑定或运行时数据源。不能把它们当成独立页面，也不能因无文案而删除。",
            "",
            "| 资源 | 业务域 | 角色 | 字段数 |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for form in embedded_forms:
        lines.append(
            f"| `{form['resource']}` | {escape_cell(form['domain_label'])} | "
            f"{escape_cell(form['role_label'])} | {form['field_count']} |"
        )
    lines.extend(
        [
            "",
            "## 6. 对开发需求的约束",
            "",
            "1. 每个业务窗体必须对应应用命令、查询端口或配置端口，UI 不得直接访问 SQLite 表。",
            "2. 同一业务域中的录入窗体、交易明细、统计视图和报表共享领域对象及金额/数量/汇率口径。",
            "3. 技术支撑窗体不单独形成业务模块，但其筛选、选择、日期、进度和命令状态能力必须由共享组件承接。",
            "4. 旧窗体名仅用于追溯；新系统可以合并重复页面，但合并后必须保留矩阵中的功能信号和数据流结果。",
            "5. 删除旧功能或将多个窗体合并为一个工作流时，验收记录必须回指本矩阵中的全部相关资源。",
            "6. 代表性动态验证优先覆盖有命令的业务表面，再覆盖父窗体驱动的嵌入式统计和技术组件。",
            "",
            "## 7. 尚未证明的部分",
            "",
            "- 菜单可达性、动态启用条件和窗口跳转",
            "- 每个事件处理器的校验、确认、级联与持久化副作用",
            "- 交易、投资、预算、规划和报表的真实计算结果",
            "- 导入导出、备份还原、附件和同步的真实格式与协议结果",
            "",
            "这些项目继续由 `runtime-validation-scenarios.md` 管理；不得因为静态覆盖率达到 100% 就宣称动态功能完全兼容。",
            "",
        ]
    )
    return "\n".join(lines)


def ensure_workspace_path(path: Path) -> Path:
    resolved = path.resolve()
    if WORKSPACE != resolved and WORKSPACE not in resolved.parents:
        raise SystemExit(f"输出必须位于固定工作区内：{WORKSPACE}")
    return resolved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成全量运行时窗体覆盖审计")
    parser.add_argument("--dfm-input", type=Path, default=DEFAULT_DFM_INPUT)
    parser.add_argument("--command-input", type=Path, default=DEFAULT_COMMAND_INPUT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dfm_input = args.dfm_input.resolve()
    command_input = args.command_input.resolve()
    json_output = ensure_workspace_path(args.json_output)
    markdown_output = ensure_workspace_path(args.markdown_output)
    for path in (dfm_input, command_input):
        if not path.is_file():
            raise SystemExit(f"输入不存在：{path}")

    evidence = build_evidence(
        json.loads(dfm_input.read_text(encoding="utf-8")),
        json.loads(command_input.read_text(encoding="utf-8")),
        dfm_input,
        command_input,
        load_preserved_dynamic_statuses(json_output),
        load_passed_resources(),
    )
    json_output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    markdown_output.write_text(
        build_markdown(evidence), encoding="utf-8", newline="\n"
    )
    metrics = evidence["metrics"]
    print(
        "已生成全量窗体覆盖审计："
        f"{metrics['classified_form_count']}/{metrics['runtime_form_count']} 已分类，"
        f"{metrics['unclassified_form_count']} 个未分类，"
        f"{metrics['command_count']} 个命令"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
