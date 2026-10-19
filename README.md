# indrajala-papers

Our own papers on the indrajala work, in LaTeX (arXiv style). **Private** until we choose to
publish a paper.

| paper | status | about |
| --- | --- | --- |
| `snapped-window-recurrence.tex` | third draft, 2026-10-17 (E2b' to add) | learning finite-state transducers from examples, with proof: a window-recurrent network with a snapped (vector-quantised) state; certifying the learned machine; the exclusion bound; addition and modular sums |
| `certified-modular-division.tex` | second draft, 2026-10-17 (the approximation claim and `p` 11 to add) | the companion: larger transducers, product machines; modular division (25 and 49 states) learned by training on a cover of the target machine; an enforced factorisation that blocks learning; collapse past a solution |
| `transition-and-output-paths.tex` | research note, 2026-10-19 | where the method stops (division at 121 against 169 states, the general algebras at 120); at 169 the learned transition function is exact but the answers' features aren't linearly separable; window branches, a path for each state factor and one for the output, with their registered claims |

## Layout

Flat: every paper is one `.tex` at the top level, with dated review notes (`review-<date>-<topic>.md`) beside them
and [`contribution.md`](contribution.md), the current statement of both papers' novel contribution (kept up to date); `extra.bib` holds references that aren't in
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
