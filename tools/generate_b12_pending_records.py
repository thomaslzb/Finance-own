from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T14:20:00+08:00"
STAMP = "20260730T142000+0800"
BASELINE_SHA = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
EXIT_STATE_SHA = "A83CB2AA3ABAA1783CE01CBD262DB0C30A53CD7D6542C3A47269F078A4505E1D"
BEFORE_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "test-before-b12-contract-calibration-20260730.mh8"
)
EXIT_STATE_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "test-after-b12-contract-calibration-before-restore-20260730.mh8"
)
BATCH_OBSERVED_AT = "2026-07-31T13:31:47+08:00"
BATCH_STAMP = "20260731T133147+0800"
BATCH_EXIT_STATE_SHA = (
    "72D1F4133B99C6A07580C2792E8BCCF68794AF11AC5CF0C5C09DF89A2A31E2DE"
)
BATCH_BEFORE_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "test-before-b12-batch-direct-payment-20260731.mh8"
)
BATCH_EXIT_STATE_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "test-after-b12-batch-direct-payment-unavailable-20260731.mh8"
)


def base_record(
    execution_id: str,
    resource: str,
    entry_point: str,
    steps: list[str],
) -> dict:
    """创建基于真实临时合同的共享运行记录。"""
    return {
        "schema_version": 1,
        "execution_id": execution_id,
        "resource": resource,
        "observed_at": OBSERVED_AT,
        "application": {
            "executable": (
                "C:\\Program Files (x86)\\MoneyWise\\MoneyHome8\\Program\\"
                "MoneyHome8.exe"
            ),
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": "C:\\DCG-SZ\\IT Manage\\Private\\Personal-Docs\\test.mh8",
            "sha256_before": BASELINE_SHA,
            "sha256_after": BASELINE_SHA,
            "backup_artifact": BEFORE_BACKUP,
        },
        "navigation": {
            "entry_point": entry_point,
            "steps": steps,
            "reachable": True,
            "unreachable_reason": None,
        },
    }


def direct_repayment_record(
    execution_id: str,
    resource: str,
    title: str,
    contract_kind: str,
    contract_number: str,
    value_label: str,
    value_hint: str,
    value_default: str,
    screenshot: str,
) -> dict:
    """记录单份融资或融券合同的直接偿还窗口。"""
    record = base_record(
        execution_id,
        resource,
        f"融资融券账户 -> 选择具体{contract_kind}合同 -> {title}",
        [
            "备份 test.mh8 并启动隔离 MoneyHome8 进程",
            "创建临时融资融券账户 Codex-B12-Contract-20260730",
            f"创建合同 {contract_number}，形成未偿{value_label}",
            f"从真实合同上下文打开{title}窗口",
            "核对账户、合同、默认值、日期、标签、备注和按钮后关闭，不保存",
            "删除临时账户并退出隔离进程",
            "保存退出状态副本，再将 test.mh8 恢复为运行前备份并复核指纹",
        ],
    )
    record.update(
        states=[
            {
                "name": "真实合同上下文",
                "status": "observed",
                "observations": (
                    f"窗口显示临时账户、{contract_kind}合同 {contract_number}；"
                    f"提示“{value_hint}”。"
                ),
                "evidence_paths": [screenshot],
            },
            {
                "name": "初始录入值",
                "status": "observed",
                "observations": (
                    f"{value_label}默认 {value_default}，返还利息默认 0.00，"
                    "日期默认 2026-07-30，并提供标签和备注字段。"
                ),
                "evidence_paths": [screenshot],
            },
            {
                "name": "取消路径",
                "status": "observed",
                "observations": (
                    "窗口提供“保存并继续”和“确定”；本轮使用标题栏关闭，"
                    "未提交偿还，退出后账簿恢复到运行前同一 SHA-256。"
                ),
                "evidence_paths": [screenshot, EXIT_STATE_BACKUP],
            },
        ],
        commands=[
            {
                "component": f"{contract_kind}合同上下文",
                "label": title,
                "initial_state": {"enabled": True, "visible": True},
                "trigger": f"选择存在未偿余额的{contract_kind}合同",
                "confirmation": None,
                "outcome": f"已打开{title}并加载合同默认值；关闭时未保存。",
                "status": "partial",
            },
            {
                "component": "btnSaveNext/btnOK",
                "label": "保存并继续/确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "本轮未点击",
                "confirmation": None,
                "outcome": "成功写入、校验提示和失败回滚尚未验证。",
                "status": "partial",
            },
        ],
        data_flow={
            "inputs": [
                f"融资融券账户、{contract_kind}合同、{value_label}、返还利息、日期、标签、备注"
            ],
            "reads": [
                f"{contract_kind}合同号、证券、未偿本金或数量、累计利息和账户资产"
            ],
            "writes": [
                "预计写入偿还事件、合同剩余量、资金或证券分录；本轮未提交，写入结构待验证"
            ],
            "derived_results": [
                "窗口由合同未偿值初始化偿还上限；保存后的余额、利息和风险统计待验证"
            ],
            "side_effects": [
                "成功保存预计联动现金或证券持仓、合同状态和负债汇总；本轮未触发"
            ],
            "rollback": "偿还事件、资金或证券分录、利息和合同状态必须原子提交。",
        },
        evidence=[
            {
                "kind": "screenshot",
                "path": screenshot,
                "description": f"脱敏后的真实{contract_kind}合同{title}窗口及默认值。",
            },
            {
                "kind": "manual_note",
                "path": "artifacts/runtime-validation/B12-pending-close-notes.md",
                "description": "临时合同、隔离进程、取消路径、清理和账簿恢复证据。",
            },
            {
                "kind": "manual_note",
                "path": EXIT_STATE_BACKUP,
                "description": (
                    f"隔离进程退出状态备份，SHA-256 为 {EXIT_STATE_SHA}；"
                    "仅用于复核运行副作用，不作为当前 test.mh8。"
                ),
            },
        ],
        requirements_update=[
            f"{title}必须从具体{contract_kind}合同进入，并显示合同未偿值作为默认上限。",
            "本金或数量与利息分别保存，不能仅用一个净额覆盖。",
            "日期、标签和备注随偿还事件保存，保存并继续必须清空上一笔草稿并保留账户上下文。",
            "重复提交使用幂等键，不能重复减少合同余额或重复扣减资产。",
            "缺少有效合同、偿还值为零或超过未偿上限时禁止提交。",
        ],
        result={
            "status": "partial",
            "summary": (
                f"已用真实{contract_kind}合同动态打开{title}并确认合同绑定、"
                f"未偿提示、默认{value_label}、利息、日期和取消路径；未验证保存。"
            ),
            "remaining_gaps": [
                "零值、负值、超过未偿上限和资产不足的校验提示",
                "真实偿还、利息分配、幂等、撤销、失败回滚和统计联动",
                "保存并继续后的字段重置、焦点和下一份合同选择行为",
            ],
        },
    )
    return record


def edit_contract_record() -> dict:
    """记录真实融资合同的编辑窗口及取消路径。"""
    screenshot = (
        "artifacts/runtime-validation/screenshots/"
        "b12-edit-margin-contract-sanitized.png"
    )
    record = base_record(
        "RT-12-008",
        "TEDITMARGINCONTRACTDLGFM",
        "融资融券账户 -> 选择融资合同 -> 编辑融资融券",
        [
            "备份 test.mh8 并启动隔离 MoneyHome8 进程",
            "创建临时融资融券账户 Codex-B12-Contract-20260730",
            "创建融资合同 FM-CODEX-20260730-1",
            "从真实融资合同上下文打开编辑融资融券窗口",
            "核对合同号、利率、证券、更新代码和保存按钮后关闭，不保存",
            "删除临时账户并退出隔离进程",
            "保存退出状态副本，再将 test.mh8 恢复为运行前备份并复核指纹",
        ],
    )
    record.update(
        states=[
            {
                "name": "真实融资合同",
                "status": "observed",
                "observations": (
                    "窗口标题为“融资融券合约”，合同号为 FM-CODEX-20260730-1，"
                    "年利率为 1.00，对应证券为 002594 比亚迪。"
                ),
                "evidence_paths": [screenshot],
            },
            {
                "name": "类型显示",
                "status": "observed",
                "observations": (
                    "窗口存在“类型”标签，但本次融资合同的可见值为空；"
                    "Rust 版不能依赖空显示推断合同类型，必须读取稳定类型字段。"
                ),
                "evidence_paths": [screenshot],
            },
            {
                "name": "取消路径",
                "status": "observed",
                "observations": (
                    "“更新代码”和“保存”按钮可见；本轮标题栏关闭且未保存，"
                    "退出后账簿恢复到运行前同一 SHA-256。"
                ),
                "evidence_paths": [screenshot, EXIT_STATE_BACKUP],
            },
        ],
        commands=[
            {
                "component": "合同上下文",
                "label": "编辑融资融券",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "选择已存在的融资合同",
                "confirmation": None,
                "outcome": "已加载真实合同字段，关闭时未保存。",
                "status": "partial",
            },
            {
                "component": "btnUpdateCode/btnOK",
                "label": "更新代码/保存",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "本轮未点击",
                "confirmation": None,
                "outcome": "证券代码更新、字段校验和持久化行为尚未验证。",
                "status": "partial",
            },
        ],
        data_flow={
            "inputs": ["合同类型、年利率、合同号、对应证券和证券代码"],
            "reads": [
                "现有融资合同 FM-CODEX-20260730-1、证券主数据和合同引用关系"
            ],
            "writes": ["预计写入合同资料或更正事件；本轮未提交，写入结构待验证"],
            "derived_results": ["后续利息计提、合同显示代码和风险投影"],
            "side_effects": [
                "修改可能影响未来计息和合同查询，但不得静默重写已结算历史"
            ],
            "rollback": "合同版本、证券映射和派生投影必须原子更新；冲突时保留旧版本。",
        },
        evidence=[
            {
                "kind": "screenshot",
                "path": screenshot,
                "description": "脱敏后的真实融资合同编辑窗口和加载值。",
            },
            {
                "kind": "manual_note",
                "path": "artifacts/runtime-validation/B12-pending-close-notes.md",
                "description": "临时合同、隔离进程、取消路径、清理和账簿恢复证据。",
            },
            {
                "kind": "manual_note",
                "path": EXIT_STATE_BACKUP,
                "description": (
                    f"隔离进程退出状态备份，SHA-256 为 {EXIT_STATE_SHA}；"
                    "仅用于复核运行副作用，不作为当前 test.mh8。"
                ),
            },
        ],
        requirements_update=[
            "合同编辑必须从稳定合同 ID 进入，显示类型、利率、合同号和对应证券。",
            "类型必须有明确值；旧版空显示作为兼容缺陷记录，不复制到 Rust 版。",
            "修改利率默认只影响生效日后的计提；历史重算必须是显式更正操作。",
            "更新证券代码不得改变证券稳定 ID，也不能破坏历史交易引用。",
            "并发编辑使用版本检查，冲突时禁止静默覆盖。",
        ],
        result={
            "status": "partial",
            "summary": (
                "已用真实融资合同动态打开编辑窗口并确认合同号、年利率、证券、"
                "类型空显示、更新代码、保存和取消路径；未验证字段修改与保存。"
            ),
            "remaining_gaps": [
                "利率、合同号和证券代码的校验、更新与持久化行为",
                "融券合同编辑状态及类型字段显示差异",
                "历史计息、并发冲突、撤销和失败回滚",
            ],
        },
    )
    return record


def batch_direct_payment_record() -> dict:
    """记录真实未结融资合同在批量直接还款中的候选解析失败。"""
    before_dialog = (
        "artifacts/runtime-validation/screenshots/"
        "b12-batch-direct-payment-with-contract-before-save-sanitized.png"
    )
    after_restart_dialog = (
        "artifacts/runtime-validation/screenshots/"
        "b12-batch-direct-payment-after-restart-sanitized.png"
    )
    edit_attempt = (
        "artifacts/runtime-validation/screenshots/"
        "b12-batch-grid-edit-attempt-sanitized.png"
    )
    validation_message = (
        "artifacts/runtime-validation/screenshots/"
        "b12-batch-empty-row-validation-sanitized.png"
    )
    contract_before_restart = (
        "artifacts/runtime-validation/screenshots/"
        "b12-batch-financing-saved-before-repayment-sanitized.png"
    )
    contract_after_restart = (
        "artifacts/runtime-validation/screenshots/"
        "b12-batch-after-restart-contract-sanitized.png"
    )
    record = base_record(
        "RT-12-003",
        "TBATCHDIRECTPAYMENTSDLGFM",
        "融资融券账户 -> 记账 -> 批量直接还款",
        [
            "确认 test.mh8 路径、进程、恢复文件和运行前基线指纹",
            "创建临时融资融券账户 Codex-B12-Batch-20260731",
            "保存融资合同 FM-BATCH-20260731-1，形成未偿本金 1.00",
            "打开批量直接还款并观察合同候选、合计和账户选择器",
            "正常重启后复核合同、负债和批量候选",
            "使用 F2 激活空白合同行并尝试选择合同",
            "点击确定并记录空行校验提示，不产生还款",
            "正常退出、保存失败路径副本并恢复 test.mh8 基线",
        ],
    )
    record["observed_at"] = BATCH_OBSERVED_AT
    record["ledger"] = {
        "path": "C:\\DCG-SZ\\IT Manage\\Private\\Personal-Docs\\test.mh8",
        "sha256_before": BASELINE_SHA,
        "sha256_after": BASELINE_SHA,
        "backup_artifact": BATCH_BEFORE_BACKUP,
    }
    record.update(
        states=[
            {
                "name": "真实未结融资合同",
                "status": "observed",
                "observations": (
                    "融资合同 FM-BATCH-20260731-1 使用证券 002594 比亚迪、"
                    "价格 1.00、数量 1、年利率 1.00%、佣金 5.00 和总流出 "
                    "6.00 保存。工作区显示融资负债 -1.00、可用资金 -5.00；"
                    "正常重启后合同、持仓和负债仍存在。"
                ),
                "evidence_paths": [
                    contract_before_restart,
                    contract_after_restart,
                ],
            },
            {
                "name": "批量候选初始状态",
                "status": "observed",
                "observations": (
                    "批量直接还款显示当前融资融券账户，但合同表格在重启前后均"
                    "没有自动列出已存在的未结融资合同，还款金额和利息合计均为 0.00。"
                ),
                "evidence_paths": [before_dialog, after_restart_dialog],
            },
            {
                "name": "空行编辑",
                "status": "observed",
                "observations": (
                    "在合同表格首行按 F2 可创建空白行，并显示融资合同下拉编辑器；"
                    "当前样例无法从编辑器解析或选择工作区中可见的未结合同。"
                ),
                "evidence_paths": [edit_attempt],
            },
            {
                "name": "提交校验",
                "status": "observed",
                "observations": (
                    "空白合同行点击确定后提示“请选择合约并输入还款金额”，"
                    "对话框保持打开，未生成还款、利息或资金分录。"
                ),
                "evidence_paths": [validation_message],
            },
            {
                "name": "退出与恢复",
                "status": "observed",
                "observations": (
                    f"失败路径副本 SHA-256 为 {BATCH_EXIT_STATE_SHA}；最终 test.mh8 "
                    f"恢复为 {BASELINE_SHA}，MoneyHome8 进程数为 0。恢复文件未手工修改，"
                    "并把 test.mh8 修改时间置于恢复文件之后，避免下次启动优先载入旧状态。"
                ),
                "evidence_paths": [BATCH_EXIT_STATE_BACKUP],
            },
        ],
        commands=[
            {
                "component": "融资融券记账菜单",
                "label": "批量直接还款",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "存在未结融资合同后打开，重启后再次打开",
                "confirmation": None,
                "outcome": "窗口可达，但未结合同未进入批量候选集合。",
                "status": "partial",
            },
            {
                "component": "TMHTreeList/TdxInplaceTreeListButtonEdit",
                "label": "融资合同",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "在空白首行按 F2",
                "confirmation": None,
                "outcome": "生成可编辑空行，但无法选择已存在合同。",
                "status": "partial",
            },
            {
                "component": "btnSaveExit",
                "label": "确定",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "合同和还款金额为空时点击",
                "confirmation": "请选择合约并输入还款金额",
                "outcome": "保存被阻止，未产生还款写入。",
                "status": "pass",
            },
        ],
        data_flow={
            "inputs": [
                "融资融券账户、融资合同、逐合同还款金额、利息、标签、日期和备注"
            ],
            "reads": [
                "账户内未结融资合同、剩余本金、合同版本、应计利息和账户可用资金"
            ],
            "writes": [
                "本轮仅创建校准账户与融资合同；批量还款校验失败，未写入偿还事件"
            ],
            "derived_results": [
                "合同候选集合为空，还款金额与利息合计保持 0.00"
            ],
            "side_effects": [
                "空行提交只显示校验消息；未改变合同余额、现金、持仓或风险汇总"
            ],
            "rollback": (
                "Rust 版必须先按账户和合同状态解析稳定候选，再在单事务内提交全部分配；"
                "候选缺失或任一行无效时不得产生部分还款。"
            ),
        },
        evidence=[
            {
                "kind": "screenshot",
                "path": contract_before_restart,
                "description": "保存后工作区中的真实融资合同、持仓、负债和交易投影。",
            },
            {
                "kind": "screenshot",
                "path": after_restart_dialog,
                "description": "重启后批量直接还款仍未列出未结融资合同。",
            },
            {
                "kind": "screenshot",
                "path": edit_attempt,
                "description": "F2 激活的空白融资合同编辑行。",
            },
            {
                "kind": "screenshot",
                "path": validation_message,
                "description": "缺少合同和还款金额时的提交阻断提示。",
            },
            {
                "kind": "manual_note",
                "path": "artifacts/runtime-validation/B12-pending-close-notes.md",
                "description": "B12 真实合同、批量候选缺失、重启和恢复记录。",
            },
            {
                "kind": "manual_note",
                "path": BATCH_EXIT_STATE_BACKUP,
                "description": (
                    "包含临时账户和融资合同但没有批量还款的退出状态副本；"
                    f"SHA-256 为 {BATCH_EXIT_STATE_SHA}。"
                ),
            },
        ],
        requirements_update=[
            "批量还款候选必须按稳定账户 ID 查询未结融资合同，不能依赖显示文本、当前选中行或过期缓存。",
            "窗口打开和重启后应自动列出符合条件的合同；手工新增行也只能选择同账户未结合同。",
            "每行必须显式保存合同 ID、合同版本、还款本金和利息，合计由行数据确定性计算。",
            "没有合同、还款金额为空或非正数时必须在提交前返回字段级错误并保持草稿。",
            "全部行校验通过后才能原子更新偿还事件、分配、合同余额、资金分录和风险投影。",
        ],
        result={
            "status": "partial",
            "summary": (
                "已用真实未结融资合同验证批量直接还款的入口、重启、空行编辑和提交校验；"
                "旧程序未能把该合同解析为候选，因此没有伪造成功还款。"
            ),
            "remaining_gaps": [
                "能被批量候选解析的合同形成条件或旧程序筛选规则",
                "真实单合同和多合同保存、利息、资金扣减、合同结清与风险联动",
                "超额、资金不足、重复提交、版本冲突、撤销和整批回滚",
                "批量直接还券的真实合同候选与保存行为",
            ],
        },
    )
    return record


def main() -> None:
    """写出 B12 真实合同条件入口与批量候选失败记录。"""
    records = [
        direct_repayment_record(
            "RT-12-001",
            "TALSOCOUPONSDIRECTLYDLGFM",
            "直接还券",
            "融券",
            "SM-CODEX-20260730-1",
            "返还数量",
            "[002594 比亚迪]未还数量：1",
            "1",
            (
                "artifacts/runtime-validation/screenshots/"
                "b12-direct-return-with-contract-sanitized.png"
            ),
        ),
        direct_repayment_record(
            "RT-12-007",
            "TDIRECTPAYMENTSDLGFM",
            "直接还款",
            "融资",
            "FM-CODEX-20260730-1",
            "还款金额",
            "未还金额：1.00",
            "1.00",
            (
                "artifacts/runtime-validation/screenshots/"
                "b12-direct-payment-with-contract-sanitized.png"
            ),
        ),
        edit_contract_record(),
        batch_direct_payment_record(),
    ]
    for record in records:
        stamp = BATCH_STAMP if record["execution_id"] == "RT-12-003" else STAMP
        path = ARTIFACT_DIR / f"{record['execution_id']}-{stamp}.json"
        path.write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
