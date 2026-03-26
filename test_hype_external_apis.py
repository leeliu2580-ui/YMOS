from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import requests

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


def test_coinmarketcap(api_key: str) -> dict:
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "X-CMC_PRO_API_KEY": api_key,
        "Accept": "application/json",
    }
    params = {"symbol": "HYPE"}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    return {
        "status_code": resp.status_code,
        "ok": resp.ok,
        "json": resp.json(),
    }


def test_tavily(api_key: str) -> dict:
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": "Hyperliquid HYPE token price market cap current price",
        "search_depth": "advanced",
        "max_results": 5,
        "include_answer": True,
    }
    resp = requests.post(url, json=payload, timeout=30)
    body = resp.json()
    return {
        "status_code": resp.status_code,
        "ok": resp.ok,
        "answer": body.get("answer"),
        "results": body.get("results", [])[:3],
        "raw": body,
    }


def main() -> None:
    env = load_env(ENV_PATH)
    cmc_key = env.get("COINMARKETCAP_API_KEY", "")
    tavily_key = env.get("TAVILY_API_KEY", "")

    results = {"tests": {}}

    try:
        cmc = test_coinmarketcap(cmc_key)
        results["tests"]["coinmarketcap"] = {
            "ok": cmc["ok"],
            "status_code": cmc["status_code"],
            "data": cmc["json"],
        }
    except Exception as e:
        results["tests"]["coinmarketcap"] = {"ok": False, "error": str(e)}

    try:
        tavily = test_tavily(tavily_key)
        results["tests"]["tavily"] = {
            "ok": tavily["ok"],
            "status_code": tavily["status_code"],
            "answer": tavily["answer"],
            "results": tavily["results"],
        }
    except Exception as e:
        results["tests"]["tavily"] = {"ok": False, "error": str(e)}

    print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
