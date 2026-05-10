#!/usr/bin/env python3
"""
FRED 宏观经济数据拉取脚本

使用 fredapi 库获取美联储官方宏观经济数据：
- GDP、CPI、PPI、非农就业、失业率
- 联邦基金利率、国债收益率
- 消费者信心、零售销售、制造业PMI
- 住房开工、房地产数据

用法：
  # 获取最新 CPI 同比数据
  python3 Eyes/scripts/fetch_fred_data.py --series CPI --output cpi.json

  # 获取 GDP 季度数据（过去 8 个季度）
  python3 Eyes/scripts/fetch_fred_data.py --series GDP --limit 8 --output gdp.json

  # 获取利率数据
  python3 Eyes/scripts/fetch_fred_data.py --series FEDFUNDS --output fed_rate.json

  # 批量获取多个指标
  python3 Eyes/scripts/fetch_fred_data.py --batch CPI,GDP,FEDFUNDS,UNRATE --output macro.json

常用 FRED 系列 ID：
  CPIAUCSL     - 消费者价格指数 (CPI)
  PCEPI        - PCE 物价指数
  GDP          - GDP
  FEDFUNDS     - 联邦基金利率
  DGS10        - 10年期国债收益率
  UNRATE       - 失业率
  NROU         - 自然失业率
  PAYEMS       - 非农就业人数
  SP500        - 标普500指数
  DXY          - 美元指数
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from fredapi import Fred


SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT = SCRIPTS_DIR.parents[1]

sys.path.insert(0, str(SCRIPTS_DIR))
from env_loader import load_dotenv


# ── 常用 FRED 系列 ID 速查 ──────────────────────────────────────────────────

SERIES_CATALOG = {
    # 通胀
    "CPI": "CPIAUCSL",        # 消费者价格指数
    "PCE": "PCEPI",           # PCE物价指数
    "PPI": "PPIACO",          # 生产者价格指数

    # 增长
    "GDP": "GDP",             # GDP
    "NGDP": "NGDPP",          # 名义GDP

    # 利率
    "FEDFUNDS": "FEDFUNDS",   # 联邦基金利率
    "DGS1": "DGS1",           # 1年期国债
    "DGS2": "DGS2",           # 2年期国债
    "DGS5": "DGS5",           # 5年期国债
    "DGS10": "DGS10",         # 10年期国债
    "DGS30": "DGS30",         # 30年期国债

    # 就业
    "UNRATE": "UNRATE",       # 失业率
    "NROU": "NROU",           # 自然失业率
    "PAYEMS": "PAYEMS",       # 非农就业人数
    "PAYROLL": "PAYEMS",      # 非农就业（别名）

    # 消费
    "PCEC": "PCEC",           # 个人消费支出
    "RSales": "RSales",       # 零售销售

    # 房地产
    "HOUST": "HOUST",         # 新建住房开工
    "CSUSHPINSI": "CSUSHPINSI",  # S&P/CS房价指数

    # 市场
    "SP500": "SP500",         # 标普500
    "DXY": "DXY",             # 美元指数
}


# ── 主函数 ─────────────────────────────────────────────────────────────────

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="FRED 宏观经济数据拉取脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "常用系列 ID:\n"
            "  CPI, PCE, PPI          - 通胀指标\n"
            "  GDP, NGDP               - 经济增长\n"
            "  FEDFUNDS, DGS10        - 利率\n"
            "  UNRATE, PAYEMS          - 就业\n"
            "  SP500, DXY              - 市场指标\n"
            "或直接使用 FRED 系列 ID 如 CPIAUCSL\n"
        )
    )
    parser.add_argument("--series", type=str, help="单个系列 ID 或别名 (如 CPI, GDP)")
    parser.add_argument("--limit", type=int, default=1, help="获取观测值数量，默认 1（最新）")
    parser.add_argument("--output", default="fred_data.json", help="输出文件路径")
    parser.add_argument("--batch", type=str, help="逗号分隔的多个系列 (如 CPI,GDP,FEDFUNDS)")
    parser.add_argument("--api-key", default=os.environ.get("FRED_API_KEY", ""), help="FRED API Key")

    args = parser.parse_args()

    if not args.api_key:
        print("⚠️ 未提供 FRED API Key，跳过。")
        print("   如需启用，请在 .env 中配置 FRED_API_KEY")
        sys.exit(0)

    # 初始化 FRED 客户端
    try:
        fred = Fred(args.api_key)
    except Exception as e:
        print(f"❌ FRED 初始化失败: {e}")
        sys.exit(1)

    series_list = []

    # 解析系列列表
    if args.batch:
        for s in args.batch.split(","):
            s = s.strip().upper()
            if s in SERIES_CATALOG:
                series_list.append(SERIES_CATALOG[s])
            else:
                series_list.append(s)
    elif args.series:
        s = args.series.strip().upper()
        if s in SERIES_CATALOG:
            series_list.append(SERIES_CATALOG[s])
        else:
            series_list.append(s)
    else:
        parser.print_help()
        print("\n❌ 请指定 --series 或 --batch")
        sys.exit(1)

    print(f"📊 FRED 数据拉取：{series_list}")

    all_results = []
    meta_info = {"series": {}, "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}

    for series_id in series_list:
        print(f"  → {series_id}...", end=" ", flush=True)

        try:
            # fredapi 的 limit 参数是从数据起点算的，不是最近的
            # 所以需要用 observation_start 来获取最近的数据
            # 估算：月度数据 × 2 倍系数（考虑不同频率）
            from datetime import datetime as dt, timedelta
            start_date = dt.now() - timedelta(days=args.limit * 60)

            series_data = fred.get_series(
                series_id,
                observation_start=start_date.strftime('%Y-%m-%d')
            )

            if series_data.empty:
                print("无数据")
                continue

            # 取升序数据的最后 N 条 = 最新的 N 条
            if len(series_data) > args.limit:
                series_data = series_data.tail(args.limit)

            # 转换为列表格式
            observations = []
            for date, value in series_data.items():
                observations.append({
                    "series_id": series_id,
                    "date": date.strftime("%Y-%m-%d") if hasattr(date, 'strftime') else str(date),
                    "value": str(value),
                    "value_numeric": float(value) if value != "." else None,
                })

            # 按日期降序排列（最新的在前）
            observations.sort(key=lambda x: x["date"], reverse=True)

            all_results.extend(observations)

            # 记录元信息
            latest = observations[0]
            meta_info["series"][series_id] = {
                "latest_date": latest["date"],
                "latest_value": latest["value"],
                "observations_count": len(observations),
            }
            print(f"{latest['date']}: {latest['value']}")

        except Exception as e:
            print(f"请求失败: {e}")

    output = {
        "meta": meta_info,
        "data": all_results,
    }

    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n💾 已保存：{args.output}")
    print(f"   总计：{len(all_results)} 条观测值，{len(series_list)} 个系列")


if __name__ == "__main__":
    main()