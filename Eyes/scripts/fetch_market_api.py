#!/usr/bin/env python3
"""
YMOS Market Data API 示例脚本

说明：
- 这是“市场信息洞察”数据源的示例模板
- 适合用户替换为自己的市场信息 API
- 不内置任何真实私钥，统一通过环境变量或命令行参数传入
"""

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT = SCRIPTS_DIR.parents[1]  # Eyes/scripts → Eyes → YMOS
sys.path.insert(0, str(SCRIPTS_DIR))
from env_loader import load_dotenv


DEFAULT_API_URL = "https://yongmai.xyz/wp-json/tib/v1/reports"
DEFAULT_CATEGORIES = [
    "#中国股市",
    "#美国股市",
    "#Crypto",
    "#宏观经济",
    "#科技动态",
    "#个人精选",
]


# ── Provider: YMOS (yongmai.xyz) ──────────────────────────────────────────────

def fetch_ymos(api_url, api_key, time_value, categories):
    """从 yongmai.xyz 拉取结构化市场报告。"""
    params = {
        "time_value": time_value,
        "categories": ",".join(categories),
    }
    full_url = f"{api_url}?{urllib.parse.urlencode(params)}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "YMOS-MarketAPI/1.0",
        "Accept": "application/json",
    }
    print(f"📡 尝试从 YMOS (yongmai.xyz) 拉取数据...")
    return _do_get_request(full_url, headers)


# ── Provider: Finnhub (General News) ─────────────────────────────────────────

def fetch_finnhub(api_key, hours=24):
    """从 Finnhub 拉取全量市场新闻。"""
    url = f"https://finnhub.io/api/v1/news?category=general&token={api_key}"
    headers = {"User-Agent": "YMOS/2.0"}
    print(f"📡 尝试从 Finnhub (General News) 拉取数据...")
    raw_news = _do_get_request(url, headers)
    
    if not isinstance(raw_news, list):
        return None

    # 简单清洗并转换为 YMOS 格式
    cutoff_ts = (datetime.now(timezone.utc) - timedelta(hours=hours)).timestamp()
    events = []
    for item in raw_news:
        if item.get("datetime", 0) < cutoff_ts:
            continue
        events.append({
            "title": item.get("headline", ""),
            "content": item.get("summary", ""),
            "source": item.get("source", ""),
            "url": item.get("url", ""),
            "datetime": datetime.fromtimestamp(item.get("datetime", 0), tz=timezone.utc).isoformat(),
            "category": "#美股动态"
        })
    return {"count": len(events), "events": events, "source": "Finnhub"}


# ── Provider: Tushare (News) ───────────────────────────────────────────────

def fetch_tushare(token, hours=24):
    """从 Tushare 拉取 A 股新闻。"""
    url = "https://api.tushare.pro"
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(hours=hours)
    
    payload = {
        "api_name": "news",
        "token": token,
        "params": {
            "start_date": start_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": end_dt.strftime("%Y-%m-%d %H:%M:%S")
        },
        "fields": "datetime,content,title,channels"
    }
    
    print(f"📡 尝试从 Tushare (A股新闻) 拉取数据...")
    try:
        resp_data = _do_post_request(url, payload)
        if resp_data.get("code") != 0:
            print(f"  ❌ Tushare API Error: {resp_data.get('msg')}")
            return None
        
        items = resp_data.get("data", {}).get("items", [])
        events = []
        for item in items:
            events.append({
                "title": item[2],
                "content": item[1],
                "source": item[3],
                "datetime": item[0],
                "category": "#A股内参"
            })
        return {"count": len(events), "events": events, "source": "Tushare"}
    except Exception as e:
        print(f"  ❌ Tushare 请求失败: {e}")
        return None


# ── Provider: Tavily (AI Search) ─────────────────────────────────────────────

def fetch_tavily(api_key, categories):
    """使用 Tavily 进行 AI 驱动的市场情报搜索。"""
    url = "https://api.tavily.com/search"
    query = f"Latest market news and trends for: {', '.join(categories)}"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": 10,
        "include_answer": True
    }
    
    print(f"📡 尝试使用 Tavily 进行 AI 市场情报搜索...")
    try:
        resp_data = _do_post_request(url, payload)
        results = resp_data.get("results", [])
        events = []
        for res in results:
            events.append({
                "title": res.get("title", ""),
                "content": res.get("content", ""),
                "url": res.get("url", ""),
                "source": "Tavily Search",
                "category": "#AI搜索情报"
            })
        
        # 将 Tavily 的 AI 回答作为一个特殊的事件
        if resp_data.get("answer"):
            events.insert(0, {
                "title": "Tavily AI 市场综述",
                "content": resp_data.get("answer"),
                "source": "Tavily AI",
                "category": "#AI分析"
            })
            
        return {"count": len(events), "events": events, "source": "Tavily"}
    except Exception as e:
        print(f"  ❌ Tavily 请求失败: {e}")
        return None


# ── Helper functions ────────────────────────────────────────────────────────

def _do_get_request(url, headers):
    """通用的 GET 请求。"""
    req = urllib.request.Request(url, headers=headers, method="GET")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"  ❌ GET 请求失败: {e}")
        return None


def _do_post_request(url, payload):
    """通用的 POST 请求。"""
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", "User-Agent": "YMOS/2.0"}
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"  ❌ POST 请求失败: {e}")
        raise e


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="YMOS Market Data 综合获取脚本")
    parser.add_argument("time_value", type=float, nargs="?", default=1, help="回溯天数，默认 1")
    parser.add_argument("--output", default="market_data.json", help="输出文件路径")
    parser.add_argument(
        "--api-url",
        default=os.environ.get("YMOS_MARKET_API_URL", DEFAULT_API_URL),
        help="YMOS API URL",
    )
    parser.add_argument(
        "--categories",
        default=",".join(DEFAULT_CATEGORIES),
        help="逗号分隔的分类列表",
    )
    args = parser.parse_args()

    # 从环境变量加载所有可能的 KEY
    keys = {
        "YMOS": os.environ.get("YMOS_MARKET_API_KEY", ""),
        "FINNHUB": os.environ.get("FINNHUB_API_KEY", ""),
        "TUSHARE": os.environ.get("TUSHARE_TOKEN", ""),
        "TAVILY": os.environ.get("TAVILY_API_KEY", "")
    }

    if not any(keys.values()):
        print("⚠️ 未检测到任何可用的 API Key（YMOS, Finnhub, Tushare, Tavily）。")
        print("   💡 请在 .env 中配置至少一个 KEY，或使用 RSS 路径。")
        sys.exit(0)

    categories = [item.strip() for item in args.categories.split(",") if item.strip()]
    all_events = []
    sources_used = []

    # 1. 尝试 YMOS (优先级最高)
    if keys["YMOS"]:
        res = fetch_ymos(args.api_url, keys["YMOS"], args.time_value, categories)
        if res and res.get("events"):
            all_events.extend(res["events"])
            sources_used.append("YMOS")

    # 2. 尝试 Finnhub
    if keys["FINNHUB"]:
        res = fetch_finnhub(keys["FINNHUB"], hours=int(args.time_value * 24))
        if res and res.get("events"):
            all_events.extend(res["events"])
            sources_used.append("Finnhub")

    # 3. 尝试 Tushare
    if keys["TUSHARE"]:
        res = fetch_tushare(keys["TUSHARE"], hours=int(args.time_value * 24))
        if res and res.get("events"):
            all_events.extend(res["events"])
            sources_used.append("Tushare")

    # 4. 尝试 Tavily
    if keys["TAVILY"]:
        res = fetch_tavily(keys["TAVILY"], categories)
        if res and res.get("events"):
            all_events.extend(res["events"])
            sources_used.append("Tavily")

    if not all_events:
        print("❌ 所有 API 数据源均未获取到有效数据。")
        sys.exit(1)

    # 合并结果并保存
    final_output = {
        "count": len(all_events),
        "events": all_events,
        "sources": sources_used,
        "fetched_at": datetime.now(timezone.utc).isoformat()
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(final_output, handle, ensure_ascii=False, indent=2)

    print(f"\n✅ 成功从 {', '.join(sources_used)} 拉取共 {len(all_events)} 条情报。")
    print(f"💾 已保存至：{out_path}")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
