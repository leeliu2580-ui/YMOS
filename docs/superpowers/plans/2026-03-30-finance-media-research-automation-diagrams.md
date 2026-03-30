# 财经自媒体与投研自动化系统架构图（v1）

> 配套主文档：`docs/superpowers/plans/2026-03-30-finance-media-research-automation-architecture.md`
> 用途：用于沟通系统边界、数据流、任务流和 MVP 先后顺序。

---

## 1. 系统总体架构图

```mermaid
flowchart TB
    U[用户 / 审校人] --> R[审校后台\nStreamlit / Web UI]
    U --> N8N[n8n 调度中心]

    N8N --> API[Python / FastAPI 服务层]
    R --> API

    subgraph Data[数据采集层]
        DS1[财经资讯源\n新浪/东财/同花顺/RSS]
        DS2[投研数据源\nTushare/AkShare/公告/财务]
        DS3[视频/图文素材源]
    end

    WA[OpenClaw web-access 技能\n复杂联网增强层]

    DS1 --> API
    DS2 --> API
    DS3 --> API
    DS1 -.复杂网页/动态站点.-> WA
    DS3 -.登录态/交互站点.-> WA
    WA --> API

    subgraph Rule[规则处理层]
        RP1[清洗/去重/聚类]
        RP2[规则筛选/公告分类]
        RP3[token 预算预估\n上下文裁剪]
    end

    API --> RP1
    API --> RP2
    API --> RP3

    subgraph AI[AI 分析层]
        LLM_LOCAL[本地模型\nOllama + Qwen2.5-7B]
        ASR[本地转写\nfaster-whisper]
        LLM_CLOUD[云端模型 API\nGemini / GPT / DeepSeek]
        IMG[图像 API\n豆包 / Gemini / Flux]
    end

    RP1 --> LLM_LOCAL
    RP1 --> ASR
    RP2 --> LLM_CLOUD
    RP3 --> LLM_CLOUD
    RP3 --> LLM_LOCAL

    subgraph Store[存储层]
        DB[(SQLite / PostgreSQL)]
        VDB[(ChromaDB)]
        FILES[(原文/转写/报告文件)]
    end

    API --> DB
    API --> VDB
    API --> FILES
    LLM_LOCAL --> API
    ASR --> API
    LLM_CLOUD --> API
    IMG --> API

    subgraph Delivery[交付层]
        OUT1[自媒体选题 / 草稿 / 配图]
        OUT2[投研筛股 / 日报 / YMOS 报告]
        OUT3[通知推送\n飞书/企微/Telegram]
    end

    API --> OUT1
    API --> OUT2
    API --> OUT3

    subgraph Observe[监控与控制层]
        METRICS[/metrics]
        DLQ[DLQ / 重试队列]
        BUDGET[预算 / 熔断器]
        LOGS[结构化日志 / trace_id]
    end

    API --> METRICS
    API --> DLQ
    API --> BUDGET
    API --> LOGS
    N8N --> DLQ
    N8N --> BUDGET
```

---

## 2. 分层职责图

```mermaid
flowchart LR
    A[数据采集层] --> B[规则处理层]
    B --> C[AI 分析层]
    C --> D[交付层]
    D --> E[人机协同层]
    E --> F[反馈回流层]
    F --> B

    A1[抓数据 / 抽正文 / 转结构化] --- A
    B1[去重 / 聚类 / 筛选 / 路由 / 预算预估] --- B
    C1[本地批处理 + 云端深度分析] --- C
    D1[日报 / 草稿 / Dashboard / 通知] --- D
    E1[审校 / 采纳 / 驳回 / 重生成] --- E
    F1[周报 / 调规则 / 调 prompt / 版本回滚] --- F
```

---

## 3. 财经自媒体数据流图

```mermaid
flowchart TB
    S1[热点源 / RSS / 财经站点 / 视频链接] --> P1[采集与正文抽取]
    P1 --> P2[去重 / 聚类 / 热度评分]
    P2 --> P3[本地模型初筛\n标签 / 主题 / 提纲]
    P3 --> P4[候选选题池]
    P4 --> P5[固定选题库 topic_library]
    P4 --> P6[云端模型生成高质量提纲 / 初稿]
    P6 --> P7[配图 API]
    P6 --> P8[审校后台]
    P7 --> P8
    P8 --> P9[导出 Markdown / HTML / 平台草稿]
    P8 --> P10[反馈事件\nselected / edit_level / publish]
    P10 --> P11[周度统计与 Act 调整]
    P11 -.高采纳选题入库.-> P5
```

---

## 4. 金融投研数据流图

```mermaid
flowchart TB
    R1[行情 / 财务 / 公告 / 新闻] --> R2[采集与标准化]
    R2 --> R3[规则筛股引擎]
    R3 --> R35[交易规则引擎\nPhase 2 扩展]
    R3 --> R4[候选标的池]
    R4 --> R5[本地/云端批量初评]
    R5 --> R6[重点标的深挖]
    R6 --> R7[YMOS 四步闭环\n市场洞察 → 投资雷达 → 策略分析 → 持仓收口]
    R7 --> R8[日报 / 盘后报告 / Dashboard]
    R8 --> R9[审校与人工确认]
    R9 --> R10[反馈回流\nselected / actual_return_5d / max_drawdown]
    R10 --> R11[周度统计与 rule_versions 更新]
```

---

## 5. 任务流图（异步任务状态机）

```mermaid
stateDiagram-v2
    [*] --> pending
    pending --> running
    running --> succeeded
    running --> failed_retryable
    running --> failed_terminal
    failed_retryable --> pending: 指数退避后重试
    failed_retryable --> dead_lettered: 超过重试阈值
    failed_terminal --> dead_lettered
    dead_lettered --> pending: 人工重放
    dead_lettered --> ignored: 人工忽略
    succeeded --> [*]
    ignored --> [*]
```

---

## 6. 成本与熔断控制图

```mermaid
flowchart LR
    T[任务进入执行前] --> C1[检查模型预算]
    C1 --> C2[检查 token 上限]
    C2 --> C3[检查熔断状态 circuit_open]
    C3 -->|正常| C4[允许执行]
    C3 -->|已熔断| C7[阻止执行 / 等待人工确认]
    C4 --> C5[记录预估成本]
    C5 --> C6[执行后回写实际成本]
    C6 --> C8{是否超预算 / 连续失败?}
    C8 -->|否| C9[继续运行]
    C8 -->|是| C10[打开熔断器]
    C10 --> C11[推送告警]
    C11 --> C12[降级到本地模型 / 暂停非核心任务]
```

---

## 7. GPU 调度图

```mermaid
flowchart TB
    Q1[GPU 队列 A\n本地 LLM 文本任务]
    Q2[GPU 队列 B\nWhisper 转写]
    Q3[GPU 队列 C\nEmbedding / 建库]

    SCH[GPU 调度器\n并发上限=1] --> Q1
    SCH --> Q2
    SCH --> Q3

    T1[白天\n热点初筛 / 轻量摘要] --> SCH
    T2[盘后\n投研筛选 / 候选分析] --> SCH
    T3[夜间\n批量转写 / RAG 重建] --> SCH

    SCH --> GPU[RTX 3060 12GB]
```

---

## 8. MVP 先后顺序图

```mermaid
flowchart LR
    M0[总方案定稿] --> M1{选哪条主线先闭环?}
    M1 --> A1[路线 A\n自媒体选题列表 MVP]
    M1 --> B1[路线 B\n投研筛选 MVP]

    A1 --> A2[热点采集]
    A2 --> A3[聚类与选题]
    A3 --> A4[审校页]
    A4 --> A5[Markdown 导出]

    B1 --> B2[数据采集]
    B2 --> B3[规则筛股]
    B3 --> B4[简版分析]
    B4 --> B5[日报输出]

    A5 --> M2[Phase 2: 降本增效]
    B5 --> M2
    M2 --> M3[本地模型 / RAG / 爆款拆解 / Dashboard]
    M3 --> M4[Phase 3: 半自动运营]
```

---

## 9. 审校与回流图

```mermaid
flowchart TB
    G1[待审项目\n选题 / 草稿 / 筛股结果 / 报告] --> G2[审校后台]
    G2 --> G3{人工决策}
    G3 -->|采纳| G4[导出 / 发布 / 入库]
    G3 -->|驳回| G5[记录驳回原因]
    G3 -->|重生成| G6[回到 Python 服务重新生成]
    G3 -->|观察| G7[保留为候选]

    G4 --> G8[feedback_events]
    G5 --> G8
    G7 --> G8
    G8 --> G9[周度统计脚本]
    G9 --> G10[Act: 调整阈值 / 权重 / prompt]
    G10 --> G11[写入 rule_versions 可回滚]
```

---

## 10. 图文档使用建议

### 对老板 / 合作者沟通优先看
1. 系统总体架构图
2. 财经自媒体数据流图
3. 金融投研数据流图
4. MVP 先后顺序图

### 对开发实现优先看
1. 分层职责图
2. 任务流图（状态机）
3. 成本与熔断控制图
4. GPU 调度图
5. 审校与回流图

### 对后续实施的意义
- 主文档负责原则与约束
- 图文档负责边界和路径
- 两者一起，基本可以进入 MVP 实施计划拆分阶段
