import json, urllib.request, ssl, datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://query1.finance.yahoo.com/v8/finance/chart/GC%3DF?interval=1d&range=10d'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
    data = json.loads(r.read())

q = data['chart']['result'][0]
meta = q['meta']
print('Symbol:', meta.get('symbol'))
print('Currency:', meta.get('currency'))
print('Current price:', meta.get('regularMarketPrice'))
print('Prev close:', meta.get('previousClose'))
print('52wk high:', meta.get('fiftyTwoWeekHigh'))
print('52wk low:', meta.get('fiftyTwoWeekLow'))
print('Market time:', meta.get('regularMarketTime'))

timestamps = q['timestamp']
closes = q['indicators']['quote'][0]['close']
for i in range(min(8, len(timestamps))):
    dt = datetime.datetime.fromtimestamp(timestamps[i])
    c = closes[i] if closes[i] else 0
    print(f'{dt.strftime("%Y-%m-%d")}: {c:.2f}')
