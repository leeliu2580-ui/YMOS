---
name: subagent-driven-development
description: |
  子代理驱动开发技能。在当前 session 中执行含有独立任务实施计划时使用——每个任务派遣新鲜子代理，两阶段审查（规格合规→代码质量）。
  触发方式：子代理驱动、并行任务、独立任务、多个任务同时
  Subagent-driven development skill. Execute plans with independent tasks in current session via subagents.
  Trigger: subagent, parallel tasks, independent tasks, multiple tasks
---

# Subagent-Driven Development：子代理驱动开发

## 概述

通过为每个任务派遣新鲜子代理来执行计划，每个任务后进行两阶段审查：首先审查规格合规，然后审查代码质量。

**为什么用子代理：** 将任务委托给具有隔离上下文的专业化代理。通过精确构建它们的指令和上下文，确保它们保持专注并成功完成任务。它们不应继承你的 session 上下文或历史——你构建它们所需的精确内容。这也为你保留了协调工作的上下文。

**核心原则：** 每个任务新鲜子代理 + 两阶段审查（规格→质量）= 高质量、快速迭代

## 何时使用 | When to Use

```
有实施计划？
  ↓ 是
任务大部分独立？
  ↓ 是
保持在当前 session？
  ↓ 是
→ 使用 subagent-driven-development

任务耦合？
→ 使用 brainstorming 或手动执行

需要并行 session？
→ 使用 executing-plans
```

**vs. Executing Plans（并行 session）：**
- 同一 session（无上下文切换）
- 每个任务新鲜子代理（无上下文污染）
- 每个任务后两阶段审查：规格合规优先，然后代码质量
- 更快迭代（任务之间无人为循环）

## 工作流程 | The Process

```
每个任务：
  1. 派遣实施者子代理
  2. 实施者提问？→ 回答并提供上下文
  3. 实施者实施、测试、提交、自我审查
  4. 派遣规格合规审查者
  5. 规格合规？→ 否 → 修复
  6. 派遣代码质量审查者
  7. 代码质量批准？→ 否 → 修复
  8. 标记任务完成

所有任务完成后：
  → 派遣最终代码审查者（整个实现）
  → 使用 finishing-a-development-branch
```

## 模型选择 | Model Selection

使用能够处理每个角色的最弱模型以节省成本并提高速度。

| 任务类型 | 推荐模型 |
|---------|---------|
| 机械实现（清晰规格，1-2 文件）| 快速、便宜的模型 |
| 集成与判断（多文件协调、模式匹配）| 标准模型 |
| 架构、设计和审查 | 最强可用模型 |

## 处理实施者状态 | Handling Implementer Status

子代理报告四种状态之一。适当处理：

**DONE：** 进入规格合规审查。

**DONE_WITH_CONCERNS：** 实施者完成了工作但标记了疑虑。先阅读疑虑再继续。如果疑虑关于正确性或范围，在审查前处理。如果只是观察（如"这个文件变大了"），记录并继续审查。

**NEEDS_CONTEXT：** 实施者需要未提供的信息。提供缺失的上下文并重新派遣。

**BLOCKED：** 实施者无法完成任务。评估阻碍：
1. 如果是上下文问题，提供更多上下文，用相同模型重新派遣
2. 如果任务需要更多推理，用更有能力的模型重新派遣
3. 如果任务太大，分解成更小的块
4. 如果计划本身是错的，升级给人类

**永远不要**忽略升级或强制相同模型重试而不改变。

## 整合关系 | Integration

**必需工作流 skills：**
- **superpowers:using-git-worktrees** - 必需：在开始之前设置隔离工作空间
- **superpowers:writing-plans** - 创建这个 skill 执行的计划
- **superpowers:requesting-code-review** - 代码审查模板
- **superpowers:finishing-a-development-branch** - 所有任务完成后完成开发

**子代理应使用：**
- **superpowers:test-driven-development** - 子代理对每个任务遵循 TDD
