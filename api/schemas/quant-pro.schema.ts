import { z } from 'zod';
import { AssetIdentitySchema, AuditTrailSchema, EnvelopeSchema, SignalEnum } from './shared.schema';

// ── Timeframe block (1D / 4H) ────────────────────────────────────────────────

const ConfluenceBlockSchema = z.object({
  timeframe: z.enum(['4h', '1d']),
  confluence_score: z.number().min(0).max(100),
  signal: SignalEnum,
  candle_count: z.number().int(),
  timestamp: z.string(),
});

// ── MIR diagnostics ──────────────────────────────────────────────────────────

const MIRDiagnosticsSchema = z.object({
  base_raw_score: z.number(),
  // Fewer than 50 candles in either timeframe: the score's distance to 50 is halved.
  insufficient_data: z.boolean(),
  conviction_multiplier: z.number(),
  explanation: z.string(),
});

// ── Signal response ──────────────────────────────────────────────────────────
// `audit_trail` is the `output_seal`: it covers the deterministic outputs.

const QuantProSignalDataSchema = z.object({
  asset: AssetIdentitySchema,
  symbol: z.string(),
  resolved_signal: SignalEnum,
  resolved_score: z.number().min(0).max(100),
  mir_diagnostics: MIRDiagnosticsSchema,
  macro_1d: ConfluenceBlockSchema,
  micro_4h: ConfluenceBlockSchema,
  version: z.string(),
  audit_trail: AuditTrailSchema.optional(),
});

export const QuantProSignalResponseSchema = EnvelopeSchema.extend({
  data: QuantProSignalDataSchema,
});
