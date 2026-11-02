# Workplan: the numeral reader (aligning written operands by place value)

**Status: drafted 2026-11-02 at the owner's direction; no code yet.** The owner, on writing up
addition at any length under the literature's conditions (base 10, operands as an `a + b =` string):
"to my mind, there are 2 separate problems - 1. the generic problem of digit alignment in a binary
operator targeting multi-digit tokens/variables - i.e the concept of string direction = left or right
first, combined with incremental-position-significance (i.e. the actual concept of a base) 2. the
effect of the particular binary operator, in our case addition"; then "focus on researching 1 in
depth and developing a detailed workplan for exploring it. once we have 1 in place, we can then
return to 2 in time". The framing is in
[numerals-and-operators.md](../research-notes/numerals-and-operators.md). The owner delegates the
decisions (each below with its options' pros and cons) except those marked **for the owner**.

This plan takes over the alignment questions that
[arbitrary-length-addition-workplan.md](arbitrary-length-addition-workplan.md) left in P3 (positions
as data: position coupling, Abacus indices) and P8 (the string format), and its parked "composing
outside the network". That plan's milestone A (the window-recurrent adder over aligned columns) is
the operator side, problem 2, and is untouched.

## The IDs, in time order

| ID | When | Short label | What it is |
|---|---|---|---|
| D1 | 2026-11-02 | the reader's contract | input `a op b =` most significant digit first; output the column stream, digits paired by place value, zero-padded, least significant first, then an end mark |
| D2 | 2026-11-02 | heads, not attention | the main line is a finite snapped controller driving discrete read heads over the string; a transformer reader is not built here |
| D3 | 2026-11-02 | the programmed reader | a programmed reader with the same contract, as the control and the harness's reference |
| D4 | 2026-11-02 | soft heads, snapped | heads trained as position distributions moved by the controller, snapped to exact positions as the state is to codes; reinforcement learning only as the fallback |
| D5 | 2026-11-02 | copy, not emit | the controller outputs which head to copy (or a pad), not the digit itself, so the learned machine has no base in it |
| D6 | 2026-11-02 | the reader as its own task first | first trained on the reader's own answers (the column stream), then end to end on operators' answers only |
| D7 | 2026-11-02 | the certificate on the controller | the controller certified as a Mealy machine against the target controller over every head-symbol pair (sound, possibly incomplete); the heads' semantics is exact by construction |
| D8 | 2026-11-02 | base 3, then 10 | the existence ladder at base 3 (the programme's known ground), base 10 once it works |
| D9 | 2026-11-02 | studies first | the tape, heads and soft-head training prototyped in indrajala-studies; moved to indrajala-ml once stable |

## The problem

**Input.** A tape `⊢ a + b = ⊣` over the digits `0..β-1`, the operator symbol, `=` and the two end
marks; each operand written most significant digit first (as people write them), lengths `n` and `m`
from 1 up, no leading zeros beyond a lone `0`.

**Output (D1).** The column stream `(a_0, b_0), (a_1, b_1), ..., (a_{L-1}, b_{L-1}), ⊣` with
`L = max(n, m)`, the shorter operand padded with 0, least significant column first. This is exactly the
input the window-recurrent adder certifies over, so a reader meeting the contract composes with any
operator machine over columns. The operator machine handles the final carry at `⊣`.

**Parameters, not tasks.** The base `β` (D5 keeps it out of the learned machine) and the direction:
an operator that needs most significant first (none planned) gets the same reader with its heads
started at the other ends. The operator symbol is read but does not change the reader. Writing the
answer back most significant first is a reversal, the same kind of problem; it is stage R8.

**Why it is not finite-state.** A one-way finite reader would have to hold all of `a` before `b`
arrives. Pairing `a_i` with `b_i` matches positions by their distance from `+` and `=`, which no MSO
formula can express on strings (it would define `{x^k + y^k}`). So, to be checked in R0: the reader is
not a regular function (Engelfriet & Hoogeboom: regular = two-way deterministic transducers = MSO
transductions), and not polyregular either (Bojańczyk 2018: polyregular = MSO interpretations, pebble
transducers). Our certificate proves finite machines, so it cannot prove a reader whole.

**What computes it.** A finite controller with two two-way read heads: head 1 runs right to `+`, head
2 right to `=`, both step left once, then both step left together, copying the digits they read (0
once a head reaches its operand's left end), until both are at their ends. The controller has about
four states; the unbounded part is the heads' positions, which are not learned. Attention can do the
same by matching positions (what position coupling makes easy). The reader is thus a
deterministic two-head two-way transducer (multi-head automata: Holzer, Kutrib & Malcher's survey).

**The idea this plan tests (D2, D7).** Learn only the finite controller, with the network the
programme already has, and give it heads whose semantics is exact. Then the learned part is a Mealy
machine, the certificate applies to it, and equality with the target controller gives the whole reader
at every length: one hand-proved lemma (same controller, same head semantics, same function) plus the
target reader's correctness (proved by hand once, in the note). The general architecture is extended,
not replaced: the window-recurrent network becomes the controller, its window the symbols under the
heads.

## What the literature has (searched 2026-11-02; R0 reads it properly)

**Alignment supplied, not learned** (the strongest length-generalisation results):

- position coupling: digits of equal significance share a position ID; trained to 30 digits, over 95%
  exact at 200 (Cho et al. 2024, arXiv 2405.20671); with scratchpads, multi-operand (Cho et al. 2024,
  2410.15787);
- Abacus embeddings, a digit's index within its number (McLeish et al. 2024);
- index hints with FIRE positions, "not robustly" (Zhou et al. 2024);
- formats rewritten so that a short RASP-L program exists (Zhou et al. 2023, "What Algorithms can
  Transformers Learn?", 2310.16028);
- explicit structural symmetry encodings, trained to 5 digits, tested to 50 (arXiv 2406.01895);
- Zaremba et al. 2016 ("Learning Simple Algorithms from Examples", 1511.07275): a controller with
  read heads trained by Q-learning, the closest design to D2. But addition there reads a 2-D grid with
  the operands stacked, so the alignment is given; only copy and reverse use a tape. Their controllers
  could settle on automata tied to the training length.

**Alignment left to the network:** learned absolute positions don't extrapolate; relative or no
positions extend somewhat (Jelassi et al. 2023; Kazemnejad et al. 2023; Ruoss et al. 2023; a 2025
Hamburg thesis finds no positional encoding best for full integer addition); none is exact at every
length.

**Memory-augmented networks:** neural Turing machines (Graves et al. 2014), RL-NTMs (Zaremba &
Sutskever 2015), neural GPUs (Kaiser & Sutskever 2016; Price et al. 2016), neural RAMs (Kurach et al.
2016), stack and tape RNNs on copy, reverse and duplicate (Delétang et al. 2023), stack RNNs (Joulin &
Mikolov 2015; Grefenstette et al. 2015), pointer networks (Vinyals et al. 2015). Neural programmer-
interpreters (Reed & de Freitas 2016) train on traces, which this programme does not.

**Theory:** Chen, Ma & Li 2025 ("Non-Asymptotic Length Generalization", 2506.03085): an `n`-state
DFA is learned at every length from inputs of length at most `2n - 2` by a minimum-complexity
interpolator, and a class admits such a bound exactly when its equivalence problem is decidable.
Equivalence of multi-head automata is undecidable in general, so no bound covers every reader; the
certificate's route (equality with a given target controller) is a sufficient check, not a decision
procedure.

**The gap, as far as found:** no work learns operand alignment from answers alone, none proves a
learned reader at every length, and none shares one reader across operators.

## Decisions

- **D1. The reader's contract. Settled: (a).**
  - (a) *Chosen.* Columns least significant first, zero-padded, an end mark. Pros: exactly the
    certified adder's input, so R6 composes with no change; the operator machine owns the carry.
    Cons: fixes the direction addition needs; another operator may need the other (a parameter).
  - (b) Emit the operands reversed, one after the other. Cons: the alignment is still undone, and
    pairing them is the hard part.
- **D2. The reader's mechanism. Settled: (a).**
  - (a) *Chosen.* A finite snapped controller driving two read heads. Pros: the learned part is
    finite, so the certificate applies and the claim can be "proved at every length"; it reuses the
    window-recurrent network as the controller (the general architecture); the unbounded part is
    exact by construction. Cons: new machinery (a tape and heads), and moving heads is a discrete
    choice that gradients don't see directly (D4).
  - (b) A transformer reader, attention over the whole string. Pros: the literature's route, the
    framework has attention. Cons: unbounded-length attention is beyond the certificate, and the
    literature shows its extrapolation is not robust; it would reproduce others' results.
  - (c) Only the programmed reader (D3). Pros: immediate. Cons: answers nothing about learning.
- **D3. The programmed reader. Settled: build it first.** Pros: it is the contract's reference, the
  tests' oracle, the target controller written as code, and the control the learned reader is
  compared with. It also lets the operator side (problem 2) resume later without waiting. Cons: none
  beyond a small cost.
- **D4. Training the heads. Settled: (a), with (b) as the fallback.**
  - (a) *Chosen.* Soft heads: each head a distribution over tape positions, moved by the controller's
    shift distribution (left, stay, right) as in neural Turing machines; reads are the expected symbol
    embedding. Annealed and snapped to exact positions (one-hot) as the state is snapped to codes;
    the snapped network is what is certified. Pros: end-to-end gradients; the programme's
    crystallisation and snap carry over. Cons: a soft head blurs over long tapes; the anneal may need
    tuning.
  - (b) Discrete heads trained by reinforcement learning (Zaremba et al. 2016). Pros: exact heads
    throughout. Cons: they report that standard Q-learning failed on most tasks; sparse rewards.
  - (c) Supervised head moves. Rejected: a trace of the target's method (learn the method, not
    imitate).
- **D5. Copy, not emit. Settled: (a).**
  - (a) *Chosen.* The controller sees each head's symbol and outputs, per column, a copy of head 1's
    digit or a pad, and likewise for head 2. Pros: the learned machine has no base in it, so a reader
    trained at base 3 can be tested at base 10 unchanged (a sharp test of genericity); the controller's
    output alphabet is small. Cons: a pointer output, new beside the network's softmax outputs.
  - (b) The controller emits the digit pair itself. Pros: plain softmax outputs. Cons: `β²` outputs,
    and a different machine per base.
  - Whether the controller sees digit values at all, or only the class (digit, operator, `=`, end),
    is left to R4: classes alone would be known structure given, values make it learn to ignore them.
- **D6. Training signal. Settled: (a), then (b).**
  - (a) *Chosen first.* The reader as its own task, trained on its answers, the column stream. Pros:
    the owner's framing makes it a task of its own, with inputs and answers; the shortest path to
    one working reader (existence first). Cons: the columns are the composite's intermediate, so this
    alone doesn't show the reader can be learned through an operator.
  - (b) *Then.* End to end, on operators' answers only, the column stream never shown. Pros: the
    real question (learn the method from inputs and answers), and with several operators sharing
    one reader, the test of genericity. Cons: the credit assignment runs through two machines.
- **D7. The proof. Settled: (a).**
  - (a) *Chosen.* Certify the snapped controller as a Mealy machine against the target controller,
    over every pair of symbols under the heads, not only pairs a valid tape can show. Pros: sound,
    and the existing certificate's form. Cons: incomplete: a correct controller that differs from the
    target only on impossible pairs fails it. R5 measures how often; the refinement restricts to the
    configurations valid tapes reach (head 1 never past `+`, and so on).
  - (b) A target-free proof (as paper 1's appendix F does for finite machines). Cons: equivalence of
    two-head transducers is undecidable in general, so only special cases; an R0 question.
- **D8. Bases. Settled: base 3, then 10.** Pros: base 3 is where every working cell so far ran; D5
  makes base 10 a test, not a retraining. Cons: none.
- **D9. Where the code lives. Settled: indrajala-studies first.** Pros: research code, fast to change;
  the library moves only what is stable. Cons: a later move into indrajala-ml's three implementations
  and the crate.
- **For the owner, later:** whether this becomes a note or paper of its own (after R5 or R6), and
  whether the operator side (the base-10 addition note) waits for R6.

## Stages

Each stage ends in a PR; probes are short and persisted as tools; every cell passes the feasibility
check first.

- **R0. Literature.** Read the papers above, fetch and persist each (bib in indrajala-literature;
  PDFs public only if openly licensed). Settle: the formal class of the reader (not regular, not
  polyregular: check against Bojańczyk 2018 and Nguyễn, Noûs & Pradic 2021's comparison-free pebble
  transducers); decidability of equivalence for one-way and two-way two-head transducers (Holzer,
  Kutrib & Malcher); what Zaremba et al. 2016 and Delétang et al. 2023 found about heads and tapes
  at length; anything from 2025-2026 on learned alignment. Output: a section in
  [window-recurrent-literature.md](../research-notes/window-recurrent-literature.md), and D2, D4, D7
  revisited.
- **R1. The contract and the target.** The reader's specification (D1) with its edge cases (unequal
  lengths both ways, single digits, a lone 0); the programmed reader (D3) with its tests; the target
  controller as a machine (states, transitions over head-symbol classes, moves and copy outputs); the
  hand proof that the target reader meets the contract at every length; the lemma that an equal
  controller gives an equal reader.
- **R2. Tape and heads.** In indrajala-studies (D9): a tape, `k` heads with exact and soft semantics
  (D4), the window-recurrent network as the controller (its window the symbols under the heads), copy
  outputs (D5), a loss on the column stream; length-free by construction. Tests: exact heads driven
  by the target controller reproduce the programmed reader bitwise; soft heads at temperature zero
  equal exact heads.
- **R3. Feasibility.** An entry in `docs/protocols/information-flow.md`'s register for the reader
  cell: enough codes for the target controller's states, training lengths that exercise every
  controller transition (both orders of unequal length, both heads at their ends, single digits; Chen
  et al.'s `2n - 2` as a reference), the soft heads' reach at the longest training tape, and each
  run's memory (measured, runners only).
- **R4. Existence (the reader as its own task, D6a).** Base 3, a short budget, a few seeds, the
  configuration varied on the fly: does one reader learn the contract and snap to a controller? Then
  base 10 with the same network, untrained (D5's test), and trained if needed.
- **R5. The certificate on the controller (D7).** Read the snapped controller's table, certify it
  against the target controller, measure D7's incompleteness on the runs, long-test the reader to
  1,024 digits and past. A certified reader is the first "proved at every length" for alignment.
- **R6. End to end (D6b).** The reader composed with the certified base-3 adder: trained on sums
  only. Then one reader shared by two or three operators (addition, subtraction, comparison), each
  operator machine its own, with a held-out operator as the test of a generic reader.
- **R7. Write-up.** Findings into this plan and an internal research note; whether to publish is
  the owner's (above).
- **R8. The writer.** The answer emitted least significant first, written back most significant
  first: one head over the operator's output, the same machinery reversed.

## Order and dependencies

R0 and R1 are offline and can start once the certificate note's release (its stage 7) frees the
attention it needs; the owner's order (2026-11-02) is the certificate note, then the architecture
note, with this plan's research beside them as compute allows. R2 needs R1; R3 needs R2; R4-R6 need
the runners (jebel, klip, stone), never pyramidon. R8 after R6.

## Not in this plan

- The operator side: a base-10 addition note, other operators' machines beyond R6's few (problem 2,
  later, as the owner said).
- A transformer reader (D2b), unless R0 finds a reason to need it as a baseline.
- More than two operands: `k` heads generalise it; a later question.
