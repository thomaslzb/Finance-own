from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-30T19:50:16+08:00"
STAMP = "20260730T195016+0800"
BASELINE_SHA = "D8E4AE302231A7A9B99B06D28C4D83500F8CD32D95F003814039E91EB0E165AC"
AFTER_SHA = "EFBA4CA8536F1DA37587909C03FE1250F1FA753F71E726ADD680E501418DF054"
DELETE_OBSERVED_AT = "2026-07-31T09:05:21+08:00"
DELETE_STAMP = "20260731T090521+0800"
DELETE_BEFORE_SHA = "EFBA4CA8536F1DA37587909C03FE1250F1FA753F71E726ADD680E501418DF054"
DELETE_AFTER_SHA = "5EF7633C4A850F5551882DECC4CA06B9C3E9EC4316B33725BDC95144B725D4CD"
MULTIDATE_OBSERVED_AT = "2026-07-31T10:39:38+08:00"
MULTIDATE_STAMP = "20260731T103938+0800"
MULTIDATE_BEFORE_SHA = "EFBA4CA8536F1DA37587909C03FE1250F1FA753F71E726ADD680E501418DF054"
MULTIDATE_AFTER_CLOSE_SHA = "DFC88AE9C7E96FD96DD2AE3BB012D6624B8BFA8D301ACEAD7A9E59511609C6E0"
MULTIDATE_AFTER_REOPEN_SHA = "76325EAEC5E3B95258B92F4D07190E7DADF0413E4C71D60AF1CA87FA27FD2AA1"
NONLATEST_OBSERVED_AT = "2026-07-31T11:53:56+08:00"
NONLATEST_STAMP = "20260731T115356+0800"
NONLATEST_BEFORE_SHA = "EFBA4CA8536F1DA37587909C03FE1250F1FA753F71E726ADD680E501418DF054"
NONLATEST_AFTER_CLOSE_SHA = "FD380D74968AF04802C4B28DF87444A65CC43CF9569B026B3525DBAEAE59152D"
NONLATEST_AFTER_REOPEN_SHA = "4D4255F106196008B2C0EECFA86965B74E3E1960884427E468E77D3481F4067B"
DATE_BOUNDARY_OBSERVED_AT = "2026-07-31T12:12:37+08:00"
DATE_BOUNDARY_STAMP = "20260731T121237+0800"
DATE_BOUNDARY_BEFORE_SHA = "EFBA4CA8536F1DA37587909C03FE1250F1FA753F71E726ADD680E501418DF054"
DATE_BOUNDARY_AFTER_CLOSE_SHA = "14045F16DB95DFE20B2686A69A84904D83114F3363F521C79E87C51EEC847788"
DATE_BOUNDARY_AFTER_REOPEN_SHA = "A99AADD1BE59219037A166482E3B84A02F46E7A36C444FD38C309D9994B71236"
AMOUNT_BOUNDARY_OBSERVED_AT = "2026-07-31T12:42:08+08:00"
AMOUNT_BOUNDARY_STAMP = "20260731T124208+0800"
AMOUNT_BOUNDARY_BEFORE_SHA = "EFBA4CA8536F1DA37587909C03FE1250F1FA753F71E726ADD680E501418DF054"
AMOUNT_BOUNDARY_AFTER_CLOSE_SHA = "325155C2ABDC24B5E485FD6C2721627526DF04DD6C9B70EECA8792A0A7BC3D6F"
AMOUNT_BOUNDARY_AFTER_REOPEN_SHA = "F915EDFEC920E753FF34D2DABC543C4C4EBA9738C6FBD5F2DC34AEA9A14E54F3"


def base_record(execution_id: str, resource: str, entry_point: str) -> dict:
    """创建 B13 记录共享的应用、账簿和导航边界。"""
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
            "sha256_after": AFTER_SHA,
            "backup_artifact": "artifacts/runtime-validation/backups/test-before-b13-cash-value-calibration-20260730.mh8",
        },
        "navigation": {
            "entry_point": entry_point,
            "steps": [
                "仅在 PID 3432 的专用 MoneyHome8 实例中操作指定测试账簿",
                "创建投保金额 100.00、已缴保费 10.00 的人民币临时商业保险账户",
                "验证开户交易、同日现金价值新增覆盖、修改和跨页刷新",
                "正常退出后保留写入态副本，并用操作前备份恢复测试账簿",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
    }


def legacy_value_record(execution_id: str, resource: str, title: str) -> dict:
    """记录当前版本无入口、由现金价值快照页替代的旧对话框。"""
    record = base_record(execution_id, resource, f"商业保险账户 -> 查找 {title} 入口")
    record["navigation"].update(
        reachable=False,
        unreachable_reason=(
            "MoneyHome8 8.50.0.0 的账户操作、保险记账和现金价值页均无该命令；"
            "当前版本使用按日期现金价值快照维护。"
        ),
    )
    record.update(
        states=[
            {
                "name": "旧资源结构",
                "status": "observed",
                "observations": f"{title} DFM 仅包含保险账户和金额字段，类只发布 FormCreate。",
                "evidence_paths": ["docs/runtime-dfm-control-catalog.md"],
            },
            {
                "name": "现行替代页面",
                "status": "observed",
                "observations": "现金价值页按日期提供添加、修改和删除，不暴露增减金额命令。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-commercial-insurance-cash-value-tab-sanitized.png"
                ],
            },
            {
                "name": "动态可达性",
                "status": "not_applicable",
                "observations": "穷举现行账户操作、记账和现金价值菜单后未发现用户入口。",
                "evidence_paths": [
                    "artifacts/runtime-validation/b13-commercial-insurance-account-operation-menu.png",
                    "artifacts/runtime-validation/b13-insurance-bookkeeping-menu-deep.png",
                ],
            },
        ],
        commands=[
            {
                "component": "现行保险工作区",
                "label": title,
                "initial_state": {"enabled": False, "visible": False},
                "trigger": "穷举账户操作、保险记账和现金价值命令",
                "confirmation": None,
                "outcome": "未发现可触发命令，功能由现金价值快照维护替代。",
                "status": "not_applicable",
            }
        ],
        data_flow={
            "inputs": ["旧资源字段候选：保险账户、金额"],
            "reads": ["保险账户当前现金价值"],
            "writes": ["当前版本没有该旧 UI 的动态写入入口"],
            "derived_results": ["旧数据迁移时转换为迁移事件或现金价值快照"],
            "side_effects": ["本轮未提交现金价值或保险业务交易"],
            "rollback": "迁移转换与现金价值快照写入必须原子化，失败不得留下半成品。",
        },
        evidence=[
            {
                "kind": "manual_note",
                "path": "artifacts/runtime-validation/B13-pending-close-notes.md",
                "description": "B13 入口穷举、进程隔离、临时账户删除和账簿恢复记录。",
            },
            {
                "kind": "manual_note",
                "path": "docs/runtime-insurance-and-social-security-contract.md",
                "description": "Rust 保险、社保、现金价值和旧数据迁移合同。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-commercial-insurance-cash-value-tab-sanitized.png",
                "description": "现行现金价值快照页面。",
            },
        ],
        requirements_update=[
            "Rust 不复刻当前版本不可达的保险价值增减对话框。",
            "现金价值按估值日保存快照，并保留新增、修改、删除审计。",
            "旧库价值增减事实迁移为显式迁移事件或可追溯快照。",
            "现金价值变化不得自动推断为资金流水或已实现收益。",
        ],
        result={
            "status": "unreachable",
            "summary": f"{title} 旧资源在当前版本无用户入口，现行功能由按日期现金价值快照页替代。",
            "remaining_gaps": [
                "是否仍存在历史插件或外部命令入口",
                "旧价值增减数据的正式迁移样例",
                "现金价值真实保存、同日覆盖和失败回滚",
            ],
        },
    )
    return record


def transaction_workspace_record() -> dict:
    """记录保险交易工作区和最终宿主的动态组合证据。"""
    record = base_record(
        "RT-13-010", "TINSURETRANSFM", "账户中心 -> 临时商业保险账户 -> 交易明细"
    )
    record.update(
        states=[
            {
                "name": "最终宿主",
                "status": "observed",
                "observations": "保险账户真实进入共享工作区，运行宿主报告为 TSocialSecurityTransFm，内部交易区域为 TInsureTransFrame。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-pending-transaction-workspace-sanitized.png"
                ],
            },
            {
                "name": "空交易",
                "status": "observed",
                "observations": "交易明细显示没有交易记录，查找禁用，记录数和底部金额汇总为零。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-pending-transaction-workspace-sanitized.png"
                ],
            },
            {
                "name": "页签与查询",
                "status": "observed",
                "observations": "工作区提供交易明细、现金价值和账户概况页签，并保留日期范围、记账和操作入口。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-pending-transaction-workspace-sanitized.png"
                ],
            },
        ],
        commands=[
            {
                "component": "交易明细命令区",
                "label": "查找",
                "initial_state": {"enabled": False, "visible": True},
                "trigger": "零记录状态观察",
                "confirmation": None,
                "outcome": "无交易时保持禁用。",
                "status": "pass",
            },
            {
                "component": "交易明细命令区",
                "label": "记账",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "打开保险记账菜单",
                "confirmation": None,
                "outcome": "显示缴纳保费、保费返还、退保和保险分红。",
                "status": "pass",
            },
        ],
        data_flow={
            "inputs": ["保险账户选择、日期范围和可选交易筛选"],
            "reads": ["保险事件、现金价值快照、账户资料和查询汇总"],
            "writes": ["本轮未提交交易；记账命令应通过专用事件编辑器写入"],
            "derived_results": ["记录数、缴费总额、领取总额和当前现金价值"],
            "side_effects": ["只创建并删除零余额临时账户，退出后恢复账簿基线"],
            "rollback": "保险事件、资金分录、保单状态和计划变更必须同事务回滚。",
        },
        evidence=[
            {
                "kind": "manual_note",
                "path": "artifacts/runtime-validation/B13-pending-close-notes.md",
                "description": "B13 动态工作区、类组合、临时账户和恢复记录。",
            },
            {
                "kind": "manual_note",
                "path": "docs/runtime-insurance-and-social-security-contract.md",
                "description": "Rust 保险与社保领域合同。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-pending-transaction-workspace-sanitized.png",
                "description": "脱敏后的保险交易工作区空状态。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/b13-insurance-bookkeeping-menu-deep.png",
                "description": "保险记账专用事件菜单。",
            },
        ],
        requirements_update=[
            "保险工作区的账户列表、交易、现金价值和概况共享账户选择与查询时点。",
            "空状态不得生成占位交易，汇总必须逐分为零。",
            "缴费、返还、分红和退保保存不同事件类型，不能用金额方向推断。",
            "交易、资金、保单状态和缴费计划变更必须原子提交。",
        ],
        result={
            "status": "partial",
            "summary": "已动态确认保险交易工作区的最终宿主、空状态、页签、查询和记账入口。",
            "remaining_gaps": [
                "有数据列表、排序、筛选和导出打印",
                "真实缴费、返还、分红和退保写入",
                "精确金额、状态迁移和失败回滚",
            ],
        },
    )
    return record


def cash_value_calibration_records() -> list[dict]:
    """记录商业保险现金价值真实保存及其跨页面投影。"""
    shared_evidence = [
        {
            "kind": "manual_note",
            "path": "artifacts/runtime-validation/B13-pending-close-notes.md",
            "description": "B13 现金价值真实写入、退出态副本和账簿恢复记录。",
        },
        {
            "kind": "hash",
            "path": "artifacts/runtime-validation/backups/test-after-b13-cash-value-calibration-before-restore-20260730.mh8",
            "description": f"真实写入后的账簿副本，SHA-256 为 {AFTER_SHA}。",
        },
    ]

    editor = base_record(
        "RT-13-004",
        "TINSURECASHVALUEEDITDLGFM",
        "商业保险工作区 -> 现金价值 -> 添加或修改",
    )
    editor.update(
        states=[
            {
                "name": "新增初始值",
                "status": "observed",
                "observations": "新增编辑器默认日期为 2026-07-30、现金价值为 0.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/b13-cash-calibration-value-add-dialog.png"
                ],
            },
            {
                "name": "同日新增保存",
                "status": "observed",
                "observations": "在已有开户日 0.00 行时以相同日期保存 8.00，未提示重复且仍只有一行，证明同账户同日新增采用覆盖更新。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-calibration-value-after-same-day-add-sanitized.png"
                ],
            },
            {
                "name": "修改保存",
                "status": "observed",
                "observations": "修改编辑器回填 2026-07-30 和 8.00；保存 9.00 后原行、当前余额和趋势图同步更新。",
                "evidence_paths": [
                    "artifacts/runtime-validation/b13-cash-calibration-value-modify-filled.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-calibration-value-after-modify-sanitized.png",
                ],
            },
            {
                "name": "其它日期与非法金额",
                "status": "pending",
                "observations": "Delphi 日期控件不接受 WM_SETTEXT 作为绑定值变更；本轮未取得未来/历史日期、负值或非法精度的有效业务证据。",
            },
        ],
        commands=[
            {
                "component": "现金价值编辑器",
                "label": "确定（新增）",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "在开户日输入 8.00 并确定",
                "confirmation": None,
                "outcome": "覆盖开户日 0.00 快照为 8.00，不新增重复日期行。",
                "status": "pass",
            },
            {
                "component": "现金价值编辑器",
                "label": "确定（修改）",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "把已选快照从 8.00 修改为 9.00 并确定",
                "confirmation": None,
                "outcome": "更新同一日期快照并刷新账户余额和趋势图。",
                "status": "pass",
            },
            {
                "component": "现金价值页",
                "label": "删除",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "本轮未触发 UI 删除",
                "confirmation": None,
                "outcome": "删除确认、回退当前值和图表重算仍待验证。",
                "status": "pending",
            },
        ],
        data_flow={
            "inputs": ["保险账户 ID", "价值日期", "现金价值"],
            "reads": ["同账户同日现金价值快照", "现金价值时间序列"],
            "writes": ["同日新增执行快照 upsert", "修改执行快照 update"],
            "derived_results": ["当前现金价值", "保险账户余额投影", "现金价值趋势图"],
            "side_effects": ["不新增保险交易", "不改变缴费总额、领取总额和交易记录数"],
            "rollback": "快照写入与当前值、账户余额和图表刷新必须原子一致；失败时保留旧快照及全部旧投影。",
        },
        evidence=shared_evidence
        + [
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/b13-cash-calibration-value-add-filled.png",
                "description": "开户日现金价值 8.00 的新增保存输入。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/b13-cash-calibration-value-modify-filled.png",
                "description": "同一快照从 8.00 修改为 9.00 的保存输入。",
            },
        ],
        requirements_update=[
            "同一保险账户和估值日只保留一个有效现金价值快照；新增同日值必须按可审计 upsert 处理。",
            "现金价值修改只改变估值快照及其投影，不得伪造保险交易或资金流水。",
            "日期控件自动化失败不能作为日期业务规则证据，历史与未来日期策略继续保持待校准。",
        ],
        result={
            "status": "partial",
            "summary": "已真实验证现金价值同日新增覆盖和修改保存，以及余额、表格和趋势图联动。",
            "remaining_gaps": ["删除及确认", "历史和未来日期", "负值与精度校验", "并发冲突和失败回滚"],
        },
    )

    frame = base_record("RT-13-005", "TINSURECASHVALUEFRAME", "商业保险工作区 -> 现金价值")
    frame.update(
        states=[
            {
                "name": "开户日初始快照",
                "status": "observed",
                "observations": "开户后自动存在 2026-07-30 / 0.00 快照，账户余额为 0.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-calibration-workspace-before-value-sanitized.png"
                ],
            },
            {
                "name": "同日覆盖",
                "status": "observed",
                "observations": "添加 8.00 后仍只有 2026-07-30 一行，账户列表余额、快照表和图表同时显示 8.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-calibration-value-after-same-day-add-sanitized.png"
                ],
            },
            {
                "name": "修改刷新",
                "status": "observed",
                "observations": "修改为 9.00 后，账户列表余额、快照表、纵轴范围和数据点同步变为 9.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-calibration-value-after-modify-sanitized.png"
                ],
            },
        ],
        commands=[
            {
                "component": "现金价值页",
                "label": "添加",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "选择开户日 0.00 行后添加同日 8.00",
                "confirmation": None,
                "outcome": "同日覆盖并刷新表格、余额和图表。",
                "status": "pass",
            },
            {
                "component": "现金价值页",
                "label": "修改",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "选中 8.00 行并修改为 9.00",
                "confirmation": None,
                "outcome": "原行和跨组件投影同步更新。",
                "status": "pass",
            },
            {
                "component": "现金价值页",
                "label": "删除",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "未执行",
                "confirmation": None,
                "outcome": "保留待验证。",
                "status": "pending",
            },
        ],
        data_flow={
            "inputs": ["保险账户", "估值日", "现金价值"],
            "reads": ["按日快照序列"],
            "writes": ["单日唯一现金价值快照"],
            "derived_results": ["当前现金价值", "账户余额投影", "趋势图序列"],
            "side_effects": ["交易页现金价值汇总刷新", "交易行和累计缴费保持不变"],
            "rollback": "快照和所有读模型必须在提交后统一刷新，任何失败均不得产生混合新旧投影。",
        },
        evidence=shared_evidence
        + [
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-calibration-value-after-same-day-add-sanitized.png",
                "description": "同日新增覆盖后的单行快照、8.00 余额和趋势图。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-calibration-value-after-modify-sanitized.png",
                "description": "修改为 9.00 后的单行快照、余额和趋势图。",
            },
        ],
        requirements_update=[
            "现金价值页按账户和日期执行唯一键 upsert，表格、账户余额、底部汇总和图表读取同一提交版本。",
            "现金价值是估值投影，不计入缴费、领取或交易记录数。",
        ],
        result={
            "status": "partial",
            "summary": "已真实验证现金价值页的同日覆盖、修改和跨组件刷新。",
            "remaining_gaps": ["删除和回退规则", "多日期趋势", "统计口径关闭状态", "失败回滚"],
        },
    )

    transaction_state = {
        "name": "开户交易与现金价值独立",
        "status": "observed",
        "observations": "向导已缴保费 10.00 生成一条 2026-07-30 余额调整，缴费 10.00、领取 0.00、记录数 1；现金价值改为 9.00 后该交易及缴费汇总不变。",
        "evidence_paths": [
            "artifacts/runtime-validation/screenshots/b13-cash-calibration-transaction-after-value-modify-sanitized.png"
        ],
    }
    transaction_records = []
    for execution_id, resource, entry_point in [
        ("RT-13-010", "TINSURETRANSFM", "商业保险账户 -> 交易明细最终宿主"),
        ("RT-13-011", "TINSURETRANSFRAME", "商业保险工作区 -> 交易明细"),
    ]:
        record = base_record(execution_id, resource, entry_point)
        record.update(
            states=[transaction_state],
            commands=[
                {
                    "component": "交易明细页签",
                    "label": "切换并刷新",
                    "initial_state": {"enabled": True, "visible": True},
                    "trigger": "现金价值修改后切回交易明细",
                    "confirmation": None,
                    "outcome": "现金价值显示 9.00；原余额调整、缴费 10.00 和记录数 1 保持不变。",
                    "status": "pass",
                }
            ],
            data_flow={
                "inputs": ["开户已缴保费", "保险账户", "查询日期范围"],
                "reads": ["保险交易", "现金价值当前快照"],
                "writes": ["开户时写入余额调整保险交易", "本页签切换不写入"],
                "derived_results": ["缴费总额 10.00", "领取总额 0.00", "记录数 1", "现金价值 9.00"],
                "side_effects": ["现金价值快照变化只刷新现金价值汇总"],
                "rollback": "开户交易与账户创建必须原子提交；快照修改不能改写保险交易。",
            },
            evidence=shared_evidence
            + [
                {
                    "kind": "screenshot",
                    "path": "artifacts/runtime-validation/screenshots/b13-cash-calibration-transaction-after-value-modify-sanitized.png",
                    "description": "现金价值 9.00 与单条缴费余额调整 10.00 并存的交易页。",
                }
            ],
            requirements_update=[
                "开户已缴保费应保存为显式保险初始调整事件并计入缴费汇总。",
                "现金价值快照与保险交易是独立事实，不能互相推导或覆盖。",
            ],
            result={
                "status": "partial",
                "summary": "已验证非零开户交易及现金价值修改后的交易独立性。",
                "remaining_gaps": ["代表性缴费、返还、分红和退保保存", "筛选排序和导出", "失败回滚"],
            },
        )
        transaction_records.append(record)

    wizard = base_record(
        "RT-13-012",
        "TNEWACCTWIZARDINSURECOMMERCEDLGFM",
        "账户中心 -> 新增账户 -> 商业保险",
    )
    wizard.update(
        states=[
            {
                "name": "非零保费开户",
                "status": "observed",
                "observations": "人身保险账户以投保金额 100.00、已缴保费 10.00、年缴金额 10.00、无缴费账户和仅做提醒完成创建。",
                "evidence_paths": [
                    "artifacts/runtime-validation/b13-cash-calibration-wizard-page3.png",
                    "artifacts/runtime-validation/b13-cash-calibration-wizard-page4.png",
                ],
            },
            transaction_state,
        ],
        commands=[
            {
                "component": "商业保险向导",
                "label": "完成",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "提交投保金额 100.00 和已缴保费 10.00",
                "confirmation": None,
                "outcome": "创建账户、开户日零现金价值快照和一条缴费 10.00 的余额调整。",
                "status": "pass",
            }
        ],
        data_flow={
            "inputs": ["保险类别", "账户资料", "投保金额", "已缴保费", "缴费频率与金额", "提醒策略"],
            "reads": ["币种", "人员与机构候选", "可选资金账户"],
            "writes": ["保险账户", "保单资料", "开户日 0.00 现金价值快照", "10.00 初始余额调整保险交易"],
            "derived_results": ["账户投保金额 100.00", "累计缴费 10.00", "现金价值 0.00"],
            "side_effects": ["无缴费账户时未观察到资金账户分录", "仅做提醒策略已保存但提醒实例未核验"],
            "rollback": "账户、保单、初始交易、现金价值快照和提醒配置必须单事务提交。",
        },
        evidence=shared_evidence
        + [
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/b13-cash-calibration-wizard-page4.png",
                "description": "已缴保费 10.00、年缴 10.00、无缴费账户和仅做提醒。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-calibration-workspace-before-value-sanitized.png",
                "description": "开户后现金价值 0.00 与缴费 10.00、记录数 1 的初始状态。",
            },
        ],
        requirements_update=[
            "向导已缴保费是开户事件输入，不是现金价值；二者必须分别持久化和投影。",
            "未选择资金账户时不得伪造资金分录，迁移与 UI 应明确该初始调整的来源。",
        ],
        result={
            "status": "partial",
            "summary": "已验证非零投保金额和已缴保费开户，以及初始交易与零现金价值快照。",
            "remaining_gaps": [
                "固定扣款独立修改、后台执行和冷启动；提醒跳过与手工执行已由 RT-15-037 补证",
                "三类保险差异",
                "重复与必填校验",
                "失败回滚",
            ],
        },
    )

    statistic = base_record(
        "RT-13-014",
        "TSOCIALSECURITYSTATISTICFRAME",
        "商业保险共享工作区 -> 上部账户统计区",
    )
    statistic.update(
        states=[
            {
                "name": "估值余额联动",
                "status": "observed",
                "observations": "同一保单统计行从 0.00 随现金价值新增变为 8.00，修改后变为 9.00；投保金额 100.00 未作为余额。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-calibration-value-after-modify-sanitized.png"
                ],
            }
        ],
        commands=[
            {
                "component": "账户统计区",
                "label": "选择保单",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "现金价值保存后观察选中行",
                "confirmation": None,
                "outcome": "余额按当前现金价值刷新为 9.00。",
                "status": "pass",
            }
        ],
        data_flow={
            "inputs": ["保险账户 ID", "查询时点"],
            "reads": ["不晚于查询时点的当前现金价值快照"],
            "writes": ["统计区不直接写入"],
            "derived_results": ["保险账户余额 9.00"],
            "side_effects": ["选中行驱动下部三个页签"],
            "rollback": "快照保存失败时统计区不得提前显示未提交值。",
        },
        evidence=shared_evidence
        + [
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-calibration-value-after-modify-sanitized.png",
                "description": "上部保险账户统计余额与当前现金价值均为 9.00。",
            }
        ],
        requirements_update=["保险账户余额投影取当前现金价值，不取投保金额或累计缴费。"],
        result={
            "status": "partial",
            "summary": "已验证商业保险统计行余额由当前现金价值驱动。",
            "remaining_gaps": ["多保单聚合", "多日期查询时点", "删除后的余额回退", "失败回滚"],
        },
    )

    host = base_record(
        "RT-13-015",
        "TSOCIALSECURITYTRANSFM",
        "账户中心 -> 商业保险账户 -> 共享工作区",
    )
    host.update(
        states=[
            {
                "name": "跨页一致性",
                "status": "observed",
                "observations": "共享宿主在现金价值页保存后同步刷新上部余额；切回交易页显示现金价值 9.00，同时缴费 10.00 和记录数 1 不变。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-calibration-value-after-modify-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-calibration-transaction-after-value-modify-sanitized.png",
                ],
            }
        ],
        commands=[
            {
                "component": "共享页签",
                "label": "交易明细 / 现金价值",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "保存快照后往返切换",
                "confirmation": None,
                "outcome": "账户选择、现金价值、缴费汇总和交易记录保持一致。",
                "status": "pass",
            }
        ],
        data_flow={
            "inputs": ["选中保险账户", "查询日期范围", "当前估值日"],
            "reads": ["保险交易", "现金价值快照", "账户资料"],
            "writes": ["通过子页面命令写入领域对象"],
            "derived_results": ["账户余额", "现金价值", "缴费与领取汇总", "交易记录数"],
            "side_effects": ["保存后刷新共享账户上下文中的全部相关投影"],
            "rollback": "子命令失败时宿主必须保留同一已提交版本，不能跨页展示不一致数据。",
        },
        evidence=shared_evidence
        + [
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-calibration-transaction-after-value-modify-sanitized.png",
                "description": "共享宿主中交易与估值的独立且一致投影。",
            }
        ],
        requirements_update=["共享工作区必须在写入后以同一提交版本刷新账户统计、交易汇总和现金价值投影。"],
        result={
            "status": "partial",
            "summary": "已验证商业保险共享宿主的非零跨页一致性。",
            "remaining_gaps": ["账户概况写入", "社保非零跨页一致性", "并发刷新", "失败回滚"],
        },
    )

    return [editor, frame, *transaction_records, wizard, statistic, host]


def cash_value_delete_record() -> dict:
    """记录删除唯一现金价值快照后的持久化结果和旧程序读模型缺陷。"""
    return {
        "schema_version": 1,
        "execution_id": "RT-13-005",
        "resource": "TINSURECASHVALUEFRAME",
        "observed_at": DELETE_OBSERVED_AT,
        "application": {
            "executable": "C:\\Program Files (x86)\\MoneyWise\\MoneyHome8\\Program\\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": "C:\\DCG-SZ\\IT Manage\\Private\\Personal-Docs\\test.mh8",
            "sha256_before": DELETE_BEFORE_SHA,
            "sha256_after": DELETE_AFTER_SHA,
            "backup_artifact": "artifacts/runtime-validation/backups/test-before-b13-cash-value-delete-20260731.mh8",
        },
        "navigation": {
            "entry_point": "账户中心 -> 商业保险账户 -> 共享工作区 -> 现金价值",
            "steps": [
                "从现金价值校准副本加载 Codex-B13-Cash-20260730 保单",
                "点击账户名称进入 TSocialSecurityTransFm，并切换到现金价值页",
                "选中唯一的 2026-07-30 / 11.00 快照并点击删除",
                "正常关闭后保留写入态副本，重新打开测试账簿复核各投影",
                "保留重开态副本后，用操作前备份恢复 test.mh8 基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "删除前",
                "status": "observed",
                "observations": "唯一快照为 2026-07-30 / 11.00；账户余额、交易页现金价值汇总和趋势图数据点均为 11.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-delete-value-before-sanitized.png"
                ],
            },
            {
                "name": "删除后当前会话",
                "status": "observed",
                "observations": "没有确认框；快照表清空，修改和删除禁用，图表归零，但账户余额与交易页现金价值汇总错误变为 1.00。初始缴费交易、缴费 10.00、领取 0.00 和记录数 1 均未改变。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-delete-value-after-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-delete-transaction-after-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-delete-account-center-after-sanitized.png",
                ],
            },
            {
                "name": "重新打开账簿",
                "status": "observed",
                "observations": "被删快照仍未恢复，表格为空且图表为零；账户中心、工作区余额和交易页现金价值汇总却回到 11.00，证明旧程序各读模型跨重启不一致。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-delete-account-center-after-reopen-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-delete-value-after-reopen-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-delete-transaction-after-reopen-sanitized.png",
                ],
            },
            {
                "name": "测试库恢复",
                "status": "observed",
                "observations": "退出 MoneyHome8 后从专用备份恢复 test.mh8，文件长度和 SHA-256 均回到操作前基线。",
                "evidence_paths": ["artifacts/runtime-validation/B13-pending-close-notes.md"],
            },
        ],
        "commands": [
            {
                "component": "现金价值页",
                "label": "删除",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "选中唯一的 2026-07-30 / 11.00 快照并点击删除",
                "confirmation": "未出现确认对话框，命令立即执行。",
                "outcome": "快照行持久删除，但当前会话投影为 1.00，重开后投影为 11.00，而表格和图表持续为空/零。",
                "status": "fail",
            }
        ],
        "data_flow": {
            "inputs": ["保险保单 ID", "估值日 2026-07-30", "选中的现金价值 11.00"],
            "reads": ["现金价值快照序列", "保险当前值投影", "账户余额投影", "保险交易汇总"],
            "writes": ["删除唯一现金价值快照", "持久化删除后的旧程序内部状态（具体表结构未确认）"],
            "derived_results": ["当前现金价值", "保险账户余额", "交易页现金价值汇总", "趋势图", "总资产"],
            "side_effects": ["保险初始缴费事件和交易不变", "缴费总额、领取总额和记录数不变"],
            "rollback": "验证结束后关闭旧程序，并用 test-before-b13-cash-value-delete-20260731.mh8 恢复唯一测试账簿。",
        },
        "evidence": [
            {
                "kind": "manual_note",
                "path": "artifacts/runtime-validation/B13-pending-close-notes.md",
                "description": "现金价值删除、重开复核、写入态指纹和基线恢复记录。",
            },
            {
                "kind": "hash",
                "path": "artifacts/runtime-validation/backups/test-after-b13-cash-value-delete-before-reopen-20260731.mh8",
                "description": "删除后首次正常退出副本，SHA-256 为 1BA60F2602E43FE093E77D814FB21DD6E894D58B0935A5A90A669F04AFCF1AD9。",
            },
            {
                "kind": "hash",
                "path": "artifacts/runtime-validation/backups/test-after-b13-cash-value-delete-reopen-before-restore-20260731.mh8",
                "description": f"重开复核并退出后的副本，SHA-256 为 {DELETE_AFTER_SHA}。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-delete-value-before-sanitized.png",
                "description": "删除前快照、账户余额和趋势图均为 11.00。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-delete-value-after-sanitized.png",
                "description": "删除后表格为空、图表归零但账户余额错误显示 1.00。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-delete-value-after-reopen-sanitized.png",
                "description": "重开后表格仍为空、图表仍为零，但账户余额错误回到 11.00。",
            },
        ],
        "requirements_update": [
            "删除现金价值快照必须显式、可审计，并在同一事务提交后重新计算最新有效快照。",
            "删除唯一快照后，当前现金价值、账户余额、交易页汇总和趋势图必须统一为 0。",
            "不得把快照删除实现为对缓存余额的独立增量修改；所有投影必须从快照事实重建。",
            "删除后和重新启动后，全部组件必须读取同一已提交版本。",
            "删除现金价值不得新增、删除或改写保险交易，也不得改变缴费、领取和记录数。",
        ],
        "result": {
            "status": "partial",
            "summary": "已验证唯一现金价值快照可无确认删除并持久缺失，同时确认旧程序存在当前会话 1.00、重开 11.00、表格/图表为零的跨读模型不一致缺陷。",
            "remaining_gaps": [
                "多日期删除后的上一有效快照回退",
                "旧程序恢复文件是否参与当前值重建及数据库根因",
                "历史/未来日期、负值和金额精度",
                "并发版本冲突、重复提交和持久化失败回滚",
            ],
        },
    }


def cash_value_multidate_delete_record() -> dict:
    """记录删除最新现金价值后上一快照回退及重启投影缺陷。"""
    return {
        "schema_version": 1,
        "execution_id": "RT-13-005",
        "resource": "TINSURECASHVALUEFRAME",
        "observed_at": MULTIDATE_OBSERVED_AT,
        "application": {
            "executable": "C:\\Program Files (x86)\\MoneyWise\\MoneyHome8\\Program\\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": "C:\\DCG-SZ\\IT Manage\\Private\\Personal-Docs\\test.mh8",
            "sha256_before": MULTIDATE_BEFORE_SHA,
            "sha256_after": MULTIDATE_AFTER_REOPEN_SHA,
            "backup_artifact": "artifacts/runtime-validation/backups/test-before-b13-cash-value-multidate-20260731.mh8",
        },
        "navigation": {
            "entry_point": "账户中心 -> 商业保险账户 -> 共享工作区 -> 现金价值",
            "steps": [
                "从现金价值校准副本加载 Codex-B13-Cash-20260730 保单",
                "保留 2026-07-30 / 11.00，并用编辑器默认日期新增 2026-07-31 / 13.00",
                "选中最新的 2026-07-31 / 13.00 快照并点击删除",
                "核对现金价值页、交易页和账户余额后正常退出",
                "重新打开同一 test.mh8，复核明细、图表和余额投影",
                "保留重开态副本后，用操作前备份恢复 test.mh8 基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "新增第二日期",
                "status": "observed",
                "observations": "新增 2026-07-31 / 13.00 后列表按日期降序显示 13.00、11.00；账户余额和趋势图最新点同步为 13.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-multidate-after-add-sanitized.png"
                ],
            },
            {
                "name": "删除最新值的当前会话回退",
                "status": "observed",
                "observations": "删除没有确认框；2026-07-31 行消失，剩余 2026-07-30 / 11.00，账户余额、交易页现金价值汇总和趋势图均立即回退为 11.00。缴费 10.00、领取 0.00、记录数 1 和原保险交易不变。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-multidate-after-delete-latest-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-multidate-transaction-after-delete-sanitized.png",
                ],
            },
            {
                "name": "重新打开账簿",
                "status": "observed",
                "observations": "被删的 2026-07-31 行没有恢复，表格和趋势图仍只显示 2026-07-30 / 11.00；但账户中心、工作区余额和交易页现金价值汇总错误回到 13.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-multidate-account-center-after-reopen-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-multidate-value-after-reopen-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-multidate-transaction-after-reopen-sanitized.png",
                ],
            },
            {
                "name": "测试库恢复",
                "status": "observed",
                "observations": "MoneyHome8 正常退出且无锁文件后恢复 test.mh8；长度和 SHA-256 回到操作前基线。",
                "evidence_paths": ["artifacts/runtime-validation/B13-pending-close-notes.md"],
            },
        ],
        "commands": [
            {
                "component": "现金价值页",
                "label": "删除",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "选中最新的 2026-07-31 / 13.00 快照并点击删除",
                "confirmation": "未出现确认对话框，命令立即执行。",
                "outcome": "当前会话正确回退上一快照 11.00；重开后明细仍为 11.00，但余额与汇总错误回填已删除的 13.00。",
                "status": "fail",
            }
        ],
        "data_flow": {
            "inputs": ["保险保单 ID", "估值日 2026-07-31", "选中的现金价值 13.00"],
            "reads": ["现金价值快照序列", "保险当前值投影", "账户余额投影", "保险交易汇总"],
            "writes": ["删除最新现金价值快照", "保留上一日期快照"],
            "derived_results": ["最新有效现金价值", "保险账户余额", "交易页现金价值汇总", "趋势图", "总资产"],
            "side_effects": ["保险初始缴费事件和交易不变", "缴费总额、领取总额和记录数不变"],
            "rollback": "验证结束后关闭旧程序，并用 test-before-b13-cash-value-multidate-20260731.mh8 恢复唯一测试账簿。",
        },
        "evidence": [
            {
                "kind": "manual_note",
                "path": "artifacts/runtime-validation/B13-pending-close-notes.md",
                "description": "多日期新增、删除最新值、重开复核和基线恢复记录。",
            },
            {
                "kind": "hash",
                "path": "artifacts/runtime-validation/backups/test-after-b13-cash-value-multidate-delete-before-reopen-20260731.mh8",
                "description": f"删除后首次退出副本，SHA-256 为 {MULTIDATE_AFTER_CLOSE_SHA}。",
            },
            {
                "kind": "hash",
                "path": "artifacts/runtime-validation/backups/test-after-b13-cash-value-multidate-delete-reopen-before-restore-20260731.mh8",
                "description": f"重开复核并退出后的副本，SHA-256 为 {MULTIDATE_AFTER_REOPEN_SHA}。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-multidate-after-add-sanitized.png",
                "description": "两日期快照按日期降序显示，最新余额和图表点为 13.00。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-multidate-after-delete-latest-sanitized.png",
                "description": "当前会话删除最新值后，明细、余额和图表正确回退到 11.00。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-multidate-value-after-reopen-sanitized.png",
                "description": "重开后明细和图表仍为 11.00，但账户余额错误显示 13.00。",
            },
        ],
        "requirements_update": [
            "当前现金价值必须由估值日最大的有效快照计算；删除最新快照后立即选择上一有效快照。",
            "快照表、趋势图、账户余额、交易页汇总和资产投影必须读取同一提交版本。",
            "不得单独持久化或从恢复状态回填一个可能脱离快照事实的当前现金价值缓存。",
            "删除后重新启动必须从剩余快照确定性重建投影，结果仍为上一有效快照 11.00。",
            "现金价值删除不得新增、删除或改写保险交易，也不得改变缴费、领取和记录数。",
        ],
        "result": {
            "status": "partial",
            "summary": "已验证多日期按日期降序显示及当前会话删除最新值后正确回退 11.00；同时确认重开后明细保持 11.00、余额与汇总错误回到已删除 13.00 的旧程序读模型缺陷。",
            "remaining_gaps": [
                "删除非最新快照及历史/未来查询时点",
                "旧程序恢复文件是否参与当前值重建及数据库根因",
                "负值和金额精度",
                "并发版本冲突、重复提交和持久化失败回滚",
            ],
        },
    }


def cash_value_nonlatest_delete_record() -> dict:
    """记录删除非最新现金价值后当前值与重启投影保持不变。"""
    return {
        "schema_version": 1,
        "execution_id": "RT-13-005",
        "resource": "TINSURECASHVALUEFRAME",
        "observed_at": NONLATEST_OBSERVED_AT,
        "application": {
            "executable": "C:\\Program Files (x86)\\MoneyWise\\MoneyHome8\\Program\\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": "C:\\DCG-SZ\\IT Manage\\Private\\Personal-Docs\\test.mh8",
            "sha256_before": NONLATEST_BEFORE_SHA,
            "sha256_after": NONLATEST_AFTER_REOPEN_SHA,
            "backup_artifact": "artifacts/runtime-validation/backups/test-before-b13-cash-value-delete-nonlatest-20260731.mh8",
        },
        "navigation": {
            "entry_point": "账户中心 -> 商业保险账户 -> 共享工作区 -> 现金价值",
            "steps": [
                "从现金价值校准副本加载 Codex-B13-Cash-20260730 保单",
                "保留 2026-07-30 / 11.00，并新增 2026-07-31 / 13.00",
                "选中较早的 2026-07-30 / 11.00 快照并点击删除",
                "核对现金价值页、交易页和账户余额后正常退出",
                "重新打开同一 test.mh8，复核明细、图表和余额投影",
                "保存重开态副本后，用操作前备份恢复 test.mh8 基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "删除非最新值前",
                "status": "observed",
                "observations": "列表按日期降序显示 2026-07-31 / 13.00 和 2026-07-30 / 11.00；选中较早行时账户余额仍为 13.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-nonlatest-before-delete-selected-sanitized.png"
                ],
            },
            {
                "name": "删除后的当前会话",
                "status": "observed",
                "observations": "删除没有确认框；较早行消失，只保留 2026-07-31 / 13.00。账户余额、交易页现金价值汇总和趋势图均保持 13.00，缴费 10.00、领取 0.00、记录数 1 和原保险交易不变。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-nonlatest-after-delete-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-nonlatest-transaction-after-delete-sanitized.png",
                ],
            },
            {
                "name": "重新打开账簿",
                "status": "observed",
                "observations": "删除结果持久化；现金价值表、趋势图、账户中心、工作区余额和交易页现金价值汇总均保持最新值 13.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-nonlatest-account-center-after-reopen-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-nonlatest-value-after-reopen-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-nonlatest-transaction-after-reopen-sanitized.png",
                ],
            },
            {
                "name": "测试库恢复",
                "status": "observed",
                "observations": "MoneyHome8 正常退出且无锁文件后恢复 test.mh8；长度和 SHA-256 回到操作前基线。",
                "evidence_paths": ["artifacts/runtime-validation/B13-pending-close-notes.md"],
            },
        ],
        "commands": [
            {
                "component": "现金价值页",
                "label": "删除",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "选中非最新的 2026-07-30 / 11.00 快照并点击删除",
                "confirmation": "未出现确认对话框，命令立即执行。",
                "outcome": "较早快照持久删除，最新快照及全部当前值投影在当前会话和重启后均保持 13.00。",
                "status": "pass",
            }
        ],
        "data_flow": {
            "inputs": ["保险保单 ID", "估值日 2026-07-30", "选中的非最新现金价值 11.00"],
            "reads": ["现金价值快照序列", "最大估值日快照", "保险当前值投影", "保险交易汇总"],
            "writes": ["删除非最新现金价值快照", "保留最新日期快照"],
            "derived_results": ["最新有效现金价值", "保险账户余额", "交易页现金价值汇总", "趋势图", "总资产"],
            "side_effects": ["当前现金价值保持 13.00", "保险交易、缴费、领取和记录数不变"],
            "rollback": "验证结束后关闭旧程序，并用 test-before-b13-cash-value-delete-nonlatest-20260731.mh8 恢复唯一测试账簿。",
        },
        "evidence": [
            {
                "kind": "manual_note",
                "path": "artifacts/runtime-validation/B13-pending-close-notes.md",
                "description": "删除非最新现金价值、重开复核和基线恢复记录。",
            },
            {
                "kind": "hash",
                "path": "artifacts/runtime-validation/backups/test-after-b13-cash-value-delete-nonlatest-before-reopen-20260731.mh8",
                "description": f"删除后首次退出副本，SHA-256 为 {NONLATEST_AFTER_CLOSE_SHA}。",
            },
            {
                "kind": "hash",
                "path": "artifacts/runtime-validation/backups/test-after-b13-cash-value-delete-nonlatest-reopen-before-restore-20260731.mh8",
                "description": f"重开复核并退出后的副本，SHA-256 为 {NONLATEST_AFTER_REOPEN_SHA}。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-nonlatest-before-delete-selected-sanitized.png",
                "description": "删除前选中较早的 11.00 快照，最新值为 13.00。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-nonlatest-after-delete-sanitized.png",
                "description": "删除较早快照后只保留最新 13.00，账户余额和图表保持不变。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-nonlatest-value-after-reopen-sanitized.png",
                "description": "重开后明细、图表和账户余额继续一致显示 13.00。",
            },
        ],
        "requirements_update": [
            "删除非最新快照不得改变当前现金价值或任何当前余额投影。",
            "当前现金价值始终由估值日最大的剩余快照派生，与被删历史快照的金额无关。",
            "趋势图删除对应历史数据点后必须保留其它快照，不能重写最新值。",
            "删除结果和当前值在重新启动后必须从同一快照事实重建。",
            "现金价值删除不得新增、删除或改写保险交易，也不得改变缴费、领取和记录数。",
        ],
        "result": {
            "status": "partial",
            "summary": "已验证删除非最新 11.00 快照后，最新 13.00 快照、余额、交易页汇总和图表在当前会话及重启后均保持一致；旧程序缺陷集中在删除当前最新或唯一快照后的重启投影。",
            "remaining_gaps": [
                "历史/未来日期的新增和查询时点",
                "旧程序删除最新值后的恢复文件参与方式及数据库根因",
                "负值和金额精度",
                "并发版本冲突、重复提交和持久化失败回滚",
            ],
        },
    }


def cash_value_date_boundary_record() -> dict:
    """记录历史、未来估值日及按查询日期选择当前现金价值的边界。"""
    return {
        "schema_version": 1,
        "execution_id": "RT-13-005",
        "resource": "TINSURECASHVALUEFRAME",
        "observed_at": DATE_BOUNDARY_OBSERVED_AT,
        "application": {
            "executable": "C:\\Program Files (x86)\\MoneyWise\\MoneyHome8\\Program\\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": "C:\\DCG-SZ\\IT Manage\\Private\\Personal-Docs\\test.mh8",
            "sha256_before": DATE_BOUNDARY_BEFORE_SHA,
            "sha256_after": DATE_BOUNDARY_AFTER_REOPEN_SHA,
            "backup_artifact": "artifacts/runtime-validation/backups/test-before-b13-cash-value-date-boundaries-20260731.mh8",
        },
        "navigation": {
            "entry_point": "账户中心 -> 商业保险账户 -> 共享工作区 -> 现金价值",
            "steps": [
                "从现金价值校准副本加载 Codex-B13-Cash-20260730 保单",
                "通过日期控件键盘操作新增 2026-07-29 / 7.00 历史快照",
                "新增 2026-08-01 / 15.00 未来快照",
                "核对列表、趋势图、账户余额和交易页汇总后正常退出",
                "重新打开同一 test.mh8，复核快照持久化与当前值投影",
                "保存重开态副本后，用操作前备份恢复 test.mh8 基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "新增历史估值日",
                "status": "observed",
                "observations": "日期控件接受键盘上下调整；新增 2026-07-29 / 7.00 后，列表按日期降序显示 2026-07-30 / 11.00、2026-07-29 / 7.00，趋势图包含两点，当前余额仍为 11.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/b13-cash-date-boundary-history-dialog.png",
                    "artifacts/runtime-validation/b13-cash-date-boundary-history-filled.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-date-boundary-after-history-add-sanitized.png",
                ],
            },
            {
                "name": "新增未来估值日",
                "status": "observed",
                "observations": "新增 2026-08-01 / 15.00 后，列表按日期降序显示 15.00、11.00、7.00，趋势图包含三点；在 2026-07-31 当前会话中，账户余额和交易页现金价值汇总仍为 11.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/b13-cash-date-boundary-future-dialog.png",
                    "artifacts/runtime-validation/b13-cash-date-boundary-future-filled.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-date-boundary-after-future-add-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-date-boundary-transaction-before-reopen-sanitized.png",
                ],
            },
            {
                "name": "重新打开账簿",
                "status": "observed",
                "observations": "三条快照和趋势图均持久化，但账户中心、工作区余额和交易页现金价值汇总错误显示 0.00；这与退出前按 2026-07-31 查询得到 11.00 不一致。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-date-boundary-account-center-after-reopen-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-date-boundary-value-after-reopen-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-date-boundary-transaction-after-reopen-sanitized.png",
                ],
            },
            {
                "name": "测试库恢复",
                "status": "observed",
                "observations": "MoneyHome8 正常退出且无锁文件后恢复 test.mh8；长度和 SHA-256 回到操作前基线。",
                "evidence_paths": ["artifacts/runtime-validation/B13-pending-close-notes.md"],
            },
        ],
        "commands": [
            {
                "component": "现金价值页",
                "label": "新增历史快照",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "设置估值日 2026-07-29、现金价值 7.00 并确认",
                "confirmation": "对话框关闭，列表和趋势图新增历史数据点。",
                "outcome": "历史快照保存成功，当前现金价值保持截止查询日的 11.00。",
                "status": "pass",
            },
            {
                "component": "现金价值页",
                "label": "新增未来快照",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "设置估值日 2026-08-01、现金价值 15.00 并确认",
                "confirmation": "对话框关闭，列表和趋势图新增未来数据点。",
                "outcome": "快照持久化成功，当前会话能按 2026-07-31 保持 11.00；重启后旧程序错误投影为 0.00。",
                "status": "fail",
            },
        ],
        "data_flow": {
            "inputs": ["保险保单 ID", "估值日", "现金价值", "查询基准日 as_of_date"],
            "reads": ["现金价值快照序列", "生效日期区间", "截止查询日的当前现金价值", "保险交易汇总"],
            "writes": ["新增历史现金价值快照", "新增未来现金价值快照"],
            "derived_results": ["按日期降序的快照表", "完整趋势图", "截止查询日的保险账户余额", "交易页现金价值汇总", "总资产"],
            "side_effects": ["保险交易、缴费 10.00、领取 0.00、记录数 1 均不变"],
            "rollback": "验证结束后关闭旧程序，并用 test-before-b13-cash-value-date-boundaries-20260731.mh8 恢复唯一测试账簿。",
        },
        "evidence": [
            {
                "kind": "manual_note",
                "path": "artifacts/runtime-validation/B13-pending-close-notes.md",
                "description": "历史和未来日期新增、重开复核及基线恢复记录。",
            },
            {
                "kind": "hash",
                "path": "artifacts/runtime-validation/backups/test-after-b13-cash-value-date-boundaries-before-reopen-20260731.mh8",
                "description": f"未来快照新增后首次退出副本，SHA-256 为 {DATE_BOUNDARY_AFTER_CLOSE_SHA}。",
            },
            {
                "kind": "hash",
                "path": "artifacts/runtime-validation/backups/test-after-b13-cash-value-date-boundaries-reopen-before-restore-20260731.mh8",
                "description": f"重开复核并退出后的副本，SHA-256 为 {DATE_BOUNDARY_AFTER_REOPEN_SHA}。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-date-boundary-after-future-add-sanitized.png",
                "description": "未来快照进入列表和趋势图，但当前会话余额仍按查询日显示 11.00。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-date-boundary-value-after-reopen-sanitized.png",
                "description": "重开后三条明细仍在，但旧程序当前值错误归零。",
            },
        ],
        "requirements_update": [
            "现金价值当前值查询必须显式接收 as_of_date；默认值应来自应用或账簿业务日期，而不是直接取数据库最大估值日。",
            "未来快照可以保存并进入完整趋势图，但在估值日到达前不得计入当前余额、交易页汇总或总资产。",
            "同一保单的快照应形成左闭右开生效区间 [effective_from, effective_to_exclusive)，按 as_of_date 选择唯一有效值。",
            "历史快照不得覆盖更晚且已生效的当前值；列表展示顺序与当前值计算必须彼此独立。",
            "重新启动后必须从快照事实和查询基准日确定性重建同一结果，本场景应继续为 11.00，不能变为 0.00。",
            "不得持久化脱离快照事实、查询基准日或生效区间的当前现金价值缓存。",
        ],
        "result": {
            "status": "partial",
            "summary": "已验证历史和未来现金价值快照均可保存、按日期降序展示并进入趋势图；当前会话会排除尚未生效的未来快照，但旧程序重启后错误将当前值归零。",
            "remaining_gaps": [
                "应用或账簿业务日期的真实来源，以及跨月、跨年和时区边界",
                "旧程序重启投影归零的数据库或恢复文件根因",
                "负值和金额精度",
                "并发版本冲突、重复提交和持久化失败回滚",
            ],
        },
    }


def cash_value_amount_boundary_record() -> dict:
    """记录现金价值负数、空值、币种精度和大额金额边界。"""
    return {
        "schema_version": 1,
        "execution_id": "RT-13-005",
        "resource": "TINSURECASHVALUEFRAME",
        "observed_at": AMOUNT_BOUNDARY_OBSERVED_AT,
        "application": {
            "executable": "C:\\Program Files (x86)\\MoneyWise\\MoneyHome8\\Program\\MoneyHome8.exe",
            "version": "8.50.0.0",
            "window_title": "test - 财智8",
        },
        "ledger": {
            "path": "C:\\DCG-SZ\\IT Manage\\Private\\Personal-Docs\\test.mh8",
            "sha256_before": AMOUNT_BOUNDARY_BEFORE_SHA,
            "sha256_after": AMOUNT_BOUNDARY_AFTER_REOPEN_SHA,
            "backup_artifact": "artifacts/runtime-validation/backups/test-before-b13-cash-value-amount-boundaries-20260731.mh8",
        },
        "navigation": {
            "entry_point": "账户中心 -> 商业保险账户 -> 共享工作区 -> 现金价值",
            "steps": [
                "从现金价值校准副本加载 Codex-B13-Cash-20260730 保单",
                "新增 2026-07-31 / -1 并观察保存结果",
                "依次修改为 1.234、1.235 和空值",
                "测试十一位整数金额和十位整数金额的分币精度",
                "核对交易页、账户中心和现金价值页后正常退出并重开",
                "保存重开态副本后恢复 test.mh8 基线",
            ],
            "reachable": True,
            "unreachable_reason": None,
        },
        "states": [
            {
                "name": "负数输入",
                "status": "observed",
                "observations": "输入框显示 -1，点击确定没有校验提示；旧程序把新快照静默保存为 0.00，并把账户余额、交易页汇总和趋势图当前点同步为 0.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/b13-cash-amount-boundary-negative-filled.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-amount-boundary-after-negative-add-sanitized.png",
                ],
            },
            {
                "name": "币种精度",
                "status": "observed",
                "observations": "人民币现金价值输入 1.234 后保存为 1.23，输入 1.235 后保存为 1.24；界面按两位小数四舍五入。",
                "evidence_paths": [
                    "artifacts/runtime-validation/b13-cash-amount-boundary-precision-filled.png",
                    "artifacts/runtime-validation/b13-cash-amount-boundary-rounding-filled.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-amount-boundary-after-rounding-save-sanitized.png",
                ],
            },
            {
                "name": "空值输入",
                "status": "observed",
                "observations": "清空金额后点击确定没有提示，旧程序将同日快照保存为 0.00。",
                "evidence_paths": [
                    "artifacts/runtime-validation/b13-cash-amount-boundary-empty-filled.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-amount-boundary-after-empty-save-sanitized.png",
                ],
            },
            {
                "name": "十一位整数精度缺陷",
                "status": "observed",
                "observations": "尝试输入 999999999999.99 时，控件只显示 99999999999.99；保存后又变为 100,000,000,000.00，发生分币丢失和整数进位。",
                "evidence_paths": [
                    "artifacts/runtime-validation/b13-cash-amount-boundary-large-filled.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-amount-boundary-after-large-save-sanitized.png",
                ],
            },
            {
                "name": "十位整数跨页与重启",
                "status": "observed",
                "observations": "9,999,999,999.99 在现金价值列表、账户余额、交易页汇总和趋势图中保持一致；正常退出并重开后，账户中心、交易页和现金价值页继续精确显示该值。保险交易、缴费 10.00、领取 0.00 和记录数 1 不变。",
                "evidence_paths": [
                    "artifacts/runtime-validation/screenshots/b13-cash-amount-boundary-after-large-safe-save-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-amount-boundary-transaction-large-safe-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-amount-boundary-account-center-after-reopen-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-amount-boundary-transaction-after-reopen-sanitized.png",
                    "artifacts/runtime-validation/screenshots/b13-cash-amount-boundary-value-after-reopen-sanitized.png",
                ],
            },
            {
                "name": "测试库恢复",
                "status": "observed",
                "observations": "关闭进程后首次恢复因旧程序仍短暂占用 test.mh8 而被系统拒绝；等待进程完全退出后重试成功，长度和 SHA-256 回到基线。旧程序生成的 ~$test 恢复文件保持原样，未由验证脚本修改。",
                "evidence_paths": ["artifacts/runtime-validation/B13-pending-close-notes.md"],
            },
        ],
        "commands": [
            {
                "component": "现金价值编辑器",
                "label": "保存负数或空值",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "分别输入 -1 和空值后点击确定",
                "confirmation": "没有校验提示，编辑器直接关闭。",
                "outcome": "旧程序均静默写入 0.00；目标实现不得复制该行为。",
                "status": "fail",
            },
            {
                "component": "现金价值编辑器",
                "label": "保存多余小数位",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "分别输入 1.234 和 1.235 后点击确定",
                "confirmation": "编辑器关闭，列表显示两位小数。",
                "outcome": "保存结果分别为 1.23 和 1.24。",
                "status": "pass",
            },
            {
                "component": "现金价值编辑器",
                "label": "保存大额金额",
                "initial_state": {"enabled": True, "visible": True},
                "trigger": "输入十一位或十位整数金额并点击确定",
                "confirmation": "编辑器关闭，列表和投影刷新。",
                "outcome": "十位整数精确持久化；十一位整数发生控件截断和浮点进位。",
                "status": "fail",
            },
        ],
        "data_flow": {
            "inputs": ["保险保单 ID", "估值日", "金额文本", "币种小数位", "舍入规则", "金额上限"],
            "reads": ["币种精度", "同日现金价值快照", "当前现金价值投影", "保险交易汇总"],
            "writes": ["同日快照版本化 upsert", "现金价值变更审计"],
            "derived_results": ["整数最小单位金额", "当前保险余额", "交易页现金价值汇总", "趋势图", "总资产"],
            "side_effects": ["现金价值变化不新增或改写保险交易", "旧程序创建或更新 ~$test 恢复文件"],
            "rollback": "关闭 MoneyHome8，等待文件占用完全释放后，用 test-before-b13-cash-value-amount-boundaries-20260731.mh8 恢复唯一测试账簿。",
        },
        "evidence": [
            {
                "kind": "manual_note",
                "path": "artifacts/runtime-validation/B13-pending-close-notes.md",
                "description": "金额输入、精度、大额持久化、重开和恢复记录。",
            },
            {
                "kind": "hash",
                "path": "artifacts/runtime-validation/backups/test-after-b13-cash-value-amount-boundaries-before-reopen-20260731.mh8",
                "description": f"首次退出副本，SHA-256 为 {AMOUNT_BOUNDARY_AFTER_CLOSE_SHA}。",
            },
            {
                "kind": "hash",
                "path": "artifacts/runtime-validation/backups/test-after-b13-cash-value-amount-boundaries-reopen-before-restore-20260731.mh8",
                "description": f"重开复核副本，SHA-256 为 {AMOUNT_BOUNDARY_AFTER_REOPEN_SHA}。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-amount-boundary-after-large-save-sanitized.png",
                "description": "十一位整数金额发生分币丢失并进位。",
            },
            {
                "kind": "screenshot",
                "path": "artifacts/runtime-validation/screenshots/b13-cash-amount-boundary-value-after-reopen-sanitized.png",
                "description": "十位整数金额在重启后保持精确并保留两日期趋势。",
            },
        ],
        "requirements_update": [
            "现金价值为空时必须阻止提交并给出字段级错误，不能静默转换为 0.00。",
            "现金价值必须大于或等于零；负数应在应用层和数据库层同时拒绝，不能静默夹取为零。",
            "金额文本必须先按币种小数位和明确舍入模式转换，再写入整数最小单位；人民币样例采用两位小数、0.005 向上舍入。",
            "现金价值、余额、资产和报表不得使用 f32/f64 作为账本金额事实，SQLite 使用 INTEGER 最小单位，Rust 使用 i64 或受检定点类型。",
            "输入控件不得静默截掉高位；超出产品配置或整数范围时必须阻止提交并显示允许范围。",
            "聚合和格式化必须使用受检加法并检测溢出；重启、跨页和趋势图读取同一精确整数事实。",
        ],
        "result": {
            "status": "partial",
            "summary": "已验证负数与空值被旧程序静默转零、人民币三位小数按两位四舍五入、十位整数金额跨页和重启精确持久化，以及十一位整数发生控件截断和浮点进位缺陷。",
            "remaining_gaps": [
                "其它币种小数位和舍入规则",
                "精确最大金额、聚合溢出和多账户大额合计",
                "科学计数法、千分位、非数字和本地化小数分隔符",
                "并发版本冲突、重复提交和持久化失败回滚",
            ],
        },
    }


def main() -> None:
    """写出 B13 商业保险现金价值校准的最新结构化记录。"""
    records = cash_value_calibration_records()
    for record in records:
        path = ARTIFACT_DIR / f"{record['execution_id']}-{STAMP}.json"
        path.write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(path.relative_to(ROOT))

    delete_record = cash_value_delete_record()
    delete_path = ARTIFACT_DIR / f"{delete_record['execution_id']}-{DELETE_STAMP}.json"
    delete_path.write_text(
        json.dumps(delete_record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(delete_path.relative_to(ROOT))

    multidate_record = cash_value_multidate_delete_record()
    multidate_path = ARTIFACT_DIR / f"{multidate_record['execution_id']}-{MULTIDATE_STAMP}.json"
    multidate_path.write_text(
        json.dumps(multidate_record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(multidate_path.relative_to(ROOT))

    nonlatest_record = cash_value_nonlatest_delete_record()
    nonlatest_path = ARTIFACT_DIR / f"{nonlatest_record['execution_id']}-{NONLATEST_STAMP}.json"
    nonlatest_path.write_text(
        json.dumps(nonlatest_record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(nonlatest_path.relative_to(ROOT))

    date_boundary_record = cash_value_date_boundary_record()
    date_boundary_path = (
        ARTIFACT_DIR
        / f"{date_boundary_record['execution_id']}-{DATE_BOUNDARY_STAMP}.json"
    )
    date_boundary_path.write_text(
        json.dumps(date_boundary_record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(date_boundary_path.relative_to(ROOT))

    amount_boundary_record = cash_value_amount_boundary_record()
    amount_boundary_path = (
        ARTIFACT_DIR
        / f"{amount_boundary_record['execution_id']}-{AMOUNT_BOUNDARY_STAMP}.json"
    )
    amount_boundary_path.write_text(
        json.dumps(amount_boundary_record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(amount_boundary_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
