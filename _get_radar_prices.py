#!/usr/bin/env python3
"""Fetch current crypto prices for radar and insight reports."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import urllib.request
import urllib.error

def fetch_hyperliquid_btc():
    try:
        req = urllib.request.Request(
            'https://api.hyperliquid.xyz/info',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({"type": "trades", "coin": "BTC"}).encode()
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            trades = data.get('trades', [])
            if trades:
                return float(trades[0]['px'])
    except Exception as e:
        print(f'HL BTC error: {e}', file=sys.stderr)
    return None

def fetch_coingecko_markets():
    try:
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,hyperliquid&order=market_cap_desc&per_page=3&price_change_percentage=24h'
        req = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            return {c['id']: {'price': c['current_price'], 'change_24h': c.get('price_change_percentage_24h', 0)} for c in data}
    except Exception as e:
        print(f'CG markets error: {e}', file=sys.stderr)
    return {}

def fetch_fear_greed():
    try:
        url = 'https://api.alternative.me/fng/?limit=1'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            if data.get('data'):
                return int(data['data'][0]['value']), data['data'][0]['value_classification']
    except Exception as e:
        print(f'FG error: {e}', file=sys.stderr)
    return None, None

results = {}

# BTC from Hyperliquid
hl_btc = fetch_hyperliquid_btc()
if hl_btc:
    results['BTC_HL'] = hl_btc

# From CoinGecko
cg = fetch_coingecko_markets()
if cg:
    results['CG'] = cg

# Fear & Greed
fg_val, fg_cls = fetch_fear_greed()
if fg_val:
    results['FearGreed'] = {'value': fg_val, 'classification': fg_cls}

print(json.dumps(results, indent=2, ensure_ascii=False))
