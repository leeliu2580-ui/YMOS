# HEARTBEAT.md

## Backup Check

每天执行：
- Windows: `./backup.ps1`
- Git Bash / Linux / macOS: `./backup.sh`

检查规则：
- 如果 push 成功：`BACKUP_OK`
- 如果 push 失败：`BACKUP_FAILED`

说明：
- 优先使用当前环境可执行的脚本
- 如果没有变更，允许跳过 commit，但仍要检查 push 是否可用
