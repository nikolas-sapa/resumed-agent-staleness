# H1 PILOT v2 SPEC — FROZEN 2026-10-07 before any paid v2 call

Pre-registration for the corrected pilot. v1 artifacts, spec, and analysis remain published and
untouched. v2 fixes every defect the hostile review established (see deviations.md): scorer asserts
superseded values *as current* (S1); nonresponders excluded from stale denominators (S2);
condition-relative, path-tolerant success (S3); discoverable `query_records` (W1); brief staleness
hints removed from two families and promoted to a measured arm (D1); family-clustered bootstrap
from the start.

## Design

- Model `deepseek-v4-flash` (VyceAI relay), temperature 0, turn cap 12, max_tokens 1024/turn.
- 96 task instances (12 families × 8 seeds), identical across cells (paired by instance).
- **6 cells × 96 = 576 runs:**
  | Cell | State | Summary | Brief |
  |---|---|---|---|
  | changed-A | changed | plain | plain |
  | changed-B | changed | provenance | plain |
  | changed-C | changed | plain + "re-verify" instruction | plain |
  | changed-H | changed | plain | brief + staleness hint |
  | unchanged-A | unchanged | plain | plain |
  | unchanged-B | unchanged | provenance | plain |
- Provenance summaries (B) are content-identical to plain (A) plus per-fact validity provenance;
  C adds an explicit re-verify instruction; H leaves the summary plain and adds the hint line to
  the task brief. Arm cost differences are metered (tokens and calls per run).

## Metrics

- **Stale-use** (S1 rules; None for nonresponders), **success** (S3 condition-relative), tokens and
  calls per run, re-verification rate, nonresponder rate.
- Primary statistic for every contrast: mean paired per-instance difference; 95% CI via
  **family-clustered bootstrap** (12 families, 10k resamples, fixed seed).

## Pre-registered contrasts and decision rules

1. **V2a phenomenon (descriptive, no contrast claim):** changed-A stale rate with per-family
   breakdown; unchanged-A/B reported as scorer specificity controls only (unchanged stale is 0 by
   construction — NOT an effect size).
2. **V2b primary intervention contrast (B vs A, changed):**
   - **Qualify for confirmation planning** iff: point reduction ≥ 10 pp AND family-clustered CI
     lower bound > 0 AND mean token ratio B/A ≤ 1.2 AND success change > −3 pp.
   - **Killed as intervention** iff CI upper bound < 5 pp.
   - Otherwise: narrowed (≥5 pp point, CI straddling or gates failing) / inconclusive (<5 pp point,
     CI straddling).
3. **V2c mechanism (C vs B, changed, descriptive):** does a bare re-verify instruction differ from
   provenance content? No gate; reported with CI.
4. **V2d hint locus (H vs B, changed, descriptive):** brief-hint vs summary-provenance. No gate.
5. **Nonresponse guard:** any arm with nonresponder rate > 15% is flagged as a design defect and its
   contrasts labeled with the caveat.

## Validity gates before the kill batch

1. Scorer v2 validation (no paid calls): 43/43 required — synthetic behaviors, all 19 hand-verified
   v1 false positives as regression negatives, verified v1 true positives still positive, 3 success
   path-flips fixed, nonresponder binning. **PASSED 2026-10-07 (43/43).**
2. Probe: 8 changed-A paid runs — tool behavior, per-run cost, throughput; full batch must project
   ≤ $15 even at 10× price stress to launch.
3. Cumulative cap US$50 across v1+v2, enforced by metered ledger (v1: $0.52 at 1× / $5.17 at 10×;
   v2 projection ≈ $0.9 at 1× / $9 at 10×).

## Exclusions, stopping, analysis discipline

- Infra-failed runs: one re-run each, then excluded and listed. No outcome-based exclusions.
- No optional-stopping re-reads; the batch runs to completion (cap breach excepted).
- All raw runs, both summaries, world logs, and the metered ledger are preserved per run.
- Deviations from this spec go in deviations.md at the time they occur.
- Independent hostile review re-derives verdicts from raw logs before the result is reported.
