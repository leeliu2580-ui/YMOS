#!/usr/bin/env python3
"""
BlockBeats 新闻拉取脚本

BlockBeats (theblockbeats.info) 提供深度的 Crypto/Blockchain 行业新闻，
覆盖专业 Web3 内容。API Key 配置在 .env 的 BLOCKBEATS_API_KEY 中。

用法：
  python3 Eyes/scripts/fetch_blockbeats_news.py --days 1 --output "Eyes/市场洞察/Raw_Data/2026-05/blockbeats_news_20260509.json"

  python3 Eyes/scripts/fetch_blockbeats_news.py --search "Bitcoin" --limit 20 --output "blockbeats_search.json"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT = SCRIPTS_DIR.parents[1]

sys.path.insert(0, str(SCRIPTS_DIR))
from env_loader import load_dotenv


# ── API 请求 ────────────────────────────────────────────────────────────────

def call_blockbeats_api(api_key: str, endpoint: str, params: dict) -> dict | None:
    """
    调用 BlockBeats API。

    endpoint: "news" | "search" | "netflow"
    params: 传递给 API 的查询参数
    """
    # BlockBeats API 入口
    base_url = "http://api-pro.theblockbeats.info"

    # 构建 URL
    if endpoint == "news":
        url = f"{base_url}/v1/newsflash"
    elif endpoint == "search":
        url = f"{base_url}/v1/search"
    elif endpoint == "netflow":
        url = f"{base_url}/v1/data/top10_netflow"
    else:
        print(f"❌ 未知 endpoint: {endpoint}")
        return None

    # 添加分页和限制参数
    if "page" not in params:
        params["page"] = params.get("page", 1)
    if "size" not in params and endpoint in ("news", "search"):
        params["size"] = params.get("size", params.get("limit", 50))

    # 构建完整 URL
    from urllib.parse import urlencode
    full_url = f"{url}?{urlencode(params)}"

    headers = {
        "User-Agent": "YMOS/1.0",
        "api-key": api_key,
        "Accept": "application/json",
    }

    req = urllib.request.Request(full_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")[:500]
        print(f"❌ HTTP {e.code}: {e.reason}")
        print(f"   Response: {error_body}")
        return None
    except urllib.error.URLError as e:
        print(f"❌ 网络错误: {e.reason}")
        return None
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None


def parse_news_response(data: dict, days_back: int) -> list[dict]:
    """解析 BlockBeats 新闻响应，转换为统一格式。"""
    articles = []

    # BlockBeats API v1 返回格式: {status: 0, data: {page: 1, data: [...]}}
    raw_list = []
    if isinstance(data, dict):
        if "data" in data:
            inner = data["data"]
            if isinstance(inner, dict):
                # {page: 1, data: [...]}
                raw_list = inner.get("data", [])
            elif isinstance(inner, list):
                raw_list = inner
    elif isinstance(data, list):
        raw_list = data

    cutoff_dt = datetime.now(timezone.utc) - timedelta(days=days_back)

    for item in raw_list:
        if not isinstance(item, dict):
            continue

        # 提取时间戳 - BlockBeats 用 create_time 字符串
        create_time = item.get("create_time", "")
        ts = 0
        if create_time:
            try:
                dt = datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")
                # 假设 create_time 是北京时间 (UTC+8)
                dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))
                ts = dt.timestamp()
            except:
                pass
            if ts < cutoff_dt.timestamp():
                continue

        # 标准化字段 - BlockBeats 字段名
        content_html = item.get("content", "")
        # 简单去除 HTML 标签作为 summary
        import re
        summary = re.sub(r"<[^>]+>", "", content_html)[:500] if content_html else ""

        article = {
            "source": "BlockBeats",
            "title": item.get("title", ""),
            "summary": summary,
            "url": item.get("url", item.get("link", "")),
            "datetime_ts": ts,
            "datetime_readable": create_time if create_time else "",
            "category": item.get("type", item.get("category", "")),
            "tags": item.get("labels", item.get("tags", [])),
            "author": item.get("author", item.get("source", "")),
            "thumbnail": item.get("pic", item.get("image", "")),
        }
        articles.append(article)

    return articles


def parse_search_response(data: dict) -> list[dict]:
    """解析 BlockBeats 搜索响应。"""
    results = []

    raw_list = []
    if isinstance(data, dict):
        raw_list = data.get("data", data.get("results", []))
    elif isinstance(data, list):
        raw_list = data

    for item in raw_list:
        if not isinstance(item, dict):
            continue

        results.append({
            "source": "BlockBeats",
            "title": item.get("title", ""),
            "summary": item.get("description", "")[:500],
            "url": item.get("url", ""),
            "datetime_ts": item.get("datetime", 0),
            "datetime_readable": item.get("time", ""),
            "category": item.get("category", ""),
        })

    return results


# ── 主函数 ─────────────────────────────────────────────────────────────────

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="BlockBeats 新闻拉取脚本")
    parser.add_argument("--output", default="blockbeats_news.json", help="输出文件路径")
    parser.add_argument("--days", type=int, default=1, help="回溯天数，默认 1")
    parser.add_argument("--limit", type=int, default=50, help="返回条数限制，默认 50")
    parser.add_argument("--search", type=str, default="", help="搜索关键词（设置则走搜索 API）")
    parser.add_argument("--api-key", default=os.environ.get("BLOCKBEATS_API_KEY", ""), help="BlockBeats API Key")

    args = parser.parse_args()

    if not args.api_key:
        print("⚠️ 未提供 BlockBeats API Key，跳过。")
        print("   如需启用，请在 .env 中配置 BLOCKBEATS_API_KEY")
        sys.exit(0)

    print(f"📡 BlockBeats 数据拉取（回溯 {args.days} 天，限制 {args.limit} 条）")

    if args.search:
        print(f"   🔍 搜索模式: {args.search}")
        data = call_blockbeats_api(args.api_key, "search", {"keyword": args.search, "limit": args.limit})
        if data:
            articles = parse_search_response(data)
        else:
            articles = []
    else:
        print(f"   📰 新闻列表模式")
        data = call_blockbeats_api(args.api_key, "news", {"limit": args.limit})
        if data:
            articles = parse_news_response(data, args.days)
        else:
            articles = []

    now_utc = datetime.now(timezone.utc)

    output = {
        "meta": {
            "source": "BlockBeats API",
            "mode": "search" if args.search else "news",
            "days_back": args.days,
            "limit": args.limit,
            "search_keyword": args.search if args.search else None,
            "generated_at": now_utc.strftime("%Y-%m-%d %H:%M UTC"),
            "counts": {
                "total": len(articles),
            },
        },
        "articles": articles,
    }

    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"💾 已保存：{args.output}")
    print(f"   总计：{len(articles)} 条")


if __name__ == "__main__":
    main()