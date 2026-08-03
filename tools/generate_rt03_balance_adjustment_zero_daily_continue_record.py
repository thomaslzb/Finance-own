"""生成 RT-03-024 零差额与日常收支保存并继续运行记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-03-024-20260731T225800+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造可被运行记录 schema 校验的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出零差额、续记状态和删除恢复的动态结论。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-03-024",
        "resource": "TNEWRECTRANSDLGFM",
        "observed_at": "2026-07-31T22:58:00+08:00",
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8",
            "sha256_before": "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC",
            "sha256_after": "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC",
            "backup_artifact": (
                "artifacts/runtime-validation/backups/"
                "test-before-rt03-balance-zero-daily-continue-20260731T222430.mh8"
            ),
        },
        "navigation": {
            "entry_point": "账户中心 -> Cash-CNY -> 行操作 -> 余额调整",
            "steps": [
                "分别用默认余额调整和日常收支提交 608.00 -> 608.00 的零差额",
                "用日常收支保存并继续分别提交 +1.00 和 -1.00 差额",
                "观察提交后仍保持打开的草稿字段和账面余额显示",
                "正常退出并冷启动复核四条记录、余额和记录数",
                "通过财务记录标准删除命令依次删除四条测试记录",
                "再次冷启动复核删除态并恢复精确基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "默认余额调整零差额",
                "status": "observed",
                "observations": (
                    "账面和真实余额均为 608.00 时确定不报错，生成零金额余额调整记录；"
                    "账户记录数 9 -> 10，全局记录数 23 -> 24，余额、CASH 和净资产不变。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-zero-default-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-zero-default-after-submit-main-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-zero-default-financial-records-sanitized.png",
                ],
            },
            {
                "name": "日常收支零差额",
                "status": "observed",
                "observations": (
                    "账面和真实余额均为 608.00 时确定不报错，生成零金额普通对账收入；"
                    "记录数继续各增加一条而所有金额投影不变，确认 delta == 0 归入收入。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-zero-daily-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-zero-daily-after-submit-cash-ledger-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-zero-daily-financial-records-sanitized.png",
                ],
            },
            {
                "name": "日常收支正差额保存并继续",
                "status": "observed",
                "observations": (
                    "608.00 -> 609.00 提交普通对账收入 1.00 并保持编辑器打开；旧界面保留"
                    "账户、日期、类型、真实余额 609.00 和原备注，同时仍显示陈旧账面 608.00。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-continue-plus-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-continue-after-plus-draft-sanitized.png",
                ],
            },
            {
                "name": "日常收支负差额保存并继续",
                "status": "observed",
                "observations": (
                    "重新从 609.00 -> 608.00 提交普通对账支出 1.00；下一草稿同样保留真实余额、"
                    "备注和陈旧账面 609.00，证明这是可复现的旧版状态同步缺陷。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-continue-minus-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-continue-after-minus-draft-sanitized.png",
                ],
            },
            {
                "name": "冷启动、删除与精确恢复",
                "status": "observed",
                "observations": (
                    "四条记录冷启动保持，Cash-CNY 最终仍为 608.00，账户记录数 13、全局记录数 27；"
                    "四条记录均可通过标准删除确认清理，删除态冷启动恢复账户记录数 9、全局记录数 23，"
                    "最终账簿恢复到初始长度和 SHA-256。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-zero-daily-continue-cold-restart-cash-ledger-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-zero-daily-continue-delete-bottom-selected-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-zero-after-delete-all-account-center-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-zero-deleted-cold-restart-cash-ledger-sanitized.png",
                ],
            },
        ],
        "commands": [
            {
                "component": "余额调整编辑器",
                "label": "确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "分别提交默认策略和日常收支策略的零差额。",
                "confirmation": None,
                "outcome": "两个策略都创建可查询和可删除的零金额记录。",
                "status": "pass",
            },
            {
                "component": "差额类型菜单",
                "label": "日常收支",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "提交零、正和负差额。",
                "confirmation": None,
                "outcome": "负差额转对账支出，其余差额转对账收入。",
                "status": "pass",
            },
            {
                "component": "余额调整编辑器",
                "label": "保存并继续",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "在日常收支模式分别提交 +1.00 和 -1.00。",
                "confirmation": None,
                "outcome": "提交成功并保持编辑器打开，但旧界面留下已提交字段和陈旧账面显示。",
                "status": "partial",
            },
            {
                "component": "财务记录操作菜单",
                "label": "删除",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "依次删除两条零金额和两条非零测试记录。",
                "confirmation": "标准删除确认框选择是。",
                "outcome": "四条记录均被完整删除，金额和记录数投影恢复业务基线。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": [
                "Cash-CNY、有效日期和当前账面余额版本",
                "真实余额 608.00、609.00 和 608.00",
                "差额策略：余额调整或日常收支",
            ],
            "reads": [
                "提交时显示的账面余额 608.00 或 609.00",
                "账户币种、状态、余额版本和稳定对账分类",
            ],
            "writes": [
                "默认策略写入零金额余额调整事件",
                "日常收支零差额写入零金额普通对账收入",
                "正差额写入普通对账收入，负差额写入普通对账支出",
            ],
            "derived_results": [
                "delta < 0 时为 reconciliation_expense，否则为 reconciliation_income",
                "零金额事实参与记录数、查询、审计和删除，不改变余额或汇总金额",
                "日常收支保存并继续的提交结果正确，但旧页面草稿显示未与新余额版本同步",
            ],
            "side_effects": [
                "账户流水和全局财务记录立即增加并在冷启动后保持",
                "标准删除完整撤销四条测试事实并恢复记录数",
                "旧 Jet 文件删除态冷启动退出会改变哈希，但业务投影保持基线",
            ],
            "rollback": (
                "四条记录已标准删除并通过删除态冷启动复核，随后将 test.mh8 恢复为"
                "初始 18,669,568 字节及 D8E4...165AC；未测试陈旧草稿的未修改重复提交。"
            ),
        },
        "evidence": [
            evidence(
                "manual_note",
                "artifacts/runtime-validation/RT03-balance-adjustment-zero-daily-continue-notes.md",
                "零差额、日常收支续记缺陷、删除和文件指纹时间线。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-balance-zero-daily-continue-delete-bottom-selected-sanitized.png",
                "冷启动后同时存在两条零金额与两条非零记录。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-balance-daily-continue-after-plus-draft-sanitized.png",
                "日常收支正差额保存并继续后的陈旧草稿。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/test-after-rt03-balance-zero-daily-continue-verified-20260731T224600.mh8",
                "已通过冷启动复核的四记录状态账簿。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/test-after-rt03-balance-zero-daily-continue-deleted-20260731T225500.mh8",
                "标准删除四条记录后的业务基线状态账簿。",
            ),
        ],
        "requirements_update": [
            "两个差额策略都必须允许 delta == 0，并保留可审计的零金额事实。",
            "日常收支分类规则固定为 delta < 0 进入对账支出，否则进入对账收入。",
            "零金额事实参与记录数、查询、审计、迁移和删除，但不改变金额投影。",
            "日常收支保存并继续必须原子提交当前事实并保持编辑器打开。",
            "Rust 下一草稿应读取提交后的权威余额版本，保留账户、日期和策略，清空真实余额、标签、备注和附件。",
            "旧版陈旧账面显示和已提交字段保留属于缺陷，不能作为兼容目标。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已确认默认和日常收支零差额均真实入账，以及日常收支正负差额"
                "保存并继续、冷启动、标准删除和精确账簿恢复。"
            ),
            "remaining_gaps": [
                "在未修改陈旧草稿时再次提交的旧程序行为",
                "零金额对账收入在报表、预算、税务、标签、附件和导出中的完整口径",
                "历史/未来日期、多币种、关闭账户、版本冲突、重复提交和技术失败回滚",
            ],
        },
    }
    OUTPUT.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
