# The certificate note, the reasoning review (2026-11-05)

A fresh-context review of Theorem 1, the conditions, the checker, the bounds, the fault chain and the target-free
section, against the code, with small experiments. No blocker. It could not break Theorem 1(a), wrong-label minimality,
the wrong-state dichotomy, the checker's logic, the bounds' second derivatives, softmax rewrite, ReLU chord, symbol
alignment or the Markov chain.

| # | Severity | Finding | Done |
|---|---|---|---|
| 1 | MAJOR | "Every length" against whole windows | "Words" paragraph with the premise; the review's "all 37 targets" was recomputed and is narrower (the workplan) |
| 2 | MAJOR | At `k` > 1, "onto" and "minimises to the target's size" false as written; the checker rejected a right machine | Note reworded; checker fixed (studies #18). No result changes: addition only |
| 3 | MAJOR | With branching on, counterexamples and counts can describe no real evaluation; `wrong_ties` can be wrong | Note restricts them to the strict run. **The certifier isn't changed** |
| 4 | MAJOR | The setting omitted the query adapter, 452 tables | $F'$ defined; adapter in the trusted base |
| 5 | MAJOR | C1-C3 outside the witness; trusted base incomplete | Base listed in full; the step-to-sequence link stated. **The proposed checker step over whole words isn't added** |
| 6 | MAJOR | Fault catalogue inexact; the abstract hid it | "A model", exceptions extended; the abstract uses division's `k` 1 figure |
| 7 | MINOR | Start snap not bounded | Stated, with its smallest ratio |
| 8 | MINOR | Rounding of radii not charged exactly | Stated; headroom recomputed here on the four tightest tables (centre over 31,000 radii). **Inflation not raised, no rerun** |
| 9 | MINOR | "4 ulps" | Relative error $4u$ |
| 10 | MINOR | NaN passes the margin checks | Checker fixed (studies #18); no table has a NaN |
| 11 | MINOR | "Caught 4,032" guaranteed by construction; negatives fail on structure only | Both said; dropped from the abstract |
| 12 | MINOR | Rarest faults all at window 0 | Stated, keyed. The harness docstring's final-window remark isn't changed |
| 13 | MINOR | Chow premises; "soon out of reach" not shown by the table | Reworded |
| 14 | MINOR | Abstract and opening wording | Reworded |
