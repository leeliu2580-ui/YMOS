#!/usr/bin/env python3
"""Fetch A-share prices via Yahoo Finance for insight report."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json, urllib.request, urllib.error

def fetch_yahoo_price(symbol):
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            result = data['chart']['result'][0]
            meta = result['meta']
            closes = result['indicators']['quote'][0]['close']
            # Get last 2 closes
            c1 = closes[-1] if closes[-1] is not None else 0
            c2 = closes[-2] if len(closes) > 1 and closes[-2] is not None else c1
            change = (c1 - c2) / c2 * 100 if c2 > 0 else 0
            return {'symbol': symbol, 'price': round(c1, 2), 'change_pct': round(change, 2)}
    except Exception as e:
        return {'symbol': symbol, 'error': str(e)}

symbols = ['600000.SS', '000001.SZ', '000300.SS']
for s in symbols:
    result = fetch_yahoo_price(s)
    if 'error' not in result:
        print(f"{result['symbol']}: {result['price']} ({result['change_pct']:+.2f}%)")
    else:
        print(f"{s}: ERROR {result['error']}")