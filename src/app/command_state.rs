/// 命令在当前界面上下文中的可用状态。
///
/// `Hidden` 用于批量模式等不应提前暴露的命令；`Disabled` 用于需要保留位置、
/// 但必须等待选择或数据加载完成的命令。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CommandState {
    /// 命令可见且可执行。
    Enabled,
    /// 命令可见但不可执行。
    Disabled,
    /// 命令在当前模式下不显示。
    Hidden,
}

/// 列表或表格的当前选择数量。
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct SelectionState {
    count: usize,
}

impl SelectionState {
    /// 创建选择状态；`count` 为零表示没有选中记录。
    pub const fn new(count: usize) -> Self {
        Self { count }
    }

    /// 返回当前选中记录数。
    pub const fn count(self) -> usize {
        self.count
    }

    /// 返回是否至少选中一条记录。
    pub const fn has_selection(self) -> bool {
        self.count > 0
    }
}

/// 财务记录页是否处于批量操作模式。
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum BatchMode {
    /// 普通浏览和单条操作模式。
    #[default]
    Inactive,
    /// 批量选择和批量设置模式。
    Active,
}

/// 财务记录页的选择相关命令状态。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct LedgerCommandStates {
    /// 修改当前记录。
    pub modify: CommandState,
    /// 删除当前记录。
    pub delete: CommandState,
    /// 从当前记录位置开始查找。
    pub find: CommandState,
    /// 批量设置标签。
    pub set_tags_in_batch: CommandState,
    /// 批量设置说明。
    pub set_description_in_batch: CommandState,
    /// 退出批量模式。
    pub exit_batch_mode: CommandState,
}

impl LedgerCommandStates {
    /// 根据记录选择和批量模式计算命令状态。
    ///
    /// 旧程序在无选择时禁用修改、删除和查找；批量命令只在批量模式下显示，
    /// 并在至少选择一条记录后允许修改数据。
    pub const fn from_context(selection: SelectionState, batch_mode: BatchMode) -> Self {
        let selected = if selection.has_selection() {
            CommandState::Enabled
        } else {
            CommandState::Disabled
        };

        let (set_tags_in_batch, set_description_in_batch, exit_batch_mode) = match batch_mode {
            BatchMode::Inactive => (
                CommandState::Hidden,
                CommandState::Hidden,
                CommandState::Hidden,
            ),
            BatchMode::Active => (selected, selected, CommandState::Enabled),
        };

        Self {
            modify: selected,
            delete: selected,
            find: selected,
            set_tags_in_batch,
            set_description_in_batch,
            exit_batch_mode,
        }
    }
}

/// 报表数据相对筛选条件的加载状态。
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum ReportLoadState {
    /// 尚未生成报表结果。
    #[default]
    Empty,
    /// 正在执行查询。
    Loading,
    /// 筛选条件已变化，当前结果需要刷新。
    Dirty,
    /// 报表结果已成功加载；行数用于区分空结果和可导出结果。
    Ready {
        /// 当前结果投影的记录数。
        row_count: usize,
    },
    /// 最近一次查询失败，可由用户重新刷新。
    Failed,
}

/// 报表页的结果相关命令状态。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ReportCommandStates {
    /// 使用当前筛选条件刷新报表。
    pub refresh: CommandState,
    /// 导出已经加载的报表结果。
    pub export_report: CommandState,
    /// 预览已经加载的报表打印布局。
    pub print_preview: CommandState,
}

impl ReportCommandStates {
    /// 根据报表加载状态计算刷新、导出和打印命令。
    ///
    /// 导出和打印只读取已经完成的同一份结果投影，避免筛选条件变化后导出旧数据。
    pub const fn from_load_state(load_state: ReportLoadState) -> Self {
        match load_state {
            ReportLoadState::Empty => Self {
                refresh: CommandState::Enabled,
                export_report: CommandState::Disabled,
                print_preview: CommandState::Disabled,
            },
            ReportLoadState::Loading => Self {
                refresh: CommandState::Disabled,
                export_report: CommandState::Disabled,
                print_preview: CommandState::Disabled,
            },
            ReportLoadState::Dirty | ReportLoadState::Failed => Self {
                refresh: CommandState::Enabled,
                export_report: CommandState::Disabled,
                print_preview: CommandState::Disabled,
            },
            ReportLoadState::Ready { row_count } if row_count > 0 => Self {
                refresh: CommandState::Enabled,
                export_report: CommandState::Enabled,
                print_preview: CommandState::Enabled,
            },
            ReportLoadState::Ready { .. } => Self {
                refresh: CommandState::Enabled,
                export_report: CommandState::Disabled,
                print_preview: CommandState::Disabled,
            },
        }
    }
}

/// 导入预览页的输入和选择上下文。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ImportCommandContext {
    /// 是否已经解析出可导入的有效输入。
    pub has_valid_input: bool,
    /// 预览表格中的当前选择状态。
    pub selection: SelectionState,
}

impl ImportCommandContext {
    /// 返回“导入选中记录”的状态。
    pub const fn import_selected(self) -> CommandState {
        if self.has_valid_input && self.selection.has_selection() {
            CommandState::Enabled
        } else {
            CommandState::Disabled
        }
    }

    /// 返回“从剪贴板导入”的状态。
    ///
    /// 剪贴板内容的格式校验由适配器完成；这里只消费校验后的布尔结果。
    pub const fn import_from_clipboard(has_valid_clipboard_data: bool) -> CommandState {
        if has_valid_clipboard_data {
            CommandState::Enabled
        } else {
            CommandState::Disabled
        }
    }
}

/// 标签页的选择相关命令状态。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TagCommandStates {
    /// 从当前标签移出所选记录。
    pub remove_from_current: CommandState,
    /// 将所选记录转移到其它标签。
    pub move_selected: CommandState,
    /// 将所选记录快速加入标签。
    pub quick_add: CommandState,
    /// 修改当前标签定义。
    pub modify_tag: CommandState,
    /// 删除当前标签定义。
    pub delete_tag: CommandState,
    /// 隐藏当前标签定义。
    pub hide_tag: CommandState,
}

impl TagCommandStates {
    /// 根据当前标签和记录选择计算命令状态。
    pub const fn from_context(tag_selected: bool, records: SelectionState) -> Self {
        let tag_command = if tag_selected {
            CommandState::Enabled
        } else {
            CommandState::Disabled
        };
        let record_command = if records.has_selection() {
            CommandState::Enabled
        } else {
            CommandState::Disabled
        };

        Self {
            remove_from_current: record_command,
            move_selected: record_command,
            quick_add: record_command,
            modify_tag: tag_command,
            delete_tag: tag_command,
            hide_tag: tag_command,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ledger_selection_and_batch_mode_drive_commands() {
        let empty = LedgerCommandStates::from_context(SelectionState::new(0), BatchMode::Inactive);
        assert_eq!(empty.modify, CommandState::Disabled);
        assert_eq!(empty.set_tags_in_batch, CommandState::Hidden);

        let batch = LedgerCommandStates::from_context(SelectionState::new(2), BatchMode::Active);
        assert_eq!(batch.delete, CommandState::Enabled);
        assert_eq!(batch.set_tags_in_batch, CommandState::Enabled);
        assert_eq!(batch.exit_batch_mode, CommandState::Enabled);
    }

    #[test]
    fn report_result_commands_require_ready_state() {
        let dirty = ReportCommandStates::from_load_state(ReportLoadState::Dirty);
        assert_eq!(dirty.refresh, CommandState::Enabled);
        assert_eq!(dirty.export_report, CommandState::Disabled);

        let ready = ReportCommandStates::from_load_state(ReportLoadState::Ready { row_count: 12 });
        assert_eq!(ready.export_report, CommandState::Enabled);
        assert_eq!(ready.print_preview, CommandState::Enabled);

        let empty_result =
            ReportCommandStates::from_load_state(ReportLoadState::Ready { row_count: 0 });
        assert_eq!(empty_result.export_report, CommandState::Disabled);
    }

    #[test]
    fn import_commands_require_validated_input() {
        let context = ImportCommandContext {
            has_valid_input: true,
            selection: SelectionState::new(1),
        };
        assert_eq!(context.import_selected(), CommandState::Enabled);
        assert_eq!(
            ImportCommandContext::import_from_clipboard(false),
            CommandState::Disabled
        );
    }

    #[test]
    fn tag_commands_distinguish_tag_and_record_selection() {
        let state = TagCommandStates::from_context(true, SelectionState::new(0));
        assert_eq!(state.modify_tag, CommandState::Enabled);
        assert_eq!(state.remove_from_current, CommandState::Disabled);
    }
}
