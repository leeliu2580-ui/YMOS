#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import requests

API_KEY = os.getenv("COINMARKETCAP_API_KEY", "")
BASE_URL = "https://pro-api.coinmarketcap.com"

DERIVATIVE_UNDERLYING = {
    "HYPE-PERP-SHORT": "HYPE",
    "ETH-PERP-SHORT": "ETH",
    "BTC-PERP-SHORT": "BTC",
    "SOL-PERP-SHORT": "SOL",
}

CMC_SUPPORTED = {"BTC", "ETH", "SOL", "HYPE"}


def parse_symbols(raw: str) -> List[str]:
    return [s.strip().upper() for s in raw.split(",") if s.strip()]


def underlying_symbol(symbol: str) -> str:
    upper = symbol.upper()
    if upper in DERIVATIVE_UNDERLYING:
        return DERIVATIVE_UNDERLYING[upper]
    return upper


def cmc_get(path: str, params: Dict[str, str]) -> dict:
    headers = {"X-CMC_PRO_API_KEY": API_KEY, "Accept": "application/json"}
    resp = requests.get(f"{BASE_URL}{path}", headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_quotes(symbols: List[str]) -> tuple[list[dict], list[str]]:
    requested = []
    mapping = {}
    skipped = []

    for original in symbols:
        base = underlying_symbol(original)
        if base not in CMC_SUPPORTED:
            skipped.append(original)
            continue
        requested.append(base)
        mapping.setdefault(base, []).append(original)

    if not requested:
        return [], skipped

    payload = cmc_get("/v1/cryptocurrency/quotes/latest", {"symbol": ",".join(sorted(set(requested)))})
    data = payload.get("data", {})
    rows = []

    for base_symbol, originals in mapping.items():
        item = data.get(base_symbol)
        if not item:
            skipped.extend(originals)
            continue
        quote = item.get("quote", {}).get("USD", {})
        for original in originals:
            row = {
                "type": "quote",
                "symbol": original,
                "base_symbol": base_symbol,
                "price": quote.get("price"),
                "change": None,
                "change_pct": quote.get("percent_change_24h"),
                "high": None,
                "low": None,
                "open": None,
                "prev_close": None,
                "market_cap": quote.get("market_cap"),
                "volume_24h": quote.get("volume_24h"),
                "cmc_rank": item.get("cmc_rank"),
                "timestamp": quote.get("last_updated"),
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            }
            if original != base_symbol:
                row["position_hint"] = f"derived from underlying {base_symbol} spot quote"
            rows.append(row)

    return rows, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="CoinMarketCap crypto price fetcher")
    parser.add_argument("--symbols", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--token", default="")
    args = parser.parse_args()

    global API_KEY
    if args.token:
        API_KEY = args.token
    if not API_KEY:
        raise SystemExit("Missing COINMARKETCAP_API_KEY")

    symbols = parse_symbols(args.symbols)
    quotes, skipped = fetch_quotes(symbols)

    result = {
        "source": "CoinMarketCap",
        "watchlist": symbols,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(quotes),
        "skipped": skipped,
        "data": quotes,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"📡 CoinMarketCap 拉取 Crypto 价格: {', '.join(symbols)}")
    for q in quotes:
        pct = q.get('change_pct')
        pct_text = f"{pct:+.2f}%" if isinstance(pct, (int, float)) else "—"
        print(f"  ✅ {q['symbol']:<16} ${q['price']:.4f}  ({pct_text})  [base={q['base_symbol']}]")
    if skipped:
        print(f"  ⚠️ 跳过未支持 symbol: {skipped}")
    print(f"\n💾 已保存：{out}  ({len(quotes)}/{len(symbols)} 成功)")


if __name__ == "__main__":
    main()
