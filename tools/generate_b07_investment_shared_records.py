"""生成 B07 投资公共能力的结构化动态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T08:20:55+08:00"
STAMP = "20260730T082055+0800"
LEDGER = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
SHA_BEFORE = "8E57AC3FC7B8F43CDBA50382117622B52E5664F9E5EE68C57CA3E979C180FB10"
SHA_AFTER = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
BACKUP = "artifacts/runtime-validation/backups/test-before-b07-investment-shared-20260730.mh8"

COMMON_REQUIREMENTS = [
    "投资交易、持仓批次和调整事件属于事实层，列表、图表和盈亏属于可重建投影层。",
    "列表、汇总、构成图和报表必须绑定同一账簿版本、估值时间、行情批次和汇率批次。",
    "共享编辑器必须接收显式产品域与事件类型，不能从窗体标题、菜单层级或金额正负推断。",
    "未通过真实交易样例校准前，不得把成本分配、实现盈亏、收益率或旧格式标记为已兼容。",
]


def evidence(path: str, description: str, kind: str = "screenshot") -> dict:
    """创建证据条目，路径统一保持为工作区相对路径。"""
    return {"kind": kind, "path": path, "description": description}


def state(name: str, status: str, observations: str, paths: list[str] | None = None) -> dict:
    """创建页面状态条目，仅在确有文件证据时附加路径。"""
    result = {"name": name, "status": status, "observations": observations}
    if paths:
        result["evidence_paths"] = paths
    return result


def command(component: str, label: str, trigger: str, outcome: str, status: str = "pass") -> dict:
    """创建命令观察，默认只表示入口和可见结果已经确认。"""
    return {
        "component": component,
        "label": label,
        "initial_state": {"enabled": True, "visible": True},
        "trigger": trigger,
        "confirmation": None,
        "outcome": outcome,
        "status": status,
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
    remaining_gaps: list[str],
    requirements: list[str] | None = None,
) -> dict:
    """组装符合运行观察 Schema 的单个 B07 记录。"""
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
            "sha256_before": SHA_BEFORE,
            "sha256_after": SHA_AFTER,
            "backup_artifact": BACKUP,
        },
        "navigation": {
            "entry_point": entry_point,
            "steps": [
                "打开所属投资页面或最终宿主",
                "观察字段、模式、列表、汇总和空状态",
                "只执行查询、页签或图表模式切换，不提交业务写入",
                "退出专用进程并核对账簿哈希、文件占用和原有进程",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": states,
        "commands": commands,
        "data_flow": data_flow,
        "evidence": [
            evidence(
                "artifacts/runtime-validation/B07-investment-shared-notes.md",
                "B07 动态时间线、金额核对、进程隔离和账簿指纹。",
                "manual_note",
            ),
            evidence(
                "docs/runtime-investment-shared-projections-contract.md",
                "Rust 持仓、估值、构成图、历史盈亏和共享现金事件合同。",
                "manual_note",
            ),
            *evidence_items,
        ],
        "requirements_update": COMMON_REQUIREMENTS + (requirements or []),
        "result": {"status": "partial", "summary": summary, "remaining_gaps": remaining_gaps},
    }


def records() -> list[dict]:
    """返回 B07 六个资源的最新部分观察记录。"""
    return [
        record(
            "RT-07-001",
            "TADJUSTHELDDLGFM",
            "记账 -> 更多交易活动 -> 调整 -> 持仓调整",
            [
                state("初始字段", "observed", "账户/资产、持有产品、持仓总成本、持仓数量、标签、日期和备注可见。", ["artifacts/runtime-validation/holdings-adjustment-dialog.png"]),
                state("保存与并发", "pending", "真实保存、数量与成本差额、持仓版本冲突和失败回滚仍待验证。"),
            ],
            [
                command("调整子菜单", "持仓调整", "选择持仓调整", "打开 TAdjustHeldDlgFm。"),
                command("底部操作区", "保存并继续、确定", "本轮未提交", "命令可见，真实保存待验证。", "pending"),
            ],
            {
                "inputs": ["账户或资产", "持有产品", "调整后总成本和数量", "标签、日期和备注"],
                "reads": ["当前持仓数量、成本基础和持仓版本"],
                "writes": ["目标保存应新增持仓调整事件、成本变化和审计记录"],
                "derived_results": ["数量差额", "成本差额", "重建后的持仓与估值"],
                "side_effects": ["本轮未提交；保存后应刷新投资投影"],
                "rollback": "调整事件、成本批次影响和投影刷新必须原子提交，禁止直接覆盖汇总。",
            },
            [evidence("artifacts/runtime-validation/holdings-adjustment-dialog.png", "持仓调整字段。")],
            "已确认持仓调整入口、字段和取消边界。",
            ["真实保存和持仓刷新", "数量与成本差额规则", "并发冲突和失败回滚"],
        ),
        record(
            "RT-07-002",
            "THISTORYPROFITFRAME",
            "贵金属/贵金属 TD/期货/融资融券等工作区 -> 历史盈亏",
            [
                state("空状态与列", "observed", "列为交易日期、名称、活动类型、价格、数量、交易金额、实现盈亏和盈亏比例。", ["artifacts/runtime-validation/b11-gold-profit-tab.png", "artifacts/runtime-validation/b11-td-profit-tab.png"]),
                state("筛选与汇总", "observed", "支持盈亏范围筛选，并显示盈利合计、亏损合计和总盈亏。", ["artifacts/runtime-validation/b11-td-profit-tab.png"]),
                state("有数据与输出", "pending", "真实关闭交易、成本分配、排序、钻取、导出和打印仍待验证。"),
            ],
            [
                command("历史盈亏工具栏", "盈亏范围", "切换历史盈亏页签", "显示范围筛选、列表和三项汇总。"),
                {"component": "操作菜单", "label": "导出、打印", "initial_state": {"enabled": False, "visible": True}, "trigger": "空账户下展开操作菜单", "confirmation": None, "outcome": "导出和打印保持禁用。", "status": "pass"},
            ],
            {
                "inputs": ["账户", "产品范围", "日期范围", "盈亏范围和排序"],
                "reads": ["关闭交易、成本批次分配、费用、现金流和产品资料"],
                "writes": [],
                "derived_results": ["实现盈亏行", "盈亏比例", "盈利合计", "亏损合计", "总盈亏"],
                "side_effects": ["查询、筛选和页签切换不应修改业务数据"],
                "rollback": "查询失败保留筛选与最后成功结果；列表、汇总和输出使用同一查询快照。",
            },
            [
                evidence("artifacts/runtime-validation/b11-gold-profit-tab.png", "贵金属宿主中的历史盈亏空状态。"),
                evidence("artifacts/runtime-validation/b11-td-profit-tab.png", "TD 宿主中的历史盈亏列、筛选和汇总。"),
                evidence("artifacts/runtime-validation/b11-td-bottom-operation-menu.png", "空状态导出和打印命令。"),
            ],
            "已确认历史盈亏 Frame 的真实宿主、列、筛选、汇总和空状态命令。",
            ["真实卖出、赎回和平仓样例", "成本与费用分配公式", "有数据导出、打印和钻取"],
        ),
        record(
            "RT-07-003",
            "TINVESTFEEDLGFM",
            "投资域记账菜单 -> 其它费用/利息收入",
            [
                state("其它费用模式", "observed", "标题为其它投资费用；资金账户和日期必填，币种由账户确定。", ["artifacts/runtime-validation/foreign-exchange-other-expense-dialog.png"]),
                state("利息收入模式", "observed", "同一字段结构切换为资金利息收入，业务方向由入口命令决定。", ["artifacts/runtime-validation/foreign-exchange-interest-income-dialog.png"]),
                state("保存与折算", "pending", "真实资金分录、外币折算、收益统计和失败回滚仍待验证。"),
            ],
            [
                command("投资域菜单", "其它费用", "选择其它费用", "以费用模式打开共享窗体。"),
                command("投资域菜单", "利息收入", "选择利息收入", "以收入模式打开共享窗体。"),
            ],
            {
                "inputs": ["事件类型", "产品域", "资金账户", "金额", "日期、标签和备注"],
                "reads": ["账户币种、有效汇率和投资上下文"],
                "writes": ["目标保存应生成明确方向的费用或利息事件及资金分录"],
                "derived_results": ["账户余额变化", "本位币折算额", "投资净收益"],
                "side_effects": ["本轮取消未写入；保存后刷新余额和收益投影"],
                "rollback": "现金事件、资金分录、分类和汇率快照必须同事务提交。",
            },
            [
                evidence("artifacts/runtime-validation/foreign-exchange-other-expense-dialog.png", "其它投资费用模式。"),
                evidence("artifacts/runtime-validation/foreign-exchange-interest-income-dialog.png", "资金利息收入模式。"),
            ],
            "已确认费用与利息共享编辑器的双模式和显式业务方向。",
            ["真实保存与资金分录", "外币折算和收益统计", "失败回滚"],
        ),
        record(
            "RT-07-004",
            "TINVESTMENTCHARTFRAME",
            "财务数据 -> 投资一览 -> 投资构成图",
            [
                state("按市值统计", "observed", "重大资产、上市证券、开放式基金和外汇的图例合计为 6,997,592.58，与页面当前市值完全一致。", ["artifacts/runtime-validation/screenshots/b07-investment-chart-live.png"]),
                state("按成本统计", "observed", "四类资产的图例合计为 4,778,184.00，与页面投入成本完全一致。", ["artifacts/runtime-validation/screenshots/b07-investment-chart-cost-live.png"]),
                state("空数据与多币种", "pending", "无持仓、缺行情、缺汇率和多币种边界仍待验证。"),
            ],
            [
                command("投资一览", "投资构成图", "点击投资构成图", "从持仓列表切换到环形构成图。"),
                command("构成图模式", "按市值统计/按成本统计", "选择两个模式", "只切换聚合指标，图例和底部合计保持同快照一致。"),
                command("投资一览", "持仓数据", "点击持仓数据", "返回账户分组持仓列表。"),
            ],
            {
                "inputs": ["构成指标：市值或成本"],
                "reads": ["同一估值快照中的投资账户、持仓成本、市值、资产类别、行情和汇率"],
                "writes": [],
                "derived_results": ["按资产类别聚合的成本或市值", "图例金额和占比", "底部总额"],
                "side_effects": ["图表模式切换为只读展示状态；未触发行情更新"],
                "rollback": "图表渲染失败应保留持仓列表和最后成功快照，不得发布部分聚合结果。",
            },
            [
                evidence("artifacts/runtime-validation/screenshots/b07-investment-chart-live.png", "按市值统计的投资构成图。"),
                evidence("artifacts/runtime-validation/screenshots/b07-investment-chart-cost-live.png", "按成本统计的投资构成图。"),
                evidence("artifacts/runtime-validation/screenshots/b07-investment-list-after-chart.png", "构成图返回持仓数据。"),
            ],
            "已动态确认投资构成图、成本/市值双模式及与页面合计的逐分一致性。",
            ["空持仓和缺失行情", "多币种折算", "行情更新期间的快照一致性"],
            ["构成图模式切换只能改变聚合指标，不能隐式刷新估值快照。"],
        ),
        record(
            "RT-07-005",
            "TINVESTMENTLISTFM",
            "财务数据左侧导航 -> 投资一览",
            [
                state("有数据", "observed", "按投资账户分组显示名称、数量、均价、成本、市值、浮动盈亏和涨幅。", ["artifacts/runtime-validation/screenshots/b07-investment-list-live3.png"]),
                state("合计公式", "observed", "投入成本 4,778,184.00，当前市值 6,997,592.58，浮动盈亏 2,219,408.58，三者精确相符。", ["artifacts/runtime-validation/screenshots/b07-investment-list-live3.png"]),
                state("行情与输出", "pending", "行情更新、操作菜单、空持仓、多币种估值和输出仍待完整验证。"),
            ],
            [
                command("左侧导航", "投资一览", "点击投资一览", "显示账户分组持仓和底部合计。"),
                command("页面命令区", "投资构成图", "点击后切换两种图表模式", "构成图金额与列表合计一致。"),
                command("页面命令区", "更新行情数据", "本轮未触发", "入口可用，网络和发布语义由 B18 证据补充。", "pending"),
            ],
            {
                "inputs": ["账簿投资账户和持仓", "估值时间、行情批次和汇率批次"],
                "reads": ["持仓数量、成本批次、当前价格、汇率和资产类别"],
                "writes": ["本轮只读导航和图表切换，没有提交业务写入"],
                "derived_results": ["投入成本 4,778,184.00", "当前市值 6,997,592.58", "浮动盈亏 2,219,408.58"],
                "side_effects": ["旧程序退出后账簿哈希变化，按会话或内部写回记录，不归因于交易保存"],
                "rollback": "查询失败应保留最后成功估值快照；行情更新只有整批校验通过后才能发布。",
            },
            [evidence("artifacts/runtime-validation/screenshots/b07-investment-list-live3.png", "当前投资一览与底部合计。")],
            "已验证投资一览有数据状态、账户分组、主要列、合计公式和构成图入口。",
            ["行情更新异常路径", "空持仓和多币种估值", "操作菜单、导出和打印"],
        ),
        record(
            "RT-07-006",
            "TMARKETCONSTITUTESFRAME",
            "上市证券/开放式基金/贵金属工作区 -> 市值构成和变动",
            [
                state("宿主组合", "observed", "Frame 嵌入上市证券、开放式基金和贵金属交易工作区，不作为独立页面。", ["artifacts/runtime-validation/b11-gold-market-value-tab.png"]),
                state("空状态与列", "observed", "显示名称、今日市值、昨日市值、涨跌额、涨跌幅、当前仓位及三项总额。", ["artifacts/runtime-validation/b11-gold-market-value-tab.png"]),
                state("有数据和日期口径", "pending", "真实持仓、当日交易、缺失昨日行情、跨币种和总额公式仍待验证。"),
            ],
            [command("下半区页签", "市值构成和变动", "点击页签", "显示共享市场构成 Frame。")],
            {
                "inputs": ["账户", "产品范围", "今日和昨日估值日期"],
                "reads": ["持仓、今日与昨日行情、汇率批次和资产类别"],
                "writes": [],
                "derived_results": ["今日市值", "昨日市值", "涨跌额", "涨跌幅", "当前仓位和总额"],
                "side_effects": ["页签切换和查询不应修改业务数据"],
                "rollback": "缺行情或查询失败时显示明确状态并保留最后成功快照，不得写回交易事实。",
            },
            [evidence("artifacts/runtime-validation/b11-gold-market-value-tab.png", "贵金属宿主中的市值构成和变动空状态。")],
            "已确认市场构成 Frame 的三个最终宿主、列、汇总和空状态。",
            ["有数据公式", "当日交易与价格变化拆分", "跨币种和缺失昨日行情"],
        ),
    ]


def main() -> None:
    """写出六条记录，文件名时间戳保持一致以便队列选择最新版本。"""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    generated = []
    for item in records():
        path = OUTPUT / f"{item['execution_id']}-{STAMP}.json"
        path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        generated.append(path.name)
    print(f"B07 观察记录生成完成：{len(generated)} 条")


if __name__ == "__main__":
    main()
