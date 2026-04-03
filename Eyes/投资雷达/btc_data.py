import urllib.request, json, datetime, os

# BTC price from Yahoo Finance BTC-USD
url = 'https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD?interval=1d&range=3mo'
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
        print('Monthly closes (last 6):')
        start = max(0, len(ts) - 6)
        for i in range(start, len(ts)):
            dt = datetime.datetime.fromtimestamp(ts[i])
            c = closes[i]
            if c is not None:
                print('  ' + dt.strftime('%Y-%m') + ': $' + str(round(c, 2)))
except Exception as e:
    print('Error:', e)

# Also get BTC cost basis context from state machine
btc_dir = r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\持仓\BTC_BTC'
os.makedirs(btc_dir, exist_ok=True)
print('BTC folder created at:', btc_dir)
