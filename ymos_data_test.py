from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Optional

import requests
from tickflow import TickFlow

ENV_PATH = Path(r"D:\0_workspace\trae_2601\ymos\YMOS\.env")
OUTPUT_DIR = Path(r"D:\0_workspace\trae_2601\ymos\YMOS\output")


# -----------------------------
# 基础工具
# -----------------------------
def load_env(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data



def detect_market(symbol: str) -> str:
    s = symbol.upper()
    if s.endswith((".SH", ".SZ", ".BJ")):
        return "CN"
    if s.endswith((".HK",)):
        return "HK"
    return "US"



def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)



def save_csv_text(symbol: str, text: str) -> Path:
    ensure_output_dir()
    filename = symbol.replace('.', '_') + ".csv"
    path = OUTPUT_DIR / filename
    path.write_text(text, encoding="utf-8-sig")
    return path



def print_block(title: str, payload) -> None:
    print(f"\n=== {title} ===")
    if isinstance(payload, str):
        print(payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


# -----------------------------
# 数据源：Finnhub
# -----------------------------
def finnhub_quote(api_key: str, symbol: str) -> dict:
    url = "https://finnhub.io/api/v1/quote"
    resp = requests.get(url, params={"symbol": symbol, "token": api_key}, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    if not data or all((data.get("c", 0) == 0, data.get("h", 0) == 0, data.get("l", 0) == 0, data.get("o", 0) == 0, data.get("pc", 0) == 0, data.get("t", 0) == 0)):
        raise RuntimeError(f"Finnhub 未返回有效报价，请检查 symbol 是否正确: {symbol}")

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



def finnhub_profile(api_key: str, symbol: str) -> dict:
    url = "https://finnhub.io/api/v1/stock/profile2"
    resp = requests.get(url, params={"symbol": symbol, "token": api_key}, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    if not data or not any(data.values()):
        raise RuntimeError(f"Finnhub 未返回有效公司资料，请检查 symbol 是否正确: {symbol}")

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


# -----------------------------
# 数据源：TickFlow
# -----------------------------
def tickflow_client(api_key: str) -> TickFlow:
    return TickFlow(api_key=api_key)



def tickflow_klines(api_key: str, symbol: str, count: int = 20):
    tf = tickflow_client(api_key)
    df = tf.klines.get(symbol, period="1d", count=count, as_dataframe=True)
    if df is None or df.empty:
        raise RuntimeError("TickFlow K线返回为空")
    return df



def tickflow_instruments(api_key: str, symbols: list[str]):
    tf = tickflow_client(api_key)
    return tf.instruments.batch(symbols=symbols)


# -----------------------------
# 统一入口
# -----------------------------
def get_cn_data(env: Dict[str, str], symbol: str, count: int, save_csv: bool) -> dict:
    api_key = env.get("TICKFLOW_API_KEY", "")
    if not api_key:
        raise RuntimeError("未配置 TICKFLOW_API_KEY，A股/港股当前默认走 TickFlow")

    df = tickflow_klines(api_key, symbol, count=count)
    instruments = tickflow_instruments(api_key, [symbol])

    result = {
        "market": "CN/HK",
        "symbol": symbol,
        "source": "TickFlow",
        "latest_kline": df.tail(1).to_dict(orient="records")[0],
        "tail_5": df.tail(5).to_dict(orient="records"),
        "instrument": instruments,
    }

    if save_csv:
        csv_path = save_csv_text(symbol, df.to_csv(index=False))
        result["csv_path"] = str(csv_path)

    return result



def get_us_data(env: Dict[str, str], symbol: str) -> dict:
    api_key = env.get("FINNHUB_API_KEY", "")
    if not api_key:
        raise RuntimeError("未配置 FINNHUB_API_KEY，美股当前默认走 Finnhub")

    quote = finnhub_quote(api_key, symbol)
    profile = finnhub_profile(api_key, symbol)

    return {
        "market": "US",
        "symbol": symbol,
        "source": "Finnhub",
        "quote": quote,
        "profile": profile,
    }



def validate_symbol(symbol: str, market: str) -> None:
    if market == "CN":
        if "." not in symbol:
            raise RuntimeError(f"A股代码格式不对，应类似 600000.SH / 000001.SZ，你输入的是: {symbol}")
        code, suffix = symbol.split('.', 1)
        if suffix not in {"SH", "SZ", "BJ"}:
            raise RuntimeError(f"A股后缀不对，应为 .SH / .SZ / .BJ，你输入的是: {symbol}")
        if not (code.isdigit() and len(code) == 6):
            raise RuntimeError(f"A股代码应为 6 位数字，你输入的是: {symbol}")

    if market == "HK":
        if "." not in symbol:
            raise RuntimeError(f"港股代码格式不对，应类似 0700.HK，你输入的是: {symbol}")

    if market == "US":
        if not symbol.isalpha() or len(symbol) > 5:
            raise RuntimeError(f"美股代码格式可疑，请检查是否拼错: {symbol}")



def main() -> None:
    parser = argparse.ArgumentParser(description="YMOS 统一行情/标的信息测试脚本")
    parser.add_argument("--symbol", required=True, help="证券代码，例如 600000.SH / 000001.SZ / AAPL")
    parser.add_argument("--count", type=int, default=20, help="K线数量，默认20")
    parser.add_argument("--save-csv", action="store_true", help="保存 K线到 output/*.csv")
    args = parser.parse_args()

    env = load_env(ENV_PATH)
    symbol = args.symbol.upper().strip()
    market = detect_market(symbol)
    validate_symbol(symbol, market)

    print_block("输入参数", {
        "symbol": symbol,
        "market_detected": market,
        "count": args.count,
        "save_csv": args.save_csv,
    })

    try:
        if market in {"CN", "HK"}:
            result = get_cn_data(env, symbol, args.count, args.save_csv)
        else:
            result = get_us_data(env, symbol)

        print_block("查询结果", result)

    except Exception as e:
        print_block("运行失败", {
            "symbol": symbol,
            "error": str(e),
        })


if __name__ == "__main__":
    main()
