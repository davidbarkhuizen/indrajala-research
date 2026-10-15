# Contribution review of both papers (2026-10-15)

An internal assessment, made before the registered division comparison (stage 5), E2 and E2b were
read; to revisit in the critique the publication route calls for. Overall: a rigorous methods
contribution (proof-based evaluation, registered claims, manifests) with one potentially
significant idea; limited for the wider field by scale and breadth (small machines, one
architecture, few seeds where newest, base-3 toy tasks).

## P1 (`snapped-window-recurrence.tex`)

| contribution | novelty | evidence | assessment |
| --- | --- | --- | --- |
| The certificate as an instrument (complete over 531k windows, outputs and states, near ties branched, hundreds of networks) | moderate (reading the machine off a snapped state: Zeng et al. 1993) | strong | P1's best contribution, as a method for studying learning; every other finding is visible only through it |
| Sampled tests overstate success (328,000 cases to 1,024 columns passed, provably wrong at 12) | low as a claim (Weiss et al. 2018), high as evidence | strong (complete) | quotable; relevant to length-generalisation work judged on samples |
| More codes buy test-passing wrong machines (working rate rises with m, certified rate doesn't) | not found | moderate (20 seeds a cell) | non-obvious; undersold in the draft |
| Certify each step, stop at the first proof; training destroys proved networks | moderate | good | practical; P2 strengthens the destruction |
| The exclusion bound as a design rule | low (Moore 1956) | good | methodology, not a result |
| The design | low-moderate (block-recurrent and memory transformers, Rational Transductors) | good | E6 shows the transformer isn't needed at k 1 |

Critical gap: E2 (continuous state) and a plain recurrent baseline (now E2b, D38 of the claims
workplan). Reviewers' first question.

## P2 (`certified-modular-division.tex`)

| contribution | novelty | evidence | assessment |
| --- | --- | --- | --- |
| Certified 25- and 49-state product machines from answers only | not found (extracted machines in this line have a few states) | good at p 5 (11), thin at p 7 (1 of 4) | P2's strongest empirical result; small in absolute terms |
| Training on a cover of the target machine | the framing is new (homomorphic images from automaton decomposition); the mechanism isn't (Caruana's eavesdropping; Dan et al. 2022's state supervision) | screens 5/8 vs 0/6; stage 5 decides | with the full cover the outputs determine the state, so close to Dan et al. |
| One approximation without a cover suffices (quotient with the sum, 2 of 2, no faster to distinguish states than the quotient alone) | potentially the most original finding in either paper | weak (2 seeds, no control) | needs the AB control and 20 seeds |
| An enforced factorisation blocks learning | moderate | weak (2 seeds a cell) | a useful negative result; a section, not a headline |
| Collapse past a solution, at scale | low as a phenomenon (transient solutions, Adam's late instability, index collapse) | strong as observation | a curiosity until explained or prevented |

## What would raise the contribution most

1. E2 and E2b (running, 2026-10-15).
2. The approximation claim registered: target alone, with one approximation, with the cover, with
   AB, 20 seeds each at p 5.
3. A second composite task whose decomposition is a cascade: the running affine map mod p (chosen
   with the owner); if one approximation helps there, the idea generalises beyond two counters.
4. A fix for the collapse (chosen to come first), then division at p 11 (121 states) on `jebel`.

Venues: P1 to LearnAut or TMLR once E2 is in; P2 a workshop paper now, a TMLR paper with 2 and 3.
