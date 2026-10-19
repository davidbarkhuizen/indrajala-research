# The work's novel contribution (living document)

What the two papers contribute under their common framing, kept current as they are finalised.
Update a row when its evidence changes (a registered result read, a long test in, a critique
finding), and date the change in the log at the end. Novelty throughout is "not found in our
search", never "first". The dated reviews beside this file (`review-<date>-<topic>.md`) are
snapshots; this file is the current statement.

**The framing (agreed 2026-10-17):** can a network trained by gradient descent on input/output
examples alone, never on states or intermediate steps, come to compute a finite-state transducer
exactly at every length, and can we prove which machine it learned? P1
(`snapped-window-recurrence.tex`) is the method and the small machines (3-5 states); P2
(`certified-modular-division.tex`) is how it scales to product machines (25, 49 states).

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

## What is new

| # | contribution | paper | evidence | status |
| --- | --- | --- | --- | --- |
| 1 | **A complete, automatic equivalence check as the instrument of a study:** whether a trained network is the target transducer at every length, or a counterexample; every window from every reachable code (531,441 at `k` 4), outputs and states, near ties branched both ways, numerical margins; run on hundreds of networks | P1 | 724 distinct networks certified in P1's studies; every division network in P2 | strong; the strongest contribution |
| 2a | **Sampled tests overstate:** networks passing every test to 64 columns, one all 328,000 cases to 1,024, are provably wrong | P1 | E1: 2 counterexample networks | strong (the finding is Weiss's; the complete check is ours) |
| 2b | **More codes buy test-passing networks, not correct ones** | P1 | E3/E4, 20 seeds a cell: working rate rises (p 0.014, Holm-adjusted 0.042), certified rate doesn't (p 0.43) | registered |
| 2c | **The snap is what extrapolates** | P1 | E2: continuous 0/20 against snapped 8/20 at 1,024 (p 0.0033, Holm-adjusted 0.013); E2b: 0/20 against 20/20 (p 7.3e-12, exploratory); E2b', trained to the bound with no early stop: 0/20 against 20/20 (p 7.3e-12) | registered (E2, and E2b' as C2b) |
| 2d | **Training short of the exclusion bound memorises:** runs fit their training lengths and learn larger, wrong machines; a classical bound as a design rule | P1 | modular sums: 37 of 40 runs exact to 3 columns, minimised to 6-22 states against 4 and 5 | strong |
| 3a | **Certification as a training control:** certify each curriculum step, stop at the first proof | P1, P2 | modular sums 1/20 and 0/20 to at least 3/6 and 6/6; division from 0 of 160 to certified networks | existence tests and screens; not separated on division |
| 3b | **Collapse past a solution:** further training destroys proved networks; traced on one network's 10 replays: each collapse starts as 1-3 transitions flipped by an ordinary update, mostly invisible to the loss, then Adam's amplification; **repaired by a certificate guard** (undo any update that makes a right machine wrong): 10 of 10 replays keep the proof, against 1 of 10 (registered) | P1 (P2's data at scale) | every division run that solved or nearly solved and trained on; P1's replays (9 of 10 lost the proof; the machine read off every batch); E2b' and the stable-replay probe show it is not universal (20/20 kept or regained at their cell) | onset described and, on replays, repaired; the guard untested in training, and at 121 states it holds right machines by undoing 66-100% of updates (a probe: it freezes learning there) |
| 4 | **Product machines learned from answers alone:** certified 25-, 49- and 121-state division transducers (minimal Mealy machines), one to two orders of magnitude above previous extracted machines (at most a few states), no states or traces in training | P2 | 13/20 in the registered comparison at `p` 5; six networks at `p` 7 and four at `p` 11 (screens: 4 of 6), all long-tested (663,000 cases each at `p` 11) | 25, 49 and 121 done; rates above 25 states from screens; **169** (`p` 13) registered: W1, the window 32 wide, 5 of 6 against 0 of 6 at width 16 (indrajala-ml #867; long test pending) |
| 5 | **Training on a cover of the target machine:** beside the target's output, the outputs of its homomorphic images, which together cover it; terms from automaton decomposition used as a training signal | P2 | registered twice: 13/20 against the quotient alone's 1/20 (p 6.9e-5); the approximation claim, 15/20 against 1/20 (Holm-adjusted p 1.5e-5) | registered; **what makes it work too (5b)** |
| 5b | **One approximation suffices, because it is one:** the quotient with the sum alone (a homomorphic image, not a cover; its outputs don't determine the state) certifies where the quotient with the product (an extra output as informative, not an approximation) doesn't | P2 | registered (the approximation claim, A2, A3): sum 10/20 against the quotient alone's 1/20 (Holm-adjusted p 0.0017) and the product's 0/20 (4.4e-4) | registered, every network long-tested; one control, at `p` 5 |
| 6 | **An enforced factorisation blocks learning:** one codebook per counter, blind to the other's state, cannot learn even one counter; the factors that learn are coupled, and their machine is not factored by residue | P2 | the D10 check; every certified network spreads the pair over both codebooks | screens |

## Open, and what would settle it

- **The cover's novelty (5):** settled by the approximation claim (5b): with the full cover the
  outputs determine the state, close to Dan et al. 2022's state supervision, but the sum alone,
  whose outputs don't, beats the product, an equally informative non-approximation. Open: whether
  any approximation helps, and at larger `p`.
- **Breadth:** every target is an arithmetic transducer; a target with no arithmetic reading
  (a random or permutation machine) would test the framing's generality (a candidate for
  next-steps, not needed for these papers).

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

## Log

- 2026-10-17: written after the reframing (indrajala-papers #13); P2's six `p` 7 networks
  long-tested (#12); the `p` 11 ladder's 4 networks recertified; the approximation claim's runs
  ending.
- 2026-10-17: the approximation claim read (A1-A3 hold): row 5 registered twice, row 5b new.
- 2026-10-19: the architecture's novelty pass (indrajala-ml #866's literature extension): five
  precedents added to "Not ours", the weakest-point bullet restated. Row 4: W1 certifies 169 states
  (registered, 5 of 6; its long test pending). A candidate contrast, not registered: chunked
  recurrence with a continuous state loses swap-based S5 (RLT-2); whether the snap keeps it.
