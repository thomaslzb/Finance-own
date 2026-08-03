use std::path::PathBuf;

/// 旧数据源只读检查状态。
///
/// 第一阶段只把外部旧格式归类为迁移输入或诊断输入，不把它们作为新账簿真相源。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LegacySourceStatus {
    /// 文件存在，且当前检查项达到只读识别要求。
    Success,
    /// 指定文件不存在或路径不是普通文件。
    FileNotFound,
    /// 检测到同名锁文件、Access 锁库或 MoneyHome8 进程占用线索。
    Locked,
    /// 操作系统拒绝只读访问。
    PermissionDenied,
    /// 文件可识别为受控 Jet/Access 数据库，但缺少工作组账号或口令。
    AuthFailed,
    /// 连接层成功但对象列表不可见，通常表示对象级权限仍未打通。
    ObjectInvisible,
    /// 当前适配器尚未实现该检查。
    NotImplemented,
    /// 文件头或结构不是当前已确认格式。
    InvalidFormat,
}

/// 旧数据源只读检查结果。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LegacySourceInspection {
    /// 被检查的旧数据源路径。
    pub path: PathBuf,
    /// 本次检查得到的最高优先级状态。
    pub status: LegacySourceStatus,
    /// 文件大小，单位字节；文件不存在时为空。
    pub file_size_bytes: Option<u64>,
    /// 是否在文件头或解压副本中识别到 Jet/Access 数据库标记。
    pub has_jet_header: bool,
    /// 检测到的锁文件或占用线索路径。
    pub lock_indicators: Vec<PathBuf>,
    /// 诊断说明，只记录技术状态，不包含账簿敏感数据。
    pub diagnostics: Vec<String>,
}
