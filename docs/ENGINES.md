# Engines — CryptoCapi API v1

CryptoCapi exposes four analytical engines. Each targets a different use case and execution model, and each one is sold as its own pass: a key that holds one engine does not open the others (see [Entitlement](AUTHENTICATION.md#entitlement-one-pass-per-engine)). The public demo key opens Radar and Quant Plus for `bitcoin` and `ethereum`, with no signup.

---

## Engine Overview

| Engine | Execution | Universe | Latency | Pass |
|---|---|---|---|---|
| **Radar** | Pre-computed (scheduler) | ~15 coins | < 100 ms | `alpha` (the Pulse view is free) |
| **Quant Plus** | Pre-computed (scheduler) | ~15 coins | < 100 ms | `quant_plus` |
| **Quant Pro** | On-demand per request | Any Binance USDT pair | ~2–3 s | `quant` |
| **Market Scanner** | On-demand (reads Quant Plus signals) | All coins scored by Quant Plus | < 100 ms | `market_scan` |

---

## Radar

**What it does:** Delivers AI-generated market intelligence for each asset in the scheduled universe. For every coin, Radar produces a natural-language analysis, a sentiment label, and a confidence score — with all numeric claims mathematically verified before delivery (see [SEAL.md](SEAL.md)).

**Output includes:**
- `summary`: concise directional take (1–2 sentences)
- `detailed_report`: structured narrative (max 150 words)
- `sentiment`: `bullish` | `bearish` | `neutral`
- `market_regime`: structural regime: `BULLISH_TREND`, `BEARISH_TREND`, `RANGING_CHOP`, `EXTREME_VOLATILITY`, `UNUSUAL_VOLATILITY`
- `confidence`: `HIGH` / `MEDIUM` / `LOW` with a numeric score (`0.0–1.0`)
- `sources_verified`: news sources with credibility tier (`Tier 1`–`3`); empty array means no news met relevance thresholds (not an error)
- `math_diagnostics.audit_trail`: `process_seal` SHA-256 hash certifying which mathematical corrections were applied

**Endpoint:** `GET /market/insights/:id?view=alpha`
(`id` = CoinGecko slug, e.g. `bitcoin`, `ethereum`). Without `view=alpha` the route answers the free Pulse view, with no diagnostics and no seal.

> **Note on `sources_verified: []`:** An empty sources array is a deliberate signal, not missing data. It means no news from the last window influenced the asset — the analysis is based purely on price action.

---

## Quant Plus

**What it does:** Produces a fully deterministic quantitative signal for each asset in the scheduled universe. No AI is involved — every output field is computed by Python from historical price data.

**Output includes:**
- `actionable_insight.signal`: `BUY_WATCH` | `SELL_WATCH` | `ALERT` | `HOLD`, with its `risk_level` (`LOW` | `MEDIUM` | `HIGH`) and the `trigger_condition` that explains it
- `sentiment`: `bullish` | `bearish` | `neutral`
- `market_regime`: same 5-regime taxonomy as Radar
- `confidence`: deterministic `score` and `label`, from data coverage and volatility, lowered when the on-chain read is unavailable
- `onchain_stats`: network congestion, whale activity and how reliable the on-chain read was
- `math_diagnostics.audit_trail`: `reproducible` SHA-256 hash. It includes the input price vector, so third parties can independently recompute the result and verify it matches (see [SEAL.md](SEAL.md))

**Endpoints:**
- `GET /quant-plus/:id/signal?view=alpha`: single asset signal (`id` = CoinGecko slug, e.g. `bitcoin`). Same payload as `GET /market/insights/:id?engine=quant_plus&view=alpha`. Without `view=alpha`, both answer the free Pulse view.
- `POST /quant/batch`: signals for up to 50 assets in one request

```json
// POST /quant/batch body
{ "symbols": ["bitcoin", "ethereum", "solana"] }
```

---

## Quant Pro

**What it does:** Runs a live dual-timeframe quantitative analysis on any Binance USDT pair, on demand. Fetches real candle data at request time and computes the signal immediately — no pre-computation, no universe restriction.

**Output includes:**
- `resolved_signal`: `STRONG_BUY` (>= 85) | `BUY` (65-84) | `NEUTRAL_CHOP` (35-64) | `SELL` (16-34) | `STRONG_SELL` (< 16). It says how many indicators agree: STRONG is high confluence, not a probability or a forecast
- `resolved_score`: composite signal strength (`0–100`)
- `macro_1d` and `micro_4h`: per-timeframe breakdown with individual indicator scores, confluence score, signal and `candle_count`
- `mir_diagnostics`: how the two timeframes were resolved (`base_raw_score`) and whether the data fail-safe applied (`insufficient_data`, `conviction_multiplier`): with fewer than 50 candles in either timeframe, the score's distance to 50 is halved. Plus an `explanation`
- `audit_trail`: `output_seal` SHA-256 hash: tamper-evident seal over all deterministic outputs; any alteration of the response invalidates the hash (see [SEAL.md](SEAL.md))

**Endpoint:** `GET /quant/:symbol/signal`
(`symbol` = Binance pair in uppercase, e.g. `BTCUSDT`, `ETHUSDT`, `SOLUSDT`)

> **Latency note:** Quant Pro fetches live candle data at request time. Expect ~2–3 seconds per call. Not suitable for high-frequency polling — use Quant Plus batch for that pattern.

---

## Market Scanner

**What it does:** Scans all assets currently scored by Quant Plus and returns a ranked list by signal strength. Useful for discovering which assets in the universe have the strongest directional conviction at a given moment.

**Output includes:**
- Ranked array of assets with signal, score, and regime
- Filtered to assets with a Quant Plus signal fresher than 24 hours
- Stablecoins are left out while they hold their peg. One that moves more than 1% in 24 hours comes back into the ranking, because a depeg is a signal

**Query parameters:**
| Param | Values | Default |
|---|---|---|
| `strategy` | `balanced` \| `aggressive` \| `conservative` | `balanced` |
| `limit` | `1`–`50` | `10` |

**Endpoint:** `GET /quant/market-scan`

---

## Coin Universe (Radar & Quant Plus)

The collector runs every hour over a fixed core of **10 coins**, plus up to **5 volatile additions** from the top 20 by market cap (≥ 5% price change in 24h), deduplicated.

**Fixed core (always included):**

| | | | | |
|---|---|---|---|---|
| bitcoin | ethereum | tether | binancecoin | ripple |
| usd-coin | solana | tron | dogecoin | leo-token |

**Volatile additions:** up to 5 coins from the top 20 that moved ≥ 5% in the last 24h. The set changes each scheduler cycle.

**Update frequency:** Priority coins (BTC, ETH, BNB, SOL, USDT) refresh every **2 hours**. All others refresh every **4 hours**.

**Data window:** the Z-Score and the Bollinger bands use the last 51 closed daily candles (UTC) from Yahoo Finance. Since engine `v2.3.0` (`v2.3.0-math` and `v2.3.0-radar`) the day in progress is never part of the series, so the last date in `input_timestamps` is a complete day, not today.

---

## Choosing the Right Engine

| Goal | Engine |
|---|---|
| "What's the AI read on Bitcoin right now?" | Radar |
| "Give me a pure math signal on Ethereum, reproducible" | Quant Plus |
| "Analyze PEPEUSDT — not in your universe" | Quant Pro |
| "Which coins in your universe have the strongest buy signal?" | Market Scanner |
| "I distrust AI — give me math only" | Quant Plus or Quant Pro |

---

## Reaching these engines from an AI agent

All four are also exposed as native tools by the **MCP server** [`@cryptocapi/mcp`](https://www.npmjs.com/package/@cryptocapi/mcp), so an agent can call them without any REST integration:

| Tool | Engine |
|---|---|
| `get_insight` | Radar, or Quant Plus with `engine="quant_plus"` |
| `get_signal` | Quant Pro |
| `batch_signals` | Quant Plus, several assets in one call |
| `scan_market` | Market Scanner |

The package is a thin client over this same API and forwards responses verbatim, so the `protocol_hash` an agent receives is byte-identical to the one documented in [SEAL.md](SEAL.md). It is listed in the official MCP Registry as `io.github.Jegoba90/cryptocapi`, so clients that read that registry find it without being handed a URL. Setup and the demo-key path are in the [README](../README.md#-nativo-para-agentes).

If your client does not speak MCP, the same engines are reachable over plain HTTP, and the domain says where everything is:

| Resource | What it is |
|---|---|
| [`/v1/openapi.json`](https://api.cryptocapi.com/v1/openapi.json) | The OpenAPI contract as a downloadable document, not the Swagger UI |
| [`/.well-known/api-catalog`](https://www.cryptocapi.com/.well-known/api-catalog) | RFC 9727 linkset: contract, HTML reference, health endpoint |
| [`/.well-known/ai-catalog.json`](https://www.cryptocapi.com/.well-known/ai-catalog.json) | Every machine-readable resource, enumerated |
| [`llms.txt`](https://www.cryptocapi.com/llms.txt) | Entry index: what each engine does, how to authenticate, where to go next |

Both catalogs are announced in a `Link` header on every response. Editorial pages also have a markdown mirror: append `.md` to a page URL. **Branch on the `Content-Type`, not the status code** — a `.md` URL with no mirror returns 200 with the HTML shell, so `text/markdown` is the only reliable signal that the mirror exists.
