"""生成普通提醒在今日提醒与财务日历中的补充运行记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-08-03T16:10:00+08:00"
FILE_SUFFIX = "20260803T161000+0800"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
BACKUP_ARTIFACT = (
    "artifacts/runtime-validation/backups/"
    "RT-15-009-future-recurring-reminder-before-20260803T-current.mh8"
)
FIRST_SKIP_ARTIFACT = (
    "artifacts/runtime-validation/backups/"
    "RT-15-009-future-recurring-reminder-after-first-skip-20260803T1601+0800.mh8"
)
AFTER_DELETE_ARTIFACT = (
    "artifacts/runtime-validation/backups/"
    "RT-15-009-future-recurring-reminder-after-delete-20260803T1610+0800.mh8"
)
CONTRACT = "docs/runtime-reminder-calendar-contract.md"


def shot(name: str) -> str:
    """返回本轮截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(path: str, description: str, kind: str = "screenshot") -> dict:
    """构造一条可追溯证据。"""

    return {"kind": kind, "path": path, "description": description}


def build_record() -> dict:
    """生成包含日记、生日和两类普通提醒样例的最新版日历记录。"""

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
            "entry_point": "财智8 -> 计划提醒 -> 计划与提醒 / 今日提醒 / 财务日历",
            "steps": [
                "创建开始日为次日、每天重复2次、提前3天的普通提醒",
                "核对今日提醒资格日、计划列表和开始日日历投影",
                "跳过第一期并核对今日提醒推进与两个发生日的日历状态",
                "完整冷启动后重复核对中间状态",
                "跳过第二期并核对定义完成后的日历状态",
                "删除临时定义并恢复test.mh8精确基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "日记来源既有闭环",
                "status": "observed",
                "observations": "同日日记摘要可与账务记录共存；删除日记只移除日记摘要。",
                "evidence_paths": [
                    shot("rt19-diary-extended-financial-calendar-20260803T1425.png"),
                    shot("rt19-diary-extended-calendar-after-delete-20260803T1429.png"),
                ],
            },
            {
                "name": "生日来源既有闭环",
                "status": "observed",
                "observations": "公历当天生日进入摘要并在人物删除后消失；农历样例的三个候选日期均未投影。",
                "evidence_paths": [
                    shot("rt15-birthday-calendar-gregorian-today-20260803T1501.png"),
                    shot("rt15-birthday-calendar-after-person-delete-20260803T1506.png"),
                    shot("rt15-birthday-calendar-lunar-june7-20260803T1447.png"),
                ],
            },
            {
                "name": "一次性提醒完成后投影消失",
                "status": "observed",
                "observations": "一次性提醒在开始日显示，跳过后定义完成且标记消失；因开始日、唯一发生日和完成日重合，该样例不能单独证明实例投影。",
                "evidence_paths": [
                    shot("rt15-calendar-reminder-pending-projection-20260803T1519.png"),
                    shot("rt15-calendar-reminder-after-skip-20260803T1523.png"),
                    shot("rt15-calendar-reminder-completed-plan-list-20260803T1526.png"),
                ],
            },
            {
                "name": "提前资格只进入今日提醒",
                "status": "observed",
                "observations": "2026-08-03今日提醒显示第一期2026-08-04和1天后；同日财务日历没有提醒，开始日2026-08-04才显示勾选图标和名称。",
                "evidence_paths": [
                    shot("rt15-future-daily-plan-list-after-save-20260803T1550.png"),
                    shot("rt15-future-daily-today-before-first-skip-20260803T1551.png"),
                    shot("rt15-future-daily-calendar-eligibility-day-20260803T1556.png"),
                    shot("rt15-future-daily-calendar-first-occurrence-20260804T1557.png"),
                ],
            },
            {
                "name": "首次跳过后日历仍锚定开始日",
                "status": "observed",
                "observations": "第一期跳过后今日提醒和计划下次日期推进到2026-08-05；日历仍只在2026-08-04显示，2026-08-05为空。",
                "evidence_paths": [
                    shot("rt15-future-daily-today-after-first-skip-20260803T1558.png"),
                    shot("rt15-future-daily-plan-list-after-first-skip-20260803T1600.png"),
                    shot("rt15-future-daily-calendar-first-after-skip-20260804T1559.png"),
                    shot("rt15-future-daily-calendar-second-occurrence-20260805T1559.png"),
                ],
            },
            {
                "name": "中间状态冷启动保持",
                "status": "observed",
                "observations": "完整重启后今日提醒仍显示第二期，财务日历仍只在定义开始日显示，排除单纯页面缓存。",
                "evidence_paths": [
                    shot("rt15-future-daily-today-cold-after-first-skip-20260803T1604.png"),
                    shot("rt15-future-daily-calendar-cold-first-after-skip-20260804T1605.png"),
                    shot("rt15-future-daily-calendar-cold-second-after-skip-20260805T1605.png"),
                ],
            },
            {
                "name": "定义完成、删除与基线恢复",
                "status": "observed",
                "observations": "第二期跳过后定义完成，开始日和第二发生日均无标记；删除临时定义后指定测试账簿恢复精确指纹。",
                "evidence_paths": [
                    shot("rt15-future-daily-today-after-second-skip-20260803T1606.png"),
                    shot("rt15-future-daily-calendar-first-after-complete-20260804T1607.png"),
                    shot("rt15-future-daily-calendar-second-after-complete-20260805T1607.png"),
                    shot("rt15-future-daily-plan-list-completed-20260803T1608.png"),
                    shot("rt15-future-daily-plan-list-after-delete-20260803T1609.png"),
                ],
            },
        ],
        "commands": [
            {
                "component": "legacyReminderCalendarProjection",
                "label": "普通提醒兼容日历摘要",
                "initial_state": {"schedule_state": "active", "visible_on_start_date": True},
                "trigger": "分别选择资格日、定义开始日和第二发生日",
                "confirmation": None,
                "outcome": "只在活动定义的开始日显示；不按提前资格日或下一发生日迁移。",
                "status": "pass",
            },
            {
                "component": "todayReminder/reminderOccurrence",
                "label": "跳过重复提醒实例",
                "initial_state": {"can_execute": False, "can_skip": True},
                "trigger": "依次跳过两期并在第一期后完整冷启动",
                "confirmation": None,
                "outcome": "第一期后实例推进但开始日投影保持；最终定义完成后兼容日历投影消失。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": ["账簿ID", "当前业务日", "选中自然日", "提醒定义或实例ID和版本"],
            "reads": [
                "今日提醒读取提前资格窗口内的pending普通提醒实例",
                "旧日历读取开始日等于选中日期的活动普通提醒定义",
                "同日交易、日记和生日来源",
            ],
            "writes": ["跳过命令写实例动作、处理时间和审计并推进定义；日历查询本身无写入"],
            "derived_results": [
                "按occurrence_id生成的今日提醒项",
                "按schedule_id和start_date生成的旧日历兼容项",
                "来源命令能力",
            ],
            "side_effects": ["跳过不生成交易、不删除定义或同日其它来源"],
            "rollback": "跳过提交失败时实例和定义推进均不生效；成功后今日提醒与兼容日历从同一提交版本刷新。",
        },
        "evidence": [
            evidence(CONTRACT, "普通提醒与财务日历运行合同。", "manual_note"),
            evidence("artifacts/runtime-validation/RT15-financial-calendar-notes.md", "财务日历运行笔记。", "manual_note"),
            evidence("artifacts/runtime-validation/RT15-plans-and-reminders-notes.md", "计划与提醒运行笔记。", "manual_note"),
            evidence(BACKUP_ARTIFACT, "运行前精确基线。", "file"),
            evidence(FIRST_SKIP_ARTIFACT, "首次跳过后的冷启动中间业务状态。", "file"),
            evidence(AFTER_DELETE_ARTIFACT, "删除临时定义后的业务副本。", "file"),
            evidence("artifacts/runtime-validation/backups/RT-15-009-future-recurring-reminder-side-after-first-skip-20260803T1601+0800", "首次跳过并关闭进程后的恢复侧文件。", "file"),
            evidence("artifacts/runtime-validation/backups/RT-15-009-future-recurring-reminder-side-after-delete-20260803T1610+0800", "删除临时定义并关闭进程后的恢复侧文件。", "file"),
        ],
        "requirements_update": [
            "ReminderSchedule、ReminderOccurrence和LegacyReminderCalendarProjection必须分层。",
            "今日提醒按eligible_from_date到occurrence_date的资格窗口读取实例，并在跳过后推进下一实例。",
            "旧版兼容日历只在活动普通提醒定义的start_date返回schedule_id来源，不跟随next_occurrence_date。",
            "最终实例处理使定义完成后，开始日兼容标记退出；历史skipped动作和实例审计继续保留。",
            "start_date、occurrence_date和eligible_from_date分别保存，不能互相覆盖。",
            "目标产品如增加逐实例日历，必须与MoneyHome8兼容投影明确区分。",
            "同日提醒、交易、日记和生日独立聚合，任一来源状态变化不得覆盖其它来源。",
        ],
        "result": {
            "status": "partial",
            "summary": "已验证今日提醒按发生实例和提前资格窗口推进；MoneyHome8旧财务日历则把活动普通提醒定义锚定在开始日，并在定义完成后移除。",
            "remaining_gaps": [
                "每周、每月、每年和自定义重复规则的开始日投影",
                "定义修改开始日以及暂停、停用、归档和删除后的投影",
                "同日多提醒及跨来源稳定排序",
                "提醒摘要点击、下钻和详情提示",
                "执行、失败和并发提交的一致性",
                "历史公历生日周年、农历规则和日记查看下钻",
            ],
        },
    }


def main() -> None:
    """写出最新版财务日历普通提醒投影记录。"""

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
