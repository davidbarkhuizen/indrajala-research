# Audit findings: the research programme (2026-10-23)

**Status: a dated review, deliverable 3 of the programme audit** (indrajala-ml
`docs/workplans/programme-audit-workplan.md`, #953). The owner's request: "a list of audit
findings". Its companions:
[`review-2026-10-23-programme-evolution.md`](review-2026-10-23-programme-evolution.md) and
[`review-2026-10-23-programme-reasoning.md`](review-2026-10-23-programme-reasoning.md), which groups
these findings into inconsistencies, gaps and assumptions. Paths without a repository name are
indrajala-ml's under `docs/`; `research:` marks this repository. "The workplan" is
`workplans/state-formation-workplan.md`.

**Severity.**
- **S1:** a registered claim, or a paper's or research note's statement, is wrong or unsupported.
- **S2:** a stated rule is broken, or a claim is weaker than stated.
- **S3:** documents disagree, or a statement is stale.
- **S4:** records and hygiene.

**What happens to them (the plan's D2):** S3 and S4 are corrected in follow-up PRs. S1 and S2 go to
the owner, since each changes a claim, a verdict or a rule. A recommendation is a proposal, not a
decision.

**Method and limits:**
- **Read in full:** the papers, the research notes, `contribution.md`, the protocols, and the
  state-formation, batch-runner, general-algebras and snap-wall workplans.
- **Read in the parts the claims cite:** the retired workplans and the study scripts' findings.
- **Spot checks:** every headline statistic recomputed with `inference.py`; six manifests verified
  across the phases.
- **Out of scope:** the engineering roadmap.
- **Excluded from the data:** the running probes (the deadline's completion (D67) and the reheat
  against restarts (D63)), audited as designs only.
- **Independence:** the auditor is an author of most of what is audited.

## Summary

| # | sev | finding | where |
| --- | --- | --- | --- |
| F1 | S1 | The fresh-seed rate's registered verdict is being re-scored by a completion registered after a borderline read | the workplan D64, D67; research: continuous-crystallisation.tex |
| F2 | S1 | "The guard is untested in training" is false; it was tested and certified fewer seeds; "repaired" overstates | research: P1 l. 690, 733; contribution.md row 3b |
| F3 | S2 | "One approximation helps because it is one": the control differs in two ways | research: P2 l. 49, 98, 374, 407; contribution.md 5b; next-steps.md l. 194 |
| F4 | S2 | A design-seed rate serves as the method's comparator | the workplan D61 l. 970, D64 l. 1088; both 10-22/23 notes |
| F5 | S2 | The plan's acceptance gate (the panel) never ran; the method changed about thirty times without it | the workplan D1, D11, D12, D40, D46-D48 |
| F6 | S2 | Every rate is at an exact state bound; discovery's slack is unmeasured | D43; research: machine-discovery.md |
| F7 | S2 | Restarts' Las Vegas premise fails in the use ("find" mode) the runner is built for | batch-runner-workplan.md D3 |
| F8 | S2 | The notes say training reaches the exclusion bound; certificates come before it, and trained lengths aren't reported | research: three notes' Settings; D42 |
| F9 | S2 | One-sided Fisher tests where the protocol fixes two-sided | research: protocols/experiment-design.md §3; E1, B3, P2, C2b |
| F10 | S2 | A dozen fixed constants against "no constants without a derivation"; no sensitivity | D28, D49-D52, D59 |
| F11 | S2 | "Every failure freezes" is close to definitional; "the schedule is not the lever" rests on analogy | the workplan's freeze findings; research: freeze-and-restarts.tex |
| F12 | S2 | The epoch-budget lesson (D46) was lost for two days, and ten runs were cut | D46 l. 742; D54-D64 |
| F13 | S2 | `contribution.md`, "the current statement", stops at 2026-10-21 | research: contribution.md |
| F14 | S2 | "724 distinct networks certified" against "ran on 724" | research: contribution.md row 1; P1 l. 121 |
| F15 | S2 | "Groups need a seed" still claimed generally, uncorrected after two reviews | research: state-formation-status.tex l. 45-47, 88-96 |
| F16 | S2 | "The state count isn't the limit: division certifies at 121, same cell" is confounded | general-algebras-workplan.md l. 210; research: transition note |
| F17 | S2 | "One general architecture" rests on two backdrops | the workplan; D57, D64 |
| F18 | S2 | The approximations (P2) are absent from the current method; D39 (i) never ran | D39; research: machine-discovery.md |
| F19 | S3 | "Random fail at forming, S4 at keeping" contradicted by D64 | research: freeze-and-restarts.tex l. 80; the scaling conjecture |
| F20 | S3 | C2b's "registered" test reuses an arm seen before registration | `scripts/window_recurrent_study.py` E2b'; research: P1 |
| F21 | S3 | "The handover is needed" overstated | research: continuous-crystallisation.tex l. 53 |
| F22 | S3 | P1: "training stops at the proof" as a condition of success | research: P1 l. 713 |
| F23 | S3 | P2's 0 of 160 baseline isn't like for like | research: P2 l. 47, 72 |
| F24 | S3 | The feasibility register and the protocol lag practice | research: information-flow.md rows 8, 13; experiment-design.md §5 |
| F25 | S3 | The margin stop's separation is shown on the networks that defined it | D59; research: continuous-crystallisation.tex |
| F26 | S3 | Small-sample bars read as rates | the notes; D12, D40 |
| F27 | S3 | The papers have stalled since 2026-10-17, and their statuses are wrong | research: README; P1; P2 |
| F28 | S3 | The pace outruns the record | across the documents |
| F29 | S4 | Workplans superseded since 2026-10-20 are still listed as in progress | next-steps.md l. 10-23 |
| F30 | S4 | Retired paths and plans cited as current | research: P1, P2 Reproducibility; machine-discovery.md l. 66 |
| F31 | S4 | Per-host manifests don't verify on the archive as written; option1.sha256 predates D54 | `data/window-recurrent/state-formation/option1/` |
| F32 | S3 | The stage B tool D42 promised (Chow's test set) is not built | D42; `indrajala_ml/studies/window_tasks.py` |
| F33 | S3 | A registered probe whose trigger fired was neither run nor set aside on the record | the workplan, D34's probe, D45 |

## Findings

### F1 (S1). The fresh-seed rate's verdict is being re-scored after a borderline read

**Where:** the workplan, the fresh-seed rate (D64, l. 1085) and the deadline's completion (D67,
l. 1242); research: continuous-crystallisation.tex (abstract, "The method's fresh-seed rate").

**Evidence:**
1. D64's cell is D54's, "1,600 epochs or 690 minutes a run". Its registration lists "the deadline's
   stops" among the readings, so a deadline stop was an anticipated end.
2. It was read at 05:30 on 2026-10-23 as 7 of 12, with the bar at 8 and refutation at 6 or fewer:
   "between the bars".
3. At 06:05 D67 was registered: the three runs the wall clock cut are re-run to 1,600 epochs, and
   "each completion's outcome ... stands in for its cut run: ... its bar met, if any of its three
   certifies".
4. The research note now calls D64 "undetermined" and gives the same rule.

The completions are a sound new experiment. Using them to change an already-read registered verdict
is what experiment-design.md §2 forbids ("a flaw found mid-study is recorded and the study runs as
registered; the fix is a new, separately registered experiment"). It was decided within about an
hour of a result one short of its bar (the read merged at 05:17 in #941; D67 at 06:32 in #942),
which is the pattern pre-registration exists to rule out. The owner's
principled reason (epochs are thermodynamically the right clock) doesn't change that.

**Recommendation (the owner's call):**
- Keep D64's registered verdict as read: 7 of 12, between its bars.
- Report D67 as its own registered experiment with its own count: the completions' outcomes, and
  the pooled rate in epochs labelled post hoc for D64.
- If the pooled rate is to decide anything, register that use first in the next batch (stage 5's
  first registered batch), on fresh seeds.

### F2 (S1). The certificate guard: "untested in training" is false, and "repaired" overstates

**Where:** research: P1 l. 690 ("in training it is untested") and l. 733 (Limitations); research:
contribution.md row 3b ("repaired by a certificate guard ... the guard untested in training").

**Evidence:** the guard was tested in training: P1 of the consolidation plan, indrajala-ml #857,
read 2026-10-19, after P1's last edit on 2026-10-17. On move-to-front-4 it certified 1 of 6 guarded
against 3 of 6 unguarded (Fisher two-sided p 0.55), with S4 6 of 6 in both. It armed on a perfect
screen and froze two networks right at ratio 1.0 with near ties, undoing 96-100% of updates. The
transition note (2026-10-19) reports this correctly. The 10 of 10 repair is on 10 replays of one
network (seed 6's step 7, E2b').

**Recommendation:** in P1 and `contribution.md`, state the guard as shown on one network's replays,
harmful as built in training (1 of 6 against 3 of 6, a screen), and freezing learning at 121 states.
Drop "repaired" from row 3b's headline.

### F3 (S2). "One approximation helps because it is one" outruns its control

**Where:** research: P2 abstract (l. 49) and §One approximation (l. 374, 407); contribution.md
row 5b; next-steps.md l. 194; research: machine-discovery.md ("Result 5b is the seed of the goal").

**Evidence:** A3 compares the sum (an approximation) with the product (not one). P2 itself names
the operative difference: "the sum's next value is a function of the sum and the column, so it can
be learned as a counter on its own, while the product's needs both residues". It also notes the
product isn't even learned (0.71 at the best step). Being a congruence *is* being a self-contained
counter, so the design cannot separate "an approximation" from "an extra output the network can
learn by itself". A learnable non-congruence output (for example a function of the last column only,
or of a short suffix) would separate them. The registered tests hold as registered; the "because" is
an interpretation.

**Recommendation:** word 5b as "the sum, an approximation, helps where an equally distinguishing
non-approximation, the product, which the network does not learn, doesn't". Name the missing
control. Register it if the claim is to carry the discovery premise.

### F4 (S2). A design-seed rate serves as the method's comparator

**Where:** the workplan, the paced coupling (D61, l. 970: adoption "against the method's current
rate ... S3 11 of 16, move-to-front-4 7 of 8 at D59's reading") and the fresh-seed rate (D64,
l. 1088); research: continuous-crystallisation.tex ("it agrees with the margin stop's re-runs").

**Evidence:** the fresh-seed matrix (D55) refuted its S3 bar as registered (7 of 16, refuted at 8 or
fewer). The margin stop (D59) was then designed from D55's stopped networks, its split-tie rule read
off those 19, and re-run on the same seeds. Its 11 of 16 and 7 of 8 are therefore design-seed rates,
the kind the owner's rule excludes. The fresh rate (D64) is S3 5 of 8 and move-to-front-4 2 of 4;
pooled, 7 of 12 against 18 of 24 (Fisher two-sided p 0.45: not a detectable difference, but not
"agreement" either).

**Recommendation:** quote the fresh-seed rate (D64), with the margin re-runs as design-seed readings.
Record D55's refutation beside the method's history in the notes.

### F5 (S2). The plan's acceptance gate never ran

**Where:** the workplan, one option at a time (D1), the panel (D11), accept or reject (D12), the
panel's verdict (D40), the core matrix (D46), the matrix set aside (D47) and the continuous
crystallisation (D48); its Stages (4b still listed).

**Evidence:**
- **The gate:** D1 has each option understood, built, tested on the panel and accepted or rejected
  before the next.
- **What happened:** option 1 went through about thirty redesigns (D13-D66). The panel (4b) was
  never run. Its affordable form (D46) was registered and set aside unlaunched within hours (D47).
  The continuous crystallisation (D48) changed five parts at once at the owner's direction, against
  the one-change rule.
- **The consequences:** options 2-4 are shelved pending the panel's diagnosis (D31). The harm
  question (D37) was asked only on S4.

**Recommendation (the owner's call):**
- Either retire D1/D12/D40 explicitly, saying the method is now judged by fresh-seed batches on the
  runner, or schedule the panel's affordable form as that first batch.
- Amend the one-change rule to allow an owner-directed bundle when it is recorded as one.

### F6 (S2). Every rate is at an exact state bound

**Where:** the exact state bound (D43); the answers-only stop (D35); research: machine-discovery.md
("a bound `m` known"); the 2026-10-21 consistency review, item 4.

**Evidence:** every option-1 run stops at `N = q`. The re-reading found 25 false stops and 1 false
discovery at 1.1 times the target's size, and 44 and 4 at 1.5. D43's slack reading was planned
"offline on the panel's saved step networks", and the panel never ran. The discovery premise is a
known bound, not an exact one.

**Recommendation:** run the planned offline slack reading on the D54-D64 runs' saved step networks
(`answers-stop` at 1.1 and 1.5). It needs no new training; offline analyses are exempt from the
finish-planned-work rule. Report every rate as "under an exact state bound" (most notes already do).

### F7 (S2). Restarts assume a verifier that discovery doesn't have

**Where:** batch-runner-workplan.md, the batch's modes (D3), "Find: attempts until `k`
certificates (machine discovery's use: one proved machine, stages C-F)"; research:
freeze-and-restarts.tex ("a certified run is a Las Vegas run").

**Evidence:** a run is Las Vegas only if whatever stops it is free of false positives. With the
target known, the certificate is. In discovery the stop is answers-only under a bound, and a slack
bound gives false discoveries (F6). Find mode, as written, counts certificates, which discovery
cannot compute.

**Recommendation:** state find mode's verifier: the certificate (known target, stages A and C's
evaluation), or answers-only plus Chow's test set under a bound and queries (stage D). Note that
Luby's cost model holds only with the first.

### F8 (S2). "Training reaches the exclusion bound" in the notes

**Where:** research: state-formation-status.tex l. 68, continuous-crystallisation.tex l. 79,
transition-and-output-paths.tex l. 69; the bound as trained (D42).

**Evidence:** the quasi-static crucible's certificates all came at length 8, before growth, against
S3's bound of 69. D42 made the bound a property of the config and required "certified, trained to
length L" beside each claim. The notes keep the unconditional sentence and give no trained lengths.

**Recommendation:** in each note, "the config's cap is the exclusion bound; runs certified at trained
lengths L1-L2", from `population`'s trained-length column.

### F9 (S2). One-sided tests against a two-sided protocol

**Where:** research: protocols/experiment-design.md §3 ("two arms by Fisher's exact test,
two-sided"). One-sided in: the general algebras' E1 bar; the window branches' B3 harm (0 of 6
against 4 of 6, p 0.030, also in information-flow.md row 4 and failure-kinds.md); P2's registered
claims; C2b (E2b').

**Evidence:** recomputed: 0 of 6 against 4 of 6 is 0.030 one-sided and 0.061 two-sided. Every
one-sided test was registered as one-sided, so no verdict is invalid. But the protocol says
otherwise, and B3's "harm, p 0.030" is not significant two-sided.

**Recommendation:** amend §3. One-sided tests are allowed when registered with their direction, and
two-sided is the default; report both where a verdict sits between them (B3).

### F10 (S2). Fixed constants against "no constants without a derivation"

**Where:**
- the crucible at the cap (D28: 8);
- the continuous rate (D49: 0.95, 0.99, halving 30);
- the coupling from sharpness (D50: its zero point);
- no hard switch (D51: 0.999);
- continuous growth (D52: 0.02);
- the margin stop (D59: 200 steps);
- the profile (D15-D17: `T_hot` 2 `T_c`, hold 20, `kappa` 1e-2);
- the cell (codes ratio 32/11, width 32).

**Evidence:** the owner's convention, and the paced coupling's (D61) rejection of "a fixed constant",
set the bar. Most of these constants were set on the design seeds and "not tuned since; their
sensitivity is unmeasured" (the crystallisation note's open list). Some have reasons (0.99 from
certified runs' screens), none a derivation.

**Recommendation:** list the method's constants in one table with their source (derived, measured
on design seeds, or chosen). Plan a sensitivity reading before claiming generality: one constant at
a time, on fresh seeds, on the runner.

### F11 (S2). "Every failure freezes" is close to definitional

**Where:** the workplan's "the freeze, every failure's end" and D64's reading; research:
freeze-and-restarts.tex; continuous-crystallisation.tex.

**Evidence:** the freeze is the cool's clock held at zero. The gate (D49) does that whenever the
screen stays below 0.95 of the hold's level, so any run whose answers stay wrong freezes by
construction. Certified runs freeze and thaw too (S3 30, 40, 41). The rise of the coupling at a held
clock follows from the coupling from sharpness (D50), which ignores the clock; the note says so. The
conclusion "no schedule passes a kinetic arrest; the schedule is not the lever" applies finite-time
thermodynamics, but no relaxation time was measured (the note's own caveat). The order-biased cool's
(D65) stage-0 evidence (the gate's holds of 1-5 epochs before the freeze) is the real support, and it
is about the cool before the freeze, not inside it.

**Recommendation:**
- Word it as "every failure's screen stays below the gate's floor, which holds the clock".
- Keep the physical reading as a hypothesis.
- Measure a relaxation time (the constant-lag clock already listed) before using it to rule out
  schedules.

### F12 (S2). The epoch-budget lesson was lost for two days

**Where:** the workplan, the core matrix (D46, l. 742: "a minutes budget would give a run's outcome
its machine"); the continuous probe (D54) to the fresh-seed rate (D64): "1,600 epochs or 690
minutes"; the deadline's completion (D67).

**Evidence:** the reasoning was written at 16:30 on 2026-10-21. The probes registered from that
evening used the wall clock as a co-binding budget and ran up to 12 at once on `stone`. Ten runs of
D63 and D64 were cut, which led to D67 and to F1.

**Recommendation:** this is fixed now (`--budget-epochs` required). Record it in working-notes.md as
a gotcha with its history, so the reason survives.

### F13 (S2). `contribution.md` stops at 2026-10-21

**Where:** research: contribution.md (log's last entry 2026-10-21; rows 9 and 10, "Open", "Where it
is weakest"); research: README (the 4.4x restart figure).

**Evidence:** row 10 still reads "S3 8 of 8 ... `p` unmeasured until the panel's fresh seeds".
Since then:
- the panel didn't run;
- the fresh-seed matrix (D55) refuted its S3 bar;
- the fresh-seed rate (D64) read 7 of 12 on the ordered machines and 0 of 10 on the others;
- the method changed to the continuous crystallisation and the margin stop;
- restarts were read at 3.5x in epochs, not 4.4x.

The document calls itself "the current statement, kept up to date".

**Recommendation:** update rows 9 and 10, "Open" and "Where it is weakest" to the fresh-seed
evidence (and to F2, F3 and F14), and log it.

### F14 (S2). 724 networks: certified, or checked?

**Where:** research: contribution.md row 1 ("724 distinct networks certified in P1's studies");
research: P1 l. 121 (the certificate "ran on 724 distinct trained networks").

**Evidence:** the two differ in kind. P1's certificate section counts 110 certified networks (its
margins' median); 724 is the number checked.

**Recommendation:** correct row 1 to "run on 724 distinct networks".

### F15 (S2). "Groups need a seed" is still claimed generally

**Where:** research: state-formation-status.tex (abstract l. 45-47; §In a snapped state, l. 88-96);
continuous-crystallisation.tex ("Groups such as `S_3` ... needed their state seeded").

**Evidence:**
- **The earlier reviews:** the reasoning review (item 2) found the mechanism (no synchronising word)
  explains conversion, while the failure without a crucible was formation. The consistency review
  (item 10) found the class line drawn from one machine of each kind, with move-to-front-5 (reset)
  failing by failure A in 4 of 6, and asked for "on the two machines tried" at the next revision.
  Neither change was made.
- **Since then:** the continuous crucible certifies both S3 and move-to-front-4; S4, a group, fails
  either way.

**Recommendation:** narrow to "on S3 and move-to-front-4, in a snapped state", and give the
formation account the reasoning review proposed as the alternative.

### F16 (S2). "The state count isn't the limit" is confounded

**Where:** general-algebras-workplan.md l. 210 ("division certifies at 121 in the same cell");
research: transition-and-output-paths.tex (§The general algebras at 120 states).

**Evidence:** division's runs train on the quotient *and* its two approximations' outputs (the
cover). The algebras train on one output that hides most of the state (the general algebras' D2).
The cell's settings match, but the training signal differs in exactly the way P2 showed decides
learnability.

**Recommendation:** state the confound wherever the 121-against-120 comparison appears.

### F17 (S2). "One general architecture" rests on two backdrops

**Where:** the workplan; the S4 probe (D57); the fresh-seed rate (D64); research:
machine-discovery.md, stage A.

**Evidence:**
- **Fresh seeds:** S3 5 of 8 and move-to-front-4 2 of 4 certify (D64); S4 0 of 3, random-q12-0 0 of
  4 and random-q16-0 0 of 3 don't.
- **Across the continuous cell's probes:** S4 1 of 6, the random machines 1 of 8 and 0 of 7.
- **Never run under option 1:** the harm cells (division at 169, move-to-front-4 seed 0) and the
  120-169 state tier, which are unaffordable at today's epoch times (5.5-27 days a run).

**Recommendation:** state the method's scope as "S3 and move-to-front-4" until a registered batch on
the runner says otherwise. Plan the large tier's cost (a cheaper length distribution, or the crate's
threads) as stage A's own item.

### F18 (S2). P2's approximations are absent from the current method

**Where:** the workplan, the design probes (D39) (i) ("an approximation's output beside S3's
answers"); research: machine-discovery.md ("Result 5b is the seed of the goal"); the reasoning
review's item 9.

**Evidence:**
- **P2's result:** the approximations' outputs turned 1 of 20 into 13-15 of 20.
- **The premise:** discovery supplies known approximations.
- **The current method:** trains on answers alone.
- **The joining probe:** D39 (i), never run; the panel it followed was set aside.

**Recommendation:** register D39 (i) as a short probe on the runner after the current work: S3 with
`places {1}` or the sign beside its answer, under `--whole`, fresh seeds.

### F19 (S3). "Random fail at forming, S4 at keeping" contradicted

**Where:** research: freeze-and-restarts.tex l. 80; the workplan's scaling conjecture ("the larger
machine fails at keeping").

**Evidence:** the S4 probe (D57) formed 3 of 3. The fresh-seed rate (D64) lists S4 4 and 5 as never
formed.

**Recommendation:** "S4 fails both at forming and at keeping"; S4 is 1 of 6 in all.

### F20 (S3). C2b's registered test reuses an arm seen before registration

**Where:** `scripts/window_recurrent_study.py` (E2b' findings: "continuous (E2b, as run)");
research: P1 §The snap is what extrapolates; contribution.md row 2c.

**Evidence:** E2b' was registered (#781) after E2b's continuous arm had run (it ended 2026-10-16
06:34). Only the snapped arm was rerun. With 20 of 20 against 0 of 20 the verdict is not in doubt,
but "registered" covers one arm.

**Recommendation:** add "against E2b's continuous arm, run before E2b' was registered" in P1 and the
report.

### F21 (S3). "The handover is needed" is overstated

**Where:** research: continuous-crystallisation.tex l. 53 ("refutes the claim that the handover is
dispensable"); the workplan's final readings ("The handover is needed").

**Evidence:** the coupling probe (D38) failed its registered bar (at least 6 of 8), so it is refuted
as registered. As a comparison, 4 of 8 against the quasi-static crucible's 8 of 8 on the same design
seeds is Fisher p 0.077 two-sided.

**Recommendation:** "the coupling probe's bar was refuted (4 of 8); a handover-free method was not
shown to work".

### F22 (S3). P1 makes "training stops at the proof" a condition of success

**Where:** research: P1 l. 713 ("when its state is discrete, its training reaches the exclusion
bound or a proof, and training stops at the proof").

**Evidence:** P1's own E2b': trained past the first proof, 19 of 20 runs stayed certified at every
step.

**Recommendation:** "and, where training past a proof destroys it, training stops at the proof".

### F23 (S3). P2's 0 of 160 baseline isn't like for like

**Where:** research: P2 abstract l. 47; Introduction l. 72.

**Evidence:**
- **Infeasible cells:** the 160 include E7's `p` 7, `m` 32 cells, which couldn't succeed.
- **Different protocol:** all 160 trained short of the exclusion bound and to completion, with no
  stop at the first proof.
- **Juxtaposition:** the abstract sets them beside the registered 13 of 20.

The registered comparator (1 of 20) is the fair one, and the paper's Discussion names the four
confounded changes.

**Recommendation:** in the abstract, lead with 13 of 20 against 1 of 20 (registered). Give the 160
as history.

### F24 (S3). The register and the protocol lag practice

**Where:** research: information-flow.md (no coupling row; row 13 is the answers-only stop (D35);
row 8); research: experiment-design.md §5 l. 137 ("a curriculum run's resume from a middle step
isn't checked for bits").

**Evidence:**
- **The coupling row:** the consistency review (item 9) promised a coupling row once the coupling
  probe (D38) was read. D38 showed the coupling is needed (F21), and no row was written.
- **The stop:** the stop in use is the margin stop (D59) under the margin deadline (D60).
- **Resumes:** the resume test exists (`run --resume` is bit-identical up to the stop, the
  consolidation plan's stage 3), cross-machine parity of the continuous cell is checked, and D63 and
  D67 move runs mid-flight on that basis.

**Recommendation:**
- Add the coupling's row.
- Restate row 13 as the margin stop.
- Restate §5: mid-run moves are allowed with the resume test and `same-prefix`.

### F25 (S3). The margin stop's separation is shown on its own design data

**Where:** the margin stop (D59); research: continuous-crystallisation.tex ("separated the 19
networks examined without exception").

**Evidence:** the split-tie rule was read off those 19 networks, so their separation is by
construction. Its replays are the same seeds. D59's own cons say so ("shown on 19 networks of two
machines only"); the note's wording doesn't. On fresh seeds (D64) the stop fired only on certified
networks, with waits of 0-1 steps: no false discovery, but little exercise of the wait.

**Recommendation:** in the note, "read off D55's 19 stopped networks; on fresh seeds (D64) no false
discovery".

### F26 (S3). Small-sample bars read as rates

**Where:** the research notes (8 of 8 "Wilson 0.68-1.00" as the crucible's rate); accept or reject
(D12) and the panel's verdict (D40) ("adoption ... on 6 seeds per backdrop"); research:
experiment-design.md §3 ("5 a cell is a screen").

**Evidence:** option 1's verdicts are bars on 4-12 seeds: existence and screens by the protocol's
own definition. The notes give their Wilson intervals honestly, but call some of them rates. The
adoption rule (6 seeds) is below the protocol's 20 for a comparison.

**Recommendation:** call them screens, as the protocol does. Size the runner's first registered
batch from the protocol's power line (20 a cell tells 0.8 from 0.4).

### F27 (S3). The papers have stalled, and their statuses are wrong

**Where:** research: README (P1 "E2b' to add"; P2 "the approximation claim and `p` 11 to add");
P1; P2.

**Evidence:**
- **Last edits:** both papers' last substantive edits are 2026-10-17.
- **P1:** the route sends P1 first "once E2b' is in", and it has been in since 2026-10-17. Its guard
  text is stale (F2).
- **P2:** lacks the 169-state result (W1, 5 of 6, registered), which contribution.md row 4 lists.
- **README:** its statuses are wrong both ways.
- **The route:** none of its steps (internal critique, figures re-derived from the data, cold read,
  datapack) has started.

**Recommendation (the owner's call on priority):** fix the README now. Decide whether the papers
wait for stage A or go out on their 2026-10-17 evidence plus F2, F3 and W1.

### F28 (S3). The pace outruns the record

**Where:** across the documents (this audit's S3 and S4 findings).

**Evidence:**
- **Volume:** about 20-35 merged PRs a day; 67 decisions in the state-formation workplan in four
  days; two reviews in one day.
- **Overlap:** probes launched while their predecessors were unread (the fresh-seed matrix (D55)
  before the continuous probe's (D54) last runs; three backdrops overnight).
- **Living documents:** contribution.md, the register, the README and the status notes lag by days.
- **Reactive rules:** the owner added three rules in two days to keep the record straight.

**Recommendation:** a closing step in every findings PR: update the living documents it touches
(contribution.md, the register, the README, failure-kinds.md), or say in the PR that none are
touched.

### F29 (S4). Superseded workplans listed as in progress

**Where:** next-steps.md l. 10-23; the workplans:
- general-algebras (stages 5-8: the trigger, the guard's softenings, G2);
- snap-wall (paused since 2026-10-16);
- factorisation-machine (stage 2 on, waiting since 2026-10-14);
- arbitrary-length-addition (milestone A done).

**Evidence:** the owner's direction of 2026-10-20 abandoned all planned work. These plans' remaining
stages haven't moved since 2026-10-14 to 10-19.

**Recommendation:** retire each with its leftovers to next-steps.md (the CLAUDE.md rule), or mark it
paused with its reason and date.

### F30 (S4). Retired paths and plans cited as current

**Where:**
- research: P1 Reproducibility (`docs/window-recurrent-claims-workplan.md`);
- research: P2 Reproducibility (`docs/division-workplan.md`, `docs/factored-state-workplan.md`);
- research: machine-discovery.md l. 66 ("width 32 pending C0"; the one-code-one-state plan as the
  plan in force) and "What stands between" item 1.

**Evidence:** all three workplans were retired, and are readable only via `git show`. C0 was read on
2026-10-20, and the one-code-one-state plan was retired the same day.

**Recommendation:** cite the `git show` forms (as next-steps.md does) and the state-formation
workplan.

### F31 (S4). Per-host manifests don't verify on the archive as written

**Where:** `data/window-recurrent/state-formation/option1/` (`stone-option1-d64.sha256`,
`klip-option1-d64.sha256`; `option1.sha256`).

**Evidence:** `sha256sum -c` from the archive fails on `probe-d64/launch.log` (renamed
`launch-stone.log` and `launch-klip.log` on copying). `klip`'s manifest names `data-d64/probe-d64/...`
and so fails 1,351 lines. With the paths mapped, `stone`'s verifies with 0 problems, and `klip`'s
with only `data-d64/temp` (the thermal guard's file) absent. The content is intact.
`option1.sha256` (570 files) verifies but predates the continuous probe (D54) onward. The handover
already plans its regeneration. The other manifests checked (E3-E4, E2b', the division and
approximation claims, the `p` 11 ladder, the guard's replays) verify with 0 problems.

**Recommendation:** when copying, keep host files under a `HOST/` prefix rather than renaming them,
or write an archive-side manifest after the copy. Regenerate `option1.sha256` as planned.

### F32 (S3). The stage B tool the bound as trained (D42) promised isn't built

**Where:** the workplan, the bound as trained (D42) ("Chow's test set from the read machine ...
built as stage B's first tool, run offline on the panel's stops"); `indrajala_ml/studies/window_tasks.py`
(only Chow's `k`).

**Evidence:** no transition cover, characterization set or test-set generator exists in the code.
The panel it was tied to never ran.

**Recommendation:** build it as an offline tool and run it on the D54-D64 stops. It is the exact
answers-only check discovery needs (F6, F7).

### F33 (S3). A registered probe whose trigger fired was neither run nor set aside on the record

**Where:** the workplan, the bounded handover's probe (D34's probe, `~/code/probe-d34.sh`,
registered 2026-10-21 08:30) and D38's reading and D34's order (D45: "runs only if D38 is refuted
on S3 ...; if D38 holds, it is set aside unrun, recorded").

**Evidence:** the coupling probe (D38) was refuted, so by D45 D34's probe should have run. No data
for it exists on `pyramidon` (its registered machine), and the workplan records no reading and no
setting aside. The continuous crystallisation (D48) superseded the coupling it bounds (D50 replaced
D25's window) the same evening, which is the likely reason, but the record doesn't say so. The
consistency review's item 8 asked for exactly this record.

**Recommendation:** one line in the workplan: D34's probe set aside unrun on 2026-10-21 evening,
superseded by the coupling from sharpness (D50).

## Not findings: what was checked and holds

- **Statistics:** recomputed with `indrajala_ml/studies/inference.py`:
  - every Fisher test in the papers (6.9e-5, 5.0e-6, 0.0017, 2.2e-4, 0.0033, 0.044, 7.3e-12, 0.031);
  - every Holm adjustment (A1-A3; C2-C4 and C6);
  - Cochran-Armitage (z 2.45, p 0.014; z 0.79, p 0.43);
  - every Wilson interval quoted in the notes.

  All match.
- **Manifests:** six across the phases, from the claims to option 1 (F31 for the per-host ones).
- **E1's arithmetic example** (1559 + 6329 + 5231 = 13,119) and P1's counts (105 networks; 57
  working; 52 certified; 48 robust) against `window-recurrent-report.md`.
- **The margin stop's counts:** 10 of 12 = S3 4, move-to-front-4 4, the continuous probe's (D54)
  move-to-front-4 2. Consistent with the table's 7→11 and 3→7.
- **The registration headers' existence** for every probe from 4a on, and the stage-0 gates
  honoured (the order-biased cool (D65); the paced coupling's (D61) fresh-seed batch dropped).
