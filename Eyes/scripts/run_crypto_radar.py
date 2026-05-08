#!/usr/bin/env python3
"""
Eyes/scripts/run_crypto_radar.py
读取加密观察清单，批量执行当天的观察流程。
"""

import os
import sys
import datetime
import subprocess
import re

# ── 配置 ──────────────────────────────────────────────────
WATCHLIST_PATH = os.path.join("持仓与关注", "加密观察清单.md")
BASE_DIR = os.getcwd()

def parse_watchlist(path):
    """解析 Markdown 表格中的 Ticker"""
    if not os.path.exists(path):
        print(f"❌ Watchlist not found at {path}")
        return []
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配表格行中的 Ticker (假设第二列是 Ticker)
    # | 名称 | Ticker | 类型 | ... |
    # |:---|:---|:---|:---|
    # | PENDLE | PENDLE | 持仓 | ... |
    tickers = []
    lines = content.split('\n')
    for line in lines:
        if '|' in line and not line.strip().startswith('|:'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 2 and parts[2].isupper():
                tickers.append(parts[2])
    return list(set(tickers))

def run_command(cmd):
    print(f"🚀 Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        return False

def main():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    month = datetime.datetime.now().strftime("%Y-%m")
    
    # 解析清单
    tickers = parse_watchlist(WATCHLIST_PATH)
    if not tickers:
        print("⚠️ No tickers found in watchlist.")
        return

    print(f"📊 Crypto Radar started for: {tickers}")
    
    # 创建目录
    dirs = [
        f"Eyes/价格与TVL/{month}",
        f"Eyes/官方信息/{month}",
        f"Eyes/K线观察/{month}",
        f"Eyes/价格与TVL/Raw_Data/{month}",
        f"Eyes/官方信息/Raw_Data/{month}",
        f"Eyes/K线观察/Raw_Data/{month}",
        f"Brain/加密策略分析/{month}/Raw_Data"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    for ticker in tickers:
        print(f"\n--- Processing {ticker} ---")
        
        # 1. 价格
        price_out = f"Eyes/价格与TVL/Raw_Data/{month}/price_{ticker}_{today}.json"
        run_command(f"python Eyes/scripts/fetch_crypto_prices.py --symbols {ticker},BTC,ETH --output {price_out}")
        
        # 2. TVL
        tvl_out = f"Eyes/价格与TVL/Raw_Data/{month}/tvl_{ticker}_{today}.json"
        run_command(f"python Eyes/scripts/fetch_tvl_metrics.py --protocols {ticker.lower()} --output {tvl_out}")
        
        # 3. K线
        kline_out = f"Eyes/K线观察/Raw_Data/{month}/kline_{ticker}_{today}.json"
        run_command(f"python Eyes/scripts/fetch_kline_levels.py --symbols {ticker} --output {kline_out}")
        
        # 4. 官方
        official_out = f"Eyes/官方信息/Raw_Data/{month}/official_{ticker}_{today}.json"
        run_command(f"python Eyes/scripts/fetch_official_updates.py --project {ticker} --output {official_out}")
        
        # 5. 聚合
        unified_out = f"Brain/加密策略分析/{month}/Raw_Data/snapshot_{ticker}_{today}.json"
        run_command(f"python Eyes/scripts/build_project_snapshot.py --project {ticker} --price {price_out} --tvl {tvl_out} --official {official_out} --kline {kline_out} --output {unified_out}")

    print(f"\n✅ Crypto Radar completed for {today}")

if __name__ == "__main__":
    main()
