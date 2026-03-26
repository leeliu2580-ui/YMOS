# Finnhub Skill

Use Finnhub to fetch US stock and crypto market data when the workspace has `FINNHUB_API_KEY` configured in `.env`.

## When to use

Use this skill when the user asks for any of the following and Finnhub is an appropriate source:
- US stock real-time quote
- Company profile / industry / exchange / IPO date
- Daily candles or recent historical price data
- Company news by ticker
- Basic symbol validation for US tickers

Do **not** use this skill for:
- A-share as primary source when TickFlow is available
- Trading decisions without a risk disclaimer and a separate analysis step
- Massive batch crawling in tight loops

## Inputs

Common parameters:
- `symbol`: US ticker like `AAPL`, `TSLA`, `NVDA`
- `from_date`: `YYYY-MM-DD`
- `to_date`: `YYYY-MM-DD`
- `resolution`: `D`, `60`, `30`, `15`, etc.
- `count`: optional local limit for display

## API coverage in this skill

Implemented helper script: `scripts/finnhub_client.py`

Supported actions:
- `quote` → `/quote`
- `profile` → `/stock/profile2`
- `candles` → `/stock/candle`
- `news` → `/company-news`

## Usage

Run from workspace root:

```bash
python skills/finnhub/scripts/finnhub_client.py quote --symbol AAPL
python skills/finnhub/scripts/finnhub_client.py profile --symbol AAPL
python skills/finnhub/scripts/finnhub_client.py candles --symbol AAPL --from-date 2026-03-01 --to-date 2026-03-26 --resolution D --save-json
python skills/finnhub/scripts/finnhub_client.py news --symbol AAPL --from-date 2026-03-20 --to-date 2026-03-26 --limit 5
```

Common mistake:

```bash
# wrong
python skills/finnhub/scripts/finnhub_client.py quote --symbol APL

# correct
python skills/finnhub/scripts/finnhub_client.py quote --symbol AAPL
```

## Output rules

- Output JSON to stdout
- If `--save-json` is passed, also save JSON under `output/finnhub/`
- If Finnhub returns empty quote payloads (`0` values) or empty profiles, treat that as a validation failure and surface a clear error
- Keep failures explicit; do not silently downgrade

## Integration notes for YMOS

- Prefer TickFlow for CN tickers
- Prefer Finnhub for US tickers and US company metadata
- In reports, declare the data source explicitly, e.g. `本次使用了 Finnhub 补充数据`
- If Finnhub fails, continue the broader SOP when possible instead of blocking the whole workflow

## Environment

Reads `FINNHUB_API_KEY` from the workspace `.env` file.

## Rate-limit attitude

Finnhub free tier is limited. Avoid high-frequency loops. Prefer fewer larger requests, and cache or reuse results when possible.
