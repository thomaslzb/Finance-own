"""生成 B17 导入导出的运行态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T01:16:49+08:00"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "B1136914BD1246E917BBB4A40D24F53AFF7E9C0B2769B238E5890D7F643D9C79"
FINAL_HASH = "9F41B350CA975C2302DACFA923FB30E16477DEFF1E033F740710417C7E3245F7"
BACKUP_ARTIFACT = "artifacts/runtime-validation/backups/test-before-b17-import-crash.mh8"
NOTES = "artifacts/runtime-validation/B17-import-export-notes.md"


def shot(name: str) -> str:
    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(kind: str, path: str, description: str) -> dict:
    return {"kind": kind, "path": path, "description": description}


RECORDS = {
    "RT-17-001": {
        "resource": "TEXPORTDATAFM",
        "entry": "财智8主菜单 -> 导出账簿数据",
        "steps": ["打开数据导出", "核对基本选项和 21 类数据选项", "执行全选导出", "执行仅货币信息导出", "校验两个 XML 文件"],
        "states": [
            ("默认选项", "默认导出 XML、当年日期范围、所有账户、增加模式和 21 类数据。", [shot("b17-export-data-dialog.png"), shot("b17-export-data-options.png")]),
            ("全量长时间运行", "界面超过 90 秒无完成反馈且控件禁用，后台随后生成可完整解析的 10,146,378 字节 XML。", [shot("b17-export-stalled.png")]),
            ("最小成功", "仅货币信息约 1.36 秒完成并显示导出成功，文件包含 184 条货币。", [shot("b17-export-currency-success-message.png")]),
        ],
        "commands": [
            ("BtnOk", "导出", {"enabled": True, "visible": True}, "选择目标路径并开始导出", None, "最小导出成功；全量导出最终生成文件但缺少及时完成反馈。", "partial"),
            ("tsOptions", "数据选项", {"enabled": True, "visible": True}, "双击清空后仅选择货币信息", None, "支持按类别缩小导出范围。", "pass"),
        ],
        "data_flow": {
            "inputs": ["目标 XML 路径", "日期范围", "账户范围", "增加或覆盖语义", "21 类数据选择"],
            "reads": ["人员、货币、分类、证券、基金、汇率、账户、交易等账簿数据"],
            "writes": ["账簿外 GB2312 XML 文件"],
            "derived_results": ["INOUTDATA 根节点", "VERSION 1.21 交换合同", "按实际数据生成的 14 个全量数据段"],
            "side_effects": ["全量导出界面长时间无反馈但后台继续写文件", "导出不改变业务数据；会话级账簿元数据仍可能在关闭时变化"],
            "rollback": "目标文件应先写临时文件并校验完整 XML 后原子替换；取消或失败不得留下半成品或误报成功。",
        },
        "evidence": [
            evidence("screenshot", shot("b17-export-data-dialog.png"), "数据导出默认基本选项。"),
            evidence("screenshot", shot("b17-export-data-options.png"), "21 类数据选项。"),
            evidence("screenshot", shot("b17-export-stalled.png"), "全量导出长时间无反馈状态。"),
            evidence("screenshot", shot("b17-export-currency-success-message.png"), "最小导出成功消息。"),
            evidence("export", "artifacts/runtime-validation/export-samples/currency-only.xml", "可回读的货币信息 XML。"),
            evidence("export", "artifacts/runtime-validation/export-samples/test-ledger-all.xml", "延迟生成但结构完整的全量 XML。"),
            evidence("manual_note", NOTES, "XML 编码、数据段、哈希和时序说明。"),
        ],
        "requirements": ["兼容读取旧版 GB2312/代码页 936、CRLF、INOUTDATA VERSION 1.21 XML。", "长任务必须提供可取消进度、后台任务状态和明确成功/失败结果。", "导出使用临时文件、完整性校验和原子替换。"],
        "summary": "已验证全量和最小导出、真实 XML 编码与节点合同；全量导出存在长时间无反馈但后台继续完成的问题。",
        "gaps": ["逐个校准 21 类选择与实际 XML 节点的映射", "验证覆盖模式和不可写路径", "验证用户取消后台任务"],
    },
    "RT-17-002": {
        "resource": "TIMPORTCATEGORYDLGFM",
        "entry": "财务记录 -> 操作 -> 替换收支项目",
        "steps": ["打开替换收支项目", "观察候选列表和查询命令", "观察目标项目和确定替换", "关闭取消"],
        "states": [("初始和取消", "列为日期、收支项目、流入、流出、币种、资金账户/款项、标签和备注；未执行批量替换。", ["artifacts/runtime-validation/replace-income-expense-item-dialog.png"])],
        "commands": [
            ("btnFilter", "查询记录", {"enabled": True, "visible": True}, "本轮未执行", None, "用于装载候选交易。", "pending"),
            ("btnSaveExit", "确定替换", {"enabled": True, "visible": True}, "本轮未选择记录和目标项目", None, "真实批量写入和失败回滚仍待验证。", "pending"),
        ],
        "data_flow": {
            "inputs": ["查询条件", "候选记录选择", "目标收支项目"],
            "reads": ["交易分类引用及列表显示字段"],
            "writes": ["确认后批量更新所选交易的收支项目引用；本轮未写入"],
            "derived_results": ["查询、选择、目标和确认四阶段批量流程"],
            "side_effects": ["关闭取消未产生业务写入"],
            "rollback": "批量替换必须单事务提交，任一记录失败时整体回滚并报告影响数量。",
        },
        "evidence": [evidence("screenshot", "artifacts/runtime-validation/replace-income-expense-item-dialog.png", "替换收支项目窗口。"), evidence("manual_note", NOTES, "B17 统一边界说明。")],
        "requirements": ["提交前显示选中数量、来源分类和目标分类。", "禁止空选择和同分类替换。", "列表、预算和报表必须在同一提交后读取新分类引用。"],
        "summary": "已验证批量替换入口、列和四阶段结构，真实查询和替换仍未执行。",
        "gaps": ["查询候选、多选、确认和影响数量", "成功结果、失败回滚和报表联动"],
    },
    "RT-17-003": {
        "resource": "TIMPORTDATAFM",
        "entry": "财智8主菜单 -> 导入账簿数据",
        "steps": ["打开导入数据", "选择 currency-only.xml", "仅选择货币信息", "执行导入", "记录两次异常和进程退出"],
        "states": [
            ("文件和类别选择", "支持 21 类数据选择，本轮只保留货币信息。", [shot("b17-import-data-dialog.png"), shot("b17-import-currency-only.png")]),
            ("执行失败", "导入旧程序自己的成功导出文件时先后发生 EAccessViolation 和 C0000025，目标进程退出。", [shot("b17-import-currency-application-error.png"), shot("b17-import-currency-application-error-2.png")]),
        ],
        "commands": [("BtnOk", "导入", {"enabled": True, "visible": True}, "导入 currency-only.xml 的货币信息", None, "旧程序崩溃；异常前未观察到账簿变化，重开后无业务变化。", "fail")],
        "data_flow": {
            "inputs": ["旧版交换 XML", "导入数据类别", "增加或覆盖语义"],
            "reads": ["外部 XML 和现有账簿引用数据"],
            "writes": ["本轮在崩溃前未观察到业务写入"],
            "derived_results": ["应先形成解析批次、字段错误和重复检测结果"],
            "side_effects": ["旧程序进程崩溃", "首次解锁后建立二进制备份"],
            "rollback": "解析和校验必须在账簿外完成；只有全部校验通过后才允许单事务提交，崩溃或错误不得留下部分数据。",
        },
        "evidence": [
            evidence("screenshot", shot("b17-import-data-dialog.png"), "整账簿导入页面。"),
            evidence("screenshot", shot("b17-import-currency-application-error.png"), "EAccessViolation。"),
            evidence("screenshot", shot("b17-import-currency-application-error-2.png"), "C0000025 外部异常。"),
            evidence("file", BACKUP_ARTIFACT, "崩溃后首次解锁的账簿备份。"),
            evidence("manual_note", NOTES, "异常文本和重开复核。"),
        ],
        "requirements": ["任何输入错误不得导致进程崩溃。", "解析、映射、校验、预览和提交必须分阶段隔离。", "错误报告必须指出文件、数据段、行或字段，并保证原子回滚。"],
        "summary": "已验证整账簿导入选择流程，并复现旧程序回导自身 XML 时崩溃的严重缺陷。",
        "gaps": ["构造可成功回导的完整最小样本", "覆盖模式、重复检测、逐行错误和成功提交"],
    },
    "RT-17-004": {
        "resource": "TIMPORTJIAOGEDANDLGFM",
        "entry": "财智8主菜单 -> 财务工具 -> 导入股票交割单",
        "steps": ["打开交割单导入", "展开系统方案", "输入一条空格分隔样本", "进入预览", "关闭取消"],
        "states": [
            ("方案和映射", "默认空格分隔、按列头文字匹配，显示交易文字和 10 个字段映射。", [shot("b17-import-trade-statement-scheme-details.png")]),
            ("解析预览", "测试买入记录成功解析为证券买入，默认证券账户和结算账户为国泰君安。", [shot("b17-import-trade-statement-sample.png"), shot("b17-import-trade-statement-preview.png")]),
        ],
        "commands": [
            ("btnNext", "下一步", {"enabled": True, "visible": True}, "解析一条测试交割单", None, "成功进入预览。", "pass"),
            ("btnImport", "确认导入", {"enabled": True, "visible": True}, "本轮未触发", None, "投资成交、费用和资金分录未写入。", "pending"),
        ],
        "data_flow": {
            "inputs": ["原始交割单文本", "分隔符", "交易类型映射", "字段映射", "含费口径", "目标账户"],
            "reads": ["证券账户、结算账户、证券列表和投资收益分类"],
            "writes": ["确认后应原子写入成交、费用、持仓和资金分录；本轮未确认"],
            "derived_results": ["证券买入预览记录", "字段标准化和默认账户映射"],
            "side_effects": ["预览关闭前未观察到确认导入产生的业务写入"],
            "rollback": "预览和方案编辑不写业务真相；确认导入必须对成交、费用、持仓和资金分录整体提交或回滚。",
        },
        "evidence": [evidence("screenshot", shot("b17-import-trade-statement-entry.png"), "交割单入口页。"), evidence("screenshot", shot("b17-import-trade-statement-scheme-details.png"), "系统方案和映射。"), evidence("screenshot", shot("b17-import-trade-statement-preview.png"), "成功解析的预览。"), evidence("manual_note", NOTES, "样本和可达性结论。")],
        "requirements": ["无可执行 VMT 不能作为不可达结论，功能范围以真实入口为准。", "交易文字、字段映射和方案必须可版本化审计。", "预览可批量修改，最终提交必须生成平衡且可追溯的投资分录。"],
        "summary": "已证明无 VMT 的交割单窗体真实可达，并完成系统方案、字段映射和一条买入记录预览。",
        "gaps": ["确认导入后的持仓和资金结果", "卖出、分红、送股、费用、负数、千分位、空值和重复检测"],
    },
    "RT-17-005": {
        "resource": "TIMPORTPREVIEWFM",
        "entry": "Pluxee Card -> 操作 -> 导入 -> 从文件导入",
        "steps": ["选择最小 CSV", "观察原始数据", "观察准备导入的记录", "关闭取消", "重开核对无测试交易"],
        "states": [
            ("原始数据", "原样显示日期、流入、流出、活动类型和备注。", [shot("b17-import-preview-original-data.png")]),
            ("准备导入", "自动映射为一条默认勾选的职业工资流入记录，最终按钮已启用。", [shot("b17-import-preview-raw-data.png")]),
            ("取消后复核", "未执行最终导入；重开后 Pluxee Card 仍为 80 条、余额 95.68。", [shot("b17-reopen-pluxee-no-import.png")]),
        ],
        "commands": [("btnImport", "导入选中的记录", {"enabled": True, "visible": True}, "本轮未触发", None, "关闭预览后没有测试交易写入。", "pending")],
        "data_flow": {
            "inputs": ["CSV 原始列", "自动字段识别", "逐行选择"],
            "reads": ["目标账户和活动类型映射"],
            "writes": ["本轮未确认导入"],
            "derived_results": ["原始行表格", "标准化待导入记录", "默认选择状态"],
            "side_effects": ["仅打开预览就使锁定中的账簿增加 32,768 字节", "关闭预览后未继续变化，重开后没有业务记录残留"],
            "rollback": "预览暂存必须移到账簿外；取消应删除暂存批次且不触碰核心账簿。",
        },
        "evidence": [evidence("file", "artifacts/runtime-validation/import-samples/current-account-preview.csv", "最小 CSV 样本。"), evidence("screenshot", shot("b17-import-preview-original-data.png"), "原始数据页。"), evidence("screenshot", shot("b17-import-preview-raw-data.png"), "准备导入记录页。"), evidence("screenshot", shot("b17-reopen-pluxee-no-import.png"), "取消后重开复核。"), evidence("manual_note", NOTES, "预览阶段文件副作用。")],
        "requirements": ["原始行和标准化记录必须分层保存。", "字段映射和逐行错误必须在最终提交前可审阅。", "预览和取消不得修改账簿文件。"],
        "summary": "已验证 CSV 原始数据、自动映射、选择提交界面和取消后无业务记录；发现预览阶段修改账簿文件的缺陷。",
        "gaps": ["字段修正、部分错误、取消选择和成功提交", "XLS/XLSX/HTML/TXT 的边界样本"],
    },
    "RT-17-006": {
        "resource": "TIMPORTSELECTDLGFM",
        "entry": "Pluxee Card -> 操作 -> 导入",
        "steps": ["打开来源选择器", "观察内置来源", "打开通用文件选择器", "记录文件筛选器"],
        "states": [("来源选择", "显示支付宝、财付通、多家银行、随手记和挖财；从剪贴板导入初始禁用。", [shot("b17-import-source-selector.png")]), ("文件选择", "支持 csv、xls、xlsx、htm、html 和 txt。", [shot("b17-import-file-dialog.png")])],
        "commands": [
            ("btnImport", "从文件导入", {"enabled": True, "visible": True}, "打开系统文件选择器", None, "成功进入受支持文件选择。", "pass"),
            ("btnImportFromClipboard", "从剪贴板导入", {"enabled": False, "visible": True}, "未触发", None, "需要有效剪贴板内容或来源状态才能启用。", "partial"),
        ],
        "data_flow": {
            "inputs": ["内置来源类型", "文件路径", "可选剪贴板内容"],
            "reads": ["外部文件或剪贴板原始数据"],
            "writes": ["选择来源本身不写账簿"],
            "derived_results": ["来源适配器选择", "文件类型约束"],
            "side_effects": ["文件选择器默认打开测试账簿所在目录"],
            "rollback": "取消来源或文件选择必须无业务和文件副作用。",
        },
        "evidence": [evidence("screenshot", shot("b17-import-source-selector.png"), "导入来源选择器。"), evidence("screenshot", shot("b17-import-file-dialog.png"), "通用文件筛选器。"), evidence("manual_note", NOTES, "来源和格式说明。")],
        "requirements": ["每个来源通过独立适配器输出统一原始行模型。", "文件和剪贴板共用解析、校验和预览流水线。", "来源选择、文件取消和格式不支持必须返回可区分结果。"],
        "summary": "已验证通用导入来源选择器、内置来源、剪贴板初始状态和六类文件扩展名。",
        "gaps": ["各银行专用解析器的真实样本", "剪贴板启用条件和 HTML/._clip 合同"],
    },
    "RT-17-007": {
        "resource": "TIMPORTTHEMEDLGFM",
        "entry": "标签 -> 选择标签 -> 操作 -> 导入记录到标签",
        "steps": ["确认无标签时命令禁用", "创建临时标签", "打开标签数据设置", "执行默认查询", "关闭并删除临时标签", "重开确认标签为空"],
        "states": [
            ("空状态", "测试库无标签，导入记录到标签命令禁用。", [shot("b17-tag-page.png")]),
            ("查询条件", "筛选支持日期、资产、活动类型、关键字、标签和金额。", [shot("b17-theme-data-filter.png")]),
            ("查询结果", "结果列为日期、活动类型、流入、流出、币种、资金账户/款项、标签和备注。", [shot("b17-theme-data-results.png")]),
            ("清理复核", "未点击设置，临时标签删除，重开后标签页为空。", [shot("b17-temporary-tag-deleted.png"), shot("b17-reopen-tags-empty.png")]),
        ],
        "commands": [
            ("btnFilter", "查询记录", {"enabled": True, "visible": True}, "按默认条件查询", None, "成功加载账簿交易候选。", "pass"),
            ("btnSaveExit", "设置", {"enabled": True, "visible": True}, "本轮未触发", None, "没有给交易写入临时标签。", "pending"),
        ],
        "data_flow": {
            "inputs": ["目标标签", "日期", "资产", "活动类型", "关键字", "现有标签", "金额范围", "候选记录选择"],
            "reads": ["账簿交易及其分类、账户、币种、标签和备注"],
            "writes": ["确认设置后批量更新交易标签关系；本轮未执行"],
            "derived_results": ["筛选后的可选交易列表"],
            "side_effects": ["临时标签创建后删除", "重开确认没有标签残留"],
            "rollback": "批量设置标签必须单事务更新关系；取消和删除临时标签后不得留下孤立关联。",
        },
        "evidence": [evidence("screenshot", shot("b17-theme-data-settings.png"), "标签数据设置初始页。"), evidence("screenshot", shot("b17-theme-data-filter.png"), "查询筛选。"), evidence("screenshot", shot("b17-theme-data-results.png"), "交易候选结果。"), evidence("screenshot", shot("b17-reopen-tags-empty.png"), "删除后重开复核。"), evidence("manual_note", NOTES, "临时标签清理时间线。")],
        "requirements": ["无目标标签时写入命令必须禁用。", "候选查询与最终关系写入分离。", "批量标签更新必须原子提交并保护已有多标签关系。"],
        "summary": "已验证标签批量设置入口、筛选、结果字段、命令状态和临时标签完整清理。",
        "gaps": ["多选、已有标签合并或覆盖语义", "成功设置、撤销、失败回滚和报表联动"],
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
            "reachable": True,
            "unreachable_reason": None,
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
        output_path = OUTPUT_DIR / f"{execution_id}-20260730T011649+0800.json"
        output_path.write_text(
            json.dumps(build_record(execution_id, spec), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"generated {len(RECORDS)} B17 records")


if __name__ == "__main__":
    main()
