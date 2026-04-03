import urllib.request
import json
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

def post(url, body, timeout=15):
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers=HEADERS
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return {'error': str(e)}

# 1. Hyperliquid - BTC and ETH funding rate
print('=== Hyperliquid Funding Rates ===')
url = 'https://api.hyperliquid.xyz/info'

# Get all funding rates for BTC and ETH
body = {"type": "fundingRate", "coins": ["BTC", "ETH"]}
data = post(url, body)
print('Funding rates response:', json.dumps(data, indent=2)[:800] if isinstance(data, dict) else str(data)[:300])

time.sleep(0.5)

# Get recent candlesticks to infer market structure
print('\n=== Hyperliquid BTC Recent Candles ===')
body = {
    "type": "candleSnapshot",
    "req": {
        "coin": "BTC",
        "interval": "1d",
        "startTime": 1743034800,  # approx March 2026
        "endTime": 1745284800     # approx April 2026
    }
}
data = post(url, body)
if isinstance(data, dict) and 'data' in data:
    candles = data['data'].get('candle', {})
    print('BTC candles:', json.dumps(candles, indent=2)[:600])
elif isinstance(data, dict) and 'error' in data:
    print('Error:', data['error'])
else:
    print('Response:', str(data)[:500])

time.sleep(0.5)

# 2. Get Hyperliquid BTC open interest / market data
print('\n=== Hyperliquid BTC Market Meta ===')
body = {"type": "ticker", "coin": "BTC"}
data = post(url, body)
if isinstance(data, dict) and 'data' in data:
    ticker = data['data']
    print('Funding rate:', ticker.get('fundingRate'))
    print('Open interest:', ticker.get('openInterest'))
    print('Prev funding rate:', ticker.get('prevFundingRate'))
else:
    print('Response:', str(data)[:500])

time.sleep(0.5)

# 3. ETH
body = {"type": "ticker", "coin": "ETH"}
data = post(url, body)
if isinstance(data, dict) and 'data' in data:
    ticker = data['data']
    print('\nETH Funding rate:', ticker.get('fundingRate'))
    print('ETH Open interest:', ticker.get('openInterest'))
else:
    print('Response:', str(data)[:500])

time.sleep(0.5)

# 4. Try Binance for funding rate
print('\n=== Binance BTC Funding Rate ===')
url2 = 'https://fapi.binance.com/fapi/v1/premiumIndex'
req = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
        for item in data:
            if item['symbol'] in ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']:
                fr = float(item.get('lastFundingRate', 0)) * 100
                next_fund = item.get('nextFundingTime', 'N/A')
                print(f"  {item['symbol']}: funding={fr:.4f}%  next={next_fund}")
except Exception as e:
    print('Binance error:', e)

time.sleep(0.5)

# 5. Try CoinGecko global via different approach
print('\n=== CoinGecko Global (via coingecko.com) ===')
url3 = 'https://www.coingecko.com/en'
req = urllib.request.Request(url3, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html',
    'Accept-Language': 'en-US,en;q=0.9'
})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        text = r.read().decode('utf-8', errors='replace')
        # Look for market cap data in page
        import re
        # Find btc_dominance
        match = re.search(r'"btc_dominance"[:\s]*([0-9.]+)', text)
        if match:
            print(f'  BTC Dominance: {match.group(1)}%')
        match2 = re.search(r'"total_market_cap"[:\s]*{[^}]*"usd"[:\s]*([0-9.]+)', text)
        if match2:
            print(f'  Total MCap: ${float(match2.group(1))/1e12:.2f}T')
        match3 = re.search(r'"total_volume"[:\s]*{[^}]*"usd"[:\s]*([0-9.]+)', text)
        if match3:
            print(f'  24h Volume: ${float(match3.group(1))/1e9:.2f}B')
        if not match and not match2:
            print('  Page length:', len(text))
            print('  First 500:', text[:500])
except Exception as e:
    print('CoinGecko error:', e)

print('\n=== Done ===')
