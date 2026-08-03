"""生成财务日历生日来源投影的补充运行记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-08-03T15:10:00+08:00"
FILE_SUFFIX = "20260803T151000+0800"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
BACKUP_ARTIFACT = "artifacts/runtime-validation/backups/RT-15-009-birthday-projection-before-20260803T-current.mh8"
CONTRACT = "docs/runtime-birthday-calendar-contract.md"


def shot(name: str) -> str:
    """返回本轮截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(path: str, description: str, kind: str = "screenshot") -> dict:
    """构造一条可追溯证据。"""

    return {"kind": kind, "path": path, "description": description}


def build_record() -> dict:
    """生成包含既有日记证据和本轮生日证据的最新版日历记录。"""

    return {
        "schema_version": 1,
        "execution_id": "RT-15-009",
        "resource": "TFINANCIALCALENDARDLG",
        "observed_at": OBSERVED_AT,
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": LEDGER_PATH,
            "sha256_before": BASELINE_HASH,
            "sha256_after": BASELINE_HASH,
            "backup_artifact": BACKUP_ARTIFACT,
        },
        "navigation": {
            "entry_point": "财智8 -> 计划提醒 -> 财务日历",
            "steps": [
                "载入已验证的农历人物业务副本并核对人物生日字段",
                "检查农历周年、原始月日和精确出生日期",
                "新增默认当天公历生日人物",
                "核对公历生日与账务记录同日独立展示",
                "删除公历人物并核对生日摘要消失",
                "删除农历临时人物并恢复test.mh8精确基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "日记来源既有闭环",
                "status": "observed",
                "observations": "2026-08-03的日记摘要和查看入口可与有账务记录共存；删除日记后只移除日记摘要。",
                "evidence_paths": [
                    shot("rt19-diary-extended-financial-calendar-20260803T1425.png"),
                    shot("rt19-diary-extended-calendar-after-delete-20260803T1429.png"),
                ],
            },
            {
                "name": "农历生日未投影",
                "status": "observed",
                "observations": "CodexRT34Person保存为农历1991-06-07；对应2026年农历六月初七、2026-06-07原始月日和1991-06-07精确出生日期均无生日摘要。",
                "evidence_paths": [
                    shot("rt15-birthday-person-business-state-20260803T1444.png"),
                    shot("rt15-birthday-calendar-lunar-june7-20260803T1447.png"),
                    shot("rt15-birthday-calendar-raw-month-day-20260803T1449.png"),
                    shot("rt15-birthday-calendar-exact-birth-date-19910607-20260803T1450.png"),
                ],
            },
            {
                "name": "公历生日投影",
                "status": "observed",
                "observations": "CodexRT15Bday保存为公历2026-08-03后，日历显示今天是CodexRT15Bday的生日，并独立保留有账务记录。",
                "evidence_paths": [
                    shot("rt15-birthday-person-after-save-20260803T1500.png"),
                    shot("rt15-birthday-calendar-gregorian-today-20260803T1501.png"),
                ],
            },
            {
                "name": "人物删除后投影消失",
                "status": "observed",
                "observations": "确认删除公历人物后重新打开日历，生日摘要消失而有账务记录保持；随后清理农历临时人物。",
                "evidence_paths": [
                    shot("rt15-birthday-person-delete-confirm-20260803T1504.png"),
                    shot("rt15-birthday-calendar-after-person-delete-20260803T1506.png"),
                    shot("rt15-birthday-person-after-cleanup-20260803T1508.png"),
                ],
            },
        ],
        "commands": [
            {
                "component": "birthdayProjection",
                "label": "生日摘要",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "选择公历生日人物对应的2026-08-03",
                "confirmation": None,
                "outcome": "显示今天是CodexRT15Bday的生日；未观察到查看入口。",
                "status": "pass",
            },
            {
                "component": "partyDelete/birthdayProjection",
                "label": "删除人物并刷新生日摘要",
                "initial_state": {"party": "CodexRT15Bday", "calendar": "gregorian"},
                "trigger": "人员列表确认删除后重新打开财务日历",
                "confirmation": "人员删除确认对话框提供是/否",
                "outcome": "生日摘要立即消失，同日交易标记保持。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": ["账簿ID", "选中自然日", "人物稳定ID、当前名称、历法和原始生日分量"],
            "reads": ["同日交易存在性", "同日日记事实", "可见且未删除人物的生日真相"],
            "writes": [],
            "derived_results": ["按来源类型分组的日期摘要", "公历生日发生实例", "来源命令能力"],
            "side_effects": ["人物新增和删除由人员主数据命令完成；日历查询本身无写入"],
            "rollback": "财务日历为只读投影；人物命令失败时不得出现只有日历摘要或只有人物记录的部分状态。",
        },
        "evidence": [
            evidence(CONTRACT, "生日与财务日历运行合同。", "manual_note"),
            evidence("artifacts/runtime-validation/RT15-financial-calendar-notes.md", "财务日历运行笔记。", "manual_note"),
            evidence(BACKUP_ARTIFACT, "运行前精确基线。", "file"),
            evidence("artifacts/runtime-validation/backups/RT-15-009-birthday-projection-after-delete-20260803T1509+0800.mh8", "删除临时人物后的业务副本。", "file"),
        ],
        "requirements_update": [
            "生日保留在PartyBirthday人物真相中，日历只生成可重建的BirthdayOccurrence投影。",
            "投影保留party_id、来源版本、历法、原始分量、发生日期和换算规则版本。",
            "公历和农历周年、2月29日、农历闰月、时区与账簿业务日策略必须显式版本化。",
            "人物改名、生日修改、隐藏或删除后，所有日期摘要必须从同一提交版本刷新。",
            "同日生日、交易、计划、提醒和日记按独立来源项聚合，任一来源删除不得覆盖其它来源。",
            "旧版农历样例未投影是兼容证据和缺陷线索，目标产品仍应明确实现并测试农历生日。",
        ],
        "result": {
            "status": "partial",
            "summary": "已验证公历生日摘要、与交易标记共存、人物删除后的投影消失，并确认一个农历生日在三种候选日期口径下均未投影。",
            "remaining_gaps": [
                "历史年份公历生日的年度重复和年龄口径",
                "农历生日换算、闰月和大小月策略",
                "人物隐藏、改名和生日修改后的投影刷新",
                "同日多人生日排序和生日摘要下钻",
                "提醒来源的真实日历样例",
            ],
        },
    }


def main() -> None:
    """写出最新版财务日历生日投影记录。"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"RT-15-009-{FILE_SUFFIX}.json"
    output_path.write_text(
        json.dumps(build_record(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"generated {output_path.name}")


if __name__ == "__main__":
    main()
