# Skills 在当前工作流里的推荐使用顺序图

本文档回答一个更实用的问题：
**不是“有哪些 skill”，而是“在你当前这套工作流里，通常先用哪个、后用哪个”。**

适用范围：
- 方案设计
- MVP 开发
- bug 排查
- 投研数据分析
- skill 管理
- 开发收尾与验证

---

## 1. 总体原则

### 一条核心线
先判断任务类型，再决定 skill 顺序；不要为了“用了 skill”而用 skill。

### 典型顺序
1. **先澄清 / 发散** → `brainstorming`
2. **再写计划** → `writing-plans`
3. **再执行实现** → `subagent-driven-development` / `executing-plans`
4. **中途出问题就切换** → `systematic-debugging`
5. **完成前必须验证** → `verification-before-completion`
6. **需要质量兜底时** → `requesting-code-review`
7. **收尾分支时** → `finishing-a-development-branch`

---

## 2. 方案设计类任务

### 场景
- 做系统架构方案
- 做总方案文档
- 拆 MVP
- 讨论模块边界

### 推荐顺序
```text
brainstorming
  ↓
writing-plans
```

### 解释
- `brainstorming`：先把目标、边界、约束、路径想清楚
- `writing-plans`：再把实施步骤、模块、文件、任务拆细

### 典型例子
- 设计“财经自媒体 + 投研自动化系统”
- 写“自媒体选题列表 MVP 实施计划”

---

## 3. 开发实现类任务

### 场景
- 开始做 MVP
- 新增功能
- 重构模块
- 多文件开发

### 推荐顺序（标准开发流）
```text
brainstorming
  ↓
writing-plans
  ↓
test-driven-development
  ↓
subagent-driven-development 或 executing-plans
  ↓
verification-before-completion
  ↓
requesting-code-review
  ↓
finishing-a-development-branch
```

### 解释
- `brainstorming`：确认需求不是拍脑袋
- `writing-plans`：把实现拆开，避免边做边散
- `test-driven-development`：先立测试标准
- `subagent-driven-development`：大任务分给子代理推进
- `executing-plans`：如果不拆子代理，也可在当前会话按计划执行
- `verification-before-completion`：完成前跑测试、看输出，不能嘴上说好了
- `requesting-code-review`：让另一个视角做质量检查
- `finishing-a-development-branch`：最后决定怎么收口

---

## 4. Bug / 异常排查类任务

### 场景
- 测试挂了
- 结果不对
- 流程异常
- 数据不一致

### 推荐顺序
```text
systematic-debugging
  ↓
（必要时）test-driven-development
  ↓
verification-before-completion
```

### 解释
- `systematic-debugging`：先定位，不要直接盲修
- `test-driven-development`：补上复现测试，防止修了又回归
- `verification-before-completion`：修完必须验证

---

## 5. 投研 / 数据研究类任务

### 场景
- A 股数据分析
- 板块/个股筛选
- 财务趋势查看
- 资金流 / 公告 / 指数研究

### 推荐顺序
```text
tushare-data
  ↓
（如果要形成系统方案）brainstorming
  ↓
writing-plans
```

### 解释
- `tushare-data`：最适合中文投研数据请求直接转流程
- 如果只是问“看一下某只股票”，一般不用拉太多工程化 skill
- 如果要做成长期系统，再回到 `brainstorming + writing-plans`

---

## 6. Skill 本身管理类任务

### 场景
- 安装 skill
- 改 skill
- 审计 skill
- 发布 skill
- 检查 skill 目录

### 推荐顺序
```text
clawhub（找 / 装 / 更新）
  ↓
skill-creator 或 writing-skills（写 / 改 / 审计）
```

### 解释
- `clawhub`：偏“市场与分发”
- `skill-creator` / `writing-skills`：偏“内容与结构本身”

### 当前已安装/已拉取的外部仓库（2026-03-30）
- `D:\0_workspace\openclaw\.agents\skills\pua`
- `D:\0_workspace\openclaw\.agents\skills\web-access`
- `D:\0_workspace\openclaw\.agents\skills\anthropic-skills`

---

## 7. 并行任务类

### 场景
- 两个以上子任务互不依赖
- 想加速
- 各自边界清楚

### 推荐顺序
```text
dispatching-parallel-agents
  ↓
subagent-driven-development
```

### 解释
- 先判断能不能并行
- 再分发给不同子代理执行

---

## 8. 开发隔离环境类

### 场景
- 要开新功能
- 要避免污染当前工作区
- 计划较大，适合隔离环境

### 推荐顺序
```text
using-git-worktrees
  ↓
brainstorming
  ↓
writing-plans
  ↓
subagent-driven-development
```

### 解释
大任务先隔离工作树，再设计，再实现，最稳。

---

## 9. 当前最适合你的默认顺序

结合你现在这套工作流，我建议把默认顺序理解成：

```text
有新需求
  ↓
brainstorming
  ↓
writing-plans
  ↓
subagent-driven-development
  ↓
（出问题时切到）systematic-debugging
  ↓
verification-before-completion
  ↓
requesting-code-review
  ↓
finishing-a-development-branch
```

如果是投研数据问题，则改成：

```text
tushare-data
  ↓
（需要工程化时）brainstorming
  ↓
writing-plans
```

如果是改 skill 或装 skill，则改成：

```text
clawhub
  ↓
skill-creator / writing-skills
```

---

## 10. 一句话版速查

- **先想清楚**：`brainstorming`
- **先拆计划**：`writing-plans`
- **开始大任务实现**：`subagent-driven-development`
- **按计划在当前会话执行**：`executing-plans`
- **先写测试**：`test-driven-development`
- **查 bug**：`systematic-debugging`
- **完成前验收**：`verification-before-completion`
- **请求代码审查**：`requesting-code-review`
- **收尾分支**：`finishing-a-development-branch`
- **做中文投研数据研究**：`tushare-data`
- **装 / 管 skill**：`clawhub`
- **写 / 改 skill**：`skill-creator` / `writing-skills`

---

## 11. 结论

对你当前这套系统建设节奏来说，最重要的不是“多用 skill”，而是：

**在合适的时机，用合适的顺序调用 skill。**

真正高频的主链通常就是：

`brainstorming → writing-plans → subagent-driven-development → verification-before-completion`

这条主链，基本可以覆盖你现在大部分系统设计和开发场景。
