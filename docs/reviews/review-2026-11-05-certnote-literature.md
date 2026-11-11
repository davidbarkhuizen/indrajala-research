# The certificate note, the literature review (2026-11-05)

A fresh-context review of `research-notes/certificate-method.tex` (stage 6, D12), checking each citation against the
held text or the web and searching for precedents. Findings below as reported, with what was done. Web sources for
finding 4 were read at abstract level.

| # | Severity | Finding | Done |
|---|---|---|---|
| 1 | BLOCKER | Brandoit et al. 2026 misdescribed: their Appendix H.6.1 explores every reachable joint index under every symbol, a map fixed on first reach, correctness at every length by induction. "A third kind of evidence" was false | Checked against the text; the owner chose to publish with Brandoit named as nearest precedent (D14). Opening, related work and closing claim rewritten |
| 2 | MAJOR | "Neither enumerates" unsupported for Zeng et al. 1993 | Split: Zeng run each found state under each input but state no closure, soundness or decision |
| 3 | MAJOR | Omlin & Giles 1996 overstated | Now "generalising better than its network" |
| 4 | MAJOR | "Each has the precedent above" not true of numerics or checker | Added DeepZ, DeepT, Shi et al., Isac et al., Desmartin et al. |
| 5 | MAJOR | Koul et al. 2019 and Wang & Niepert 2019 omitted | Added, on the trace side |
| 6 | MINOR | Self-citations' DOIs don't print | Fixed in `extra.bib` |
| 7 | MINOR | Wickramasinghe et al.'s venue | Corrected from Crossref (literature #10) |
| 8 | MINOR | C4's "bit identity" stronger than the preprint | Now the retraining's step logs and SHA-256, not tables |
| 9 | MINOR | Higham chapters; underflow | "Chapters 3-4"; the interval's floor stated. Chapter placement is from memory, not the text |
| 10 | MINOR | DreamerV2 doesn't meet the conditions as published | Said so; determinism added |
| 11 | MINOR | Midpoint-radius citation | Rump 1999 added (pages per Crossref, not the review's) |
| 12 | MINOR | Henzinger wording | The problem is PSPACE-hard, not the method |
| 13 | MINOR | Chow: "minimal" | Added |
| 14 | MINOR | "Given one paragraph" | Now one paragraph and parts of the appendices |
| 15 | MINOR | Optional: Marzouk & de la Higuera 2020; Papazov et al. 2025 | Marzouk added, abstract read; Papazov not |

**Not checked:** Pnueli et al. 1998 beyond its abstract, so the note no longer says "an analyser and a small checker";
Vasilevskii 1973, de Figueiredo & Stolfi 2004, Moore 1966 and Higham 2002 are not held, fields and content from memory
or records. The search for an undercutting precedent was a limited web search, which is what "not found in our review"
means.
