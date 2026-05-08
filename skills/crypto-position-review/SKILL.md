# crypto-position-review Skill

## Description
结合最新市场快照与用户持仓成本，生成标准化的仓位复盘报告。

## Input
- `symbol`: 加密货币 Ticker
- `cost`: 开仓成本价
- `value`: 当前仓位价值 (可选)

## Workflow
1. 调用 `crypto-snapshot` 获取最新市场数据。
2. 读取真相源获取持仓细节。
3. 执行 `Brain/SOP_仓位复盘.md`。
4. 基于 `Brain/references/p18-position-review.md` 给出判断。

## Output
- 标准化仓位复盘 Markdown 报告。
- 包含浮盈亏、逻辑核验、持有前提和失效条件。
