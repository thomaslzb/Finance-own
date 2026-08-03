/// 综合缓存中的检索记录。
///
/// 数据来源为 `MoneyHome8.cache`。当前只确认 `_PY` 和 `_LIST` 是搜索/列表索引线索，
/// 尚未完整逆向字段分隔协议，因此第一期记录保留原始键和值。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LookupIndexEntry {
    /// 缓存中的原始键，例如 `600030_PY` 或 `中信证券_LIST`。
    pub raw_key: String,
    /// 原始键去掉后缀后的主体文本，通常是代码或中文名称。
    pub key_text: String,
    /// 缓存后缀，例如 `_PY` 或 `_LIST`。
    pub suffix: LookupIndexSuffix,
    /// 与该键相邻或解析得到的原始值；协议未完全确认前不拆成业务字段。
    pub raw_value: Option<String>,
}

/// 综合检索缓存中已确认的后缀类型。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LookupIndexSuffix {
    /// 拼音、缩写或其它检索键线索。
    Pinyin,
    /// 展示列表线索。
    List,
}

/// 投资缓存中按类别码归档的候选投资品。
///
/// 数据来源为 `Investment.cache`。`_3/_4/_9` 的业务含义来自样本推断和
/// `code-type-mapping.md`，仍保留 `legacy_type_code` 作为旧缓存事实。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InvestmentCatalogEntry {
    /// 旧缓存中的投资品代码。
    pub instrument_code: String,
    /// 旧缓存类别码。
    pub legacy_type_code: InvestmentCatalogTypeCode,
    /// 投资品显示名称；无法从当前协议可靠解析时为空。
    pub name: Option<String>,
    /// 原始缓存片段，供后续协议校准追溯。
    pub raw_fragment: String,
}

/// `Investment.cache` 中当前高可信的类别码。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum InvestmentCatalogTypeCode {
    /// `_3`，高可信对应交易型市场标的。
    TradingInstrument,
    /// `_4`，高可信对应场外基金或公募基金产品。
    OpenFund,
    /// `_9`，高可信对应货币基金或现金管理类产品。
    MoneyMarketFund,
}

/// 缓存读取失败的阶段性错误。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CacheStoreError {
    /// 文件不存在或路径不是普通文件。
    FileNotFound(String),
    /// 文件头不是已确认的 `MoneyHomeCache`。
    InvalidFormat(String),
    /// 文件系统读取失败；消息不得包含真实财务敏感数据。
    Io(String),
    /// 当前协议解析不足以满足请求。
    UnsupportedLayout(String),
}

/// 程序缓存仓储端口。
///
/// 实现必须只读访问 `.cache` 样本或明确副本；缓存只作为搜索和候选目录输入，
/// 不得成为新账簿真相源。
pub trait CacheStoreRepository {
    /// 按关键字搜索综合索引，匹配代码、名称或拼音缩写线索。
    fn search_lookup(&self, keyword: &str) -> Result<Vec<LookupIndexEntry>, CacheStoreError>;

    /// 按代码搜索综合索引。
    fn search_lookup_by_code(&self, code: &str) -> Result<Vec<LookupIndexEntry>, CacheStoreError>;

    /// 按拼音或缩写搜索综合索引。
    fn search_lookup_by_abbr(&self, abbr: &str) -> Result<Vec<LookupIndexEntry>, CacheStoreError>;

    /// 按投资缓存类别码列出候选投资品。
    fn list_investment_catalog_by_type(
        &self,
        type_code: InvestmentCatalogTypeCode,
    ) -> Result<Vec<InvestmentCatalogEntry>, CacheStoreError>;
}
