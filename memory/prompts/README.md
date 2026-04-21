# Prompt 资产库

> 所有 Prompt 模板按版本管理，每次修改通过 Git 提交记录。

## 目录结构

```
memory/prompts/
├── README.md          # 本文件
├── prompt_v1.md       # Day2 产出，基础结构化模板
├── prompt_v2.md       # Day3 产出，Few-Shot + CoT
├── prompt_v3.md       # Day4 产出，自检环节
├── master_prompt.md   # 迭代成熟后合并的最终模板
└── generation_log.md  # 每次生成记录（选题/版本/修改量/评分）
```

## 版本规范

| 版本 | 状态 | 说明 |
|------|------|------|
| prompt_v1.md | 基础版 | Day2，基础结构化模板 |
| prompt_v2.md | 迭代版 | Day3，+ Few-Shot + CoT |
| prompt_v3.md | 自检版 | Day4，+ 自检环节 |
| master_prompt.md | 成熟版 | 多次迭代后合并 |

## 提交规范

每次修改 Prompt 后：
```bash
git add memory/prompts/prompt_vX.md
git commit -m "feat(prompt): description of changes"
```

## 生成记录格式

```markdown
## YYYY-MM-DD HH:mm

- **选题**：[标题]
- **Prompt 版本**：vX
- **模型**：MiniMax 2.7
- **质量评分**：X/10
- **修改量**：X%
- **主要问题**：[描述]
- **修改记录**：[如何修改]
```