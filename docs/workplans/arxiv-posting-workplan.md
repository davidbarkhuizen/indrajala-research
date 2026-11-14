# Workplan: paper 1 and the certificate note on arXiv

**Status (2026-11-07): drafted. Decisions D1-D7 settled under the owner's delegation, with their options below;
O1 settled by the owner (a personal endorser, Brandoit first); O2 (the go) after A3. A1-A3 done (Findings); A4, the owner's endorsement and submission, next: `docs/datapack/arxiv-submissions.md`.** Submitting is the owner's step: their account,
their endorsement, their click. Everything before it is prepared here.

**Noted 2026-11-10:** whether paper 1's submission waits for a new version is the owner's call, O2 and O3 of
[what-is-told-workplan.md](what-is-told-workplan.md): the programme review
([review-2026-11-10-programme-review.md](../reviews/review-2026-11-10-programme-review.md)) found statements in paper 1
to correct (its G1, G2, G5-G7), and that plan's stage 1 tests what the paper's title claims. The certificate
note is untouched by it.

**Settled 2026-11-14 (the owner, the told plan's O2 and O3):** nothing goes to arXiv until the endorser can vouch.
Brandoit's arXiv paper (September 2026) counts toward endorsing once it is three months old, about December
2026 (O1 below). Until then corrections are self-published on Zenodo: paper 1's next version, after the told
plan's stage 1 is read. A4 waits for December; paper 1 goes then in its corrected version, beside the note.

**The ask.** Julien Brandoit read the certificate note and paper 1 (2026-11-07) and suggested arXiv, because
Google Scholar doesn't index Zenodo, so citations from there are mostly invisible. The owner: "let's plan and
prep".

**What goes up.**
- **Paper 1:** *Learning Finite-State Transducers Through Their Approximations, with Proof*,
  `papers/learning-transducers-with-proof.tex` at tag `paper1-v1.2` (doi:10.5281/zenodo.23826655; its datapack
  doi:10.5281/zenodo.23733575). Unchanged on `main` since the tag (checked).
- **The certificate note:** *Proving a Trained Network Is a Finite-State Machine: an Exact Certificate, Its
  Witness and Its Numerics*, `research-notes/certificate-method.tex` at tag `certnote-v1`
  (doi:10.5281/zenodo.23972277; its addendum doi:10.5281/zenodo.23972256). Unchanged since the tag (checked).
  It cites paper 1.

## arXiv's rules as they stand (checked 2026-11-07)

- **Endorsement (since 2026-01-21):** a new submitter is endorsed automatically only with an institutional
  email **and** earlier authorship of an arXiv paper in the same endorsement domain. Otherwise they need a
  **personal endorsement** from an established author in that domain: they start the submission, receive a
  six-character code, and send it to the endorser. arXiv's staff can't endorse or waive it. Endorsers must have
  authored a number of papers in the domain, submitted between three months and five years ago
  ([the announcement](https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/),
  [the help page](https://info.arxiv.org/help/endorsement.html)). **The owner has neither, so a personal
  endorsement is needed.**
- **The HAL route:** HAL deposits can be transferred to arXiv with no endorsement, and the CCSD says arXiv's
  change leaves that agreement as it was; the transfer doesn't guarantee acceptance
  ([CCSD](https://www.ccsd.cnrs.fr/en/2026/03/do-arxiv-s-rule-changes-have-an-impact-on-hal/)). HAL's metadata
  makes an affiliation mandatory; whether "independent researcher" passes is not known.
- **Generative AI** ([moderation](https://info.arxiv.org/help/moderation/index.html)): significant use of
  sophisticated tools, text-to-text generative AI among them, must be reported in the work; an AI tool is not
  listed as an author; the authors answer for every error. Since May 2026, incontrovertible evidence of
  unchecked LLM output (a hallucinated reference, a stray assistant remark) brings a one-year ban, after which
  submissions must first pass peer review
  ([report](https://www.researchinformation.info/news/arxiv-imposes-one-year-ban-for-unchecked-ai-generated-content/)).
- **Rate limits (since 2026-10-01):** two new submissions a calendar month, at most three active at once.
  Both papers fit in one month.
- **Content:** moderation isn't review, but declines what lacks substantive research or needs significant
  revision.

## Decisions (settled under the owner's delegation; options with pros and cons)

- **D1. What goes up, and in what order.**
  - (a) *Chosen.* **Both, paper 1 first, the note after it is announced.** Pros: the note cites paper 1, so
    paper 1 is on arXiv when readers follow the citation; both are what Brandoit read; two fits the monthly
    limit. Cons: two moderations, and two chances of a hold.
  - (b) Paper 1 only. Pros: one moderation. Cons: the note, the one Brandoit's group engages with, stays
    unindexed.
  - (c) The note only. Pros: the shorter, sharper text first. Cons: it cites a paper Scholar can't see.
- **D2. Which text.**
  - (a) *Chosen.* **The released texts, unchanged:** the sources at their tags, the Zenodo DOI already in each
    title block, the arXiv comments field naming the DOIs. Pros: one text in two places, no version to keep in
    step; every number already checked at release. Cons: the note cites paper 1 by its Zenodo DOI, not its
    arXiv ID (Scholar links them by title anyway; an arXiv v2 can add it with any later revision).
  - (b) A revised version for arXiv (v1.3, v1.1). Pros: the arXiv ID in the note's citation. Cons: a new
    release on Zenodo too, or two texts that differ; work for no reader's gain.
- **D3. Categories.**
  - (a) *Chosen.* **cs.LG primary, cs.FL cross-listed, for both.** Pros: the audience that trains networks
    and the one that studies automata; cs.LG's endorsers are many. Cons: cs.LG is crowded, so the papers are
    announced among many.
  - (b) cs.FL primary. Pros: the closest field, a smaller list. Cons: fewer endorsers, and the method is a
    learning method.
  - (c) cs.LO for the note. Pros: a certificate is a proof. Cons: the proof is a decision procedure for
    automata equivalence, which is cs.FL's.
- **D4. The licence.**
  - (a) *Chosen.* **CC BY 4.0**, as on Zenodo. Pros: the same terms in both places; anyone may reuse with
    credit. Cons: none for us.
  - (b) arXiv's non-exclusive distribution licence. Pros: the narrowest grant. Cons: terms that differ from
    the Zenodo copy of the same text.
- **D5. The upload.**
  - (a) *Chosen.* **A source package: the `.tex` and its `.bbl`, comments stripped,** built by `make arxiv`
    and checked by compiling it in an empty directory without the bibliography. Pros: arXiv refuses a PDF made
    from TeX, so source is required; the `.bbl` frees arXiv's build from our `library.bib`; stripping keeps
    working comments out of the public source. Cons: a make target and a check to write.
  - (b) The repository's source as it is, with the `.bib` files. Pros: nothing new. Cons: `library.bib` is
    the whole literature, not the paper's; comments go public.
- **D6. The AI disclosure.**
  - (a) *Chosen.* **The papers' contribution statements as they are.** Each names Claude (Opus 5.5) and Claude
    Code, says what it did at every stage, says Claude isn't an author and Anthropic wasn't involved, and says
    how the work was verified. Pros: meets arXiv's reporting rule; true. Cons: none found.
  - (b) A shorter statement for arXiv. Cons: a second text (D2), and less than the truth.
- **D7. The checks before upload** (against the ban's triggers and a moderator's hold).
  - (a) *Chosen.* **A reference check and a text check, as tools in this repository:** every cited entry
    resolves (its DOI, arXiv ID or URL answers, and the title and first author there match the `.bib`); the
    built PDF's text holds no draft note (`[Draft:`), no `TODO`, no assistant remark; the abstract in plain
    text within arXiv's 1,920 characters. Pros: the ban's two named triggers checked by machine, durable for
    every later paper (memory: durable measurement infra). Cons: a script to write and keep.
  - (b) A read by eye. Pros: no code. Cons: 36 and 35 cited entries; misses are what the ban punishes.

## Open for the owner

- **O1. The endorsement route.**
  - (a) *Chosen by the owner (2026-11-07).* **A personal endorsement from someone the owner knows of, asked once, with the code.**
    Brandoit first, since he suggested arXiv, but his arXiv record shows one paper, which looks like
    neuroscience, so he may not qualify in CS. arXiv's form says when he enters the code. If not, an author
    of a cited cs.LG or cs.FL paper. Pros: the normal route; fast once someone agrees. Cons: depends on a
    stranger's goodwill; arXiv asks for one request at a time, not many at once.
  - (b) HAL, then its transfer to arXiv. Pros: no endorsement. Cons: the mandatory affiliation is untested for
    an independent researcher; a third record of the same text; the transfer can still be refused.
  - (c) Not now. Pros: nothing to ask of anyone. Cons: Scholar keeps not seeing the work.
- **O2. The go:** once A1-A3 are done, the owner submits.

## Stages

| # | What | Where | Done when |
|---|---|---|---|
| A0 | This plan, O1 settled | indrajala-research | merged |
| A1 | The checks (D7): `scripts/check_references.py` and the text check | indrajala-research | both papers pass, or each failure fixed and recorded (a fix to a released text means a new release, D2 revisited with the owner) |
| A2 | `make arxiv` (D5): one `.tar.gz` per paper, built in a clean directory | indrajala-research | each package compiles alone with `pdflatex` twice, no undefined reference; its PDF's text equals the Zenodo PDF's (`pdftotext`, page furniture aside) |
| A3 | The submission sheet for each: title, authors, plain-text abstract, comments (pages, the DOIs), categories, licence | indrajala-research, `docs/datapack/arxiv-*.md` | written; the abstract under 1,920 characters |
| A4 | The owner's endorsement and submission, paper 1 then the note | the owner | both announced |
| A5 | The arXiv IDs recorded: memory, the READMEs; on Zenodo as related identifiers (an edit to published records, so the owner's go) | indrajala-research, Zenodo | done |

The packages are built from the tags, not from `main`, so later edits can't slip in.

## Findings

### A1: the checks (2026-11-07)

`scripts/check_references.py` (each cited key from the `.aux`, looked up by DOI on Crossref, by arXiv ID on
arXiv, by URL, or by a Crossref search on title and first author) and `scripts/check_text.py` (the built PDF's
text, for draft notes, to-dos, `??` and an assistant's phrases). On the two papers, built from `main` (the same
sources as their tags):
- **References: none false.** 59 distinct keys cited across both: 54 match their record's title and first
  author, 2 are ours, and 3 have no identifier and no Crossref match, each checked by hand against its
  publisher: Kolen 1993 (NIPS 6, pp. 501-508), Singh et al. 2018 (NeurIPS 31), Moore 1966 (Prentice-Hall).
  Two first runs flagged arXiv records whose titles end "(Technical Report)"; the check now drops such a
  trailer.
- **Text: nothing flagged** in either PDF.
- **For O1:** Brandoit's CS paper (arXiv:2609.32447, cited in the note) is from September 2026, inside
  arXiv's three-month exclusion, so it doesn't count toward endorsing yet; his co-authors on it (Ernst,
  Drion, Sacré) may qualify (not checked). Asking Brandoit first still fits: he can say who can endorse.

### A2: the packages (2026-11-07)

`scripts/arxiv_package.py` and `make arxiv`: the source from the tag, the bibliographies as they were at the
tag (indrajala-literature `1f8e5d0` for paper 1, `954cba8` for the note), comments stripped, the `.bbl` made,
then the `.tex` and `.bbl` built alone (`pdflatex` twice, no `bibtex`) with no undefined reference.
**Both packages reproduce the Zenodo PDFs' text word for word:** paper 1, 10,678 words, 19 pages (package
`fcfe612f211c…`); the note, 7,786 words, 14 pages (`f917f07e6792…`). The packages are byte-reproducible (two builds, the
same SHA-256). One bibtex warning: Henzinger et al.'s entry has both volume and number; harmless, since the
text equals the release's.

### A3: the submission sheet (2026-11-07)

`docs/datapack/arxiv-submissions.md`: the owner's steps, each field for both submissions (abstracts in plain
text: 1,441 and 1,396 characters, under 1,920), and a draft of the endorsement request to Brandoit.
