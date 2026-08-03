use crate::domain::reporting::{
    AccountBalanceProjection, InvestmentPositionInput, LedgerEntryProjection, RealizedProfitInput,
    RunningBalanceProjection, TaggedAssetProjection, TaggedLedgerEntryProjection,
};

/// 闭区间业务日期范围。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DateRange {
    /// 开始日期，格式为 `YYYY-MM-DD`。
    pub start: String,
    /// 结束日期，格式为 `YYYY-MM-DD`。
    pub end: String,
}

/// 财务记录和基础报表的查询条件。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LedgerEntryFilter {
    /// 查询所属账簿，所有读取必须显式限定账簿。
    pub ledger_id: String,
    /// 可选业务日期闭区间。
    pub date_range: Option<DateRange>,
    /// 空集合表示不限制账户。
    pub account_ids: Vec<String>,
    /// 空集合表示不限制分类。
    pub category_ids: Vec<String>,
    /// 空集合表示不限制标签。
    pub tag_ids: Vec<String>,
    /// 是否包含作废记录；正常报表必须为 `false`。
    pub include_voided: bool,
}

/// 投资输入投影的查询条件。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InvestmentProjectionFilter {
    /// 查询所属账簿。
    pub ledger_id: String,
    /// 空集合表示不限制投资账户。
    pub account_ids: Vec<String>,
    /// 空集合表示不限制投资标的。
    pub instrument_ids: Vec<String>,
    /// 可选业务日期闭区间；持仓查询通常只使用结束日期。
    pub date_range: Option<DateRange>,
}

/// 报表只读仓储错误。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReportReadError {
    /// 查询条件违反日期、账簿或筛选边界。
    InvalidFilter(String),
    /// 本地数据库查询失败；消息不得包含密钥或完整敏感路径。
    Storage(String),
    /// 数据精度、币种或关联关系不满足投影契约。
    InconsistentData(String),
}

/// 报表与图表共享的只读查询端口。
///
/// SQLite 适配器必须返回同一组 DTO 给表格、图表、导出和打印流程，避免各层重复计算。
pub trait ReportReadRepository {
    /// 查询财务记录原子分录，按业务日期、交易序号和分录序号升序返回。
    fn list_ledger_entries(
        &self,
        filter: &LedgerEntryFilter,
    ) -> Result<Vec<LedgerEntryProjection>, ReportReadError>;

    /// 查询账户流水及累计余额，结果不包含草稿和作废交易。
    fn list_account_running_balances(
        &self,
        filter: &LedgerEntryFilter,
    ) -> Result<Vec<RunningBalanceProjection>, ReportReadError>;

    /// 查询账簿内账户当前余额，可由目标、资产和账户中心复用。
    fn list_account_balances(
        &self,
        ledger_id: &str,
    ) -> Result<Vec<AccountBalanceProjection>, ReportReadError>;

    /// 查询标签关联流水；聚合流入和流出由报表服务按方向完成。
    fn list_tagged_entries(
        &self,
        filter: &LedgerEntryFilter,
    ) -> Result<Vec<TaggedLedgerEntryProjection>, ReportReadError>;

    /// 查询标签关联资产余额。
    fn list_tagged_assets(
        &self,
        ledger_id: &str,
        tag_ids: &[String],
    ) -> Result<Vec<TaggedAssetProjection>, ReportReadError>;

    /// 查询投资持仓计算输入，不返回尚未校准的成本和收益率结果。
    fn list_investment_position_inputs(
        &self,
        filter: &InvestmentProjectionFilter,
    ) -> Result<Vec<InvestmentPositionInput>, ReportReadError>;

    /// 查询已实现盈亏批次输入，不在仓储层隐式选择收益率公式。
    fn list_realized_profit_inputs(
        &self,
        filter: &InvestmentProjectionFilter,
    ) -> Result<Vec<RealizedProfitInput>, ReportReadError>;
}
