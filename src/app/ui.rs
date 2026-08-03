use std::collections::HashMap;

use crate::{
    app::{
        reference_data::{ReferenceDataError, ReferenceDataRepository},
        reporting::{LedgerEntryFilter, ReportReadError, ReportReadRepository},
        workspace_shell::WorkspaceShellState,
    },
    domain::{
        reference_data::{AccountGroupRecord, AccountRecord, LedgerRecord},
        reporting::{AccountBalanceProjection, LedgerEntryProjection},
    },
};

/// UI 适配层读取首屏数据时的结构化错误。
///
/// 该错误只表达页面模型装配失败的原因，不绑定 Flutter 的弹窗、Toast 或日志实现。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum UiProjectionError {
    /// 账户、账簿或基础资料读取失败。
    ReferenceData(ReferenceDataError),
    /// 报表、余额或流水投影读取失败。
    ReportRead(ReportReadError),
    /// 仓储返回的数据无法组成一致页面，例如余额引用了不存在的账户。
    InconsistentData(String),
}

/// 首个桌面纵向原型可消费的主页视图模型。
///
/// 该模型聚合工作区壳层、账户中心和财务记录摘要，Flutter 只负责绑定显示和命令回调。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WorkspaceHomeViewModel {
    /// 当前账簿基础信息。
    pub ledger: LedgerRecord,
    /// 当前工作区壳层状态，用于导航、高亮和加载状态展示。
    pub shell: WorkspaceShellState,
    /// 账户中心首屏树和余额。
    pub account_center: AccountCenterViewModel,
    /// 财务记录首屏列表，默认不包含作废记录。
    pub recent_entries: Vec<LedgerEntryProjection>,
}

/// 账户中心首屏视图模型。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AccountCenterViewModel {
    /// 有分组归属的账户树。
    pub groups: Vec<AccountGroupViewNode>,
    /// 没有关联账户组或原组已失效的账户；UI 应明确归入未分组区。
    pub ungrouped_accounts: Vec<AccountViewRow>,
    /// 按币种汇总的资产账户余额。
    pub asset_totals: Vec<CurrencyBalanceSummary>,
    /// 按币种汇总的负债账户余额。
    pub liability_totals: Vec<CurrencyBalanceSummary>,
}

/// 账户组树节点。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AccountGroupViewNode {
    /// 账户组稳定标识。
    pub id: String,
    /// 账户组名称。
    pub name: String,
    /// 分组类型键，交给 Flutter 映射图标或颜色。
    pub kind: String,
    /// 同级排序值。
    pub sort_order: i64,
    /// 当前组直属账户。
    pub accounts: Vec<AccountViewRow>,
    /// 当前组直属子组。
    pub children: Vec<AccountGroupViewNode>,
}

/// 账户列表展示行。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AccountViewRow {
    /// 账户稳定标识。
    pub id: String,
    /// 可选账户组标识；保留它是为了让 Flutter 端实现分组拖拽和迁移命令。
    pub group_id: Option<String>,
    /// 账户名称。
    pub name: String,
    /// 账户类型键，Flutter 可据此选择图标。
    pub kind: String,
    /// 账户币种。
    pub currency_code: String,
    /// 当前已入账余额，单位为账户币种最小单位。
    pub balance_minor: i64,
    /// `true` 表示资产账户，`false` 表示负债账户。
    pub is_asset: bool,
    /// 是否隐藏；隐藏账户仍应在显式管理视图可见。
    pub is_hidden: bool,
    /// 可选关闭日期。
    pub closed_on: Option<String>,
}

/// 同一币种下的余额汇总。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CurrencyBalanceSummary {
    /// 汇总币种。
    pub currency_code: String,
    /// 汇总后的最小单位余额。
    pub balance_minor: i64,
}

/// 读取并装配首个桌面纵向原型的主页数据。
///
/// 该函数是 Flutter PC 本地 API 的应用层入口：它只依赖应用端口，不直接依赖 `rusqlite`
/// 或任何具体 Flutter 控件，保护 PC 本地 API 与页面之间不用复制业务状态。
pub fn load_workspace_home(
    reference_repository: &impl ReferenceDataRepository,
    report_repository: &impl ReportReadRepository,
    ledger_id: &str,
) -> Result<WorkspaceHomeViewModel, UiProjectionError> {
    let ledger = reference_repository
        .get_ledger(ledger_id)
        .map_err(UiProjectionError::ReferenceData)?;
    let groups = reference_repository
        .list_account_groups(ledger_id)
        .map_err(UiProjectionError::ReferenceData)?;
    let accounts = reference_repository
        .list_accounts(ledger_id)
        .map_err(UiProjectionError::ReferenceData)?;
    let balances = report_repository
        .list_account_balances(ledger_id)
        .map_err(UiProjectionError::ReportRead)?;
    let recent_entries = report_repository
        .list_ledger_entries(&LedgerEntryFilter {
            ledger_id: ledger_id.to_owned(),
            date_range: None,
            account_ids: Vec::new(),
            category_ids: Vec::new(),
            tag_ids: Vec::new(),
            include_voided: false,
        })
        .map_err(UiProjectionError::ReportRead)?;

    Ok(WorkspaceHomeViewModel {
        shell: WorkspaceShellState::opened(&ledger.id, &ledger.name),
        account_center: build_account_center(groups, accounts, balances)?,
        ledger,
        recent_entries,
    })
}

/// 根据基础资料和余额投影组装账户中心页面模型。
pub fn build_account_center(
    groups: Vec<AccountGroupRecord>,
    accounts: Vec<AccountRecord>,
    balances: Vec<AccountBalanceProjection>,
) -> Result<AccountCenterViewModel, UiProjectionError> {
    let mut balance_by_account = HashMap::new();
    for balance in balances {
        if balance_by_account
            .insert(balance.account_id.clone(), balance)
            .is_some()
        {
            return Err(UiProjectionError::InconsistentData(
                "账户余额投影中出现重复账户".to_owned(),
            ));
        }
    }

    let group_ids: HashMap<String, AccountGroupRecord> = groups
        .iter()
        .map(|group| (group.id.clone(), group.clone()))
        .collect();
    let mut accounts_by_group: HashMap<String, Vec<AccountViewRow>> = HashMap::new();
    let mut ungrouped_accounts = Vec::new();
    let mut asset_totals = HashMap::new();
    let mut liability_totals = HashMap::new();

    for account in accounts {
        let balance = balance_by_account
            .remove(&account.id)
            .map(|balance| balance.balance_minor)
            .unwrap_or(0);
        let row = account_row(account, balance);
        add_currency_total(
            if row.is_asset {
                &mut asset_totals
            } else {
                &mut liability_totals
            },
            &row.currency_code,
            row.balance_minor,
        )?;

        if let Some(group_id) = row_group_id(&row, &group_ids) {
            accounts_by_group.entry(group_id).or_default().push(row);
        } else {
            ungrouped_accounts.push(row);
        }
    }

    if !balance_by_account.is_empty() {
        return Err(UiProjectionError::InconsistentData(
            "账户余额投影引用了不存在的账户".to_owned(),
        ));
    }

    let mut roots = build_group_tree(None, &groups, &mut accounts_by_group);
    sort_account_rows(&mut ungrouped_accounts);
    sort_group_nodes(&mut roots);

    Ok(AccountCenterViewModel {
        groups: roots,
        ungrouped_accounts,
        asset_totals: currency_totals(asset_totals),
        liability_totals: currency_totals(liability_totals),
    })
}

fn account_row(account: AccountRecord, balance_minor: i64) -> AccountViewRow {
    AccountViewRow {
        id: account.id,
        group_id: account.group_id,
        name: account.name,
        kind: account.kind,
        currency_code: account.currency_code,
        balance_minor,
        is_asset: account.is_asset,
        is_hidden: account.is_hidden,
        closed_on: account.closed_on,
    }
}

fn row_group_id(
    row: &AccountViewRow,
    group_ids: &HashMap<String, AccountGroupRecord>,
) -> Option<String> {
    row.group_id
        .as_ref()
        .filter(|group_id| group_ids.contains_key(*group_id))
        .cloned()
}

fn build_group_tree(
    parent_id: Option<&str>,
    groups: &[AccountGroupRecord],
    accounts_by_group: &mut HashMap<String, Vec<AccountViewRow>>,
) -> Vec<AccountGroupViewNode> {
    groups
        .iter()
        .filter(|group| normalized_parent_id(group, groups) == parent_id)
        .map(|group| {
            let mut accounts = accounts_by_group.remove(&group.id).unwrap_or_default();
            sort_account_rows(&mut accounts);
            AccountGroupViewNode {
                id: group.id.clone(),
                name: group.name.clone(),
                kind: group.kind.clone(),
                sort_order: group.sort_order,
                accounts,
                children: build_group_tree(Some(&group.id), groups, accounts_by_group),
            }
        })
        .collect()
}

fn normalized_parent_id<'a>(
    group: &'a AccountGroupRecord,
    groups: &'a [AccountGroupRecord],
) -> Option<&'a str> {
    group
        .parent_id
        .as_deref()
        .filter(|parent_id| groups.iter().any(|candidate| candidate.id == *parent_id))
}

fn add_currency_total(
    totals: &mut HashMap<String, i64>,
    currency_code: &str,
    balance_minor: i64,
) -> Result<(), UiProjectionError> {
    let total = totals.entry(currency_code.to_owned()).or_insert(0);
    *total = total.checked_add(balance_minor).ok_or_else(|| {
        UiProjectionError::InconsistentData("账户余额汇总超过 i64 范围".to_owned())
    })?;
    Ok(())
}

fn currency_totals(totals: HashMap<String, i64>) -> Vec<CurrencyBalanceSummary> {
    let mut rows: Vec<_> = totals
        .into_iter()
        .map(|(currency_code, balance_minor)| CurrencyBalanceSummary {
            currency_code,
            balance_minor,
        })
        .collect();
    rows.sort_by(|left, right| left.currency_code.cmp(&right.currency_code));
    rows
}

fn sort_group_nodes(nodes: &mut [AccountGroupViewNode]) {
    nodes.sort_by(|left, right| {
        left.sort_order
            .cmp(&right.sort_order)
            .then_with(|| left.name.cmp(&right.name))
            .then_with(|| left.id.cmp(&right.id))
    });
    for node in nodes {
        sort_group_nodes(&mut node.children);
    }
}

fn sort_account_rows(rows: &mut [AccountViewRow]) {
    rows.sort_by(|left, right| {
        left.name
            .cmp(&right.name)
            .then_with(|| left.id.cmp(&right.id))
    });
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::app::workspace_shell::{LedgerSessionState, WorkspaceKind};

    fn group(id: &str, parent_id: Option<&str>, sort_order: i64) -> AccountGroupRecord {
        AccountGroupRecord {
            id: id.to_owned(),
            ledger_id: "ledger-1".to_owned(),
            parent_id: parent_id.map(str::to_owned),
            name: id.to_owned(),
            kind: "asset".to_owned(),
            sort_order,
        }
    }

    fn account(id: &str, group_id: Option<&str>, name: &str, is_asset: bool) -> AccountRecord {
        AccountRecord {
            id: id.to_owned(),
            ledger_id: "ledger-1".to_owned(),
            group_id: group_id.map(str::to_owned),
            name: name.to_owned(),
            kind: "cash".to_owned(),
            currency_code: "CNY".to_owned(),
            institution_name: None,
            account_number_masked: None,
            is_asset,
            is_hidden: false,
            closed_on: None,
            created_at: "2026-08-03T00:00:00+08:00".to_owned(),
        }
    }

    fn balance(account_id: &str, balance_minor: i64) -> AccountBalanceProjection {
        AccountBalanceProjection {
            ledger_id: "ledger-1".to_owned(),
            account_id: account_id.to_owned(),
            account_name: account_id.to_owned(),
            currency_code: "CNY".to_owned(),
            balance_minor,
        }
    }

    #[test]
    fn account_center_keeps_tree_balances_and_totals_framework_neutral() {
        let view = build_account_center(
            vec![group("root", None, 2), group("child", Some("root"), 1)],
            vec![
                account("cash", Some("child"), "现金", true),
                account("card", None, "信用卡", false),
            ],
            vec![balance("cash", 10_000), balance("card", -2_500)],
        )
        .unwrap();

        assert_eq!(view.groups.len(), 1);
        assert_eq!(view.groups[0].children[0].accounts[0].balance_minor, 10_000);
        assert_eq!(view.ungrouped_accounts[0].name, "信用卡");
        assert_eq!(view.asset_totals[0].balance_minor, 10_000);
        assert_eq!(view.liability_totals[0].balance_minor, -2_500);
    }

    #[test]
    fn account_center_rejects_balance_for_unknown_account() {
        let error = build_account_center(Vec::new(), Vec::new(), vec![balance("ghost", 1)])
            .expect_err("unknown account balance should be rejected");

        assert!(matches!(error, UiProjectionError::InconsistentData(_)));
    }

    #[test]
    fn account_center_promotes_group_with_missing_parent_to_root() {
        let view = build_account_center(
            vec![group("orphan", Some("missing-parent"), 1)],
            vec![account("cash", Some("orphan"), "现金", true)],
            vec![balance("cash", 10_000)],
        )
        .unwrap();

        assert_eq!(view.groups[0].id, "orphan");
        assert_eq!(view.groups[0].accounts[0].id, "cash");
    }

    #[test]
    fn workspace_home_uses_opened_financial_data_shell() {
        let shell = WorkspaceShellState::opened("ledger-1", "家庭账簿");

        assert_eq!(shell.active_workspace, WorkspaceKind::FinanceData);
        assert!(matches!(
            shell.ledger_session,
            LedgerSessionState::Opened {
                ref ledger_id,
                ref ledger_name
            } if ledger_id == "ledger-1" && ledger_name == "家庭账簿"
        ));
    }
}
