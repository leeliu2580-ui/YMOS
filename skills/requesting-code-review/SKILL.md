---
name: requesting-code-review
description: |
  请求代码审查技能。完成任务、实现重要功能或合并之前，请求审查以验证工作满足需求。
  触发方式：审查代码、review、请求审查、代码审查
  Request code review skill. Before merging, request review to verify work meets requirements.
  Trigger: code review, review request, request review, review
---

# Requesting Code Review：请求代码审查

## 概述

派遣 superpowers:code-reviewer 子代理来在级联之前发现问题。审查者获得精确构建的评估上下文——而不是你 session 的历史。这保持审查者专注于工作产出，而不是你的思维过程，并为你保持自己的上下文以持续工作。

**核心原则：** 尽早审查，经常审查。

## 何时请求审查 | When to Request Review

**强制：**
- subagent-driven development 中每个任务之后
- 完成重要功能之后
- Merge 到 main 之前

**可选但有价值：**
- 卡住时（新的视角）
- 重构之前（基线检查）
- 修复复杂 Bug 之后

## 如何请求 | How to Request

**1. 获取 git SHA：**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # 或 origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 派遣 code-reviewer 子代理：**

使用 Task 工具，类型为 superpowers:code-reviewer，填写 `code-reviewer.md` 中的模板。

**占位符：**
- `{WHAT_WAS_IMPLEMENTED}` - 刚刚构建的内容
- `{PLAN_OR_REQUIREMENTS}` - 它应该做什么
- `{BASE_SHA}` - 起始提交
- `{HEAD_SHA}` - 结束提交
- `{DESCRIPTION}` - 简要总结

**3. 处理反馈：**
- 立即修复 Critical 问题
- 继续之前修复 Important 问题
- 记录 Minor 问题稍后处理
- 如果审查者错了，用推理反驳

## 整合关系 | Integration

**Subagent-Driven Development：**
- 每个任务之后审查
- 在问题级联之前捕获
- 修复后再继续

**Executing Plans：**
- 每个批次（3 个任务）后审查
- 获取反馈，应用，继续

## 红牌警告 | Red Flags

**永远不要：**
- 因为"简单"跳过审查
- 忽略 Critical 问题
- 在未修复 Important 问题的情况下继续
- 对有效技术反馈争论

**如果审查者错了：**
- 用技术推理反驳
- 显示证明它 work 的代码/测试
- 请求澄清
