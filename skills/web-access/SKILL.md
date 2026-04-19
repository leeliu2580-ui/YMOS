---
name: web-access
description: |
  网页访问技能。所有联网操作必须通过此 skill 处理——搜索信息、网页抓取、登录后操作、社交媒体内容提取（小红书/微博/推特等）、动态渲染页面、以及任何需要真实浏览器环境的网络任务。
  触发方式：搜索、网页、抓取、登录、小红书、微博、推特、动态渲染、CDP、浏览器
  All web access operations: search, scraping, authenticated access, social media extraction, dynamic pages, browser automation.
  Trigger: search, scrape, login, social media, Xiaohongshu, Twitter, CDP, browser
---

# web-access：网页访问

## 前置检查 | Prerequisites

在开始联网操作前，先检查 CDP 模式可用性：

```bash
node "$CLAUDE_SKILL_DIR/scripts/check-deps.mjs"
```

- **Node.js 22+**：必需（使用原生 WebSocket）
- **Chrome remote-debugging**：在 Chrome 地址栏打开 `chrome://inspect/#remote-debugging`，勾选 **"Allow remote debugging for this browser instance"**

## 浏览哲学 | Browser Philosophy

**像人一样思考，兼顾高效与适应性的完成任务。**

带着目标进入，边看边判断，遇到阻碍就解决，发现内容不够就深入——全程围绕「我要达成什么」做决策。

**① 拿到请求** — 先明确成功标准：什么算完成了？

**② 选择起点** — 根据任务性质选最可能直达的方式。不成功则调整。

**③ 过程校验** — 每一步的结果都是证据，不只是成功或失败的二元信号。

**④ 完成判断** — 对照任务成功标准，确认完成后就停止。

## 联网工具选择 | Tool Selection

| 场景 | 工具 |
|------|------|
| 搜索摘要或关键词 | **WebSearch** |
| 已知 URL 提取特定信息 | **WebFetch** |
| 已知 URL 获取原始 HTML | **curl** |
| 非公开内容、静态层无效的平台 | **浏览器 CDP** |
| 需要登录态或像人一样导航 | **浏览器 CDP** |

## 浏览器 CDP 模式 | Browser CDP Mode

通过 CDP Proxy 直连用户 Chrome，天然携带登录态。

### 常用 API

```bash
# 列出已打开的 tab
curl -s http://localhost:3456/targets

# 创建新后台 tab
curl -s "http://localhost:3456/new?url=https://example.com"

# 执行 JS（读写 DOM、提取数据）
curl -s -X POST "http://localhost:3456/eval?target=ID" -d 'document.title'

# 截图
curl -s "http://localhost:3456/screenshot?target=ID&file=/tmp/shot.png"

# 点击元素
curl -s -X POST "http://localhost:3456/click?target=ID" -d 'button.submit'

# 滚动
curl -s "http://localhost:3456/scroll?target=ID&y=3000"

# 关闭 tab
curl -s "http://localhost:3456/close?target=ID"
```

## 信息核实原则 | Source Verification

信息来源优先级：**一手来源 > 权威媒体 > 二手报道**

| 信息类型 | 一手来源 |
|----------|---------|
| 政策/法规 | 发布机构官网 |
| 企业公告 | 公司官方新闻页 |
| 工具能力/用法 | 官方文档、源码 |

## 并行调研 | Parallel Research

多个独立目标时，鼓励分治给子代理并行执行。

每个子代理：
- 在用户浏览器中自行创建后台 tab
- 任务结束自行关闭 tab
- 无竞态风险（共享 Chrome 实例）
