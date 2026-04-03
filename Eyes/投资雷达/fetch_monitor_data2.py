import urllib.request
import json
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/html, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.coingecko.com/',
}

def get(url, timeout=15):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            ct = r.headers.get('Content-Type', '')
            raw = r.read()
            if 'json' in ct or 'text' in ct:
                text = raw.decode('utf-8', errors='replace')
                try:
                    return json.loads(text)
                except:
                    return text
            return raw
    except Exception as e:
        return {'error': str(e)}

results = {}

# 1. CoinGecko global data
print('=== CoinGecko Global ===')
data = get('https://api.coingecko.com/api/v3/global')
if isinstance(data, dict):
    gd = data.get('data', {})
    print('Total MCap:', f"${gd.get('total_market_cap',{}).get('usd',0):,.0f}")
    print('BTC Dom:', f"{gd.get('market_cap_percentage',{}).get('btc',0):.1f}%")
    print('ETH Dom:', f"{gd.get('market_cap_percentage',{}).get('eth',0):.1f}%")
    results['coingecko_global'] = gd
else:
    print('Result:', str(data)[:200])

time.sleep(1)

# 2. CoinGecko stablecoins (simple price for major stablecoins)
print('\n=== CoinGecko Stablecoin Total Supply ===')
# Get USDT, USDC, DAI market caps as proxy for supply
data = get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=tether,usd-coin,dai,binance-usd,gemini-dollar&order=market_cap_desc&per_page=5&page=1&sparkline=false')
if isinstance(data, list):
    total = 0
    for coin in data:
        name = coin.get('symbol','')
        mcap = coin.get('market_cap', 0)
        price = coin.get('current_price', 0)
        print(f"  {name.upper()}: mcap=${mcap:,.0f}  price=${price}")
        total += mcap
    print(f"  TOTAL Stablecoin MCap: ${total:,.0f}")
    results['stablecoins'] = total
else:
    print('Result:', str(data)[:200])

time.sleep(1)

# 3. CoinGecko BTC premium index via their API
print('\n=== CoinGecko BTC ETF Flow (estimate via premium) ===')
# CoinGecko doesn't expose ETF flow directly, but we can get funding rate proxy
# Try Binance BTCUSDT funding rate
data = get('https://api.binance.com/api/v3/premiumIndex')
if isinstance(data, list):
    for symbol in ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']:
        for item in data:
            if item.get('symbol') == symbol:
                funding = float(item.get('lastFundingRate', 0)) * 100
                print(f"  {symbol} funding rate: {funding:.4f}% (next: {item.get('nextFundingTime', 'N/A')})")
else:
    print('Result:', str(data)[:200])

time.sleep(1)

# 4. Hyperliquid API - funding rate
print('\n=== Hyperliquid Funding Rate ===')
# Try Hyperliquid's public API
data = get('https://api.hyperliquid.xyz/info', timeout=10)
if isinstance(data, dict):
    # Try to get meta info
    req_body = json.dumps({"type": "meta"}).encode()
    req = urllib.request.Request(
        'https://api.hyperliquid.xyz/info',
        data=req_body,
        headers={**HEADERS, 'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            resp = json.loads(r.read())
            print('Hyperliquid meta response:', str(resp)[:300])
    except Exception as e:
        print('Meta error:', e)
else:
    print('Result:', str(data)[:200])

time.sleep(1)

# 5. CoinGlass - try their public endpoints
print('\n=== CoinGlass ETF Data ===')
# CoinGlass has some public data
endpoints = [
    'https://api.coinglass.com/public/api/v1/bitcoin/etf/flow',
    'https://api.coinglass.com/public/api/v1/pro/trade/longShortRatio?symbol=BTC',
]
for url in endpoints:
    data = get(url)
    print(f'  URL: {url}')
    if isinstance(data, (dict, list)):
        print('  Data:', json.dumps(data, indent=2)[:500])
    else:
        print('  Result:', str(data)[:300])
    time.sleep(0.5)

# 6. DeFiLlama stablecoins
print('\n=== DeFiLlama Stablecoins ===')
data = get('https://api.llama.fi/stablecoinchart/all?stablecoin=usdt')
if isinstance(data, list) and len(data) > 0:
    print('USDT latest:', data[-1])
else:
    print('Trying alternative...')
    data = get('https://api.llama.fi/stablecoinchart/Tether')
    if isinstance(data, list) and len(data) > 0:
        print('Tether:', data[-1])
    else:
        print('Result:', str(data)[:200])

print('\n=== All done ===')
