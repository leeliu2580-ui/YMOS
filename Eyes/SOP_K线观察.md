# K线观察 SOP

## 1. 触发暗号
- `看一下 K线 [TICKER]`
- `调研一下 [TICKER]` (作为子流程)

## 2. 执行流程
1. 调用 `fetch_kline_levels.py` 获取 K 线快照。
2. 识别支撑位、阻力位和趋势。

## 3. 报告模板
```markdown
# K线观察 - [SYMBOL] - [YYYY-MM-DD]

## 1. 当前结构
- **周期**: [TIMEFRAME]
- **现价**: $[PRICE]
- **区间**: $[RANGE_LOW] ~ $[RANGE_HIGH]

## 2. 关键价位
- **支撑位**: [SUPPORT_LEVELS]
- **阻力位**: [RESISTANCE_LEVELS]

## 3. 趋势状态
- **状态**: [TREND_STATE] (uptrend / range / downtrend / unclear)

## 4. 关键触发条件
- **突破关注**: 价格站稳 [RESISTANCE] 之上。
- **跌破关注**: 价格收于 [SUPPORT] 之下。
```

## 4. 注意事项
- 只做客观结构描述。
- 支撑阻力位仅供参考。
