---
name: finishing-a-development-branch
description: |
  完成开发分支技能。开发完成、测试通过后，决定如何整合工作——Merge、PR 或清理。
  触发方式：完成、开发完、合并、创建PR、收尾
  Finish development branch skill. After implementation is complete and tests pass, decide how to integrate work.
  Trigger: finish, complete, merge, PR, development branch
---

# Finishing a Development Branch：完成开发分支

## 概述

通过提供明确选项和处理选择的工作流来指导完成开发工作。

**核心原则：** 验证测试 → 提供选项 → 执行选择 → 清理。

**开始时宣布：** "I'm using the finishing-a-development-branch skill to complete this work."

## 工作流程 | Workflow

### 步骤 1：验证测试

**在提供选项之前，验证测试通过：**

```bash
# 运行项目测试套件
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：**
```
Tests failing (<N> failures). Must fix before completing:

[显示失败]

Cannot proceed with merge/PR until tests pass.
```

停。不要进入步骤 2。

**如果测试通过：** 继续步骤 2。

### 步骤 2：确定基础分支

```bash
# 尝试常见基础分支
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

或询问："This branch split from main - is that correct?"

### 步骤 3：提供选项

提供恰好这 4 个选项：

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**不要添加解释**——保持选项简洁。

### 步骤 4：执行选择

#### 选项 1：本地 Merge

```bash
# 切换到基础分支
git checkout <base-branch>

# 拉取最新
git pull

# Merge 功能分支
git merge <feature-branch>

# 在合并结果上验证测试
<test command>

# 如果测试通过
git branch -d <feature-branch>
```

然后：清理 worktree（步骤 5）

#### 选项 2：Push 并创建 PR

```bash
# Push 分支
git push -u origin <feature-branch>

# 创建 PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

然后：清理 worktree（步骤 5）

#### 选项 3：保持原样

报告："Keeping branch <name>. Worktree preserved at <path>."

**不要清理 worktree。**

#### 选项 4：丢弃

**首先确认：**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

等待确切确认。

如果确认：
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

然后：清理 worktree（步骤 5）

### 步骤 5：清理 Worktree

**对于选项 1、2、4：**

检查是否在 worktree 中：
```bash
git worktree list | grep $(git branch --show-current)
```

如果是：
```bash
git worktree remove <worktree-path>
```

**对于选项 3：** 保持 worktree。

## 快速参考 | Quick Reference

| 选项 | Merge | Push | 保持 Worktree | 清理分支 |
|------|-------|------|--------------|----------|
| 1. 本地 merge | ✓ | - | - | ✓ |
| 2. 创建 PR | - | ✓ | ✓ | - |
| 3. 保持原样 | - | - | ✓ | - |
| 4. 丢弃 | - | - | - | ✓（force）|

## 整合关系 | Integration

**被调用于：**
- **subagent-driven-development**（步骤 7）——所有任务完成后
- **executing-plans**（步骤 5）——所有批次完成后

**配合：**
- **using-git-worktrees**——清理该 skill 创建的 worktree
