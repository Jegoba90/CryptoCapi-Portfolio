# Authentication — CryptoCapi API v1

Base URL: `https://api.cryptocapi.com/v1`

---

## Overview

CryptoCapi uses two independent auth layers. Which one you need depends on the endpoint:

| Layer | Header | When to use |
|---|---|---|
| **API Key** | `x-api-key: <your-key>` | Programmatic data access (PRO endpoints) |
| **Firebase Token** | `Authorization: Bearer <id-token>` | Account management, trial activation, payments |

Most data endpoints only need an API key. Firebase tokens are required only when managing your account (getting your key, activating a trial, paying).

---

## API Keys

Every account key looks like `sk_live_<id>.<secret>`, whatever its plan. **The prefix does not tell you the plan**: the plan and the engine a key covers are attributes the server keeps for it (see Entitlement below).

| Key | Plan | Access |
|---|---|---|
| `sk_live_…` with an active pass | **PRO** | Deep analysis and `audit_trail` for **the engine that pass covers** |
| `sk_live_…` without one | **Free / Pulse** | Public data + Pulse View (summaries only, numeric fields stripped) |
| `demo_btc_eth_public` | **Demo** | Shared public key. Radar and Quant Plus for `bitcoin`/`ethereum` only, full Alpha payload |

Keys are obtained via `GET /payments/me` after authenticating with Firebase. The demo key requires no account at all: it is published as-is.

---

## Plans

### Demo (public key, no signup)
- One shared public key for instant testing: `demo_btc_eth_public`.
- Works **only** for `bitcoin` and `ethereum`, and only on the Radar and Quant Plus routes: `/market/insights/:id` (also with `?engine=quant_plus`), `/quant-plus/:id/signal` and `POST /quant/batch`. It always returns the **full Alpha payload**, including the `audit_trail` seal.
- Any other coin returns `403 DEMO_COIN_RESTRICTED`. Quant Pro (`/quant/:symbol/signal`) and Market Scan (`/quant/market-scan`) need a key with their own pass.
- Rate limit: **30 requests / hour**, scoped per IP so one abuser cannot exhaust the shared key.

```http
GET /v1/market/insights/bitcoin?view=alpha
x-api-key: demo_btc_eth_public
```

### Free (Pulse View)
- No payment required. A key is created on registration; new accounts start with the 14-day trial (below), and when it ends the key stays on Free.
- Access to all public market endpoints.
- Insights endpoint (`/market/insights/:id`) returns **Pulse View**: summary text only. Fields like `math_diagnostics`, `analysis`, and `confidence` are omitted from the response (not sent as `null`).
- Rate limit: **1,000 requests / hour**.

### PRO (Alpha / Deep Alpha)
- Activated by trial or PayPal pass.
- Unlocks deep analysis for **the engine that pass covers**, not for all four. See Entitlement below.
- For that engine, the insights endpoint returns the complete payload including `math_diagnostics`, `confidence`, and the `audit_trail` seal.
- The 14-day trial is the exception: it is meant to show the whole product, so it opens every engine for its duration.
- Rate limit: **10,000 requests / hour**.

#### 14-Day Free Trial
No card required. It turns your key into PRO for 14 days, with every engine open. Accounts created from the dashboard activate it with:
```
POST /payments/trial
Authorization: Bearer <firebase-id-token>
```

#### PRO Pass (30 days)
Purchased via PayPal. Activates or renews your `sk_live_` key for 30 days.

---

## Making Authenticated Requests

### API Key (most endpoints)
```http
GET /v1/quant/BTCUSDT/signal
x-api-key: sk_live_x8F9…
```

### Firebase Token (account endpoints)
```http
GET /v1/payments/me
Authorization: Bearer eyJhbGciOiJSUzI1NiIs…
```

---

## Public Endpoints (no authentication required)

These endpoints return data to any caller with no key:

| Endpoint | Description |
|---|---|
| `GET /market/prices/latest` | Real-time prices, top assets |
| `GET /market/market-summary` | Global market cap, BTC dominance, Fear & Greed |
| `GET /market/market-history` | Historical market cap snapshots |
| `GET /market/assets/:id` | Asset detail (description, ATH/ATL, supply) |
| `GET /market/macro` | Macro indicators (Fed rate, CPI, DXY, M2) |
| `GET /market/global-inflation` | CPI by country (World Bank) |

---

## PRO-Only Endpoints

These require a key whose pass covers the engine (the demo key reaches the Radar and Quant Plus ones for `bitcoin` and `ethereum`):

| Endpoint | Description |
|---|---|
| `GET /market/insights/:id?view=alpha` | Radar insight (or Quant Plus with `&engine=quant_plus`), full Alpha payload + `audit_trail` |
| `GET /quant-plus/:id/signal?view=alpha` | Quant Plus signal, full Alpha payload + `audit_trail` |
| `GET /quant/:symbol/signal` | Quant Pro dual-timeframe signal (live Binance data) |
| `GET /quant/market-scan` | Market Scanner, ranked signals by strategy |
| `POST /quant/batch` | Quant Plus batch signals for multiple assets |

Free keys can call `/market/insights/:id` but receive **Pulse View**: a reduced payload without numeric diagnostics.

---

## Rate Limits

Limits are enforced per API key on a fixed one-hour window that resets at the top of each hour (UTC), with an additional burst guard:

| Plan | Hourly limit | Burst limit |
|---|---|---|
| Demo (`demo_btc_eth_public`) | 30 req / hour (per IP) | 5 req / 2 seconds |
| Free | 1,000 req / hour | 20 req / 2 seconds |
| PRO | 10,000 req / hour | 20 req / 2 seconds |

### Response Headers

Every response from a keyed endpoint includes:

```
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9847
X-RateLimit-Reset: 1718200000
```

`X-RateLimit-Reset` is a Unix timestamp (seconds) indicating when the current window resets.

### 429 Too Many Requests

When a limit is exceeded the API returns `429` with a `Retry-After` header (seconds) and this body:

```json
{
  "status": "error",
  "message": "Too Many Requests. Rate limit exceeded."
}
```

It carries no `code`: branch on the `429` status and wait out `Retry-After`.

---

## Entitlement: one pass per engine

Access is decided by **two independent attributes**, and confusing them is the classic mistake:

| Attribute | Question it answers | Values |
|---|---|---|
| **plan** | Is this key paid and current? | `free`, `pro`, `internal`, `demo` |
| **product** | Which engine was bought? | `pulse`, `alpha`, `quant`, `quant_plus`, `market_scan` |

The four products are sold separately, so **buying one engine grants exactly that engine**. Holding Quant Pro does not open Quant Plus. This is enforced server-side on every route, not in the client.

It also applies *within* a single endpoint: `GET /market/insights/:id` serves two different engines depending on `?engine=`, and each one requires its own pass (`alpha` for Radar, `quant_plus` for Quant Plus).

### The two error codes, and why there are two

A missing pass returns `403` naming the exact product, with a machine-readable `code` so you never have to parse prose:

| `code` | Meaning | What to do |
|---|---|---|
| `PRODUCT_NOT_INCLUDED` | This key never included that engine | Buy that pass. Retrying with the same key fails identically. |
| `PRODUCT_NOT_ACTIVE` | This key **does** hold that engine, but the pass lapsed | **Renew.** You already own it. |

A real response, captured from production with the public demo key:

```json
{
  "status": "error",
  "message": "Your API key does not include this engine. Required product: 'market_scan'.",
  "code": "PRODUCT_NOT_INCLUDED",
  "required_product": "market_scan"
}
```

`required_product` is always present. `your_product` is added when the key holds *some other* engine, so a client can say "you have Quant Pro, this needs Market Scan" without a second request. It is absent above because the demo key has no product attributed to it.

Branch on `code`, never on the message text. The distinction between the two exists because telling somebody with an expired pass that their key "does not include" the engine is false, and it sends them to buy something they already own.

---

## Payload Shaping by Key Tier

> This section applies **only to `GET /market/insights/:id`**. The other engines (Quant Plus, Quant Pro, Market Scan) have no reduced-payload fallback: without the right pass they return `403` with a `code`, as described in Entitlement above.

The `/market/insights/:id` response structure changes based on your key. **Do not assume missing fields are `null`** — they are simply absent in the free tier. Use optional chaining:

```typescript
// Safe — works for both Pulse and Alpha responses
const score = data.confidence?.score;
const zScore = data.math_diagnostics?.z_score;
```

| Field | Free (Pulse) | PRO (Alpha) |
|---|---|---|
| `summary` | ✅ | ✅ |
| `sentiment` | ✅ | ✅ |
| `analysis` | ❌ omitted | ✅ |
| `math_diagnostics` | ❌ omitted | ✅ |
| `confidence` | ❌ omitted | ✅ |

---

## Error Reference

Every error body has `status: "error"` and a `message`. Some also carry a `code`: branch on it when it is there, never on `message`. The ones without a `code` are told apart by their HTTP status.

| HTTP Code | `code` | Meaning |
|---|---|---|
| `401` | none | Missing or invalid API key / Firebase token |
| `403` | `PRODUCT_NOT_INCLUDED` | This key never included that engine (see Entitlement) |
| `403` | `PRODUCT_NOT_ACTIVE` | This key holds that engine, but the pass lapsed |
| `403` | `DEMO_COIN_RESTRICTED` | Demo key used on a coin other than `bitcoin`/`ethereum` |
| `403` | none | Invalid, revoked or inactive key, invalid Firebase token, or a Free key asking for `view=alpha` |
| `429` | none | Hourly or burst limit exceeded; see `Retry-After` |
