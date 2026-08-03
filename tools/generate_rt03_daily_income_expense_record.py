"""生成 RT-03-016 日常收入与支出真实保存记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-03-016-20260731T161524+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造运行记录中的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出通用日常收支编辑器两个方向的保存与持久性结论。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-03-016",
        "resource": "TINCEXPDLGFM",
        "observed_at": "2026-07-31T16:15:24+08:00",
        "application": {
            "executable": (
                r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe"
            ),
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8",
            "sha256_before": (
                "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
            ),
            "sha256_after": (
                "ED9442940B2F9489D5BA41D3705BA248A833E7CA83272AB5BD5BA3E5C584B643"
            ),
            "backup_artifact": (
                "artifacts/runtime-validation/backups/"
                "test-before-rt03-daily-expense-20260731.mh8"
            ),
        },
        "navigation": {
            "entry_point": "顶部记账菜单 -> 日常收支（命令 ID 104）",
            "steps": [
                "收入和支出分别从同一 test.mh8 基线建立独立备份",
                "打开日常收支并在收支项目下拉中切换收入或支出分类",
                "从真实账户候选列表绑定 Cash-CNY",
                "分别保存其它收入 3.00 CNY 和教育培训支出 2.00 CNY",
                "核对账户余额、CASH 分组折算值和全局财务记录",
                "分别正常退出、冷启动复核并保存成功状态副本",
                "每次会话结束后恢复相同基线并核对进程与文件指纹",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "日常收入有效保存",
                "status": "observed",
                "observations": (
                    "选择其它收入、Cash-CNY 和 3.00 CNY 后，窗体标题切换为日常收入；"
                    "保存后 Cash-CNY 608.00 -> 611.00，CASH 分组 9,495.70 -> "
                    "9,498.70，全局记录为单边流入 3.00。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-daily-income-filled.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-daily-income-balances-after-restart-sanitized.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-daily-income-global-after-restart-sanitized.png",
                ],
            },
            {
                "name": "日常支出有效保存",
                "status": "observed",
                "observations": (
                    "选择教育培训、Cash-CNY 和 2.00 CNY 后，窗体标题切换为日常支出；"
                    "保存后 Cash-CNY 608.00 -> 606.00，CASH 分组 9,495.70 -> "
                    "9,493.70，全局记录为单边流出 2.00。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-daily-expense-filled.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-daily-expense-balances-after-restart-sanitized.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-daily-expense-global-after-restart-sanitized.png",
                ],
            },
            {
                "name": "分类决定方向与共享字段",
                "status": "observed",
                "observations": (
                    "同一 TIncExpDlgFm 和 TIncExpEditFrame 使用项目、金额、账户、标签、"
                    "日期、备注和附件字段。空白草稿标题为日常收支，选中收入或支出项目后"
                    "分别切换为日常收入或日常支出；两个方向都录入正金额。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-daily-income-filled.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-daily-expense-filled.png",
                ],
            },
            {
                "name": "冷启动持久性与基线恢复",
                "status": "observed",
                "observations": (
                    "收入状态首次关闭哈希为 C2BE...15987，冷启动验证哈希为 "
                    "D814...1D26；支出状态首次关闭哈希为 47F0...3B75，冷启动验证"
                    "哈希为 ED94...B643。两次最终均恢复 D8E4...165AC 基线，"
                    "MoneyHome8 进程数为 0。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/backups/"
                    "test-after-rt03-daily-income-verified-20260731.mh8",
                    "artifacts/runtime-validation/backups/"
                    "test-after-rt03-daily-expense-verified-20260731.mh8",
                    "artifacts/runtime-validation/RT03-daily-income-expense-notes.md",
                ],
            },
        ],
        "commands": [
            {
                "component": "顶部记账菜单",
                "label": "日常收支",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "投递命令 ID 104。",
                "confirmation": None,
                "outcome": "打开空白 TIncExpDlgFm，选择分类后切换交易方向。",
                "status": "pass",
            },
            {
                "component": "收支项目选择器",
                "label": "支出 / 收入 / 搜索",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "分别选择其它收入和搜索教育培训。",
                "confirmation": None,
                "outcome": "绑定分类对象并切换父窗标题与提交方向。",
                "status": "pass",
            },
            {
                "component": "确定按钮",
                "label": "确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "收入和支出场景分别提交一次。",
                "confirmation": None,
                "outcome": "原子写入单边账户分录并关闭编辑器。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": [
                "稳定分类 ID 及分类方向",
                "稳定账户 ID：Cash-CNY",
                "正金额、日期、可选标签、备注和附件关系",
            ],
            "reads": [
                "分类所属收入或支出方向",
                "账户身份、状态、币种和提交前余额 608.00",
            ],
            "writes": [
                "日常收入或日常支出交易头",
                "Cash-CNY 单边流入 +3.00 或单边流出 -2.00 的账户分录",
                "分类、日期、标签、备注、附件和审计关系",
            ],
            "derived_results": [
                "收入场景余额 611.00、CASH 分组 9,498.70",
                "支出场景余额 606.00、CASH 分组 9,493.70",
                "全局活动类型分别为其它收入和教育培训",
            ],
            "side_effects": [
                "账户中心和全局财务记录立即刷新并在冷启动后保持",
                "本位币 CNY 在全局列表的币种显示列为空",
            ],
            "rollback": (
                "本轮验证两个 CNY 正常提交路径和最终基线恢复；保存并继续、附件、"
                "分期、修改删除、校验失败、重复提交、并发冲突和故障回滚仍待验证。"
            ),
        },
        "evidence": [
            evidence(
                "manual_note",
                "artifacts/runtime-validation/RT03-daily-income-expense-notes.md",
                "输入、余额、流水、冷启动、哈希和基线恢复时间线。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-daily-income-filled.png",
                "其它收入 3.00 CNY 提交前的完整测试字段。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-daily-income-balances-after-restart-sanitized.png",
                "收入冷启动后的 Cash-CNY 余额和 CASH 分组。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-daily-income-global-after-restart-sanitized.png",
                "收入冷启动后的单边流入记录。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-daily-expense-filled.png",
                "教育培训支出 2.00 CNY 提交前的完整测试字段。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-daily-expense-balances-after-restart-sanitized.png",
                "支出冷启动后的 Cash-CNY 余额和 CASH 分组。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-daily-expense-global-after-restart-sanitized.png",
                "支出冷启动后的单边流出记录。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/"
                "test-after-rt03-daily-income-verified-20260731.mh8",
                "已通过冷启动复核的日常收入成功状态账簿。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/"
                "test-after-rt03-daily-expense-verified-20260731.mh8",
                "已通过冷启动复核的日常支出成功状态账簿。",
            ),
        ],
        "requirements_update": [
            "通用收支草稿必须保存显式 transaction_kind，不能在提交后仅靠分类名称反推方向。",
            "分类选择必须绑定稳定 ID，并在事务内校验分类仍属于草稿方向。",
            "收入和支出都接收正金额，领域层按 transaction_kind 生成单边流入或流出。",
            "账户选择必须绑定稳定 ID，币种由账户确定并在提交时再次校验。",
            "交易头、账户分录、分类、标签、备注、附件关系和审计信息必须原子提交。",
            "余额、分组折算和全局流水必须从同一已提交事实重建并通过冷启动保持一致。",
            "本位币即使在列表隐藏币种文字，交易、分录、接口、导出和审计仍必须保存 CNY。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证 TIncExpDlgFm 的日常收入和日常支出两个 CNY 正常提交方向，"
                "包括分类切换、账户绑定、单边分录、余额与全局投影、冷启动和基线恢复。"
            ),
            "remaining_gaps": [
                "保存并继续的连续草稿重置和重复提交保护",
                "标签、附件和信用卡分期关系的真实保存",
                "零负金额、缺少分类、无效账户和日期边界",
                "修改、删除、退款、冲销和跨报表重建",
                "并发冲突、数据库失败和崩溃中断的完整原子回滚",
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
