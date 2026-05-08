# crypto-snapshot Skill

## Description
获取指定加密货币的完整观察快照，包括价格、TVL、官方更新、K 线关键位等。

## Input
- `symbol`: 加密货币 Ticker (如 PENDLE)

## Workflow
1. 检查 `Eyes/scripts/` 脚本是否存在。
2. 运行 `fetch_crypto_prices.py`。
3. 运行 `fetch_tvl_metrics.py`。
4. 运行 `fetch_official_updates.py`。
5. 运行 `fetch_kline_levels.py`。
6. 运行 `build_project_snapshot.py` 聚合。
7. 根据 `Eyes/SOP_*` 渲染观察报告。

## Output
- 包含所有维度事实的结构化快照报告。
- 指向原始 JSON 数据的路径。
