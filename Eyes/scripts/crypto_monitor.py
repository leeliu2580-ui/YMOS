#!/usr/bin/env python3
"""
Eyes/scripts/crypto_monitor.py
Daily auto-run: 00:00 / 08:00 / 16:00 (CST)
Sources: CoinGecko API + Binance API + Hyperliquid Info API
Output: Eyes/监控数据/YYYY-MM/crypto_monitor_YYYYMMDD_HHMM.md
"""

import urllib.request, json, ssl, os, datetime

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
ctx = ssl._create_unverified_context()

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
date_str = now.strftime('%Y-%m-%d')
time_str = now.strftime('%H:%M')
ym = now.strftime('%Y-%m')
output_dir = f'Eyes/监控数据/{ym}'
os.makedirs(output_dir, exist_ok=True)

def get(url, timeout=12):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return json.loads(r.read().decode('utf-8', errors='replace'))
    except Exception as e:
        return {'_error': str(e)}

def post(url, body, timeout=12):
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers={**HEADERS, 'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return json.loads(r.read().decode('utf-8', errors='replace'))
    except Exception as e:
        return {'_error': str(e)}

def fetch_coingecko_global():
    d = get('https://api.coingecko.com/api/v3/global')
    if '_error' in d:
        return {}
    gd = d.get('data', {})
    return {
        'tmc': gd.get('total_market_cap', {}).get('usd', 0),
        'vol': gd.get('total_volume', {}).get('usd', 0),
        'btc_dom': gd.get('market_cap_percentage', {}).get('btc', 0),
        'eth_dom': gd.get('market_cap_percentage', {}).get('eth', 0),
    }

def fetch_stablecoins():
    data = get('https://api.coingecko.com/api/v3/coins/categories')
    if '_error' in data:
        return {}, 0
    usd_mcap = 0
    total_mcap = 0
    for cat in data:
        name = cat.get('name', '')
        mcap = cat.get('market_cap', 0) or 0
        if name == 'USD Stablecoin':
            usd_mcap = mcap
        if 'stablecoin' in name.lower() and mcap > 0:
            total_mcap += mcap
    return {'usd': usd_mcap, 'total': total_mcap}, total_mcap

def fetch_stablecoin_markets():
    ids = 'tether,usd-coin,dai,binance-usd'
    url = (
        f'https://api.coingecko.com/api/v3/coins/markets'
        f'?vs_currency=usd&ids={ids}&order=market_cap_desc'
        f'&per_page=4&page=1&sparkline=false&price_change_percentage=24h'
    )
    data = get(url)
    if '_error' in data:
        return []
    result = []
    for c in data:
        result.append({
            'name': c.get('name', ''),
            'symbol': c.get('symbol', '').upper(),
            'price': c.get('current_price') or 0,
            'mcap': c.get('market_cap') or 0,
            'chg': c.get('price_change_percentage_24h') or 0,
        })
    return result

def fetch_coingecko_prices():
    """Get BTC/ETH prices from CoinGecko markets (fallback + primary)."""
    url = (
        'https://api.coingecko.com/api/v3/coins/markets'
        '?vs_currency=usd&ids=bitcoin,ethereum&order=market_cap_desc'
        '&per_page=2&page=1&sparkline=false&price_change_percentage=24h'
    )
    data = get(url)
    result = {}
    if '_error' not in data and isinstance(data, list):
        for c in data:
            sym = c.get('symbol', '').upper()
            label = {'btc': 'BTC', 'eth': 'ETH'}.get(c.get('id', ''), sym)
            result[label] = {
                'price': c.get('current_price') or 0,
                'chg': c.get('price_change_percentage_24h') or 0,
                'high': c.get('high_24h') or 0,
                'low': c.get('low_24h') or 0,
            }
    return result
def fetch_binance_funding():
    result = {}
    for sym, label in [('BTCUSDT', 'BTC'), ('ETHUSDT', 'ETH'), ('SOLUSDT', 'SOL')]:
        d = get(f'https://fapi.binance.com/fapi/v1/premiumIndex?symbol={sym}')
        if '_error' not in d:
            fr = float(d.get('lastFundingRate') or 0) * 100
            result[label] = {
                'fr': fr,
                'signal': 'Long pays Short (bullish)' if fr > 0.01 else 'Short pays Long (bearish)' if fr < -0.01 else 'Neutral',
            }
    return result

def fetch_hl_trades():
    data = post('https://api.hyperliquid.xyz/info', {'type': 'recentTrades', 'coin': 'BTC'})
    if '_error' in data or not isinstance(data, list):
        return []
    trades = []
    for t in data[:5]:
        ts = int(t.get('time', 0)) // 1000
        dt = datetime.datetime.fromtimestamp(ts, datetime.timezone(datetime.timedelta(hours=8)))
        side = t.get('side', '')
        trades.append({
            'time': dt.strftime('%H:%M:%S'),
            'side': 'B (Buy)' if side == 'B' else 'S (Sell)',
            'price': float(t.get('px') or 0),
            'size': float(t.get('sz') or 0),
        })
    return trades

def main():
    print(f'[{date_str} {time_str}] Fetching crypto data...')

    print('  [1/6] CoinGecko Global...')
    g = fetch_coingecko_global()

    print('  [2/6] CoinGecko Categories...')
    sc_cat, _ = fetch_stablecoins()

    print('  [3/6] CoinGecko Markets...')
    sc_mkts = fetch_stablecoin_markets()

    print('  [4/6] CoinGecko BTC/ETH prices...')
    spot = fetch_coingecko_prices()

    print('  [5/6] Binance Funding...')
    funding = fetch_binance_funding()

    print('  [6/6] Hyperliquid Trades...')
    hl = fetch_hl_trades()

    tmc = g.get('tmc', 0)
    btc_dom = g.get('btc_dom', 0)
    eth_dom = g.get('eth_dom', 0)
    usd_sc = sc_cat.get('usd', 0)
    btc = spot.get('BTC', {})
    eth = spot.get('ETH', {})
    btc_price = btc.get('price', 0)
    eth_price = eth.get('price', 0)

    stable_rows = '\n'.join([
        f"| {c['name']} | {c['symbol']} | ${c['mcap']/1e9:.2f}B | ${c['price']:.4f} | {c['chg']:+.3f}% |"
        for c in sc_mkts
    ])

    fund_rows = '\n'.join([
        f"| {l} | {fd['fr']:+.4f}% | {fd['signal']} |"
        for l, fd in funding.items()
    ])

    trade_rows = '\n'.join([
        f"| {t['time']} | {t['side']} | ${t['price']:,.2f} | {t['size']:.5f} |"
        for t in hl
    ]) or '| - | - | - | - |'

    report = f"""# Crypto Market Monitor

> **Time:** {date_str} {time_str} (CST)
> **Sources:** CoinGecko API + Binance API + Hyperliquid Info API
> **Schedule:** 00:00 / 08:00 / 16:00 CST daily

---

## Market Cap Overview

| Metric | Value |
|:---|---:|
| **Total MCap** | **${tmc/1e12:.2f}T** |
| BTC Dominance | {btc_dom:.1f}% |
| ETH Dominance | {eth_dom:.1f}% |

---

## USD Stablecoin Market Cap

| Metric | Value |
|:---|---:|
| USD Stablecoins | ${usd_sc/1e9:.2f}B |

### Stablecoin Details

| Name | Symbol | MCap | Price | 24h |
|:---|:---|---:|---:|---:|
{stable_rows}

---

## Spot Prices (Binance)

| Asset | Price | 24h Change | Range |
|:---|---:|---:|---:|
| **BTC** | **${btc_price:,.2f}** | {btc.get('chg', 0):+.2f}% | ${btc.get('low', 0):,.2f} ~ ${btc.get('high', 0):,.2f} |
| **ETH** | **${eth_price:,.2f}** | {eth.get('chg', 0):+.2f}% | ${eth.get('low', 0):,.2f} ~ ${eth.get('high', 0):,.2f} |

---

## Funding Rates (Binance Futures)

| Asset | Funding Rate | Interpretation |
|:---|---:|:---|
{fund_rows}

> Positive = Long pays Short (market is long-biased). Negative = Short pays Long (bearish bias). |rate| < 0.01% is noise.

---

## Hyperliquid BTC Recent Trades

| Time | Side | Price | Size |
|:---:|:---:|---:|---:|
{trade_rows}

---

## Quick Summary

- **Total MCap:** ${tmc/1e12:.2f}T | BTC {btc_dom:.1f}% / ETH {eth_dom:.1f}%
- **Stablecoins:** ${usd_sc/1e9:.2f}B
- **BTC:** ${btc_price:,.0f} ({btc.get('chg',0):+.2f}%)
- **ETH:** ${eth_price:,.0f} ({eth.get('chg',0):+.2f}%)

---
*Auto-generated by Eyes/scripts/crypto_monitor.py | {date_str} {time_str}*
"""

    out_file = os.path.join(output_dir, f'crypto_monitor_{date_str.replace("-","")}_{time_str.replace(":","")}.md')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f'[OK] Saved: {out_file}')
    print(f'[{date_str} {time_str}] SNAPSHOT')
    print(f'  Total MCap:  ${tmc/1e12:.2f}T')
    print(f'  Stablecoins: ${usd_sc/1e9:.2f}B')
    print(f'  BTC:         ${btc_price:,.0f} ({btc.get("chg",0):+.2f}%)')
    print(f'  ETH:         ${eth_price:,.0f} ({eth.get("chg",0):+.2f}%)')

    return report

if __name__ == '__main__':
    main()
