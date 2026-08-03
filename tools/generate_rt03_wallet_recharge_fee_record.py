"""生成 RT-03-026 第三方钱包充值手续费真实保存记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-03-026-20260731T191900+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造运行记录中的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出钱包充值手续费承担侧和完整双向费用规则。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-03-026",
        "resource": "TRECHARGEDLGFM",
        "observed_at": "2026-07-31T19:19:00+08:00",
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
                "326623F751A820029824CD497D7FB8086BA8F2D14F572A8B86117DECD78F36AE"
            ),
            "backup_artifact": (
                "artifacts/runtime-validation/backups/"
                "test-before-rt03-wallet-recharge-fee-20260731T191108.mh8"
            ),
        },
        "navigation": {
            "entry_point": (
                "记账 -> 更多交易活动 -> 支付宝、微信钱包 -> 充值（命令 ID 135）"
            ),
            "steps": [
                "从 D8E4...165AC 基线建立充值手续费操作前备份",
                "用动态命令 135 打开 TRechargeDlgFm / 充值",
                "保留微信钱包并从未过滤候选列表绑定 Cash-CNY",
                "输入本金 1.00、手续费 0.10 和唯一备注后确定保存",
                "核对来源、钱包、CASH 分组、净资产和全局记录",
                "正常退出、冷启动复核并保留两份成功状态账簿",
                "恢复操作前基线并核对进程数、恢复文件和 SHA-256",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "有效充值手续费输入",
                "status": "observed",
                "observations": (
                    "Cash-CNY 到微信钱包的本金为 1.00 CNY、手续费为 0.10 CNY；"
                    "稳定账户对象绑定后可直接确定保存。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-wallet-recharge-fee-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-wallet-recharge-fee-source-dropdown-sanitized.png",
                ],
            },
            {
                "name": "资金来源承担充值手续费",
                "status": "observed",
                "observations": (
                    "Cash-CNY 608.00 -> 606.90，总扣款 1.10；微信钱包 "
                    "2,986.44 -> 2,987.44，只收到本金 1.00；CASH 分组减少 1.10。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-wallet-recharge-fee-wallet-after-restart-sanitized.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-wallet-recharge-fee-balances-after-restart-sanitized.png",
                ],
            },
            {
                "name": "费用与全局投影",
                "status": "observed",
                "observations": (
                    "钱包流水只显示流入 1.00；全局充值显示流入 1.00、流出 1.10；"
                    "净资产 7,095,607.18 -> 7,095,607.08，只减少手续费 0.10。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt03-wallet-recharge-fee-financial-record-after-restart-sanitized.png",
                    "artifacts/runtime-validation/RT03-wallet-recharge-fee-notes.md",
                ],
            },
            {
                "name": "双向费用规则",
                "status": "observed",
                "observations": (
                    "结合提现手续费记录，充值由资金来源承担费用，提现由钱包来源承担费用；"
                    "统一规则是发出资金的一侧支付本金加手续费，接收侧只取得本金。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/RT-03-026-20260731T184800+0800.json",
                    "artifacts/runtime-validation/RT03-wallet-withdrawal-fee-notes.md",
                ],
            },
            {
                "name": "冷启动持久性与基线恢复",
                "status": "observed",
                "observations": (
                    "首次退出哈希 03F4...9A38，冷启动后二次退出哈希 3266...36AE；"
                    "余额、费用和流水语义保持。最终只恢复 test.mh8 到 D8E4...165AC，"
                    "MoneyHome8 进程数为 0，软件生成的 ~$test 未被手工处理。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/backups/"
                    "test-after-rt03-wallet-recharge-fee-verified-20260731T192322.mh8",
                    "artifacts/runtime-validation/backups/"
                    "test-after-rt03-wallet-recharge-fee-cold-restart-20260731T192738.mh8",
                    "artifacts/runtime-validation/RT03-wallet-recharge-fee-notes.md",
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
                "trigger": "从 TmwSelectAccountDrop 的未过滤 TmwList 选择首项。",
                "confirmation": None,
                "outcome": "绑定稳定账户对象并允许提交。",
                "status": "pass",
            },
            {
                "component": "确定按钮",
                "label": "确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "提交本金 1.00 和手续费 0.10。",
                "confirmation": None,
                "outcome": "来源扣除 1.10、钱包收到 1.00，净资产减少 0.10。",
                "status": "pass",
            },
            {
                "component": "保存并继续按钮",
                "label": "保存并继续",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "本轮未执行。",
                "confirmation": None,
                "outcome": "成功后的字段保留和草稿重置策略仍待验证。",
                "status": "pending",
            },
        ],
        "data_flow": {
            "inputs": [
                "稳定钱包账户 ID：微信钱包",
                "稳定资金来源账户 ID：Cash-CNY",
                "本金 1.00 CNY、手续费 0.10 CNY",
                "日期、可选标签、备注和附件关系",
            ],
            "reads": [
                "钱包账户状态、币种和余额版本",
                "资金来源账户状态、币种、可用余额和余额版本",
            ],
            "writes": [
                "一个显式 wallet_recharge 交易头",
                "Cash-CNY 本金流出 1.00",
                "Cash-CNY 手续费流出 0.10",
                "微信钱包本金流入 1.00",
                "日期、标签、备注、附件和审计关系",
            ],
            "derived_results": [
                "Cash-CNY 余额 606.90，微信钱包余额 2,987.44",
                "CASH 分组 9,494.60，净资产减少 0.10",
                "钱包流水流入 1.00，全局流入 1.00、流出 1.10",
            ],
            "side_effects": [
                "账户中心、钱包流水和全局财务记录立即刷新并在冷启动后保持",
                "接收侧钱包流水只显示本金，来源侧承担手续费",
                "Jet 打开关闭周期可能改写文件哈希但不改变业务事实",
            ],
            "rollback": (
                "本轮验证正常充值手续费路径和最终基线恢复；费用报表分类、"
                "修改删除、并发冲突和故障回滚仍待验证。"
            ),
        },
        "evidence": [
            evidence(
                "manual_note",
                "artifacts/runtime-validation/RT03-wallet-recharge-fee-notes.md",
                "手续费承担侧、余额、流水、哈希变化和基线恢复时间线。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-wallet-recharge-fee-filled-sanitized.png",
                "充值账户、资金来源、本金、手续费、日期和唯一备注。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-wallet-recharge-fee-wallet-after-restart-sanitized.png",
                "冷启动后的钱包余额和本金流入 1.00。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-wallet-recharge-fee-balances-after-restart-sanitized.png",
                "冷启动后的 Cash-CNY、CASH 分组和净资产。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt03-wallet-recharge-fee-financial-record-after-restart-sanitized.png",
                "冷启动后的全局流入 1.00、流出 1.10 投影。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/"
                "test-after-rt03-wallet-recharge-fee-cold-restart-20260731T192738.mh8",
                "已通过冷启动业务复核的钱包充值手续费成功状态账簿。",
            ),
        ],
        "requirements_update": [
            "钱包充值手续费由资金来源账户承担，来源总扣款等于本金加手续费。",
            "钱包只接收本金，净资产变化严格等于手续费。",
            "本金和手续费必须作为可区分组成在一个数据库事务内原子提交。",
            "钱包双向统一规则是发出资金的一侧承担手续费，接收侧只取得本金。",
            "查询投影可合并来源总扣款，但费用报表、审计和修改删除必须保留组成。",
            "冷启动验收必须比较业务事实；Jet 文件哈希只标识具体证据副本。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证 Cash-CNY 到微信钱包的 1.00 CNY 本金和 0.10 CNY "
                "充值手续费，并结合提现证据确认钱包双向均由资金发出侧承担费用。"
            ),
            "remaining_gaps": [
                "充值和提现手续费在费用报表中的分类与筛选投影",
                "保存并继续的字段保留与草稿重置",
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
