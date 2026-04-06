import os
from pathlib import Path

folder = Path(r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\持仓\BTC_BTC')
for f in folder.iterdir():
    print(f.name, '|', f.stat().st_size, 'bytes')
