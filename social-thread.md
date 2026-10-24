# Social thread — draft (X / LinkedIn carousel source)

## Hook options (pick one)
- "I gave an AI agent the current data. It checked it. Then it wrote the old value anyway."
- "Your agent's compaction summary is overwriting live data — after the agent verifies it."
- "2,631 agent runs, $3.50, one uncomfortable finding about agent memory."

## Thread (X, ~10 posts)

1/ I ran 2,631 pre-registered agent runs to answer one question: when an agent resumes from a
compaction summary and the world has changed, does it act on stale facts? Total cost: $3.50.
The answer changed how I think about agent memory. 🧵

2/ Setup: a simulated workspace with exact ground truth (records + files), a checkpoint, an
external change, then a resume from a compaction summary. Behavioral scoring: did the agent write
or assert the superseded value as current? Every run transcript saved.

3/ RESULT 1 — with a plain summary: ~24% of changed-state runs acted on a superseded fact. In
credential- and endpoint-type tasks: essentially 100%.

4/ The uncomfortable transcript: the agent queries the record → sees the NEW api key → writes the
OLD key anyway. "The record says X, but my summary says Y." The notes beat the live data.

5/ RESULT 2 — verification doesn't save you. 95-96% of runs in EVERY arm queried before acting.
Agents checked. Then the summary won anyway. This is a source-authority failure, not a tool-use
failure.

6/ RESULT 3 — the partial fix: provenance annotations in the summary ("recorded at checkpoint; not
re-verified") HALVED stale behavior (13.5pp, CI excludes 0) at 1.14x tokens, and success went UP
10 points. A byte-identical filler control did nothing — it's the content, not the length.

7/ RESULT 4 — the twist that matters for production: model-WRITTEN compaction summaries break the
fix entirely. Provenance instructions: 0.0pp ±3.1. Prepending the warning header: 0.0pp ±3.1.
Forcing the full structured format: promising but unconfirmed + 2/8 refusals on secret-bearing
tasks.

8/ What I'd ship tomorrow: if your checkpoint summaries are templated, add the provenance header.
If they're model-generated (most harnesses), there is no validated fix yet — treat resumed context
as untrusted and make verification binding, not polite.

9/ Honesty section: one model family confirmed end-to-end; a second showed the same direction,
didn't reach significance. 8/12 task families were immune because their briefs said "use the
CURRENT value." My scorer had 19 bugs before hostile review caught them. All documented.

10/ Full bundle is public: harness, all 2,631 transcripts, pre-registrations, deviations log,
metered ledger. Replicate it for ~$3.50. [link]

## LinkedIn carousel (8 slides) — skeleton
1. Title: "Agents check the data. Then overwrite it anyway." (the transcript moment, redacted)
2. The setup in one diagram: checkpoint → world changes → resume from summary.
3. Result: ~24% stale-write rate; 100% in credential tasks.
4. The mechanism: source authority, not verification (95-96% verified first — in every arm).
5. What fixes it (templated summaries): provenance markers. Halves it, +10pp success.
6. What doesn't: anything attached to model-written compaction. Instructions, headers: zero.
7. The eval lesson: long-horizon benchmarks that compact mid-task measure summary authority too.
8. Bundle link + "replicate for $3.50" + limitations box.
