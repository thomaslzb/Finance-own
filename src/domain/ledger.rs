/// 账本基础信息。
///
/// 当前仅保留最小骨架，后续再逐步映射 `test.mh8` 中的真实业务字段。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LedgerProfile {
    /// 账本显示名称。
    pub name: String,
}

impl LedgerProfile {
    /// 创建一个最小账本对象，供后续导入流程和 UI 原型共用。
    pub fn new(name: impl Into<String>) -> Self {
        Self { name: name.into() }
    }
}
