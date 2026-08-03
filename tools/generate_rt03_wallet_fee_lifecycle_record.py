"""生成 RT-03-026 钱包充值手续费修改与删除生命周期记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-03-026-20260731T195000+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造运行记录中的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出充值手续费创建、差额修改、删除冲销和冷启动结果。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-03-026",
        "resource": "TRECHARGEDLGFM",
        "observed_at": "2026-07-31T19:50:00+08:00",
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
                "test-before-rt03-wallet-fee-lifecycle-20260731T194600.mh8"
            ),
        },
        "navigation": {
            "entry_point": "微信钱包流水 -> 选中本轮充值 -> 操作 -> 修改/删除",
            "steps": [
                "从 D8E4...165AC 基线创建本金 1.00、手续费 0.10 的充值记录",
                "通过当前账户流水操作菜单位置 0 打开 TRechargeDlgFm / 充值",
                "把手续费从 0.10 修改为 0.20，并修改唯一备注后保存",
                "正常退出并从修改态账簿冷启动复核余额和记录",
                "通过操作菜单位置 1 打开删除确认框并选择是",
                "核对记录消失、账户余额和净资产恢复，再冷启动复核",
                "等待 MoneyHome8 进程数为 0 后恢复精确基线 SHA-256",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "初始充值手续费记录",
                "status": "observed",
                "observations": (
                    "本金 1.00、手续费 0.10 保存后，Cash-CNY 为 606.90，"
                    "微信钱包为 2,987.44，净资产为 7,095,607.08。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-create-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-after-create-wallet-sanitized.png",
                ],
            },
            {
                "name": "修改按差额重算",
                "status": "observed",
                "observations": (
                    "手续费 0.10 -> 0.20 后，钱包本金和余额保持，Cash-CNY 与 CASH 分组"
                    "各再减少 0.10，净资产也只再减少 0.10；备注替换为 modified 版本。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-modify-before-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-modify-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-cold-restart-modified-balances-sanitized.png",
                ],
            },
            {
                "name": "修改态冷启动持久化",
                "status": "observed",
                "observations": (
                    "修改态正常退出 SHA-256 为 8B8E...E83DF；冷启动后手续费 0.20 对应的"
                    "钱包记录、Cash-CNY 606.80、CASH 9,494.50 和净资产 7,095,606.98 保持。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/backups/test-after-rt03-wallet-fee-lifecycle-modified-20260731T195900.mh8",
                    "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-cold-restart-modified-wallet-sanitized.png",
                ],
            },
            {
                "name": "删除确认与完整冲销",
                "status": "observed",
                "observations": (
                    "删除前显示“您确定删除此记录吗？”并提供是/否。确认后测试行消失，"
                    "钱包恢复 2,986.44、Cash-CNY 608.00、CASH 9,495.70、净资产 7,095,607.18。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-delete-confirmation-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-cold-restart-deleted-wallet-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-cold-restart-deleted-balances-sanitized.png",
                ],
            },
            {
                "name": "删除态冷启动与基线恢复",
                "status": "observed",
                "observations": (
                    "删除态首次退出 SHA-256 为 3AEF...FC1D，冷启动后记录仍不存在且业务投影保持基线。"
                    "最终等待所有 MoneyHome8 进程退出后恢复 test.mh8 到 D8E4...165AC；"
                    "软件生成的 ~$test 仅观察，未手工处理。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/backups/test-after-rt03-wallet-fee-lifecycle-deleted-20260731T200300.mh8",
                    "artifacts/runtime-validation/RT03-wallet-fee-lifecycle-notes.md",
                ],
            },
        ],
        "commands": [
            {
                "component": "账户流水操作菜单",
                "label": "修改",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "选中新建充值行并选择菜单位置 0。",
                "confirmation": None,
                "outcome": "打开已加载原记录的 TRechargeDlgFm / 充值。",
                "status": "pass",
            },
            {
                "component": "充值编辑器",
                "label": "确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "把手续费改为 0.20 并提交。",
                "confirmation": None,
                "outcome": "只按手续费增量 0.10 重算来源、分组和净资产。",
                "status": "pass",
            },
            {
                "component": "账户流水操作菜单",
                "label": "删除",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "选中修改后的充值行并选择菜单位置 1。",
                "confirmation": "您确定删除此记录吗？",
                "outcome": "确认后删除交易并完整反向重建所有相关投影。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": [
                "原 wallet_recharge 稳定交易 ID 与当前版本",
                "原本金 1.00、原手续费 0.10、修改后手续费 0.20",
                "原钱包账户、资金来源账户、日期和备注关系",
            ],
            "reads": [
                "原交易头、分录组成、账户余额版本和关联投影",
                "修改或删除提交时的最新账簿版本",
            ],
            "writes": [
                "修改后的手续费组成和备注",
                "来源账户、账户组、净资产和查询投影的差额更新",
                "删除确认后的交易撤销状态或等价审计事件",
            ],
            "derived_results": [
                "修改后钱包 2,987.44、Cash-CNY 606.80、CASH 9,494.50",
                "修改后净资产 7,095,606.98",
                "删除后钱包、Cash-CNY、CASH、净资产和记录数全部恢复基线",
            ],
            "side_effects": [
                "修改和删除后当前流水立即刷新，并在冷启动后保持",
                "删除要求显式确认，取消分支本轮未执行",
                "Jet 打开关闭会改变具体文件哈希，验收比较业务事实",
            ],
            "rollback": (
                "本轮验证成功修改、成功删除和最终文件级基线恢复；取消删除、"
                "并发版本冲突、数据库失败和进程崩溃回滚仍待验证。"
            ),
        },
        "evidence": [
            evidence(
                "manual_note",
                "artifacts/runtime-validation/RT03-wallet-fee-lifecycle-notes.md",
                "修改差额、删除冲销、冷启动、文件锁和基线恢复时间线。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-modify-filled-sanitized.png",
                "手续费从 0.10 改为 0.20 的编辑器状态。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-cold-restart-modified-balances-sanitized.png",
                "修改态冷启动后的来源、分组和净资产。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-delete-confirmation-sanitized.png",
                "删除记录前的显式确认。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-wallet-fee-lifecycle-cold-restart-deleted-wallet-sanitized.png",
                "删除态冷启动后测试行不存在且钱包恢复基线。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/test-after-rt03-wallet-fee-lifecycle-modified-20260731T195900.mh8",
                "已通过冷启动复核的修改态账簿。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/test-after-rt03-wallet-fee-lifecycle-deleted-20260731T200300.mh8",
                "已通过冷启动复核的删除态账簿。",
            ),
        ],
        "requirements_update": [
            "交易修改必须以稳定交易 ID 和版本为条件，在一个事务中更新本金、费用、备注和所有投影。",
            "手续费由 0.10 改为 0.20 时只应用净差额 0.10，不得重复过账本金。",
            "删除充值必须先显示确认，并完整撤销本金与手续费对所有账户、分组、净资产和查询投影的影响。",
            "修改和删除后必须可从领域事实确定性重建冷启动投影。",
            "审计层应保留创建、修改前后值和删除操作者；旧界面是否物理删除不能作为 Rust 版丢失历史的理由。",
            "提交必须检查账簿或交易版本；并发冲突时拒绝覆盖并保留编辑草稿。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证钱包充值手续费记录从创建、手续费差额修改到删除完整冲销的生命周期，"
                "修改态和删除态均通过冷启动复核。"
            ),
            "remaining_gaps": [
                "删除确认的否分支与编辑取消分支",
                "提现记录修改删除、费用报表分类和余额调整关系",
                "重复提交、并发冲突、数据库失败和崩溃中断回滚",
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
