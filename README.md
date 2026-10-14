# indrajala-papers

Our own papers on the indrajala work, in LaTeX (arXiv style). **Private** until we choose to
publish a paper.

| paper | status | about |
| --- | --- | --- |
| `snapped-window-recurrence.tex` | first draft, 2026-10-14 | window-recurrent transformers with a snapped (vector-quantised) state; certifying the learned machine; the exclusion bound; addition, modular sums, modular division |

## Layout

Flat: every paper is one `.tex` at the top level; `extra.bib` holds references that aren't in
the literature collection (textbooks, classical automata theory, statistics).

**Other people's papers are an external repository:**
[`davidbarkhuizen/indrajala-literature`](https://github.com/davidbarkhuizen/indrajala-literature)
(private), the PDFs we read and its `library.bib`, keyed by file stem. It is not vendored or a
submodule here: clone it beside this repository, or tell the build where it is.

## Building

Needs a TeX distribution with `latexmk` (on Ubuntu: `sudo apt install texlive-latex-extra
texlive-fonts-recommended texlive-bibtex-extra latexmk`).

    git clone git@github.com:davidbarkhuizen/indrajala-literature.git ../indrajala-literature
    make                      # or: make LITERATURE=/path/to/indrajala-literature

## Sources

Every figure in a paper comes from the code repository's recorded findings
([`davidbarkhuizen/indrajala-ml`](https://github.com/davidbarkhuizen/indrajala-ml): the study
scripts' docstrings and the workplans under `docs/`), with the commit named in the paper. Claims
of novelty are "not found in our review", never "first", with the nearest prior work cited beside
each.
