# I ran 2,631 agent runs to find out whether resumed agents trust stale summaries. They overwrite live data *after checking it*.

*First-person technical post · draft for publication · all numbers pre-registered and independently re-derived*

## The setup

AI agents rarely finish a task in one sitting. Sessions get interrupted, context gets compacted
into a summary, and the agent resumes later from that summary. In between, the world moves: a key
rotates, an endpoint gets deprecated, an owner changes.

Question: when the agent resumes, does it act on the summary's stale facts as if they were
current? And does telling it "these facts may be stale" actually help?

I built a small deterministic environment — a simulated workspace of records and files with exact
ground truth, twelve task families, an instrumented resume procedure (checkpoint → external state
mutation → resume from summary → behavioral scoring), and a scorer validated on hand-labeled cases
including real-transcript regressions. Then I ran **2,631 pre-registered runs** across four
studies, spending **about $3.50** of API credit, with every number independently re-derived by
separate-context hostile reviews that re-scored every single run from raw logs.

## Finding 1: agents overwrite live data with summary facts — after looking at it

With a plain compaction summary and a changed world, **~24% of runs wrote or asserted the
superseded value as current**. In credential- and endpoint-type tasks it was **essentially every
run**. The transcript that made me sit up: the agent queries the record, *sees the current API
key*, and then writes the old one anyway — reasoning, in effect, "the record says X, but my notes
say the key is Y," and trusting the notes.

Here's the part I didn't expect: **verification doesn't protect you.** 95–96% of runs in *every*
experimental arm queried the live state before acting. The agents checked. Then the summary won
anyway. This is not a tool-use deficit; it's a source-authority problem.

## Finding 2: provenance warnings halve it — in templated summaries

Adding per-fact validity provenance to the summary ("recorded at checkpoint; not re-verified")
cut stale behavior roughly in half (13.5 percentage points paired, family-clustered 95% CI
[1.1, 31.3]) at 1.14× token cost, and task *success went up* ~10 points. A byte-identical-length
control summary with neutral filler did nothing — it's the warning content, not summary length.

## Finding 3: the fix breaks completely with model-written summaries

Here's the twist that matters for every real harness: production compaction is written by the
model itself. So I tested it. Provenance *instructions* to the compaction model: **nothing**
(0.0 pp ± 3.1, n=96). Prepending the warning header to the model's own summary: **nothing**
(0.0 pp ± 3.1, n=96). Forcing the model to emit the full structured format: a positive signal
concentrated in exactly the same task families, but statistically unconfirmed — and the template
triggered **refusals in 2 of 8** credential-task compactions.

So the honest headline is two-sided: the fix is real and cheap for templated summaries, and it
**does not survive contact with model-authored compaction** — which is what most harnesses
actually run.

## What I'd do if you ship agents

1. Templated checkpoint summaries: add the provenance header and per-fact markers. Cheap, measured.
2. Model-generated compaction: there is currently **no validated fix** — treat resumed context as
   untrusted and design your verification to bind (e.g., re-verify gates that block writes, not
   polite instructions).
3. Task phrasing matters: families whose briefs said "use the CURRENT value from the records"
   never went stale at all.
4. Eval people: if your long-horizon benchmarks allow compaction mid-task, you are measuring
   summary authority mixed into capability. Control it or report it.

## The fine print, because it matters

One model family confirmed end-to-end (a second, claude-sonnet-4-6, showed the same direction but
didn't reach significance at my sample size). Eight of twelve task families sat at floor because
their instructions already said "use the CURRENT value from the records." No human evaluation. My
scorer was wrong in nineteen places before hostile review caught it; my first "effect size" was
partly an artifact of my own contrast design; one of my exploratory findings was withdrawn after
review showed it was a composition artifact. All of it is documented — pre-registrations,
deviations log, every transcript, and the metered ledger — because a result you can't audit is a
story, not a finding.

The full bundle (harness, all 2,631 runs, pre-registrations, ~$3.50 ledger) is public. Take it,
break it, replicate it.
