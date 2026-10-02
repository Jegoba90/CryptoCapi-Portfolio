import { z } from 'zod';
import {
  AssetIdentitySchema,
  ConfidenceSchema,
  EnvelopeSchema,
  MathDiagnosticsSchema,
  SentimentEnum,
} from './shared.schema';

// ── On-chain stats ───────────────────────────────────────────────────────────

export const OnchainStatsSchema = z.object({
  network: z.string().nullable().optional(),
  mvrv_ratio: z.number().nullable().optional(),
  exchange_netflow_usd: z.number().nullable().optional(),
  active_addresses_24h: z.number().nullable().optional(),
  whale_activity_alert: z.boolean().nullable().optional(),
  gas_price_gwei: z.number().nullable().optional(),
  network_congestion: z.enum(['LOW', 'MEDIUM', 'HIGH', 'UNKNOWN']).nullable().optional(),
  onchain_confidence_score: z.number().nullable().optional(),
});

// ── Actionable insight ───────────────────────────────────────────────────────

export const ActionableInsightSchema = z.object({
  // 'BUY_WATCH' | 'SELL_WATCH' | 'ALERT' | 'HOLD'. Typed as a string, like the
  // server's own contract, so a new value does not break your client.
  signal: z.string(),
  // 'LOW' | 'MEDIUM' | 'HIGH'
  risk_level: z.string(),
  trigger_condition: z.string(),
});

// ── Pulse view (FREE) ────────────────────────────────────────────────────────

const QuantPlusPulseDataSchema = z.object({
  engine_used: z.literal('quant_plus'),
  asset: AssetIdentitySchema,
  generated_at: z.string(),
  summary: z.string(),
  sentiment: SentimentEnum,
  statistical_anomaly_detected: z.boolean(),
});

export const QuantPlusPulseResponseSchema = EnvelopeSchema.extend({
  data: QuantPlusPulseDataSchema,
});

// ── Alpha view (PRO) ─────────────────────────────────────────────────────────
// `math_diagnostics.audit_trail` is the `reproducible` seal: it carries the
// input vector, so anyone can recompute the result (docs/SEAL.md).

const QuantPlusAlphaDataSchema = z.object({
  engine_used: z.literal('quant_plus'),
  asset: AssetIdentitySchema,
  generated_at: z.string(),
  summary: z.string(),
  sentiment: SentimentEnum,
  statistical_anomaly_detected: z.boolean(),
  confidence: ConfidenceSchema,
  math_diagnostics: MathDiagnosticsSchema,
  analysis: z.object({
    detailed_report: z.string(),
  }),
  onchain_stats: OnchainStatsSchema.optional(),
  actionable_insight: ActionableInsightSchema.optional(),
});

export const QuantPlusAlphaResponseSchema = EnvelopeSchema.extend({
  data: QuantPlusAlphaDataSchema,
});
