# The work's novel contribution (living document)

What the two papers contribute under their common framing, kept current as they are finalised.
Update a row when its evidence changes (a registered result read, a long test in, a critique
finding), and date the change in the log at the end. Novelty throughout is "not found in our
search", never "first". The dated reviews beside this file (`review-<date>-<topic>.md`) are
snapshots; this file is the current statement.

**The framing (agreed 2026-10-17):** can a network trained by gradient descent on input/output
examples alone, never on states or intermediate steps, come to compute a finite-state transducer
exactly at every length, and can we prove which machine it learned? P1
(`papers/snapped-window-recurrence.tex`) is the method and the small machines (3-5 states); P2
(`papers/certified-modular-division.tex`) is how it scales to product machines (25, 49 states).

**In one sentence:** a method for learning finite-state transducers by gradient descent and
proving which machine was learned, and what the proof revealed: sampled tests overstate, the snap
is what extrapolates, the exclusion bound and stopping at the first proof decide success, further
training destroys solutions, and training on the target's cover makes product machines of 25-49
states learnable from answers alone.

## Not ours (stated as such in the papers)

| what | whose |
| --- | --- |
| Snapping a recurrent state during training (straight-through), reading off and minimising its machine | Zeng et al. 1993 |
| Learned clusterings or centroids of a recurrent state | Das & Mozer 1993; Wang et al. 2019 |
| The carry automaton extracted from a trained adder | Oliva & Lago-Fernández 2020 |
| A learned adder proved correct at every length (by hand, one network) | Lan et al. 2022 |
| Perfect test accuracy, still wrong | Weiss et al. 2018 |
| The length bound behind the exclusion bound | Moore 1956 |
| Learning automata and transducers from examples (far more efficiently) | Angluin 1987 (L\*); Oncina, García & Vidal 1992 (OSTIA) |
| Separate transition and output paths in a recurrent Mealy network | Tiňo & Šajda 1995 |
| Factored categorical latents trained straight-through | Hafner et al. 2021 (DreamerV2); Liu et al. 2021 (DVNC) |
| A pooling, cell and state a module | Goyal et al. 2021 (RIMs) |
| A shared trunk with a branch a consumer (the window branches) | Vandenhende et al. 2020; Guo et al. 2020 |
| A recurrent state handed to a transformer once a chunk | Block-Recurrent Transformers; RMT; Zhang et al. 2026 (RLT) |
| Annealing a soft clustering of a recurrent state to hard, the temperature tied to the training error (a closed-loop schedule) | Das & Mozer 1993 (DOLCE) |
| A soft-to-hard schedule tied to the gap between the soft and hard losses; codes initialised from the network's own outputs | Agustsson et al. 2017 |
| Codes at the data's mean above a critical temperature; the heat capacity peaking at the phase transitions | Rose 1998 |
| An adaptive cool: the temperature steps once an equilibrium test passes, by the heat capacity | Huang et al. 1986; Romeo & Sangiovanni-Vincentelli 1989 |
| Flip-flops easy and parity hard for state-space models; non-solvable groups beyond fixed depth (S3 is solvable), as expressivity | Liu et al. 2023; Merrill et al. 2024; Sarrof et al. 2024 |
| Training on short strings first ("starting small"), and its dispute | Elman 1993; Rohde & Plaut 1999 |
| Probing a network for the target's state; transformers on permutations computing the sign first | Li, Guo & Andreas 2025 |
| A state probe separating failures a score conflates; permutation automata as a warning sign (86 of 103 fail the probe, under RL) | Allchin 2026 |
| A recurrent cell learning exact transition tables of groups and monoids, correct beyond the tested lengths | Brandoit et al. 2026 (NFSM) |

## What is new

| # | contribution | paper | evidence | status |
| --- | --- | --- | --- | --- |
| 1 | **A complete, automatic equivalence check as the instrument of a study:** whether a trained network is the target transducer at every length, or a counterexample; every window from every reachable code (531,441 at `k` 4), outputs and states, near ties branched both ways, numerical margins; run on hundreds of networks | P1 | run on 724 distinct networks in P1's studies (not all certified); every division network in P2 | strong; the strongest contribution |
| 2a | **Sampled tests overstate:** networks passing every test to 64 columns, one all 328,000 cases to 1,024, are provably wrong | P1 | E1: 2 counterexample networks | strong (the finding is Weiss's; the complete check is ours) |
| 2b | **More codes buy test-passing networks, not correct ones** | P1 | E3/E4, 20 seeds a cell: working rate rises (p 0.014, Holm-adjusted 0.042), certified rate doesn't (p 0.43) | registered |
| 2c | **The snap is what extrapolates** | P1 | E2: continuous 0/20 against snapped 8/20 at 1,024 (p 0.0033, Holm-adjusted 0.013); E2b: 0/20 against 20/20 (p 7.3e-12, exploratory); E2b', trained to the bound with no early stop: 0/20 against 20/20 (p 7.3e-12; its continuous arm is E2b's, run before E2b' was registered) | registered (E2, and E2b' as C2b, its snapped arm) |
| 2d | **Training short of the exclusion bound memorises:** runs fit their training lengths and learn larger, wrong machines; a classical bound as a design rule | P1 | modular sums: 37 of 40 runs exact to 3 columns, minimised to 6-22 states against 4 and 5 | strong |
| 3a | **Certification as a training control:** certify each curriculum step, stop at the first proof | P1, P2 | modular sums 1/20 and 0/20 to at least 3/6 and 6/6; division from 0 of 160 to certified networks | existence tests and screens; not separated on division |
| 3b | **Collapse past a solution:** further training destroys proved networks; traced on one network's 10 replays: each collapse starts as 1-3 transitions flipped by an ordinary update, mostly invisible to the loss, then Adam's amplification; **on replays, held by a certificate guard** (undo any update that makes a right machine wrong): 10 of 10 replays keep the proof, against 1 of 10 (registered) | P1 (P2's data at scale) | every division run that solved or nearly solved and trained on; P1's replays (9 of 10 lost the proof; the machine read off every batch); E2b' and the stable-replay probe show it is not universal (20/20 kept or regained at their cell) | onset described and, on one network's replays, repaired; in training the guard as built did harm (move-to-front-4 1 of 6 against 3 of 6 unguarded, a screen: indrajala-ml #857), and at 121 states it holds right machines by undoing 66-100% of updates (a probe: it freezes learning there) |
| 4 | **Product machines learned from answers alone:** certified 25-, 49- and 121-state division transducers (minimal Mealy machines), one to two orders of magnitude above previous extracted machines (at most a few states), no states or traces in training | P2 | 13/20 in the registered comparison at `p` 5; six networks at `p` 7 and four at `p` 11 (screens: 4 of 6), all long-tested (663,000 cases each at `p` 11) | 25, 49 and 121 done; rates above 25 states from screens; **169** (`p` 13) registered: W1, the window 32 wide, 5 of 6 against 0 of 6 at width 16 (indrajala-ml #867), long-tested (807,000 cases) |
| 5 | **Training on a cover of the target machine:** beside the target's output, the outputs of its homomorphic images, which together cover it; terms from automaton decomposition used as a training signal | P2 | registered twice: 13/20 against the quotient alone's 1/20 (p 6.9e-5); the approximation claim, 15/20 against 1/20 (Holm-adjusted p 1.5e-5) | registered; **what makes it work too (5b)** |
| 5b | **One approximation suffices; whether because it is one is open (the audit's F3):** the quotient with the sum alone (a homomorphic image, not a cover; its outputs don't determine the state) certifies where the quotient with the product (an extra output as informative, not an approximation) doesn't | P2 | registered (the approximation claim, A2, A3): sum 10/20 against the quotient alone's 1/20 (Holm-adjusted p 0.0017) and the product's 0/20 (4.4e-4) | registered, every network long-tested; one control, at `p` 5, which differs twice (not an approximation, and not learnable on its own): the learnable non-approximation control is the paper's T1 (indrajala-ml `docs/workplans/paper-workplan.md`) |
| 6 | **An enforced factorisation blocks learning:** one codebook per counter, blind to the other's state, cannot learn even one counter; the factors that learn are coupled, and their machine is not factored by residue | P2 | the D10 check; every certified network spreads the pair over both codebooks | screens |
| 7 | **Learned factors are the target's approximations, proved, and sometimes a cover:** each factor's code read exactly as the finest congruence quotient it fixes; nothing told the network about any decomposition | status note | move-to-front-4: pairwise recency orders (flip-flops, Krohn-Rhodes's kind), one certificate a cover, 13 earlier networks the same kind; word-problem-S3 seed 7 a cover (the places of items 1 and 2), seeds 0, 2, 6 a point's stabiliser on top; **no S3 network holds the sign**, against transformers' parity-first algorithm (Li et al. 2025) | read on 8 S3 and 15 move-to-front networks; not registered; whether the factor and code budget steers it is unread |
| 8 | **Formation and conversion are two problems, told apart by one measurement:** state separation (the target's state named from the cell outputs, the target read only to measure) beside the certificate; an abrupt snap destroys a formed state | status note (and P1) | S4: joint separation 0.98 to 0.25 at the snap; move-to-front's 1.00 at every length through the melt | strong as diagnosis; probing itself is not ours |
| 9 | **In a snapped recurrent state, on the two machines tried, formation depended on the algebra:** move-to-front-4 formed from the whole length distribution, S3 only from a seed (the mechanism offered, no synchronising word, explains conversion; the failure without a seed was formation) | status note | move-to-front-4 1.00 at lengths 4-128 with no curriculum; S3 at chance from length 16 without one; move-to-front-5 (reset) failed to form in 4 of 6 with a curriculum; since, the continuous crucible certifies both S3 and move-to-front-4, and S4 (a group) 1 of 6 | one machine of each kind, not a class line; may be the architecture's: Merrill et al. 2024 report single-layer RNNs learning group word problems at every length, while Allchin 2026 finds permutation automata mostly unlearned under RL; a plain-RNN control would settle it |
| 10 | **Conversion as a crystallisation:** a full melt, each factor's coupling handed over log-linearly in `T` between its own measured melting point and last transition, the clock held while the answers' screen dips (the quasi-static crucible); certificates with the commitment term never on | status note; continuous-crystallisation.tex | the quasi-static crucible: S3 8 of 8 on the six seeds the fixes were designed from (Wilson 0.68-1.00), against 2 of 8; the continuous crystallisation with the margin stop (D48-D60): fresh seeds read S3 7 of 16 at the first stop (its registered bar refuted, D55); the fresh-seed rate (D64), registered: S3 5 of 8, move-to-front-4 2 of 4 (7 of 12, between its bars; three runs cut by the wall clock, completed by D67), S4 and the random machines 0 of 10 | a combination of known parts (above: DOLCE's error-tied schedule is the closest); screens on two backdrops (about 3 in 5 fresh runs); none beyond them |

## Open, and what would settle it

- **The cover's novelty (5):** settled by the approximation claim (5b): with the full cover the
  outputs determine the state, close to Dan et al. 2022's state supervision, but the sum alone,
  whose outputs don't, beats the product, an equally informative non-approximation. Open: whether
  any approximation helps, and at larger `p`.
- **Breadth:** every target is an arithmetic transducer; a target with no arithmetic reading
  (a random or permutation machine) would test the framing's generality (a candidate for
  next-steps, not needed for these papers).
- **The state-formation strand (rows 7-10):** fresh seeds measure `p` (D64; the batch runner's
  first registered batch next). Still open from the 2026-10-21 reviews, the panel (4b) that would
  have carried them never run: the approximations question (which quotients appear, the sign among
  them), a plain-RNN control on S3 without a seed (row 9), a DOLCE-style error-tied schedule (row 10),
  an approximation's output beside S3 (D39 (i)), and S4, division and the 120-state tier under the
  method. The adaptive cool (D33) met its bar (4 of 8) and was set aside; the bounded handover's
  probe (D34) never ran.

## Where it is weakest

- The design is close to Zeng et al. 1993, and every other part has precedents ("Not ours";
  the literature review's "Extension (2026-10-19)"). Not found: their combination, in which the
  factored codes make the trained network a finite product machine, checked exactly. The novelty
  is the certificate, the protocol and the measurements, not the network; the window branches'
  is the diagnosis that motivates them (a transition proved exact, an output its features don't
  linearly separate), not their design.
- Arithmetic transducers only, and one architecture family.
- Rates beyond the registered comparisons come from screens of 4-8 seeds.
- A classical learner would find every machine here from far fewer examples; the papers say why
  that is not the comparison ("Why a network").
- The state-formation strand's evidence is two backdrops (6 and 24 states), one cell each, at an
  exact state bound: about 3 in 5 fresh runs certify there (D64), none of 10 on S4 and the random
  machines; its 8 of 8 and the margin stop's 11 of 16 reran the seeds their fixes were built from;
  its conversion method is compared only with our own earlier variants.

## Log

- 2026-10-17: written after the reframing (indrajala-research #13); P2's six `p` 7 networks
  long-tested (#12); the `p` 11 ladder's 4 networks recertified; the approximation claim's runs
  ending.
- 2026-10-17: the approximation claim read (A1-A3 hold): row 5 registered twice, row 5b new.
- 2026-10-19: the architecture's novelty pass (indrajala-ml #866's literature extension): five
  precedents added to "Not ours", the weakest-point bullet restated. Row 4: W1 certifies 169 states
  (registered, 5 of 6; long-tested, 807,000 cases). A candidate contrast, not registered: chunked
  recurrence with a continuous state loses swap-based S5 (RLT-2); whether the snap keeps it.
- 2026-10-21: the state-formation strand reviewed (`review-2026-10-21-state-formation.md`):
  rows 7-10 and nine precedents added (five fetched, indrajala-literature #7); the status note to
  cite Das & Mozer and Agustsson for the quasi-static cool, and to narrow row 9 to a snapped state.
- 2026-10-23: the programme audit (`review-2026-10-23-programme-findings.md`): row 1's 724 is the
  networks checked, not certified (F14); row 2c's continuous arm predates C2b's registration (F20);
  row 3b, the guard did harm in training (F2); row 9 narrowed to the two machines tried (F15); row 10,
  "Open" and "Where it is weakest" brought to the fresh-seed evidence (D55, D64; F13). Row 5b's
  "because it is one" is left for the owner (F3).
