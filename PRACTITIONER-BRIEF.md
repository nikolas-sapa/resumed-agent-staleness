# Practitioner brief — resumed-agent staleness

## The setting

You run agents that work in sessions. Sessions get interrupted; context gets compacted into
summaries; the agent resumes later. Meanwhile the world changed — a key rotated, an endpoint was
deprecated, an owner changed.

## What we measured (deepseek-v4-flash-class agents, 1,060 fresh runs, pre-registered)

- With a plain templated summary, **~1 in 4 resumptions acted on a superseded fact as current**.
  Worst case: the agent queries the live record, sees the new value, and writes the summary's old
  value anyway. In credential- and endpoint-type tasks this happened in **essentially every run**.
- Task success dropped ~10 points in the changed-state condition vs unchanged.

## What helped (and what didn't)

| Intervention | Effect |
|---|---|
| Provenance annotations in a **templated** summary ("recorded at checkpoint; not re-verified") | **Halves stale behavior**, ~1.14× tokens, +10 pp success — confirmed |
| The same summary padded to identical length (no warning) | No effect — it's the content, not the length |
| Telling the *compaction model* to include provenance markers | **No effect** (0.0 pp ±3.1, n=96) |
| Prepending a warning header to a model-written compaction | **No effect** (0.0 pp ±3.1, n=96) |
| Forcing the compaction model to emit the full structured format | Unconfirmed lead (10.5 pp, CI includes 0) + 2/8 **refusals** when the template forces echoing secrets |

## Actionable response

1. If your harness uses **templated** checkpoint summaries, add per-fact validity provenance and a
   prominent "state may have changed" header. Cheap, measured, no success loss.
2. If your summaries are **model-generated** (most harnesses), the cheap fix is **not yet
   available** — this is the open problem. Deterministic post-processing of model compactions into
   a structured provenance format is the untested-in-this-study candidate; forcing the format at
   generation time has a demonstrated refusal cost on secret-bearing tasks.
3. Briefs that say "use the CURRENT value from the records" drove baseline stale behavior to zero
   in our task families — task phrasing is itself a lever.
4. Do not assume more tool-calling protects you: agents verified and then overwrote anyway. The
   failure is source authority, not missing verification.

## Scope

One model family (confirmed), one harness, deterministic record/file tasks, no human evaluation.
The confirmation's negative results are as decision-relevant as the positive: do not assume this
transfers to model-generated compaction or other model families without testing.
