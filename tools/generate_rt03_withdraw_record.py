"""生成 RT-03-004 取款与手续费真实保存记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-03-004-20260731T163739+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造运行记录中的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出同币种取款本金和来源手续费的持久化结论。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-03-004",
        "resource": "TCASHWITHDRAWDLGFM",
        "observed_at": "2026-07-31T16:37:39+08:00",
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
                "C254269F3476EE1E8126F9CDF32234D7630C26573ACB6530E31DEB72DD47FB38"
            ),
            "backup_artifact": (
                "artifacts/runtime-validation/backups/"
                "test-before-rt03-withdraw-20260731.mh8"
            ),
        },
        "navigation": {
            "entry_point": "顶部记账菜单 -> 取款（命令 ID 110）",
            "steps": [
                "从 test.mh8 基线建立取款前备份",
                "打开 TCashWithdrawDlgFm 并从真实候选列表选择顺德农行",
                "确认可用资金为 100.00 CNY，选择资金去向 Cash-CNY",
                "输入取款本金 4.00、手续费 1.00 和唯一备注",
                "确认手续费支出账户自动跟随顺德农行",
                "保存后核对两侧余额、账户组、净资产和全局流水",
                "正常退出、冷启动复核并保存成功状态副本",
                "恢复基线并核对主库、恢复文件和进程状态",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "来源账户与可用资金联动",
                "status": "observed",
                "observations": (
                    "从真实候选列表选择顺德农行后，可用资金刷新为 100.00 CNY，"
                    "手续费支出账户自动默认为同一来源账户。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-withdraw-filled.png"
                ],
            },
            {
                "name": "取款与来源手续费有效保存",
                "status": "observed",
                "observations": (
                    "保存本金 4.00 CNY 和来源手续费 1.00 CNY 后，顺德农行 "
                    "100.00 -> 95.00，Cash-CNY 608.00 -> 612.00；CASH 分组增加"
                    "4.00，中国银行分组减少 5.00，净资产减少 1.00。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-withdraw-balances-after-restart-sanitized.png"
                ],
            },
            {
                "name": "全局取款投影",
                "status": "observed",
                "observations": (
                    "全局财务记录以一个取款业务身份显示流入 4.00、流出 5.00、"
                    "资产账户顺德农行->Cash-CNY 和唯一备注；本位币显示列为空。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-withdraw-global-after-restart-sanitized.png"
                ],
            },
            {
                "name": "冷启动持久性与基线恢复",
                "status": "observed",
                "observations": (
                    "首次正常退出哈希为 8C1E...C287，冷启动验证哈希为 "
                    "C254...FB38；余额和全局流水保持。最终恢复 D8E4...165AC "
                    "基线，MoneyHome8 进程数为 0。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/backups/"
                    "test-after-rt03-withdraw-verified-20260731.mh8",
                    "artifacts/runtime-validation/RT03-withdraw-notes.md",
                ],
            },
        ],
        "commands": [
            {
                "component": "顶部记账菜单",
                "label": "取款",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "投递命令 ID 110。",
                "confirmation": None,
                "outcome": "打开专用 TCashWithdrawDlgFm。",
                "status": "pass",
            },
            {
                "component": "取款账户选择器",
                "label": "顺德农行",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "从真实候选列表搜索并选择稳定账户对象。",
                "confirmation": None,
                "outcome": "可用资金刷新为 100.00，手续费账户自动跟随。",
                "status": "pass",
            },
            {
                "component": "确定按钮",
                "label": "确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "提交本金 4.00 和手续费 1.00。",
                "confirmation": None,
                "outcome": "原子更新两侧资金、费用和统一取款投影。",
                "status": "pass",
            },
            {
                "component": "全部取完复选框",
                "label": "全部取完",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "本轮未触发。",
                "confirmation": None,
                "outcome": "余额快照、手续费和超额利息规则仍待验证。",
                "status": "pending",
            },
        ],
        "data_flow": {
            "inputs": [
                "稳定来源账户 ID：顺德农行",
                "稳定资金去向账户 ID：Cash-CNY",
                "本金 4.00 CNY、手续费 1.00 CNY",
                "手续费支出账户 ID：顺德农行",
                "日期、可选标签、备注和附件关系",
            ],
            "reads": [
                "来源账户状态、币种和同一版本的可用资金 100.00",
                "目标账户状态和币种",
            ],
            "writes": [
                "一个取款交易头",
                "顺德农行本金流出 4.00 和手续费流出 1.00",
                "Cash-CNY 本金流入 4.00",
                "日期、标签、备注、附件和审计关系",
            ],
            "derived_results": [
                "顺德农行余额 95.00，Cash-CNY 余额 612.00",
                "CASH 分组 9,499.70，中国银行分组 337,755.19",
                "全局取款流入 4.00、流出 5.00",
            ],
            "side_effects": [
                "账户中心和全局财务记录立即刷新并在冷启动后保持",
                "净资产只减少手续费 1.00",
                "本位币 CNY 在旧全局列表隐藏币种文字",
            ],
            "rollback": (
                "本轮验证正常路径和最终基线恢复；全部取完、超额利息、余额不足、"
                "第三手续费账户、修改删除、并发冲突和故障回滚仍待验证。"
            ),
        },
        "evidence": [
            evidence(
                "manual_note",
                "artifacts/runtime-validation/RT03-withdraw-notes.md",
                "输入、账户联动、余额、流水、哈希和基线恢复时间线。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-withdraw-filled.png",
                "取款本金、手续费、来源、去向和自动手续费账户。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-withdraw-balances-after-restart-sanitized.png",
                "冷启动后的来源与目标余额及账户组变化。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-withdraw-global-after-restart-sanitized.png",
                "冷启动后的统一取款流入/流出投影。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/"
                "test-after-rt03-withdraw-verified-20260731.mh8",
                "已通过冷启动复核的取款成功状态账簿。",
            ),
        ],
        "requirements_update": [
            "取款必须保存显式业务身份、来源账户、资金去向、本金和手续费组成。",
            "账户选择必须绑定稳定 ID；可用资金必须来自同一提交版本的余额快照。",
            "来源本金、目标本金和手续费必须在单个数据库事务内原子提交。",
            "来源账户承担手续费时来源总流出等于本金加手续费，目标只增加本金。",
            "净资产只减少费用；本金在资产账户之间移动不得计入收入或支出。",
            "列表可合并显示流入 4.00/流出 5.00，但领域事实必须保留独立组成。",
            "本位币即使隐藏显示文字，交易、分录、接口、导出和审计仍必须保存 CNY。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证顺德农行到 Cash-CNY 的 4.00 CNY 取款和 1.00 CNY "
                "来源手续费，包括账户联动、双边资金、费用、全局投影、冷启动和基线恢复。"
            ),
            "remaining_gaps": [
                "全部取完的同一余额快照、手续费扣除和草稿联动",
                "超过可用资金时的利息生成与到期选项",
                "零负金额、余额不足、同账户和币种不兼容校验",
                "手续费由第三账户承担的余额与报表口径",
                "修改、删除、退款、并发冲突和数据库失败回滚",
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
