#!/usr/bin/env python3
"""
Eyes/scripts/fetch_official_updates.py
聚合官方信息，包括官网公告、博客、治理、官方账号更新。
使用 Snapshot GraphQL 获取治理，以及 CryptoPanic API (可选) 获取聚合新闻。
"""

import urllib.request
import json
import ssl
import argparse
import datetime
import os
import sys

# ── 配置 ──────────────────────────────────────────────────
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
ctx = ssl._create_unverified_context()

def get_json(url, data=None, timeout=15):
    """通用 JSON 获取函数，支持 POST"""
    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={**HEADERS, 'Content-Type': 'application/json'})
    else:
        req = urllib.request.Request(url, headers=HEADERS)
        
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {"_error": str(e)}

def fetch_snapshot_governance(space_id, limit=5):
    """从 Snapshot 获取治理提案"""
    url = "https://hub.snapshot.org/graphql"
    query = {
        "query": f"""
        query Proposals {{
          proposals (
            first: {limit},
            skip: 0,
            where: {{
              space_in: ["{space_id}"],
              state: "all"
            }},
            orderBy: "created",
            orderDirection: desc
          ) {{
            id
            title
            body
            choices
            start
            end
            snapshot
            state
            author
            space {{
              id
              name
            }}
          }}
        }}
        """
    }
    
    data = get_json(url, data=query)
    if "_error" in data:
        return []
    
    proposals = data.get("data", {}).get("proposals", [])
    results = []
    for p in proposals:
        results.append({
            "title": p.get("title"),
            "url": f"https://snapshot.org/#/{space_id}/proposal/{p.get('id')}",
            "source_type": "governance",
            "published_at": datetime.datetime.fromtimestamp(p.get("start")).isoformat(),
            "summary": p.get("body")[:200] + "..." if p.get("body") else "",
            "status": p.get("state")
        })
    return results

def fetch_cryptopanic_updates(symbol, limit=5):
    """从 CryptoPanic 获取聚合新闻 (需要 API Key，MVP 暂不强制)"""
    # 这里仅作为占位和扩展示例
    api_key = os.getenv("CRYPTOPANIC_API_KEY")
    if not api_key:
        return []
        
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={api_key}&currencies={symbol}&filter=hot"
    data = get_json(url)
    if "_error" in data:
        return []
        
    posts = data.get("results", [])
    results = []
    for p in posts[:limit]:
        results.append({
            "title": p.get("title"),
            "url": p.get("url"),
            "source_type": "news",
            "published_at": p.get("published_at"),
            "summary": "",
            "source": p.get("domain")
        })
    return results

def main():
    parser = argparse.ArgumentParser(description="聚合项目官方更新")
    parser.add_argument("--project", required=True, help="项目名称或 Symbol，如 PENDLE")
    parser.add_argument("--output", required=True, help="输出 JSON 文件路径")
    parser.add_argument("--snapshot", help="Snapshot Space ID，如 pendle.eth")
    args = parser.parse_args()

    project = args.project.upper()
    print(f"📡 Fetching official updates for: {project}...")
    
    all_updates = []
    
    # 1. 尝试获取治理提案
    snapshot_id = args.snapshot or f"{args.project.lower()}.eth"
    print(f"   Checking Snapshot: {snapshot_id}...")
    gov_updates = fetch_snapshot_governance(snapshot_id)
    all_updates.extend(gov_updates)
    
    # 2. 尝试获取聚合新闻
    print(f"   Checking News for {project}...")
    news_updates = fetch_cryptopanic_updates(project)
    all_updates.extend(news_updates)
    
    # 如果什么都没拿到，记录暂无数据，不编造
    if not all_updates:
        print(f"   ! No updates found for {project}")
    
    output_data = {
        "project": project,
        "items": all_updates,
        "timestamp": datetime.datetime.now().isoformat(),
        "count": len(all_updates)
    }

    # 写入文件
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Official updates saved to {args.output} ({len(all_updates)} items)")

if __name__ == "__main__":
    main()
