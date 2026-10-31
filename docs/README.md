# Research docs

The research side of the indrajala work, in Markdown, beside the papers and notes it feeds:

- [`research-notes/`](research-notes/): the studies' findings, notes, reports and literature
  review, and the goal they serve ([`machine-discovery.md`](research-notes/machine-discovery.md)).
- [`protocols/`](protocols/): how a study is designed, run and judged
  ([`experiment-design.md`](protocols/experiment-design.md)) and the feasibility checklist every
  cell is checked against ([`information-flow.md`](protocols/information-flow.md)).
- [`workplans/`](workplans/README.md): the research workplans, where decisions are settled and
  findings registered and recorded (paper 1's is [`paper-workplan.md`](workplans/paper-workplan.md)).
- [`datapack/`](datapack/): paper 1's Zenodo records: the datapack's verify page (`README.md`, the
  record's [doi:10.5281/zenodo.23733575](https://doi.org/10.5281/zenodo.23733575)) and its metadata
  (`zenodo-metadata.json`), and the preprint's (`paper-zenodo-metadata.json`), read by indrajala-studies' `scripts/paper/datapack.py` and `zenodo_deposit.py` (indrajala-ml's until 2026-10-31).

They moved here from [indrajala-ml](https://github.com/davidbarkhuizen/indrajala-ml) on
2026-10-23; their history before that is in indrajala-ml's git log (`git log --follow` on their old
paths, `docs/research-notes/` and `docs/protocols/`). **Paths in their prose that aren't links**
(`scripts/...`, `indrajala_ml/...`, `data/...`, `docs/next-steps.md`, `docs/measurement.md`)
**name indrajala-ml's files as they were when written.** Since 2026-10-31 the research code and its
data are in [indrajala-studies](https://github.com/davidbarkhuizen/indrajala-studies) (sibling clone
`../indrajala-studies/`): `indrajala_ml/studies/<module>.py`, `indrajala_ml/batch.py` and
`indrajala_ml/data/{addition,modular}_data.py` are its `indrajala_studies/<module>.py`, the study,
paper, runner and family-probe scripts keep their `scripts/...` paths there, and `data/` is its
`data/`; the library (`indrajala_ml/model/...`), `ab.py` and `docs/measurement.md` stay in ml. The research workplans, where
findings are registered and recorded, followed on 2026-10-30 ([workplans/](workplans/README.md)). Links to them point at indrajala-ml on GitHub;
in a local clone, indrajala-ml is the sibling `../indrajala-ml/`.
