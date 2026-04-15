import os

path = r'D:\0_workspace\trae_2601\ymos\YMOS'
for root, dirs, files in os.walk(path):
    for f in files:
        if 'crypto_monitor' in f and '20260415' in f and '0926' in f:
            full = os.path.join(root, f)
            print('Found:', full)
            with open(full, 'r', encoding='utf-8', errors='replace') as fp:
                content = fp.read()
            
            out = r'D:\0_workspace\trae_2601\ymos\YMOS\_crypto_latest.txt'
            with open(out, 'w', encoding='utf-8') as fp:
                fp.write(content)
            print('Written', len(content), 'chars')
