# Contribution record

**Project:** Resumed-agent staleness — selection, pilots, confirmation, and mechanism
investigation. **Period:** 2026-10-04 to 2026-10-07. **Status:** complete; unreleased.

## Roles

- **Nikolas Sapalidis (project owner):** supplied the research agenda, domain priorities
  (browser agents, long-horizon agents, harness design, orchestration), the protocol with
  evidence standards and phase gates, budget and provider decisions, and all go/no-go decisions
  (candidate selection, pilot approval, confirmation approval). No experiments were run before
  the user-approved selection gate.
- **AI orchestration (this system, GLM-5.3-Flash session):** resource verification, three-lane
  literature discovery (120-source ledger), synthesis and candidate scoring, harness and scorer
  implementation, batch execution and metered spend accounting, frozen pre-registrations,
  analyses.
- **AI hostile reviewers (same model family, separate fresh contexts):** four review rounds
  (selection, v1 pilot, v2 pilot, confirmation + mc) independently re-deriving verdicts from raw
  artifacts — in the final three rounds, re-scoring **all** runs (576 + 1,060 + 384) with zero
  unresolved verdict mismatches — plus bootstrap seed sweeps, exclusion-robustness imputation,
  composer byte-equality recomputation, and adherence audits. Reviewer findings forced: one
  candidate's disqualification (novelty), 19+ scorer false-positive fixes, a withdrawn
  exploratory claim, corrected denominators and spend accounting, and disclosure of two protocol
  breaches (partial recovery pass; retroactive deviations logging).

## AI-assistance disclosure

All literature discovery, coding, execution, and drafting were AI-performed under the owner's
protocol and decisions, consistent with the owner's instruction that orchestration delegate
bounded work while the human owns question selection and gates. No human subjects, no external
validation, no human-written analysis. Nobody outside this system has seen or confirmed any
result.

## Integrity notes (visible in the record)

- Pre-registrations frozen before each paid batch; three phase reports plus one withdrawn
  exploratory claim, all preserved.
- Deviations log (§1–22) includes protocol breaches and their bounds — nothing silently dropped.
- Every load-bearing number traces to `claim-evidence` mappings and raw artifacts under
  `research/consequential-ai-selection-2026-10-04/`.
- Total external experiment spend: ≈ US$3.5 of the US$50 authorized cap; all calls metered.

## Suggested venue/audience fit (identified from published work; no contact made)

1. **Safe to Resume / Terminal-Bench agent-reliability authors** — this work extends their SF3
   (stale external dependencies) finding from adversarial observation to a controlled benign
   measurement with a working mitigation and its boundary conditions.
2. **StateGuard authors** — our training-free summary-format result complements their
   trained state-graph manager: the provenance signal helps only in templated summaries, which
   sharpens the case for their approach.
3. **DART (restore-boundary certification) authors** — our zero-mechanism alternative and its
   mc-transfer failure quantify what runtime gating adds beyond summary engineering.
4. **BrowserGym/AgentLab and WebArena-Verified maintainers** — the evaluator-side lesson
   (negative checks in 8/812 tasks) and the resume-validity harness are directly reusable.
5. **METR time-horizon evaluation team** — checkpoint/resume validity is a confound for
   long-horizon measurement that their task suites currently do not control.
