# Resumed agents act on stale summary facts as current — and what does and does not fix it

**Technical report · October 2026 · status: complete, unreleased (private draft pending owner approval)**

## Central claim (restrained)

When a deepseek-v4-flash-class agent resumes a task from a templated checkpoint summary and the
world has moved on since the checkpoint, the agent writes or asserts the summary's superseded
value as current in **~24% of runs** (up to 100% in credential- and endpoint-type task families) —
including cases where it queries the live record, observes the current value, and overwrites it
with the summary's stale value anyway. Appending per-fact validity provenance to that templated
summary ("recorded at checkpoint; not re-verified") **roughly halves** this behavior (paired
reduction 13.48 pp, family-clustered 95% CI [1.09, 31.25]) at **1.14× token cost** with a
**+10 pp success gain**. This is established on fresh, pre-registered instances with an
independently re-derived scorer.

## What this does NOT establish

1. **Model-generated compaction summaries** (the realistic deployment case): provenance
   *instructions* change nothing (0.0 pp, CI ±3.12, n=96); deterministically *prepending* the
   warning header to a model compaction changes nothing (0.0 pp, CI ±3.12, n=96); forcing the
   model to emit the full structured format is an **unconfirmed lead** (10.53 pp, CI [−1.04, 27.96];
   9.57 pp excluding a compaction refusal) with a demonstrated **2/8 refusal cost** when the
   template forces echoing credential values.
2. **claude-sonnet-4-6**: direction consistent (16.2% → 7.3%) but not established (3.12 pp,
   CI [−0.00, 10.71], n=32 pairs).
3. **Task-family breadth**: 8 of 12 families sit at zero baseline stale because their briefs
   already instruct "use the CURRENT value from the records" — the effect exists where the brief
   does not pre-warn, concentrated in deprecated-endpoint (15/15→3/14) and key-rotation
   (14/15→3/16). Contact-style records are immovable (16/16 vs 14/14 stale even with warnings).
4. One harness, one task domain (deterministic record/file simulations), scripted or forced
   summaries, no human evaluation.

## Mechanism reading (supported by transcripts, not proven by intervention)

Verification does not prevent stale writes: 95–96% of runs in *every* arm query before acting.
Warnings work by changing **which source wins on conflict** — in plain-summary runs the model
explicitly reasons "the record says X, but the summary says Y" and overwrites fresh evidence.
The finding is therefore about summary authority, not agent laziness. (Caveat: the mc arms show
the authority flip is not triggered by the *mere presence* of warning text in model-voiced
summaries — format and framing matter in ways this study bounds but does not fully explain.)

## Claim-to-evidence map

| Claim | Evidence | Independent check |
|---|---|---|
| Stale-use phenomenon, ~24% baseline | `analysis-conf.json` cell_rates.changed-A (48/187) | Reviewer re-scored all 1,060 runs, 0 mismatches |
| Warning halves it | `analysis-conf.json` V2b_primary (13.48 pp, CI [1.09, 31.25]) | Bootstrap 20-seed sweep; exclusion imputation 9.90–14.07 pp |
| Not summary length | `analysis-conf.json` length_control (byte-equal filler arm: 3.31 pp) | Byte-equality recomputed 192/192 by reviewer |
| Not verification deficit | reverified saturated in all arms (disclosed, demoted metric) | Transcript audit |
| Family concentration | `analysis-conf.json` stratum_replication | Reviewer per-family recomputation |
| mc transfer failure | `analysis-mc.json` M1/M3 (0.0 pp ±3.12 at n=96 each) | Reviewer re-scored all 384 runs, 0 mismatches; adherence corrected |
| Refusal cost of forced-format compaction | `analysis-mc-exploratory.json` (2/8 key-rotation refusals) | Reviewer transcript verification |
| Success gain, no success loss | confirmation success 72.3%→82.5%; outcome-only 79.6%→86.3% | Reviewer audit incl. 3 path-dependence fixes (v2) |

## Provenance and integrity

Pre-registered specs frozen before any paid run (`SPEC-CONFIRMATION-frozen-2026-10-07.md`,
`SPEC-MC-INVESTIGATION-frozen-2026-10-07.md`); all deviations logged (`deviations.md` §1–22),
including two protocol breaches (partial recovery pass; retroactive deviations sections) and one
withdrawn exploratory claim (compliance-dilution). Three independent hostile reviews re-derived
verdicts from raw logs (v2: all 576 runs; confirmation: all 1,060; mc: all 384) — total 12 verdict
mismatches found and corrected across the project, none remaining. All ~2,600 raw runs with full
transcripts, world logs, and per-call metered spend (~US$3.5 total) are preserved.

## Reproduction

Environment: Python 3.12+, macOS arm64 (any), network access to an Anthropic-compatible relay.
`pilot/harness/` contains the full instrument (task generator with exact ground truth, scorer,
runners, frozen analyses). Entry points: `python3 -m harness.conf_validate` (58/58 pre-flight),
`python3 -m harness.run_conf --all` (confirmation grid), `python3 -m harness.analyze_conf`.
Estimated full replication cost at official peak prices: ≈ US$2.5–4 (relay-dependent).

## Limitations of this report

Single research effort, single harness, one cheap model family for the primary result; the second
model family and the realistic compaction case both failed to confirm. No external replication.
Reviewer independence is same-model separate-context (hostile drafting + full re-derivation), not
independent laboratories. Recognition-worthy claims should be treated as hypotheses for
independent reproduction, not settled findings.
