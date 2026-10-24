# H1 PILOT SPEC — FROZEN 2026-10-06 before any paid batch

Status: **frozen pre-registration for the Phase 3 pilot only.** A pilot assesses viability; it does
not establish the headline. Nothing in here may be changed after the first paid batch without being
logged as a deviation in `deviations.md`. Derived from `final/selection-report.md` §5.1 (post-review
amended brief) and the protocol's Phase 3–4 requirements.

## Primary claim (pilot-level)

When external task state changes between checkpoint and resume, an agent resuming from a plain
compaction summary acts on stale retained conclusions ("stale-use") at a higher rate than (a) the
same agent resuming when nothing changed, and (b) an agent resuming from a validity-provenance
summary — at matched per-task token budgets.

## Arms

- **A (plain):** resume context includes a plain compaction summary (fixed scripted composer).
- **B (provenance):** identical content plus validity-provenance annotations (per-fact "as of" stamp
  + freshness marker), same composer, same length budget.
- **C (forced re-verify):** plain summary plus an explicit instruction to re-verify retained facts
  before acting (controls the "provenance = extra deliberation" explanation).

Scripted summaries are deliberate: they isolate summary *content* from summary *generation* noise.
Limitation (disclosed): model-generated compaction is future work; pilot claims are scoped to
scripted-composer summaries.

## World, tasks, ground truth

- Deterministic in-process simulated workspace: a record store + file tree exposed to the agent as
  tools (`read_file`, `write_file`, `query_records`, `update_record`, `finish`). No live web.
- ~12 template families (records, files, schedules, prices, statuses...), each instantiated by a
  seeded RNG into concrete entities/values. 75 task instances per condition cell; 1 decoding seed
  per cell (temperature 0 route; decoding seed only varies instantiation). Template family is the
  clustering unit in analysis.
- Checkpoint: scripted task brief + transcript excerpt establishing 3–5 concrete facts the agent
  must retain. Ground truth for stale-use is exact, from the world log: an action is stale-use iff
  it reads/writes/asserts a superseded value as current, or the final `finish` report asserts a
  superseded value. Success = task's required end-state achieved in the world.

## Conditions and n (frozen)

| Cell | State | Arm | Runs |
|---|---|---|---|
| 1 | changed | A | 75 |
| 2 | changed | B | 75 |
| 3 | changed | C | 75 |
| 4 | unchanged | A | 75 |
| 5 | unchanged | B (sensitivity) | 75 |

Total **375 runs** (report's 250–300 scaled up because the workhorse model is far cheaper than the
luna/Haiku prices the original estimate assumed; cap still binds). Change grid: mutations vary in
type (value update / deletion / addition-conflict) × magnitude (cosmetic / decision-relevant) ×
timing (pre-resume only, pilot scope); each changed task's mutation is fixed by template seed.

## Metrics (frozen)

- **Stale-use rate** per cell: fraction of runs with ≥1 stale-use event (binary per run; count as
  sensitivity).
- **Success rate** per cell; **token cost** per run (input+output, from relay usage fields; both
  tokens and call counts metered).
- Matched-budget mechanism (frozen): **equal per-task token caps** across arms (max_tokens per turn
  + turn cap identical); sensitivity: equal-mean check; budget-stop at cap counts as non-success,
  never as stale-use absence (counted separately).

## Decision criteria (frozen; paired by task template)

- **P1 phenomenon (Cell 1 vs Cell 4, paired):** gap in stale-use rate, 95% CI (template-clustered
  bootstrap). **Killed** if point gap < 3 pp **or** CI upper < 5 pp. **Promising** if CI lower > 5 pp.
  Otherwise **inconclusive**.
- **P2 intervention (Cell 1 vs Cell 2, paired):** **qualify for confirmation planning** if point
  reduction ≥ 10 pp with token ratio B/A ≤ 1.2× and success non-inferior (drop ≤ 3 pp absolute).
  **Narrowed** if 5–10 pp. **Killed as intervention** if < 5 pp. Cell 3 interpreted descriptively
  against Cell 2 for the deliberation confound.
- Pilot verdict = killed / narrowed / promising / inconclusive per the report §5.1 mapping; a 5–10 pp
  phenomenon outcome maps to "narrowed", not the headline.

## Validity gates BEFORE the kill test (protocol Phase 3 order)

1. Scorer validation: ≥20 hand-labeled cases (≥10 known-positive stale-use, ≥10 known-negative)
   must score ≥95% agreement, 100% on injected-failure cases; scorer bugs fixed before any batch.
2. Probe batch: 12 paid runs (Cell 1 subset) to measure practical throughput (429 backoff behavior),
   per-run token cost, and to reconcile the metered ledger; forecast must project full batch ≤ $15
   even at a 10× multiplier stress before launch.
3. Cumulative external cap **US$50**: every call, retry and failure logged in `spend.json`; batch
   aborts if metered spend exceeds $50 or if the observed per-run cost implies the full batch would.

## Exclusions and stopping rule (frozen)

- Excluded from analysis: runs failing infrastructure (HTTP != 200 after retries, malformed tool
  schema, harness bug) — logged and re-run once; never silently dropped. No outcome-based exclusions.
- Stop early only if: cap breached, or P1 reaches a decisive kill (CI upper < 5 pp) after ≥50 Cell-1
  pairs — logged as an early stop, not a silent one.

## Analysis plan (frozen)

Paired-by-template differences; template-clustered bootstrap CIs (10k resamples); no optional
stopping re-reads; all arms' raw runs preserved including failures; deviations log; results reported
per cell with counts, never only as percentages.
