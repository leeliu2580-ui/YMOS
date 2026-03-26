from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

import requests

ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = ROOT / ".env"
OUTPUT_DIR = ROOT / "output" / "finnhub"
BASE_URL = "https://finnhub.io/api/v1"


def load_env(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def get_api_key() -> str:
    api_key = load_env(ENV_PATH).get("FINNHUB_API_KEY", "")
    if not api_key:
        raise RuntimeError("FINNHUB_API_KEY not found in .env")
    return api_key


COMMON_TICKER_FIXES = {
    "APL": "AAPL",
    "APPL": "AAPL",
    "TESLA": "TSLA",
    "GOOG": "GOOGL",
}



def ticker_hint(symbol: str) -> str:
    suggestion = COMMON_TICKER_FIXES.get(symbol.upper().strip())
    return f" Did you mean: {suggestion}?" if suggestion else ""



def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if not symbol.isalpha() or len(symbol) > 5:
        raise RuntimeError(f"Invalid US ticker format: {symbol}.{ticker_hint(symbol)}")
    return symbol


def finnhub_get(path: str, **params: Any) -> Any:
    params["token"] = get_api_key()
    url = f"{BASE_URL}{path}"
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def quote(symbol: str) -> Dict[str, Any]:
    symbol = validate_symbol(symbol)
    data = finnhub_get("/quote", symbol=symbol)
    if not data or all((data.get("c", 0) == 0, data.get("h", 0) == 0, data.get("l", 0) == 0, data.get("o", 0) == 0, data.get("pc", 0) == 0, data.get("t", 0) == 0)):
        raise RuntimeError(f"Finnhub returned no valid quote for symbol: {symbol}.{ticker_hint(symbol)}")
    return {
        "symbol": symbol,
        "current": data.get("c"),
        "high": data.get("h"),
        "low": data.get("l"),
        "open": data.get("o"),
        "prev_close": data.get("pc"),
        "timestamp": data.get("t"),
        "source": "Finnhub",
    }


def profile(symbol: str) -> Dict[str, Any]:
    symbol = validate_symbol(symbol)
    data = finnhub_get("/stock/profile2", symbol=symbol)
    if not data or not any(data.values()):
        raise RuntimeError(f"Finnhub returned no valid company profile for symbol: {symbol}.{ticker_hint(symbol)}")
    return {
        "symbol": symbol,
        "name": data.get("name"),
        "country": data.get("country"),
        "currency": data.get("currency"),
        "exchange": data.get("exchange"),
        "industry": data.get("finnhubIndustry"),
        "ipo": data.get("ipo"),
        "market_cap": data.get("marketCapitalization"),
        "source": "Finnhub",
    }


def to_unix(date_text: str) -> int:
    return int(datetime.strptime(date_text, "%Y-%m-%d").timestamp())


def candles(symbol: str, from_date: str, to_date: str, resolution: str) -> Dict[str, Any]:
    symbol = validate_symbol(symbol)
    data = finnhub_get(
        "/stock/candle",
        symbol=symbol,
        resolution=resolution,
        **{"from": to_unix(from_date), "to": to_unix(to_date)},
    )
    if data.get("s") != "ok":
        raise RuntimeError(f"Finnhub candles request failed for {symbol}: {data}")

    rows = []
    for i in range(len(data.get("t", []))):
        rows.append(
            {
                "timestamp": data["t"][i],
                "open": data["o"][i],
                "high": data["h"][i],
                "low": data["l"][i],
                "close": data["c"][i],
                "volume": data["v"][i],
            }
        )

    return {
        "symbol": symbol,
        "resolution": resolution,
        "from_date": from_date,
        "to_date": to_date,
        "count": len(rows),
        "candles": rows,
        "source": "Finnhub",
    }


def news(symbol: str, from_date: str, to_date: str, limit: int) -> Dict[str, Any]:
    symbol = validate_symbol(symbol)
    data = finnhub_get("/company-news", symbol=symbol, _from=from_date, to=to_date)
    items = data[:limit]
    return {
        "symbol": symbol,
        "from_date": from_date,
        "to_date": to_date,
        "count": len(items),
        "items": [
            {
                "headline": item.get("headline"),
                "source_name": item.get("source"),
                "summary": item.get("summary"),
                "url": item.get("url"),
                "datetime": item.get("datetime"),
            }
            for item in items
        ],
        "source": "Finnhub",
    }


def save_json(action: str, symbol: str, payload: Dict[str, Any]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = OUTPUT_DIR / f"{symbol}_{action}_{ts}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def default_dates() -> tuple[str, str]:
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    return week_ago.isoformat(), today.isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description="Finnhub local skill client")
    sub = parser.add_subparsers(dest="action", required=True)

    p_quote = sub.add_parser("quote")
    p_quote.add_argument("--symbol", required=True)
    p_quote.add_argument("--save-json", action="store_true")

    p_profile = sub.add_parser("profile")
    p_profile.add_argument("--symbol", required=True)
    p_profile.add_argument("--save-json", action="store_true")

    p_candles = sub.add_parser("candles")
    p_candles.add_argument("--symbol", required=True)
    p_candles.add_argument("--from-date")
    p_candles.add_argument("--to-date")
    p_candles.add_argument("--resolution", default="D")
    p_candles.add_argument("--save-json", action="store_true")

    p_news = sub.add_parser("news")
    p_news.add_argument("--symbol", required=True)
    p_news.add_argument("--from-date")
    p_news.add_argument("--to-date")
    p_news.add_argument("--limit", type=int, default=5)
    p_news.add_argument("--save-json", action="store_true")

    args = parser.parse_args()

    if args.action in {"candles", "news"}:
        default_from, default_to = default_dates()
        from_date = args.from_date or default_from
        to_date = args.to_date or default_to

    if args.action == "quote":
        result = quote(args.symbol)
    elif args.action == "profile":
        result = profile(args.symbol)
    elif args.action == "candles":
        result = candles(args.symbol, from_date, to_date, args.resolution)
    elif args.action == "news":
        result = news(args.symbol, from_date, to_date, args.limit)
    else:
        raise RuntimeError(f"Unsupported action: {args.action}")

    if getattr(args, "save_json", False):
        result["saved_to"] = str(save_json(args.action, validate_symbol(args.symbol), result))

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
