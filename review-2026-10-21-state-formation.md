# Contribution review of the state-formation strand (2026-10-21)

An internal assessment of option 1 as it stood on 2026-10-21, morning: the crucible's
crystallisation, the quasi-static cool (D29), the adaptive cool (D33) and the bounded handover
(D34), as reported in `state-formation-status.tex`. It was made before the adaptive cool's
existence probe (D33's probe), the bounded handover's probe (D34's probe) and the panel (4b) were
read. Novelty is "not found in our search". The current statement is `contribution.md`, rows 7-10.

Overall: the strongest new result is what the certified networks contain (proved approximations
and covers, found unprompted), not the method that makes them certify. The method is an engineered
combination of known parts, one close precedent (DOLCE's error-tied annealing) uncited until now.
The algebra finding may be the architecture's. Everything rests on two backdrops and on the seeds
the fixes were designed from.

| contribution | novelty | evidence | assessment |
| --- | --- | --- | --- |
| Learned factors as the target's approximations, proved, sometimes a cover (row 7) | not found; the decomposition side of machine discovery | 8 S3 and 15 move-to-front networks read exactly; not registered | the most original; its sharpest point is the contrast with Li et al. 2025 (transformers on permutations compute the sign first; no S3 network here holds it, they go through a point's stabiliser). Open: whether two factors of 8 codes steer it |
| Formation against conversion, one measurement (row 8) | moderate: probing for the target's state is common (Li et al. 2025; Allchin 2026 separates RL failures the same way) | strong: the abrupt snap destroying a formed state (S4 0.98 to 0.25) | the diagnosis that made earlier remedies readable; as much P1's as a new paper's |
| Resets form from the whole distribution, groups need a seed (row 9) | low as stated generally: expressivity draws a related split (flip-flops against parity, Sarrof et al. 2024; non-solvable groups beyond fixed depth, Liu et al. 2023 and Merrill et al. 2024, which S3, being solvable, escapes); seeding is Elman 1993, disputed by Rohde & Plaut 1999 | thin: few runs, two backdrops differing in more than the algebra | Merrill et al. report single-layer RNNs learning group word problems at every length; Allchin 2026 finds permutation automata mostly unlearned under RL. Our mechanism (no synchronising word, so a wrong snap persists) is the snap's, so the claim should be narrowed to a snapped recurrent state, or a plain-RNN control run |
| Conversion as crystallisation: per-factor melting points, the coupling window, the clock held on the screen (row 10) | modest: Das & Mozer 1993 anneal a soft clustering of an RNN state with the temperature tied to the error (beta proportional to 1/error), a closed-loop schedule; Agustsson et al. 2017 tie theirs to the soft-hard gap; Rose 1998; Huang et al. 1986 | 8 of 8 on the six seeds the fixes were built from; move-to-front-4 seed 3 under three shapes | the combination and the certificates without the commitment term are ours; `p` is unmeasured until fresh seeds |
| The heat capacity's hump over the cascades | low: Rose's prediction confirmed in a new setting | three certified runs, passive logging | supporting; its use is pacing the adaptive cool |
| The adaptive cool (D33), the bounded handover (D34) | engineering | in flight | nothing claimed until read |

Closest near-precedent for the papers as a whole, noted here for P1's related work: Brandoit et
al. 2026 (NFSM) learn exact transition tables of groups and monoids with a nonaffine scan-
compatible cell, correct beyond the tested lengths. Their check is of the learned table, not a
certificate against the target from every reachable state; P1 should say how the two differ.

## What would raise the contribution most

1. **The panel (4b) on fresh S3 seeds 8-15:** the first measure of `p`; 8 of 8 measured the fixes
   on their own failures.
2. **At the panel's registration, before its data:** which approximations appear and how often,
   the sign among them (row 7); a plain-RNN control on S3 without a seed (row 9); a DOLCE-style
   error-tied schedule as an arm (row 10), which reopens the two-arm design (D31-D34) and is the
   owner's call.
3. **The status note:** cite Das & Mozer and Agustsson as the quasi-static cool's precedents; narrow
   the algebra claim to a snapped state; cite Merrill, Sarrof, Elman, Rohde & Plaut and Li et al.
4. **Framing:** a third paper is premature. Row 7 strengthens the common frame ("a proved machine,
   and often a proved decomposition of it"); row 8 strengthens P1.

Papers fetched for this review: indrajala-literature #7 (Merrill 2024, Sarrof 2024, Li 2025, Elman
1993, Rohde & Plaut 1999); Das & Mozer, Agustsson, Rose, Huang/Romeo, Allchin and Brandoit were
already in the collection.
