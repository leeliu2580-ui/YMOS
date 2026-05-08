# 价格与TVL跟踪 SOP

## 1. 触发暗号
- `查一下价格 [TICKER]`
- `看一下 TVL [TICKER]`
- `调研一下 [TICKER]` (作为子流程)

## 2. 执行流程
1. 调用 `fetch_crypto_prices.py` 获取价格。
2. 调用 `fetch_tvl_metrics.py` 获取 TVL。
3. 如果是调研，则调用 `build_project_snapshot.py` 聚合。

## 3. 报告模板
```markdown
# 价格与TVL跟踪 - [SYMBOL] - [YYYY-MM-DD]

## 1. 标的概览
- **现价**: $[PRICE] ([24H_CHANGE]%)
- **市值**: $[MARKET_CAP]
- **成交量**: $[VOLUME]

## 2. 相对强弱
- **vs BTC**: [VS_BTC_STRENGTH]%
- **vs ETH**: [VS_ETH_STRENGTH]%

## 3. TVL 表现
- **当前 TVL**: $[TVL]
- **1d 变化**: [TVL_1D]%
- **7d 变化**: [TVL_7D]%

## 4. 简评
[基于 P17 框架给出 2-3 句客观描述，不含主观买卖建议]
```

## 4. 注意事项
- 数据来源必须标记。
- 如果数据获取失败，显示“获取失败/暂无数据”。
