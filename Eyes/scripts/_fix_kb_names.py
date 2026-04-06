import re
from pathlib import Path

fixes = [
    (r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\持仓\BTC_BTC',       'BTC',   '2026-04-03'),
    (r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\动态Watchlist\NVDA_NVDA', 'NVDA', '2026-04-03'),
    (r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\动态Watchlist\GOLD_GOLD', 'GOLD', '2026-04-03'),
    (r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\持仓\HYPE_HYPE',        'HYPE',  '2026-04-02'),
]

results = []

for folder, label, update_date in fixes:
    folder_path = Path(folder)
    if not folder_path.exists():
        results.append(f'{label}: FOLDER NOT FOUND')
        continue

    kb_src = None
    for f in folder_path.iterdir():
        if ('基础知识库' in f.name or '投资备忘录' in f.name) and f.suffix == '.md':
            kb_src = f
            break

    if not kb_src:
        results.append(f'{label}: NO KB FILE')
        continue

    content = kb_src.read_text(encoding='utf-8')
    has_date = bool(re.search(r"> 更新于 \d{4}-\d{2}-\d{2}", content))

    if has_date:
        results.append(f'{label}: date OK in {kb_src.name}')
        final_content = content
    else:
        final_content = re.sub(r"(## P4 重点关注点\n)", rf"\1> 更新于 {update_date}\n", content)
        kb_src.write_text(final_content, encoding='utf-8')
        results.append(f'{label}: added date to {kb_src.name}')

    # Create 个股基础知识库.md copy
    dest = folder_path / '个股基础知识库.md'
    dest.write_text(final_content, encoding='utf-8')
    results.append(f'{label}: created 个股基础知识库.md')

for r in results:
    print(r)
