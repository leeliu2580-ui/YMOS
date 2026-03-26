#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from tickflow import TickFlow


def parse_symbols(raw: str) -> list[str]:
    return [s.strip().upper() for s in raw.split(",") if s.strip()]


def is_cn_symbol(symbol: str) -> bool:
    s = symbol.upper()
    return s.endswith((".SH", ".SZ", ".BJ"))


def main() -> None:
    parser = argparse.ArgumentParser(description="TickFlow A股价格拉取")
    parser.add_argument("--symbols", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--token", default=os.environ.get("TICKFLOW_API_KEY", ""))
    args = parser.parse_args()

    if not args.token:
        print("⚠️ 未提供 TICKFLOW_API_KEY，跳过 TickFlow A股拉取。")
        raise SystemExit(0)

    raw_symbols = parse_symbols(args.symbols)
    symbols = [s for s in raw_symbols if is_cn_symbol(s)]
    skipped = [s for s in raw_symbols if s not in symbols]

    if not symbols:
        print("⚠️ 没有可查询的 A股标的，退出。")
        raise SystemExit(0)

    tf = TickFlow(api_key=args.token)
    data = []

    print(f"📡 TickFlow 拉取 A股价格: {', '.join(symbols)}")

    for symbol in symbols:
        try:
            df = tf.klines.get(symbol, period="1d", count=5, as_dataframe=True)
            if df is None or df.empty:
                raise RuntimeError("K线返回为空")
            row = df.tail(1).to_dict(orient="records")[0]
            prev_close = None
            change = None
            pct_chg = None
            if len(df) >= 2:
                prev_close = float(df.iloc[-2]["close"])
                change = float(row["close"]) - prev_close
                pct_chg = (change / prev_close * 100) if prev_close else None
            item = {
                "symbol": symbol,
                "ok": True,
                "trade_date": row.get("trade_date", ""),
                "last_close": float(row.get("close") or 0),
                "last_open": float(row.get("open") or 0),
                "last_high": float(row.get("high") or 0),
                "last_low": float(row.get("low") or 0),
                "last_volume": float(row.get("volume") or 0),
                "pre_close": prev_close,
                "change": change,
                "pct_chg": pct_chg,
                "amount": float(row.get("amount") or 0),
                "name": row.get("name"),
            }
            data.append(item)
            pct_text = f"{pct_chg:+.2f}%" if isinstance(pct_chg, (int, float)) else "—"
            print(f"  ✅ {symbol:12s} ¥{item['last_close']:.2f}  ({pct_text})  [{item['trade_date']}]")
        except Exception as e:
            data.append({"symbol": symbol, "ok": False, "error": str(e)})
            print(f"  ❌ {symbol:12s} ERROR: {e}")

    output = {
        "source": "TickFlow daily API",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(data),
        "symbols": raw_symbols,
        "skipped": skipped,
        "data": data,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = sum(1 for x in data if x.get("ok"))
    print(f"\n💾 已保存：{out_path}  ({ok}/{len(data)} 成功)")


if __name__ == "__main__":
    main()
