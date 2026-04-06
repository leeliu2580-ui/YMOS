import os, json
from pathlib import Path

result = {}
for label, folder in [
    ('BTC_BTC', r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\持仓\BTC_BTC'),
    ('NVDA_NVDA', r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\动态Watchlist\NVDA_NVDA'),
    ('GOLD_GOLD', r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\动态Watchlist\GOLD_GOLD'),
    ('HYPE_HYPE', r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\持仓\HYPE_HYPE'),
]:
    files = []
    if Path(folder).exists():
        for f in Path(folder).iterdir():
            files.append({'name': f.name, 'size': f.stat().st_size, 'is_kb': '基础知识库' in f.name or '个股基础' in f.name or '投资备忘录' in f.name})
    result[label] = files

with open(r'D:\0_workspace\trae_2601\ymos\YMOS\Eyes\scripts\_files_report.json', 'w', encoding='utf-8') as out:
    json.dump(result, out, ensure_ascii=False, indent=2)
print('done')
