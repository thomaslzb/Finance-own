"""生成 RT-15-012 至 RT-15-027 财务规划子窗体的最新运行记录。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-08-03T02:57:46+08:00"
FILE_TIMESTAMP = "20260803T025746+0800"
BASELINE_HASH = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
COLD_HASH = "F1BA217B37FB904F979826CC6B56356082F8DA4CBF0B5FC178F5D97E8DF350CE"
BASELINE_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-011-financial-planning-before-20260803T0209+0800.mh8"
)
NOTE_PATH = "artifacts/runtime-validation/RT15-financial-planning-notes.md"
SCREENSHOT_ROOT = "artifacts/runtime-validation/screenshots"


def screenshot(name: str) -> str:
    """返回仓库内可移植的截图相对路径。"""

    return f"{SCREENSHOT_ROOT}/{name}"


FORM_SPECS: dict[str, dict[str, Any]] = {
    "RT-15-012": {
        "resource": "TFPANNUALSALARYINFODLGFM",
        "title": "工资",
        "screenshots": [
            screenshot("rt15-financial-planning-salary-dialog-20260803.png"),
            screenshot("rt15-financial-planning-salary-sample-20260803.png"),
            screenshot("rt15-financial-planning-salary-persisted-20260803.png"),
            screenshot("rt15-financial-planning-cold-reopen-20260803.png"),
        ],
        "summary": "已真实保存年工资 120000、结束年份 2075、年增长率 0%，并在冷启动后保持。",
        "inputs": ["年工资", "结束年份", "年增长率"],
        "reads": ["当前规划年度范围", "已保存工资输入"],
        "writes": ["工资规划输入：120000、2075、0%"],
        "derived": ["2026 至 2075 年每年 120000 的工资收入流", "年度余额图重算"],
        "mode": "saved",
        "requirements": [
            "工资输入必须保存年工资、结束年份和年增长率，并按规划年度展开收入流。",
            "零增长受控样例应在 2026 至 2075 年每年产生 120000 工资收入。",
        ],
        "gaps": ["非零增长率的生效年度和复利顺序", "结束年份边界、负值、极大值、舍入和失败回滚"],
    },
    "RT-15-013": {
        "resource": "TFPASSETEXPENSESINFODLGFM",
        "title": "资产带来的支出",
        "screenshots": [
            screenshot("rt15-financial-planning-current-asset-expense-dialog-20260803.png"),
            screenshot("rt15-financial-planning-asset-expense-dialog-20260803.png"),
        ],
        "summary": "已确认当前资产支出和资产购置后支出共用名称、来源资产、年支出、期间及增长率结构；本轮未保存样例。",
        "inputs": ["名称", "来源资产账户", "年支出", "开始年份", "持续年数", "结束年份", "年增长率"],
        "reads": ["规划中的资产账户候选", "当前规划年度范围"],
        "derived": ["按期间展开的资产相关年度支出"],
        "requirements": ["资产相关支出必须绑定稳定资产 ID，并保存金额、期间和增长假设。"],
        "gaps": ["真实保存与冷启动", "增长率、来源资产失效、跨币种、负值、舍入和失败回滚"],
    },
    "RT-15-014": {
        "resource": "TFPASSETGROWTHINFODLGFM",
        "title": "资产增长",
        "screenshots": [screenshot("rt15-financial-planning-asset-growth-dialog-20260803.png")],
        "summary": "已确认资产预计年增长率和年度现金盈余追加投资比例，旧版默认追加投资比例为 100.00%；本轮未改值保存。",
        "inputs": ["资产预计年增长率", "年度现金盈余追加投资比例"],
        "reads": ["规划内投资资产", "年度现金盈余"],
        "derived": ["年度投资资产增长", "年度现金盈余再投资金额"],
        "requirements": ["资产增长与现金盈余再投资必须分开建模，并记录各自生效年度和计算顺序。"],
        "gaps": ["增长与再投资的先后顺序", "负增长、比例边界、复利、舍入和失败回滚"],
    },
    "RT-15-015": {
        "resource": "TFPASSETINCOMEINFODLGFM",
        "title": "资产带来的收入",
        "screenshots": [
            screenshot("rt15-financial-planning-current-asset-income-dialog-20260803.png"),
            screenshot("rt15-financial-planning-asset-income-dialog-20260803.png"),
        ],
        "summary": "已确认当前资产收入和资产购置后收入共用名称、来源资产、年收入、期间及增长率结构；本轮未保存样例。",
        "inputs": ["名称", "来源资产账户", "年收入", "开始年份", "持续年数", "结束年份", "年增长率"],
        "reads": ["规划中的资产账户候选", "当前规划年度范围"],
        "derived": ["按期间展开的资产相关年度收入"],
        "requirements": ["资产相关收入必须绑定稳定资产 ID，并保存金额、期间和增长假设。"],
        "gaps": ["真实保存与冷启动", "增长率、来源资产失效、跨币种、负值、舍入和失败回滚"],
    },
    "RT-15-016": {
        "resource": "TFPASSETPURCHASEPLANINFOFM",
        "title": "资产购置",
        "screenshots": [
            screenshot("rt15-financial-planning-asset-purchase-dialog-20260803.png"),
            screenshot("rt15-financial-planning-asset-income-dialog-20260803.png"),
            screenshot("rt15-financial-planning-asset-expense-dialog-20260803.png"),
        ],
        "summary": "已确认购置名称、年度、金额、一次性/分期分支，以及首付、期数、年利率、月供和购置后收支页签；本轮未保存购置事件。",
        "inputs": ["购置名称", "购置年份", "购置金额", "付款方式", "首付", "期数（月）", "年利率", "月供", "购置后收入", "购置后支出"],
        "reads": ["规划年度范围", "购置后资产收支输入"],
        "derived": ["一次性购置现金流或分期付款现金流", "购置后年度收入和支出"],
        "requirements": ["资产购置必须原子保存付款方案及购置后收支，并生成可审计的逐年现金流。"],
        "gaps": ["真实保存与冷启动", "首付、月供、利息和期数公式", "购置后收支生效年度、舍入和失败回滚"],
    },
    "RT-15-017": {
        "resource": "TFPBASEDLGFM",
        "title": "财务规划基础对话框",
        "screenshots": [
            screenshot("rt15-financial-planning-family-dialog-20260803.png"),
            screenshot("rt15-financial-planning-salary-dialog-20260803.png"),
        ],
        "summary": "该资源是规划专题编辑器的公共基类，没有独立用户入口；确定与取消行为由家庭、工资和其它派生对话框覆盖。",
        "inputs": ["规划专题编辑器通用草稿"],
        "reads": ["派生对话框提供的字段和初始值"],
        "derived": ["派生对话框的统一确定、取消和关闭协议"],
        "mode": "base",
        "requirements": ["Rust 版应以共享对话框壳承载草稿隔离、确定提交、取消丢弃和错误聚焦，不暴露伪造的独立页面。"],
        "gaps": ["窗口关闭按钮、Escape、校验失败和并发冲突的统一协议"],
    },
    "RT-15-018": {
        "resource": "TFPBASEINFODLGFM",
        "title": "家庭资料",
        "screenshots": [
            screenshot("rt15-financial-planning-family-dialog-20260803.png"),
            screenshot("rt15-financial-planning-family-sample-20260803.png"),
            screenshot("rt15-financial-planning-family-spouse-branch-20260803.png"),
            screenshot("rt15-financial-planning-cold-reopen-family-20260803.png"),
        ],
        "summary": "已真实保存本人出生年份 1990 和预计寿命 85，派生身故年份 2075 与 2026~2075 规划区间；配偶字段分支已打开但未保存。",
        "inputs": ["本人出生年份", "本人预计寿命", "是否有配偶", "配偶出生年份", "配偶预计寿命"],
        "reads": ["系统当前年份", "已保存家庭资料"],
        "writes": ["本人家庭资料：1990、85、2075"],
        "derived": ["本人身故年份 2075", "规划区间 2026 至 2075，共 50 个年度"],
        "mode": "saved",
        "requirements": ["家庭资料决定规划年度边界；配偶分支必须独立保存双方寿命输入并生成家庭寿命终点。"],
        "gaps": ["配偶数据真实保存", "双方寿命终点选择规则", "年份边界、无效输入和失败回滚"],
    },
    "RT-15-019": {
        "resource": "TFPDAILYEXPENSESINFODLGFM",
        "title": "日常支出",
        "screenshots": [
            screenshot("rt15-financial-planning-daily-expense-dialog-20260803.png"),
            screenshot("rt15-financial-planning-daily-expense-sample-20260803.png"),
            screenshot("rt15-financial-planning-daily-expense-reopen-20260803.png"),
            screenshot("rt15-financial-planning-cold-reopen-expense-20260803.png"),
        ],
        "summary": "已真实保存家庭年日常支出 60000，并在冷启动后保持；与工资样例合并后年度净现金流由 120000 降为 60000。",
        "inputs": ["家庭年日常支出"],
        "reads": ["已保存日常支出", "通胀率参考值"],
        "writes": ["家庭年日常支出：60000"],
        "derived": ["年度基础生活支出 60000", "工资 120000 减支出 60000 后的年度净现金流 60000"],
        "mode": "saved",
        "requirements": ["家庭日常支出必须作为独立年度输入，并与通胀假设按明确顺序展开。"],
        "gaps": ["通胀率的生效年度和复利顺序", "零值、负值、极大值、舍入和失败回滚"],
    },
    "RT-15-020": {
        "resource": "TFPEDUCATIONEXPENSESINFODLGFM",
        "title": "教育计划",
        "screenshots": [screenshot("rt15-financial-planning-education-dialog-20260803.png")],
        "summary": "已确认名称、开始年份、持续年数、结束年份、每年学费、生活费、其它费用及合计字段；本轮未保存样例。",
        "inputs": ["名称", "开始年份", "持续年数", "结束年份", "每年学费", "每年生活费", "每年其它费用"],
        "reads": ["规划年度范围"],
        "derived": ["每年教育费用合计", "按期间展开的教育支出"],
        "requirements": ["教育计划应保留费用分项和年度合计，不能只保存汇总金额。"],
        "gaps": ["真实保存与冷启动", "合计公式、期间边界、增长规则、舍入和失败回滚"],
    },
    "RT-15-021": {
        "resource": "TFPEXPENSESADJUSTMENTINFODLGFM",
        "title": "支出调整",
        "screenshots": [screenshot("rt15-financial-planning-expense-adjustment-dialog-20260803.png")],
        "summary": "已确认名称、开始年份、持续年数、结束年份和日常支出增量，减少支出时输入负数；本轮未保存样例。",
        "inputs": ["名称", "开始年份", "持续年数", "结束年份", "日常支出增量"],
        "reads": ["家庭年日常支出", "规划年度范围"],
        "derived": ["指定期间内调整后的家庭日常支出"],
        "requirements": ["支出调整必须保存有符号增量和适用期间，并避免把负数静默归零。"],
        "gaps": ["真实保存与冷启动", "负数边界、与通胀的计算顺序、叠加规则和失败回滚"],
    },
    "RT-15-022": {
        "resource": "TFPINFLATIONRATEINFODLGFM",
        "title": "通货膨胀率",
        "screenshots": [screenshot("rt15-financial-planning-inflation-dialog-20260803.png")],
        "summary": "已确认通胀率输入作为家庭日常支出增长参考；本轮保持零值，未保存非零样例。",
        "inputs": ["通货膨胀率"],
        "reads": ["家庭年日常支出", "规划年度范围"],
        "derived": ["通胀调整后的年度家庭日常支出"],
        "requirements": ["通胀假设必须版本化，并明确从哪个年度开始作用于哪些支出。"],
        "gaps": ["非零通胀真实保存", "生效年度、复利顺序、负通胀、精度和失败回滚"],
    },
    "RT-15-023": {
        "resource": "TFPOTHEREXPENSESINFODLGFM",
        "title": "其它支出",
        "screenshots": [
            screenshot("rt15-financial-planning-other-expense-dialog-20260803.png"),
            screenshot("rt15-financial-planning-expense-dialog-20260803.png"),
        ],
        "summary": "已确认当前其它支出与未来普通重大支出共用名称、年支出、期间和增长率结构；本轮未保存样例。",
        "inputs": ["名称", "年支出", "开始年份", "持续年数", "结束年份", "年增长率"],
        "reads": ["规划年度范围"],
        "derived": ["按期间展开的其它或重大年度支出"],
        "requirements": ["普通其它支出与重大支出可复用结构，但必须保留业务类型和来源入口。"],
        "gaps": ["真实保存与冷启动", "增长率、同年多支出排序、负值、舍入和失败回滚"],
    },
    "RT-15-024": {
        "resource": "TFPOTHERINCOMEINFODLGFM",
        "title": "其它收入",
        "screenshots": [screenshot("rt15-financial-planning-other-income-dialog-20260803.png")],
        "summary": "已确认名称、年收入、开始年份、持续年数、结束年份和年增长率；本轮未保存样例。",
        "inputs": ["名称", "年收入", "开始年份", "持续年数", "结束年份", "年增长率"],
        "reads": ["规划年度范围"],
        "derived": ["按期间展开的其它年度收入"],
        "requirements": ["其它收入必须保存业务名称、金额、期间和增长假设。"],
        "gaps": ["真实保存与冷启动", "增长率、期间边界、负值、舍入和失败回滚"],
    },
    "RT-15-025": {
        "resource": "TFPRETIREMENTINFODLGFM",
        "title": "养老计划",
        "screenshots": [screenshot("rt15-financial-planning-retirement-dialog-20260803.png")],
        "summary": "已确认退休年龄与退休年份联动、退休年收入、收入增长率和退休后家庭年支出；本轮未保存样例。",
        "inputs": ["退休年龄", "退休年份", "退休年收入", "退休收入增长率", "退休后家庭年支出"],
        "reads": ["本人出生年份", "规划年度范围", "退休前家庭支出"],
        "derived": ["退休年份", "退休后的年度收入和家庭支出"],
        "requirements": ["养老计划必须保留退休年龄/年份联动规则，并分别展开退休收入与退休后支出。"],
        "gaps": ["真实保存与冷启动", "退休当年口径、收入和支出的增长顺序、边界与失败回滚"],
    },
    "RT-15-026": {
        "resource": "TFPSELECTASSETSDLGFM",
        "title": "选择资产",
        "screenshots": [
            screenshot("rt15-financial-planning-cash-deposit-dialog-20260803.png"),
            screenshot("rt15-financial-planning-investment-assets-dialog-20260803.png"),
            screenshot("rt15-financial-planning-debt-selector-dialog-20260803.png"),
            screenshot("rt15-financial-planning-commercial-insurance-dialog-20260803.png"),
        ],
        "summary": "同一选择器按入口展示现金与存款、投资资产、债权债务或商业保险；列表显示账户名称和余额并提供新增账户，测试库前三类默认全选，商业保险为空。",
        "inputs": ["账户勾选范围", "新增账户命令"],
        "reads": ["账户稳定 ID", "账户类型", "账户名称", "账户余额或估值"],
        "derived": ["规划纳入的现金、投资、债权债务和保险账户集合"],
        "requirements": ["规划账户范围必须保存稳定 ID 与估值快照，显示名称和余额不能代替引用关系。"],
        "gaps": ["取消勾选后的保存与冷启动", "新增账户返回刷新", "候选失效、跨币种估值、并发和失败回滚"],
    },
    "RT-15-027": {
        "resource": "TFPYEARDATAINFODLGFM",
        "title": "年度情况",
        "screenshots": [
            screenshot("rt15-financial-planning-sample-chart-20260803.png"),
            screenshot("rt15-financial-planning-sample-chart-recalc-20260803.png"),
            screenshot("rt15-financial-planning-cold-reopen-20260803.png"),
        ],
        "summary": "规划中心已显示 2026~2075 共 50 个年度结果；工资 120000、日常支出 60000、零增长时余额每年净增 60000 并冷启动保持，但未确认该类独立明细窗体。",
        "inputs": ["家庭寿命区间", "全部规划专题输入", "账户与估值快照"],
        "reads": ["已保存家庭资料", "工资 120000", "家庭年日常支出 60000", "规划账户范围"],
        "derived": ["2026 至 2075 年年度余额序列", "年度净现金流 60000", "图表纵轴缩放", "绿色健康状态"],
        "mode": "result",
        "requirements": ["年度结果必须保留逐年数值、输入与估值快照、公式版本和计算时间，图表只作为可重算展示。"],
        "gaps": ["独立年度明细窗体和全部字段", "首年余额组成", "复利、分期、跨币种、舍入、负余额和失败回滚"],
    },
}


def build_record(execution_id: str, spec: dict[str, Any]) -> dict[str, Any]:
    """按真实操作模式构造单个 schema v1 观察记录。"""

    mode = spec.get("mode", "observed")
    reachable = mode != "base"
    state_status = "not_applicable" if mode == "base" else "observed"
    result_status = "unreachable" if mode == "base" else "partial"

    if mode == "saved":
        command = {
            "component": spec["resource"],
            "label": "确定并保存",
            "initial_state": {"enabled": True, "visible": True, "draft_isolated": True},
            "trigger": "填写受控样例后点击确定",
            "confirmation": "专题对话框中的确定按钮",
            "outcome": "输入保存到规划，年度结果立即重算，并在关闭旧程序后冷启动保持。",
            "status": "pass",
        }
        side_effects = ["确定后立即重算年度余额图", "正常关闭后输入和年度结果在冷启动中保持"]
    elif mode == "base":
        command = {
            "component": spec["resource"],
            "label": "独立打开",
            "initial_state": {"enabled": False, "visible": False, "implementation_only": True},
            "trigger": "寻找独立用户入口",
            "confirmation": None,
            "outcome": "未发现独立入口；公共行为由派生规划编辑器提供。",
            "status": "not_applicable",
        }
        side_effects = []
    elif mode == "result":
        command = {
            "component": spec["resource"],
            "label": "查看年度结果",
            "initial_state": {"enabled": True, "visible": True, "planning_exists": True},
            "trigger": "保存规划输入后查看并冷启动复核年度余额图",
            "confirmation": None,
            "outcome": "主图显示并持久化年度余额序列；独立年度明细窗体仍未确认。",
            "status": "partial",
        }
        side_effects = ["输入变化会重新计算图表范围和健康状态"]
    else:
        command = {
            "component": spec["resource"],
            "label": "打开并取消",
            "initial_state": {"enabled": True, "visible": True, "planning_exists": True},
            "trigger": "从财务规划对应专题点击新增或修改",
            "confirmation": None,
            "outcome": "字段、分支和默认值已记录；关闭未确认的对话框没有保存该专题样例。",
            "status": "pass",
        }
        side_effects = []

    evidence = [
        {"kind": "screenshot", "path": path, "description": f"{spec['title']}运行态证据。"}
        for path in spec["screenshots"]
    ]
    evidence.append({"kind": "manual_note", "path": NOTE_PATH, "description": "财务规划字段、受控计算、持久化和目标数据流。"})
    if mode in {"saved", "result"}:
        evidence.append({
            "kind": "hash",
            "path": "artifacts/runtime-validation/backups/RT-15-011-financial-planning-after-cold-20260803T025746+0800.mh8",
            "description": f"冷启动复核后的修改态账簿，SHA-256 为 {COLD_HASH}。",
        })

    rollback = (
        f"共享验证结束后已用 {BASELINE_BACKUP} 整体恢复 test.mh8 至 {BASELINE_HASH}；"
        "MoneyHome8 进程和恢复文件均为 0。"
    )
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
            "path": r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8",
            "sha256_before": BASELINE_HASH,
            "sha256_after": COLD_HASH,
            "backup_artifact": BASELINE_BACKUP,
        },
        "navigation": {
            "entry_point": "财智8 -> 财务分析 -> 财务规划",
            "steps": [
                "进入财务规划并建立 2026~2075 年规划",
                f"打开{spec['title']}对应入口",
                "记录字段、分支、默认值和命令结果",
                "按记录说明保存受控样例或取消未保存草稿",
                "归档修改态并恢复 test.mh8 基线",
            ],
            "reachable": reachable,
            "unreachable_reason": None if reachable else "公共基类没有独立用户入口，由派生规划编辑器间接覆盖。",
        },
        "states": [{
            "name": spec["title"],
            "status": state_status,
            "observations": spec["summary"],
            "evidence_paths": spec["screenshots"],
        }],
        "commands": [command],
        "data_flow": {
            "inputs": spec["inputs"],
            "reads": spec["reads"],
            "writes": spec.get("writes", []),
            "derived_results": spec["derived"],
            "side_effects": side_effects,
            "rollback": rollback,
        },
        "evidence": evidence,
        "requirements_update": spec["requirements"],
        "result": {
            "status": result_status,
            "summary": spec["summary"],
            "remaining_gaps": spec["gaps"],
        },
    }


def main() -> None:
    """写入新时间戳记录，保留旧记录用于审计。"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for execution_id, spec in FORM_SPECS.items():
        record = build_record(execution_id, spec)
        path = OUTPUT_DIR / f"{execution_id}-{FILE_TIMESTAMP}.json"
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(FORM_SPECS)} RT-15 planning subrecords")


if __name__ == "__main__":
    main()
