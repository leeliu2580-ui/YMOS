import urllib.request
import json
import re
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def fetch(url, timeout=10):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            content_type = r.headers.get('Content-Type', '')
            raw = r.read()
            if 'json' in content_type or url.endswith('.json'):
                return 'json', raw.decode('utf-8', errors='replace')
            else:
                text = raw.decode('utf-8', errors='replace')
                # Try to extract JSON from page
                return 'html', text
    except Exception as e:
        return 'error', str(e)

results = {}

# 1. DeFiLlama Stablecoins
print('=== 1. DeFiLlama Stablecoins ===')
url = 'https://api.llama.fi/stablecoincharts/all'
try:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
        if data:
            latest = data[-1]
            print(f"Latest: timestamp={latest.get('date')}, totalCirculatingUSD={latest.get('totalCirculatingUSD')}")
            results['defillama'] = latest
        else:
            print('No data')
except Exception as e:
    print(f'Error: {e}')

time.sleep(1)

# 2. CoinGecko categories (total market cap)
print('\n=== 2. CoinGecko Global Data ===')
url = 'https://api.coingecko.com/api/v3/global'
try:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
        gd = data.get('data', {})
        print(f"Total Market Cap: ${gd.get('total_market_cap', {}).get('usd', 0):,.0f}")
        print(f"24h Volume: ${gd.get('total_volume', {}).get('usd', 0):,.0f}")
        print(f" BTC Dominance: {gd.get('market_cap_percentage', {}).get('btc', 0):.1f}%")
        results['coingecko_global'] = gd
except Exception as e:
    print(f'Error: {e}')

time.sleep(1)

# 3. CoinGecko stablecoin data
print('\n=== 3. CoinGecko Stablecoin Data ===')
url = 'https://api.coingecko.com/api/v3/search?query=usdt'
try:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
        print(json.dumps(data, indent=2)[:500])
except Exception as e:
    print(f'Error: {e}')

time.sleep(1)

# 4. Hyperdash TOP300 long/short ratio
print('\n=== 4. Hyperdash TOP300 Long/Short ===')
url = 'https://hyperdash.com/explore/cohorts/extremely_profitable'
_, text = fetch(url)
# Look for data patterns
if 'error' not in _:
    # Try to find JSON data in page
    json_matches = re.findall(r'window\.initialState\s*=\s*({[^<]+})', text)
    if json_matches:
        print('Found initialState:', json_matches[0][:500])
    else:
        # Look for numbers
        numbers = re.findall(r'(\d+\.?\d*)', text)
        print('Text length:', len(text))
        print('First 2000 chars:', text[:2000])
else:
    print('Error:', text)

print('\nDone')
