"""生成 B20 共享 UI 与技术支撑组件的代表性运行记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T03:34:54+08:00"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "EE62C77052FA558F26A6ABF1439844CC3DB62EFC0375A124339F6222633ACB9D"
FINAL_HASH = "67760084CD376DAAC0B400A3917F72CBCE98398C484143B11E9A4BAFDBF1812A"
BACKUP_ARTIFACT = "artifacts/runtime-validation/backups/test-before-b20.mh8"
NOTES = "artifacts/runtime-validation/B20-shared-infrastructure-notes.md"
CONTRACT = "docs/runtime-shared-ui-contract.md"


def screenshot(name: str) -> str:
    """返回运行截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(kind: str, path: str, description: str) -> dict:
    """构造一条可追溯证据。"""

    return {"kind": kind, "path": path, "description": description}


def flow(
    inputs: list[str],
    reads: list[str],
    writes: list[str],
    results: list[str],
    effects: list[str],
    rollback: str,
) -> dict:
    """统一生成共享组件的数据流结构。"""

    return {
        "inputs": inputs,
        "reads": reads,
        "writes": writes,
        "derived_results": results,
        "side_effects": effects,
        "rollback": rollback,
    }


COMMON_REQUIREMENTS = [
    "共享组件只维护宿主草稿或显示状态，不得直接访问 SQLite 或提交领域事务。",
    "组件取消、关闭和校验失败必须保留宿主最后一次有效业务状态。",
    "旧窗体名仅作为追溯标识，Rust 版按职责合并，不建立同名独立页面。",
]


SPECS = {
    "RT-20-001": {
        "resource": "TAMOUNTSCREENINGFRAME",
        "entry": "财务记录 -> 查找 -> 筛选 -> 金额条件",
        "steps": ["打开财务记录", "选择筛选", "观察金额条件默认值和输入门控", "关闭筛选"],
        "states": [("金额筛选宿主", "金额条件嵌入完整筛选窗体；默认不筛选金额，支持大于等于、小于等于和闭区间。", [screenshot("b20-filter-host.png")])],
        "commands": [("rbNoAmount", "不筛选金额", True, "默认选中", "金额输入禁用。", "pass"), ("amountModes", "金额比较模式", True, "未提交筛选", "模式切换控制对应金额输入。", "partial")],
        "data_flow": flow(["金额比较模式", "一个或两个金额边界"], ["宿主筛选草稿"], ["只回填宿主筛选条件"], ["规范化金额谓词"], ["关闭窗体未改变业务数据"], "取消时丢弃未应用的金额条件。"),
        "evidence": [evidence("screenshot", screenshot("b20-filter-host.png"), "财务记录完整筛选窗体中的金额条件。")],
        "requirements": ["金额边界使用十进制定点类型，并验证区间下限不大于上限。"],
        "summary": "已确认金额筛选是宿主筛选窗体中的共享组件。",
        "gaps": ["三种金额模式的真实查询结果和边界包含规则"],
    },
    "RT-20-002": {
        "resource": "TCHILDFORM",
        "entry": "多个主工作区的通用子窗体外壳",
        "states": [("子窗体宿主", "财务记录和账户中心均装配在主内容区，标题、帮助、关闭和窗口状态由宿主统一管理。", [screenshot("b20-financial-record-host.png")])],
        "commands": [("close/help", "关闭与帮助", True, "通过代表宿主观察", "由具体页面决定是否显示和启用。", "partial")],
        "summary": "子窗体是窗口生命周期基类，不是独立产品页面。",
        "gaps": ["各派生窗体关闭前未保存提示的一致性"],
    },
    "RT-20-003": {
        "resource": "TDIALOGFORM",
        "entry": "筛选、自定义日期等模态窗体的通用外壳",
        "states": [("模态外壳", "筛选与自定义日期均使用统一标题栏、关闭按钮和客户区结构。", [screenshot("b20-filter-host.png"), screenshot("b20-custom-date-range.png")])],
        "commands": [("close", "关闭", True, "标题栏关闭", "不提交筛选或日期草稿。", "pass")],
        "summary": "模态对话框外壳已由两个真实宿主代表验证。",
        "gaps": ["Esc、Enter、帮助键和窗口缩放的全局一致性"],
    },
    "RT-20-004": {
        "resource": "TDROPDOWNDATE",
        "entry": "日期输入框的日历下拉组件",
        "states": [("日期下拉宿主", "自定义日期窗体的两个 TMHDatetimePicker 提供日历按钮，选择结果只回填起止日期草稿。", [screenshot("b20-custom-date-range.png")])],
        "commands": [("calendarChange", "选择日期", True, "本轮未改变默认日期", "保持原日期范围。", "partial")],
        "summary": "日期下拉是输入组件，不进入导航。",
        "gaps": ["键盘导航、月份切换、最小最大日期和弹层定位"],
    },
    "RT-20-005": {
        "resource": "TDROPFM",
        "entry": "账户、分类、标签和树形选择控件的通用下拉宿主",
        "states": [("树形下拉", "财务筛选中的资产、活动类型和标签选择均以宿主下拉控件呈现；技术窗体负责选择、键盘和失焦关闭。", [screenshot("b20-filter-host.png")])],
        "commands": [("treeSelection", "选择树节点", True, "未改变筛选条件", "选择结果由宿主接收。", "partial")],
        "summary": "通用树形下拉应合并为可复用选择弹层。",
        "gaps": ["多选、搜索、失焦关闭和层级展开行为"],
    },
    "RT-20-006": {
        "resource": "TFMCUSTOMDIALOG",
        "entry": "旧网格 Custom AutoFilter 内部对话框",
        "reachable": False,
        "unreachable_reason": "当前 MoneyHome8 工作流未发现独立入口；静态资源仅表明 And/Or、OK、Cancel 条件组合能力。",
        "states": [("静态条件组合", "旧网格自动筛选支持 And/Or 两条件组合，不构成独立业务模块。", [CONTRACT])],
        "commands": [("okCancel", "OK / Cancel", True, "未动态触发", "保留为可选数据网格能力。", "partial")],
        "summary": "旧网格自动筛选对话框没有独立产品入口。",
        "gaps": ["哪些列表实际启用双条件自动筛选"],
    },
    "RT-20-007": {
        "resource": "TMHFRAME",
        "entry": "业务工作区和嵌入视图的基础 Frame",
        "states": [("工作区基类", "财务记录列表、账户中心和报表均以主内容区内嵌工作区呈现。", [screenshot("b20-financial-record-host.png"), screenshot("b16-income-expense-statistics-result.png")])],
        "commands": [],
        "summary": "基础 Frame 只提供生命周期和宿主绑定。",
        "gaps": ["派生工作区激活、刷新和销毁时序"],
    },
    "RT-20-008": {
        "resource": "TMISCDIALOGFM",
        "entry": "轻量提示和辅助对话框基类",
        "reachable": False,
        "unreachable_reason": "无独立标题和产品入口，只能由派生对话框间接覆盖。",
        "states": [("派生外壳", "静态证据显示该类只承担通用对话框行为，Rust 版不保留同名窗体。", [CONTRACT])],
        "commands": [],
        "summary": "轻量对话框基类按技术外壳处理。",
        "gaps": ["全部派生类清单和关闭语义"],
    },
    "RT-20-009": {
        "resource": "TMWADJUSTBUTTONDROP",
        "entry": "财务记录日期范围按钮",
        "states": [("日期范围菜单", "菜单提供日、周、月、季、年、最近 7 天/1 月/3 月/6 月/1 年和自定义。", [screenshot("b20-date-range-menu.png")])],
        "commands": [("yearMonthConfirm", "日期范围选择", True, "打开自定义日期", "进入 TSelectDateRangeDlgFm。", "pass")],
        "summary": "日期调整下拉负责预设区间和自定义入口。",
        "gaps": ["周、季、年边界与本地化周起始日"],
    },
    "RT-20-010": {
        "resource": "TNODEWRAPFORM",
        "entry": "概况和财务计算器等本地 Web 内容的隐藏宿主",
        "states": [("WebView 宿主", "目标进程中存在 TNodeForm/NODEWRAP 和 wkeWebWindow；窗口由主内容区装配而非独立导航。", [screenshot("b20-main-baseline.png")])],
        "commands": [],
        "summary": "Node/WebView 包装层是可替换技术适配器。",
        "gaps": ["页面资源加载失败、导航限制、脚本桥权限和进程隔离"],
    },
    "RT-20-011": {
        "resource": "TOKCANCELDIALOGFM",
        "entry": "带确定/取消的标准模态窗体基类",
        "states": [("确定/取消外壳", "筛选和自定义日期均使用底部确认区；标题栏关闭不应用草稿。", [screenshot("b20-filter-host.png"), screenshot("b20-custom-date-range.png")])],
        "commands": [("ok", "确定", True, "本轮未提交", "留在宿主草稿边界。", "partial"), ("cancel", "取消/关闭", True, "标题栏关闭", "未改变筛选结果。", "pass")],
        "summary": "标准确认对话框按共享模态组件实现。",
        "gaps": ["Enter/Esc 默认按钮和脏草稿提示"],
    },
    "RT-20-012": {
        "resource": "TPAGECONTRLFM",
        "entry": "报表、行情和账户工作区的页签外壳",
        "states": [("页签工作区", "报表筛选、行情和账户详情均使用页签切换同一业务上下文。", [screenshot("b16-report-filter-dialog.png"), screenshot("b18-online-quote-update.png")])],
        "commands": [("tabChange", "切换页签", True, "由既有宿主代表验证", "切换显示投影，不直接写业务数据。", "partial")],
        "summary": "页签外壳应由统一工作区组件承接。",
        "gaps": ["懒加载、脏草稿切换和页签状态恢复"],
    },
    "RT-20-013": {
        "resource": "TPROGRESSFORM",
        "entry": "在线行情更新等长任务",
        "states": [("运行中", "在线行情更新显示当前任务进度，并提供中止路径；静态资源文案为正在处理数据。", [screenshot("b18-online-quote-update-running.png")])],
        "commands": [("btnCancel", "取消", True, "B18 已执行股票更新中止", "任务停止且未观察到账簿写入。", "pass")],
        "summary": "长任务需要统一进度、取消和结果状态。",
        "gaps": ["不可取消阶段、后台错误、重试和应用退出协商"],
    },
    "RT-20-014": {
        "resource": "TRZFRMCUSTOMIZETOOLBAR",
        "entry": "第三方工具栏库内部定制器",
        "reachable": False,
        "unreachable_reason": "资源无已知 MoneyHome8 用户入口，也没有确认业务配置持久化；属于第三方 UI 库内部能力。",
        "states": [("技术排除", "静态资源包含添加间隔、上移下移、文本选项和关闭，但未发现产品入口。", [CONTRACT])],
        "commands": [("customize", "工具栏定制", False, "未触发", "不纳入首版产品功能。", "partial")],
        "summary": "工具栏库定制器标记为技术排除，不复制第三方内部窗体。",
        "gaps": ["是否存在隐藏配置入口或历史用户布局数据"],
    },
    "RT-20-015": {
        "resource": "TSELECTDATERANGEDLGFM",
        "entry": "财务记录日期范围 -> 自定义",
        "steps": ["打开日期范围菜单", "选择自定义", "观察起止日期", "关闭取消"],
        "states": [("自定义日期", "默认起止为 2026-06-30 到 2026-07-30；静态页签覆盖日、月、季、年。", [screenshot("b20-custom-date-range.png")])],
        "commands": [("btnOk", "确定", True, "未提交", "保持原最近 1 月筛选。", "partial")],
        "data_flow": flow(["日期粒度", "起止日期"], ["宿主当前日期范围"], ["只回填宿主查询条件"], ["规范化闭区间"], ["关闭未执行查询"], "取消保留原日期范围；非法区间不得覆盖宿主条件。"),
        "evidence": [evidence("screenshot", screenshot("b20-custom-date-range.png"), "自定义日期对话框。"), evidence("screenshot", screenshot("b20-date-range-menu.png"), "日期范围预设菜单。")],
        "requirements": ["日期区间必须定义时区、闭开边界和日/月/季/年归一化规则。"],
        "summary": "已动态到达自定义日期并确认起止日期输入。",
        "gaps": ["月、季、年页签的具体控件和非法区间校验"],
    },
    "RT-20-016": {
        "resource": "TSTATISTICFRAME",
        "entry": "报表中心和概况统计宿主",
        "states": [("统计工作区", "报表结果提供查询范围、导出、打印和统计视图；投资报表树可切换多种统计结果。", [screenshot("b16-income-expense-statistics-result.png"), screenshot("b16-investment-overview-result.png")])],
        "commands": [("operate/export/print", "操作、导出、打印", True, "B16 代表报表已查询", "命令依赖当前统计快照。", "partial")],
        "summary": "统计 Frame 是报表工作区抽象，不是单一报表。",
        "gaps": ["设置主页、余额/持仓调整入口和各派生统计公式"],
    },
    "RT-20-017": {
        "resource": "TSTATISTICGRIDFRAME",
        "entry": "报表中心表格结果区域",
        "states": [("统计表格", "收入支出统计等报表以可选择表格展示分组和金额结果。", [screenshot("b16-income-expense-statistics-result.png")])],
        "commands": [("selection", "选择统计行", True, "代表报表可见", "选择驱动明细或图表联动。", "partial")],
        "summary": "统计表格应实现统一列、选择和导出快照协议。",
        "gaps": ["排序、汇总、复制、列定制和大数据分页"],
    },
    "RT-20-018": {
        "resource": "TSTATISTICTREEFRMAE",
        "entry": "报表中心左侧报表树",
        "states": [("统计树", "投资报表树支持层级展开，切换后右侧加载对应统计工作区。", [screenshot("b16-investment-tree-expanded.png")])],
        "commands": [("expandAll", "全部展开", True, "代表树已展开", "展示全部层级。", "pass"), ("collapseAll", "全部折叠", True, "未单独触发", "静态命令已确认。", "partial")],
        "summary": "统计树是报表导航组件。",
        "gaps": ["折叠状态持久化、键盘导航和大量节点性能"],
    },
    "RT-20-019": {
        "resource": "TVIEWFRAME",
        "entry": "账户概况和领域详情的基础视图",
        "states": [("详情投影", "账户中心及多个账户概况页使用主信息、附加信息和属性网格展示领域投影。", [screenshot("b19-account-center-credit-probe.png")])],
        "commands": [],
        "summary": "ViewFrame 应收敛为只读详情投影，不保留 Delphi 基类层次。",
        "gaps": ["密码字段遮罩、所有者绘制单元格和字段级权限"],
    },
}


def build_record(execution_id: str, spec: dict) -> dict:
    """把紧凑规格转换为统一运行记录。"""

    states = [
        {"name": name, "status": "observed", "observations": observations, "evidence_paths": paths}
        for name, observations, paths in spec["states"]
    ]
    commands = [
        {
            "component": component,
            "label": label,
            "initial_state": {"enabled": enabled, "visible": True},
            "trigger": trigger,
            "confirmation": None,
            "outcome": outcome,
            "status": status,
        }
        for component, label, enabled, trigger, outcome, status in spec.get("commands", [])
    ]
    default_flow = flow(
        ["宿主状态和用户交互"],
        ["宿主提供的只读模型或草稿"],
        ["仅更新宿主 UI 状态"],
        ["选择、显示或窗口状态"],
        ["不直接写入账簿业务数据"],
        "关闭或取消时释放组件状态，不提交领域副作用。",
    )
    default_evidence = [
        evidence("manual_note", NOTES, "B20 共享组件动态与静态对照。"),
        evidence("manual_note", CONTRACT, "旧组件到 Rust 共享抽象的收敛合同。"),
    ]
    return {
        "schema_version": 1,
        "execution_id": execution_id,
        "resource": spec["resource"],
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
            "entry_point": spec["entry"],
            "steps": spec.get("steps", ["从代表性宿主观察组件", "核对静态命令和事件", "关闭宿主"]),
            "reachable": spec.get("reachable", True),
            "unreachable_reason": spec.get("unreachable_reason"),
        },
        "states": states,
        "commands": commands,
        "data_flow": spec.get("data_flow", default_flow),
        "evidence": spec.get("evidence", default_evidence),
        "requirements_update": COMMON_REQUIREMENTS + spec.get("requirements", []),
        "result": {
            "status": "partial",
            "summary": spec["summary"],
            "remaining_gaps": spec["gaps"],
        },
    }


def main() -> None:
    """写出 19 条 B20 代表性运行记录。"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for execution_id, spec in SPECS.items():
        output_path = OUTPUT_DIR / f"{execution_id}-20260730T033454+0800.json"
        output_path.write_text(
            json.dumps(build_record(execution_id, spec), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"generated {len(SPECS)} B20 records")


if __name__ == "__main__":
    main()
