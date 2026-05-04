#!/usr/bin/env python3
"""
从状态机提取 ticker 后触发统一价格扫描。

读取 持仓_状态机.md 和 Watchlist_状态机.md 的 Ticker 列，
然后调用 fetch_price_router.py 完成价格路由。

支持三种模式：
  1. 无特殊参数     → 价格扫描
  2. --check-files → 档案完整性预检（雷达 Step 4）
  3. --check-p4    → P4 新鲜度纪律检查（策略分析 Step 4）
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT = SCRIPTS_DIR.parents[1]  # Eyes/scripts → Eyes → YMOS

sys.path.insert(0, str(SCRIPTS_DIR))
from env_loader import load_dotenv
from runtime_paths import repo_paths

PATHS = repo_paths(ROOT)


def extract_tickers_from_state_machine(filepath: Path) -> list[str]:
    """从 Markdown 状态机表格中提取 Ticker 列的值。"""
    if not filepath.exists():
        return []

    text = filepath.read_text(encoding="utf-8")
    tickers = []

    # 找到表格行，提取 Ticker 列
    in_table = False
    ticker_col_idx = -1

    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            in_table = False
            continue

        cols = [c.strip() for c in line.split("|")]
        # 去掉首尾空列（| 开头和结尾产生的空字符串）
        cols = [c for c in cols if c or c == ""]

        if not in_table:
            # 寻找表头行
            for i, col in enumerate(cols):
                if col.lower() in ("ticker", "代码", "标的"):
                    ticker_col_idx = i
                    in_table = True
                    break
            continue

        # 跳过分隔行 |:---|:---|
        if all(c.replace("-", "").replace(":", "") == "" for c in cols):
            continue

        # 提取 ticker 值
        if 0 <= ticker_col_idx < len(cols):
            val = cols[ticker_col_idx].strip()
            if val and val != "---" and not val.startswith(":"):
                tickers.append(val.upper())

    return tickers


def get_symbols_from_state_machine() -> list[tuple[str, str]]:
    """返回 [(label, folder_abs_path)] 列表，从状态机动态读取。"""
    watch_path = PATHS.watchlist_state
    hold_path = PATHS.holding_state

    items = []

    for label, state_file in [("Watchlist", watch_path), ("持仓", hold_path)]:
        text = state_file.read_text(encoding="utf-8")

        for line in text.splitlines():
            line_s = line.strip()
            if not line_s.startswith("|"):
                continue
            cols = [c.strip() for c in line_s.split("|")]
            cols = [c for c in cols if c or c == ""]
            if all(c.replace("-", "").replace(":", "") == "" for c in cols):
                continue

            ticker_col_idx = name_col_idx = -1
            for i, col in enumerate(cols):
                cl = col.lower()
                if cl in ("ticker", "代码", "标的"):
                    ticker_col_idx = i
                if cl in ("名称", "name"):
                    name_col_idx = i

            if ticker_col_idx < 0:
                continue

            ticker = cols[ticker_col_idx].strip().upper()
            if not ticker or ticker == "---" or ticker.startswith(":"):
                continue

            # 去除 ~~删除线~~ 格式
            ticker = re.sub(r"^~~|~~$", "", ticker)

            name = ""
            if name_col_idx >= 0:
                name = re.sub(r"^~~|~~$", "", cols[name_col_idx].strip())

            folder_name = f"{name}_{ticker}" if name else ticker
            if label == "Watchlist":
                folder = PATHS.watchlist_dir / folder_name
            else:
                folder = PATHS.holding_dir / folder_name

            items.append((ticker, str(folder)))

    return items


def check_files() -> dict:
    """档案完整性预检（雷达 Step 4）。返回每个标的的文件状态。"""
    results = {}
    for ticker, folder in get_symbols_from_state_machine():
        folder_path = Path(folder)
        files = []
        complete = True
        missing = []

        if folder_path.exists():
            for f in folder_path.iterdir():
                is_kb = "基础知识库" in f.name
                is_memo = "买入卖出备忘录" in f.name
                files.append({"name": f.name, "size": f.stat().st_size, "is_kb": is_kb, "is_memo": is_memo})

            kb_exists = any("基础知识库" in f["name"] for f in files)
            memo_exists = any("买入卖出备忘录" in f["name"] for f in files)

            # 判断标的类型（通过路径判断：持仓 vs Watchlist）
            is_holding = "持仓" in folder and "动态Watchlist" not in folder
            if is_holding:
                if not kb_exists:
                    missing.append("基础知识库.md")
                    complete = False
                if not memo_exists:
                    missing.append("买入卖出备忘录.md")
                    complete = False
            else:
                if not kb_exists:
                    missing.append("基础知识库.md")
                    complete = False
        else:
            files = []
            complete = False
            missing.append("目录不存在")

        results[ticker] = {
            "folder": folder,
            "files": files,
            "complete": complete,
            "missing": missing,
        }

    return results


def check_p4() -> dict:
    """P4 新鲜度纪律检查（策略分析 Step 4）。返回每个标的的 P4 状态。"""
    results = {}
    date_tag = dt.datetime.now().strftime("%Y%m%d")

    for ticker, folder in get_symbols_from_state_machine():
        folder_path = Path(folder)
        kb_file = None

        if folder_path.exists():
            for f in folder_path.iterdir():
                if "基础知识库" in f.name:
                    kb_file = f
                    break

        if not kb_file:
            results[ticker] = {"status": "NO_KB_FILE", "folder": folder}
            continue

        content = kb_file.read_text(encoding="utf-8")
        match = re.search(r"## P4 重点关注点.*?> *更新于 (\d{4}-\d{2}-\d{2})", content, re.DOTALL)
        has_p4 = "## P4 重点关注点" in content
        has_date = bool(match)

        status = "OK"
        if not has_p4:
            status = "NO_P4"
        elif not has_date:
            status = "NO_DATE"
        elif match:
            p4_date = dt.datetime.strptime(match.group(1), "%Y-%m-%d")
            days_ago = (dt.datetime.now() - p4_date).days
            if days_ago > 30:
                status = "STALE"
            else:
                status = "OK"

        results[ticker] = {
            "status": status,
            "folder": folder,
            "file": kb_file.name,
            "date": match.group(1) if match else None,
        }

    return results


def main() -> None:
    load_dotenv()

    p = argparse.ArgumentParser(description="从状态机触发统一价格扫描 / 档案完整性预检 / P4 新鲜度检查")
    p.add_argument("--finnhub-token", default="", help="可选；不传则尝试读取 FINNHUB_API_KEY")
    p.add_argument("--tushare-token", default="", help="可选；不传则尝试读取 TUSHARE_TOKEN")
    p.add_argument("--date-tag", default=dt.datetime.now().strftime("%Y%m%d"))
    p.add_argument("--output", default="", help="输出 JSON 路径（不传则自动按日期生成）")
    p.add_argument("--check-files", action="store_true", help="档案完整性预检（雷达 Step 4）")
    p.add_argument("--check-p4", action="store_true", help="P4 新鲜度纪律检查（策略分析 Step 4）")
    args = p.parse_args()

    PATHS.ensure_layout()
    date_tag = args.date_tag

    # ── 模式：档案完整性预检 ────────────────────────
    if args.check_files:
        results = check_files()
        out_dir = PATHS.radar_raw_dir(date_tag)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"files_check_{date_tag}.json"
        out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 档案完整性预检完成 → {out_path}")
        for ticker, info in results.items():
            status = "✅" if info["complete"] else "❌"
            print(f"  {status} {ticker}: {info['missing'] if info['missing'] else '完整'}")
        return

    # ── 模式：P4 新鲜度检查 ────────────────────────
    if args.check_p4:
        results = check_p4()
        out_dir = PATHS.strategy_raw_dir(date_tag)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"p4_check_{date_tag}.json"
        out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ P4 新鲜度纪律检查完成 → {out_path}")
        for ticker, info in results.items():
            print(f"  {info['status']:10s} {ticker} (更新于 {info.get('date', '无日期')})")
        return

    # ── 模式：价格扫描（默认）────────────────────
    tickers = []
    tickers.extend(extract_tickers_from_state_machine(PATHS.watchlist_state))
    tickers.extend(extract_tickers_from_state_machine(PATHS.holding_state))

    seen = set()
    deduped = []
    for t in tickers:
        if t not in seen:
            seen.add(t)
            deduped.append(t)

    if not deduped:
        print("NO_SYMBOLS: 状态机里没有可扫描 ticker")
        return

    print(f"📊 从状态机提取到 {len(deduped)} 个 ticker: {', '.join(deduped)}")

    out_dir = str(PATHS.radar_raw_dir(date_tag))
    finnhub_key   = args.finnhub_token  or os.getenv("FINNHUB_API_KEY", "")
    tushare_token = args.tushare_token  or os.getenv("TUSHARE_TOKEN", "")

    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "fetch_price_router.py"),
        "--symbols", ",".join(deduped),
        "--output-dir", out_dir,
        "--date-tag", date_tag,
    ]
    if finnhub_key:
        cmd += ["--finnhub-token", finnhub_key]
    if tushare_token:
        cmd += ["--tushare-token", tushare_token]

    code = subprocess.call(cmd, cwd=str(ROOT))
    raise SystemExit(code)


if __name__ == "__main__":
    main()
