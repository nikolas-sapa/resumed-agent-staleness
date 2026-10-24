# H1 CONFIRMATION SPEC (Phase 4) — FROZEN 2026-10-07 before any confirmation run

Phase 3 pilots (v1: narrowed; v2: qualified under frozen gates) are development data. This spec
freezes the confirmatory claim, design, and decision criteria on FRESH data before any of it is
collected. Mandatory non-goals: no new research questions, no mechanism engineering beyond the
frozen arms, no additional model families beyond the two pre-registered, no benchmark expansion,
no publication or outreach. Any deviation lands in deviations.md at the time it occurs.

## Primary claim (frozen)

On fresh task instances, across 12 pre-stratified task families and two model families, agents
resuming from a summary that warns external state may have changed (provenance format) act on
superseded checkpoint conclusions at a lower paired rate than agents resuming from a plain summary
of identical content, at matched per-task token budgets, with no success loss and a token ratio
≤ 1.2×.

## Design (all arms; every contrast paired by task instance)

- Fresh instances: seeds 100–115 (12 families × 16 = 192 per deepseek cell). No v1/v2 instance
  reuse. Contact-update's mutation is redesigned to a NON-interpretable value (a full address-style
  email on a different domain), fixing the alias "correction" pathology the v2 review identified;
  this planned change is part of the frozen design, not a post-hoc fix.
- Cells (deepseek-v4-flash): changed-A (plain), changed-B (provenance), **changed-L
  (length-matched plain — neutral filler replacing provenance annotations, byte-equal total
  length; kills the "it's just longer text" confound)**, unchanged-A, unchanged-B.
  5 × 192 = 960 runs.
- **Model-generated compaction pair** (deepseek, seeds 100–103 = 48 instances): the checkpoint
  summary is produced by the model itself from a scripted prior-session log under a plain vs
  provenance compaction instruction (one extra temp-0 call per run, logged). changed-A-mc /
  changed-B-mc = 96 runs. Addresses the "scripted summaries" scope limitation of both pilots.
- **Second model family** (claude-sonnet-4-6 via the same relay, seeds 100–103): changed-A-s /
  changed-B-s = 96 runs. Sonnet sub-cap: US$10 at 2× assumed list pricing; if projections exceed
  it, sonnet cells abort and the family-generality claim is honestly narrowed.
- Total ≈ 1,152 runs. Cost projection: deepseek ≈ $1.1, sonnet ≈ $2–6 at list prices — cumulative
  cap US$50 holds with margin. Metered per call in spend-log-conf.jsonl with CELL included in
  run_id (fixes the v2 ledger collision).

## Metrics

Identical instrument to v2 (scorer2 rules, unchanged): stale-use asserted-as-current (None for
nonresponders), condition-relative success, tokens and calls per run. Primary statistic: mean
paired per-instance difference, 95% CI via family-clustered bootstrap (12 families, 10k reps,
fixed seed 31). All raw runs, summaries, world logs preserved.

## Decision criteria (frozen, applied to FRESH data only)

- **Confirmation (primary, B vs A, changed):** reduction ≥ 10 pp AND CI lower > 0 AND token ratio
  ≤ 1.2 AND success drop ≤ 3 pp → **confirmed**; CI upper < 5 pp → **refuted**; otherwise
  **not confirmed** (reported with CI).
- **Stratum replication (required for the deployable claim):** deprecated-endpoint and
  key-rotation each show point reduction > 0 on fresh data. Failure → the claim is reported as
  family-fragile with the stratum result stated.
- **Length control (L vs A, pre-registered re-scoping rule):** if L's point reduction ≥ B's
  reduction − 5 pp, the "warning content" interpretation is confounded by summary length and the
  confirmed claim re-scopes to "additional summary content, regardless of meaning".
- **Model-generated summaries (mc pair):** the scripted-summary claim generalizes to realistic
  compaction iff the mc B−A reduction is > 0 with CI excluding 0; otherwise reported as limited to
  scripted summaries.
- **Model-family generality (sonnet pair):** same rule as the mc pair.
- **Instrument controls (Phase 5):** unchanged cells must show exactly 0 stale (scorer null);
  stub-agent positive regressions must be detected; scorer v2 regression suite (43/43) re-run on
  the new instance seeds before any paid run; nonresponse guard at 15%; one re-run per infra-failed
  run, then exclusion.
- Multiplicity: one primary contrast; every other comparison is descriptive with CIs and cannot
  rescue a failed primary.

## Exclusions and stopping

Infra-failed runs: one re-run each, then excluded and listed (no exceptions, unlike v2 §7).
Batch stops only on cap breach. No outcome-based exclusions, no optional-stopping re-reads.
Analysis runs once on the complete fresh dataset; the independent hostile review re-derives
verdicts from raw logs before any result is reported.
