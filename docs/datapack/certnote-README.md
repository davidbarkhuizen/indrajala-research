# Verifying the certificate note

The addendum to *Proving a Trained Network Is a Finite-State Machine: an Exact Certificate, Its Witness and Its
Numerics* (the note, [doi:10.5281/zenodo.23972277](https://doi.org/10.5281/zenodo.23972277); this record,
[doi:10.5281/zenodo.23972256](https://doi.org/10.5281/zenodo.23972256)). It holds what a reader needs to rerun the note's numbers, the checker and
the bounds, with no other record. No network here was trained for the note.

| file | what it holds |
| --- | --- |
| `certnote-results.tar.gz` | the result files `certificate_note_tables.py` reads, the jobs and their manifest |
| `certnote-tables.tar.gz` | every emitted table, the witnesses: 1,088, about 2.9 GB |
| `certnote-networks.tar.gz` | every network the jobs name, and the stored certificate each reproduces |
| `MANIFEST.sha256` | the hash of every archive, and of every file inside each |

Files keep the paths they have in a checkout, so the archives unpack at the root of a clone.

## 1. The files

```bash
git clone --recurse-submodules --branch certnote-v1 https://github.com/davidbarkhuizen/indrajala-studies.git
cd indrajala-studies && ./cli setup   # .venv, dependencies, a release build of the crate (needs a Rust toolchain)
.venv/bin/python scripts/paper/certnote_addendum.py check /path/to/this/record
for a in /path/to/this/record/certnote-*.tar.gz; do tar xzf "$a"; done
```

## 2. Every number and table in the note

The note's source is `research-notes/certificate-method.tex` in
[indrajala-research](https://github.com/davidbarkhuizen/indrajala-research) at tag `certnote-v1`.

```bash
.venv/bin/python scripts/paper/certificate_note_tables.py check /path/to/certificate-method.tex
```

It fails on any difference from the result files, whose hashes it checks first.

## 3. A witness, against its network

```bash
.venv/bin/python scripts/certnote/certificate_check.py data/certificate-note/recertify/tables/<id>.npz
```

That runs the structure check and re-runs every entry through the forward pass. The checker reads the target from
its tables and imports nothing from the certifier. `recertify/jobs.jsonl` names each table's network.

## 4. The bounds

```bash
.venv/bin/python scripts/certnote/certificate_bound.py data/certificate-note/recertify/tables/<id>.npz --out bound.jsonl
.venv/bin/python scripts/certnote/certificate_affine.py data/certificate-note/recertify/tables/<id>.npz --out affine.jsonl
```

The interval pass takes at most minutes a table. The affine pass ran on the 229 tables the intervals left undecided: a
deep window takes minutes, and the one `k` 4 table the longest, 45 hours on one core.

## What a rerun won't reproduce

- The seconds, which depend on the machine.
- The original runs' code. The certificates, faults and bounds ran from indrajala-studies between its #9 and #14, on
  `klip`. Two later checker fixes (#18) change no verdict: rerun, the structure check agrees on all 1,088 tables.

## Known limits

The note's Limits section and its three reviews (`review-2026-11-05-certnote-*.md` in indrajala-research) say what this
does not cover, including the networks without a bound and the findings stated rather than acted on.
