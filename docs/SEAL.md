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

**How the 6 decimals round.** Half to even, on the exact binary value of the number: what Python's `format(x, '.6f')` and C's `printf("%.6f")` do. `0.0078125` becomes `"0.007812"`, and `0.0234375` becomes `"0.023438"`. JavaScript's `toFixed(6)` rounds an exact tie up instead (`"0.007813"`), so it does not reproduce the seal. Ties are common in practice: the price feed delivers float32 values, which at bitcoin's level are multiples of 1/128 or 1/256, and every odd multiple of 1/128 has exactly seven decimals ending in 5. Whenever prices travel at full precision, about half of bitcoin's are exact ties.

**Step 4 — serialize and hash.** `json.dumps(payload, sort_keys=True, separators=(",",":"))`, then `sha256` of those bytes, prefixed with `0x`. Compare against `protocol_hash`.

`json.dumps` escapes every character outside printable ASCII as `\uXXXX` with lowercase hex, and that is part of the bytes: the Quant Plus `algorithm_id` contains a sigma (`σ`), which is hashed as `\u03c3`. `JSON.stringify` keeps it as is, so in JavaScript the escape has to be applied by hand.

A complete reference in JavaScript (any modern browser, or Node 19+), with both rules:

```js
// Six decimals, rounded half to even on the exact value of the double: what
// Python's format(x, '.6f') does. toFixed(6) rounds exact ties up instead.
function fixed6(x) {
  if (x === 0) return '0.000000'; // also -0
  const view = new DataView(new ArrayBuffer(8));
  view.setFloat64(0, Math.abs(x));
  const bits = view.getBigUint64(0);
  const biased = Number((bits >> 52n) & 0x7ffn);
  const fraction = bits & ((1n << 52n) - 1n);
  const mantissa = biased === 0 ? fraction : fraction | (1n << 52n);
  const exponent = (biased === 0 ? 1 : biased) - 1075;
  let num = mantissa * 1000000n;
  let den = 1n;
  if (exponent >= 0) num <<= BigInt(exponent);
  else den <<= BigInt(-exponent);
  let q = num / den;
  const twice = 2n * (num % den);
  if (twice > den || (twice === den && q % 2n === 1n)) q += 1n;
  const digits = q.toString().padStart(7, '0');
  return (x < 0 ? '-' : '') + digits.slice(0, -6) + '.' + digits.slice(-6);
}

// Step 3: every number to its 6-decimal string, keys sorted.
function canonical(value) {
  if (typeof value === 'number') return fixed6(value);
  if (Array.isArray(value)) return value.map(canonical);
  if (value !== null && typeof value === 'object') {
    const out = {};
    for (const key of Object.keys(value).sort()) out[key] = canonical(value[key]);
    return out;
  }
  return value;
}

// Step 4: compact JSON, non-ASCII escaped like Python, then SHA-256.
async function sealHash(payload) {
  const json = JSON.stringify(canonical(payload)).replace(
    /[\u007f-\uffff]/g,
    (c) => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0'),
  );
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(json));
  return '0x' + [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

// payload = the eight keys of step 2, taken from the response as published.
// (await sealHash(payload)) === audit_trail.protocol_hash
```

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
