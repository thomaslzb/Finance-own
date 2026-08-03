# Finance Own 项目约束

本文件只约束 `Finance-own` Rust 重构项目及其子目录；用户在对话中的最新明确指令始终优先。

## 项目专用例外

- 本项目不读取、不写入 `C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\MyRules.txt`。
- 本项目不读取、不写入 `C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\MyBugLog.txt`。
- MoneyHome8 的新增、修改、删除和动态验证只能使用 `C:\DCG-SZ\IT Manage\Private\Personal-Docs\test.mh8`，不得操作其它账簿。
- Rust 重构生成、修改、导出和整理的文件必须位于 `C:\DCG-SZ\SZ-System-Docs\CodexWorkSpace\Finance-own` 或其子目录。

## 当前验证边界

- 静态分析证据可以从 MoneyHome8 程序文件和指定测试账簿读取。
- 动态操作前后必须核对 `test.mh8` 的路径、锁文件、进程状态和文件指纹。
- 不得把尚未通过真实操作验证的旧格式、投资公式或外部协议标记为已兼容。
