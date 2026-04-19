# Skill 双语翻译工程 - 参考模板与任务分配

> 用于指导 4 个并行 subagent 同步翻译所有 skill

---

## 📐 翻译模板：SKILL.md 双语结构

每个 skill 的 `SKILL.md` 遵循以下结构：

```markdown
---
name: {skill-name}           # 不变
description: |
  {中文描述，2-4句话，包含触发关键词和功能说明}
  触发方式：{中文触发词}
  {English description, 2-4 sentences}
  Trigger: {English trigger keywords}
---

# {中文名称}

{中文概述，2-3句话，说明这个 skill 是什么、核心原则是什么}

## 触发关键词 | Trigger Keywords
- 中文：["关键词1", "关键词2", ...]
- English: ["keyword1", "keyword2", ...]

## 何时使用 | When to Use
{什么时候应该调用这个 skill}
{When to invoke this skill}

## 核心原则 | Core Principles
{核心原则列表}

## 工作流程 | Workflow
### Phase X：{阶段名称}
{步骤列表}

## 常见错误 | Common Mistakes
| 错误 | 正确做法 |
|------|----------|
| {错误描述} | {正确做法} |

## 注意事项 | Notes
{补充说明}

## 整合关系 | Integration
{这个 skill 和哪些其他 skill 配合使用}
```

---

## 📂 目录映射

| 原路径 | 目标路径 | 批次 |
|--------|----------|------|
| `D:\0_workspace\openclaw\.agents\skills\systematic-debugging` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\systematic-debugging` | 批次1 |
| `D:\0_workspace\openclaw\.agents\skills\test-driven-development` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\test-driven-development` | 批次1 |
| `D:\0_workspace\openclaw\.agents\skills\verification-before-completion` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\verification-before-completion` | 批次1 |
| `D:\0_workspace\openclaw\.agents\skills\writing-plans` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\writing-plans` | 批次1 |
| `D:\0_workspace\openclaw\.agents\skills\finishing-a-development-branch` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\finishing-a-development-branch` | 批次1 |
| `D:\0_workspace\openclaw\.agents\skills\using-git-worktrees` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\using-git-worktrees` | 批次1 |
| `D:\0_workspace\openclaw\.agents\skills\requesting-code-review` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\requesting-code-review` | 批次1 |
| `D:\0_workspace\openclaw\.agents\skills\receiving-code-review` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\receiving-code-review` | 批次1 |
| `D:\0_workspace\openclaw\.agents\skills\executing-plans` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\executing-plans` | 批次4 |
| `D:\0_workspace\openclaw\.agents\skills\subagent-driven-development` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\subagent-driven-development` | 批次4 |
| `D:\0_workspace\openclaw\.agents\skills\skill-creator` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\skill-creator` | 批次4 |
| `D:\0_workspace\openclaw\.agents\skills\using-superpowers` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\using-superpowers` | 批次4 |
| `D:\0_workspace\openclaw\.agents\skills\summarize` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\summarize` | 批次2 |
| `D:\0_workspace\openclaw\.agents\skills\web-access` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\web-access` | 批次2 |
| `D:\0_workspace\openclaw\.agents\skills\tushare-data` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\tushare-data` | 批次2 |
| `D:\0_workspace\openclaw\.agents\skills\openai-image-gen` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\openai-image-gen` | 批次3 |
| `D:\0_workspace\openclaw\.agents\skills\openai-whisper` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\openai-whisper` | 批次3 |
| `D:\0_workspace\openclaw\.agents\skills\video-frames` | `D:\0_workspace\trae_2601\ymos\YMOS\skills\video-frames` | 批次3 |
| `D:\0_workspace\trae_2601\ymos\YMOS\skills\brainstorming` | 原地翻译（已是双语） | 批次3 |
| `D:\0_workspace\trae_2601\ymos\YMOS\skills\dispatching-parallel-agents` | 原地翻译 | 批次4 |
| `D:\0_workspace\trae_2601\ymos\YMOS\skills\exa-search` | 原地翻译 | 批次2 |
| `D:\0_workspace\trae_2601\ymos\YMOS\skills\grok-search` | 原地翻译 | 批次2 |
| `D:\0_workspace\trae_2601\ymos\YMOS\skills\finnhub` | 原地翻译 | 批次2 |
| `D:\0_workspace\trae_2601\ymos\YMOS\skills\cmc-official` | 原地翻译 | 批次2 |
| `D:\0_workspace\trae_2601\ymos\YMOS\skills\memory-lancedb-pro` | 原地翻译 | 批次2 |
| `D:\0_workspace\trae_2601\ymos\YMOS\skills\wan-image-video-generation-editting` | 原地翻译 | 批次3 |

---

## 🎯 翻译原则

1. **YAML frontmatter**：`name` 不变，`description` 字段改为双语句子（中文在前，英文在后，用空行分隔）
2. **触发关键词**：必须包含中文和英文两组触发词
3. **正文结构**：中文为主，英文为辅；代码/API 块保持原样，仅添加中文注释
4. **参考格式**：参考 `D:\0_workspace\trae_2601\ft_media\dbskill\skills\dbs\SKILL.md` 的双语格式
5. **原文精华保留**：英文关键术语（如 TDD、Red-Green-Refactor 等）保留原文，在中文后加括号说明
6. **输出位置**：直接写入目标路径（替换原 SKILL.md）
7. **每个 skill 完成后**：追加一行 `✅ {skill-name}` 到 `D:\0_workspace\trae_2601\ymos\YMOS\skills\_translation_status.md`

---

## 📋 任务分配

### 批次1（Agent-1）：开发流程类（8个）
- systematic-debugging / 系统调试
- test-driven-development / TDD测试驱动
- verification-before-completion / 完成后验证
- writing-plans / 编写计划
- finishing-a-development-branch / 完成开发分支
- using-git-worktrees / Git隔离工作空间
- requesting-code-review / 请求代码审查
- receiving-code-review / 接收代码审查

### 批次2（Agent-2）：数据研究类（9个）
- summarize / 摘要
- web-access / 网页访问
- tushare-data / A股数据
- exa-search / Exa搜索
- grok-search / Grok搜索
- finnhub / Finnhub美股
- cmc-official / CMC加密货币
- memory-lancedb-pro / 长期记忆

### 批次3（Agent-3）：内容创意类（5个）
- brainstorming / 头脑风暴
- openai-image-gen / 图片生成
- wan-image-video-generation-editting / 万图生成
- openai-whisper / 语音转写
- video-frames / 视频抽帧

### 批次4（Agent-4）：编排工作流类（5个）
- executing-plans / 执行计划
- subagent-driven-development / 子代理驱动开发
- using-superpowers / 使用超能力
- dispatching-parallel-agents / 并行代理分发
- skill-creator / 技能创建
