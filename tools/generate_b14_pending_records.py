from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T11:55:00+08:00"
STAMP = "20260730T115500+0800"
BASELINE_SHA = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"


def base_record(execution_id: str, resource: str, entry_point: str) -> dict:
    """创建 B14 记录共享的应用、账簿和隔离边界。"""
    return {
        "schema_version": 1,
        "execution_id": execution_id,
        "resource": resource,
        "observed_at": OBSERVED_AT,
        "application": {
            "executable": "C:\\Program Files (x86)\\MoneyWise\\MoneyHome8\\Program\\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": "C:\\DCG-SZ\\IT Manage\\Private\\Personal-Docs\\test.mh8",
            "sha256_before": BASELINE_SHA,
            "sha256_after": BASELINE_SHA,
            "backup_artifact": "artifacts/runtime-validation/backups/test-before-b14-pending-close-20260730.mh8",
        },
        "navigation": {
            "entry_point": entry_point,
            "steps": [
                "仅在 PID 28128 的专用 MoneyHome8 实例中操作指定测试账簿",
                "创建零余额人民币临时家居物品账户并检查物品工作区",
                "取消所有交易编辑器，删除临时账户并正常退出专用进程",
                "保留退出态副本并恢复操作前账簿指纹",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
    }


def value_change_record() -> dict:
    """记录物品价值变更编辑器的动态字段和未提交路径。"""
    record = base_record(
        "RT-14-003", "TASSETINCREMENTDLGFM", "物品账户 -> 记账 -> 物品价值变更"
    )
    record.update(
        states=[
            {
                "name": "价值变更编辑器",
                "status": "observed",
                "observations": "动态窗口提供物品账户、物品分类、物品名称、重估前价值、重估后价值、标签、备注和日期。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b14-item-value-change-dialog-sanitized.png"
                ],
            },
            {
                "name": "空账户状态",
                "status": "observed",
                "observations": "无持有物品时分类和名称为空，重估前价值只读为 0.00，重估后价值可编辑且未提交。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b14-item-value-change-dialog-sanitized.png"
                ],
            },
        ],
        commands=[
            {
                "component": "物品记账菜单",
                "label": "物品价值变更",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "选择记账菜单第三项",
                "confirmation": None,
                "outcome": "打开物品价值变更编辑器；本轮关闭且未保存。",
                "status": "pass",
            }
        ],
        data_flow={
            "inputs": ["物品账户、分类、物品、重估后价值、标签、备注和日期"],
            "reads": ["选中物品在变更日前的有效价值"],
            "writes": ["物品估值事件；本轮未提交"],
            "derived_results": ["最新市值、未实现损益和成本市值构成投影"],
            "side_effects": ["不得生成资金收支或改变购买成本"],
            "rollback": "估值事件与全部派生投影必须同事务失效或回滚。",
        },
        evidence=[
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b14-item-value-change-dialog-sanitized.png",
                "description": "脱敏后的物品价值变更编辑器。",
            },
            {
                "kind": "manual_note",
                "path": "docs/runtime-major-and-tangible-assets-contract.md",
                "description": "Rust 重大资产、家居物品、估值和分期合同。",
            },
        ],
        requirements_update=[
            "价值变更保存独立估值事件，不覆盖原始买入成本。",
            "重估前价值按交易日之前的有效事件计算并保持只读。",
            "无持有物品时禁止提交，不能生成零值占位记录。",
            "估值变化不自动生成资金流水或已实现收益。",
        ],
        result={
            "status": "partial",
            "summary": "已动态确认物品价值变更窗口、字段、空账户状态和取消路径。",
            "remaining_gaps": [
                "有持仓物品选择和重估前价值口径",
                "真实保存、同日多次变更及撤销规则",
                "市值、损益、报表和失败回滚的精确联动",
            ],
        },
    )
    return record


def installment_record() -> dict:
    """记录物品买入分期向导的真实宿主和当前隐藏入口限制。"""
    record = base_record(
        "RT-14-017",
        "TPRACBUYINSTALLMENTWIZARDDLG",
        "物品账户 -> 记账 -> 物品买入 -> TPracBuyEditFrame.btnInstallmentClick",
    )
    record["navigation"]["steps"].insert(
        2,
        "确认普通买入模式的分期按钮存在但不可见，直接触发其已绑定点击事件打开向导",
    )
    record.update(
        states=[
            {
                "name": "向导第一页",
                "status": "observed",
                "observations": "真实打开 TPracBuyInstallmentWizardDlg，第一页标题为物品买入信息，复用物品账户、分类、名称、单价、数量、金额、标签、日期和备注字段。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b14-item-installment-page1-sanitized.png"
                ],
            },
            {
                "name": "前置校验",
                "status": "observed",
                "observations": "缺少物品分类时点击下一步，明确提示“请选择或输入物品分类”，页面未推进且没有写入。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b14-item-installment-validation-message-raw.png"
                ],
            },
            {
                "name": "后续页面结构",
                "status": "pending",
                "observations": "DFM 静态确认分期信息与确认信息两页，组合 TInstallmentEditFrame，并在完成页说明将生成的内容；本轮未绕过前置校验动态推进。",
                "evidence_paths": [
                    "docs/runtime-dfm-control-catalog.md",
                    "docs/runtime-form-composition-evidence.md",
                ],
            },
        ],
        commands=[
            {
                "component": "TPracBuyEditFrame.btnInstallment",
                "label": "分期付款",
                "initial_state": {"enabled": True, "visible": False},
                "trigger": "直接投递该隐藏控件的已绑定点击事件",
                "confirmation": None,
                "outcome": "打开物品买入分期向导；普通买入模式下该控件被资金账户选择器覆盖。",
                "status": "partial",
            },
            {
                "component": "向导导航",
                "label": "下一步",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "在缺少物品分类时点击",
                "confirmation": "请选择或输入物品分类",
                "outcome": "阻止推进，未产生任何业务写入。",
                "status": "pass",
            },
        ],
        data_flow={
            "inputs": ["物品买入信息、分期本金、期数、手续费、利息、首次记账日和资金账户"],
            "reads": ["物品主数据、账户币种、分期配置和交易日期"],
            "writes": ["物品买入、分期协议及计划分录；本轮均未提交"],
            "derived_results": ["每期本金、手续费、利息、未还期数和确认页摘要"],
            "side_effects": ["完成时可能生成物品持仓、分期负债和计划交易"],
            "rollback": "买入、持仓、分期协议和计划分录必须原子提交，失败不得留下半成品。",
        },
        evidence=[
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b14-item-installment-page1-sanitized.png",
                "description": "脱敏后的物品买入分期向导第一页。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b14-item-installment-validation-message-raw.png",
                "description": "物品分类必填校验。",
            },
            {
                "kind": "manual_note",
                "path": "artifacts/runtime-validation/B14-pending-close-notes.md",
                "description": "隐藏入口、动态向导、临时账户和账簿恢复记录。",
            },
        ],
        requirements_update=[
            "Rust 必须把分期入口放在用户可见且可解释的位置，不复制当前隐藏控件状态。",
            "向导第一页通过物品必填校验后才允许创建分期草稿。",
            "买入、持仓、负债和计划交易在完成操作中原子提交。",
            "取消或任一步校验失败不得保留分期协议或占位持仓。",
        ],
        result={
            "status": "partial",
            "summary": "已动态打开物品买入分期向导并确认第一页和必填校验；当前版本普通买入模式下入口不可见。",
            "remaining_gaps": [
                "分期入口在何种正式业务模式下可见",
                "分期信息和确认页的动态值与计算公式",
                "完成后的持仓、负债、计划交易及失败回滚",
            ],
        },
    )
    return record


def constituent_record() -> dict:
    """记录物品成本市值构成页的动态空状态和投影边界。"""
    record = base_record(
        "RT-14-025", "TASSETSCONSTITUTECHARTFRAME", "物品账户 -> 成本市值构成页签"
    )
    record.update(
        states=[
            {
                "name": "最终宿主页签",
                "status": "observed",
                "observations": "物品工作区下半区在交易明细与成本市值构成之间切换；构成页左右展示成本与市值图形区域。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b14-item-cost-market-constituent-empty-sanitized.png"
                ],
            },
            {
                "name": "空投影",
                "status": "observed",
                "observations": "零持仓账户的购买均价、数量、购买成本和市值列表为空，成本合计和市值合计均为 0.00，两侧明确显示无数据显示。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b14-item-cost-market-constituent-empty-sanitized.png"
                ],
            },
        ],
        commands=[
            {
                "component": "物品工作区页签",
                "label": "成本市值构成",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "切换到成本市值构成",
                "confirmation": None,
                "outcome": "显示成本、市值双投影；空账户不绘制伪造扇区。",
                "status": "pass",
            }
        ],
        data_flow={
            "inputs": ["账户、持仓范围和查询时点"],
            "reads": ["物品持仓数量、购买成本和查询时点有效市值"],
            "writes": ["只读投影不写业务数据"],
            "derived_results": ["分类或物品维度的成本、市值及其合计"],
            "side_effects": ["切换页签不改变账户或估值"],
            "rollback": "只读查询失败时保持旧快照或错误态，不写入空结果。",
        },
        evidence=[
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b14-item-cost-market-constituent-empty-sanitized.png",
                "description": "裁掉私人账户树后的成本市值构成空状态。",
            },
            {
                "kind": "manual_note",
                "path": "docs/runtime-major-and-tangible-assets-contract.md",
                "description": "Rust 成本、市值、估值事件和查询投影合同。",
            },
        ],
        requirements_update=[
            "购买成本和当前市值使用不同数据来源，不得互相覆盖。",
            "成本、市值列表、合计和图形必须来自同一查询快照。",
            "零持仓返回零合计和明确空状态，不绘制零值扇区。",
            "查询时点市值取不晚于该时点的最新有效估值。",
        ],
        result={
            "status": "partial",
            "summary": "已动态确认成本市值构成页的最终宿主、双投影布局和零持仓空状态。",
            "remaining_gaps": [
                "有持仓时的分组维度、颜色、排序和百分比",
                "缺失估值、负值、跨币种和历史查询时点",
                "列表、图形、合计及导出打印的一致性",
            ],
        },
    )
    return record


def main() -> None:
    """写出 B14 三个剩余执行项的最新结构化记录。"""
    for record in [value_change_record(), installment_record(), constituent_record()]:
        path = ARTIFACT_DIR / f"{record['execution_id']}-{STAMP}.json"
        path.write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
