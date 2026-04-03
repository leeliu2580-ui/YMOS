import urllib.request, json, datetime

# Get NVDA 2-year monthly chart
url = 'https://query1.finance.yahoo.com/v8/finance/chart/NVDA?interval=1mo&range=2y'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
        result = data['chart']['result'][0]
        meta = result['meta']
        print('Symbol:', meta['symbol'])
        print('Current Price:', meta['regularMarketPrice'])
        print('52W High:', meta.get('fiftyTwoWeekHigh'))
        print('52W Low:', meta.get('fiftyTwoWeekLow'))
        
        ts = result['timestamp']
        closes = result['indicators']['quote'][0]['close']
        print()
        print('Last 12 monthly closes:')
        start = max(0, len(ts) - 12)
        for i in range(start, len(ts)):
            dt = datetime.datetime.fromtimestamp(ts[i])
            c = closes[i]
            if c is not None:
                print(f'  {dt.strftime("%Y-%m")}: ${c:.2f}')
except Exception as e:
    print('Error:', e)
