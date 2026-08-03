use super::money::ScaledValue;

/// 财务记录的一条原子账户分录投影。
///
/// 数据来自 `v_ledger_entries`；同一业务交易可以包含多条分录，以表达转账、
/// 手续费以及分类或账户拆分。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LedgerEntryProjection {
    /// 新账簿标识。
    pub ledger_id: String,
    /// 业务交易标识。
    pub transaction_id: String,
    /// 原子分录标识。
    pub entry_id: String,
    /// 账簿内稳定交易顺序。
    pub sequence_no: i64,
    /// 交易内稳定分录顺序。
    pub line_no: i64,
    /// 业务日期，格式为 `YYYY-MM-DD`。
    pub business_date: String,
    /// 交易类型，例如收入、支出或转账。
    pub transaction_kind: String,
    /// 交易状态；报表默认只包含 `posted`。
    pub status: String,
    /// 分录角色，例如主分录、对方分录或手续费。
    pub role: String,
    /// 账户标识。
    pub account_id: String,
    /// 账户展示名称。
    pub account_name: String,
    /// 可选分类标识；转账分录可以为空。
    pub category_id: Option<String>,
    /// 可选分类展示名称。
    pub category_name: Option<String>,
    /// 原币最小单位金额，正负号已经包含流入/流出方向。
    pub signed_amount_minor: i64,
    /// 原币代码。
    pub currency_code: String,
    /// 本币最小单位金额；缺少历史汇率时必须为空。
    pub signed_base_amount_minor: Option<i64>,
    /// 本币代码；与本币金额同时为空或同时有值。
    pub base_currency_code: Option<String>,
    /// 交易主题。
    pub theme: Option<String>,
    /// 交易说明。
    pub description: Option<String>,
    /// 分录备注。
    pub memo: Option<String>,
    /// 是否存在附件关联。
    pub has_attachments: bool,
    /// 按名称排序后拼接的标签名称。
    pub tag_names: Vec<String>,
}

/// 账户流水及其累计余额。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RunningBalanceProjection {
    /// 对应的原子流水分录。
    pub entry: LedgerEntryProjection,
    /// 按业务日期、交易顺序和分录顺序累计后的账户币种余额。
    pub balance_minor: i64,
}

/// 账户当前余额投影。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AccountBalanceProjection {
    /// 账簿标识。
    pub ledger_id: String,
    /// 账户标识。
    pub account_id: String,
    /// 账户展示名称。
    pub account_name: String,
    /// 余额币种。
    pub currency_code: String,
    /// 已入账分录汇总后的最小单位余额。
    pub balance_minor: i64,
}

/// 标签关联的流水投影。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TaggedLedgerEntryProjection {
    /// 标签标识。
    pub tag_id: String,
    /// 标签展示名称。
    pub tag_name: String,
    /// 标签关联的原子流水分录。
    pub entry: LedgerEntryProjection,
}

/// 标签关联的资产余额投影。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TaggedAssetProjection {
    /// 标签标识。
    pub tag_id: String,
    /// 标签展示名称。
    pub tag_name: String,
    /// 账户余额。
    pub account: AccountBalanceProjection,
}

/// 投资持仓公式的已确认输入。
///
/// 该类型不包含成本、市值、盈亏和收益率最终值，因为旧程序的成本法与费用口径
/// 尚未通过代表性数据校准。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InvestmentPositionInput {
    /// 账簿标识。
    pub ledger_id: String,
    /// 投资账户标识。
    pub account_id: String,
    /// 投资标的标识。
    pub instrument_id: String,
    /// 投资标的展示名称。
    pub instrument_name: String,
    /// 标的类型，例如证券、基金、期货或贵金属。
    pub instrument_kind: String,
    /// 行情币种。
    pub quote_currency_code: String,
    /// 买卖和转入转出抵销后的持仓数量。
    pub net_quantity: ScaledValue,
    /// 累计买入数量。
    pub bought_quantity: ScaledValue,
    /// 累计卖出数量。
    pub sold_quantity: ScaledValue,
}

/// 已实现盈亏公式的批次分配输入。
///
/// 最终盈亏和收益率由可替换的计算策略生成，校准前不得在 Repository 中隐式计算。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RealizedProfitInput {
    /// 账簿标识。
    pub ledger_id: String,
    /// 卖出业务日期。
    pub business_date: String,
    /// 卖出成交标识。
    pub sell_trade_id: String,
    /// 投资账户标识。
    pub account_id: String,
    /// 投资标的标识。
    pub instrument_id: String,
    /// 投资标的展示名称。
    pub instrument_name: String,
    /// 卖出数量。
    pub sold_quantity: ScaledValue,
    /// 卖出价格；没有价格的特殊业务类型返回空。
    pub price: Option<ScaledValue>,
    /// 已匹配到买入批次的数量。
    pub allocated_quantity: ScaledValue,
    /// 已分配成本，使用成交币种最小单位。
    pub allocated_cost_minor: i64,
    /// 已分配卖出收入，使用成交币种最小单位。
    pub allocated_proceeds_minor: i64,
}
