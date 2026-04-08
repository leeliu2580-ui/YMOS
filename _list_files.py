import os
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

src_dir = r"D:\6_命理\精选十部紫薇六爻基础"

files = os.listdir(src_dir)
for f in sorted(files):
    print(repr(f))
