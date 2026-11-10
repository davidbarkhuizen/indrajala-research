# Workplan: what a network must be told (congruence against information, the cost's laws, discovery controlled)

**Status (2026-11-10): drafted, at the owner's direction after the programme review
([review-2026-11-10-programme-review.md](../../review-2026-11-10-programme-review.md)): "re-frame the
planned work in this light". Nothing is built or run. D1-D10 are settled under the owner's
delegation, each with its options' pros and cons. O1 is resolved by that direction; O2-O4 are the
owner's and open. This plan re-orders the open plans; it retires none.** "The review" below is that
review, and O1-O6 and G1-G10 with "the review's" before them are its findings. This plan's own IDs
are D1-D10, O1-O4 and stages 0-7.

**Order changed by the owner (2026-11-10, after this plan was drafted): "I would like to complete the SMB work
first - then return to the machine discovery research".** O1 below is reversed: the SMB world-model plan
([smb-world-model-workplan.md](smb-world-model-workplan.md)) runs first, as it stands, and this plan's stages
1-6 wait until it is complete. Nothing else here changes: the stages keep their order among themselves, and
O2-O4 stay open.

**The question.** Paper 1 trained networks on a target's answers and some of its approximations and
found machines it didn't find from the answers alone. The review found that one variable orders
every result there: the classes of the target's states that the training targets at a column tell
apart (its O1). Whether an extra output is an approximation has no evidence of its own. So:

1. Does being a congruence matter beyond what the output tells of the state?
2. What does a certificate cost, as a function of what is told and of the machine's factors?
3. Is there any behaviour (noisy, limited, with suggestions right and wrong) from which the network
   recovers a machine that a classical learner doesn't?

The goal is unchanged: [machine-discovery.md](../research-notes/machine-discovery.md). Question 1
decides what paper 1 can claim. Question 3 decides whether discovery by a network has a case.

## The IDs, in time order

| ID | When | Short label | What it is |
| --- | --- | --- | --- |
| O1 | 2026-11-10 | SMB first | **reversed by the owner the same day:** the SMB work is completed first, then this plan (it first read: W2.4 and W8 wait for this plan's stages) |
| O2 | 2026-11-10 | paper 1's next version | whether and when the review's G1, G2 and G5-G7 are corrected in a new version; open |
| O3 | 2026-11-10 | paper 1 on arXiv | whether paper 1's submission waits for stage 1's reading; open |
| O4 | 2026-11-10 | the exclusion bound's rule | whether the protocol's rule is replaced by a coverage rule; open |
| D1 | 2026-11-10 | the order | the record, the matched controls, the seed's part, the cost's scaling, crystallisation's A/B, discovery controlled, then W8 |
| D2 | 2026-11-10 | the outcome | the certified rate first in stage 1, the cost beside it; the cost first from stage 3 on |
| D3 | 2026-11-10 | the cost's measure | a paired sign test on epochs to a certificate; the cost per certificate at a cross-fitted cutoff |
| D4 | 2026-11-10 | the matched partition | a balanced partition of the states, no congruence, telling exactly what the approximation tells |
| D5 | 2026-11-10 | stage 1's targets | division at `p` 5 and fresh planted machines of 16 states, three arms each |
| D6 | 2026-11-10 | fresh arms | every arm of a registered test run fresh; no arm reused from paper 1 |
| D7 | 2026-11-10 | the seed's probe | weights and words crossed on five bad and five good seeds at 169 states |
| D8 | 2026-11-10 | the scaling ladder | the cover at `p` 17, 19 and 23, budgets in proportion to `p`; three coordinates after |
| D9 | 2026-11-10 | the classical learner | chosen from the literature first, noise-tolerant learners included |
| D10 | 2026-11-10 | what waits | branching and depth behind the seed's probe; the organ behind stages 1-2 |

From other plans: crystallisation's A/B (X), branching (B) and depth (L) in
[post-paper-retests-workplan.md](post-paper-retests-workplan.md); the events (W2.4) and discovery
(W8) in [smb-world-model-workplan.md](smb-world-model-workplan.md); the submission (A4) in
[arxiv-posting-workplan.md](arxiv-posting-workplan.md); paper 1's tests T1-T12 (the retired paper
workplan, `git show 0d1aaef:docs/workplans/paper-workplan.md`); the feasibility register's rows in
[information-flow.md](../protocols/information-flow.md).

## Why

**What the review found, in the terms this plan uses.**
- **The classes told** (the review's O1). For an arm, the number of classes of the target's states
  that the answer's label and every extra output's label together tell apart, at one column. At `p`
  5: the answers alone 6 of 25, with the product 10, with the sum 22, with the cover or the state
  25. The certified rates follow that order, and nothing else is needed to order them.
- **No matched control** (its G3). The product tells less than the sum; the suffix is no function
  of the state. A function of the state that is no congruence and tells as much as the sum was
  never run.
- **The planted arm is not coarse** (its O2, G2). Given their blocks, the planted machines' targets
  tell 11.2 of 16 states on average, against 4 without.
- **The clean contrast was dropped** (its G4): the same planted machines, given their blocks or
  not, has no registered test.
- **The cost has regularities** (its O3, O5, O6). The certified step doesn't grow with the machine;
  epochs grow with `p`; a run certifies early or not at all; a rate at a fixed budget hides all
  three.
- **Failures share seeds** (its O4), across machine sizes.
- **Discovery's case is untested** (its G9): no classical learner has been run, and the data so far
  is unlimited and clean.

**Why this order.** Stage 1 costs days and decides the headline of everything published so far.
Stage 2 costs a night and says whether failure is the weights', the words' or the method's, which
every later reliability study (crystallisation, branching, depth) needs to know. Only then are the
long runs spent.

## Decisions

- **D1. The order: (a).**
  - *After the SMB work (O1, as the owner reversed it).*
  - (a) *Chosen.* Stage 0 the record; 1 the matched controls; 2 the seed's part; 3 the cost's
    scaling; 4 crystallisation's A/B on the cost outcome; 5 discovery, controlled; 6 W8.
    - Pros: the cheapest and most decisive first; each later stage is designed on the one before
      (5's cells are sized on what 1 says helps; 4's pairs on what 2 says a seed is).
    - Cons: discovery, the goal, comes fifth; crystallisation, which the owner expects to be the
      default, waits behind two short stages.
  - (b) Discovery first (stage 5).
    - Pros: the goal's own question soonest.
    - Cons: its cells give suggestions as extra outputs, and what a suggestion must be (a
      congruence, or anything that tells the state) is stage 1's question.
  - (c) Finish the organ's events and W8 first, then this plan.
    - Pros: the planned work finished before new work is planned.
    - Cons: W8 has no input alphabet, no reference arms and no measured tolerance to the organ's
      misses (the review's G10); its result couldn't be placed either way.
- **D2. The outcome: (b).**
  - (a) The certified rate at the cell's budget, as paper 1.
    - Pros: comparable with every earlier number.
    - Cons: mixes how often with how long (the review's G6).
  - (b) *Chosen.* In stage 1, the certified rate is the registered test's outcome (the claim under
    test is paper 1's, so it is measured paper 1's way), with D3's cost measures registered beside
    it. From stage 3 on, the cost is first and the rate beside it.
    - Pros: stage 1 can't be read as a change of goalposts; later stages measure what the paper
      says a rate is.
    - Cons: two readings a test.
  - (c) The cost first everywhere.
    - Cons: stage 1's verdict would rest on a measure paper 1 never registered.
- **D3. The cost's measure: (c).**
  - (a) Stop every run before curriculum step 15 (the review's O5) and count epochs a certificate.
    - Pros: one line. Cons: a constant read from paper 1's cell; the continuous cell has no such
      steps.
  - (b) An epoch cutoff a backdrop, from earlier runs.
    - Cons: a constant a backdrop; none exists for a new target.
  - (c) *Chosen.* Two measures, neither with a constant:
    - **the paired sign test on epochs to a certificate:** for each seed (or machine) shared by two
      arms, the arm that certified in fewer epochs wins; a certified run beats a spent one; two
      spent runs tie and are dropped. Exact, two-sided unless registered otherwise;
    - **the cost per certificate at a cross-fitted cutoff:** an arm's seeds are split in two by
      their registered order; each half's cutoff, in epochs, is the one that minimises the other
      half's restart cost; the cost is the epochs spent under those cutoffs over the certificates
      kept. Reported with the cost as run and a bootstrap interval over seeds.
    - Pros: uses the time and the pairing; nothing tuned on the data it is read from; works on any
      cell. Cons: two small builds (`inference.py`, `restart-cost`); the cross-fit halves the
      seeds a cutoff is chosen on.
- **D4. The matched partition: (a).**
  - (a) *Chosen.* For a target and an approximation of it: a partition of the target's states with
    the approximation's block sizes, that is **no congruence**, and that with the answer tells
    **exactly as many classes** as the approximation does. Drawn from a seeded generator until all
    three hold, fixed in the code with a test of each property, before any run.
    - Pros: a function of the state, so the machine to be learned is unchanged (the review's G8);
      the same label count and the same classes told; only the congruence differs.
    - Cons: a random partition has no meaning a person would suggest; it is a control, not a
      method.
  - (b) An algebraic non-congruence (`A + B^2` at `p` 5).
    - Cons: tells 19 classes against the sum's 22: not matched.
  - (c) A congruence of another machine on the same states.
    - Cons: brings a second machine's structure in; harder to say what differs.
- **D5. Stage 1's targets: (a).**
  - (a) *Chosen.* **Division at `p` 5** in T12's cell (the approximation claim's, 400 epochs), on
    one vocabulary: the answers alone; with the sum; with the sum's matched partition. **Planted
    machines of 16 states** in the paper's cell (600 epochs), 25 fresh machines: the answers alone;
    with the planted blocks; with the blocks' matched partition, matched machine by machine.
    - Pros: the two places paper 1 claims a single approximation helps; the planted arms share
      their machines, so planting's own effect (paper 1's A4) cancels; the given-against-not-given
      contrast (the review's G4) is in the same batch.
    - Cons: two small targets; the planted runs are the slow ones.
  - (b) Division alone.
    - Cons: arithmetic only; the review's G4 left open.
  - (c) Primitive random machines given a random partition, beside (a).
    - Pros: a target with no congruence at all.
    - Cons: 100 more long runs for a contrast the planted arms already make on shared machines.
      Kept for stage 1's follow-up if the readings disagree.
- **D6. Fresh arms: (a).**
  - (a) *Chosen.* Every arm of a registered test is run fresh, on seeds and machines no earlier
    test used.
    - Pros: no arm seen before its registration (the audit's F20).
    - Cons: T10r's given arm on disk isn't reused: about 50 runs more.
  - (b) Reuse paper 1's arms where the cell is unchanged, with two reruns to check bit identity.
    - Pros: fewer runs. Cons: a registered test with a known arm; the audit already faulted one.
- **D7. The seed's probe: (a).**
  - (a) *Chosen.* A probe (it claims nothing). A second seed for the training words
    (`--data-seed`, default the run's seed, so every earlier run is unchanged). At `p` 13, where
    all five of the review's seeds (303, 306, 310, 314, 315) fail and five others (300, 301, 302,
    304, 305) certify at every size: each bad seed's weights with a good seed's words, and the
    reverse, in five pairs. Ten runs, and one rerun of each kind with the flag unset to check the
    path is unchanged.
    - Pros: a clear outcome reads at once (the failures follow the weights, or the words); a night
      on one machine.
    - Cons: five pairs show only a clear outcome; a mixed one needs more pairs, registered then.
  - (b) At `p` 7, cheaper.
    - Cons: only two of the five seeds fail there.
  - (c) A full cross of ten weights by ten words.
    - Cons: 100 runs of up to two hours before knowing whether there is anything to find.
- **D8. The scaling ladder: (a).**
  - (a) *Chosen.* **Existence first:** the cover at `p` 17, four seeds, the paper's cell, a budget
    of 46 epochs a unit of `p` (the paper's 600 at `p` 13, in proportion). **Then, registered:**
    `p` 17, 19 and 23 (289, 361 and 529 states), 20 seeds each, the prediction that the median
    epochs to a certificate lie between 20 and 30 times `p` and the median certified step between
    7 and 14. **Then three coordinates** (three numbers, three factors), designed at its own
    registration, if the ladder holds.
    - Pros: three more points on a line drawn through three; a refutable number; the step up to
      more factors only if the law it rests on holds.
    - Cons: the window's width, 32, is untested past 169 states (the register's row 3); a failure
      is read by kind before anything is concluded, and a wider window is its own registered arm.
  - (b) Three coordinates first.
    - Cons: a new target and a third factor at once: two changes.
  - (c) One large `p` (31, 961 states).
    - Cons: a lone point; if it fails, nothing says where the law broke.
- **D9. The classical learner: (a).**
  - (a) *Chosen.* Literature first: passive learners of Mealy machines from labelled words, with
    and without label noise (state merging; SAT and MaxSAT identification; the statistical
    mergers). The papers are persisted by the rule (indrajala-literature). The baseline is the
    strongest that runs on our data, plain state merging beside it.
    - Pros: the comparison is with what the field would use, not a straw man; if a library does
      it, nothing is built.
    - Cons: a reading stage before any run.
  - (b) Our own state merger only.
    - Cons: plain merging breaks on one wrong label; beating it under noise shows nothing.
  - (c) No baseline, the network alone.
    - Cons: the review's G9 stands.
- **D10. What waits: (a).**
  - (a) *Chosen.* Branching (B) and depth (L) wait for stage 2's reading and then for X, as the
    post-paper plan already orders them. The organ's events (W2.4) and W8 wait as O1 says. The
    paused plans (the general algebras, the factorisation machine, addition at any length, the
    numeral reader) stay as they are.
    - Pros: no architecture study runs before it is known whether failure is the architecture's.
    - Cons: the builds done ahead for B (the merge op) sit unused a while longer.
  - (b) B and L now, beside stage 1.
    - Cons: two more long batches on two machines; their reading depends on stage 2.

## The owner's calls

- **O1. SMB first: resolved (the owner, 2026-11-10: "I would like to complete the SMB work first - then return
  to the machine discovery research").** The SMB world-model plan runs first, from where it stands (W2.4 next).
  This plan's stages 1-6 follow it.
  - *As first drafted,* O1 held W2.4 and W8 behind this plan's stages; that was read from "re-frame the planned
    work in this light", and the owner reversed it the same day.
  - Stage 6 (W8's additions: its input alphabet fixed at registration, an arm on RAM's exact tracks, a classical
    learner on the same tracks, Chow's test set on the emulator's restore) applies whenever W8 runs.
- **O2. Paper 1's next version: open.** The review's G1 (the definition of "told"), G2 (the
  planted arm's count), G5 (shared seeds), G6 (rate and cost) and G7 (the exclusion bound's
  sentence) are statements in a published preprint.
  - (a) A new version now, with those five corrected. Pros: the record right soonest. Cons: stage
    1 may change the headline within a week, and a third version would follow.
  - (b) *Recommended.* One new version after stage 1 is read, carrying the corrections and stage
    1's result. Pros: one revision. Cons: the known faults stand for a week or two.
  - (c) No new version; the corrections in a second paper. Cons: the preprint keeps a vacuous
    definition.
- **O3. Paper 1 on arXiv: open** (the arXiv plan's A4, the owner's submission).
  - (a) Submit both now. Pros: indexed sooner. Cons: paper 1's title claims what stage 1 tests.
  - (b) *Recommended.* The certificate note now (nothing here touches it); paper 1 with O2's new
    version. Pros: nothing posted that a week's runs may revise. Cons: paper 1 waits.
- **O4. The exclusion bound's rule: open** (experiment-design.md, section 1; the register's row 2).
  - (a) Keep it. Cons: it can't be met within the budgets at 121 and 169 states, and no run has
    come near it (the review's G7).
  - (b) *Recommended.* Replace it at stage 3's registration with a coverage rule: training lengths
    of at least a stated multiple of the target's depth plus its distinguishing length (the
    register's row 15, made general), the multiple read from paper 1's certified steps. Pros: a
    rule that binds and that the data fits. Cons: a protocol change; stage 3 tests it at sizes it
    wasn't read from.

## Feasibility

Every cell is checked against the register before its registration; these are the rows as they
stand, completed there. A new row from the review's G8: **the machine to be learned is the joint
minimal machine of the answers and every extra output**, and the codes are counted against it.

| stage | cell | states (joint) | codes a factor, joint | width | notes |
| --- | --- | --- | --- | --- | --- |
| 1, division `p` 5 | the approximation claim's | 25 (every arm: each output a function of the state) | 16, 256 (10.2 times) | 16 | the cell certified 6-17 of 20 at `p` 5 given an extra output; the sum a congruence, its matched partition tested not to be; both tell 22 |
| 1, planted 16 states | the paper's | 16 (every arm) | 12, 144 (9 times) | 32 | T10r's cell; each machine's only nontrivial principal congruence the planted one (T10's rule) |
| 2, `p` 13 | the paper's | 169 | 38, 1,444 (8.5 times) | 32 | T2's cell, 15 of 20 |
| 3, `p` 17, 19, 23 | the paper's | 289, 361, 529 | 50, 56, 67; 2,500, 3,136, 4,489 (8.5-8.7 times) | 32 | width untested past 169 (row 3): the existence probe first |

The training lengths: division's depth plus its distinguishing length is at most 4 at every size
here, and the curriculum passes it within its first steps (O4); the planted machines' is computed
at stage 1's registration.

## Stages

Each stage that makes claims registers them here, with their refutations and its feasibility rows,
before its data. Builds are one PR each, in indrajala-studies unless said.

0. **The record.**
   - machine-discovery.md corrected where the review's G7 and G8 found it stale (done with this
     plan's PR); the workplans' statuses; the handover.
   - O2-O4 put to the owner.
1. **The matched controls (D4-D6).**
   - **Builds:** `told` in `modular_family_probe.py` (an arm's classes told, from the machine and
     the arm's partitions); the matched partitions (D4), each with its test; division's arm for a
     named partition and a machine's (`--arm matched`); D3's sign test and cross-fitted cost; the
     review's readings as probe commands (the seeds' clustering, the pairs).
   - **A probe** of each cell for its epoch time on `stone` and `klip`.
   - **Registration.** The tests, each paired, Holm over the five:
     - *information, twice:* the matched partition against the answers alone, one-sided, at `p` 5
       (McNemar's exact test over seeds) and on the planted machines (the exact signed-rank test
       over the machines' differences in certified runs);
     - *congruence, twice:* the approximation against its matched partition, two-sided, the same
       two tests;
     - *given against not given:* the planted blocks against the answers alone, one-sided.
   - **The readings, fixed at registration:** *information* if the partition helps and the
     approximation doesn't beat it; *congruence* if the approximation beats the partition;
     *both*; or *undecided*, with the interval on each difference.
   - **The draws:** at `p` 5, seeds 800-839 in every arm; the planted machines the next 25 seeds
     from 53 whose only nontrivial principal congruence is the planted one (T10r's rule), two
     runs each, the same run seeds in every arm.
   - **The batch,** run to its end, then the reading and the long tests.
2. **The seed's part (D7).** `--data-seed`; the ten runs and two checks at `p` 13; the reading
   (the weights, the words, or mixed). A clear reading names the next probe: what in the weights
   (which layer's draw), or what in the words (which epochs').
3. **The cost's scaling (D8).** The existence probe at `p` 17; the registration with its
   predictions and O4's rule if the owner takes it; the ladder; then three coordinates.
4. **Crystallisation's A/B (the post-paper plan's X),** as designed there, with two changes fixed
   at its registration: D3's measures beside its paired test, and stage 2's reading taken into its
   pairs (if the words carry failure, both arms draw the same words, as they do now; if the
   weights, the pairs share them where the cells allow). The incremental reheat as that plan
   orders it.
5. **Discovery, controlled** (machine-discovery.md's stages C and C2, with E's noise).
   - **The literature (D9),** and the baseline chosen.
   - **Builds:** a fixed corpus of words (drawn once, reused every epoch) and label noise at a
     stated rate, both in the data path; the baseline's harness.
   - **The cells, at registration:** hidden targets from paper 1's set; the amount of behaviour;
     the noise; suggestions right and wrong, each cell sized on the joint machine. What stage 1
     found decides what counts as a right suggestion.
   - **The claim to register:** a noise level or a corpus size at which the network recovers the
     machine exactly (proved against the hidden target afterwards) and the baseline doesn't. If
     there is none, that is the finding, and machine-discovery.md's "Why a network" is rewritten
     to it.
6. **W8** (the SMB plan's), with: its input alphabet fixed and written into its registration; an
   arm on RAM's exact tracks; the classical baseline on the same tracks; Chow's test set on the
   emulator's restore; and stage 5's measured tolerance to noise set against the organ's misses.
7. **Findings** into paper 1's next version (O2), contribution.md, failure-kinds.md and the
   register; this plan retired, its leftovers to next-steps.md.

## The size, roughly (each stage's probe replaces it)

`jebel` is out of service, so the fleet is `stone` (7 workers) and `klip` (7 slots under its
thermal guard). Epoch times below are paper 1's on those two, measured under heavier load than
now.

- **Stage 1:** 120 runs at `p` 5 of at most 400 epochs (about 10-19 s an epoch): under a day. 150
  planted runs of at most 600 epochs (25-65 s an epoch), most of them spent: about three days.
- **Stage 2:** 12 runs of at most 600 epochs at `p` 13: a night on `stone`.
- **Stage 3:** the probe a night; the ladder 60 runs of up to about 1,060 epochs: about two days.
- **Stage 4:** as the post-paper plan sizes X (180 runs of up to 1,600 epochs): the longest, a
  week or more on two machines.
- **Stage 5:** sized at its registration.

## Machines

The batch runner on `stone` and `klip`, memory planned a host before launch; `pyramidon` for the
builds and the readings only; `litshe` parity only; `jebel` not until the owner says.

## Findings

None yet.
