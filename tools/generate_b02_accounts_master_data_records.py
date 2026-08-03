"""生成 B02 账户与基础资料的运行态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
QUEUE_PATH = ROOT / "docs" / "runtime-execution-queue.json"
OBSERVED_AT = "2026-07-30T04:55:45+08:00"
OUTPUT_STAMP = "20260730T045545+0800"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "FC2B9A2A9BAAA1FFED6DFD51D4C9A197A6BE2FDA505EEC4D254629AC5A9BD0B8"
FINAL_HASH = "B7B385F17A45005FEEB1F805E213ED6A0C9FCF9674C60C17C92E581A3B25345C"
BACKUP_ARTIFACT = (
    "artifacts/runtime-validation/backups/"
    "test-before-b02-accounts-master-data-20260730.mh8"
)
NOTES = "artifacts/runtime-validation/B02-accounts-master-data-notes.md"
CONTRACT = "docs/runtime-accounts-and-master-data-contract.md"
STATIC_CATALOG = "docs/runtime-dfm-control-catalog.md"


def shot(name: str) -> str:
    """返回本轮截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(kind: str, path: str, description: str) -> dict:
    """构造一条统一证据记录。"""

    return {"kind": kind, "path": path, "description": description}


def state(name: str, observations: str, *paths: str, status: str = "observed") -> dict:
    """构造页面状态并保持静态与动态证据边界。"""

    result = {"name": name, "status": status, "observations": observations}
    if paths:
        result["evidence_paths"] = list(paths)
    return result


def command(
    component: str,
    label: str,
    trigger: str,
    outcome: str,
    status: str = "partial",
    *,
    confirmation: str | None = None,
    enabled: bool = True,
) -> dict:
    """构造命令观察，未执行保存时不得标记通过。"""

    return {
        "component": component,
        "label": label,
        "initial_state": {"enabled": enabled, "visible": True},
        "trigger": trigger,
        "confirmation": confirmation,
        "outcome": outcome,
        "status": status,
    }


COMMON_REQUIREMENTS = [
    "账户、账户组和期初余额必须在同一事务内创建或全部回滚。",
    "分类、人员、币种和标签被引用后不得静默物理删除，应拒绝、迁移引用或显式停用。",
    "金额使用定点最小货币单位；汇率和利率使用显式精度、方向、生效日期和来源。",
    "向导的上一步、取消和标题栏关闭不得留下账户、余额、分组或基础资料半成品。",
    "旧 Delphi 窗体名仅用于证据追溯，Rust 版按领域实体、命令服务和查询投影拆分。",
]


PREVIOUS_RECORDS = {
    "RT-02-002": "artifacts/runtime-validation/RT-02-002-20260729T091433+0800.json",
    "RT-02-004": "artifacts/runtime-validation/RT-02-004-20260729T091433+0800.json",
    "RT-02-012": "artifacts/runtime-validation/RT-02-012-20260729T091433+0800.json",
    "RT-02-018": "artifacts/runtime-validation/RT-02-018-20260729T023432+0800.json",
    "RT-02-028": "artifacts/runtime-validation/RT-02-028-20260729T140321+0800.json",
    "RT-02-033": "artifacts/runtime-validation/RT-02-033-20260729T023432+0800.json",
}


DYNAMIC = {
    "RT-02-002": {
        "entry": "财务数据 -> 账户中心",
        "states": [
            state(
                "账户中心有数据状态",
                "账户中心显示账户组、账户列表、类型筛选、查看方式、新增账户组、新增账户和操作入口。",
                shot("b02-main-start.png"),
            ),
            state(
                "历史分组验证",
                "既有运行记录已验证按类型/自定义分组切换、空组汇总、组级操作、删除确认和测试组清理。",
                PREVIOUS_RECORDS["RT-02-002"],
            ),
        ],
        "summary": "账户中心、分组投影和账户类型入口已动态验证，状态筛选及全部账户操作仍待补齐。",
        "gaps": ["隐藏、注销、到期和已结清状态筛选", "含交易账户的删除影响预览与失败回滚"],
    },
    "RT-02-003": {
        "entry": "账户工作区 -> 账户概况",
        "states": [
            state(
                "代表性账户概况",
                "外汇、保险、社保、贵金属等账户均复用账户概况外壳，并按账户类型装载专属字段和统计投影。",
                "artifacts/runtime-validation/foreign-account-overview-dialog.png",
                "artifacts/runtime-validation/b13-insurance-account-overview-verified.png",
            )
        ],
        "summary": "账户概况被确认是按账户类型组合详情与统计的通用投影。",
        "gaps": ["现金、活期、组合存款和第三方储值的逐字段往返", "附件和标签的统一展示协议"],
    },
    "RT-02-004": {
        "entry": "账户组 -> 详细资料",
        "states": [
            state(
                "账户详细资料",
                "历史运行记录已验证详细资料二级窗、密码遮罩、父级统一提交和随组删除清理。",
                PREVIOUS_RECORDS["RT-02-004"],
                "artifacts/runtime-validation/account-group-detail-filled.png",
            )
        ],
        "summary": "账户详细资料的嵌套编辑和父级提交边界已验证。",
        "gaps": ["不同账户类型的详细字段矩阵", "附件存储和敏感字段加密迁移"],
    },
    "RT-02-006": {
        "entry": "账户中心 -> 新增账户 -> 现金",
        "states": [
            state("账户资料", "名称、币种、所有者、备注和账户组组成现金账户资料。", shot("b02-wizard-cash.png")),
            state("期初余额", "日期和账户余额组成第二步；本轮未点击完成。", shot("b02-wizard-cash-balance.png")),
        ],
        "summary": "现金账户的基础资料和期初余额两步结构已验证。",
        "gaps": ["非零余额资金来源", "成功创建、重名校验和失败回滚"],
    },
    "RT-02-007": {
        "entry": "主菜单 -> 资料管理 -> 收支项目",
        "states": [
            state(
                "分类列表",
                "支出和收入分开显示，支持搜索、新增项目、二级项目及操作菜单；系统预置项目提示不可修改或删除。",
                shot("b02-information-management.png"),
            )
        ],
        "summary": "收支项目的方向、层级、搜索和系统预置保护已动态确认。",
        "gaps": ["排序页、隐藏项显示、引用中分类删除和迁移语义"],
    },
    "RT-02-008": {
        "entry": "资料管理 -> 币种与汇率 -> 币种操作",
        "states": [
            state(
                "内置币种与本币关系",
                "币种列表显示本币标记、名称、代码和对人民币牌价；当前页面没有新增币种入口，CNY/CHF 的修改删除禁用。CHF 设置为本币后即时刷新并在冷启动保持，人民币牌价列不变。",
                shot("rt02-currency-master-cold-restart-chf-local-20260802.png"),
                STATIC_CATALOG,
            )
        ],
        "summary": "已确认内置币种保护、本币即时切换和本币与人民币报价锚点分离。",
        "gaps": ["自定义币种来源和 TCurrDlg 真实保存", "代码唯一性、引用保护及本币切换跨模块影响"],
    },
    "RT-02-009": {
        "entry": "账户中心 -> 新增账户 -> 储蓄卡 -> 活期(卡/折)",
        "states": [
            state("账户资料", "默认名称为我的活期，包含币种、所有者、备注和账户组。", shot("b02-wizard-current.png")),
            state("余额和资金来源", "开户日期、余额和可选资金来源账户位于第二步。", shot("b02-wizard-current-balance.png")),
        ],
        "summary": "活期存款账户资料、开户日期、余额和资金来源结构已验证。",
        "gaps": ["成功创建、归属一卡通、资金转入原子分录和编辑往返"],
    },
    "RT-02-010": {
        "entry": "主菜单 -> 资料管理 -> 币种与汇率",
        "states": [
            state(
                "币种列表",
                "上半区维护本币、名称、缩写和对人民币牌价；搜索和操作入口可见。",
                shot("b02-currency-list.png"),
            ),
            state(
                "汇率列表和新增",
                "下半区按日期维护两个币种、比较关系、报价方式和四位汇率；新增页默认当天。",
                shot("b02-exchange-rate-editor.png"),
            ),
        ],
        "summary": "币种主档和日期化双币汇率的两层结构已验证。",
        "gaps": ["报价方向公式、在线更新合并、重复日期币种对约束和历史编辑"],
    },
    "RT-02-011": {
        "entry": "账户中心 -> 查看方式 -> 设置[自定义]显示",
        "states": [
            state(
                "自定义分组投影",
                "账户中心可在按类型和按自定义分组之间切换，并保留相同的资产、负债和净资产汇总。",
                "artifacts/runtime-validation/account-center-view-menu-selected.png",
                "artifacts/runtime-validation/account-center-custom-group-view-activated.png",
            )
        ],
        "summary": "自定义账户导航应是账户与分组关系上的独立查询投影。",
        "gaps": ["拖放或批量调整顺序", "隐藏组、空组和跨组重复显示规则"],
    },
    "RT-02-012": {
        "entry": "账户中心 -> 新增账户组/修改账户组",
        "states": [
            state(
                "账户组编辑",
                "历史记录已覆盖空名称校验、有效创建、详细资料父级提交、空组汇总和删除清理。",
                PREVIOUS_RECORDS["RT-02-012"],
                "artifacts/runtime-validation/account-group-detail-dialog-initial.png",
            )
        ],
        "summary": "账户组创建、详细资料和删除清理已形成可复现证据。",
        "gaps": ["重名规则、嵌套组限制和含账户组删除失败回滚"],
    },
    "RT-02-013": {
        "entry": "资料管理 -> 收支项目 -> 新增项目",
        "states": [
            state(
                "新增收支项目",
                "编辑器包含支出/收入方向、名称、上级项目，以及保存并新添和保存。",
                shot("b02-edit-category.png"),
            )
        ],
        "summary": "分类编辑器的方向、名称、父级和连续新增能力已验证。",
        "gaps": ["空名称、重名、跨方向父子关系和成功保存清理"],
    },
    "RT-02-017": {
        "entry": "主菜单 -> 资料管理",
        "states": [
            state("收支项目宿主", "资料管理以统一外壳装载收支项目列表。", shot("b02-information-management.png")),
            state("人员与机构宿主", "同一外壳可由菜单命令直接装载人员与机构列表。", shot("b02-information-command40.png")),
            state("币种和利率宿主", "币种与汇率、存款利率也通过相同资料管理外壳打开。", shot("b02-currency-list.png"), shot("b02-deposit-rates.png")),
        ],
        "summary": "资料管理是按资料类型装载目录编辑器的统一工作区。",
        "gaps": ["统一路由参数、返回导航、搜索状态保存和全部资料类型菜单映射"],
    },
    "RT-02-018": {
        "entry": "主工作区 -> 标签",
        "states": [
            state(
                "标签空状态和新增",
                "历史记录已验证空状态、新增对话框和取消无写入；B17 进一步覆盖查询和临时标签清理。",
                PREVIOUS_RECORDS["RT-02-018"],
                shot("b17-tag-page.png"),
            )
        ],
        "summary": "标签列表、空状态、新增和取消边界已验证。",
        "gaps": ["排序、隐藏、合并、批量关系更新和引用保护"],
    },
    "RT-02-019": {
        "entry": "开户向导或账户编辑器 -> 资金来源账户选择",
        "states": [
            state(
                "嵌入式账户选择器",
                "活期、一本通、定期和第三方储值向导均嵌入 TmwSelectAccount，用于可选资金来源或去向。",
                shot("b02-wizard-current-balance.png"),
                shot("b02-wizard-deposit-one-card-funding.png"),
            )
        ],
        "summary": "账户下拉选择器是多个向导共享的嵌入组件。",
        "gaps": ["下拉树层级、账户类型过滤、隐藏/注销账户和清空行为"],
    },
    "RT-02-020": {
        "entry": "交易或规则编辑器 -> 收支项目选择",
        "states": [
            state(
                "嵌入式分类选择器",
                "静态资源确认选择器区分支出/收入，支持搜索、新增和进入收支项目管理；分类列表动态证据验证其目标目录。",
                STATIC_CATALOG,
                shot("b02-information-management.png"),
            )
        ],
        "summary": "分类选择器应复用分类查询服务，并允许从选择上下文进入受控新增。",
        "gaps": ["选择结果回传、无匹配搜索、隐藏分类和新增后自动选中"],
    },
    "RT-02-021": {
        "entry": "交易或账户编辑器 -> 标签选择",
        "states": [
            state(
                "嵌入式标签选择器",
                "静态资源显示标签列表、确定和新增标签；标签页动态证据验证空状态与新增入口。",
                STATIC_CATALOG,
                shot("b17-tag-page.png"),
            )
        ],
        "summary": "标签下拉选择器与标签目录共享同一标签身份和新增服务。",
        "gaps": ["多选、取消、清空、隐藏标签和新增后选择"],
    },
    "RT-02-022": {
        "entry": "账户中心 -> 新增账户",
        "states": [
            state(
                "账户类型目录",
                "页面按现金储蓄、金融投资、重大资产、债权债务和保险组织账户类型，并对储蓄卡、信用卡、第三方储值、基金、预收预付、垫付待摊和贵金属提供子菜单。",
                shot("b02-new-account-types.png"),
            )
        ],
        "summary": "新增账户类型目录和主要分类已动态确认。",
        "gaps": ["全部子菜单标题与许可边界", "不可用类型和失败提示"],
    },
    "RT-02-023": {
        "entry": "账户中心 -> 新增账户 -> 现金",
        "states": [
            state("账户资料", "现金账户第一步维护名称、币种、所有者、备注和账户组。", shot("b02-wizard-cash.png")),
            state("期初余额", "第二步维护日期和账户余额。", shot("b02-wizard-cash-balance.png")),
        ],
        "summary": "现金开户两步向导已导航到完成前。",
        "gaps": ["成功创建、重名和异常回滚"],
    },
    "RT-02-024": {
        "entry": "账户中心 -> 新增账户 -> 储蓄卡 -> 活期一本通",
        "states": [
            state("一本通账户组", "先录入一本通名称和所有者。", shot("b02-wizard-current-one-card.png")),
            state("活期子账户", "第二步录入子账户名称和币种。", shot("b02-wizard-current-one-card-subaccount.png")),
            state("余额和归属", "第三步录入日期、余额、资金来源并显示归属一本通。", shot("b02-wizard-current-one-card-balance.png")),
        ],
        "summary": "活期一本通按账户组、子账户和期初余额三层创建。",
        "gaps": ["多个子账户、非人民币、成功提交和部分失败回滚"],
    },
    "RT-02-025": {
        "entry": "账户中心 -> 新增账户 -> 储蓄卡 -> 活期(卡/折)",
        "states": [
            state("账户资料", "活期账户资料包含名称、币种、所有者、备注和账户组。", shot("b02-wizard-current.png")),
            state("期初状态", "开户日期、余额和资金来源位于第二步。", shot("b02-wizard-current-balance.png")),
        ],
        "summary": "活期存折银行卡两步向导已验证。",
        "gaps": ["归属一卡通、成功创建和资金来源分录"],
    },
    "RT-02-026": {
        "entry": "账户中心 -> 新增账户 -> 储蓄卡 -> 定期一本通",
        "states": [
            state("一本通账户组", "第一步录入定期一本通名称和所有者。", shot("b02-wizard-deposit-one-card.png")),
            state("定期子账户", "第二步录入子账户名称和币种。", shot("b02-wizard-deposit-one-card-details.png")),
            state("存款条款", "第三步包含存款类型、存期及单位、年利率、起存日期和自动续存。", shot("b02-wizard-deposit-one-card-terms.png")),
            state("金额和来源", "最后一步包含存款金额、资金来源和归属一本通。", shot("b02-wizard-deposit-one-card-funding.png")),
        ],
        "summary": "定期一本通的账户组、子账户、利率条款和资金来源四步结构已验证。",
        "gaps": ["零存整取等取款去向分支", "到期规则、成功提交和原子回滚"],
    },
    "RT-02-027": {
        "entry": "各新增账户类型 -> 公共向导宿主",
        "states": [
            state(
                "公共向导协议",
                "现金、活期、一本通、定期、理财和第三方储值向导共享上一步、下一步/完成以及分页草稿模式。",
                shot("b02-wizard-cash.png"),
                shot("b02-wizard-deposit-one-card-terms.png"),
                shot("b02-wizard-money-product-balance.png"),
            )
        ],
        "summary": "NewAcctWizardDlgFm 是公共向导宿主，不应在 Rust 版复制为领域实体。",
        "gaps": ["统一校验时机、步骤跳转、错误聚焦和关闭确认"],
    },
    "RT-02-028": {
        "entry": "账户中心 -> 新增账户 -> 外汇",
        "states": [
            state(
                "三步创建和清理",
                "历史运行记录已验证外汇账户基本资料、期初余额、附加币种、成功创建、工作区刷新和临时账户删除。",
                PREVIOUS_RECORDS["RT-02-028"],
            )
        ],
        "summary": "外汇账户创建和删除清理已有成功路径证据。",
        "gaps": ["非零多币种期初、校验错误和数据库失败回滚"],
    },
    "RT-02-029": {
        "entry": "账户中心 -> 新增账户 -> 银行理财产品",
        "states": [
            state("账户资料", "第一步维护名称、币种、所有者、备注和账户组。", shot("b02-wizard-money-product.png")),
            state("资金来源", "第二步维护日期，并在账户自身余额与其它账户之间选择资金来源。", shot("b02-wizard-money-product-balance.png")),
        ],
        "summary": "银行理财账户资料和期初资金来源已验证。",
        "gaps": ["成功创建、非零余额、资金转入和产品主档关联"],
    },
    "RT-02-030": {
        "entry": "账户中心 -> 新增账户 -> 储蓄卡 -> 一卡通",
        "states": [
            state("一卡通名称", "第一步录入一卡通账户组名称和备注。", shot("b02-wizard-one-card.png")),
            state("子账户组成", "第二步要求至少选择一个子账户，并提供创建活期或定期子账户。", shot("b02-wizard-one-card-subaccounts.png")),
        ],
        "summary": "一卡通由账户组和至少一个活期/定期子账户组成。",
        "gaps": ["选择现有子账户、重复归属、成功提交和子账户失败回滚"],
    },
    "RT-02-031": {
        "entry": "账户中心 -> 新增账户 -> 家居物品",
        "states": [
            state(
                "家居物品开户",
                "B14 已动态验证家居物品账户向导，包含名称、所有者、币种、资产性质、备注和账户组。",
                "artifacts/runtime-validation/b14-item-account-wizard.png",
            )
        ],
        "summary": "家居物品账户创建结构已有跨批次动态证据。",
        "gaps": ["本轮 B02 独立成功路径复核", "分类主档和首笔物品交易的原子关系"],
    },
    "RT-02-032": {
        "entry": "账户中心 -> 新增账户 -> 第三方储值 -> 支付宝",
        "states": [
            state("账户资料", "第一步维护名称、币种、所有者、备注和账户组；默认名会避让既有同名账户。", shot("b02-wizard-third-party-storage.png")),
            state("余额和来源", "第二步维护日期、余额和可选资金来源账户。", shot("b02-wizard-third-party-storage-balance.png")),
        ],
        "summary": "第三方储值两步开户和默认名称避让行为已验证。",
        "gaps": ["微信、财付通、其它储值类型", "成功创建、类型代码和编辑往返"],
    },
    "RT-02-033": {
        "entry": "标签 -> 新增标签",
        "states": [
            state(
                "新增标签",
                "历史记录已验证新增标签对话框、分号批量输入提示、默认保存按钮和取消无写入。",
                PREVIOUS_RECORDS["RT-02-033"],
                shot("b17-new-tag-dialog.png"),
            )
        ],
        "summary": "新增标签对话框和批量名称输入提示已验证。",
        "gaps": ["空名称、重名、批量部分失败和成功保存"],
    },
    "RT-02-034": {
        "entry": "资料管理 -> 人员与机构 -> 新增家庭成员",
        "states": [
            state(
                "人员与机构编辑",
                "编辑器包含名称、类型、性别、联系方式、地址和可选生日；本轮未保存。",
                shot("b02-edit-person.png"),
            )
        ],
        "summary": "人员与机构编辑器的核心字段和默认家庭成员类型已验证。",
        "gaps": ["机构类型字段、生日启用行为、重名和引用保护"],
    },
    "RT-02-035": {
        "entry": "主菜单 -> 资料管理 -> 人员与机构",
        "states": [
            state(
                "人员与机构列表",
                "页面提供搜索、新增家庭成员和操作菜单，并由资料管理外壳承载。",
                shot("b02-information-command40.png"),
            )
        ],
        "summary": "人员与机构列表的搜索、新增和操作入口已验证。",
        "gaps": ["有数据列、修改、隐藏、删除引用保护、导出和打印"],
    },
    "RT-02-036": {
        "entry": "账户中心 -> 新增账户 -> 垫付/待摊 -> 待摊费用",
        "states": [
            state(
                "待摊费用编辑",
                "当前版本实际类为 TPrepaidExpensesDlgFm，页面包含日期、币种、金额、资金账户、摊销周期参数和保存入口；旧 TPREPEXPEACCTDLGFM 作为概况资源保留追溯。",
                shot("b02-prepaid-expense-account.png"),
                STATIC_CATALOG,
            )
        ],
        "summary": "待摊费用现行编辑器和旧概况资源的替代关系已确认。",
        "gaps": ["摊销公式、首期日期、余数处理、成功生成计划和删除回滚"],
    },
    "RT-02-037": {
        "entry": "主菜单 -> 资料管理 -> 存款利率",
        "states": [
            state(
                "人民币和外币利率目录",
                "页面按人民币/外币储蓄分区，并按储蓄类型、储蓄期间和年利率展示；数值仅代表测试库当前参考数据。",
                shot("b02-deposit-rates.png"),
            )
        ],
        "summary": "人民币手工提交、冷启动和在线刷新已有动态证据；反汇编补齐仅数字解析、失败回退和乘 10000 取整写入协议。",
        "gaps": ["外币真实编辑", "非法数值和焦点提交边界", "导出打印", "在线失败回滚和并发"],
    },
    "RT-02-038": {
        "entry": "账户或交易操作 -> 选择标签",
        "states": [
            state(
                "标签选择上下文",
                "账户中心真实宿主已验证外层取消零写入、内联新增独立写标签主数据、外层确定写账户关系、清空解除关系和冷启动；通用下拉另验证过滤、多选和清空。",
                shot("rt02-002-account-tag-dialog-initial-20260801.png"),
                shot("rt02-002-account-tag-after-association-20260801.png"),
                shot("rt02-002-account-tag-master-remains-unselected-cold-restart-20260801.png"),
            )
        ],
        "summary": "账户标签外层选择器的取消、创建、关联、解除和冷启动已闭环。",
        "gaps": ["隐藏标签和大量候选", "版本冲突、关系失败和重复提交", "键盘可访问性"],
    },
    "RT-02-039": {
        "entry": "旧主题关联流程 -> 选择主题",
        "states": [
            state(
                "旧主题选择器",
                "静态资源确认其生命周期存在；当前产品标签页使用新标签术语，未单独触发旧 SelectThemeDlgFm。",
                STATIC_CATALOG,
                shot("b17-tag-page.png"),
                status="pending",
            )
        ],
        "summary": "旧主题选择器按标签选择兼容适配处理，不复制平行领域模型。",
        "gaps": ["仍在使用该窗体的旧交易路径和主题到标签的数据迁移"],
    },
    "RT-02-040": {
        "entry": "旧程序内部主题 UI 配置",
        "states": [
            state(
                "内部皮肤配置",
                "静态资源包含启动画面、对话框图片、主窗口图片、工具栏图片、功能区图片和其它页签；当前用户流程未触发。",
                STATIC_CATALOG,
                status="pending",
            )
        ],
        "summary": "ThemeUIFm 属于旧 UI 皮肤配置，不进入财务领域模型。",
        "gaps": ["是否存在用户可达入口", "Rust 前端主题能力的实际产品要求"],
    },
    "RT-02-041": {
        "entry": "账户中心 -> 新增账户 -> 第三方储值",
        "states": [
            state(
                "第三方储值账户资料",
                "其它储值账户已完成两页非零外部期初提交和冷启动；TThirdDepositsAcctDlgFm 已验证名称、所有者、备注、创建日期、只读币种、取消和资料保存。",
                shot("rt41-third-party-wizard-initial.png"),
                shot("rt41-cold-start-after-create.png"),
                shot("rt41-third-party-editor-initial.png"),
            )
        ],
        "summary": "其它储值账户的非零外部期初、提交后刷新故障和资料编辑已闭环。",
        "gaps": ["真实资金来源双边分录", "提供方专属字段", "并发幂等和有交易账户删除保护"],
    },
}


def role_flow(role: str) -> dict:
    """按队列角色生成保守的数据流，不编造旧库表名。"""

    if role in {"account_editor", "transaction_editor"}:
        return {
            "inputs": ["账户资料或向导草稿", "期初日期、金额和可选资金来源", "关联人员、币种、账户组和标签"],
            "reads": ["账户类型规则", "基础资料目录", "可用资金账户和当前账簿上下文"],
            "writes": ["本轮未点击保存；真实提交应原子写入账户、期初状态和必要关联"],
            "derived_results": ["账户身份、分组投影、期初余额和账户类型专属配置"],
            "side_effects": ["本轮关闭向导后未观察到测试账户或业务对象残留"],
            "rollback": "取消丢弃完整草稿；任一步校验或持久化失败时不得留下账户、余额或关联半成品。",
        }
    if role == "catalog_editor":
        return {
            "inputs": ["基础资料名称、类型、层级、状态和日期化参数"],
            "reads": ["现有目录项、父子关系和业务引用"],
            "writes": ["本轮未提交新增或修改；真实保存应写入版本化基础资料"],
            "derived_results": ["搜索列表、选择器候选和业务规则参数"],
            "side_effects": ["页面导航和取消不应修改账簿业务事实"],
            "rollback": "保存失败保持原目录；已引用项目必须拒绝物理删除或在同一事务迁移引用。",
        }
    if role == "selector_filter":
        return {
            "inputs": ["搜索词、候选范围和当前选择"],
            "reads": ["账户、分类或标签目录及可见状态"],
            "writes": ["选择器本身不写业务数据，只向宿主返回稳定 ID"],
            "derived_results": ["过滤候选和选中值"],
            "side_effects": ["取消不改变宿主草稿"],
            "rollback": "关闭或取消返回未选择结果；从选择器新增资料失败时不得污染宿主草稿。",
        }
    if role == "projection_view":
        return {
            "inputs": ["账户 ID、显示范围和估值时点"],
            "reads": ["账户资料、余额、关联对象和类型专属统计"],
            "writes": ["只读概况不写业务事实"],
            "derived_results": ["账户概况、余额和类型专属字段投影"],
            "side_effects": ["关闭投影不改变账簿"],
            "rollback": "查询失败显示可重试错误，不回写部分投影。",
        }
    return {
        "inputs": ["配置草稿和当前选择"],
        "reads": ["现有配置、基础资料和引用关系"],
        "writes": ["本轮未提交配置变更"],
        "derived_results": ["配置后的显示顺序、分组或选择状态"],
        "side_effects": ["取消后保持进入前状态"],
        "rollback": "配置保存应单事务替换；取消和失败保留原配置。",
    }


def static_states(form: dict) -> list[dict]:
    """为未直接到达的资源生成明确标注的静态状态。"""

    details = []
    if form.get("fields"):
        details.append("字段：" + "、".join(form["fields"]))
    if form.get("tabs"):
        details.append("页签：" + "、".join(form["tabs"]))
    if form.get("options"):
        details.append("选项：" + "、".join(form["options"]))
    text = "；".join(details) if details else "静态目录已确认窗体类、角色和事件边界。"
    return [
        state("静态结构", text, STATIC_CATALOG),
        state("动态成功路径", "本轮未直接触发该旧资源的独立成功提交。", NOTES, status="pending"),
    ]


def queue_commands(form: dict) -> list[dict]:
    """把静态命令目录转换为待验证命令，避免遗漏高风险入口。"""

    result = []
    for item in form.get("actionable_commands", []):
        initial = dict(item.get("initial_state") or {})
        enabled = initial.get("Enabled", True)
        initial.setdefault("enabled", enabled)
        initial.setdefault("visible", True)
        related = list(item.get("related_event_ids") or [])
        entry = {
            "component": item.get("component", "unknown"),
            "label": item.get("label") or item.get("component", "未命名命令"),
            "initial_state": initial,
            "trigger": "本轮未单独触发；已从静态事件目录登记。",
            "confirmation": "高风险写入或删除需要显式确认。" if item.get("high_risk") else None,
            "outcome": "等待后续真实操作、数据前后对比和失败回滚验证。",
            "status": "pending",
        }
        if related:
            entry["event_ids"] = related
        result.append(entry)
    return result


def build_record(form: dict) -> dict:
    """把队列项和本轮动态证据合并为统一观察记录。"""

    execution_id = form["execution_id"]
    dynamic = DYNAMIC.get(execution_id, {})
    states = dynamic.get("states", static_states(form))
    commands = dynamic.get("commands", queue_commands(form))
    record_evidence = [
        evidence("manual_note", NOTES, "B02 动态验证时间线、文件指纹和取消边界。"),
        evidence("manual_note", CONTRACT, "Rust 账户与基础资料领域合同。"),
        evidence("manual_note", STATIC_CATALOG, "旧窗体字段、页签和命令静态目录。"),
    ]
    seen = {NOTES, CONTRACT, STATIC_CATALOG}
    for item in states:
        for path in item.get("evidence_paths", []):
            if path in seen:
                continue
            seen.add(path)
            kind = "screenshot" if path.lower().endswith(".png") else "log"
            record_evidence.append(evidence(kind, path, f"{item['name']} 的追溯证据。"))
    previous = PREVIOUS_RECORDS.get(execution_id)
    if previous and previous not in seen:
        record_evidence.append(evidence("log", previous, "该资源此前的动态观察记录。"))

    default_summary = (
        f"{form.get('title') or form['resource']} 已完成静态结构登记；"
        "本轮未直接提交其独立成功路径。"
    )
    default_gaps = [
        "独立入口、有效输入、校验失败、成功提交和取消路径",
        "写入前后数据、引用保护和失败回滚",
    ]
    entry = dynamic.get("entry") or form.get("entry_strategy") or "通过所属业务宿主间接触发"
    return {
        "schema_version": 1,
        "execution_id": execution_id,
        "resource": form["resource"],
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
            "entry_point": entry,
            "steps": ["打开所属业务入口", "观察字段和默认状态", "只导航到提交前", "关闭取消并核对进程与账簿"],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": states,
        "commands": commands,
        "data_flow": dynamic.get("data_flow", role_flow(form.get("role", "configuration_editor"))),
        "evidence": record_evidence,
        "requirements_update": COMMON_REQUIREMENTS + dynamic.get("requirements", []),
        "result": {
            "status": "partial",
            "summary": dynamic.get("summary", default_summary),
            "remaining_gaps": dynamic.get("gaps", default_gaps),
        },
    }


def main() -> None:
    """写出 41 条 B02 最新运行记录。"""

    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    forms = [
        form
        for form in queue["forms"]
        if form["batch_id"] == "B02-accounts_master_data"
    ]
    if len(forms) != 41:
        raise RuntimeError(f"B02 队列数量异常：{len(forms)}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for form in forms:
        output_path = OUTPUT_DIR / f"{form['execution_id']}-{OUTPUT_STAMP}.json"
        output_path.write_text(
            json.dumps(build_record(form), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"generated {len(forms)} B02 records")


if __name__ == "__main__":
    main()
