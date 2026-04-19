---
name: executing-plans
description: |
  执行计划技能。在独立 session 中执行书面实施计划，按检查点逐步完成任务。
  触发方式：执行计划、按计划执行、运行任务、执行任务列表
  Execute implementation plans skill. Execute written plans in an isolated session with checkpoints.
  Trigger: execute plan, follow the plan, run tasks, implementation
---

# Executing Plans：执行计划

## 概述

加载计划，批判性审查，执行所有任务，完成后报告。

**开始时宣布：** "I'm using the executing-plans skill to implement this plan."

**注意：** 告诉你的搭档，Superpowers 在有子代理支持时效果更好。如果有子代理可用，使用 superpowers:subagent-driven-development 而不是这个 skill。

## 工作流程 | The Process

### 步骤 1：加载和审查计划

1. 读取计划文件
2. 批判性审查——识别对计划的任何问题或担忧
3. 如果有担忧：在开始之前向搭档提出
4. 如果没有担忧：创建 TodoWrite 并继续

### 步骤 2：执行任务

每个任务：
1. 标记为进行中
2. 精确遵循每个步骤（计划有小的步骤）
3. 按指定运行验证
4. 标记为完成

### 步骤 3：完成开发

所有任务完成并验证后：
- 宣布："I'm using the finishing-a-development-branch skill to complete this work."
- **必需子技能：** 使用 superpowers:finishing-a-development-branch
- 遵循该 skill 验证测试、提供选项、执行选择

## 何时停止并寻求帮助 | When to Stop and Ask for Help

**立即停止执行当：**
- 遇到阻碍（缺失依赖、测试失败、指令不清）
- 计划有阻止开始的 critical 缺口
- 不理解指令
- 验证反复失败

**提问澄清而不是猜测。**

## 何时回到早期步骤 | When to Revisit Earlier Steps

**回到审查（步骤 1）当：**
- 搭档根据你的反馈更新了计划
- 基本方法需要重新思考

**不要强行通过阻碍**——停并提问。

## 记住 | Remember

- 首先批判性审查计划
- 精确遵循计划步骤
- 不要跳过验证
- 计划说引用 skills 时引用
- 遇到阻碍停下来，不猜测
- 未经搭档明确许可绝不在 main/master 分支上开始实施

## 整合关系 | Integration

**必需工作流 skills：**
- **superpowers:using-git-worktrees** - 必需：在开始之前设置隔离工作空间
- **superpowers:writing-plans** - 创建这个 skill 执行的计划
- **superpowers:finishing-a-development-branch** - 所有任务完成后完成开发
