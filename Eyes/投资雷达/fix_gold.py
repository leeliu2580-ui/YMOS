import os, shutil

dst_dir = r'D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\动态Watchlist\GOLD_GOLD'
files = os.listdir(dst_dir)
print('Files:', files)

src = r'D:\0_workspace\trae_2601\ymos\YMOS\Eyes\投资雷达\gold_kb_updated.md'
fname = files[0]
old_path = os.path.join(dst_dir, fname)
backup_path = os.path.join(dst_dir, '基础知识库_backup_20260402.md')

shutil.copy(old_path, backup_path)
print('Backup done to:', backup_path)

# Write new file
new_path = os.path.join(dst_dir, '基础知识库.md')
shutil.copy(src, new_path)
print('New file written to:', new_path)
