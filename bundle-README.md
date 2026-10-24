# Resumed-agent staleness — replication bundle

Raw data, harness, pre-registrations, analyses, and logs for the study "Resumed agents act on
stale summary facts as current — and what does and does not fix it" (October 2026).

## Contents
- `harness/` — full instrument: deterministic task generator with exact ground truth (12 task
  families), stale-use/success scorers (v1/v2), relay client with metered ledger, batch runners,
  frozen analyses, validation suites.
- `runs/`, `runs-v2/`, `runs-conf/` — every episode: full transcript, tool calls, world state,
  world log, per-call usage. 2,631 runs total across four studies (pilot 370, v2 575,
  confirmation 1,060, mc investigation 384; plus excluded-infra artifacts preserved).
- `spend-log*.jsonl` — per-call metered spend (~US$3.5 total at official prices).
- `SPEC-*.md` — the three pre-registrations, frozen before each paid batch.
- `analysis*.json` — frozen primary analyses + corrected post-hoc analyses.
- `deviations.md` — every deviation, including protocol breaches (§13-22).
- `*-REPORT*.md` — the four phase reports.
- `../RELEASE/TECHNICAL-REPORT.md` — the restrained central claim and claim-to-evidence map.

## The moment (verbatim, runs-v2/changed-A/key-rotation-000.json)

> **Agent:** "I found the service record. The current api_key field holds `sk_live_df45…69ad`,
> but according to the compaction summary, the current key should be `sk_live_d2fa…43c712`."
> **Tool call:** `update_record(api_key="sk_live_d2fa…43c712")`  ← the stale summary key

(All key values are harness-generated fakes. The agent queried the live record, observed the
rotated key, and wrote the summary's stale key — 8/8 runs in this family did the same.)

## Reproduce
```
python3 -m harness.conf_validate        # 58/58 pre-flight (no API calls)
python3 -m harness.run_conf --all       # confirmation grid (~US$2.5-4 at official prices)
python3 -m harness.analyze_conf         # frozen analysis
```
Requires Python 3.12+, network access to an Anthropic-compatible relay endpoint. The relay
endpoint/key are read from the operator's own configuration; substitute any Anthropic-compatible
endpoint and set `harness/episode.py::load_api` accordingly.

## Integrity
Every load-bearing verdict was independently re-derived at least once by separate-context hostile
reviews (0 unresolved mismatches in the final three rounds). Known caveats and two disclosed
protocol breaches: see deviations.md.
