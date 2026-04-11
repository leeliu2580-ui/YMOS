#!/usr/bin/env python3
import json, os, glob

base = r"D:\0_workspace\trae_2601\ymos\YMOS\Eyes\市场洞察\Raw_Data\2026-04"
for fname in ["financial_data_20260406.json", "financial_data_20260407.json", "financial_data_20260409.json"]:
    fpath = os.path.join(base, fname)
    if not os.path.exists(fpath):
        print(f"=== {fname}: NOT FOUND ===")
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("data", [])
    hype_items = [i for i in items if "hype" in i.get("title","").lower() or "hyperliquid" in i.get("title","").lower() or "hype" in i.get("description","").lower()]
    print(f"=== {fname} ({len(items)} total, {len(hype_items)} HYPE) ===")
    for i in hype_items:
        print("TITLE:", i.get("title"))
        print("LINK:", i.get("link"))
        print("DESC:", i.get("description", "")[:200])
        print("---")
