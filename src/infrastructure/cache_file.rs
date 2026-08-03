use std::fs;
use std::path::{Path, PathBuf};

use crate::domain::cache_store::{
    CacheStoreError, CacheStoreRepository, InvestmentCatalogEntry, InvestmentCatalogTypeCode,
    LookupIndexEntry, LookupIndexSuffix,
};

const CACHE_HEADER: &[u8] = b"MoneyHomeCache";

/// `.cache` 文件级探测结果。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CacheFileInspection {
    /// 被探测的缓存文件路径。
    pub path: PathBuf,
    /// 文件大小，单位字节。
    pub file_size_bytes: u64,
    /// 是否识别到 `MoneyHomeCache` 文件头。
    pub has_money_home_cache_header: bool,
    /// `_PY` 标记出现次数。
    pub pinyin_marker_count: usize,
    /// `_LIST` 标记出现次数。
    pub list_marker_count: usize,
    /// `_3` 类别码出现次数。
    pub trading_marker_count: usize,
    /// `_4` 类别码出现次数。
    pub open_fund_marker_count: usize,
    /// `_9` 类别码出现次数。
    pub money_market_marker_count: usize,
}

/// 只读缓存文件视图。
///
/// 当前协议尚未完整逆向，本类型只提供头部识别、ASCII 标记统计和代码候选解析。
/// 中文字段在样本中更像 GBK/ANSI 长度前缀片段，第一期先不做业务化拆解。
#[derive(Debug, Clone)]
pub struct CacheFile {
    /// 缓存文件路径。
    pub path: PathBuf,
    bytes: Vec<u8>,
}

impl CacheFile {
    /// 只读加载缓存文件。
    pub fn open(path: impl AsRef<Path>) -> Result<Self, CacheStoreError> {
        let path = path.as_ref().to_path_buf();
        if !path.is_file() {
            return Err(CacheStoreError::FileNotFound(path.display().to_string()));
        }

        let bytes =
            fs::read(&path).map_err(|error| CacheStoreError::Io(error.kind().to_string()))?;
        if !bytes.starts_with(CACHE_HEADER) {
            return Err(CacheStoreError::InvalidFormat(
                "文件头未识别到 MoneyHomeCache".to_owned(),
            ));
        }

        Ok(Self { path, bytes })
    }

    /// 返回当前文件的低风险结构统计。
    pub fn inspect(&self) -> CacheFileInspection {
        CacheFileInspection {
            path: self.path.clone(),
            file_size_bytes: self.bytes.len() as u64,
            has_money_home_cache_header: self.bytes.starts_with(CACHE_HEADER),
            pinyin_marker_count: count_marker(&self.bytes, b"_PY"),
            list_marker_count: count_marker(&self.bytes, b"_LIST"),
            trading_marker_count: count_type_marker(&self.bytes, b"_3"),
            open_fund_marker_count: count_type_marker(&self.bytes, b"_4"),
            money_market_marker_count: count_type_marker(&self.bytes, b"_9"),
        }
    }

    /// 按原始文本关键字搜索 `_PY/_LIST` 附近的综合索引候选。
    pub fn search_lookup_candidates(&self, keyword: &str) -> Vec<LookupIndexEntry> {
        let keyword = keyword.trim();
        if keyword.is_empty() {
            return Vec::new();
        }

        let mut results = Vec::new();
        for suffix in [
            (b"_PY".as_slice(), LookupIndexSuffix::Pinyin),
            (b"_LIST".as_slice(), LookupIndexSuffix::List),
        ] {
            for key_text in visible_ascii_tokens_before_suffix(&self.bytes, suffix.0) {
                if key_text.contains(keyword) || keyword.contains(&key_text) {
                    results.push(LookupIndexEntry {
                        raw_key: format!("{key_text}{}", String::from_utf8_lossy(suffix.0)),
                        key_text,
                        suffix: suffix.1,
                        raw_value: None,
                    });
                }
            }
        }
        dedup_lookup(results)
    }

    /// 按投资类别码从可见文本中抽取候选。
    pub fn list_investment_catalog_candidates_by_type(
        &self,
        type_code: InvestmentCatalogTypeCode,
    ) -> Vec<InvestmentCatalogEntry> {
        let marker = match type_code {
            InvestmentCatalogTypeCode::TradingInstrument => b"_3".as_slice(),
            InvestmentCatalogTypeCode::OpenFund => b"_4".as_slice(),
            InvestmentCatalogTypeCode::MoneyMarketFund => b"_9".as_slice(),
        };

        visible_ascii_tokens_before_suffix(&self.bytes, marker)
            .into_iter()
            .map(|instrument_code| InvestmentCatalogEntry {
                raw_fragment: format!("{instrument_code}{}", String::from_utf8_lossy(marker)),
                instrument_code,
                legacy_type_code: type_code,
                name: None,
            })
            .collect()
    }
}

impl CacheStoreRepository for CacheFile {
    fn search_lookup(&self, keyword: &str) -> Result<Vec<LookupIndexEntry>, CacheStoreError> {
        Ok(self.search_lookup_candidates(keyword))
    }

    fn search_lookup_by_code(&self, code: &str) -> Result<Vec<LookupIndexEntry>, CacheStoreError> {
        Ok(self.search_lookup_candidates(code))
    }

    fn search_lookup_by_abbr(&self, abbr: &str) -> Result<Vec<LookupIndexEntry>, CacheStoreError> {
        Ok(self.search_lookup_candidates(abbr))
    }

    fn list_investment_catalog_by_type(
        &self,
        type_code: InvestmentCatalogTypeCode,
    ) -> Result<Vec<InvestmentCatalogEntry>, CacheStoreError> {
        Ok(self.list_investment_catalog_candidates_by_type(type_code))
    }
}

fn count_marker(bytes: &[u8], marker: &[u8]) -> usize {
    bytes
        .windows(marker.len())
        .filter(|window| *window == marker)
        .count()
}

fn count_type_marker(bytes: &[u8], marker: &[u8]) -> usize {
    visible_ascii_tokens_before_suffix(bytes, marker).len()
}

fn visible_ascii_tokens_before_suffix(bytes: &[u8], suffix: &[u8]) -> Vec<String> {
    let mut results = Vec::new();
    let mut search_from = 0;
    while let Some(offset) = find_bytes(&bytes[search_from..], suffix) {
        let suffix_start = search_from + offset;
        let token: Vec<u8> = bytes[..suffix_start]
            .iter()
            .rev()
            .copied()
            .take_while(|byte| is_visible_ascii_cache_token_char(*byte))
            .collect::<Vec<_>>()
            .into_iter()
            .rev()
            .collect();
        if !token.is_empty() {
            results.push(String::from_utf8_lossy(&token).to_string());
        }
        search_from = suffix_start + suffix.len();
    }
    results
}

fn find_bytes(haystack: &[u8], needle: &[u8]) -> Option<usize> {
    haystack
        .windows(needle.len())
        .position(|window| window == needle)
}

fn is_visible_ascii_cache_token_char(byte: u8) -> bool {
    byte.is_ascii_alphanumeric() || matches!(byte, b'_' | b'-' | b'.')
}

fn dedup_lookup(entries: Vec<LookupIndexEntry>) -> Vec<LookupIndexEntry> {
    let mut deduped = Vec::new();
    for entry in entries {
        if !deduped.iter().any(|existing: &LookupIndexEntry| {
            existing.raw_key == entry.raw_key && existing.suffix == entry.suffix
        }) {
            deduped.push(entry);
        }
    }
    deduped
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rejects_non_cache_header() {
        let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("artifacts")
            .join("mhlink-copy.mdb");
        let error = CacheFile::open(path).unwrap_err();
        assert!(matches!(error, CacheStoreError::InvalidFormat(_)));
    }

    #[test]
    fn detects_runtime_cache_headers_and_markers_when_present() {
        let money_cache = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("tools")
            .join("moneyhome8-runtime")
            .join("MoneyHome8.cache");
        if !money_cache.is_file() {
            return;
        }

        let cache = CacheFile::open(money_cache).unwrap();
        let inspection = cache.inspect();
        assert!(inspection.has_money_home_cache_header);
        assert!(inspection.pinyin_marker_count > 0);
        assert!(inspection.list_marker_count > 0);
    }

    #[test]
    fn extracts_investment_type_candidates_when_present() {
        let investment_cache = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("tools")
            .join("moneyhome8-runtime")
            .join("Investment.cache");
        if !investment_cache.is_file() {
            return;
        }

        let cache = CacheFile::open(investment_cache).unwrap();
        let inspection = cache.inspect();
        assert!(inspection.trading_marker_count > 0);
        assert!(inspection.open_fund_marker_count > 0);
        assert!(inspection.money_market_marker_count > 0);
        assert!(!cache
            .list_investment_catalog_candidates_by_type(InvestmentCatalogTypeCode::MoneyMarketFund)
            .is_empty());
    }

    #[test]
    fn exposes_cache_file_through_repository_port_when_sample_exists() {
        let investment_cache = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("tools")
            .join("moneyhome8-runtime")
            .join("Investment.cache");
        if !investment_cache.is_file() {
            return;
        }

        let repository: Box<dyn CacheStoreRepository> =
            Box::new(CacheFile::open(investment_cache).unwrap());
        let entries = repository
            .list_investment_catalog_by_type(InvestmentCatalogTypeCode::MoneyMarketFund)
            .unwrap();
        assert!(!entries.is_empty());
    }
}
