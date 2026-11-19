# arXiv submissions: paper 1 and the certificate note

The sheets for the owner's two submissions (the arXiv plan, `docs/workplans/arxiv-posting-workplan.md`,
stage A3). Each field below is pasted as it stands. Paper 1 goes first; the note after paper 1 is announced
(D1).

## The packages

`make arxiv` builds both from their release tags into `arxiv-packages/` (gitignored), checks that each
compiles alone as arXiv will (`pdflatex` twice, no `bibtex`), and checks that its text equals the Zenodo
PDF's, word for word. The packages are byte-reproducible; paper 1's rebuilt at version 2 on 2026-11-19, the note's
unchanged since 2026-11-07:

| document | tag | upload | SHA-256 |
|---|---|---|---|
| paper 1 | `paper1-v2` | `arxiv-packages/paper1/learning-transducers-with-proof.tar.gz` | `887eae46c57370a3cf3f46d5a57610b73805782e27b734c99de66fad88f899ff` |
| the note | `certnote-v1` | `arxiv-packages/certnote/certificate-method.tar.gz` | `f917f07e6792dbc9cda961139c3705c05c7ffec74373be657b595760ede11c3e` |

## The steps (the owner's)

1. Register at <https://arxiv.org/user/register> (name: David Barkhuizen; the email the owner wants public
   correspondence on).
2. **Start a new submission** for paper 1: licence **CC BY 4.0** (D4), primary archive **cs**, category
   **cs.LG**. arXiv then emails an **endorsement request** with a six-character code (since 2026-01-21 a
   new submitter needs a personal endorser, O1).
3. **Ask one endorser, with the code** (draft below): Brandoit first. If arXiv tells him he can't endorse
   in cs.LG (his CS paper, arXiv:2609.32447, is under arXiv's three-month floor), ask whom on his team can.
4. Once endorsed: upload the `.tar.gz`; arXiv compiles it; **check its PDF** against
   `arxiv-packages/paper1/learning-transducers-with-proof.pdf` (21 pages); fill in the metadata below; add
   the cross-list **cs.FL** (D3); submit.
5. After paper 1 is announced, the note the same way (no new endorsement needed in cs.LG). Two new
   submissions a month is arXiv's limit; these are two.
6. Send me both arXiv IDs (stage A5).

## Paper 1

- **Title:** Learning Finite-State Transducers Through Their Approximations, with Proof
- **Authors:** David Barkhuizen
- **Abstract:**

  > What must a recurrent network be told to learn a finite-state transducer exactly? We train it on a target's answers and some of its approximations, its homomorphic images (the congruence quotients of its states), as extra outputs. A complete certificate then proves every learned network equal to its target at every length, so, given the target, one certified run settles a machine. Approximations raise the rate at which runs certify within a fixed budget. On modular division at 121 states, 16 of 20 runs given a cover, the sum and the difference, learn the machine, against none given the modular quotient alone; given the cover, 17, 16 and 15 of 20 do so at 49, 121 and 169 states. At 25 states the help is the approximation's own, not only that of what it tells about the state: the sum certified in 18 of 40 runs against 5 for a partition of the states that tells exactly as many classes and is no congruence (paired, Holm-adjusted $p = 0.0012$), though the state itself, the finest approximation, did at least as well as the cover (17 against 11 of 20, no difference detected). On random machines of 16 states with an approximation of 4 blocks planted in them, giving the blocks was not detected to help: on the same 25 fresh machines, 8 of 50 runs given them certified against 11 of 50 on the answers alone, so the earlier help against primitive machines (10 of 25 machines against 2) is not shown to be the giving's. $S_4$ and move-to-front-4 learn in 16 and 18 of 20 runs given two approximations, against 4 and 4 on their answers alone. On division (exploratory) and $S_3$, a factor of the learned state that holds an approximation holds one the network was given; elsewhere factors rarely hold them. Sampled tests overstate: they pass networks the certificate refutes.

- **Comments:** 21 pages. Version 2 of the preprint at Zenodo, doi:10.5281/zenodo.24303026; code, data and
  certificates at doi:10.5281/zenodo.24303030.
- **Categories:** cs.LG (primary), cs.FL
- **MSC class:** 68Q45; 68T07 &nbsp; **ACM class:** I.2.6; F.1.1
- **Journal-ref, DOI, report number:** none (the Zenodo DOI goes in the comments, not the DOI field, which
  is for a journal's version)
- **Licence:** CC BY 4.0

## The certificate note

- **Title:** Proving a Trained Network Is a Finite-State Machine: an Exact Certificate, Its Witness and Its
  Numerics
- **Authors:** David Barkhuizen
- **Abstract:**

  > A network trained on a task that a finite-state machine solves can pass every test and still be wrong: tests sample, and a machine extracted from the network is not the network. This note decides the question exactly, for networks built to allow it. When the only channel between a recurrent network's steps is a finite code, each state replaced exactly by its nearest codebook row, the network is a Mealy machine, and its equivalence with a target machine is decided by enumerating every reachable code under every input window. That core has a recent precedent. This note states it as a method for steps that read the state, with its proof, near ties branched, a witness that an independent checker of a few hundred lines verifies by re-running every entry through the forward pass, and sound bounds on its floating-point decisions. We validate it on existing networks, training none. All 1,077 certified tables of 674 networks were valid and all 11 uncertified ones invalid. A modelled sampled test of 100,000 words a length misses a planted fault at a rarely visited entry with chance up to 0.9998 on modular division. Interval and affine bounds show that every entry's decisions in the 613 tables they cover hold for the network's real-valued function, not only for its floating-point evaluation. Without the target, the proof needs a bound on the target's size, and we say where that holds.

- **Comments:** 14 pages. Research note, also at Zenodo, doi:10.5281/zenodo.23972277; its addendum (results,
  witnesses, networks, certificates) at doi:10.5281/zenodo.23972256. Cites arXiv:<paper 1's ID> (as its
  Zenodo DOI in the text).
- **Categories:** cs.LG (primary), cs.FL
- **MSC class:** 68Q45; 68T07 &nbsp; **ACM class:** I.2.6; F.1.1
- **Journal-ref, DOI, report number:** none
- **Licence:** CC BY 4.0

## The endorsement request (a draft for the owner)

> Subject: arXiv endorsement for the two notes
>
> Dear Julien,
>
> Thank you again for reading the certificate note and the preprint, and for the suggestion to post them on
> arXiv. I've prepared both. As a first-time submitter without an institutional address I now need a
> personal endorsement in cs.LG. Would you be willing to endorse me? arXiv's code is **XXXXXX**; you enter it at
> <https://arxiv.org/auth/endorse>. If arXiv says you can't yet endorse in cs (its rule counts papers more
> than three months old), would one of your co-authors be willing? I'd be grateful for a name.
>
> The abstracts and the source are the ones on Zenodo, unchanged.
>
> With thanks,
> David Barkhuizen
