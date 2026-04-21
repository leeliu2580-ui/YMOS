#!/usr/bin/env python3
"""
极简市场报告生成脚本
Day 1 产出：用 MiniMax API 生成一篇投研报告

用法:
    python generate_report.py "Apple CEO 换帅"
    python generate_report.py "宁德时代 财报"
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

# ── 配置 ────────────────────────────────────────────
MINIMAX_API_URL = "https://api.minimaxi.com/anthropic/v1/messages"
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MODEL = "MiniMax-M2.7"

# Tavily API
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
TAVILY_API_URL = "https://api.tavily.com/search"

# ── Prompt 模板 ────────────────────────────────────
SYSTEM_PROMPT = """你是一位 A 股资深分析师，擅长用数据说话，语言简洁，逻辑清晰。
输出格式为 Markdown，直接可复制到飞书。
每次输出末尾附上来源链接。

输出结构：
## [标题]

### 背景
[事件核心事实，2-3句话]

### 核心影响
[对市场/行业/个股的主要影响，2-3个关键点]

### 受益/受损板块
[哪些板块受益，哪些受损，简短说明逻辑]

### 风险提示
[潜在风险点，1-2条，注明"需核实"的数据]

---
*本报告由 AI 辅助生成，仅供参考，不构成投资建议。*
"""

USER_PROMPT_TEMPLATE = """请根据以下选题，生成一篇投研报告初稿：

【选题】：{topic}
【背景信息】：{context}
"""

# ── 工具函数 ───────────────────────────────────────

def search_tavily(query, api_key):
    """用 Tavily 搜索热点信息"""
    if not api_key:
        print("⚠️ TAVILY_API_KEY 未设置，跳过搜索")
        return ""

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": 5
    }

    req = urllib.request.Request(
        TAVILY_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
            results = data.get("results", [])
            context = "\n".join([
                f"- {r.get('title', '')}: {r.get('content', '')[:200]}"
                for r in results
            ])
            return context
    except urllib.error.URLError as e:
        print(f"⚠️ Tavily 搜索失败: {e}")
        return ""


def call_minimax(topic, context, api_key):
    """调用 MiniMax API 生成报告"""
    if not api_key:
        print("⚠️ MINIMAX_API_KEY 未设置")
        return None

    user_prompt = USER_PROMPT_TEMPLATE.format(topic=topic, context=context or "无")

    payload = {
        "model": MODEL,
        "max_tokens": 2048,
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
        "system_prompt": SYSTEM_PROMPT
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "anthropic-version": "2023-06-01"
    }

    req = urllib.request.Request(
        MINIMAX_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
            # MiniMax Anthropic 兼容格式
            return data.get("content", [{}])[0].get("text", "")
    except urllib.error.URLError as e:
        print(f"⚠️ MiniMax API 调用失败: {e}")
        return None


def save_report(topic, content):
    """保存报告到 output 目录"""
    output_dir = os.path.join(os.path.dirname(__file__), "output", "reports")
    os.makedirs(output_dir, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    # 清理标题中的非法字符
    safe_topic = "".join(c if c.isalnum() or c in " -_" else "_" for c in topic)
    filename = f"{date_str}_{safe_topic}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 报告已保存: {filepath}")
    return filepath


# ── 主流程 ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="极简市场报告生成")
    parser.add_argument("topic", nargs="?", default="今日市场热点",
                        help="报告选题，例如：Apple CEO 换帅")
    args = parser.parse_args()

    topic = args.topic
    print(f"\n📊 选题：{topic}")
    print(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("-" * 40)

    # Step 1: 搜索热点
    print("\n🔍 搜索热点...")
    context = search_tavily(topic, TAVILY_API_KEY)
    if context:
        print(f"✅ 找到 {len(context)} 字相关信息")
    else:
        print("⚠️ 使用空上下文继续")

    # Step 2: 生成报告
    print("\n🤖 生成报告中...")
    report = call_minimax(topic, context, MINIMAX_API_KEY)

    if not report:
        print("❌ 报告生成失败")
        sys.exit(1)

    # Step 3: 保存
    print("\n💾 保存报告...")
    filepath = save_report(topic, report)

    # Step 4: 打印报告
    print("\n" + "=" * 40)
    print("📄 报告内容：")
    print("=" * 40)
    print(report)

    return filepath


if __name__ == "__main__":
    main()
