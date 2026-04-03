import os, shutil

btc_dir = r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\持仓\BTC_BTC'
os.makedirs(btc_dir, exist_ok=True)

src = r'D:\0_workspace\trae_2601\ymos\YMOS\Eyes\投资雷达\btc_kb.md'
dst = os.path.join(btc_dir, '基础知识库.md')

with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

with open(dst, 'w', encoding='utf-8') as f:
    f.write(content)

print('Written successfully')
print('BTC dir files:', os.listdir(btc_dir))
