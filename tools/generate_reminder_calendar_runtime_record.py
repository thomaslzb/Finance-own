"""生成普通提醒实例到财务日历投影的补充运行记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-08-03T15:30:00+08:00"
FILE_SUFFIX = "20260803T153000+0800"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
BACKUP_ARTIFACT = "artifacts/runtime-validation/backups/RT-15-009-reminder-projection-before-20260803T-current.mh8"
CONTRACT = "docs/runtime-reminder-calendar-contract.md"


def shot(name: str) -> str:
    """返回本轮截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(path: str, description: str, kind: str = "screenshot") -> dict:
    """构造一条可追溯证据。"""

    return {"kind": kind, "path": path, "description": description}


def build_record() -> dict:
    """生成包含日记、生日和普通提醒结论的最新版日历记录。"""

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
                "创建当天一次性普通提醒并核对计划列表",
                "核对待处理实例的今日提醒能力",
                "核对同日日历提醒图标、名称摘要和交易标记",
                "跳过实例并重新打开财务日历",
                "显示已完成定义并确认兼容完成态",
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
                "name": "普通提醒待处理投影",
                "status": "observed",
                "observations": "CodexRT15CalendarReminder待处理时，日期格显示独立勾选图标，摘要显示提醒名称；同日账务图标和有账务记录保持。",
                "evidence_paths": [
                    shot("rt15-calendar-reminder-plan-list-after-save-20260803T1518.png"),
                    shot("rt15-calendar-reminder-pending-projection-20260803T1519.png"),
                    shot("rt15-calendar-reminder-today-before-skip-20260803T1521.png"),
                ],
            },
            {
                "name": "跳过后投影消失",
                "status": "observed",
                "observations": "跳过后今日提醒清空，日历提醒图标和摘要消失，交易来源保持；定义仍在已完成范围并显示执行完毕。",
                "evidence_paths": [
                    shot("rt15-calendar-reminder-today-after-skip-20260803T1522.png"),
                    shot("rt15-calendar-reminder-after-skip-20260803T1523.png"),
                    shot("rt15-calendar-reminder-completed-plan-list-20260803T1526.png"),
                ],
            },
            {
                "name": "临时定义删除与基线恢复",
                "status": "observed",
                "observations": "确认删除后临时定义退出已完成列表；指定测试账簿恢复到运行前精确指纹。",
                "evidence_paths": [
                    shot("rt15-calendar-reminder-delete-confirm-20260803T1529.png"),
                    shot("rt15-calendar-reminder-after-delete-20260803T1529.png"),
                ],
            },
        ],
        "commands": [
            {
                "component": "reminderOccurrenceProjection",
                "label": "提醒摘要",
                "initial_state": {"status": "pending", "visible": True},
                "trigger": "选择提醒应发生日2026-08-03",
                "confirmation": None,
                "outcome": "显示CodexRT15CalendarReminder和独立提醒图标；未观察到查看入口。",
                "status": "pass",
            },
            {
                "component": "todayReminder/reminderOccurrenceProjection",
                "label": "跳过提醒实例",
                "initial_state": {"can_execute": False, "can_skip": True},
                "trigger": "今日提醒点击跳过后重新打开财务日历",
                "confirmation": None,
                "outcome": "本期实例退出今日提醒和日历，定义保留为兼容完成态，同日交易标记保持。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": ["账簿ID", "选中自然日", "提醒实例ID和版本"],
            "reads": ["pending普通提醒实例", "同日交易存在性", "同日日记和生日来源"],
            "writes": ["跳过命令写实例动作、处理时间和审计；日历查询本身无写入"],
            "derived_results": ["按来源类型分组的日期图标和摘要", "提醒实例当前可见性", "来源命令能力"],
            "side_effects": ["跳过不生成交易、不删除提醒定义或同日其它来源"],
            "rollback": "跳过提交失败时实例保持待处理；成功后今日提醒和日历从同一提交版本刷新。",
        },
        "evidence": [
            evidence(CONTRACT, "普通提醒与财务日历运行合同。", "manual_note"),
            evidence("artifacts/runtime-validation/RT15-financial-calendar-notes.md", "财务日历运行笔记。", "manual_note"),
            evidence("artifacts/runtime-validation/RT15-plans-and-reminders-notes.md", "计划与提醒运行笔记。", "manual_note"),
            evidence(BACKUP_ARTIFACT, "运行前精确基线。", "file"),
            evidence("artifacts/runtime-validation/backups/RT-15-009-reminder-projection-after-delete-20260803T1530+0800.mh8", "删除临时定义后的业务副本。", "file"),
            evidence("artifacts/runtime-validation/backups/RT-15-009-reminder-projection-recovery-side-after-delete-20260803T1530+0800", "关闭进程后的恢复侧文件。", "file"),
        ],
        "requirements_update": [
            "普通提醒定义与每次发生实例分层，日历使用occurrence_id而不是定义名称作为来源键。",
            "当前兼容投影只返回应发生日在选中日期且状态为pending的普通提醒实例。",
            "跳过原子保存skipped动作和审计，随后移出今日提醒和日历，但保留定义与历史实例。",
            "应发生日与提前提醒资格窗口分别保存，未来日期日历口径在验证前不得合并。",
            "同日提醒、交易、日记和生日独立聚合，任一来源状态变化不得覆盖其它来源。",
            "摘要下钻使用明确can_open能力；旧版未观察到查看入口，不能臆造兼容行为。",
        ],
        "result": {
            "status": "partial",
            "summary": "已验证普通提醒待处理实例进入财务日历、与交易独立共存，并在跳过后立即退出日历而定义保留为已完成。",
            "remaining_gaps": [
                "未来提醒的提前窗口与日历应发生日口径",
                "重复提醒多期投影和冷启动保持",
                "同日多提醒及跨来源稳定排序",
                "提醒摘要点击、下钻和详情提示",
                "执行、失败、停用、归档和修改后的日历状态",
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
