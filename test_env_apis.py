from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import requests
from tickflow import TickFlow


ENV_PATH = Path(r"D:\0_workspace\trae_2601\ymos\YMOS\.env")


def load_env(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def mask(value: str, keep: int = 4) -> str:
    if not value:
        return "<empty>"
    if len(value) <= keep * 2:
        return "*" * len(value)
    return f"{value[:keep]}...{value[-keep:]}"


def test_finnhub(api_key: str) -> dict:
    url = "https://finnhub.io/api/v1/quote"
    params = {"symbol": "AAPL", "token": api_key}
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return {
        "symbol": "AAPL",
        "current": data.get("c"),
        "high": data.get("h"),
        "low": data.get("l"),
        "open": data.get("o"),
        "prev_close": data.get("pc"),
        "timestamp": data.get("t"),
    }



def test_tushare(token: str) -> dict:
    url = "https://api.tushare.pro"
    payload = {
        "api_name": "daily",
        "token": token,
        "params": {"ts_code": "600000.SH"},
        "fields": "ts_code,trade_date,open,high,low,close,vol",
    }
    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"Tushare error: {data}")
    items = data.get("data", {}).get("items", [])
    if not items:
        raise RuntimeError("Tushare 返回为空")
    first = items[0]
    return {
        "ts_code": first[0],
        "trade_date": first[1],
        "open": first[2],
        "high": first[3],
        "low": first[4],
        "close": first[5],
        "vol": first[6],
    }



def test_tickflow(api_key: str) -> dict:
    tf = TickFlow(api_key=api_key)
    df = tf.klines.get("600000.SH", period="1d", count=5, as_dataframe=True)
    if df is None or df.empty:
        raise RuntimeError("TickFlow K线返回为空")
    last = df.tail(1).to_dict(orient="records")[0]
    return last



def main() -> None:
    env = load_env(ENV_PATH)

    results = {
        "configured": {
            "FINNHUB_API_KEY": mask(env.get("FINNHUB_API_KEY", "")),
            "TUSHARE_TOKEN": mask(env.get("TUSHARE_TOKEN", "")),
            "TICKFLOW_API_KEY": mask(env.get("TICKFLOW_API_KEY", "")),
        },
        "tests": {},
    }

    try:
        results["tests"]["finnhub"] = {"ok": True, "data": test_finnhub(env.get("FINNHUB_API_KEY", ""))}
    except Exception as e:
        results["tests"]["finnhub"] = {"ok": False, "error": str(e)}

    try:
        results["tests"]["tushare"] = {"ok": True, "data": test_tushare(env.get("TUSHARE_TOKEN", ""))}
    except Exception as e:
        results["tests"]["tushare"] = {"ok": False, "error": str(e)}

    try:
        results["tests"]["tickflow"] = {"ok": True, "data": test_tickflow(env.get("TICKFLOW_API_KEY", ""))}
    except Exception as e:
        results["tests"]["tickflow"] = {"ok": False, "error": str(e)}

    print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
