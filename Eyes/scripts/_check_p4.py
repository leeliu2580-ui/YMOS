import re
from pathlib import Path

results = {}
for label, folder in [
    ('BTC', r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\持仓\BTC_BTC'),
    ('NVDA', r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\动态Watchlist\NVDA_NVDA'),
    ('GOLD', r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\动态Watchlist\GOLD_GOLD'),
    ('HYPE', r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\持仓\HYPE_HYPE'),
]:
    kb_file = None
    for f in Path(folder).iterdir():
        if '基础知识库' in f.name or '投资备忘录' in f.name:
            kb_file = f
            break
    if kb_file:
        content = kb_file.read_text(encoding='utf-8')
        match = re.search(r"## P4 重点关注点.*?> 更新于 (\d{4}-\d{2}-\d{2})", content, re.DOTALL)
        has_p4 = '## P4 重点关注点' in content
        has_date = bool(match)
        results[label] = {'file': kb_file.name, 'has_p4': has_p4, 'has_date': has_date, 'date': match.group(1) if match else None}
    else:
        results[label] = 'NO KB FILE'

import json
with open(r'D:\0_workspace\trae_2601\ymos\YMOS\Eyes\scripts\_p4_check.json', 'w', encoding='utf-8') as out:
    json.dump(results, out, ensure_ascii=False, indent=2)
print('done')
