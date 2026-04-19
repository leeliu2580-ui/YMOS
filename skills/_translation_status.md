# Skill 双语翻译状态 | Translation Status

## 项目信息
- **启动时间**：2026-04-19
- **目标**：将所有 YMOS skills 的 SKILL.md 翻译为英中双语格式
- **格式**：YAML frontmatter `name` 不变，`description` 双语并行；正文中文为主，英文术语保留原文

## 翻译格式规范
```
---
name: skill-name
description: |
  中文描述（触发场景在前）
  English description (trigger scenarios first)
---
正文：中文为主，英文术语保留原文
代码块：保持原样，仅加中文注释
```

## 状态总览

| Skill | 状态 | 说明 |
|-------|------|------|
| systematic-debugging | ✅ 完成 | 全文双语 |
| test-driven-development | ✅ 完成 | 全文双语 |
| verification-before-completion | ✅ 完成 | 全文双语 |
| writing-plans | ✅ 完成 | 全文双语 |
| finishing-a-development-branch | ✅ 完成 | 全文双语 |
| using-git-worktrees | ✅ 完成 | 全文双语 |
| requesting-code-review | ✅ 完成 | 全文双语 |
| receiving-code-review | ✅ 完成 | 全文双语 |
| subagent-driven-development | ✅ 完成 | 全文双语 |
| using-superpowers | ✅ 完成 | 全文双语 |
| executing-plans | ✅ 完成 | 全文双语 |
| dispatching-parallel-agents | ✅ 完成 | 仅 frontmatter 更新 |
| brainstorming | ✅ 完成 | 仅 frontmatter 更新 |
| writing-skills | ✅ 完成 | 仅 frontmatter 更新 |
| wan-image-video-generation-editting | ✅ 完成 | 仅 frontmatter 更新 |
| exa-search | ✅ 完成 | 仅 frontmatter 更新 |
| grok-search | ✅ 完成 | 仅 frontmatter 更新 |
| summarize | ✅ 完成 | 仅 frontmatter 更新（正文已是中文） |
| finnhub | ✅ 完成 | 新增 frontmatter（正文英文，保留） |
| cmc-official | ✅ 完成 | 新建顶层 SKILL.md + frontmatter |
| web-access | ✅ 完成 | 重建（正文已是中文） |
| openai-image-gen | ✅ 完成 | OpenClaw 全局 skill，仅 frontmatter 更新 |
| openai-whisper | ✅ 完成 | OpenClaw 全局 skill，仅 frontmatter 更新 |
| video-frames | ✅ 完成 | OpenClaw 全局 skill，仅 frontmatter 更新 |
| skill-creator | ✅ 完成 | OpenClaw 全局 skill，仅 frontmatter 更新 |

## 外部 Skill（不在本工作区）

| Skill | 状态 | 说明 |
|-------|------|------|
| feishu-doc | ⏸️ 跳过 | 外部路径 B:\~BUN\root\__extensions__\feishu\skills |
| feishu-drive | ⏸️ 跳过 | 外部路径 |
| feishu-perm | ⏸️ 跳过 | 外部路径 |
| feishu-wiki | ⏸️ 跳过 | 外部路径 |
| clawhub | ⏸️ 跳过 | 外部路径 B:\~BUN\root\__skills__ |
| coding-agent | ⏸️ 跳过 | 外部路径 |
| healthcheck | ⏸️ 跳过 | 外部路径 |
| nano-banana-pro | ⏸️ 跳过 | 外部路径 |
| weather | ⏸️ 跳过 | 外部路径 |

## 已完成时间
- **主批次完成**：2026-04-19 13:08 CST
