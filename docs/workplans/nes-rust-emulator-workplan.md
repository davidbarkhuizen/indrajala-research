# Workplan: a Rust NES emulator for Super Mario Bros

**Status: drafted 2026-11-06, with D1-D19 settled under the owner's delegation, and O1 (the go) and O2 (emulation on `pyramidon`) settled by the owner. E1-E4 done 2026-11-06 (indrajala-nes #1-#5; Findings). **O3 (the owner, 2026-11-06): FCEUmm, not nes-py, is the oracle, and the ROM moves to the canonical dump;** E5 goes on against FCEUmm.** **E5 against FCEUmm, first readings (indrajala-rl #19, indrajala-nes #8; Findings): its frame ends at line 240; 14,740 development frames equal; the full trace set waits for a runner.** **E6 built (indrajala-nes #9, indrajala-rl #20) and its runner gates pass (Findings): PPO on the Rust console equals PPO on FCEUmm bit for bit.** **E5's gate is not met: 3 of 97,079 frames unequal, one transient at a lag frame's cut (Findings); the owner chose a generic method (O4): E5 goes on under the sub-plan `nes-emulator-parity-workplan.md` (D20-D26).** **Pixel mode and a viewer (O5): the sub-plan `nes-pixel-mode-workplan.md` (D27-D29, V1-V4), after the parity sub-plan's P1-P2.** This is the NES plan's stage E (`nes-one-network-workplan.md`), worked out PR by PR. It
builds on the analysis `docs/research-notes/nes-rust-emulator-analysis.md` and replaces that note's E1-E8
table. The analysis keeps the hardware facts and its first estimates.

**The owner:** "start building the nes emulator in rust according to the plan while we wait", then "first write up
a detailed workplan - do a proper research first - then analyse - also double check there is no
existing workplan (check across repos)". Earlier, on its shape (the NES plan's D12): "build it with a
clean mapper interface and a separate per-game observation layer, implement only mapper 0 and SMB at
first, and add more when another game is actually wanted"; and "designed from the ground up for
integration with an nn", "based on existing os code and designs".

**No existing workplan** (checked 2026-11-06): every local repository's default branch and remote
branches, indrajala-ml's `docs/workplans/` and `docs/next-steps.md`, and the GitHub repository list.
There's only the analysis note and the NES plan's stage E section, both extended here.

**The question this answers.** How to build a headless NES that runs Super Mario Bros (NROM, mapper 0)
**bit for bit as `nes-py` does**, from its RAM, much faster a core, batched for a network. Where nes-py
isn't hardware-accurate, the plan says what happens. Then how to swap it into indrajala-rl with no change
to the trainer, and measure what it buys.

## The IDs, in time order

| ID | When | Short label | What it is |
|---|---|---|---|
| O1 | 2026-11-06 | the go | the owner's go: build now, ahead of D10's reading at 3.4, beside the NES plan's runs |
| D1 | 2026-11-06 | build or adopt | our own emulator, with turbo-emu, TetaNES and NeSLE as references, not dependencies |
| D2 | 2026-11-06 | the repository | `indrajala-nes`, new and private, MIT; three crates: core, game, Python |
| D3 | 2026-11-06 | the CPU's timing | one bus access a cycle, dummy accesses included |
| D4 | 2026-11-06 | the PPU's sync | catch-up to the exact dot, by predicted events; no frame buffer |
| D5 | 2026-11-06 | sprite 0 | computed from OAM, the pattern table and the nametable, not a constant a game supplies |
| D6 | 2026-11-06 | the frame boundary | two modes: nes-py's (measured at E5) for parity, the hardware's (VBlank) beside it |
| D7 | 2026-11-06 | the oracle | nes-py first, as a black box, on recorded console calls; stable-retro's FCEUmm second, only on a divergence |
| D8 | 2026-11-06 | idle skip | a jump to itself is skipped to the next event, generically and bit for bit; game routines aren't replaced |
| D9 | 2026-11-06 | the state | plain data: a reset is a copy; a versioned byte form for checkpoints; the ROM outside it |
| D10 | 2026-11-06 | the Python boundary | a drop-in `Console` first, then a Rust batch with SMB's layer in Rust; E7's measure sets the batch's shape |
| D11 | 2026-11-06 | the threads | scoped threads claiming consoles from a counter, no dependency; persistent workers only if measured to matter |
| D12 | 2026-11-06 | sticky draws | drawn in Python by the environment's generator and passed in, so the bits equal `NesEnv`'s |
| D13 | 2026-11-06 | test data | SingleStepTests (MIT) in CI; blargg's ROMs and nestest fetched by script and pinned, never committed |
| D14 | 2026-11-06 | the machines | development, its emulation included, on `pyramidon` and in CI; parity traces, measures and anything for a finding on runners, after D18 ends |
| D15 | 2026-11-06 | sound later | an `Apu` trait with a silent implementation |
| D16 | 2026-11-06 | the mapper seam | a `Mapper` trait taken as a type parameter, monomorphised; NROM alone |
| D17 | 2026-11-06 | the game seam | a `Game` trait in the core; SMB in its own crate; the core holds no RAM address, checked in CI |
| D18 | 2026-11-06 | every machine's bits | integers only, no SIMD: the same bits on x86-64 and aarch64, checked on `litshe` |
| D19 | 2026-11-06 | sources and licences | MIT and Apache code adapted with notices; GPL code and nes-py's C++ never read |
| O2 | 2026-11-06 | emulation on `pyramidon` | the owner: emulation that is development may run on `pyramidon` |
| O3 | 2026-11-06 | the oracle and the ROM | FCEUmm (stable-retro), not nes-py, is the oracle; the canonical SMB dump replaces ours; what rests on either is redone |
| O4 | 2026-11-06 | the parity method's go | the owner: a generic method for E5, in the sub-plan `nes-emulator-parity-workplan.md` |
| D20 | 2026-11-06 | the parity criterion | every oracle snapshot reached, in order, within ±114 cycles of our frame end (the sub-plan) |
| D21 | 2026-11-06 | the window search | on a mismatch only, the frame re-run from its start (the sub-plan) |
| D22 | 2026-11-06 | the timing reference | Mesen's write log, run as a black box; FCEUmm stays the state oracle (the sub-plan) |
| D23 | 2026-11-06 | the write log | in nes-core behind a Cargo feature, off by default (the sub-plan) |
| D24 | 2026-11-06 | which Mesen | MesenCE first, `mesen-agent` as fallback; pinned by SHA-256 (the sub-plan) |
| D25 | 2026-11-06 | aligning the logs | absolute CPU cycle; one constant calibrated without input (the sub-plan) |
| D26 | 2026-11-06 | observing at the game's sync | not planned unless a `Step` differs (the sub-plan) |
| O5 | 2026-11-06 | the pixel mode's go | the owner: a real pixel pipeline as a second PPU mode, and a viewer; the sub-plan `nes-pixel-mode-workplan.md` |
| D27 | 2026-11-06 | the render mode | a type parameter on the PPU (`NoPixels`, `Pixels`): tile mode unchanged (the pixel sub-plan) |
| D28 | 2026-11-06 | the pixel gate | both modes' RAM equal where no extra is read; pixels against FCEUmm's, as numbers (the pixel sub-plan) |
| D29 | 2026-11-06 | the palette | generated from the NESdev wiki's NTSC account (the pixel sub-plan) |
| V1-V4 | 2026-11-06 | the viewer and its terms | a Rust viewer fed by episode files; pixel mode fuller; local recordings; after the parity sub-plan's P1-P2 (the owner; the pixel sub-plan) |

## What the research found (2026-11-06)

### Prior work in our niche

Three Rust NES projects aimed at reinforcement learning have appeared since the analysis was written.
The first matters most:

| Project | Licence | What it is | What it tells us |
|---|---|---|---|
| [env-SuperMarioBrosNes-turbo-emu](https://github.com/tsilva/env-SuperMarioBrosNes-turbo-emu) (PyPI `env-supermariobrosnes-turbo-emu` 0.7.4, 2026-10-03) | MIT | A Rust NROM core, an SMB driver crate, and a PyO3 vector environment with Rayon over lanes. Created 2026-06, one maintainer, built with an AI agent (its `AGENTS.md`, `.codex/`) | **That it can be done, and how fast:** 10,400 environment steps/s at one environment (frameskip 4, about 41,600 frames/s, with rendering and preprocessing), 63,600 at 32, on a Ryzen 5 7600X (5.4 GHz). That's 15-17× stable-retro, with paired bootstrap intervals. **Parity is with stable-retro's FCEUmm** on CPU RAM, observations, rewards and episode ends, over the `Level1-1`-`1-4` states. Its design: `NromMachine<G: NromGame>`, monomorphised for one game, with no trait objects in the frame loop; the PPU is caught up when the next event is due; **sprite-0 hit at a fixed dot the game supplies** (`PpuTiming::SPRITE0_HIT_DOT`); and **13 native "fast paths" replacing SMB's own routines** (an idle `JMP`, the sprite-0 poll, digit maths, bounding boxes, sprite drawing), each guarded by an exact signature check on the ROM and an equivalence test against the interpreter. A CI check keeps its dependency closure fixed |
| [RLcade](https://github.com/crazyguitar/RLcade) | Apache-2.0 | A PyTorch RL framework with a Rust NES core and PyO3; 5 mappers | No validation or speed published; the core's origin isn't stated |
| [tetanes-py](https://pypi.org/project/tetanes-py/) 0.1.9 (2025-09) | MIT or Apache-2.0 | Bindings for TetaNES, headless, one environment, a Gymnasium example | A general, accurate emulator, not batched; wheels for x86-64 Linux, macOS arm64 and Windows, none for aarch64 Linux |

**[NeSLE](https://github.com/hbofz/NeSLE)** (MIT): one CUDA thread a console, CPU, PPU and OAM DMA in one kernel, with a C++ CPU
reference console for parity. Its 6502 is gated on Klaus Dormann's functional test, and its table-driven decoder
matched the previous interpreter over 8M random instructions (results, bus traffic and cycles). A single
environment on the GPU runs at 0.4× its CPU emulator. GPU backends are out of this project for now, so its
design carries over and its fast path doesn't.

**What this changes from the analysis.** The analysis estimated 15-25× nes-py a core with no prior
measurement. Turbo-emu's 41,600 frames/s on a fast desktop core, against nes-py's 1,075 on `stone`, supports the order
of magnitude. Turbo-emu does rendering we skip, and fast paths we don't build at first (D8), and
our cores are slower (`stone`'s i7-1255U, `klip`'s 3700U). So the estimate becomes **10-25× a core,
before fast paths**, still an estimate until E7. It also shows **a cheap win the analysis missed:** SMB's main
program, after its start-up, is an endless `JMP` to itself, and all of a frame's work runs in the NMI
handler. So the time spent idling is skipped by jumping the cycle counter to the next event (D8).

### Test suites

| Suite | Licence | What it checks | Use |
|---|---|---|---|
| [SingleStepTests 65x02, `nes6502/v1`](https://github.com/SingleStepTests/65x02) | MIT | the 2A03's 6502 (decimal mode off): 10,000 random cases an opcode, every cycle's bus access (address, value, read or write), and the state before and after | **the CPU's main gate** (E2): the 151 official opcodes, about 640 MB of JSON (1.08 GB for all 256) |
| nestest (kevtris), with its log | unstated | every official opcode in sequence, with a cycle count on each line | E2 and E3: cycle-exact against the log from `$C000` |
| blargg's `instr_test-v5` (`official_only`), `ppu_vbl_nmi` (10 tests), `sprite_hit_tests_2005.10.05` (11 tests), and `cpu_dummy_reads`, `ppu_read_buffer`, `oam_read` if headless | unstated | instructions on the real memory map; VBlank and NMI to the PPU dot, races included; sprite-0 hit's rules and timing | E3, read through `$6000` (v5 and later) or the nametable's text, with no pixels |
| Klaus Dormann's functional test | GPL-3.0 | the 6502 broadly, decimal mode included | **not used:** the prebuilt binary tests decimal mode, which the 2A03 lacks, and SingleStepTests cover more |

These come from [christopherpow/nes-test-roms](https://github.com/christopherpow/nes-test-roms), a collection with no licence file. So
**they're fetched one file at a time by a script, pinned by SHA-256, into a gitignored directory, and never
committed or shipped** (D13). The no-ROM check catches them by header anyway.

### What SMB needs, and the hardware's rules it depends on

The analysis's table stands (NMI at VBlank, sprite-0 hit, the loopy registers, OAM DMA, the controller,
APU registers, official opcodes only). The research adds the exact rules, from the NESdev wiki:

- **VBlank:** set at scanline 241, dot 1; cleared at dot 1 of the pre-render line (261), with sprite 0 and overflow.
  **The race:** reading `$2002` one dot before the set reads it clear and suppresses that frame's NMI;
  reading on the set dot or one after reads it set, clears it, and still suppresses the NMI; two or
  more dots away is normal. `ppu_vbl_nmi` tests this to the dot.
- **The odd frame:** with rendering on, odd frames skip one dot (from (339, 261) to (0, 0)), so a frame is
  89,342 dots, or 89,341 on odd frames: 29,780⅔ CPU cycles on average.
- **Sprite-0 hit:** at the first pixel where sprite 0 and the background are both opaque (colour index not 0),
  never at x = 255, not in x 0-7 when either left-clip bit of `$2001` is clear, not with either layer
  off, once a frame at most; priority and palette don't matter. Cleared at dot 1 of the pre-render line.
- **OAM DMA:** 513 CPU cycles after the write to `$4014`, 514 when it starts on an odd cycle.
- **Catch-up** (the NESdev wiki's method): run the CPU ahead, and bring the PPU up to the CPU before
  any access that can see or change it. Events the PPU can predict (VBlank's NMI, a line that could
  hold the sprite-0 hit) bound how far ahead the CPU may run. A write that could change a prediction
  (to OAM, the scroll, the mask) catches up first, then predicts again. **The result must equal
  dot-by-dot stepping, and the test ROMs check that it does.**

### Our side, read before planning

- **indrajala-rl's seams are ready** (the NES plan's D12): `Console` (`ram` as a live view, `power_on`,
  `step(buttons)`, `save`, `restore`) and `Game`/`Episode` (`start`, `begin`, `observe`,
  `after_decision`). `NesEnv`, `VectorEnv` (processes over shared memory) and the trainer's `Rollouts`
  protocol (`reset`, `step`, `records`, `replay`) know no emulator. **A Rust console is one more
  `Console`, and a Rust batch one more `Rollouts`.**
- **nes-py's behaviour, as found from outside it** (`indrajala_rl/console.py`): its native reset is a
  warm boot, so the state after the first reset is saved as power-on; **a frame is a fixed count of CPU
  cycles, not the game's NMI**, so a boundary can fall inside the game's pad read; and its snapshot
  leaves out the pads, which our console saves beside it.
- **The recorded inputs exist:** stage 2.2's driven runs of all 32 levels (`indrajala-studies`'
  `data/nes-levels/`), 20,314 decisions with 26 replayed clears, about 100,000 frames with the skips.
  The evaluation's controls (4.1) and seeded random play add more.
- **indrajala-math-rust's patterns:** Rust 1.98.1 pinned (`rust-toolchain.toml`), edition 2021, PyO3
  0.29, maturin 1.15.0, `PyBuffer` for one-copy numpy input (D13's `from_buffer`), and a thread pool with
  no dependencies (`sys/pool.rs`). Two extension modules each link their own copy of a crate, so a
  second module can't share that pool (D11).
- **The second oracle is installable:** `stable-retro` 1.0.1 has a CPython 3.14 x86-64 wheel. Its FCEUmm
  core is GPL, so it's **run, never read** (D7, D19).

## Decisions

Each has its options with pros and cons; the chosen one is marked.

- **O1. The go** (the owner, 2026-11-06). Build now, while D18 runs, ahead of D10's reading at 3.4, which
  still gets made, from D18's timings. The NES plan's runs stay on nes-py until E6's gates pass. After that a
  run may use either console, as the two give the same bits by construction and test (E6). The gate's
  registration (4.2) names the console it uses.

- **D1. Build or adopt.**
  - (a) *Chosen.* **Our own emulator**, built to this plan, with turbo-emu (MIT) as the closest design
    reference and TetaNES, pinky (Apache-2.0) and takahirox/nes-rust (MIT) for structure. Pros: bit parity
    with nes-py, which every reading so far rests on; D12's seams in our shape; per-access CPU timing
    and a general sprite-0 hit, so a second NROM game isn't blocked; code we understand and can defend. Cons: the
    most work, about 3 weeks at the plan's rate; the verification is ours to do.
  - (b) Depend on turbo-emu's package. Pros: working and fast today. Cons: its parity is with FCEUmm, not
    nes-py, so every reading would need redoing or reconciling; its API is a Gymnasium vector environment
    with its own episode, reward and preprocessing, which duplicate our game layer; no aarch64 Linux
    wheel; sprite-0 hit fixed for SMB; one maintainer, four months old.
  - (c) Fork turbo-emu's NROM core (about 4,100 lines). Pros: a head start on the CPU and PPU. Cons: the
    head start is the cheap part: the verification is the cost, and it applies in full to inherited code;
    its CPU is stepped by instruction, so it can't pass SingleStepTests' bus checks without a rewrite; the
    renderer, FCEU state loader and fast paths would have to be removed first.
  - (d) TetaNES's core as a dependency. Pros: general and accurate. Cons: draws every frame and keeps a
    general emulator's state, so most of the gain is lost; not batched; not designed for our seams.

- **D2. The repository.**
  - (a) *Chosen.* **`indrajala-nes`, new, private until publication, MIT**, a Cargo workspace of three crates:
    `nes-core` (CPU, PPU, bus, cartridge and `Mapper`, APU trait, console, the `Game` trait, idle skip;
    no dependencies, `#![forbid(unsafe_code)]`); `nes-smb` (SMB's game layer, the only game-specific
    code); `nes-python` (PyO3, the module `indrajala_nes`, the only `unsafe`, for buffer views).
    indrajala-rl takes it as a submodule, `nes/`, built by maturin as `ml/rust` is. Pros: the NES plan's D7
    (b), stage E's own choice; the core publishable alone later; the seams are crate boundaries, so they're
    enforced by the compiler. Cons: one more repository to pin.
  - (b) Inside indrajala-rl. Cons: Rust and its CI in a Python repository; the core can't be reused or
    published alone.
  - (c) Inside indrajala-math-rust. Cons: a NES in a maths crate, against D12 and that crate's scope.

- **D3. The CPU's timing.**
  - (a) *Chosen.* **One bus access a cycle**, every access through the bus (the dummy reads and writes
    included), a cycle counter advanced on each. Pros: SingleStepTests checks exactly this, so the CPU is
    verified cycle by cycle; a `BIT $2002` sees the PPU at the cycle it actually reads; dummy reads of
    `$2002` or `$2007` have their side effects, as on the hardware; costs little over (b), as the
    counter is an add and catch-up happens only on PPU accesses. Cons: more care per opcode than
    (b).
  - (b) Stepped by instruction, with the cycles added at the end (turbo-emu's way). Pros: simpler. Cons: a
    register read can be off by up to 3 cycles (9 dots), which matters at the VBlank race and the
    sprite-0 poll; it can't be checked against bus traces.

- **D4. The PPU's sync.**
  - (a) *Chosen.* **Catch-up to the exact dot by predicted events.** The PPU's state at any dot is computed
    from its last sync. It's brought up to the CPU's cycle before any PPU register access, at the
    next predicted event (VBlank's set and NMI, the sprite-0 hit's dot, the pre-render clear, the frame's
    end), and at the boundary. No frame buffer. The loopy `v`/`t`/`x`/`w` registers are kept exactly, with the
    increments rendering applies (coarse x every 8 dots, y at dot 256, horizontal copy at 257, vertical at
    280-304), computed in bulk over a caught-up span. Pros: the fastest exact choice (262 lines
    and a handful of events a frame, against 89,342 dot steps); the result equals dot stepping by
    construction, checked by the test ROMs. Cons: the span arithmetic is subtle; mistakes show only
    as timing errors, which is why the PPU's tests come before SMB.
  - (b) Step every dot. Pros: the simplest to get right. Cons: 89,342 steps a frame, about half of a
    frame's cost at a few nanoseconds each, which halves the gain.
  - (c) Catch-up by scanline only. Cons: not exact within a line: the VBlank race and the sprite-0 dot
    need finer timing.

- **D5. Sprite 0.**
  - (a) *Chosen.* **Computed:** when rendering is on and sprite 0 is in range, its 8 or 16 rows are overlapped with the
    background under the scroll in effect on each line, applying the rules above (x = 255, left clip,
    opaque only), giving the hit's dot. Predicted at the start of each line that could hold it, and predicted again
    after any write that could move it (OAM, `$2000`, `$2001`, `$2005`, `$2006`, the nametable or
    pattern memory under it). Pros: hardware behaviour, so any NROM game works and `sprite_hit_tests`
    can pass; no constant for SMB. Cons: about a day more than (b).
  - (b) A fixed dot the game supplies (turbo-emu). Pros: trivial, and right for SMB, whose sprite 0 doesn't move.
    Cons: wrong for any other game and for the tests, so it's a game's knowledge inside the PPU, against D12.

- **D6. The frame boundary.** `step_frame(buttons)` ends where a "frame" ends. What matters for parity is
  nes-py's definition: a fixed count of CPU cycles, from a phase set at power-on.
  - (a) *Chosen.* **Two modes, nes-py's the default.** `Boundary::Cycles { per_frame, phase }`, with
    the count and phase **measured at E5** from outside nes-py (RAM after N frames from power-on,
    compared over candidate counts and phases until one matches everywhere), and `Boundary::VBlank`, the
    hardware's natural frame, kept beside it for games and tests with no nes-py history. Pros: bit parity, so training
    gives the same bits on either console (O1); the hardware mode costs a comparison. Cons: the
    default copies a quirk (a boundary can fall inside the pad read), kept deliberately and stated.
  - (b) VBlank only. Cons: no frame-by-frame parity with any recorded run; every reading on nes-py
    would differ in the bits.

- **D7. The oracle.**
  - (a) *Chosen.* **nes-py, as a black box, on recorded console calls.** A `RecordingConsole` in indrajala-rl
    wraps `NesPyConsole` and logs every call (`power_on`, `step(buttons)`, `save`, `restore`) with the RAM
    after each frame. The Rust side replays the log through its own console and compares RAM every frame.
    Recorded: 2,000 idle frames from power-on; every level's start (`SMB.start`); the 32 driven runs through
    `NesEnv` (resets by restore and the skips included); seeded random play with sticky actions; the 4.1
    controls. **Pass: no divergence on any frame of any trace.** If one is found where nes-py looks wrong,
    **stable-retro's FCEUmm is run as a second black box** on the same inputs. If FCEUmm agrees with ours, the
    divergence is recorded as nes-py's, and the owner decides whether ours copies it or the runs move to
    the hardware's behaviour. Pros: RAM is all the game and the network see; the whole stack's calls are tested,
    not just frames. Cons: traces of about 200 MB raw (2 KB a frame), kept compressed and gitignored.
  - (b) FCEUmm as the only oracle (turbo-emu's choice). Cons: breaks continuity with every nes-py reading.

- **D7, amended by O3** (the owner, 2026-11-06, after E5b's first readings, Findings). nes-py ends a frame every 29,781
  CPU cycles, and its CPU-PPU timing isn't the hardware's: on two development traces, 3-10% of frame ends had
  RAM unlike nes-py's under the best phase (all transient), with either timing model. Asked whether FCEUmm was
  practical, then: "let's swap over, it's clearly the correct move", and on the ROM, "if we need to swap roms
  I don't mind ... but only if its best".
  - **The oracle is FCEUmm,** through stable-retro 1.0.1's low-level `RetroEmulator` (any ROM file; the pad,
    a frame, state, RAM), run as a black box (GPLv2, never read). A `FceummConsole` in indrajala-rl behind the
    `Console` protocol, so `RecordingConsole`, `record_traces.py` and `nes-trace` serve unchanged.
  - **Our console is judged in its hardware timing** at FCEUmm's frame boundary, measured as nes-py's was.
    The experimental instruction-granular timing (E5b's draft) is dropped.
  - **The ROM: the canonical dump,** the one stable-retro's SMB integration hashes (`rom.sha`) and
    turbo-emu names. Ours differs from both (SHA-1 `ab30029e…`, headerless CRC32 `9A2DB086`). The canonical
    dump makes stable-retro's SMB data work as shipped, turbo-emu a third emulator to cross-check, and results
    comparable with others'. The owner supplies it; it's checked against stable-retro's hash before use.
  - **Redone:** stage 2.2's level table and driven runs on the new dump; runs made on nes-py stand as made,
    and are redone on our console where the plan needs them.
  - **Machines:** stable-retro has no aarch64 Linux wheel, so FCEUmm runs on x86 only (`pyramidon`, `stone`,
    `klip`); `litshe` runs our emulator (E9's check that its bits equal x86's).
  - stable-retro's wheel ships one game image, *Airstriker* (homebrew, non-commercial, by Electrokinesis via
    pdroms.de); it's installed only in a scratch venv, never in a repository.

- **D8. Idle skip.**
  - (a) *Chosen.* **Generic and exact:** when the CPU is about to execute a `JMP abs` whose target is its own address
    (and later a branch to itself, if a trace shows one), with no interrupt pending, the cycle
    counter jumps to the next event in 3-cycle steps. That leaves the same CPU, PPU and RAM state as stepping it. A test runs
    every trace with the skip on and off and compares. Pros: SMB idles most of each frame in its
    `EndlessLoop`, so this may be the largest single gain; nothing in it knows SMB. Cons: one more
    path to verify.
  - (b) Native replacements of SMB's routines (turbo-emu's 13 fast paths). Pros: more speed. Cons: game
    code re-implemented in Rust, each with a signature guard and an equivalence test; a maintenance cost per
    game. **Not planned:** revisited only if E9 shows the emulator is still the bottleneck.

- **D9. The state.**
  - (a) *Chosen.* **Plain data:** CPU registers, 2 KB RAM, 2 KB nametable RAM, 32 B palette, 256 B OAM,
    PPU registers and timing, the controller's shift state, the APU's few registers, cycle counters, and
    the mapper's state (none for NROM): about 5 KB, in one `Clone` struct, so a save or a reset is a copy.
    **The ROM isn't in it:** it's shared by `Arc` across consoles. A byte form with a version number
    serialises it explicitly, field by field, for checkpoints. Pros: reset by copy (the analysis's design),
    checkpoints without replay become possible, and `unsafe` isn't needed. Cons: the byte form must change with the
    struct, so it carries a version number and a round-trip test.

- **D10. The Python boundary.**
  - (a) *Chosen.* **Two steps.** First (E6) a **drop-in `Console`** in `indrajala_nes`, with `ram` a live
    numpy view and `save` returning bytes, so `NesEnv`, `VectorEnv` and every existing test run on it unchanged, and
    parity is checked through the whole stack. Then (E7) **measure** where the rollout's time goes now
    (emulation, Python per decision, process round trips, the network). Then (E8) the **Rust batch**: N
    consoles and SMB's episode, observation and skips in Rust (`nes-smb`), one call a decision for all
    environments, observations written into the caller's arrays. E7's measurement sets its shape: how much of the
    environment moves to Rust, and whether one process or several. Pros: parity and a gain early, with low
    risk; the batch built against measured costs, not guesses (existence first). Cons: SMB's episode
    logic then exists twice, Python's the reference and Rust's tested against it bit for bit.
  - (b) The batch straight away. Cons: parity, threads and game logic debugged at once; no measurement to
    shape it.
  - (c) The drop-in only. Cons: Python then runs per decision for each environment, plus a round trip
    per step. At 10-25× emulation that's likely most of the rollout (E7 measures it).

- **D11. The threads.**
  - (a) *Chosen.* **`std::thread::scope` each batch step, with workers claiming consoles from an atomic
    counter.** No dependency, no threads left idling while the network trains, and claiming evens out
    `stone`'s performance and efficiency cores (D15's finding there). The consoles are independent, so the
    bits don't depend on which thread runs one. Persistent workers replace it only if E8 measures thread start-up above
    2% of a step. Pros: simplest; nothing spins while the crate's pool works. Cons: about 10-20 µs
    a thread a step, to be measured.
  - (b) Rayon (turbo-emu's choice). Pros: mature work stealing. Cons: a dependency, and an idle pool
    that spins briefly beside the crate's.
  - (c) Share indrajala-math's pool. Cons: impossible across two extension modules (each links its own
    copy).

- **D12. Sticky draws.**
  - (a) *Chosen.* **Drawn in Python by each environment's own numpy generator, as now, and passed in** with the
    actions (one float an environment a step). Pros: the same bits as `NesEnv` for a seed, so the two backends
    can be compared run against run; `EpisodeRecord` and replay keep working. Cons: a small array crossing per
    step.
  - (b) A generator in Rust (stage E's first sketch). Cons: different streams, so no run-for-run comparison.

- **D13. Test data.**
  - (a) *Chosen.* **SingleStepTests' official opcodes in CI** (about 640 MB, fetched by a script pinned to a commit,
    cached), and a fixed 1,000-case subset per opcode for local runs. **blargg's ROMs and nestest fetched one file at a
    time by `scripts/fetch_test_roms.py`, each pinned by SHA-256, into gitignored `test-roms/`, never
    committed** (their licences are unstated). Tests that need them skip, with a message, when the files are
    absent. Pros: strong gates at no licence risk. Cons: CI depends on two external sources,
    covered by caches and by pinned hashes that fail loudly.

- **D14. The machines** (amended by O2). **Development on `pyramidon`, its emulation included:**
  building, clippy, the unit tests, the test ROMs and SingleStepTests' subset, and short SMB checks while
  building (booting, a driven run, a trace's first divergence). The owner (O2): "you can run emulation on
  pyramidon as part of development - the idea of the restriction is to prevent unrelated work gumming up
  development - but if the work is development in effect then thats fine". `pyramidon`'s rules still hold: one heavy
  job at a time, no swap, memory estimated first. **On runners** (`klip`, `stone`): recording the parity traces
  (E5a, as they come from nes-py's runs), the full parity sweep, the measures (E7, E9) and anything a finding
  rests on, **after D18 ends**, so its timings, which 3.4 reads, stay clean. CI runs everything that needs no
  SMB ROM, on x86-64 and on GitHub's arm64 runner. The SMB ROM comes from `~/roms`, SHA-1 checked, everywhere.

- **D15. Sound later.** `Apu` is a trait. `SilentApu` takes every write and answers `$4015` (length-counter
  bits zero, the frame interrupt's flag as the frame counter sets it) and `$4017`'s mode. E4's trace
  checks that SMB never enables DMC, takes an IRQ, or reads APU state beyond `$4015`. Sound is a new
  implementation (the analysis: about a week), with no change to the CPU, PPU or mapper.

- **D16. The mapper seam.** `trait Mapper { cpu_read, cpu_write, ppu_read, ppu_write, mirroring }` (and later
  an IRQ line), with the console generic over it: `Console<M: Mapper, A: Apu>`. `Nrom` is the only implementation, with
  the header's mirroring and optional PRG RAM at `$6000` (which blargg's tests use for their status, not
  SMB). The Python module names the concrete type once, so no virtual call reaches the frame loop. A second mapper is a new
  type and its tests.

- **D17. The game seam.** `nes-core` defines `trait Game` (the ROM's hash, the level starts, the action
  buttons, `observe(ram, ids, values)`, an episode's `after_decision`), and `nes-smb` holds SMB's, ported
  from indrajala-rl's `games/smb.py` with each address's source and check carried across. **The core holds no
  RAM address and no game's terms.** A CI script checks that `nes-core` depends on nothing and that no
  game crate is a dependency of it (turbo-emu's dependency-closure check, in small). The Python layer stays the
  reference: Rust's observations and outcomes are tested bit for bit against it on every trace (E8).

- **D18. Every machine's bits.** The emulator is integer arithmetic only, with no SIMD and no floats (the observation's
  floats are copies of small integers), so its bits can't depend on the machine. CI tests on x86-64 and
  arm64; E9 replays every trace on `litshe` (aarch64), which also makes it a possible runner, and the Pi 4
  a playback machine (the NES plan's D9).

- **D19. Sources and licences.** The hardware's behaviour comes from the NESdev wiki. MIT and Apache-2.0
  code (turbo-emu, TetaNES, pinky, takahirox/nes-rust, NeSLE) may be read and adapted, with its notice kept
  in `NOTICE` and at the adapted code. **Never read:** nes-py's C++ (derived from GPL-3.0 SimpleNES,
  provenance unresolved), SimpleNES, Mesen2, FCEUX, FCEUmm, starrhorne/nes-rust (all GPL). They're run
  only, as oracles.

## Stages

Each stage is one or more PRs, each merged on green CI before the next starts, with nothing stacked. A stage that changes
indrajala-rl needs the `indrajala-nes` PR merged first and a submodule bump. Times are building estimates
at the plan's rate (stages 2.3-3.3 took a day against five estimated; these aren't lowered for that).

### E0: this plan (indrajala-research)

This workplan; the NES plan's D4 and D10 amended (the owner's go, O1) with stage E pointing here; the
workplans README. **Done when** merged.

### E1: the repository and the cartridge (indrajala-nes)

- **Scaffold:** the workspace (D2), `rust-toolchain.toml` at 1.98.1, `rustfmt.toml`, MIT `LICENSE`,
  `NOTICE`, `README.md`, `CLAUDE.md` (the workflow and the ROM rules, as indrajala-rl's), a
  `.gitignore` for `*.nes`, `test-roms/` and `traces/`.
- **CI:** `cargo fmt --check`; `cargo clippy --workspace --all-targets -- -D warnings`; `cargo test` on
  `ubuntu-latest` and `ubuntu-24.04-arm`; `scripts/check_no_roms.py` (indrajala-rl's, copied); the
  dependency check (D17).
- **The cartridge:** an iNES parser (header, mapper number, mirroring, PRG and CHR sizes, trainer, NES 2.0
  recognised and refused unless it's plain NROM), `trait Mapper`, `Nrom` (16 or 32 KB PRG mirrored,
  8 KB CHR ROM, or CHR RAM when the header gives none; PRG RAM optional).
- **Tests:** iNES images built in the test from bytes (no ROM file); mirroring; a planted `.nes`
  fails the check. **Time:** ½ day.

### E2: the CPU (indrajala-nes)

- `cpu.rs`: the registers, a decode table, the 13 addressing modes with their dummy accesses, the 151
  official opcodes with page-cross and branch penalties, the stack, NMI on its edge and IRQ on its level, `BRK`,
  interrupt hijacking (an NMI during `BRK`'s or an IRQ's push takes the NMI vector), the one-instruction delay of
  `CLI`, `SEI` and `PLP`; **an unofficial opcode traps**, returning an error with the CPU's state, never
  running on silently.
- `trait Bus { read(addr, cycle), write(addr, value, cycle) }`, one call a cycle (D3).
- **Gates:** SingleStepTests `nes6502/v1`, all 10,000 cases of every official opcode: the final state and **every
  cycle's bus access**; each of the 105 unofficial opcodes traps; nestest from `$C000` (its automated mode) matches its log
  line for line (PC, A, X, Y, P, SP, cycles) through the official section.
- **Time:** 2-3 days.

### E3: the bus and the PPU (indrajala-nes), two PRs

- **E3a, timing and registers:** the CPU's memory map (RAM mirrors, PPU registers mirrored every 8 bytes,
  `$4000-$4017`, the cartridge); the PPU's registers (`$2000-$2007`): the loopy model, the `$2007` read buffer and
  its palette exception, the increments of 1 or 32, the data bus latch for `$2002`'s low bits, write-only registers
  reading the latch; nametable RAM through the mapper's mirroring; palette RAM with its mirrors; the catch-up
  engine (D4) with VBlank, NMI (its race and suppression, NMI on enabling `$2000` bit 7 during VBlank), the pre-render clear
  and the odd frame's skipped dot. The harness for test ROMs: run to completion, read `$6000`'s status and its
  text, or the nametable's text.
  **Gates:** `ppu_vbl_nmi` 01-10; `instr_test-v5` `official_only`; nestest's ROM in normal mode;
  `ppu_read_buffer` and `cpu_dummy_reads` if they run headless (a test needing pixels is listed
  as not run, with why). **Time:** 2-3 days.
- **E3b, sprites and DMA:** OAM and `$2003`/`$2004`; `$4014` DMA, 513 or 514 cycles by the cycle's parity, with the
  CPU halted; the sprite-0 hit computed and predicted (D5), with 8×16 sprites, flips and the clipping rules.
  **Gates:** `sprite_hit_tests_2005.10.05` 01-11, `oam_read`. **Time:** 1-2 days.

### E4: the console and SMB's boot (indrajala-nes)

- **The controller** (strobe, the shift register, bits 5-7 from the open bus as the hardware's), **`SilentApu`**
  (D15), **power-on** (RAM zeroed, as nes-py's power-on state is matched at E5), reset, **the state** (D9) with
  its byte form, **`step_frame(buttons)`** in both boundary modes (D6; nes-py's count is a placeholder
  until E5), and **idle skip** (D8) behind a switch.
- **On `pyramidon` (development, D14):** SMB boots to its title and enters 1-1 by `SMB.start`'s inputs; replaying 1-1's driven
  run in the hardware mode reaches the flagpole (by RAM, `Player_State` 3). **A trace audit:** no unofficial
  opcode, no IRQ taken, `$4015` bit 4 (DMC) never set, the APU addresses read listed; and SMB's idle `JMP` found,
  with the share of cycles it takes (the skip's gain) measured.
- **Gates:** the above; a state round trip (bytes back to the same state, then the same frames); the skip on
  against off on 1-1's run, same RAM and cycle count every frame. **Time:** 1-2 days.

### E5: parity with nes-py (indrajala-rl, then indrajala-nes)

- **E5a, the recorder (indrajala-rl):** `RecordingConsole` (D7) and `scripts/record_traces.py`, writing
  each trace as its calls and RAM a frame (zstd-compressed `.npz`), with a manifest, into indrajala-studies'
  gitignored `data/nes-parity/`. Recorded on a runner: power-on, the 32 starts, the 32 driven runs, 20 random
  episodes on 1-1 and 4 on each other level with sticky actions, the two 4.1 controls. **Time:** ½ day.
- **E5b, the comparison (indrajala-nes):** `nes-trace`, a binary that replays a trace and stops at the first
  divergence, printing the frame, the differing addresses and bytes, the CPU's state and the PPU's dot.
  **First the boundary:** nes-py's cycles a frame and phase, and its power-on state (registers, RAM, PPU),
  measured from the power-on trace and fixed as the default (D6). **Then every trace.**
- **Gate (amended by D20, O4; the sub-plan `nes-emulator-parity-workplan.md`):** every oracle frame reached
  by our run, in order, within ±114 cycles of our frame end, the offsets reported; timing judged against
  Mesen's write log (D22). **Was:** no divergence on any frame of any trace. **If not:** each divergence is diagnosed; where nes-py
  looks wrong, FCEUmm's verdict is taken (D7) and the case goes to the owner with both readings. **Time:**
  3-6 days, the uncertain part.

### E6: the drop-in console (indrajala-nes, then indrajala-rl)

- **indrajala-nes:** `indrajala_nes.Console(rom_bytes, boundary=...)`: `ram` as a numpy `uint8` view of the
  state's RAM (buffer protocol; valid while the console lives); `power_on`, `step`, `save` (bytes),
  `restore`; a type stub. **CI** builds the wheel and runs a Python smoke test on a synthetic iNES image.
- **indrajala-rl:** the submodule `nes/`; `./cli setup` builds it; `RustConsole` in `console.py` (the
  ROM checked, then passed as bytes); a `--console {nes-py,rust}` option in `scripts/train.py`,
  `evaluate.py`, `feasibility.py`, `drive_levels.py` and the probe; the boundary test still passes.
- **Gates, on a runner:** every `emulate` test on both consoles; **the same `Step`s and observations** as
  nes-py over the 32 driven runs; the vector runner's bit test on the Rust console; **a 2-iteration PPO run
  on 1-1 whose log, network file and trainer state equal nes-py's, bit for bit**; resume equal to a
  run never stopped. **Time:** 1-2 days.

### E7: the first measure (indrajala-rl, indrajala-research)

- `scripts/probe_throughput.py` with `--console rust`: emulation alone (frames/s a core, skip on and off),
  then a PPO iteration on 1-1 at D3's settings on `stone` and `klip`, split into emulation, Python
  a decision, the runner's round trips, and the network. Readings go in a manifest in `data/nes-probe/rust/`
  and the Findings below. No speedup is claimed against `jebel`'s protocol (it's out); these are working
  readings on the runners, as D10's first was.
- **It decides E8's shape** (D10): how much of the environment moves to Rust, and one process or
  several. **Time:** ½ day.

### E8: the batch (indrajala-nes, then indrajala-rl), three PRs

- **E8a, SMB in Rust (`nes-smb`):** `Game` and `Episode` for SMB: the level starts, the actions, the skips,
  the reward, the clear and the death, and `observe` into caller-owned id and value buffers.
  **Gate:** on every E5 trace, Rust's observation, outcome and progress equal `games/smb.py`'s bit for bit,
  decision by decision. **Time:** 1-2 days.
- **E8b, the batch (`nes-core`, `nes-python`):** `Batch` of N consoles at one level: `reset(mask)`,
  `step(actions, sticky_draws)` (D12) writing ids, values, reward, terminated, truncated, cleared, taken, progress
  and the final observation into numpy arrays, with the reset-on-end semantics of `VectorEnv`; threads
  per D11; `save` and `restore` per console for records. **Gate:** a batch of N equals N single
  `NesEnv`s on the Rust console, bit for bit, over 1,000 random decisions; at 1 to 8 threads, the same
  bits. **Time:** 1-2 days.
- **E8c, `RustRollouts` (indrajala-rl):** a `Rollouts` over the batch, the history of value planes kept as
  `NesEnv` keeps it, `records` and `replay` as now. **Gates:** a PPO run of 2 iterations equals the
  `VectorEnv` run on nes-py, bit for bit; resume equal. **Time:** 1 day.

### E9: the measure, and D10's reading again (indrajala-research)

- E7's measures repeated on the batch, on `stone`, `klip` and `litshe` (one core, at most 70 C). Every E5
  trace replayed on `litshe` with no divergence (D18). The NES plan's budget table is updated with the numbers before and after,
  and D10 is read again. **What's next is decided then:** fast paths (D8 (b)), the network, or nothing.
  **Time:** ½ day.

**Total: about 15-21 days at the plan's rate**, a little over the analysis's 13-18 days. The difference is
E5's recorder, E6's drop-in, and the measured step between them.

## The execution plan, PR by PR

| # | Repository | PR | Done when |
|---|---|---|---|
| E0 | indrajala-research | This workplan; NES plan D4/D10 and stage E amended; README | merged |
| E1 | indrajala-nes (new, private) | Scaffold, CI, iNES, `Mapper`, `Nrom` | CI green on x86-64 and arm64; a planted ROM fails |
| E2 | indrajala-nes | The CPU | SingleStepTests official (state and bus), unofficial traps, nestest's log |
| E3a | indrajala-nes | Bus, PPU timing and registers, test-ROM harness | `ppu_vbl_nmi`, `instr_test-v5` official, nestest ROM |
| E3b | indrajala-nes | OAM, DMA, sprite-0 hit | `sprite_hit_tests`, `oam_read` |
| E4 | indrajala-nes | Console, controller, `SilentApu`, state, boundary, idle skip | SMB boots and clears 1-1's driven run; audit; skip equivalence |
| E5a | indrajala-rl | `RecordingConsole`, `record_traces.py` | traces in `data/nes-parity/` with a manifest |
| E5b | indrajala-nes | `nes-trace`; nes-py's boundary and power-on matched | no divergence on any trace, or the owner has the cases |
| E6 | indrajala-nes, then indrajala-rl | `indrajala_nes.Console`; submodule, `RustConsole`, `--console` | stack parity; a PPO run equal to nes-py's bit for bit |
| E7 | indrajala-rl, indrajala-research | Probe on Rust; Findings | the rollout's time split, on `stone` and `klip` |
| E8a | indrajala-nes | `nes-smb` | Rust's observations and outcomes equal Python's on every trace |
| E8b | indrajala-nes | `Batch`, threads, PyO3 | batch equals N single envs; same bits at 1-8 threads |
| E8c | indrajala-rl | `RustRollouts` | PPO run equal to `VectorEnv` on nes-py's; resume |
| E9 | indrajala-research | Measures, `litshe`, D10 again | Findings and the budget table; **to the owner** |

**Order.** E1-E4 need no runner, so they go first, while D18 runs; E5a onward use a runner after D18 ends.
The NES plan's work (D18's result, 3.4, 4.1 and the gate's probes) is fitted between them; the runners
are shared, and the gate's runs take priority on them.

**The owner hears at:** E5 if any divergence needs a choice; E9's readings; and at once if
anything here proves false.

## Not planned

- **Fast paths** for SMB's routines (D8 (b)): only if E9 calls for them.
- **Checkpoints holding console states** in place of replay: the byte form makes it possible (D9). The
  trainer's checkpoint format changes only if replay becomes a measured cost.
- **Pixels, sound, other mappers and other games:** each is a new implementation behind its seam,
  when wanted.
- **Turbo-emu as a peer benchmark:** it could be timed on the same runner as context, never as a claim.
  Optional, at E9.

### E5's and E6's gates on `klip` (2026-11-06)

On `klip`, indrajala-rl `d2b4952` with `nes/` at `6495440`, the canonical dump; the gate script and its
outputs in indrajala-studies' gitignored `data/nes-emulator-gates/`, the traces in `data/nes-parity/`, each
with its manifest. The guard's peak 50 C.

**E6's gates pass.**
- **The emulate suite:** 239 tests pass on all three consoles, the vector runner's bit test and `NesEnv` on
  Rust against FCEUmm (four levels, every `Step`, observation and RAM) among them.
- **PPO, 2 iterations on 1-1** (8 workers × 1 environment, split networks, seed 30, `--backend rust`):
  `--console rust` and `--console fceumm` give **the same `log.jsonl` (bar timings), `network.json` and
  `trainer.json`, bit for bit**; their configs differ only in `console`.
- **Resume:** a Rust run of 1 iteration resumed to 2 equals the 2-iteration run in all three files.
- Not yet: the `Step`s over the 32 driven runs, which wait for stage 2.2 on the canonical dump.

**E5's gate is not met: 3 frames of 97,079 unequal.** `record_traces.py --console fceumm` (34 traces:
power-on, random play on every level, the right-jump control), then `nes-trace` (line 240, lead 1).
- **All three are the same event:** frame 65 of `random-2-2`, `random-5-3` and `random-7-2`, the title's
  lag frame after START (the frame E5's first readings used to place the boundary), one byte, `$230` (a
  sprite's Y in SMB's OAM buffer), `$00` against `$F8`, both ways round. Frame 66 is equal again, and so is every
  other frame in the set, play included.
- **The cause is the cut, not the state.** In a lag frame SMB is still writing RAM as the frame ends, so
  RAM equals FCEUmm's only in a narrow window of our cycles: here 66 cycles wide (`trace-boundary`, all 34
  traces in `frame65-windows.txt`). In 31 traces the window holds our cut, the first instruction boundary at
  line 240. In `random-2-2` and `random-7-2` it ends one cycle before it, (239, 340); in `random-5-3` it
  starts 13 cycles after it, (240, 38). **No single cut point fits all 34**, if our cycle counts are
  FCEUmm's: so our timing within that frame differs from FCEUmm's by a few cycles, varying with the level's
  code path, invisible to RAM except where a write lands at the cut.
- **Probes, claiming nothing** (a scratch build, `pyramidon`): moving sprite 0's hit (`SPRITE_0_DELAY`, 1
  now) to 0 fixes `random-5-3` and to 8 fixes the other two, so no single delay fits; a cut 3-45 dots before
  line 240 fixes those two and not `random-5-3`; delay 0 with a cut 3 dots early gives 0 unequal, but 1 or 28
  dots early breaks most traces. Two knobs fitted to three frames isn't FCEUmm's rule, and FCEUmm can't be
  read (D19), so nothing was changed.
- **What it means for training:** a frame's RAM differs only at a lag frame's cut, and the next frame is
  equal; it changes a `Step` only if such a frame is one the environment observes. None was in this set, and
  E6's checks were all equal. **Per the gate's rule, the case goes to the owner.**

## Risks

| Risk | Effect | Answer |
|---|---|---|
| nes-py's quirks change RAM | E5 runs long | its boundary and power-on matched first; FCEUmm as the second oracle; the owner decides on copying a quirk |
| Catch-up arithmetic subtly wrong | wrong timing, perhaps only in rare frames | the PPU's test ROMs before SMB; every trace frame by frame; the hang on a missed sprite 0 is loud |
| SMB uses something "not needed" | drift | unofficial opcodes trap; E4's audit of IRQ, DMC and APU reads |
| The test ROMs' terms | can't be committed | fetched by script, pinned, gitignored |
| The gain smaller than estimated | under D10's 1.5× | E7 measures before E8 is shaped; the other gains (serialisable state, no pad bug, aarch64, no nes-py dependency) stand anyway |
| Learning, not emulation, is the bottleneck | the gain capped near 1.8× at today's network | expected (the analysis, NeSLE's notes); the network is the next work, which E9 names |
| Runner time shared with the gate | stage E slows | the gate's runs go first; E1-E4 need no runner |

## Findings

### E1-E4 (2026-11-06, indrajala-nes #1-#5)

Every gate passes in CI on x86-64 and arm64 unless noted.

| Stage | Gate | Result |
|---|---|---|
| E1 | the cartridge; a planted ROM fails the check | passed; 16 tests on iNES images built from bytes |
| E2 | SingleStepTests `nes6502/v1`, the 151 official opcodes, state and every cycle's bus access | **all 1,510,000 cases pass**; a mutation (an indexed write's dummy read dropped) fails 18 opcodes |
| E2 | the 105 unofficial opcodes trap | each traps after its fetch alone |
| E2 | nestest from `$C000` against its log | the 5,003 official lines match (PC, A, X, Y, P, S, cycles); trap at `$C6BD`; result bytes zero |
| E3a | `ppu_vbl_nmi` 01-10, to one PPU dot | **all pass** |
| E3a | `instr_test-v5` | 01 and 10-16 pass; 02-09 report no failure before their first unofficial opcode, where the CPU traps; `official_only` is MMC1, not run |
| E3a | catch-up against a dot-by-dot reference | equal over 8 seeds of 12 frames with random writes; a mutation fails it |
| E3b | `sprite_hit_tests_2005` 01-11, `oam_read` | **all pass**; with no hit, 01-10 fail; with the hit 10 dots late, 09 and 10 fail (11 checks only lateness) |
| E4 | `cpu_interrupts_v2` 1-5 | **all pass** (once the frame IRQ was at cycle 29828) |
| E4 | idle skip on against off | state bytes equal every frame, 240 frames, both boundaries |
| E4 | SMB boots and plays (on `pyramidon`, development) | **1-1 entered at frame 208** by `start_play`'s inputs; holding RIGHT+B, Mario runs, dies at the first enemy three times, game over, back to the title |
| E4 | the audit, 1,800 frames of SMB | **no unofficial opcode; no IRQ while `I` was clear** (SMB writes `$4017 = $FF`); **DMC never enabled**, though `$4010-$4013` are written; reads in `$4000-$401F`: the pads, and dummy reads of indexed stores |

**Constants the tests fixed:**
- **NMI as a level, sampled 1 PPU dot after the CPU's access.** A pulse with a delivery delay passed 9 of 10 `ppu_vbl_nmi` tests at best. The level passes all 10 with the sample at +1 dot, and fails at 0, 2 and 3. The global CPU-PPU alignment passes at all three phases, so **E5 fixes it against nes-py**.
- **The odd frame decides its skipped dot at dot 338** (339 fails `10-even_odd_timing`).
- **Sprite 0's flag at dot x + 2 for pixel x**, the wiki's figure; the timing tests accept x + 1 to x + 3.
- **The APU's frame flag first set at CPU cycle 29828**, the wiki's figure; 29826, 29827 and 29829 fail `cpu_interrupts_v2` 3-5.

**Findings for later stages:**
- **SMB's idle `JMP` takes 69.9% of its cycles** (1,800 frames, start-up and play). D8's skip removes it exactly.
- **Speed, a development reading on `pyramidon`, no claim:** 8,300 frames/s a core with idle skip, 3,350 without. That's roughly 7-8× nes-py's 1,075 on `stone` (different machines, so indicative only), **below the analysis's 15-25×**. The profile, after catch-up's bulk increments (34% of the time to 5%), is now mostly the CPU's step and bus reads. E7 measures on the runners; E9 decides whether speed work (D8 (b), or the CPU's dispatch) is next.
- **One bug, found by its own test:** idle skip at first jumped over an NMI when a frame ended after the PPU set VBlank but before the CPU sampled it. A guard fixed it, and the test now drives frame ends through every phase of VBlank.

**Amended:** E4's replay of 1-1's driven run to its clear moved to E5/E6, as it needs indrajala-rl's episode logic (the skips between decisions); there it's checked frame by frame against nes-py.

### E5 against FCEUmm, first readings (2026-11-06, indrajala-rl #19, indrajala-nes #8)

Development readings on `pyramidon` (O2); the gate is the full trace set, recorded on a runner.

- **`FceummConsole`** (indrajala-rl #19): FCEUmm through stable-retro 1.0.1's `RetroEmulator`, installed by
  `./cli setup --fceumm` (the wheel, `--no-deps`: stable-retro's pyglet pin conflicts with nes-py's, and
  neither renders here). stable-retro hands out RAM as copies, so the console keeps its own and passes a game
  layer's writes in (`memory.assign`) before each frame and save. **Its state restores exactly** at all 1,500
  frame boundaries tried in play, the pads included; one emulator a process; about 3,300 frames/s.
- **FCEUmm's power-on RAM is all `$FF`**; ours now is too (`POWER_ON_RAM`).
- **Its frame ends at the end of the visible picture, line 240, not at VBlank.** `trace-boundary` gives each
  oracle frame the window of our cycles in which RAM equals it. Every window contains VBlank's start, except
  one lag frame's (random play on 1-1, frame 65, the title turning to play while SMB clears its OAM buffer):
  **(239, 151) to (240, 8)**. With frames ending at VBlank, that frame was unequal (`$22C`, `$230`); with
  `Boundary::Line { line: 240 }`, none is. **FCEUmm's first frame takes in two of ours** (frame k holds our
  (k+2)th VBlank), so our power-on runs one lead frame.
- **Parity, under hardware timing, from our own power-on:** power-on (2,000 frames), random play on 1-1
  (5,293), 1-2 (2,925), 8-4 (693), and the right-jump control on 1-1 (3,829): **14,740 frames, none
  unequal.** nes-py had 3-10% of frame ends unequal under its best phase (D7, amended).
- **The lead frame belongs in the drop-in console** (E6): `indrajala_nes.Console`'s power-on is ours plus one
  frame with no buttons, so its first `step` equals FCEUmm's.

**Next:** the full trace set (`record_traces.py --console fceumm`) on a runner, then `nes-trace` over it;
the driven traces after stage 2.2 is redone on the canonical dump.

### E6, built (2026-11-06, indrajala-nes #9, indrajala-rl #20)

- **`indrajala_nes.Console`** (`crates/nes-python`, PyO3 0.29): `power_on`, `step`, `save` (bytes),
  `restore`, `close`, and `ram`, a live writable numpy view through the buffer protocol (the workspace's only
  `unsafe`). FCEUmm's frame (line 240), lead frame and power-on RAM by default. CI builds the wheel and runs
  smoke tests on a synthetic NROM image on x86-64 and arm64.
- **indrajala-rl:** `nes/` as a submodule built by `./cli setup`; `rust_console` returns the native console
  with no wrapper; `--console {nes-py,fceumm,rust}` in `train.py`, `evaluate.py`, `drive_levels.py`, the
  probe and `record_traces.py`, recorded in their outputs; the default stays nes-py until the gates pass.
  **CI fetches `ml/` only:** indrajala-nes is private, and the Rust console's tests need the ROM anyway.
- **Development readings on `pyramidon` (not the gate):** the emulate suite, 98 tests, passes on nes-py,
  FCEUmm and Rust, the vector runner's bit test included. **`NesEnv` on the Rust console against FCEUmm**
  (1-1, 1-2, 4-4, 8-4; 1,500 decisions each, sticky actions, deaths and resets by restore): **every `Step`,
  observation and RAM equal.** The five E5 traces replayed through the Python module: 14,740 frames equal.

**Next, on a runner:** E5's full trace set; the emulate suite; **a 2-iteration PPO run on 1-1 on the Rust
console equal, bit for bit, to one on FCEUmm** (one environment a worker, as FCEUmm allows one emulator a
process); resume equal to a run never stopped. Then E7.

## Sources

- Prior work: [env-SuperMarioBrosNes-turbo-emu](https://github.com/tsilva/env-SuperMarioBrosNes-turbo-emu) (its
  `ARCHITECTURE.md`, `BENCHMARKS.md`, `SPECS.md`, `CONTRIBUTING.md`, and the outline of
  `crates/nes-turbo-nrom-core/src/machine.rs`), [NeSLE](https://github.com/hbofz/NeSLE),
  [RLcade](https://github.com/crazyguitar/RLcade), [tetanes-py](https://pypi.org/project/tetanes-py/),
  [TetaNES](https://github.com/lukexor/tetanes), [pinky](https://github.com/koute/pinky),
  [takahirox/nes-rust](https://github.com/takahirox/nes-rust); licences checked 2026-11-06 on GitHub and PyPI.
- Tests: [SingleStepTests 65x02](https://github.com/SingleStepTests/65x02) (`nes6502/README.md`),
  [christopherpow/nes-test-roms](https://github.com/christopherpow/nes-test-roms),
  [NESdev: emulator tests](https://www.nesdev.org/wiki/Emulator_tests).
- Hardware: NESdev wiki, [PPU frame timing](https://www.nesdev.org/wiki/PPU_frame_timing),
  [PPU OAM](https://www.nesdev.org/wiki/PPU_OAM), [Catch-up](https://www.nesdev.org/wiki/Catch-up).
- Oracles: [nes-py](https://pypi.org/project/nes-py/) 9.0.1 and its
  [LICENSING.md](https://github.com/Kautenja/nes-py/blob/master/LICENSING.md);
  [stable-retro](https://pypi.org/project/stable-retro/) 1.0.1.
- Our own: the analysis note; the NES plan's stages 0-3 Findings; indrajala-rl's `console.py`,
  `games/base.py`, `env.py`, `vector.py`, `ppo/train.py`; indrajala-math-rust's `sys/pool.rs` and
  `src/array.rs`.
