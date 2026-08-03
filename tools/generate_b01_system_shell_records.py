"""生成 B01 系统外壳、账簿生命周期与设置页面的运行记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T04:09:27+08:00"
OUTPUT_STAMP = "20260730T040927+0800"
LEDGER_PATH = r"C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8"
BASELINE_HASH = "67760084CD376DAAC0B400A3917F72CBCE98398C484143B11E9A4BAFDBF1812A"
FINAL_HASH = "FC2B9A2A9BAAA1FFED6DFD51D4C9A197A6BE2FDA505EEC4D254629AC5A9BD0B8"
BACKUP_ARTIFACT = (
    "artifacts/runtime-validation/backups/"
    "test-before-b01-system-shell-20260730.mh8"
)
NOTES = "artifacts/runtime-validation/B01-system-shell-notes.md"
CONTRACT = "docs/runtime-ledger-lifecycle-and-settings-contract.md"
STATIC_CATALOG = "docs/runtime-dfm-control-catalog.md"


def screenshot(name: str) -> str:
    """返回运行截图的仓库相对路径。"""

    return f"artifacts/runtime-validation/screenshots/{name}"


def evidence(kind: str, path: str, description: str) -> dict:
    """构造一条不包含认证值的追溯证据。"""

    return {"kind": kind, "path": path, "description": description}


def command(
    component: str,
    label: str,
    trigger: str,
    outcome: str,
    status: str,
    *,
    confirmation: str | None = None,
    enabled: bool = True,
) -> dict:
    """构造命令观察，明确区分观察与真实提交。"""

    return {
        "component": component,
        "label": label,
        "initial_state": {"enabled": enabled, "visible": True},
        "trigger": trigger,
        "confirmation": confirmation,
        "outcome": outcome,
        "status": status,
    }


def flow(
    inputs: list[str],
    reads: list[str],
    writes: list[str],
    results: list[str],
    effects: list[str],
    rollback: str,
) -> dict:
    """构造账簿生命周期和配置页面的数据流。"""

    return {
        "inputs": inputs,
        "reads": reads,
        "writes": writes,
        "derived_results": results,
        "side_effects": effects,
        "rollback": rollback,
    }


COMMON_REQUIREMENTS = [
    "账簿生命周期命令必须在执行前显示目标路径、影响范围和可恢复点。",
    "配置、密码和授权页面不得在日志、截图或错误信息中暴露秘密值。",
    "取消和标题栏关闭不得提交账簿、设置、快捷键、密码或授权变更。",
    "旧窗体名只用于追溯；Rust 版按应用外壳、账簿服务、安全和设置职责拆分。",
]


SPECS = {
    "RT-01-001": {
        "resource": "TABOUTFORM",
        "entry": "帮助 -> 关于",
        "steps": ["打开帮助菜单", "选择关于", "核对产品和版本信息", "关闭窗体"],
        "states": [
            (
                "关于页",
                "显示财智8产品标识、版本、操作系统和公司版权信息；本轮未打开公司网站。",
                [screenshot("b01-about.png")],
            )
        ],
        "commands": [
            command(
                "lblCompany",
                "公司链接",
                "未点击外部链接",
                "保留在本地关于页。",
                "partial",
            )
        ],
        "summary": "已动态确认关于页的产品、版本和环境信息。",
        "gaps": ["公司链接离线失败处理、更新通道与构建标识展示"],
        "screenshots": [("b01-about.png", "关于页，未包含认证信息。")],
    },
    "RT-01-002": {
        "resource": "TBACKUPBOOKFM",
        "entry": "账簿(test) -> 备份账簿",
        "steps": ["打开账簿菜单", "选择备份账簿", "观察名称和目录", "关闭取消"],
        "states": [
            (
                "备份初始页",
                "默认备份名包含账簿名和日期，默认目录位于 MoneyHome8 Backup；提供更改和确定。",
                [screenshot("b01-backup-book.png")],
            )
        ],
        "commands": [
            command("BtnDBrowse", "更改", "未打开目录选择", "默认目录保持不变。", "partial"),
            command(
                "RzButtonOk",
                "确定",
                "未触发高风险确认",
                "没有生成旧格式备份文件。",
                "partial",
                confirmation="执行后会创建备份文件。",
            ),
        ],
        "data_flow": flow(
            ["备份名称", "目标目录"],
            ["当前 test.mh8 的一致性快照", "备份设置"],
            ["未执行；真实提交应只写目标备份文件和清单"],
            ["可校验、可恢复的账簿备份"],
            ["本轮未创建备份输出；关闭后只观察到旧程序会话写回"],
            "取消时不创建文件；失败时删除未完成临时文件并保留原账簿。",
        ),
        "requirements": ["备份必须使用一致性快照、临时文件、原子改名和 SHA-256 清单。"],
        "summary": "已确认备份名称、默认目录和确认入口，未执行文件创建。",
        "gaps": ["旧 .mh8k 格式、压缩算法、附件范围、保留策略和失败恢复"],
        "screenshots": [("b01-backup-book.png", "备份账簿初始页。")],
    },
    "RT-01-003": {
        "resource": "TCHECKBOOKDLG",
        "entry": "账簿(test) -> 结算账簿",
        "steps": ["打开账簿菜单", "选择结算账簿", "观察截止日和结算备份路径", "关闭取消"],
        "states": [
            (
                "结算确认前",
                "默认截止日为当天，先显示结算备份路径；文案说明截止日前记录会被合并，完整历史依赖还原备份查看。",
                [screenshot("b01-check-book.png")],
            )
        ],
        "commands": [
            command("btnChange", "更改", "未打开路径选择", "默认结算备份路径保持不变。", "partial"),
            command(
                "RzButtonOk",
                "确定",
                "未触发破坏性确认",
                "没有合并或删除任何历史记录。",
                "partial",
                confirmation="结算会改变截止日前历史的可见明细。",
            ),
        ],
        "data_flow": flow(
            ["结算截止日", "结算备份路径"],
            ["截止日前交易及关联对象", "当前账簿版本"],
            ["本轮未执行；兼容实现必须先生成可验证恢复点"],
            ["归档或结算后的活动账簿视图"],
            ["本轮未改变业务历史"],
            "确认前可取消；执行失败必须恢复原文件，成功后仍可访问完整历史。",
        ),
        "requirements": ["Rust 版应保留结算目的，但不得把完整历史仅锁在不可验证的旧备份中。"],
        "summary": "已确认结算的截止日、先备份语义和历史合并风险，未执行结算。",
        "gaps": ["合并算法、余额结转口径、跨期引用、旧备份恢复和失败回滚"],
        "screenshots": [("b01-check-book.png", "结算确认前页面。")],
    },
    "RT-01-004": {
        "resource": "TGUIDEDLG",
        "entry": "启动或首次使用流程中的内部引导宿主",
        "reachable": False,
        "unreachable_reason": "当前 test.mh8 正常启动未出现引导页，静态资源也没有可执行命令或业务字段。",
        "states": [
            (
                "未出现",
                "当前会话直接进入主窗口；GuideDlg 仅保留为旧启动引导资源。",
                [NOTES],
            )
        ],
        "summary": "当前账簿启动没有引导页，Rust 版按可跳过的新手引导能力处理。",
        "gaps": ["全新安装、空配置和首次新建账簿时是否出现"],
    },
    "RT-01-005": {
        "resource": "TMAINFORM",
        "entry": "启动 MoneyHome8 并自动打开 test.mh8",
        "steps": ["启动专用进程", "等待 test - 财智8", "展开主菜单", "打开代表页面", "正常关闭"],
        "states": [
            (
                "已打开账簿",
                "主窗口标题为 test - 财智8，左侧账户导航、工作区和顶部工具栏可见。",
                [screenshot("b01-main-baseline.png")],
            ),
            (
                "主菜单展开",
                "顶层包含账簿、资料管理、计划提醒、财务工具、设置、帮助和退出。",
                [screenshot("b01-main-menu.png")],
            ),
            (
                "正常关闭",
                "目标 PID 正常退出、无 test.mh8 锁文件；另一 MoneyHome8 进程保持运行。",
                [NOTES],
            ),
        ],
        "commands": [
            command("pmMainPopupMenu", "主菜单", "点击主菜单按钮", "展开七个顶层菜单。", "pass"),
            command("close", "关闭应用", "发送正常窗口关闭", "目标进程在等待后正常退出。", "pass"),
        ],
        "data_flow": flow(
            ["启动应用", "最近账簿配置", "菜单命令"],
            ["test.mh8", "应用级设置", "会话状态"],
            ["正常退出时旧程序写回了未识别的会话级二进制状态"],
            ["主工作区、导航历史和当前账簿上下文"],
            ["文件长度不变但 SHA-256 变化；未执行业务对象写入"],
            "启动或关闭失败不得破坏原账簿；会话元数据必须与账务事实分离。",
        ),
        "requirements": ["主外壳必须支持无账簿、已打开账簿、菜单展开、导航和可等待的正常退出。"],
        "summary": "补齐了主窗口、菜单和正常关闭证据；旧程序退出会改变账簿哈希。",
        "gaps": ["最近账簿配置来源、全部快捷键、窗口状态恢复和会话写回字段"],
        "screenshots": [
            ("b01-main-baseline.png", "打开 test.mh8 后的主工作区。"),
            ("b01-main-menu.png", "七个顶层菜单。"),
        ],
    },
    "RT-01-006": {
        "resource": "TNEWBOOKFM",
        "entry": "账簿(test) -> 新建账簿",
        "steps": ["打开账簿菜单", "选择新建账簿", "观察默认位置和密码选项", "关闭取消"],
        "states": [
            (
                "新建账簿初始页",
                "显示账簿名、保存位置、立即设置密码选项和非系统分区提示；未输入名称。",
                [screenshot("b01-new-book.png")],
            )
        ],
        "commands": [
            command("CheckPaw", "建好后立即设置账簿密码", "未切换", "保持默认选项。", "partial"),
            command("BtnOK", "确定", "未触发创建", "没有创建新账簿。", "partial"),
            command("btnChange", "更改", "未打开目录选择", "默认路径保持不变。", "partial"),
        ],
        "data_flow": flow(
            ["新账簿名", "保存位置", "是否立即设置密码"],
            ["目标目录可写性", "现有同名文件", "当前数据库版本"],
            ["本轮未执行；真实提交应原子创建独立账簿"],
            ["可打开的新账簿和可选密码设置后续步骤"],
            ["本轮没有新增文件"],
            "取消时不留下空文件；失败时清理临时文件且不切换当前账簿。",
        ),
        "requirements": ["新建账簿必须拒绝覆盖、规范化扩展名并在首次打开前完成结构校验。"],
        "summary": "已确认新建账簿字段、默认目录和可选密码流程，未创建文件。",
        "gaps": ["名称校验、同名冲突、磁盘错误、密码后续页和成功后自动切换"],
        "screenshots": [("b01-new-book.png", "新建账簿初始页。")],
    },
    "RT-01-007": {
        "resource": "TPASSWORDDIALOG",
        "entry": "旧数据库驱动的内部密码列表对话框",
        "reachable": False,
        "unreachable_reason": "当前 test.mh8 的产品路径未触发该英文对话框；静态控件包含 OK、Cancel、Add、Remove 和 Remove all。",
        "states": [
            (
                "技术依赖对话框",
                "静态证据显示它管理密码项列表，不等同于账簿密码设置页。",
                [STATIC_CATALOG],
            )
        ],
        "summary": "该英文密码列表页按旧数据库技术依赖处理，不复制为 Rust 产品页面。",
        "gaps": ["哪些旧格式账簿或数据库驱动错误会触发该对话框"],
    },
    "RT-01-008": {
        "resource": "TPWDCHANGEFM",
        "entry": "账簿(test) -> 设置账簿密码",
        "steps": ["打开账簿菜单", "选择设置账簿密码", "观察两次密码输入", "关闭取消"],
        "states": [
            (
                "新密码输入",
                "页面要求输入新密码和再次输入，密码值为空且未提交。",
                [screenshot("b01-password-settings.png")],
            )
        ],
        "commands": [command("BtnOk", "确定", "未输入密码且未提交", "账簿密码未改变。", "partial")],
        "data_flow": flow(
            ["新密码", "重复密码"],
            ["当前账簿安全状态", "密码策略"],
            ["本轮未执行；真实提交只保存版本化密钥派生参数和密文"],
            ["账簿解锁凭证"],
            ["本轮没有密码或业务数据写入"],
            "取消保留原安全状态；失败不得留下半加密账簿。",
        ),
        "requirements": ["密码修改必须验证两次输入，并通过可中断迁移和原子换档保护整库。"],
        "summary": "已确认账簿密码使用两次新密码输入，未提交任何秘密。",
        "gaps": ["旧密码校验、密码策略、加密范围、忘记密码和迁移失败恢复"],
        "screenshots": [("b01-password-settings.png", "空白密码设置页，不含秘密值。")],
    },
    "RT-01-009": {
        "resource": "TPWDCHECKFM",
        "entry": "受密码保护账簿或最小化保护恢复时的密码输入",
        "reachable": False,
        "unreachable_reason": "当前 test.mh8 未设置账簿密码，且本轮没有启用最小化保护，因此未触发真实密码校验页。",
        "states": [
            (
                "静态密码校验",
                "静态资源提供密码输入和确定；具体错误计数和锁定策略未动态验证。",
                [STATIC_CATALOG],
            )
        ],
        "commands": [command("RzButtonOk", "确定", "未触发", "没有提交密码。", "partial")],
        "summary": "密码校验页可达条件已确认，但当前无密码账簿无法动态触发。",
        "gaps": ["错误提示、重试限制、退避、取消和锁定恢复"],
    },
    "RT-01-010": {
        "resource": "TREGISTERFORM",
        "entry": "帮助 -> 软件许可",
        "steps": ["打开帮助菜单", "选择软件许可", "只识别初始页结构", "关闭取消"],
        "states": [
            (
                "软件许可初始页",
                "真实窗体类为 TRegisterForm，包含免费使用、购买、激活、离线激活、通行证和用户资料等多阶段页。所有输入值均已脱敏，未保存截图。",
                [NOTES, STATIC_CATALOG],
            )
        ],
        "commands": [
            command("btnFirstUse_FreeUse", "使用免费功能", "未点击", "授权状态保持不变。", "partial"),
            command("btnIndex_Register", "激活高级功能", "未点击", "未联网、未提交序列号。", "partial"),
            command("btnOfflineReg", "离线激活", "未点击", "未生成或导入激活数据。", "partial"),
        ],
        "data_flow": flow(
            ["序列号", "保护信息", "通行证", "用户资料", "离线激活数据"],
            ["本地授权状态", "许可服务响应"],
            ["本轮未执行；授权数据必须与财务账簿隔离"],
            ["免费或高级功能权限集合"],
            ["未联网、未注册、未购买、未更改授权状态"],
            "取消时不改变权限；网络失败不得阻止离线账务核心。",
        ),
        "requirements": ["授权适配器不得上传账簿内容，离线核心功能不得依赖许可服务可用性。"],
        "summary": "已动态到达软件许可窗体并识别多阶段流程，敏感字段全部脱敏。",
        "gaps": ["许可服务协议、免费版边界、离线激活格式、迁移策略和失败码"],
    },
    "RT-01-011": {
        "resource": "TRESTOREBOOKFM",
        "entry": "账簿(test) -> 还原账簿",
        "steps": ["打开账簿菜单", "选择还原账簿", "观察覆盖警告和文件选择", "关闭取消"],
        "states": [
            (
                "还原初始页",
                "页面警告还原会覆盖当前账簿，并建议还原到新建账簿；提供选择和确定。",
                [screenshot("b01-restore-book.png")],
            )
        ],
        "commands": [
            command("BtnSelect", "选择", "未打开文件选择", "没有读取外部备份。", "partial"),
            command(
                "RzButtonOk",
                "确定",
                "未触发覆盖确认",
                "当前 test.mh8 未被还原或覆盖。",
                "partial",
                confirmation="还原可能覆盖当前账簿。",
            ),
        ],
        "data_flow": flow(
            ["备份文件", "还原到新账簿或覆盖当前账簿"],
            ["备份清单、版本、校验和和当前账簿状态"],
            ["本轮未执行；真实覆盖前必须自动创建安全备份"],
            ["校验通过并可打开的还原账簿"],
            ["本轮未读取备份、未覆盖文件"],
            "默认还原到新账簿；覆盖失败必须原子恢复原文件。",
        ),
        "requirements": ["还原默认目标必须是新账簿，覆盖当前账簿需要二次确认和自动安全备份。"],
        "summary": "已确认还原覆盖警告和推荐新账簿路径，未执行还原。",
        "gaps": ["备份校验、版本迁移、附件恢复、空间不足、覆盖回滚和旧格式兼容"],
        "screenshots": [("b01-restore-book.png", "还原账簿覆盖警告。")],
    },
    "RT-01-012": {
        "resource": "TSHORTCUTMANAGEDLGFM",
        "entry": "设置 -> 快捷键设置",
        "steps": ["打开设置菜单", "选择快捷键设置", "观察老板键、F1-F12 和菜单快捷键", "关闭取消"],
        "states": [
            (
                "快捷键设置",
                "老板键已启用并显示组合键；F1 为日常收支、F2 为转账，其余功能键为空；下方列出菜单命令和快捷键。",
                [screenshot("b01-shortcuts.png")],
            )
        ],
        "commands": [
            command("cbBossKey", "启用老板键", "未切换", "现有设置保持不变。", "partial"),
            command("btnNewShortCut", "保存快捷键", "未点击", "没有新增快捷键。", "partial"),
            command("miDelete", "删除", "未点击", "没有删除快捷键。", "partial"),
            command("RzButtonOk", "确定", "未点击，使用标题栏关闭", "配置未提交。", "pass"),
        ],
        "data_flow": flow(
            ["老板键开关和组合键", "F1-F12 功能", "菜单命令快捷键"],
            ["命令注册表", "系统保留组合键", "现有用户映射"],
            ["本轮未执行；真实提交写应用级快捷键配置"],
            ["无冲突的命令到按键映射"],
            ["本轮没有设置写入"],
            "取消恢复打开前映射；冲突校验失败不得覆盖原映射。",
        ),
        "requirements": ["快捷键保存前必须检测命令重复、系统保留键和老板键冲突。"],
        "summary": "已确认老板键、功能键和菜单快捷键三层配置，未保存修改。",
        "gaps": ["冲突提示、清除流程、导入迁移、全局热键注册失败和重启持久化"],
        "screenshots": [("b01-shortcuts.png", "快捷键设置初始状态。")],
    },
    "RT-01-013": {
        "resource": "TSYSTEMSETTINGSFM",
        "entry": "设置 -> 系统设置",
        "steps": ["打开设置菜单", "选择系统设置", "观察系统、网络、备份和高级", "关闭取消"],
        "states": [
            (
                "系统、网络和备份",
                "可配置更新检查、音效、任务栏或托盘、最小化保护、离线模式、代理、同步压缩和备份目录/优化/压缩。",
                [screenshot("b01-system-settings-system.png")],
            ),
            (
                "高级",
                "可配置显示缓存、交易高亮、统计金额隐藏、报表自动查询和报表单元格定制；授权区敏感值未截图。",
                [screenshot("b01-system-settings-advanced.png")],
            ),
        ],
        "commands": [
            command("tvSection", "设置分区", "选择高级分区", "滚动到高级设置区域。", "pass"),
            command("btnChangeSerialPass", "修改序列号保护信息", "打开后只枚举脱敏字段并关闭", "进入 TUpdateVerifyCodeFm。", "pass"),
            command("close", "关闭", "标题栏关闭", "没有提交设置修改。", "pass"),
        ],
        "data_flow": flow(
            ["应用显示、网络、备份、授权和高级偏好"],
            ["应用级设置", "账簿级安全状态", "本地授权状态"],
            ["本轮未执行；不同作用域必须写入独立设置存储"],
            ["下一次启动或当前会话可应用的有效设置"],
            ["授权值只读观察后脱敏，未写入产物"],
            "取消恢复打开前设置；单项应用失败不得污染其它分区。",
        ),
        "requirements": ["应用级、设备级、账簿级和秘密设置必须分库存储并明确应用时机。"],
        "summary": "已动态确认系统、网络、备份、授权入口和高级设置，未保存修改。",
        "gaps": ["设置持久化位置、即时生效项、代理认证、默认值迁移和重启行为"],
        "screenshots": [
            ("b01-system-settings-system.png", "系统、网络和备份设置。"),
            ("b01-system-settings-advanced.png", "高级设置，不含授权值。"),
        ],
    },
    "RT-01-014": {
        "resource": "TUPDATEVERIFYCODEFM",
        "entry": "设置 -> 系统设置 -> 授权 -> 修改序列号保护信息",
        "steps": ["打开系统设置", "进入修改保护信息", "只确认字段数量和窗体类", "关闭取消"],
        "states": [
            (
                "保护信息修改",
                "真实窗体类为 TUpdateVerifyCodeFm，包含三个文本输入和确定按钮；所有输入内容按秘密处理并脱敏。",
                [NOTES, STATIC_CATALOG],
            )
        ],
        "commands": [command("btnEnter", "确定", "未点击", "序列号保护信息未改变。", "partial")],
        "data_flow": flow(
            ["序列号", "旧保护信息", "新保护信息"],
            ["本地授权状态"],
            ["本轮未执行；秘密只允许写入授权秘密存储"],
            ["更新后的授权恢复凭据"],
            ["未记录、未截图、未提交任何秘密值"],
            "取消保留原保护信息；失败不得使现有许可失效。",
        ),
        "requirements": ["秘密输入必须遮罩、禁止日志记录，并提供明确的恢复和失败回滚路径。"],
        "summary": "已动态到达保护信息修改页并完成脱敏结构观察，未提交。",
        "gaps": ["旧保护信息校验、复杂度、错误提示、找回流程和服务端协议"],
    },
    "RT-01-015": {
        "resource": "TSPLASHFORM",
        "entry": "应用启动阶段的短时启动画面",
        "reachable": False,
        "unreachable_reason": "本轮等待到稳定主窗口后未捕获到可交互 SplashForm；静态资源只有启动画面外壳。",
        "states": [
            (
                "启动过渡",
                "目标进程最终进入 test - 财智8；SplashForm 不承担业务输入或持久化。",
                [screenshot("b01-main-baseline.png"), STATIC_CATALOG],
            )
        ],
        "summary": "启动画面是短时过渡状态，Rust 版只在真实初始化耗时时显示。",
        "gaps": ["最短显示时长、初始化错误、无账簿启动和无障碍提示"],
    },
}


def build_record(execution_id: str, spec: dict) -> dict:
    """把紧凑规格转换为统一运行记录。"""

    states = [
        {
            "name": name,
            "status": "observed",
            "observations": observations,
            "evidence_paths": paths,
        }
        for name, observations, paths in spec["states"]
    ]
    screenshots = [
        evidence("screenshot", screenshot(name), description)
        for name, description in spec.get("screenshots", [])
    ]
    record_evidence = screenshots + [
        evidence("manual_note", NOTES, "B01 动态验证边界、脱敏规则和文件指纹。"),
        evidence("manual_note", CONTRACT, "Rust 账簿生命周期、安全、设置和授权合同。"),
        evidence("manual_note", STATIC_CATALOG, "旧窗体静态控件和命令目录。"),
    ]
    default_flow = flow(
        ["页面导航和用户输入"],
        ["应用或账簿当前状态"],
        ["本轮未提交任何页面修改"],
        ["页面显示或本地草稿"],
        ["关闭页面后未观察到业务对象变更"],
        "取消或关闭时丢弃草稿并恢复进入前状态。",
    )
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
            "steps": spec.get("steps", ["核对入口条件", "观察静态资源", "记录未覆盖条件"]),
            "reachable": spec.get("reachable", True),
            "unreachable_reason": spec.get("unreachable_reason"),
        },
        "states": states,
        "commands": spec.get("commands", []),
        "data_flow": spec.get("data_flow", default_flow),
        "evidence": record_evidence,
        "requirements_update": COMMON_REQUIREMENTS + spec.get("requirements", []),
        "result": {
            "status": "partial",
            "summary": spec["summary"],
            "remaining_gaps": spec["gaps"],
        },
    }


def main() -> None:
    """写出 15 条 B01 运行记录。"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for execution_id, spec in SPECS.items():
        output_path = OUTPUT_DIR / f"{execution_id}-{OUTPUT_STAMP}.json"
        output_path.write_text(
            json.dumps(build_record(execution_id, spec), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"generated {len(SPECS)} B01 records")


if __name__ == "__main__":
    main()
