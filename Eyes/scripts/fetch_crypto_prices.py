#!/usr/bin/env python3
"""
Eyes/scripts/fetch_crypto_prices.py
抓取加密标的价格快照，输出结构化 JSON。
"""

import urllib.request
import urllib.parse
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

def fetch_coingecko_prices(symbols, vs_currencies="usd"):
    """使用 CoinGecko Simple Price API 获取价格"""
    # 将 symbol 转换为 CoinGecko ID (简化处理：常用 symbol 映射)
    # 注意：真实环境建议使用 CoinGecko Pro 或维护完整的 symbol->id 映射表
    symbol_to_id = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "PENDLE": "pendle",
        "HYPE": "hyperliquid", # 假设映射
        "ENA": "ethena",
        "SOL": "solana",
    }
    
    ids = []
    id_to_symbol = {}
    for s in symbols:
        sid = symbol_to_id.get(s.upper(), s.lower())
        ids.append(sid)
        id_to_symbol[sid] = s.upper()
    
    ids_str = ",".join(ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies={vs_currencies}&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
    
    data = get_json(url)
    if "_error" in data:
        return data
    
    result = {}
    for sid, info in data.items():
        sym = id_to_symbol.get(sid, sid.upper())
        result[sym] = {
            "price_usd": info.get("usd", 0),
            "change_24h": info.get("usd_24h_change", 0),
            "market_cap": info.get("usd_market_cap", 0),
            "volume_24h": info.get("usd_24h_vol", 0),
            "source": "CoinGecko"
        }
    return result

def main():
    parser = argparse.ArgumentParser(description="抓取加密标的价格快照")
    parser.add_argument("--symbols", required=True, help="逗号分隔的标的，如 PENDLE,BTC,ETH")
    parser.add_argument("--vs", default="btc,eth", help="相对强弱比较的基准，如 btc,eth")
    parser.add_argument("--output", required=True, help="输出 JSON 文件路径")
    args = parser.parse_args()

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    vs_bases = [v.strip().upper() for v in args.vs.split(",") if v.strip()]
    
    # 确保基准也在查询列表中
    query_symbols = list(set(symbols + vs_bases))
    
    print(f"📡 Fetching prices for: {query_symbols}...")
    prices = fetch_coingecko_prices(query_symbols)
    
    if "_error" in prices:
        print(f"❌ Error fetching prices: {prices['_error']}")
        # 记录错误到输出文件
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump({"success": False, "error": prices["_error"]}, f, indent=2)
        sys.exit(1)

    output_data = []
    timestamp = datetime.datetime.now().isoformat()
    
    for sym in symbols:
        if sym not in prices:
            # 记录缺失数据，不编造
            output_data.append({
                "symbol": sym,
                "price_usd": None,
                "status": "暂无数据",
                "timestamp": timestamp
            })
            continue
            
        p_info = prices[sym]
        item = {
            "symbol": sym,
            "price_usd": p_info["price_usd"],
            "change_24h": p_info["change_24h"],
            "market_cap": p_info["market_cap"],
            "volume_24h": p_info["volume_24h"],
            "timestamp": timestamp,
            "source": p_info["source"]
        }
        
        # 计算相对强弱
        for base in vs_bases:
            if base in prices and prices[base]["price_usd"] > 0 and p_info["price_usd"] > 0:
                # 简单计算：(价格/基准价格) 的 24h 变化差异
                # 或者直接记录 24h change 的差值
                strength = p_info["change_24h"] - prices[base]["change_24h"]
                item[f"vs_{base.lower()}_strength"] = strength
            else:
                item[f"vs_{base.lower()}_strength"] = None
        
        output_data.append(item)

    # 写入文件
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Prices saved to {args.output}")

if __name__ == "__main__":
    main()
