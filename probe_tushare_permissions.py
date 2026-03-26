from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Dict, Any

import tushare as ts

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


def safe_call(label: str, func: Callable[[], Any]) -> dict:
    try:
        data = func()
        rows = len(data) if hasattr(data, "__len__") else None
        sample = []
        if hasattr(data, "head"):
            sample = data.head(2).to_dict(orient="records")
        return {
            "ok": True,
            "rows": rows,
            "sample": sample,
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
        }


def main() -> None:
    env = load_env(ENV_PATH)
    token = env.get("TUSHARE_TOKEN", "")
    if not token:
        raise RuntimeError("TUSHARE_TOKEN not found in .env")

    pro = ts.pro_api(token)

    tests = {
        "trade_cal": lambda: pro.trade_cal(exchange="SSE", start_date="20260301", end_date="20260310"),
        "stock_basic": lambda: pro.stock_basic(exchange="", list_status="L", fields="ts_code,symbol,name,list_date"),
        "daily": lambda: pro.daily(ts_code="600000.SH", start_date="20260301", end_date="20260326"),
        "daily_basic": lambda: pro.daily_basic(ts_code="600000.SH", start_date="20260301", end_date="20260326", fields="ts_code,trade_date,close,pe,pb"),
        "fina_indicator": lambda: pro.fina_indicator(ts_code="600000.SH", year=2025, quarter=4),
        "income": lambda: pro.income(ts_code="600000.SH", start_date="20240101", end_date="20260331"),
        "balancesheet": lambda: pro.balancesheet(ts_code="600000.SH", start_date="20240101", end_date="20260331"),
        "cashflow": lambda: pro.cashflow(ts_code="600000.SH", start_date="20240101", end_date="20260331"),
        "moneyflow": lambda: pro.moneyflow(ts_code="600000.SH", start_date="20260301", end_date="20260326"),
        "index_basic": lambda: pro.index_basic(market="SSE"),
        "index_daily": lambda: pro.index_daily(ts_code="000001.SH", start_date="20260301", end_date="20260326"),
        "fund_basic": lambda: pro.fund_basic(market="E", status="L"),
        "fund_nav": lambda: pro.fund_nav(ts_code="000001.OF", start_date="20260301", end_date="20260326"),
        "news": lambda: pro.news(start_date="2026-03-20 00:00:00", end_date="2026-03-26 23:59:59"),
    }

    results = {"tests": {}}
    for name, fn in tests.items():
        results["tests"][name] = safe_call(name, fn)

    print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
