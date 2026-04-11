#!/usr/bin/env python3
import os
folder = r"D:\0_workspace\trae_2601\ymos\YMOS\持仓与关注\持仓\HYPE_HYPE"
if os.path.exists(folder):
    for f in os.listdir(folder):
        print(f)
else:
    print("FOLDER NOT FOUND")
