# crypto-event-check Skill

## Description
针对加密市场的争议事件或重大变动，进行多源取证与可信度核验。

## Input
- `event_description`: 待核验的事件描述
- `symbol`: 关联的项目 Ticker (可选)

## Workflow
1. 调用 `fetch_official_updates.py` 和 `fetch_research_links.py` 收集信息。
2. 按照 `Brain/references/p19-event-verification.md` 进行证据等级划分。
3. 执行 `Brain/SOP_事件核验.md`。

## Output
- 事件核验报告，包含事实、证据链、可信度评分。
