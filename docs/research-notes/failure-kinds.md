# Failure kinds: what stops a network learning a machine (a living map)

**Written 2026-10-19 at the owner's request as a three-bottleneck view; renamed 2026-10-21, at the
owner's direction, to failure kinds named by what fails and how it is measured** (the first
bottleneck split in two once `state-separation` told formation from conversion,
[state-formation-workplan.md](https://github.com/davidbarkhuizen/indrajala-ml/blob/main/docs/workplans/state-formation-workplan.md)). Every failure seen since the general
algebras' round 1 is one of four kinds, each with its own cause and its own fix. A fix for one isn't
expected to move another, so a study's failures are each classified first, and a remedy is chosen by
its fit to the kind (the workplan's D31). This file maps them to their evidence and plans; the
evidence lives in the probe script's findings (`scripts/modular_family_probe.py`) and the plans named
below. Update a row when a result is read, and date it in the log at the end.

**What it serves:** [machine-discovery.md](machine-discovery.md), the work's goal from its inception:
discovering an unknown finite-state machine from its behaviour and known structure (its
approximations, a state bound), the machine read off a network and proved. Discovery needs a network
that learns a machine reliably: these failures are what stand in the way.

A transducer is two functions of the state: the transition `delta`, the next state, and the output
`lambda`, the answer. The four kinds:

| kind | what fails | measured by |
| --- | --- | --- |
| **formation** | the continuous network's cell outputs never carry the target's state | `state-separation --live` near chance |
| **conversion** | the continuous state carries it, the snapped codes lose it | `state-separation` snapped against `--live` |
| **extra codes** | a snapped state with an exact core, but longer words reach codes standing for several states, whose transitions break | pairs per code above 1 (`breaks`, `by-length`) |
| **answer separation** | the machine exact, some answers on it wrong | the certificate's answer errors on an exact machine |

**Older names, for the dated text:** *bottleneck 1* and *failure A* are formation or conversion
(before 2026-10-20 the two weren't told apart: S3 without a curriculum was formation, 4a's S4 and S3's
k-means snap conversion, the rest unassigned); *bottleneck 2* is extra codes; *bottleneck 3* is answer
separation. The table below is as of 2026-10-19, its first column the two then undivided.

| | formation or conversion (failure A) | extra codes | answer separation |
| --- | --- | --- | --- |
| **what fails** | no state forms: 2-6 codes a factor, the state's share 0.06-0.35, the machine minimising to 3-6 | a state forms with an exact core (each state's first code breaks 0-4% of its transitions), but longer words reach many more codes, whose transitions break | the machine is exact, but some answers on it are wrong |
| **where seen** | S3 (round 1, 5 of 6 failures); move-to-front 4 (round 1, P1: seeds 0, 3, 4); move-to-front 5 (round 2, 4 of 6; B2's first three seeds) | S4's near miss (round 1); random-4-0, random-q16-0 (2b, A, B, P2); S5 (round 2: 385-748 codes for 120 states, minimised to 175-842; B2's first three seeds: 425-737) | division `p` 13 (L3 seed 5 only: its 169-state machine exact, 15-22 of 1,521 answers wrong; L3's other five failures are in 2) |
| **cause, as far as shown** | the commitment's pull: with nothing yet distinguishing the states, a constant meets it most cheaply. Diagnostic (2026-10-19, registered): with the commitment off for steps 1-5, 3 of 6 failure-A runs formed a state (0.87, 0.97, 1.0) and S3 seed 5 certified; the states eroded when it returned at step 6 | not duplicates: an extra code's outputs are wrong within `d` tokens, so the network's own equivalence can't merge them (A's reading). Not rarity (random-4-0). Where they first arise is unshown | a crowded window: the answers and every factor's transition read one 16-wide stream; its features don't linearly separate the answers (the separability check) |
| **tried** | the commitment off early (the diagnostic: forms states, doesn't keep them); the thermostat (0 of 6 twice; states formed and eroded at its return); annealing as built (0 of 8: codes merged above the critical temperature); **the commitment never on: 4 of 6 failure-A runs certified, but harm where it worked** (S4, division at 32) | A, consolidation (0 of 6, pulled little); B, the long tail (0 of 6, a longer exact prefix in 2 seeds); P2, restore the step's best (0 of 6: the best was never a machine); P1, the guard (fewer certified); **R3/R4 at 32 (C2): S5 2 of 6, move-to-front-5 3 of 6, against 0 of 6 each: works** | readout-tune (15 left: not an under-trained readout); W1, the window 32 wide: **5 of 6 against 0 of 6, cured** |; R1, the answers' own branch: 0 of 6 at 16 and at 32 (harm on division at 32)
| **plan** | [state-formation-workplan.md](https://github.com/davidbarkhuizen/indrajala-ml/blob/main/docs/workplans/state-formation-workplan.md), option 1 (the annealed initial snap: a continuous warm-up, codes from the states seen, cooled from the critical temperature) and option 2 (cell noise) | the same plan, option 3 (the rotation trick); R3/R4 an option | width 32, the base |
| **next** | the plan's stage 2: Rose's critical temperature on annealing's merged networks, Zhao et al.'s effective dimension on the failure-A runs | after option 1 | division `p` 17 at width 32 (not planned) |

## The bottlenecks ranked (2026-10-27)

At the owner's request, after paper 1's tests and the recombining window's first probe. **The main
bottleneck is reaching a state in training, not the architecture's capacity:** the same network
certifies S4, move-to-front 4 and random 16-state machines on some seeds (paper 1's T5, T10, T10r),
so it can represent them; most failures are seeds whose training never reaches one. Since results
are proved, one find settles a machine and a rate is a cost ([machine-discovery.md](machine-discovery.md)),
so each bottleneck below limits the machines within a budget's reach. Ranked by evidence:

1. **Formation, the main one on hidden-state machines.** No state forms: 1-8 codes a factor of the
   15 available, the state's share 0.09-0.30, machines minimising to a few states. Seen in T5's
   failed S4 seeds and in the recombining window's probe on four of them (seeds 300-303, 400
   epochs, 2026-10-27: none certified, the same signature a little stronger: at the end more codes and a
   state share of 0.20-0.30 in three, against T5's 0.09-0.17 at 600, and seed 301 losing its state
   at its last step; claims nothing). Its cause, as shown, is the
   commitment's pull before states are told apart. Its remedies are training dynamics: the
   crucible (S3 8 of 8), and the strongest, the target's approximations as outputs (paper 1's
   claim A). A structural change didn't move it.
2. **Extra codes at scale, no cause shown.** An exact core, longer words reaching codes standing
   for several states (S5: 385-748 codes for 120 states). Width (R3/R4 at 32) moved it (5 of 12).
   The likeliest limit as machines pass about 100 states.
3. **The shared stream's width (answer separation).** The answers and every factor's transition
   read one stream; 16 failed division at 13, 32 cured it (W1, 5 of 6). Untested past 169 states.
4. **The fixed factor layout.** Two factors and a fixed codes ratio for every machine (one general
   architecture, by design, where Brandoit et al. 2026 size heads to a known decomposition). A
   machine whose decomposition doesn't fit packs its state into joint codes; a primitive one has
   none. Likely costs rate more than reach; the 32-wide factors and the recombining window address it.
5. **Retention.** Near solutions found and lost when trained on (every random-q16-0 run; L2's
   collapses). The stop at the first certified step keeps a solution once reached, not a near one.
6. **A run's cost.** About 1-4 hours a run on CPU; with one find enough, runs times epochs a
   certificate decides which machines are within reach. Approximations cut it; cheaper runs would.
7. **The state bound** (for proof, not training): an unknown machine needs a bound or a sweep
   upward guarded by Chow's test set (T6: wrong stops at 1.1 times the bound, each caught).

**Not likely a bottleneck:** depth for expressiveness, since the state is carried recurrently by
snapped codes, not computed by fixed-depth layers; nor holding the transition table, since the
successes hold it. **So after paper 1** the first work is on formation (training dynamics,
approximations, the crucible); the recombining window and depth serve scale (2-4).

## The common measure: one code, one state (2026-10-19)

Every certified network has each of its codes standing for exactly one target state (pairs per
code 1.0, `breaks`); each failure kind is a way of missing that: no state (formation), a state lost
by its codes (conversion), codes standing for several states (extra codes), an exact state with wrong
answers (answer separation). The numbers (1), (2), (3) below are the 2026-10-19 bottlenecks. Read across W1, L3, B1 (mid-run), B2 and
round 2 in `git show df1dcac:docs/one-code-one-state-workplan.md` ("Why"), which plans
the remedies: the answers' own branch with the factors on the shared window (3), pairs per code
logged and used to keep the best machine, counterexample training (2), the thermostat (1).

- **B2 (2026-10-19): the branches moved 1 and 2 in one seed each** (S5 1 of 6, move-to-front-5
  1 of 6, against 0 of 6 each in round 2): works, gain undecided.
- **Division at width 16 was mostly 2, not 3 (stage 6's findings, 2026-10-19):** L3's five other
  failures stood at 20-135 pairs per code; only seed 5 had an exact state. B1's failures (26-76) and
  W2's at width 22 (34-120) are the same kind, so the branches didn't move division (as first read
  from B1 mid-run); width relieved it (W2 3 of 6, W1 5 of 6).
- **The branches, not adopted:** B1 1 of 6 and B2 1 of 6 a cell (works, gain undecided), W2 3 of 6
  at B1's size, and harm on S4 (B3, 0 of 6 against round 1's 4 of 6, p 0.030); division `p` 11
  fell to 1 of 6 from the ladder's 4 (no harm by the rule, p 0.12), its failures in 2 (9-88 pairs
  per code). The side probe
  (branches at 32, S5 seeds 0 and 1) left pairs per code unchanged (120, 77).

## How they combine

- **One cell can hit more than one.** Move-to-front 5's seeds split between 1 and 2 (round 2: four
  failure A, two with states but no exact core). Division `p` 13 at width 16 hit 2 in five
  seeds and 3 in one (L3). So a cell's count says little until each failure is read by D9's probes (`breaks`,
  `by-length`) and assigned.
- **A fix is read on its own failure kind's cells.** The branches target 3; B2 (S5, move-to-front 5)
  hits 1 and 2, so a 0 of 6 there doesn't count against the branches on division, and isn't
  evidence the branches generalise either.
- **Across all three: retention.** Near solutions are found and lost when trained on (every
  random-q16-0 run; L2's collapses). Stopping at the first certified step keeps a solution once
  reached; it doesn't help a run that only came near. The guard as built freezes near solutions
  (P1); its first softening, arming only on a step that passes both verdicts, is in
  [next-steps.md](https://github.com/davidbarkhuizen/indrajala-ml/blob/main/docs/next-steps.md).

## Log

- 2026-10-19: written. 3 is cured on division at 13 by width (W1); the branches' answer (B1,
  W2) tonight. 1 has a cause shown (the commitment) and a fix to build. 2 has no remedy that
  works and no shown cause.
- 2026-10-21: renamed to failure kinds (formation, conversion, extra codes, answer separation),
  the owner's direction; formation and conversion told apart by `state-separation` (2026-10-20).
  The quasi-static crucible cured both on word-problem-s3 (8 of 8 certified; findings 4a''''); the
  handover probe (4a''), with no crucible, certified move-to-front-4 seed 3 under every shape, which
  hasn't yet certified in the crucible (corrected 2026-10-21, [reasoning-review-2026-10-21.md](https://github.com/davidbarkhuizen/indrajala-ml/blob/main/docs/audits/reasoning-review-2026-10-21.md));
  the panel (4b) classifies what is left. The 2026-10-19 table's "plan" and "next" rows are
  superseded: D31 shelved options 2-4, called down only by the panel's diagnosis
  ([consistency-review-2026-10-21.md](https://github.com/davidbarkhuizen/indrajala-ml/blob/main/docs/audits/consistency-review-2026-10-21.md)).
- 2026-10-19: the common measure (pairs per code) and its workplan; B2 read (1 of 6 on each
  cell).
- 2026-10-19: the window branches' stage 6 read and the plan retired (not adopted: harm on S4).
  Division at width 16 was mostly 2, not 3 (L3's other five failures read). R3 and R4's probe
  certified S5 seed 1, a seed that failed in round 2 and B2: the first move on 2.
- 2026-10-20: the night's results (the probe script's findings): **1** forms with the commitment never
  on (4 of 6) but that harms where it worked, so the commitment hurts before a state forms and helps
  after (Zhao et al. 2026); annealing as built merged its codes (Rose 1998's critical temperature);
  **2** moved with R3/R4 at 32 (5 of 12); R1 shelved. The owner abandoned the open plans and set
  [state-formation-workplan.md](https://github.com/davidbarkhuizen/indrajala-ml/blob/main/docs/workplans/state-formation-workplan.md): the literature review's options, one at
  a time.
- 2026-10-27: the bottlenecks ranked (above): formation first, a training-dynamics problem, not
  capacity; the recombining window's probe on four of T5's failed S4 seeds certified none.
- 2026-10-27: the incremental reheat's probe (six S4 runs, claims nothing): none certified. The
  state formed in every run (a share of 0.97-1.0 within 175 steps) and was lost 45-80 epochs later;
  stepping back one stage at a time never recovered it, each run walking back 16-21 stages to its
  first. On these runs the loss, not formation, is what stops the cool: evidence for retention
  (5) as a cause of 1's signature in the crucible.
