# Workplans

The research programme's workplans: studies, probes and the papers, where decisions are settled and
findings registered and recorded. They moved here from indrajala-ml's `docs/workplans/research/` on
2026-10-30; their history before that is in
[indrajala-ml](https://github.com/davidbarkhuizen/indrajala-ml)'s git. Code and data paths in them
(`scripts/...`, `indrajala_ml/...`, `tests/...`, `data/...`, `rust/...`) are indrajala-ml's.

A workplan is retired (deleted) once every stage and decision is resolved (paper 1's, on 2026-11-03:
`git show 0d1aaef:docs/workplans/paper-workplan.md`; the certificate note's on 2026-11-06, once both records were published: doi:10.5281/zenodo.23972277 and doi:10.5281/zenodo.23972256, read it at its parent commit); its leftovers move to
indrajala-ml's [next-steps.md](https://github.com/davidbarkhuizen/indrajala-ml/blob/main/docs/next-steps.md).
The library and infrastructure workplans stay in indrajala-ml.

| workplan | state |
| --- | --- |
| [what-is-told-workplan.md](what-is-told-workplan.md) | **the programme's order since 2026-11-10** (the owner, after [the programme review](../../review-2026-11-10-programme-review.md): "re-frame the planned work in this light"): whether being a congruence matters beyond what an output tells of the state (the matched controls), what in a seed fails a run, the cost's scaling, then crystallisation's A/B, discovery controlled against a classical learner, then W8; drafted 2026-11-10 (D1-D10; O1 resolved; O2-O4 the owner's, open); nothing built; stage 1's builds next |
| [nes-one-network-workplan.md](nes-one-network-workplan.md) | how far one network can take Super Mario Bros, on tiles; gated on 1-1; detailed through the gate 2026-11-05; the owner's go (O1) 2026-11-05; stages 0-2.2 done (the level table, 2026-11-06), 2.3 (the vector runner) next; the conv network's first 1-1 probe ran to the cap (greedy 89-93, sampled to 82), and the owner switched to the machine policy (O3, 2026-11-08) |
| [smb-machine-policy-workplan.md](smb-machine-policy-workplan.md) | a sub-plan of the NES plan's (O3): a snapped recurrent policy, exactly a finite-state machine, that clears 1-1 under sticky actions, read off and minimised; drafted 2026-11-08 (D24-D31); M1-M3 done; M4 (the control) failed, the policy never used the cue; paused after M4 by the world-model plan (its D11) |
| [smb-world-model-workplan.md](smb-world-model-workplan.md) | motion control from a world model, SMB as the simplest platform scroller (the owner's picture, 2026-11-08): an exact visual organ, then self, a world model, play, control and the level; final (2026-11-08): W0's literature read and the plan corrected against it, D1-D3 the owner's, D4-D13 decided under delegation; crystallisation left out for now (O1); W0-W2.3′ done (objects closed under D15); **held 2026-11-10** (the told plan's O1): W2.4 (events; planned, nothing built) waits for that plan's stages 1 and 2, W8 for its stage 5 |
| [nes-rust-emulator-workplan.md](nes-rust-emulator-workplan.md) | the NES plan's stage E in detail: a Rust emulator for SMB, bit for bit with FCEUmm (O3), then batched; E1-E6 done (E5 under the parity method, closed 2026-11-07 with D34's power-on phase, which fits Mesen too); the pixel mode and viewer done; the DMC (E10) done; the console (`nes-console`) done; its parity, pixel, sound and console sub-plans retired 2026-11-07; E7 next |
| [arxiv-posting-workplan.md](arxiv-posting-workplan.md) | paper 1 and the certificate note on arXiv (Brandoit's suggestion): D1-D7, O1 (a personal endorser); drafted 2026-11-07; A1-A3 done (checks, packages, the submission sheet); A4, the owner's submission, next; whether paper 1's waits for the told plan's stage 1 is the owner's (that plan's O3) |
| [post-paper-retests-workplan.md](post-paper-retests-workplan.md) | after paper 1: crystallisation (X), then branching and depth; the owner (2026-11-08): next after the machine policy, or sooner if it gets stuck; **since 2026-11-10** X is the told plan's stage 4 (its cost measures beside X's paired test), and B and L wait for that plan's stage 2 (the seed's part), then X |
| [incremental-reheat-workplan.md](incremental-reheat-workplan.md) | stage 0 read; the build and its probe after paper 1 (D9), X's second arm declined (D8); the owner (2026-11-08): next after the machine policy, or sooner if it gets stuck; since 2026-11-10 with X, the told plan's stage 4 |
| [state-formation-workplan.md](state-formation-workplan.md) | option 1 worked to a decision (the method); options 2-4 shelved (D31) |
| [general-algebras-workplan.md](general-algebras-workplan.md) | rounds 1-2 done; the fork's trigger and the guard to tune here (stages 5-7); paused since 2026-10-20; kept paused by the owner 2026-11-03 (the programme audit's F29) |
| [arbitrary-length-addition-workplan.md](arbitrary-length-addition-workplan.md) | a high-level plan; paused since 2026-10-20; its alignment questions (P3, P8) moved to the numeral reader; kept paused by the owner 2026-11-03 (the programme audit's F29) |
| [numeral-reader-workplan.md](numeral-reader-workplan.md) | the numeral reader (problem 1 of [numerals-and-operators.md](../research-notes/numerals-and-operators.md)); drafted 2026-11-02, R0 (literature) first |
| [factorisation-machine-workplan.md](factorisation-machine-workplan.md) | a high-level plan; paused since 2026-10-20; kept paused by the owner 2026-11-03 (the programme audit's F29) |
