/// 顶层账簿会话状态。
///
/// UI 壳层必须先消费该状态，再决定是否加载业务工作区；这样可以避免无账簿或打开失败时
/// 仍然触发 SQLite、旧账簿或外部参考库读取。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LedgerSessionState {
    /// 尚未选择或创建账簿。
    NoLedger,
    /// 正在打开账簿；此时业务命令应保持禁用。
    Opening {
        /// 用户选择的账簿路径或展示名，失败时用于错误页追溯。
        target: String,
    },
    /// 已打开账簿，可以进入业务工作区。
    Opened {
        /// 当前账簿稳定标识。
        ledger_id: String,
        /// 当前账簿显示名称。
        ledger_name: String,
    },
    /// 正在关闭账簿；此时应等待后台写入、备份或同步进入可恢复状态。
    Closing {
        /// 正在关闭的账簿稳定标识。
        ledger_id: String,
    },
    /// 打开或恢复失败，用户可重新选择账簿或查看诊断。
    Failed {
        /// 失败目标路径或账簿显示名。
        target: String,
        /// 已脱敏的失败原因。
        reason: String,
    },
}

impl LedgerSessionState {
    /// 返回业务工作区是否可以读取当前账簿数据。
    pub const fn can_enter_workspace(&self) -> bool {
        matches!(self, Self::Opened { .. })
    }
}

/// 第一阶段目标 UI 的四大工作区。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum WorkspaceKind {
    /// 财务数据：账户、基础资料、流水浏览和资料管理入口。
    FinanceData,
    /// 记账：日常收支、转账、工资、分拆、批量模板和投资交易录入入口。
    Bookkeeping,
    /// 财务报表：报表定义、筛选、结果表、图表、导出和打印入口。
    FinancialReports,
    /// 财务分析：预算、诊断、规划、目标和分析图表入口。
    FinancialAnalysis,
}

/// 工作区内容加载状态。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum WorkspaceLoadState {
    /// 当前工作区尚未加载或没有账簿上下文。
    Empty,
    /// 正在加载首屏数据。
    Loading,
    /// 工作区已可交互。
    Ready,
    /// 工作区加载失败，保留错误说明用于页面错误状态。
    Failed {
        /// 已脱敏的错误说明。
        reason: String,
    },
}

/// 顶层工作区壳层状态。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WorkspaceShellState {
    /// 当前账簿会话状态。
    pub ledger_session: LedgerSessionState,
    /// 当前选中的顶层工作区。
    pub active_workspace: WorkspaceKind,
    /// 当前工作区内容状态。
    pub load_state: WorkspaceLoadState,
}

impl WorkspaceShellState {
    /// 创建无账簿空壳层。
    pub const fn no_ledger() -> Self {
        Self {
            ledger_session: LedgerSessionState::NoLedger,
            active_workspace: WorkspaceKind::FinanceData,
            load_state: WorkspaceLoadState::Empty,
        }
    }

    /// 根据账簿打开结果创建可交互壳层。
    pub fn opened(ledger_id: impl Into<String>, ledger_name: impl Into<String>) -> Self {
        Self {
            ledger_session: LedgerSessionState::Opened {
                ledger_id: ledger_id.into(),
                ledger_name: ledger_name.into(),
            },
            active_workspace: WorkspaceKind::FinanceData,
            load_state: WorkspaceLoadState::Ready,
        }
    }

    /// 尝试切换工作区；无账簿、打开中、关闭中或失败状态只记录目标工作区，不加载业务数据。
    pub fn switch_workspace(&mut self, workspace: WorkspaceKind) {
        self.active_workspace = workspace;
        self.load_state = if self.ledger_session.can_enter_workspace() {
            WorkspaceLoadState::Loading
        } else {
            WorkspaceLoadState::Empty
        };
    }

    /// 标记当前工作区首屏数据加载完成。
    pub fn mark_ready(&mut self) {
        if self.ledger_session.can_enter_workspace() {
            self.load_state = WorkspaceLoadState::Ready;
        }
    }

    /// 标记当前工作区加载失败。
    pub fn mark_failed(&mut self, reason: impl Into<String>) {
        self.load_state = WorkspaceLoadState::Failed {
            reason: reason.into(),
        };
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn no_ledger_shell_keeps_workspace_empty() {
        let mut shell = WorkspaceShellState::no_ledger();
        shell.switch_workspace(WorkspaceKind::Bookkeeping);

        assert_eq!(shell.active_workspace, WorkspaceKind::Bookkeeping);
        assert_eq!(shell.load_state, WorkspaceLoadState::Empty);
        assert!(!shell.ledger_session.can_enter_workspace());
    }

    #[test]
    fn opened_shell_loads_selected_workspace_then_becomes_ready() {
        let mut shell = WorkspaceShellState::opened("ledger-1", "家庭账簿");
        shell.switch_workspace(WorkspaceKind::FinancialReports);

        assert_eq!(shell.load_state, WorkspaceLoadState::Loading);
        shell.mark_ready();
        assert_eq!(shell.load_state, WorkspaceLoadState::Ready);
    }

    #[test]
    fn failed_workspace_preserves_diagnostic_reason() {
        let mut shell = WorkspaceShellState::opened("ledger-1", "家庭账簿");
        shell.mark_failed("报表查询失败");

        assert_eq!(
            shell.load_state,
            WorkspaceLoadState::Failed {
                reason: "报表查询失败".to_owned()
            }
        );
    }
}
