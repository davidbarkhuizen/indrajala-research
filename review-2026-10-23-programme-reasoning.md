# The programme's reasoning: inconsistencies, gaps and assumptions (audit, 2026-10-23)

**Status: a dated review, deliverable 2 of the programme audit** (indrajala-ml
`docs/workplans/programme-audit-workplan.md`, #953). The owner's request: "a summary of logical
inconsistencies, gaps and bad assumptions". Each item cites the finding that records its evidence
and recommendation in
[`review-2026-10-23-programme-findings.md`](review-2026-10-23-programme-findings.md) (F1, F2, ...).
The evolution is in
[`review-2026-10-23-programme-evolution.md`](review-2026-10-23-programme-evolution.md). Nothing here
changes a document. Corrections follow in their own PRs, and anything that touches a claim is the
owner's call (the plan's D2).

**The auditor is an author.** Claude implemented, ran and drafted most of what is audited here. The
reading tries to be adversarial, but an outside cold read (the publication route's own step) is
still needed.

## The short version

The programme's core holds up. The certificate is a real proof, every statistic recomputed matches,
the manifests verify, and registration is practised, not just stated. The weaknesses lie in four
places:
1. **Readings made after the data, where the record says registered.** The fresh-seed rate's verdict
   was re-scored by the deadline's completion (D67). A design-seed rate is used as the comparator.
   The registered continuous arm of E2b' had already been seen.
2. **Claims that outran their evidence and were not walked back.** The guard is called untested in
   training, though it was tested and did worse. "Because it is an approximation" rests on one
   control that differs in two ways. "Groups need a seed" is drawn from one machine of each kind.
   "Every failure freezes" is close to true by definition.
3. **A method that kept changing without its own acceptance gate.** The panel never ran.
4. **A goal (discovery) whose premises are assumed rather than tested.** The state bound is always
   exact. The certificate needs the target. Restarts assume a verifier that discovery doesn't have.
   The known approximations that P2 showed matter are absent from the current method.

## 1. Logical inconsistencies

### 1a. Rules the programme states, against what it does

| rule (where) | practice | finding |
| --- | --- | --- |
| No settings or analysis changed after seeing results; a flaw is recorded, the study runs as registered, the fix is a new experiment (experiment-design.md §2) | The fresh-seed rate (D64) was read at 05:30 as 7 of 12, one short of its bar. At 06:05 the deadline's completion (D67) was registered, with its outcomes to "stand in for" the cut runs and "the bar met if any of the three certifies". D64's registration had listed "the deadline's stops" among its readings. | F1 |
| Adopt a remedy only on a fresh-seed rate against the current method's, never on rescued seeds (the owner, 2026-10-22) | "The method's current rate" quoted for comparison (D61, D64, both research notes) is the margin stop's re-run of the fresh-seed matrix's (D55) own seeds. Those are the seeds the margin stop was designed from, and D55's S3 bar was refuted as registered. | F4 |
| One change between an experiment and its follow-up (experiment-design.md §2, D26 of the claims plan) | The continuous crystallisation (D48) changed five parts at once, at the owner's explicit direction ("all at once"). The record names this, but the rule was never amended. | F5 |
| Each option is understood, built, tested on the panel and accepted or rejected before the next (D1, D11, D12, then D40) | The panel never ran. Option 1 was never accepted or rejected; it was rebuilt about thirty times. Options 2-4 were shelved pending a diagnosis the panel would have supplied. | F5 |
| Fisher's exact test two-sided (experiment-design.md §3) | Several registrations use one-sided tests (the general algebras' E1, B3's harm, P2's registered claims, C2b). The "significant failure" bar, 0 of 6 against 4 of 6 at p 0.030, is 0.061 two-sided. | F9 |
| No constants without a derivation (the owner's convention; D61's rejection of a fixed cap) | The method carries at least a dozen fixed constants: the gate's 0.95 and 0.99, the halving of 30, growth at 0.02, hardness at 0.999, a margin wait of 200 steps, the crucible's cap of 8, `kappa`, `T_hot` at 2 `T_c`, a hold of 20, a codes ratio of 32/11, a width of 32. Their sensitivity is unmeasured. | F10 |
| Epochs, not wall-clock, bind a run, because minutes give a run's outcome its machine (D46, 2026-10-21) | The probes from 2026-10-21 evening to 10-22 (D54-D64) registered "1,600 epochs or 690 minutes" and ran on a loaded machine, so ten runs were cut. The lesson was written on 2026-10-21 and re-learned on 2026-10-23. | F12 |
| A study moves between machines only between whole runs; a mid-run resume isn't checked for bits (experiment-design.md §5) | Runs were moved mid-run with `--resume` (D63, D67), justified by resume tests and cross-machine parity. The practice is defensible; the protocol's text is stale. | F24 |
| Every cell's training reaches the exclusion bound (the research notes' Settings) | Certificates come before growth (S3 at length 8 against a bound of 69). D42 restated the rule as a property of the config, and required each claim to say "certified, trained to length L". The notes still say the training reaches the bound and give no trained lengths. | F8 |

### 1b. Claims against their own evidence

- **The certificate guard "repairs" the collapse and is "untested in training"** (P1 §Training past
  a proof and Limitations; `contribution.md` row 3b). It *was* tested in training (P1 of the
  consolidation plan, read 2026-10-19). It froze near solutions and certified fewer seeds (1 of 6
  against 3 of 6 on move-to-front-4). The repair holds on 10 replays of one network. **F2**
- **"One approximation helps, because it is one"** (P2's abstract and §One approximation;
  `contribution.md` 5b; `next-steps.md`; `machine-discovery.md`). The control, the product, differs
  from the sum in two ways. It is not a congruence, and it cannot be learned as a counter of its own.
  An approximation is exactly an output computable from its own past, so the design cannot tell
  "approximation" from "an extra output the network can learn by itself". The registered test (sum
  against product) holds; the "because" goes beyond it. **F3**
- **"Groups need a seed; resets form from the whole distribution"** (the status note's abstract;
  the crystallisation note). The claim was drawn from one machine of each kind. Its mechanism (no
  synchronising word) explains conversion, while the failure was formation. Both 2026-10-21 reviews
  said so, and the consistency review asked for "on the two machines tried" at the next revision. The
  status note's abstract is unchanged. **F15**
- **"The state count alone isn't the limit: division certifies at 121 in the same cell"** (the
  general algebras' round 2; the transition note). Division was trained on its approximations' outputs
  (sum and difference); the algebras had one output that hides most of the state. Only the cell's
  settings matched. **F16**
- **"Every failure ends frozen; the schedule is not the lever"** (the freeze findings;
  freeze-and-restarts.tex). The freeze is defined as the clock held at zero, which the gate (D49)
  does whenever the screen stays below 0.95 of the hold's level. Certified runs freeze and thaw too
  (S3 30, 40, 41). So "every failure freezes" is close to a property of the controller, not a finding
  about the network. The step to "no schedule passes it" rests on a thermodynamic analogy whose
  relaxation time was never measured; the note says so. **F11**
- **"Random machines fail at forming, S4 at keeping"** (the scaling conjecture;
  freeze-and-restarts.tex). The fresh-seed rate (D64) contradicts the S4 half: two of its three S4
  failures never formed. **F19**
- **"The handover is needed"** (the coupling probe (D38)). D38 refuted its own registered bar (at
  least 6 of 8 with the coupling at 0). As a comparison with the quasi-static crucible, 4 of 8 against
  8 of 8 on design seeds is Fisher p 0.077 two-sided. **F21**
- **"Training stops at the proof"** stated as a condition of success (P1's Discussion), while E2b'
  kept the proof at every step in 19 of 20 runs. **F22**

### 1c. Documents against each other

- **`contribution.md`, "the current statement"**, was last updated 2026-10-21. Rows 9-10, "Open" and
  "Where it is weakest" predate the following:
  - the answers-only stop (D35);
  - the continuous crystallisation (D48);
  - the fresh-seed matrix's (D55) refutation;
  - the margin stop (D59);
  - the fresh-seed rate (D64) of 7 of 12, and 0 of 10 on the larger and random machines.

  Its row 1 says "724 distinct networks certified", while P1 says the certificate "ran on 724 distinct
  trained networks". **F13, F14**
- **The repository README** says P1 has E2b' "to add" (it is in) and P2 the approximation claim and
  `p` 11 "to add" (both are in). P2 has no 169-state result, though `contribution.md` row 4 lists it.
  **F27**
- **The restart cost is 4.4 times in one place and 3.5 times in another.** The README and
  freeze-and-restarts.tex give 4.4x, read in steps; the crystallisation note and the workplan give
  3.5x, read in epochs. **F13, F27**
- **The feasibility register** has no coupling row, though the consistency review promised one once
  the coupling probe (D38) was read, and D38 showed the coupling exists. Its row 13 is the answers-only
  stop (D35), not the margin stop (D59) under the margin deadline (D60). **F24**

## 2. Gaps: what the aim needs that is missing

The aim is machine discovery (`machine-discovery.md`, stages A-F). Today's evidence covers stage A
on machines of 6-24 states.

1. **Discovery's premises are untested.**
   - **The state bound.** Every rate is at the exact bound `N = q` (the exact state bound (D43)).
     The slack reading planned "offline on the panel's networks" never happened, because the panel
     didn't run. At 1.1 times the target's size the re-reading found 25 false stops and a false
     discovery. **F6**
   - **The verifier.** Restarts are justified as Las Vegas runs (Luby), and the batch runner's
     "find" mode is described as discovery's use. In discovery there is no certificate, only the
     answers-only stop, which is not free of false positives under a slack bound. **F7**
2. **No stage B tool.** The exact answers-only check (Chow's test set from the read machine), which
   the bound as trained (D42) promised as "stage B's first tool, run offline on the panel's stops", is
   not built; only Chow's `k` exists, inside `window_tasks`. **F32**
3. **The two strands are not joined.** P2's central result is that known approximations given as
   outputs make product machines learnable, and discovery's premise is that some are known. Yet the
   state-formation method trains on answers alone, and the probe that would join them (D39 (i): an
   approximation beside S3) never ran. **F18**
4. **Generality is untested where it was lost before.**
   - The harm cells (division at 169 states, move-to-front-4 seed 0) have never run under option 1;
     S4 has, at 1 of 6 in all.
   - The 120-169 state tier, where the papers' results and the failure kinds were mapped, is
     unaffordable at today's epoch times (5.5-27 days a run).
   - The random machines certify 2 of 21 across the continuous cell's probes.

   "One general architecture" rests on S3 and move-to-front-4. **F17**
5. **No architecture control in the state-formation strand.** Whether a plain recurrent network, or
   the window without its transformer (which certified the carry automaton at `k` 1, E6), needs the
   crucible or the anneal at all has not been tested (`contribution.md` row 9; both 2026-10-21
   reviews). Every option-1 run uses the 32-wide transformer window.
6. **No sensitivity analysis** of the method's constants (F10), and no constant-lag clock or
   measured relaxation time behind the freeze's physical reading (F11).
7. **No classical baseline**, even as a cost reference. The papers say why classical learners are not
   the comparator for "does a network implement a machine". `machine-discovery.md` says they *are* the
   baseline for any discovery claim, and stage C has no plan for one.
8. **The papers' own route is unfinished.** No internal critique, re-derivation of figures from the
   data, cold read, datapack or preprint. P1 was to go first "once E2b' is in" (it has been since
   2026-10-17). **F27**
9. **Collapses are unexplained.** The collapse past a solution (P1, P2), S4's collapse at a steady
   coupling, and the freeze have each been named, traced or escaped, but not explained. The slingshot
   reading is not supported; the plasticity correlates come after, not before.

## 3. Assumptions

| # | assumption | relied on by | evidence | verdict |
| --- | --- | --- | --- | --- |
| A1 | The certificate has no false positives | every "certified" claim; D41's success; restarts as Las Vegas runs | complete enumeration with near ties branched; every certified network passes every long-test case (17 M cases in P1, millions in P2); no failing network certifies | **sound** (for the snapped network as computed in double precision; its margins recorded) |
| A2 | Runs are reproducible bit for bit across machines and resumes | moving runs mid-flight; paired designs (D61, D63) | C0 15 of 15; the continuous cell 255 rows identical on four machines; `same-prefix` per pair | **sound**, checked per use; the protocol's text lags (F24) |
| A3 | Fresh seeds are independent, identically distributed draws, and a failure that correlates with nothing early is "the phase space" | the statistical method; restarts; the batch runner | true by construction for fresh seeds; but the method's constants were set on design seeds, and its "current rate" is partly a design-seed rate (F4) | **sound for fresh seeds**; misapplied where design seeds stand in |
| A4 | A state bound is known in discovery, and tight | the answers-only stop (D35); the exclusion bound's stand-in; restarts | none: every rate at `N = q`; slack 1.1x already gives false stops | **untested; the main risk to the goal** (F6, F7) |
| A5 | Meeting the exclusion bound in the config makes a cell sound | the feasibility claims in every note | true as a property of the config; certificates come before growth, so the bound is a cap, and under D35 the stop's sampled answers stand in for it | **weaker than stated** (F8) |
| A6 | The physical picture (melt, crystal, glass, kinetic arrest) describes the network's codes | the profile (D15-D30, D48-D53); the freeze's reading; "the schedule is not the lever" | exact for Rose's deterministic annealing on fixed data (the merge and splits matched, the melting curve within a fifth of an octave with weak noise); training moves the material (the splits 2-6 octaves early); no relaxation time measured; the freeze partly the gate's definition | **useful as a design source, not established as mechanism** (F11) |
| A7 | Epochs are a machine-neutral cost | budgets, cutoffs, restart costs | true of the computation; but an epoch's cost differs between methods and grows with the length distribution (the continuous profile's epochs cost about twice the quasi-static crucible's), so comparisons of methods in epochs aren't comparisons of compute | **sound for budgets; partial for costs** |
| A8 | One general architecture, unchanged across backdrops, exists | stage A; "tasks are backdrops" | division's 121-169 needed width 32; S4 and division certified before only with the commitment, which option 1 never turns on; S4 and random 0 of 10 on fresh seeds | **open; evidence on two backdrops only** (F17) |
| A9 | The failure kinds are separable, and a fix for one doesn't move another | remedies chosen by fit (D31) | the commitment helped one kind and hurt another; the paced coupling removed every jump and changed nothing; S4 both formed (D57) and failed to form (D64) | **partly contradicted**: the kinds are useful labels, not independent mechanisms |
| A10 | Random machines are discovery's likely targets | weighting the panel and D64 toward them | an assumption about real systems, which usually have structure (protocols, controllers, parsers); stage F names structured systems | **unargued**; their difficulty matters, their priority isn't shown |
| A11 | An approximation helps *because* it is a congruence | P2 5b; machine-discovery's premise | one control (the product) that also isn't self-closing | **underdetermined** (F3) |
| A12 | Groups need a seed; resets don't | the crucible; the class line | one machine of each kind; the mechanism given explains conversion; the continuous crucible certifies both, and S4 (a group) fails either way | **unestablished as general** (F15) |
| A13 | The certificate's near-tie ratio (1.05) is the right robustness margin | D41's success; the margin stop | a convention; the margin stop shows it decides about half the early stops | **a convention, worth stating as one** |
| A14 | The window's transformer is needed | every option-1 cell | at `k` 1 the plain window certified the carry automaton (E6), and the snap made the plain recurrence extrapolate (E2b'); never re-tested under option 1 | **untested where it matters** (gap 5) |
| A15 | Restarts beat running seeds out by about 3.5 times | the batch runner's design | Luby's theory is exact for i.i.d. Las Vegas runs; `t*` on S3 is set by one early success; on S4 by 3 runs | **sound in form, rough in number**; to be measured by the runner's first batch, as planned |

## What holds up

- **The instrument.** The certificate is complete, branched and cross-checked by long tests
  everywhere it can be. It is the programme's strongest contribution and its foundation.
- **The arithmetic.** Every headline statistic in the papers and notes was recomputed with
  `indrajala_ml/studies/inference.py`: Wilson intervals, Fisher (both sides), Holm and
  Cochran-Armitage. Every one matches its document.
- **The records.** Five manifests across the phases verify. E3-E4, E2b', the division and
  approximation claims, the `p` 11 ladder and the guard's replays have 0 problems; the option-1
  manifest has 0. The per-host D64 manifests verify once their paths are mapped to the archive (F31).
- **The registration practice.** Every probe since 2026-10-20 has its expectations in a header
  before its data, and several plans were dropped on their own stage-0 criteria (the order-biased
  cool (D65); the paced coupling's (D61) fresh-seed batch).
- **Self-correction.** Restating the time axis in epochs, the D61 reading "the jumps are a symptom,
  not the cause", the correction that the continuous profile is not faster in epochs, and the two
  2026-10-21 reviews all show the programme correcting itself. What this audit adds is where the
  corrections did not reach.
