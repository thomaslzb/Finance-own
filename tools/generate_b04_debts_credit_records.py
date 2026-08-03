"""生成 B04 债权债务与信用卡功能的运行态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
QUEUE_PATH = ROOT / "docs" / "runtime-execution-queue.json"
OBSERVED_AT = "2026-07-30T06:48:05+08:00"
OUTPUT_STAMP = "20260730T064805+0800"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "1E751F2151F8326BD4E98AA8D2AFD870EB485ECBBED9AE1253B3388300D26B49"
FINAL_HASH = "9EDF9111BA5DB1FC19E9A3BC9B5435322E8B4A202C958F9CAB11E32055C2BD17"
BACKUP_ARTIFACT = (
    "artifacts/runtime-validation/backups/"
    "test-before-b04-debts-credit-20260730.mh8"
)
NOTES = "artifacts/runtime-validation/B04-debts-credit-notes.md"
CONTRACT = "docs/runtime-debts-credit-and-amortization-contract.md"
STATIC_CATALOG = "docs/runtime-dfm-control-catalog.md"
COMPOSITION = "docs/runtime-form-composition-evidence.md"
EVENT_FLOW = "docs/runtime-event-command-dataflow.md"


def shot(name: str) -> str:
    """返回本轮截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/screenshots/{name}"


def legacy_shot(name: str) -> str:
    """返回早期动态截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/{name}"


def evidence(kind: str, path: str, description: str) -> dict:
    """构造统一证据记录。"""

    return {"kind": kind, "path": path, "description": description}


def state(name: str, observations: str, *paths: str, status: str = "observed") -> dict:
    """构造页面状态并保留静态与动态证据边界。"""

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
    """构造命令观察；未核对业务写入时不得标记为通过。"""

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
    "债权、债务、应收、应付、预收、预付、垫付和待摊必须使用显式方向与合同类型，不得只依赖金额正负号。",
    "本金、利息、手续费、罚息、奖励和坏账损失必须分别保存，并通过同一领域命令原子生成关联分录。",
    "还款、收回、返还、提前结清和坏账必须引用原合同、计划或账单，不得直接覆盖初始金额或删除历史。",
    "还款方式、利率、账单日、期数和摊还计划的修改必须版本化，保护已入账期次并记录影响预览。",
    "信用卡账单、交易、分期、还款和账户概况必须读取同一账户身份、账期规则和数据版本。",
    "网贷平台、投资对象、收款计划和实际交易使用稳定关联 ID；显示名称和 URL 不得充当业务主键。",
    "合同列表、交易明细、还款表、概况和图表必须共享查询口径、估值快照、稳定排序和分页规则。",
    "Rust 版在未通过旧软件真实样本验证前，不得把摊还公式、旧格式或外部协议标记为已兼容。",
]


PREVIOUS_RECORDS = {
    "RT-04-002": "artifacts/runtime-validation/RT-04-002-20260729T120933+0800.json",
    "RT-04-003": "artifacts/runtime-validation/RT-04-003-20260729T120933+0800.json",
    "RT-04-017": "artifacts/runtime-validation/RT-04-017-20260729T120933+0800.json",
    "RT-04-031": "artifacts/runtime-validation/RT-04-031-20260729T120933+0800.json",
    "RT-04-032": "artifacts/runtime-validation/RT-04-032-20260729T120933+0800.json",
    "RT-04-034": "artifacts/runtime-validation/RT-04-034-20260729T114300+0800.json",
    "RT-04-039": "artifacts/runtime-validation/RT-04-039-20260729T120933+0800.json",
    "RT-04-041": "artifacts/runtime-validation/RT-04-041-20260729T120933+0800.json",
    "RT-04-043": "artifacts/runtime-validation/RT-04-043-20260729T105225+0800.json",
    "RT-04-044": "artifacts/runtime-validation/RT-04-044-20260729T120933+0800.json",
}


DYNAMIC = {
    "RT-04-001": {
        "entry": "账户中心 -> 新增账户 -> 预收/预付",
        "states": [
            state(
                "账户类型入口",
                "新增账户页动态显示预收/预付菜单；应收款账户筛选和债权债务工作台确认这些账户进入统一合同域。",
                shot("b04-new-account-type-dialog.png"),
                shot("b04-account-center-receivables-sanitized.png"),
            )
        ],
        "summary": "预收和预付账户入口及所属业务域已确认，独立账户编辑成功路径未提交。",
        "gaps": ["预收与预付账户字段差异", "创建、修改、删除和余额初始化"],
    },
    "RT-04-002": {
        "entry": "债权记账子菜单 -> 预付",
        "states": [state("历史预付编辑器", "既有记录已确认预付交易字段和取消路径。", PREVIOUS_RECORDS["RT-04-002"], legacy_shot("claim-prepayment-dialog.png"))],
        "summary": "预付交易编辑器已有历史动态证据，本轮未再次保存。",
        "gaps": ["有效预付与超额核销", "资金分录、合同余额和失败回滚"],
    },
    "RT-04-003": {
        "entry": "债权记账子菜单 -> 垫付",
        "states": [state("历史垫付编辑器", "既有记录已确认垫付交易字段和取消路径。", PREVIOUS_RECORDS["RT-04-003"], legacy_shot("claim-advance-payment-dialog.png"))],
        "summary": "垫付入口和编辑结构已有历史动态证据。",
        "gaps": ["垫付明细选择和报销关系", "部分收回、重复收回和回滚"],
    },
    "RT-04-005": {
        "entry": "资产侧栏 -> 债权债务 -> 债权债务概况",
        "states": [
            state("概况容器", "债权债务概况会按当前合同类型切换应付款、应收款概况或预收款；静态目录还登记待摊费用和预付款。", shot("b04-claims-overview-sanitized.png"), COMPOSITION, NOTES)
        ],
        "summary": "TClaimsDebtContainer 的宿主和类型切换职责已确认。",
        "gaps": ["预付款和待摊费用动态页", "空状态、已完成合同和刷新规则"],
    },
    "RT-04-006": {
        "entry": "债权债务工作台 -> 债权债务构成",
        "states": [state("构成图宿主", "构成页动态加载两个图表窗口，并提供按人员显示菜单；单位切换由静态命令目录确认。", shot("b04-claims-workspace-sanitized.png"), NOTES, STATIC_CATALOG)],
        "summary": "债权债务图表宿主已到达，单位和下钻未执行。",
        "gaps": ["单位菜单和图表下钻", "负数、零值、跨币种和已完成合同口径"],
    },
    "RT-04-007": {
        "entry": "债权债务工作台 -> 债权债务构成",
        "states": [state("构成维度", "构成页可按人员显示，静态目录登记显示类型命令。", shot("b04-claims-workspace-sanitized.png"), STATIC_CATALOG)],
        "summary": "构成图维度切换入口已确认，所有选项未逐项执行。",
        "gaps": ["按人员、类型和币种的完整选项", "图表与合同列表合计一致性"],
    },
    "RT-04-008": {
        "entry": "资产侧栏 -> 债权债务",
        "states": [
            state("合同统计列表", "工作台显示债权人/债务人、款项、类型、收还款方式、利率、剩余期数和待收/还本金。", shot("b04-claims-workspace-sanitized.png")),
            state("范围筛选", "筛选菜单支持显示债权和债务、仅债权、仅债务及忽略已完成款项。", shot("b04-claims-filter-menu.png")),
        ],
        "summary": "合同统计框架和范围筛选已动态确认。",
        "gaps": ["删除命令的引用保护", "排序、分页、跨币种合计和刷新冲突"],
    },
    "RT-04-009": {
        "entry": "债权债务工作台 -> 交易明细",
        "states": [state("合同交易流水", "交易页展示日期、本金减少、本金增加、利息、合计、活动类型、标签、剩余本金、备注和附件，并提供查看未报销记录。", shot("b04-claims-workspace-sanitized.png"), NOTES)],
        "summary": "债权债务交易流水投影和未报销入口已动态确认。",
        "gaps": ["逐列金额方向与余额公式", "查找、操作、导出和大数据分页"],
    },
    "RT-04-010": {
        "entry": "资产侧栏 -> 债权债务",
        "states": [state("债权债务工作台", "页面动态显示交易明细、债权债务构成、已还金额和还款表、债权债务概况四个主视图。", shot("b04-claims-workspace-sanitized.png"), NOTES)],
        "summary": "TClaimsTransFm 最终宿主及四个主视图已动态到达。",
        "gaps": ["完整启用状态的还款表", "所有合同类型与顶部筛选组合"],
    },
    "RT-04-012": {
        "entry": "账户中心 -> 信用卡 -> 临时账户 -> 修改账户",
        "states": [state("信用卡账户编辑", "页面包含账单日管理、更多信息、附件、年费模式、最低还款比例、已出账/未出账金额、透支限额和提醒。", shot("b04-credit-account-editor.png"))],
        "summary": "单币信用卡账户编辑器已动态到达，未修改或保存字段。",
        "gaps": ["账单日变更生效规则", "敏感卡号存储、年费和最低还款计算"],
    },
    "RT-04-013": {
        "entry": "概况 -> 信用卡一览 -> 临时信用卡",
        "states": [state("账单统计", "工作台显示账单记录时间段、账单日、还款日、流入、流出和账单金额，并可切换最近三期或所有账单。", shot("b04-credit-card-workspace.png"))],
        "summary": "信用卡账单统计框架已动态确认。",
        "gaps": ["真实已出账账单和导入", "跨账期归属、最低还款和逾期口径"],
    },
    "RT-04-014": {
        "entry": "概况 -> 信用卡一览 -> 双击临时信用卡",
        "states": [
            state("信用卡交易工作台", "页面包含交易明细和分期付款管理两个页签。", shot("b04-credit-card-workspace.png")),
            state("分期付款管理", "分期页提供新增、显示所有分期付款和操作入口，并展示期数、本金、手续费、利息及未还金额列。", shot("b04-credit-card-installment-tab.png")),
        ],
        "summary": "TCreditCardTransFm 及两个主视图已动态到达。",
        "gaps": ["真实账单交易和分页", "分期编辑、删除、提前结清和账单联动"],
    },
    "RT-04-015": {
        "entry": "信用卡交易工作台 -> 交易明细",
        "states": [
            state("信用卡交易列表", "交易页提供记账、单个账单交易明细、查找和操作入口。", shot("b04-credit-card-workspace.png")),
            state("记账菜单", "菜单包含日常收支、分拆、物品买入、信用卡取现、信用卡还款、转账、货币兑换和批量命令。", shot("b04-credit-card-bookkeeping-menu.png")),
        ],
        "summary": "信用卡交易列表外壳和记账命令集合已动态确认。",
        "gaps": ["已出账与未出账列表口径", "导入、修改、删除和账单重算"],
    },
    "RT-04-016": {
        "entry": "账户中心 -> 新增账户 -> 信用卡 -> 双币信用卡",
        "states": [
            state("双币卡基础信息", "向导第一步包含账户名称和所属账户组。", shot("b04-double-currency-credit-wizard-step1.png")),
            state("共享账单规则", "第二步包含开户日期、固定或月末账单日、账单日后若干天或固定还款日。", shot("b04-double-currency-credit-wizard-step2.png")),
            state("双币额度", "第三步分别选择人民币和美元并维护各自透支额度和提醒。", shot("b04-double-currency-credit-wizard-step3.png")),
        ],
        "summary": "双币信用卡账户结构和三步向导已动态确认，未完成创建。",
        "gaps": ["两币种账单与还款关系", "自动购汇、汇率、额度和费用规则"],
    },
    "RT-04-017": {
        "entry": "债权或债务记账子菜单 -> 坏账",
        "states": [state("历史坏账编辑器", "既有记录已覆盖债权和债务坏账对话框。", PREVIOUS_RECORDS["RT-04-017"], legacy_shot("claim-bad-debt-dialog.png"), legacy_shot("debt-bad-debt-dialog.png"))],
        "summary": "坏账入口和基本字段已有历史动态证据。",
        "gaps": ["部分坏账和坏账后收回", "损失分录、合同状态和撤销"],
    },
    "RT-04-019": {
        "entry": "账户中心 -> 新增账户 -> 网贷",
        "states": [
            state("网贷账户基础信息", "向导第一步包含账户名称、币种、账户组和所有者。", shot("b04-net-loan-wizard-step1.png")),
            state("平台信息", "第二步包含日期、账户余额、平台名称和平台网址。", shot("b04-net-loan-wizard-step2.png")),
        ],
        "summary": "网贷账户入口和平台元数据已动态确认，未创建账户。",
        "gaps": ["平台机构复用和唯一性", "账户修改、删除、余额和交易宿主"],
    },
    "RT-04-031": {
        "entry": "债权记账子菜单 -> 收回",
        "states": [state("历史收回编辑器", "既有记录已确认收回本金、利息和资金账户结构。", PREVIOUS_RECORDS["RT-04-031"], legacy_shot("claim-recovery-dialog.png"))],
        "summary": "债权收回编辑器已有历史动态证据。",
        "gaps": ["部分与超额收回", "本金利息分配、计划更新和回滚"],
    },
    "RT-04-032": {
        "entry": "债务记账子菜单 -> 返还",
        "states": [state("历史返还编辑器", "既有记录已确认债务返还字段和取消路径。", PREVIOUS_RECORDS["RT-04-032"], legacy_shot("debt-return-dialog.png"))],
        "summary": "债务返还编辑器已有历史动态证据。",
        "gaps": ["部分返还、利息和手续费", "计划更新、余额不足和回滚"],
    },
    "RT-04-033": {
        "entry": "账户中心 -> 应收款 -> 双击既有账户",
        "states": [state("应收款账户概况", "账户编辑器动态显示人员类型、款项名称、备注和附件入口；账户中心按应收款类型筛选。", shot("b04-account-center-receivables-sanitized.png"), NOTES)],
        "summary": "应收款账户筛选和账户概况已动态确认。",
        "gaps": ["应付、应收字段差异和修改保存", "删除引用、账户关闭和合同迁移"],
    },
    "RT-04-034": {
        "entry": "信用卡交易工作台 -> 记账 -> 信用卡还款",
        "states": [state("信用卡还款", "页面包含信用卡、资金来源、还款本金、利息、只读还款总额、标签、日期和备注。", shot("b04-credit-card-repayment-dialog.png"), PREVIOUS_RECORDS["RT-04-034"])],
        "commands": [
            command("信用卡记账菜单", "信用卡还款", "选择菜单项", "打开 TDrawalCardDlgFm。", status="pass"),
            command("还款对话框", "保存并继续、确定", "本轮未提交", "本金、利息、总额和账户写入仍待验证。", status="pending"),
        ],
        "summary": "信用卡还款入口、字段和取消路径已动态确认。",
        "gaps": ["还款总额、超额还款和最低还款", "资金分录、额度刷新、跨币种和失败回滚"],
    },
    "RT-04-035": {
        "entry": "账户中心 -> 新增账户 -> 信用卡 -> 单币信用卡",
        "states": [
            state("信用卡基础信息", "向导第一步包含名称、币种、所有者和账户组。", shot("b04-credit-card-wizard-step1.png")),
            state("账单和额度规则", "第二步包含开户日期、账单日、还款日、透支限额和提醒。", shot("b04-credit-card-wizard-step2.png")),
            state("创建后工作区", "零余额临时卡出现在信用卡一览和账户中心，并可进入交易工作台。", shot("b04-credit-card-created-filtered.png"), shot("b04-credit-card-workspace.png")),
            state("清理", "删除确认框明确指向临时卡，删除后信用卡筛选页不再显示该账户。", shot("b04-credit-card-delete-confirmation.png"), shot("b04-credit-card-after-delete.png")),
        ],
        "commands": [
            command("信用卡向导", "完成", "创建零余额临时卡", "账户创建成功并可进入工作台。", status="pass"),
            command("账户操作菜单", "删除账户", "按精确账户名确认删除", "临时卡从信用卡筛选和侧栏移除。", status="pass", confirmation="确认框必须显示 Codex-B04-Credit-20260730。"),
        ],
        "summary": "单币信用卡创建、工作台到达和精确删除清理已动态完成。",
        "gaps": ["非零余额、已有交易和账单引用下的删除保护", "卡号、年费、最低还款和账单生成"],
    },
    "RT-04-036": {
        "entry": "账户中心 -> 新增账户 -> 网贷",
        "states": [
            state("网贷向导第一步", "包含名称、币种、所有者和账户组。", shot("b04-net-loan-wizard-step1.png")),
            state("网贷向导第二步", "包含日期、账户余额、平台名称和平台网址。", shot("b04-net-loan-wizard-step2.png")),
        ],
        "summary": "网贷账户向导已动态走到完成前，未保存。",
        "gaps": ["创建后账户工作台", "机构复用、平台 URL 校验和取消回滚"],
    },
    "RT-04-037": {
        "entry": "账户中心 -> 新增账户 -> 信用卡 -> 双币信用卡",
        "states": [
            state("双币信用卡三步向导", "已观察基础信息、共享账单规则和两币种额度，未点击完成。", shot("b04-double-currency-credit-wizard-step1.png"), shot("b04-double-currency-credit-wizard-step2.png"), shot("b04-double-currency-credit-wizard-step3.png"))
        ],
        "summary": "双币信用卡向导完整页面流已动态确认，未创建账户。",
        "gaps": ["完成创建和双币工作台", "账单、还款、汇率和自动购汇"],
    },
    "RT-04-039": {
        "entry": "债务记账子菜单 -> 借入或借出",
        "states": [state("历史借入借出编辑器", "既有记录覆盖期限、频率、还款方式和保存命令。", PREVIOUS_RECORDS["RT-04-039"], legacy_shot("claim-lend-dialog.png"), legacy_shot("debt-borrow-dialog.png"))],
        "summary": "新建借入借出页面已有历史动态证据。",
        "gaps": ["有效合同和还款表生成", "利率公式、频率、首尾期和回滚"],
    },
    "RT-04-041": {
        "entry": "债务记账子菜单 -> 预收",
        "states": [state("历史预收编辑器", "既有记录已确认预收交易字段。", PREVIOUS_RECORDS["RT-04-041"], legacy_shot("debt-advance-receipt-dialog.png"))],
        "summary": "预收交易编辑器已有历史动态证据。",
        "gaps": ["收入核销和退款", "合同余额、资金分录和失败回滚"],
    },
    "RT-04-042": {
        "entry": "债权债务记账 -> 待摊费用",
        "states": [state("待摊费用编辑器", "历史截图显示待摊费用新增页面；本轮未重新进入或提交。", legacy_shot("prepaid-expenses-dialog.png"), STATIC_CATALOG)],
        "summary": "待摊费用页面结构已有动态截图，计划生成未验证。",
        "gaps": ["摊销期次和费用交易生成", "修改、删除、尾差和已入账保护"],
    },
    "RT-04-043": {
        "entry": "待摊费用 -> 生成收支",
        "states": [state("历史待摊收支编辑器", "既有记录已确认待摊费用生成收支的入口和字段。", PREVIOUS_RECORDS["RT-04-043"], legacy_shot("prepaid-expenses-dialog.png"))],
        "summary": "待摊费用收支编辑器已有历史部分证据。",
        "gaps": ["期次到普通费用交易的映射", "重复生成、修改和回滚"],
    },
    "RT-04-044": {
        "entry": "债权或债务记账子菜单 -> 提前收回或提前返还",
        "states": [state("历史提前结清页面", "既有记录已覆盖提前收回和提前返还页面。", PREVIOUS_RECORDS["RT-04-044"], legacy_shot("claim-early-recovery-dialog.png"), legacy_shot("debt-early-return-dialog.png"))],
        "summary": "提前返还页面已有历史动态证据。",
        "gaps": ["提前结清金额与违约费用", "剩余期次重算、审计和回滚"],
    },
    "RT-04-045": {
        "entry": "债权债务工作台 -> 已还金额和还款表",
        "states": [state("还款表禁用状态", "主视图已动态到达，当前选择下显示 tsDisabled；添加、修改、删除、利率变更和打印由静态目录确认。", shot("b04-claims-workspace-sanitized.png"), NOTES, STATIC_CATALOG)],
        "summary": "还款表宿主和禁用状态已确认，完整可编辑计划未到达。",
        "gaps": ["tsEnabled 页面和期次列表", "计划增删改、利率变更、打印和引用保护"],
    },
    "RT-04-046": {
        "entry": "债权债务工作台 -> 债权债务概况 -> 预付款概况",
        "states": [state("预付款视图宿主", "TClaimsTransFm 和概况容器已动态到达；预付款内嵌帧由静态组合证据确认。", shot("b04-claims-overview-sanitized.png"), COMPOSITION)],
        "summary": "预付款视图的最终宿主已确认，独立内容未动态显示。",
        "gaps": ["预付款字段和余额口径", "核销、退款和已完成状态"],
    },
    "RT-04-047": {
        "entry": "信用卡工作台 -> 操作 -> 查看账户资料",
        "states": [state("信用卡账户概况", "概况动态显示账户类型、币种、账单日、还款日、额度、最低还款、年费、账户组、标签和附件。", shot("b04-credit-card-account-overview.png"), COMPOSITION)],
        "summary": "TCardViewFrame 的账户概况宿主已动态确认。",
        "gaps": ["有卡号和敏感字段时的掩码", "多币种、附件和修改后刷新"],
    },
    "RT-04-051": {
        "entry": "债权债务工作台 -> 债权债务概况 -> 待摊费用",
        "states": [state("待摊视图宿主", "债权债务概况容器已动态到达；待摊费用内嵌帧由静态组合证据确认。", shot("b04-claims-overview-sanitized.png"), COMPOSITION)],
        "summary": "待摊费用视图的最终宿主已确认，内容未动态显示。",
        "gaps": ["摊销计划、已摊和剩余金额", "空状态、完成状态和费用下钻"],
    },
    "RT-04-052": {
        "entry": "债权债务工作台 -> 债权债务概况 -> 应付款",
        "states": [state("应付款概况", "选择应付款合同后，概况内嵌页动态切换为应付款，并展示合同、账户组、标签和附件区域。", shot("b04-claims-overview-sanitized.png"), NOTES, COMPOSITION)],
        "summary": "应付款视图已通过最终宿主动态确认。",
        "gaps": ["字段逐项映射和隐藏账户", "修改、附件、已完成和跨币种"],
    },
    "RT-04-053": {
        "entry": "债权债务工作台 -> 债权债务概况 -> 应收款概况",
        "states": [state("应收款概况", "选择应收合同后内嵌页动态切换为应收款概况；账户中心也可按应收款筛选。", shot("b04-account-center-receivables-sanitized.png"), NOTES, COMPOSITION)],
        "summary": "应收款视图已通过工作台和账户中心动态确认。",
        "gaps": ["字段逐项映射和金额口径", "已完成、坏账、附件和修改刷新"],
    },
    "RT-04-054": {
        "entry": "债权债务工作台 -> 债权债务概况 -> 预收款",
        "states": [state("预收款概况", "选择预收合同后内嵌页动态切换为预收款。", shot("b04-claims-overview-sanitized.png"), NOTES, COMPOSITION)],
        "summary": "预收款视图已通过最终宿主动态确认。",
        "gaps": ["收入核销和退款投影", "完成状态、附件和跨币种"],
    },
}


def debt_flow(role: str) -> dict:
    """生成债权债务、预收预付和待摊的保守数据流。"""

    if role == "transaction_history":
        return {
            "inputs": ["合同范围、方向、类型、状态、日期和是否包含已完成款项"],
            "reads": ["合同版本、交易、还款计划、实际还款、对手方、标签和附件"],
            "writes": ["查询不写业务事实；修改和删除必须转为领域命令"],
            "derived_results": ["本金增减、利息、合计、剩余本金和列表汇总"],
            "side_effects": ["切换筛选只改变查询参数"],
            "rollback": "查询失败保留上次稳定快照；写命令失败后重新读取目标版本。",
        }
    if role == "projection_view":
        return {
            "inputs": ["当前合同、合同类型、状态范围和估值日期"],
            "reads": ["合同、计划、交易、账户组、标签、附件和估值快照"],
            "writes": ["概况、图表和还款表只读，不写业务事实"],
            "derived_results": ["应收应付概况、构成、计划、已还和剩余金额"],
            "side_effects": ["页签和维度切换只改变投影"],
            "rollback": "投影失败显示明确错误，不展示部分聚合结果。",
        }
    return {
        "inputs": ["合同类型、方向、对手方、币种、本金、日期、利率、频率、期数、标签和备注"],
        "reads": ["账户、对手方、原合同、还款计划和当前版本"],
        "writes": ["本轮未提交；真实保存应写合同版本、计划、交易、平衡分录和审计事件"],
        "derived_results": ["剩余本金、下一期日期、计划本金、利息、手续费和状态"],
        "side_effects": ["本轮只观察或取消，未确认债权债务业务保存"],
        "rollback": "合同、计划、交易和分录必须原子提交，任一失败时整体回滚。",
    }


def credit_flow(role: str) -> dict:
    """生成信用卡、账单、还款和分期的保守数据流。"""

    if role in {"transaction_history", "projection_view"}:
        return {
            "inputs": ["信用卡账户、币种、账期、日期范围、账单状态和分期状态"],
            "reads": ["卡账户、账单、交易、分期协议、期次、还款和估值快照"],
            "writes": ["查询不写业务事实；菜单写操作通过独立命令服务"],
            "derived_results": ["已出账、未出账、流入、流出、账单金额、未还金额和分期汇总"],
            "side_effects": ["页签和账单范围切换只改变查询参数"],
            "rollback": "查询失败保留上次稳定账期；写命令失败不生成部分账单或单边分录。",
        }
    return {
        "inputs": ["卡账户、币种、账单规则、额度、还款本金、利息、手续费、分期参数和日期"],
        "reads": ["账户状态、账单、未出账交易、资金来源、分期协议和当前版本"],
        "writes": ["本轮除零余额临时账户创建和删除外未提交；真实保存应写账户、账单、协议、交易和审计"],
        "derived_results": ["账单日、还款日、可用额度、最低还款、还款总额和每期金额"],
        "side_effects": ["临时信用卡创建后进入工作台，随后按名称确认删除"],
        "rollback": "账户、账单、还款、分期和资金分录必须原子提交并支持幂等重试。",
    }


def net_loan_flow(role: str) -> dict:
    """生成网贷账户、投资对象和收款计划的保守数据流。"""

    if role in {"transaction_history", "projection_view"}:
        return {
            "inputs": ["网贷账户、投资对象、持有状态、日期和计划状态"],
            "reads": ["平台账户、投资对象、收款计划、实际交易、奖励、转让和坏账"],
            "writes": ["查询不写业务事实"],
            "derived_results": ["本金、利息、收益、剩余期数、待收金额和资产价值"],
            "side_effects": ["切换持有或已完成只改变查询范围"],
            "rollback": "投影失败不缓存部分结果；任务写入失败按幂等键重试。",
        }
    return {
        "inputs": ["平台、投资对象、本金、利率、期数、收款方式、频率、日期和备注"],
        "reads": ["平台账户、资金账户、现有对象、计划规则和当前版本"],
        "writes": ["本轮未提交；真实保存应写投资对象、计划、交易、分录和审计"],
        "derived_results": ["收款表、下一收款日、剩余本金、收益、奖励和损失"],
        "side_effects": ["本轮只走到网贷账户向导完成前"],
        "rollback": "投资对象、计划和资金分录必须原子提交；自动任务使用幂等键避免重复收款。",
    }


def role_flow(form: dict) -> dict:
    """按资源所属领域选择数据流，不编造旧库表名。"""

    resource = form["resource"].upper()
    role = form.get("role", "configuration_editor")
    if "DEBTINVESTMENT" in resource:
        return net_loan_flow(role)
    if any(token in resource for token in ("CREDIT", "CARD", "DRAWALCARD")):
        return credit_flow(role)
    return debt_flow(role)


def static_states(form: dict) -> list[dict]:
    """为未直接到达的资源生成明确标注的静态状态。"""

    details = []
    if form.get("fields"):
        details.append("字段：" + "、".join(form["fields"]))
    if form.get("tabs"):
        details.append("页签：" + "、".join(form["tabs"]))
    if form.get("options"):
        details.append("选项：" + "、".join(form["options"]))
    text = "；".join(details) if details else "静态目录已确认窗体类、角色和事件边界。"
    return [
        state("静态结构", text, STATIC_CATALOG, COMPOSITION),
        state("动态成功路径", "本轮未直接完成该资源的独立成功提交。", NOTES, status="pending"),
    ]


def queue_commands(form: dict) -> list[dict]:
    """把静态命令目录转换为待验证命令并保留高风险确认要求。"""

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
        related = list(item.get("related_event_ids") or [])
        entry = {
            "component": item.get("component", "unknown"),
            "label": item.get("label") or item.get("component", "未命名命令"),
            "initial_state": initial,
            "trigger": "本轮未单独触发；已从静态事件目录登记。",
            "confirmation": "修改、删除、坏账、提前结清或计划重算需要影响预览和确认。" if item.get("high_risk") else None,
            "outcome": "等待真实操作、业务对象前后对比、审计和失败回滚验证。",
            "status": "pending",
        }
        if related:
            entry["event_ids"] = related
        result.append(entry)
    return result


def build_record(form: dict) -> dict:
    """把 B04 队列项与动态、历史和静态证据合并。"""

    execution_id = form["execution_id"]
    dynamic = DYNAMIC.get(execution_id, {})
    states = dynamic.get("states", static_states(form))
    commands = dynamic.get("commands", queue_commands(form))
    record_evidence = [
        evidence("manual_note", NOTES, "B04 动态验证时间线、进程隔离、清理和账簿指纹。"),
        evidence("manual_note", CONTRACT, "Rust 债权债务、信用卡、分期和网贷运行合同。"),
        evidence("manual_note", STATIC_CATALOG, "旧窗体字段、命令、选项和页签静态目录。"),
        evidence("manual_note", COMPOSITION, "嵌入帧与最终宿主组合证据。"),
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

    default_summary = (
        f"{form.get('title') or form['resource']} 已完成静态结构登记；"
        "本轮未直接提交其独立成功路径。"
    )
    default_gaps = [
        "独立入口、有效输入、校验失败、成功提交和取消路径",
        "合同或账单前后状态、关联分录、审计记录和失败回滚",
    ]
    entry = dynamic.get("entry") or form.get("entry_strategy") or "通过所属业务宿主间接触发"
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
            "entry_point": entry,
            "steps": ["打开所属业务入口", "观察字段、页签、列表和命令", "仅在临时信用卡创建和清理时确认写入", "退出专用进程并核对账簿、筛选和恢复副本"],
            "reachable": True,
            "unreachable_reason": None,
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
    """写出 54 条 B04 最新运行记录。"""

    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    forms = [form for form in queue["forms"] if form["batch_id"] == "B04-debts_credit"]
    if len(forms) != 54:
        raise RuntimeError(f"B04 队列数量异常：{len(forms)}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for form in forms:
        output_path = OUTPUT_DIR / f"{form['execution_id']}-{OUTPUT_STAMP}.json"
        output_path.write_text(
            json.dumps(build_record(form), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"generated {len(forms)} B04 records")


if __name__ == "__main__":
    main()
