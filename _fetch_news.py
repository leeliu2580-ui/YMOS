#!/usr/bin/env python3
"""Fetch market news for insight report."""
import sys, json, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

# Read Finnhub token
token = None
with open('.env', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('FINNHUB_API_KEY='):
            token = line.split('=', 1)[1].strip()
            break

if not token:
    print('No FINNHUB_API_KEY found')
    sys.exit(1)

# Fetch general market news
try:
    url = f'https://finnhub.io/api/v1/news?category=general&token={token}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        news = json.loads(r.read())
        for n in news[:10]:
            print(f"[{n.get('source','?')}] {n.get('headline','?')} | {n.get('url','')}")
except Exception as e:
    print(f'News fetch error: {e}')
