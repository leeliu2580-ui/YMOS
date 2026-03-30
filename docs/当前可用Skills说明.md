# 当前可用 Skills 说明

本文档整理当前会话环境中可用的 skills，以及各自适用场景。目的不是复述底层实现细节，而是帮助快速判断：**什么时候该用哪个 skill。**

---

## 1. clawhub
**作用：**
用 ClawHub CLI 搜索、安装、更新、发布 skills。

**适用场景：**
- 需要临时从 clawhub.com 拉新 skill
- 想把本地 skill 升级到最新版
- 想发布新的 skill 或更新已有 skill

**一句话理解：**
这是 **skill 市场/仓库管理器**。

---

## 2. coding-agent
**作用：**
把复杂编程任务委托给 Codex、Claude Code、Pi 等编码代理执行。

**适用场景：**
- 新功能开发
- 大范围重构
- PR review
- 需要大量文件探索与迭代实现的编码任务

**不适合：**
- 很小的一行改动
- 只是读代码
- 当前聊天里直接 thread-bound 的 ACP harness 请求

**一句话理解：**
这是 **重型编程外包 skill**。

---

## 3. healthcheck
**作用：**
用于 OpenClaw 所在机器的安全检查、暴露面审查、加固与风险配置建议。

**适用场景：**
- 做安全审计
- 检查 SSH / 防火墙 / 更新策略
- 看 OpenClaw 部署机器的风险暴露
- 配置定期安全检查 cron

**一句话理解：**
这是 **主机安全与运维体检 skill**。

---

## 4. skill-creator
**作用：**
创建、改进、审计、清理 AgentSkills。

**适用场景：**
- 从零创建 skill
- 改进现有 skill
- 审核 SKILL.md 是否规范
- 调整 skill 目录结构

**一句话理解：**
这是 **Skill 本身的作者/审计员**。

---

## 5. weather
**作用：**
查询天气与天气预报。

**适用场景：**
- 用户问某地天气
- 需要未来几天温度/降雨趋势

**不适合：**
- 历史天气
- 极端气象深度分析
- 专业灾害预警体系

**一句话理解：**
这是 **轻量天气查询 skill**。

---

## 6. brainstorming
**作用：**
在任何创造性工作、功能设计、行为修改之前，先做需求探索、意图澄清和方案发散。

**适用场景：**
- 设计新功能
- 建新组件
- 增加系统能力
- 在动手实现前先梳理目标与边界

**一句话理解：**
这是 **先想清楚再动手的前置 skill**。

---

## 7. dispatching-parallel-agents
**作用：**
当存在 2 个及以上相互独立的任务时，并行分发给多个代理处理。

**适用场景：**
- 多个子任务互不依赖
- 希望并行提速
- 需要明确切分职责

**一句话理解：**
这是 **并行调度多个代理的 skill**。

---

## 8. executing-plans
**作用：**
执行已经写好的实施计划，并在关键检查点进行 review。

**适用场景：**
- 已经有明确实现计划
- 想按步骤推进落地
- 需要在当前会话中分阶段执行计划

**一句话理解：**
这是 **计划执行器**。

---

## 9. finishing-a-development-branch
**作用：**
当开发工作完成、测试通过后，帮助决定如何结束分支：合并、提 PR、清理等。

**适用场景：**
- 功能做完了
- 准备收尾
- 需要决定 merge / PR / cleanup 路径

**一句话理解：**
这是 **开发分支收口 skill**。

---

## 10. receiving-code-review
**作用：**
在收到 code review 意见后，先进行技术核验，再决定是否采纳。

**适用场景：**
- 收到审查意见
- 建议可能不清楚或不一定合理
- 需要防止机械照改

**一句话理解：**
这是 **代码审查意见的鉴别器**。

---

## 11. requesting-code-review
**作用：**
在任务完成后，主动发起代码审查，验证实现是否满足要求。

**适用场景：**
- 功能做完了
- 大改动准备合并前
- 想让另一个代理做 review

**一句话理解：**
这是 **发起代码审查的 skill**。

---

## 12. subagent-driven-development
**作用：**
在当前会话里按计划把实现任务拆给多个子代理逐步完成。

**适用场景：**
- 已有实施计划
- 希望逐任务分派子代理
- 任务较大，且需要 review → 执行 → 再 review 的节奏

**一句话理解：**
这是 **子代理驱动开发 skill**。

---

## 13. systematic-debugging
**作用：**
在遇到 bug、测试失败、异常行为时，先系统化定位问题，再修复。

**适用场景：**
- 出现 bug
- 测试挂了
- 行为与预期不一致

**一句话理解：**
这是 **标准化排障 skill**。

---

## 14. test-driven-development
**作用：**
实现 feature 或 bugfix 前，先写测试，再写实现。

**适用场景：**
- 新功能开发
- 缺陷修复
- 需要更稳定的实现闭环

**一句话理解：**
这是 **TDD 开发 skill**。

---

## 15. tushare-data
**作用：**
把中文自然语言投研需求转成 Tushare 数据获取、清洗、筛选、导出和简析流程。

**适用场景：**
- A 股/指数/ETF/财报/资金流/板块研究
- “看看这只股票最近怎么样”
- “帮我查财报趋势”
- “最近哪个板块最强”

**一句话理解：**
这是 **中文投研数据分析 skill**。

---

## 16. using-git-worktrees
**作用：**
在开始功能开发前，创建独立 git worktree，避免污染当前工作区。

**适用场景：**
- 新功能开发
- 大改动前需要隔离环境
- 多任务并行开发时避免冲突

**一句话理解：**
这是 **开发隔离环境 skill**。

---

## 17. using-superpowers
**作用：**
作为对话入口约束，提醒先识别并使用合适的 skill。

**适用场景：**
- 新对话开始时
- 需要先判断有没有合适 skill 可用

**一句话理解：**
这是 **skill 路由总开关**。

---

## 18. verification-before-completion
**作用：**
在声称“完成了 / 修好了 / 通过了”之前，强制先跑验证命令并检查输出。

**适用场景：**
- 准备宣布任务完成
- 准备提交代码
- 准备提 PR

**一句话理解：**
这是 **先验证再宣告完成的 skill**。

---

## 19. writing-plans
**作用：**
在有明确需求但还没动手前，先写详细实施计划。

**适用场景：**
- 多步骤任务
- 功能实现前先拆计划
- 需要把模块、文件、步骤、测试都写清楚

**一句话理解：**
这是 **实施计划编写 skill**。

---

## 20. writing-skills
**作用：**
创建、编辑、验证 skill，并确保 skill 可正常工作后再部署。

**适用场景：**
- 写新 skill
- 改 skill
- 验证某个 skill 是否可用

**一句话理解：**
这是 **Skill 编写与验证 skill**。

---

# 怎么快速选 skill

## A. 如果是编程任务
优先看：
- `brainstorming`
- `writing-plans`
- `test-driven-development`
- `subagent-driven-development`
- `verification-before-completion`
- `requesting-code-review`

## B. 如果是排查问题
优先看：
- `systematic-debugging`
- `verification-before-completion`

## C. 如果是 skill 本身相关
优先看：
- `skill-creator`
- `writing-skills`
- `clawhub`

## D. 如果是投研 / A 股数据
优先看：
- `tushare-data`

## E. 如果是方案设计 / 前期拆解
优先看：
- `brainstorming`
- `writing-plans`

---

# 当前最常用的一组（按实用度）

对现在这个工作区来说，最常用的通常是：

1. `brainstorming`
2. `writing-plans`
3. `subagent-driven-development`
4. `test-driven-development`
5. `verification-before-completion`
6. `systematic-debugging`
7. `tushare-data`

---

# 一句话总览

- **写方案**：`writing-plans`
- **开工实现**：`subagent-driven-development` / `executing-plans`
- **先想清楚需求**：`brainstorming`
- **先写测试**：`test-driven-development`
- **查 bug**：`systematic-debugging`
- **完成前验证**：`verification-before-completion`
- **做投研数据分析**：`tushare-data`
- **写/改 skill**：`skill-creator` / `writing-skills`

如果你要，我下一步可以继续给你补一版：
**“这些 skills 在你当前工作流里的推荐使用顺序图”**。
