import os

# Create NVDA folder structure properly
nvda_dir = r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\动态Watchlist\NVDA_NVDA'
os.makedirs(nvda_dir, exist_ok=True)
print('Created NVDA dir:', nvda_dir)

# Remove any garbage files from failed copy
for f in os.listdir(nvda_dir):
    if not f.endswith('.md'):
        os.remove(os.path.join(nvda_dir, f))
        print('Removed non-md file:', f)

print('Final files:', os.listdir(nvda_dir))
