"""生成 B18 登录、同步与外部服务的运行态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T01:58:07+08:00"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "9F41B350CA975C2302DACFA923FB30E16477DEFF1E033F740710417C7E3245F7"
FINAL_HASH = "C8315E2B65CA39C57F9C4CB1BFA5D537EAA403BCED60CB4FB298189439E2377D"
BACKUP_ARTIFACT = "artifacts/runtime-validation/backups/test-before-b18.mh8"
NOTES = "artifacts/runtime-validation/B18-auth-sync-external-notes.md"


def shot(name: str) -> str:
    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(kind: str, path: str, description: str) -> dict:
    return {"kind": kind, "path": path, "description": description}


RECORDS = {
    "RT-18-001": {
        "resource": "TLOGINDIALOG",
        "entry": "无正常业务入口；旧数据库驱动认证失败时的技术兜底资源",
        "steps": ["正常打开 test.mh8", "执行 B18 各业务入口", "核对菜单和静态调用边", "确认窗口未出现"],
        "reachable": False,
        "unreachable_reason": "正常账簿启动和全部 B18 业务流程均未触发；无菜单入口和已定位业务调用边。",
        "states": [
            ("正常账簿启动", "test.mh8 正常打开，未显示 Database Login。", [shot("b18-main-baseline.png")]),
            ("技术资源定位", "资源字段为 Database、User Name、Password，属于数据库驱动登录兜底，不是用户同步账号登录。", [NOTES]),
        ],
        "commands": [
            ("OKButton", "OK", {"enabled": True, "visible": True}, "正常流程不可达", None, "不纳入产品业务命令。", "partial"),
            ("CancelButton", "Cancel", {"enabled": True, "visible": True}, "正常流程不可达", None, "不纳入产品业务命令。", "partial"),
        ],
        "data_flow": {
            "inputs": ["旧数据库名称", "数据库用户名", "数据库密码"],
            "reads": ["旧数据库连接认证上下文"],
            "writes": ["无业务写入"],
            "derived_results": ["数据库连接成功或认证失败"],
            "side_effects": ["正常 MoneyHome8 业务流程未触发该窗口"],
            "rollback": "Rust 版只返回结构化数据库打开错误，不创建要求用户输入数据库凭据的产品页面。",
        },
        "evidence": [
            evidence("screenshot", shot("b18-main-baseline.png"), "正常打开 test.mh8 的主界面。"),
            evidence("manual_note", NOTES, "技术资源定位与排除依据。"),
        ],
        "requirements": [
            "Database Login 不进入 Rust 产品 UI 功能范围。",
            "数据库打开失败返回结构化本地错误，不要求最终用户输入数据库账号密码。",
            "任何数据库凭据不得写入日志、截图或业务账簿。",
        ],
        "summary": "确认 TLoginDialog 是旧数据库驱动技术兜底，正常产品流程不可达，不应复刻为用户功能。",
        "gaps": ["仅在需要完全复现旧 Jet 认证失败路径时，补充其精确触发条件"],
    },
    "RT-18-002": {
        "resource": "TONLINEGETDATAFM",
        "entry": "财智8主菜单 -> 财务工具 -> 更新行情数据",
        "steps": ["观察最新和历史页签", "选择外汇牌价并更新", "记录 28 条成功结果", "选择股票收盘价", "运行中点击中止", "完成关闭"],
        "states": [
            ("最新行情", "列出股票、港股、美股、开放式基金、贵金属、期货、外汇、存款利率和证券交易费率九类数据源。", [shot("b18-online-quote-update.png")]),
            ("历史行情", "列出七类价格数据源，并提供开始日期和结束日期。", [shot("b18-online-quote-history.png")]),
            ("外汇成功", "下载 2026-07-29 的 28 条外汇牌价并写入账簿，页面显示明确成功日志。", [shot("b18-online-quote-update-running.png")]),
            ("股票中止", "运行中筛选控件禁用并只显示中止；中止后恢复操作，日志为空且账簿文件未变化。", [shot("b18-online-quote-stock-selected.png"), shot("b18-online-quote-aborted.png")]),
        ],
        "commands": [
            ("RzButtonUpdate", "更新", {"enabled": True, "visible": True}, "更新外汇牌价", None, "成功更新 28 条记录。", "pass"),
            ("RzButtonAbort", "中止", {"enabled": True, "visible": True}, "股票收盘价更新运行中点击", None, "恢复筛选和更新按钮，本次无文件写入。", "pass"),
            ("btnComplete", "完成", {"enabled": True, "visible": True}, "成功或中止后关闭", None, "窗口正常关闭。", "pass"),
        ],
        "data_flow": {
            "inputs": ["最新或历史模式", "数据源选择", "持仓范围", "历史开始和结束日期"],
            "reads": ["现有持仓和历史交易标的", "各数据源上次更新时间", "外部行情服务"],
            "writes": ["行情批次和 MarketQuote 时间序列；本轮写入 28 条外汇牌价"],
            "derived_results": ["最后更新时间", "持仓市值、盈亏和报表估值输入"],
            "side_effects": ["外汇成功时锁定账簿增加 102,400 字节", "中止股票更新时账簿大小和时间戳不变"],
            "rollback": "行情批次完整下载和校验后才发布快照；中止或部分失败保留最近有效行情，不覆盖完整快照。",
        },
        "evidence": [
            evidence("screenshot", shot("b18-online-quote-update.png"), "最新行情数据源列表。"),
            evidence("screenshot", shot("b18-online-quote-history.png"), "历史行情数据源和日期列。"),
            evidence("screenshot", shot("b18-online-quote-update-running.png"), "28 条外汇牌价成功结果。"),
            evidence("screenshot", shot("b18-online-quote-aborted.png"), "股票行情中止后恢复状态。"),
            evidence("manual_note", NOTES, "行情更新文件变化和取消时序。"),
        ],
        "requirements": [
            "每类行情由独立 provider adapter 输出统一行情批次。",
            "成功、离线、失败、中止和重试具有可区分状态，部分响应不得覆盖最近有效快照。",
            "行情写入与持仓、投资一览和报表刷新共享同一批次版本和估值时点。",
        ],
        "summary": "已验证最新/历史行情、九类数据源、外汇 28 条成功写入和股票更新中止。",
        "gaps": ["其余八类最新行情的成功和失败结果", "历史行情日期边界", "网络失败、超时和重试", "行情字段与旧表的精确映射"],
    },
    "RT-18-003": {
        "resource": "TREMOTENOTIFICATIONDLGFM",
        "entry": "财智8主菜单 -> 设置 -> 手机提醒设置",
        "steps": ["观察已启用状态", "关闭手机快查", "观察即时保存和控件状态", "恢复启用", "从注册账号进入共享注册页", "重开复核"],
        "states": [
            ("默认启用", "复用已保存同步身份，手机快查开关已启用；截图已脱敏。", [shot("b18-remote-notification-default.png")]),
            ("关闭并即时保存", "取消启用后页面显示已保存，密码和注册按钮仍可用，账簿时间戳改变。", [shot("b18-remote-notification-disabled.png")]),
            ("恢复复核", "重新启用后关闭并重开，开关保持启用。", [shot("b18-remote-notification-restored.png")]),
        ],
        "commands": [
            ("chkEnable", "启用手机快查功能", {"enabled": True, "visible": True}, "关闭后再恢复", None, "两次操作均即时保存。", "pass"),
            ("btnRegister", "注册账号", {"enabled": True, "visible": True}, "打开注册入口后取消", None, "复用 TSyncUserRegisterFm。", "pass"),
        ],
        "data_flow": {
            "inputs": ["已保存同步身份", "手机快查启用标志"],
            "reads": ["本地同步配置和远程通知设置"],
            "writes": ["手机快查启用设置"],
            "derived_results": ["移动端财务提醒和投资、预算快查资格"],
            "side_effects": ["开关点击立即修改账簿时间戳", "本轮未调用远端通知服务"],
            "rollback": "设置保存失败时恢复原开关状态；远端服务失败不得影响本地提醒和账簿写入。",
        },
        "evidence": [
            evidence("screenshot", shot("b18-remote-notification-default.png"), "脱敏后的默认启用状态。"),
            evidence("screenshot", shot("b18-remote-notification-disabled.png"), "关闭后即时保存状态。"),
            evidence("screenshot", shot("b18-remote-notification-restored.png"), "恢复后重开复核。"),
            evidence("manual_note", NOTES, "手机快查数据流与安全边界。"),
        ],
        "requirements": [
            "手机快查作为可禁用外部适配器，不能成为本地预算、持仓或提醒的真相源。",
            "密码和令牌进入系统凭据存储，不得出现在账簿业务表、日志、截图或 UI Automation 值中。",
            "开关保存显示明确成功或失败状态，失败时不伪装为已保存。",
        ],
        "summary": "已验证手机快查启用、即时保存、恢复、共享注册入口和凭据暴露缺陷。",
        "gaps": ["真实移动端查询和通知投递", "服务器开关下载/上传", "离线和身份过期结果"],
    },
    "RT-18-004": {
        "resource": "TSYNCUSERDATAFM",
        "entry": "财智8主菜单 -> 设置 -> 同步设置",
        "steps": ["观察默认双向同步", "取消条款同意", "验证开始同步禁用", "切换单向上传和关闭时自动同步", "恢复默认", "打开注册页", "取消删除账号密码", "重开复核"],
        "states": [
            ("默认同步配置", "显示上次同步时间和已保存身份；双向同步、同意条款启用，关闭账簿自动同步关闭。截图已脱敏。", [shot("b18-sync-settings-default.png")]),
            ("条款门控", "取消我同意后开始同步立即禁用。", [shot("b18-sync-agreement-off.png")]),
            ("单向上传和自动同步", "单向上传说明以本地账簿为准覆盖远端；关闭账簿自动同步可独立启用。", [shot("b18-sync-one-way-auto-close.png")]),
            ("恢复和删除取消", "重开确认恢复双向同步与自动同步关闭；删除本地保存账号密码显示确认并选择否。", [shot("b18-sync-restored.png"), shot("b18-sync-delete-account-confirm.png")]),
        ],
        "commands": [
            ("chkAgree", "我同意", {"enabled": True, "visible": True}, "取消后恢复", None, "控制开始同步可用状态。", "pass"),
            ("rbOneWay", "单向上传", {"enabled": True, "visible": True}, "临时选择后恢复双向", None, "模式设置会修改账簿时间戳。", "pass"),
            ("chkSyncByCloseBook", "关闭账簿时自动同步", {"enabled": True, "visible": True}, "临时启用后恢复", None, "设置即时保存。", "pass"),
            ("btnSyncStart", "开始同步", {"enabled": True, "visible": True}, "本轮未触发真实同步", None, "避免操作测试账簿之外的远端账号数据。", "pending"),
            ("miDeleteSyncUserPassword", "删除同步账号密码", {"enabled": True, "visible": True}, "打开确认后选择否", "您确定删除此账簿中保存的同步账号密码吗？", "本地凭据未删除。", "pass"),
            ("miModifySyncUserPassword", "修改同步账号密码", {"enabled": True, "visible": True}, "菜单命令", None, "不打开本地窗体，静态代码指向旧 HTTP 密码页面。", "partial"),
        ],
        "data_flow": {
            "inputs": ["同步身份引用", "双向或单向模式", "条款同意", "关闭时自动同步"],
            "reads": ["本地账簿对象、变更日志、同步游标和旧远端参数"],
            "writes": ["同步配置；确认同步后写批次、对象结果、冲突和远端对象"],
            "derived_results": ["双向合并计划", "单向覆盖计划", "上次同步时间"],
            "side_effects": ["设置切换立即改变账簿时间戳", "本轮未发送真实同步请求", "旧条款和密码管理使用明文 HTTP URL"],
            "rollback": "模式和设置保存失败恢复原值；同步按对象记录结果，取消停止后续对象，已提交对象必须可审计和续传。",
        },
        "evidence": [
            evidence("screenshot", shot("b18-sync-settings-default.png"), "脱敏后的默认双向同步状态。"),
            evidence("screenshot", shot("b18-sync-agreement-off.png"), "条款未同意时开始同步禁用。"),
            evidence("screenshot", shot("b18-sync-one-way-auto-close.png"), "单向上传和关闭时自动同步。"),
            evidence("screenshot", shot("b18-sync-delete-account-confirm.png"), "删除本地保存同步凭据确认。"),
            evidence("manual_note", NOTES, "同步模式、旧 URL、文件变化和恢复结果。"),
        ],
        "requirements": [
            "本地账簿始终可独立写入，远端失败、身份过期和旧服务下线不得阻塞记账。",
            "双向同步提供逐对象冲突和删除墓碑；单向上传提交前展示远端覆盖范围并生成本地快照。",
            "同步秘密使用系统凭据存储，所有网络通信使用 HTTPS，UI 自动化和日志不得暴露明文。",
            "关闭账簿自动同步必须可取消、有限时并在关闭后提供可追踪结果，不能无限阻塞退出。",
        ],
        "summary": "已验证同步默认模式、条款门控、单向覆盖说明、自动同步设置、凭据删除确认和设置恢复。",
        "gaps": ["真实双向/单向同步结果", "网络失败、冲突、删除传播和续传", "关闭账簿自动同步的超时与取消", "旧服务协议字段"],
    },
    "RT-18-005": {
        "resource": "TSYNCUSERREGISTERFM",
        "entry": "同步设置或手机快查设置 -> 注册账号",
        "steps": ["从同步设置打开注册页", "观察四个字段", "提交空表单", "记录邮箱必填提示", "取消关闭", "从手机快查确认复用同一窗体"],
        "states": [
            ("空注册表单", "字段为电子邮箱、密码、确认密码和昵称；注册按钮在全空状态仍启用。", [shot("b18-sync-register.png")]),
            ("空值校验", "点击注册后首先提示请输入电子邮箱。", [shot("b18-sync-register-empty-validation.png")]),
        ],
        "commands": [
            ("btnRegister", "注册", {"enabled": True, "visible": True}, "全空表单提交", None, "阻止提交并提示请输入电子邮箱。", "pass"),
        ],
        "data_flow": {
            "inputs": ["电子邮箱", "密码", "确认密码", "昵称"],
            "reads": ["本地输入和远端账号注册服务"],
            "writes": ["远端同步账号；成功后绑定本地账簿身份，本轮未创建"],
            "derived_results": ["字段级校验错误或新同步身份"],
            "side_effects": ["空值校验无账簿和远端写入", "同步和手机快查复用同一注册窗体"],
            "rollback": "远端注册成功与本地身份绑定分阶段处理；本地绑定失败不得丢失可恢复结果，远端失败不得写入本地身份。",
        },
        "evidence": [
            evidence("screenshot", shot("b18-sync-register.png"), "空注册表单。"),
            evidence("screenshot", shot("b18-sync-register-empty-validation.png"), "邮箱必填提示。"),
            evidence("manual_note", NOTES, "共享入口和未提交边界。"),
        ],
        "requirements": [
            "电子邮箱、密码确认和昵称按明确规则校验，错误定位到字段。",
            "客户端未满足最低有效条件时禁用提交；服务端错误仍保留原始可读原因。",
            "注册请求不得记录密码，成功后只保存凭据引用和远端稳定身份。",
        ],
        "summary": "已验证同步账号注册字段、共享入口和空邮箱校验，未创建真实远端账号。",
        "gaps": ["有效注册、重复邮箱、密码策略、昵称边界和服务端失败", "注册成功后的本地绑定和撤销"],
    },
}


def build_record(execution_id: str, spec: dict) -> dict:
    states = [
        {"name": name, "status": "observed", "observations": observations, "evidence_paths": paths}
        for name, observations, paths in spec["states"]
    ]
    commands = [
        {
            "component": component,
            "label": label,
            "initial_state": initial_state,
            "trigger": trigger,
            "confirmation": confirmation,
            "outcome": outcome,
            "status": status,
        }
        for component, label, initial_state, trigger, confirmation, outcome, status in spec["commands"]
    ]
    return {
        "schema_version": 1,
        "execution_id": execution_id,
        "resource": spec["resource"],
        "observed_at": OBSERVED_AT,
        "application": {
            "executable": r"C:\Program Files (x86)\MoneyWise\MoneyHome8\Program\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": LEDGER_PATH,
            "sha256_before": BASELINE_HASH,
            "sha256_after": FINAL_HASH,
            "backup_artifact": BACKUP_ARTIFACT,
        },
        "navigation": {
            "entry_point": spec["entry"],
            "steps": spec["steps"],
            "reachable": spec.get("reachable", True),
            "unreachable_reason": spec.get("unreachable_reason"),
        },
        "states": states,
        "commands": commands,
        "data_flow": spec["data_flow"],
        "evidence": spec["evidence"],
        "requirements_update": spec["requirements"],
        "result": {"status": "partial", "summary": spec["summary"], "remaining_gaps": spec["gaps"]},
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for execution_id, spec in RECORDS.items():
        output_path = OUTPUT_DIR / f"{execution_id}-20260730T015807+0800.json"
        output_path.write_text(
            json.dumps(build_record(execution_id, spec), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"generated {len(RECORDS)} B18 records")


if __name__ == "__main__":
    main()
