"""生成 RT-15 计划与提醒窗体的最新页面级运行记录。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-08-03T04:11:02+08:00"
FILE_TIMESTAMP = "20260803T041102+0800"
BASELINE_HASH = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
BASELINE_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-029-financial-goal-before-20260803T-current.mh8"
)
DYNAMIC_OBSERVED_AT = "2026-08-03T05:23:00+08:00"
DYNAMIC_FILE_TIMESTAMP = "20260803T052300+0800"
DYNAMIC_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-dynamic-before-20260803T042639+0800.mh8"
)
DYNAMIC_POST_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-normal-reminder-lifecycle-after-20260803T0526+0800.mh8"
)
DYNAMIC_POST_HASH = "E14AFBF2FD552AEE9906F70B06A3458F9259ED6D6D1C03AED3F104A73730E63C"
RECURRING_OBSERVED_AT = "2026-08-03T05:35:00+08:00"
RECURRING_FILE_TIMESTAMP = "20260803T053500+0800"
RECURRING_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-recurring-reminder-before-20260803T050754+0800.mh8"
)
RECURRING_POST_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-recurring-reminder-after-20260803T0540+0800.mh8"
)
RECURRING_POST_HASH = "44141F66050D30C610C4A7153F67A5F51A5657BBD905E7D191CF7379990A1166"
RECURRING_STALE_LOCK = (
    "artifacts/runtime-validation/backups/"
    "RT-15-recurring-reminder-stale-lock-20260803T0540+0800.mh8"
)
RECURRING_STALE_LOCK_HASH = "FC2FD4B0B3561EB93B08C953B75EBE2E371E6CE3D8D075443D4C3ECA33395259"
TRANSACTION_PLAN_OBSERVED_AT = "2026-08-03T06:18:00+08:00"
TRANSACTION_PLAN_FILE_TIMESTAMP = "20260803T061800+0800"
TRANSACTION_PLAN_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-income-expense-plan-before-20260803T053737+0800.mh8"
)
TRANSACTION_PLAN_POST_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-income-expense-plan-after-20260803T0618+0800.mh8"
)
TRANSACTION_PLAN_POST_HASH = "8A337C2E30BA654235FB4571FD48746C5A559DCE3EC921AC44E36FBAFC68DC09"
TRANSACTION_PLAN_STALE_LOCK = (
    "artifacts/runtime-validation/backups/"
    "RT-15-income-expense-plan-stale-lock-20260803T0618+0800.mh8"
)
TRANSACTION_PLAN_STALE_LOCK_HASH = "8E0EE2EF0BB69B28915A4C6010C48AA6AAD97103D803AE8AA06593EB26CE5982"
TRANSFER_PLAN_OBSERVED_AT = "2026-08-03T06:58:00+08:00"
TRANSFER_PLAN_FILE_TIMESTAMP = "20260803T065800+0800"
TRANSFER_PLAN_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-transfer-plan-before-20260803T062603+0800.mh8"
)
TRANSFER_PLAN_POST_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-transfer-plan-after-20260803T0658+0800.mh8"
)
TRANSFER_PLAN_POST_HASH = "E6D6FA34AB0E63ED04BF3596822CE98EA753346E5D7768DB1CF6F431544A06C5"
TRANSFER_PLAN_STALE_LOCK = (
    "artifacts/runtime-validation/backups/"
    "RT-15-transfer-plan-stale-lock-20260803T0658+0800.mh8"
)
TRANSFER_PLAN_STALE_LOCK_HASH = "33C0087E864957DE6DCC77CBA4D38ABF5560589A52B9A21B48333A48ADF8A952"
FUND_PLAN_OBSERVED_AT = "2026-08-03T08:55:23+08:00"
FUND_PLAN_FILE_TIMESTAMP = "20260803T085523+0800"
FUND_PLAN_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-fund-plan-before-20260803T070512+0800.mh8"
)
FUND_PLAN_POST_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-fund-plan-after-20260803T085523+0800.mh8"
)
FUND_PLAN_POST_HASH = "DAD4F38BD8BE10F17DFFA75F8D418C300B38255B7212ACF6ACE1D8786320C236"
FUND_PLAN_STALE_LOCK = (
    "artifacts/runtime-validation/backups/"
    "RT-15-fund-plan-stale-lock-20260803T085523+0800.mh8"
)
FUND_PLAN_STALE_LOCK_HASH = "EAD592C694B45FF5E4D31522B181A5C967DC9F932516174D9E5AB5EE760B0A3E"
INSURANCE_PLAN_OBSERVED_AT = "2026-08-03T11:48:00+08:00"
INSURANCE_PLAN_FILE_TIMESTAMP = "20260803T114800+0800"
INSURANCE_PLAN_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-insurance-plan-before-20260803T091737+0800.mh8"
)
INSURANCE_PLAN_POST_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-insurance-plan-after-20260803T1148+0800.mh8"
)
INSURANCE_PLAN_POST_HASH = "2B2FAFAEA6B9A0390DFFAEFAA47F9A5E50259DB9ECE843A2A3F8217A1670A6F8"
INSURANCE_PLAN_STALE_LOCK = (
    "artifacts/runtime-validation/backups/"
    "RT-15-test-recovery-after-20260803T1151+0800.mh8"
)
INSURANCE_PLAN_STALE_LOCK_HASH = "B6C8E1EC7079D109037ED433F211399E59FC8985914588C8288F7CF512CCE67E"
INSURANCE_PLAN_UNINTENDED_LEDGER = (
    "artifacts/runtime-validation/backups/"
    "RT-15-unintended-test001-after-20260803T1151+0800.mh8"
)
INSURANCE_PLAN_UNINTENDED_LEDGER_HASH = "30A61E26A6F232400902812FBF3681562755196850DA6FFD952708BAAF10262A"
INSURANCE_PLAN_UNINTENDED_LOCK = (
    "artifacts/runtime-validation/backups/"
    "RT-15-unintended-test001-recovery-20260803T1151+0800.mh8"
)
INSURANCE_PLAN_UNINTENDED_LOCK_HASH = "6168B243A01841945F6592E56B6D4DAC93D8E8120C753CF600CE03EE1A4A881F"
INSURANCE_PLAN_MODIFY_OBSERVED_AT = "2026-08-03T12:31:00+08:00"
INSURANCE_PLAN_MODIFY_FILE_TIMESTAMP = "20260803T123100+0800"
INSURANCE_PLAN_MODIFY_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-insurance-plan-modify-before-20260803T-current.mh8"
)
INSURANCE_PLAN_MODIFY_POST_SAVE_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-insurance-plan-modify-after-save-20260803T1221.mh8"
)
INSURANCE_PLAN_MODIFY_POST_SAVE_HASH = (
    "42A2E087950FC30DEFF44B494371976B844193131A24A41884DF9E1BF06EA98D"
)
INSURANCE_PLAN_MODIFY_COLD_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-insurance-plan-modify-cold-start-auto-posted-20260803T1231.mh8"
)
INSURANCE_PLAN_MODIFY_COLD_HASH = (
    "31B03CDE392229D6DF165332B5E5A844A64CA9F76EF82E5BF23E27D8CE6339E9"
)
INSURANCE_PLAN_MODIFY_COLD_RECOVERY = (
    "artifacts/runtime-validation/backups/"
    "RT-15-insurance-plan-modify-recovery-cold-start-20260803T1231"
)
INSURANCE_PLAN_MODIFY_COLD_RECOVERY_HASH = (
    "AC75C27F92B690D89408A875AE145430DC3C736BD3F1E32D4110EF17500566D9"
)
LIMIT_REMINDER_OBSERVED_AT = "2026-08-03T13:45:41+08:00"
LIMIT_REMINDER_FILE_TIMESTAMP = "20260803T134541+0800"
LIMIT_REMINDER_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-limit-reminders-before-20260803T-current.mh8"
)
LIMIT_REMINDER_ALL_FOUR_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-limit-reminders-all-four-before-cold-20260803T1324.mh8"
)
LIMIT_REMINDER_ALL_FOUR_HASH = (
    "B72A01D1764152F9B16227434560316B5452BAE215C820FCB952438668B31A10"
)
LIMIT_REMINDER_FINAL_BACKUP = (
    "artifacts/runtime-validation/backups/"
    "RT-15-limit-reminders-final-cold-20260803T1345.mh8"
)
LIMIT_REMINDER_FINAL_HASH = (
    "61D56C651A93013EDD15EBD7E69447656E4FF5033020CBD4FCAA09E77FDFD9D9"
)
LIMIT_REMINDER_FINAL_RECOVERY = (
    "artifacts/runtime-validation/backups/"
    "RT-15-limit-reminders-recovery-final-cold-20260803T1345"
)
LIMIT_REMINDER_FINAL_RECOVERY_HASH = (
    "FF0BA19F47B012A2D53243C348D5F0FC0CAF43F7601D5D1E16CC9AFC11E5068F"
)
NOTE_PATH = "artifacts/runtime-validation/RT15-plans-and-reminders-notes.md"
SCREENSHOT_ROOT = "artifacts/runtime-validation/screenshots"

DYNAMIC_ROLLBACK = (
    "已归档普通提醒生命周期操作后的账簿副本 "
    f"{DYNAMIC_POST_BACKUP}，SHA-256 为 {DYNAMIC_POST_HASH}；"
    f"随后用 {DYNAMIC_BACKUP} 恢复 test.mh8 至 {BASELINE_HASH}。"
    "退出残留的锁副本已移入 runtime-validation/backups，最终 MoneyHome8 进程和锁文件均为 0。"
)
DYNAMIC_NAVIGATION_STEPS = [
    "显式用 test.mh8 启动 MoneyHome8，并通过 TMoneyHome8 顶层窗体句柄直接取证",
    "打开 财智8 -> 计划提醒 -> 计划与提醒，核对列表、新增类型和上下文命令",
    "新建 CodexReminder-20260803-0455，保留当天、一次性和提前 3 天默认值后保存",
    "从顶部时钟打开今日提醒，确认执行禁用、跳过启用并实际执行跳过",
    "重新打开计划列表，启用显示已完成，核对兼容状态并确认删除测试提醒",
    "归档操作后账簿与残留锁副本，再恢复 test.mh8 基线",
]
RECURRING_ROLLBACK = (
    "已归档重复提醒操作后的账簿副本 "
    f"{RECURRING_POST_BACKUP}，SHA-256 为 {RECURRING_POST_HASH}；"
    f"退出残留锁副本 {RECURRING_STALE_LOCK} 的 SHA-256 为 {RECURRING_STALE_LOCK_HASH}。"
    f"随后用 {RECURRING_BACKUP} 恢复 test.mh8 至 {BASELINE_HASH}，"
    "最终 MoneyHome8 进程和锁文件均为 0。"
)
RECURRING_NAVIGATION_STEPS = [
    "显式用 test.mh8 启动 MoneyHome8，并通过 TMoneyHome8 顶层窗体和 VCL 子窗体句柄取证",
    "打开普通提醒的重复菜单，逐项记录一次性、每天、每周、每月、每年和自定义",
    "打开自定义重复频率，确认默认每 1 天重复及天、周、月、年四种单位",
    "展开提前提醒菜单，逐项记录当天及提前 1 至 7 天",
    "创建 CodexDailyReminder-20260803，开始日期 2026-08-03、每天、重复 999 次、提前 3 天",
    "从今日提醒跳过当天实例，确认下次日期推进至 2026-08-04、结束日期和执行中状态保持",
    "核对提醒操作菜单不提供终止或恢复，删除测试提醒后归档操作副本并恢复账簿基线",
]
TRANSACTION_PLAN_ROLLBACK = (
    "已归档收支计划生命周期操作后的账簿副本 "
    f"{TRANSACTION_PLAN_POST_BACKUP}，SHA-256 为 {TRANSACTION_PLAN_POST_HASH}；"
    f"退出残留锁副本 {TRANSACTION_PLAN_STALE_LOCK} 的 SHA-256 为 "
    f"{TRANSACTION_PLAN_STALE_LOCK_HASH}。"
    f"随后用 {TRANSACTION_PLAN_BACKUP} 恢复 test.mh8 至 {BASELINE_HASH}，"
    "最终 MoneyHome8 进程和锁文件均为 0。"
)
TRANSACTION_PLAN_NAVIGATION_STEPS = [
    "显式用 test.mh8 启动 MoneyHome8，并确认唯一进程、指定账簿和运行前基线副本",
    "创建一次性手工收支计划，绑定 Cash-CNY、食物和 0.01，保存到期计划但在立即执行询问中选择否",
    "从计划列表执行该实例，确认先打开可编辑日常支出草稿，再立即入账生成唯一交易",
    "创建每天重复 3 次的手工收支计划，绑定 Cash-CNY、食物和 0.02，核对结束日包含首次发生",
    "执行首期后从今日提醒跳过后两期，核对下次日期逐期推进、跳过不生成交易且最终进入完成态",
    "核对完成计划修改为只读快照，操作菜单没有终止或恢复；删除测试定义后归档并恢复账簿基线",
]
TRANSFER_PLAN_ROLLBACK = (
    "已归档转账计划生命周期操作后的账簿副本 "
    f"{TRANSFER_PLAN_POST_BACKUP}，SHA-256 为 {TRANSFER_PLAN_POST_HASH}；"
    f"退出残留锁副本 {TRANSFER_PLAN_STALE_LOCK} 的 SHA-256 为 "
    f"{TRANSFER_PLAN_STALE_LOCK_HASH}。"
    f"随后用 {TRANSFER_PLAN_BACKUP} 恢复 test.mh8 至 {BASELINE_HASH}，"
    "最终 MoneyHome8 进程和锁文件均为 0。"
)
TRANSFER_PLAN_NAVIGATION_STEPS = [
    "显式用 test.mh8 启动 MoneyHome8，并确认唯一进程、指定账簿和运行前基线副本",
    "创建一次性手工转账计划，绑定 Cash-CNY、Qrd 农行、本金 0.03 和来源手续费 0.01",
    "保存到期计划但在立即执行询问中选择否，确认只保存定义且自动执行默认未勾选",
    "从计划列表执行实例，核对可编辑转账草稿并立即入账，交叉验证账户中心和财务记录",
    "创建每天重复 2 次的零手续费转账计划，从今日提醒连续跳过两期并确认不生成交易",
    "核对完成计划只读、操作菜单无终止或恢复、旧版已执行次数包含跳过次数，再删除测试定义",
    "归档操作后账簿和残留锁副本，并恢复 test.mh8 精确基线",
]
FUND_PLAN_ROLLBACK = (
    "已归档基金计划生命周期操作后的账簿副本 "
    f"{FUND_PLAN_POST_BACKUP}，SHA-256 为 {FUND_PLAN_POST_HASH}；"
    f"退出残留锁副本 {FUND_PLAN_STALE_LOCK} 的 SHA-256 为 "
    f"{FUND_PLAN_STALE_LOCK_HASH}。"
    f"随后用 {FUND_PLAN_BACKUP} 恢复 test.mh8 至 {BASELINE_HASH}，"
    "最终 MoneyHome8 进程和锁文件均为 0。"
)
FUND_PLAN_NAVIGATION_STEPS = [
    "显式用 test.mh8 启动 MoneyHome8，并确认唯一进程、指定账簿和运行前基线副本",
    "创建一次性手工基金计划，绑定国泰证券开放基金、Cash-CNY、008903 广发科技先锋混合、费率 1.00% 和定额 1.00",
    "保存到期计划但在立即执行询问中选择否，确认只保存定义且自动执行默认未勾选",
    "从计划列表执行实例，在开放式基金申购草稿补充单位净值 1.0000 后立即入账",
    "交叉核对财务记录、Cash-CNY、投资一览中的份额、成本、均价、市值和浮动盈亏",
    "创建每天重复 2 次的基金计划，从今日提醒连续跳过两期并确认不生成交易",
    "核对完成列表、归档操作后账簿和残留锁副本，并恢复 test.mh8 精确基线",
]
INSURANCE_PLAN_ROLLBACK = (
    "已归档保险缴费计划操作后的 test.mh8 副本 "
    f"{INSURANCE_PLAN_POST_BACKUP}，SHA-256 为 {INSURANCE_PLAN_POST_HASH}；"
    f"退出后的恢复副本 {INSURANCE_PLAN_STALE_LOCK} 的 SHA-256 为 "
    f"{INSURANCE_PLAN_STALE_LOCK_HASH}。菜单探针期间产生的 test001.mh8 及锁副本已分别归档为 "
    f"{INSURANCE_PLAN_UNINTENDED_LEDGER}（{INSURANCE_PLAN_UNINTENDED_LEDGER_HASH}）和 "
    f"{INSURANCE_PLAN_UNINTENDED_LOCK}（{INSURANCE_PLAN_UNINTENDED_LOCK_HASH}），随后从测试目录清理。"
    f"独立修改复测另归档定义保存态 {INSURANCE_PLAN_MODIFY_POST_SAVE_BACKUP}"
    f"（{INSURANCE_PLAN_MODIFY_POST_SAVE_HASH}）和冷启动自动入账态 "
    f"{INSURANCE_PLAN_MODIFY_COLD_BACKUP}（{INSURANCE_PLAN_MODIFY_COLD_HASH}）；"
    f"冷启动恢复副本 {INSURANCE_PLAN_MODIFY_COLD_RECOVERY} 的 SHA-256 为 "
    f"{INSURANCE_PLAN_MODIFY_COLD_RECOVERY_HASH}。最终用 {INSURANCE_PLAN_MODIFY_BACKUP} "
    f"恢复 test.mh8 至 {BASELINE_HASH}，MoneyHome8 进程、test001 和本轮恢复文件均为 0。"
)
INSURANCE_PLAN_NAVIGATION_STEPS = [
    "显式用 test.mh8 启动 MoneyHome8，并确认只在商业保险开户、计划列表、今日提醒和保险工作区操作测试对象",
    "创建仅提醒的零金额与 1.00 单期保险计划，观察今日提醒能力并跳过其中一条实例",
    "创建绑定 Cash-CNY、金额 1.00 的固定账户定期扣款计划，确认列表类型为自动计划且创建时未立即扣款",
    "从财务计划和提醒列表执行自动计划，观察执行计划-缴纳保费草稿并点击立即入账",
    "核对 Cash-CNY 余额和记录数，以及保险工作区的缴费交易、累计保费和来源备注",
    "创建缴费年限 2 年、年缴 1.00、绑定 Cash-CNY 的固定账户保险计划",
    "从保单工作区操作菜单打开独立缴费计划编辑器，记录年缴、月缴、半年缴、季度缴和一次性缴五种频率",
    "把频率改为半年缴、金额改为 1.01，保存后核对每 6 月、2026-08-03..2028-02-03 和执行草稿金额",
    "正常退出并冷启动，核对计划推进、保险缴费、Cash-CNY 流出、独立编辑器回填和账户中心刷新差异",
    "归档操作后账簿、恢复副本和意外产生的 test001 副本，清理副本后恢复 test.mh8 基线",
]
LIMIT_REMINDER_ROLLBACK = (
    "已归档四类规则冷启动前状态 "
    f"{LIMIT_REMINDER_ALL_FOUR_BACKUP}（{LIMIT_REMINDER_ALL_FOUR_HASH}）和证券删除后的最终冷启动状态 "
    f"{LIMIT_REMINDER_FINAL_BACKUP}（{LIMIT_REMINDER_FINAL_HASH}）；"
    f"最终恢复副本 {LIMIT_REMINDER_FINAL_RECOVERY} 的 SHA-256 为 "
    f"{LIMIT_REMINDER_FINAL_RECOVERY_HASH}。随后用 {LIMIT_REMINDER_BACKUP} 恢复 test.mh8 至 "
    f"{BASELINE_HASH}，最终 MoneyHome8 进程、~$test 和 test001 残留均为 0。"
)
LIMIT_REMINDER_NAVIGATION_STEPS = [
    "显式用 test.mh8 启动 MoneyHome8，并核对唯一进程、指定账簿、锁文件和运行前基线副本",
    "从 计划提醒 -> 限额提醒 分别创建账户余额、信用卡透支、证券市价和开放式基金价格规则",
    "把信用卡规则直接切换为停用，把账户下限修改为 609.00，并验证上下限相等时拒绝保存",
    "冷启动后打开今日提醒，核对账户余额和证券价格两条触发、信用卡停用不触发、基金未越界不触发",
    "取消一次证券规则删除，再确认删除并核对今日提醒立即只剩账户余额告警",
    "再次冷启动核对账户和基金规则启用、信用卡规则停用、证券规则不再存在",
    "归档最终账簿及恢复副本，正常退出后恢复 test.mh8 精确基线并清理锁文件",
]


def screenshot(name: str) -> str:
    """返回运行证据截图的仓库相对路径。"""

    return f"{SCREENSHOT_ROOT}/{name}"


def command(
    component: str,
    label: str,
    outcome: str,
    status: str = "partial",
    event_ids: list[str] | None = None,
    enabled: bool | None = None,
    confirmation: str | None = None,
) -> dict[str, Any]:
    """构造统一命令记录，区分可见能力和已实际执行结果。"""

    initial_state: dict[str, Any] = {"visible": True}
    if enabled is not None:
        initial_state["enabled"] = enabled
    result: dict[str, Any] = {
        "component": component,
        "label": label,
        "initial_state": initial_state,
        "trigger": f"点击“{label}”或对应菜单项",
        "confirmation": confirmation,
        "outcome": outcome,
        "status": status,
    }
    if event_ids:
        result["event_ids"] = event_ids
    return result


FORM_SPECS: dict[str, dict[str, Any]] = {
    "RT-15-001": {
        "resource": "TACCTBALAREMINDDLG",
        "title": "账户余额提醒",
        "observed_at": LIMIT_REMINDER_OBSERVED_AT,
        "file_timestamp": LIMIT_REMINDER_FILE_TIMESTAMP,
        "backup_artifact": LIMIT_REMINDER_BACKUP,
        "navigation_steps": LIMIT_REMINDER_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("moneyhome-account-balance-reminder-empty-validation-live-20260803T1257.png"),
            screenshot("moneyhome-account-balance-reminder-threshold-order-validation-live-20260803T1327.png"),
            screenshot("moneyhome-account-balance-reminder-trigger-valid-live-20260803T1328.png"),
            screenshot("moneyhome-limit-reminders-today-triggered-cold-live-20260803T1327.png"),
        ],
        "summary": "已真实保存并修改 Cash-CNY 账户余额规则。空账户提示“请选择账户”，上下限相等提示“最小值需小于最大值”；把下限改为 609.00、上限改为 610.00 后，当前余额 608.00 在冷启动今日提醒中投影为低 1.00 元。",
        "result_status": "pass",
        "inputs": ["账户稳定 ID", "余额小于阈值", "余额大于阈值"],
        "reads": ["可用账户候选", "账户当前余额及币种"],
        "writes": ["账户余额提醒规则及启用状态"],
        "derived": ["当前余额越过任一有效阈值时生成只读告警投影", "告警文案显示与边界的差额而不是重复显示阈值"],
        "commands": [command("btnSaveNew", "保存", "已验证新建、修改、必选账户和下限严格小于上限校验；修改结果跨冷启动保持。", "pass", ["planning_budget_goal.acct_bala_remind_dlg.btn_save_new_click"])],
        "requirements": ["账户余额提醒必须绑定稳定账户 ID，并分别保存下限、上限、币种和条件版本；校验 lower < upper，触发快照同时冻结余额、阈值和差额。"],
        "gaps": ["只填单侧、恰好等于边界、上限触发和跨币种行为", "账户删除或关闭后的规则处置、并发和失败持久化"],
        "side_effects": ["Cash-CNY 余额 608.00 未改变；仅新增和修改提醒规则。", "冷启动今日提醒生成账户余额低 1.00 元的只读告警，执行和跳过均不可用。"],
        "rollback": LIMIT_REMINDER_ROLLBACK,
    },
    "RT-15-004": {
        "resource": "TBUYFUNDPLANDLGFM",
        "title": "基金申购/定投计划",
        "observed_at": FUND_PLAN_OBSERVED_AT,
        "file_timestamp": FUND_PLAN_FILE_TIMESTAMP,
        "backup_artifact": FUND_PLAN_BACKUP,
        "navigation_steps": FUND_PLAN_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("moneyhome-fund-plan-default-live-20260803T0710.png"),
            screenshot("moneyhome-fund-plan-filled-manual-20260803T0717.png"),
            screenshot("moneyhome-fund-plan-save-due-prompt-20260803T0718.png"),
            screenshot("moneyhome-fund-plan-list-after-save-no-execute-20260803T0719.png"),
            screenshot("moneyhome-fund-plan-execution-editor-aligned-20260803T0727.png"),
            screenshot("moneyhome-fund-plan-list-after-execution-completed-visible-20260803T0730.png"),
            screenshot("moneyhome-fund-plan-account-center-after-execution-20260803T0731.png"),
            screenshot("moneyhome-fund-plan-financial-record-after-execution-20260803T0846.png"),
            screenshot("moneyhome-fund-plan-investment-overview-after-execution-20260803T0848.png"),
            screenshot("moneyhome-fund-plan-daily-filled-before-save-20260803T0854.png"),
            screenshot("moneyhome-today-reminder-fund-plan-before-skip-20260803T0900.png"),
            screenshot("moneyhome-today-reminder-after-first-fund-skip-20260803T0901.png"),
            screenshot("moneyhome-today-reminder-after-second-fund-skip-20260803T0902.png"),
            screenshot("moneyhome-fund-plan-daily-list-after-two-skips-completed-visible-20260803T0905.png"),
            screenshot("moneyhome-fund-plan-financial-record-after-skips-20260803T0906.png"),
        ],
        "summary": "已真实完成一次性基金计划人工执行和每天重复 2 次计划的跳过生命周期。保存到期定义时选择否不会入账；执行草稿要求补充成交净值并计算费用和份额；最终交易同步更新资金账户、基金持仓和按最新行情形成的估值投影。",
        "result_status": "pass",
        "inputs": ["计划名称", "开始日期", "重复规则", "重复次数", "提前提醒", "基金账户", "资金账户", "基金", "申购费率", "定投金额", "自动执行"],
        "reads": ["基金账户和资金账户候选", "基金资料候选", "重复规则", "执行时单位净值", "持仓估值使用的最新基金行情"],
        "writes": ["基金申购交易模板", "计划定义及执行模式", "计划实例执行或跳过动作", "最终开放式基金申购交易", "基金持仓数量和成本"],
        "derived": ["逐期基金申购计划实例", "申购费用和净申购份额", "含费用的持仓均价", "按最新行情计算的当前市值和浮动盈亏", "执行完毕兼容状态"],
        "commands": [
            command("btnUpdateFund", "更新基金", "可刷新基金候选；联网结果和失败回滚未执行。", "partial"),
            command("chkAutoExecute", "自动执行", "真实新增态默认未勾选；本轮使用手工执行模式，自动执行到期行为仍待验证。", "pass", ["planning_budget_goal.buy_fund_plan_dlg_fm.chk_auto_execute_click"]),
            command("btnSave", "确定", "到期计划保存时询问是否继续执行；选择否仍保存计划定义且不创建交易。", "pass"),
            command("actExecute", "执行", "计划列表执行打开开放式基金申购草稿；补充单位净值 1.0000 后，1.00 金额与 1.00% 前端费率计算费用 0.01、份额 0.99，立即入账生成唯一交易。", "pass", ["planning_budget_goal.plan_list_dlg.act_execute_execute"], enabled=True),
            command("actJump", "跳过", "今日提醒先跳过 2026-08-03 实例并推进到提前展示的 2026-08-04，再跳过第二期；两次均未生成交易，计划最终完成。", "pass", ["planning_budget_goal.new_remind_dlg_fm.act_jump_execute"], enabled=True),
        ],
        "requirements": ["基金计划必须分层保存模板、定义、实例、可编辑执行草稿和最终交易；执行交易冻结基金、账户、成交净值、收费模式、费率、费用、金额和份额，持仓估值再独立读取行情快照。"],
        "gaps": ["自动执行、冷启动、修改和删除", "基金更新失败、余额不足、其它收费模式、大金额舍入、重复提交和失败回滚"],
        "side_effects": [
            "一次性计划申购 008903 广发科技先锋混合：Cash-CNY 从 608.00 降至 607.00，财务记录数由 2189 增至 2190，新增流出 1.00 的开放式基金申购。",
            "投资一览新增 0.99 份，持仓成本 1.00、买入均价 1.0101；按最新行情显示当前市值 1.10、浮动盈亏 0.10。",
            "每天重复 2 次的基金计划两期均跳过，财务记录保持 2190；操作后账簿和残留锁已归档，再恢复精确基线。",
        ],
        "rollback": FUND_PLAN_ROLLBACK,
    },
    "RT-15-006": {
        "resource": "TCREDITREMINDDLG",
        "title": "信用卡透支额提醒",
        "observed_at": LIMIT_REMINDER_OBSERVED_AT,
        "file_timestamp": LIMIT_REMINDER_FILE_TIMESTAMP,
        "backup_artifact": LIMIT_REMINDER_BACKUP,
        "navigation_steps": LIMIT_REMINDER_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("moneyhome-credit-reminder-account-candidates-cleared-live-20260803T1306.png"),
            screenshot("moneyhome-credit-overdraft-reminder-filled-live-20260803T1322.png"),
            screenshot("moneyhome-limit-reminders-credit-disabled-live-20260803T1324.png"),
            screenshot("moneyhome-limit-reminders-three-rules-final-cold-live-20260803T1345.png"),
        ],
        "summary": "基线无可用信用卡时选择器明确提示新增账户；创建零余额临时信用卡后保存 0.01 元透支阈值，并在统一列表直接停用。停用状态跨两次冷启动保持且未进入今日提醒。",
        "result_status": "pass",
        "inputs": ["信用卡账户稳定 ID", "透支额阈值"],
        "reads": ["信用卡候选", "当前欠款、额度和币种"],
        "writes": ["信用卡透支提醒规则及启用状态"],
        "derived": ["透支额达到规则条件时生成提醒触发实例"],
        "commands": [command("btnSaveNew", "保存", "已保存绑定临时信用卡的 0.01 元阈值，并验证新规则默认启用。", "pass", ["planning_budget_goal.credit_remind_dlg.btn_save_new_click"])],
        "requirements": ["信用卡提醒必须保存账户 ID、阈值、币种、条件版本及触发时欠款快照；启停必须原子持久化，停用规则不参与评估。"],
        "gaps": ["实际透支触发方向、等于边界、额度变化和多币种", "引用信用卡删除或关闭后的处置、规则修改/删除、并发和失败持久化"],
        "side_effects": ["创建临时零余额信用卡 CodexLimitCredit-20260803我的信用卡，仅用于建立候选；未生成财务交易。", "规则停用后跨冷启动保持，未产生今日提醒。"],
        "rollback": LIMIT_REMINDER_ROLLBACK,
    },
    "RT-15-031": {
        "resource": "TINCEXPPLANDLGFM",
        "title": "收支计划",
        "observed_at": TRANSACTION_PLAN_OBSERVED_AT,
        "file_timestamp": TRANSACTION_PLAN_FILE_TIMESTAMP,
        "backup_artifact": TRANSACTION_PLAN_BACKUP,
        "navigation_steps": TRANSACTION_PLAN_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("moneyhome-income-expense-plan-default-live-20260803T0542.png"),
            screenshot("moneyhome-income-expense-plan-filled-manual-20260803T0549.png"),
            screenshot("moneyhome-income-expense-plan-save-message-20260803T0550.png"),
            screenshot("moneyhome-income-expense-plan-execution-editor-20260803T0554.png"),
            screenshot("moneyhome-financial-records-after-plan-posting-20260803T0558.png"),
            screenshot("moneyhome-recurring-expense-plan-ready-20260803T0612.png"),
            screenshot("moneyhome-recurring-expense-plan-completed-after-execute-and-skips-20260803T0624.png"),
            screenshot("moneyhome-account-center-after-recurring-expense-plan-lifecycle-20260803T0628.png"),
        ],
        "summary": "已真实完成一次性和每天重复 3 次的手工收支计划生命周期。到期计划保存前询问是否继续执行，选择否仍保存定义；执行先打开可编辑交易草稿，入账后生成唯一支出并推进下一实例；后续实例可在今日提醒跳过且不生成交易。",
        "inputs": ["计划名称", "开始日期", "重复规则", "资金账户", "收入或支出项目", "金额", "标签", "自动执行"],
        "reads": ["账户、分类和标签候选", "重复规则与提醒提前量"],
        "writes": ["收支交易模板", "计划定义及执行模式", "计划实例执行或跳过动作", "执行后生成的收入或支出交易"],
        "derived": ["逐期收支计划实例", "执行实例关联唯一交易", "跳过实例只推进下一日期", "完成计划只读快照"],
        "commands": [
            command("chkAutoExecute", "自动执行", "页面提供自动执行开关；本轮使用未勾选的手工执行模式完成生命周期。", "pass", ["planning_budget_goal.inc_exp_plan_dlg_fm.chk_auto_execute_click"]),
            command("btnSave", "确定", "到期计划保存时询问是否继续执行；选择否仍保存计划定义且不创建交易。", "pass"),
            command("actExecute", "执行", "计划列表执行先打开可编辑日常支出草稿；立即入账后创建唯一交易并推进下次执行日期。", "pass", ["planning_budget_goal.plan_list_dlg.act_execute_execute"], enabled=True),
            command("actJump", "跳过", "已从今日提醒跳过周期计划的 2026-08-04 和 2026-08-05 实例；两次均未生成交易，最后一期后计划进入完成态。", "pass", ["planning_budget_goal.new_remind_dlg_fm.act_jump_execute"], enabled=True),
            command("actEdit", "修改", "完成计划仍提供修改入口，但打开后全部业务字段禁用，仅可查看快照。", "pass", ["planning_budget_goal.plan_list_dlg.act_edit_execute"]),
        ],
        "requirements": ["收支计划必须把交易模板、重复定义、每次计划实例和最终交易分层保存；手工执行先生成可编辑交易草稿，自动执行仍使用同一幂等业务命令。"],
        "gaps": ["自动执行、冷启动和失败重试", "收入方向、零值/负值、账户失效、标签、并发与重复提交"],
        "side_effects": [
            "一次性计划执行生成食物支出 0.01；每天计划首期生成食物支出 0.02，财务记录数由 2189 增至 2191。",
            "Cash-CNY 从 608.00 降至 607.97；两次跳过没有生成交易或继续扣款。",
            "两个测试计划定义已删除；操作后账簿和残留锁已归档，再恢复精确基线。",
        ],
        "rollback": TRANSACTION_PLAN_ROLLBACK,
    },
    "RT-15-032": {
        "resource": "TLIMITREMINDDLG",
        "title": "限额提醒",
        "observed_at": LIMIT_REMINDER_OBSERVED_AT,
        "file_timestamp": LIMIT_REMINDER_FILE_TIMESTAMP,
        "backup_artifact": LIMIT_REMINDER_BACKUP,
        "navigation_steps": LIMIT_REMINDER_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("moneyhome-limit-reminders-all-four-saved-live-20260803T1323.png"),
            screenshot("moneyhome-limit-reminders-credit-disabled-live-20260803T1324.png"),
            screenshot("moneyhome-limit-reminders-delete-confirmation-live-20260803T1331.png"),
            screenshot("moneyhome-limit-reminders-security-deleted-live-20260803T1333.png"),
            screenshot("moneyhome-limit-reminders-three-rules-final-cold-live-20260803T1345.png"),
        ],
        "summary": "已真实创建四类规则，确认统一列表只显示类别、提醒条件和生效状态；新规则默认启用，生效列可直接停用并跨冷启动保持。修改账户规则、取消及确认删除证券规则均已验证，删除后规则和当前告警立即消失且冷启动不恢复。",
        "result_status": "pass",
        "inputs": ["四类阈值规则", "生效状态", "选中提醒"],
        "reads": ["提醒规则列表", "目标账户或投资品当前状态"],
        "writes": ["提醒规则新增、修改、启停和删除"],
        "derived": ["按类别和条件显示规则", "按启用规则与最新目标快照计算当前告警投影"],
        "commands": [
            command("N1", "新增账户余额提醒", "已打开对应编辑器。", "pass", ["planning_budget_goal.limit_remind_dlg.n1_click"]),
            command("N2", "新增信用卡透支额提醒", "已打开对应编辑器。", "pass", ["planning_budget_goal.limit_remind_dlg.n2_click"]),
            command("N3", "新增证券市价提醒", "已打开对应编辑器。", "pass", ["planning_budget_goal.limit_remind_dlg.n3_click"]),
            command("N4", "新增开放式基金价格提醒", "已打开对应编辑器。", "pass", ["planning_budget_goal.limit_remind_dlg.n4_click"]),
            command("miModify", "修改", "已修改账户余额上下限，列表和冷启动结果均使用新条件。", "pass", ["planning_budget_goal.limit_remind_dlg.mi_modify_click"]),
            command("miDelete", "删除", "已验证删除确认文案、取消无副作用和确认后立即删除证券规则及其当前告警。", "pass", ["planning_budget_goal.limit_remind_dlg.mi_delete_click"], confirmation="旧版确认文案为“您确定删除该提醒吗？”。目标实现还应展示目标和当前告警影响。"),
        ],
        "requirements": ["限额提醒列表必须统一管理四类规则，但每类条件使用类型化载荷和稳定目标 ID；新建默认启用，启停持久化，删除与当前告警重算保持原子一致。"],
        "gaps": ["规则排序、批量操作、并发和保存失败回滚", "引用目标删除/关闭语义未验证；自动化选择上下文指向其它基线账户时已安全取消，不得据此推断旧版级联行为"],
        "side_effects": ["四类规则均真实保存；信用卡规则停用，账户规则修改，证券规则确认删除。", "规则操作不生成财务交易；临时信用卡未删除以避免未证明选择上下文时误删基线账户。"],
        "rollback": LIMIT_REMINDER_ROLLBACK,
    },
    "RT-15-033": {
        "resource": "TNEWREMINDDLGFM",
        "title": "今日提醒",
        "observed_at": LIMIT_REMINDER_OBSERVED_AT,
        "file_timestamp": LIMIT_REMINDER_FILE_TIMESTAMP,
        "backup_artifact": LIMIT_REMINDER_BACKUP,
        "navigation_steps": LIMIT_REMINDER_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("b15-today-reminder.png"),
            screenshot("moneyhome-today-reminder-after-create-live-20260803T0505.png"),
            screenshot("moneyhome-today-reminder-after-skip-live-20260803T0508.png"),
            screenshot("moneyhome-today-recurring-expense-plan-before-skip-20260803T0620.png"),
            screenshot("moneyhome-today-recurring-expense-plan-after-skip-20260803T0621.png"),
            screenshot("moneyhome-today-recurring-expense-plan-after-final-skip-20260803T0623.png"),
            screenshot("moneyhome-today-recurring-transfer-plan-before-first-skip-20260803T0649.png"),
            screenshot("moneyhome-today-recurring-transfer-plan-after-first-skip-20260803T0650.png"),
            screenshot("moneyhome-today-recurring-transfer-plan-after-final-skip-20260803T0651.png"),
            screenshot("moneyhome-limit-reminders-today-triggered-cold-live-20260803T1327.png"),
            screenshot("moneyhome-limit-reminders-today-after-security-delete-live-20260803T1334.png"),
        ],
        "summary": "今日提醒按来源计算命令能力：普通提醒不可执行但可跳过，手工交易计划可执行也可跳过，限额告警既不可执行也不可跳过。冷启动触发账户余额和证券价格两条告警；停用信用卡和未越界基金均不出现。删除证券规则后列表立即只剩账户告警。",
        "inputs": ["选中的今日提醒实例", "自动弹出偏好", "今日抑制偏好"],
        "reads": ["到期计划实例", "阈值提醒实例", "预算偏差提醒实例"],
        "writes": ["计划实例执行或跳过状态", "提醒处理状态", "账簿或用户级提醒偏好"],
        "derived": ["按日期和来源统一展示提醒收件箱", "仅可执行计划实例生成交易"],
        "commands": [
            command("actExecute", "执行", "普通提醒实例不可执行；手工收支和转账计划实例可执行，并进入对应的可编辑交易草稿。", "pass", ["planning_budget_goal.new_remind_dlg_fm.act_execute_execute"]),
            command("actJump", "跳过", "普通提醒、收支计划和转账计划实例均已实际跳过；跳过立即消费当前实例且不生成交易，周期计划会显示下一实例。", "pass", ["planning_budget_goal.new_remind_dlg_fm.act_jump_execute"], enabled=True),
            command("chkAutoShowRemindToday", "打开账簿时自动弹出今日提醒", "可见偏好开关，具体作用域和冷启动尚未校准。", "partial", ["planning_budget_goal.new_remind_dlg_fm.chk_auto_show_remind_today_click"]),
            command("chkNoRemindToday", "今日不再提醒", "可见偏好开关，只应抑制当天展示，不改变规则或实例真相。", "partial", ["planning_budget_goal.new_remind_dlg_fm.chk_no_remind_today_click"]),
            command("RzBitBtn1", "关闭", "关闭只退出收件箱，不处理选中实例。", "pass", ["planning_budget_goal.new_remind_dlg_fm.rz_bit_btn1_click"]),
        ],
        "requirements": ["今日提醒应统一投影计划实例和提醒实例，并由来源能力决定执行、跳过、详情和不再提醒命令；限额告警是非执行型读模型。目标实现应保留触发审计，即使兼容视图按当前规则删除后立即隐藏旧告警。"],
        "gaps": ["基金计划自动执行和失败重试", "详情、不再提醒、偏好作用域、同日去重及限额规则的精确评估时点"],
        "side_effects": [
            "保存一次性提醒后生成当日提醒实例；跳过后实例从今日列表移除，未生成财务交易。",
            "收支计划首期执行后，2026-08-04 和 2026-08-05 实例因提前 3 天进入今日列表；连续跳过后计划完成且只生成首期交易。",
            "每天 2 次的转账计划连续跳过 2026-08-03 和 2026-08-04 两个实例，今日列表清空且财务记录数保持不变。",
            "冷启动后账户余额与证券价格告警进入列表，执行和跳过均禁用；证券规则删除后其告警立即消失。",
            "测试提醒和计划随后从计划列表删除，操作后账簿副本已归档并恢复基线。",
        ],
        "rollback": LIMIT_REMINDER_ROLLBACK,
    },
    "RT-15-034": {
        "resource": "TNORMALPLANDLGFM",
        "title": "普通提醒",
        "observed_at": RECURRING_OBSERVED_AT,
        "file_timestamp": RECURRING_FILE_TIMESTAMP,
        "backup_artifact": RECURRING_BACKUP,
        "navigation_steps": RECURRING_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("b15-reminder-dialog.png"),
            screenshot("moneyhome-normal-reminder-default-live-20260803T0455.png"),
            screenshot("moneyhome-normal-reminder-repeat-menu-live-20260803T0513.png"),
            screenshot("moneyhome-normal-reminder-advance-menu-live-20260803T0519.png"),
            screenshot("moneyhome-daily-reminder-filled-live-20260803T0522.png"),
            screenshot("moneyhome-plan-list-after-daily-reminder-save-20260803T0524.png"),
        ],
        "summary": "普通提醒有一次性、每天、每周、每月、每年和自定义六种重复选择；提前提醒为当天或提前 1 至 7 天。选择每天后显示重复次数且默认 999，测试规则的结束日期为开始日期加 998 天，证明次数包含首次发生。",
        "inputs": ["提醒名称", "开始日期", "重复规则", "重复次数", "提前提醒天数"],
        "reads": ["重复频率选择", "系统日期"],
        "writes": ["时间型提醒规则"],
        "derived": ["按开始日期、重复规则、重复次数和提前量生成提醒实例及定义结束日期"],
        "commands": [
            command("cboRepeat", "重复", "已逐项确认六个业务选项；分隔线不是第七种重复规则。", "pass"),
            command("cboAdvance", "提前提醒", "已逐项确认当天及提前 1 至 7 天共八个选项。", "pass"),
            command("btnSave", "确定", "已真实保存每天重复 999 次的提醒，列表显示结束日期 2029-04-27、下次执行日期 2026-08-03 和执行中状态。", "pass"),
        ],
        "requirements": ["普通提醒必须保存重复规则版本、包含首次发生的重复次数和提前量；结束日期应由开始日期及规则确定性推导，触发实例不能覆盖规则定义。"],
        "gaps": ["修改和未来日期触发", "空值、零值、负数和超大重复次数", "月末短月、闰年、自定义间隔边界和冷启动"],
        "side_effects": [
            "创建 CodexDailyReminder-20260803，开始日期 2026-08-03、每天、重复 999 次、提前 3 天。",
            "跳过 2026-08-03 实例后下次执行日期推进到 2026-08-04，结束日期仍为 2029-04-27；随后删除测试定义。",
        ],
        "rollback": RECURRING_ROLLBACK,
    },
    "RT-15-035": {
        "resource": "TOPENFUNDREMINDDLG",
        "title": "开放式基金价格提醒",
        "observed_at": LIMIT_REMINDER_OBSERVED_AT,
        "file_timestamp": LIMIT_REMINDER_FILE_TIMESTAMP,
        "backup_artifact": LIMIT_REMINDER_BACKUP,
        "navigation_steps": LIMIT_REMINDER_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("moneyhome-open-fund-price-reminder-filled-live-20260803T1314.png"),
            screenshot("moneyhome-limit-reminders-after-fund-save-live-20260803T1315.png"),
            screenshot("moneyhome-limit-reminders-three-rules-final-cold-live-20260803T1345.png"),
        ],
        "summary": "已真实保存 000001 华夏成长混合的净值下限 0.01、上限 9999.99；规则默认启用并跨冷启动保持。当前行情未越界，因此今日提醒中没有基金告警。",
        "result_status": "pass",
        "inputs": ["基金稳定 ID", "价格下限", "价格上限"],
        "reads": ["基金候选和最新净值"],
        "writes": ["基金价格提醒规则"],
        "derived": ["净值越过阈值时生成带行情快照的提醒实例"],
        "commands": [
            command("btnUpdateCode", "更新基金", "更新入口已确认，联网结果未执行。", "partial", ["planning_budget_goal.open_fund_remind_dlg.btn_update_code_click"]),
            command("btnSaveNew", "保存", "已保存基金上下限规则，并验证启用状态和冷启动持久化。", "pass", ["planning_budget_goal.open_fund_remind_dlg.btn_save_new_click"]),
        ],
        "requirements": ["基金提醒必须保存标的 ID、上下限、净值精度、行情来源、行情版本和条件版本；未越界时不得生成当前告警。"],
        "gaps": ["净值等于边界、上下限倒置、无行情和真实越界触发", "行情更新、修改、删除、引用失效、并发和失败持久化"],
        "side_effects": ["保存规则但未生成交易或当前告警；规则跨冷启动保持启用。"],
        "rollback": LIMIT_REMINDER_ROLLBACK,
    },
    "RT-15-036": {
        "resource": "TPARENTPLANDLGFM",
        "title": "计划/提醒公共编辑器",
        "screenshots": [screenshot("b15-reminder-dialog.png"), screenshot("b15-income-expense-plan-dialog.png")],
        "summary": "该资源是普通提醒和交易计划的公共基类，没有独立用户入口；提供名称、开始日期、重复、重复次数、已执行次数、提前提醒和确定协议。",
        "inputs": ["名称", "开始日期", "重复规则", "最大重复次数", "已执行次数投影", "提前提醒"],
        "reads": ["派生编辑器草稿", "计划实例生命周期统计"],
        "writes": ["派生计划或提醒定义"],
        "derived": ["公共草稿校验和生命周期展示"],
        "mode": "base",
        "commands": [command("btnSave", "确定", "公共命令由派生编辑器调用，无独立页面。", "not_applicable")],
        "requirements": ["Rust 版应使用共享计划编辑组件承载规则草稿和校验，不创建伪造的公共业务页面。"],
        "gaps": ["最大次数与结束日期联动", "已执行次数是否可编辑、关闭和校验失败协议"],
    },
    "RT-15-037": {
        "resource": "TPLANINSUREPAYFEEDLGFM",
        "title": "保险缴费计划",
        "observed_at": INSURANCE_PLAN_MODIFY_OBSERVED_AT,
        "file_timestamp": INSURANCE_PLAN_MODIFY_FILE_TIMESTAMP,
        "backup_artifact": INSURANCE_PLAN_MODIFY_BACKUP,
        "navigation_steps": INSURANCE_PLAN_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("moneyhome-insurance-debit-plan-account-keyboard-selected-20260803T1034.png"),
            screenshot("moneyhome-today-reminder-insurance-plan-observed-20260803T1010.png"),
            screenshot("moneyhome-today-reminder-insurance-after-one-skip-20260803T1011.png"),
            screenshot("moneyhome-plan-list-after-fixed-insurance-plan-create-20260803T1103.png"),
            screenshot("moneyhome-plan-list-show-completed-insurance-skip-20260803T1111.png"),
            screenshot("moneyhome-insurance-auto-plan-execute-dialog-20260803T1115.png"),
            screenshot("moneyhome-insurance-auto-plan-after-execute-completed-20260803T1118.png"),
            screenshot("moneyhome-cash-cny-after-insurance-auto-plan-execute-20260803T1121.png"),
            screenshot("moneyhome-insurance-debit-transaction-after-plan-execute-20260803T1129.png"),
            screenshot("moneyhome-insurance-plan-modify-dialog-initial-20260803T1219.png"),
            screenshot("moneyhome-insurance-plan-modify-frequency-popup-20260803T1220.png"),
            screenshot("moneyhome-insurance-plan-modify-dialog-edited-20260803T1221.png"),
            screenshot("moneyhome-insurance-plan-modify-plan-list-after-save-20260803T1224.png"),
            screenshot("moneyhome-insurance-plan-modify-execution-draft-20260803T1225.png"),
            screenshot("moneyhome-insurance-plan-modify-plan-list-cold-start-20260803T1227.png"),
            screenshot("moneyhome-insurance-plan-modify-workspace-cold-start-20260803T1229.png"),
            screenshot("moneyhome-insurance-plan-modify-cash-workspace-cold-start-20260803T1230.png"),
            screenshot("moneyhome-insurance-plan-modify-dialog-cold-start-20260803T1231.png"),
        ],
        "summary": (
            "保险缴费计划已完成代表性动态生命周期：仅提醒策略生成普通计划，今日提醒中执行禁用、跳过启用；"
            "固定账户定期扣款绑定 Cash-CNY 后生成自动计划，创建时不立即扣款，计划列表可手工执行。"
            "执行草稿预填保单、支付账户、金额 1.00、日期和来源备注，立即入账后 Cash-CNY 从 608.00 降至 "
            "607.00、记录数从 9 增至 10，保险侧新增同一笔缴费并使累计保费为 1.00。"
            "多年度样例又从保单上下文打开独立 TPlanInsurePayFeeDlgFm，确认五种频率，并把年缴 1.00 "
            "改为半年缴 1.01；中央列表重算为每 6 月、2026-08-03..2028-02-03，执行草稿同步为 1.01。"
            "关闭未入账草稿并重启后的首次核对已出现 1.01 自动缴费：Cash-CNY 为 606.99、保险累计保费为 "
            "1.01、下次日期为 2027-02-03；独立编辑器冷启动回填保持。旧账户中心短暂仍显示 608.00。"
        ),
        "inputs": ["保单账户", "缴费频率", "缴费金额", "缴费账户", "固定扣款/仅提醒/不提醒策略"],
        "reads": ["保单条款和缴费年限", "支付账户候选", "计划实例状态", "支付账户余额"],
        "writes": ["保险缴费交易模板", "计划定义与单期实例", "执行或跳过动作", "保险事件与资金交易"],
        "derived": [
            "单缴费年度年缴唯一实例，以及两缴费年度半年缴的四个应期和最后应期日",
            "普通计划或自动计划类型与命令能力",
            "执行完成后的累计保费、资金余额和完成状态",
            "计划条款修改后的未来实例重算和下次执行日期",
        ],
        "commands": [
            command(
                "btnSaveExit",
                "确定",
                "独立修改窗体已把年缴 1.00 保存为半年缴 1.01，同会话及冷启动均回填成功。",
                "pass",
                ["planning_budget_goal.plan_insure_pay_fee_dlg_fm.btn_save_exit_click"],
            ),
            command(
                "miModifyPlan",
                "修改缴费计划",
                "已从保单工作区底部操作菜单打开 TPlanInsurePayFeeDlgFm；中央列表仍不直接编辑派生定义。",
                "pass",
                ["insurance_social.insure_trans_frame.mi_modify_plan_click"],
                enabled=True,
            ),
            command(
                "btnFrequency",
                "缴费频率",
                "菜单真实列出年缴、月缴、半年缴、季度缴和一次性缴，半年缴已保存并驱动实例重算。",
                "pass",
                enabled=True,
            ),
            command(
                "TNewRemindDlgFm.btnIgnore",
                "跳过",
                "仅提醒的单期保险计划被消费并进入执行完毕查询范围，未生成保险或资金交易。",
                "pass",
                enabled=True,
            ),
            command(
                "TPlanListDlg.btnExecPlan",
                "执行",
                "自动计划打开类型化缴费草稿；立即入账原子生成保险缴费和 Cash-CNY 资金流出。",
                "pass",
                enabled=True,
            ),
        ],
        "side_effects": [
            "跳过只更新单个计划实例，不生成交易",
            "执行 1.00 后 Cash-CNY 余额 608.00 -> 607.00、记录数 9 -> 10",
            "保险工作区新增缴费 1.00、累计保费 1.00、记录数 1，现金价值保持 0.00",
            "两缴费年度计划从年缴 1.00 改为半年缴 1.01 后，结束日重算为 2028-02-03，执行草稿同步为 1.01",
            "关闭未入账草稿并重启后的状态包含自动缴费 1.01：Cash-CNY 608.00 -> 606.99、记录数 9 -> 10，保险累计保费 1.01",
            "自动入账后账户中心短暂显示旧 Cash-CNY 608.00，现金工作区显示真实 606.99",
        ],
        "rollback": INSURANCE_PLAN_ROLLBACK,
        "requirements": [
            "保险计划必须把保单、支付账户、策略和条款版本保存为稳定引用；仅提醒实例不可执行但可跳过。",
            "固定账户策略生成自动计划，但保存定义不得立即扣款；用户显式执行先形成可审阅草稿，后台执行使用同一幂等提交命令。",
            "缴费入账必须以幂等事务原子生成保险事件和资金交易，并在两侧保存同一来源关联。",
            "修改计划必须从保单上下文提交新版本，并只重算未处理实例；所有账户、计划和保险投影在提交后读取同一版本。",
        ],
        "gaps": [
            "月缴、季度缴、一次性缴的多年度保存，以及月末/闰年边界",
            "关闭未入账手工草稿到重启自动入账之间的精确提交时点和取消协议",
            "余额不足、账户失效、失败补偿、重复提交和并发修改",
        ],
    },
    "RT-15-038": {
        "resource": "TPLANLISTDLG",
        "title": "财务计划和提醒",
        "observed_at": TRANSFER_PLAN_OBSERVED_AT,
        "file_timestamp": TRANSFER_PLAN_FILE_TIMESTAMP,
        "backup_artifact": TRANSFER_PLAN_BACKUP,
        "navigation_steps": TRANSFER_PLAN_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("b15-plan-list.png"),
            screenshot("moneyhome-plan-list-after-daily-reminder-save-20260803T0524.png"),
            screenshot("moneyhome-today-daily-reminder-before-skip-20260803T0527.png"),
            screenshot("moneyhome-plan-list-after-daily-skip-20260803T0530.png"),
            screenshot("moneyhome-daily-reminder-operation-menu-20260803T0532.png"),
            screenshot("moneyhome-plan-list-after-daily-delete-20260803T0535.png"),
            screenshot("moneyhome-income-expense-plan-list-after-save-no-execute-20260803T0551.png"),
            screenshot("moneyhome-recurring-expense-plan-list-after-first-posting-20260803T0619.png"),
            screenshot("moneyhome-recurring-expense-plan-list-after-skip-20260803T0622.png"),
            screenshot("moneyhome-recurring-expense-plan-completed-after-execute-and-skips-20260803T0624.png"),
            screenshot("moneyhome-income-expense-plan-list-after-test-plan-deletes-20260803T0626.png"),
            screenshot("moneyhome-transfer-plan-list-after-save-no-execute-20260803T0638.png"),
            screenshot("moneyhome-transfer-plan-operation-menu-before-execute-20260803T0639.png"),
            screenshot("moneyhome-transfer-plan-completed-after-posting-20260803T0643.png"),
            screenshot("moneyhome-transfer-plans-completed-after-execute-and-skips-20260803T0653.png"),
            screenshot("moneyhome-completed-transfer-plan-modify-readonly-20260803T0655.png"),
            screenshot("moneyhome-transfer-plan-list-after-test-plan-deletes-20260803T0656.png"),
        ],
        "summary": "计划列表已验证普通提醒、收支计划和转账计划的差异化生命周期。转账计划执行中和完成态均无终止或恢复，完成修改为只读；每天 2 次且两期均跳过的计划仍把已执行次数显示为 2，证明该兼容字段实际是已处理次数。",
        "inputs": ["当前选中计划或提醒", "新增类型", "是否显示已完成"],
        "reads": ["计划定义", "计划实例统计", "提醒规则", "下次执行日期和状态"],
        "writes": ["计划新增、修改、终止、恢复和删除", "计划实例执行或跳过"],
        "derived": ["统一计划/提醒列表", "命令能力随类型和状态变化"],
        "commands": [
            command("N2", "提醒", "普通提醒入口已打开。", "pass"),
            command("N3", "收支计划", "收支计划入口已打开。", "pass"),
            command("N4", "转账计划", "转账计划入口已打开。", "pass", ["planning_budget_goal.plan_list_dlg.n4_click"]),
            command("N5", "基金申购/定投计划", "基金计划入口已打开。", "pass"),
            command("actExecute", "执行", "普通提醒上下文中按钮禁用；手工收支和转账计划上下文中启用，执行后生成对应交易并推进实例。", "pass", ["planning_budget_goal.plan_list_dlg.act_execute_execute"]),
            command("actCancel", "跳过", "已通过今日提醒跳过每天提醒、收支计划和转账计划实例；均未生成交易，周期定义按规则推进。", "pass", ["planning_budget_goal.plan_list_dlg.act_cancel_execute"]),
            command("actEdit", "修改", "完成收支和转账计划的修改入口均打开全字段禁用的只读快照。", "pass", ["planning_budget_goal.plan_list_dlg.act_edit_execute"]),
            command("actDel", "删除", "已删除一次性和周期收支、转账测试计划；列表立即移除定义，既有交易保留到最终基线恢复。", "pass", ["planning_budget_goal.plan_list_dlg.act_del_execute"], confirmation="您确定删除该计划吗？"),
            command("actEnd", "终止", "执行中的普通提醒、收支计划和转账计划操作菜单均不提供终止。", "pass", ["planning_budget_goal.plan_list_dlg.act_end_execute"], enabled=False),
            command("actResume", "恢复", "已完成收支和转账计划均不提供恢复；旧版仅保留只读修改和删除。", "pass", ["planning_budget_goal.plan_list_dlg.act_resume_execute"], enabled=False),
            command("miIncludFinish", "显示已完成的计划和提醒", "已实际启用；测试提醒和历史终止提醒进入查询结果，菜单项显示勾选。", "pass", ["planning_budget_goal.plan_list_dlg.mi_includ_finish_click"]),
        ],
        "requirements": ["计划中心必须从定义和实例生命周期投影列表；跳过只消费当前实例并推进下次日期，不能改写定义结束日期。内部必须分别统计 processed、executed、skipped 和 failed；兼容界面的已执行次数可投影 processed，但不得覆盖真实动作。"],
        "gaps": ["基金计划的命令启用矩阵", "自动执行、失败重试、并发、重复提交和冷启动"],
        "side_effects": [
            "新增每天重复提醒后列表立即刷新为执行中；跳过当天实例后下次日期由 2026-08-03 推进到 2026-08-04。",
            "每天 3 次的收支计划执行首期、跳过后两期后进入完成态，只生成一条 0.02 交易。",
            "每天 2 次的转账计划两期均跳过后进入完成态，已执行次数显示 2，但财务记录未增加。",
            "删除测试提醒和计划后列表移除定义；最终通过运行前副本恢复账簿精确基线。",
        ],
        "rollback": TRANSFER_PLAN_ROLLBACK,
    },
    "RT-15-039": {
        "resource": "TSECURITYREMINDDLG",
        "title": "证券市价提醒",
        "observed_at": LIMIT_REMINDER_OBSERVED_AT,
        "file_timestamp": LIMIT_REMINDER_FILE_TIMESTAMP,
        "backup_artifact": LIMIT_REMINDER_BACKUP,
        "navigation_steps": LIMIT_REMINDER_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("moneyhome-security-price-reminder-filled-live-20260803T1309.png"),
            screenshot("moneyhome-limit-reminders-today-triggered-cold-live-20260803T1327.png"),
            screenshot("moneyhome-limit-reminders-delete-confirmation-live-20260803T1331.png"),
            screenshot("moneyhome-limit-reminders-security-deleted-live-20260803T1333.png"),
        ],
        "summary": "已真实保存 000001 平安银行的价格下限 0.0100、上限 9999.99；冷启动后因当前行情低于 0.0100 生成只读告警。统一列表把 0.0100 格式化为 0.01，存在精度展示不一致；证券规则取消删除和确认删除均已验证。",
        "result_status": "pass",
        "inputs": ["证券稳定 ID", "价格下限", "价格上限"],
        "reads": ["证券候选和最新行情"],
        "writes": ["证券市价提醒规则"],
        "derived": ["行情越过阈值时生成带行情快照的提醒实例"],
        "commands": [
            command("btnUpdateCode", "更新证券", "更新入口已确认，联网结果未执行。", "partial", ["planning_budget_goal.security_remind_dlg.btn_update_code_click"]),
            command("btnSaveNew", "保存", "已保存四位小数下限规则，并在冷启动后观察到真实触发。", "pass", ["planning_budget_goal.security_remind_dlg.btn_save_new_click"]),
        ],
        "requirements": ["证券提醒必须保存标的 ID、四位价格精度、行情来源、行情版本、上下限和条件版本；列表格式化不得把领域精度降为两位。"],
        "gaps": ["等于边界、上下限倒置、上限触发、停牌和无行情", "行情更新、修改、引用失效、并发和失败持久化"],
        "side_effects": ["冷启动生成证券价格低于 0.0100 的当前告警；执行和跳过均不可用。", "删除证券规则后当前告警立即消失，最终冷启动不再恢复该规则。"],
        "rollback": LIMIT_REMINDER_ROLLBACK,
    },
    "RT-15-040": {
        "resource": "TSELECTREPETITIONFREQUENCYDLGFM",
        "title": "重复频率选择",
        "observed_at": RECURRING_OBSERVED_AT,
        "file_timestamp": RECURRING_FILE_TIMESTAMP,
        "backup_artifact": RECURRING_BACKUP,
        "navigation_steps": RECURRING_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("moneyhome-normal-reminder-repeat-menu-live-20260803T0513.png"),
            screenshot("moneyhome-custom-recurrence-dialog-live-20260803T0515.png"),
            screenshot("moneyhome-custom-recurrence-unit-menu-live-20260803T0517.png"),
        ],
        "summary": "重复菜单有一次性、每天、每周、每月、每年和自定义六个业务选项；自定义窗体默认“每 1 天 重复”，单位菜单为天、周、月、年。此前计数为 7 是把分隔线误算成选项。",
        "inputs": ["间隔数值", "频率单位"],
        "reads": ["父计划当前重复规则"],
        "writes": ["父计划草稿中的版本化重复规则"],
        "derived": ["开始日期后的应发生日期序列"],
        "commands": [command("btnSave", "确定", "已动态打开自定义重复频率窗体并确认默认间隔和四种单位；本轮未保存自定义规则。", "partial", ["planning_budget_goal.select_repetition_frequency_dlg_fm.btn_save_click"])],
        "requirements": ["重复规则必须保存频率单位、间隔、时区、短月策略和版本，不能只保存显示标签。"],
        "gaps": ["空值、零值、负数和超大自定义间隔", "月末短月、闰年、时区和结束边界", "自定义规则真实保存和冷启动"],
        "rollback": RECURRING_ROLLBACK,
    },
    "RT-15-041": {
        "resource": "TTRANSACTIONPLANDLGFM",
        "title": "交易计划公共编辑器",
        "observed_at": TRANSFER_PLAN_OBSERVED_AT,
        "file_timestamp": TRANSFER_PLAN_FILE_TIMESTAMP,
        "backup_artifact": TRANSFER_PLAN_BACKUP,
        "navigation_steps": TRANSFER_PLAN_NAVIGATION_STEPS,
        "screenshots": [screenshot("moneyhome-income-expense-plan-default-live-20260803T0542.png"), screenshot("moneyhome-income-expense-plan-execution-editor-20260803T0554.png"), screenshot("moneyhome-transfer-plan-default-live-20260803T0629.png"), screenshot("moneyhome-transfer-plan-execution-editor-20260803T0641.png"), screenshot("b15-fund-plan-dialog.png")],
        "summary": "该资源是收支、转账和基金计划的公共基类，没有独立入口；收支和转账计划均确认到期保存询问、定义与入账分离，以及手工执行先生成可编辑类型化交易草稿。",
        "inputs": ["交易计划名称", "公共日期和重复规则", "派生交易草稿"],
        "reads": ["派生计划类型和交易模板"],
        "writes": ["派生交易模板与计划定义"],
        "derived": ["统一计划草稿和保存协议", "到期实例执行前的交易草稿", "执行或跳过后的下一实例投影"],
        "mode": "base",
        "commands": [command("TTransactionPlanDlgFm", "独立打开", "没有独立用户入口，由三个派生计划编辑器覆盖。", "not_applicable")],
        "requirements": ["Rust 版应复用交易计划编辑组件，但保留收支、转账和基金的类型化字段与执行命令；手工执行必须先建立可编辑草稿，再由幂等命令提交最终交易。实例统计必须区分执行、跳过和失败，兼容已执行次数只能作为已处理数投影。"],
        "gaps": ["基金计划是否共享同一到期询问", "公共关闭、校验失败和并发冲突协议"],
        "rollback": TRANSFER_PLAN_ROLLBACK,
    },
    "RT-15-042": {
        "resource": "TXFERPLANDLGFM",
        "title": "转账计划",
        "observed_at": TRANSFER_PLAN_OBSERVED_AT,
        "file_timestamp": TRANSFER_PLAN_FILE_TIMESTAMP,
        "backup_artifact": TRANSFER_PLAN_BACKUP,
        "navigation_steps": TRANSFER_PLAN_NAVIGATION_STEPS,
        "screenshots": [
            screenshot("moneyhome-transfer-plan-add-menu-20260803T0628.png"),
            screenshot("moneyhome-transfer-plan-default-live-20260803T0629.png"),
            screenshot("moneyhome-transfer-plan-out-account-dropdown-20260803T0630.png"),
            screenshot("moneyhome-transfer-plan-accounts-selected-20260803T0634.png"),
            screenshot("moneyhome-transfer-plan-filled-manual-20260803T0636.png"),
            screenshot("moneyhome-transfer-plan-save-due-prompt-20260803T0637.png"),
            screenshot("moneyhome-transfer-plan-execution-editor-20260803T0641.png"),
            screenshot("moneyhome-account-center-after-transfer-plan-posting-20260803T0644.png"),
            screenshot("moneyhome-financial-records-after-transfer-plan-posting-20260803T0645.png"),
            screenshot("moneyhome-recurring-transfer-plan-ready-20260803T0647.png"),
            screenshot("moneyhome-transfer-plans-completed-after-execute-and-skips-20260803T0653.png"),
            screenshot("moneyhome-completed-transfer-plan-modify-readonly-20260803T0655.png"),
        ],
        "summary": "转账计划已完成一次性执行和周期跳过生命周期。新增默认当天、一次性、提前 3 天、金额/手续费 0.00、自动执行未勾选；选择转出账户后手续费账户默认同一账户。到期保存选择否只保存定义，人工执行打开可编辑转账草稿，立即入账后原子生成本金双边和手续费。",
        "inputs": ["计划名称", "开始日期", "重复规则", "转出账户", "转入账户", "金额", "手续费账户", "手续费", "标签", "自动执行"],
        "reads": ["账户和标签候选", "账户币种与状态", "重复规则"],
        "writes": ["转账交易模板", "计划定义及执行模式"],
        "derived": ["逐期转账计划实例", "执行后原子生成转出、转入和手续费分录"],
        "commands": [
            command("SelOutAcct", "选择转出账户", "已从真实账户候选绑定 Cash-CNY；选择后手续费账户自动默认为 Cash-CNY。", "pass", ["planning_budget_goal.xfer_plan_dlg_fm.sel_out_acct_close_up"]),
            command("SelInAcct", "选择转入账户", "已从真实账户候选绑定 Qrd 农行，必须保存稳定账户对象而非显示文字。", "pass"),
            command("selAcctFees", "选择手续费账户", "已确认可与转出账户相同；本次手续费 0.01 从 Cash-CNY 扣除。", "pass", ["planning_budget_goal.xfer_plan_dlg_fm.sel_acct_fees_close_up"]),
            command("chkAutoExecute", "自动执行", "新增态默认未勾选；本轮保持手工执行。", "pass", ["planning_budget_goal.xfer_plan_dlg_fm.chk_auto_execute_click"]),
            command("btnSave", "确定", "到期保存弹出立即执行询问；选择否后定义保留且不生成交易。", "pass"),
            command("actExecute", "执行", "打开执行计划-转账草稿，带出账户、本金、手续费、标签、日期和计划自动入账备注；点击立即入账后生成唯一转账。", "pass", ["planning_budget_goal.plan_list_dlg.act_execute_execute"]),
            command("actJump", "跳过", "每天 2 次的转账计划两期均实际跳过，日期逐期推进且财务记录数不变。", "pass", ["planning_budget_goal.new_remind_dlg_fm.act_jump_execute"]),
            command("actEdit", "修改", "完成计划打开全字段禁用的只读快照；两期均跳过时已执行次数仍显示 2。", "pass", ["planning_budget_goal.plan_list_dlg.act_edit_execute"]),
            command("actDel", "删除", "一次性和周期测试计划定义均已删除；已生成交易直到基线恢复前仍保留。", "pass", ["planning_budget_goal.plan_list_dlg.act_del_execute"], confirmation="您确定删除该计划吗？"),
        ],
        "requirements": ["转账计划执行必须用单个幂等命令原子生成两侧本金和独立手续费分录；来源总流出为本金加由该账户承担的手续费，目标只增加本金，净资产只减少费用。计划实例必须分别记录 executed、skipped、failed 和 processed 统计。"],
        "gaps": ["同账户、跨币种、其它手续费账户和余额不足", "自动执行、冷启动、重复执行、失败重试、并发和事务回滚"],
        "side_effects": [
            "一次性计划本金 0.03、手续费 0.01 入账后，Cash-CNY 608.00 -> 607.96，Qrd 农行所在 China Bank 分组增加 0.03，净资产只减少 0.01。",
            "全局财务记录新增一条转账，流入 0.03、流出 0.04、账户显示 Cash-CNY->Qrd 农行；记录数 2189 -> 2190。",
            "每天 2 次的周期计划两期均跳过，未生成任何额外交易；完成快照的已执行次数显示 2。",
            "删除两个测试计划定义后归档业务态，再恢复 test.mh8 精确基线。",
        ],
        "rollback": TRANSFER_PLAN_ROLLBACK,
    },
}


def build_record(execution_id: str, spec: dict[str, Any]) -> dict[str, Any]:
    """按截图、DFM 和事件证据构造 schema v1 观察记录。"""

    mode = spec.get("mode", "observed")
    reachable = mode != "base"
    state_status = "not_applicable" if mode == "base" else "pending" if mode == "static" else "observed"
    result_status = spec.get("result_status", "unreachable" if mode == "base" else "partial")
    evidence = [
        {"kind": "screenshot", "path": path, "description": f"{spec['title']}真实运行页面。"}
        for path in spec["screenshots"]
    ]
    evidence.extend(
        [
            {"kind": "file", "path": "docs/runtime-dfm-all-forms.json", "description": f"{spec['resource']} 控件、字段、菜单和事件资源。"},
            {"kind": "file", "path": "docs/runtime-event-command-dataflow.json", "description": f"{spec['resource']} 事件到 Rust 命令边界。"},
            {"kind": "manual_note", "path": NOTE_PATH, "description": "计划、实例、提醒规则、触发实例和今日收件箱的数据流结论。"},
        ]
    )
    return {
        "schema_version": 1,
        "execution_id": execution_id,
        "resource": spec["resource"],
        "observed_at": spec.get("observed_at", OBSERVED_AT),
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8",
            "sha256_before": BASELINE_HASH,
            "sha256_after": BASELINE_HASH,
            "backup_artifact": spec.get("backup_artifact", BASELINE_BACKUP),
        },
        "navigation": {
            "entry_point": "财智8 -> 计划与提醒，或限额提醒/今日提醒入口",
            "steps": spec.get(
                "navigation_steps",
                DYNAMIC_NAVIGATION_STEPS
                if spec.get("file_timestamp") == DYNAMIC_FILE_TIMESTAMP
                else [
                    "复核 2026-07-29 在 test.mh8 上取得的真实页面截图",
                    f"对账 {spec['resource']} 的 DFM 控件和事件处理器",
                    "区分已观察命令、静态入口、未执行写入和公共基类",
                    "回填计划定义、实例、提醒规则和触发实例的数据流",
                ],
            ),
            "reachable": reachable,
            "unreachable_reason": None if reachable else "公共基类没有独立用户入口，由派生编辑器覆盖。",
        },
        "states": [
            {
                "name": spec["title"],
                "status": state_status,
                "observations": spec["summary"],
                "evidence_paths": spec["screenshots"],
            }
        ],
        "commands": spec["commands"],
        "data_flow": {
            "inputs": spec["inputs"],
            "reads": spec["reads"],
            "writes": spec["writes"],
            "derived_results": spec["derived"],
            "side_effects": spec.get("side_effects", ["本次证据整理未提交计划或提醒业务数据。"]),
            "rollback": spec.get(
                "rollback",
                (
                    "2026-08-03 的补充启动因 Windows 自动化未返回旧 VCL 窗口而未操作业务页面；"
                    f"已归档启动副本并用 {BASELINE_BACKUP} 恢复 test.mh8 至 {BASELINE_HASH}，"
                    "MoneyHome8 进程和锁文件均为 0。"
                ),
            ),
        },
        "evidence": evidence,
        "requirements_update": spec["requirements"],
        "result": {
            "status": result_status,
            "summary": spec["summary"],
            "remaining_gaps": spec["gaps"],
        },
    }


def main() -> None:
    """写入新时间戳记录，保留旧记录作为历史证据。"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for execution_id, spec in FORM_SPECS.items():
        record = build_record(execution_id, spec)
        path = OUTPUT_DIR / f"{execution_id}-{spec.get('file_timestamp', FILE_TIMESTAMP)}.json"
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(FORM_SPECS)} RT-15 plan/reminder subrecords")


if __name__ == "__main__":
    main()
