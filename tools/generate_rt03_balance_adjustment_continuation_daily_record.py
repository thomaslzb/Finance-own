"""生成 RT-03-024 保存并继续与日常收支转换记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-03-024-20260731T220600+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造运行记录中的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出保存并继续和对账收入/支出转换的动态结论。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-03-024",
        "resource": "TNEWRECTRANSDLGFM",
        "observed_at": "2026-07-31T22:06:00+08:00",
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
                "test-before-rt03-balance-adjustment-continuation-daily-20260731T214529.mh8"
            ),
        },
        "navigation": {
            "entry_point": "账户中心 -> Cash-CNY -> 行操作 -> 余额调整",
            "steps": [
                "从 608.00 基线使用余额调整类型提交真实余额 609.00 并点击保存并继续",
                "观察下一草稿的保留、清空和账面余额刷新规则",
                "选择日常收支，分别提交 +1.00 和 -1.00 差额",
                "核对账户流水、账户中心、全局财务记录和编辑器路由",
                "正常退出并冷启动复核三条记录",
                "依次删除对账支出、对账收入和余额调整，再冷启动复核",
                "等待进程数为 0 后恢复精确基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "默认余额调整保存并继续",
                "status": "observed",
                "observations": (
                    "提交 608.00 -> 609.00 后对话框保持打开；下一草稿保留 Cash-CNY、"
                    "日期和余额调整类型，账面余额刷新为 609.00，真实余额重置 0.00，"
                    "标签和备注清空。关闭空草稿后只生成一条记录。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-savecontinue-first-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-savecontinue-next-draft-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-savecontinue-after-close-cash-ledger-sanitized.png",
                ],
            },
            {
                "name": "日常收支正差额转换",
                "status": "observed",
                "observations": (
                    "账面 609.00、真实 610.00 的 +1.00 差额转换为普通日常收入，"
                    "分类为对账收入；账户和全局记录均显示单边流入 1.00。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-positive-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-positive-account-center-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-positive-financial-records-sanitized.png",
                ],
            },
            {
                "name": "正差额编辑路由",
                "status": "observed",
                "observations": (
                    "修改对账收入记录时打开 TIncExpDlgFm / 日常收入，加载对账收入、"
                    "正金额 1.00、Cash-CNY、日期和备注，不再打开余额调整编辑器。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-positive-edit-routed-income-sanitized.png"
                ],
            },
            {
                "name": "日常收支负差额转换",
                "status": "observed",
                "observations": (
                    "账面 610.00、真实 609.00 的 -1.00 差额转换为普通日常支出，"
                    "分类为对账支出；账户和全局记录均显示单边流出 1.00。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-negative-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-negative-cash-ledger-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-negative-financial-records-sanitized.png",
                ],
            },
            {
                "name": "负差额编辑路由",
                "status": "observed",
                "observations": (
                    "修改对账支出记录时打开 TIncExpDlgFm / 日常支出，加载对账支出、"
                    "正金额 1.00、Cash-CNY、日期和备注。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-daily-negative-edit-routed-expense-sanitized.png"
                ],
            },
            {
                "name": "冷启动与删除恢复",
                "status": "observed",
                "observations": (
                    "三条记录和最终余额 609.00 冷启动保持；依次删除后恢复 Cash-CNY 608.00、"
                    "CASH 9,495.70、净资产 7,095,607.18 和记录数 9，删除态冷启动保持。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-continuation-daily-cold-restart-cash-ledger-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-continuation-daily-cold-restart-financial-records-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-continuation-daily-after-delete-all-account-center-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-continuation-daily-deleted-cold-restart-cash-ledger-sanitized.png",
                ],
            },
        ],
        "commands": [
            {
                "component": "余额调整编辑器",
                "label": "保存并继续",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "提交默认余额调整 +1.00。",
                "confirmation": None,
                "outcome": "提交一条记录并创建使用新账面余额的重置草稿。",
                "status": "pass",
            },
            {
                "component": "差额类型菜单",
                "label": "日常收支",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "分别提交正差额和负差额。",
                "confirmation": None,
                "outcome": "按符号转换为对账收入或对账支出的普通收支交易。",
                "status": "pass",
            },
            {
                "component": "财务记录/账户流水操作菜单",
                "label": "修改",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "分别修改对账收入和对账支出。",
                "confirmation": None,
                "outcome": "路由到日常收入或日常支出编辑器，加载差额绝对值。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": [
                "稳定账户 Cash-CNY、有效日期和当前余额版本",
                "真实余额 609.00、610.00、609.00",
                "差额策略：余额调整或日常收支",
            ],
            "reads": [
                "每次提交前的最新账面余额 608.00、609.00、610.00",
                "账户币种、状态、余额版本和稳定对账分类",
            ],
            "writes": [
                "默认策略写入余额调整事件和流入 1.00",
                "日常收支正差额写入普通收入及对账收入分类",
                "日常收支负差额写入普通支出及对账支出分类",
            ],
            "derived_results": [
                "保存并继续下一草稿账面余额刷新为 609.00",
                "正差额编辑路由为日常收入，负差额编辑路由为日常支出",
                "三条记录净影响 +1.00，删除后所有投影恢复基线",
            ],
            "side_effects": [
                "账户流水、账户中心和全局财务记录立即刷新并通过冷启动保持",
                "对账收入/支出参与普通全局流入和流出汇总",
                "旧 Jet 文件无业务变化的冷启动退出仍可能改变哈希",
            ],
            "rollback": (
                "本轮验证空下一草稿关闭不追加记录、三条记录删除和最终文件级基线恢复；"
                "日常收支保存并继续、零差额、并发冲突和技术失败回滚仍待验证。"
            ),
        },
        "evidence": [
            evidence(
                "manual_note",
                "artifacts/runtime-validation/RT03-balance-adjustment-continuation-daily-notes.md",
                "保存并继续、转换策略、编辑路由、冷启动、删除和哈希时间线。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-balance-savecontinue-next-draft-sanitized.png",
                "默认余额调整保存并继续后的下一草稿字段。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-balance-daily-positive-edit-routed-income-sanitized.png",
                "正差额转换记录路由到日常收入编辑器。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-balance-daily-negative-edit-routed-expense-sanitized.png",
                "负差额转换记录路由到日常支出编辑器。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/test-after-rt03-balance-continuation-daily-verified-20260731T215923.mh8",
                "已通过冷启动复核的三记录状态账簿。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/test-after-rt03-balance-continuation-daily-deleted-20260731T220405.mh8",
                "删除三条测试记录后的业务基线状态账簿。",
            ),
        ],
        "requirements_update": [
            "默认余额调整保存并继续必须刷新账面余额版本，保留账户、日期和类型，清空交易字段。",
            "日常收支是差额到普通收支的转换策略，不能与余额调整事件使用同一后续生命周期。",
            "正差额创建普通收入和稳定对账收入分类，负差额创建普通支出和稳定对账支出分类。",
            "转换后修改必须路由到通用收支编辑器并以差额绝对值作为正金额。",
            "差额计算与普通收支创建必须原子完成，不能同时留下重复余额调整事件。",
            "对账分类必须使用稳定 ID，不能依赖显示文字决定方向或编辑器路由。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证默认余额调整保存并继续，以及日常收支正负差额转换为"
                "对账收入/对账支出并路由通用收支生命周期的完整数据流。"
            ),
            "remaining_gaps": [
                "日常收支模式的保存并继续字段规则",
                "两个差额类型的零差额行为",
                "对账收入/支出的全部报表、预算、税务、标签和导出口径",
                "历史未来日期、多币种、关闭账户、并发冲突和故障回滚",
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
