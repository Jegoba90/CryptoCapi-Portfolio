# Math Override Certified — Verification Seal

Every response from a CryptoCapi analytical engine carries an `audit_trail` object with a `protocol_hash` (SHA-256). This page explains what that seal guarantees and how to use it.

---

## What the Seal Guarantees

The seal certifies the **verification process**, not a perfect result.

**It DOES certify that:**
- All numeric fields in the response were computed by a deterministic Python engine — not generated or modified by AI
- Where AI is involved (Radar), mathematical corrections were applied before delivery
- The process is auditable and, for deterministic engines, independently reproducible

**It does NOT certify that:**
- The AI never makes mistakes
- Market data from external sources is correct
- Predictions will be accurate

> CryptoCapi actively defends against AI hallucinations through deterministic verification. We certify the process — not an absolute outcome.

---

## Three Seal Types

Each engine declares its `seal_type` in the `audit_trail`. The type tells you exactly what the hash covers:

| Engine | `seal_type` | What the hash covers | Reproducible by third parties? |
|---|---|---|---|
| **Quant Plus** | `reproducible` | Input price vector + computed outputs | **Yes** — the `audit_trail` is self-contained: recompute from the embedded inputs and compare |
| **Quant Pro** | `output_seal` | All deterministic output values | **Yes** — re-fetch the same candles from Binance and re-run; any output alteration breaks the hash |
| **Radar** | `process_seal` | Mathematical corrections applied (overrides + filters triggered) | **No** — AI-generated text is non-deterministic by nature; the hash certifies which corrections Python applied, not the prose itself |

The `seal_type` field is always present so consumers know exactly what they are verifying.

---

## Where to Find the Seal

| Engine | Location in response |
|---|---|
| **Radar** | `data.math_diagnostics.audit_trail` |
| **Quant Plus** | `data.math_diagnostics.audit_trail` |
| **Quant Pro** | `data.audit_trail` |

---

## Verifying Quant Plus (Reproducible Seal)

The Quant Plus `audit_trail` is self-contained: it carries everything needed to reproduce the result independently. No external data source is required, and you never have to ask us for anything.

**Step 1 — recompute the numbers.** From `input_vector` alone you can reproduce all three:

| Value | How |
|---|---|
| `z_score` | Logarithmic returns between consecutive prices (`ln(p[i]/p[i-1]) * 100`); take the latest return and score it against the mean and **sample** standard deviation of the previous 49. Round to 4 decimals. |
| `bollinger_bandwidth` | SMA over the last 20 prices, bands at ±2 **population** standard deviations, each band rounded to 2 decimals, then `(upper - lower) / sma`. Round to 4 decimals. |
| `market_regime` | Derived from `z_score`, `daily_change_pct` and the published `regime_thresholds`. |

**Step 2 — build the payload.** Exactly these eight keys, taken from the response as published:

```
algorithm_id, bollinger_bandwidth, daily_change_pct, engine_version,
input_timestamps, input_vector, market_regime, z_score
```

Note what is *not* in it: `calculated_at` is deliberately excluded. It is wall-clock metadata, and including it would make identical inputs produce different hashes.

**Step 3 — apply the canonical number form.** This is the one rule you cannot skip, and it is one line:

> **Every number becomes a fixed-precision decimal string with 6 decimals.**

Integers and decimals are treated **identically**: `63482` becomes `"63482.000000"`, and `-0.6651` becomes `"-0.665100"`. The reason is simple and worth knowing: JSON does not record whether a number was an integer or a decimal, so any rule that depended on that distinction could not be reproduced from a response. Booleans stay booleans, and negative zero is normalized to zero.

**Step 4 — serialize and hash.** `json.dumps(payload, sort_keys=True, separators=(",",":"))`, then `sha256` of those bytes, prefixed with `0x`. Compare against `protocol_hash`.

A match confirms the response you are holding carries exactly the inputs and outputs that were sealed at computation time.

> **Version boundary, stated plainly.** The canonical number form above applies to seals from **`v2.2.0-math`** onward (Radar `v2.2.0-radar`, Quant Pro `v1.1.0-quant`). Earlier seals serialized numbers directly, which meant a price landing on a whole number lost its decimal part in transport and the recomputed hash would not match. `engine_version` travels inside the response precisely so you can tell which rule applies to what you are holding.

A complete, live response you can run this on is committed at [`api/examples/quant-plus-signal.json`](../api/examples/quant-plus-signal.json). It is a real bitcoin insight, and its vector contains one whole-number price, so verifying it exercises the canonical rule rather than assuming it.

---

## Honest Degradation

The seal never inflates confidence. When data quality is limited, the response says so explicitly:

| Situation | What the API reports |
|---|---|
| Insufficient historical data | `data_quality: "INSUFFICIENT"`, `confidence.label: "LOW"` (capped) |
| Partial data (contingency source) | `data_quality: "PARTIAL"`, `confidence.label` capped at `"MEDIUM"` |
| Full AI chain exhausted | Insight discarded — not sent. No fabricated analysis. |

`confidence.label` is always derived from the actual data quality — never from the AI's self-assessed confidence.
