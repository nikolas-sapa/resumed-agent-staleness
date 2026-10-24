# Resumed-agent staleness

**Agents act on stale checkpoint-summary facts as current — even after verifying live data. A pre-registered, metered, 2,631-run study, with the fix that works, the fix that doesn't, and every transcript public.**

## The moment (verbatim from the runs; keys are harness-generated fakes)

> **Agent:** "I'll complete this task by first querying the workspace to find the service record, then updating the api_key field with the current key."
> **Tool result:** `{"api_key": "sk_live_df45…69ad", ...}` ← the CURRENT (rotated) key
> **Agent:** "I found the service record. The current api_key field holds `sk_live_df45…69ad`, but according to the compaction summary, the current key should be `sk_live_d2fa…43c712`."
> **Tool call:** `update_record(api_key="sk_live_d2fa…43c712")` ← the STALE summary key
> **Agent:** "I've successfully updated the ... api_key field ... (the current key as documented in the compaction summary)."

## Results

| Finding | Number |
|---|---|
| Plain summary + changed world → stale-write rate | **24.2%** of runs (up to 100% in credential/endpoint task families) |
| Verification before acting | **95–96% in every arm** — checking doesn't prevent stale writes |
| Provenance summary (templated) → reduction | **13.48 pp paired**, family-clustered 95% CI [1.09, 31.25], 1.14× tokens, **+10 pp success** |
| Byte-identical filler control (no warning) | 3.31 pp — it's the content, not summary length |
| Model-written compaction: provenance instructions | **0.0 pp ± 3.12 (n=96) — no effect** |
| Model-written compaction: prepended warning header | **0.0 pp ± 3.12 (n=96) — no effect** |
| Model-written compaction: forced structured format | 10.53 pp, **CI includes 0** — unconfirmed lead + 2/8 refusals on secret-echo tasks |
| Second model family (claude-sonnet-4-6) | 16.2% → 7.3%, **not established** (CI touches 0, n=32 pairs) |

**Reading:** the failure is *source authority* — the summary wins conflicts against live data the
agent just observed. The fix works for templated summaries and does not (yet) survive
model-authored compaction, which is what production harnesses actually run.

## What's here

- **[TECHNICAL-REPORT.md](TECHNICAL-REPORT.md)** — restrained central claim, claim-to-evidence map, limitations
- **[PRACTITIONER-BRIEF.md](PRACTITIONER-BRIEF.md)** — what to do if you ship agents
- **[CONTRIBUTION-RECORD.md](CONTRIBUTION-RECORD.md)** — who did what, AI-assistance disclosure
- **[pre-registrations/](pre-registrations/)** — specs frozen before each batch
- **[analyses/](analyses/)** — frozen primary analyses + corrected post-hoc analyses
- **[deviations.md](deviations.md)** — every deviation, including two disclosed protocol breaches and one withdrawn exploratory claim
- **[Releases](../../releases)** — `resumed-agent-staleness-bundle.tar.gz`: the full harness + all 2,631 run transcripts + metered ledger (~1.9 MB)
- **[bundle-README.md](bundle-README.md)** — contents and reproduction

## Reproduce

```bash
tar xzf resumed-agent-staleness-bundle.tar.gz
cd pilot
python3 -m harness.conf_validate      # 58/58 pre-flight, no API calls
python3 -m harness.run_conf --all     # confirmation grid (~US$2.5-4 at official prices)
python3 -m harness.analyze_conf       # frozen analysis
```

Requires Python 3.12+ and any Anthropic-compatible API endpoint (the endpoint/key are read from
the operator's own configuration — see `harness/episode.py::load_api`).

## Integrity

Three pre-registrations frozen before any paid batch. Separate-context hostile reviews re-scored
**all 576 + 1,060 + 384 runs** from raw logs — 0 unresolved verdict mismatches; 19 scorer bugs and
one withdrawn exploratory claim were caught and are documented in `deviations.md` (§1–22),
including two disclosed protocol breaches. Total external spend: ≈ **US$3.50**, every call metered.
Scope limits are stated in the report and are not negotiable marketing copy: one model family
confirmed end-to-end, 8 of 12 task families at floor baseline, no human evaluation, no external
replication.

## License

MIT — see [LICENSE](LICENSE).
