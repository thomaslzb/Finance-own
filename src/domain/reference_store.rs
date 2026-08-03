use super::money::ScaledValue;

/// 共享参考库中一条存款或产品利率规则。
///
/// 数据来源为 `mhlink.mdb.HBRate`。第一期只把旧字段转换成可追溯 DTO，
/// 不把利率直接写入新账簿真相表；账簿内版本化利率仍由存款利率发布流程负责。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RateRule {
    /// 旧参考库中的币种类型值，例如人民币在当前证据中对应 `1`。
    pub legacy_currency_type: i64,
    /// 旧参考库中的存款类型值，对应定期、活期或其它产品口径。
    pub legacy_deposit_type: i64,
    /// 旧参考库中的期限值；真实单位由旧表字段和页面证据共同校准。
    pub legacy_deposit_term: i64,
    /// 旧表 `ARate` 原始利率值；真实比例单位尚待校准，不能直接当成百分数使用。
    pub legacy_rate_value: ScaledValue,
    /// 旧表原始行号或主键线索；没有稳定主键时为空。
    pub legacy_row_id: Option<String>,
}

/// 共享参考库中一条行情价格。
///
/// 数据来源为 `mhlink.mdb.TBSecuPrice`，支撑证券、基金、债券、贵金属等估值。
/// 第一阶段只保留原始类型码和币种码，避免在校准前误合并不同市场对象。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Quote {
    /// 旧参考库中的证券、基金、债券或其它投资品代码。
    pub instrument_code: String,
    /// 行情日期，格式为 `YYYY-MM-DD`；无法解析的原始日期应由适配层返回错误。
    pub price_date: String,
    /// 行情价格，按旧表原始小数位保存。
    pub price: ScaledValue,
    /// 旧参考库中的对象类型码，例如 `_3/_4` 缓存类别需通过映射层关联。
    pub legacy_object_type: i64,
    /// 旧参考库中的币种类型码。
    pub legacy_currency_type: i64,
    /// 旧表原始行号或主键线索；没有稳定主键时为空。
    pub legacy_row_id: Option<String>,
}

/// 共享参考库中一条交易费率规则。
///
/// 数据来源为 `mhlink.mdb.TBTransFee`。费率只作为参考模板输入，账户级费率、
/// 在线更新批次和账簿内快照必须由后续应用命令显式发布。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FeeRule {
    /// 旧参考库中的交易或市场类型值。
    pub legacy_type: i64,
    /// 佣金费率；旧字段通常对应 `YJFL`。
    pub commission_rate: Option<ScaledValue>,
    /// 印花税率；旧字段通常对应 `YHSL`。
    pub stamp_tax_rate: Option<ScaledValue>,
    /// 最低佣金，按对应市场币种最小单位或旧表金额精度保存。
    pub minimum_commission: Option<ScaledValue>,
    /// 过户费率；旧字段通常对应 `GHF`。
    pub transfer_fee_rate: Option<ScaledValue>,
    /// 附加费率；旧字段通常对应 `FJF`。
    pub surcharge_rate: Option<ScaledValue>,
    /// 结算费率；旧字段通常对应 `JSFL`。
    pub settlement_rate: Option<ScaledValue>,
    /// 旧表原始行号或主键线索；没有稳定主键时为空。
    pub legacy_row_id: Option<String>,
}

/// 共享参考库读取失败的阶段性错误。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReferenceStoreError {
    /// 文件不存在或路径不是普通文件。
    FileNotFound(String),
    /// 文件头不是已确认的 Jet/Access 数据库格式。
    InvalidFormat(String),
    /// 读取过程中遇到文件系统错误；消息不得包含密钥或完整财务数据。
    Io(String),
    /// 当前运行环境缺少可读取 Access/Jet 表数据的适配器。
    AdapterUnavailable(String),
    /// 表存在性、字段或数据类型不满足当前契约。
    SchemaMismatch(String),
}

/// 共享参考库仓储端口。
///
/// 实现必须只读访问 `mhlink.mdb` 或其测试副本，不得修改原参考库文件；
/// UI 只能通过应用层调用该端口，不能直接读取 Access 文件。
pub trait ReferenceStoreRepository {
    /// 读取全部利率规则。
    fn list_rate_rules(&self) -> Result<Vec<RateRule>, ReferenceStoreError>;

    /// 按投资品代码读取行情价格，返回值按日期升序或适配器文档中的稳定顺序排列。
    fn find_quotes_by_code(&self, code: &str) -> Result<Vec<Quote>, ReferenceStoreError>;

    /// 读取一批行情价格；`limit` 为空时由实现使用安全默认上限。
    fn list_quotes(&self, limit: Option<usize>) -> Result<Vec<Quote>, ReferenceStoreError>;

    /// 读取全部交易费率规则。
    fn list_fee_rules(&self) -> Result<Vec<FeeRule>, ReferenceStoreError>;
}
