# Skills 全局清单

> 本文档由 AI 自动生成，记录所有可用 Skill 的路径、描述和用途。
> 生成时间：2026-04-21
> 数据来源：OpenClaw 安装目录 + YMOS 工作区

---

## 图例

| 标记 | 含义 | 说明 |
|------|------|------|
| ✅ 已启用 | 当前配置中激活 | 可直接使用 |
| 🔧 已安装 | 扩展包存在，已在你的 OpenClaw 目录中 | 需要配置才能启用 |
| 📦 可用 | 技能文件存在，属于 OpenClaw 内置 | 始终可用 |
| ❌ 未安装 | 扩展包在 npm 目录中但未复制到实际运行环境 | 需要额外安装 |

---

## 执行摘要——你当前真正能用的

根据 `C:\Users\guanhai\.openclaw\openclaw.json` 配置：

### ✅ 已启用

| 类型 | 项目 | 说明 |
|------|------|------|
| **模型** | MiniMax-M2.7 | 主要 AI 模型 |
| **频道** | 飞书 (feishu) | 消息接收和推送 |
| **插件** | tavily | 网页搜索 |
| **插件** | minimax | MiniMax 模型集成 |
| **工具·搜索** | tavily | Web 搜索 |

### 🔧 已安装（未启用，但文件存在）

| 类型 | 数量 | 示例 |
|------|------|------|
| 飞书扩展 | 4个 | feishu-doc, feishu-wiki, feishu-drive, feishu-perm |
| 扩展插件 | 90+个 | discord, slack, qqbot, tavily, memory-lancedb 等 |

---

## 一、OpenClaw 内置 Skills（始终可用）

路径：`C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\skills\<skill-name>\SKILL.md`

> 内置 Skills 属于 OpenClaw 核心包，文件始终存在，无需额外安装。

### 核心基础设施

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **clawhub** | ClawHub CLI，用于搜索/安装/发布 agent skills | 安装 skill、同步 skill、发布 skill |
| **skill-creator** | 创建、编辑、改进、审计 AgentSkills | 创建技能、改进技能、审计技能 |
| **taskflow** | 持久化任务流编排，支持多步骤后台任务 | 多步骤任务、后台任务、任务编排 |
| **taskflow-inbox-triage** | TaskFlow 收件箱分类示例 | 收件箱分类、消息分流 |
| **healthcheck** | 主机安全审计、防火墙/SSH/更新加固 | 安全审计、主机加固、风险评估 |
| **node-connect** | 诊断移动端配对连接失败问题 | 配对失败、QR码、节点连接 |

### 编码与开发

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **coding-agent** | 委托编码任务给 Codex/Claude Code/Pi agents | 构建功能、代码实现 |
| **github** | gh CLI 操作：issues、PRs、CI、代码审查 | PR状态、创建issue |
| **gh-issues** | 获取 GitHub issues 并派遣 subagent 修复 | issue修复、自动化PR |
| **subagent-driven-development** | 子代理驱动开发，两阶段审查 | 子代理驱动、并行任务 |
| **dispatching-parallel-agents** | 并行分发独立任务给多个子代理 | 并行任务、独立任务 |
| **git-worktrees** | Git 隔离工作空间 | worktree、隔离开发 |
| **tmux** | 远程控制 tmux 会话 | tmux、交互CLI |

### 规划与流程

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **brainstorming** | 头脑风暴，任何创意工作前必须使用 | 头脑风暴、创意、设计方案 |
| **writing-plans** | 编写实施计划，将规格分解为可执行步骤 | 写计划、任务分解 |
| **executing-plans** | 在独立 session 中执行书面实施计划 | 执行计划、按计划执行 |
| **finishing-a-development-branch** | 完成开发分支：Merge、PR 或清理 | 完成开发、合并 |
| **verification-before-completion** | 完成后验证，必须运行验证命令再声明成功 | 完成、验证 |
| **systematic-debugging** | 系统调试，找到根本原因再提出修复方案 | Bug、报错、调试 |
| **receiving-code-review** | 接收代码审查反馈，验证后再实施 | 审查反馈、review意见 |
| **requesting-code-review** | 请求代码审查，验证工作满足需求 | 请求审查 |
| **using-superpowers** | 超能力入口，建立如何使用 skills 的框架 | 使用技能、激活 |
| **writing-skills** | 编写新技能，编辑或验证现有技能 | 创建技能、编写技能 |

### 测试与质量

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **test-driven-development** | TDD 测试驱动开发，先写测试再看实现 | TDD、测试驱动 |
| **systematic-debugging** | 系统调试，找到根本原因再修复 | Bug、调试 |

### 平台集成（消息）

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **discord** | Discord 操作 | Discord、频道操作 |
| **slack** | Slack 控制 | Slack、控制 |
| **notion** | Notion API：页面、数据库 | Notion |
| **obsidian** | Obsidian vault 操作 | Obsidian、笔记库 |
| **trello** | Trello boards 管理 | Trello |

### Apple 生态

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **apple-notes** | Apple Notes 管理 | Apple Notes |
| **apple-reminders** | Apple Reminders 管理 | Apple Reminders |
| **bear-notes** | Bear 笔记 | Bear |
| **things-mac** | Things 3 任务管理 | Things 3 |
| **sag** | ElevenLabs TTS 语音合成 | 语音合成 |
| **sherpa-onnx-tts** | 本地离线 TTS | 离线TTS |
| **openhue** | Philips Hue 灯光控制 | 灯光 |
| **spotify-player** | Spotify 播放控制 | Spotify |
| **sonoscli** | Sonos 音箱控制 | Sonos |
| **songsee** | 音频频谱图可视化 | 频谱图 |
| **blucli** | BluOS 设备控制 | 音响 |
| **gog** | Google Workspace | Gmail、Google |
| **imsg** | iMessage 发送 | iMessage |
| **bluebubbles** | iMessage via BlueBubbles | iMessage |
| **wacli** | WhatsApp 消息 | WhatsApp |
| **ordercli** | Foodora 订单查询 | 订单 |
| **eightctl** | Eight Sleep pods 控制 | 睡眠 |
| **peekaboo** | macOS UI 自动化 | macOS UI |
| **voice-call** | OpenClaw 语音通话 | 语音通话 |

### 实用工具

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **weather** | 天气查询（wttr.in） | 天气 |
| **video-frames** | FFmpeg 视频帧提取 | 视频帧 |
| **openai-whisper** | 本地语音转文本 | 语音转文本 |
| **openai-whisper-api** | OpenAI Whisper API | 音频转录 |
| **nano-pdf** | PDF 编辑 | PDF编辑 |
| **gifgrep** | GIF 搜索下载 | GIF |
| **xurl** | X (Twitter) API | Twitter |
| **blogwatcher** | RSS/博客监控 | RSS |
| **session-logs** | Session 日志搜索 | 日志 |
| **canvas** | 画布操作 | canvas |
| **model-usage** | 模型使用量统计 | 使用量 |
| **mcporter** | MCP 工具调用 | MCP |
| **oracle** | Oracle CLI | Oracle |

### 搜索与研究

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **gemini** | Gemini CLI 问答 | Gemini |
| **summarize** | 长内容摘要 | 摘要、总结 |
| **web-access** | 网页访问：搜索、抓取、登录、动态渲染 | 搜索、网页抓取 |

---

## 二、OpenClaw 扩展 Skills

路径：`C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\dist\extensions\<extension>\skills\<skill>\SKILL.md`

> 扩展是可选插件，需要在 `openclaw.json` 中配置才能启用。文件存在 ≠ 已启用。

### 飞书扩展（✅ 已启用）

| Skill | 路径 | 描述 |
|-------|------|------|
| **feishu-doc** | `feishu\skills\feishu-doc\` | 飞书文档读写操作 |
| **feishu-wiki** | `feishu\skills\feishu-wiki\` | 飞书知识库导航 |
| **feishu-drive** | `feishu\skills\feishu-drive\` | 飞书云盘文件管理 |
| **feishu-perm** | `feishu\skills\feishu-perm\` | 飞书文档权限管理 |

### 搜索扩展（✅ 已启用 tavily）

| Skill | 路径 | 描述 |
|-------|------|------|
| **tavily** | `tavily\skills\tavily\` | Tavily 网页搜索、内容提取、研究工具 |

### 其他扩展（🔧 已安装但未启用）

| 扩展 | 包含 Skills | 说明 |
|------|------------|------|
| **acpx** | acp-router | ACP 路由 |
| **diffs** | diffs | Diff 查看器 |
| **memory-wiki** | wiki-maintainer, obsidian-vault-maintainer | Wiki 维护 |
| **open-prose** | prose | 多代理工作流 |
| **qqbot** | qqbot-channel, qqbot-media, qqbot-remind | QQ 频道机器人 |
| **tlon** | tlon | Tlon/Urbit API |
| **discord** | (channel) | Discord 集成 |
| **slack** | (channel) | Slack 集成 |
| **whatsapp** | (channel) | WhatsApp 集成 |
| **telegram** | (channel) | Telegram 集成 |
| **signal** | (channel) | Signal 集成 |
| **anthropic** | (model provider) | Anthropic 模型 |
| **openai** | (model provider) | OpenAI 模型 |
| **minimax** | (model provider) | MiniMax 模型 |
| **memory-lancedb** | memory-lancedb-pro | 向量记忆系统 |
| **...** | (90+ extensions) | 更多扩展略 |

---

## 三、YMOS 定制 Skills

路径：`D:\7_AI\YMOS\skills\<skill-name>\SKILL.md`

> YMOS 工作区内置的技能，克隆下来就存在。

### 投研数据

| Skill | 描述 | 触发词 | 状态 |
|-------|------|--------|------|
| **finnhub** | Finnhub 美股数据：行情、财报、新闻 | 美股行情、NVDA财报 | 📦 |
| **tushare-data** | Tushare A股数据：行情、财报、板块、资金流 | A股、指数、ETF、财务 | 📦 |
| **cmc-official** | 加密货币数据 | 加密货币 | 📦 |

### 搜索与研究

| Skill | 描述 | 触发词 | 状态 |
|-------|------|--------|------|
| **web-access** | 网页访问：搜索、抓取、登录、动态渲染 | 搜索、网页抓取 | 📦 |
| **grok-search** | Grok 实时搜索：突发新闻、舆情 | 最新消息、舆情 | 📦 |
| **exa-search** | Exa 搜索：结构化搜索和内容提取 | 搜索、内容提取 | 📦 |

### 内容生产

| Skill | 描述 | 触发词 | 状态 |
|-------|------|--------|------|
| **summarize** | 内容摘要：长网页、文档、访谈、研报 | 摘要、总结 | 📦 |
| **wan-image-video-generation-editting** | 阿里万德：文生图/视频 | 生成图片、生成视频 | 📦 |

### 开发流程

| Skill | 描述 | 触发词 | 状态 |
|-------|------|--------|------|
| **brainstorming** | 头脑风暴：创意工作前的需求和设计探索 | 头脑风暴、创意 | 📦 |
| **writing-plans** | 编写实施计划 | 写计划 | 📦 |
| **executing-plans** | 执行书面实施计划 | 执行计划 | 📦 |
| **finishing-a-development-branch** | 完成开发分支：Merge/PR/清理 | 完成开发、合并 | 📦 |
| **verification-before-completion** | 完成后验证 | 完成、验证 | 📦 |
| **systematic-debugging** | 系统调试 | Bug、调试 | 📦 |
| **receiving-code-review** | 接收代码审查反馈 | 审查反馈 | 📦 |
| **requesting-code-review** | 请求代码审查 | 请求审查 | 📦 |
| **test-driven-development** | TDD 测试驱动开发 | TDD、测试驱动 | 📦 |
| **subagent-driven-development** | 子代理驱动开发 | 子代理驱动 | 📦 |
| **dispatching-parallel-agents** | 并行代理分发 | 并行任务 | 📦 |
| **using-git-worktrees** | Git 隔离工作空间 | worktree | 📦 |
| **using-superpowers** | 超能力入口 | 使用技能 | 📦 |
| **writing-skills** | 编写新技能 | 创建技能 | 📦 |

### 记忆系统

| Skill | 描述 | 触发词 | 状态 |
|-------|------|--------|------|
| **memory-lancedb-pro** | LanceDB 向量数据库：混合检索、智能提取 | 长期记忆、向量检索 | 📦 |

---

## 四、Skill 速查索引

### 按用途分类——你当前能用的

**财经投研（YMOS，需配置 API Key）**
- finnhub（需 FINNHUB_API_KEY）
- tushare-data（需 TUSHARE_TOKEN）

**搜索研究（✅ 已启用 tavily）**
- tavily（已配置 API Key）

**飞书集成（✅ 已启用）**
- feishu-doc, feishu-wiki, feishu-drive, feishu-perm

**内容创作（YMOS）**
- summarize, wan-image-video-generation-editting

**开发流程（OpenClaw 内置，始终可用）**
- brainstorming, writing-plans, executing-plans, systematic-debugging, test-driven-development 等

### 触发词速查

| 你说 | AI 会调用 |
|------|----------|
| 帮我查一下宁德时代的财报 | finnhub |
| 帮我查一下A股最近的板块动态 | tushare-data |
| 帮我搜索一下最新的AI新闻 | tavily ✅ |
| 生成一张科技感的图片 | wan-image-video-generation-editting |
| 把这篇研报摘要一下 | summarize |
| 帮我做一个产品设计 | brainstorming |
| 帮我写个执行计划 | writing-plans |
| 帮我debug这个问题 | systematic-debugging |
| TDD方式写个功能 | test-driven-development |
| 把这个PR审查一下 | receiving-code-review |
| 帮我同步到飞书文档 | feishu-doc ✅ |
| 查一下天气 | weather |
| 帮我配对移动端 | node-connect |
| 给我做一个安全审计 | healthcheck |

---

## 五、Skill 路径速查表

| Skill | Windows 路径 | 状态 |
|-------|------------|------|
| clawhub | `...\openclaw\skills\clawhub\SKILL.md` | 📦 |
| skill-creator | `...\openclaw\skills\skill-creator\SKILL.md` | 📦 |
| taskflow | `...\openclaw\skills\taskflow\SKILL.md` | 📦 |
| healthcheck | `...\openclaw\skills\healthcheck\SKILL.md` | 📦 |
| node-connect | `...\openclaw\skills\node-connect\SKILL.md` | 📦 |
| weather | `...\openclaw\skills\weather\SKILL.md` | 📦 |
| feishu-doc | `...\extensions\feishu\skills\feishu-doc\SKILL.md` | ✅ |
| feishu-wiki | `...\extensions\feishu\skills\feishu-wiki\SKILL.md` | ✅ |
| feishu-drive | `...\extensions\feishu\skills\feishu-drive\SKILL.md` | ✅ |
| feishu-perm | `...\extensions\feishu\skills\feishu-perm\SKILL.md` | ✅ |
| tavily | `...\extensions\tavily\skills\tavily\SKILL.md` | ✅ |
| finnhub (YMOS) | `D:\7_AI\YMOS\skills\finnhub\SKILL.md` | 📦 |
| tushare-data (YMOS) | `D:\7_AI\YMOS\skills\tushare-data\SKILL.md` | 📦 |
| web-access (YMOS) | `D:\7_AI\YMOS\skills\web-access\SKILL.md` | 📦 |
| grok-search (YMOS) | `D:\7_AI\YMOS\skills\grok-search\SKILL.md` | 📦 |
| summarize (YMOS) | `D:\7_AI\YMOS\skills\summarize\SKILL.md` | 📦 |
| brainstorming (YMOS) | `D:\7_AI\YMOS\skills\brainstorming\SKILL.md` | 📦 |
| writing-plans (YMOS) | `D:\7_AI\YMOS\skills\writing-plans\SKILL.md` | 📦 |
| test-driven-development (YMOS) | `D:\7_AI\YMOS\skills\test-driven-development\SKILL.md` | 📦 |
| wan-image-video-generation-editting (YMOS) | `D:\7_AI\YMOS\skills\wan-image-video-generation-editting\SKILL.md` | 📦 |

---

## 六、如何启用更多 Skills

### 启用飞书相关 Skill（当前已支持）
飞书文档/知识库/云盘/权限管理已可用，仅需在对话中触发即可。

### 启用其他扩展插件
在 `openclaw.json` 的 `plugins.entries` 中添加配置，例如：

```json
"plugins": {
  "entries": {
    "tavily": { "enabled": true, "config": { ... } },
    "minimax": { "enabled": true },
    "qqbot": { "enabled": true, "config": { ... } },
    "discord": { "enabled": true, "config": { ... } }
  }
}
```

### 安装新的 Skill（通过 clawhub）
```bash
clawhub install <skill-name>
```

---

*文档版本：v1.1.0*
*生成时间：2026-04-21*
*下次审查：2026-05-21*