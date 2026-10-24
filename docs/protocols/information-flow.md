# Information flow and its constraints (a feasibility checklist)

**Written 2026-10-19 at the owner's request: "we should be starting to think in terms of the
constraints that our architecture imposes on the flow-through of information - we should always be
sure that, if things work as we want, that the solution is at least always feasible".** A diagram of
one window step, with these constraints marked where they act, is in the owner's artifacts ("Window
Information Flow"). This file is the register; [experiment-design.md](experiment-design.md),
section 1, requires every study to check its cells against it before they run.

## One window step

The window's tokens (one column, `k` 1, and the query tokens) and the snapped state `c` enter one
residual stream of width `D`: Embedding and Position, with a StateInput adding `P c` before every
block. Three transformer blocks (`H` heads, FFN `2D`) work on it, and its output tokens feed two
consumers:

- **the transition (`delta`)**: each factor `g`'s pooling (one learned query), its cell (state
  `s_g` wide) and its snap to one of `m_g` codes give the next state `c`, the only memory carried
  to the next window;
- **the output (`lambda`)**: the linear output layer gives the answers, the target's and each
  approximation's.

Everything both consumers need passes through the stream, so its width is a capacity bound like
the codes'.

## The register

| # | Where it acts | Requirement | Why, and the evidence | Status |
| --- | --- | --- | --- | --- |
| 1 | the snap | joint codes `m = prod m_g` at least the target's minimal states `q`; a surplus of 3-5x | fewer can't represent it (E7: 32 codes for 49 states, 20 runs that couldn't work) | imposed rule |
| 2 | the training data | longest length `L >= m + q - 1` (the exclusion bound) | below it a wrong machine fits every case (E8: 37 of 40 memorised); with an unknown target a state bound stands in for `q`; a property of the config: a run certified before reaching it reports its trained length (D42) | imposed rule |
| 3 | the residual stream | width `D` enough for every consumer at once | division 13: 0 of 6 at 16, 3 of 6 at 22, 5 of 6 at 32; at 16 five of L3's six failures had ambiguous codes (20-135 pairs per code) and one an exact state whose answers its features couldn't separate; the base is now 32 | measured (2026-10-19) |
| 4 | attention, per consumer | splitting the stream adds no capacity; each consumer keeps enough heads and width | a single-head branch per consumer at 16: B1 1 of 6 (W2, width alone at its size, 3 of 6); harm on S4 (B3, 0 of 6 against 4 of 6, p 0.030); not adopted | measured (2026-10-19) |
| 5 | the output layer | the answers linearly separable on the stream's features | the layer is linear; no linear readout of L3's 16 features fixed its last 1% (the separability check) | measured |
| 6 | the poolings | each reads the window's output, not the tokens before the state | before the state a cell must compute the whole transition (the D10 check: 0 of 2 against 2 of 2) | imposed rule |
| 7 | the codes | one code, one state (pairs per code 1.0) | every certified network has it; extra codes are its failure; the branches don't fix it (at 16 or 32 on S5); R3 and R4's probe certified one S5 seed of two | required, open |
| 8 | the commitment | a state can form before the commitment pulls outputs to their codes | off early, 3 of 6 failure-A runs formed a state; the thermostat's code-use signal returns it too soon (its probe so far); option 1 (the state formation workplan) runs with the commitment never on, so the row holds trivially there, and the harm cells test what that costs (D37) | required, open |
| 9 | the cell | each factor's state `s_g` enough for its transition | 32 in use; 16 to 32 (L3) didn't cure division 13 | design choice |
| 10 | the window | `k` 1: the state handed on every symbol | keeps the step one symbol and the certificate fast; a chunked step is another capacity question | design choice |
| 11 | the data | every example ends in a final zero window, whose answer needs the state | without it a one-column step passes on the column alone | imposed rule |
| 12 | the state input | the state reaches every block (`P c` before each) | W11's window | design choice |
| 13 | training control | stop once the snapped machine answers right within the state bound and no near tie splits it, at most 200 steps past the first such pass, on the best pass (the margin stop, D59 under D60, since 2026-10-22; D35's first pass before it; before 2026-10-21, the first certified step) | training past a proof destroys it (E8b); the answers-only stop kept every certificate when the bound is tight, and fails fast when it isn't (the state-formation workplan's re-reading); the split ties separate the strict-only stops (D59) | imposed rule |
| 14 | the proof | every state reachable and every pair told apart within the check; near ties branched | sampled tests overstate (networks passing 328,000 cases provably wrong) | imposed rule |
| 15 | the crucible (option 1, D26) | its lengths (to the warm-up's cap, 8) reach every state and tell every pair apart: the deepest state's depth plus Chow's `k` at most the cap | on every machine backdrop at most 7 (move-to-front-5: 4 + 3); division unread (state-formation-workplan.md, the review's re-reading) | imposed rule (2026-10-21) |
| 16 | the coupling (option 1, D25, then D50) | the codes take the state over from the continuous path gradually: the next state `(1 - l) h + l q`, `l` read from the codes' sharpness | an abrupt snap lost a formed state (S4: joint separation 0.98 to 0.25); with `l` held at 0 S3 certified 4 of 8, its bar refuted, the failures never answering right on their snapped machine (D38) | required (2026-10-21; added 2026-10-23, the programme audit's F24) |
| 17 | the target's structure | the target's congruences stated beside every backdrop (`modular_family_probe.py congruences TASK`: the nontrivial principal congruences and their blocks); a primitive target (none: Rystsov and Szykuła 2023's term) has no approximation to be given or to find | descriptive, not a gate. Primitive: every random machine in our runs (random-3-0, random-4-0, random-q12-0, random-q16-0) and 52 of 53 more drawn (random-q16 seeds 0-39 among them; random-3-1 has one, of 2 blocks); not: division (its p + 1 lines), S3 4, S4 16, move-to-front-4 264. A congruence isn't necessary at 12 states (random-q12-0 certified: 2 of 3 in the consolidation, 1 of 4 in D58); whether it is at scale, apart from `order` (the answers' predictability against random machines, which agrees with it on all five backdrops read), is the paper's T10 | descriptive (2026-10-24) |

## Before a study

1. Codes and lengths (rows 1, 2): computed and written beside each cell.
2. The stream (row 3): at least the width that worked on a comparable cell.
3. Any split or new path (row 4): does it take capacity from a consumer that already needed it?
4. The readout (row 5): can a linear layer separate the answers at this width?
5. The proof (row 14): can the check see every state?
6. The target (row 17): its congruences stated; a primitive target said so, with its `order`.

**What would break it next:** more consumers (each added approximation's answers share the stream:
rows 3, 5); more states (more codes, longer training, more of the stream for the state: rows 1-3);
chunked windows (rows 3, 10); discovery (an unknown target makes a state bound mandatory: rows 1,
2; [machine-discovery.md](../research-notes/machine-discovery.md)).
