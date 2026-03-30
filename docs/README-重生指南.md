# README-重生指南

> 目标：当你换电脑、重装系统、或本地环境损坏时，用这份指南尽快把 YMOS 工作区恢复到可继续工作的状态。

---

## 1. 这份仓库里保存了什么

GitHub 仓库当前保存的是“核心生命体”：

- 主要文档、SOP、策略文件
- `skills/` 中已纳入版本控制的技能
- `memory/`、`MEMORY.md`
- `AGENTS.md`、`SOUL.md`、`TOOLS.md`、`USER.md`
- `backup.ps1`、`backup.sh`
- `HEARTBEAT.md`

GitHub 仓库**不再保存**以下本地态/赘肉：

- `.tools/`
- `output/`
- `.openclaw/`
- `.clawhub/`
- `skills/cmc-official`（本地可用，但不再由主仓库跟踪）

这意味着：

- **核心知识和工作流可以重生**
- **本地运行时、缓存、输出文件需要重新准备**

---

## 2. 新电脑首次恢复

### 2.1 安装基础工具

至少安装：

- Git
- PowerShell 7+（推荐；Windows PowerShell 也可用）
- 你工作流需要的运行环境（按项目实际情况补充）
  - Node.js
  - Python
  - OpenClaw / 相关本地工具

### 2.2 克隆仓库

在新电脑上执行：

```powershell
git clone https://github.com/leeliu2580-ui/YMOS.git
cd YMOS
```

如果你想恢复到固定目录，可改成：

```powershell
cd D:\0_workspace\trae_2601\ymos
git clone https://github.com/leeliu2580-ui/YMOS.git YMOS
cd YMOS
```

### 2.3 检查仓库状态

```powershell
git remote -v
git branch --show-current
```

期望结果：

- remote 指向：`https://github.com/leeliu2580-ui/YMOS.git`
- 当前分支：`main`

---

## 3. 恢复后哪些东西会缺失

因为仓库已经做过“瘦身 + 历史清理”，以下内容不会自动随 clone 出现：

### 3.1 `.tools/`

这是本地运行时/工具目录，不再进入 Git。

如果后续某些脚本依赖 `.tools/`，需要你：

- 手动重新安装相应工具
- 或重新下载到本地
- 或改用系统全局安装版本

### 3.2 `output/`

这是产物目录。

恢复原则：

- 需要时重新生成
- 不作为“系统灵魂”的组成部分

### 3.3 `.openclaw/` / `.clawhub/`

这是本地状态目录。

恢复原则：

- 允许重新生成
- 不需要从 Git 恢复

### 3.4 `skills/cmc-official`

这个目录现在是：

- 本地可保留使用
- 不随主仓库备份

如果新电脑也要用它，你需要单独恢复它。可选做法：

- 从它自己的来源重新拉取/安装
- 手动从旧电脑拷过去
- 后续单独给它建立独立仓库或正式 submodule（推荐后续再整理）

---

## 4. 备份系统恢复

仓库内已经包含：

- `backup.ps1`
- `backup.sh`
- `HEARTBEAT.md`

### 4.1 Windows 环境

执行：

```powershell
./backup.ps1
```

逻辑：

- `git add .`
- 有变更则自动提交
- 无变更则跳过 commit
- 最后 push 到 `origin main`
- 成功输出：`BACKUP_OK`

### 4.2 Git Bash / Linux / macOS

执行：

```bash
./backup.sh
```

如无执行权限：

```bash
chmod +x backup.sh
./backup.sh
```

---

## 5. 恢复后的自检清单

建议按顺序执行。

### 5.1 Git 检查

```powershell
git remote -v
git branch --show-current
git status --short
```

### 5.2 备份脚本检查

```powershell
./backup.ps1
```

期望：

- 无报错
- 成功 push 时输出 `BACKUP_OK`

### 5.3 Heartbeat 检查

确认 `HEARTBEAT.md` 中有 Backup Check 区块。

关键内容应包括：

- Windows 使用 `./backup.ps1`
- Unix-like 环境使用 `./backup.sh`
- 成功：`BACKUP_OK`
- 失败：`BACKUP_FAILED`

---

## 6. 如果旧电脑还有一份仓库副本

这个仓库已经做过一次 **历史重写（force push）**。

所以旧副本不要盲目直接继续推送，最稳妥做法是：

### 方案 A：直接重新 clone（推荐）

最干净，最省心。

### 方案 B：硬重置到远端

如果你明确知道自己在做什么，可以：

```powershell
git fetch origin
git reset --hard origin/main
```

**警告：** 这会丢弃当前工作树未保存改动。

---

## 7. 灾难恢复

### 7.1 GitHub 还在，远端正常

最简单：

```powershell
git clone https://github.com/leeliu2580-ui/YMOS.git
```

### 7.2 如果你需要回看历史清理前的旧状态

本地保留过一个 bundle 快照（如果旧机器还在）：

```text
.git/backup-pre-filter-YYYYMMDD-HHMMSS.bundle
```

可用方式示例：

```powershell
git clone path\to\backup-pre-filter-20260331-053729.bundle old-recovery
```

或：

```powershell
git fetch path\to\backup-pre-filter-20260331-053729.bundle
```

这个 bundle 更像“后悔药”，不是日常恢复主路径。

---

## 8. 真正影响“重生”的关键原则

记住一句话：

> 真正重要的是“源码 + 记忆 + SOP + 恢复方法”，不是缓存、日志和本地二进制。

所以以后新增内容时，建议按这个标准判断：

### 应该进 Git 的

- 文档
- 规则
- SOP
- 核心源码
- 技能定义
- 重要 memory
- 恢复说明
- 自动化脚本

### 不应该进 Git 的

- 缓存
- 日志
- 临时产物
- 大型本地二进制
- 本地状态目录
- 可重新下载/重新生成的文件

---

## 9. 建议的换机恢复顺序（最短路径）

1. 安装 Git / PowerShell / 必要运行环境
2. clone `YMOS`
3. 检查 `remote` 和 `main`
4. 手动恢复本地依赖工具
5. 单独恢复 `skills/cmc-official`（如需要）
6. 运行 `./backup.ps1`
7. 确认输出 `BACKUP_OK`
8. 开始继续工作

---

## 10. 当前仓库恢复基线

- 仓库：`https://github.com/leeliu2580-ui/YMOS.git`
- 默认分支：`main`
- 备份命令（Windows）：`./backup.ps1`
- 备份命令（Unix-like）：`./backup.sh`

如果你看到这些都正常，说明“小龙虾”已经成功重生。
