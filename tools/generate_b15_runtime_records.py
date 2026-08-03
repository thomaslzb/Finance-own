"""生成 B15 预算、提醒、规划与目标的运行态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
OBSERVED_AT = "2026-07-29T22:30:17+08:00"
LEDGER_HASH = "18A99BFCC76727A44A2ABE09C1054953C122EBAEF38E5404D6990F678B300ADD"


def shot(name: str, *, nested: bool = False) -> str:
    base = "artifacts/runtime-validation/screenshots" if nested else "artifacts/runtime-validation"
    return f"{base}/{name}"


RECORDS = {
    "RT-15-001": ("TACCTBALAREMINDDLG", "账户余额提醒", [shot("b15-account-balance-reminder-dialog.png", nested=True)], "账户、低余额阈值、高余额阈值", "已确认账户余额上下限提醒输入结构；未保存新提醒。"),
    "RT-15-002": ("TBUDGETCOPYDLGFM", "复制预算金额", [shot("b15-budget-copy-year-dialog.png")], "目标年度", "已确认复制上一年度入口；运行时实际窗体类为 TInputTextDlgFm，与静态类名不一致。"),
    "RT-15-003": ("TBUDGETLISTFM", "预算", [shot("b15-budget-created.png"), shot("b15-budget-after-delete-refresh.png", nested=True)], "预算周期、分类金额、实际支出", "已创建并删除临时预算，确认预算与实际支出对比、周期切换和空状态。"),
    "RT-15-004": ("TBUYFUNDPLANDLGFM", "基金定投计划", [shot("b15-fund-plan-dialog.png", nested=True)], "计划日期、重复规则、基金、现金账户、费率、定投金额、自动执行", "已确认基金申购/定投计划字段；未保存计划。"),
    "RT-15-005": ("TCREATEBUDGETDLGFM", "新增预算", [shot("b15-budget-create-dialog.png")], "名称、月度/季度/年度周期", "已确认新增预算字段和周期选项。"),
    "RT-15-006": ("TCREDITREMINDDLG", "信用卡透支额提醒", [shot("b15-credit-overdraft-reminder-dialog.png", nested=True)], "信用账户、透支阈值", "已确认信用卡透支提醒输入结构；未保存新提醒。"),
    "RT-15-007": ("TEDITBUDGETAMOUNTDLGFM", "预算金额设置", [shot("b15-budget-amount-dialog.png"), shot("b15-budget-amount-imported.png"), shot("b15-budget-amount-close-confirmation.png")], "十二个月预算金额、最近十二个月实际支出", "已确认十二个月金额网格、实际支出导入、复制菜单和放弃修改确认。"),
    "RT-15-008": ("TEDITBUDGETCATEGORYDLGFM", "选择预算收支项目", [shot("b15-budget-category-dialog.png"), shot("b15-budget-category-modify.png")], "收支分类树、全选、反选、新增分类", "已确认分类树和选择命令。"),
    "RT-15-009": ("TFINANCIALCALENDARDLG", "财务日历", [shot("b15-financial-calendar.png", nested=True)], "年、月、日期、农历、节日与计划事件", "已确认月历、农历/节气、选中日期卡片和事件标记。"),
    "RT-15-010": ("TFINANCIALDIAGNOSISFM", "财务诊断", [shot("b15-financial-diagnosis-input.png"), shot("b15-financial-diagnosis-result.png"), shot("b15-financial-diagnosis-result-lower.png")], "收入、支出、资产、负债及资产性质", "已确认诊断输入、资产性质设置、指标结果和部分显示公式。"),
    "RT-15-011": ("TFINANCIALPLANNINGCENTERFM", "财务规划", [shot("b15-financial-planning-created.png"), shot("b15-planning-after-clear.png", nested=True)], "家庭资料、年度收支、资产、债务、保险、事件和通胀", "已建立并清除临时规划，确认年度余额图、三类页签及专题输入入口。"),
    "RT-15-012": ("TFPANNUALSALARYINFODLGFM", "工资", [shot("b15-planning-salary-dialog.png")], "年工资、结束年度、年增长率", "已确认工资规划输入字段。"),
    "RT-15-013": ("TFPASSETEXPENSESINFODLGFM", "资产带来的支出", [shot("b15-planning-asset-expense-dialog.png")], "资产账户、年支出、期间、增长率", "已确认资产关联支出的输入字段。"),
    "RT-15-014": ("TFPASSETGROWTHINFODLGFM", "资产增长", [shot("b15-planning-asset-growth-dialog.png")], "预期年增长率、结余现金再投资比例", "已确认投资资产增长和再投资比例输入。"),
    "RT-15-015": ("TFPASSETINCOMEINFODLGFM", "资产带来的收入", [shot("b15-planning-asset-income-dialog.png")], "名称、资产账户、年收入、期间、增长率", "已确认资产关联收入的输入字段。"),
    "RT-15-016": ("TFPASSETPURCHASEPLANINFOFM", "资产购置", [shot("b15-planning-asset-purchase-dialog.png", nested=True), shot("b15-planning-asset-purchase-income-tab.png", nested=True), shot("b15-planning-asset-purchase-expense-tab.png", nested=True)], "购置年度与金额、一次性/分期、首付、利率、月供、购置后收支", "已确认资产购置、分期参数和购置后收支页签。"),
    "RT-15-017": ("TFPBASEDLGFM", "财务规划基础对话框", [shot("b15-planning-family-info.png")], "规划专题对话框通用保存/取消框架", "该基类未作为独立页面出现，通用行为由多个规划子类间接覆盖。"),
    "RT-15-018": ("TFPBASEINFODLGFM", "家庭资料", [shot("b15-planning-family-info.png")], "出生年份、预期寿命、配偶信息", "已确认家庭基础资料字段。"),
    "RT-15-019": ("TFPDAILYEXPENSESINFODLGFM", "日常支出", [shot("b15-planning-daily-expense-dialog.png")], "家庭年度生活支出", "已确认日常支出输入字段。"),
    "RT-15-020": ("TFPEDUCATIONEXPENSESINFODLGFM", "教育计划", [shot("b15-planning-education-dialog.png", nested=True)], "名称、年数、年度学费/生活费/其他费用、总额", "已确认教育支出计划输入与合计字段。"),
    "RT-15-021": ("TFPEXPENSESADJUSTMENTINFODLGFM", "支出调整", [shot("b15-planning-expense-adjustment-dialog.png")], "名称、开始/结束年度、调整额", "已确认支出调整期间和负数表示减少的规则。"),
    "RT-15-022": ("TFPINFLATIONRATEINFODLGFM", "通货膨胀率", [shot("b15-planning-inflation-dialog.png", nested=True)], "通货膨胀率", "已确认通胀率作为家庭生活支出年增长参考。"),
    "RT-15-023": ("TFPOTHEREXPENSESINFODLGFM", "其它支出", [shot("b15-planning-other-expense-dialog.png"), shot("b15-planning-major-expense-dialog.png", nested=True)], "名称、年支出、期间、增长率", "已确认普通其他支出及未来重大支出共用的输入结构。"),
    "RT-15-024": ("TFPOTHERINCOMEINFODLGFM", "其它收入", [shot("b15-planning-other-income-dialog.png")], "名称、年收入、期间、增长率", "已确认非账户关联收入输入字段。"),
    "RT-15-025": ("TFPRETIREMENTINFODLGFM", "养老计划", [shot("b15-planning-retirement-dialog.png", nested=True)], "退休年龄/年度、退休年收入、增长率、退休后家庭年支出", "已确认养老计划输入字段和退休年度联动。"),
    "RT-15-026": ("TFPSELECTASSETSDLGFM", "选择资产", [shot("b15-planning-select-assets-dialog.png"), shot("b15-planning-select-debts-dialog.png"), shot("b15-planning-insurance-dialog.png", nested=True)], "资产、债务或商业保险账户树", "同一选择器按入口切换资产、债权债务和商业保险标题及账户范围。"),
    "RT-15-027": ("TFPYEARDATAINFODLGFM", "年度情况", [shot("b15-financial-planning-created.png")], "年度规划结果", "年度结果在规划中心图表中出现，但未确认该类独立窗体及全部明细字段。"),
    "RT-15-028": ("TGOALACCTLISTDLG", "财务目标账户余额列表", [shot("b15-goal-created.png", nested=True)], "目标绑定账户及其余额", "目标创建时已绑定单一账户并影响初始值；独立余额列表窗体未单独打开。"),
    "RT-15-029": ("TGOALCENTERFM", "财务目标", [shot("b15-goal-created.png", nested=True), shot("b15-goal-after-delete.png", nested=True)], "目标、账户估值、标准进度、实际进度", "已创建并删除临时目标，确认进度展示和空状态。"),
    "RT-15-030": ("TGOALSAVEFM", "新增/修改财务目标", [shot("b15-goal-create-dialog.png", nested=True), shot("b15-goal-validation-message.png", nested=True), shot("b15-goal-create-filled.png", nested=True)], "名称、起止日期、金额、全部或指定账户", "已确认字段、名称必填校验和账户范围选择。"),
    "RT-15-031": ("TINCEXPPLANDLGFM", "收支计划", [shot("b15-income-expense-plan-dialog.png", nested=True)], "名称、日期、重复、账户、分类、金额、标签、自动执行", "已确认收支计划字段；未保存计划。"),
    "RT-15-032": ("TLIMITREMINDDLG", "限额提醒", [shot("b15-limit-reminder-list.png", nested=True)], "提醒类别、条件、启用状态", "已确认限额提醒列表和四类新增入口。"),
    "RT-15-033": ("TNEWREMINDDLGFM", "今日提醒", [shot("b15-today-reminder.png", nested=True)], "当日计划、预算偏差、执行/跳过、自动弹出选项", "已确认今日提醒列表、执行/跳过命令和预算偏差联动。"),
    "RT-15-034": ("TNORMALPLANDLGFM", "提醒", [shot("b15-reminder-dialog.png", nested=True)], "名称、开始日期、重复规则、提前提醒", "已确认普通提醒字段和当前默认选项；未保存提醒。"),
    "RT-15-035": ("TOPENFUNDREMINDDLG", "开放式基金价格提醒", [shot("b15-fund-price-reminder-dialog.png", nested=True)], "基金、价格下限、价格上限", "已确认基金价格上下限提醒结构；未保存新提醒。"),
    "RT-15-036": ("TPARENTPLANDLGFM", "计划基础对话框", [shot("b15-reminder-dialog.png", nested=True), shot("b15-income-expense-plan-dialog.png", nested=True)], "计划名称、日期、重复规则等共用字段", "该基类未独立出现，共用行为由提醒和交易计划子类间接覆盖。"),
    "RT-15-037": ("TPLANINSUREPAYFEEDLGFM", "保险缴费计划", [shot("b15-planning-insurance-dialog.png", nested=True)], "商业保险账户与缴费计划", "确认商业保险可纳入规划，但本轮未打开独立保险缴费计划窗体。"),
    "RT-15-038": ("TPLANLISTDLG", "财务计划和提醒", [shot("b15-plan-list.png", nested=True)], "类型、名称、频率、起止日期、下次执行日、执行状态", "已确认已有提醒列表、执行状态和四类新增计划入口。"),
    "RT-15-039": ("TSECURITYREMINDDLG", "证券市价提醒", [shot("b15-security-price-reminder-dialog.png", nested=True)], "证券、价格下限、价格上限", "已确认证券价格上下限提醒结构；未保存新提醒。"),
    "RT-15-040": ("TSELECTREPETITIONFREQUENCYDLGFM", "重复频率选择", [shot("b15-reminder-dialog.png", nested=True)], "一次性及其他重复频率", "已确认重复频率菜单存在七项且当前为一次性；其他标签未逐项确认。"),
    "RT-15-041": ("TTRANSACTIONPLANDLGFM", "交易计划基础对话框", [shot("b15-income-expense-plan-dialog.png", nested=True), shot("b15-transfer-plan-dialog.png", nested=True), shot("b15-fund-plan-dialog.png", nested=True)], "交易计划共用日期、重复和自动执行能力", "该基类未独立出现，收支、转账和基金计划子类已覆盖主要共用行为。"),
    "RT-15-042": ("TXFERPLANDLGFM", "转账计划", [shot("b15-transfer-plan-dialog.png", nested=True)], "名称、日期、重复、转出/转入账户、金额、手续费、标签、自动执行", "已确认转账计划字段；未保存计划。"),
}


def build_record(execution_id: str, data: tuple[str, str, list[str], str, str]) -> dict:
    resource, title, screenshots, inputs, summary = data
    independent_gap = execution_id in {"RT-15-017", "RT-15-027", "RT-15-028", "RT-15-036", "RT-15-037", "RT-15-040", "RT-15-041"}
    wrote_temp_data = execution_id in {"RT-15-003", "RT-15-011", "RT-15-029", "RT-15-030"}
    evidence = [
        {"kind": "screenshot", "path": path, "description": f"{title}运行态证据。"}
        for path in screenshots
    ]
    writes = []
    side_effects = []
    rollback = "本轮只观察窗体并取消，未写入计划或提醒。"
    if wrote_temp_data:
        writes = ["仅写入指定 test.mh8 的临时验证数据"]
        side_effects = ["测试账簿文件长度由 18,919,424 增至 18,939,904 字节"]
        rollback = "临时预算、规划和目标均已从界面删除或清除，并刷新确认空状态。"

    return {
        "schema_version": 1,
        "execution_id": execution_id,
        "resource": resource,
        "observed_at": OBSERVED_AT,
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8",
            "sha256_before": LEDGER_HASH,
            "sha256_after": None,
            "backup_artifact": None,
        },
        "navigation": {
            "entry_point": "财务分析或计划提醒菜单",
            "steps": ["仅操作 PID 37604 的 test 账簿", f"进入{title}", "记录字段、命令和状态", "取消或清理临时数据"],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [{
            "name": title,
            "status": "observed",
            "observations": summary,
            "evidence_paths": screenshots,
        }],
        "commands": [{
            "component": title,
            "label": "打开并观察",
            "initial_state": {"enabled": True, "visible": True},
            "trigger": "通过主菜单、页面按钮或上下文菜单进入",
            "confirmation": None,
            "outcome": summary,
            "status": "partial" if independent_gap else "pass",
        }],
        "data_flow": {
            "inputs": [item.strip() for item in inputs.split("、")],
            "reads": ["账户、交易、分类、投资或规划基础资料中的适用数据"],
            "writes": writes,
            "derived_results": ["预算执行、提醒条件、规划年度结果或目标进度中的适用结果"],
            "side_effects": side_effects,
            "rollback": rollback,
        },
        "evidence": evidence,
        "requirements_update": [summary],
        "result": {
            "status": "partial",
            "summary": summary,
            "remaining_gaps": (["该静态类的独立运行态页面仍待确认"] if independent_gap else [])
            + ["精确持久化字段、计算公式及关闭旧程序后的 SHA-256 仍待校准"],
        },
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for execution_id, data in RECORDS.items():
        record = build_record(execution_id, data)
        path = OUTPUT_DIR / f"{execution_id}-20260729T223017+0800.json"
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(RECORDS)} B15 records")


if __name__ == "__main__":
    main()
