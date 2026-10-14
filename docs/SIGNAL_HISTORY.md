# Verifiable Signal History · Anchored to Bitcoin

Every signal that Radar and Quant Plus publish leaves a **receipt** in an append-only history. Each UTC day, that day's receipts are summarized in a **manifest**, and the manifest's SHA-256 is anchored to Bitcoin with [OpenTimestamps](https://opentimestamps.org). The manifests and their proofs are public: you can check any day without asking us and without an API key.

---

## What It Proves, and What It Does Not

**It proves** that every receipt of an anchored day existed, exactly as it is, no later than the date of the Bitcoin block, and that none changed since: not a field of a row, and no receipt added, removed or reordered in its day. Not even whoever runs the database can change it without the verification failing.

**It does not prove** that a signal was right. It proves that it is the signal that was published, with the inputs and the seal it declares. To recompute a Quant Plus signal, use its `reproducible` seal ([SEAL.md](SEAL.md)).

> We certify when, not whether. A confirmed day is evidence of what was said and when, never of whether it was a good call.

---

## The Endpoints (Public, No Key)

Base URL: `https://api.cryptocapi.com/v1`. CORS is open on these three routes, so a page on any origin can call them from the browser.

| Endpoint | Returns |
|---|---|
| `GET /history/anchors` | Every anchored day, oldest first, pending days included: `day`, `status` (`pending` or `confirmed`), `row_count`, `min_id`, `max_id`, `id_order`, `manifest_sha256`, `bitcoin_block`, `stamped_at`, `confirmed_at`, `manifest_url`, `ots_url` |
| `GET /history/anchors/{day}/manifest` | That day's manifest, byte for byte (`text/plain`) |
| `GET /history/anchors/{day}/ots` | The OpenTimestamps proof of that manifest, named `manifiesto-{day}.txt.ots` |

Errors carry a machine-readable `code`: `400 INVALID_DAY` when `{day}` is not a real `YYYY-MM-DD` date, and `404 ANCHOR_NOT_FOUND` when that day is not anchored. Day D is anchored after 01:00 UTC of D+1.

These endpoints serve **no signals and no receipts**, only receipt ids and hashes. A day can be verified on its own. Verifying one receipt also needs that receipt's row, which we hand to whoever audits it.

---

## Verify a Day in a Browser

1. Pick a day from `GET https://api.cryptocapi.com/v1/history/anchors` and note its `bitcoin_block`.
2. Download its manifest and its `.ots`, from `manifest_url` and `ots_url`.
3. On [opentimestamps.org](https://opentimestamps.org), drop the **`.ots` first**, and the manifest **when it asks for it**. It must say *"Success! Bitcoin block N attests existence as of …"*, with N equal to `bitcoin_block`.

If you drop the manifest first, the page does not verify anything: it stamps the file again and downloads a new proof, which is useless here.

Prefer not to depend on the page? The official client (`pip install opentimestamps-client`) does the same with `ots verify manifiesto-2026-10-05.txt.ots`, against your own Bitcoin node.

---

## Verify a Day with the Verifier

[`tools/verificar_recibo.py`](../tools/verificar_recibo.py) is an independent implementation in Python 3.10+, standard library only. It shares no code with our backend, which builds the manifests in TypeScript. Its messages are in Spanish.

```bash
python tools/verificar_recibo.py --dia 2026-10-05
```

It downloads the list, the manifest and the proof, and checks, with no trust in what the list says:

- the manifest's shape: the v1 header, one `id leaf` line per receipt, the line count and the id order;
- that the manifest is the one of the requested day;
- that the list says the same as the files: the digest, the line count and the id order (the expected order comes from the verifier, not from the list);
- that the `.ots` proves the manifest's digest and carries a Bitcoin block attestation.

It ends with the block opentimestamps.org has to show. With a receipt row as a JSON file, it also checks the receipt:

```bash
python tools/verificar_recibo.py --dia 2026-10-05 receipt.json
```

It recomputes the receipt's leaf and finds it in the manifest, on the line of its id. With local files instead of the API: `python tools/verificar_recibo.py receipt.json manifest.txt manifest.txt.ots`.

---

## How a Day Is Built (Format v1)

The **manifest** is UTF-8 text. The first line is `cryptocapi-signal-ledger v1 day=YYYY-MM-DD rows=N`; then one line `id leaf` per receipt recorded in `[day 00:00, day+1 00:00)` UTC, in numeric id order. Every line ends in LF, the last one too. A day with no receipts is the header alone, with `rows=0`.

The **leaf** is the SHA-256 of the receipt row in canonical JSON ([RFC 8785, JCS](https://www.rfc-editor.org/rfc/rfc8785)):

- the 17 columns, sorted by name, no whitespace;
- `id` and `insight_id` as integers;
- `z_score` and `confidence` as ECMAScript numbers (`2`, not `2.0`; `1e-7`, not `1e-07`);
- every other column as a string;
- `null` written out.

The **proof** is an OpenTimestamps file proof over the manifest's bytes. A day turns `confirmed` when a calendar returns the attestation of a Bitcoin block.

---

## Things to Know

- **The 2026-09-30 exception.** It is the only day anchored outside v1: its lines are in id order **as text** (`1`, `10`, `100`, …, `99`), because of a bug fixed on 2026-10-13. The anchor is confirmed and cannot be changed. Its proof still holds, because a receipt is looked up by its id. The list says so in the data (`id_order: "text"`), its `max_id` is 99 (the last line) rather than the day's highest id (166), and the verifier accepts that order for that day only.
- **The proven date is the block's, not the day's.** Days are anchored after 01:00 UTC of the next day. The days up to 2026-10-11 were anchored late, in one batch, when automatic anchoring started on 2026-10-12 (2026-10-05 on 2026-10-13), so their block is later than the day.
- **One byte changes everything.** If the manifest goes through anything that converts line endings (LF to CRLF), its digest changes and it no longer verifies. Download it and use it as is.
