---
name: using-git-worktrees
description: |
  Git 隔离工作空间技能。开始需要与当前工作隔离的功能开发时使用——创建隔离的 git worktree。
  触发方式：worktree、隔离开发、单独工作空间、并行任务
  Git worktrees isolation skill. Create isolated workspaces for parallel development.
  Trigger: worktree, isolated workspace, separate development
---

# Using Git Worktrees：Git 隔离工作空间

## 概述

Git worktree 创建共享同一仓库的隔离工作空间，允许同时在多个分支上工作而无需切换。

**核心原则：** 系统化目录选择 + 安全验证 = 可靠隔离。

**开始时宣布：** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## 目录选择流程 | Directory Selection Process

按此优先级顺序：

### 1. 检查现有目录

```bash
# 按优先级检查
ls -d .worktrees 2>/dev/null     # 优先（隐藏）
ls -d worktrees 2>/dev/null      # 替代
```

**如果找到：** 使用它。如果两者都存在，`.worktrees` 优先。

### 2. 检查 CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**如果指定了偏好：** 使用它，不问。

### 3. 询问用户

如果没有目录存在且没有 CLAUDE.md 偏好：

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

## 安全验证 | Safety Verification

### 对于项目本地目录（.worktrees 或 worktrees）

**创建 worktree 前必须验证目录被忽略：**

```bash
# 检查目录是否被忽略（遵守本地、全局和系统 gitignore）
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**如果没有被忽略：**

按 Jesse 的规则"立即修复坏掉的东西"：
1. 添加适当行到 .gitignore
2. 提交变更
3. 继续 worktree 创建

### 对于全局目录（~/.config/superpowers/worktrees）

不需要 .gitignore 验证——完全在项目外部。

## 创建步骤 | Creation Steps

### 1. 检测项目名称

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. 创建 Worktree

```bash
# 确定完整路径
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# 用新分支创建 worktree
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. 运行项目设置

自动检测并运行适当设置：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. 验证干净基线

运行测试确保 worktree 起始干净：

```bash
# 示例——使用项目适当的命令
npm test
cargo test
pytest
go test ./...
```

**如果测试失败：** 报告失败，询问是继续还是调查。

**如果测试通过：** 报告就绪。

### 5. 报告位置

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## 快速参考 | Quick Reference

| 情况 | 动作 |
|------|------|
| `.worktrees/` 存在 | 使用它（验证被忽略） |
| `worktrees/` 存在 | 使用它（验证被忽略） |
| 两者都存在 | 使用 `.worktrees/` |
| 都不存在 | 检查 CLAUDE.md → 询问用户 |
| 目录没有被忽略 | 添加到 .gitignore + 提交 |
| 测试在基线时失败 | 报告失败 + 询问 |
| 没有 package.json/Cargo.toml | 跳过依赖安装 |

## 常见错误 | Common Mistakes

### 跳过 ignore 验证

- **问题：** Worktree 内容被跟踪，污染 git status
- **修复：** 创建项目本地 worktree 前始终使用 `git check-ignore`

### 假设目录位置

- **问题：** 创建不一致，违反项目约定
- **修复：** 按优先级遵循：现有 > CLAUDE.md > 询问

### 在测试失败时继续

- **问题：** 无法区分新 Bug 和已有问题
- **修复：** 报告失败，获得明确许可继续

## 整合关系 | Integration

**被调用于：**
- **brainstorming**（阶段 4）——设计批准后实施跟随时必需
- **subagent-driven-development**——在执行任何任务之前必需
- **executing-plans**——在执行任何任务之前必需

**配合：**
- **finishing-a-development-branch**——完成后清理
