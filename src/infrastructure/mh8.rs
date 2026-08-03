use std::fs::{self, File};
use std::io::Read;
use std::path::{Path, PathBuf};

use crate::domain::legacy_source::{LegacySourceInspection, LegacySourceStatus};

const JET_HEADER: &[u8] = b"Standard Jet DB";

/// `mh8` 文件定位信息。
///
/// 这里先封装路径对象，后续再补齐格式识别、只读解析与安全写入策略。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Mh8Library {
    /// 源账本文件完整路径。
    pub path: PathBuf,
}

impl Mh8Library {
    /// 通过文件路径构造账本句柄。
    pub fn new(path: impl AsRef<Path>) -> Self {
        Self {
            path: path.as_ref().to_path_buf(),
        }
    }

    /// 对旧账簿或解压后的 Jet 库做只读静态检查。
    ///
    /// 该方法只读取文件元数据和头部字节，并检查常见锁文件线索；认证、对象枚举和迁移映射
    /// 由后续适配器完成，避免在未知权限上下文中误报读取成功。
    pub fn inspect_read_only(&self) -> LegacySourceInspection {
        inspect_legacy_file(&self.path)
    }
}

/// 对旧数据源做只读静态检查。
pub fn inspect_legacy_file(path: impl AsRef<Path>) -> LegacySourceInspection {
    let path = path.as_ref().to_path_buf();
    let mut diagnostics = Vec::new();
    let mut lock_indicators = detect_lock_indicators(&path);

    if !path.is_file() {
        diagnostics.push("文件不存在或路径不是普通文件".to_owned());
        return LegacySourceInspection {
            path,
            status: LegacySourceStatus::FileNotFound,
            file_size_bytes: None,
            has_jet_header: false,
            lock_indicators,
            diagnostics,
        };
    }

    let metadata = match fs::metadata(&path) {
        Ok(metadata) => metadata,
        Err(error) if error.kind() == std::io::ErrorKind::PermissionDenied => {
            diagnostics.push("操作系统拒绝读取文件元数据".to_owned());
            return LegacySourceInspection {
                path,
                status: LegacySourceStatus::PermissionDenied,
                file_size_bytes: None,
                has_jet_header: false,
                lock_indicators,
                diagnostics,
            };
        }
        Err(error) => {
            diagnostics.push(format!("读取文件元数据失败：{}", error.kind()));
            return LegacySourceInspection {
                path,
                status: LegacySourceStatus::InvalidFormat,
                file_size_bytes: None,
                has_jet_header: false,
                lock_indicators,
                diagnostics,
            };
        }
    };

    let has_jet_header = match read_header(&path, 256) {
        Ok(header) => header
            .windows(JET_HEADER.len())
            .any(|window| window == JET_HEADER),
        Err(error) if error.kind() == std::io::ErrorKind::PermissionDenied => {
            diagnostics.push("操作系统拒绝只读打开文件".to_owned());
            return LegacySourceInspection {
                path,
                status: LegacySourceStatus::PermissionDenied,
                file_size_bytes: Some(metadata.len()),
                has_jet_header: false,
                lock_indicators,
                diagnostics,
            };
        }
        Err(error) => {
            diagnostics.push(format!("读取文件头失败：{}", error.kind()));
            false
        }
    };

    if !lock_indicators.is_empty() {
        diagnostics.push(
            "检测到 Access/MoneyHome8 锁文件线索，后续认证或枚举前应先确认进程状态".to_owned(),
        );
    }
    if !has_jet_header {
        diagnostics.push("未在文件头前 256 字节识别到 Standard Jet DB 标记".to_owned());
    }

    let status = if !lock_indicators.is_empty() {
        LegacySourceStatus::Locked
    } else if has_jet_header {
        LegacySourceStatus::Success
    } else {
        LegacySourceStatus::InvalidFormat
    };

    lock_indicators.sort();
    LegacySourceInspection {
        path,
        status,
        file_size_bytes: Some(metadata.len()),
        has_jet_header,
        lock_indicators,
        diagnostics,
    }
}

fn read_header(path: &Path, limit: usize) -> std::io::Result<Vec<u8>> {
    let mut file = File::open(path)?;
    let mut buffer = vec![0; limit];
    let read = file.read(&mut buffer)?;
    buffer.truncate(read);
    Ok(buffer)
}

fn detect_lock_indicators(path: &Path) -> Vec<PathBuf> {
    let mut indicators = Vec::new();
    let Some(parent) = path.parent() else {
        return indicators;
    };

    if let Some(stem) = path.file_stem().and_then(|name| name.to_str()) {
        let access_lock = parent.join(format!("~${stem}.ldb"));
        if access_lock.is_file() {
            indicators.push(access_lock);
        }
    }

    for lock_name in ["mh.ldb", "MoneyHome8.ldb"] {
        let lock_path = parent.join(lock_name);
        if lock_path.is_file() {
            indicators.push(lock_path);
        }
    }

    indicators
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reports_missing_legacy_source() {
        let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("artifacts")
            .join("missing-ledger.mh8");
        let inspection = inspect_legacy_file(path);
        assert_eq!(inspection.status, LegacySourceStatus::FileNotFound);
        assert_eq!(inspection.file_size_bytes, None);
    }

    #[test]
    fn detects_test_copy_as_jet_source_when_present() {
        let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("artifacts")
            .join("test-copy.mh8");
        if !path.is_file() {
            return;
        }

        let inspection = Mh8Library::new(path).inspect_read_only();
        assert_eq!(inspection.status, LegacySourceStatus::Success);
        assert!(inspection.has_jet_header);
        assert!(inspection.file_size_bytes.unwrap_or_default() > 0);
    }

    #[test]
    fn detects_decompressed_moneyhome_data_as_jet_source_when_present() {
        let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("artifacts")
            .join("MoneyHome8.data.decompressed.mdb");
        if !path.is_file() {
            return;
        }

        let inspection = inspect_legacy_file(path);
        assert_eq!(inspection.status, LegacySourceStatus::Success);
        assert!(inspection.has_jet_header);
    }
}
