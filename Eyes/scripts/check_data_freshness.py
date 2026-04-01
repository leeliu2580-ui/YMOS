#!/usr/bin/env python3
"""
YMOS 数据新鲜度检查脚本

功能：
- 扫描 持仓/ 和 动态Watchlist/ 下的所有标的文件夹
- 检查 个股基础知识库.md 中的 P4 关注点更新时间
- 如果更新时间超过 30 天，则将其列为“待处理缺口”
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path

# 路径基准
ROOT = Path(__file__).resolve().parents[2]
HOLDING_DIR = ROOT / "持仓与关注" / "持仓"
WATCHLIST_DIR = ROOT / "持仓与关注" / "动态Watchlist"

def check_freshness(directory):
    gaps = []
    if not directory.exists():
        return gaps

    for folder in directory.iterdir():
        if not folder.is_dir():
            continue
        
        kb_path = folder / "个股基础知识库.md"
        if not kb_path.exists():
            gaps.append(f"{folder.name}: 缺少个股基础知识库.md")
            continue

        content = kb_path.read_text(encoding="utf-8")
        # 寻找 P4 更新时间，匹配格式如 "> 更新于 2026-03-18"
        match = re.search(r"## P4 重点关注点.*?> 更新于 (\d{4}-\d{2}-\d{2})", content, re.DOTALL)
        
        if not match:
            gaps.append(f"{folder.name}: P4 关注点从未更新或格式错误")
            continue

        update_date_str = match.group(1)
        update_date = datetime.strptime(update_date_str, "%Y-%m-%d")
        
        if datetime.now() - update_date > timedelta(days=30):
            gaps.append(f"{folder.name}: P4 关注点已过期（最后更新于 {update_date_str}）")

    return gaps

def main():
    print("📡 正在检查个股文件夹新鲜度...")
    
    holding_gaps = check_freshness(HOLDING_DIR)
    watchlist_gaps = check_freshness(WATCHLIST_DIR)
    
    all_gaps = holding_gaps + watchlist_gaps
    
    if not all_gaps:
        print("✅ 所有标的数据均在有效期内。")
    else:
        print(f"⚠️ 发现 {len(all_gaps)} 项数据缺口：")
        for gap in all_gaps:
            print(f"  - {gap}")

    # 将结果写入临时 JSON 供 Dashboard 读取
    import json
    output_path = ROOT / "Eyes" / "市场洞察" / "Raw_Data" / "data_freshness_gaps.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"gaps": all_gaps, "checked_at": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
