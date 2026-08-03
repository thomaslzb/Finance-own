"""生成 B03 交易与流水功能的运行态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
QUEUE_PATH = ROOT / "docs" / "runtime-execution-queue.json"
OBSERVED_AT = "2026-07-30T05:51:18+08:00"
OUTPUT_STAMP = "20260730T055118+0800"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "B7B385F17A45005FEEB1F805E213ED6A0C9FCF9674C60C17C92E581A3B25345C"
FINAL_HASH = "1E751F2151F8326BD4E98AA8D2AFD870EB485ECBBED9AE1253B3388300D26B49"
BACKUP_ARTIFACT = (
    "artifacts/runtime-validation/backups/"
    "test-before-b03-transactions-20260730.mh8"
)
NOTES = "artifacts/runtime-validation/B03-transactions-notes.md"
CONTRACT = "docs/runtime-transactions-and-ledger-contract.md"
STATIC_CATALOG = "docs/runtime-dfm-control-catalog.md"
COMPOSITION = "docs/runtime-form-composition-evidence.md"
EVENT_FLOW = "docs/runtime-event-command-dataflow.md"


def shot(name: str) -> str:
    """返回本轮截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(kind: str, path: str, description: str) -> dict:
    """构造统一证据记录。"""

    return {"kind": kind, "path": path, "description": description}


def state(name: str, observations: str, *paths: str, status: str = "observed") -> dict:
    """构造页面状态并标明静态与动态证据边界。"""

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
    "所有交易命令必须通过领域服务原子提交，页面不得直接拼接或写入数据库记录。",
    "金额使用定点最小货币单位；汇率、手续费和利息使用显式精度、方向、日期和舍入策略。",
    "转账、取款、充值、余额调整和分期生成必须保持关联分录平衡，失败时全部回滚。",
    "交易修改、删除、退款、类型转换和批量操作必须保留来源关系、审计记录和影响预览。",
    "列表、筛选、查找、账户流水和概况图表必须读取同一交易查询口径与估值快照。",
    "旧 Delphi 窗体和嵌入帧仅用于证据追溯，Rust 版按交易命令、查询投影和专属扩展拆分。",
]


PREVIOUS_RECORDS = {
    "RT-03-001": "artifacts/runtime-validation/RT-03-001-20260729T114300+0800.json",
    "RT-03-004": "artifacts/runtime-validation/RT-03-004-20260729T102603+0800.json",
    "RT-03-005": "artifacts/runtime-validation/RT-03-005-20260729T140321+0800.json",
    "RT-03-009": "artifacts/runtime-validation/RT-03-009-20260729T111430+0800.json",
    "RT-03-010": "artifacts/runtime-validation/RT-03-010-20260729T095135+0800.json",
    "RT-03-012": "artifacts/runtime-validation/RT-03-012-20260729T095135+0800.json",
    "RT-03-016": "artifacts/runtime-validation/RT-03-016-20260729T101026+0800.json",
    "RT-03-017": "artifacts/runtime-validation/RT-03-017-20260729T101026+0800.json",
    "RT-03-024": "artifacts/runtime-validation/RT-03-024-20260729T105225+0800.json",
    "RT-03-025": "artifacts/runtime-validation/RT-03-025-20260729T102603+0800.json",
    "RT-03-026": "artifacts/runtime-validation/RT-03-026-20260729T114300+0800.json",
    "RT-03-028": "artifacts/runtime-validation/RT-03-028-20260729T105225+0800.json",
    "RT-03-034": "artifacts/runtime-validation/RT-03-034-20260729T095135+0800.json",
}


DYNAMIC = {
    "RT-03-001": {
        "entry": "信用卡账户工作区 -> 记账 -> 信用卡取现",
        "states": [
            state(
                "历史取现编辑器",
                "既有记录已确认信用卡取现的金额、信用卡、现金账户、日期、手续费和备注结构。",
                PREVIOUS_RECORDS["RT-03-001"],
            )
        ],
        "summary": "信用卡取现结构已有历史动态证据，本轮未再次提交。",
        "gaps": ["信用额度与现金到账的平衡分录", "手续费入账、取消和失败回滚"],
    },
    "RT-03-002": {
        "entry": "资产侧栏 -> CASH -> Cash-CNY",
        "states": [
            state(
                "现金交易工作区",
                "现金账户显示账户余额、日期范围、记账/查找/操作入口、交易明细和流入流出汇总。",
                shot("b03-cash-account-workspace.png"),
            )
        ],
        "summary": "TCashTransFm 作为现金账户流水工作区已动态到达。",
        "gaps": ["空状态、分页和超大数据量", "现金专属操作菜单逐项执行"],
    },
    "RT-03-003": {
        "entry": "现金、活期或第三方账户工作区内嵌流水框架",
        "states": [
            state(
                "共享交易列表框架",
                "现金、活期和第三方账户工作区复用日期范围、记账、查找、操作、交易列表和底部汇总结构。",
                shot("b03-cash-account-workspace.png"),
                shot("b03-current-account-workspace.png"),
                shot("b03-third-party-account-workspace.png"),
                COMPOSITION,
            )
        ],
        "summary": "TCashTransFrame 被确认是多个账户流水页共享的查询框架。",
        "gaps": ["不同账户类型的列差异", "选择、多选和列表刷新协议"],
    },
    "RT-03-004": {
        "entry": "顶部记账菜单 -> 取款",
        "states": [
            state(
                "取款编辑器",
                "取款入口可达；既有记录补充账户、金额、现金去向、日期、标签和备注字段。",
                shot("b03-command-110.png"),
                PREVIOUS_RECORDS["RT-03-004"],
            )
        ],
        "summary": "取款页面与历史字段证据已合并，未执行保存。",
        "gaps": ["有效取款和余额不足校验", "来源与现金账户平衡、手续费及回滚"],
    },
    "RT-03-005": {
        "entry": "顶部记账菜单 -> 转账",
        "states": [
            state(
                "转账编辑器",
                "转账入口可达；历史记录已覆盖转出、转入、金额、手续费、日期、标签和备注等结构。",
                shot("b03-command-111.png"),
                PREVIOUS_RECORDS["RT-03-005"],
            )
        ],
        "summary": "单笔转账页面结构已确认，未提交跨账户分录。",
        "gaps": ["同币种与跨币种转账", "手续费承担方、汇率、原子性和失败回滚"],
    },
    "RT-03-006": {
        "entry": "概况 -> 收支构成",
        "states": [
            state(
                "本月收支构成",
                "概况页按本月显示收入和支出的双环形图、分类图例及金额。",
                shot("b03-overview-income-expense-composition.png"),
                COMPOSITION,
            )
        ],
        "summary": "本月收入支出构成图已通过最终宿主动态验证。",
        "gaps": ["空数据、负数和退款口径", "点击图例下钻与筛选联动"],
    },
    "RT-03-007": {
        "entry": "资产侧栏 -> 代表性活期账户",
        "states": [
            state(
                "活期账户流水",
                "活期账户工作区显示账户名称、余额、日期范围、记账/查找/操作入口和交易列表。",
                shot("b03-current-account-workspace.png"),
            )
        ],
        "summary": "TCurrentTransFm 的账户流水外壳已动态确认。",
        "gaps": ["利息、存取款和转账的专属列", "空状态、对账和异常余额"],
    },
    "RT-03-009": {
        "entry": "财务记录 -> 代表性支出 -> 报销流程",
        "states": [
            state(
                "历史报销编辑器",
                "既有记录确认报销会关联原支出、报销账户、金额、日期和说明。",
                PREVIOUS_RECORDS["RT-03-009"],
                shot("b03-expense-row-selected.png"),
            )
        ],
        "summary": "报销入口依赖原始支出选择，成功写入仍待复测。",
        "gaps": ["部分报销、超额报销和重复报销", "原交易关系、余额与分类报表口径"],
    },
    "RT-03-010": {
        "entry": "财务记录 -> 查找 -> 筛选",
        "states": [
            state(
                "筛选条件",
                "筛选页包含资产、活动类型、关键字、标签和金额区间，并提供清空条件和确定。",
                shot("b03-filter-dialog.png"),
                PREVIOUS_RECORDS["RT-03-010"],
            )
        ],
        "summary": "交易筛选条件和清空边界已动态确认，未提交新的持久化视图。",
        "gaps": ["组合条件查询结果", "条件持久化、非法金额区间和大数据性能"],
    },
    "RT-03-011": {
        "entry": "财务记录 -> 查找 -> 筛选 -> 结果列表",
        "states": [
            state(
                "筛选结果宿主",
                "财务记录页提供查找/筛选菜单；TFilterTransFrame 由静态组合证据确认负责筛选后的交易列表。",
                shot("b03-financial-records-find-menu.png"),
                shot("b03-filter-dialog.png"),
                COMPOSITION,
            )
        ],
        "summary": "筛选入口与结果宿主关系已确认，结果列表未用自定义条件执行。",
        "gaps": ["条件到查询 DTO 的逐字段映射", "结果总计、重置和返回原列表"],
    },
    "RT-03-012": {
        "entry": "财务记录 -> 查找 -> 查找",
        "states": [
            state(
                "逐项查找对话框",
                "查找页可选择字段、输入值，并执行重新开始和查找下一个。",
                shot("b03-find-dialog.png"),
                PREVIOUS_RECORDS["RT-03-012"],
            )
        ],
        "summary": "查找对话框的字段和值输入及游标式查找命令已验证。",
        "gaps": ["每个字段的数据类型和匹配规则", "无结果、循环查找和大小写/日期口径"],
    },
    "RT-03-013": {
        "entry": "交易列表宿主 -> 查找服务",
        "states": [
            state(
                "查找宿主关系",
                "财务记录的查找菜单和 TFindDlgFm 已动态到达；TFindForm 的独立生命周期仅由静态事件目录确认。",
                shot("b03-financial-records-find-menu.png"),
                shot("b03-find-dialog.png"),
                STATIC_CATALOG,
            )
        ],
        "summary": "查找能力已确认，但 TFindForm 与 TFindDlgFm 的版本关系仍需定位。",
        "gaps": ["TFindForm 的实际调用方", "查找游标跨排序和刷新后的行为"],
    },
    "RT-03-016": {
        "entry": "顶部记账菜单 -> 日常收支",
        "states": [
            state(
                "日常收支草稿",
                "编辑器包含收支项目、金额、收支账户、标签、日期、备注、附件以及保存并继续和确定。",
                shot("b03-command-104.png"),
                shot("b03-command-123.png"),
                PREVIOUS_RECORDS["RT-03-016"],
            ),
            state(
                "既有支出编辑",
                "双击财务记录中的普通支出可打开同类编辑器；本轮未修改字段或保存。",
                shot("b03-existing-expense-editor.png"),
            ),
        ],
        "summary": "日常收入/支出新增和既有交易编辑入口已动态确认。",
        "gaps": ["收入与支出方向切换规则", "保存并继续、附件、校验失败和真实提交"],
    },
    "RT-03-017": {
        "entry": "TIncExpDlgFm 内嵌编辑框架",
        "states": [
            state(
                "收支编辑框架",
                "收支项目、金额、账户、标签、日期、备注和附件由共享编辑框架承载。",
                shot("b03-command-123-installment-host.png"),
                shot("b03-existing-expense-editor.png"),
                PREVIOUS_RECORDS["RT-03-017"],
                COMPOSITION,
            )
        ],
        "summary": "TIncExpEditFrame 的宿主和通用字段已确认。",
        "gaps": ["账户类型驱动的分期入口", "字段联动、默认值和嵌入式选择器回传"],
    },
    "RT-03-018": {
        "entry": "日常支出 -> 信用卡账户条件满足时 -> 分期",
        "states": [
            state(
                "分期入口条件",
                "普通活期账户的日常收支页未显示分期按钮，说明入口受账户类型或交易方向约束；向导页和确认页由静态目录确认。",
                shot("b03-command-123-installment-host.png"),
                STATIC_CATALOG,
                COMPOSITION,
            )
        ],
        "summary": "分期支出向导的信用卡门控已形成假设，三步成功路径未动态完成。",
        "gaps": ["信用卡账户下的真实入口", "分期计划生成、首期入账和整体回滚"],
    },
    "RT-03-023": {
        "entry": "概况 -> 收支对比",
        "states": [
            state(
                "按月收支柱状图",
                "概况页按月显示收入和支出柱状对比，并提供时间粒度菜单。",
                shot("b03-overview-host-charts.png"),
                COMPOSITION,
            )
        ],
        "summary": "月度收支柱状图已通过最终宿主动态验证。",
        "gaps": ["按年或其它粒度", "退款、转账排除和图表下钻口径"],
    },
    "RT-03-024": {
        "entry": "交易列表 -> 操作 -> 余额调整",
        "states": [
            state(
                "余额调整历史证据",
                "既有记录已确认余额调整编辑器；本轮财务记录操作菜单再次显示相关交易维护入口。",
                PREVIOUS_RECORDS["RT-03-024"],
                shot("b03-financial-records-operation-menu.png"),
            )
        ],
        "summary": "余额调整属于显式交易命令，不能直接覆盖账户当前余额。",
        "gaps": ["调整差额的系统分类和对手分录", "反向调整、删除和报表口径"],
    },
    "RT-03-025": {
        "entry": "顶部记账菜单 -> 工资收入",
        "states": [
            state(
                "工资收入编辑器",
                "工资收入入口可从顶层和更多活动进入；历史记录补充工资项目拆分结构。",
                shot("b03-command-107.png"),
                shot("b03-command-126.png"),
                PREVIOUS_RECORDS["RT-03-025"],
            )
        ],
        "summary": "工资收入专用编辑器入口与历史结构已确认。",
        "gaps": ["税前税后、扣款和多账户拆分", "模板复用、成功入账和撤销"],
    },
    "RT-03-026": {
        "entry": "第三方储值或预付账户 -> 充值",
        "states": [
            state(
                "充值历史证据",
                "既有记录已确认充值编辑器的来源账户、目标账户、金额、日期和备注边界。",
                PREVIOUS_RECORDS["RT-03-026"],
                shot("b03-third-party-account-workspace.png"),
            )
        ],
        "summary": "充值应作为来源与储值账户之间的原子交易，成功路径待复测。",
        "gaps": ["现金充值与银行卡充值差异", "手续费、失败回滚和重复提交"],
    },
    "RT-03-028": {
        "entry": "顶部记账菜单 -> 更多活动 -> 收支 -> 分拆收支",
        "states": [
            state(
                "分拆收支编辑器",
                "分拆收支入口可达；历史记录已确认总额与多条分类明细的编辑结构。",
                shot("b03-command-124.png"),
                PREVIOUS_RECORDS["RT-03-028"],
            )
        ],
        "summary": "分拆收支应作为一个业务交易和多条分类分配原子提交。",
        "gaps": ["分拆和必须等于总额", "增删行、舍入尾差、退款和编辑往返"],
    },
    "RT-03-029": {
        "entry": "顶部记账菜单 -> 批量记账",
        "states": [
            state(
                "批量记账模板",
                "页面提供模板保存、删除和生成收支记录；零金额行不会生成记录。",
                shot("b03-command-105.png"),
                COMPOSITION,
            )
        ],
        "commands": [
            command("TTemplateDlgFm", "存为模板", "观察可用命令，未点击", "模板保存语义待真实写入验证。", status="pending"),
            command("TTemplateDlgFm", "删除模板", "观察可用命令，未点击", "删除需要引用影响与确认。", status="pending", confirmation="显示模板名称和影响范围。"),
            command("TTemplateDlgFm", "生成收支记录", "观察页面警告，未点击", "仅非零行应生成，并报告跳过行。"),
        ],
        "summary": "批量记账模板和零金额跳过规则已动态确认。",
        "gaps": ["多行校验失败时的原子性", "模板版本、重复生成和逐行结果报告"],
    },
    "RT-03-030": {
        "entry": "资产侧栏 -> 第三方账户 -> 支付宝",
        "states": [
            state(
                "第三方储值流水",
                "第三方账户工作区显示账户流水，并复用记账、查找和操作入口。",
                shot("b03-third-party-account-workspace.png"),
            )
        ],
        "summary": "TThirdDepositsTransFm 的流水外壳已动态确认。",
        "gaps": ["充值、消费、提现和退款专属类型", "平台字段、导入对账和异常余额"],
    },
    "RT-03-032": {
        "entry": "顶部记账菜单 -> 批量转账",
        "states": [
            state(
                "批量转账模板",
                "页面提供模板保存、删除和生成转账记录；仅非零转账生成记录，手续费从转出账户扣除。",
                shot("b03-command-106.png"),
                COMPOSITION,
            )
        ],
        "commands": [
            command("TTransferTemplateDlgFm", "存为模板", "观察可用命令，未点击", "模板保存语义待真实写入验证。", status="pending"),
            command("TTransferTemplateDlgFm", "删除模板", "观察可用命令，未点击", "删除需要确认和引用保护。", status="pending", confirmation="显示模板名称和引用范围。"),
            command("TTransferTemplateDlgFm", "生成转账记录", "观察页面警告，未点击", "非零行和手续费规则已确认，原子性待验证。"),
        ],
        "summary": "批量转账模板、零金额跳过和手续费扣减方向已动态确认。",
        "gaps": ["跨币种批量转账", "任一行失败时的批次回滚和结果报告"],
    },
    "RT-03-033": {
        "entry": "财务记录或账户流水内嵌交易框架",
        "states": [
            state(
                "交易列表操作",
                "财务记录操作菜单显示修改、删除、替换收支项目、分组显示、批量操作、导出、打印和设为软件首页。",
                shot("b03-financial-records-operation-menu.png"),
                STATIC_CATALOG,
                EVENT_FLOW,
            ),
            state(
                "记录范围",
                "列表可在仅收支记录和全部记录之间切换。",
                shot("b03-financial-records-view-menu.png"),
            ),
        ],
        "summary": "TTransFrame 的核心列表和操作面已由财务记录宿主动态确认。",
        "gaps": ["复制粘贴、退款、转计划、改类型、附件和批量命令逐项执行", "多选快照、并发修改和失败回滚"],
    },
    "RT-03-034": {
        "entry": "主工作区 -> 财务记录",
        "states": [
            state(
                "全局财务记录",
                "页面展示日期、流入、流出、活动类型、账户、标签、余额、备注和附件等交易投影。",
                shot("b03-financial-records.png"),
                PREVIOUS_RECORDS["RT-03-034"],
            ),
            state(
                "查找与筛选入口",
                "查找菜单明确区分逐项查找和条件筛选。",
                shot("b03-financial-records-find-menu.png"),
            ),
        ],
        "summary": "TWasteBookFm 的全局交易查询、范围菜单和操作面已动态确认。",
        "gaps": ["分页、排序、导出和打印结果一致性", "隐藏账户、删除记录和本币折算口径"],
    },
    "RT-03-037": {
        "entry": "批量转账 -> 内嵌转账模板列表",
        "states": [
            state(
                "转账模板行",
                "宿主页面确认模板列表承载日期、转出账户、转入账户、金额、手续费、标签和备注。",
                shot("b03-command-106.png"),
                STATIC_CATALOG,
                COMPOSITION,
            )
        ],
        "summary": "TTransferListTemplateFrame 作为批量转账草稿行编辑器已确认。",
        "gaps": ["行级新增删除和排序", "账户组合校验、跨币种和错误定位"],
    },
    "RT-03-038": {
        "entry": "批量记账 -> 内嵌收支模板列表",
        "states": [
            state(
                "记账模板行",
                "宿主页面确认模板列表承载日期、分类、账户、金额、标签和备注。",
                shot("b03-command-105.png"),
                STATIC_CATALOG,
                COMPOSITION,
            )
        ],
        "summary": "TTransListTemplateFrame 作为批量收支草稿行编辑器已确认。",
        "gaps": ["收入支出方向和金额符号", "行级校验、模板版本与重复生成"],
    },
}


def role_flow(role: str) -> dict:
    """按队列角色生成保守数据流，不编造旧库表名。"""

    if role == "transaction_editor":
        return {
            "inputs": ["交易类型、账户、分类、日期、定点金额、标签、备注和附件", "类型专属的手续费、汇率、分拆或分期参数"],
            "reads": ["账户状态和币种", "分类、标签和交易对象目录", "原交易或模板上下文"],
            "writes": ["本轮未提交；真实保存应写入交易命令、平衡分录、关系和专属扩展"],
            "derived_results": ["账户余额、分类统计、交易列表和概况图表"],
            "side_effects": ["本轮只打开或取消编辑器，没有确认业务保存"],
            "rollback": "校验、持久化或派生更新失败时回滚完整业务命令，不保留孤立交易或单边分录。",
        }
    if role == "transaction_history":
        return {
            "inputs": ["账户或全局范围", "日期范围、记录类型、排序、分页、查找和筛选条件"],
            "reads": ["交易头、分录、账户、分类、标签、附件和专属交易扩展"],
            "writes": ["纯查询不写业务事实；修改、删除和批量操作必须转为独立命令"],
            "derived_results": ["交易行、流入流出、余额、总计和选择状态"],
            "side_effects": ["打开列表或切换视图可能保存 UI 偏好，但不得改写交易事实"],
            "rollback": "查询失败保留上次稳定视图；写命令失败后刷新原始快照并报告逐项结果。",
        }
    if role == "selector_filter":
        return {
            "inputs": ["字段、关键字、账户、活动类型、标签、金额范围和当前查找游标"],
            "reads": ["可查询字段元数据和交易投影"],
            "writes": ["查找和临时筛选不写交易；持久化视图需使用独立用户偏好模型"],
            "derived_results": ["匹配交易、命中位置和筛选条件摘要"],
            "side_effects": ["清空或取消只重置查询草稿"],
            "rollback": "非法条件不执行查询；取消恢复进入前的列表范围和选中行。",
        }
    if role == "projection_view":
        return {
            "inputs": ["时间范围、账户范围、币种和估值快照"],
            "reads": ["与交易列表相同的交易查询模型和分类维度"],
            "writes": ["图表和账户概况只读，不写业务事实"],
            "derived_results": ["收入支出序列、分类构成和账户概况"],
            "side_effects": ["切换图表只改变查询参数"],
            "rollback": "聚合失败显示明确错误，不缓存或展示部分口径结果。",
        }
    return {
        "inputs": ["配置或模板草稿、名称和行列表"],
        "reads": ["账户、分类、标签、交易类型和现有模板"],
        "writes": ["本轮未提交；真实保存应版本化模板或配置，不直接生成交易"],
        "derived_results": ["可复用草稿、列配置或分期计划"],
        "side_effects": ["取消不应生成交易或修改模板"],
        "rollback": "模板、配置或分期计划保存失败时保留旧版本并丢弃完整草稿。",
    }


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
    """把静态命令目录转换为待验证命令，保留高风险确认要求。"""

    result = []
    for item in form.get("actionable_commands", []):
        initial = dict(item.get("initial_state") or {})
        enabled = initial.get("Enabled", True)
        initial.setdefault("enabled", enabled)
        initial.setdefault("visible", True)
        related = list(item.get("related_event_ids") or [])
        entry = {
            "component": item.get("component", "unknown"),
            "label": item.get("label") or item.get("component", "未命名命令"),
            "initial_state": initial,
            "trigger": "本轮未单独触发；已从静态事件目录登记。",
            "confirmation": "修改、删除或批量写入需要显式影响预览和确认。" if item.get("high_risk") else None,
            "outcome": "等待真实操作、业务对象前后对比和失败回滚验证。",
            "status": "pending",
        }
        if related:
            entry["event_ids"] = related
        result.append(entry)
    return result


def build_record(form: dict) -> dict:
    """把 B03 队列项与动态、历史和静态证据合并。"""

    execution_id = form["execution_id"]
    dynamic = DYNAMIC.get(execution_id, {})
    states = dynamic.get("states", static_states(form))
    commands = dynamic.get("commands", queue_commands(form))
    record_evidence = [
        evidence("manual_note", NOTES, "B03 动态验证时间线、进程隔离和账簿指纹。"),
        evidence("manual_note", CONTRACT, "Rust 交易命令、分录、查询和分期运行合同。"),
        evidence("manual_note", STATIC_CATALOG, "旧窗体字段、命令和页签静态目录。"),
        evidence("manual_note", COMPOSITION, "嵌入帧与最终宿主组合证据。"),
    ]
    seen = {NOTES, CONTRACT, STATIC_CATALOG, COMPOSITION}
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
        "业务写入前后、关联分录、审计记录和失败回滚",
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
            "steps": ["打开所属交易入口", "观察字段、列表和命令", "不确认业务写入", "关闭页面并核对进程、锁和账簿"],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": states,
        "commands": commands,
        "data_flow": dynamic.get("data_flow", role_flow(form.get("role", "configuration_editor"))),
        "evidence": record_evidence,
        "requirements_update": COMMON_REQUIREMENTS + dynamic.get("requirements", []),
        "result": {
            "status": "partial",
            "summary": dynamic.get("summary", default_summary),
            "remaining_gaps": dynamic.get("gaps", default_gaps),
        },
    }


def main() -> None:
    """写出 38 条 B03 最新运行记录。"""

    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    forms = [form for form in queue["forms"] if form["batch_id"] == "B03-transactions"]
    if len(forms) != 38:
        raise RuntimeError(f"B03 队列数量异常：{len(forms)}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for form in forms:
        output_path = OUTPUT_DIR / f"{form['execution_id']}-{OUTPUT_STAMP}.json"
        output_path.write_text(
            json.dumps(build_record(form), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"generated {len(forms)} B03 records")


if __name__ == "__main__":
    main()
