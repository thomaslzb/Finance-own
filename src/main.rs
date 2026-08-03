//! MoneyHome8 Rust 重构入口。

fn main() {
    // 当前阶段先输出工程状态，后续再替换为桌面应用启动流程。
    println!("{}", finance_own::app::bootstrap::startup_banner());
}
