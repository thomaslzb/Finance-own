"""生成 B19 辅助工具与长尾能力的运行态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T03:12:47+08:00"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "C8315E2B65CA39C57F9C4CB1BFA5D537EAA403BCED60CB4FB298189439E2377D"
FINAL_HASH = "EE62C77052FA558F26A6ABF1439844CC3DB62EFC0375A124339F6222633ACB9D"
BACKUP_ARTIFACT = "artifacts/runtime-validation/backups/test-before-b19.mh8"
NOTES = "artifacts/runtime-validation/B19-tools-longtail-notes.md"


def shot(name: str, *, nested: bool = False) -> str:
    """返回 B19 截图的仓库相对路径。"""

    prefix = "artifacts/runtime-validation/screenshots" if nested else "artifacts/runtime-validation"
    return f"{prefix}/{name}"


def evidence(kind: str, path: str, description: str) -> dict:
    """构造一条可追溯证据。"""

    return {"kind": kind, "path": path, "description": description}


def flow(inputs: list[str], reads: list[str], writes: list[str], results: list[str], effects: list[str], rollback: str) -> dict:
    """统一生成运行记录的数据流结构。"""

    return {
        "inputs": inputs,
        "reads": reads,
        "writes": writes,
        "derived_results": results,
        "side_effects": effects,
        "rollback": rollback,
    }


RECORDS = {
    "RT-19-001": {
        "resource": "TACCESSORIESDLG",
        "entry": "记账 -> 日常收支 -> 查看附件",
        "steps": ["打开日常收支草稿", "点击查看附件", "观察空附件状态", "关闭并取消草稿"],
        "states": [
            ("空附件", "预览区为空；添加可用，删除、打开附件和打开附件文件夹禁用。", [shot("b19-attachments-empty.png", nested=True)]),
        ],
        "commands": [
            ("btnAdd", "添加", True, "未触发文件选择", "未写入附件。", "partial"),
            ("btnDelete", "删除", False, "空列表", "保持禁用。", "pass"),
            ("btnView", "打开附件", False, "空列表", "保持禁用。", "pass"),
            ("btnOpen", "打开附件文件夹", False, "未形成附件目录", "保持禁用。", "pass"),
        ],
        "data_flow": flow(
            ["宿主业务对象", "本地文件选择"],
            ["附件元数据和业务关联"],
            ["受管附件副本、附件元数据和关系；本轮未写入"],
            ["预览、可打开状态和附件数量"],
            ["没有打开文件选择器或外部程序"],
            "父业务草稿取消时不得提交附件关系；文件复制、哈希和关系写入必须作为可补偿事务。",
        ),
        "evidence": [evidence("screenshot", shot("b19-attachments-empty.png", nested=True), "附件管理空态。"), evidence("manual_note", NOTES, "附件动态边界。")],
        "requirements": [
            "附件使用账簿拥有的相对目录、内容哈希和独立关系表。",
            "没有有效选择时删除、打开和打开文件夹必须禁用。",
            "父草稿取消、复制失败或关系提交失败时清理本次临时副本。",
        ],
        "summary": "已从日常收支草稿打开附件管理并确认空态和命令门控。",
        "gaps": ["添加、预览、打开、删除和最后引用解除后的真实文件生命周期", "旧附件目录命名与迁移"],
    },
    "RT-19-002": {
        "resource": "TCALCULATORDLG",
        "entry": "财智8 -> 财务工具 -> 财务计算器",
        "steps": ["打开财务计算器", "展开存款、贷款、证券和其它分类", "观察代表页面", "关闭"],
        "states": [
            ("存款类", "七个存款计算器；首页包含存取日期、金额、利率、计算目标和本息结果。", [shot("b19-financial-calculator.png")]),
            ("贷款类", "八个贷款计算器，含普通贷款、累进还款、提前还款及购房租房比较。", [shot("b19-financial-calculator-loan-menu.png")]),
            ("证券类", "证券目标收益和价格计算器。", [shot("b19-financial-calculator-securities-menu.png")]),
            ("其它类", "个人所得税及两类通货膨胀影响计算器。", [shot("b19-financial-calculator-other-menu.png")]),
        ],
        "commands": [
            ("btnCalculate", "计算", True, "本轮未提交数值", "公式结果待校准。", "partial"),
            ("btnReset", "重置", True, "代表页面可见", "未改变账簿。", "partial"),
        ],
        "data_flow": flow(
            ["日期、金额、利率、期限、税率和计算目标"],
            ["用户输入和计算器内置参数"],
            ["无账簿业务写入"],
            ["19 类计算结果和比较结果"],
            ["页面为本地 WebView/原生树混合界面"],
            "输入错误只影响当前计算草稿；不得写入账户、交易或报表真相。",
        ),
        "evidence": [evidence("screenshot", shot("b19-financial-calculator.png"), "财务计算器存款页。"), evidence("manual_note", NOTES, "19 类计算器目录。")],
        "requirements": [
            "保留 19 类计算能力，但公式、精度、税率口径和日期边界必须逐项校准。",
            "金额统一使用十进制定点类型，计算结果不得直接成为账务分录。",
            "计算器参数与公式版本可追踪，历史政策参数不得静默覆盖。",
        ],
        "summary": "已动态确认四大分类共 19 个财务计算器及代表字段。",
        "gaps": ["19 类公式、舍入、校验失败和边界结果", "本地 HTML 与旧政策参数来源"],
    },
    "RT-19-003": {
        "resource": "TCLEANPRICEFM",
        "entry": "资料管理 -> 贵金属产品 -> 操作 -> 价格整理",
        "steps": ["打开贵金属产品列表", "选择价格整理", "观察范围和删除条件", "直接关闭，不确认"],
        "states": [
            ("价格整理", "可选择股票、基金、贵金属和币种汇率，支持指定日期前、日期区间、未交易对象及历史保留规则。", [shot("b19-price-cleanup.png")]),
        ],
        "commands": [("btnOK", "确定", True, "未触发", "避免广泛删除历史价格。", "partial")],
        "data_flow": flow(
            ["价格类型范围", "截止日期或日期区间", "未交易对象和历史保留选项"],
            ["金融产品、交易引用和历史价格"],
            ["匹配条件的历史价格删除；本轮未执行"],
            ["删除预期范围"],
            ["旧程序建议每 2 至 3 个月整理一次"],
            "先计算并展示影响数量；确认后单事务删除，任何失败整体回滚并保留审计记录。",
        ),
        "evidence": [evidence("screenshot", shot("b19-price-cleanup.png"), "价格整理范围和条件。"), evidence("manual_note", NOTES, "未执行破坏性确认。")],
        "requirements": [
            "价格整理属于高风险维护命令，提交前必须预览数据源、对象数和记录数。",
            "已被交易估值引用的历史价格按明确保留策略处理。",
            "不得默认勾选跨全部价格类型的不可逆删除。",
        ],
        "summary": "已确认价格整理范围和条件，未执行广泛历史价格删除。",
        "gaps": ["各选项默认勾选状态", "预览数量、实际删除、引用保护和回滚"],
    },
    "RT-19-004": {
        "resource": "TCUSTOMERDLGFM",
        "entry": "财智8 -> 帮助 -> 客户服务",
        "steps": ["打开客户服务", "观察联系方式和工作时间", "不点击外部链接", "关闭"],
        "states": [("客户服务", "展示客服/销售邮箱、QQ、微博、网站、微信二维码、FAQ 和周一至周五 9:00-18:00 工作时间。", [shot("b19-customer-service.png")])],
        "commands": [("externalLinks", "邮箱、QQ、微博、网站和 FAQ", True, "未触发", "未启动浏览器或外部通信。", "partial")],
        "data_flow": flow(["用户选择的支持渠道"], ["内置联系方式"], ["无账簿写入"], ["外部支持入口"], ["本轮未打开外部程序"], "外部入口失败不得影响本地账簿。"),
        "evidence": [evidence("screenshot", shot("b19-customer-service.png"), "客户服务页面。")],
        "requirements": ["支持信息应配置化并允许离线查看。", "外链必须使用 HTTPS 并明确提示将离开本地应用。", "不得把账簿数据自动附带到客服请求。"],
        "summary": "已确认客户服务渠道、二维码和工作时间，未触发外链。",
        "gaps": ["各外链当前目标和失效状态", "FAQ 内容"],
    },
    "RT-19-005": {
        "resource": "TDIARYDLGFM",
        "entry": "财智8 -> 财务工具 -> 日记 -> 写日记",
        "steps": ["打开编辑器", "空内容保存校验", "输入测试文本并保存", "从列表删除测试日记"],
        "states": [
            ("编辑器", "日期、字体、字号、粗体、斜体、下划线、对齐、项目符号、颜色、正文和保存均可见。", [shot("b19-diary-editor.png")]),
            ("空值校验", "空内容保存提示请输入日记内容。", [shot("b19-diary-save-message.png")]),
            ("有效草稿", "输入 Codex B19 Diary Probe 2026-07-30 后保存成功。", [shot("b19-diary-editor-filled.png")]),
        ],
        "commands": [("btnSave", "保存", True, "先空值后有效文本", "空值被阻止，有效文本写入列表。", "pass")],
        "data_flow": flow(["日记日期", "富文本内容和格式"], ["当前日记草稿"], ["日记正文和格式"], ["按月归档和日记数量"], ["有效保存时账簿文件增加 4096 字节"], "校验失败不写入；保存应原子提交正文和格式。"),
        "evidence": [evidence("screenshot", shot("b19-diary-editor.png"), "日记富文本编辑器。"), evidence("screenshot", shot("b19-diary-save-message.png"), "空内容校验。"), evidence("manual_note", NOTES, "日记保存与清理时序。")],
        "requirements": ["日记正文为空时阻止保存并定位到编辑区。", "富文本存储必须定义可迁移格式并过滤危险内容。", "保存和列表计数刷新保持一致。"],
        "summary": "已验证日记编辑、空值校验、有效保存和后续清理。",
        "gaps": ["全部富文本格式持久化", "修改、搜索和导出结果"],
    },
    "RT-19-006": {
        "resource": "TDIARYUNTFM",
        "entry": "财智8 -> 财务工具 -> 日记",
        "steps": ["观察空月份", "写入测试日记", "确认计数和列表", "执行删除确认", "确认恢复空月份"],
        "states": [
            ("空月份", "左侧按年和 12 个月导航，2026 年 7 月显示共 0 篇。", [shot("b19-diary-list.png")]),
            ("保存后", "2026 年 7 月显示共 1 篇并出现测试日记。", [shot("b19-diary-after-save.png")]),
            ("删除确认", "删除前提示您确定删除该日记吗？", [shot("b19-diary-delete-confirm.png")]),
            ("删除后", "列表恢复共 0 篇，测试日记不再显示。", [shot("b19-diary-after-delete.png")]),
        ],
        "commands": [
            ("btnWrite", "写日记", True, "打开编辑器", "可达。", "pass"),
            ("miModify", "修改", True, "未触发", "待测。", "partial"),
            ("miDelete", "删除", True, "选中测试日记并确认", "测试日记删除。", "pass"),
            ("miSearch", "搜索", True, "未触发", "待测。", "partial"),
            ("miExport", "导出列表", True, "未触发", "待测。", "partial"),
        ],
        "data_flow": flow(["年份、月份、日记选择"], ["日记索引和正文摘要"], ["删除选中日记"], ["月度计数和列表"], ["逻辑删除后文件长度未立即回退，退出时账簿压缩"], "删除确认后单事务移除日记；取消不写入。"),
        "evidence": [evidence("screenshot", shot("b19-diary-after-save.png"), "保存后的月度列表。"), evidence("screenshot", shot("b19-diary-after-delete.png"), "删除后的空列表。"), evidence("manual_note", NOTES, "日记列表命令和文件变化。")],
        "requirements": ["日记按年月导航并显示准确计数。", "删除必须二次确认且同步刷新列表和计数。", "搜索和导出不得泄漏未选择范围之外的日记。"],
        "summary": "已完成日记列表空态、保存刷新、删除确认和清理闭环。",
        "gaps": ["修改、全部查看、搜索和导出", "跨年月和大量日记性能"],
    },
    "RT-19-007": {
        "resource": "TMANAGEBILLDATEDLGFM",
        "entry": "账户中心 -> 信用卡账户 -> 修改 -> 账单日管理",
        "steps": ["创建零余额临时信用卡", "打开信用卡编辑器", "进入账单日管理", "观察现有规则", "关闭后永久删除临时账户"],
        "states": [("规则列表", "列表按设置日期和账单日展示当前规则：2026-07-30、生效账单日每月 1 号；设置和删除可用。", [shot("b19-manage-bill-date.png", nested=True)])],
        "commands": [("btnModify", "设置", True, "打开设置账单日", "进入 TModifyBillDateDlgFm。", "pass"), ("btnDelete", "删除", True, "未触发规则删除", "随临时信用卡账户永久删除。", "partial")],
        "data_flow": flow(["信用卡账户", "生效日期和账单日规则"], ["信用卡账单日历史"], ["新增、修改或删除规则；本轮只创建账户默认规则后随账户删除"], ["交易归属账期和账单边界"], ["临时账户最终永久删除，账户列表恢复无信用卡数据"], "规则修改与账户配置同事务；账户永久删除按明确级联规则清理。"),
        "evidence": [evidence("screenshot", shot("b19-manage-bill-date.png", nested=True), "账单日历史管理。"), evidence("screenshot", shot("b19-credit-card-after-delete.png", nested=True), "临时信用卡删除后列表。"), evidence("manual_note", NOTES, "临时账户创建与清理。")],
        "requirements": ["账单日规则按生效日期版本化，历史交易使用对应时点规则。", "规则删除前展示受影响账单范围。", "信用卡删除必须明确提示关联收支、转账和计划的级联影响。"],
        "summary": "已通过临时信用卡完整到达账单日管理，并在取证后删除账户。",
        "gaps": ["多条历史规则排序和重叠校验", "删除规则对既有账单的影响"],
    },
    "RT-19-008": {
        "resource": "TMODIFYBILLDATEDLGFM",
        "entry": "账单日管理 -> 设置",
        "steps": ["选中默认规则", "点击设置", "观察两种账单日模式", "关闭取消"],
        "states": [("设置账单日", "字段为生效日期；固定账单日每月 N 日；或每月最后一天是账单日。", [shot("b19-modify-bill-date.png", nested=True)])],
        "commands": [("btnSaveExit", "确定", True, "未触发", "保持原规则。", "partial")],
        "data_flow": flow(["生效日期", "固定日或月末模式"], ["当前和历史账单日规则"], ["新的规则版本；本轮未写入"], ["后续交易的账期边界"], ["关闭取消不改变规则"], "校验日期顺序和规则冲突后原子保存；取消丢弃草稿。"),
        "evidence": [evidence("screenshot", shot("b19-modify-bill-date.png", nested=True), "设置账单日页面。")],
        "requirements": ["账单日支持固定 1 至 31 日和每月最后一天。", "短月份采用明确规则，不能产生无效日期。", "新规则只影响生效日之后的账期，历史结果可重算且可审计。"],
        "summary": "已确认账单日设置的生效日期、固定日和月末两种模式。",
        "gaps": ["短月份行为", "重叠生效日期、过去日期和非法日校验", "实际保存后的账单归属"],
    },
    "RT-19-009": {
        "resource": "TMONTHDAYFM",
        "entry": "作为 TMHDatetimePicker 的共享日期选择支撑组件间接触发",
        "steps": ["在日记和日常收支日期控件尝试按钮与键盘触发", "观察日期字段", "核对静态事件和共享组件证据"],
        "reachable": True,
        "states": [("宿主日期输入", "日常收支和账单日页面均使用 TMHDatetimePicker；本轮未观察到独立顶层 TMonthDayFm。", [shot("b19-income-date-probe.png", nested=True), shot("b19-modify-bill-date.png", nested=True)])],
        "commands": [("mwCalendarPanel", "日期面板", True, "宿主内尝试展开", "未形成独立产品窗口。", "partial")],
        "data_flow": flow(["宿主当前日期和日期选择"], ["日历月份和日期范围"], ["只回填宿主草稿"], ["选定日期"], ["不应独立持久化"], "宿主取消时日期草稿一并丢弃。"),
        "evidence": [evidence("screenshot", shot("b19-income-date-probe.png", nested=True), "普通收支日期宿主。"), evidence("manual_note", NOTES, "共享日期组件的动态触发边界。")],
        "requirements": ["作为统一日期选择组件实现，不进入主导航。", "日期回填只修改宿主草稿。", "键盘、鼠标、月份切换和最小最大日期必须具有一致行为。"],
        "summary": "确认 TMonthDayFm 属于共享日期支撑，不是独立业务页面；独立弹层未动态捕获。",
        "gaps": ["弹层精确触发方式", "月份切换、键盘导航和日期边界"],
    },
    "RT-19-010": {
        "resource": "TSOFTINDEXCENTERFORM",
        "entry": "左侧导航 -> 概况",
        "steps": ["打开概况", "观察异常提示、收支、资产和图表", "检查信用卡、投资和预算区", "打开操作菜单"],
        "states": [("概况", "显示财务异常、7 月收支结余、总资产/负债/净资产、六类图表、信用卡、投资和预算区。", [shot("b19-overview.png")])],
        "commands": [("btnUpdateQuote", "更新行情", True, "未触发", "B18 已单独验证行情页。", "partial"), ("miSort", "调整显示顺序", True, "打开排序窗体", "可达。", "pass"), ("miShowSections", "显示图表/信用卡/投资/预算", True, "观察勾选状态", "四个区块默认显示。", "pass")],
        "data_flow": flow(["统计期间、图表口径、显示区块"], ["交易、账户、负债、投资、预算和行情投影"], ["首页布局偏好"], ["收支、净资产、构成和异常摘要"], ["概况读取多个领域投影"], "布局变更不修改账务真相；投影失败只降级对应区块。"),
        "evidence": [evidence("screenshot", shot("b19-overview.png"), "概况完整页面。"), evidence("manual_note", NOTES, "概况菜单和数据口径。")],
        "requirements": ["概况按统一估值时点聚合收支、资产负债、投资和预算。", "各区块可独立显示隐藏和排序。", "异常提示必须可追溯到具体对象和校验规则。"],
        "summary": "已动态确认概况的核心指标、六类图表和四个可配置区块。",
        "gaps": ["各图表切换和期间结果", "异常详情、预算新增和投资详情", "投影刷新时序"],
    },
    "RT-19-011": {
        "resource": "TSORTSOFTINDEXCENTERDLGFM",
        "entry": "概况 -> 操作 -> 调整显示顺序",
        "steps": ["打开排序窗体", "观察五个可拖动区块", "不改变顺序并关闭"],
        "states": [("区块排序", "统计数据、统计图表、信用卡一览、投资一览、财务预算五项均可拖动。", [shot("b19-overview-sort.png")])],
        "commands": [("btnOK", "确定", True, "未触发", "保持原顺序。", "partial")],
        "data_flow": flow(["五个区块的新顺序"], ["当前首页布局"], ["用户布局偏好"], ["概况区块顺序"], ["本轮未保存布局"], "取消恢复原顺序；保存失败不得留下部分排序。"),
        "evidence": [evidence("screenshot", shot("b19-overview-sort.png"), "概况区块排序。")],
        "requirements": ["拖动排序提供稳定标识而不是依赖显示文本。", "保存为用户级布局偏好，不改变账簿数据。", "新增区块时保留既有顺序并采用明确默认位置。"],
        "summary": "已确认概况五个区块的拖动排序页面。",
        "gaps": ["实际保存、重开持久化和恢复默认"],
    },
    "RT-19-012": {
        "resource": "TAIPANELDLG",
        "entry": "未发现用户菜单或已定位动态入口；实验性内部 WebView",
        "steps": ["检查主菜单和隐藏入口", "核对本地 AIPanel.html 与方法证据", "禁止向旧 HTTP 服务发送请求"],
        "reachable": False,
        "unreachable_reason": "当前发行版未发现用户入口；旧实现会向明文 HTTP 端点发送用户输入、key、时间值和 MD5 签名，本轮按安全边界不触发。",
        "states": [("代码实证", "加载 data/AIPanel.html，通过 JavaScript 桥访问咨询、术语解释和 FAQ 三类旧 HTTP 接口。", [NOTES])],
        "commands": [("WebBrowser", "AI 内容请求", False, "安全禁止", "未发送任何用户或账簿数据。", "partial")],
        "data_flow": flow(["用户主动输入的问题、术语或 FAQ 主题"], ["本地 HTML、外部 AI 配置"], ["旧实现无核心账簿写入"], ["外部内容响应"], ["旧端点为明文 HTTP 且客户端包含固定秘密"], "外部失败不得影响离线记账；取消和超时丢弃响应。"),
        "evidence": [evidence("manual_note", NOTES, "AI 入口搜索和禁止外联结论。"), evidence("manual_note", "docs/runtime-ai-console-calculator-contract.md", "AI 请求字段和安全合同。")],
        "requirements": ["AI 作为默认关闭的外部适配器，不进入财务核心。", "只允许 HTTPS、明确同意和用户主动输入，不自动发送财务数据。", "密钥不得硬编码，日志必须脱敏并支持超时、取消和响应大小限制。"],
        "summary": "AI 面板仅有静态代码实证，当前发行版无用户入口，因旧明文 HTTP 风险未动态请求。",
        "gaps": ["动态入口和本地页面实际渲染", "用户明确同意后的真实发送字段和响应状态"],
    },
    "RT-19-013": {
        "resource": "TCONSOLEFM",
        "entry": "内部快捷键 Ctrl+F12；当前桌面会话未打开可见窗口",
        "steps": ["打开快捷键设置确认 Ctrl+F12", "尝试后台和组合键触发", "核对三页与 25 个命令类代码证据"],
        "reachable": False,
        "unreachable_reason": "快捷键设置明确显示控制台 Ctrl+F12，但当前自动化会话无法将组合键路由为可见 TConsoleFm；无普通菜单入口。",
        "states": [("快捷键设置", "控制台字段只读显示 Ctrl+F12；老板键为 Ctrl+1。", [shot("b19-shortcuts.png", nested=True)]), ("代码实证", "控制台、网银插件与网络、SQL 三页；主控制台可写，其余只读；最近保存 10 条历史。", [NOTES])],
        "commands": [("hotkey", "Ctrl+F12", True, "多种后台键盘路径", "未出现可见 TConsoleFm。", "partial"), ("miClear", "清除控制台记录", True, "未动态触发", "处理器静态为无副作用。", "partial")],
        "data_flow": flow(["诊断命令和内部日志"], ["应用配置、网络日志、SQL 日志和系统状态"], ["命令历史和高风险维护副作用"], ["三页诊断输出"], ["包含 SQL、远程、修复、重命名等高风险命令类"], "高风险命令必须结构化授权、预览、审计和可回滚；不得直接执行任意 Shell 或 SQL。"),
        "evidence": [evidence("screenshot", shot("b19-shortcuts.png", nested=True), "快捷键设置中的 Ctrl+F12。"), evidence("manual_note", "docs/runtime-ai-console-calculator-contract.md", "控制台页面、历史和命令合同。")],
        "requirements": ["控制台只在开发或诊断构建启用，不进入普通用户导航。", "SQL、远程、修复和重命名命令使用结构化接口与权限门控。", "诊断日志必须脱敏，命令历史不进入默认同步和备份。"],
        "summary": "已动态确认控制台快捷键配置，窗口在当前发行版/会话中未可见；三页和 25 个命令由代码实证。",
        "gaps": ["可达前置条件", "help 输出、命令语法和副作用", "隐藏重开、历史和清除行为"],
    },
    "RT-19-014": {
        "resource": "TCALCUFM",
        "entry": "日常收支 -> 金额字段 -> F4 共享计算器",
        "steps": ["打开日常收支草稿", "聚焦 TMHCalcuEdit", "发送 F4", "观察按钮和关闭行为", "取消草稿"],
        "states": [("共享金额计算器", "显示 C、退格、倒数、除、乘、减、加、数字、正负号、小数点和等号。", [shot("b19-calculator-popup.png", nested=True)])],
        "commands": [("FormKeyDown", "F4 打开；Esc/方向上关闭", True, "F4 成功打开", "弹层可见且未写入账簿。", "pass"), ("dxCalculatorResult", "=", True, "按钮级自动化未完成表达式", "结果回填待测。", "partial")],
        "data_flow": flow(["宿主金额文本和计算按键"], ["当前金额草稿"], ["有效结果只回填宿主草稿"], ["十进制计算结果或错误"], ["覆盖 160 个窗体中的 429 个 TMHCalcuEdit"], "取消或错误保留原值；父窗取消不产生账务写入。"),
        "evidence": [evidence("screenshot", shot("b19-calculator-popup.png", nested=True), "共享金额计算器弹层。"), evidence("screenshot", shot("b19-probe-command-104.png", nested=True), "日常收支金额宿主。"), evidence("manual_note", "docs/runtime-ai-console-calculator-contract.md", "关闭键和错误/结果合同。")],
        "requirements": ["429 个金额输入复用一个十进制计算器组件。", "有效结果明确完成后回填，取消或错误保留原值。", "Esc 和方向上关闭并消费按键，焦点返回原金额字段。"],
        "summary": "已通过日常收支金额字段用 F4 动态打开共享计算器并确认完整按键布局。",
        "gaps": ["表达式结果回填、除零错误文案、焦点恢复和按键消费"],
    },
}


def build_record(execution_id: str, spec: dict) -> dict:
    """把紧凑规格转换为统一运行记录。"""

    states = [
        {"name": name, "status": "observed", "observations": observations, "evidence_paths": paths}
        for name, observations, paths in spec["states"]
    ]
    commands = [
        {
            "component": component,
            "label": label,
            "initial_state": {"enabled": enabled, "visible": True},
            "trigger": trigger,
            "confirmation": None,
            "outcome": outcome,
            "status": status,
        }
        for component, label, enabled, trigger, outcome, status in spec["commands"]
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
    """写出 14 条 B19 运行记录。"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for execution_id, spec in RECORDS.items():
        output_path = OUTPUT_DIR / f"{execution_id}-20260730T031247+0800.json"
        output_path.write_text(
            json.dumps(build_record(execution_id, spec), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"generated {len(RECORDS)} B19 records")


if __name__ == "__main__":
    main()
