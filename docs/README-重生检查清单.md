# README-重生检查清单

> 用法：换电脑或系统重装后，按顺序逐项检查，尽量不要跳步。

---

## A. 基础环境

- [ ] 已安装 Git
- [ ] 已安装 PowerShell 7+（或可用的 Windows PowerShell）
- [ ] 已安装需要的运行环境（如 Node.js / Python / OpenClaw）

---

## B. 克隆仓库

- [ ] 已执行：

```powershell
git clone https://github.com/leeliu2580-ui/YMOS.git
cd YMOS
```

- [ ] `git remote -v` 正常
- [ ] `git branch --show-current` 显示 `main`

---

## C. 核心文件检查

- [ ] `AGENTS.md` 存在
- [ ] `SOUL.md` 存在
- [ ] `TOOLS.md` 存在
- [ ] `MEMORY.md` 存在
- [ ] `memory/` 存在
- [ ] `skills/` 存在
- [ ] `backup.ps1` 存在
- [ ] `backup.sh` 存在
- [ ] `HEARTBEAT.md` 存在
- [ ] `docs/README-重生指南.md` 存在

---

## D. 本地态恢复

这些不会自动从 GitHub 回来，需要手动确认：

- [ ] `.tools/` 如有需要，已重新安装或重建
- [ ] `.openclaw/` 如有需要，已重新生成
- [ ] `.clawhub/` 如有需要，已重新生成
- [ ] `output/` 按需重新生成
- [ ] `skills/cmc-official` 已单独恢复（如需要）

---

## E. 备份系统检查

- [ ] 已执行：

```powershell
./backup.ps1
```

- [ ] 输出包含 `BACKUP_OK`
- [ ] `git status --short` 正常

---

## F. 心跳检查

- [ ] `HEARTBEAT.md` 中存在 `Backup Check`
- [ ] Windows 备份命令为 `./backup.ps1`
- [ ] Unix-like 备份命令为 `./backup.sh`
- [ ] 成功状态为 `BACKUP_OK`
- [ ] 失败状态为 `BACKUP_FAILED`

---

## G. 完成判定

满足以下条件即可视为“小龙虾成功重生”：

- [ ] 仓库可正常拉取与提交
- [ ] 核心文档与 memory 完整
- [ ] 关键 skills 可用
- [ ] 备份脚本可正常 push
- [ ] 后续工作可继续开展
