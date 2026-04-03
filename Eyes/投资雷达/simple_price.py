import urllib.request
import json
import datetime

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_yahoo(symbol, range_='1d'):
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range={range_}'
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    result = data['chart']['result'][0]
    meta = result['meta']
    ts = result.get('timestamp', [])
    closes = result['indicators']['quote'][0]['close']
    highs = result['indicators']['quote'][0]['high']
    lows = result['indicators']['quote'][0]['low']
    opens = result['indicators']['quote'][0]['open']
    return meta, ts, closes, highs, lows, opens

def fmt(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

items = [
    ('BTC-USD', 'BTC'),
    ('ETH-USD', 'ETH'),
    ('GC=F',   'GOLD'),
]

for symbol, name in items:
    try:
        meta, ts, closes, highs, lows, opens = fetch_yahoo(symbol)
        price = meta['regularMarketPrice']
        prev = meta.get('previousClose') or (closes[-2] if len(closes) > 1 else None)
        high = meta.get('regularMarketDayHigh') or highs[-1]
        low = meta.get('regularMarketDayLow') or lows[-1]
        chg = (price - prev) / prev * 100 if prev else 0
        print(f'{name}: ${price:,.2f}  ({chg:+.2f}%)  H:${high:,.2f} L:${low:,.2f}')
    except Exception as e:
        print(f'{name}: Error - {e}')

# NVDA from Yahoo
try:
    meta, ts, closes, highs, lows, opens = fetch_yahoo('NVDA')
    price = meta['regularMarketPrice']
    prev = meta.get('previousClose') or (closes[-2] if len(closes) > 1 else None)
    high = meta.get('regularMarketDayHigh') or highs[-1]
    low = meta.get('regularMarketDayLow') or lows[-1]
    chg = (price - prev) / prev * 100 if prev else 0
    print(f'NVDA: ${price:,.2f}  ({chg:+.2f}%)  H:${high:,.2f} L:${low:,.2f}')
except Exception as e:
    print(f'NVDA: Error - {e}')

print()
print('Data source: Yahoo Finance')
print('Timestamp:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
