"""生成 B16 报表与分析投影的运行态观察记录。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "artifacts" / "runtime-validation"
OBSERVED_AT = "2026-07-29T23:19:06+08:00"
LEDGER_HASH = "18A99BFCC76727A44A2ABE09C1054953C122EBAEF38E5404D6990F678B300ADD"


def screenshot(name: str) -> str:
    return f"artifacts/runtime-validation/screenshots/{name}"


RECORDS = {
    "RT-16-001": ("TREPORTFM", "报表通用容器", [screenshot("b16-report-center-entry.png"), screenshot("b16-daily-income-expense-result.png")], "左树、日期范围、筛选、表格/图表和操作菜单", "确认财务报表采用左树导航和右侧参数化结果容器；查询后进入 tsReport，操作菜单包含四项，导出报表和打印预览由结果状态控制。"),
    "RT-16-002": ("TREPORTOPTIONDLGFM", "报表筛选", [screenshot("b16-report-filter-dialog.png")], "相关资产、人员/机构、活动类型、收支项目、标签、币种/对象、金额范围", "动态确认筛选窗按页签组织条件；当前投资收益率场景显示相关资产与币种/对象页，支持全选、反选和恢复默认条件。"),
    "RT-16-003": ("TRPTACCOUNTINCOMESTATFRM", "账户日常收支表", [screenshot("b16-account-income-expense-result.png")], "账户与统计期间", "按账户展示收入、支出及差额，并提供合计。"),
    "RT-16-004": ("TRPTBSSTATFRM", "资产负债表", [screenshot("b16-balance-sheet-result.png")], "统计日期与账户估值", "资产和负债左右并列，分别显示项目、金额和占比，并汇总净资产。"),
    "RT-16-005": ("TRPTCASHWASTEFM", "现金流表", [screenshot("b16-cash-flow-result.png")], "统计期间与现金流分类", "收入来源和资金去向左右并列，按项目汇总现金流并显示总计。"),
    "RT-16-006": ("TRPTCREDITDEBTSTATFM", "债权债务表", [screenshot("b16-credit-debt-result.png")], "债权债务款项、对象、日期和余额", "按债权/债务及状态汇总对象、金额和合计，负数使用红色显示。"),
    "RT-16-007": ("TRPTDEBTINVESTMENTINVESTYKFORM", "网贷盈亏一览表", [screenshot("b16-online-lending-profit-loss-result.png")], "统计期间与网贷投资", "默认条件下返回明确的无数据状态，并提示调整日期或筛选条件后重新查询。"),
    "RT-16-008": ("TRPTEXCHANGE6FM", "外汇交易一览表", [screenshot("b16-foreign-exchange-overview-result.png")], "外汇账户、币种、交易和期间", "按外汇账户/币种展示买入、卖出及盈亏类指标，并提供账户和总计分组。"),
    "RT-16-009": ("TRPTFINANCIALPRODUCTSFM", "银行理财产品收益率表", [screenshot("b16-financial-product-return-result.png")], "统计期间与银行理财产品", "默认条件下返回明确无数据状态，并提示调整日期或筛选条件。"),
    "RT-16-010": ("TRPTFUNDSAVAILABLEFM", "可用资金表", [screenshot("b16-available-funds-result.png")], "现金与可用资金账户", "按账户列出可用资金并分组汇总。"),
    "RT-16-011": ("TRPTFUNDTRENDFM", "开放式基金市值大势图", [screenshot("b16-open-fund-market-value-trend-result.png")], "日期序列、资产总值、基金市值和资金余额", "折线图动态确认资产总值、基金市值和资金余额三条默认序列。"),
    "RT-16-012": ("TRPTINCEXPCOMPAREFM", "两段时间收支对比表", [screenshot("b16-period-income-expense-compare-result.png")], "两个统计期间与收支项目", "按收入/支出项目并列展示两段期间金额和差额，正负差异使用颜色区分。"),
    "RT-16-013": ("TRPTINCEXPZSTOVFM", "收支走势图", [screenshot("b16-income-expense-trend-result.png")], "月份、收入和支出", "柱状图按月对比收入与支出。"),
    "RT-16-014": ("TRPTINCOMELISTFM", "日常收支明细表", [screenshot("b16-daily-income-expense-detail-result.png")], "交易日期、项目、账户、金额和说明", "按收入/支出分组展示逐笔交易明细和分组小计。"),
    "RT-16-015": ("TRPTINCOMESTATFRM", "日常收支表", [screenshot("b16-daily-income-expense-result.png")], "统计期间与收支项目", "按收入/支出分组展示收支项目、金额、占比和合计。"),
    "RT-16-016": ("TRPTINVESTINCOMEFM", "投资收益一览表", [screenshot("b16-investment-income-overview-result.png")], "投资账户、收益事件和期间", "按投资类型与账户汇总收益，负收益使用红色并提供合计。"),
    "RT-16-017": ("TRPTINVESTMENTPERFORMANCESTATFM", "投资收益率统计表", [screenshot("b16-investment-performance-result.png")], "账户/投资查询模式、期间、相关资产", "按账户展示投资收益、投资收益率、年化收益率、期初市值、期间转入/转出、其它收支和期末市值，并汇总收益。"),
    "RT-16-018": ("TRPTINVESTVIEWFM", "投资一览表", [screenshot("b16-investment-overview-result.png")], "投资账户、持仓、买卖和估值", "按账户和投资品展示买卖数量/均价、买卖盈亏、持仓均价/成本/市值、浮动盈亏和涨幅，并提供账户小计。"),
    "RT-16-019": ("TRPTMONTHASSETFM", "月资产走势图", [screenshot("b16-monthly-assets-trend-result.png")], "月份、资产、负债和净资产", "折线图按月展示资产、负债和净资产三条序列。"),
    "RT-16-020": ("TRPTMONTHAVERAGEINCEXPFM", "月平均收支表", [screenshot("b16-monthly-average-income-expense-result.png")], "统计期间与收支项目", "按收入/支出项目展示月平均金额、占比和合计。"),
    "RT-16-021": ("TRPTOPENFUNDINVESTFM", "开放式基金投资一览表", [screenshot("b16-open-fund-investment-overview-result.png")], "基金账户、份额、买卖、净值和市值", "按基金账户展示买卖、持仓、成本、市值、盈亏和涨幅，并提供账户与总计。"),
    "RT-16-022": ("TRPTOPENFUNDINVESTLOSSFM", "开放式基金费用及盈亏一览表", [screenshot("b16-open-fund-fee-profit-loss-result.png")], "基金账户、费用、分红和盈亏", "按基金账户与产品汇总费用、收入和盈亏并提供合计。"),
    "RT-16-023": ("TRPTSECURITINVESTFM", "证券投资一览表", [screenshot("b16-security-investment-overview-result.png")], "证券账户、数量、均价、成本、期末市价和市值", "按证券账户展示买卖、持仓、成本、期末市价、市值、浮动盈亏和涨幅，并提供总计。"),
    "RT-16-024": ("TRPTSECURITINVESTLOSSFM", "证券费用及盈亏一览表", [screenshot("b16-security-fee-profit-loss-result.png")], "证券账户、交易费用、收入和盈亏", "按证券账户与证券汇总费用和盈亏，包含账户小计与总计。"),
    "RT-16-025": ("TRPTSTOCKTRENDFM", "证券市值大势图", [screenshot("b16-security-market-value-trend-result.png")], "日期序列、资产总值、证券市值、资金余额和指数", "动态确认证券趋势图支持资产总值、证券市值、资金余额、上证指数和深证成指序列。"),
    "RT-16-026": ("TRPTTAGINCOMESTATFRM", "标签日常收支表", [screenshot("b16-tag-income-expense-result.png")], "标签、收入和支出", "按标签汇总收入、支出和差额，并提供总计。"),
    "RT-16-027": ("TRPTYEARINCEXPFORM", "收支统计表", [screenshot("b16-income-expense-statistics-result.png")], "年度/月度期间与收支项目", "以收支项目为行、月份为列展示期间矩阵、行合计和收入/支出分组。"),
    "RT-16-028": ("TUSABLEMONEYCHARTFRAME", "概况可用资金图", ["docs/screenshots/page-overview.png", screenshot("b16-available-funds-result.png")], "概况页账户可用资金投影", "该嵌入图表属于概况页而非报表中心；本轮通过可用资金表确认其数据投影语义，独立图表交互仍待概况页校准。"),
}


def build_record(execution_id: str, data: tuple[str, str, list[str], str, str]) -> dict:
    resource, title, screenshots, inputs, summary = data
    indirect = execution_id == "RT-16-028"
    evidence = [
        {"kind": "screenshot", "path": path, "description": f"{title}运行态证据。"}
        for path in screenshots
    ]
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
            "entry_point": "顶栏财务报表工作区",
            "steps": ["切换到财务报表", f"从左树进入{title}", "保持默认筛选并执行只读查询", "记录表格、图表或空结果"],
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
            "label": "查询",
            "initial_state": {"enabled": True, "visible": True},
            "trigger": "默认日期与筛选条件下执行只读查询",
            "confirmation": None,
            "outcome": summary,
            "status": "partial" if indirect else "pass",
        }],
        "data_flow": {
            "inputs": [item.strip() for item in inputs.split("、")],
            "reads": ["账户、交易、持仓、行情、汇率和分类标签中的适用真相数据"],
            "writes": [],
            "derived_results": ["分组、排序、小计、合计、占比、收益率或时间序列中的适用投影"],
            "side_effects": ["只读查询期间旧账簿文件长度由 18,939,904 增至 18,984,960 字节，未执行财务业务写入"],
            "rollback": "报表查询不写财务真相；筛选窗口未修改条件，未执行导出或打印。",
        },
        "evidence": evidence,
        "requirements_update": [summary],
        "result": {
            "status": "partial",
            "summary": summary,
            "remaining_gaps": (["概况页嵌入图表的独立空态、有数据态和交互"] if indirect else [])
            + ["精确 SQL/公式、排序分页、筛选边界、导出格式、打印和关闭旧程序后的 SHA-256 仍待校准"],
        },
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for execution_id, data in RECORDS.items():
        path = OUTPUT_DIR / f"{execution_id}-20260729T231906+0800.json"
        path.write_text(
            json.dumps(build_record(execution_id, data), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"generated {len(RECORDS)} B16 records")


if __name__ == "__main__":
    main()
