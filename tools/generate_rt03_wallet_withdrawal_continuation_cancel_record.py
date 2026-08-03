"""生成 RT-03-026 钱包提现保存并继续与取消分支记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-03-026-20260731T204900+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造运行记录中的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出提现保存并继续、编辑关闭和删除确认分支的实际行为。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-03-026",
        "resource": "TRECHARGEDLGFM",
        "observed_at": "2026-07-31T20:49:00+08:00",
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
                "test-before-rt03-wallet-withdrawal-continuation-cancel-20260731T203640.mh8"
            ),
        },
        "navigation": {
            "entry_point": "记账 -> 更多交易活动 -> 支付宝、微信钱包 -> 提现",
            "steps": [
                "创建本金 1.00、手续费 0.10、唯一备注的提现草稿",
                "点击保存并继续并观察同一编辑器的字段状态",
                "关闭已重置草稿并核对只生成一条钱包记录",
                "打开该记录修改手续费和备注后直接关闭编辑器",
                "删除确认先选择否并比较取消前后界面文件哈希",
                "再次删除选择是完成清理，冷启动确认记录不存在",
                "退出全部 MoneyHome8 进程并恢复精确账簿基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "提现保存并继续成功",
                "status": "observed",
                "observations": (
                    "本金 1.00、手续费 0.10 提交后编辑器保持打开；提现账户微信钱包和日期 "
                    "2026-07-31 保留，资金去向、金额、手续费、标签和备注清空。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-after-save-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-after-save-wallet-sanitized.png",
                ],
            },
            {
                "name": "编辑关闭放弃修改",
                "status": "observed",
                "observations": (
                    "把手续费改为 0.20、备注改为 CANCELLED 后直接关闭，没有确认提示；"
                    "原手续费 0.10、原备注、钱包 2,985.34、流出 1.10 和记录数 244 保持。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-edit-cancel-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-after-edit-cancel-wallet-sanitized.png",
                ],
            },
            {
                "name": "删除否分支零写入",
                "status": "observed",
                "observations": (
                    "删除确认选择否后记录和余额保持；编辑取消后与删除否后的钱包截图 "
                    "SHA-256 同为 4178...00E，当前投影逐像素一致。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-delete-no-confirmation-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-after-delete-no-wallet-sanitized.png",
                ],
            },
            {
                "name": "确认删除与冷启动清理",
                "status": "observed",
                "observations": (
                    "再次删除选择是后钱包恢复 2,986.44、记录数恢复 243；冷启动截图与既有"
                    "删除态基线 SHA-256 同为 0243...DEA，测试记录仍不存在。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-after-delete-yes-wallet-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-cold-restart-deleted-wallet-sanitized.png",
                    "artifacts/runtime-validation/backups/test-after-rt03-wallet-withdrawal-continuation-cancel-deleted-20260731T204510.mh8",
                ],
            },
            {
                "name": "文件级基线恢复",
                "status": "observed",
                "observations": (
                    "最终等待全部 MoneyHome8 同名进程退出后恢复 test.mh8 到 D8E4...165AC，"
                    "进程数为 0；软件生成的 ~$test 仅观察，未手工处理。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/RT03-wallet-withdrawal-continuation-cancel-notes.md"
                ],
            },
        ],
        "commands": [
            {
                "component": "提现编辑器",
                "label": "保存并继续",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "提交完整有效提现草稿。",
                "confirmation": None,
                "outcome": "保存一条记录并保留编辑器，只保留钱包账户和日期。",
                "status": "pass",
            },
            {
                "component": "提现编辑器标题栏",
                "label": "关闭",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "修改已保存记录后直接关闭。",
                "confirmation": None,
                "outcome": "无提示放弃未提交修改，原业务事实保持。",
                "status": "pass",
            },
            {
                "component": "删除确认框",
                "label": "否",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "在删除确认中选择否。",
                "confirmation": "您确定删除此记录吗？",
                "outcome": "关闭确认框，记录、余额和查询投影零变化。",
                "status": "pass",
            },
            {
                "component": "删除确认框",
                "label": "是",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "再次删除并选择是。",
                "confirmation": "您确定删除此记录吗？",
                "outcome": "删除本轮记录并恢复全部业务投影。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": [
                "稳定微信钱包 ID 和 Cash-CNY 资金去向 ID",
                "本金 1.00、手续费 0.10、日期和唯一备注",
                "编辑取消草稿中的手续费 0.20 和 CANCELLED 备注",
            ],
            "reads": [
                "钱包与目标账户状态、币种和余额版本",
                "被编辑或删除交易的稳定 ID、当前版本和原组成",
            ],
            "writes": [
                "保存并继续只提交第一份有效提现交易",
                "编辑关闭和删除否不得写入交易、分录、余额或审计事实",
                "删除是完整撤销本轮交易影响并记录删除审计",
            ],
            "derived_results": [
                "保存后钱包 2,985.34、流出 1.10、记录数 244",
                "两个取消分支后业务投影保持不变",
                "确认删除后钱包 2,986.44、记录数 243",
            ],
            "side_effects": [
                "保存并继续重置下一条草稿的可变交易字段",
                "编辑标题栏关闭不显示未保存修改确认",
                "删除否与编辑关闭均保持当前查询投影不变",
            ],
            "rollback": (
                "本轮证明用户取消路径零写入；校验失败、并发冲突、数据库失败和进程崩溃"
                "下的技术回滚仍待验证。"
            ),
        },
        "evidence": [
            evidence(
                "manual_note",
                "artifacts/runtime-validation/RT03-wallet-withdrawal-continuation-cancel-notes.md",
                "提现保存并继续字段矩阵、两个取消分支、截图哈希和基线恢复。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-after-save-sanitized.png",
                "保存并继续后保留钱包和日期、重置其它字段。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-after-edit-cancel-wallet-sanitized.png",
                "编辑关闭后原记录和余额保持。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-after-delete-no-wallet-sanitized.png",
                "删除否后记录和余额保持。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-wallet-withdrawal-continuation-cold-restart-deleted-wallet-sanitized.png",
                "确认删除后的冷启动基线钱包状态。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/test-after-rt03-wallet-withdrawal-continuation-cancel-deleted-20260731T204510.mh8",
                "已通过冷启动复核的删除清理状态账簿。",
            ),
        ],
        "requirements_update": [
            "充值与提现保存并继续成功后都保留钱包账户和业务日期，重置对方账户、金额、手续费、标签、备注和附件草稿。",
            "保存并继续只能提交一次当前草稿并生成新的草稿实例，重复点击不得重放上一交易。",
            "编辑已保存交易后关闭窗口必须零写入；Rust 版应提供明确取消语义。",
            "删除确认选择否必须零写入，交易版本、余额、记录数、投影和审计状态均保持。",
            "取消与确认删除都必须使用稳定交易 ID 和版本，避免当前选中行变化导致误操作。",
            "冷启动兼容验收必须比较业务事实和投影，不能要求旧 Jet 文件字节恒等。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证钱包提现的保存并继续字段保留策略、编辑关闭放弃修改、删除否零写入，"
                "并完成确认删除、冷启动清理和精确基线恢复；充值与提现对应分支现均有动态证据。"
            ),
            "remaining_gaps": [
                "附件、标签与内联新建账户在保存并继续后的保留策略",
                "钱包费用报表分类和提现费用修改差额重算",
                "校验失败、重复提交、并发冲突、数据库失败和崩溃中断回滚",
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
