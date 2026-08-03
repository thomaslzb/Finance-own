"""提取 MoneyHome8 数据交换、备份、附件与同步窗体证据。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = WORKSPACE / "docs" / "runtime-dfm-all-forms.json"
DEFAULT_JSON_OUTPUT = WORKSPACE / "docs" / "runtime-data-exchange-evidence.json"
DEFAULT_MARKDOWN_OUTPUT = (
    WORKSPACE / "docs" / "data-exchange-and-persistence-contract.md"
)
FOCUS_FORMS = {
    "TACCESSORIESDLG": "附件",
    "TBACKUPBOOKFM": "备份",
    "TRESTOREBOOKFM": "还原",
    "TEXPORTDATAFM": "整账簿数据导出",
    "TIMPORTDATAFM": "整账簿数据导入",
    "TIMPORTSELECTDLGFM": "导入来源选择",
    "TIMPORTPREVIEWFM": "导入预览",
    "TIMPORTJIAOGEDANDLGFM": "股票交割单导入",
    "TSYNCUSERDATAFM": "同步",
    "TSYNCUSERREGISTERFM": "同步账号注册",
    "TSYSTEMSETTINGSFM": "备份与同步设置",
    "TMAINFORM": "入口命令",
    "TCREDITCARDSTATISTICFRAME": "信用卡账单导入",
    "TREPORTFM": "报表导出",
    "TWASTEBOOKFM": "财务记录导出与附件入口",
}
EVENT_PROPERTIES = (
    "OnClick",
    "OnExecute",
    "OnDblClick",
    "OnChange",
    "OnSelect",
    "OnKeyDown",
    "OnShow",
    "OnClose",
)
EVIDENCE_PROPERTIES = (
    "Caption",
    "Hint",
    "Text",
    "Items.Strings",
    "Lines.Strings",
    "FieldName",
    "DataField",
    "DefaultExt",
    "Filter",
    "FileName",
    "Enabled",
    "Visible",
    "Checked",
    "ReadOnly",
    "Tag",
    *EVENT_PROPERTIES,
)


def iter_nodes(
    root: dict[str, Any],
    ancestors: tuple[dict[str, Any], ...] = (),
) -> Iterable[tuple[dict[str, Any], tuple[dict[str, Any], ...]]]:
    """深度优先遍历控件树，并保留父级路径用于识别字段分组。"""

    yield root, ancestors
    next_ancestors = (*ancestors, root)
    for child in root.get("children", []):
        yield from iter_nodes(child, next_ancestors)


def node_path(
    node: dict[str, Any], ancestors: tuple[dict[str, Any], ...]
) -> str:
    names = [str(item.get("name", "")) for item in ancestors]
    names.append(str(node.get("name", "")))
    return "/".join(name for name in names if name)


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(flatten_strings(item))
        return result
    return []


def unique_strings(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = " ".join(value.replace("\r", " ").replace("\n", " ").split())
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def extract_form(resource: str, root: dict[str, Any]) -> dict[str, Any]:
    controls: list[dict[str, Any]] = []
    for node, ancestors in iter_nodes(root):
        properties = node.get("properties", {})
        selected = {
            name: properties[name]
            for name in EVIDENCE_PROPERTIES
            if name in properties
        }
        if not selected:
            continue
        controls.append(
            {
                "component": node.get("name", ""),
                "path": node_path(node, ancestors),
                "class": node.get("class", ""),
                "properties": selected,
            }
        )
    return {
        "resource": resource,
        "domain": FOCUS_FORMS[resource],
        "title": str(root.get("properties", {}).get("Caption", "")),
        "controls": controls,
    }


def controls_for(form: dict[str, Any], path_contains: str = "") -> list[dict[str, Any]]:
    return [
        control
        for control in form["controls"]
        if not path_contains or path_contains.lower() in control["path"].lower()
    ]


def captions(
    form: dict[str, Any],
    path_contains: str = "",
    class_suffixes: tuple[str, ...] = (),
) -> list[str]:
    values: list[str] = []
    for control in controls_for(form, path_contains):
        if class_suffixes and not str(control["class"]).endswith(class_suffixes):
            continue
        values.extend(flatten_strings(control["properties"].get("Caption")))
    return unique_strings(values)


def captions_excluding_components(
    form: dict[str, Any],
    path_contains: str,
    excluded_components: set[str],
) -> list[str]:
    """提取业务选项标题，排除仅用于描述分组的标签组件。"""

    values: list[str] = []
    for control in controls_for(form, path_contains):
        if control["component"] in excluded_components:
            continue
        if not str(control["class"]).endswith("Label"):
            continue
        values.extend(flatten_strings(control["properties"].get("Caption")))
    return unique_strings(values)


def commands(form: dict[str, Any], path_contains: str = "") -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for control in controls_for(form, path_contains):
        properties = control["properties"]
        events = {
            name: properties[name]
            for name in EVENT_PROPERTIES
            if properties.get(name)
        }
        if not events:
            continue
        labels = flatten_strings(properties.get("Caption"))
        result.append(
            {
                "component": control["component"],
                "path": control["path"],
                "class": control["class"],
                "label": labels[0] if labels else control["component"],
                "events": events,
                "state": {
                    name: properties[name]
                    for name in ("Enabled", "Visible", "Checked", "ReadOnly")
                    if name in properties
                },
            }
        )
    return result


def option_controls(form: dict[str, Any], path_contains: str = "") -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for control in controls_for(form, path_contains):
        if not str(control["class"]).endswith(("CheckBox", "RadioButton")):
            continue
        labels = flatten_strings(control["properties"].get("Caption"))
        if not labels:
            continue
        result.append(
            {
                "component": control["component"],
                "label": labels[0],
                "checked": bool(control["properties"].get("Checked", False)),
                "visible": control["properties"].get("Visible", True),
                "path": control["path"],
            }
        )
    return result


def find_form(forms: dict[str, dict[str, Any]], resource: str) -> dict[str, Any]:
    return forms[resource]


def build_evidence(data: dict[str, Any], source: Path) -> dict[str, Any]:
    missing = sorted(set(FOCUS_FORMS) - set(data["forms"]))
    if missing:
        raise ValueError(f"缺少重点窗体：{', '.join(missing)}")

    forms = {
        resource: extract_form(resource, data["forms"][resource])
        for resource in FOCUS_FORMS
    }
    export_form = find_form(forms, "TEXPORTDATAFM")
    import_form = find_form(forms, "TIMPORTDATAFM")
    delivery_form = find_form(forms, "TIMPORTJIAOGEDANDLGFM")
    backup_form = find_form(forms, "TBACKUPBOOKFM")
    restore_form = find_form(forms, "TRESTOREBOOKFM")
    attachment_form = find_form(forms, "TACCESSORIESDLG")
    sync_form = find_form(forms, "TSYNCUSERDATAFM")
    settings_form = find_form(forms, "TSYSTEMSETTINGSFM")

    export_datasets = [
        item["label"] for item in option_controls(export_form, "tsOptions")
    ]
    import_datasets = [
        item["label"] for item in option_controls(import_form, "OptionsGroup")
    ]
    common_datasets = [name for name in export_datasets if name in import_datasets]

    delivery_transaction_types = captions_excluding_components(
        delivery_form,
        "gBoxTransType",
        {"lblTransTypeCaption"},
    )
    delivery_fields = captions_excluding_components(
        delivery_form,
        "gBoxDataCol",
        {"lblDataColCaption"},
    )
    delivery_options = option_controls(delivery_form)

    backup_extensions = unique_strings(
        caption
        for control in backup_form["controls"]
        for caption in flatten_strings(control["properties"].get("Caption"))
        if caption.startswith(".")
    )
    attachment_descriptions = unique_strings(
        caption
        for control in attachment_form["controls"]
        for caption in flatten_strings(control["properties"].get("Caption"))
        if len(caption) >= 20
    )
    sync_descriptions = unique_strings(
        caption
        for control in sync_form["controls"]
        for caption in flatten_strings(control["properties"].get("Caption"))
        if caption.startswith("(")
    )
    backup_options = [
        item
        for item in option_controls(settings_form)
        if "backup" in item["path"].lower()
    ]
    sync_options = [
        item
        for item in option_controls(settings_form)
        if item["component"] == "cbSyncCompress"
    ]
    sync_modes = [
        item
        for item in option_controls(sync_form)
        if item["component"] in {"rbTwoWay", "rbOneWay"}
    ]

    return {
        "source": str(source),
        "evidence_scope": {
            "direct": [
                "窗体标题、控件标题和提示",
                "设计时选中、启用、可见和只读状态",
                "事件处理器名称",
                "整账簿导入导出的可选数据集",
                "交割单分隔符、交易类型、字段映射和预览步骤",
                "备份扩展名、还原覆盖警告、附件路径警告和同步方式说明",
            ],
            "architecture_decisions": [
                "SQLite 是 Rust 版唯一账簿真相源",
                "导入采用批次、预览、逐行校验和幂等提交",
                "备份使用 SQLite 一致性备份机制，不复制活跃数据库文件",
                "附件使用账簿相对路径、内容哈希和独立关系表",
                "同步是可选适配器，不能阻塞本地记账",
            ],
            "not_recovered": [
                "通用导入导出文件的实际扩展名、编码和序列化格式",
                "旧同步服务协议、冲突算法和服务端字段",
                "备份压缩算法、保留数量默认值和文件命名规则",
                "信用卡账单支持的来源格式与字段映射",
                "报表导出的实际文件格式和排版结果",
            ],
        },
        "metrics": {
            "focused_form_count": len(forms),
            "control_evidence_count": sum(
                len(form["controls"]) for form in forms.values()
            ),
            "import_dataset_count": len(import_datasets),
            "export_dataset_count": len(export_datasets),
            "common_dataset_count": len(common_datasets),
            "delivery_transaction_type_count": len(delivery_transaction_types),
            "delivery_field_count": len(delivery_fields),
        },
        "flows": {
            "ledger_data_exchange": {
                "import_datasets": import_datasets,
                "export_datasets": export_datasets,
                "common_datasets": common_datasets,
                "export_only_datasets": [
                    name for name in export_datasets if name not in import_datasets
                ],
                "import_only_datasets": [
                    name for name in import_datasets if name not in export_datasets
                ],
                "export_options": option_controls(export_form, "tsBase"),
                "import_commands": commands(import_form),
                "export_commands": commands(export_form),
                "format_status": "unverified",
            },
            "delivery_note_import": {
                "transaction_types": delivery_transaction_types,
                "mapped_fields": delivery_fields,
                "options": delivery_options,
                "commands": commands(delivery_form),
                "preview_columns": captions(delivery_form, "/ts2/tl1/"),
            },
            "import_preview": {
                "source_commands": commands(forms["TIMPORTSELECTDLGFM"]),
                "preview_commands": commands(forms["TIMPORTPREVIEWFM"]),
                "tabs": captions(forms["TIMPORTPREVIEWFM"], class_suffixes=("TabSheet",)),
            },
            "backup_restore": {
                "backup_extensions": backup_extensions,
                "backup_commands": commands(backup_form),
                "restore_commands": commands(restore_form),
                "restore_warnings": captions(restore_form, "pnlHint"),
                "backup_options": backup_options,
            },
            "attachments": {
                "descriptions": attachment_descriptions,
                "commands": commands(attachment_form),
            },
            "sync": {
                "modes": sync_modes,
                "descriptions": sync_descriptions,
                "commands": commands(sync_form),
                "settings": sync_options,
            },
            "secondary_import_export": {
                "credit_card_statement_commands": commands(
                    forms["TCREDITCARDSTATISTICFRAME"]
                ),
                "report_commands": commands(forms["TREPORTFM"]),
                "ledger_commands": commands(forms["TWASTEBOOKFM"]),
            },
        },
        "forms": list(forms.values()),
    }


def escape_cell(value: Any) -> str:
    if isinstance(value, list):
        value = "；".join(str(item) for item in value)
    return str(value or "").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def build_markdown(evidence: dict[str, Any]) -> str:
    metrics = evidence["metrics"]
    flows = evidence["flows"]
    ledger = flows["ledger_data_exchange"]
    delivery = flows["delivery_note_import"]
    backup = flows["backup_restore"]
    attachments = flows["attachments"]
    sync = flows["sync"]
    lines = [
        "# MoneyHome8 数据交换与持久化开发契约",
        "",
        "本文档由 `runtime-dfm-all-forms.json` 自动生成。它把旧程序的导入、导出、交割单、备份还原、附件和同步证据转换为 Rust + SQLite 的开发边界。",
        "",
        "## 1. 证据结论",
        "",
        f"- 重点窗体：`{metrics['focused_form_count']}` 个",
        f"- 保留控件证据：`{metrics['control_evidence_count']}` 条",
        f"- 整账簿导入数据集：`{metrics['import_dataset_count']}` 类",
        f"- 整账簿导出数据集：`{metrics['export_dataset_count']}` 类",
        f"- 导入导出共有数据集：`{metrics['common_dataset_count']}` 类",
        f"- 交割单交易类型：`{metrics['delivery_transaction_type_count']}` 类",
        f"- 交割单映射字段：`{metrics['delivery_field_count']}` 项",
        "",
        "窗体标题、选项、事件名、初始状态和提示文案属于直接证据。通用交换文件格式、旧同步协议和真实写入结果尚未通过运行操作确认，不能标为兼容完成。",
        "",
        "## 2. 旧程序功能证据",
        "",
        "### 2.1 整账簿导入导出",
        "",
        "导入与导出共同覆盖：",
        "",
        escape_cell(ledger["common_datasets"]),
        "",
        "导出窗体还提供日期范围、账户范围、输出文件名以及“增加 / 删除并覆盖”模式；“导入时更新账户余额”在设计时隐藏。Rust 版不得直接写余额，余额始终由已提交分录计算。",
        "",
        "通用交换文件的扩展名、编码、版本头和内部结构仍未恢复。实现旧格式兼容器前，必须在解锁桌面会话中执行一次最小导出并回导，保存文件样本和结果。",
        "",
        "### 2.2 股票交割单导入",
        "",
        f"- 交易类型：{escape_cell(delivery['transaction_types'])}",
        f"- 映射字段：{escape_cell(delivery['mapped_fields'])}",
        "- 分隔符支持制表符、空格和单个自定义字符，制表符为默认选项，并提供自动识别。",
        "- 字段既可按列头文字匹配，也可按列序号匹配；列头文字为默认模式。",
        "- 金额可声明已包含印花税、佣金、过户费和其它费用，导入器必须避免重复计费。",
        "- 导入前可预览和批量修改交易类型、证券代码、标签，并可关联或取消关联新股申购。",
        "- 匹配方案支持保存与删除，方案必须带版本、来源标识和字段规则，禁止用不可追踪的全局配置覆盖。",
        "",
        "### 2.3 备份、还原与附件",
        "",
        f"- 旧备份窗体直接显示扩展名：{escape_cell(backup['backup_extensions'])}",
        f"- 还原警告：{escape_cell(backup['restore_warnings'])}",
        "- 系统设置支持默认备份目录、保留最近若干份、备份前优化/完整性校验、压缩和打开备份目录。",
        f"- 附件说明：{escape_cell(attachments['descriptions'])}",
        "- 附件可添加、删除、打开并打开所在文件夹；打开和删除在没有有效选择时初始禁用。",
        "",
        "### 2.4 同步与次级交换入口",
        "",
        f"- 同步模式：{escape_cell([item['label'] for item in sync['modes']])}",
        f"- 模式说明：{escape_cell(sync['descriptions'])}",
        "- 双向同步为默认选项；单向上传以本地账簿覆盖远端。支持关闭账簿时自动同步和压缩传输数据。",
        "- 信用卡账单列表存在导入命令；财务记录可导出到文件；报表可另存、导出和打印，其中导出与打印在报表未就绪时初始禁用。",
        "",
        "## 3. Rust + SQLite 开发契约",
        "",
        "### 3.1 导入流水线",
        "",
        "```text",
        "来源文件/粘贴数据 -> 格式识别 -> 原始行暂存 -> 字段映射 -> 规范化预览",
        "-> 逐行校验与去重 -> 用户选择 -> 单批事务提交 -> 结果与错误报告",
        "```",
        "",
        "1. 每次导入创建不可变的 `import_batch`，记录来源哈希、适配器版本、账簿、数据范围、创建时间和最终状态。",
        "2. 每个原始行创建 `import_row`，保留行号、原始文本或结构化载荷、规范化结果、校验错误和提交对象标识，便于重试与审计。",
        "3. 预览只产生候选记录，不修改账户、交易、持仓、预算或提醒。只有明确选择的有效记录才能提交。",
        "4. 幂等键至少包含来源文件哈希、来源行标识和规范化业务指纹；重复导入必须提示并允许跳过，不能静默复制交易。",
        "5. “删除并覆盖”必须明确数据集、账户和日期范围，执行前展示删除数量，创建自动备份，并在一个事务中完成删除与导入。",
        "6. 账户余额、投资市值和报表汇总不得从导入文件直接覆盖；导入写入真相记录后统一重算查询投影。",
        "7. 大批量导入允许分块解析，但一个用户确认批次必须具有明确的整体结果；失败时不得留下无法识别的半批数据。",
        "",
        "### 3.2 交割单映射",
        "",
        "- `import_mapping_profile` 保存来源、分隔符、标题行规则、列匹配模式、交易类型映射、字段映射、金额含费规则和版本。",
        "- 价格、数量、金额和四类费用使用定点十进制解析；空值、负值和千分位规则必须由适配器明确处理。",
        "- 交易资金账户、转账资金账户、证券账户和盈亏归类是批次级必填上下文，不得从不可信文本自动猜测后直接入账。",
        "- 新股申购关联必须引用已存在或同批创建的申购记录；无法匹配时保留为待处理行，不能伪造关联。",
        "- 确认导入时，投资成交、费用、资金分录、证券对象和标签关系在同一数据库事务内提交。",
        "",
        "### 3.3 备份与还原",
        "",
        "- SQLite 处于 WAL 或活动连接状态时，禁止直接复制 `.db` 文件。备份服务使用 SQLite Online Backup API 或 `VACUUM INTO` 生成一致性快照。",
        "- 备份前执行轻量检查；用户选择完整性校验时运行 `PRAGMA integrity_check`，失败则中止并返回可读错误。",
        "- 备份清单记录应用版本、模式版本、创建时间、源账簿标识、文件哈希、大小、压缩方式和附件包含策略。",
        "- 自动保留策略只删除已确认成功且超出数量的旧备份；当前账簿、最新成功备份和还原前备份不得被清理。",
        "- 还原默认创建新账簿。覆盖当前账簿需要二次确认、还原前自动备份、关闭活动连接、校验快照后原子替换。",
        "- `.mh8` 仅作为旧格式兼容扩展名证据；Rust 新备份格式必须有版本清单，不能假定旧 `.mh8` 就是 SQLite 文件。",
        "",
        "### 3.4 附件",
        "",
        "- 附件元数据保存在 `attachments`，业务对象关系保存在独立关联表；原文件位于账簿拥有的附件目录。",
        "- 数据库只保存账簿根目录下的相对路径，同时保存 SHA-256、大小、MIME 类型、原文件名和创建时间，避免旧程序因绝对路径或账簿名变化而失效。",
        "- 添加附件先复制到受管目录并校验哈希，再提交元数据与关系；任一步失败都清理本次临时文件。",
        "- 删除关系与删除物理文件分离。仅当没有任何业务对象引用且回收策略允许时，才删除内容文件。",
        "- 打开附件前校验路径仍位于账簿附件根目录，拒绝路径穿越和外部命令注入。",
        "",
        "### 3.5 同步",
        "",
        "- 本地 SQLite 始终可独立记账；登录、网络或远端服务失败不得阻塞本地写入。",
        "- 双向同步按对象标识、版本和删除墓碑合并；单向上传必须先展示远端将被覆盖的范围并生成本地同步快照。",
        "- 远端字段通过同步映射层转换为领域命令，禁止直接写核心表或直接覆盖计算余额。",
        "- 同步顺序至少为基础资料、账户、交易与分录、投资扩展、标签与附件关系、计划提醒、派生状态；依赖对象未到达时进入待重试队列。",
        "- 每个同步批次记录游标、对象结果、冲突、重试次数和取消状态。取消只停止后续对象，已提交对象必须可审计并可继续同步。",
        "- 旧财智在线服务协议尚未恢复，因此首版把同步定义为适配器接口和本地日志，不宣称兼容旧服务。",
        "",
        "### 3.6 导出与报表",
        "",
        "- 导出读取稳定查询 DTO，不直接拼接领域表；表格、图表、打印和文件导出共享同一结果集及筛选快照。",
        "- 导出文件记录格式版本、时区、基准币种、金额单位和筛选条件，避免重新导入时丢失口径。",
        "- 报表只有在结果状态为 `ready` 时才能导出或打印；筛选变化后立即进入 `dirty`，刷新成功再恢复 `ready`。",
        "- 导出是交换投影，不是账簿真相或备份替代品。",
        "",
        "## 4. 最小数据模型",
        "",
        "| 模型 | 责任 | 关键约束 |",
        "| --- | --- | --- |",
        "| `import_batches` | 一次导入的来源、适配器、范围、状态与统计 | 来源哈希和账簿范围可追踪 |",
        "| `import_rows` | 原始行、规范化候选、错误与提交结果 | 批次内行号唯一；保留失败证据 |",
        "| `import_mapping_profiles` | 可复用交割单和账单映射方案 | 来源 + 名称 + 版本唯一 |",
        "| `backup_manifests` | 备份文件、模式版本、哈希和校验结果 | 只登记成功完成的快照 |",
        "| `attachments` | 受管文件元数据 | 内容哈希可去重；路径必须相对 |",
        "| `transaction_attachments` | 交易与附件多对多关系 | 禁止重复关联 |",
        "| `sync_batches` / `sync_items` | 同步游标、对象结果、冲突和重试 | 本地提交与远端结果分开记录 |",
        "",
        "这些模型是开发契约，不代表旧 `.mh8` 内必然存在同名表。",
        "",
        "## 5. 验收要求",
        "",
        "1. 同一文件连续导入两次，第二次必须识别重复且不新增交易。",
        "2. 含一条错误记录的文件可预览全部行，错误行给出字段级原因，未确认前数据库无变化。",
        "3. 交割单金额标记为含费时，资金分录不会再次扣除同一费用；不含费时四类费用分别可审计。",
        "4. 备份期间并发新增交易，恢复后的数据库通过完整性和外键检查，且只能呈现一个一致时间点的数据。",
        "5. 覆盖还原失败时，原账簿仍可打开，还原前备份存在且哈希可验证。",
        "6. 重命名或移动整个账簿目录后，附件仍可通过相对路径打开；移动单个外部原文件不影响受管副本。",
        "7. 断网时本地记账成功；恢复网络后同步批次能继续，并明确展示冲突与失败对象。",
        "8. 报表筛选变更后导出命令禁用，刷新成功后导出内容与屏幕表格合计一致。",
        "9. 在旧程序中完成最小导出回导、备份还原、交割单导入和附件增删后，才能把相应格式或结果从“待验证”升级为“兼容”。",
        "",
        "## 6. 仍需动态验证",
        "",
        "- 通用账簿数据导入导出的文件扩展名、编码、版本和覆盖范围",
        "- 交割单粘贴内容的标题行、日期、负数、千分位和空值解析规则",
        "- 信用卡账单导入来源、字段和去重方式",
        "- 备份压缩后的实际文件结构、默认保留数量和命名规则",
        "- 附件目录命名、复制或引用行为以及删除最后一个引用后的结果",
        "- 旧同步对象顺序、冲突提示、删除传播和取消后的恢复行为",
        "- 报表和财务记录导出的实际文件格式、列顺序、编码与金额精度",
        "",
    ]
    return "\n".join(lines)


def ensure_workspace_path(path: Path) -> Path:
    resolved = path.resolve()
    if WORKSPACE != resolved and WORKSPACE not in resolved.parents:
        raise SystemExit(f"输出必须位于固定工作区内：{WORKSPACE}")
    return resolved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成数据交换与持久化证据")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = args.input.resolve()
    json_output = ensure_workspace_path(args.json_output)
    markdown_output = ensure_workspace_path(args.markdown_output)
    if not input_path.is_file():
        raise SystemExit(f"DFM JSON 不存在：{input_path}")

    data = json.loads(input_path.read_text(encoding="utf-8"))
    evidence = build_evidence(data, input_path)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    markdown_output.write_text(
        build_markdown(evidence), encoding="utf-8", newline="\n"
    )
    metrics = evidence["metrics"]
    print(
        "已生成数据交换证据："
        f"{metrics['focused_form_count']} 个重点窗体，"
        f"{metrics['common_dataset_count']} 类共有导入导出数据集，"
        f"{metrics['delivery_field_count']} 个交割单映射字段"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
