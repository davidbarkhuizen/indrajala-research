# Workplan: E5's parity method — the same states, and a timing reference

**Status: drafted 2026-11-06 on the owner's go (O4). P1 (indrajala-nes #10) and P2 done the same day: E5's 97,079 frames all within the slack, the 3 unequal at the cut matched at −6, +11 and −6 cycles (the parent's Findings). P3 (indrajala-nes #20), P4 (#21) and P5 done 2026-11-07 (the parent's Findings): one power-on phase fits Mesen and FCEUmm (D34). Next: P6, D34 in nes-core.** A sub-plan of the emulator
workplan (`nes-rust-emulator-workplan.md`), for its stage E5. It replaces E5's gate ("no divergence on any
frame") with a criterion that separates wrong state from small timing drift (D20), and adds a
cycle-accurate timing reference beside FCEUmm (D22). IDs continue the parent's (D1-D19, O1-O3).

**The owner:** after E5's gate failed on 3 of 97,079 frames, "take a step back - do some fresh research and
re-analysis - is there not a good generic solution to this problem ?", "existing or novel"; then, on the
proposal below, "ok - good - now write up a detailed sub-workplan".

## Why: what E5's runner gate showed (2026-11-06, the parent's Findings)

- 34 FCEUmm traces on `klip` (power-on, random play on all 32 levels, the right-jump control): **97,079
  frames, 3 unequal**, all frame 65 of `random-2-2`, `random-5-3`, `random-7-2`: the title's lag frame after
  START, one byte (`$230`, a sprite's Y in SMB's OAM buffer), transient (frame 66 equal).
- **A frame end is a cut through a running program.** In most frames the game's writes end long before it,
  so the cut is invisible. In a lag frame the game is writing as the frame ends, and RAM equals FCEUmm's only
  in a narrow window of our cycles (66 cycles here). In 31 traces the window holds our cut; in two it ends 1
  cycle before it; in one it starts 13 cycles after it. **No single cut point fits all 34**: our timing
  within that frame differs from FCEUmm's by a few cycles, varying with the level's code path.
- Probes (claiming nothing): moving sprite 0's hit or the cut fixes some traces and breaks others; both
  together reach 0 at one setting, with its neighbours breaking most traces. That's fitting to three frames.
- **FCEUmm isn't cycle-accurate** (nothing found claims so; its core runs a fixed scanline structure, and
  its input lag has differed from Nestopia's by a frame), and it can't be read (D19). Matching it to the
  cycle risks copying its errors, against O3's reason for it: hardware-faithful behaviour.

## The research (2026-11-06)

- **Differential testing against a reference's logs** is the standard way to localise an emulator's
  timing: instruction or bus logs compared line by line (nestest's log; lockstep harnesses that stop at the
  first divergent access; work on CPU emulators against real devices, arXiv 2105.14273).
- **Mesen** is the usual cycle-accuracy reference for the NES. It has a trace logger with CPU cycle, PPU
  dot and frame tags, a Lua API with memory callbacks (Mesen 1's documented `emu.addMemoryCallback`), and a
  headless test runner that loads a ROM and a Lua script and exits (Mesen issue #526). The upstream Mesen2
  repository is archived; development goes on as MesenCE (nesdev-org). A third-party fork, `mesen-agent`,
  ships headless CLI binaries for Linux x86-64 **and arm64**, with Lua I/O off unless `--lua-allow-io`. All
  GPL-3.0-or-later: run as an oracle only, never read (D19).
- **Stuttering equivalence** (formal methods): two systems are equivalent if they pass through the same
  sequence of observable states, ignoring how long internal steps take. Adding a bound on the drift makes
  it a checkable criterion for "same states, nearly the same time".
- **Lag frames** are defined in TAS tools by the game's controller read (a frame with no read is a lag
  frame): a game-defined sync point, where a fixed frame end is the emulator's.
- **Existing or novel:** each part exists. Applying a bounded stuttering equivalence to an oracle that
  exposes RAM only at its frame ends, with a cycle-accurate emulator's write log as the timing reference,
  wasn't found described; it's a small assembly of known parts.

## The IDs, in time order

| ID | When | Short label | What it is |
|---|---|---|---|
| O4 | 2026-11-06 | the parity method's go | the owner: a generic method for E5, written up as this sub-plan |
| D20 | 2026-11-06 | the parity criterion | every oracle snapshot reached by our run, in order, within ±114 cycles of our frame end |
| D21 | 2026-11-06 | the window search | on a mismatch only, re-run the frame from its start, one instruction at a time |
| D22 | 2026-11-06 | the timing reference | Mesen's write log, run as a black box; FCEUmm stays the state oracle |
| D23 | 2026-11-06 | the write log | in nes-core behind a Cargo feature, off by default |
| D24 | 2026-11-06 | which Mesen | MesenCE's release first, `mesen-agent` if its headless Lua doesn't serve; pinned by SHA-256 |
| D25 | 2026-11-06 | aligning the logs | absolute CPU cycle from power-on; one constant calibrated on a no-input run, never per trace |
| D26 | 2026-11-06 | observing at the game's sync | not planned: revisit only if a `Step` ever differs between consoles |
| D34 | 2026-11-07 | the power-on phase | cycle count from 1, `ACCESS_DOT` 4, sprite 0's flag a dot earlier, no lead frame: one phase fits Mesen and FCEUmm |

## Decisions

Each has its options with pros and cons; the chosen one is marked.

- **O4. The go** (the owner, 2026-11-06). This sub-plan, then building it in a new session.

- **D20. The parity criterion.** What E5's gate claims.
  - (a) *Chosen.* **Bounded stuttering equivalence.** For each oracle frame, our run reaches the oracle's RAM
    at an instruction boundary within ±k CPU cycles of our frame end, k = 114 (one scanline, 113⅔ cycles);
    our run goes on from its own frame end, never from the matched point, so a wrong state can't be hidden:
    it shows in the following frames. Reported per trace: frames equal at the cut, frames matched with an
    offset, the offsets' distribution and maximum, and any frame unmatched (a failure, diagnosed).
    Pros: separates state (must be exact) from timing (a measured number); needs only RAM between frames,
    all stable-retro gives; generic, for any oracle and any game. Cons: tolerates up to a scanline of drift
    at a cut; timing is then judged by D22, not here.
  - (b) Exact at the cut (E5's gate as written). Pros: the strictest. Cons: tests FCEUmm's sub-frame
    timing, which isn't the hardware's, wherever a write meets the cut; fails now with no defect found.
  - (c) k = 30 (near the 13 cycles seen). Pros: tighter. Cons: fitted to three frames; a later lag frame
    could exceed it for the same reason.
  - (d) k = a frame. Pros: never fails on timing. Cons: so loose that a frame-late write would pass.
  - **Why one scanline:** FCEUmm's structure is per scanline, so its drift from the hardware should be
    under a line's cycles; and a write a whole line out is a real timing defect worth a failure.

- **D21. The window search** (in `nes-trace`).
  - (a) *Chosen.* **On a mismatch only:** keep a clone of the console at each frame's start (the previous
    cut); when the frame is unequal at the cut, run the clone one instruction at a time from k cycles before
    the cut to k after, comparing RAM at each boundary; then go on from the frame's own end. Pros: no cost on
    equal frames (all but a handful); simple; the same code as `trace-boundary`'s windows. Cons: a second
    run of the frame when unequal.
  - (b) A write log with undo, to step back from the cut. Pros: one pass. Cons: more machinery in the
    core's hot path for a rare case.
  - (c) Forward only from the cut. Pros: simplest. Cons: misses a match before the cut (two of the three
    frames match only before it).

- **D22. The timing reference.**
  - (a) *Chosen.* **Mesen's log of CPU writes**, run headless as a black box: for each write the CPU cycle,
    the address and the value; compared with ours write by write. FCEUmm stays the oracle for state (O3).
    Pros: localises timing to the exact write; Mesen is the reference for cycle accuracy; settles whether a
    drift is ours or FCEUmm's; `mesen-agent`'s arm64 build could run on `litshe`, which FCEUmm can't.
    Cons: a second oracle to install and pin; its Lua API to verify (P3); GPL (run only).
  - (b) FCEUX's trace logger. Pros: FCEUmm's relative. Cons: not cycle-accurate either; inherits the doubt.
  - (c) No timing reference: D20 alone. Pros: no new oracle. Cons: the 13 cycles stay unexplained.
  - (d) Real hardware. Pros: the truth. Cons: no console or capture rig here.

- **D23. The write log in nes-core.**
  - (a) *Chosen.* **A Cargo feature, `write-log`, off by default:** `Machine` keeps a `Vec` of (cycle,
    address, value) for every CPU write when on; `nes-tools` enables it. Pros: zero cost when off, so the
    Python module and E7's measures are untouched; no dependency (D17). Cons: feature unification: a
    workspace-wide build with `nes-tools` enables it in that build; the Python module is built alone
    (`maturin develop`), so it's off there; checked in P4.
  - (b) A runtime flag (`Option<Vec<..>>`). Pros: one build. Cons: a branch on every write in every build.
  - (c) A callback trait. Pros: general. Cons: a type parameter or a dynamic call in the hot path.

- **D24. Which Mesen.**
  - (a) *Chosen.* **MesenCE's official Linux release first;** `mesen-agent` if MesenCE's headless Lua run
    needs a display or can't write a file. Pros: the maintained upstream; the fork as a tested fallback with
    arm64. Cons: MesenCE is a .NET application; a headless run may need `xvfb-run`.
  - (b) `mesen-agent` first. Pros: built for headless use, JSON output, arm64. Cons: a small third-party fork:
    less provenance for an oracle.
  - **Either way:** the binary from a release, pinned by SHA-256 in a fetch script, installed outside every
    repository (`~/oracles/mesen/`, its config dir there too), run on runners only. Its source and bundled
    scripts are never read; our Lua script is our own (MIT, in indrajala-nes). The ROM stays in `~/roms`.

- **D25. Aligning the two logs.**
  - (a) *Chosen.* **Absolute CPU cycle since power-on,** with one constant offset (the reset sequence's
    cycles, the CPU-PPU phase at power-on) calibrated once on a no-input run and recorded; never fitted per
    trace. Mesen's RAM at power-on set to `$FF` (its setting; FCEUmm's and ours). Buttons set from the
    trace before each frame's pad read (SMB reads it in its NMI, after line 241): at Mesen's frame event,
    checked in P3 to come before the read. Pokes written at line 240, as FCEUmm takes them.
    Pros: one number, testable on test ROMs first. Cons: Mesen's power-on phase may differ from ours; if
    it can't be set, the constant absorbs it, and a varying phase would show as a varying offset.
  - (b) Align by frame (writes counted from each frame's start). Pros: robust to a power-on difference.
    Cons: frame starts are what's in question.

- **D26. Observing at the game's sync point** (for training, not E5).
  - (a) *Chosen:* **not planned.** E6's checks were equal bit for bit; a lag-frame cut changes a `Step` only
    if the environment observes that frame; revisit if one ever differs.
  - (b) End each environment step at the game's controller read. Pros: no observation is ever a
    half-written frame, on any emulator or the hardware. Cons: changes the environment's semantics against
    FCEUmm's frame API; a design change for the NES plan, not a parity fix.

- **D34. The power-on phase** (P5's reading, the parent's Findings; settled under the owner's delegation, the
  owner told at P6).
  - (a) *Chosen.* **Our cycle count starts at 1 (Mesen's count: D25's offset 0), `ACCESS_DOT` 4, sprite 0's
    flag at dot x + 1 (`SPRITE_0_DELAY` 0, in both PPU modes), and no lead frame before FCEUmm's first
    (the Python console's and `nes-trace`'s lead 0).** Pros: Mesen's writes equal ours to the cycle on 23
    timing ROMs and on 575,328 of SMB's 576,602; FCEUmm's 97,079 frames as before or better (97,077 equal,
    2 within the slack); E5's lead frame, a fitted constant, goes; every earlier test passes in tile mode.
    Cons: a change to nes-core's bits, so E6's PPO check against FCEUmm is run again; the pixel mode's
    sprite 0 changes with it.
  - (b) `main` as it is. Pros: no change. Cons: every timing ROM differs from Mesen; the lead frame stays
    unexplained.
  - (c) O without the sprite 0 change. Pros: smaller. Cons: SMB's status-bar split 9 cycles late against
    Mesen in 18,891 writes; one more lag frame off the cut against FCEUmm.
  - **The hardware's power-on alignment varies** (the wiki's "DMA": one of two CPU-APU alignments; the CPU-PPU
    one too). D34 picks the one both oracles show, for parity; no claim that it's every console's.
  - **Mesen as state oracle (the question O3 raises):** not needed for D34; FCEUmm stays (stable-retro's
    comparability). The owner hears it at P6.

## Stages, PR by PR

| # | Repository | PR or run | Done when |
|---|---|---|---|
| P0 | indrajala-research | This sub-plan; the parent's IDs, E5's gate and status point here | merged |
| P1 | indrajala-nes | `nes-trace`'s offset check (D20, D21) | tests below pass; CI green |
| P2 | `klip`, then indrajala-research | E5 rerun under D20 on the 34 traces (and the driven traces when they exist) | Findings: E5 passes or each unmatched frame diagnosed |
| P3 | `klip` (no PR), then indrajala-nes | Mesen installed and its capabilities verified; `scripts/fetch_mesen.sh` pinned | a test ROM's write log from Mesen, headless |
| P4 | indrajala-nes | `write-log` feature (D23); `nes-writes`, `write-diff`, `oracles/mesen/writes.lua` | tests pass; the Python module built without the feature |
| P5 | `klip`, then indrajala-research | Our writes against Mesen's: test ROMs, SMB's power-on, frame 65 of the three traces | Findings: whose timing departs, at which write |
| P6 | per P5 | A fix in nes-core with its test (if ours), or FCEUmm's quirk recorded (if theirs); E5 closed | the owner hears; parent's E5 marked done |

### P1: the offset check (indrajala-nes, ½ day)

- `nes-trace` gains `SLACK=k` (default 114) beside `BOUNDARY`: on an unequal frame, D21's search; the
  report per trace adds `equal at the cut`, `matched (offset)`, the offsets' histogram and maximum, and lists
  unmatched frames with their differing addresses (as now). Pokes stay applied at the cut; a save stores the
  console at the cut; a restore clears the frame-start clone.
- **Tests** (synthetic programs, no ROM, as `crates/nes-python/tests` and `nes-core/tests/console.rs` do):
  a program that writes a byte a few cycles after line 240 in one frame: a trace built with the oracle's
  cut 20 cycles later matches with offset +20; one built 20 cycles earlier matches with −20 (the
  before-the-cut case); with k = 10 both are unmatched; a trace with a byte altered is unmatched at any k;
  equal frames cost no second run (a counter in the report).
- Idle skip (D8) stays on in the main run; the search steps instructions with it off. Bit-equal by D8.

### P2: E5 under D20 (`klip`, 1 hour)

- `nes-trace` over `~/gates/traces/*.trace` (the 34, also in indrajala-studies' `data/nes-parity/`).
  **Expected:** the 3 frames matched at offsets of about −1 to +13 cycles, everything else equal at the cut.
- When stage 2.2 is redone on the canonical dump: `record_traces.py --levels-dir` on FCEUmm (driven runs:
  level ends, pipes, area changes, the richest source of lag frames), then the same.
- **Pass:** no unmatched frame; the offsets listed. Findings in the parent; E5's state check is then met.

### P3: Mesen on `klip` (½-1 day)

- Fetch MesenCE's Linux release (D24), pin its SHA-256 in `scripts/fetch_mesen.sh` (gitignored target, as
  `scripts/fetch_test_roms.py`), install to `~/oracles/mesen/`. Fall back to `mesen-agent` per D24.
- **Verify, on a test ROM already fetched (nestest or blargg's, never SMB first):** a headless run with a
  Lua script exits by itself; a memory-write callback gets address and value; the CPU cycle count and the
  PPU's line and dot are readable in it (Mesen 1's `emu.getState()`; Mesen2's names to confirm from its
  documentation, not its source); a file can be written (or stdout); RAM at power-on can be set to `$FF`;
  the frame event's position relative to line 240 and to the NMI.
- If any capability is missing: the alternative distribution; if both lack it, P4-P5 stop and the owner
  hears (D20 still stands on its own).

### P4: the write logs (indrajala-nes, 1 day)

- **`write-log` (D23):** `Machine::write` pushes (cycle, address, value) for every CPU write when the
  feature is on. A test: the idling program's writes, with their cycles, equal a hand-worked list; a check in
  CI that `nes-python` builds without the feature (`cargo tree -e features -p nes-python`).
- **`nes-writes ROM TRACE [from] [to]`:** replays a trace (as `nes-trace`, lead 1, line 240) and prints
  every write with its absolute cycle, line and dot, from frame `from` to `to`.
- **`oracles/mesen/writes.lua`** (ours, MIT): reads a trace's per-frame buttons and pokes from a small text
  form that `nes-writes --script` emits (no ROM, no art), sets them per D25, logs every CPU write as
  (cycle, address, value, line, dot), and stops after frame `to`.
- **`write-diff OURS MESEN [--offset c]`:** aligns by cycle (D25) and reports the first write differing in
  address or value, and every write at a different cycle (the delta's histogram); exits nonzero on the
  first difference in value.

### P5: the comparison (`klip`, ½ day)

1. **Calibration on test ROMs** (no input), from those `scripts/fetch_test_roms.py` already pins: `nestest.nes`,
   then timing-sensitive ones (`vbl_set_time.nes`, `nmi_timing.nes`, `timing_order.nes`, `edge_timing.nes`):
   writes equal with one constant offset, which is recorded (D25).
2. **SMB's power-on, 600 frames, no input:** writes equal in address, value and cycle (the reset routine's
   two VBlank polls and every NMI's sprite-0 wait are in here).
3. **Frame 65 of `random-2-2`, `random-5-3`, `random-7-2`, and two traces equal at the cut:** frames 0-70.
   **The reading:** the first write whose cycle differs from Mesen's, if any, with the instruction and the
   PPU's position; and FCEUmm's window (from P2) against Mesen's write at the cut.
4. **Then wider:** every trace up to its first restore (restores need Mesen's savestates; later if needed).

### P6: the outcome

- **If our timing departs from Mesen's:** the cause found from the first differing write (sprite 0's hit,
  an NMI's latency, a DMA's alignment, a `$2002` race), fixed in nes-core from the NESdev wiki's account,
  with a test ROM or a synthetic test; then E5's traces, the emulate suite and E6's PPO check again.
- **If ours equals Mesen's and FCEUmm differs:** FCEUmm's sub-frame timing recorded as the cause; D20's
  offsets are its measure; nothing changes in nes-core.
- **Either way the owner hears,** with the question O3 then raises: whether Mesen should become the state
  oracle too (it would take FCEUmm's place in `record_traces.py`; FCEUmm's comparability with stable-retro
  is the reason to keep it).

## Not planned

- Reading FCEUmm's, FCEUX's or Mesen's source (D19), or tuning nes-core to FCEUmm's frames (the probes).
- Mesen as a training console (it's an oracle; our emulator is the one trained on).
- D26's game-synced steps, unless a `Step` differs.

## Risks

| Risk | Effect | Answer |
|---|---|---|
| MesenCE's headless Lua needs a display or lacks file output | P3 stalls | `xvfb-run`; then `mesen-agent` (D24) |
| Mesen2's Lua names differ from Mesen 1's docs | P4's script changes | verified in P3 from the documentation and on a test ROM |
| Mesen's power-on CPU-PPU phase differs from ours and can't be set | a constant or varying offset | calibrated once (D25); a varying one is itself a finding |
| A write's reported cycle means the instruction's start, not the access | off-by-a-few in every write | calibration on a test ROM whose write cycles are known (our CPU's bus timing is SingleStepTests-exact) |
| D20's k hides a real timing bug | a defect passes E5 | D22 checks timing write by write; k is one scanline, not a frame |
| The level-driver regression on the canonical dump (stage 2.2, under diagnosis) | P2's driven traces wait | P2 runs on the 34 now; driven traces later |

## Sources

- Mesen trace logger: https://www.mesen.ca/docs/debugging/tracelogger.html
- Mesen Lua callbacks (Mesen 1 docs): https://www.mesen.ca/docs/apireference/callbacks.html
- Mesen headless test runner: https://github.com/SourMesen/Mesen/issues/526
- mesen-agent (headless fork, x86-64 and arm64): https://github.com/atonamy/mesen-agent
- libretro-fceumm's frame structure: https://github.com/libretro/libretro-fceumm/blob/e57dc07a44f8bc13146111774fe84ad7f46b3996/src/drivers/libretro/libretro.c
- fceumm's input lag against Nestopia: https://forums.libretro.com/t/an-input-lag-investigation/4407/177
- Differential testing of CPU emulators against devices: https://arxiv.org/pdf/2105.14273
