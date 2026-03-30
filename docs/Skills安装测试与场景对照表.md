# Skills 安装、测试与使用场景对照表

更新时间：2026-03-31

本文档回答三件事：
1. 这批点名 skill 是否已经安装到统一目录
2. 当前测试状态如何
3. 在你的实际需求里，什么情况下该用哪个 skill

统一 skills 目录：
`D:\0_workspace\openclaw\.agents\skills`

---

## 一、总览

| Skill | 安装状态 | 测试状态 | 建议级别 | 说明 |
|:---|:---|:---|:---|:---|
| web-access | 已安装 | 已验证核心链路 | 高 | 复杂联网 / 动态网页 / 登录态首选增强层 |
| tushare-data | 已安装 | 已完成落位验证 | 高 | A 股 / 指数 / 财报 / 资金流等中文投研数据任务 |
| skill-creator | 已安装 | 已完成落位验证 | 高 | 创建、改造、整理你自己的 skill |
| subagent-driven-development | 已安装 | 已完成落位验证 | 高 | 有实施计划后，按任务拆给子代理执行 |
| test-driven-development | 已安装 | 已完成落位验证 | 高 | 做功能 / 修 bug 前，先写测试 |
| systematic-debugging | 已安装 | 已完成落位验证 | 高 | 遇到 bug / 测试失败 / 异常时先系统排查 |
| verification-before-completion | 已安装 | 已完成落位验证 | 高 | 在宣称完成前先跑验证 |
| executing-plans | 已安装 | 已完成落位验证 | 中高 | 已有计划时，在当前会话按步骤执行 |
| summarize | 未安装 | 无标准来源确认 | 中 | 建议先不要装假货，后续明确来源或自建 |
| openai-whisper | 未安装 | 无标准来源确认 | 中 | 建议优先通过工具/脚本实现，后续再封装成 skill |
| openai-image-gen | 未安装 | 无标准来源确认 | 中 | 建议优先通过 API 工具链实现，后续再封装成 skill |
| video-frames | 未安装 | 无标准来源确认 | 中 | 建议先作为脚本/流程能力，后续再技能化 |
| coding-agent | 未安装到统一目录 | 当前会话可用，但源目录当前不可直接读取 | 高 | 编码重活外包给 Codex / Claude Code / Pi |

---

## 二、已安装并验证的 skills

## 1. web-access
### 安装位置
`D:\0_workspace\openclaw\.agents\skills\web-access`

### 测试结果
已完成核心链路验证：
- `check-deps.mjs`：通过
- Chrome 调试端口：`9222`
- proxy：`ready`
- 成功执行：`new -> targets -> info -> eval -> close`
- 已成功读取微信公众号正文

### 在你的需求中什么时候用
#### 用于：
- 复杂联网抓取
- 动态页面内容读取
- 登录态页面访问
- 公众号 / 小红书 / B站 / 飞书等非纯静态网页
- 热点素材抓取

#### 不优先用于：
- 纯 RSS
- 公开静态页面且结构稳定的正文抓取
- 可直接 `httpx + feedparser` 完成的轻量任务

### 一句话作用
**复杂网页与真实浏览器访问的统一增强层。**

---

## 2. tushare-data
### 安装位置
`D:\0_workspace\openclaw\.agents\skills\tushare-data`

### 测试结果
- 已完成 skill 落位验证
- `SKILL.md` 已就绪
- 本轮未做真实 A 股查询回归，但当前工作区本身长期面向投研场景，适配度高

### 在你的需求中什么时候用
#### 用于：
- 查看 A 股个股最近怎么样
- 财报趋势、估值、北向资金、板块强弱
- 导出行情/财务/资金流数据
- 把中文自然语言投研需求转成 Tushare 数据流程

#### 不优先用于：
- 泛网页抓取
- 海外股票深度网页研究
- 自媒体内容生产

### 一句话作用
**中文 A 股投研数据请求的专用技能。**

---

## 3. skill-creator
### 安装位置
`D:\0_workspace\openclaw\.agents\skills\skill-creator`

### 测试结果
- 已完成 skill 落位验证
- 来源：`anthropic-skills/skills/skill-creator`

### 在你的需求中什么时候用
#### 用于：
- 你想把自己的流程沉淀成 skill
- 想整理、审计、清理已有 skill
- 想把服务器管理、内容 SOP、投研分析流程封装成个人 skill

#### 不优先用于：
- 单次普通业务执行
- 不是在处理 skill 本身的时候

### 一句话作用
**把经验和 SOP 变成你自己的 skill。**

---

## 4. subagent-driven-development
### 安装位置
`D:\0_workspace\openclaw\.agents\skills\subagent-driven-development`

### 测试结果
- 已完成落位验证
- 当前工作流非常适配

### 在你的需求中什么时候用
#### 用于：
- 已经写好了实施计划
- 要执行中大型开发任务
- 想一任务一子代理推进，并在任务间 review

#### 最适合你的场景
- 自媒体 MVP 开发
- 自动化系统模块开发
- 多文件、多步骤任务推进

### 一句话作用
**有计划后，用子代理分任务推进实现。**

---

## 5. test-driven-development
### 安装位置
`D:\0_workspace\openclaw\.agents\skills\test-driven-development`

### 测试结果
- 已完成落位验证

### 在你的需求中什么时候用
#### 用于：
- 开发任何 feature
- 修任何 bug
- 想让 MVP 更稳

#### 最适合你的场景
- FastAPI 服务开发
- 状态机 / 导出器 / 路由 / 规则引擎开发

### 一句话作用
**先写测试，再写实现。**

---

## 6. systematic-debugging
### 安装位置
`D:\0_workspace\openclaw\.agents\skills\systematic-debugging`

### 测试结果
- 已完成落位验证

### 在你的需求中什么时候用
#### 用于：
- API 返回异常
- n8n 工作流失败
- skill 集成不通
- 数据抓取不一致
- 测试失败

### 一句话作用
**先定位、再修复，避免盲改。**

---

## 7. verification-before-completion
### 安装位置
`D:\0_workspace\openclaw\.agents\skills\verification-before-completion`

### 测试结果
- 已完成落位验证

### 在你的需求中什么时候用
#### 用于：
- 宣称“完成了”之前
- 提交代码前
- 说“抓取成功了 / 可用了 / 跑通了”之前

### 一句话作用
**不验证，不算完成。**

---

## 8. executing-plans
### 安装位置
`D:\0_workspace\openclaw\.agents\skills\executing-plans`

### 测试结果
- 已完成落位验证

### 在你的需求中什么时候用
#### 用于：
- 已有计划，但你不想拆成多个子代理
- 想在当前会话按计划逐步执行

### 一句话作用
**在当前会话里按计划执行。**

---

## 三、未安装 / 待补来源的 skills

## 9. summarize
### 当前状态
- 未发现明确标准来源
- 当前不建议为了“凑清单”装不明来源 skill

### 建议
如果你确实想要这个 skill，建议后续两种路径二选一：
1. 明确标准仓库来源后再安装
2. 直接自建一个总结 skill，适配你的工作流

### 在你的需求中适合做什么
- 长文摘要
- 周报压缩
- 会议纪要提炼
- 投研报告 TL;DR

---

## 10. openai-whisper
### 当前状态
- 未发现明确标准 skill 来源

### 建议
更合理的方式是：
- 先把 Whisper 作为工具链/脚本能力接入
- 等流程稳定后，再封装成 skill

### 在你的需求中适合做什么
- 视频转写
- 音频转写
- 自媒体素材拆解前的文本化

---

## 11. openai-image-gen
### 当前状态
- 未发现明确标准 skill 来源

### 建议
更合理的方式是：
- 先把图像生成作为 API 能力接入
- 再根据你的配图流程沉淀成 skill

### 在你的需求中适合做什么
- 自媒体封面图
- 文章配图
- 数据摘要海报图

---

## 12. video-frames
### 当前状态
- 未发现明确标准 skill 来源

### 建议
更合理的方式是：
- 先用脚本或浏览器/CDP 做视频抽帧
- 后续若高频使用，再封装 skill

### 在你的需求中适合做什么
- 视频内容拆解
- 按时间点抽帧
- 对短视频做画面层分析

---

## 13. coding-agent
### 当前状态
- 当前会话能力里可用
- 但原始 skill 文件所在路径当前不可直接读取并复制到统一目录
- 所以现在不能算“已安装到统一目录”

### 在你的需求中什么时候用
#### 用于：
- 中大型编码任务
- 多文件开发
- 新功能 / 新模块
- 重构与 PR review

### 一句话作用
**把重型编码任务外包给专门编码代理。**

---

## 四、结合你的实际需求，推荐使用顺序

## 需求 1：做系统方案 / 架构 / 文档
推荐：
1. `skill-creator`（如果目标是沉淀成 skill）
2. `subagent-driven-development`（如果后续要执行）
3. `executing-plans`

## 需求 2：开发自媒体 MVP / 自动化系统
推荐：
1. `test-driven-development`
2. `subagent-driven-development`
3. `systematic-debugging`
4. `verification-before-completion`
5. `coding-agent`（重型开发时）

## 需求 3：抓取网页 / 热点 / 公众号 / 动态页面
推荐：
1. `web-access`

## 需求 4：A 股 / 投研 / 财报 / 资金流
推荐：
1. `tushare-data`
2. `web-access`（需要网页补充信息时）

## 需求 5：未来要做转写 / 配图 / 视频拆解
当前建议：
- 先做工具链
- 后做技能化

也就是：
- `openai-whisper` → 先工具化
- `openai-image-gen` → 先工具化
- `video-frames` → 先工具化

---

## 五、最终结论

### 已经可以直接纳入你当前体系的
- `web-access`
- `tushare-data`
- `skill-creator`
- `subagent-driven-development`
- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `executing-plans`

### 还不建议硬装的
- `summarize`
- `openai-whisper`
- `openai-image-gen`
- `video-frames`

### 特殊项
- `coding-agent`：当前会话可用，但还没以统一目录方式落位

一句话总结：

**先把“确有来源、确有价值、已能验证”的 skill 纳入体系；对转写、配图、抽帧这类能力，先做工具链，再做技能化。**
