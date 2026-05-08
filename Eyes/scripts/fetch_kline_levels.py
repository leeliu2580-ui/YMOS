#!/usr/bin/env python3
"""
Eyes/scripts/fetch_kline_levels.py
生成 K 线关键位和结构判断所需的结构化数据。
使用 Binance 公开接口获取 OHLCV 并计算基础位。
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

def analyze_kline(symbol, interval="1d", limit=30):
    """从 Binance 获取 K 线并分析支撑阻力"""
    # 归一化 symbol (例如 BTC -> BTCUSDT)
    binance_sym = symbol.upper()
    if not binance_sym.endswith("USDT") and binance_sym not in ["USDC", "DAI"]:
        binance_sym += "USDT"
        
    url = f"https://api.binance.com/api/v3/klines?symbol={binance_sym}&interval={interval}&limit={limit}"
    
    data = get_json(url)
    if "_error" in data:
        return data
    
    # Binance K 线数据结构:
    # [ [open_time, open, high, low, close, vol, close_time, ...], ... ]
    closes = [float(x[4]) for x in data]
    highs = [float(x[2]) for x in data]
    lows = [float(x[3]) for x in data]
    current_price = closes[-1]
    
    # 简单计算支撑/阻力 (过去 N 天的最高/最低，以及成交密集区占位)
    # 这里使用简化逻辑：
    range_high = max(highs)
    range_low = min(lows)
    
    # 趋势判断 (简单 20 日均线或价格位置)
    ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else sum(closes) / len(closes)
    
    if current_price > ma20 * 1.05:
        trend_state = "uptrend"
    elif current_price < ma20 * 0.95:
        trend_state = "downtrend"
    else:
        trend_state = "range"
        
    # 提取最近的局部高低点作为支撑阻力
    support_levels = sorted(list(set([round(range_low, 4), round(min(lows[-7:]), 4)])))
    resistance_levels = sorted(list(set([round(range_high, 4), round(max(highs[-7:]), 4)])))

    return {
        "symbol": symbol.upper(),
        "timeframe": interval,
        "current_price": current_price,
        "support_levels": support_levels,
        "resistance_levels": resistance_levels,
        "trend_state": trend_state,
        "range_high": range_high,
        "range_low": range_low,
        "source": "Binance"
    }

def main():
    parser = argparse.ArgumentParser(description="生成 K 线关键位快照")
    parser.add_argument("--symbols", required=True, help="逗号分隔的标的，如 PENDLE,BTC")
    parser.add_argument("--output", required=True, help="输出 JSON 文件路径")
    parser.add_argument("--interval", default="1d", help="K 线周期，默认 1d")
    args = parser.parse_args()

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    
    print(f"📡 Analyzing K-lines for: {symbols}...")
    
    output_data = []
    timestamp = datetime.datetime.now().isoformat()
    
    for sym in symbols:
        k_data = analyze_kline(sym, args.interval)
        
        if "_error" in k_data:
            print(f"⚠️ Error analyzing K-line for {sym}: {k_data['_error']}")
            output_data.append({
                "symbol": sym,
                "status": "分析失败",
                "error": k_data["_error"],
                "timestamp": timestamp
            })
            continue
            
        k_data["timestamp"] = timestamp
        output_data.append(k_data)

    # 写入文件
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ K-line levels saved to {args.output}")

if __name__ == "__main__":
    main()
