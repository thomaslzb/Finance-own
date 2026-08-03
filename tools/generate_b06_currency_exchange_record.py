"""生成 B06 货币兑换真实保存与冷启动验证记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-06-001-20260731T144139+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造符合运行观察记录模式的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出本次跨币种兑换、投影持久性和基线恢复结论。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-06-001",
        "resource": "TCURRCHGXFERDLGFM",
        "observed_at": "2026-07-31T14:41:39+08:00",
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8",
            "sha256_before": "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC",
            "sha256_after": "026283CD94A21AC04344D2F25FDE3B8F612B82D1546F7CDDF8DF890EEA0C3803",
            "backup_artifact": (
                "artifacts/runtime-validation/backups/"
                "test-before-b06-currency-exchange-20260731.mh8"
            ),
        },
        "navigation": {
            "entry_point": "记账 -> 更多交易活动 -> 银行存款 -> 货币兑换（命令 ID 133）",
            "steps": [
                "核对 test.mh8、~$test、进程状态和前置指纹并建立备份",
                "选择 Cash-CNY 为换出账户、Cash-GBP 为换入账户",
                "填写换出 9.00 CNY、换入 1.00 GBP 和唯一合成备注后确定",
                "核对账户中心余额、账户组折算值和全局财务记录",
                "正常退出并冷启动，复核余额和全局记录仍存在",
                "保存成功状态副本，退出后恢复本轮前基线并再次核对指纹",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "有效输入",
                "status": "observed",
                "observations": (
                    "货币兑换窗体没有独立汇率字段；本轮实际选择 Cash-CNY 和 Cash-GBP，"
                    "填写换出 9.00、换入 1.00、日期 2026-07-31 和合成备注。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "b06-currency-exchange-filled-before-save.png"
                ],
            },
            {
                "name": "余额与估值影响",
                "status": "observed",
                "observations": (
                    "Cash-CNY 从 608.00 降为 599.00，Cash-GBP 从 908.30 增为 909.30；"
                    "CASH 账户组人民币折算值从 9,495.70 变为 9,495.74。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "b06-balances-after-restart-sanitized.png"
                ],
            },
            {
                "name": "全局财务记录",
                "status": "observed",
                "observations": (
                    "全局列表以一条“货币兑换”展示流入 1.00、流出 9.00、账户 "
                    "Cash-CNY->Cash-GBP 和备注；该行币种列为空，页脚仍把不同币种的"
                    "名义金额直接并入流入流出合计。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "b06-financial-record-after-restart-sanitized.png"
                ],
            },
            {
                "name": "隐含汇率与折算口径",
                "status": "observed",
                "observations": (
                    "输入形成 1 GBP = 9 CNY，或 1 CNY = 0.111111... GBP 的隐含成交比例；"
                    "账户组折算只增加 0.04，说明余额投影使用既有估值汇率，而不是强制"
                    "按本次两侧金额保持人民币价值不变。旧账本是否另存成交汇率快照仍未确认。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/B06-currency-exchange-notes.md"
                ],
            },
            {
                "name": "冷启动持久性与基线恢复",
                "status": "observed",
                "observations": (
                    "正常退出并重启后两侧余额、账户组折算值和全局记录均保持；成功状态"
                    "已保存为独立备份。最终 test.mh8 恢复为前置 SHA-256 D8E4...E165AC，"
                    "且最后写入时间晚于恢复文件。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/backups/"
                    "test-after-b06-currency-exchange-verified-20260731.mh8",
                    "artifacts/runtime-validation/B06-currency-exchange-notes.md",
                ],
            },
        ],
        "commands": [
            {
                "component": "银行存款子菜单",
                "label": "货币兑换",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "动态读取菜单层级后投递命令 ID 133。",
                "confirmation": None,
                "outcome": "打开 TCurrChgXferDlgFm，并默认带入 Cash-CNY。",
                "status": "pass",
            },
            {
                "component": "btnSaveExit",
                "label": "确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "选择真实两侧账户对象并填写两个正金额后点击确定。",
                "confirmation": None,
                "outcome": "一次提交更新两侧余额并生成单条货币兑换记录；冷启动后保持一致。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": [
                "换出账户 ID：Cash-CNY，币种 CNY",
                "换入账户 ID：Cash-GBP，币种 GBP",
                "换出金额：CNY 9.00",
                "换入金额：GBP 1.00",
                "业务日期和备注",
            ],
            "reads": [
                "两侧账户的稳定身份、状态、币种和提交前余额",
                "账户中心人民币折算投影使用的既有估值汇率或估值结果",
            ],
            "writes": [
                "一条用户可识别的货币兑换业务记录",
                "来源账户减少 9.00 CNY、目标账户增加 1.00 GBP 的关联余额影响",
                "两侧账户、两侧原币金额、日期和备注之间的业务关系",
            ],
            "derived_results": [
                "隐含成交比例：1 GBP = 9 CNY",
                "账户余额：599.00 CNY 与 909.30 GBP",
                "CASH 账户组人民币折算值：9,495.74",
                "财务记录：流入 1.00、流出 9.00、币种列为空",
            ],
            "side_effects": [
                "账户中心按既有估值口径重新折算账户组金额",
                "旧全局列表把不同币种名义金额直接加入统一流入流出页脚合计",
                "正常退出和重启会更新会话级文件状态，但业务投影保持不变",
            ],
            "rollback": (
                "本轮只验证有效提交和最终基线恢复；同币种、零负金额、余额不足、并发冲突、"
                "数据库写入失败和崩溃中断时的完整原子回滚仍待故障验证。"
            ),
        },
        "evidence": [
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "b06-currency-exchange-filled-before-save.png",
                "真实账户对象、双原币金额和合成备注的确认前输入。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "b06-balances-after-restart-sanitized.png",
                "冷启动后的两侧余额和账户组折算结果。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "b06-financial-record-after-restart-sanitized.png",
                "冷启动后的单条货币兑换记录、双金额和空币种列。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/"
                "test-after-b06-currency-exchange-verified-20260731.mh8",
                "已通过冷启动复核的货币兑换成功状态账簿副本。",
            ),
            evidence(
                "manual_note",
                "artifacts/runtime-validation/B06-currency-exchange-notes.md",
                "进程、文件指纹、保存结果、冷启动和基线恢复时间线。",
            ),
            evidence(
                "manual_note",
                "docs/runtime-transactions-and-ledger-contract.md",
                "由本次真实行为校准的 Rust 跨币种兑换合同。",
            ),
        ],
        "requirements_update": [
            "货币兑换必须保存稳定的两侧账户 ID、两侧币种和两侧原币金额，不能只保存净额。",
            "没有显式汇率输入时，系统仍必须保存报价方向和可重算的成交比例；本例为 1 GBP = 9 CNY。",
            "账户余额按原币逐分更新；账户组、净资产和报表折算必须使用有时间和来源的估值汇率快照。",
            "成交汇率与估值汇率必须分开建模，不能用账户中心当前折算结果反推或覆盖成交事实。",
            "跨币种全局列表不得把 1.00 GBP 和 9.00 CNY 直接相加；应按原币分组或按同一估值快照折算。",
            "同一兑换业务下的两侧分录、汇率/比例、舍入差额和可选汇兑损益必须原子提交。",
            "账户中心和财务记录应从同一兑换事实重建，并在冷启动后保持一致。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证 Cash-CNY 换出 9.00 CNY、Cash-GBP 换入 1.00 GBP 的有效保存、"
                "两侧余额、估值投影、全局记录、冷启动持久性和基线恢复。"
            ),
            "remaining_gaps": [
                "旧账本是否持久化成交汇率、报价方向、估值快照和汇兑损益",
                "同币种阻止、零负金额、余额不足、相同账户和账户状态校验",
                "非整除汇率、多币种小数位、舍入尾差和显式汇兑损益",
                "手续费、修改、删除、退款和批量换汇的关系与审计",
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
