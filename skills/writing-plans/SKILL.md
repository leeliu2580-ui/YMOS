---
name: writing-plans
description: |
  编写实施计划技能。当有规格或需求文档、需要分解为可执行步骤时使用。在接触代码之前先写计划。
  触发方式：写计划、制定计划、实施方案、任务分解
  Writing implementation plans skill. Break down specs into executable steps before touching code.
  Trigger: write plan, make plan, implementation plan, break down tasks
---

# Writing Plans：编写实施计划

## 概述

假设工程师对我们的代码库零上下文且品味可疑，写全面的实施计划。记录他们需要知道的一切：每个任务要修改哪些文件、代码、测试、需要检查的文档、如何测试。把整个计划写成小步骤任务。DRY。YAGNI。TDD。频繁提交。

**开始时宣布：** "I'm using the writing-plans skill to create the implementation plan."

**上下文：** 这应在专用 worktree 中运行（由 brainstorming skill 创建）。

**保存计划到：** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`

## 范围检查 | Scope Check

如果规格涵盖多个独立子系统，应该在 brainstorming 期间已分解为子规格规格。如果没有，建议分解为独立计划——每个子系统一个。每个计划应该独立产生可工作、可测试的软件。

## 文件结构 | File Structure

在定义任务之前，映射将创建或修改哪些文件以及每个文件的职责。这是锁定分解决策的地方。

**每个文件一个明确职责。** 文件改变时应该在一起。**按职责分离，不要按技术层。**

## 任务粒度 | Bite-Sized Task Granularity

**每个步骤是一个动作（2-5 分钟）：**
- "写失败的测试" - 步骤
- "运行它确保失败" - 步骤
- "写最小代码让测试通过" - 步骤
- "运行测试确保它们通过" - 步骤
- "提交" - 步骤

## 计划文档头部 | Plan Document Header

**每个计划必须以此头部开始：**

```markdown
# [功能名称] 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标：** [一句话描述构建内容]

**架构：** [2-3 句话关于方法]

**技术栈：** [关键技术和库]

---
```

## 任务结构 | Task Structure

```markdown
### 任务 N：[组件名称]

**文件：**
- 创建：`exact/path/to/file.py`
- 修改：`exact/path/to/existing.py:123-145`
- 测试：`tests/exact/path/to/test.py`

- [ ] **步骤 1：写失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **步骤 2：运行测试验证它失败**

运行：`pytest tests/path/test.py::test_name -v`
预期：FAIL，显示 "function not defined"

- [ ] **步骤 3：写最小实现**

```python
def function(input):
    return expected
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/path/test.py::test_name -v`
预期：PASS

- [ ] **步骤 5：提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## 无占位符 | No Placeholders

每个步骤必须包含工程师需要的实际内容。这些是**计划失败**——永远不要写：
- "TBD"、"TODO"、"稍后实现"、"填写细节"
- "添加适当的错误处理"/"添加验证"/"处理边界情况"
- "为上述写测试"（没有实际测试代码）
- "类似于任务 N"（重复代码——工程师可能乱序阅读任务）
- 描述做什么而不显示如何做的步骤（代码块是代码步骤所必需的）

## 自审 | Self-Review

写完完整计划后，用新眼光看规格并检查计划：

**1. 规格覆盖：** 浏览规格的每个部分/需求。能指向实现它的任务吗？列出任何缺口。

**2. 占位符扫描：** 在计划中搜索红旗——任何来自"无占位符"部分的内容。修复它们。

**3. 类型一致性：** 在后面的任务中使用的类型、方法签名和属性名与前面定义的一致吗？

## 执行交接 | Execution Handoff

保存计划后，提供执行选择：

**"计划已保存到 `docs/superpowers/plans/<filename>.md`。两种执行选项：**

**1. 子代理驱动（推荐）** - 我为每个任务派遣新鲜子代理，任务之间审查，快速迭代

**2. 内联执行** - 在此 session 中使用 executing-plans 执行，带检查点的批量执行

**哪种？"**

**如果选择子代理驱动：**
- **必需子技能：** 使用 superpowers:subagent-driven-development
- 每个任务新鲜子代理 + 两阶段审查

**如果选择内联执行：**
- **必需子技能：** 使用 superpowers:executing-plans
- 带检查点的批量执行
