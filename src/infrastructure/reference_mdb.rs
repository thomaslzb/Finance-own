use std::fs::File;
use std::io::{self, Read};
use std::path::{Path, PathBuf};

use crate::domain::reference_store::ReferenceStoreError;

const JET_HEADER_TEXT: &[u8] = b"Standard Jet DB";

/// `mhlink.mdb` 只读探测结果。
///
/// 第一阶段先确认文件可访问性和 Jet 容器身份；正式表行读取需要后续接入
/// Access/ODBC/COM 或其它只读适配层。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReferenceMdbInspection {
    /// 被探测文件的路径。
    pub path: PathBuf,
    /// 是否识别到 Jet/Access 数据库文件头。
    pub is_jet_database: bool,
    /// 第一阶段必须读取的共享参考表。
    pub required_tables: Vec<&'static str>,
    /// 当前是否已经具备表行读取适配器。
    pub table_reader_available: bool,
}

impl ReferenceMdbInspection {
    /// 当前 P1-02 所需的三张共享参考表。
    fn new(path: PathBuf, is_jet_database: bool) -> Self {
        Self {
            path,
            is_jet_database,
            required_tables: vec!["HBRate", "TBSecuPrice", "TBTransFee"],
            table_reader_available: false,
        }
    }
}

/// `mhlink.mdb` 文件级只读探测器。
///
/// 该类型只打开并读取文件头，不枚举表、不写入文件，适合在未选定 Access
/// 适配技术前作为 P1-02 的最低风险状态检查。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReferenceMdbProbe {
    /// 待探测的参考库或测试副本路径。
    pub path: PathBuf,
}

impl ReferenceMdbProbe {
    /// 构造一个只读探测器。
    pub fn new(path: impl AsRef<Path>) -> Self {
        Self {
            path: path.as_ref().to_path_buf(),
        }
    }

    /// 读取文件头并判断是否为 Jet/Access 数据库。
    pub fn inspect(&self) -> Result<ReferenceMdbInspection, ReferenceStoreError> {
        if !self.path.is_file() {
            return Err(ReferenceStoreError::FileNotFound(
                self.path.display().to_string(),
            ));
        }

        let mut file = File::open(&self.path).map_err(map_io_error)?;
        let mut header = [0_u8; 128];
        let bytes_read = file.read(&mut header).map_err(map_io_error)?;
        let is_jet_database = header[..bytes_read]
            .windows(JET_HEADER_TEXT.len())
            .any(|window| window == JET_HEADER_TEXT);

        if !is_jet_database {
            return Err(ReferenceStoreError::InvalidFormat(
                "文件头未识别到 Standard Jet DB".to_owned(),
            ));
        }

        Ok(ReferenceMdbInspection::new(
            self.path.clone(),
            is_jet_database,
        ))
    }
}

fn map_io_error(error: io::Error) -> ReferenceStoreError {
    ReferenceStoreError::Io(error.kind().to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fixture_path() -> PathBuf {
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("artifacts")
            .join("mhlink-copy.mdb")
    }

    #[test]
    fn detects_mhlink_copy_as_jet_database_without_table_reader() {
        let inspection = ReferenceMdbProbe::new(fixture_path()).inspect().unwrap();

        assert!(inspection.is_jet_database);
        assert_eq!(
            inspection.required_tables,
            vec!["HBRate", "TBSecuPrice", "TBTransFee"]
        );
        assert!(!inspection.table_reader_available);
    }

    #[test]
    fn reports_missing_reference_file_as_structured_error() {
        let missing = ReferenceMdbProbe::new(
            PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("artifacts")
                .join("missing-mhlink.mdb"),
        );

        let error = missing.inspect().unwrap_err();

        assert!(matches!(error, ReferenceStoreError::FileNotFound(_)));
    }
}
