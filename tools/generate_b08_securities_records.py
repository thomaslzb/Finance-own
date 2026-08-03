"""生成 B08 上市证券页面的结构化动态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T09:11:56+08:00"
STAMP = "20260730T091156+0800"
LEDGER = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
SHA = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
BACKUP = "artifacts/runtime-validation/backups/test-before-b08-securities-20260730.mh8"
NOTES = "artifacts/runtime-validation/B08-securities-notes.md"
CONTRACT = "docs/runtime-securities-ledger-and-valuation-contract.md"
STATIC_CATALOG = "docs/runtime-dfm-control-catalog.md"
COMPOSITION = "docs/runtime-form-composition-evidence.md"

COMMON_REQUIREMENTS = [
    "证券、账户、交易、持仓、行情和费率使用稳定 ID，证券代码不能作为跨表主键。",
    "交易事实、资金分录、持仓批次、费用和公司行为关系必须原子提交。",
    "持仓列表、市值构成、历史盈亏、导出和打印必须绑定同一账簿与估值快照。",
    "未用真实样例校准前，不得把费率舍入、成本分配、新股关联或代码迁移标记为已兼容。",
]


def shot(name: str) -> str:
    """返回 B08 截图的仓库相对路径。"""
    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(path: str, description: str, kind: str = "screenshot") -> dict:
    """创建结构化证据条目。"""
    return {"kind": kind, "path": path, "description": description}


def state(name: str, status: str, observations: str, *paths: str) -> dict:
    """创建页面状态，并仅附加真实存在的证据路径。"""
    item = {"name": name, "status": status, "observations": observations}
    if paths:
        item["evidence_paths"] = list(paths)
    return item


def command(label: str, trigger: str, outcome: str, status: str = "pass") -> dict:
    """创建命令观察；pass 只代表入口与可见结果已确认。"""
    return {
        "component": "页面命令区",
        "label": label,
        "initial_state": {"enabled": status != "disabled", "visible": True},
        "trigger": trigger,
        "confirmation": None,
        "outcome": outcome,
        "status": "pass" if status == "disabled" else status,
    }


def flow(inputs: list[str], reads: list[str], writes: list[str], derived: list[str], rollback: str) -> dict:
    """创建证券领域的数据流说明。"""
    return {
        "inputs": inputs,
        "reads": reads,
        "writes": writes,
        "derived_results": derived,
        "side_effects": ["本轮未提交业务保存；专用进程退出后已从 B08 前备份恢复账簿。"],
        "rollback": rollback,
    }


def record(
    execution_id: str,
    resource: str,
    entry_point: str,
    states: list[dict],
    commands: list[dict],
    data_flow: dict,
    evidence_items: list[dict],
    summary: str,
    gaps: list[str],
    requirements: list[str] | None = None,
    reachable: bool = True,
    unreachable_reason: str | None = None,
) -> dict:
    """组装符合运行观察 Schema 的 B08 记录。"""
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
            "path": LEDGER,
            "sha256_before": SHA,
            "sha256_after": SHA,
            "backup_artifact": BACKUP,
        },
        "navigation": {
            "entry_point": entry_point,
            "steps": [
                "仅在 PID 34568 的专用 MoneyHome8 实例中打开证券页面",
                "观察字段、菜单、页签、列表、汇总和禁用状态",
                "在保存或向导完成前取消，不提交业务写入",
                "正常退出并保存退出态证据，再恢复 B08 前账簿指纹",
            ],
            "reachable": reachable,
            "unreachable_reason": unreachable_reason,
        },
        "states": states,
        "commands": commands,
        "data_flow": data_flow,
        "evidence": [
            evidence(NOTES, "B08 动态时间线、进程隔离、脱敏规则和账簿恢复证据。", "manual_note"),
            evidence(CONTRACT, "Rust 证券身份、账户、费率、交易、持仓和估值合同。", "manual_note"),
            *evidence_items,
        ],
        "requirements_update": COMMON_REQUIREMENTS + (requirements or []),
        "result": {"status": "partial", "summary": summary, "remaining_gaps": gaps},
    }


def new_records() -> list[dict]:
    """返回本轮新增或直接补证的十四条证券资源记录。"""
    workspace = shot("b08-security-workspace-sanitized.png")
    return [
        record(
            "RT-08-001", "TACCOUNTFEESETFM", "证券持仓上下文 -> 费率设置（当前运行态隐藏）",
            [
                state("账户级结构", "observed", "DFM 确认 A 股、B 股费率表及确定命令；全局页动态确认相同费率字段。", shot("b08-security-fee-settings.png"), STATIC_CATALOG),
                state("直接入口", "pending", "当前证券账户的运行态菜单隐藏费率设置，未直接打开账户级窗体。", shot("b08-security-grid-context-menu.png")),
            ],
            [command("确定", "本轮未直接触发", "账户级保存仍待有可见入口的账户上下文验证。", "pending")],
            flow(["证券账户", "A/B 股分项费率"], ["账户现有费率和创建时模板版本"], ["目标保存应写入账户级版本化费率表"], ["账户交易适用费率"], "账户费率更新必须整体校验并原子替换，不能部分覆盖。"),
            [evidence(shot("b08-security-fee-settings.png"), "动态全局费率字段与 A/B 股分表。"), evidence(STATIC_CATALOG, "账户级费率窗体结构。", "manual_note")],
            "已确认账户级费率结构及其与全局模板的边界，但当前账户未直接到达该窗体。",
            ["直接打开账户级费率页", "保存、覆盖优先级和历史交易不回算", "非法费率与回滚"],
            ["全局模板只在创建账户时复制，账户级费率后续独立版本化。"], False, "当前账户运行态隐藏费率设置菜单。",
        ),
        record(
            "RT-08-002", "TEDITSECURITYFM", "数据管理 -> 上市证券 -> 添加股票",
            [state("初始字段", "observed", "字段为代码、名称、证券类型和锁定名称，默认类型为深圳股票。", shot("b08-security-editor.png")), state("保存", "pending", "重复代码、名称锁定、市场校验和真实保存未执行。")],
            [command("添加股票", "点击证券资料页添加股票", "打开 TEditSecurityFm。"), command("保存", "本轮关闭未保存", "保存边界待验证。", "pending")],
            flow(["证券代码", "名称", "类型", "名称锁定"], ["现有证券代码和别名"], ["目标保存应新增或更新稳定证券目录项"], ["市场内代码唯一性", "可选显示名称"], "目录项、代码别名和审计事件必须原子提交。"),
            [evidence(shot("b08-security-editor.png"), "证券资料编辑器。")], "已动态到达证券资料编辑器并确认核心字段。", ["新增、修改和删除保存", "重复代码和锁名规则", "被交易引用时的删除限制"],
        ),
        record(
            "RT-08-003", "TEDITSECURITYPRICEFM", "证券工作区 -> 操作 -> 添加股票价格",
            [state("初始字段", "observed", "字段为证券、日期和价格，日期默认上一交易日，价格默认四位小数。", shot("b08-security-price-dialog.png")), state("保存", "pending", "重复日期价格、零值和覆盖策略未验证。")],
            [command("添加股票价格", "从证券工作区操作菜单进入", "打开 TEditSecurityPriceFm。"), command("保存", "本轮关闭未保存", "行情发布待验证。", "pending")],
            flow(["证券", "价格日期", "收盘价"], ["证券目录和既有行情"], ["目标保存应写入版本化行情观察"], ["持仓市值", "浮动盈亏", "收益率"], "价格写入和估值批次发布必须可回滚，失败时保留最后成功批次。"),
            [evidence(shot("b08-security-price-dialog.png"), "单证券价格编辑器。")], "已确认手工价格入口、字段和取消边界。", ["重复价格覆盖", "停牌、零价和非法日期", "保存后估值刷新"],
        ),
        record(
            "RT-08-004", "TFEESETFORM", "应用菜单 -> 数据管理 -> 证券费率",
            [state("全局模板", "observed", "页面明确说明只影响新建账户，不回写已有账户。", shot("b08-security-fee-settings.png")), state("A/B 股字段", "observed", "表格包含印花税、佣金、最低佣金、附加费、过户费、结算费和交易规费。", shot("b08-security-fee-settings.png")), state("单元格编辑", "observed", "点击费率单元格进入内联计算编辑器，操作菜单含更新费率、导出和打印。", shot("b08-security-fee-operation-menu.png"))],
            [command("更新费率", "本轮只进入内联编辑后取消", "真实模板更新未提交。", "pending"), command("导出、打印", "展开操作菜单", "命令可见，输出内容未验证。", "pending")],
            flow(["市场和证券类型", "分项费率", "最低费用和上限"], ["当前全局模板版本"], ["目标保存应新增全局模板版本"], ["新账户初始费率表"], "整张模板表校验通过后一次发布，不能让新账户读取半更新状态。"),
            [evidence(shot("b08-security-fee-settings.png"), "全局证券费率页。"), evidence(shot("b08-security-fee-operation-menu.png"), "费率操作菜单。")], "已动态确认全局费率模板、A/B 股分项字段和只影响新账户的继承规则。", ["真实更新和校验", "舍入与单位", "导出和打印"],
        ),
        record(
            "RT-08-005", "TNEWACCTWIZARDSECURITYDLGFM", "账户中心 -> 新增账户 -> 上市证券",
            [state("第一页", "observed", "账户名称、证券类型、锁定币种、所有者、备注和账户组。", shot("b08-security-account-wizard-page1.png")), state("第二页", "observed", "日期及自有余额或其它资金账户来源。", shot("b08-security-account-wizard-page2.png")), state("完成", "pending", "本轮在完成前取消，没有创建账户。")],
            [command("下一步", "完成第一页后进入第二页", "显示资金来源与完成命令。"), command("完成", "本轮未触发", "账户、初始资金和费率复制待验证。", "pending")],
            flow(["账户资料", "证券类型和币种", "初始资金来源"], ["账户组、所有者、资金账户和全局费率模板"], ["目标完成应创建证券账户、资金事件和账户费率副本"], ["账户初始余额", "导航投影"], "账户、初始资金和费率副本必须同事务创建。"),
            [evidence(shot("b08-security-account-wizard-page1.png"), "证券账户向导第一页。"), evidence(shot("b08-security-account-wizard-page2.png"), "证券账户向导第二页。")], "已验证证券账户向导两页字段和资金来源分支，未完成创建。", ["真实创建与删除", "类型到币种规则", "其它账户转入和费率复制"],
        ),
        record(
            "RT-08-006", "TRELATIONNEWSTOCKRECORDSDLGFM", "新股申购记录上下文 -> 关联新股申购记录",
            [state("静态结构", "observed", "DFM 确认申购记录、中签记录、退款记录和确定命令。", STATIC_CATALOG), state("动态前置条件", "pending", "当前账簿没有可同时关联的申购、中签和退款样例，未直接打开。")],
            [command("确定", "本轮未直接触发", "关系保存和校验待真实新股记录组合验证。", "pending")],
            flow(["申购记录", "中签记录", "退款记录"], ["三类新股事件及未关联状态"], ["目标保存应写入稳定的新股流程关系"], ["申购冻结资金、中签成本和退款闭环"], "关系、资金冻结释放和持仓形成必须保持一致，不能只保存界面行号。"),
            [evidence(STATIC_CATALOG, "新股记录关联窗体字段。", "manual_note")], "已确认新股三记录关联结构，但当前账簿不具备直接触发前置数据。", ["直接入口", "部分中签与退款", "重复关联、取消和回滚"], None, False, "缺少可关联的新股申购、中签和退款记录组合。",
        ),
        record(
            "RT-08-007", "TSECURITYACCTDLGFM", "证券账户概况 -> 修改账户概况",
            [state("账户字段", "observed", "账户名称、所有者、类型、创建日期、币种、备注、深沪北股东代码、机构和默认资金账户可见。", shot("b08-security-account-editor-sanitized.png")), state("保存", "pending", "本轮关闭未修改账户。")],
            [command("修改账户概况", "从账户概况进入", "打开 TSecurityAcctDlgFm。"), command("确定", "本轮未触发", "真实账户修改待验证。", "pending")],
            flow(["账户资料", "股东代码", "开户机构", "默认资金账户"], ["当前账户和引用关系"], ["目标保存应更新账户聚合并写审计事件"], ["账户概况和交易默认值"], "账户更新与默认资金关系必须原子提交，已存在交易的币种和类型不得静默改写。"),
            [evidence(shot("b08-security-account-editor-sanitized.png"), "脱敏后的证券账户编辑器。")], "已动态确认证券账户编辑器及主要业务字段。", ["真实修改", "账户类型和币种变更限制", "默认资金账户失效处理"],
        ),
        record(
            "RT-08-008", "TSECURITYCODECONVERTFM", "证券工作区 -> 操作 -> 证券代码变更",
            [state("初始字段", "observed", "源证券或申购代码映射到上市代码，并提供帮助和确定。", shot("b08-security-code-convert-dialog.png")), state("迁移", "pending", "本轮未提交代码变更。")],
            [command("证券代码变更", "从工作区操作菜单进入", "打开 TSecurityCodeConvertFm。"), command("确定", "本轮未触发", "引用迁移待验证。", "pending")],
            flow(["源证券 ID", "目标市场代码", "生效日期"], ["代码历史、交易、持仓、行情和新股关系"], ["目标保存应新增代码变更事件或别名有效期"], ["当前显示代码和检索别名"], "代码变更必须保持稳定证券 ID，并原子校验冲突和引用一致性。"),
            [evidence(shot("b08-security-code-convert-dialog.png"), "证券代码变更对话框。")], "已确认代码变更入口和源代码到上市代码的映射结构。", ["真实迁移", "目标代码冲突", "历史交易、行情和报表兼容"],
        ),
        record(
            "RT-08-009", "TSECURITYLISTFM", "应用菜单 -> 数据管理 -> 上市证券",
            [state("证券目录", "observed", "目录显示代码、名称、类型、搜索、添加股票和操作菜单。", shot("b08-master-data-dialog.png")), state("价格目录", "observed", "价格列表显示日期、代码、名称、价格，并支持添加价格和按日查看。", shot("b08-master-data-dialog.png")), state("写入与删除", "pending", "新增、修改、删除、价格清理和输出未真实执行。")],
            [command("添加股票", "点击证券资料页按钮", "打开证券编辑器。"), command("添加价格", "页面入口可见", "价格保存未执行。", "pending"), command("导出、打印", "静态和菜单证据确认", "输出待验证。", "pending")],
            flow(["证券类别和搜索条件", "证券资料", "历史价格"], ["证券目录、别名和行情"], ["目标命令可维护目录和行情事实"], ["候选证券、价格查询和交易选择"], "被交易引用的证券不得物理删除；目录和行情更新分别使用明确事务。"),
            [evidence(shot("b08-master-data-dialog.png"), "证券资料与价格双列表。")], "已动态确认证券资料目录、分类导航、搜索及历史价格维护区域。", ["修改和删除限制", "价格清理与重复规则", "导出和打印"],
        ),
        record(
            "RT-08-010", "TSECURITYSTATISTICFRAME", "证券账户 -> 持仓统计上半区",
            [state("持仓列", "observed", "动态列包含数量、成本、市值、占比、浮动和交易盈亏、均价、保本价、收盘价及收益率。", workspace), state("合计公式", "observed", "成本 16,424.30、市值 15,860.00、浮动盈亏 -564.30 精确相符。", workspace), state("范围与右键菜单", "observed", "支持当前持仓或所有交易过的证券；右键可调整持仓、变更代码和添加价格。", shot("b08-security-grid-context-menu.png"))],
            [command("当前持仓证券", "展开范围菜单", "可切换到所有交易过的证券。"), command("获取收盘价", "入口可见但本轮未联网更新", "批次更新待 B18 与后续异常验证。", "pending")],
            flow(["账户", "证券范围", "估值快照"], ["持仓批次、行情、费用和关闭分配"], [], ["持仓成本、市值、浮动盈亏、交易盈亏、均价、保本价和收益率"], "查询失败保留最后成功快照；所有行与页脚必须来自同一版本。"),
            [evidence(workspace, "脱敏后的证券持仓统计与合计。"), evidence(shot("b08-security-grid-context-menu.png"), "持仓右键菜单。")], "已动态确认证券持仓统计 Frame、范围菜单、主要列和合计公式。", ["缺行情和跨币种", "保本价与交易盈亏公式", "在线更新与并发快照"],
        ),
        record(
            "RT-08-011", "TSECURITYTRANSFM", "账户中心 -> 上市证券账户",
            [state("组合宿主", "observed", "宿主动态组合持仓统计、交易明细、市值构成和历史盈亏。", workspace, COMPOSITION), state("顶部操作", "observed", "操作包含余额调整、持仓调整、代码变更、添加价格、账户资料、导出、打印和设为首页。", shot("b08-security-top-operation-menu.png")), state("输出", "pending", "有数据导出和打印未执行。")],
            [command("查看账户资料", "从顶部操作菜单进入", "打开账户概况及 TStockViewFrame。"), command("导出、打印", "菜单可见", "输出内容和快照一致性待验证。", "pending")],
            flow(["证券账户", "页签和查询范围"], ["账户、交易、持仓、行情、费率和标签"], [], ["统一证券工作区状态"], "任一子查询失败不得发布互相不一致的列表、图表和页脚。"),
            [evidence(workspace, "证券工作区宿主。"), evidence(shot("b08-security-top-operation-menu.png"), "工作区顶部操作菜单。")], "已动态确认证券工作区及其统计、交易、构成、盈亏和账户概况入口。", ["导出和打印", "异常和空账户", "页签间快照版本显示"],
        ),
        record(
            "RT-08-012", "TSECURITYTRANSFRAME", "证券工作区 -> 交易明细",
            [state("交易列", "observed", "显示日期、证券名称、价格、数量、佣金、总费用、交易金额、活动类型、标签、余额和备注。", workspace), state("筛选", "observed", "支持记账、证券范围、日期范围、查找和操作。", workspace), state("行操作", "pending", "修改、删除、附件、导出和打印未逐项验证。")],
            [command("记账", "交易明细工具栏入口可见", "进入证券交易命令集合。"), command("查找", "入口可见", "筛选条件和结果保持语义待验证。", "pending")],
            flow(["账户", "证券范围", "日期范围", "搜索条件"], ["已提交证券交易、费用、标签和账户余额投影"], [], ["交易明细行、流入流出和记录数"], "查询和输出只读；删除或修改必须调用领域命令并重建相关持仓。"),
            [evidence(workspace, "脱敏后的证券交易明细。")], "已确认交易明细 Frame 的真实列、工具栏和有数据状态。", ["行级修改删除", "附件、导出和打印", "分页、排序和大数据量"],
        ),
        record(
            "RT-08-013", "TSELECTSECURITIESCODEDLGFM", "证券交易编辑器 -> 选择证券",
            [state("静态结构", "observed", "DFM 确认证券候选、确定和更新证券命令。", STATIC_CATALOG), state("动态探测", "pending", "买入页点击更新代码实际进入在线行情页，未直接触发选择证券对话框。", shot("b08-security-buy-code-dropdown.png"))],
            [command("更新证券", "买入页点击更新代码", "本轮进入在线行情页，不足以证明选择对话框运行态。", "pending"), command("确定", "未直接触发", "返回值和取消语义待验证。", "pending")],
            flow(["账户、市场和搜索条件"], ["可交易证券目录和最新代码别名"], [], ["返回稳定 SecurityId 和显示代码"], "选择器不写业务事实；更新失败时保留原候选列表和用户输入。"),
            [evidence(shot("b08-security-buy-code-dropdown.png"), "买入页证券代码控件探测。"), evidence(STATIC_CATALOG, "选择证券窗体结构。", "manual_note")], "已确认选择器静态结构及父流程，但未直接到达独立对话框。", ["直接入口", "候选过滤和返回值", "在线更新后的列表刷新"], None, False, "当前父流程直接使用代码控件并把更新命令路由到在线行情页。",
        ),
        record(
            "RT-08-021", "TSTOCKVIEWFRAME", "证券账户 -> 操作 -> 查看账户资料",
            [state("动态宿主", "observed", "TAccountOverviewDlgFm 内动态加载 TStockViewFrame。", shot("b08-security-account-overview-sanitized.png")), state("概况字段", "observed", "显示账户组、标签、附件、证券类型、机构、股东代码、托管银行、联系方式和密码查看入口。", shot("b08-security-account-overview-sanitized.png"))],
            [command("修改账户概况", "点击概况页链接", "打开 TSecurityAcctDlgFm。")],
            flow(["证券账户 ID"], ["账户聚合、分组、标签、附件和机构资料"], [], ["只读证券账户概况"], "概况查询失败不得修改账户；敏感字段按权限按需读取并避免进入日志。"),
            [evidence(shot("b08-security-account-overview-sanitized.png"), "脱敏后的证券账户概况 Frame。")], "已动态确认 TStockViewFrame 的最终宿主、字段和账户编辑入口。", ["密码查看权限和审计", "附件增删", "空字段和已关闭账户"],
        ),
    ]


def updated_existing_records() -> list[dict]:
    """保留 014-020 的既有交易表单观察，并统一到 B08 最终账簿边界。"""
    updated = []
    for number in range(14, 21):
        execution_id = f"RT-08-{number:03d}"
        candidates = sorted(OUTPUT.glob(f"{execution_id}-*.json"))
        if not candidates:
            raise FileNotFoundError(f"缺少既有观察记录：{execution_id}")
        item = json.loads(candidates[-1].read_text(encoding="utf-8"))
        item["observed_at"] = OBSERVED_AT
        item["ledger"] = {
            "path": LEDGER,
            "sha256_before": SHA,
            "sha256_after": SHA,
            "backup_artifact": BACKUP,
        }
        item["evidence"] = [
            evidence(NOTES, "B08 最终进程隔离、账簿恢复和综合证券页面观察。", "manual_note"),
            evidence(CONTRACT, "Rust 证券交易、费率、持仓和公司行为合同。", "manual_note"),
            *[entry for entry in item.get("evidence", []) if entry.get("path") not in {NOTES, CONTRACT}],
        ]
        existing_requirements = item.get("requirements_update", [])
        item["requirements_update"] = list(dict.fromkeys(COMMON_REQUIREMENTS + existing_requirements))
        item["result"]["status"] = "partial"
        updated.append(item)
    return updated


def main() -> None:
    """写出 B08 全部二十一条最新记录。"""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    items = new_records() + updated_existing_records()
    items.sort(key=lambda item: item["execution_id"])
    if len(items) != 21:
        raise RuntimeError(f"B08 记录数量错误：{len(items)}")
    for item in items:
        path = OUTPUT / f"{item['execution_id']}-{STAMP}.json"
        path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"B08 观察记录生成完成：{len(items)} 条")


if __name__ == "__main__":
    main()
