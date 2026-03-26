from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from tickflow import TickFlow

ENV_PATH = Path(r"D:\0_workspace\trae_2601\ymos\YMOS\.env")


TEST_SYMBOLS = {
    "A股": "300308.SZ",
    "港股": "0700.HK",
    "美股": "AAPL.US",
}


def load_env(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data



def test_symbol(tf: TickFlow, market_name: str, symbol: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "market": market_name,
        "symbol": symbol,
        "tests": {},
    }

    # 1) 日K线
    try:
        df = tf.klines.get(symbol, period="1d", count=5, as_dataframe=True)
        if df is None or df.empty:
            raise RuntimeError("K线返回为空")
        result["tests"]["klines_1d"] = {
            "ok": True,
            "rows": len(df),
            "last": df.tail(1).to_dict(orient="records")[0],
        }
    except Exception as e:
        result["tests"]["klines_1d"] = {"ok": False, "error": str(e)}

    # 2) 标的信息
    try:
        instruments = tf.instruments.batch(symbols=[symbol])
        if not instruments:
            raise RuntimeError("instrument 返回为空")
        result["tests"]["instrument"] = {
            "ok": True,
            "data": instruments[0],
        }
    except Exception as e:
        result["tests"]["instrument"] = {"ok": False, "error": str(e)}

    return result



def main() -> None:
    env = load_env(ENV_PATH)
    api_key = env.get("TICKFLOW_API_KEY", "")
    if not api_key:
        raise RuntimeError("TICKFLOW_API_KEY not found in .env")

    tf = TickFlow(api_key=api_key)

    all_results = {
        "summary": {},
        "results": [],
    }

    for market_name, symbol in TEST_SYMBOLS.items():
        result = test_symbol(tf, market_name, symbol)
        all_results["results"].append(result)

    all_results["summary"] = {
        item["market"]: {
            name: data.get("ok", False)
            for name, data in item["tests"].items()
        }
        for item in all_results["results"]
    }

    print(json.dumps(all_results, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
