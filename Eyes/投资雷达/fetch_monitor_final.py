import urllib.request
import json
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/html, */*',
}

def get(url, timeout=15):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return json.loads(raw.decode('utf-8', errors='replace'))
    except Exception as e:
        return {'error': str(e)}

def post(url, body, headers=None, timeout=15):
    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    if headers:
        h.update(headers)
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers=h
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return {'error': str(e)}

results = {}

# =============================================
# 1. CoinCap - BTC price + market data
# =============================================
print('=== CoinCap BTC Data ===')
data = get('https://api.coincap.io/v2/assets/bitcoin')
if 'error' not in data:
    btc = data.get('data', {})
    price = float(btc.get('priceUsd', 0))
    mcap = float(btc.get('marketCapUsd', 0))
    vol24h = float(btc.get('volumeUsd24Hr', 0))
    change24h = float(btc.get('changePercent24Hr', 0))
    supply = float(btc.get('supply', 0))
    print(f"  Price: ${price:,.2f}")
    print(f"  Market Cap: ${mcap/1e12:.3f}T")
    print(f"  24h Volume: ${vol24h/1e9:.3f}B")
    print(f"  24h Change: {change24h:.2f}%")
    print(f"  Supply: {supply/1e6:.2f}M BTC")
    results['btc'] = {'price': price, 'mcap': mcap, 'vol24h': vol24h, 'change24h': change24h}
else:
    print('Error:', data)

time.sleep(0.5)

# =============================================
# 2. CoinCap - ETH price
# =============================================
print('\n=== CoinCap ETH Data ===')
data = get('https://api.coincap.io/v2/assets/ethereum')
if 'error' not in data:
    eth = data.get('data', {})
    price = float(eth.get('priceUsd', 0))
    mcap = float(eth.get('marketCapUsd', 0))
    change24h = float(eth.get('changePercent24Hr', 0))
    print(f"  Price: ${price:,.2f}")
    print(f"  Market Cap: ${mcap/1e9:.3f}B")
    print(f"  24h Change: {change24h:.2f}%")
    results['eth'] = {'price': price, 'mcap': mcap, 'change24h': change24h}
else:
    print('Error:', data)

time.sleep(0.5)

# =============================================
# 3. CoinCap - Stablecoins (USDT, USDC, DAI)
# =============================================
print('\n=== CoinCap Stablecoins ===')
stablecoins = ['tether', 'usd-coin', 'dai']
total_stablecap = 0
for sc in stablecoins:
    data = get(f'https://api.coincap.io/v2/assets/{sc}')
    if 'error' not in data:
        coin = data.get('data', {})
        mcap = float(coin.get('marketCapUsd', 0))
        price = float(coin.get('priceUsd', 0))
        print(f"  {coin.get('symbol', sc)}: mcap=${mcap/1e9:.3f}B  price=${price:.4f}")
        total_stablecap += mcap
    time.sleep(0.3)
print(f"  Total (top3): ${total_stablecap/1e9:.3f}B")
results['stablecoins_top3'] = total_stablecap

time.sleep(0.5)

# =============================================
# 4. CoinCap - Global data
# =============================================
print('\n=== CoinCap Global Data ===')
data = get('https://api.coincap.io/v2/global')
if 'error' not in data:
    glb = data.get('data', {})
    mcap = float(glb.get('marketCapUsd', 0))
    vol24h = float(glb.get('volumeUsd24Hr', 0))
    btc_dom = float(glb.get('bitcoinDominance', 0))
    eth_dom = float(glb.get('etherumDominance', 0))
    print(f"  Total MCap: ${mcap/1e12:.3f}T")
    print(f"  24h Volume: ${vol24h/1e9:.2f}B")
    print(f"  BTC Dom: {btc_dom:.1f}%")
    print(f"  ETH Dom: {eth_dom:.1f}%")
    results['global'] = {'mcap': mcap, 'vol24h': vol24h, 'btc_dom': btc_dom}
else:
    print('Error:', data)

time.sleep(0.5)

# =============================================
# 5. Hyperliquid - BTC funding (correct format)
# =============================================
print('\n=== Hyperliquid BTC Funding Rate ===')
hl_url = 'https://api.hyperliquid.xyz/info'

# Try the correct body format for ticker
body = {"type": "ticker", "coin": "BTC"}
data = post(hl_url, body)
if 'error' not in data:
    ticker = data.get('data', {}) if isinstance(data, dict) else data
    fr = ticker.get('fundingRate', 'N/A')
    oi = ticker.get('openInterest', 'N/A')
    prev_fr = ticker.get('prevFundingRate', 'N/A')
    print(f"  BTC Funding Rate: {fr}")
    print(f"  BTC Open Interest: {oi}")
    print(f"  BTC Prev Funding Rate: {prev_fr}")
    print(f"  Full ticker:", json.dumps(ticker, indent=2)[:500])
    results['hl_btc'] = {'fundingRate': fr, 'openInterest': oi, 'prevFundingRate': prev_fr}
else:
    print('HL Error:', data)

time.sleep(0.5)

body = {"type": "ticker", "coin": "ETH"}
data = post(hl_url, body)
if 'error' not in data:
    ticker = data.get('data', {}) if isinstance(data, dict) else data
    fr = ticker.get('fundingRate', 'N/A')
    oi = ticker.get('openInterest', 'N/A')
    print(f"  ETH Funding Rate: {fr}")
    print(f"  ETH Open Interest: {oi}")
    results['hl_eth'] = {'fundingRate': fr, 'openInterest': oi}
else:
    print('HL ETH Error:', data)

time.sleep(0.5)

# =============================================
# 6. Try Deribit BTC price + funding (for reference)
# =============================================
print('\n=== Summary ===')
print('BTC Price:   ', results.get('btc', {}).get('price', 'N/A'))
print('BTC 24h Chg: ', results.get('btc', {}).get('change24h', 'N/A'))
print('BTC MCap:    ', results.get('btc', {}).get('mcap', 'N/A'))
print('Total Stable:', results.get('stablecoins_top3', 'N/A'))
print('Global MCap: ', results.get('global', {}).get('mcap', 'N/A'))
print('HL BTC FR:   ', results.get('hl_btc', {}).get('fundingRate', 'N/A'))
print('HL ETH FR:   ', results.get('hl_eth', {}).get('fundingRate', 'N/A'))
