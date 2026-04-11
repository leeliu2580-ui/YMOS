#!/usr/bin/env python3
import json

with open(r"D:\0_workspace\trae_2601\ymos\YMOS\Eyes\市场洞察\Raw_Data\2026-04\financial_data_20260411.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Search for HYPE mentions
for item in data.get("data", []):
    title = item.get("title", "")
    desc = item.get("description", "")
    if "hype" in title.lower() or "hyperliquid" in title.lower() or "hype" in desc.lower() or "hyperliquid" in desc.lower():
        print("TITLE:", title)
        print("LINK:", item.get("link"))
        print("DESC:", desc[:200])
        print("---")
