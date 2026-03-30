---
name: summarize
description: Use when you need to compress long webpages, documents, transcripts, notes, or research materials into concise summaries, structured takeaways, or executive digests for content work, planning, or investment research.
---

# Summarize

## Overview
这个 skill 现在已经接到本地可执行实现：`summarize_local.py`。

当前默认方案：
- 输入：网页 URL 或本地文本文件
- 提取：静态网页正文 / 本地文本读取
- 摘要：调用本机 Ollama 模型
- 默认模型：`qwen2.5-coder:7b`（可用 `YMOS_SUMMARIZE_MODEL` 覆盖）

## 什么时候用
- 长网页、长文、纪要、草稿要压缩
- 研报、资讯、访谈文本要提炼成结构化摘要
- 需要统一输出成“结论 → 要点 → 风险 → 可用价值”

## 不什么时候用
- 只有几句话的短内容
- 需要逐字逐句保真校对
- PDF/音视频尚未转成文本时（先走 OCR / Whisper / 网页提取）

## 最小命令
```bash
python summarize_local.py "https://example.com"
```

```bash
python summarize_local.py "D:\\path\\note.md" --json
```

## 参数
- `target`：URL 或文本文件路径
- `--model`：指定 Ollama 模型
- `--style`：摘要风格
- `--json`：JSON 输出

## 推荐工作流
1. 网页内容：先直接丢 URL
2. 音视频内容：先用 `openai-whisper` 转文字
3. 再用本 skill 生成摘要
4. 投研输出尽量落到：`结论 → 核心逻辑 → 风险点 → 应对预案`

## 注意
- 当前是 MVP 级本地实现，适合先把链路跑通
- 对动态网页、登录态页面、反爬页面，先配合 `web-access`
- 对 PDF、图片、音视频，先做文本化预处理再摘要
