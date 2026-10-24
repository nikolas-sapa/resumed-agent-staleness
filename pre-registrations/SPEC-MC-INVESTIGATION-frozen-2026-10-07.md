# MC INVESTIGATION SPEC — FROZEN 2026-10-07 before any paid run

Question: why did provenance warnings fail when summaries are model-generated (mc null:
-0.0pp [-8.57, 9.68] on 32 pairs) while scripted provenance summaries confirm at 13.48pp?
Adherence and fidelity are verified (41/41, 41/41, 0/37 contamination) — the null is real at n=32.

## Cells (deepseek-v4-flash, changed condition, seeds 100-107 = 96 instances per cell)

| Cell | Summary construction |
|---|---|
| changed-A-mc (extend to 96) | model compaction, plain instruction (existing arm extended) |
| changed-B-mc (extend to 96) | model compaction, provenance instruction (existing arm extended) |
| changed-S-mc (new, 96) | model compaction with instruction to emit EXACTLY the scripted provenance format (prominent header + per-fact "(as of checkpoint; not re-verified)") |
| changed-A-app (new, 96) | model's own plain compaction, with the scripted provenance HEADER prepended deterministically (no other change) |

## Pre-registered contrasts (paired by instance, family-clustered bootstrap, seed 41)

- **M1 (power check):** B-mc vs A-mc at ~96 pairs. If reduction CI now excludes 0 -> the mc
  effect is real and v2's null was underpowered; if the null persists with a tighter CI -> the
  transfer failure is confirmed.
- **M2 (structure):** S-mc vs A-mc. Reduction > 0 with CI excluding 0 -> structure of the warning
  (prominent header) is the active ingredient for model-generated summaries.
- **M3 (header-only):** A-app vs A-mc. Same rule -> a deterministic warning header appended to ANY
  compaction suffices; authorship voice is irrelevant.
- Interpretation matrix: M3 works + M1 null -> practical fix identified ("prepend a warning header
  to any compaction"); M2 works + M3 fails -> full structured provenance required; neither works ->
  model-voice compaction genuinely resists the intervention; boundary claim stands.
- No gates ride on these beyond the stated rules; the primary confirmation result is unaffected
  regardless of outcome.

## Budget and discipline

384 runs ≈ $0.45 at official prices; cumulative cap binding (currently $3.07). One re-run per
infra-failed run, then excluded and logged. No optional stopping; analysis once; hostile review
before the result is reported. Deviations land in deviations.md immediately.
