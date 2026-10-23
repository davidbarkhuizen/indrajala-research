# The earlier reviews, re-assessed (audit, 2026-10-23)

**Status: a dated review, deliverable 4 of the programme audit** (indrajala-ml
`docs/workplans/programme-audit-workplan.md`, #953). The owner's request, made mid-planning:
"also re-assess the existing reviews, once you are done with this one - in light of any audit
findings". Each item of each earlier review gets a verdict against the audit
([`review-2026-10-23-programme-findings.md`](review-2026-10-23-programme-findings.md), F1-F33):

- **right:** still correct, and still applies;
- **closed:** acted on, and the action holds;
- **overtaken:** made moot or superseded by later work;
- **lapsed:** its remedy was tied to an event that never happened, so it is still open;
- **wrong:** the audit contradicts it.

The reviews:

| review | where | scope |
| --- | --- | --- |
| the papers' contribution review (2026-10-15) | `review-2026-10-15-contribution.md` (here) | P1 and P2 before the registered division comparison |
| the state-formation contribution review (2026-10-21) | `review-2026-10-21-state-formation.md` (here) | option 1 as of 2026-10-21 morning |
| the reasoning review (2026-10-21, morning) | indrajala-ml `docs/audits/reasoning-review-2026-10-21.md` | the line of reasoning, gaps |
| the consistency review (2026-10-21, afternoon) | indrajala-ml `docs/audits/consistency-review-2026-10-21.md` | rules against practice |
| the RNG audit | indrajala-ml `docs/audits/rng-audit.md` | the generators behind every reproducibility claim |

## What re-reading them shows

1. **They were right far more often than wrong.** No item is contradicted by the audit. The
   cautions they raised were borne out:
   - the 2026-10-21 contribution review's "`p` is unmeasured until fresh seeds": the fresh-seed
     matrix (D55) was refuted on S3, and the fresh-seed rate (D64) read 5 of 8;
   - the reasoning review's "no random machine in the panel": random machines were added, and they
     fail;
   - the 2026-10-15 review's "a curiosity until explained or prevented": the collapse is still
     unexplained.
2. **Most of their open items lapsed rather than failed.** The 2026-10-21 reviews put their remedies
   "at the panel's registration" or "after the panel". The panel never ran (F5), so those items
   neither closed nor came back: the approximation beside S3, the plain-RNN control, the crucible's
   cap from the bound, the slack bound, D34's probe. **This is the audit's main lesson about
   reviews: a recommendation tied to a gate needs a re-home when the gate is dropped.**
3. **Their corrections reached the workplan, not the notes.** The reasoning and consistency
   reviews' points were settled as decisions (D35-D45). The research notes and `contribution.md`
   kept the older wording: F8, F13 and F15 are items these reviews raised.
4. **They missed what lay outside their scope.** The 2026-10-21 reviews looked at state formation
   only. By then four of the audit's findings were already present in the papers and their
   statistics:
   - the guard's training result had contradicted P1 since 2026-10-19 (F2);
   - the approximation claim's control (F3);
   - the one-sided tests (F9);
   - the 120-against-121 confound (F16).

## The papers' contribution review (2026-10-15)

| item | verdict | now |
| --- | --- | --- |
| P1: the certificate is the best contribution | **right** | still the strongest; its "724" needs "checked", not "certified" (F14) |
| P1: sampled tests overstate | **right** | |
| P1: more codes buy test-passing wrong machines; "undersold" | **right** | C3 registered and holds (working p 0.014, Holm 0.042; certified p 0.43; recomputed) |
| P1: certify each step, stop at the first proof; training destroys proved networks | **right, narrowed** | E2b' kept the proof at every step in 19 of 20 (F22); the guard fails in training as built (F2) |
| P1: the exclusion bound, methodology not a result | **right** | in practice a cap, with certificates coming before it (F8) |
| P1: E6 shows the transformer isn't needed at `k` 1 | **right; lapsed in the current strand** | never re-tested under option 1 (the reasoning document's gap 5) |
| "Critical gap: E2 and a plain recurrent baseline" | **closed** | E2 0 of 20 against 8 of 20; E2b' 0 of 20 against 20 of 20 (with F20's caveat) |
| P2: 25- and 49-state machines, "small in absolute terms" | **overtaken** | 121 (P2) and 169 (W1, not yet in P2, F27) |
| P2: the cover, close to Dan et al. | **right; closed as evidence** | registered 13 of 20 against 1 of 20, and again 15 of 20 |
| P2: one approximation, "potentially the most original"; "needs the AB control and 20 seeds" | **closed as registered, right as a caution** | A1-A3 hold. The control chosen (the product) differs in two ways, so "because it is one" outruns it (F3); the review's instinct for a control was right, the control was not enough |
| P2: an enforced factorisation blocks learning, "weak (2 seeds a cell)" | **right** | still screens |
| P2: the collapse, "a curiosity until explained or prevented" | **right** | avoided (stop at proof, fork), escaped (reheat, restarts), not explained |
| Raise most: 1 E2 and E2b | **closed** | |
| Raise most: 2 the approximation claim registered | **closed** | with F3's interpretation |
| Raise most: 3 a second composite task, the running affine map | **lapsed** | never run; next-steps.md keeps it. It is the cover-free test F3's control question also needs |
| Raise most: 4 a fix for the collapse, then `p` 11 | **half closed** | `p` 11 done with the fork; the guard is not a fix in training (F2) |
| Venues: P1 once E2 is in | **lapsed** | E2 and E2b' are in; neither paper has moved since 2026-10-17 (F27) |

## The state-formation contribution review (2026-10-21)

| item | verdict | now |
| --- | --- | --- |
| Row 7: learned factors as approximations, the most original; not registered; does the factor budget steer it? | **right; lapsed** | still read on design networks only; the steering question waits on D39 (i), never run (F18) |
| Row 8: formation against conversion, "strong" as diagnosis | **right** | the failure kinds' split holds; the kinds are less independent than assumed (the reasoning document's A9) |
| Row 9: resets against groups, "thin"; narrow to a snapped state or run a plain-RNN control | **right; half acted on** | "in a snapped state" was added; the class line from one machine each stands in the status note's abstract (F15); no control |
| Row 10: crystallisation, "modest"; `p` unmeasured until fresh seeds | **right, and borne out** | fresh seeds: the fresh-seed matrix (D55) refuted its S3 bar (7 of 16); the fresh-seed rate (D64) 5 of 8 on S3 |
| The heat capacity's hump, "supporting" | **right** | its use, the adaptive cool (D33), met its bar exactly and was set aside |
| The adaptive cool (D33), the bounded handover (D34): "nothing claimed until read" | **right; D34 lapsed** | D33 4 of 8; D34's probe never ran or was set aside on the record (F33) |
| Brandoit et al. 2026 (NFSM) as P1's near precedent | **closed** | P1 cites it |
| Raise most: 1 the panel on fresh S3 seeds 8-15 | **overtaken** | fresh seeds measured instead by D55 (24-39) and D64 (40-47); seeds 8-23 were the core matrix's, never launched |
| Raise most: 2 at registration, the approximations question, a plain-RNN control, a DOLCE-style arm | **lapsed** | the panel's registration never happened (F5, F18) |
| Raise most: 3 the status note's citations; narrow the algebra claim | **closed / half** | citations added; the narrowing incomplete (F15) |
| Raise most: 4 a third paper premature | **right, and since overtaken in practice** | continuous-crystallisation.tex and freeze-and-restarts.tex now hold the strand's material; a decision on where it is published is the owner's (F27) |

## The reasoning review (2026-10-21, morning)

| # | item | verdict | now |
| --- | --- | --- | --- |
| 1 | The target in the training loop | **right; partly closed, reopened in a new form** | the answers-only stop (D35) took the certificate out of the stop; the exact bound keeps the target's size in (D43, F6); restarts and the runner's find mode make the certificate the selector again (F7) |
| 2 | The seed mechanism explains conversion, not formation | **right; not acted on** | F15 |
| 3 | The coupling window rests on a curve that mispredicts; the working ingredient is a slow, gradual coupling | **right as an inconsistency; its conjecture weakened** | the coupling from sharpness (D50) replaced the curve. The coupling probe (D38) showed a coupling is needed (F21). The paced coupling (D61) removed every jump and changed nothing, so slow coupling is not the ingredient |
| 4 | Two methods, not one general architecture | **overtaken for move-to-front-4; right beyond it** | the continuous crucible certifies move-to-front-4; S4 and the random machines fail (F17) |
| 5 | The bounded handover erodes the two-arm rationale | **closed** | the crucible against whole (D36) replaced the second arm; then moot |
| 6 | Two misstatements | **closed** | |
| 7 | No random machine in the panel | **closed, and borne out** | added (D37, D56, D58, D64); 1 of 8 and 0 of 7 |
| 8 | The feasibility register predates option 1 | **half closed** | row 15 added; the coupling row never written (F24); the cap from the bound lapsed (D44) |
| 9 | The two strands aren't joined | **right; lapsed** | F18 |
| 10 | The harm question has no stated mechanism | **right; half acted on** | the expectation was registered (D37); only S4 tested, both formation and keeping failing (F19); division never run (F17) |
| — | Recommended offline: would an answers-only stop have kept each certificate? | **closed** | the re-reading: yes at the exact bound; slack costs (F6) |

## The consistency review (2026-10-21, afternoon)

| # | item | verdict | now |
| --- | --- | --- | --- |
| 1 | D12 against D37 | **closed, then moot** | the panel's verdict (D40) replaced D12; the panel never ran (F5) |
| 2 | The exclusion bound is met by the configs, not by the certified runs | **closed in the workplan, not in the notes** | the bound as trained (D42); the notes still say training reaches it, and give no trained lengths (F8) |
| 3 | The crucible's cap is a constant read from the target | **right; lapsed** | the crucible's cap from the bound (D44) deferred to after the panel; the continuous method still grows from the cap of 8 |
| 4 | The answers-only stop moves the target's size into the loop | **right; open** | claims worded "under an exact state bound"; the slack study never run (F6) |
| 5 | One success definition | **closed** | one success (D41) |
| 6 | At coupling 0 the gate reads the liquid: two changes | **closed** | read by D38's reading and D34's order (D45) |
| 7 | D38's expectation omits the evidence against it; write up both accounts | **right, and borne out** | D38 refuted; the account is a line ("the handover is needed"), overstated (F21) |
| 8 | D34's probe only after D38's reading; "if D38 holds, it is set aside unrun, recorded" | **right; not followed** | D38 failed, so D34's probe should have run; it neither ran nor was recorded as set aside (F33) |
| 9 | Stale statements, corrected in the same PRs | **closed at the time** | new staleness since (F13, F24, F27, F29, F30) |
| 10 | The status note's claim broader than its evidence, "for the next revision" | **right; not acted on** | F15 |

## The RNG audit

| finding | verdict | now |
| --- | --- | --- |
| Three global states (closed) | **right** | |
| FMA contraction on other platforms (low, latent): "today's CI can't show a difference"; the PyPI plan's multi-platform CI will catch it | **overtaken; its pointer stale** | CI now runs every test shard and the crate's parity tests on arm64 (the aarch64 workplan), and `litshe` (aarch64) holds bit parity, so the risk is watched on Linux arm64 by another plan than the one named; macOS is still unchecked |
| `[low, high)` not strictly guaranteed (informational) | **right** | |
| Bearing on the research | **right, and relied on** | the cross-machine parity behind moving runs mid-flight (D63, D67) and the paired designs rests on it (the reasoning document's A2, sound) |

**Recommendation for the RNG audit:** point its FMA finding at the aarch64 workplan's arm64 CI, and
narrow it to macOS.

## Recommendations about reviews

1. **Re-home lapsed items when a gate is dropped.** When a plan sets aside a step (the panel, by the
   matrix set aside (D47)), list every recommendation that waited on it, and give each a new home or
   an explicit drop. The lapsed items above are that list for the panel.
2. **A review's corrections go to the notes too.** Each settled item names the documents that state
   the old position, and the same PR corrects them or records why not. F8, F13 and F15 would have been
   caught.
3. **Scope a review to the claims, not the strand.** A review of the reasoning reads the papers'
   claims beside the current strand. Four of the audit's findings sat in the papers through two
   reviews.
