#!/usr/bin/env python3
"""
Eyes/scripts/fetch_tvl_metrics.py
抓取协议 TVL 及相关指标快照。
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

def get_json(url, timeout=15):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {"_error": str(e)}

def fetch_defillama_tvl(protocol_slug):
    """从 DeFiLlama 获取协议 TVL 详情"""
    # 转换名称为 slug (简化处理)
    slug = protocol_slug.lower().replace(" ", "-")
    url = f"https://api.llama.fi/protocol/{slug}"
    
    data = get_json(url)
    if "_error" in data:
        return data
    
    # 提取关键指标
    # DeFiLlama 详情接口返回的 'tvl' 字段在某些情况下可能是历史数据列表
    # 而最新的 TVL 通常在列表的最后一项，或者有一个单独的字段
    tvl_field = data.get("tvl", 0)
    if isinstance(tvl_field, list) and len(tvl_field) > 0:
        current_tvl = tvl_field[-1].get("totalLiquidityUSD", 0)
    elif isinstance(tvl_field, (int, float)):
        current_tvl = tvl_field
    else:
        current_tvl = 0
    
    # 计算变化 (DeFiLlama 返回历史数据点，我们需要手动计算或从概览接口拿)
    # 为了简化，这里先从详情拿当前 TVL 和链分布
    chain_tvls = data.get("chainTvls", {})
    chains = {}
    for k, v in chain_tvls.items():
        if isinstance(v, dict):
            chains[k] = v.get("tvl", 0)
        else:
            chains[k] = v
    
    # 获取池子 (如果接口提供)
    # DeFiLlama /protocol/{slug} 接口返回的数据结构中包含 tokens 和 pools
    pools = []
    # 简化处理：记录前几个主要链的 TVL 作为 main_pools 占位
    for c_name, c_tvl in sorted(chains.items(), key=lambda x: x[1] if isinstance(x[1], (int, float)) else 0, reverse=True)[:3]:
        pools.append({"name": c_name, "tvl": c_tvl})
        
    return {
        "protocol": data.get("name", protocol_slug),
        "tvl_usd": current_tvl,
        "tvl_change_1d": data.get("change_1d", 0), # 详情接口可能不直接给，需要从概览拿
        "tvl_change_7d": data.get("change_7d", 0),
        "chain_breakdown": chains,
        "main_pools": pools,
        "source": "DeFiLlama"
    }

def fetch_defillama_summary(slugs):
    """从 DeFiLlama 概览列表获取变化率"""
    url = "https://api.llama.fi/protocols"
    all_data = get_json(url)
    if "_error" in all_data:
        return {}
    
    summary = {}
    slug_set = set(slugs)
    for p in all_data:
        p_slug = p.get("slug")
        if p_slug in slug_set:
            summary[p_slug] = {
                "change_1d": p.get("change_1d", 0),
                "change_7d": p.get("change_7d", 0)
            }
    return summary

def main():
    parser = argparse.ArgumentParser(description="抓取协议 TVL 指标快照")
    parser.add_argument("--protocols", required=True, help="逗号分隔的协议 Slug，如 pendle,ethena")
    parser.add_argument("--output", required=True, help="输出 JSON 文件路径")
    args = parser.parse_args()

    protocol_list = [p.strip().lower() for p in args.protocols.split(",") if p.strip()]
    
    print(f"📡 Fetching TVL for: {protocol_list}...")
    
    # 先拿概览数据获取变化率
    summaries = fetch_defillama_summary(protocol_list)
    
    output_data = []
    timestamp = datetime.datetime.now().isoformat()
    
    for slug in protocol_list:
        p_data = fetch_defillama_tvl(slug)
        
        if "_error" in p_data:
            print(f"⚠️ Error fetching TVL for {slug}: {p_data['_error']}")
            output_data.append({
                "protocol": slug,
                "tvl_usd": None,
                "status": "获取失败",
                "timestamp": timestamp
            })
            continue
            
        # 补全变化率
        if slug in summaries:
            p_data["tvl_change_1d"] = summaries[slug]["change_1d"]
            p_data["tvl_change_7d"] = summaries[slug]["change_7d"]
            
        p_data["timestamp"] = timestamp
        output_data.append(p_data)

    # 写入文件
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ TVL metrics saved to {args.output}")

if __name__ == "__main__":
    main()
