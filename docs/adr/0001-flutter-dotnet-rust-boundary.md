# Flutter, .NET, and Rust Boundary

Finance Own will use Flutter for PC, mobile, and Web UI, .NET as the first-version cloud service technology, and Rust as an embedded PC local core for legacy migration, local offline ledger work, import/export, and high-risk financial processing. This avoids forcing Rust into the cloud service layer while still preserving PC offline capability and the existing Rust migration work.

**Considered Options**

- All Rust: stronger language uniformity, but higher cost for account, sync, Web API, background job, and Flutter integration work.
- All .NET: simpler cloud/backend stack, but weaker fit for PC local legacy migration, file-heavy processing, and the Rust work already completed.
- Flutter + .NET + Rust local core: keeps Flutter focused on three-client UI, .NET focused on cloud services, and Rust focused on PC local correctness and migration.
