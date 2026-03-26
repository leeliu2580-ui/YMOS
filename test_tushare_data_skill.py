from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

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


def main() -> None:
    env = load_env(ENV_PATH)
    token = env.get("TUSHARE_TOKEN", "")
    if not token:
        raise RuntimeError("TUSHARE_TOKEN not found in .env")

    pro = ts.pro_api(token)

    results = {"tests": {}}

    # 1) 轻量冒烟：股票基础信息
    try:
        stock_basic = pro.stock_basic(exchange="", list_status="L", fields="ts_code,symbol,name,area,industry,list_date")
        results["tests"]["stock_basic"] = {
            "ok": True,
            "rows": len(stock_basic),
            "sample": stock_basic.head(3).to_dict(orient="records"),
        }
    except Exception as e:
        results["tests"]["stock_basic"] = {"ok": False, "error": str(e)}

    # 2) 日线：600000.SH
    try:
        daily = pro.daily(ts_code="600000.SH", start_date="20260301", end_date="20260326")
        results["tests"]["daily_600000_SH"] = {
            "ok": True,
            "rows": len(daily),
            "sample": daily.head(3).to_dict(orient="records"),
        }
    except Exception as e:
        results["tests"]["daily_600000_SH"] = {"ok": False, "error": str(e)}

    # 3) 财务指标：测试权限
    try:
        fina = pro.fina_indicator(ts_code="600000.SH", year=2025, quarter=4)
        results["tests"]["fina_indicator_600000_SH"] = {
            "ok": True,
            "rows": len(fina),
            "sample": fina.head(3).to_dict(orient="records"),
        }
    except Exception as e:
        results["tests"]["fina_indicator_600000_SH"] = {"ok": False, "error": str(e)}

    print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
