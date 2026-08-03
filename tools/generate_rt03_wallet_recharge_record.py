"""生成 RT-03-026 第三方钱包充值真实保存记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-03-026-20260731T174810+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造运行记录中的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出 Cash-CNY 到微信钱包的最小充值持久化结论。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-03-026",
        "resource": "TRECHARGEDLGFM",
        "observed_at": "2026-07-31T17:48:10+08:00",
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
                "30A8D2AD3C287F19F01292E4BD329177DA079E57998F9788961A4674113B8424"
            ),
            "backup_artifact": (
                "artifacts/runtime-validation/backups/"
                "test-before-rt03-wallet-recharge-20260731T173206.mh8"
            ),
        },
        "navigation": {
            "entry_point": (
                "记账 -> 更多交易活动 -> 支付宝、微信钱包 -> 充值（命令 ID 135）"
            ),
            "steps": [
                "从 D8E4...165AC 基线建立充值前备份",
                "初始化位置 14 的动态子菜单并把钱包分组位置 3 映射到命令 135/136",
                "用命令 135 打开 TRechargeDlgFm / 充值",
                "保留默认微信钱包并从真实候选列表选择 Cash-CNY",
                "输入本金 2.00、手续费 0.00 和唯一备注后确定保存",
                "核对 Cash-CNY、CASH 分组、微信钱包和全局财务记录",
                "正常退出、冷启动复核并保留两份成功状态账簿",
                "恢复操作前基线并核对进程数和 SHA-256",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "动态菜单与命令映射",
                "status": "observed",
                "observations": (
                    "更多交易活动在 WM_INITMENUPOPUP 后生成 22 个业务分组；"
                    "钱包分组位置 3 的命令 135/136 分别对应充值和提现。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/RT03-wallet-recharge-notes.md"
                ],
            },
            {
                "name": "稳定账户候选与有效提交",
                "status": "observed",
                "observations": (
                    "充值账户默认微信钱包；资金来源通过真实候选列表选择 Cash-CNY。"
                    "提交本金 2.00 CNY、手续费 0.00 后窗口正常关闭。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-wallet-recharge-live-filled.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-wallet-recharge-source-dropdown-sanitized.png",
                ],
            },
            {
                "name": "双边余额与账户流水",
                "status": "observed",
                "observations": (
                    "Cash-CNY 608.00 -> 606.00，CASH 分组 9,495.70 -> 9,493.70；"
                    "微信钱包 2,986.44 -> 2,988.44，并新增充值|Cash-CNY 流入 2.00。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-wallet-recharge-balances-after-restart-sanitized.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-wallet-recharge-wallet-after-restart-sanitized.png",
                ],
            },
            {
                "name": "全局充值投影",
                "status": "observed",
                "observations": (
                    "全局财务记录显示充值流入 2.00、流出 2.00、账户链 "
                    "Cash-CNY->微信钱包和唯一备注；本位币显示列为空。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-wallet-recharge-global-after-restart-sanitized.png"
                ],
            },
            {
                "name": "冷启动持久性与基线恢复",
                "status": "observed",
                "observations": (
                    "冷启动后余额和流水保持。首次退出哈希 F793...3E04，二次退出哈希 "
                    "30A8...424；Jet 会在无业务变化的打开/关闭周期改写文件。最终恢复 "
                    "D8E4...165AC 基线，MoneyHome8 进程数为 0。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/backups/"
                    "test-after-rt03-wallet-recharge-verified-20260731.mh8",
                    "artifacts/runtime-validation/backups/"
                    "test-after-rt03-wallet-recharge-cold-restart-20260731.mh8",
                    "artifacts/runtime-validation/RT03-wallet-recharge-notes.md",
                ],
            },
        ],
        "commands": [
            {
                "component": "第三方钱包子菜单",
                "label": "充值",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "投递命令 ID 135。",
                "confirmation": None,
                "outcome": "唯一打开 TRechargeDlgFm / 充值。",
                "status": "pass",
            },
            {
                "component": "资金来源账户选择器",
                "label": "Cash-CNY",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "从 TmwSelectAccountDrop 的真实候选列表选择首项。",
                "confirmation": None,
                "outcome": "编辑器回读稳定候选 Cash-CNY，并允许提交。",
                "status": "pass",
            },
            {
                "component": "确定按钮",
                "label": "确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "提交本金 2.00 和手续费 0.00。",
                "confirmation": None,
                "outcome": "原子更新来源和钱包本金并生成统一充值投影。",
                "status": "pass",
            },
            {
                "component": "保存并继续按钮",
                "label": "保存并继续",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "本轮未触发。",
                "confirmation": None,
                "outcome": "成功后的字段保留和草稿重置策略仍待验证。",
                "status": "pending",
            },
        ],
        "data_flow": {
            "inputs": [
                "稳定钱包账户 ID：微信钱包",
                "稳定资金来源账户 ID：Cash-CNY",
                "本金 2.00 CNY、手续费 0.00 CNY",
                "日期、可选标签、备注和附件关系",
            ],
            "reads": [
                "钱包账户状态和币种",
                "资金来源账户状态、币种和余额版本",
            ],
            "writes": [
                "一个显式 wallet_recharge 交易头",
                "Cash-CNY 本金流出 2.00",
                "微信钱包本金流入 2.00",
                "日期、标签、备注、附件和审计关系",
            ],
            "derived_results": [
                "Cash-CNY 余额 606.00，微信钱包余额 2,988.44",
                "CASH 分组 9,493.70，净资产不变",
                "全局充值流入 2.00、流出 2.00",
            ],
            "side_effects": [
                "账户中心、钱包流水和全局财务记录立即刷新并在冷启动后保持",
                "旧全局列表对本位币 CNY 隐藏币种文字",
                "Jet 打开关闭周期可能改写文件哈希但不改变业务事实",
            ],
            "rollback": (
                "本轮验证正常充值路径和最终基线恢复；手续费、提现、余额不足、"
                "同账户、币种不兼容、重复提交、并发冲突和故障回滚仍待验证。"
            ),
        },
        "evidence": [
            evidence(
                "manual_note",
                "artifacts/runtime-validation/RT03-wallet-recharge-notes.md",
                "命令定位、输入、余额、流水、哈希变化和基线恢复时间线。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-wallet-recharge-live-filled.png",
                "钱包、资金来源、本金、手续费、日期和唯一备注。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-wallet-recharge-wallet-after-restart-sanitized.png",
                "冷启动后的微信钱包余额和充值流水。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-wallet-recharge-balances-after-restart-sanitized.png",
                "冷启动后的 Cash-CNY 和 CASH 分组余额。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-wallet-recharge-global-after-restart-sanitized.png",
                "冷启动后的统一充值流入/流出投影。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/"
                "test-after-rt03-wallet-recharge-cold-restart-20260731.mh8",
                "已通过冷启动业务复核的钱包充值成功状态账簿。",
            ),
        ],
        "requirements_update": [
            "钱包充值必须保存显式 wallet_recharge 业务身份和稳定两侧账户 ID。",
            "资金来源本金流出和钱包本金流入必须在一个数据库事务内原子提交。",
            "本金移动不改变净资产，也不得计入收入或支出。",
            "查询投影可同时显示流入和流出，但领域事实必须保留独立双边分录。",
            "本位币即使隐藏显示文字，交易、分录、接口、导出和审计仍必须保存 CNY。",
            "冷启动验收必须比较业务事实；Jet 文件哈希只标识具体证据副本。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证 Cash-CNY 到微信钱包的 2.00 CNY 零手续费充值，"
                "包括动态命令、稳定账户候选、双边余额、统一流水、冷启动和基线恢复。"
            ),
            "remaining_gaps": [
                "充值手续费的承担账户、余额和费用报表口径",
                "钱包提现的真实保存和反向双边资金流",
                "保存并继续的字段保留与草稿重置",
                "零负金额、余额不足、同账户和币种不兼容校验",
                "修改、删除、重复提交、并发冲突和数据库失败回滚",
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
