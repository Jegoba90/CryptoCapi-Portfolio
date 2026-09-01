# Engines — CryptoCapi API v1

CryptoCapi exposes four analytical engines. Each targets a different use case and execution model. All four require a **PRO API key** (`sk_live_…`).

---

## Engine Overview

| Engine | Execution | Universe | Latency | Plan |
|---|---|---|---|---|
| **Radar** | Pre-computed (scheduler) | ~15 coins | < 100 ms | PRO |
| **Quant Plus** | Pre-computed (scheduler) | ~15 coins | < 100 ms | PRO |
| **Quant Pro** | On-demand per request | Any Binance USDT pair | ~2–3 s | PRO |
| **Market Scanner** | On-demand (reads Quant Plus signals) | All coins scored by Quant Plus | < 100 ms | PRO |

---

## Radar

**What it does:** Delivers AI-generated market intelligence for each asset in the scheduled universe. For every coin, Radar produces a natural-language analysis, a sentiment label, and a confidence score — with all numeric claims mathematically verified before delivery (see [SEAL.md](SEAL.md)).

**Output includes:**
- `summary` — concise directional take (1–2 sentences)
- `detailed_report` — structured narrative (max 150 words)
- `sentiment` — `bullish` | `bearish` | `neutral`
- `market_regime` — structural regime: `BULLISH_TREND`, `BEARISH_TREND`, `RANGING_CHOP`, `EXTREME_VOLATILITY`, `UNUSUAL_VOLATILITY`
- `confidence` — `HIGH` / `MEDIUM` / `LOW` with a numeric score (`0.0–1.0`)
- `sources_verified` — news sources with credibility tier (`Tier 1`–`3`); empty array means no news met relevance thresholds (not an error)
- `math_diagnostics.audit_trail` — `process_seal` SHA-256 hash certifying which mathematical corrections were applied

**Endpoint:** `GET /market/insights/:id`
(`id` = CoinGecko slug, e.g. `bitcoin`, `ethereum`)

> **Note on `sources_verified: []`:** An empty sources array is a deliberate signal, not missing data. It means no news from the last window influenced the asset — the analysis is based purely on price action.

---

## Quant Plus

**What it does:** Produces a fully deterministic quantitative signal for each asset in the scheduled universe. No AI is involved — every output field is computed by Python from historical price data.

**Output includes:**
- `signal` — `BUY` | `SELL` | `HOLD`
- `sentiment` — numeric score and label
- `market_regime` — same 5-regime taxonomy as Radar
- `confidence` — deterministic score based on data coverage and volatility
- `math_diagnostics.audit_trail` — `reproducible` SHA-256 hash: includes the input price vector, so third parties can independently recompute the result and verify it matches (see [SEAL.md](SEAL.md))

**Endpoints:**
- `GET /quant/:symbol/signal` — single asset signal (pass CoinGecko slug, e.g. `bitcoin`)
- `POST /quant/batch` — signals for multiple assets in one request

```json
// POST /quant/batch body
{ "symbols": ["bitcoin", "ethereum", "solana"] }
```

---

## Quant Pro

**What it does:** Runs a live dual-timeframe quantitative analysis on any Binance USDT pair, on demand. Fetches real candle data at request time and computes the signal immediately — no pre-computation, no universe restriction.

**Output includes:**
- `final_signal` — `BUY` | `SELL` | `HOLD`
- `final_score` — composite signal strength (`0–100`)
- Per-timeframe breakdown (1D and 4H): individual indicator scores, confluence score
- `MIR diagnostics` — market instability read
- `audit_trail` — `output_seal` SHA-256 hash: tamper-evident seal over all deterministic outputs; any alteration of the response invalidates the hash (see [SEAL.md](SEAL.md))

**Endpoint:** `GET /quant/:symbol/signal`
(`symbol` = Binance pair in uppercase, e.g. `BTCUSDT`, `ETHUSDT`, `SOLUSDT`)

> **Latency note:** Quant Pro fetches live candle data at request time. Expect ~2–3 seconds per call. Not suitable for high-frequency polling — use Quant Plus batch for that pattern.

---

## Market Scanner

**What it does:** Scans all assets currently scored by Quant Plus and returns a ranked list by signal strength. Useful for discovering which assets in the universe have the strongest directional conviction at a given moment.

**Output includes:**
- Ranked array of assets with signal, score, and regime
- Filtered to assets with a Quant Plus signal fresher than 24 hours

**Query parameters:**
| Param | Values | Default |
|---|---|---|
| `strategy` | `balanced` \| `aggressive` \| `conservative` | `balanced` |
| `limit` | number | `10` |

**Endpoint:** `GET /quant/market-scan`

---

## Coin Universe (Radar & Quant Plus)

The scheduler runs continuously on a fixed core of **10 coins**, plus up to **5 volatile additions** from the top 20 by market cap (≥ 5% price change in 24h), deduplicated.

**Fixed core (always included):**

| | | | | |
|---|---|---|---|---|
| bitcoin | ethereum | tether | binancecoin | ripple |
| usd-coin | solana | tron | dogecoin | leo-token |

**Volatile additions:** up to 5 coins from the top 20 that moved ≥ 5% in the last 24h. The set changes each scheduler cycle.

**Update frequency:** Priority coins (BTC, ETH, BNB, SOL, USDT) refresh every **2 hours**. All others refresh every **4 hours**.

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

The package is a thin client over this same API and forwards responses verbatim, so the `protocol_hash` an agent receives is byte-identical to the one documented in [SEAL.md](SEAL.md). Setup and the demo-key path are in the [README](../README.md#-nativo-para-agentes).
