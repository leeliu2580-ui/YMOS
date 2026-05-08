#!/usr/bin/env python3
"""
Eyes/scripts/build_project_snapshot.py
聚合价格、TVL、官方信息、K 线、投研链接，生成单标的统一快照。
"""

import json
import argparse
import datetime
import os
import sys

def load_json(path):
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading {path}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="生成项目统一观察快照")
    parser.add_argument("--project", required=True, help="项目 Symbol，如 PENDLE")
    parser.add_argument("--price", help="价格 JSON 路径")
    parser.add_argument("--tvl", help="TVL JSON 路径")
    parser.add_argument("--official", help="官方更新 JSON 路径")
    parser.add_argument("--kline", help="K 线快照 JSON 路径")
    parser.add_argument("--research", help="投研链接 JSON 路径")
    parser.add_argument("--output", required=True, help="输出 JSON 路径")
    args = parser.parse_args()

    project = args.project.upper()
    print(f"🏗️ Building snapshot for {project}...")

    # 加载数据
    price_data = load_json(args.price)
    tvl_data = load_json(args.tvl)
    official_data = load_json(args.official)
    kline_data = load_json(args.kline)
    research_data = load_json(args.research)

    # 提取本项目的数据 (如果 JSON 是列表)
    def extract_item(data, key_field, value):
        if isinstance(data, list):
            for item in data:
                if str(item.get(key_field, "")).upper() == str(value).upper():
                    return item
        return data

    snapshot = {
        "project": project,
        "price_snapshot": extract_item(price_data, "symbol", project),
        "tvl_snapshot": extract_item(tvl_data, "protocol", project),
        "official_updates": official_data,
        "kline_snapshot": extract_item(kline_data, "symbol", project),
        "research_links": research_data,
        "generated_at": datetime.datetime.now().isoformat()
    }

    # 写入文件
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Unified snapshot saved to {args.output}")

if __name__ == "__main__":
    main()
