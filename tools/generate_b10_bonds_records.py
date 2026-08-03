"""生成 B10 债券页面的结构化动态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T10:49:00+08:00"
STAMP = "20260730T104900+0800"
LEDGER = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
SHA = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
BACKUP = "artifacts/runtime-validation/backups/test-before-b10-bonds-20260730.mh8"
NOTES = "artifacts/runtime-validation/B10-bonds-notes.md"
CONTRACT = "docs/runtime-bonds-ledger-and-maturity-contract.md"
STATIC_CATALOG = "docs/runtime-dfm-control-catalog.md"
COMPOSITION = "docs/runtime-form-composition-evidence.md"

COMMON_REQUIREMENTS = [
    "债券、发行人、账户、交易、持仓批次和估值批次必须使用稳定 ID。",
    "净价、全价、应计利息、资本成本、费用和税费必须分项保存。",
    "买卖、利息、到期和提前兑取必须原子更新交易、资金、持仓、成本和收益。",
    "持仓、页脚、成本市值构成、历史盈亏、导出和打印必须绑定同一估值快照。",
    "未经真实保存样例校准，不得把报价单位、舍入、税费、到期或提前兑取公式标记为已兼容。",
]


def shot(name: str) -> str:
    """返回 B10 截图的仓库相对路径。"""
    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(path: str, description: str, kind: str = "screenshot") -> dict:
    """创建结构化证据条目。"""
    return {"kind": kind, "path": path, "description": description}


def state(name: str, status: str, observations: str, *paths: str) -> dict:
    """创建页面状态并附加可公开引用的证据。"""
    item = {"name": name, "status": status, "observations": observations}
    if paths:
        item["evidence_paths"] = list(paths)
    return item


def command(label: str, trigger: str, outcome: str, status: str = "pass") -> dict:
    """记录命令可见性和动态结果；pass 不代表业务公式已兼容。"""
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
    """创建债券领域的数据流说明。"""
    return {
        "inputs": inputs,
        "reads": reads,
        "writes": writes,
        "derived_results": derived,
        "side_effects": [
            "本轮只创建并删除零余额临时债券账户；未保存债券资料或交易，退出后已恢复 B10 前账簿。"
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
) -> dict:
    """组装符合运行观察 Schema 的 B10 记录。"""
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
                "仅在 PID 25552 的专用 MoneyHome8 实例中打开 B10 页面",
                "观察字段、菜单、页签、空状态、必填校验和组合关系",
                "除创建和删除零余额临时债券账户外不提交业务写入",
                "正常退出、保留退出态副本并恢复 B10 前账簿指纹",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": states,
        "commands": commands,
        "data_flow": data_flow,
        "evidence": [
            evidence(NOTES, "B10 动态时间线、临时账户、进程隔离和账簿恢复证据。", "manual_note"),
            evidence(CONTRACT, "Rust 债券资料、账户、交易、应计、终止事件和估值合同。", "manual_note"),
            *evidence_items,
        ],
        "requirements_update": COMMON_REQUIREMENTS + (requirements or []),
        "result": {"status": "partial", "summary": summary, "remaining_gaps": gaps},
    }


def records() -> list[dict]:
    """返回 B10 的十五条债券资源记录。"""
    workspace = shot("b10-bond-workspace-sanitized.png")
    return [
        record(
            "RT-10-001",
            "TEDITNMARKETBONDFM",
            "资料管理 -> 债券 -> 新增债券",
            [
                state("主数据字段", "observed", "名称、代码、币种、发行单位、发行日、到期日、年利率、类型、两个付息月日、面值和免税均已显示。", shot("b10-bond-editor.png")),
                state("面值规则", "observed", "面值只读为 100，界面提示当前只提供面值 100 的债券。", shot("b10-bond-editor.png")),
                state("必填校验", "observed", "空名称保存被阻止，并提示请输入债券名称。", shot("b10-bond-editor-required-validation.png")),
                state("真实保存", "pending", "本轮未创建债券资料。"),
            ],
            [
                command("保存", "债券名称为空时点击", "显示必填提示且编辑器保持打开。"),
                command("保存", "有效资料未提交", "唯一性、日期和引用规则待验证。", "pending"),
            ],
            flow(["债券名称、代码和币种", "发行、到期和付息规则", "利率、面值、类型和免税"], ["发行人和既有债券目录"], ["目标保存应写入版本化债券主数据"], ["票息日程和到期状态"], "债券、发行人关系和审计必须同事务提交；失败不得留下半成品目录项。"),
            [evidence(shot("b10-bond-editor.png"), "债券资料编辑器。"), evidence(shot("b10-bond-editor-required-validation.png"), "债券名称必填校验。")],
            "已动态确认债券资料字段、固定面值提示和名称必填校验。",
            ["真实新增、修改和删除", "债券类型完整候选和代码唯一性", "日期、付息、发行人和免税规则"],
        ),
        record(
            "RT-10-002",
            "TMARKETDEBTSTATISTICFRAME",
            "债券账户工作区 -> 上半区持仓统计",
            [
                state("空持仓", "observed", "列为债券代码名称、数量、投资金额、面值、年利率、年限和到期日。", workspace),
                state("页脚", "observed", "总实现盈亏、可用资金、总市值和总计在零余额账户中均为 0.00。", workspace),
                state("有数据估值", "pending", "当前临时账户没有债券持仓，未校准价格和收益公式。"),
            ],
            [command("当前持仓债券", "范围菜单默认状态", "支持切换到所有交易过的债券。"), command("双击持仓", "空账户无行", "有数据时的详情入口待验证。", "pending")],
            flow(["账户、债券范围和估值引用"], ["债券交易、持仓成本、行情、票息和汇率"], [], ["数量、投资金额、面值、年限、市值、占比和页脚"], "查询失败不得发布部分列表或混用不同估值批次。"),
            [evidence(workspace, "脱敏后的债券空持仓统计。")],
            "已动态确认债券持仓统计 Frame 的空状态、列和页脚。",
            ["有数据市值和占比", "年限、到期和票息状态", "缺行情、跨币种和并发快照"],
        ),
        record(
            "RT-10-003",
            "TMARKETDEBTTRANSFM",
            "账户中心 -> 临时债券账户",
            [
                state("组合宿主", "observed", "宿主组合持仓统计、交易明细、成本市值构成和历史盈亏。", workspace, COMPOSITION),
                state("顶部操作", "observed", "余额调整、持仓调整、查看账户资料、导出、打印和设为首页可见；空账户时导出和打印禁用。", shot("b10-bond-top-operation-menu.png")),
                state("临时账户清理", "observed", "完成页面覆盖后通过影响范围确认框删除临时账户。", shot("b10-delete-temp-bond-confirm.png")),
            ],
            [command("查看账户资料", "从顶部操作菜单进入", "打开账户概况及 TBondsViewFrame。"), command("删除账户", "返回账户中心并确认", "临时账户及其零余额上下文被移除。")],
            flow(["债券账户、页签和查询范围"], ["账户、债券、交易、持仓、行情和票息"], [], ["统一债券工作区"], "任一子查询失败不得发布互相不一致的持仓、交易、图表和页脚。"),
            [evidence(workspace, "债券工作区空状态。"), evidence(shot("b10-bond-top-operation-menu.png"), "债券工作区操作菜单。"), evidence(shot("b10-delete-temp-bond-confirm.png"), "临时债券账户删除确认。")],
            "已动态确认债券工作区宿主、子视图、命令状态和账户清理。",
            ["有数据工作区", "导出和打印", "余额/持仓调整及失败回滚"],
        ),
        record(
            "RT-10-004",
            "TMARKETDEBTTRANSFRAME",
            "债券工作区 -> 交易明细",
            [
                state("空列表", "observed", "空账户显示没有交易记录，流入、流出、差额和记录数均为零。", workspace),
                state("工具栏", "observed", "支持记账、单只债券范围、日期范围、查找和操作；无记录时查找禁用。", workspace),
                state("交易字段", "observed", "静态列确认净价、应计利息、数量、费用、交易金额、活动类型和余额。", STATIC_CATALOG),
            ],
            [command("记账", "展开工具栏菜单", "显示买入、卖出、到期、提前兑取、利息、转账和货币兑换。"), command("查找", "空账户状态", "无记录时禁用。", "disabled")],
            flow(["账户、债券范围、日期范围和搜索条件"], ["已提交债券交易、标签和余额投影"], [], ["交易行、流入流出、差额和记录数"], "修改或删除必须调用领域命令重建持仓、应计、资金和收益。"),
            [evidence(workspace, "脱敏后的债券交易明细空状态。"), evidence(shot("b10-bond-bookkeeping-menu.png"), "债券记账命令集合。")],
            "已动态确认债券交易 Frame 的空状态、工具栏和命令集合。",
            ["有数据列、排序和余额", "行级修改删除", "附件、导出、打印和大数据量"],
        ),
        record(
            "RT-10-005",
            "TNEWACCTWIZARDNMARKETDEBTDLGFM",
            "账户中心 -> 新增账户 -> 债券",
            [
                state("第一页", "observed", "账户名称、币种、所有者、备注和账户组均已显示。", shot("b10-bond-account-wizard-page1.png")),
                state("第二页", "observed", "日期、余额及账户自身/其它账户资金来源均已显示。", shot("b10-bond-account-wizard-page2.png")),
                state("完成与删除", "observed", "以人民币、零余额和账户自身创建临时账户，取证后确认删除。", shot("b10-delete-temp-bond-confirm.png")),
            ],
            [command("下一步", "完成第一页", "进入余额和资金来源页。"), command("完成", "使用零余额自身资金", "创建临时债券账户。"), command("删除账户", "完成取证后确认", "临时账户被移除。")],
            flow(["账户资料、币种和账户组", "日期、余额和资金来源"], ["所有者、账户组和可选资金账户"], ["债券账户、初始余额事件和资金来源关系"], ["账户中心和债券导航投影"], "账户、初始资金、资金来源关系和审计必须同事务创建。"),
            [evidence(shot("b10-bond-account-wizard-page1.png"), "债券账户向导第一页。"), evidence(shot("b10-bond-account-wizard-page2.png"), "债券账户向导第二页。"), evidence(shot("b10-delete-temp-bond-confirm.png"), "临时账户清理确认。")],
            "已动态完成债券账户向导两页、零余额创建和删除闭环。",
            ["其它账户真实转入", "重名、非法币种和失败回滚", "有交易账户的删除限制"],
        ),
        record(
            "RT-10-006",
            "TNMARKETBONDBUYDLGFM",
            "债券工作区 -> 记账 -> 债券买入",
            [state("输入字段", "observed", "债券账户、资金账户、债券、净价、应计利息、数量、总费用、金额、标签、日期和备注均已显示。", shot("b10-bond-buy-dialog.png")), state("保存", "pending", "目录为空，本轮未提交买入。")],
            [command("债券买入", "从记账菜单选择", "打开买入表单。"), command("保存并继续/确定", "本轮未触发", "公式、保存和回滚待验证。", "pending")],
            flow(["账户、债券、净价、应计利息、数量、费用和日期"], ["债券面值、票息、账户资金和费率策略"], ["目标保存应生成买入事实、资金流出、持仓和成本批次"], ["全价、结算金额、资本成本和单位成本"], "买入事实、资金、持仓、应计和费用必须原子提交。"),
            [evidence(shot("b10-bond-buy-dialog.png"), "债券买入字段。")],
            "已动态确认债券买入入口及净价、应计利息、数量和费用边界。",
            ["全价和面值换算", "应计利息与成本口径", "真实保存、资金不足和失败回滚"],
        ),
        record(
            "RT-10-007",
            "TNMARKETBONDCASHAHEADDLGFM",
            "债券工作区 -> 记账 -> 债券提前兑取",
            [state("输入字段", "observed", "债券账户、资金账户、债券、净价、应计利息、数量、金额、标签、日期和备注均已显示，不含常规总费用。", shot("b10-bond-cash-ahead-dialog.png")), state("保存", "pending", "目录为空，本轮未提交提前兑取。")],
            [command("债券提前兑取", "从记账菜单选择", "打开提前兑取表单。"), command("保存并继续/确定", "本轮未触发", "部分兑取和回滚待验证。", "pending")],
            flow(["债券、净价、应计利息、数量和金额"], ["可用持仓、成本批次、兑取规则和资金账户"], ["目标保存应生成提前兑取终止事件、资金流入和持仓关闭"], ["兑取净额、已实现盈亏和剩余成本"], "提前兑取事件、资金、持仓、应计和收益必须原子提交。"),
            [evidence(shot("b10-bond-cash-ahead-dialog.png"), "债券提前兑取字段。")],
            "已动态确认提前兑取与正常卖出、正常到期不同的输入边界。",
            ["部分兑取", "罚息、费用和税费", "成本分配、真实保存和回滚"],
        ),
        record(
            "RT-10-008",
            "TNMARKETBONDINTERESTDLGFM",
            "债券工作区 -> 记账 -> 债券利息",
            [state("债券模式", "observed", "债券账户、资金账户、债券、金额、标签、日期和备注均已显示。", shot("b10-bond-interest-dialog.png")), state("复用边界", "observed", "既有运行证据确认该窗体还会在银行理财上下文动态替换为分红文案。", STATIC_CATALOG), state("保存", "pending", "本轮未提交票息。")],
            [command("债券利息", "从记账菜单选择", "打开债券利息表单。"), command("保存并继续/确定", "本轮未触发", "重复票息、税费和回滚待验证。", "pending")],
            flow(["债券、资金账户、利息金额和日期"], ["票息期间、免税状态和既有收益事件"], ["目标保存应生成票息收益和资金流入"], ["毛利息、税费和净利息"], "票息事实、税费、资金分录和审计必须原子提交。"),
            [evidence(shot("b10-bond-interest-dialog.png"), "债券利息字段。"), evidence(STATIC_CATALOG, "债券利息与银行理财分红的复用结构。", "manual_note")],
            "已动态确认债券利息模式及其与银行理财分红的复用边界。",
            ["真实票息保存", "重复期间、免税和税费", "银行理财分红模式再次校准"],
        ),
        record(
            "RT-10-009",
            "TNMARKETBONDLISTFM",
            "应用菜单 -> 资料管理 -> 债券",
            [
                state("空目录", "observed", "目录显示代码、名称、币种、发行日、到期日、两个付息日、年利率和面值。", shot("b10-bonds-list-sanitized.png")),
                state("命令状态", "observed", "空目录时修改和删除禁用，查找、导出和打印可见。", shot("b10-bonds-list-operation-menu.png")),
                state("新增入口", "observed", "点击新增债券打开 TEditNMarketBondFm。", shot("b10-bond-editor.png")),
            ],
            [command("新增债券", "点击目录顶部按钮", "打开债券资料编辑器。"), command("修改/删除债券", "空目录状态", "没有选中行时禁用。", "disabled"), command("查找/导出/打印", "展开操作菜单", "命令可见，输出待验证。", "pending")],
            flow(["搜索条件和目录命令"], ["债券目录、发行人和引用状态"], ["目标维护命令应写入版本化债券主数据"], ["交易候选和资料列表"], "被引用债券不得物理删除；目录变更和审计必须一致。"),
            [evidence(shot("b10-bonds-list-sanitized.png"), "脱敏后的债券空目录。"), evidence(shot("b10-bonds-list-operation-menu.png"), "债券目录操作菜单。"), evidence(shot("b10-bond-editor.png"), "新增债券入口结果。")],
            "已动态确认债券目录、列、搜索、新增和空目录命令状态。",
            ["有数据修改和删除", "引用限制和重复代码", "导出、打印、排序和大数据量"],
        ),
        record(
            "RT-10-010",
            "TNMARKETBONDMATUREDLGFM",
            "债券工作区 -> 记账 -> 债券到期",
            [state("输入字段", "observed", "债券账户、资金账户、债券、全价、数量、金额、标签、日期和备注均已显示。", shot("b10-bond-mature-dialog.png")), state("保存", "pending", "目录为空，本轮未提交到期。")],
            [command("债券到期", "从记账菜单选择", "打开正常到期表单。"), command("保存并继续/确定", "本轮未触发", "本金、末期利息和关闭规则待验证。", "pending")],
            flow(["债券、全价、数量、金额和日期"], ["到期日、可用持仓、成本批次和票息状态"], ["目标保存应生成到期事件、资金流入并关闭持仓"], ["本金回收、最后票息和已实现盈亏"], "到期、资金、持仓、成本和票息必须原子提交。"),
            [evidence(shot("b10-bond-mature-dialog.png"), "债券正常到期字段。")],
            "已动态确认正常到期使用全价而非净价加独立应计利息字段。",
            ["全价口径", "部分到期和末期票息", "真实保存、重复到期和回滚"],
        ),
        record(
            "RT-10-011",
            "TNMARKETBONDSELLDLGFM",
            "债券工作区 -> 记账 -> 债券卖出",
            [state("输入字段", "observed", "债券账户、资金账户、债券、净价、应计利息、数量、总费用、金额、标签、日期和备注均已显示。", shot("b10-bond-sell-dialog.png")), state("保存", "pending", "目录为空，本轮未提交卖出。")],
            [command("债券卖出", "从记账菜单选择", "打开卖出表单。"), command("保存并继续/确定", "本轮未触发", "持仓不足和成本分配待验证。", "pending")],
            flow(["债券、净价、应计利息、数量、费用和日期"], ["可用持仓、成本批次、行情和资金账户"], ["目标保存应生成卖出事实、资金流入和持仓关闭"], ["全价、卖出净收入、已实现盈亏和剩余成本"], "卖出事实、资金、持仓、应计、费用和收益必须原子提交。"),
            [evidence(shot("b10-bond-sell-dialog.png"), "债券卖出字段。")],
            "已动态确认债券卖出与买入对称的净价、应计利息和费用边界。",
            ["持仓不足和部分卖出", "成本分配和应计归因", "真实保存、费用舍入和回滚"],
        ),
        record(
            "RT-10-012",
            "TNMARKETDEBTACCTDLGFM",
            "账户中心 -> 临时债券账户 -> 修改账户",
            [state("账户字段", "observed", "账户名称、币种、所有者、备注、创建日期、开户机构、账号、默认资金账户和附件均已显示。", shot("b10-bond-account-editor-sanitized.png")), state("币种锁定", "observed", "临时账户创建后币种控件禁用。", shot("b10-bond-account-editor-sanitized.png")), state("保存", "pending", "本轮关闭编辑器，账户最终通过列表命令删除。")],
            [command("修改账户", "从账户行操作菜单选择", "打开 TNMarketDebtAcctDlgFm。"), command("确定", "本轮未触发", "修改校验和审计待验证。", "pending")],
            flow(["账户资料、机构、账号和默认资金账户"], ["当前账户、交易和资金账户引用"], ["目标保存应更新债券账户聚合"], ["账户概况和交易默认值"], "账户更新和默认资金关系必须原子提交；已有交易时禁止静默变更币种。"),
            [evidence(shot("b10-bond-account-editor-sanitized.png"), "脱敏后的债券账户编辑器。"), evidence(shot("b10-bond-account-row-menu.png"), "债券账户行操作菜单。")],
            "已动态确认债券账户编辑字段、币种锁定和账户级操作。",
            ["真实修改保存", "默认资金账户失效", "已有交易时的币种、注销和删除限制"],
        ),
        record(
            "RT-10-013",
            "TSTOCKBONDMATUREDLGFM",
            "上市证券债券上下文 -> 债券到期",
            [state("上市证券模式", "observed", "既有动态证据显示证券账户、资金账户、债券、全价、数量、金额、日期、标签和备注。", "artifacts/runtime-validation/security-bond-maturity-dialog.png"), state("与纯债券账户边界", "observed", "该窗体由上市证券上下文进入，不能与 TNMarketBondMatureDlgFm 静默合并账户前置条件。", CONTRACT), state("真实保存", "pending", "本轮没有上市证券债券持仓可用于提交到期。")],
            [command("债券到期", "从上市证券交易上下文进入", "打开 TStockBondMatureDlgFm。"), command("保存并继续/确定", "本轮未触发", "证券账户到期结转待验证。", "pending")],
            flow(["证券账户、债券、全价、数量和日期"], ["证券账户持仓、成本批次和资金账户"], ["目标保存应生成证券账户来源的到期事件"], ["本金、票息、成本关闭和实现盈亏"], "证券账户到期必须与资金、持仓、成本和收益原子提交，并保留来源上下文。"),
            [evidence("artifacts/runtime-validation/security-bond-maturity-dialog.png", "上市证券上下文中的债券到期表单。")],
            "已确认上市证券债券到期表单及其与纯债券账户到期的来源边界。",
            ["真实证券债券到期", "与纯债券账户命令共享范围", "成本、票息和失败回滚"],
        ),
        record(
            "RT-10-014",
            "TBONDSMARKETCONSTITUTESFRAME",
            "债券工作区 -> 成本市值构成",
            [state("动态宿主", "observed", "由 TMarketDebtTransFm 的第二页签直接承载。", shot("b10-bond-cost-market-composition-sanitized.png"), COMPOSITION), state("空状态", "observed", "显示当前仓位 0.00%，左右两块图表均显示无数据显示。", shot("b10-bond-cost-market-composition-sanitized.png")), state("有数据构成", "pending", "没有债券持仓，成本和市值扇区未校准。")],
            [command("成本市值构成", "点击第二页签", "切换到债券成本和市值图表。")],
            flow(["账户和估值引用"], ["持仓成本、债券行情、应计和汇率"], [], ["当前仓位、成本构成和市值构成"], "图表、持仓和页脚必须使用同一估值引用；失败时显示明确错误而非旧新数据混合。"),
            [evidence(shot("b10-bond-cost-market-composition-sanitized.png"), "脱敏后的债券成本市值构成空状态。"), evidence(COMPOSITION, "Frame 直接组合关系。", "manual_note")],
            "已动态确认债券成本市值构成 Frame 的宿主和空状态。",
            ["有数据扇区和总额", "缺行情、跨币种和过期价格", "图表导出、刷新和并发快照"],
        ),
        record(
            "RT-10-015",
            "TBONDSVIEWFRAME",
            "债券工作区 -> 操作 -> 查看账户资料",
            [state("动态宿主", "observed", "TAccountOverviewDlgFm 动态承载 TBondsViewFrame。", shot("b10-bond-account-overview-sanitized.png"), COMPOSITION), state("概况字段", "observed", "显示账户名称、类型、币种、所有者、资金来源、备注、机构、账号、联系方式、账户组、标签和附件。", shot("b10-bond-account-overview-sanitized.png")), state("编辑入口", "observed", "页面提供修改账户概况链接。", shot("b10-bond-account-overview-sanitized.png"))],
            [command("查看账户资料", "从债券工作区操作菜单进入", "打开账户概况。"), command("修改账户概况", "概况链接可见", "进入 TNMarketDebtAcctDlgFm。")],
            flow(["债券账户 ID"], ["账户聚合、分组、标签、附件和机构资料"], [], ["只读债券账户概况"], "概况查询只读；敏感联系方式和附件按权限加载，不能进入普通日志。"),
            [evidence(shot("b10-bond-account-overview-sanitized.png"), "脱敏后的债券账户概况。"), evidence(COMPOSITION, "TBondsViewFrame 的直接宿主证据。", "manual_note")],
            "已动态确认 TBondsViewFrame 的账户概况宿主、字段和编辑入口。",
            ["附件增删和敏感字段权限", "关闭、隐藏和异常账户", "概况修改后的并发刷新"],
        ),
    ]


def main() -> None:
    """写出 B10 全部十五条最新记录。"""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    items = sorted(records(), key=lambda item: item["execution_id"])
    if len(items) != 15:
        raise RuntimeError(f"B10 记录数量错误：{len(items)}")
    for item in items:
        path = OUTPUT / f"{item['execution_id']}-{STAMP}.json"
        path.write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"B10 观察记录生成完成：{len(items)} 条")


if __name__ == "__main__":
    main()
