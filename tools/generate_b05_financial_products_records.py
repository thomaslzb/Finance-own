"""生成 B05 存款与银行理财功能的运行态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
QUEUE_PATH = ROOT / "docs" / "runtime-execution-queue.json"
OBSERVED_AT = "2026-07-30T07:54:14+08:00"
OUTPUT_STAMP = "20260730T075414+0800"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "9EDF9111BA5DB1FC19E9A3BC9B5435322E8B4A202C958F9CAB11E32055C2BD17"
FINAL_HASH = "8E57AC3FC7B8F43CDBA50382117622B52E5664F9E5EE68C57CA3E979C180FB10"
BACKUP_ARTIFACT = (
    "artifacts/runtime-validation/backups/"
    "test-before-b05-financial-products-20260730.mh8"
)
NOTES = "artifacts/runtime-validation/B05-financial-products-notes.md"
CONTRACT = "docs/runtime-deposits-and-bank-wealth-contract.md"
STATIC_CATALOG = "docs/runtime-dfm-control-catalog.md"
COMPOSITION = "docs/runtime-form-composition-evidence.md"
EVENT_FLOW = "docs/runtime-event-command-dataflow.md"


def shot(name: str) -> str:
    """返回本轮脱敏截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/screenshots/{name}"


def legacy_shot(name: str) -> str:
    """返回早期动态截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/{name}"


def evidence(kind: str, path: str, description: str) -> dict:
    """构造统一证据项。"""

    return {"kind": kind, "path": path, "description": description}


def state(name: str, observations: str, *paths: str, status: str = "observed") -> dict:
    """构造页面状态并保留动态与静态证据边界。"""

    result = {"name": name, "status": status, "observations": observations}
    if paths:
        result["evidence_paths"] = list(paths)
    return result


def command(
    component: str,
    label: str,
    trigger: str,
    outcome: str,
    *,
    status: str = "partial",
    confirmation: str | None = None,
    enabled: bool = True,
) -> dict:
    """构造命令观察；未验证业务写入时不标记为通过。"""

    return {
        "component": component,
        "label": label,
        "initial_state": {"enabled": enabled, "visible": True},
        "trigger": trigger,
        "confirmation": confirmation,
        "outcome": outcome,
        "status": status,
    }


COMMON_REQUIREMENTS = [
    "定期存款账户与单笔存单必须分层，存单保存本金、类型、起息日、期限、利率、到期日和续存规则。",
    "续存必须引用原存单并生成新周期，不能覆盖原起息日、利率、期限和到期金额。",
    "银行理财产品目录、账户、持仓和现金流事件必须使用稳定 ID 分层关联。",
    "银行理财按本金管理，不得套用基金份额和净值模型。",
    "申购、赎回、到期、分红、其它费用和利息收入必须使用不同事件类型。",
    "本金、实际现金流、收益和费用必须分别保存，并在同一事务中生成平衡分录。",
    "金额、利率、期限单位、业务日期、计息基数和舍入规则必须显式保存。",
    "持仓、交易、历史盈亏、产品资料和账户概况必须读取同一数据版本与估值日期。",
    "未通过旧软件真实样本验证前，不得把到期本息、收益预测或旧格式标记为已兼容。",
]


PREVIOUS_RECORDS = {
    "RT-05-006": "artifacts/runtime-validation/RT-05-006-20260729T102603+0800.json",
    "RT-05-008": "artifacts/runtime-validation/RT-05-008-20260729T131339+0800.json",
    "RT-05-011": "artifacts/runtime-validation/RT-05-011-20260729T131339+0800.json",
}


DYNAMIC = {
    "RT-05-001": {
        "entry": "财智8 -> 资料管理 -> 银行理财产品 -> 新增产品",
        "states": [
            state(
                "产品编辑器",
                "产品名称、产品代码、币种、发行机构、收益起始日、委托期、收益终止日、预期年收益率和是否保本均可编辑。",
                shot("b05-bank-wealth-product-editor-sanitized.png"),
            )
        ],
        "commands": [
            command("产品列表", "新增产品", "点击新增产品", "打开 TEditBankMoneyProductDlgFm。", status="pass"),
            command("产品编辑器", "保存", "本轮未提交", "产品校验、唯一性、保存和回滚待验证。", status="pending"),
        ],
        "summary": "银行理财产品编辑器字段和取消路径已动态确认。",
        "gaps": ["产品保存、修改、注销和删除", "重复代码、日期冲突、持仓引用和失败回滚"],
    },
    "RT-05-002": {
        "entry": "定期存单到期生命周期 -> 续存",
        "reachable": False,
        "unreachable_reason": "现有到期存单工作区未显示续存命令，今日提醒为空；仅确认静态字段。",
        "states": [
            state("静态结构", "续存窗体包含存单、存期、存款类型、年利率、可用资金和续存金额。", STATIC_CATALOG),
            state("动态入口", "现有到期存单和今日提醒均未暴露续存入口。", shot("b05-fixed-certificate-operation-menu.png"), NOTES, status="pending"),
        ],
        "summary": "续存字段由静态证据确认，动态入口未到达。",
        "gaps": ["自动和手工续存入口", "续存本金、利率、期限、新存单生成和事务回滚"],
    },
    "RT-05-003": {
        "entry": "账户中心 -> 定期 -> 双击存单账户",
        "states": [
            state(
                "定期账户编辑",
                "账户名称、存单号、币种、所有者、存款类型、起存日、本金、存期、年利率、开户银行、账户组、资金来源、标签、自动续存、备注和附件均可见。",
                shot("b05-fixed-account-editor-sanitized.png"),
            )
        ],
        "summary": "定期存款账户编辑器和取消路径已动态确认。",
        "gaps": ["字段修改和保存", "余额、资金来源、到期日重算、引用保护和失败回滚"],
    },
    "RT-05-004": {
        "entry": "资产侧栏 -> 定期存单",
        "states": [
            state(
                "存单统计列表",
                "列表展示账户/存单名称、存款类型、存期、起存日、到期日、年利率、余额和到期本息。",
                shot("b05-fixed-workspace-sanitized.png"),
            )
        ],
        "summary": "定期存单统计框架和主要列已动态确认。",
        "gaps": ["排序、分组、到期筛选和大数据分页", "到期本息公式、跨币种合计和刷新一致性"],
    },
    "RT-05-005": {
        "entry": "账户中心 -> 定期 -> 选择存单账户",
        "states": [
            state("交易明细", "工作区包含存单统计、交易明细、记账、日期范围、查找和操作入口。", shot("b05-fixed-workspace-sanitized.png")),
            state("账户概况", "账户概况页加载 TFixDepositsViewFrame。", shot("b05-fixed-account-overview-sanitized.png")),
        ],
        "summary": "TFixedDepositTransFm 的交易明细和账户概况两个主视图已动态到达。",
        "gaps": ["新增存单、存取款和到期交易保存", "筛选、导出、删除、并发刷新和失败回滚"],
    },
    "RT-05-006": {
        "entry": "顶部记账菜单 -> 存款",
        "states": [
            state("历史存款编辑器", "既有记录已确认存款账户、资金来源、金额、日期、标签、备注和取消路径。", PREVIOUS_RECORDS["RT-05-006"], legacy_shot("cash-deposit-dialog.png"))
        ],
        "summary": "普通存款入口和字段已有历史动态证据。",
        "gaps": ["账户候选、币种与金额边界", "双边分录、余额刷新、保存和失败回滚"],
    },
    "RT-05-007": {
        "entry": "账户中心 -> 银行理财产品 -> 临时账户 -> 修改账户",
        "states": [
            state(
                "理财账户编辑",
                "账户名称、币种、所有者、备注、创建日期、开户机构和默认资金账户的自身/其它模式均可见。",
                shot("b05-bank-wealth-account-editor-sanitized.png"),
            ),
            state(
                "临时账户生命周期",
                "零余额临时账户用于到达空工作区；删除确认明确指向临时名称，删除后筛选页不再显示该账户。",
                shot("b05-temp-account-delete-confirmation.png"),
                NOTES,
            ),
        ],
        "commands": [
            command("银行理财账户向导", "完成", "创建零余额临时账户", "账户创建成功并可进入工作区。", status="pass"),
            command("账户操作菜单", "删除账户", "按精确账户名确认删除", "临时账户从筛选和侧栏移除。", status="pass", confirmation="确认框必须显示 Codex-B05-Money-20260730。"),
        ],
        "summary": "银行理财账户创建、编辑器到达、空工作区和精确删除已动态完成。",
        "gaps": ["非零余额与默认资金账户保存", "已有持仓或交易时的删除保护和失败回滚"],
    },
    "RT-05-008": {
        "entry": "记账 -> 更多交易活动 -> 银行理财 -> 银行理财产品申购",
        "states": [
            state("历史申购编辑器", "既有记录确认理财账户、产品、申购本金、资金账户、日期、标签、备注和取消路径。", PREVIOUS_RECORDS["RT-05-008"], legacy_shot("bank-wealth-subscribe-dialog.png")),
            state("命令分组", "银行理财子菜单包含申购、赎回、分红、其它费用和利息收入。", legacy_shot("bookkeeping-bank-wealth-popup.png")),
        ],
        "summary": "银行理财申购入口、按本金录入和取消路径已有动态证据。",
        "gaps": ["产品条款快照、日期和资金在途", "持仓本金、资金分录、保存和失败回滚"],
    },
    "RT-05-009": {
        "entry": "财智8 -> 资料管理 -> 银行理财产品",
        "states": [
            state(
                "空产品目录",
                "列表列出代码、产品名称、币种、收益起始日、委托期、收益终止日、预期年收益率和已注销；当前测试库为空。",
                shot("b05-master-data-menu.png"),
                shot("b05-bank-wealth-product-list-sanitized.png"),
            )
        ],
        "summary": "银行理财产品目录入口、列和空状态已动态确认。",
        "gaps": ["搜索、修改、注销、导出和打印", "大数据分页、重复代码和历史交易引用保护"],
    },
    "RT-05-010": {
        "entry": "银行理财持仓生命周期 -> 到期",
        "reachable": False,
        "unreachable_reason": "产品目录与持仓均为空，顶部理财记账菜单没有到期命令；仅确认静态字段。",
        "states": [
            state("静态结构", "到期窗体包含理财账户、到期本金、资金账户和收益。", STATIC_CATALOG),
            state("动态前置条件", "产品目录和临时账户持仓为空，没有创建虚假产品或持仓。", shot("b05-bank-wealth-product-list-sanitized.png"), shot("b05-bank-wealth-workspace-sanitized.png"), status="pending"),
        ],
        "summary": "银行理财到期字段由静态证据确认，动态前置数据不存在。",
        "gaps": ["到期入口和可到期持仓选择", "本金、收益、费用、资金到账、保存和失败回滚"],
    },
    "RT-05-011": {
        "entry": "记账 -> 更多交易活动 -> 银行理财 -> 银行理财产品赎回",
        "states": [
            state("历史赎回编辑器", "既有记录确认赎回本金、实际收回金额、只读赎回损益、资金账户、日期和取消路径。", PREVIOUS_RECORDS["RT-05-011"], legacy_shot("bank-wealth-redeem-dialog.png"))
        ],
        "summary": "银行理财赎回入口、本金和实际现金流字段已有动态证据。",
        "gaps": ["部分与全部赎回、提前赎回条款", "损益公式、持仓减少、资金到账和失败回滚"],
    },
    "RT-05-012": {
        "entry": "资产侧栏 -> 临时银行理财账户",
        "states": [
            state(
                "持仓统计框",
                "上半部分按产品展示产品名称、机构、累计金额、占比、购买日、到期日和预计年收益率；空账户无持仓行。",
                shot("b05-bank-wealth-workspace-sanitized.png"),
            )
        ],
        "summary": "银行理财持仓统计框及空状态已动态确认。",
        "gaps": ["当前持仓与历史产品筛选", "市值、占比、收益率公式、排序和跨币种合计"],
    },
    "RT-05-013": {
        "entry": "账户中心 -> 银行理财产品 -> 临时账户",
        "states": [
            state("交易明细", "空账户显示无交易记录，并提供记账、单个产品交易明细、日期范围、查找和操作。", shot("b05-bank-wealth-workspace-sanitized.png")),
            state("四个主视图", "页签为交易明细、市值构成、历史盈亏和产品资料。", shot("b05-bank-wealth-product-info-sanitized.png")),
        ],
        "summary": "TMoneyTransFm 及四个主视图已动态到达。",
        "gaps": ["有效持仓、交易和历史盈亏数据", "筛选、下钻、导出、分页和刷新冲突"],
    },
    "RT-05-014": {
        "entry": "银行理财工作区 -> 交易明细",
        "states": [
            state("交易框架", "TMoneyTransFrame 动态加载在交易明细页，提供记账、产品范围、日期范围、查找和操作；空账户显示明确空状态。", shot("b05-bank-wealth-workspace-sanitized.png"), COMPOSITION)
        ],
        "summary": "银行理财交易明细框的宿主、命令区和空状态已动态确认。",
        "gaps": ["各事件的金额方向和余额列", "批量、搜索、修改、删除、导出和大数据分页"],
    },
    "RT-05-015": {
        "entry": "账户中心 -> 新增账户 -> 储蓄卡 -> 定期",
        "states": [
            state("账户资料", "第一步包含名称、币种、所有者、备注和账户组。", shot("b05-fixed-wizard-step1.png")),
            state("存款条款", "第二步包含存款类型、存期及单位、年利率、起存日和到期自动续存。", shot("b05-fixed-wizard-step2.png")),
            state("金额与来源", "第三步包含存款金额和可选资金来源；本轮在完成前关闭。", shot("b05-fixed-wizard-step3.png")),
        ],
        "summary": "定期存款三步开户向导和取消路径已动态确认。",
        "gaps": ["有效创建、默认值来源和日期重算", "资金分录、重复名称、回滚和创建后工作区刷新"],
    },
    "RT-05-016": {
        "entry": "账户概况宿主 -> 活期存款概况",
        "reachable": False,
        "unreachable_reason": "本轮未打开 TAccountOverviewDlgFm 的活期存款内嵌视图；仅确认最终宿主。",
        "states": [
            state("最终宿主", "TCurrDepositsViewFrame 由 TAccountOverviewDlgFm 承载。", COMPOSITION, STATIC_CATALOG),
            state("动态内容", "活期存款概况未在本轮单独显示。", NOTES, status="pending"),
        ],
        "summary": "活期存款概况的最终宿主已确认，内容未动态到达。",
        "gaps": ["账户字段、余额和联系方式", "修改入口、附件、隐藏和注销状态"],
    },
    "RT-05-017": {
        "entry": "定期存单工作区 -> 账户概况",
        "states": [
            state(
                "定期账户概况",
                "内嵌帧显示账户名称、类型、币种、所有者、存单号、备注、存款条款、开户银行、联系方式、账户组、标签、附件和到期状态。",
                shot("b05-fixed-account-overview-sanitized.png"),
                COMPOSITION,
            )
        ],
        "summary": "TFixDepositsViewFrame 已通过最终宿主动态到达。",
        "gaps": ["修改后的即时刷新", "到期、隐藏、注销、附件和敏感信息掩码"],
    },
    "RT-05-018": {
        "entry": "银行理财工作区 -> 产品资料",
        "states": [
            state(
                "产品资料帧",
                "内嵌帧显示产品名称、代码、币种、发行机构、收益起始日、委托期、收益终止日、预期年收益率和是否保本。",
                shot("b05-bank-wealth-product-info-sanitized.png"),
                COMPOSITION,
            )
        ],
        "summary": "TMoneyInfoViewFrame 已通过银行理财工作区动态到达。",
        "gaps": ["选择有效产品后的值与条款快照", "注销产品、修改刷新和历史持仓一致性"],
    },
    "RT-05-019": {
        "entry": "账户概况宿主 -> 银行理财产品概况",
        "reachable": False,
        "unreachable_reason": "本轮未打开 TAccountOverviewDlgFm 的银行理财内嵌视图；仅确认最终宿主。",
        "states": [
            state("最终宿主", "TMoneyProductsViewFrame 由 TAccountOverviewDlgFm 承载。", COMPOSITION, STATIC_CATALOG),
            state("相邻动态证据", "银行理财账户、持仓统计和产品资料已在交易工作区动态确认。", shot("b05-bank-wealth-workspace-sanitized.png"), shot("b05-bank-wealth-product-info-sanitized.png"), status="pending"),
        ],
        "summary": "银行理财账户概况的最终宿主已确认，独立内容未动态到达。",
        "gaps": ["账户概况字段和聚合口径", "修改入口、附件、隐藏、注销和持仓刷新"],
    },
}


def fixed_deposit_flow(role: str) -> dict:
    """生成定期存款账户、存单和续存的保守数据流。"""

    if role in {"transaction_history", "projection_view"}:
        return {
            "inputs": ["存款账户范围、存款类型、到期状态、日期、币种和估值日期"],
            "reads": ["账户、存单、条款版本、交易、资金分录、标签和附件"],
            "writes": ["查询不写业务事实；修改和到期操作通过独立领域命令"],
            "derived_results": ["余额、到期日、到期本息、交易余额和账户概况"],
            "side_effects": ["页签、筛选和分组切换只改变查询参数"],
            "rollback": "查询失败保留上次稳定快照；写命令失败不保留单边余额或半个续存周期。",
        }
    return {
        "inputs": ["账户、币种、存款类型、本金、起息日、期限、利率、资金来源、标签和备注"],
        "reads": ["账户状态、资金来源余额、存款规则、原存单和当前版本"],
        "writes": ["本轮未提交；真实保存应写账户、存单、条款快照、资金分录和审计事件"],
        "derived_results": ["到期日、到期本息、可用资金、续存金额和新存单条款"],
        "side_effects": ["本轮只观察或取消，没有提交定期存款业务交易"],
        "rollback": "账户、存单、资金分录和续存事件必须原子提交，任一失败时整体回滚。",
    }


def bank_wealth_flow(role: str) -> dict:
    """生成银行理财产品、账户、持仓和事件的保守数据流。"""

    if role in {"transaction_history", "projection_view"}:
        return {
            "inputs": ["理财账户、产品范围、持仓状态、日期、币种和估值日期"],
            "reads": ["产品版本、账户、持仓本金、交易、资金分录、收益、费用、标签和附件"],
            "writes": ["查询不写业务事实；菜单写操作通过独立领域命令"],
            "derived_results": ["累计金额、占比、剩余本金、实际现金流、累计回报和历史盈亏"],
            "side_effects": ["页签、产品范围和日期切换只改变查询参数"],
            "rollback": "投影失败不展示部分聚合结果；写命令失败不改变持仓或资金。",
        }
    return {
        "inputs": ["产品、账户、资金账户、本金、实际现金流、收益、费用、日期、标签和备注"],
        "reads": ["产品条款版本、账户状态、持仓本金、可用资金和当前版本"],
        "writes": ["本轮除零余额临时账户创建和删除外未提交；真实保存应写产品、账户、持仓、事件、分录和审计"],
        "derived_results": ["到期日、剩余本金、赎回损益、到期收益、占比和累计回报"],
        "side_effects": ["临时账户创建后进入空工作区，随后按精确名称确认删除"],
        "rollback": "产品、持仓、现金流、资金分录和审计必须原子提交，并使用幂等键防止重复处理。",
    }


def role_flow(form: dict) -> dict:
    """按资源类型选择数据流，不编造旧库表名。"""

    resource = form["resource"].upper()
    role = form.get("role", "configuration_editor")
    if "MONEY" in resource and "FIX" not in resource:
        return bank_wealth_flow(role)
    return fixed_deposit_flow(role)


def queue_commands(form: dict) -> list[dict]:
    """把静态命令目录转换为待验证命令。"""

    result = []
    for item in form.get("actionable_commands", []):
        raw_initial = dict(item.get("initial_state") or {})
        initial = {
            "enabled": raw_initial.get("enabled", raw_initial.get("Enabled", True)),
            "visible": raw_initial.get("visible", raw_initial.get("Visible", True)),
        }
        for key, value in raw_initial.items():
            if key.lower() not in {"enabled", "visible"}:
                initial[key] = value
        entry = {
            "component": item.get("component", "unknown"),
            "label": item.get("label") or item.get("component", "未命名命令"),
            "initial_state": initial,
            "trigger": "本轮未单独触发；已从静态事件目录登记。",
            "confirmation": "修改、注销、删除、到期或续存需要影响预览和确认。" if item.get("high_risk") else None,
            "outcome": "等待真实操作、业务对象前后对比、审计和失败回滚验证。",
            "status": "pending",
        }
        related = list(item.get("related_event_ids") or [])
        if related:
            entry["event_ids"] = related
        result.append(entry)
    return result


def static_states(form: dict) -> list[dict]:
    """为未直接到达的资源生成明确的静态状态。"""

    details = []
    if form.get("fields"):
        details.append("字段：" + "、".join(form["fields"]))
    if form.get("tabs"):
        details.append("页签：" + "、".join(form["tabs"]))
    if form.get("options"):
        details.append("选项：" + "、".join(form["options"]))
    text = "；".join(details) if details else "静态目录已确认窗体类、角色和最终宿主。"
    return [
        state("静态结构", text, STATIC_CATALOG, COMPOSITION),
        state("动态成功路径", "本轮未直接完成该资源的独立成功提交。", NOTES, status="pending"),
    ]


def build_record(form: dict) -> dict:
    """把 B05 队列项与动态、历史和静态证据合并。"""

    execution_id = form["execution_id"]
    dynamic = DYNAMIC.get(execution_id, {})
    states = dynamic.get("states", static_states(form))
    commands = dynamic.get("commands", queue_commands(form))
    record_evidence = [
        evidence("manual_note", NOTES, "B05 动态验证时间线、进程隔离、临时账户清理和账簿指纹。"),
        evidence("manual_note", CONTRACT, "Rust 存款、续存、银行理财产品和持仓运行合同。"),
        evidence("manual_note", STATIC_CATALOG, "旧窗体字段、命令、选项和页签静态目录。"),
        evidence("manual_note", COMPOSITION, "内嵌帧与最终宿主组合证据。"),
        evidence("manual_note", EVENT_FLOW, "旧事件到命令和数据流的静态映射。"),
    ]
    seen = {NOTES, CONTRACT, STATIC_CATALOG, COMPOSITION, EVENT_FLOW}
    for item in states:
        for path in item.get("evidence_paths", []):
            if path in seen:
                continue
            seen.add(path)
            kind = "screenshot" if path.lower().endswith(".png") else "log"
            record_evidence.append(evidence(kind, path, f"{item['name']} 的追溯证据。"))
    previous = PREVIOUS_RECORDS.get(execution_id)
    if previous and previous not in seen:
        record_evidence.append(evidence("log", previous, "该资源此前的动态观察记录。"))

    reachable = dynamic.get("reachable", True)
    unreachable_reason = dynamic.get("unreachable_reason")
    default_summary = f"{form.get('title') or form['resource']} 已完成静态结构登记；独立成功提交仍待验证。"
    default_gaps = [
        "独立入口、有效输入、校验失败、成功提交和取消路径",
        "账户、产品或持仓前后状态、关联分录、审计记录和失败回滚",
    ]
    return {
        "schema_version": 1,
        "execution_id": execution_id,
        "resource": form["resource"],
        "observed_at": OBSERVED_AT,
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": LEDGER_PATH,
            "sha256_before": BASELINE_HASH,
            "sha256_after": FINAL_HASH,
            "backup_artifact": BACKUP_ARTIFACT,
        },
        "navigation": {
            "entry_point": dynamic.get("entry") or form.get("entry_strategy") or "通过所属业务宿主间接触发",
            "steps": [
                "打开所属业务入口或最终宿主",
                "观察字段、页签、列表、命令和空状态",
                "仅为理财空工作区创建并删除精确命名的零余额临时账户",
                "退出专用进程并核对账簿、筛选、哈希和文件占用",
            ],
            "reachable": reachable,
            "unreachable_reason": unreachable_reason,
        },
        "states": states,
        "commands": commands,
        "data_flow": dynamic.get("data_flow", role_flow(form)),
        "evidence": record_evidence,
        "requirements_update": COMMON_REQUIREMENTS + dynamic.get("requirements", []),
        "result": {
            "status": "partial",
            "summary": dynamic.get("summary", default_summary),
            "remaining_gaps": dynamic.get("gaps", default_gaps),
        },
    }


def main() -> None:
    """写出 19 条 B05 最新运行记录。"""

    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    forms = [form for form in queue["forms"] if form["batch_id"] == "B05-financial_products"]
    if len(forms) != 19:
        raise RuntimeError(f"B05 队列数量异常：{len(forms)}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for form in forms:
        output_path = OUTPUT_DIR / f"{form['execution_id']}-{OUTPUT_STAMP}.json"
        output_path.write_text(
            json.dumps(build_record(form), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"generated {len(forms)} B05 records")


if __name__ == "__main__":
    main()
