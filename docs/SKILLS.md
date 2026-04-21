# Skills 全局清单

> 本文档由 AI 自动生成，记录所有可用 Skill 的路径、描述和用途。
> 生成时间：2026-04-21
> 数据来源：OpenClaw 安装目录 + YMOS 工作区

---

## 目录

- [一、OpenClaw 内置 Skills](#一openclaw-内置-skills)
- [二、OpenClaw 扩展 Skills（extensions）](#二openclaw-扩展-skills-extensions)
- [三、YMOS 定制 Skills](#三ymos-定制-skills)
- [四、Skill 速查索引](#四skill-速查索引)

---

## 一、OpenClaw 内置 Skills

路径：`C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\skills\<skill-name>\SKILL.md`

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
| **coding-agent** | 委托编码任务给 Codex/Claude Code/Pi agents | 构建功能、代码实现、创建应用 |
| **github** | gh CLI 操作：issues、PRs、CI、代码审查 | PR状态、创建issue、CI检查 |
| **gh-issues** | 获取 GitHub issues 并派遣 subagent 修复 | issue修复、自动化PR |
| **subagent-driven-development** | 子代理驱动开发，两阶段审查（规格合规→代码质量） | 子代理驱动、并行任务 |
| **dispatching-parallel-agents** | 并行分发独立任务给多个子代理 | 并行任务、独立任务 |
| **git-worktrees** | Git 隔离工作空间，创建独立 worktree | worktree、隔离开发 |
| **tmux** | 远程控制 tmux 会话，发送按键并抓取输出 | tmux、交互CLI |

### 规划与流程

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **brainstorming** | 头脑风暴技能，任何创意工作前必须使用 | 头脑风暴、创意、设计方案 |
| **writing-plans** | 编写实施计划，将规格分解为可执行步骤 | 写计划、任务分解 |
| **executing-plans** | 在独立 session 中执行书面实施计划 | 执行计划、按计划执行 |
| **finishing-a-development-branch** | 完成开发分支：Merge、PR 或清理 | 完成开发、合并、创建PR |
| **verification-before-completion** | 完成后验证，必须运行验证命令再声明成功 | 完成、验证、通过 |
| **systematic-debugging** | 系统调试，找到根本原因再提出修复方案 | Bug、报错、调试、修复 |
| **receiving-code-review** | 接收代码审查反馈，验证后再实施 | 审查反馈、review意见 |
| **requesting-code-review** | 请求代码审查，验证工作满足需求 | 请求审查、代码审查 |
| **using-superpowers** | 超能力入口，建立如何使用 skills 的框架 | 使用技能、激活技能 |

### 质量与测试

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **test-driven-development** | TDD 测试驱动开发，先写测试再看实现 | TDD、测试驱动、写测试 |
| **writing-skills** | 编写新技能，编辑或验证现有技能 | 创建技能、编写技能 |

### 平台集成

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **discord** | Discord 操作（通过 message tool） | Discord、频道操作 |
| **slack** | Slack 控制：反应消息、固定/取消固定 | Slack、控制 |
| **notion** | Notion API：创建和管理页面、数据库 | Notion、页面、数据库 |
| **obsidian** | 操作 Obsidian vault（纯 Markdown 笔记） | Obsidian、笔记库 |
| **1password** | 1Password CLI (op) 安装和集成 | 1Password、密码管理 |
| **himalaya** | IMAP/SMTP 邮件管理：列表、读写、搜索 | 邮件、IMAP |
| **imsg** | iMessage/SMS：列表聊天、历史、发送 | iMessage、短信 |
| **bluebubbles** | 通过 BlueBubbles 发送 iMessage | iMessage发送 |
| **wacli** | WhatsApp 消息发送和历史搜索 | WhatsApp |
| **trello** | Trello boards、lists、cards 管理 | Trello、项目管理 |

### Apple 生态

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **apple-notes** | Apple Notes 管理（memo CLI） | Apple Notes、笔记 |
| **apple-reminders** | Apple Reminders 管理（remindctl CLI） | Apple Reminders、提醒 |
| **bear-notes** | Bear 笔记创建、搜索、管理 | Bear、笔记 |
| **things-mac** | Things 3 管理（things CLI） | Things 3、任务管理 |
| **sag** | ElevenLabs TTS，mac-style say UX | 语音合成、TTS |
| **sherpa-onnx-tts** | 本地离线 TTS（sherpa-onnx） | 离线TTS |
| **openhue** | Philips Hue 灯光控制 | Hue、智能灯光 |
| **spotify-player** | Spotify 播放/搜索（spogo） | Spotify、音乐 |
| **sonoscli** | Sonos 音箱控制 | Sonos、音箱 |
| **songsee** | 音频频谱图和特征面板可视化 | 频谱图、音频分析 |
| **blucli** | BluOS CLI：发现、播放、分组、音量 | BluOS、音响 |
| **gog** | Google Workspace：Gmail、Calendar、Drive | Gmail、Google |
| **ordercli** | Foodora 订单查询 | 订单、外卖 |
| **eightctl** | Eight Sleep pods 控制 | 睡眠追踪、温度控制 |
| **peekaboo** | macOS UI 捕获和自动化 | macOS UI、自动化 |
| **voice-call** | OpenClaw 语音通话 | 语音通话 |

### 硬件与设备

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **openhue** | Philips Hue 灯光和场景 | 灯光控制 |
| **blucli** | BluOS 设备控制 | 音响控制 |
| **camsnap** | RTSP/ONVIF 摄像头帧捕获 | 摄像头、视频流 |
| **goplaces** | Google Places API 查询 | 地点查询 |
| **oracle** | Oracle CLI（提示+文件打包） | Oracle |

### 数据与媒体

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **weather** | 天气查询（wttr.in/Open-Meteo） | 天气、天气预报 |
| **video-frames** | FFmpeg 视频帧/片段提取 | 视频帧、剪辑 |
| **openai-whisper** | 本地语音转文本（Whisper CLI） | 语音转文本、本地 |
| **openai-whisper-api** | OpenAI Whisper API 转录 | 音频转录 |
| **nano-pdf** | PDF 编辑（自然语言指令） | PDF编辑 |
| **gifgrep** | GIF 搜索、下载、提取静态图 | GIF、动图 |
| **xurl** | X (Twitter) API 认证请求 | Twitter、发帖 |
| **blogwatcher** | 博客/RSS 监控更新 | RSS、博客监控 |
| **session-logs** | 搜索和分析 session 日志 | session日志 |
| **canvas** | 画布操作 | canvas |
| **model-usage** | CodexBar CLI 本地成本使用统计 | 模型使用量 |

### 搜索与研究

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **gemini** | Gemini CLI 一次性问答、摘要、生成 | Gemini、问答 |
| **summarize** | 长内容摘要：网页、文档、访谈、研报 | 摘要、总结、提炼 |
| **web-access** | 网页访问：搜索、抓取、登录、动态渲染 | 搜索、网页抓取、浏览器 |

### 实用工具

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **mcporter** | MCP servers/tools 列表和调用 | MCP、工具调用 |
| **eightctl** | Eight Sleep pods 控制 | 睡眠设备 |

---

## 二、OpenClaw 扩展 Skills（extensions）

路径：`C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\dist\extensions\<extension>\skills\<skill>\SKILL.md`

### 飞书扩展（feishu）

| Skill | 路径 | 描述 |
|-------|------|------|
| **feishu-doc** | `feishu\skills\feishu-doc\` | 飞书文档读写操作 |
| **feishu-wiki** | `feishu\skills\feishu-wiki\` | 飞书知识库导航 |
| **feishu-drive** | `feishu\skills\feishu-drive\` | 飞书云盘文件管理 |
| **feishu-perm** | `feishu\skills\feishu-perm\` | 飞书文档权限管理 |

### 搜索扩展

| Skill | 路径 | 描述 |
|-------|------|------|
| **tavily** | `tavily\skills\tavily\` | Tavily 网页搜索、内容提取、研究工具 |

### ACP 扩展

| Skill | 路径 | 描述 |
|-------|------|------|
| **acp-router** | `acpx\skills\acp-router\` | ACP 路由：将请求路由到 OpenClaw ACP runtime sessions |
| **diffs** | `diffs\skills\diffs\` | 生成可分享的 diff 查看器 |

### 记忆扩展

| Skill | 路径 | 描述 |
|-------|------|------|
| **wiki-maintainer** | `memory-wiki\skills\wiki-maintainer\` | OpenClaw memory wiki vault 维护 |
| **obsidian-vault-maintainer** | `memory-wiki\skills\obsidian-vault-maintainer\` | Obsidian vault 维护 |

### 内容扩展

| Skill | 路径 | 描述 |
|-------|------|------|
| **prose** | `open-prose\skills\prose\` | OpenProse VM skill pack，多代理工作流编排 |

### QQBot 扩展

| Skill | 路径 | 描述 |
|-------|------|------|
| **qqbot-channel** | `qqbot\skills\qqbot-channel\` | QQ 频道管理：列表、子频道、成员、发帖 |
| **qqbot-media** | `qqbot\skills\qqbot-media\` | QQBot 富媒体收发（图片/语音/视频/文件） |
| **qqbot-remind** | `qqbot\skills\qqbot-remind\` | QQBot 定时提醒：一次性/周期性提醒 |

### Tlon 扩展

| Skill | 路径 | 描述 |
|-------|------|------|
| **tlon** | `tlon\bundled-skills\@tloncorp\tlon-skill\` | Tlon/Urbit API 交互：读取活动、消息、联系人 |

---

## 三、YMOS 定制 Skills

路径：`D:\7_AI\YMOS\skills\<skill-name>\SKILL.md`

### 投研数据

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **finnhub** | Finnhub 美股数据：行情、财报、新闻、加密货币 | 美股行情、NVDA财报、个股分析 |
| **tushare-data** | Tushare A股数据：行情、财报、板块、资金流、ETF | A股、指数、ETF、财务数据 |
| **cmc-official** | （CoinMarketCap 非官方集成） | 加密货币行情 |

### 搜索与研究

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **web-access** | 网页访问：搜索、抓取、登录、社交媒体、动态渲染 | 搜索、网页抓取、小红书、微博 |
| **grok-search** | Grok 实时搜索：突发新闻、舆情、Twitter 动态 | 最新消息、舆情、实时动态 |
| **exa-search** | Exa 搜索：结构化搜索和内容提取 | 搜索、内容提取 |

### 内容生产

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **summarize** | 内容摘要：长网页、文档、访谈、研报压缩 | 摘要、总结、提炼 |
| **wan-image-video-generation-editting** | 阿里万德：文生图、图生图、文生视频、图生视频 | 生成图片、生成视频 |

### 开发流程

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **brainstorming** | 头脑风暴：创意工作前的需求和设计探索 | 头脑风暴、创意、设计 |
| **writing-plans** | 编写实施计划 | 写计划、任务分解 |
| **executing-plans** | 执行书面实施计划 | 执行计划 |
| **finishing-a-development-branch** | 完成开发分支：Merge/PR/清理 | 完成开发、合并 |
| **verification-before-completion** | 完成后验证 | 完成、验证 |
| **systematic-debugging** | 系统调试 | Bug、调试 |
| **receiving-code-review** | 接收代码审查反馈 | 审查反馈 |
| **requesting-code-review** | 请求代码审查 | 请求审查 |
| **test-driven-development** | TDD 测试驱动开发 | TDD、测试驱动 |
| **subagent-driven-development** | 子代理驱动开发 | 子代理驱动 |
| **dispatching-parallel-agents** | 并行代理分发 | 并行任务 |
| **using-git-worktrees** | Git 隔离工作空间 | worktree、隔离开发 |
| **using-superpowers** | 超能力入口 | 使用技能 |
| **writing-skills** | 编写新技能 | 创建技能 |

### 记忆系统

| Skill | 描述 | 触发词 |
|-------|------|--------|
| **memory-lancedb-pro** | LanceDB 向量数据库记忆系统：混合检索、智能提取、生命周期管理 | 长期记忆、向量检索 |

---

## 四、Skill 速查索引

### 按用途分类

**财经投研（YMOS）**
- finnhub, tushare-data, cmc-official

**搜索研究**
- web-access, grok-search, exa-search, tavily, summarize

**飞书集成**
- feishu-doc, feishu-wiki, feishu-drive, feishu-perm

**内容创作**
- wan-image-video-generation-editting, summarize

**开发流程**
- brainstorming, writing-plans, executing-plans, TDD, systematic-debugging

**代码协作**
- github, receiving-code-review, requesting-code-review, finishing-a-development-branch

**并行任务**
- dispatching-parallel-agents, subagent-driven-development, using-git-worktrees

**平台集成（消息）**
- discord, slack, notion, imsg, bluebubbles, wacli, qqbot-*

**Apple 生态**
- apple-notes, apple-reminders, bear-notes, things-mac, sag, sherpa-onnx-tts

**硬件控制**
- openhue, blucli, camsnap, spotify-player, sonoscli, eightctl

**实用工具**
- weather, video-frames, tmux, healthcheck, node-connect

### 触发词速查

| 你说 | AI 会调用 |
|------|----------|
| 帮我查一下宁德时代的财报 | finnhub |
| 帮我查一下A股最近的板块动态 | tushare-data |
| 帮我搜索一下最新的AI新闻 | web-access / grok-search |
| 生成一张科技感的图片 | wan-image-video-generation-editting |
| 把这篇研报摘要一下 | summarize |
| 帮我做一个产品设计 | brainstorming |
| 帮我写个执行计划 | writing-plans |
| 帮我debug这个问题 | systematic-debugging |
| TDD方式写个功能 | test-driven-development |
| 把这个PR审查一下 | receiving-code-review |
| 帮我同步到飞书文档 | feishu-doc |
| 查一下天气 | weather |
| 帮我配对移动端 | node-connect |
| 给我做一个安全审计 | healthcheck |

---

## Skill 路径速查表

| Skill | Windows 路径 |
|-------|------------|
| clawhub | `C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\skills\clawhub\SKILL.md` |
| skill-creator | `C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\skills\skill-creator\SKILL.md` |
| taskflow | `C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\skills\taskflow\SKILL.md` |
| healthcheck | `C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\skills\healthcheck\SKILL.md` |
| node-connect | `C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\skills\node-connect\SKILL.md` |
| weather | `C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\skills\weather\SKILL.md` |
| feishu-doc | `C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\dist\extensions\feishu\skills\feishu-doc\SKILL.md` |
| feishu-wiki | `C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\dist\extensions\feishu\skills\feishu-wiki\SKILL.md` |
| feishu-drive | `C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\dist\extensions\feishu\skills\feishu-drive\SKILL.md` |
| feishu-perm | `C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\dist\extensions\feishu\skills\feishu-perm\SKILL.md` |
| tavily | `C:\Users\guanhai\AppData\Roaming\npm\node_modules\openclaw\dist\extensions\tavily\skills\tavily\SKILL.md` |
| finnhub (YMOS) | `D:\7_AI\YMOS\skills\finnhub\SKILL.md` |
| tushare-data (YMOS) | `D:\7_AI\YMOS\skills\tushare-data\SKILL.md` |
| web-access (YMOS) | `D:\7_AI\YMOS\skills\web-access\SKILL.md` |
| grok-search (YMOS) | `D:\7_AI\YMOS\skills\grok-search\SKILL.md` |
| summarize (YMOS) | `D:\7_AI\YMOS\skills\summarize\SKILL.md` |
| brainstorming (YMOS) | `D:\7_AI\YMOS\skills\brainstorming\SKILL.md` |
| writing-plans (YMOS) | `D:\7_AI\YMOS\skills\writing-plans\SKILL.md` |
| test-driven-development (YMOS) | `D:\7_AI\YMOS\skills\test-driven-development\SKILL.md` |
| wan-image-video-generation-editting (YMOS) | `D:\7_AI\YMOS\skills\wan-image-video-generation-editting\SKILL.md` |

---

*文档版本：v1.0.0*
*生成时间：2026-04-21*
*下次审查：2026-05-21（每月更新）*