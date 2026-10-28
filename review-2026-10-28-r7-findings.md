# R7 review of paper 1, 2026-10-28

The critique of `papers/learning-transducers-with-proof.tex` (at 7780ce6): mechanical checks (M), a
fresh-context review of the claims against indrajala-ml's `docs/workplans/paper-workplan.md` (C),
and a fresh-context literature review (L). Line numbers are the manuscript's at 7780ce6; "wp" lines
are the paper workplan's. Reviewers reported only; each finding is to be restated to the owner with
options before any correction. "Checked" marks a finding verified by hand beyond the reviewer.

## Mechanical (M)

- **M0. Passes.** `paper_tables.py check`: every table and marked number the same. Figure 1:
  the sum and difference congruences follow from `A' = 3A + a`, `B' = 3B + b`; the product's
  counterexample holds ((1,1), (2,3) in class 1; token (1,0) to (4,3), (2,4), classes 2 and 3);
  "22 of 25" holds (the merged states (1,4), (2,3), (3,2), (4,1), quotient -1). Figure 2 matches the
  method and the code.
- **M1 (major; F31 recurs; also C24). Four paper manifests fail as written:** `t2-t5` (9), `t6`
  (14), `t10` (135), `t10r` (150), all `proof/` files rewritten by R3's fixed-reader re-run
  (2026-10-28); the old files in `proof-loose/` match the old hashes; the new ones verify under
  `t6-proof.sha256`. Proposed: repoint the old manifests' `proof/` entries to `proof-loose/`
  (hashes unchanged). The T4' findings (wp l.1453) call T10's and T10r's manifests "unchanged".
- **M2 (minor).** `t4-fresh.sha256` verifies only from `paper/t2-t5/approximations`, written only in
  the workplan; the datapack's verify page must say so.
- **M3 (minor).** The reproducibility paragraph (l.606) omits t6-proof, t6-strict, t10, t10r, t11,
  t12, t4prime and p2-check.
- **M4 (nit).** Figure 2's caption, "its pooled state": each factor has its own pooling query.
- Outside paper 1: the `*.before-factored-state` manifests (superseded, expected) and nine
  per-host manifests in `state-formation/option1` (files missing) fail.

## Claims against the data (C)

1. **(major) The paper-wide Holm family was registered (D5, wp l.179-181; D13, D14, D15, D20, D31)
   but applied only within tests.** l.324-325 says "Holm across the paper's family". The reviewer's
   recompute over the 11 registered tests: T1a 0.061, T10b 0.103, T1b 0.18 (without T12: T1a
   0.0505, T10b 0.082); T2b, T3a/b, T11 S4 and move-to-front-4 survive. Options: apply it and
   restate A2 and A4's T10b (T10r, read alone under D24, then carries A4), or state that it was not
   applied and why. *To recheck by hand before the owner decides.*
2. **(major) "Not that of being told the state" survives against T12's "neither"** (wp l.1530-1534):
   contribution 2 (l.99-100), intro (l.85-86), abstract (l.53), A2 (l.414-415), related work
   (l.131-132). A2 l.438-442 has it right. Fix: say the state did at least as well as the cover (17
   against 11 of 20, two-sided p 0.08, no difference detected), the cover's help consistent with
   state supervision; "two outputs that tell about the state without being approximations did not
   help".
3. **(major; checked) The product does not tell the state as much as the sum beside the quotient**
   (l.413, l.98, l.575): with the quotient, 10 of 25 classes against the sum's 22; its classes alone
   9/4/4/4/4; never learned (F3: 0.71 at best). Fix: say so; add the arm to "What the outputs tell".
4. **(major) The suffix control's caveat is missing** (D13, wp l.326-329): its outputs need a
   125-state machine, 256 joint codes only 2.0 times that, against l.317-318's "at least 3 times".
   "Learnable" (l.97, 403) holds by construction, not shown. Fix: state it at l.404-409; except it
   at l.317.
5. **(major) A4 reads "no help detected" as "no help"** (l.101-103, l.476), against D29 (wp
   l.932-934); the given-against-present contrast (P2 against P1, signed-rank p 0.031, wp l.1377) is
   exploratory and unmentioned. Fix: "no help was detected (3 against 2 of 15, p = 0.50;
   underpowered)".
6. **(major) Planting's structural shift is unstated** (D24, wp l.778-780: `order` 0.77 against
   1.11; non-identity token ranks 10.43 against 8.80): the abstract (l.56-57) reads as the given
   approximation's effect. Fix: one sentence in A4; the abstract names the contrast as registered.
7. **(major) A6's mechanism claimed universally** (contribution 4, l.104-105; intro l.86-87) against
   move-to-front-4 (16 of 18 hold other orders, wp l.1508-1510), T12's state networks (A or B, not
   given, wp l.1543) and unasked networks (places, T4). Division's "every such congruence is one of
   the trained lines" (l.526-528) is unregistered (wp l.1050) and unlabelled. l.524 "the registered
   prediction ... held only partly": the registered expectation was the opposite (fewer than a
   quarter, wp l.239-243); the result is mixed. T4' 5 of 22 not set against its expectation of half
   (wp l.1442). Fix: scope contribution 4 to division (exploratory) and S3; label; restate T4c and
   T4' by their rules.
8. **(major) The discussion (l.570-572) calls the cover "a coarse approximation";** it determines
   the state. Fix: name the sum (10 against 1) and the planted blocks as coarse; the cover apart.
9. **(major; F9) Both sides not reported where they differ:** l.325 "one-sided as registered"
   contradicts T12 (two-sided); T1b 0.046 one-sided, 0.091 two-sided. Fix at l.325 and l.407.
10. **(major) A5's pairs determine the state too** (l.489), so T12's caveat applies; limit 3 names
    only the cover. Fix: one sentence.
11. **(major) Appendix D (l.765-803) has no body,** only a table and two draft notes, though the
    intro and discussion lean on it; also the 100pt overfull box (l.802-803).
12. **(major) "Quotient" in two senses** (congruence quotient; division's output A B^-1); "product"
    in three (machine product, AB mod p, product machines). Fix: "the ratio" for division's output;
    "direct product" for machines. (Also L4.)
13. **(minor) An approximation of a Mealy machine is a congruence of its transition structure,
    outputs set aside** (the answer is no function of the sum); l.81-82 overstates what Krohn-Rhodes
    and holonomy build from. (Also L3, L12.)
14. **(minor) Two cells, said to be one** (l.549-550, l.587 against l.296-298); l.296 omits T12.
15. **(minor) The cover arm's 15, 13, 11 across Table 1, T3's control and T12 not set side by side**
    (wp l.1535-1538).
16. **(minor) "Most failures came near a solution"** (l.706-707): about 84 of 253; "near" is not "a
    solution".
17. **(minor) Appendix A's "the only networks to fail a long test were T3's 20"** (l.644-645)
    contradicts Appendix B (l.694-697); its counts omit T10, T10r, T11, T12.
18. **(minor) Appendix E's title** ("networks not given approximations") is wrong for Table 9; T4a's
    fresh set passed at its bar, resting mostly on move-to-front-4.
19. **(minor) "Every comparison at 20 fresh seeds an arm"** (l.324): not T10, T10r (machines as
    unit); T11's control is T5's batch.
20. **(minor) Contribution 2 promises every arm's state information;** l.234-240 omits the suffix,
    token, product, state and T11 arms.
21. **(minor; F2) The certificate guard's training harm is omitted** (l.715-716; 1 of 6 against 3
    of 6, D2).
22. **(minor) Undefined or late terms:** screen, both verdicts, near/collapsed, trained lines,
    backdrop names, T-/P-/A-labels (a test-to-section table), places/pairings/order/ahead, uniform
    and stratified catalogues, spent. `tab:extra-outputs`, `app:controls`, `tab:baselines` never
    referenced; the opening draft note's "Appendices A-G".
23. **(nit)** l.293 "about 8.5 times" (8.5-9.0) and "15 at p = 5"; l.623 "are public" (not yet);
    split the abstract's certificate sentence; l.55 add "at 20 seeds an arm".
24. = M1.

**Audit items:** resolved F6, F8, F14, F16, F18, F22, F23, F26, F32; partly F2 (C21), F3 (C2-C4),
F7 ("one certified run settles a machine" needs the target or an exact bound and Chow; limits 1/2),
F9 (C9), F17 (C14); still holds F10 (constants unlabelled as chosen: fork 0.6 and 4, snap 1.05,
near 0.95, 32/11, 3 times surplus), F31 (M1); the rest not bearing on the manuscript.

## Literature (L)

1. **(major) "Hidden" and "proved" undefined in the paper; the size record rests on both.** Giles
   1995 is "told" only through teacher-forced fed-back outputs (giles-1995 l.186-187, 267). Omlin &
   Giles 1996 (held, uncited) recover a random minimal 10-state DFA exactly by extraction (l.517-521;
   the network itself errs on long strings, l.560-562). Fix: define both in Method (told = inputs and
   training targets at t determine the state, fed-back outputs included; proved = complete
   enumeration of the network's own machine); claim "the largest machines whose trained network is
   itself proved equal to the target, the state hidden"; footnote Omlin & Giles.
2. **(major; checked) Brandoit 2026 is nearer than related work says** (l.127-133): each head holds a
   congruence, the state decoded through an injective chi (brandoit l.3024-3037, "acts head by
   head"), a cross-entropy on the state (l.3384): the cover arm's analogue plus the state; their
   Prop. G.4 is A6's theoretical counterpart. The novelty stands only through "as outputs, without
   its states"; with T12 the gap is narrow for the cover; what remains is the single coarse
   approximation (A2, A4) and the controls.
3. **(major) Terms attributed loosely** (l.80-82, 134-136, 184-186): Egri-Nagy & Nehaniv 2024's
   approximation is the image of a surjective (relational) morphism (l.126-134; checked), congruences
   one way to get one; holonomy 2015 uses "approximation" and "cover" otherwise (l.172-176, 289);
   Krohn-Rhodes 1965 uses neither. l.82 wrong on what the decompositions build from. Hartmanis &
   Stearns 1966's S.P. partitions and parallel decomposition are the established terms for this
   construction (not held).
4. **(minor)** = C12 ("given the quotient's cover").
5. **(minor) Liu et al. 2022's Dyck(4,8) with stack-top observation (4,681 states, LSTM 100%)** is
   missing from "hidden, tested" (l.788-799); their numbers are maxima over 25 runs.
6. **(minor) DeepDFA:** 28 of 30 states read, 100 +- 0 on the best 5 of 10 runs to length 150, no
   equivalence check; say the record holds for what was reported.
7. **(minor) Zeng 1993** shows 4 states explicitly, targets up to about 8 (l.539-541, 130-150).
8. **(minor) Giles 1995's** zero error is a run average on the identifying set; the 256-state net
   "not usually" perfect (l.339-341).
9. **(minor) Li 2025 half reported** (l.122-124): the parity loss steered models to an algorithm that
   does not generalise (H.3, l.1272-1288): an approximation given, worse length generalisation.
10. **(minor) Dan 2022 §5.4** (free auxiliary signals, l.392-409): a non-approximation output helped;
    cite in A2; "generalise robustly" (l.69) means distribution shift there.
11. **(minor) Brandoit's "every seed"** is all 5 seeds (40 of 40 runs).
12. **(minor)** = C13.
13. **(nit) The exclusion bound:** Moore 1956 Thm 7 (2n - 1); m + q - 1 by his direct-sum argument;
    "exclusion bound" is ours.
14. **Bib:** wickramasinghe-2026 first author (Sandamali Yashodhara; PDF now held, literature #32);
    yang-2026 COLM 2026; shakerinava-2026 ICLR 2026; nowak-2026 ICML 2026 PMLR 306; moerman-2017,
    egri-nagy-2024, kocsis-2024 published versions (unverified); liu-2022 year 2023; hong-2025 drop
    "(Technical Report)"; oncina-1992 against Oncina, Garcia & Vidal 1993; extra.bib stray brace
    after huang-1986.

**Missed papers:** Zhang & Li 2026 (arXiv 2609.29951; networks hold coset/quotient stages; cite in
A6 and App. D; held, literature #32); Omlin & Giles 1996 (L1); Hartmanis & Stearns 1966 (L3);
optional: Das & Mozer 1993/94, Tino & Sajda 1995, Howe 2026. Searches (2025-2026) found no work above
24 states with a proof and the state hidden.
