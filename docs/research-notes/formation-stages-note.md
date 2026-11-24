# Note: formed is not separated; the window's load (2026-11-23)

**Status: a note, 2026-11-23, written at the owner's request: the patterns across the studies' runs between the
architecture (factors, factor width, window width, depth) and a run's state formation and certification.
Observational, read after the data, across studies of different code, arms and budgets: nothing here is
registered or a rule. Its last section names the probes that would test it. Read with indrajala-studies'
`scripts/studies/formation_reading.py stages data/window-recurrent` (studies #43); the stopping rules it
bears on are the population method's (`population-method-workplan.md`) and the told plan's shadow reading
(`what-is-told-workplan.md`, stage 3). **Corrected 2026-11-24** by its first probe (the codes probe: `p` 23
at width 32 with 43 codes a factor, 0 of 6): the load is necessary across the data, not sufficient; the
window's width binds at 529 states (section 2's last paragraph).**

## The data, and what it can say

Every curriculum run whose log and network survive in the studies' `data/window-recurrent/`: 1,277 runs with
their networks (division at `p` 5 to 23, word-problem s3 to s5, move-to-front, random machines), 904 of them
with the machine summary (`machine_reading.summary`: the codes reached, the (code, state) pairs, the pairs
right) at every step end. Each run's architecture is read from its saved network: the window's width W (the
embedding's size), its blocks (state inputs, two residual layers each), each factor's width and codes.

What the data varies, and so what it can answer:

| axis | values in the data | readable? |
| --- | --- | --- |
| window width W | 16, 22, 32, 64 | yes |
| codes a factor | 8 to 67 (128 in one probe) | yes |
| factor width | 16, 32 | barely: never alone |
| blocks (depth) | 1, 2, 3 | 1 against 3 yes; 2 against 3 only on small cells |
| factors | 2, save one probe's 6 runs with 1 | no |

Every network is a GRU cell with attention pooling and no cross term. The width probe at 64
(`told/width-probe/`) was still running when this was written; its results are entered below as read on
2026-11-23 (the told plan's stage 3 Findings), marked where they changed the first text.

## 1. Formed is not separated

A run passes three stages:

- **formed:** every step's input state lands on a code (the state share 1.0, as the formation reading has
  measured it since studies #42);
- **separated:** formed, and each code reached stands for one target state (pairs equal codes);
- **certified.**

Over the 891 runs of the cells logged at every step end, 321 formed, 282 separated and 275 certified: once a
run separates it nearly always certifies, and in no cell do the two differ by more than one run. In certified
runs, separation came at the certificate's own step in 151 of 275 (quartiles of the steps between them 0, 0
and 2); formation came earlier (quartiles 0, 2 and 5).

**Formation without separation.** The share counts a state on *a* code, not on its own. At `p` 23 and width
32 (stage 3) 8 of the 20 runs formed and one separated (with 1% of its pairs right); in the other seven each
code stood for 9 to 35 of the target's states at their best step end, and none certified. Before this
reading those runs counted as formed failures; they are failures to separate.

## 2. The load: joint codes over the window's width squared

The load is C/W²: C the factors' codes multiplied (the joint states the codebooks can name), W the window's
width. Holding the target fixed, division at `p` 13 (169 states):

| W | codes a factor (factor width) | load | runs | formed | certified |
| --- | --- | --- | --- | --- | --- |
| 16 | 9, 11 (16) | 0.3, 0.5 | 7 | 5 | 5 |
| 16 | 16 (16) | 1.0 | 139 | 53 | 42 |
| 16 | 32 (16) | 4.0 | 8 | 6 | 5 |
| 16 | 38, 50, 67 (16 or 32) | 5.6 to 17.5 | 59 | 11 | **0** |
| 16, one factor | 128 (32) | 0.5 | 6 | 6 | 6 |
| 22 | 38 (32) | 3.0 | 5 | 3 | 3 |
| 32 | 38 (32) | 1.4 | 54 | 43 | 39 |

(Each row pools its runs' arms and studies: at 16 codes the claims' quotient and product arms, which barely
form, sit beside the family's. The cell at 12 codes, 5 runs, none formed, is left out.)

- **Codes, not the target:** the target is the same in every row, and certification stops between load 4.0
  and 5.6.
- **Joint codes, not codes a factor:** one factor of 128 codes at width 16 (eight codes a unit of width)
  certifies every time; two factors of 38 (2.4 a unit) never do. Their joint codes are 128 against 1,444.
- **The window's width, not the factor's:** at width 16 and 38 codes, factors 32 wide formed 3 of 5 runs and
  certified none (factors 16 wide: 4 of 35 formed, none certified); width 22 certified 3 of 5.

The division ladder at width 32, its codes at the standard ratio (C about 8.5 times the target's states):

| `p` | states | codes | load | certified at W 32 | at W 64 |
| --- | --- | --- | --- | --- | --- |
| 13 | 169 | 38 | 1.4 | 35 of 46 (the family's arm) | |
| 17 | 289 | 50 | 2.4 | 15 of 24 (stage 3's 20 and its existence probe's 4) | |
| 19 | 361 | 56 | 3.1 | 13 of 20 | 3 of 4 (load 0.8) |
| 23 | 529 | 67 | 4.4 | **0 of 20** (8 formed, 1 separated) | **3 of 4** (load 1.1) |

The edge falls between 4.0 and 4.4 at both widths that reach it (16 and 32). At the standard ratio,
C ≤ 4W² is a target of at most about W²/2 states: about 480 at width 32 (`p` at most 21) and about 1,900 at
width 64.

**Low load, slow separation (corrected 2026-11-23).** The first text read width 64's two runs still going at
`p` 23 as likely failures: both had formed (shares 1.0 and 0.97) but stood at 48 and about 500 target states a
code. One of them (600) separated in a single step at step 34 and certified at 35 (1,003 of its 1,058 epochs);
the other (603) spent its budget unseparated. Three of four certified at load 1.1: consistent with the load.
But two of the three certified at steps 35 and 40, close to the budget, so at 529 states the budget may bind
too; four seeds can't tell.

**Necessary, not sufficient (added 2026-11-24).** The codes probe (the told plan's stage 3 Findings) ran
`p` 23 at width 32 with 43 codes a factor, load 1.81, below `p` 19's 3.1 at the same width: 0 of 6 certified,
one formed, none separated, and fewer runs formed than at 67 codes (five of the same six seeds reached a
share of 0.998 or more there). Lowering the load didn't bring the codes back; widening the window did (width
64, load 1.1: 3 of 4). So at 529 states the window's width binds beyond the load: C ≤ 4W² is consistent with
every cell here as a necessary condition and fails as a sufficient one. What width a target needs is not
measured: width 32's edge between `p` 19 and 23 is one point.

**The caveats.** The width-16 rows at load 5.6 and above are the division ladder's October rounds (code
older than the ladder's), and 24 of their 59 runs were a throughput benchmark on `stone`; what separates
them from the rows that certify is codes or width, but also their era. The observation is consistent across
two widths, not tested at either.

## 3. Depth, factors, factor width

- **One block doesn't form.** Paper 1's T3 linear arm, the only one-block cell: 0 of 20 formed (shares at most
  0.66), at `p` 5 where three blocks form 17 of 22.
- **Two blocks against three:** mixed, on cells of 6 to 19 runs at width 16. Three ahead where they differ
  much (s4: 0 of 6 certified against 16 of 19; division at 121: 1 of 6 against 4 of 6), two ahead at
  move-to-front-5 (2 of 13 against 0 of 6), level elsewhere. No reading.
- **One factor against two:** one probe, 6 runs (above). No reading.
- **Factor width:** never varied alone. At width 32, s4's 16-wide factors certified 0 of 6 and 32-wide 4 of
  24, but the cells differ in arm and era. No reading.

## 4. Below the load's edge, what is told decides formation

Where the load is low, the same network forms or not with what it is told and with the machine:

| machine | arm | formed | certified |
| --- | --- | --- | --- |
| s4 (24 states) | cover / family | 16 of 20 / 4 of 24 | 16 / 4 |
| move-to-front-4 (24) | cover / family | 18 of 20 / 4 of 20 | 18 / 4 |
| s3 (6) | cover / family | 5 of 20 / 3 of 22 | 5 / 3 |
| division at 5 | state / suffix / token | 18 / 0 / 1 of 20 | 17 / 0 / 1 |
| division at 11 | family / quotient | 17 / 0 of 20 | 16 / 0 |
| random, 16 states | planted / family | 24 of 80 / 9 of 130 | 22 / 7 |

The told plan measures this (its stages 1 and 2); the architecture enters it only through the load.

## 5. The stopping signal stays the share

Separation is what certifies, but it arrives late, close to the certificate, so it signals a failing run
later than the share does. At each multiple of the target's depth plus Chow's `k`, over the runs logged at
every step end, each signal's runs flagged (and of them, certified later):

| at | share < 0.9 | share < 0.999 | states a code > 1.2 |
| --- | --- | --- | --- |
| 2 | 567 (38) | 714 (116) | 773 (167) |
| 2.5 | 544 (22) | 654 (59) | 704 (99) |
| 3 | 559 (16) | 629 (37) | 671 (67) |
| 4 | 548 (4) | 599 (10) | 619 (21) |
| 6 | 440 (0) | 458 (0) | 461 (2) |

The share is the stopping rule's signal; separation reads why a formed run fails. *Added 2026-11-23:* the
width probe's `p` 23 run 600 held a share of 0.999 and then dipped to 0.987 at 6 times its depth plus `k`, two
steps before it separated and certified: the strictest rule (share below 0.999 at 6) loses a certificate there,
its first in any data; the rules at 0.9 lose none. A run formed but not
separated (`p` 23 at width 32) is a feasibility failure, not a seed's: a rule on the share runs it out. (The
first text said the load would refuse the cell before launch; the codes probe showed the load alone doesn't:
section 2.)

**The survey corrected.** Building this reading found the survey reading division's `p` from `/d5-` only, so
attempts named `approximation-linear.d5-family-wide-300` (paper 1's T3) were read as `p` 13 (studies #43 fixes
it). Corrected: 1,436 runs, 415 certified; not formed by 6 times depth plus `k`, certified later 0 of 537; the
three rules lose 0, 8 and 37 certificates, 1.17, 1.40 and 1.76 times the certificates per epoch (were 1,420,
403, 0 of 527, 0, 8 and 35, and 1.77). The told plan's shadow-reading paragraph is corrected with them.

## What would test it

Probes named, not registered when written; the first was registered and run in the told plan's stage 3
(2026-11-23 and 24, the codes probe):

- **`p` 23 at width 32 with fewer codes:** run 2026-11-24 (the codes probe), 0 of 6: the target's size at
  width 32, not the codes. Done.
- **The edge at another width:** `p` 23 at width 48, `p` 29 at width 64 (would find how the needed width
  grows with the target); not run: the owner stopped the told plan's runs (2026-11-24).
- **The register:** not proposed: the load is not sufficient.
- **Separation in the runner:** each step end already logs the machine summary; the batch's status could show
  states a code beside the share, so a formed run that isn't separating is seen while it runs.
