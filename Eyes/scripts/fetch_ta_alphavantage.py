#!/usr/bin/env python3
"""
Alpha Vantage 技术指标抓取脚本（免费 API Key 直接取 MA，无需自己算）

用途：YPMS Watchlist 标的技术指标（SMA / EMA / RSI / MACD / BBANDS）
数据源：Alpha Vantage（预计算指标，API 直接返回）

API Key 免费申请：https://www.alphavantage.co/support/#api-key
免费限制：25 次/分钟（完全够 Watchlist 使用）

使用示例：
  python3 fetch_ta_alphavantage.py --symbols MU,NVDA,AAPL
  python3 fetch_ta_alphavantage.py --from-watchlist

输出：ta_data.json（含 SMA20/EMA20/RSI14，预计算直接取）
"""

from __future__ import annotations

import argparse
import json
import ssl
import time
import warnings
import requests
from datetime import datetime, timezone
from pathlib import Path

warnings.filterwarnings("ignore", message=".*Unverified HTTPS.*")
requests.packages.urllib3.disable_warnings()


_API_KEY = "XVLHMJHJDUALD8L6"   # Alpha Vantage 免费 Key
_BASE_URL = "https://www.alphavantage.co/query"

# 宽松 SSL 上下文（解决证书链问题）
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

# 每个标的每次调用消耗 1 次请求额
_INDICATOR_COST = {
    "SMA": 1,
    "EMA": 1,
    "RSI": 1,
    "MACD": 1,
    "BBANDS": 1,
}

# 预定义每个标的要拉的指标（节省请求额）
_DEFAULT_INDICATORS = ["SMA", "EMA", "RSI"]


def fetch_indicator(func: str, symbol: str, **kwargs) -> dict | None:
    """拉取单个技术指标，返回最新值或 None（限速/失败时）"""
    params = {
        "function": func,
        "symbol": symbol,
        "interval": "daily",
        "series_type": "close",
        "apikey": _API_KEY,
        **kwargs,
    }
    try:
        r = requests.get(_BASE_URL, params=params, timeout=15, verify=False)
        d = r.json()

        # 检查限速 / 达到免费额度上限
        raw_str = str(d)
        if "Please consider" in raw_str or "premium" in raw_str.lower():
            print(f"  ⚠️  {symbol}/{func} 限速或已达免费上限，等待 65s...")
            time.sleep(65)
            r = requests.get(_BASE_URL, params=params, timeout=15, verify=False)
            d = r.json()

        # 找 Technical Analysis key
        ta_keys = [k for k in d if k.startswith("Technical Analysis:")]
        if not ta_keys:
            print(f"  ❌ {symbol}/{func} 无数据: {str(d)[:80]}")
            return None

        ta = d[ta_keys[0]]
        latest_date = sorted(ta.keys())[-1]
        meta = d.get("Meta Data", {})
        refreshed = meta.get("3: Last Refreshed", latest_date)

        return {"date": latest_date, "refreshed": refreshed, "values": ta[latest_date]}

    except Exception as e:
        print(f"  ❌ {symbol}/{func} 异常: {e}")
        return None


def fetch_all_for_symbol(symbol: str, indicators: list[str]) -> dict:
    """拉取一个标的全部指标"""
    result = {"symbol": symbol, "ok": True, "indicators": {}, "error": None}
    for func in indicators:
        cost = _INDICATOR_COST.get(func, 1)
        extra = {}
        if func == "SMA":
            extra = {"time_period": 20}
        elif func == "EMA":
            extra = {"time_period": 20}
        elif func == "RSI":
            extra = {"time_period": 14}
        elif func == "MACD":
            extra = {"fastperiod": 12, "slowperiod": 26, "signalperiod": 9}
        elif func == "BBANDS":
            extra = {"time_period": 20, "nbdevup": 2, "nbdevdn": 2}

        data = fetch_indicator(func, symbol, **extra)
        if data:
            result["indicators"][func] = data
            # 拉完一个等一下，避免触发 25/min 限制
            time.sleep(2)
        else:
            result["indicators"][func] = None
            result["ok"] = False
            result["error"] = f"{func} failed"

    return result


def main():
    p = argparse.ArgumentParser(description="Alpha Vantage 技术指标抓取（免费直接取 MA）")
    p.add_argument("--symbols", default="", help="逗号分隔，如 MU,NVDA,AAPL")
    p.add_argument("--indicators", default="SMA,EMA,RSI",
                   help="要拉的指标，默认 SMA,EMA,RSI（各耗 1 次请求额）")
    p.add_argument("--output", default="ta_data.json", help="输出路径")
    p.add_argument("--sleep", type=float, default=2.0, help="每次请求间隔（秒）")
    args = p.parse_args()

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    indicators = [i.strip().upper() for i in args.indicators.split(",") if i.strip()]

    if not symbols:
        print("请提供 --symbols")
        return

    results = []
    total_cost = len(indicators) * len(symbols)
    print(f"📡 将拉取 {len(symbols)} 个标的 × {len(indicators)} 个指标 = {total_cost} 次请求")

    for i, symbol in enumerate(symbols):
        print(f"\n[{i+1}/{len(symbols)}] {symbol}...")
        res = fetch_all_for_symbol(symbol, indicators)
        results.append(res)
        if i < len(symbols) - 1:
            wait = args.sleep
            print(f"  ⏳ 等 {wait}s（避免限速）...")
            time.sleep(wait)

    # 打印汇总
    print("\n\n=== 技术指标汇总（Alpha Vantage 实时）===")
    for r in results:
        sym = r["symbol"]
        print(f"\n{sym}:")
        for func, data in r.get("indicators", {}).items():
            if data and data.get("values"):
                vals = data["values"]
                # 简化打印
                val_str = " | ".join(f"{k}:{v}" for k, v in vals.items())
                print(f"  {func:6s} [{data['date']}] {val_str}")
            else:
                print(f"  {func:6s}: ❌ 无数据")

    # 保存
    out = {
        "source": "Alpha Vantage Technical Indicators API",
        "api_key_prefix": _API_KEY[:6] + "***",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "symbols": symbols,
        "indicators": indicators,
        "results": results,
    }
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = sum(1 for r in results if r["ok"])
    print(f"\n💾 已保存：{out_path}  ({ok}/{len(results)} 标的成功）")


if __name__ == "__main__":
    main()