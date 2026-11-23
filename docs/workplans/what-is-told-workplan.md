# Workplan: what a network must be told (congruence against information, the cost's laws, discovery controlled)

**Status (2026-11-22): stages 0-3 done. Stage 1 (the
matched controls): congruence at `p` 5, undecided on the planted machines. Stage 2 (the seed's part): mixed, a
follow-up probe next. Stage 3 (the cost's scaling): it breaks at `p` 19; the width probe at 19 and 23 next
(Findings, below). Paper 1's version 2 is published (O2, 2026-11-19). Drafted 2026-11-10, at the owner's
direction after the programme review
([review-2026-11-10-programme-review.md](../reviews/review-2026-11-10-programme-review.md)): "re-frame the
planned work in this light". Nothing is built or run. D1-D10 are settled under the owner's
delegation, each with its options' pros and cons. O1-O4 are resolved by the owner (O2-O4 on 2026-11-14). This
plan re-orders the open plans; it retires none.** "The review" below is that
review, and O1-O6 and G1-G10 with "the review's" before them are its findings. This plan's own IDs
are D1-D10, O1-O4 and stages 0-6.

**Order changed by the owner (2026-11-10, after this plan was drafted): "I would like to complete the SMB work
first - then return to the machine discovery research".** O1 below is reversed: the SMB world-model plan
(`smb-world-model-workplan.md`) runs first, as it stands, and this plan's stages
1-6 wait until it is complete. Nothing else here changes: the stages keep their order among themselves, and
O2-O4 stay open.

**The SMB plan stopped (2026-11-14).** The owner stopped the SMB world-model plan after its W6's R3 and retired it
("this is going nowhere, and blocking other real work"; read it with `git show 2a6aabe:docs/workplans/smb-world-model-workplan.md`). **This plan's stages no longer wait
on it:** they run in their own order (D1).

**W8 removed (the owner, 2026-11-14: "remove W8 from the plan").** The old stage 6, W8 (the retired SMB plan's
discovery stage) with its reference arms, is out of this plan; the old stage 7 (the findings) is now stage 6. The
organ's code and data stay where they are (indrajala-rl, indrajala-studies' `data/smb-world-model/`), unused here.
Stage F of machine-discovery.md (a real system) has no plan now.

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
| O2 | 2026-11-10 | paper 1's next version | whether and when the review's G1, G2 and G5-G7 are corrected in a new version; **resolved 2026-11-14: one new version on Zenodo after stage 1 is read** |
| O3 | 2026-11-10 | paper 1 on arXiv | whether paper 1's submission waits for stage 1's reading; **resolved 2026-11-14: nothing goes to arXiv before the endorser can vouch (about December 2026); paper 1 goes then, in O2's corrected version** |
| O4 | 2026-11-10 | the exclusion bound's rule | whether the protocol's rule is replaced by a coverage rule; **resolved 2026-11-14: (b), a coverage rule at stage 3's registration** |
| D1 | 2026-11-10 | the order | the record, the matched controls, the seed's part, the cost's scaling, crystallisation's A/B, discovery controlled (W8, last as drafted, removed by the owner 2026-11-14) |
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
(W8) in the retired `smb-world-model-workplan.md` (`git show 2a6aabe:docs/workplans/smb-world-model-workplan.md`); the submission (A4) in
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
    scaling; 4 crystallisation's A/B on the cost outcome; 5 discovery, controlled; 6 the findings
    (as drafted, W8 came sixth; the owner removed it 2026-11-14).
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
    post-paper plan already orders them. The organ's events (W2.4) and W8 left with the SMB plan
    (retired 2026-11-14; W8 removed from this plan the same day). The
    paused plans (the general algebras, the factorisation machine, addition at any length, the
    numeral reader) stay as they are.
    - Pros: no architecture study runs before it is known whether failure is the architecture's.
    - Cons: the builds done ahead for B (the merge op) sit unused a while longer.
  - (b) B and L now, beside stage 1.
    - Cons: two more long batches on two machines; their reading depends on stage 2.

## The owner's calls

- **O1. SMB first: resolved (the owner, 2026-11-10: "I would like to complete the SMB work first - then return
  to the machine discovery research").** The SMB world-model plan runs first, as revised the same day (its W10
  next; W8 is no longer in it: its O5).
  This plan's stages 1-6 follow it.
  - *As first drafted,* O1 held W2.4 and W8 behind this plan's stages; that was read from "re-frame the planned
    work in this light", and the owner reversed it the same day.
  - The SMB plan was stopped and retired 2026-11-14, and the owner removed W8 (this plan's old stage 6) the same
    day.
- **O2. Paper 1's next version: (b), the owner (2026-11-14).** One new version, on Zenodo (a new version of
  paper 1's record), after stage 1 is read. The review's G1 (the definition of "told"), G2 (the
  planted arm's count), G5 (shared seeds), G6 (rate and cost) and G7 (the exclusion bound's
  sentence) are statements in a published preprint.
  - (a) A new version now, with those five corrected. Pros: the record right soonest. Cons: stage
    1 may change the headline within a week, and a third version would follow.
  - (b) *Recommended.* One new version after stage 1 is read, carrying the corrections and stage
    1's result. Pros: one revision. Cons: the known faults stand for a week or two.
  - (c) No new version; the corrections in a second paper. Cons: the preprint keeps a vacuous
    definition.
- **O3. Paper 1 on arXiv: settled by a constraint, the owner (2026-11-14).** Nothing can go to arXiv until the
  endorser can vouch: Brandoit's arXiv paper (arXiv:2609.32447, September 2026) counts toward endorsing only once
  it is three months old, about December 2026 (the arXiv plan's O1). Corrections are self-published on Zenodo
  meanwhile (O2). When the endorsement is possible, paper 1 goes in O2's corrected version, beside the note;
  stage 1 is read well before then. The options as drafted (the arXiv plan's A4, the owner's submission):
  - (a) Submit both now. Pros: indexed sooner. Cons: paper 1's title claims what stage 1 tests.
  - (b) *Recommended.* The certificate note now (nothing here touches it); paper 1 with O2's new
    version. Pros: nothing posted that a week's runs may revise. Cons: paper 1 waits.
- **O4. The exclusion bound's rule: (b), the owner (2026-11-14)** (experiment-design.md, section 1; the
  register's row 2). The protocol and the register change in stage 3's registration PR, not before.
  - (a) Keep it. Cons: it can't be met within the budgets at 121 and 169 states, and no run has
    come near it (the review's G7).
  - (b) *Recommended.* Replace it at stage 3's registration with a coverage rule: training lengths
    of at least a stated multiple of the target's depth plus its distinguishing length (the
    register's row 15, made general), the multiple read from paper 1's certified steps. Pros: a
    rule that binds and that the data fits. Cons: a protocol change; stage 3 tests it at sizes it
    wasn't read from.

### O2's publishing plan (agreed with the owner 2026-11-16: "that order is fine - go ahead")

Paper 1's version 2 and the datapack's version 2.0 go to Zenodo as new versions of their records (paper
`10.5281/zenodo.23826655`, datapack `10.5281/zenodo.23733575`). **The owner presses Publish; nothing here
publishes.**

- **V1. Stage 1's numbers.** `paper_reading.py told`, the manifest `told/stage1.sha256`, the findings here.
  **Done 2026-11-17.**
- **V2. Stage 1 in the paper's tables** (indrajala-studies #32): the `told1` keys, `tab:matched` and
  `tab:told-planted` from the batch, through `paper_tables.py fill` and `check`.
- **V3. Zenodo's new versions** (indrajala-studies #31): `zenodo_deposit.py newversion`, a published record's
  next version as a draft with its DOI reserved.
- **V4. The datapack's version 2.0** (indrajala-studies #33): stage 1 as the part `told-stage1`, the ml
  submodule over HTTPS, the note that reruns match only at their run's code; then the build and `check`.
- **V5. Reserve, fill, tag.** Both drafts made (`newversion`); their DOIs and the date into the paper, the
  metadata and the datapack README (branch `paper1-v2`); the PR merged; `paper1-v2` tagged in
  indrajala-research, indrajala-studies, ml and math-rust.
- **V6. Upload, then the owner.** The PDF and the datapack's files uploaded and checked (`status`); the owner
  reviews both drafts and presses Publish. After: the arXiv plan's A4 takes version 2.
  **Done 2026-11-19:** the owner published both (preprint version 2 doi:10.5281/zenodo.24303026, datapack 2.0
  doi:10.5281/zenodo.24303030, both dated 2026-11-17); the arXiv plan's package rebuilt from `paper1-v2`.

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

0. **The record. Done 2026-11-14.**
   - machine-discovery.md corrected where the review's G7 and G8 found it stale (#226); pointed at
     this plan's order without W8 (2026-11-14).
   - The workplans' statuses (#262 for the SMB plan's retirement; the index and the arXiv plan with
     this stage's PR); the handover.
   - O2-O4 put to the owner and answered (2026-11-14): O2 (b), O3 settled by the endorsement's
     timing, O4 (b).
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
   - **Done 2026-11-17:** read (Findings, below).
2. **The seed's part (D7).** `--data-seed`; the ten runs and two checks at `p` 13; the reading
   (the weights, the words, or mixed). A clear reading names the next probe: what in the weights
   (which layer's draw), or what in the words (which epochs').
   - **Done 2026-11-18:** mixed (Findings, below); the follow-up probe (306's and 310's weights with more
     words) after stage 3.
3. **The cost's scaling (D8).** The existence probe at `p` 17; the registration with its
   predictions and O4's rule if the owner takes it; the ladder; then three coordinates.
   - **The probe passed 2026-11-18** (4 of 4 at `p` 17); **registered 2026-11-18** (below).
   - **Done 2026-11-22:** it breaks at `p` 19 (Findings, below); the three coordinates not run; the width probe
     (window 64 at `p` 19 and 23) next.
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
6. **Findings** into paper 1's next version (O2), contribution.md, failure-kinds.md and the
   register; this plan retired, its leftovers to next-steps.md.

## Stage 1, registered (2026-11-14)

Registered before any of its runs, under the owner's direction to work through stage 1 ("work your way
through stage 1", 2026-11-14) and the delegation of D choices. Nothing below changes once a run has
started; a flaw found mid-batch is recorded and fixed in a new registered experiment.

- **The builds** (indrajala-studies, each its own PR): `told`, the matched partitions and `--arm matched`
  (#23); D3's sign test and cross-fitted cost, McNemar's exact test, the signed rank two-sided (#22);
  the readout (`paper_reading.py told`), the review's seed clustering as a probe, and paper_reading's
  probe path and machine vocabulary fixed (#24); the runner: `stone` at 70% and its venv (#25), its
  bundles' pins forced (#26), the crate at `edce2de` (#27), a spec part's own cell (#28).
- **The commit:** indrajala-studies `42c5771` (ml `0b17d22`), the crate `crate-edce2de` on every host
  (`.so` sha256 `f72612f402e8e08008ec3b1c305f7059d0b2839ac76d746ef55ff3f60de0519c`).
- **The targets and arms (D5), each target's three on one vocabulary:**
  - *Division at `p` 5*, the approximation claim's cell (`approximation`: two factors of 16 codes, reading
    the output, the default window 16 wide, 400 epochs, stop at the first certified step, no fork), on the
    vocabulary `sum matched`: `told-d5-quotient` (the answers alone), `told-d5-sum` (the sum),
    `told-d5-matched` (the sum's matched partition).
  - *Planted machines of 16 states*, the paper's cell (`paper`: two factors 32 wide of 12 codes, reading
    the output, the fork, the window 32 wide, 600 epochs, stop at the first certified step), on the
    vocabulary `planted matched`: `told-alone-<m>` (the answers alone), `told-planted-<m>` (the planted
    blocks), `told-matched-<m>` (their matched partition).
- **The matched partitions (D4),** fixed in the code and tested before any run: each has the
  approximation's block sizes, is no congruence, and with the answers tells exactly as many classes.
  Division's at `p` 5 (labels `0 1 2 3 4 4 3 3 3 3 1 0 0 0 4 1 1 1 4 2 4 2 0 2 2` over the states
  `A p + B`) tells 22 of 25, as the sum does; each machine's tells what its blocks tell (below).
- **The draws (D6), all fresh:** at `p` 5, seeds **800-839** in every arm (40 a arm). The planted machines:
  the first 25 `random-planted-q16-b4` seeds from 53 whose only nontrivial principal congruence is the
  planted one, **54-61, 64, 67-69, 71-78, 80, 82, 84, 85, 87** (53, 62, 63, 65, 66, 70, 79, 81, 83 and 86
  gain others; the rule reproduces T10r's draws in a test), each run with seeds **840 and 841** in every
  arm. No earlier test used these seeds or machines.
- **The classes told** (`modular_family_probe.py told`), of 25 states at `p` 5: the answers alone 6, the
  sum 22, its matched partition 22. Of 16 on the planted machines: the answers alone 4 on every machine;
  the blocks and their matched partition the same on each machine, 8-14, mean 11.0 (54: 11, 55: 11, 56:
  11, 57: 9, 58: 10, 59: 10, 60: 13, 61: 10, 64: 11, 67: 12, 68: 12, 69: 9, 71: 11, 72: 13, 73: 10, 74:
  14, 75: 8, 76: 11, 77: 10, 78: 13, 80: 10, 82: 13, 84: 11, 85: 12, 87: 9).
- **Feasibility** (information-flow.md, rows 1, 2, 3, 11, 14 and 19, the joint machine's row added with
  this registration):
  - *Division:* every output a function of the state (the matched partition too), so the joint machine
    has 25 states; codes 16 x 16 = 256, 10.2 times. The cap 280 = 256 + 25 - 1, the exclusion bound; the
    window 16 wide, the cell's (A1, A2, T1, T12 certified in it at `p` 5). Depth plus Chow's `k`: 3.
  - *Planted:* every output a function of the state, so 16 joint states; codes 12 x 12 = 144, 9 times.
    The cap 159 = 144 + 16 - 1, the exclusion bound; at 600 epochs the curriculum reaches it only if its
    steps average under 3.8 epochs, as in T10 and T10r, whose cell this is (the review's G7; the
    exclusion bound's rule (O4) is replaced only at stage 3). Depth plus Chow's `k` 4-7 on these machines;
    T10r's certified steps were 6-22. Window 32.
  - Every state reachable and every pair told apart (row 14) on every target, by construction (minimal,
    reachable machines; the final zero window, row 11).
- **The timing probe** (2026-11-14, studies at `4b8f94f`, the crate above; 3 epochs, seed 999, machine 53
  for the planted cell, not one of the draws; six runs at once a host): the `p` 5 arms 1.2-3.5 s an epoch
  on `stone` and 5.3-7.1 on `klip`, the planted arms 2.9-4.0 and 6.3-10.8; 55-71 MB a run at its peak.
  These are curriculum steps 1-2; later steps train longer words, so the plan's sizes stand as bounds.
- **Success, a run** (as the paper's D13): certified at the stop, recertified in both verdicts (the
  default and the strict, `paper_reading.py certify`), and its network long-tested (U1, S1 at 128, 256
  and 1,024 columns, `paper_reading.py long`) with no failure.
- **The tests, Holm over the five at 0.05** (`modular_family.TOLD_TESTS`, read by `paper_reading.py
  told`):
  1. *Information, division:* the matched partition against the answers alone, one-sided (the
     partition more often), McNemar's exact test over the 40 seeds.
  2. *Information, planted:* the matched partition against the answers alone, one-sided, the exact
     signed-rank test over the 25 machines' differences in successful runs (each 0 to 2).
  3. *Congruence, division:* the sum against its matched partition, two-sided, McNemar's exact.
  4. *Congruence, planted:* the blocks against their matched partition, two-sided, the signed rank.
  5. *Given against not given:* the blocks against the answers alone, one-sided, the signed rank (the
     review's G4).
  Each mean paired difference is reported with a percentile 95% bootstrap interval over its units
  (10,000 resamples, keyed).
- **The readings, each target apart** (`modular_family.told_reading`): *information* if its partition
  helps (test 1 or 2 holds) and the approximation doesn't beat it (3 or 4 doesn't hold); *congruence* if the approximation beats its partition (3 or 4 holds, the sum or the blocks
  the more often) and the partition doesn't help; *both*; *undecided* if neither holds, with each
  interval. If test 3 or 4 holds with the partition the more often, that is reported as such, outside
  the four.
- **Beside them, D3's cost measures (D2: registered beside the rate in stage 1, not in the family):** for
  each test, the sign test on epochs to a certificate over its paired runs (sided as the test); for each
  arm, the cost per certificate at a cross-fitted cutoff (the runs in seed order at `p` 5, machine then
  seed order on the machines), the cost as run and a bootstrap interval.
- **Expectations, not bars:** at `p` 5 the answers alone about 1 in 20 (A1's quotient), the sum 6-10 in
  20 (T1's 6, the approximation claim's 10); on the planted machines the answers alone about 3 runs in
  30 (T10's P1), the blocks about 13 in 50 (T10r's P2). None for the matched partitions: that is the
  question. With 40 seeds, McNemar's two-sided test detects only a large gap between the sum and its
  partition; *undecided* is a likely reading of test 3, and the intervals say how large a gap is left
  open.
- **Where:** the batch runner, its controller on `pyramidon`, workers on `klip` (7 slots, under its
  thermal guard) and `stone` (7 slots, its hours); the planted attempts first (the longest). Data in
  indrajala-studies' gitignored `data/window-recurrent/told/stage1/`, with a manifest; the readings
  (recertify, long tests) on `pyramidon`, the crate above first on PYTHONPATH.
- **The batch:** 150 planted attempts (the paper cell) and 120 at `p` 5 (the approximation cell), run to
  the end; then the readings, then the findings here.

## Stage 3, registered (2026-11-18)

**The existence probe (D8), before this registration:** the cover at `p` 17 in the `scaling` cell (the paper's,
its budget 46 epochs a unit of `p`: 782; studies #38), seeds 400-403, on `stone` at studies `210a1c9`: **4 of
4 certified** (both verdicts), at epochs 306, 318, 414, 519 (median 366) and steps 14, 15, 17, 26 (median 16),
38-72 minutes a run, peak memory 190-290 MB. Width 32 works at 289 states (the register's row 3). These four
runs are not in the ladder's data; their seeds are not reused.

**O4's coverage rule (the protocol's change, in this PR).** experiment-design.md section 1's exclusion bound
(`L >= m + q - 1`) is replaced, for every config registered from now on, by: **training's longest length
reaches at least 1.75 times the target's depth plus Chow's `k`** (the joint machine's deepest state's
distance from the start, plus the least `k` at which every pair of its states is told apart by a word of `k`
tokens; the register's row 15, made general). The multiple is read from paper 1's certified networks: their
certified step over depth plus `k`, the least ratio 1.75 (`p` 13, three networks at step 7, depth 3 plus
`k` 1), the rest 2.0 (s3, rq12, division at `p` 7 and 11) to 2.2 (s4, mtf4) and up. The exclusion bound
stays in the protocol as what it is, a sufficient condition, no longer a rule. The register's row 2 changes
with it.

**The ladder.**

| cell | `p` | states (joint) | codes a factor, joint | width | depth + `k`; the rule's length | budget (epochs) | seeds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `scaling` on `d17-family` | 17 | 289 | 50, 2,500 | 32 | 3 + 1; 7 | 782 | 500-519 |
| `scaling` on `d19-family` | 19 | 361 | 56, 3,136 | 32 | 3 + 1; 7 | 874 | 500-519 |
| `scaling` on `d23-family` | 23 | 529 | 67, 4,489 | 32 | 3 + 1; 7 | 1,058 | 500-519 |

The curriculum trains length 7 from its seventh step, within every budget (the probe's runs at `p` 17
reached step 7 at epochs 209-249 of their 782). Every cell can succeed: codes at least 8.5 times the
joint states a factor needs, width 32 measured at 289 states (the probe), the rule's length inside the budget.

**The outcome (D2):** the cost first, epochs to a certificate (strict verdict, the recertification's), a run
spent at its budget counted beyond it.

**The predictions (D8, written 2026-11-10, before any data at these sizes; not changed since):**

- **P1, the epochs:** at each `p`, the median epochs to a certificate lies between 20 and 30 times `p` (340-510
  at 17, 380-570 at 19, 460-690 at 23). Refuted at a `p` if its median (with censored runs beyond the budget,
  so a median beyond the budget when fewer than half certify) is outside the band. Each median's 95% bootstrap
  interval beside it.
- **P2, the step:** at each `p`, the median certified step lies between 7 and 14. Refuted at a `p` if outside.
  *Beside it, not changing it: the probe's four runs at `p` 17 had a median step of 16.*
- **P3, the coverage rule:** no network certifies before training reaches 1.75 times depth plus `k` (step 7
  here). Refuted by any certificate at step 6 or below (the multiple then too large; the rule is a feasibility
  bound, and a certificate under it says the bound is not needed).

No family correction: three predictions of a law, each read at each `p`; the readings are the law's, not a
test of a difference.

**D3's measures beside them:** the cost per certificate at a cross-fitted cutoff, in epochs, at each `p`
(stage 1's tool), with its interval; the certified rate at each `p` with its exact interval.

**The reading, fixed now:** *the law holds* if P1 and P2 hold at all three; *the epochs scale but not the step*
(or the reverse) if one holds at all three; *it breaks at `p`* the first `p` where both fail. Three coordinates
(D8's next) only if P1 holds at all three.

**The batch:** one `measure` batch, the three cells, 60 attempts, the longest first (`p` 23), on `stone` (6
slots, 60%, any hour) and `klip` (7 slots, thermal guard), controller on `pyramidon`; then `paper_reading.py`
`certify` and `long` (the long tests, as stage 1's), then this plan's Findings. Memory: about 290 MB a run at
`p` 17, planned at 600 MB at `p` 23 (klip 7 runs 4.2 GB within its 5.3). Time: at `p` 17 about 7-10 s an epoch;
at `p` 23 planned at 20 s, so a spent run about six hours; about a day in all.

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

### Stage 1, the matched controls (read 2026-11-17)

The batch ran 2026-11-14 08:19 to 2026-11-16 19:36 (270 attempts, every one ended); the readings
(`links`, `certify`, `long`, `told`) by 2026-11-17. Data and manifest: indrajala-studies'
`data/window-recurrent/told/stage1/` and `told/stage1.sha256`; the reading in `stage1/told-reading.txt`.

| target | arm | succeeded | registered expectation |
| --- | --- | --- | --- |
| division, `p` 5 (40 seeds) | the answers alone (`quotient`) | 0 | about 1 in 20 |
| | the sum | 18 | 6-10 in 20 |
| | the sum's matched partition | 5 | none |
| planted, 16 states (25 machines x 2 runs) | the answers alone | 11 runs, 8 machines | about 3 in 30 (T10's P1) |
| | the planted blocks | 8 runs, 6 machines | about 13 in 50 (T10r's P2) |
| | their matched partition | 9 runs, 7 machines | none |

The five tests, Holm over the five (mean paired difference, 95% bootstrap interval):

| test | units | difference | p | Holm |
| --- | --- | --- | --- | --- |
| information, division: matched over the answers alone (one-sided) | 40 seeds | +0.125 (+0.025 to +0.225) | 0.031 | 0.125 |
| information, planted: matched over the answers alone (one-sided) | 25 machines | -0.080 (-0.480 to +0.280) | 0.72 | 1 |
| congruence, division: the sum against matched (two-sided) | 40 seeds | +0.325 (+0.175 to +0.475) | 0.00024 | **0.0012** |
| congruence, planted: the blocks against matched (two-sided) | 25 machines | -0.040 (-0.360 to +0.280) | 0.88 | 1 |
| given against not given: the blocks over the answers alone (one-sided) | 25 machines | -0.120 (-0.520 to +0.280) | 0.75 | 1 |

- **The readings (registered rule):** division at `p` 5, **congruence**; the planted machines,
  **undecided**.
- **At `p` 5 the approximation is what helps, not what it tells.** The sum and its matched partition tell
  the same 22 classes of 25; the sum certified 18 seeds, the partition 5. Every seed the partition
  certified the sum certified too (802, 810, 830, 831, 837). The partition's own help over the answers
  alone (5 against 0) doesn't hold after Holm; its interval stays above zero.
- **On the planted machines nothing was detected.** Given the blocks didn't beat the answers alone (8
  runs against 11), nor did the blocks beat their matched partition (8 against 9). The arms succeeded on
  mostly different machines (only machine 60 in all three), so a machine's draw shows no constant
  difficulty in these counts. The answers alone did far better than T10's P1 suggested (11 in 50 against
  3 in 30), and the blocks worse than T10r's P2 (8 against 13 in 50).
- **What this changes in paper 1.** T10r's help from planted blocks was measured against *primitive*
  machines (no nontrivial congruence), a contrast that changed the machine as well as what was told.
  On the same machines, giving the blocks wasn't detected to help. Paper 1's claim narrows to the
  division family, where the congruence beats a partition that tells as much; whether planting a
  congruence alone makes a machine easier stays open.
- **D3's measures agree** (beside the rate, not in the family): epochs to a certificate, the sum beat
  the partition on 17 seeds and lost on 1 (sign test p 0.00015); the partition beat the answers alone
  5-0 (p 0.031); every planted comparison null (p 0.59-0.82). Cost per certificate at a cross-fitted
  cutoff, in epochs: the sum 335 (95% 224-621), the partition 1,833 (932-10,477), the answers alone none
  certified; planted 2,525 (816-13,128), matched 784 (497-3,324), alone 1,570 (855-4,404).

**Recorded beside the reading (nothing registered changed):**

- **A slip in the registration's text.** Machines 73 and 75 tell 3 classes with the answers alone, not 4
  as the registration says for every machine (the classes told by the blocks are as registered). It
  touches no test or arm; paper 1's version 2 says "3 or 4".
- **The readout's D3 lines** read every run as failed on the first `told` (a paper run's log carries
  the default verdict alone; the strict one is the recertification's). Fixed before those lines were
  read (indrajala-studies #34): a run's success is the rate's. The rate's tests didn't change.
- **The batch's conduct.** Seven attempts at `p` 5 (the answers alone, seeds 824-826 and 828-831) were
  stopped at `stone`'s window's end (07:00 on 2026-11-16, its registered hours) and run again from the
  start, as the runner does (`lost`, why `window`; the partial runs set aside on `stone`, not pulled): one
  run each is in the data. The same day the owner opened `stone` at any hour at 60% (6 slots, from 7); the
  controller's restarts for that left three stray `opened` events in the ledger.
  The long tests ran `modular_family_probe.py long-test`, the command
  `paper_reading.py long` runs, spread over `stone`, `klip` and `pyramidon` at studies `42c5771` on the
  runners (2.5 GB a test); two first runs on `pyramidon` ran out of memory and were run again
  (`long-tests/approximation.log` is the first one's traceback). All 51 networks were long-tested and
  passed.

### Stage 2, the seed's part (read 2026-11-18)

A probe (D7; it claims nothing). The batch ran 2026-11-17 15:19 to 18:39 on `stone` and `klip` at
studies `cb10f0a` (ml `0b17d22`, crate `edce2de`), the paper cell, up to 600 epochs at `p` 13; the
networks recertified in both verdicts (studies #37 taught the reading the `-words<k>` names). When the
check (plain 303) certified, the other four bad seeds were run plain too (2026-11-18 16:36 to 20:48, `klip`,
the same commit). Data: indrajala-studies' `data/window-recurrent/told/stage2/` and `told/stage2-plain/`.

| seed | paper 1, alone (ml `9ef332c`) | now, alone | now, its weights with a good seed's words | now, its words with a good seed's weights |
| --- | --- | --- | --- | --- |
| 303 | spent | **certified** (epoch 287) | certified (300's words) | certified (300's weights) |
| 306 | spent | spent | spent (301's words) | certified (301's weights) |
| 310 | spent | spent | certified (302's words) | certified (302's weights) |
| 314 | spent | **certified** (epoch 441) | certified (304's words) | certified (304's weights) |
| 315 | spent | **certified** (epoch 257) | certified (305's words) | certified (305's weights) |
| 300 (good) | certified (epoch 187) | certified (epoch 226) | | |

- **Outcomes, not only bits, are their code's.** Three of the five bad seeds (303, 314, 315) certify alone at
  today's code. Seed 303's two runs agree through epoch 1; the screen first differs at epoch 2, the training at
  epoch 5. Between the codes lie the library's changes since paper 1 (289 commits: the crate's kernels, which
  change the order of floating-point sums, and the literature-driven layers and optimiser options).
- **The reading: mixed** (D7's third outcome). Neither the weights nor the words carry failure across the five:
  - 306 fails in all three of its runs with its own weights, and its words certify under 301's weights: the one
    seed whose failure follows its weights.
  - 310 fails alone at both codes, but either half certifies with a good seed's other half: its failure is the
    pair's, neither half's.
  - 303, 314 and 315 fail only at paper 1's code.
- **What this doesn't say.** Not that today's code certifies more often: the five were chosen for failing, and
  paper 1's `p` 13 batch certified 15 of 20, so a fresh trajectory of a seed that failed once mostly succeeds at
  either code. That needs fresh seeds at both codes, paired and registered (not planned; stage 3 gives today's
  rate at `p` 17-23).
- **The next probe (D7: a mixed reading needs more pairs, registered then):** 306's weights with five more good
  seeds' words, and 310's with five (ten runs at `p` 13, a few hours). If 306's ten all fail, its weights carry
  failure, and the probe after names the layer's draw; if they mostly certify, failure is the trajectory's and
  nothing in the draw is chased. It waits for stage 3's ladder (D1's order; its reading bears on stage 4's pairs,
  not on stage 3). Until it is read, X's pairs (stage 4) share both seeds, as they do now. **Fixed 2026-11-22,
  before its runs:** the words of 307, 308, 309, 311 and 312 (paper 1's next five good seeds at `p` 13) for both
  306 and 310, the paper cell at studies `3bc06dd`, on `klip`.
- **The next probe, read 2026-11-23: failure is the trajectory's.** 306's weights certify with four of the five
  words (307, 308, 309, 312; steps 14, 11, 11, 10; 311 spent its 601 epochs), 310's with three (308, 311, 312;
  steps 14, 12, 14; 307 and 309 spent): 7 of 10, against paper 1's 15 of 20 at `p` 13. Not all of 306's fail, so
  by the rule fixed above nothing in the draw is chased. All 7 recertified in both verdicts and passed their long
  tests (U1 and S1 at 128, 256 and 1,024 columns, on `klip`). X's pairs (stage 4) may share both seeds or one;
  this probe gives no reason to prefer either.
  - **The shadow reading** (`formation_reading.py batch`, the population method's rules fixed before the data):
    6 times depth plus `k`, share below 0.999, stops none; 4 times, below 0.9, stops the three failures at step
    16 and loses none (1.08 times the certificates per epoch); 2.5 times, below 0.9, stops the same three at step
    10 (shares 0.70-0.84), loses none and saves 20% of the epochs (1.26 times).
  - Data: indrajala-studies' `data/window-recurrent/told/stage2-followup/`, run 2026-11-22 05:39-13:00.

### Stage 3, the cost's scaling (read 2026-11-22)

The ladder ran 2026-11-18 20:57 to 2026-11-20 22:53 on `stone` (6 slots; suspended 10:20 to 15:14 on
2026-11-20, its runs paused, none lost) and `klip` (7 slots) at studies `ead8601` (ml `0b17d22`, crate
`edce2de`), the `scaling` cell, 60 runs, peak memory 171-977 MB. Every certified network (24) recertified in
both verdicts; their long tests (U1 and S1 at 128, 256 and 1,024 columns, on `stone`): all 24 passed every case
(the last three, `d19-family-513`, `514` and `517`, on 2026-11-22). Read with
`paper_reading.py scaling` (studies #40). Data: indrajala-studies' `data/window-recurrent/told/stage3/`.

| `p` | certified (exact 95%) | median epochs (95%) | P1's band | P1 | median step (the steps) | P2 | P3 | cost per certificate, cross-fitted (95%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 17 | 11 of 20, 0.55 (0.32-0.77) | 564 (397 to beyond the budget) | 340-510 | refuted | 13 (10-25) | holds | holds | 1,014 (643-2,560) |
| 19 | 13 of 20, 0.65 (0.41-0.85) | 612 (521 to beyond the budget) | 380-570 | refuted | 18 (15-27) | refuted | holds | 981 (713-2,627) |
| 23 | 0 of 20 (0-0.17) | beyond the budget (1,058) | 460-690 | refuted | none | not read | holds | none certified |

- **The registered reading: it breaks at `p` 19,** the first `p` where P1 and P2 both fail. Neither "the law
  holds" nor the epochs' or the step's law alone. D8's three coordinates (run only if P1 held at all three) are
  not run.
- **P1 fails at every `p`, by its failures.** The certified runs mostly certify inside the band (17: 10 of 11,
  321-449 epochs, the eleventh at 678; 19: 8 of 13, 346-716); the median moves beyond the band because 9 runs at 17, 7 at 19 and all 20 at
  23 spend their budget. The cost per certificate (about 1,000 epochs at 17 and at 19) is more than a run's
  budget (782, 874).
- **P2 holds at 17 and fails at 19:** the certified step rises with `p`, 13 to 18 (the probe at 17 had 16).
- **P3 holds: the coverage rule is a floor, not the step.** No certificate before step 7; the earliest at step
  10, the medians 13 and 18, ratios of 2.5 to 4.5 over depth plus `k` (paper 1's least was 1.75). The rule stays.
- **The probe overstated `p` 17:** 4 of 4 there, 11 of 20 here.
- **How the runs fail.** Every failed run trained past step 22 (17: steps 22-29; 19: 25-36; 23: 29-49). At 23 the
  state share ended at 0.07-0.98 (median 0.68) and the minimised machine at 4 to 2,392 states against 529: some
  runs collapsed onto a few codes (two factors using 2 and 3 codes), others used most of their 67 codes without
  the codes settling into states. The codebook is not short: certified networks at 17 and 19 used 24-46 codes a
  factor of 50 and 56, about 1.3 to 2.7 a unit of `p`; at 23 that is 30-62 of 67. At 17, two failed runs reached
  a share of 1.0 with machines of 683 and 933 states against 289.
- **What grows and what doesn't.** The cell scales the codes (2.9 a unit of `p`) and the budget (46 epochs a
  unit), not the widths: the window and each factor stay 32 wide while the joint machine grows from 289 to 529
  states. The register's row 3 measured width at division 13 (169 states: 32 gave 5 of 6, 22 gave 3 of 6).
- **The next probe (the owner, 2026-11-20: "we should test p 23 @ width 64"):** the `scaling` cell with only the
  window's width at 64 (each factor 32 wide, the budget 46 epochs a unit of `p`), at `p` 23 and at `p` 19, four
  fresh seeds each (600-603), an existence probe (D8's rule; it claims nothing). If width 64 certifies at 23,
  a registered rung there; if not, each factor's width at 64 is the next. One run's first epochs are timed first
  (width 32 took about 32 s an epoch at 23 on `stone`). Stage 2's follow-up (306 and 310) runs beside it.
- **The shadow reading, fixed before those runs (the owner, 2026-11-22).** A survey of every curriculum run's
  log in the studies (studies #42's `formation_reading.py survey`, corrected by #43: 1,436 runs, 415
  certified, s3 to division) found every certificate at a state share of 1.0, and on the step over the
  target's depth plus Chow's `k` no run not formed by 6 times it certified later (0 of 537; 4 of 684 at 5, 19
  of 914 at 3.5). Found after the
  data, so not yet a rule: the width probe and stage 2's follow-up run without stopping, and
  `formation_reading.py batch` reads where three rules would have stopped each run: 6(d+k) with the share
  below 0.999, 4(d+k) below 0.9, and 2.5(d+k) below 0.9 (on the survey: 0, 8 and 37 of 415 certificates lost,
  1.17, 1.40 and 1.76 times the certificates per epoch; `research-notes/formation-stages-note.md`). Expected: the first stops no run that certifies. Its
  18 runs check the rules, they don't decide them; the population method's plan
  (`population-method-workplan.md`) registers their test.
