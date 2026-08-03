"""生成 B09 开放式基金与货币基金页面的结构化动态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T10:06:00+08:00"
STAMP = "20260730T100600+0800"
FUND_BUY_OBSERVED_AT = "2026-08-03T08:55:23+08:00"
FUND_BUY_STAMP = "20260803T085523+0800"
LEDGER = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
SHA = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
BACKUP = "artifacts/runtime-validation/backups/test-before-b09-open-funds-20260730.mh8"
FUND_BUY_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-fund-plan-before-20260803T070512+0800.mh8"
)
NOTES = "artifacts/runtime-validation/B09-open-funds-notes.md"
CONTRACT = "docs/runtime-open-and-money-market-funds-contract.md"
STATIC_CATALOG = "docs/runtime-dfm-control-catalog.md"
COMPOSITION = "docs/runtime-form-composition-evidence.md"

COMMON_REQUIREMENTS = [
    "基金、账户、交易、份额批次、净值和转换关系必须使用稳定 ID。",
    "开放式基金和货币基金必须采用不同的金额、份额、费用和收益策略。",
    "交易事实、资金分录、份额与成本批次、费用和收益必须原子提交。",
    "持仓、页脚、市值构成、历史盈亏、导出和打印必须绑定同一估值快照。",
    "未经真实保存样例校准，不得把费率舍入、收益结转、成本分配或拆分公式标记为已兼容。",
]


def shot(name: str) -> str:
    """返回 B09 截图的仓库相对路径。"""
    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(path: str, description: str, kind: str = "screenshot") -> dict:
    """创建结构化证据条目。"""
    return {"kind": kind, "path": path, "description": description}


def state(name: str, status: str, observations: str, *paths: str) -> dict:
    """创建页面状态并附加证据路径。"""
    item = {"name": name, "status": status, "observations": observations}
    if paths:
        item["evidence_paths"] = list(paths)
    return item


def command(label: str, trigger: str, outcome: str, status: str = "pass") -> dict:
    """创建命令观察；pass 只表示入口及其可见结果已经确认。"""
    return {
        "component": "页面命令区",
        "label": label,
        "initial_state": {"enabled": status != "disabled", "visible": True},
        "trigger": trigger,
        "confirmation": None,
        "outcome": outcome,
        "status": "pass" if status == "disabled" else status,
    }


def flow(
    inputs: list[str],
    reads: list[str],
    writes: list[str],
    derived: list[str],
    rollback: str,
) -> dict:
    """创建基金领域的数据流说明。"""
    return {
        "inputs": inputs,
        "reads": reads,
        "writes": writes,
        "derived_results": derived,
        "side_effects": [
            "本轮只为货币基金空状态取证创建并删除临时账户；专用进程退出后已恢复 B09 前账簿。"
        ],
        "rollback": rollback,
    }


def record(
    execution_id: str,
    resource: str,
    entry_point: str,
    states: list[dict],
    commands: list[dict],
    data_flow: dict,
    evidence_items: list[dict],
    summary: str,
    gaps: list[str],
    requirements: list[str] | None = None,
    reachable: bool = True,
    unreachable_reason: str | None = None,
) -> dict:
    """组装符合运行观察 Schema 的 B09 记录。"""
    return {
        "schema_version": 1,
        "execution_id": execution_id,
        "resource": resource,
        "observed_at": OBSERVED_AT,
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": LEDGER,
            "sha256_before": SHA,
            "sha256_after": SHA,
            "backup_artifact": BACKUP,
        },
        "navigation": {
            "entry_point": entry_point,
            "steps": [
                "仅在 PID 33332 的专用 MoneyHome8 实例中打开 B09 页面",
                "观察字段、菜单、页签、列表、汇总和禁用状态",
                "货币基金空状态使用零余额临时账户，取证后通过删除确认框删除",
                "正常退出并保存退出态副本，再恢复 B09 前账簿指纹",
            ],
            "reachable": reachable,
            "unreachable_reason": unreachable_reason,
        },
        "states": states,
        "commands": commands,
        "data_flow": data_flow,
        "evidence": [
            evidence(NOTES, "B09 动态时间线、临时账户、进程隔离和账簿恢复证据。", "manual_note"),
            evidence(CONTRACT, "Rust 基金目录、账户、交易、估值和原子性合同。", "manual_note"),
            *evidence_items,
        ],
        "requirements_update": COMMON_REQUIREMENTS + (requirements or []),
        "result": {"status": "partial", "summary": summary, "remaining_gaps": gaps},
    }


def new_records() -> list[dict]:
    """返回本轮新增直接证据的十七条基金资源记录。"""
    curr_workspace = shot("b09-current-fund-workspace-sanitized.png")
    open_workspace = shot("b09-open-fund-workspace-sanitized.png")
    return [
        record(
            "RT-09-001",
            "TCURRFUNDACCTDLGFM",
            "账户中心 -> 货币基金账户 -> 修改账户",
            [
                state("账户字段", "observed", "账户名称、币种、所有者、备注、创建日期、开户机构、账号、默认资金账户、资产性质和附件均已动态显示。", shot("b09-current-fund-account-editor.png")),
                state("资产性质", "observed", "货币基金账户可选择投资或储蓄，这是开放式基金账户没有的分类字段。", shot("b09-current-fund-account-editor.png")),
                state("保存", "pending", "本轮关闭账户编辑器，临时账户通过账户列表命令删除。"),
            ],
            [command("修改账户", "双击临时货币基金账户", "打开 TCurrFundAcctDlgFm。"), command("确定", "本轮未触发", "账户修改校验和审计待验证。", "pending")],
            flow(["账户资料", "默认资金来源", "投资或储蓄"], ["账户、账户组、所有者和资金账户"], ["目标保存应更新基金账户聚合"], ["账户概况和交易默认值"], "账户修改与默认资金关系必须原子提交；已有交易时禁止静默变更类型或币种。"),
            [evidence(shot("b09-current-fund-account-editor.png"), "临时货币基金账户编辑器。"), evidence(shot("b09-current-fund-account-row-menu.png"), "账户修改、删除、注销、隐藏、分组、标签和附件菜单。")],
            "已动态确认证券账户之外的货币基金账户字段、资产性质和删除入口。",
            ["真实修改保存", "已有交易时的币种和资产性质限制", "附件和默认资金账户失效"],
        ),
        record(
            "RT-09-006",
            "TCURRFUNDSLISTFM",
            "应用菜单 -> 数据管理 -> 开放式基金 -> 货币基金",
            [
                state("基金目录", "observed", "目录显示代码、名称、币种、搜索、新增基金和操作菜单。", shot("b09-current-funds-list-sanitized.png")),
                state("目录差异", "observed", "货币基金列表不显示开放式基金的申购费率、赎回费率和历史净值区。", shot("b09-current-funds-list-sanitized.png")),
                state("写操作", "pending", "新增入口已到达，修改、删除、导出和打印未提交。"),
            ],
            [command("新增基金", "点击货币基金列表的新增基金", "打开 TEditCurrFundFm。"), command("操作", "入口可见", "修改、删除和输出待验证。", "pending")],
            flow(["类别和搜索关键字", "基金代码、名称和币种"], ["货币基金目录"], ["目标命令维护稳定基金目录"], ["交易候选和账户持仓名称"], "被交易引用的基金不得物理删除；代码和名称更新必须保留审计。"),
            [evidence(shot("b09-current-funds-list-sanitized.png"), "货币基金资料目录。")],
            "已动态确认货币基金目录、搜索和新增入口。",
            ["修改和删除限制", "重复代码和名称锁定", "导出和打印"],
        ),
        record(
            "RT-09-007",
            "TCURRFUNDSTATISTICFRAME",
            "账户中心 -> 临时货币基金账户 -> 上半区统计",
            [
                state("空持仓", "observed", "列为基金名称、累计金额和占比；零余额账户返回空集合。", curr_workspace),
                state("页脚", "observed", "页脚显示总实现盈亏、可用资金、总市值和总计，空账户均为 0.00。", curr_workspace),
                state("有数据计算", "pending", "当前账簿原本没有货币基金账户，未取得本金、收益和累计金额样例。"),
            ],
            [command("当前持仓基金", "范围菜单入口可见", "范围切换和有数据结果待验证。", "pending"), command("获取代码", "顶部入口可见", "在线更新及失败状态待验证。", "pending")],
            flow(["账户", "持仓范围", "账簿修订"], ["货币基金交易、份额、本金和收益结转"], [], ["累计金额、占比、实现盈亏、可用资金和总计"], "所有行和页脚必须来自同一账簿修订，查询失败不得发布部分汇总。"),
            [evidence(curr_workspace, "脱敏后的货币基金空持仓统计。")],
            "已动态确认货币基金统计 Frame 的空状态、列和页脚口径。",
            ["有数据累计金额公式", "本金与收益结转", "跨币种和缺代码"],
        ),
        record(
            "RT-09-008",
            "TCURRFUNDTRANSFM",
            "账户中心 -> 临时货币基金账户",
            [
                state("组合宿主", "observed", "宿主动态组合货币基金统计、交易明细和历史盈亏页。", curr_workspace, COMPOSITION),
                state("顶部操作", "observed", "菜单含余额调整、持仓调整、查看账户资料和设为首页；空账户时代码转换、导出和打印禁用。", shot("b09-current-fund-top-operation-menu.png")),
                state("临时账户清理", "observed", "页面取证后通过删除确认框删除临时账户。", shot("b09-delete-temp-current-fund-confirm.png")),
            ],
            [command("查看账户资料", "从顶部操作菜单进入", "打开账户概况及 TCurrFundViewFrame。"), command("删除账户", "返回账户中心并确认删除", "临时账户被移除。")],
            flow(["货币基金账户", "页签和查询范围"], ["账户、交易、份额、本金和收益"], [], ["统一货币基金工作区"], "子查询、账户创建和删除都必须使用明确事务与账簿版本。"),
            [evidence(curr_workspace, "货币基金工作区空状态。"), evidence(shot("b09-current-fund-top-operation-menu.png"), "货币基金顶部操作菜单。"), evidence(shot("b09-delete-temp-current-fund-confirm.png"), "临时账户删除确认。")],
            "已动态确认货币基金工作区宿主、子视图、命令状态及临时账户清理。",
            ["有数据工作区", "导出和打印", "异常、关闭账户和并发刷新"],
        ),
        record(
            "RT-09-009",
            "TCURRFUNDTRANSFRAME",
            "货币基金工作区 -> 交易明细",
            [
                state("空列表", "observed", "空账户明确显示没有交易记录，页脚流入、流出、差额和记录数均为零。", curr_workspace),
                state("工具栏", "observed", "支持记账、单只基金交易明细、日期范围、查找和操作；无数据时查找禁用。", curr_workspace),
                state("有数据列与行操作", "pending", "货币基金真实交易行、修改、删除、附件和输出待验证。"),
            ],
            [command("记账", "工具栏入口可见", "打开货币基金交易命令集合。"), command("查找", "空账户状态", "无记录时禁用。", "disabled")],
            flow(["账户", "基金范围", "日期范围和搜索条件"], ["已提交货币基金交易、标签和余额投影"], [], ["交易明细、流入流出、差额和记录数"], "查询只读；修改或删除必须通过领域命令重建持仓和收益。"),
            [evidence(curr_workspace, "脱敏后的货币基金交易明细空状态。")],
            "已动态确认货币基金交易 Frame 的工具栏、空状态和页脚。",
            ["有数据列和排序", "行级修改删除", "附件、导出、打印和大数据量"],
        ),
        record(
            "RT-09-010",
            "TEDITCURRFUNDFM",
            "数据管理 -> 货币基金 -> 新增基金",
            [state("初始字段", "observed", "字段为代码、名称、币种和名称锁定。", shot("b09-current-fund-editor.png")), state("保存", "pending", "本轮关闭未保存，重复代码、锁名和被引用删除规则待验证。")],
            [command("新增基金", "点击目录页新增基金", "打开 TEditCurrFundFm。"), command("保存", "本轮未触发", "目录写入待验证。", "pending")],
            flow(["基金代码", "名称", "币种", "名称锁定"], ["现有基金和代码别名"], ["目标保存应新增稳定货币基金目录项"], ["基金选择候选"], "基金目录项和代码唯一性校验必须同事务提交。"),
            [evidence(shot("b09-current-fund-editor.png"), "货币基金资料编辑器。")],
            "已动态到达货币基金编辑器并确认精简字段。",
            ["新增和修改保存", "重复代码、名称锁定", "被引用删除限制"],
        ),
        record(
            "RT-09-011",
            "TEDITOPENFUNDFM",
            "数据管理 -> 开放式基金 -> 新增基金",
            [state("初始字段", "observed", "字段为代码、名称、币种、申购费率、赎回费率和名称锁定。", shot("b09-open-fund-editor.png")), state("保存", "pending", "费率单位、范围、舍入和真实保存未验证。")],
            [command("新增基金", "点击开放式基金列表新增基金", "打开 TEditOpenFundFm。"), command("保存", "本轮未触发", "目录和费率写入待验证。", "pending")],
            flow(["代码、名称和币种", "申购费率和赎回费率"], ["现有开放式基金目录"], ["目标保存应新增目录项和费率版本"], ["交易默认费率"], "目录和费率必须整体校验，历史交易必须保留实际费率快照。"),
            [evidence(shot("b09-open-fund-editor.png"), "开放式基金资料编辑器。")],
            "已动态确认开放式基金编辑器及其申购、赎回费率字段。",
            ["费率单位和边界", "新增、修改和删除", "历史交易费率不回算"],
        ),
        record(
            "RT-09-020",
            "TNEWACCTWIZARDCURRFUNDDLGFM",
            "账户中心 -> 新增账户 -> 基金 -> 货币基金",
            [
                state("第一页", "observed", "账户名称、币种、所有者、备注和账户组。", shot("b09-new-current-fund-account-wizard.png")),
                state("第二页", "observed", "日期、账户自身余额或其它账户资金来源，并选择投资或储蓄。", shot("b09-new-current-fund-account-wizard-step2.png")),
                state("完成与删除", "observed", "完成创建零余额账户，覆盖工作区后通过删除确认移除。", shot("b09-delete-temp-current-fund-confirm.png")),
            ],
            [command("下一步", "完成第一页", "进入资金来源和资产性质页。"), command("完成", "使用零余额自身资金", "创建临时货币基金账户。"), command("删除账户", "完成取证后确认删除", "临时账户被移除。")],
            flow(["账户资料", "资金来源", "投资或储蓄"], ["账户组、所有者和资金账户"], ["创建账户和初始化事件；本轮随后删除"], ["账户列表和空工作区"], "账户、初始资金和资产性质必须同事务创建；删除失败不得留下孤立关系。"),
            [evidence(shot("b09-new-current-fund-account-wizard.png"), "货币基金账户向导第一页。"), evidence(shot("b09-new-current-fund-account-wizard-step2.png"), "货币基金账户向导第二页。"), evidence(shot("b09-delete-temp-current-fund-confirm.png"), "临时账户删除确认。")],
            "已动态验证货币基金账户向导两页、完成创建、空工作区和删除清理。",
            ["其它账户资金来源", "非零初始余额", "重复名称、失败回滚和并发创建"],
        ),
        record(
            "RT-09-021",
            "TNEWACCTWIZARDOPENFUNDDLGFM",
            "账户中心 -> 新增账户 -> 基金 -> 开放式基金",
            [state("第一页", "observed", "账户名称、币种、所有者、备注和账户组。", shot("b09-new-open-fund-account-wizard.png")), state("第二页", "observed", "日期及账户自身余额或其它账户资金来源。", shot("b09-new-open-fund-account-wizard-step2.png")), state("完成", "pending", "本轮在完成前关闭，没有创建开放式基金账户。")],
            [command("下一步", "完成第一页", "进入资金来源页。"), command("完成", "本轮未触发", "账户、资金事件和回滚待验证。", "pending")],
            flow(["账户资料", "币种和资金来源"], ["账户组、所有者和资金账户"], ["目标完成应创建开放式基金账户和初始化事件"], ["账户列表和工作区"], "账户和初始资金必须同事务创建。"),
            [evidence(shot("b09-new-open-fund-account-wizard.png"), "开放式基金账户向导第一页。"), evidence(shot("b09-new-open-fund-account-wizard-step2.png"), "开放式基金账户向导第二页。不可见货币基金的资产性质字段。")],
            "已动态验证开放式基金账户向导两页及其与货币基金向导的字段差异。",
            ["真实创建和删除", "非零及其它账户资金来源", "重复名称和失败回滚"],
        ),
        record(
            "RT-09-022",
            "TOPENFUNDACCTDLGFM",
            "账户中心 -> 开放式基金账户 -> 修改账户",
            [state("账户字段", "observed", "账户名称、币种、所有者、备注、创建日期、开户机构、账号、默认资金账户和附件已动态显示。", shot("b09-open-fund-account-editor-sanitized.png")), state("保存", "pending", "本轮关闭未保存，没有变更现有账户。")],
            [command("修改账户", "双击开放式基金账户", "打开 TOpenFundAcctDlgFm。"), command("确定", "本轮未触发", "真实修改与限制待验证。", "pending")],
            flow(["账户资料", "机构和账号", "默认资金来源"], ["现有账户及引用关系"], ["目标保存应更新账户聚合和审计事件"], ["账户概况和交易默认值"], "已有交易时币种和类型不可静默变更，默认关系更新必须原子提交。"),
            [evidence(shot("b09-open-fund-account-editor-sanitized.png"), "脱敏后的开放式基金账户编辑器。"), evidence(shot("b09-open-fund-account-row-menu.png"), "开放式基金账户行操作菜单。")],
            "已动态确认开放式基金账户编辑器和账户行操作。",
            ["真实修改", "币种和资金来源限制", "注销、隐藏和附件"],
        ),
        record(
            "RT-09-023",
            "TOPENFUNDSLISTFM",
            "应用菜单 -> 数据管理 -> 开放式基金",
            [state("基金目录", "observed", "目录显示代码、名称、币种、申购费率、赎回费率、搜索和新增基金。", shot("b09-open-funds-list-sanitized.png")), state("历史净值", "observed", "下半区显示日期、代码、名称和净值，并支持新增价格和显示单日所有价格。", shot("b09-open-funds-list-sanitized.png")), state("写入与输出", "pending", "目录、净值的修改删除及导出打印未提交。")],
            [command("新增基金", "点击目录页入口", "打开 TEditOpenFundFm。"), command("新增价格", "下半区入口可见", "净值保存未执行。", "pending")],
            flow(["搜索条件", "基金资料", "历史净值"], ["基金目录和净值观察"], ["目标命令维护目录与净值事实"], ["交易候选和估值批次"], "被引用基金不得物理删除；净值批次校验成功后才能发布。"),
            [evidence(shot("b09-open-funds-list-sanitized.png"), "开放式基金资料与历史净值双列表。"), evidence(shot("b09-open-fund-nav-editor-sanitized.png"), "脱敏后的基金净值编辑器。")],
            "已动态确认开放式基金目录、申赎费率、历史净值和新增入口。",
            ["目录和净值保存", "重复日期和覆盖策略", "删除限制、导出和打印"],
        ),
        record(
            "RT-09-024",
            "TOPENFUNDSTATISTICFRAME",
            "开放式基金工作区 -> 上半区持仓统计",
            [
                state("持仓列", "observed", "列为基金名称、持仓数量、持仓成本、市值、占比、浮动盈亏、均价、基金净值和浮动收益率。", open_workspace),
                state("估值公式", "observed", "60,000.81 * 2.4195 = 145,171.96；市值减成本得到浮动盈亏 73,716.97。", open_workspace),
                state("盈亏汇总", "observed", "浮动盈亏 73,716.97 加已实现盈亏 132,594.11 等于总盈亏 206,311.08。", open_workspace),
            ],
            [command("当前持仓基金", "顶部范围入口可见", "可按当前持仓范围查询。"), command("获取净值", "入口可见", "在线更新、失败和批次发布待验证。", "pending")],
            flow(["账户", "基金范围", "估值快照"], ["份额、成本批次、净值和已实现盈亏"], [], ["数量、成本、市值、均价、浮动和总盈亏"], "持仓行、页脚和下游图表必须使用同一 FundValuationRef。"),
            [evidence(open_workspace, "脱敏后的开放式基金持仓、交易和汇总。")],
            "已动态确认开放式基金持仓统计 Frame、主要列和样例估值公式。",
            ["缺净值和跨币种", "费用后成本和收益率精度", "在线更新及并发快照"],
        ),
        record(
            "RT-09-025",
            "TOPENFUNDTRANSFM",
            "账户中心 -> 开放式基金账户",
            [state("组合宿主", "observed", "宿主组合持仓统计、交易明细、市值构成和历史盈亏。", open_workspace, COMPOSITION), state("顶部操作", "observed", "菜单含余额调整、持仓调整、代码变更、添加净值、账户资料、导出、打印和设为首页。", shot("b09-open-fund-top-operation-menu.png")), state("账户资料", "observed", "查看账户资料打开账户概况和 TOpenFundViewFrame。", shot("b09-open-fund-account-overview-sanitized.png"))],
            [command("添加基金净值", "顶部操作菜单", "打开共用的 TEditSecurityPriceFm，标题为基金净值。"), command("查看账户资料", "顶部操作菜单", "打开开放式基金账户概况。")],
            flow(["开放式基金账户", "页签和查询范围"], ["账户、交易、份额、成本、净值和标签"], [], ["统一开放式基金工作区"], "任一子查询失败不得发布互相不一致的持仓、交易、图表或页脚。"),
            [evidence(open_workspace, "开放式基金工作区宿主。"), evidence(shot("b09-open-fund-top-operation-menu.png"), "开放式基金顶部操作菜单。"), evidence(shot("b09-open-fund-nav-editor-sanitized.png"), "基金净值编辑器。")],
            "已动态确认开放式基金工作区、四个查询视图及净值和账户资料入口。",
            ["导出和打印", "缺净值、关闭账户和并发刷新", "代码变更后的引用迁移"],
        ),
        record(
            "RT-09-026",
            "TOPENFUNDTRANSFRAME",
            "开放式基金工作区 -> 交易明细",
            [
                state("交易列", "observed", "显示日期、基金、价格、数量、费率、交易金额、活动类型、标签、余额、备注和附件。", open_workspace),
                state("范围与页脚", "observed", "支持记账、全部交易明细、日期范围、查找和操作；流入和流出均为 233,654.53，共 23 条。", open_workspace),
                state("行级写操作", "pending", "修改、删除、附件、导出和打印未逐项验证。"),
            ],
            [command("记账", "交易明细工具栏", "进入开放式基金交易命令集合。"), command("查找", "有数据状态入口可用", "搜索字段、排序和分页待验证。", "pending")],
            flow(["账户", "基金范围", "日期范围和搜索条件"], ["已提交基金交易、费率快照、标签和余额"], [], ["交易明细、流入流出、差额和记录数"], "查询只读；交易修改或删除必须重建份额、成本和盈亏投影。"),
            [evidence(open_workspace, "脱敏后的开放式基金交易明细。")],
            "已动态确认开放式基金交易 Frame 的真实列、工具栏、有数据状态和页脚。",
            ["行级修改删除", "附件、导出和打印", "分页、排序和大数据量"],
        ),
        record(
            "RT-09-027",
            "TCURRFUNDMARKETCONSTITUTESFRAME",
            "银行理财产品工作区 -> 市值构成（跨域复用 Frame）",
            [
                state("组合宿主", "observed", "DFM 证明该 Frame 嵌入 TMoneyTransFm 的市值构成页，不属于 TCurrFundTransFm。", COMPOSITION, STATIC_CATALOG),
                state("动态父页", "observed", "B05 已动态到达银行理财产品工作区并确认市值构成页签。", shot("b05-bank-wealth-workspace-sanitized.png")),
                state("有数据构成", "pending", "B05 空账户没有可校准的构成分项和图表数据。"),
            ],
            [command("市值构成", "银行理财产品工作区页签", "页签可见，空账户下无构成数据。", "pending")],
            flow(["银行理财产品账户", "估值快照"], ["产品持仓、成本和估值"], [], ["市值构成分项和图表"], "构成分项与宿主持仓页脚必须使用同一估值修订。"),
            [evidence(COMPOSITION, "TCurrFundMarketConstitutesFrame 到 TMoneyTransFm 的直接组合关系。", "manual_note"), evidence(STATIC_CATALOG, "Frame 工具栏和图表结构。", "manual_note"), evidence(shot("b05-bank-wealth-workspace-sanitized.png"), "银行理财产品工作区及市值构成页签。")],
            "已确认该历史命名 Frame 的真实跨域宿主和页签，但缺少有数据构成样例。",
            ["有数据分项与图表", "合计公式", "导出、打印和缺估值状态"],
        ),
        record(
            "RT-09-028",
            "TCURRFUNDVIEWFRAME",
            "货币基金工作区 -> 操作 -> 查看账户资料",
            [state("动态宿主", "observed", "TAccountOverviewDlgFm 内加载货币基金账户概况 Frame。", shot("b09-current-fund-account-overview.png")), state("概况字段", "observed", "显示账户组、标签、附件、币种、资金来源、资产性质、机构、账号、联系方式和密码入口。", shot("b09-current-fund-account-overview.png"))],
            [command("修改账户概况", "账户概况链接", "进入 TCurrFundAcctDlgFm。")],
            flow(["货币基金账户 ID"], ["账户、分组、标签、附件和机构资料"], [], ["只读货币基金账户概况"], "概况只读查询不得修改账户；敏感字段按权限读取并记录审计。"),
            [evidence(shot("b09-current-fund-account-overview.png"), "临时货币基金账户概况。")],
            "已动态确认 TCurrFundViewFrame 的宿主、资产性质和账户资料字段。",
            ["密码查看权限和审计", "附件增删", "关闭或隐藏账户状态"],
        ),
        record(
            "RT-09-029",
            "TOPENFUNDVIEWFRAME",
            "开放式基金工作区 -> 操作 -> 查看账户资料",
            [state("动态宿主", "observed", "TAccountOverviewDlgFm 内加载开放式基金账户概况 Frame。", shot("b09-open-fund-account-overview-sanitized.png")), state("概况字段", "observed", "显示账户组、标签、附件、币种、资金来源、机构、账号、联系方式和密码入口。", shot("b09-open-fund-account-overview-sanitized.png"))],
            [command("修改账户概况", "账户概况链接", "进入 TOpenFundAcctDlgFm。")],
            flow(["开放式基金账户 ID"], ["账户、分组、标签、附件和机构资料"], [], ["只读开放式基金账户概况"], "概况查询失败不得修改账户；敏感字段按权限读取并避免进入日志。"),
            [evidence(shot("b09-open-fund-account-overview-sanitized.png"), "脱敏后的开放式基金账户概况。")],
            "已动态确认 TOpenFundViewFrame 的最终宿主、字段和账户编辑入口。",
            ["密码查看权限和审计", "附件增删", "关闭或隐藏账户状态"],
        ),
    ]


def updated_existing_records() -> list[dict]:
    """保留既有十一条基金交易表单观察，并统一到 B09 最终边界。"""
    updated = []
    numbers = [2, 3, 4, 5, *range(13, 20)]
    for number in numbers:
        execution_id = f"RT-09-{number:03d}"
        candidates = sorted(OUTPUT.glob(f"{execution_id}-*.json"))
        if not candidates:
            raise FileNotFoundError(f"缺少既有观察记录：{execution_id}")
        item = json.loads(candidates[-1].read_text(encoding="utf-8"))
        item["observed_at"] = OBSERVED_AT
        item["ledger"] = {
            "path": LEDGER,
            "sha256_before": SHA,
            "sha256_after": SHA,
            "backup_artifact": BACKUP,
        }
        item["navigation"]["steps"] = [
            *item["navigation"].get("steps", []),
            "本轮纳入 B09 账户、工作区和资料管理综合观察",
            "专用进程正常退出后恢复 B09 前账簿指纹",
        ]
        item["evidence"] = [
            evidence(NOTES, "B09 最终进程隔离、临时账户和账簿恢复证据。", "manual_note"),
            evidence(CONTRACT, "Rust 开放式基金与货币基金差异化交易合同。", "manual_note"),
            *[
                entry
                for entry in item.get("evidence", [])
                if entry.get("path") not in {NOTES, CONTRACT}
            ],
        ]
        existing_requirements = item.get("requirements_update", [])
        item["requirements_update"] = list(
            dict.fromkeys(COMMON_REQUIREMENTS + existing_requirements)
        )
        item["result"]["status"] = "partial"
        item["result"]["remaining_gaps"] = [
            gap
            for gap in item["result"].get("remaining_gaps", [])
            if "SHA-256" not in gap
        ]
        updated.append(item)
    return updated


def fund_buy_record() -> dict:
    """生成基金计划执行产生的开放式基金申购动态记录。"""
    editor = shot("moneyhome-fund-plan-execution-editor-aligned-20260803T0727.png")
    financial_record = shot(
        "moneyhome-fund-plan-financial-record-after-execution-20260803T0846.png"
    )
    investment_overview = shot(
        "moneyhome-fund-plan-investment-overview-after-execution-20260803T0848.png"
    )
    return {
        "schema_version": 1,
        "execution_id": "RT-09-012",
        "resource": "TFUNDBUYDLGFM",
        "observed_at": FUND_BUY_OBSERVED_AT,
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": LEDGER,
            "sha256_before": SHA,
            "sha256_after": SHA,
            "backup_artifact": FUND_BUY_BACKUP,
        },
        "navigation": {
            "entry_point": "计划与提醒 -> 基金申购/定投计划 -> 执行",
            "steps": [
                "创建并保存到期的一次性手工基金计划，但在立即执行询问中选择否",
                "从计划列表点击执行，打开执行计划-开放式基金申购",
                "核对计划预填的基金账户、资金账户、基金、前端费率、金额、日期和自动入账备注",
                "输入单位净值 1.0000，核对费用 0.01 和份额 0.99 后立即入账",
                "交叉核对财务记录、Cash-CNY 和投资一览持仓",
                "归档操作后账簿与残留锁，再恢复 test.mh8 精确基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            state(
                "计划执行草稿",
                "observed",
                "计划预填基金账户、资金账户、基金、前端收费、费率 1.00%、申购金额 1.00、日期和计划自动入账备注；单位净值和份额仍需执行时确认。",
                shot("moneyhome-fund-plan-execution-editor-20260803T0722.png"),
                editor,
            ),
            state(
                "真实申购结果",
                "observed",
                "单位净值 1.0000、申购金额 1.00、前端费率 1.00% 计算申购费用 0.01、申购份额 0.99；入账后生成唯一交易并同步资金账户和基金持仓。",
                financial_record,
                investment_overview,
            ),
        ],
        "commands": [
            {
                **command(
                    "更新基金",
                    "点击更新基金",
                    "入口可用；联网刷新、失败提示和回滚本轮未执行。",
                    "partial",
                ),
                "component": "btnUpdateCode",
                "event_ids": ["funds.fund_buy_dlg_fm.btn_update_code_click"],
            },
            {
                **command(
                    "净值、金额、费用和份额计算",
                    "输入单位净值 1.0000 并提交申购金额 1.00",
                    "前端费率 1.00% 计算费用 0.01、净申购金额 0.99 和份额 0.99。",
                ),
                "component": "edPrice/edAmt/edFee/edQuantity",
                "event_ids": [
                    "funds.fund_buy_dlg_fm.ed_price_change",
                    "funds.fund_buy_dlg_fm.ed_price_exit",
                ],
            },
            {
                **command(
                    "立即入账",
                    "点击立即入账",
                    "生成一条流出 1.00 的开放式基金申购，Cash-CNY 减少 1.00，新增 0.99 份和成本 1.00。",
                ),
                "component": "btnSaveExit",
            },
        ],
        "data_flow": {
            "inputs": [
                "基金账户、资金账户和基金稳定引用",
                "单位净值、申购金额、收费模式和费率",
                "标签、日期和备注",
            ],
            "reads": [
                "基金资料和账户候选",
                "执行时成交净值",
                "投资一览使用的最新行情快照",
            ],
            "writes": ["开放式基金申购交易", "资金账户流出", "基金份额和持仓成本"],
            "derived_results": [
                "申购费用 0.01",
                "净申购金额 0.99",
                "申购份额 0.99",
                "含费均价 1.0101",
                "最新行情市值 1.10 和浮动盈亏 0.10",
            ],
            "side_effects": [
                "财务记录数由 2189 增至 2190，新增路径为国泰证券开放基金 <- Cash-CNY 的流出 1.00。",
                "Cash-CNY 从 608.00 降至 607.00。",
                "投资一览新增 008903 广发科技先锋混合 0.99 份，成本 1.00、均价 1.0101。",
            ],
            "rollback": (
                "操作后账簿 artifacts/runtime-validation/backups/"
                "RT-15-fund-plan-after-20260803T085523+0800.mh8 的 SHA-256 为 "
                "DAD4F38BD8BE10F17DFFA75F8D418C300B38255B7212ACF6ACE1D8786320C236；"
                "残留锁归档 SHA-256 为 "
                "EAD592C694B45FF5E4D31522B181A5C967DC9F932516174D9E5AB5EE760B0A3E。"
                "随后恢复 test.mh8 至基线，进程和锁文件均为 0。"
            ),
        },
        "evidence": [
            evidence(editor, "真实申购草稿中的净值、金额、费率、费用和份额。"),
            evidence(financial_record, "开放式基金申购财务流水。"),
            evidence(investment_overview, "申购后的份额、成本、均价、市值和浮动盈亏。"),
            evidence(
                "artifacts/runtime-validation/RT15-plans-and-reminders-notes.md",
                "基金计划定义、实例、执行草稿和最终交易的完整生命周期说明。",
                "manual_note",
            ),
            evidence(
                "docs/runtime-event-command-dataflow.json",
                "TFUNDBUYDLGFM 事件到目标命令边界。",
                "file",
            ),
        ],
        "requirements_update": [
            "开放式基金申购必须冻结基金、账户、成交净值、收费模式、费率、费用、毛金额、净金额和最终份额。",
            "资金流出、费用、份额和成本必须在一个幂等事务中提交。",
            "持仓均价使用含费用总成本，历史成交不得按最新费率重算。",
            "成交净值与后续行情估值必须分离，市值和浮动盈亏由同一估值快照重建。",
        ],
        "result": {
            "status": "pass",
            "summary": "已完成开放式基金申购的代表性真实保存，验证前端费用、净份额、资金流出、持仓成本和独立行情估值。",
            "remaining_gaps": [
                "其它金额和前端费率的舍入边界",
                "后端收费及其它收费模式",
                "余额不足、重复提交、联网更新和失败回滚",
            ],
        },
    }


def main() -> None:
    """写出 B09 全部二十九条最新记录。"""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    items = new_records() + updated_existing_records() + [fund_buy_record()]
    items.sort(key=lambda item: item["execution_id"])
    if len(items) != 29:
        raise RuntimeError(f"B09 记录数量错误：{len(items)}")
    for item in items:
        stamp = FUND_BUY_STAMP if item["execution_id"] == "RT-09-012" else STAMP
        path = OUTPUT / f"{item['execution_id']}-{stamp}.json"
        path.write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"B09 观察记录生成完成：{len(items)} 条")


if __name__ == "__main__":
    main()
