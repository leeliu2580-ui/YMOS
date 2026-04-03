import urllib.request, json, ssl
ctx = ssl._create_unverified_context()

# Task F: The Block Beats
print('=== Task F: The Block Beats ===')
urls = [
    'http://www.theblockbeats.info/api/market/global',
    'http://api.theblockbeats.info/v1/market/data',
    'https://www.theblockbeats.info/zh/market-data',
    'https://data.theblockbeats.info/feeds/market',
]
for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=8, context=ctx) as r:
            raw = r.read()
            text = raw.decode('utf-8', errors='replace')
            print('OK: ' + url + ' -> ' + text[:200])
    except Exception as e:
        print('Fail: ' + url + ' -> ' + str(e)[:80])

# Task D: Hyperliquid - try GET endpoints
print()
print('=== Task D: Hyperliquid GET ===')
hl_urls = [
    'https://api.hyperliquid.xyz/funding',
    'https://api.hyperliquid.xyz/info/funding',
    'https://api.hyperliquid.xyz/v1/funding',
]
for url in hl_urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=8, context=ctx) as r:
            data = json.loads(r.read())
            print('OK: ' + url + ' -> ' + str(data)[:200])
    except Exception as e:
        print('Fail: ' + url + ' -> ' + str(e)[:80])

# Binance BTC Funding (known working)
print()
print('=== Binance BTC Funding ===')
url = 'https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=8) as r:
        data = json.loads(r.read())
        fr = float(data.get('lastFundingRate', 0)) * 100
        nt = data.get('nextFundingTime', 'N/A')
        print('BTC Funding: ' + str(round(fr, 4)) + '%  next: ' + str(nt))
except Exception as e:
    print('Error: ' + str(e))

print('Done')
