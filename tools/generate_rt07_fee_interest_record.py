"""生成 RT-07-003 共享费用与利息双模式真实保存记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-07-003-20260731T154305+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造运行观察记录中的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出共享编辑器两个业务方向的真实保存与持久性结论。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-07-003",
        "resource": "TINVESTFEEDLGFM",
        "observed_at": "2026-07-31T15:43:05+08:00",
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8",
            "sha256_before": "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC",
            "sha256_after": "62B033DD74099F6D0515105BCBED2AC48D75F53F087280FAE2922D7143345A7A",
            "backup_artifact": (
                "artifacts/runtime-validation/backups/"
                "test-before-rt07-foreign-expense-20260731.mh8"
            ),
        },
        "navigation": {
            "entry_point": (
                "银行存款 -> 利息收入（命令 ID 132）；"
                "外汇交易 -> 其它费用（命令 ID 214）"
            ),
            "steps": [
                "两次独立会话都从相同 test.mh8 基线建立备份",
                "分别打开资金利息收入和其它投资费用模式",
                "从真实候选列表绑定 Cash-CNY 并确认币种锁定为人民币 CNY",
                "分别保存 2.00 利息收入和 1.25 其它费用",
                "核对余额、CASH 分组折算值和全局财务记录",
                "分别正常退出、冷启动复核并保存成功状态副本",
                "每次会话结束后恢复相同基线并核对主库、恢复文件和进程状态",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "银行利息收入有效保存",
                "status": "observed",
                "observations": (
                    "Cash-CNY 保存 2.00 CNY 后余额 608.00 -> 610.00，CASH 分组"
                    "9,495.70 -> 9,497.70；全局记录为利息收入、单边流入 2.00。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-bank-interest-filled-before-save.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-bank-interest-balances-after-restart-sanitized.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-bank-interest-financial-record-after-restart-sanitized.png",
                ],
            },
            {
                "name": "外汇其它费用有效保存",
                "status": "observed",
                "observations": (
                    "从外汇入口保存 Cash-CNY 其它费用 1.25 CNY 后余额 608.00 -> 606.75，"
                    "CASH 分组 9,495.70 -> 9,494.45；全局记录为其它费用、单边流出 1.25。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-foreign-expense-filled-before-save.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-foreign-expense-balances-after-restart-sanitized.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-foreign-expense-financial-record-after-restart-sanitized.png",
                ],
            },
            {
                "name": "共享字段与显式方向",
                "status": "observed",
                "observations": (
                    "两个模式都使用正金额、资金账户、锁定币种、标签、日期和备注；"
                    "业务方向由入口命令传入，同一窗体分别生成单边流入和单边流出。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-bank-interest-filled-before-save.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-foreign-expense-filled-before-save.png",
                ],
            },
            {
                "name": "本位币显示与来源上下文",
                "status": "observed",
                "observations": (
                    "两条 CNY 记录的币种显示列均为空，而同页 GBP 记录显示币种；"
                    "外汇费用行也没有可见外汇来源，只显示通用活动类型和资金账户。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-bank-interest-financial-record-after-restart-sanitized.png",
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-foreign-expense-financial-record-after-restart-sanitized.png",
                ],
            },
            {
                "name": "冷启动持久性与基线恢复",
                "status": "observed",
                "observations": (
                    "两个业务状态都在正常退出和冷启动后保持。利息状态验证哈希为"
                    "1AF7...CD96，费用状态验证哈希为 62B0...5A7A；每次最终均恢复"
                    "D8E4...E165AC 基线，且 MoneyHome8 进程数为 0。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/backups/"
                    "test-after-rt07-bank-interest-verified-20260731.mh8",
                    "artifacts/runtime-validation/backups/"
                    "test-after-rt07-foreign-expense-verified-20260731.mh8",
                    "artifacts/runtime-validation/RT07-fee-interest-notes.md",
                ],
            },
        ],
        "commands": [
            {
                "component": "银行存款子菜单",
                "label": "利息收入",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "投递命令 ID 132 并保存 2.00 CNY。",
                "confirmation": None,
                "outcome": "生成单边资金流入和利息收入记录，冷启动后保持。",
                "status": "pass",
            },
            {
                "component": "外汇交易子菜单",
                "label": "其它费用",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "投递命令 ID 214 并保存 1.25 CNY。",
                "confirmation": None,
                "outcome": "生成单边资金流出和其它费用记录，冷启动后保持。",
                "status": "pass",
            },
            {
                "component": "资金账户选择器",
                "label": "Cash-CNY",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "两个模式都从真实账户候选列表选择 Cash-CNY。",
                "confirmation": None,
                "outcome": "绑定稳定账户对象并自动锁定人民币 CNY。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": [
                "显式事件类型：interest_income 或 expense",
                "来源上下文：bank_deposit 或 foreign_exchange",
                "稳定资金账户 ID：Cash-CNY",
                "账户币种：CNY",
                "正金额、日期、可选标签和备注",
            ],
            "reads": [
                "账户身份、状态、币种和提交前余额 608.00",
                "入口命令传入的事件方向和来源上下文",
            ],
            "writes": [
                "利息收入事件和 Cash-CNY +2.00 CNY 单边流入分录",
                "其它费用事件和 Cash-CNY -1.25 CNY 单边流出分录",
                "事件类型、来源上下文、日期、标签、备注和审计关系",
            ],
            "derived_results": [
                "利息场景余额 610.00、CASH 分组 9,497.70",
                "费用场景余额 606.75、CASH 分组 9,494.45",
                "全局活动类型分别为利息收入和其它费用",
            ],
            "side_effects": [
                "账户中心和全局财务记录立即刷新并在冷启动后保持",
                "旧界面对本位币隐藏币种文字",
                "旧全局费用行不显示外汇来源，查询投影无法可靠反推 product_domain",
            ],
            "rollback": (
                "本轮验证两个 CNY 正常路径和最终基线恢复；外币折算、产品 ID 关联、"
                "零负金额、禁用账户、修改删除、并发冲突和故障回滚仍待验证。"
            ),
        },
        "evidence": [
            evidence(
                "manual_note",
                "artifacts/runtime-validation/RT07-fee-interest-notes.md",
                "双模式输入、余额、流水、冷启动、指纹和恢复时间线。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt07-bank-interest-balances-after-restart-sanitized.png",
                "利息收入冷启动后的余额与分组折算。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt07-bank-interest-financial-record-after-restart-sanitized.png",
                "利息收入单边流入和本位币空显示列。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt07-foreign-expense-balances-after-restart-sanitized.png",
                "其它费用冷启动后的余额与分组折算。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt07-foreign-expense-financial-record-after-restart-sanitized.png",
                "其它费用单边流出、本位币空显示列和不可见来源上下文。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/"
                "test-after-rt07-bank-interest-verified-20260731.mh8",
                "已通过冷启动复核的利息收入成功状态账簿。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/"
                "test-after-rt07-foreign-expense-verified-20260731.mh8",
                "已通过冷启动复核的其它费用成功状态账簿。",
            ),
            evidence(
                "manual_note",
                "docs/runtime-investment-shared-projections-contract.md",
                "由双模式真实行为校准的 Rust 共享费用与利息合同。",
            ),
        ],
        "requirements_update": [
            "共享编辑器必须接收显式 event_kind 和 source_context，不能从标题、菜单或金额正负推断。",
            "两个方向都使用正金额；领域层根据事件类型生成单边流入或单边流出。",
            "账户选择必须绑定稳定 ID，币种由账户锁定并在事务内再次校验。",
            "本位币即使在列表中隐藏文字，交易、分录、接口、导出和审计仍必须保存 CNY。",
            "通用费用行无法可靠表达外汇来源，目标模型必须持久化 product_domain 或等价来源字段。",
            "事件、账户分录、分类、来源上下文和审计记录必须原子提交并支持冷启动重建。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证共享 TInvestFeeDlgFm 的银行利息收入和外汇其它费用两个 CNY 方向，"
                "包括账户绑定、币种锁定、单边分录、余额与全局投影、冷启动和基线恢复。"
            ),
            "remaining_gaps": [
                "证券、基金、理财、期货、贵金属和融资融券上下文的产品 ID 关联",
                "外币费用/利息的汇率快照、本位币折算和显示",
                "零负金额、无效或禁用账户、日期和标签边界",
                "修改、删除、冲销、重复提交和来源上下文查询",
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
