import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}

# =============================================
# 1. Binance BTC Price
# =============================================
print('=== Binance BTC Price ===')
url = 'https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT'
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=8) as r:
        data = json.loads(r.read())
        price = float(data.get('lastPrice', 0))
        chg = float(data.get('priceChangePercent', 0))
        high = float(data.get('highPrice', 0))
        low = float(data.get('lowPrice', 0))
        vol = float(data.get('quoteVolume', 0))
        print('BTCUSDT price:', price)
        print('BTC 24h change:', chg, '%')
        print('BTC 24h high:', high)
        print('BTC 24h low:', low)
        print('BTC 24h quote vol: $' + str(round(vol/1e9, 2)) + 'B')
except Exception as e:
    print('Error:', e)

# =============================================
# 2. Binance ETH Price
# =============================================
print()
print('=== Binance ETH Price ===')
url = 'https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT'
try:
    with urllib.request.urlopen(url, timeout=8) as r:
        data = json.loads(r.read())
        price = float(data.get('lastPrice', 0))
        chg = float(data.get('priceChangePercent', 0))
        high = float(data.get('highPrice', 0))
        low = float(data.get('lowPrice', 0))
        print('ETHUSDT price:', price)
        print('ETH 24h change:', chg, '%')
        print('ETH 24h high:', high)
        print('ETH 24h low:', low)
except Exception as e:
    print('Error:', e)

# =============================================
# 3. Binance Funding Rates (futures)
# =============================================
print()
print('=== Binance Futures Funding Rates ===')
symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']
for sym in symbols:
    url = 'https://fapi.binance.com/fapi/v1/premiumIndex?symbol=' + sym
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            fr = float(data.get('lastFundingRate', 0)) * 100
            next_t = data.get('nextFundingTime', 'N/A')
            oi = data.get('openInterest', 'N/A')
            mark_price = data.get('markPrice', 'N/A')
            index_price = data.get('indexPrice', 'N/A')
            print('  ' + sym + ': funding=' + str(round(fr, 4)) + '%  next=' + str(next_t))
            print('    mark=' + str(mark_price) + '  index=' + str(index_price) + '  OI=' + str(oi))
    except Exception as e:
        print('  ' + sym + ' error:', e)

# =============================================
# 4. CoinMarketCap (free, no key) - top 10
# =============================================
print()
print('=== CoinMarketCap Top 10 (free) ===')
url = 'https://api.coinmarketcap.com/v2/ticker/?limit=10&sort=rank'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
try:
    with urllib.request.urlopen(req, timeout=8) as r:
        data = json.loads(r.read())
        if 'data' in data:
            for k, v in list(data['data'].items())[:10]:
                name = v.get('name', '')
                symbol = v.get('symbol', '')
                price = v['quotes']['USD']['price']
                chg = v['quotes']['USD']['percent_change_24h']
                mcap = v['quotes']['USD']['market_cap']
                print('  ' + name + ' (' + symbol + '): $' + str(round(price, 4)) + '  24h:' + str(round(chg, 2)) + '%  MCap:$' + str(round(mcap/1e9, 2)) + 'B')
except Exception as e:
    print('CMC error:', e)

# =============================================
# 5. CoinGecko stablecoin data (free endpoint)
# =============================================
print()
print('=== CoinGecko Stablecoin Data ===')
# Get USDT marketcap as proxy for stablecoin total
url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=tether,usd-coin,dai,binance-usd&order=market_cap_desc&per_page=4&page=1&sparkline=false&price_change_percentage=24h'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=8) as r:
        data = json.loads(r.read())
        total_mcap = 0
        for coin in data:
            name = coin.get('name', '')
            mcap = coin.get('market_cap', 0)
            price = coin.get('current_price', 0)
            chg = coin.get('price_change_percentage_24h', 0)
            print('  ' + name + ': mcap=$' + str(round(mcap/1e9, 2)) + 'B  price=$' + str(price) + '  24h:' + str(chg) + '%')
            total_mcap += mcap
        print('  Total (top4 stablecoins): $' + str(round(total_mcap/1e9, 2)) + 'B')
except Exception as e:
    print('CoinGecko error:', e)

print()
print('DONE')
