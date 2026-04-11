#!/usr/bin/env python3
"""
YMOS 工作流定时执行检查脚本
检查当日是否已生成对应报告，未生成则执行
"""
import os
from datetime import datetime, timedelta
from pathlib import Path

# 工作目录
WORKSPACE = Path("D:/0_workspace/trae_2601/ymos/YMOS")
TODAY = datetime.now().strftime("%Y-%m-%d")

# 检查函数
def check_report_exists(report_type: str) -> bool:
    """检查当日报告是否已存在"""
    paths = {
        "市场洞察": WORKSPACE / "Eyes/市场洞察/2026-04" / f"{TODAY}_市场洞察.md",
        "投资雷达": WORKSPACE / "Eyes/投资雷达/2026-04" / f"投资雷达_{TODAY}.md",
        "策略分析": WORKSPACE / "Brain/策略分析/2026-04" / f"策略分析日志_{TODAY}.md",
        "持仓收口": WORKSPACE / "持仓与关注/持仓备忘录_视图.md",
    }
    # 检查文件是否存在（修改时间为今日）
    report_path = paths.get(report_type)
    if report_path and report_path.exists():
        mtime = datetime.fromtimestamp(report_path.stat().st_mtime)
        if mtime.date() == datetime.now().date():
            return True
    return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python run_workflow_check.py <市场洞察|投资雷达|策略分析|持仓收口>")
        sys.exit(1)
    
    report_type = sys.argv[1]
    exists = check_report_exists(report_type)
    
    if exists:
        print(f"SKIP: {report_type} 报告已存在，跳过执行")
    else:
        print(f"RUN: {report_type} 报告不存在，需要执行")
        # 输出 RUN 标记，供 cron 判断