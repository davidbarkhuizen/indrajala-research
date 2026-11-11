# A fresh review of the research programme (2026-11-10)

**Status: a dated review, at the owner's request:** "review the work that has been done and the
results that have been obtained ... identify 1. any findings/observations evident to you but not
yet recorded/stated 2. any logical gaps, oversights and/or errors in the work, findings or
methodology that would materially bias or obscure results ... identify the most promising avenues
for further research, and then detail the direction you think the research should take to obtain
the most useful novel results".

**Who wrote it.** Claude (Fable 5.2, a model made by Anthropic), working through Claude Code. The
work under review was done with another model (Opus 5.5). This reviewer took no part in it and
began from the repositories alone, without the earlier sessions' context. That is not independence
in the sense a paper's referee has it: both are Anthropic's models, and the review reads the
programme's own record.

**The short of it.** No error was found in the certificate, in Chow's test set as built, or in
paper 1's statistics. The main finding is about what the results mean. Across every test in paper
1, one variable orders the outcomes: how much of the target's state the training targets at a
column determine. Whether an extra output is an approximation (a congruence's quotient) has no
evidence of its own anywhere in the data, and the one result offered for a coarse approximation
(the planted machines) is an arm whose targets tell about 11 of 16 states. The control that would
separate the two readings has not been run, and it is cheap.

## Method and limits

- **Read in full:** paper 1 (`papers/learning-transducers-with-proof.tex`); `contribution.md`;
  `docs/research-notes/` (machine-discovery, failure-kinds, adder-findings, state-formation-note,
  primitive-machines-note, factorisation-note, numerals-and-operators, window-recurrent-report);
  both protocols; the post-paper retests workplan; the 2026-10-23 audit's findings and its
  re-assessment of the earlier reviews; the 2026-10-28 review of paper 1; indrajala-ml's handover.
- **Read in part:** the SMB world-model workplan (status, the synthesis, where discovery fits, the
  stages, feasibility); the SMB machine-policy workplan (status, the stages' results); the
  certificate note (abstract); indrajala-ml's `next-steps.md` (the research items).
- **Code read (indrajala-studies):** `window_recurrent_certificate.py`, `chow.py`, `window_tasks.py`
  (the target machines), and `modular_family.py` for how a run is seeded.
- **Data read:** the seven batch ledgers behind paper 1 (T1, T2 and T5, T3, T10, T10r, T11, T12:
  590 runs) and their run logs, under indrajala-studies' `data/window-recurrent/paper/`.
- **Not read:** the state-formation workplan in full; the two superseded drafts; the LaTeX research
  notes; the NES plans; the library and the crate; `inference.py` (its results were recomputed
  instead); the SMB code and results.
- **Not done:** no network was trained or re-certified. No literature search was made: novelty is
  judged from the programme's own reading.
- **Every analysis here is post hoc and exploratory.** None was registered. Where a statistic was
  chosen after seeing the data, that is said.

**Severity** (the 2026-10-23 audit's scale): **S1** a paper's or note's statement is wrong or
unsupported; **S2** a stated rule is broken, or a claim is weaker than stated; **S3** documents
disagree, or a statement is stale.

**The tests' labels, as paper 1 numbers them:** the extra-output controls (T1); division at scale
(T2); the snap and transformer controls (T3); the algebras on their answers alone (T5); the proof
without a target (T6); the planted machines (T10) and their replication (T10r); the algebras given
approximations (T11); the cover against the state (T12).

## Summary

| # | Sev | Finding |
| --- | --- | --- |
| O1 | | One variable orders every result: the share of the state the targets at a column determine |
| O2 | | The planted machines given their blocks are told 11.2 of 16 states on average, not 4 |
| O3 | | The certified step doesn't grow with the machine's size; epochs grow with `p`, the square root of the states |
| O4 | | Division's failures fall on the same seeds across machine sizes |
| O5 | | A run certifies early or not at all; failed runs took 87% of the epochs trained |
| O6 | | S3's low rate is not a high cost per certificate |
| G1 | S1 | Paper 1's definition of "told" is vacuous as written |
| G2 | S2 | The claim that a coarse approximation helps rests on an arm that tells most of the state |
| G3 | S2 | No control separates being a congruence from telling the state |
| G4 | S2 | T10r replicated the confounded contrast and dropped the clean arm |
| G5 | S2 | "20 fresh seeds an arm": arms and backdrops share seeds 300-319 and their data stream |
| G6 | S2 | The outcome is a rate at a fixed budget, though the paper reads a rate as a cost |
| G7 | S2 | The exclusion bound can't be reached within the epoch budget at 121 and 169 states, and does no work |
| G8 | S3 | The discovery note still reads the product and the suffix as evidence about wrong suggestions |
| G9 | S2 | No classical learner has been run, and the data regime hides the question discovery asks |
| G10 | S2 | The SMB plan reaches a real system before the controlled stages |

## 1. Observations in the data, not recorded

### O1. One variable orders every result

**What.** For each arm of paper 1, count the classes of the target's states that the training
targets at a column tell apart (the answer's label together with each extra output's). Every
target here labels the state reached (`window_tasks.py`: `output = labels[transition]`), so the
count is exact. Recomputed from the machines:

| Target | Arm | Classes told / states | Certified |
| --- | --- | --- | --- |
| Division, `p` 5 | answers alone | 6 / 25 | 1 of 20 |
| | + the product | 10 / 25 | 0 of 20 |
| | + the sum | 22 / 25 | 10 of 20; 6 of 20 (T1) |
| | + the cover | 25 / 25 | 15, 13 and 11 of 20 |
| | + the state | 25 / 25 | 17 of 20 |
| Division, `p` 11 | answers alone | 12 / 121 | 0 of 20 |
| | + the cover | 121 / 121 | 16 of 20 |
| S4, move-to-front-4 | answers alone | 4 / 24 | 4 and 4 of 20 |
| | + a pair of approximations | 24 / 24 | 16 and 18 of 20 |
| S3 | answers alone | 3 / 6 | 1 of 20 |
| | + a pair of approximations | 6 / 6 | 5 of 20 |
| Random, 16 states | primitive, answers alone | 4 / 16 | 0 of 20, 2 of 30 and 2 of 50 runs |
| | planted, not given | 4 / 16 | 3 of 30 runs |
| | planted, blocks given | 11.2 / 16 (mean) | 9 of 30 and 13 of 50 runs |

**The claim.** Within each target, the rate rises with the classes told, and nothing else in the
table is needed to order it. An extra output that is no approximation and tells little (the
product) doesn't help; one that is the finest approximation and tells everything (the state) helps
most. Paper 1 says its runs "do not separate" the approximations' help from "what they tell about
the state". The table says more than that: there is no result anywhere in the paper in which being
a congruence does work that the classes told don't already account for.

**Limits.** Post hoc. S3 is low even when told everything (O6 gives a reading). The count is of
one column's targets; what a history of targets tells is larger and wasn't counted.

### O2. The planted machines given their blocks are told most of their state

**What.** Paper 1's "What the outputs tell" says a planted machine given its blocks "is told 4
classes of its 16 states, the answers' 4 labels besides", and its abstract and third limit call
this "a coarse approximation, one that leaves the state undetermined". The blocks and the answers
together were not counted.

**Evidence.** Rebuilt from `random_planted_machine(16, 4, seed)` for the 40 machines of T10's and
T10r's given arm: the block and the answer together tell a mean of 11.2 of 16 states (range 8-15).
The primitive machines' and the not-given arm's targets tell 4 (means 3.98 and 4.0).

**The claim.** The given arm is told about 70% of its state's classes, against 25%. "Undetermined"
is true and understates it. Within the given arm the certified runs rise weakly with the classes
told (one-sided permutation p 0.13 over 40 machines: not detected; the count varies little).

### O3. The certified step doesn't grow with the machine; epochs grow with `p`

**What.** Division at scale (T2), the certified runs:

| `p` | States | Median certified step | Median epochs | Epochs / `p` | Seconds / epoch | Cap (the exclusion bound) |
| --- | --- | --- | --- | --- | --- | --- |
| 7 | 49 | 11 | 195 | 27.9 | 11.5 | 489 |
| 11 | 121 | 9.5 | 261 | 23.7 | 10.6 | 1,144 |
| 13 | 169 | 11 | 313 | 24.1 | 12.8 | 1,612 |

At `p` 5 in the other cell (T12's cover arm) the medians are step 7 and 122 epochs, 24.4 a unit of
`p`; the cell differs, so it is shown apart.

**The claim.**
- The curriculum step at which a run certifies, the longest length it has trained on, is about 10
  from 49 to 169 states. Across paper 1 it is 4-7 on S3, 6-17 on S4 and 7-16 on move-to-front-4
  given their pairs (but for one run at step 28), and 6-22 on the random machines. It tracks the
  machine's depth plus its distinguishing length (3 to 5 on division and the algebras), not its
  size, and at 121 and 169 states sits two orders of magnitude under the exclusion bound (G7).
- What grows is the epochs a step takes. Total epochs to a certificate are about 25 times `p`:
  linear in the size of a coordinate, the square root of the states. Seconds an epoch are flat on
  the hosts used.
- So, given its cover, a direct product's cost follows its factors' sizes, not their product. That
  is three points and one family; it predicts medians near 425 epochs at `p` 17 and 575 at `p` 23.

### O4. Division's failures fall on the same seeds across machine sizes

**What.** T2's three division backdrops ran on the same seeds, 300-319. Their failures:
`p` 7: 306, 307, 310; `p` 11: 303, 314, 315, 316; `p` 13: 303, 306, 310, 314, 315.

**Evidence.** Five seeds (303, 306, 310, 314, 315) fail at two sizes each and carry 10 of the 12
failures. Shuffling each backdrop's failures among its seeds gives five or more such seeds with
probability 0.003 (200,000 shuffles; the statistic was chosen after seeing the data). The variance
of the seeds' success counts gives 0.057. Every one of `p` 13's five failures is a seed that also
fails at 7 or 11.

**Why it can happen.** A seed fixes the initial weights (`randomized(..., seed=seed)`) and the
training words: the generator is keyed by seed, step and epoch only (`modular_family.py`,
`run_epoch`: `random.Random(f"family-train-{seed}-{step}-{epoch}")`), so a seed draws the same
base-3 words at every `p`.

**The claim.** Part of what fails a run is the seed's, shared across targets, not the machine's.
The owner's rule (the state-formation note): "a failure that correlates with something observable
early is a design flaw lowering `p`, to fix". Which of the two it is, the weights or the words, is
one small experiment (section 4, step 3).

### O5. A run certifies early or not at all

**Evidence** (the 550 coded runs of paper 1's tests):
- 176 certified; 157 of them by curriculum step 14, 103 by step 10; the latest at step 32.
- The 374 failures ended at a median step of 34.
- Failed runs took about 87% of the 242,600 epochs trained.
- Stopping every run before step 15 would have cut the epochs by 45% and kept 157 of the 176:
  epochs a certificate, pooled, from 1,379 to 849.

**The claim.** The owner's remark ("when this architecture works, it tends to be clear-cut and
early") holds as a number. The batch runner's cutoffs and `restart-cost` exist and were used on
the crystallisation strand; paper 1's batches ran with no cutoff, and its tables report the rate at
a full budget.

### O6. S3's low rate is not a high cost

**What.** Given its approximations (T11), S3 certified 5 of 20 against 16 and 18 for S4 and
move-to-front-4; paper 1 reads it as "short of significance" and "undecided".

**Evidence.** S3's five successes all came by step 7, within 63 epochs; its 15 failures ran the
full 600. As run, it cost 1,841 epochs a certificate. With a cutoff of 38 epochs it would have cost
187, against 160 and 164 for S4 and move-to-front-4 at their own best cutoffs. The cutoffs were
chosen on the same runs, so these are optimistic; the order of magnitude is the point.

**The claim.** An S3 attempt is decided within about 40 epochs and succeeds about one time in four
or five. Its cost per proved machine is about that of the 24-state algebras. Its low rate is a
property of reading a rate at 600 epochs (G6).

## 2. Gaps, oversights and errors

### G1 (S1). Paper 1's definition of "told" is vacuous as written

**Where.** Paper 1, Method: "A target's state is *told* when what the network is given up to a
column, its inputs and its training targets, determines the state at that column".

**The fault.** A target is a deterministic machine with a fixed start, so its inputs up to a column
always determine its state. As written, every target is told and none hidden. The definition
carries the paper's size record ("hidden and proved: ... 24 here") and its sorting of the
literature.

**Recommendation.** State what is meant: the state is told when the training targets at a column
(or fed-back past outputs) determine it by a map that doesn't depend on the machine's transitions;
otherwise hidden. Better, replace the two classes by the count O1 uses, the classes told of the
states, which the paper already computes for most arms.

### G2 (S2). The claim that a coarse approximation helps rests on an arm that tells most of the state

**Where.** Paper 1's abstract, contribution 2, A4 and the third limit: "The registered evidence
that a coarse approximation helps, one that leaves the state undetermined, is a planted
approximation of 4 blocks on random machines (T10r)".

**Evidence.** O2: that arm's targets tell 11.2 of 16 states on average. The sum at `p` 5 tells 22
of 25, which the paper states. So neither arm offered as coarse is coarse in what it tells.

**Recommendation.** Add the planted arm's count to "What the outputs tell" and to the third limit.
With O1, the paper's honest headline is that partial supervision of the state makes these machines
learnable in proportion to what it tells, with approximations as the form such supervision took.

### G3 (S2). No control separates being a congruence from telling the state

**Where.** Paper 1's A2. The audit's F3 asked for "a learnable non-congruence output (for example
a function of the last column only, or of a short suffix)", and T1 ran those.

**The fault.** Neither control is matched. The suffix is not a function of the state, so its arm
must learn a machine of 125 states at a smaller surplus (the paper says so). The token tells
nothing of the state. The product is a function of the state but tells 10 classes against the
sum's 22. A function of the state that is no congruence and tells as much as the sum was never
tried.

**It exists.** At `p` 5, a balanced partition of the 25 states into 5 blocks that is no congruence
and, with the answer, tells exactly 22 states: about 5% of random balanced partitions do (92 of
2,000 drawn; they range from 14 to 24). The polynomial ones tried (`A + B^2`, `A + 2B^2`,
`A + B^3`, `A^3 + B`) are balanced non-congruences telling 19.

**Recommendation.** Section 4, step 1.

### G4 (S2). T10r replicated the confounded contrast and dropped the clean arm

**Where.** Paper 1's A4; `batch.py` ("T10r (D24): T10b on fresh machines, P0 against P2 alone").

**The fault.** T10's registered contrast is planted-and-given against primitive, and planting
changes the machines (the paper says so). The contrast free of that is the same planted machines
given their blocks or not. In T10 it favoured giving on 5 of 15 machines and the other way on
none (exploratory, one-sided p 0.031, recorded). The replication repeated the confounded contrast
on 25 fresh machines and left the not-given arm out, so the clean contrast still has no registered
test.

**Recommendation.** Section 4, step 1 (c).

### G5 (S2). "20 fresh seeds an arm" hides shared seeds and a shared data stream

**Where.** Paper 1's Statistics: "Every comparison at 20 fresh seeds an arm".

**Evidence.** T1's three arms, T3's three arms and all nine backdrops of T2 and T5 ran on seeds
300-319; T12's two arms on 320-339; T11 on 700-719. Within a seed the training words are the same
in every arm (O4). Only T12's table says "the same 20 seeds".

**What it changes.**
- The comparisons are paired, and the tests used (Fisher's, for independent samples) ignore it.
  With runs positively related within a seed that errs on the conservative side, so no verdict is
  at risk. Read in pairs, T12 gives 9 both, 2 the cover only, 8 the state only, 1 neither
  (McNemar's exact p 0.11): the registered reading stands.
- The three scale rates (17, 16 and 15 of 20) are not three independent samples (O4).
- A seed that is bad for one arm tends to be bad for another, which is power the designs could
  have used.

**Recommendation.** Say which tests share seeds. Register paired tests where seeds are shared (the
post-paper plan's D20 already does for the crystallisation A/B).

### G6 (S2). The outcome is a rate at a fixed budget, though the paper reads a rate as a cost

**Where.** Paper 1's Discussion ("a rate is a cost, not a verdict: restarts, and epochs to a
certificate") against its registered bars and tables (successes of 20 at 600 or 400 epochs).

**The fault.** A rate at a fixed budget mixes how often a run succeeds with how long it takes.
- At 169 states the certified runs take up to 534 of 600 epochs and the median grows with `p`
  (O3). The fall from 17 to 15 of 20 is as consistent with the budget cutting slow runs off as with
  the machine being harder.
- S3 reads as "undecided" while its cost per certificate is about S4's (O6).
- The registered bar (a Wilson lower bound of 0.25) would pass or fail a target on its budget.

**Recommendation.** Make the registered outcome the cost per certificate at a cutoff fixed
beforehand, with the time to a certificate compared across arms as censored data (a log-rank test,
or the restart cost at the registered cutoff). Keep the rate beside it.

### G7 (S2). The exclusion bound can't be reached within the budget, and does no work

**Where.** Paper 1's Method ("Every cell is checked against its target before any run: ... a
curriculum able to reach the exclusion bound `m + q - 1`"); experiment-design.md, section 1;
information-flow.md, row 2; machine-discovery.md ("train to `m_codes + m - 1`, which excludes
memorising for any target within the bound").

**Evidence.**
- A curriculum step takes at least one epoch, so a 600-epoch run trains on at most 600 lengths.
  The caps are 1,144 at 121 states and 1,612 at 169 (the runs' `checkpoint.json`). The bound is
  out of the budget's reach in those cells whatever the run does; at 49 states (489) it is
  reachable only if nearly every step takes one epoch. Most steps take 11.
- No run came near it: certificates come at steps of about 10 (O3), failures end near step 34.
  The paper says so ("No run came near the bound").
- The bound's argument needs agreement on every input up to that length. Training samples them.
  Even a run that reached the cap would not have shown what the argument needs.

**The claim.** The feasibility check passes on the cap's setting and ignores the budget, and the
rule has never constrained a result. The audit's F8 found that certificates come before the bound;
that the budget can't reach it, and that sampling can't establish it, is the further point. With
the target known, the certificate rules memorising out, as the paper says. With the target
unknown, the bound gives nothing: only the stop and Chow's test set do (T6), and the discovery
note should say that in place of the sentence above.

**Recommendation.** Replace the rule with the condition the data fits: training lengths that reach
every state and tell every pair apart (the depth plus the distinguishing length, the register's
row 15, made general), with a stated multiple. Correct the paper's sentence in its next version.

### G8 (S3). The discovery note still reads the product and the suffix as evidence

**Where.** machine-discovery.md, "Suggested primitives": "In paper 1 the outputs that weren't
approximations didn't help: the product, as distinguishing as the sum, 0 of 20; the suffix,
carrying state, 0 of 20. If that generalises, a suggested primitive that is part of the target
speeds the find and a wrong one doesn't".

**The fault.** Paper 1 withdrew both readings: the product tells 10 classes against the sum's 22,
and the suffix's arm needs a machine of 125 states. The premise of the suggested-primitives stage
(that learnability tests a suggestion) rests on them.

**What the suffix does show.** A suggestion that is not a function of the target's state changes
the machine to be learned: the network must compute the answers and the suggestion together, a
machine of up to the product of their sizes (25 became 125). So a wrong suggestion has a cost that
can be computed beforehand, and a right one leaves the size unchanged.

**Recommendation.** Correct the note. Adopt as a feasibility rule: a cell's codes and lengths are
checked against the joint minimal machine of the answers and every extra output, not the target's.

### G9 (S2). No classical learner has been run, and the data regime hides discovery's question

**Where.** Paper 1's related work ("it is not our comparator"); machine-discovery.md ("On clean
symbolic data the classical learners are the baseline any discovery claim must be compared
against").

**Evidence.** An epoch is 32,768 words, each labelled at every column, and a certified run trains
for about 50 to 500 of them: millions of labelled words, at lengths of mostly 10 or fewer. With
nine tokens there are 59,049 words of length 5, so every short word is seen many times over. From
such data a state-merging learner recovers these machines outright.

**The claim.** That is no fault in paper 1, whose question is what gradient descent needs to be
told. It matters for the goal. The results so far measure optimisation with unlimited clean data.
Discovery's cases are limited behaviour, noisy outputs and inputs that aren't symbols, and none
has been measured for the network or for a classical learner. Until one is, "why a network" is an
argument, not a result.

### G10 (S2). The SMB plan reaches a real system before the controlled stages

**Where.** The SMB world-model workplan, W8 (each object class's update "as a snapped machine,
read off, minimised, and checked against RAM's object state"); machine-discovery.md, stages A-F.

**The gaps.**
- **The stages skipped.** Hidden targets (C), suggested primitives (C2, "the first experiment
  after paper 1"), queries (D) and raw inputs and noise (E) have not been run. W8 is stage F with
  stage E's inputs.
- **No input alphabet.** The certificate enumerates every token from every reachable code. An
  object's inputs ("what it touches") have no finite alphabet defined yet; the machine-policy plan
  met the same wall ("a symbolic certificate isn't possible for an alphabet of grids"). Choosing
  that alphabet is most of the discovery, and the plan doesn't yet say who chooses it.
- **The organ's misses are systematic.** The objects' claim was refuted at 86.3% found, the
  shortfall mostly four levels and piranha plants behind pipes. A learner sees an object class
  that vanishes on a schedule, not noise.
- **No reference arms.** With tracks as symbols, an object's machine is a few states, which a
  classical learner finds. Without an arm on RAM's exact tracks and a classical learner on the
  same tracks, a W8 failure can't be placed (the organ, the alphabet or the network) and a success
  can't be credited.
- **The machine-policy's failure is undiagnosed.** Its control (M4) failed, and the probe named to
  separate the snap from credit assignment (the coupling held at 0) wasn't run. The world-model
  plan's case for a dense signal rests on the reading that probe would test.

**One thing in its favour.** The emulator's restore gives query access to an object's behaviour,
so Chow's test set can apply there, which no synthetic stage has needed yet.

## 3. Checked, and holds

- **The certificate's logic** (`window_recurrent_certificate.py`): a map from reachable joint
  codes onto the target's states, fixed breadth first and checked on every token; near ties
  branched to every combination; a label's near tie fails. A pass is a proof of equality at every
  length for the network's floating-point function, as the paper states.
- **Chow's test set** (`chow.py`): the transition cover, the characterisation set and the middles
  up to the slack are the W-method's; whole label sequences are compared.
- **Paper 1's statistics, recomputed from its counts:** Fisher's tests for T1 (0.010, 0.046), T2
  (7.7e-8), T3 (6.4e-6), T11 (0.091, 1.8e-4, 8.3e-6) and T12 (two-sided 0.082), and Holm's
  adjustment over the family of 12 (0.061, 0.10, 0.18, 0.038, 0.25, 0.0014, 7.5e-5): all match.
- **"What the outputs tell":** 6, 10 and 22 of 25 at `p` 5, and 12 and 112 of 121 at `p` 11.
- **The ledgers' counts** against the paper's tables: 176 certified runs, each table's rows.
- **The crystallisation cell's codes:** it used the paper's rule (`--codes-ratio 32/11`, 8 a
  factor on S3), so its S3 rate against the paper cell's is not confounded by the code count (the
  budget, the width and the stop still differ, as the post-paper plan says).

## 4. The most promising avenues

1. **Congruence against information.** The programme's own central open question, and the one a
   reader of paper 1 will ask first. Both outcomes are results. Hours of compute at `p` 5.
2. **A law for the cost.** O1 and O3 suggest two regularities: the cost of a certificate falls with
   the classes told, and, given a cover, rises with a factor's size, not the machine's. Each is a
   prediction that a small ladder can refute.
3. **Discovery where classical learners stop.** Noisy answers, limited behaviour and wrong
   suggestions are where the network is claimed to earn its place. A result there, against a
   classical learner on the same data, is what would make the discovery goal a finding.
4. **The seed's part in failure** (O4). If the initial weights carry it, a failure may be read
   before training; if the words do, the curriculum's sampling is at fault. Either is a remedy for
   reliability that needs no new method.
5. **The certificate as an instrument for others.** It is the programme's most finished piece.
   Networks from the state-tracking and length-generalisation literature that pass their tests are
   candidates for it wherever a finite code can be put between their steps.

## 5. The direction recommended

In order. Steps 1 to 3 are days of compute and bear on everything after them.

**Step 1. The matched controls (registered).**
- **(a) Division at `p` 5,** T12's cell and budget, the seeds shared across arms and read in pairs.
  Arms: the sum; a balanced 5-block partition that is no congruence and tells 22 states with the
  answer (G3), fixed before the runs; the answers alone. 40 seeds an arm: runs in this cell are
  short (T12's took a median of 12 minutes, the longest 2.4 hours), and 20 an arm tells 0.8 from
  0.4 and no less.
  - *If the partition helps as the sum does:* the claim becomes that partial supervision of the
    state helps in proportion to what it tells. Approximations then matter for a different reason,
    and a good one for discovery: they are the supervision one can have without knowing the
    target.
  - *If it doesn't:* being a congruence matters beyond what it tells, an algebraic result that
    paper 1 could then claim outright.
- **(b) Primitive random machines of 16 states** given a random balanced 4-block partition (no
  congruence exists to give), against the answers alone. It tells about what the planted blocks
  tell (O2) with no planting, so it removes T10's confound from the other side.
- **(c) Planted machines, fresh, given against not given,** the same machines in both arms, read
  in pairs by machine (G4).
- **(d) A ladder of classes told,** if (a) to (c) leave the question standing: targets with a
  lattice of congruences (two counters with a composite modulus, whose divisors give coarse
  quotients), each approximation set against a matched non-congruence. The outcome is the cost of
  a certificate against the classes told.

**Step 2. The outcome.** From the next registration on: the cost per certificate at a cutoff fixed
beforehand, the time to a certificate as censored data, paired tests on shared seeds, and the
count of classes told beside every arm (G5, G6). Run the crystallisation A/B (the post-paper
plan's X) on that outcome.

**Step 3. The seed's part.** Separate the seed of the weights from the seed of the words (one
argument more). On the five seeds of O4 and five that succeeded at every size, at 49 states: each
bad seed's weights with a good seed's words, and the reverse. About 20 runs.

**Step 4. The cost's scaling.** Division with its cover at `p` 17, 19 and 23 (289 to 529 states),
budgets set in proportion to `p`, the medians predicted beforehand (O3). Then three coordinates
(three numbers, three factors), to ask whether the cost follows the factors' sizes or their
number. Width 32 is untested past 169 states (the register's row 3), so a failure is read by kind
first.

**Step 5. Discovery, controlled.** Hidden targets from paper 1's set. The axes: the amount of
behaviour, label noise in the answers, and suggestions right and wrong (each cell sized on the
joint machine, G8). The outcome: exact recovery, proved against the hidden target afterwards, and
the same for a classical state-merging learner on the same data. The claim to register is that
the network recovers the machine at a noise level or sample size where the classical learner does
not; if it never does, that is the finding.

**Step 6. Then W8,** with what step 5 taught about noise, and with two arms added: RAM's exact
tracks as the ceiling, and a classical learner on the same tracks. Its input alphabet is fixed and
written into the registration before any run. Chow's test set runs on the emulator's restore.

**What to stop or hold.** Further work on the organ, until steps 1 to 3 are read: its results
don't bear on any open question above. The branching and depth parts of the post-paper plan, until
step 3 says whether failure is the architecture's at all.
