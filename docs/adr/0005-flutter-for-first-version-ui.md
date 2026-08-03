# Flutter for First-Version UI

Finance Own will use Flutter as the first-version UI technology for PC, mobile, and Web. This replaces the earlier Rust desktop GUI evaluation path and keeps Slint, Iced, Tauri, and egui out of first-version scope unless a later dedicated prototype reverses this decision.

**Consequences**

- PC UI is Flutter Desktop and calls an embedded Rust local core for local ledger and migration work.
- Mobile UI is Flutter Mobile and focuses on lightweight offline drafts, queueing, and synchronization.
- Web UI is Flutter Web and is online-first through the .NET API.
