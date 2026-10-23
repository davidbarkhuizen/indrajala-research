# The research programme's evolution (audit, 2026-10-23)

**Status: a dated review, deliverable 1 of the programme audit** (indrajala-ml
`docs/workplans/programme-audit-workplan.md`, #953). The owner's request: "a summary document(s)
covering the evolution of the research programme". Its companions:
[`review-2026-10-23-programme-reasoning.md`](review-2026-10-23-programme-reasoning.md) (logical
inconsistencies, gaps and bad assumptions) and
[`review-2026-10-23-programme-findings.md`](review-2026-10-23-programme-findings.md) (the numbered
findings). Written from the papers, the research notes, `contribution.md`, the protocols, the
workplans (live and retired), the study scripts' findings and indrajala-ml's git history (about 330
commits since 2026-10-08). Decision IDs are given as their short label, then the ID. Registered
probes still running at the time of writing (the deadline's completion (D67) and the reheat against
restarts (D63)) are described, not read.

## In one paragraph

The research started on 2026-10-10 as a side study of a CPU neural-network framework: the smallest
transformer that adds base-3 numbers. Within two days the question became *length*: a fixed-depth
network cannot carry at any distance, so the owner replaced length generalisation with a
**window-recurrent network whose state is snapped to learned codes**. That made every trained network
a finite-state transducer, and from 2026-10-13 a **certificate** could prove it equal to the target at
every length. The certificate reshaped the work. It showed that sampled tests overstate success, and
it led to the exclusion bound, to registering claims before data, and to stopping at the first proof.
Two papers followed: P1, the method on 3-5 state machines, and P2, product machines of 25-121 states
learned by training on the target's **approximations** (2026-10-15 to 10-17). Reframed on 2026-10-17
as *learning finite-state transducers with proof*, the programme tried non-arithmetic machines. Both
group and reset machines failed at 120 states, and random machines above about 12. On 2026-10-19 its
long-standing goal was written down: **machine discovery**, unknown machines found from behaviour
and known structure. On 2026-10-20 the owner abandoned every open plan for one strand,
**state formation**: forming a state and keeping it when the codes take over. Over four days that
strand turned an annealed snap into a crystallisation method: crucible, quasi-static cool, then a
fully continuous profile with an answers-only stop and the margin stop. Then came a statistical
reading (a parallel batch; restarts as Las Vegas runs) and the batch runner. Today the method
certifies about 3 in 5 fresh runs on S3 and move-to-front-4, and none of 10 on S4 and the random
machines. Every failure ends in what the notes call a freeze. The two papers have not changed since
2026-10-17.

## Phases

| # | dates | question | what changed it | result | where |
| --- | --- | --- | --- | --- | --- |
| 0 | to 2026-10-10 | (a CPU NN framework: layers, Rust crate, bit parity, benchmarks) | the owner's interest in a network that adds | the machinery every later study runs on: deterministic, single-threaded, bit-identical across machines | indrajala-ml README, measurement.md, rng-audit.md |
| 1 | 10-10 to 10-12 | the smallest network that adds `n`-digit base-3 numbers | carries fail over distance; fixed depth can't reach any distance | 2-3 layer column transformers at `d` 6 add at `n` 4 and 6; length generalisation planned, then terminated by the owner (10-12) | adder-findings.md §1-2; `git show 8990f74:docs/addition-study-workplan.md` |
| 2 | 10-12 to 10-13 | can a recurrence along the columns add at any length? | the window-recurrent adder (milestone A) | 45 of 90 runs work to 64 columns; the seed decides, not the cell | adder-findings.md §3 |
| 3 | 10-13 to 10-17 | what is that result, and why? (the claims C0-C8, E1-E8) | the certificate (10-13); E7's impossible cells; E8's memorising | sampled tests overstate (2 provably wrong networks pass 64 columns); the exclusion bound (10-14); experiment-design.md (10-14); the snap is what extrapolates (E2, E2b'); more codes buy test-passing, not correct, networks (E3) | window-recurrent-report.md; P1 |
| 4 | 10-14 to 10-18 | can it learn modular division (25-121 states)? | a factored state fails (C9); outputs of approximations succeed (10-15) | division certified at `p` 5 (13 of 20 registered), 7, 11 (121 states); one approximation suffices (A1-A3, 10-17); the collapse past a solution and the fork; the snap wall refuted, the certificate guard on replays | P2; `git show e45944e:docs/division-workplan.md` |
| 5 | 10-17 to 10-19 | does the method need arithmetic? where does it stop? | the transducer framing (10-17); the general algebras; the division ladder | S3/S4/move-to-front-4 certify at round 1; random machines only to about 12 states (set aside 10-18); 0 of 12 at 120 states for both Krohn-Rhodes extremes; division fails at 169, cured by a 32-wide window (W1, 5 of 6); the three bottlenecks, then the failure kinds; the goal written (10-19); the feasibility register (10-19) | transition-and-output-paths.tex; failure-kinds.md; machine-discovery.md; information-flow.md |
| 6 | 10-20 | why do states fail to form? | the owner abandons all plans for the literature's options, one at a time | the annealed snap's first panel void; heat-hold-cool; the gradual handover (first certificate, mtf-4 seed 3); groups need a seed (the crucible); the quasi-static crucible 8 of 8 on S3's design seeds | state-formation-workplan.md D1-D30; state-formation-status.tex |
| 7 | 10-21 | is the reasoning sound? | two reviews in one day; the target out of the loop | the answers-only stop (D35); one success definition (D41); the exact state bound (D43); the coupling probe refutes "no handover needed"; the core matrix registered then set aside; the owner's continuous crystallisation (D48) | the two 2026-10-21 reviews; D35-D54 |
| 8 | 10-22 | how often does the method work on fresh seeds and new machines, and why do the rest fail? | fresh seeds; the margin; the freeze; restarts | the fresh-seed matrix refuted as registered on S3 (7 of 16), then the margin stop (D59); every failure frozen; paced coupling no better (D61); the order-biased cool set aside on its stage 0 (D65); restarts as Las Vegas runs (Luby); the batch runner built | continuous-crystallisation.tex; freeze-and-restarts.tex; batch-runner-workplan.md |
| 9 | 10-23 | what is the method's rate, timed fairly? | epochs, not wall-clock, as the time axis | the fresh-seed rate (D64) 7 of 12 on the ordered machines, 0 of 10 on the rest; three runs cut by the wall clock; the deadline's completion (D67) registered; the research documents move to indrajala-research | D64, D67; experiment-design.md §1 |

## The phases in more detail

### 0. The framework (to 2026-10-10)

indrajala-ml began as a from-scratch neural-network framework on the CPU, with numpy, pure-Python
and Rust backends kept bit-identical, a measurement discipline for timing (`ab.py`, tiers, the
golden run) and a roadmap of transformer primitives. None of it was research, but the research
inherits three of its properties: runs are deterministic and reproduce exactly, across machines (C0:
15 of 15 reruns byte-identical); every number has a manifest; and the owner works by written
workplans with settled decisions, each option given its pros and cons.

### 1. The smallest adder (2026-10-10 to 10-12)

A calibration and a 619-run sweep found the smallest column transformers that add fixed-length
base-3 numbers. What failed was the carry over distance. A fixed-depth network must find a column's
deciding column at any distance, which bounded position codes cannot give. A length-generalisation
plan was written, read against the literature, and **terminated by the owner on 2026-10-12** in
favour of recurrence. This was the first redirection, and the first time the owner chose a structural
answer over tuning.

### 2. The window-recurrent adder (2026-10-12 to 10-13)

A small transformer reads a window of `k` columns and hands a state, snapped to the nearest of `m`
learned codes, to the next window. In a 90-run matrix, 45 runs worked to 64 columns after training
on at most 3 windows. The seed decided, not the cell, and failure was mostly all or nothing.

### 3. The claims and the certificate (2026-10-13 to 10-17)

The owner asked for the result to be substantiated. The claims workplan registered C0-C8 with their
refutations and fixed the statistics: Wilson, Fisher, Cochran-Armitage, Mann-Whitney and Holm, all
implemented by hand. **Its decisive tool was the certificate (E1, 2026-10-13).** Because the state is
snapped, the trained network is a Mealy machine. Walking it from every reachable code over every
window, with near ties branched both ways, proves it equal to the target or yields a counterexample.
The certificate refuted the sampled notion of "works": 2 networks passing every test to 64 columns
were provably wrong, and one of them passed 328,000 long-test cases. From then on "works" meant
"certified".

The phase also produced the rules the programme still runs on:
- **E7 → every cell must be able to succeed.** Division mod 7 was run with 32 codes for a 49-state
  machine.
- **E8 → the exclusion bound.** 37 of 40 modular-sum runs memorised below `m + q - 1`.
- **experiment-design.md (2026-10-14):** claims before data, existence first, probes before long
  runs, short focused experiments.
- **Certify each curriculum step and stop at the first proof.** E8c went from 1 of 40 to every rung
  certifying.

E2 and the plain-recurrence repeat (E2b') showed that the snap is what extrapolates: 0 of 20
continuous runs against 8 of 20 and 20 of 20 snapped at 1,024 columns. E5 found that failing runs
take wrong transitions among visited states, not unvisited states. A side question (2026-10-13) asked
what a network-machine would need to factor integers. It gave a note and a large workplan for a
tape machine with certified controllers, neither taken up since.

### 4. Division and the approximations (2026-10-14 to 10-18)

Modular division's state is two counters, so the owner first gave the network one codebook per
counter. That enforced factorisation failed outright (C9, C9', C9''): even one counter could not be
learned while its pooling read the tokens before the state. What worked (2026-10-15) was a *training
signal*: the outputs of the target's homomorphic images (the running sum and difference), answered
by query tokens beside the quotient, with the poolings reading the window's output. Registered at 20
fresh seeds it gave 13 of 20 against 1 of 20. The approximation claim (2026-10-17) separated one
approximation, the sum (10 of 20), from an equally distinguishing non-approximation, the product (0
of 20). Division then certified at 49 and 121 states.

Two other threads ran alongside. **The collapse past a solution**: proved networks destroyed by
further training. Its mechanism was read off batch by batch (1-3 transitions flipped, then Adam's
amplification). It was met by stopping at the first proof, by a fork that restores and halves the
rate, and by the certificate guard, which held the proof in 10 of 10 replays from one network. **The
snap wall**, an asymmetric margin loss, was refuted and paused (2026-10-16).

On 2026-10-15 the single paper split into P1 (the method) and P2 (division). On 2026-10-17 both
were reframed, at the owner's choice, as *learning finite-state transducers from examples, with
proof*. The publication route was agreed on 2026-10-14: an internal critique, a datapack, a
preprint, then a venue. **Both papers' last substantive edits are 2026-10-17.**

### 5. Beyond arithmetic, and where the method stops (2026-10-17 to 10-19)

The general algebras compared, over one state space, the word problem of `S_n` (a group),
move-to-front (aperiodic) and a random machine, at 6, 24 and 120 states, in division `p` 11's cell.
- **Round 1:** groups and move-to-front certified; random machines did so only to about 12 states.
  Two retention remedies (consolidation, longer words) and the restored best step all certified 0 of
  6 on random-q16-0, and **random machines were set aside on 2026-10-18**.
- **Round 2** (120 states): 0 of 12 for both extremes.
- **The division ladder:** the edge lay between 121 and 169 states, not caused by the budget or the
  factors' width. At 169 states the nearest failure had an *exact* transition function and answers
  its features couldn't linearly separate. A 32-wide window (W1) certified 5 of 6. Window branches,
  one path per consumer, were built and not adopted (harm on S4).

This phase produced the programme's maps:
- **The three bottlenecks**, renamed the **failure kinds** on 2026-10-21: formation, conversion,
  extra codes and answer separation.
- **"One code, one state"** as their common measure.
- **The feasibility register** (`information-flow.md`).
- **The goal** (`machine-discovery.md`, 2026-10-19), recorded as the aim "from the inception": stages
  A-F, from reliability through verification tools, hidden targets and queries to a real system.

Remedies for the failure kinds ran in parallel through the evening of 2026-10-19: the commitment
off early, a thermostat, annealing as built, the answers' own branch, keeping the best machine, and
counterexample training. Some moved a seed or two; none was clean.

### 6. State formation: the annealed snap becomes a crystallisation (2026-10-20)

**On 2026-10-20 the owner abandoned all planned work** and set one plan: take the literature
review's four options one at a time, each understood, built, tested on a panel, then accepted or
rejected. Option 1, annealing the snap, was rebuilt by the owner's physical picture over one day,
probe by probe:
- **The void panel (D13):** the anneal never ran.
- **Heat, hold, cool (D15-D24),** then the **gradual handover (D25)**, which gave the method's first
  certificate on move-to-front-4.
- **Seeded crystallisation (D26, the crucible):** groups need their state seeded on short words.
- **The quasi-static crucible (D28-D30):** 8 of 8 on S3, on seeds its fixes were designed from.

The day also produced the **formation/conversion distinction** (`state-separation`) and the
**approximations reading**: the certified networks' factors are the target's own homomorphic images,
sometimes a cover, found without being given.

### 7. Two reviews and a restructure (2026-10-21)

A reasoning review (morning) and a consistency review (afternoon) found two problems: the target
sat in the training loop, and the programme's rules contradicted its practice. They led to:
- **The answers-only stop (D35):** the run stops on its own answers within a state bound; the
  certificate only judges.
- **One success definition (D41).**
- **An exact state bound (D43).**
- **The coupling probe (D38)**, which refuted "no handover needed".
- **The panel's design (D36-D40).**

The panel's cost (5.5-27 days a run for the 120-169 state machines) led to a cheaper core matrix
(D46), registered at 16:30. That evening the owner set it aside, unlaunched, and asked for **every
switch of the method made continuous, all at once** (D48-D53). The continuous probe (D54) gave S3 6
of 8 on design seeds and the crucible's first move-to-front certificate.

### 8. Fresh seeds, the margin and the freeze (2026-10-22)

**The fresh-seed matrix (D55)** refuted its S3 bar as registered (7 of 16). Most of its losses were
networks right at the strict snap ratio but not with near ties branched. A target-free count of
"split ties" separated them on that data, and the **margin stop (D59)**, re-run on the same seeds,
gave S3 11 of 16 and move-to-front-4 7 of 8. The new backdrops were poor: S4 1 of 3, random-q12-0 1
of 4, random-q16-0 0 of 4.

Offline readings found that **every failure ends frozen**: the cool's clock is held at zero for
hundreds of epochs. Several attempts to explain or fix the freeze came to little:
- **The order-biased cool (D65):** set aside on its own stage 0.
- **The paced coupling (D61):** one rescue in six per arm.
- **The two-phase cool (D66):** reshaped to follow the reheat.

A same-day literature review read the freeze as the known halt of an equilibrium-gated schedule.
It read restarts as exact for the method, since a certified run is a Las Vegas run (Luby et al.
1993), and estimated a cost per certificate about 3.5 times lower with fresh-seed restarts at a
cutoff. **The reheat against restarts (D63)** was registered to compare the two escapes. The **batch
runner** (a controller on `pyramidon`, socket-connected workers) was planned and built the same day.

### 9. The rate, in epochs (2026-10-23)

**The fresh-seed rate (D64)**, registered before its data, read 7 of 12 on S3 and move-to-front-4,
between its bars, and 0 of 10 on S4 and the random machines. Three of its failures, and seven of the
reheat probe's (D63) runs, had been stopped by the 690-minute wall-clock budget on a loaded machine.
**The owner made epochs the binding budget and the time axis.** Every reading was re-read in epochs,
and **the deadline's completion (D67)** reruns the cut runs to their epoch budget. The research
documents (notes, protocols) moved to this repository the same day. The owner's direction is to wrap
up the current experiments, then run larger serial experiments on the batch runner.

## Through-lines

**The question narrowed and the goal widened.** The question went from "the smallest adder" to "an
adder at any length", then "a learned transducer, proved", then "how far it scales", then "why
states fail to form", then "a method's success rate per fresh seed". Meanwhile the stated goal grew
to discovering unknown machines (stages A-F). Since 2026-10-20 all the work has been in stage A
(reliability) on machines of 6-24 states. Stages B-F, and the 120-169 state tier the papers had
reached, are untouched.

**The rules accreted from failures, each dated to the experiment that taught it:**
- every cell feasible (E7, 10-13);
- the exclusion bound (E8, 10-14);
- claims before data and no settings changed (10-13/14);
- existence first, probes first (10-14/15);
- the window's width as a capacity bound (10-19);
- the crucible's feasibility row (10-21);
- the target out of the loop (10-21);
- path dependence and adoption by fresh-seed rates only (10-22);
- finish planned work before planning more, and run registered probes to their end (10-22);
- epochs as the time axis (10-23).

The discipline is real: every probe since 2026-10-20 has a header with expectations written before
its data, and several plans were set aside on their own stage-0 criteria. The reasoning document
lists where practice and rule part.

**The method was rebuilt constantly.** In the state-formation strand alone, 67 decisions in four
days: annealing, then crystallisation, then continuous crystallisation, then the margin stop, then
escape by reheat or restart. Its own acceptance gate, the panel (D11, D12, then D40), never ran.

**Physical analogies drove the design.** Crystallisation, melting, quasi-static cooling, glass and
kinetic arrest came largely from the owner's picture. Rose's deterministic annealing is the one part
where the analogy is literal. The later readings (heat capacity, constant thermodynamic speed, the
freeze as a glass) are analogies with literature behind them, not measured equivalences.

**The pace was very high.** About 20-35 merged PRs a day; probes launched while earlier ones were
still running; three rules added in two days to keep the record straight (finish planned work
first, no deviations from early peeks, epochs). Much of what the findings list as stale or
inconsistent is a by-product of that pace.

## Where it stands (2026-10-23)

- **Papers:** P1 and P2 are drafts from 2026-10-17. P2 doesn't yet carry the 169-state result (W1).
  Neither has had the critique, datapack or preprint the publication route lists.
- **The method:**
  - **Ordered machines:** S3 and move-to-front-4 certify on about 3 in 5 fresh seeds (D64, 7 of 12;
    undetermined until D67's three completions).
  - **The rest:** S4 and the random machines certify 0 of 10 on fresh seeds, and 2 of 21 across the
    continuous cell's probes.
  - **The 120-169 state tier** is untried under the method (too slow on today's hardware).
  - **The freeze:** every failure ends frozen. The reheat (D63) and restarts are the candidate
    escapes, with D63 still being read.
- **Infrastructure:** the batch runner, with stage-4 live checks and stage 5's first registered
  batch to run.
- **The goal:** stage A is incomplete; stages B-F are unstarted (the answers-only stop is the only
  piece of stage B in use).
