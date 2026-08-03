"""生成 B03 单笔同币种转账与手续费的真实保存记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-03-005-20260731T141122+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造符合运行观察记录模式的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出本次转账有效保存、重启持久性和基线恢复结论。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-03-005",
        "resource": "TCASHXFERDLGFM",
        "observed_at": "2026-07-31T14:11:22+08:00",
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8",
            "sha256_before": "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC",
            "sha256_after": "04D42F708345E38B3997838E4B52DA739E1B5BB6416DA03A288F7C2C7C420869",
            "backup_artifact": (
                "artifacts/runtime-validation/backups/"
                "test-before-b03-transfer-fee-20260731.mh8"
            ),
        },
        "navigation": {
            "entry_point": "顶部记账菜单 -> 转账（命令 ID 111）",
            "steps": [
                "核对 test.mh8、~$test、进程状态和前置指纹并建立备份",
                "填写 Cash-CNY -> 顺德农行、金额 50.00、手续费 1.00、手续费账户 Cash-CNY",
                "保存后核对账户中心、来源账户流水和财务记录",
                "正常退出并冷启动，复核余额、流水和全局记录仍存在",
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
                    "同币种人民币转账：Cash-CNY 转入顺德农行 50.00，手续费 1.00 "
                    "由 Cash-CNY 承担，日期 2026-07-31，备注为合成测试标识。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "b03-transfer-fee-filled-before-save.png"
                ],
            },
            {
                "name": "账户身份校验",
                "status": "observed",
                "observations": (
                    "仅写入选择器显示文本而未选定实际账户对象时，保存提示“请选择转入账户”；"
                    "从账户下拉列表选定稳定对象后才允许提交。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "b03-transfer-save-message.png"
                ],
            },
            {
                "name": "余额影响",
                "status": "observed",
                "observations": (
                    "Cash-CNY 从 608.00 降为 557.00，顺德农行从 100.00 增为 150.00；"
                    "来源减少 51.00、目标增加 50.00，净资产减少 1.00。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "b03-transfer-balances-after-restart-sanitized.png"
                ],
            },
            {
                "name": "来源账户流水",
                "status": "observed",
                "observations": (
                    "来源账户生成一条“转出|顺德农行”记录，流出显示 51.00，余额 557.00，"
                    "说明手续费与转账本金合并进入来源账户的可见流出金额。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "b03-transfer-source-ledger-after-restart-sanitized.png"
                ],
            },
            {
                "name": "全局财务记录",
                "status": "observed",
                "observations": (
                    "全局财务记录以单条转账展示流入 50.00、流出 51.00，资产账户为 "
                    "Cash-CNY->顺德农行；转账本金和手续费可从同一业务记录中分别推导。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "b03-transfer-financial-record-after-restart-sanitized.png"
                ],
            },
            {
                "name": "冷启动持久性与基线恢复",
                "status": "observed",
                "observations": (
                    "正常退出并重启后余额、来源流水和财务记录均保持；成功状态已保存为独立备份。"
                    "最终 test.mh8 恢复为前置 SHA-256 D8E4...E165AC，且时间戳晚于恢复文件。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/backups/"
                    "test-after-b03-transfer-fee-verified-20260731.mh8",
                    "artifacts/runtime-validation/B03-transactions-notes.md",
                ],
            },
        ],
        "commands": [
            {
                "component": "selAcctIn",
                "label": "转入账户",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "先仅设置显示文本，再从账户下拉列表选择顺德农行。",
                "confirmation": None,
                "outcome": "未绑定账户对象时阻止保存；选择真实账户对象后校验通过。",
                "status": "pass",
                "event_ids": ["transactions.cash_xfer_dlg_fm.sel_acct_in_close_up"],
            },
            {
                "component": "btnSaveExit",
                "label": "确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "填写有效同币种转账和手续费后点击确定。",
                "confirmation": None,
                "outcome": (
                    "一次提交更新两侧余额并生成单条用户可识别转账；冷启动后保持一致。"
                ),
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": [
                "转出账户 ID：Cash-CNY",
                "转入账户 ID：顺德农行",
                "转账金额：CNY 50.00",
                "手续费：CNY 1.00，手续费账户为 Cash-CNY",
                "业务日期和备注",
            ],
            "reads": [
                "转出与转入账户的稳定身份、状态和币种",
                "提交前账户余额与手续费账户可用性",
            ],
            "writes": [
                "一条用户可识别的转账业务记录",
                "来源账户减少 51.00、目标账户增加 50.00 的关联余额影响",
                "手续费 1.00 的显式业务组成和备注",
            ],
            "derived_results": [
                "账户中心余额：557.00 与 150.00",
                "来源账户流水：流出 51.00",
                "财务记录：流入 50.00、流出 51.00、净影响 -1.00",
            ],
            "side_effects": [
                "CASH 账户组减少 51.00，China Bank 账户组增加 50.00",
                "净资产减少手续费 1.00",
                "正常退出和重启会写回会话级文件状态，但业务投影保持不变",
            ],
            "rollback": (
                "本轮验证了必填账户校验不会产生业务写入；数据库写入失败、并发冲突和"
                "中途崩溃的完整原子回滚仍待故障注入验证。"
            ),
        },
        "evidence": [
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "b03-transfer-fee-filled-before-save.png",
                "同币种转账、手续费账户和合成备注的确认前输入。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "b03-transfer-save-message.png",
                "未选择实际转入账户对象时的必填校验。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "b03-transfer-balances-after-restart-sanitized.png",
                "冷启动后的来源、目标余额和净资产影响。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "b03-transfer-source-ledger-after-restart-sanitized.png",
                "冷启动后的来源账户流出记录。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "b03-transfer-financial-record-after-restart-sanitized.png",
                "冷启动后的全局转账记录及双金额口径。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/"
                "test-after-b03-transfer-fee-verified-20260731.mh8",
                "已通过冷启动复核的业务成功状态账簿副本。",
            ),
            evidence(
                "manual_note",
                "artifacts/runtime-validation/B03-transactions-notes.md",
                "进程、文件指纹、即时结果、冷启动和基线恢复时间线。",
            ),
            evidence(
                "manual_note",
                "docs/runtime-transactions-and-ledger-contract.md",
                "由本次真实行为校准的 Rust 转账与手续费合同。",
            ),
        ],
        "requirements_update": [
            "账户选择必须提交稳定账户 ID；显示文本不能被当作已完成选择。",
            "同币种转账本金 50.00 与手续费 1.00 必须在同一原子命令中保存。",
            "手续费由来源账户承担时，来源余额减少本金加手续费，目标余额只增加本金。",
            "账户流水可显示来源总流出 51.00，但领域模型必须保留本金 50.00 和手续费 1.00 的独立组成。",
            "全局财务记录应以同一业务身份展示流入本金和流出本金加手续费，并保持净影响等于手续费。",
            "账户中心、账户流水和财务记录在保存后及冷启动后必须使用同一持久化事实重建。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证 Cash-CNY 向顺德农行转账 50.00、来源账户手续费 1.00 的"
                "有效保存、账户与列表投影、冷启动持久性和基线恢复。"
            ),
            "remaining_gaps": [
                "跨币种转账的汇率方向、两侧金额、舍入差异和汇兑损益",
                "手续费由第三账户或目标账户承担的余额与记录口径",
                "余额不足、同账户、零负金额、并发冲突和数据库失败的完整回滚",
                "修改、删除、退款和批量转账对原交易关系及审计历史的影响",
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
