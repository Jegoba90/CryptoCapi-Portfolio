import { z } from 'zod';
import {
  AssetIdentitySchema,
  ConfidenceSchema,
  EnvelopeSchema,
  MathDiagnosticsSchema,
  SentimentEnum,
} from './shared.schema';

// ── Source (news article reference) ─────────────────────────────────────────

const SourceSchema = z.object({
  title: z.string(),
  url: z.string().url(),
  credibility: z.enum(['Tier 1', 'Tier 2', 'Tier 3']),
});

// ── Pulse view (FREE) ────────────────────────────────────────────────────────

const RadarPulseDataSchema = z.object({
  engine_used: z.literal('radar'),
  asset: AssetIdentitySchema,
  generated_at: z.string(),
  summary: z.string(),
  sentiment: SentimentEnum,
  statistical_anomaly_detected: z.boolean(),
});

export const RadarPulseResponseSchema = EnvelopeSchema.extend({
  data: RadarPulseDataSchema,
});

// ── Alpha view (PRO) ─────────────────────────────────────────────────────────
// `math_diagnostics.audit_trail` is the `process_seal`.

const RadarAlphaDataSchema = z.object({
  engine_used: z.literal('radar'),
  asset: AssetIdentitySchema,
  generated_at: z.string(),
  summary: z.string(),
  sentiment: SentimentEnum,
  statistical_anomaly_detected: z.boolean(),
  confidence: ConfidenceSchema,
  math_diagnostics: MathDiagnosticsSchema,
  analysis: z.object({
    detailed_report: z.string(),
    sources_verified: z.array(SourceSchema),
    sources_window: z.string(),
  }),
});

export const RadarAlphaResponseSchema = EnvelopeSchema.extend({
  data: RadarAlphaDataSchema,
});
