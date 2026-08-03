"""生成 RT-07-003 银行资金利息收入真实保存与冷启动验证记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-07-003-20260731T151637+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造符合运行观察记录模式的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出银行资金利息收入的保存、投影、持久性和恢复结论。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-07-003",
        "resource": "TINVESTFEEDLGFM",
        "observed_at": "2026-07-31T15:16:37+08:00",
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8",
            "sha256_before": "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC",
            "sha256_after": "1AF77A1A5C2F31DE97A42C04757A5D070A51936980031B25F723983B4733CD96",
            "backup_artifact": (
                "artifacts/runtime-validation/backups/"
                "test-before-rt07-bank-interest-20260731.mh8"
            ),
        },
        "navigation": {
            "entry_point": "记账 -> 更多交易活动 -> 银行存款 -> 利息收入（命令 ID 132）",
            "steps": [
                "核对 test.mh8、~$test、进程状态和前置指纹并建立备份",
                "从真实账户下拉列表选择 Cash-CNY，确认币种自动锁定为人民币 CNY",
                "填写金额 2.00、日期 2026-07-31 和唯一合成备注后确定",
                "核对账户中心余额、CASH 分组折算值和全局财务记录",
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
                    "共享窗体标题为资金利息收入；本轮从候选列表选择 Cash-CNY，币种自动"
                    "锁定为人民币 CNY，填写正金额 2.00、日期和备注，标签留空。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-bank-interest-filled-before-save.png"
                ],
            },
            {
                "name": "余额与账户组投影",
                "status": "observed",
                "observations": (
                    "Cash-CNY 从 608.00 增为 610.00，Cash-GBP 和 Cash-USD 不变；"
                    "CASH 账户组人民币折算值从 9,495.70 增为 9,497.70。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-bank-interest-balances-after-restart-sanitized.png"
                ],
            },
            {
                "name": "全局财务记录",
                "status": "observed",
                "observations": (
                    "全局列表新增一条利息收入，流入 2.00、流出为空、资产账户 Cash-CNY、"
                    "标签为空、备注正确。该 CNY 行的币种列为空；同页既有 GBP 利息记录"
                    "显示英镑 GBP，因此空列只能作为旧界面的本位币显示约定，不能代表无币种。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/"
                    "rt07-bank-interest-financial-record-after-restart-sanitized.png"
                ],
            },
            {
                "name": "冷启动持久性与基线恢复",
                "status": "observed",
                "observations": (
                    "正常退出并重启后余额、账户组折算值和全局记录均保持。首次关闭后的"
                    "业务状态 SHA-256 为 0AA0...31107，冷启动复核后为 1AF7...CD96；"
                    "差异属于旧程序会话写回，业务投影一致。最终 test.mh8 已恢复为"
                    "前置 SHA-256 D8E4...E165AC，且最后写入时间晚于恢复文件。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/backups/"
                    "test-after-rt07-bank-interest-verified-20260731.mh8",
                    "artifacts/runtime-validation/RT07-bank-interest-notes.md",
                ],
            },
        ],
        "commands": [
            {
                "component": "银行存款子菜单",
                "label": "利息收入",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "动态读取菜单层级后投递命令 ID 132。",
                "confirmation": None,
                "outcome": "以资金利息收入模式打开 TInvestFeeDlgFm。",
                "status": "pass",
            },
            {
                "component": "资金账户选择器",
                "label": "Cash-CNY",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "从真实账户候选列表选择第一行 Cash-CNY。",
                "confirmation": None,
                "outcome": "绑定稳定账户对象并自动锁定人民币 CNY。",
                "status": "pass",
            },
            {
                "component": "btnSaveExit",
                "label": "确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "填写 2.00 CNY、日期和唯一备注后点击确定。",
                "confirmation": None,
                "outcome": "账户增加 2.00 并生成单条利息收入记录；冷启动后保持一致。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": [
                "业务动作：interest_income",
                "资金账户 ID：Cash-CNY",
                "账户币种：CNY",
                "金额：2.00 CNY",
                "业务日期、可选标签和备注",
            ],
            "reads": [
                "资金账户的稳定身份、状态、币种和提交前余额 608.00",
                "共享编辑器由银行存款利息命令显式传入的收入模式",
            ],
            "writes": [
                "一条利息收入业务事件",
                "Cash-CNY 增加 2.00 CNY 的单边资金流入分录",
                "收入分类、日期、标签和备注关系",
            ],
            "derived_results": [
                "Cash-CNY 余额：610.00",
                "CASH 账户组人民币折算值：9,497.70",
                "财务记录：利息收入、流入 2.00、账户 Cash-CNY、币种显示列为空",
            ],
            "side_effects": [
                "账户中心和全局财务记录立即刷新",
                "本位币行可在旧界面隐藏币种文字，但领域事实仍必须保存 CNY",
                "正常退出和重启会更新会话级文件状态，但业务投影保持不变",
            ],
            "rollback": (
                "本轮只验证银行存款/CNY 有效提交和最终基线恢复；零负金额、无效账户、"
                "外币账户、投资产品域、并发冲突、数据库失败和崩溃中断仍待验证。"
            ),
        },
        "evidence": [
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt07-bank-interest-initial.png",
                "资金利息收入模式的初始字段和必填状态。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt07-bank-interest-filled-before-save.png",
                "真实账户对象、锁定币种、正金额和合成备注的确认前输入。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt07-bank-interest-balances-after-restart-sanitized.png",
                "冷启动后的 Cash-CNY 余额和 CASH 分组折算结果。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/"
                "rt07-bank-interest-financial-record-after-restart-sanitized.png",
                "冷启动后的利息收入流入、账户、备注和本位币空显示列。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/"
                "test-after-rt07-bank-interest-verified-20260731.mh8",
                "已通过冷启动复核的银行资金利息收入成功状态账簿副本。",
            ),
            evidence(
                "manual_note",
                "artifacts/runtime-validation/RT07-bank-interest-notes.md",
                "进程、文件指纹、保存结果、冷启动和基线恢复时间线。",
            ),
            evidence(
                "manual_note",
                "docs/runtime-transactions-and-ledger-contract.md",
                "由本次真实行为校准的 Rust 单边利息收入合同。",
            ),
        ],
        "requirements_update": [
            "共享费用/利息编辑器必须接收显式业务动作，不能从标题、菜单层级或金额正负推断。",
            "账户选择必须绑定稳定账户 ID；选中账户后币种由账户锁定，用户不得另行制造不一致币种。",
            "利息收入以正金额输入，领域层原子写入收入事件和单边账户流入分录。",
            "基础币种在旧列表中可显示为空，但持久层、接口和审计记录仍必须保存明确币种 CNY。",
            "账户余额、账户组投影和全局财务记录必须从同一事件重建，并在冷启动后保持一致。",
            "费用模式与其它投资产品域仍需独立验证，不能由本次银行存款正常路径外推为全部兼容。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证 Cash-CNY 资金利息收入 2.00 CNY 的账户绑定、币种锁定、有效保存、"
                "余额与全局投影、冷启动持久性和基线恢复。"
            ),
            "remaining_gaps": [
                "其它投资费用模式的真实支出分录和收益报表影响",
                "外币账户利息收入的汇率快照、本位币折算和列表币种显示",
                "证券、基金、外汇、理财、期货和融资融券上下文的产品关联",
                "零负金额、无效或禁用账户、日期边界和标签约束",
                "修改、删除、冲销、重复提交、并发冲突和故障原子回滚",
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
