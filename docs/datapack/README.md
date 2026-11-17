# Verifying paper 1

This is the datapack for *Learning Finite-State Transducers Through Their Approximations, with Proof*
(the preprint: version 2, [doi:10.5281/zenodo.24303026](https://doi.org/10.5281/zenodo.24303026); version 1,
[doi:10.5281/zenodo.23826655](https://doi.org/10.5281/zenodo.23826655); its LaTeX source is in
[indrajala-research](https://github.com/davidbarkhuizen/indrajala-research), `papers/`). This is the
datapack's version 2.0, [doi:10.5281/zenodo.24303030](https://doi.org/10.5281/zenodo.24303030); every version is under
[doi:10.5281/zenodo.23733575](https://doi.org/10.5281/zenodo.23733575)'s record. It holds only what the paper cites. Everything here can
be checked without trusting its authors: the files against their hashes, every number in the paper
against the files, every learned machine against its target, and the training itself against a
rerun.

## What is in the record

| file | what it holds |
| --- | --- |
| `verify.tar.gz` (about [VERIFY SIZE]) | what `paper_tables.py check` reads to regenerate every number and table in the paper, plus every certified network ([VERIFY FILES] files) |
| `verify.sha256` | the verify pack's manifest: each file's SHA-256, the same hashes the paper's manifests cite |
| `full-<part>.tar.gz` (about [FULL SIZE] in all) | every file the paper's manifests list, one archive per test (`t1`, `t2-t5`, ..., `t12-runs`, and version 2's `told-stage1`), plus `approximation-claim` and `addition`; each archive carries its manifests |
| `MANIFEST.sha256` | the SHA-256 of every archive (whole), of every part, and of every manifest |

The full pack's archives above 1 GB are uploaded in 1 GB parts (`full-t2-t5.tar.gz.part-00`, `-01`,
...), each on its own connection. Rejoin them before use; `MANIFEST.sha256` holds both the parts'
hashes and the whole archive's:

```bash
for a in $(ls *.part-00 | sed 's/.part-00$//'); do cat "$a".part-* > "$a"; done
```

The verify pack is enough to check every claim; the full pack is the archive of record (every
training log, every step's network, every reading).

## Setup

The code is [indrajala-studies](https://github.com/davidbarkhuizen/indrajala-studies) at `paper1-v2`, with
[indrajala-ml](https://github.com/davidbarkhuizen/indrajala-ml) and its native crate
[indrajala-math-rust](https://github.com/davidbarkhuizen/indrajala-math-rust) as submodules; the
manuscript's source is in [indrajala-research](https://github.com/davidbarkhuizen/indrajala-research) at
`paper1-v2`. (Version 1.0 named indrajala-ml at `paper1-v1.1`, where the studies' code lived then; its
numbers regenerate the same from indrajala-studies.)

The submodules are recorded with SSH URLs (`git@github.com:...`); without a GitHub SSH key, have git
fetch them over HTTPS (once, for your user):

```bash
git config --global url."https://github.com/".insteadOf git@github.com:
```

```bash
git clone --recurse-submodules https://github.com/davidbarkhuizen/indrajala-studies
cd indrajala-studies && git checkout paper1-v2 && git submodule update --init --recursive
./cli setup   # .venv, Python dependencies, a release build of the crate (needs a Rust toolchain)
git clone https://github.com/davidbarkhuizen/indrajala-research ../indrajala-research
(cd ../indrajala-research && git checkout paper1-v2)
```

## 1. The files are what the paper cites

Check the archives you downloaded against `MANIFEST.sha256`, then the verify pack's files against
`verify.sha256`:

```bash
sha256sum -c --ignore-missing MANIFEST.sha256
mkdir verify && tar -xzf verify.tar.gz -C verify
(cd verify && sha256sum -c --quiet ../verify.sha256) && echo "every file verifies"
```

Each hash in `verify.sha256` is one of the paper's manifests' own: the verify pack is a subset of the
full pack, not a new set of results.

## 2. Every number and table in the paper comes from these files

`paper_tables.py check` recomputes every table the manuscript holds, and every measured number in its
prose (each marked in the source with its key), from the result files, and compares them with the
text. It prints a line per table and fails on any difference:

```bash
.venv/bin/python scripts/paper/paper_tables.py --data ../verify \
  check ../indrajala-research/papers/learning-transducers-with-proof.tex
```

The numbers left unmarked in the paper are settings (lengths, bounds, seeds), not measurements.

## 3. Every learned machine is its target

A snapped network is a Mealy machine whose states are its reachable joint codes; the certificate
enumerates that machine from the saved network, minimises it and compares it with the target, every
output and every next state. A pass is a proof at every length, not a sample. For example, T1's
`d5-sum-319` (modular division at p = 5, trained on the sum):

```bash
.venv/bin/python scripts/studies/modular_family_probe.py certify \
  ../verify/paper/t1/runs/sum/seed319/certified-step-9.network.json \
  --task modular-division-5 --arm sum --vocabulary sum suffix token --out cert.json
# certified: 105 codes reached, minimised to 25, 0 wrong outputs, 0 wrong states ...
```

Each test's `certify/` directory holds the certificate the paper counts for every network, in both
verdicts (with the network's own snaps, and robustly: every near tie branched both ways). The
network's SHA-256 is in its long test's record (`*.long-test.json`, key `sha256`).

## 4. Training reproduces bit for bit

Training is deterministic given the seed, the code and the crate, so a rerun matches only at the code
a run ran at: version 1's runs at `paper1-v1.1` (indrajala-ml, where the scripts were then
`scripts/batch.py` and `scripts/modular_family_probe.py`), stage 1's at `paper1-v2` (indrajala-studies).
The code changed between them: at `paper1-v2`, T1's `d5-sum-319` matches its original for its first 6
log rows and differs from step 2 (checked 2026-11-17), while stage 1's `told-d5-sum-816` matches bit for
bit. `batch.py command` prints the exact command that ran an attempt, from its batch's ledger. For
version 2's study, from indrajala-studies at `paper1-v2`:

```bash
.venv/bin/python scripts/runner/batch.py command ../full/told/stage1 approximation.told-d5-sum-816 \
  --out rerun-told-d5-sum-816
```

and for version 1's, from indrajala-ml at `paper1-v1.1`:

```bash
.venv/bin/python scripts/batch.py command ../full/paper/t1 d5-sum-319 --out rerun-d5-sum-319
```

(`../full` is the full pack extracted; step 5.) Run it (T1's `d5-sum-319` takes about 5 minutes on
one core), then compare its log with the
original's, every logged row but the wall-clock seconds, and its certified network's SHA-256 with
the original's (`same-prefix` reads logs only, so indrajala-studies' serves both):

```bash
.venv/bin/python scripts/studies/modular_family_probe.py same-prefix \
  rerun-d5-sum-319/log.jsonl ../full/paper/t1/attempts/d5-sum-319/log.jsonl
sha256sum rerun-d5-sum-319/certified-step-9.network.json   # 45c72add3cc9d641...
```

The paper's T7 reran the shortest certified run of each of T1, T3, T2 and T5 this way, on aarch64 (a
Raspberry Pi 5) and on x86-64, from the code at release: all four matched bit for bit
(`full-t7-reruns.tar.gz`, `full-t7-reruns-jebel.tar.gz`).

## 5. The full pack

Rejoin the split archives (above), then extract every `full-*.tar.gz` into one directory. Each manifest verifies with `sha256sum -c` from its
own directory or its stem's (`paper/t2-t5.sha256` from `paper/t2-t5/`), with one exception,
`paper/t4-fresh.sha256`, from `paper/t2-t5/approximations/`. `datapack.py check` does all of it,
re-hashing every archive (whole, or rejoined from its parts in place) and every file inside against
the manifests each archive carries:

```bash
.venv/bin/python scripts/paper/datapack.py check <the directory holding the downloaded files>
```

## What to know

- **Manifests added after the readings.** Four manifests were written on 2026-10-28, after the tests
  they cover were read, because the originals had left those files out: `paper/t11-runs.sha256` and
  `paper/t12-runs.sha256` (T11's and T12's training logs and certified networks),
  `control/models.sha256` and `e3-e4/long-tests.sha256` (two of addition's studies). They attest the
  files as they are now, not at the time the tests ran.
- **Re-read reports.** Where a later re-read (the strict reader, T6) rewrote a test's proof reports,
  the test's manifest names the originals, kept beside them in `proof-loose/`; `t6-proof.sha256`
  covers the rewritten ones.
- **Tags.** `paper1-v1` is the code and manuscript as version 1's numbers were computed;
  `paper1-v1.1` adds only the datapack's tools for archives in parts (indrajala-ml #1068), which step
  5 needs. `paper1-v2` (indrajala-studies, indrajala-ml, indrajala-math-rust and indrajala-research)
  is the code and manuscript of version 2: the studies' code moved from indrajala-ml to
  indrajala-studies on 2026-10-31, and stage 1 of the told plan ran on it (its crate at `edce2de`).
  Certification and the tables of version 1 are the same at every tag (`paper_tables.py check`
  regenerates all of version 1's numbers from indrajala-studies at `paper1-v2`); training is not: rerun
  each run at the code it ran at (step 4).
- **Version 2.0 adds** the told plan's stage 1 (`told/stage1.sha256`, `full-told-stage1.tar.gz`) and
  regenerates the verify pack to hold it. Every archive of version 1.0 is unchanged; its hashes in
  `MANIFEST.sha256` are the same.
- **What is not here.** Earlier exploratory studies the paper does not cite (the state-formation
  work among them) are left for the papers that use them.
