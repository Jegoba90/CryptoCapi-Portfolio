import { z } from 'zod';

// Response shapes of the CryptoCapi API v1, as of engine v2.3.0 (2026-10-01).
// They are not strict: a field the API adds later does not break a client that
// validates with them.

// ── Envelope base ────────────────────────────────────────────────────────────

export const EnvelopeSchema = z.object({
  status: z.literal('success'),
  version: z.literal('1.0.0'),
  // On the insight routes it is when the analysis was computed; on /quant/* it
  // is when the response was sent. To know how old an analysis is, read
  // `generated_at` instead: it means the same thing on every route.
  timestamp: z.string(),
});

// ── Primitives ───────────────────────────────────────────────────────────────

export const AssetIdentitySchema = z.object({
  id: z.string(),
  symbol: z.string(),
});

export const SentimentEnum = z.enum(['bullish', 'bearish', 'neutral']);

export const ConfidenceSchema = z.object({
  score: z.number().min(0).max(1),
  label: z.enum(['LOW', 'MEDIUM', 'HIGH']),
});

// Quant Pro signal, per timeframe and resolved.
export const SignalEnum = z.enum([
  'STRONG_BUY',
  'BUY',
  'NEUTRAL_CHOP',
  'SELL',
  'STRONG_SELL',
]);

export const MarketRegimeEnum = z.enum([
  'BULLISH_TREND',
  'BEARISH_TREND',
  'RANGING_CHOP',
  'EXTREME_VOLATILITY',
  'UNUSUAL_VOLATILITY',
]);

export const DataQualityEnum = z.enum(['OPTIMAL', 'PARTIAL', 'INSUFFICIENT']);

// ── Verifiable seal (audit_trail) ────────────────────────────────────────────
// Emitted by the three engines. Only `protocol_hash` and `calculated_at` are
// common to the three seal types; the rest depends on the engine. How to
// verify it: docs/SEAL.md.

export const AuditTrailSchema = z.object({
  protocol_hash: z.string(),
  calculated_at: z.string(),
  seal_type: z.enum(['reproducible', 'output_seal', 'process_seal']).optional(),
  algorithm_id: z.string().optional(),
  engine_version: z.string().optional(),
  // Quant Plus (`reproducible`): everything needed to recompute the result.
  data_source: z
    .object({
      vendor: z.string(),
      symbol: z.string(),
      timeframe: z.string(),
    })
    .optional(),
  input_timestamps: z.array(z.string()).optional(),
  input_vector: z.array(z.number()).optional(),
  zscore_window_size: z.number().optional(),
  daily_change_pct: z.number().nullable().optional(),
  // Radar (`process_seal`): what Python corrected on the model's output.
  filters_applied: z.array(z.string()).optional(),
  fields_overridden: z.array(z.string()).optional(),
  sentiment_override: z.boolean().optional(),
});

// ── Math diagnostics (Radar and Quant Plus, PRO view) ────────────────────────

export const MathDiagnosticsSchema = z.object({
  z_score: z.number(),
  // The anomaly boundary the engine used (t-Student critical value).
  z_score_threshold: z.number(),
  bollinger_bandwidth: z.number(),
  market_regime: MarketRegimeEnum,
  extreme_volatility_detected: z.boolean(),
  data_quality: DataQualityEnum,
  data_quality_reason: z.array(z.string()),
  sentiment_override: z.boolean(),
  anomaly_details: z.string().nullable(),
  regime_thresholds: z.record(z.string(), z.number()).optional(),
  audit_trail: AuditTrailSchema.optional(),
});
