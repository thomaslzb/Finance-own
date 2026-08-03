"""生成 RT-03-024 余额调整完整生命周期记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "artifacts"
    / "runtime-validation"
    / "RT-03-024-20260731T213300+0800.json"
)


def evidence(kind: str, path: str, description: str) -> dict:
    """构造运行记录中的证据项。"""

    return {"kind": kind, "path": path, "description": description}


def main() -> None:
    """写出余额调整创建、反向修改、取消、删除和冷启动结论。"""

    record = {
        "schema_version": 1,
        "execution_id": "RT-03-024",
        "resource": "TNEWRECTRANSDLGFM",
        "observed_at": "2026-07-31T21:33:00+08:00",
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
                "test-before-rt03-balance-adjustment-lifecycle-20260731T210141.mh8"
            ),
        },
        "navigation": {
            "entry_point": "账户中心 -> Cash-CNY -> 行操作 -> 余额调整",
            "steps": [
                "核对 test.mh8、MoneyHome8 进程、~$test 观察状态和基线指纹",
                "把 Cash-CNY 账面余额 608.00 调整为真实余额 609.00",
                "核对账户流水、账户组、净资产和全局财务记录",
                "加载原记录，验证编辑关闭取消，再把真实余额改为 607.00",
                "正常退出并冷启动复核负向调整",
                "分别验证删除否和删除是，核对完整冲销",
                "再次冷启动复核删除态并恢复精确基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "正向余额调整",
                "status": "observed",
                "observations": (
                    "账面余额 608.00、真实余额 609.00 生成单条流入 1.00；"
                    "Cash-CNY=609.00、CASH=9,496.70、净资产=7,095,608.18。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-plus-typechars-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-plus-account-center-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-plus-financial-records-sanitized.png",
                ],
            },
            {
                "name": "编辑加载与取消",
                "status": "observed",
                "observations": (
                    "修改页保持原始账面基线 608.00 和当前真实余额 609.00；"
                    "临时改为 610.00 后关闭不写入，原 +1.00 记录和投影保持。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-edit-loaded-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-edit-cancel-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-after-edit-cancel-financial-records-sanitized.png",
                ],
            },
            {
                "name": "修改跨零改变符号",
                "status": "observed",
                "observations": (
                    "把同一调整的真实余额从 609.00 改为 607.00 后，没有新增记录；"
                    "原流入 1.00 被替换为流出 1.00，Cash-CNY=607.00、"
                    "CASH=9,494.70、净资产=7,095,606.18，记录数保持。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-minus-edit-filled-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-minus-financial-records-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-minus-cold-restart-cash-ledger-sanitized.png",
                    "artifacts/runtime-validation/backups/test-after-rt03-balance-adjustment-minus-verified-20260731T212100.mh8",
                ],
            },
            {
                "name": "删除取消与完整冲销",
                "status": "observed",
                "observations": (
                    "删除否保持负向记录和 607.00 余额；删除是移除调整并恢复"
                    "Cash-CNY=608.00、CASH=9,495.70、净资产=7,095,607.18、记录数 9。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-delete-confirmation-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-after-delete-no-cash-ledger-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-after-delete-yes-account-center-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-deleted-cold-restart-cash-ledger-sanitized.png",
                ],
            },
            {
                "name": "动态类型和本位币投影",
                "status": "observed",
                "observations": (
                    "差额类型菜单显示余额调整和日常收支两个选项；默认余额调整按正负差额进入"
                    "全局流入或流出汇总。本位币 CNY 的币种列隐藏，但账户币种明确。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-type-menu-sanitized.png",
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-minus-financial-records-sanitized.png",
                ],
            },
            {
                "name": "旧控件输入状态异常",
                "status": "observed",
                "observations": (
                    "WM_SETTEXT 只改变 TMHCalcuEdit 显示文本而未同步内部金额，随后自动化路径出现"
                    "EAccessViolation；改用控件键盘消息链后生命周期操作成功。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-application-error-sanitized.png",
                    "artifacts/runtime-validation/backups/test-after-rt03-balance-adjustment-access-violation-20260731T210843.mh8",
                ],
            },
            {
                "name": "删除态冷启动与基线恢复",
                "status": "observed",
                "observations": (
                    "删除态冷启动后业务事实保持；首次删除态退出为 F841...2536，"
                    "仅冷启动再退出后为 75A5...B621，说明旧 Jet 文件存在非业务改写。"
                    "最终 test.mh8 恢复 D8E4...165AC，MoneyHome8 进程数为 0。"
                ),
                "evidence_paths": [
                    "artifacts/runtime-validation/backups/test-after-rt03-balance-adjustment-deleted-20260731T212926.mh8",
                    "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-deleted-cold-restart-initial-sanitized.png",
                    "artifacts/runtime-validation/RT03-balance-adjustment-lifecycle-notes.md",
                ],
            },
        ],
        "commands": [
            {
                "component": "余额调整编辑器",
                "label": "确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "分别提交真实余额 609.00 和修改后的 607.00。",
                "confirmation": None,
                "outcome": "创建正差额事件，并在修改时按同一交易身份替换为负差额事件。",
                "status": "pass",
            },
            {
                "component": "余额调整编辑器",
                "label": "关闭",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "修改草稿为 610.00 后关闭。",
                "confirmation": None,
                "outcome": "草稿丢弃，账簿和业务投影不变。",
                "status": "pass",
            },
            {
                "component": "账户流水操作菜单",
                "label": "删除",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "先选择否，再次删除并选择是。",
                "confirmation": "您确定删除此记录吗？",
                "outcome": "否分支零写入；是分支完整撤销调整和所有派生投影。",
                "status": "pass",
            },
        ],
        "data_flow": {
            "inputs": [
                "稳定账户 ID：Cash-CNY",
                "有效日期 2026-07-31、账面余额 608.00 和余额版本",
                "真实余额 609.00 或 607.00、差额类型、备注",
            ],
            "reads": [
                "账户状态、币种 CNY、有效日期账面余额和调整交易版本",
                "修改时的原始账面基线、原真实余额和原差额方向",
            ],
            "writes": [
                "可审计余额调整交易及正向或负向账户分录",
                "账面基线、真实目标、计算差额、差额类型、日期和备注关系",
                "修改版本和删除撤销状态或等价审计事件",
            ],
            "derived_results": [
                "正差额时 Cash-CNY/CASH/净资产各增加 1.00",
                "负差额时 Cash-CNY/CASH/净资产各减少 1.00",
                "修改不增加记录数，删除后所有业务投影恢复基线",
            ],
            "side_effects": [
                "账户流水、账户中心、全局财务记录和汇总立即刷新并通过冷启动保持",
                "CNY 在全局列表隐藏币种显示文本，但领域币种仍为 CNY",
                "旧 Jet 文件打开关闭可能发生与业务事实无关的字节改写",
            ],
            "rollback": (
                "本轮验证编辑关闭、删除否的零写入、确认删除的完整撤销和最终文件级基线恢复；"
                "余额版本冲突、重复提交、数据库失败和进程崩溃回滚仍待验证。"
            ),
        },
        "evidence": [
            evidence(
                "manual_note",
                "artifacts/runtime-validation/RT03-balance-adjustment-lifecycle-notes.md",
                "创建、修改、取消、删除、冷启动、异常和基线恢复时间线。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-plus-account-center-sanitized.png",
                "正差额后的账户、分组和净资产投影。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-minus-financial-records-sanitized.png",
                "同一调整修改为负差额后的全局单边流出。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-delete-confirmation-sanitized.png",
                "删除余额调整前的显式确认。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-deleted-cold-restart-cash-ledger-sanitized.png",
                "删除态冷启动后调整行不存在且余额恢复。",
            ),
            evidence(
                "screenshot",
                "artifacts/runtime-validation/screenshots/rt03-balance-adjustment-application-error-sanitized.png",
                "旧自定义金额控件显示值和内部状态失配后的访问异常。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/test-after-rt03-balance-adjustment-minus-verified-20260731T212100.mh8",
                "已通过冷启动复核的负向修改状态账簿。",
            ),
            evidence(
                "file",
                "artifacts/runtime-validation/backups/test-after-rt03-balance-adjustment-deleted-20260731T212926.mh8",
                "首次正常退出后的删除状态账簿。",
            ),
        ],
        "requirements_update": [
            "余额调整必须保存稳定账户、币种、有效日期、余额版本、账面基线、真实目标和计算差额。",
            "正差额生成调整流入，负差额生成调整流出；页面不得直接覆盖当前余额。",
            "修改以稳定交易 ID 和预期版本替换同一事实，跨零改符号不得新增重复记录。",
            "编辑关闭和删除否必须零写入；确认删除必须完整撤销账户、分组、净资产和查询投影。",
            "本位币即使隐藏显示文字，交易、分录、接口、导出和审计仍必须保存明确 CNY。",
            "金额编辑器必须由单一强类型状态驱动，禁止显示文本与内部数值分离。",
            "冷启动投影必须从领域事实确定性重建，不能用旧 Jet 文件字节恒等作为兼容标准。",
        ],
        "result": {
            "status": "partial",
            "summary": (
                "已真实验证 Cash-CNY 余额调整的正向创建、编辑取消、跨零负向修改、"
                "删除否、确认删除、修改态和删除态冷启动及最终基线恢复。"
            ),
            "remaining_gaps": [
                "保存并继续后的草稿保留策略",
                "差额类型日常收支的分类和报表口径",
                "零差额、负余额、关闭账户、多币种及历史未来日期",
                "余额版本冲突、重复提交、数据库失败和崩溃中断回滚",
                "系统对手分录和其它账户域的具体差异",
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
