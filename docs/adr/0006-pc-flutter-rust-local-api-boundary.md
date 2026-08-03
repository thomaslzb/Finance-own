# PC Flutter to Rust Local API Boundary

On PC, Flutter will call the embedded Rust local core through a stable local API or FFI boundary, while Flutter will not directly access SQLite, build SQL, or read legacy ledger files. Rust owns local ledger persistence, migration, validation, and high-risk file processing; Flutter owns interaction, display, and user workflow.

**Consequences**

- Flutter pages bind to DTOs and structured errors rather than database tables.
- Rust can change SQLite internals without forcing page rewrites.
- The preferred implementation path is `flutter_rust_bridge` or an equivalent explicit FFI wrapper.
