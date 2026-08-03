"""生成日记扩展生命周期与财务日历投影的补充运行记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-08-03T14:31:00+08:00"
FILE_SUFFIX = "20260803T143100+0800"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
BACKUP_ARTIFACT = "artifacts/runtime-validation/backups/RT-19-diary-extended-before-20260803T-current.mh8"
CONTRACT = "docs/runtime-diary-contract.md"


def shot(name: str) -> str:
    """返回本轮截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(path: str, description: str, kind: str = "screenshot") -> dict:
    """构造一条可追溯证据。"""

    return {"kind": kind, "path": path, "description": description}


def build_record(execution_id: str, spec: dict) -> dict:
    """把日记补充规格转换为统一运行记录。"""

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
            "sha256_after": BASELINE_HASH,
            "backup_artifact": BACKUP_ARTIFACT,
        },
        "navigation": {
            "entry_point": spec["entry"],
            "steps": spec["steps"],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": spec["states"],
        "commands": spec["commands"],
        "data_flow": spec["data_flow"],
        "evidence": spec["evidence"] + [evidence(CONTRACT, "日记运行合同。", "manual_note")],
        "requirements_update": spec["requirements"],
        "result": {
            "status": "partial",
            "summary": spec["summary"],
            "remaining_gaps": spec["gaps"],
        },
    }


RECORDS = {
    "RT-19-005": {
        "resource": "TDIARYDLGFM",
        "entry": "财智8 -> 财务工具 -> 日记 -> 写日记/修改",
        "steps": ["创建粗体日记", "重新打开修改页", "放弃未保存更改", "重新修改并保存", "冷启动核对"],
        "states": [
            {
                "name": "粗体创建",
                "status": "observed",
                "observations": "正文以粗体保存，月度列表从 0 篇变为 1 篇。",
                "evidence_paths": [shot("rt19-diary-extended-editor-filled-bold-20260803T1409.png"), shot("rt19-diary-extended-after-create-20260803T1410.png")],
            },
            {
                "name": "修改加载",
                "status": "observed",
                "observations": "修改页加载原日期和正文，粗体按钮保持激活。",
                "evidence_paths": [shot("rt19-diary-extended-modify-loaded-20260803T1411.png")],
            },
            {
                "name": "放弃未保存更改",
                "status": "observed",
                "observations": "关闭脏草稿提示是否保存；选择否后重开仍为已保存版本。",
                "evidence_paths": [shot("rt19-diary-extended-unsaved-prompt-20260803T1412.png"), shot("rt19-diary-extended-after-discard-reopen-20260803T1413.png")],
            },
        ],
        "commands": [
            {"component": "btnSave", "label": "保存", "initial_state": {"enabled": True, "visible": True}, "trigger": "创建和修改后保存", "confirmation": None, "outcome": "正文、粗体格式、日期和月度计数跨冷启动保持。", "status": "pass"},
            {"component": "FormCloseQuery", "label": "关闭脏草稿", "initial_state": {"enabled": True, "visible": True}, "trigger": "修改正文后关闭", "confirmation": "你已修改2026-08-03的日记内容，是否保存更改？", "outcome": "选择否后丢弃草稿并保留原版本。", "status": "pass"},
        ],
        "data_flow": {
            "inputs": ["日记日期", "富文本正文", "粗体格式", "保存或放弃选择"],
            "reads": ["稳定日记记录和已保存富文本"],
            "writes": ["正文、格式版本、纯文本投影和更新时间"],
            "derived_results": ["月度摘要和篇数"],
            "side_effects": ["受控日记写入 test.mh8，冷启动核对后删除并恢复基线"],
            "rollback": "放弃脏草稿不写入；保存失败应原子回滚正文、格式和搜索投影。",
        },
        "evidence": [
            evidence(shot("rt19-diary-extended-cold-start-20260803T1424.png"), "冷启动后的日期、摘要和月度篇数。"),
        ],
        "requirements": ["修改沿用稳定日记 ID 并用行版本防止静默覆盖。", "正文与格式使用受限、版本化且可迁移的表示。", "脏草稿选择是时复用保存校验，选择否时只丢弃页面草稿。"],
        "summary": "已验证粗体持久化、修改加载、放弃未保存更改、正式保存和冷启动。",
        "gaps": ["其它格式组合和编辑菜单", "并发修改冲突", "自动化富文本替换产生的拼接文本不作为正常人工编辑结论"],
    },
    "RT-19-006": {
        "resource": "TDIARYUNTFM",
        "entry": "财智8 -> 财务工具 -> 日记",
        "steps": ["搜索命中", "搜索无结果", "查看全部", "打开导出目录选择器", "冷启动核对", "删除并确认空列表"],
        "states": [
            {"name": "搜索命中", "status": "observed", "observations": "搜索 updated 显示共 1 篇。", "evidence_paths": [shot("rt19-diary-extended-search-hit-20260803T1416.png")]},
            {"name": "搜索无结果", "status": "observed", "observations": "不存在的关键词显示搜索上下文和共 0 篇，不弹错误。", "evidence_paths": [shot("rt19-diary-extended-search-empty-20260803T1418.png")]},
            {"name": "查看全部", "status": "observed", "observations": "查看全部清除搜索模式并显示全部日记共 1 篇。", "evidence_paths": [shot("rt19-diary-extended-view-all-20260803T1419.png")]},
            {"name": "导出目录选择", "status": "observed", "observations": "导出打开浏览文件夹对话框，未选目录时确定禁用；未完成文件导出。", "evidence_paths": [shot("rt19-diary-extended-export-folder-dialog-20260803T1420.png")]},
            {"name": "删除后", "status": "observed", "observations": "确认删除后 2026 年 8 月恢复共 0 篇。", "evidence_paths": [shot("rt19-diary-extended-delete-confirm-20260803T1427.png"), shot("rt19-diary-extended-after-delete-20260803T1428.png")]},
        ],
        "commands": [
            {"component": "miModify", "label": "修改", "initial_state": {"enabled": True, "visible": True}, "trigger": "选中日记后执行", "confirmation": None, "outcome": "加载同一日记并可保存或放弃。", "status": "pass"},
            {"component": "miDelete", "label": "删除", "initial_state": {"enabled": True, "visible": True}, "trigger": "选中日记后执行并确认", "confirmation": "您确定删除该日记吗？", "outcome": "记录、月度计数和日历投影同步消失。", "status": "pass"},
            {"component": "miSearch", "label": "搜索", "initial_state": {"enabled": True, "visible": True}, "trigger": "分别输入命中和无结果关键词", "confirmation": None, "outcome": "显示显式搜索上下文和结果计数。", "status": "pass"},
            {"component": "miViewAll", "label": "查看全部", "initial_state": {"enabled": True, "visible": True}, "trigger": "在无结果搜索状态执行", "confirmation": None, "outcome": "切换到全部日记并恢复 1 条记录。", "status": "pass"},
            {"component": "miExport", "label": "导出列表", "initial_state": {"enabled": True, "visible": True}, "trigger": "在全部日记状态执行", "confirmation": None, "outcome": "仅确认目录选择器；导出文件未生成。", "status": "partial"},
        ],
        "data_flow": {
            "inputs": ["年月", "搜索文本", "全部列表命令", "当前选择", "导出目录"],
            "reads": ["日记日期、规范化纯文本、删除状态和稳定 ID"],
            "writes": ["删除命令更新日记可见状态；搜索、查看全部和导出预览只读"],
            "derived_results": ["月度计数、搜索计数、全部列表和安全摘要"],
            "side_effects": ["导出未完成；删除后的测试数据已清理并恢复账簿基线"],
            "rollback": "查询不写入；删除在确认后单事务更新真相和搜索投影。",
        },
        "evidence": [evidence(shot("rt19-diary-extended-cold-start-20260803T1424.png"), "冷启动列表。")],
        "requirements": ["月度、搜索、全部列表和日历读取同一日记真相。", "搜索匹配纯文本而不是富文本控制标记。", "导出冻结显式查询范围并只写用户选择目录。", "删除后列表计数、搜索和日历投影必须一致。"],
        "summary": "已验证搜索命中/空结果、查看全部、导出目录选择、冷启动和删除闭环。",
        "gaps": ["跨年月搜索范围和排序", "导出文件格式、编码、命名、覆盖和失败回滚", "大量日记性能"],
    },
    "RT-15-009": {
        "resource": "TFINANCIALCALENDARDLG",
        "entry": "财智8 -> 计划提醒 -> 财务日历",
        "steps": ["保留 2026-08-03 受控日记", "打开财务日历", "观察日记摘要", "删除日记", "重新打开日历核对摘要消失"],
        "states": [
            {"name": "日记存在", "status": "observed", "observations": "8 月 3 日右侧同时显示日记摘要、查看入口和有账务记录。", "evidence_paths": [shot("rt19-diary-extended-financial-calendar-20260803T1425.png")]},
            {"name": "日记删除后", "status": "observed", "observations": "日记摘要消失，同日有账务记录保持。", "evidence_paths": [shot("rt19-diary-extended-calendar-after-delete-20260803T1429.png")]},
        ],
        "commands": [
            {"component": "diaryProjection", "label": "日记摘要", "initial_state": {"enabled": True, "visible": True}, "trigger": "选择包含日记的 2026-08-03", "confirmation": None, "outcome": "按日期显示日记正文摘要。", "status": "pass"},
            {"component": "diaryView", "label": "查看", "initial_state": {"enabled": True, "visible": True}, "trigger": "窗口消息未触发，物理坐标被安全保护拒绝", "confirmation": None, "outcome": "下钻目标仍待验证。", "status": "partial"},
        ],
        "data_flow": {
            "inputs": ["账簿 ID", "选中自然日"],
            "reads": ["交易存在性和同日日记事实"],
            "writes": [],
            "derived_results": ["按来源类型分组的日期摘要和查看能力"],
            "side_effects": [],
            "rollback": "财务日历为只读投影，不保存第二套事件或日记。",
        },
        "evidence": [],
        "requirements": ["日历按账簿自然日只读聚合日记和其它来源。", "每个摘要保留来源类型和稳定来源 ID。", "删除日记后投影立即消失且不影响同日交易标记。"],
        "summary": "已验证财务日历的日记摘要以及删除后的独立刷新。",
        "gaps": ["查看下钻目标和权限", "同日多篇日记摘要排序", "提醒和生日动态样例"],
    },
}


def main() -> None:
    """写出三条日记扩展补充记录。"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for execution_id, spec in RECORDS.items():
        output_path = OUTPUT_DIR / f"{execution_id}-{FILE_SUFFIX}.json"
        output_path.write_text(
            json.dumps(build_record(execution_id, spec), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"generated {len(RECORDS)} diary extended records")


if __name__ == "__main__":
    main()
