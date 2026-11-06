# A Rust NES emulator for Super Mario Bros: what it would take

2026-11-06, for the NES plan's stage E (`docs/workplans/nes-one-network-workplan.md`), at the owner's
request: "what it would take for us to develop a rust nes emulator that supports smb (i.e. mapper 0
only) - without sound - which we could optionally add later". It extends stage E's sketch; it decides
nothing. Whether to build is D10's reading at stage 3.4, and the owner's call.

## The answer in brief

- **What:** a headless NES in Rust running SMB's cartridge (NROM, mapper 0): the 6502, a PPU that
  keeps the timing and flags the game reads but draws no pixels, the controller, OAM DMA, and an APU
  that accepts writes and answers the few reads, with no sound. Batched: N consoles stepped from Rust
  on the crate's threads, with SMB's observation decoded in Rust.
- **How much:** about **2-3 weeks of building at the plan's estimating rate**, of which the parity
  work against `nes-py` is the largest and least certain part. About 3,000-4,500 lines with tests.
  (Stages 2.3-3.3 took a day against five estimated, so the real time may be shorter; the estimate
  isn't lowered for that.)
- **What it buys:** emulation about **15-25× faster a core** than `nes-py` (an estimate, from cycle
  counts), but **about 1.8× on a whole PPO iteration today,** because learning is the other half of a
  step (D10's first reading: emulation about 46% of a 16 s iteration on `stone`). Its other gains don't
  depend on D10: a state that serialises (checkpoints without replay), no pad bug, no dependence on a
  package whose core has an unresolved GPL provenance, and native aarch64.
- **The main risk:** bit parity with `nes-py`, the oracle every reading so far rests on. It needs our
  emulator to reproduce `nes-py`'s own frame boundary and cycle accounting, not just the hardware's.
  A fallback is in the verification section.
- **Sound later:** an APU that only accepts writes leaves a clean seam. Adding sound is a new
  `Apu` implementation with no change to the CPU or PPU: roughly a week more, with its own tests.

## What SMB needs from the hardware

SMB is a 40 KB NROM cartridge: 32 KB of program ROM, 8 KB of character ROM, vertical mirroring (its
header says which; the code reads the header, never assumes it). Mapper 0 has no bank switching, so the
cartridge is two fixed memory regions. The hard parts are elsewhere:

| What the game relies on | Why | What the emulator must do |
|---|---|---|
| **The NMI at VBlank** | SMB runs its whole frame from the NMI handler: PPU updates, then game logic | VBlank flag at scanline 241 dot 1, NMI if enabled, cleared at the pre-render line; `$2002` reads clear it |
| **Sprite-0 hit** | the status bar's split: the NMI handler polls `$2002` until sprite 0 (part of the coin icon) hits the background, then writes the scroll for the playfield. **If the hit never comes, the game hangs** ([NESdev](https://nesdev.nes.science/f3/t12185.xhtml)) | compute the first pixel where sprite 0 and the background are both opaque, from the nametable, the pattern tables and the scroll, and raise the flag at that dot. No frame is drawn, but this one overlap is |
| **Scroll and VRAM address writes** | `$2005`/`$2006`/`$2000` share the PPU's `v` and `t` registers, mid-frame included | the loopy `v`/`t`/`x`/`w` model exactly, as the NESdev wiki gives it |
| **OAM DMA** (`$4014`) | sprites copied every frame | 256 bytes copied, and the CPU stalled 513 or 514 cycles, as the timing after it depends on it |
| **The controller** | strobe and serial reads at `$4016` | the shift register, **saved with the state** (`nes-py` doesn't, found at stage 2.2) |
| **APU registers** | SMB writes its music and effects every frame | accept writes; answer `$4015` and the frame counter's IRQ flag as the hardware would (SMB is expected to keep IRQs off; checked by trace, below) |
| **Official opcodes only** | expected of a 1985 first-party game, unverified | all 151 official opcodes with their cycle counts and page-cross penalties; any unofficial opcode **traps**, so a wrong expectation shows at once rather than as drift |

**What it doesn't need:** pixels for the observation (it's read from RAM, D1), sprite overflow,
open-bus behaviour beyond what a trace shows SMB reading, the DMC channel's sample fetches (they steal
CPU cycles; if SMB plays no DMC samples, which the trace checks, they never happen), PAL timing, other
mappers, a second controller.

**Power-on:** a deterministic RAM pattern (zeros), and the state just after power-on saved, as
`NesPyConsole.power_on` does today (stage 2.1b found `nes-py`'s reset is a warm boot).

## The design

**Its own repository, `indrajala-nes`** (MIT), as stage E says, with D12's seams:

```
cpu/       6502: decode table, the 151 official opcodes, cycle counts, NMI and IRQ entry
ppu/       registers, the loopy v/t model, scanline and dot timing, VBlank and NMI,
           sprite-0 hit by the overlap of one sprite with the background; no frame buffer
apu/       the trait Apu; SilentApu (writes accepted, the reads SMB makes answered)
cart/      iNES parsing, the trait Mapper; Nrom (mapper 0) alone
bus.rs     the CPU's memory map, OAM DMA, the controller
console.rs one console: step_frame(buttons), save() -> [u8; N], restore(&[u8])
batch.rs   N consoles, structure of arrays, stepped on the crate's thread pool
games/smb  SMB's observation and episode, from RAM (D12: the only game-specific code)
python/    PyO3: a Console and a Batch the existing Console protocol and VectorEnv can use
```

**Designed for a network** (stage E's list, made concrete):

- **One call a decision for all consoles:** `batch.step(actions, sticky_draws, out_ids, out_values,
  out_reward, out_flags)`: each console runs its 4 frames, the game's skipped frames (SMB's
  `after_decision`), its reward and end, and writes its observation into the caller's arrays. Python
  is entered once a decision for the batch, not once a frame per console as now.
- **The state is plain bytes,** about 10 KB a console (2 KB RAM, 2 KB VRAM, 256 B OAM, palette,
  registers, the cartridge's mapping, the controller, cycle counters). Save and restore are copies,
  and a checkpoint can hold it directly, so 3.2's replay becomes optional.
- **Threads, not SIMD:** each console is a branchy interpreter on its own instruction stream, which
  vectorises badly (NeSLE's GPU notes report the same as warp divergence). So a console a thread at a
  time, consoles shared out over the threads, as D9 shares environments over processes today, but in
  one process, with no pipes.
- **Observation in Rust:** today's `SMB.observe` is NumPy, cheap beside `nes-py` but not beside an
  emulator 20× faster. It moves into `games/smb`, written against the same tests (stage 2.2's census and
  the decoder's checks), so the observation's bits are unchanged.

**What stays:** the `Console` and `Game` protocols, `NesEnv`, `VectorEnv`, PPO and the trainer.
`NesPyConsole` stays as the oracle. The new console is one more `Console`, and the batch one more
`Rollouts`, so the trainer doesn't change (3.2's protocol was built for this).

## How we'd know it's right

Verification is most of the risk, so it's planned in four layers, each a gate for the next:

1. **CPU alone:** `nestest` (kevtris) against its published log, cycle for cycle, and blargg's
   `instr_test_v5` (official opcodes; it reports through `$6000`) and `instr_timing`. These are the
   community's standard gates; NeSLE's CPU gates on Klaus Dormann's functional test.
2. **PPU timing:** blargg's `ppu_vbl_nmi` (VBlank flag and NMI timing, to one PPU dot) and
   `ppu_sprite_hit` (sprite-0 hit's behaviour and timing), as far as a no-pixel PPU can run them; both
   report through the screen or `$6000`, so the harness reads their result bytes.
   **Their licences aren't stated** on the NESdev wiki's test page; they're fetched by a script into a
   gitignored directory, never committed, and their terms checked before any is.
3. **The oracle, `nes-py`, as a black box:** RAM compared every frame against `nes-py` on recorded
   action streams: the level driver's runs through all 32 levels (stage 2.2), random play, and the
   control's episodes. **Pass: no divergence over every recorded run.** RAM is all the game and the
   network see, so this is the test that matters.
4. **Through the stack:** `NesEnv` on the new console gives the same `Step`s and observations as on
   `NesPyConsole`; the 26 driven clears replay to clears; the vector runner's bit test (2.3) on the
   batch; a PPO run checkpointed and resumed (3.2).

**The parity risk, and its fallback.** `nes-py` ends a frame at a fixed point of its own cycle
accounting, which stage 2.2 found can fall inside the game's pad read. Bit parity frame by frame needs
our console to end its frames at the same point with the same CPU-PPU alignment, the same DMA stall
and the same handling of the odd frame's skipped dot, whatever the hardware does. So the console gets
a **`nes-py`-compatible boundary** (its definition of a frame), measured and matched first, and layer
3 runs in that mode. If `nes-py` turns out to deviate from the hardware somewhere that changes RAM, and
matching it would mean copying a bug, the fallback is a **second oracle run as a black box**: a
hardware-accurate emulator's RAM trace (Mesen2 or FCEUX; both GPL, so run, never read), plus the game
itself: the same clears and deaths at the same decisions as `nes-py`'s runs. The runs and readings
already made on `nes-py` stand either way, as they were made on it.

## Where the code comes from

| Source | Licence | Use |
|---|---|---|
| NESdev wiki | documentation | **the hardware's behaviour:** CPU, PPU (loopy registers, timing, sprite 0), DMA, controller |
| [NeSLE](https://github.com/hbofz/NeSLE) | MIT | design: batched NROM for RL, SMB as its one game, its CPU reference console, its validation (8M random instructions against its earlier interpreter, a batch against N independent consoles) |
| [TetaNES](https://github.com/lukexor/tetanes), [pinky](https://github.com/koute/pinky) | Apache-2.0 | Rust structure of a CPU and PPU; notices carried where adapted |
| [takahirox/nes-rust](https://github.com/takahirox/nes-rust) | MIT | a smaller Rust reference |
| [`nes-py`](https://github.com/Kautenja/nes-py) | MIT declared, **core derived from GPL-3.0 SimpleNES** | **the oracle only, run as a black box; its C++ not read.** Its own [LICENSING.md](https://github.com/Kautenja/nes-py/blob/master/LICENSING.md) says the provenance difference is unresolved. *This corrects stage E's table, which listed it as a structural source.* |
| SimpleNES, Mesen2, FCEUX, starrhorne/nes-rust | GPL | not read for code; Mesen2 or FCEUX may be run as a second oracle |

NeSLE is the closest prior work: SMB on NROM, batched, RAM observations. Its fast path is a CUDA kernel,
and GPU backends are out of this project for now (by the owner), so its design transfers and its fast
path doesn't. Its own figures: 3.27M environment steps a second on an A100 against `nes-py`'s 767 on 12
CPU threads. It notes the CPU stack draws every frame and its GPU path doesn't, so that isn't a
like-for-like emulator comparison. **It also reports, as we found, that at scale the PPO learner and
not the emulator is the bottleneck.**

## How fast, and what that buys

**The emulator.** A frame is 29,780 CPU cycles, about 10,000 instructions. A careful interpreter takes a
few nanoseconds an instruction, so a frame's CPU is roughly 30-60 µs. A PPU kept at scanline
granularity, with the one sprite-0 overlap, adds little. That's about **15,000-30,000 frames a second a
core**, against `nes-py`'s 1,075 a core on `stone` (stage 0's probe, drawing every frame), so **15-25× a
core**, an estimate. A decision of 4 frames then costs about 0.2 ms instead of 3.7 ms.

**The iteration** (D10's first reading, `stone`, 8,192 decisions, 16.0 s):

| | today | with the Rust batch (estimate) |
|---|---|---|
| emulation | ~7.4 s | ~0.4-0.5 s (on all 8 threads) |
| the network deciding, in the rollout | ~1.3 s | ~1.3 s |
| the update (learning) | 7.1 s | 7.1 s |
| **iteration** | **16.0 s** | **~9 s: about 1.8×** |

So it meets D10's payoff test (at least 1.5×) but not by much, and the network becomes about 90% of a
step. Beyond 1.8× the gains are the network's: D14's 1×1 conv over 125 planes (a gather would be
cheaper, D14's option d), or a smaller network. **The order the numbers suggest: the emulator only if
3.4's reading confirms the trigger, and then the network.**

**What it buys that D10 doesn't measure:**
- **A serialisable state:** checkpoints hold the consoles, no replay;
- **No pad bug** and no workaround for it (`nes-py` #110);
- **No dependence on `nes-py`:** its upstream is quiet, its pins and its native wheel are a risk on new
  Pythons, and its core's licence provenance is unresolved;
- **aarch64 natively:** `litshe` (a Pi 5) as a runner, the Pi 4 for playback (D9);
- **Room to grow:** the plan's later levels (D6) and evaluation's 100 attempts a seed run 15-25× faster.

## The work, stage by stage

Each a PR in `indrajala-nes`, merged before the next; the last one into indrajala-rl. Estimates at the
plan's rate.

| # | What | Gate | Estimate |
|---|---|---|---|
| E1 | Repository, CI (fmt, clippy, tests), iNES parser, `Mapper` trait, `Nrom`, bus | the cartridge maps; a planted ROM in the tree fails CI (as indrajala-rl's check) | ½ day |
| E2 | The 6502: decode table, official opcodes, cycles, NMI and IRQ entry; unofficial opcodes trap | `nestest` cycle-exact against its log; `instr_test_v5`'s official groups; `instr_timing` | 2-3 days |
| E3 | The PPU without pixels: registers, loopy `v`/`t`, timing, VBlank and NMI, OAM and DMA, sprite-0 overlap | `ppu_vbl_nmi` and `ppu_sprite_hit` as far as they run headless | 3-4 days |
| E4 | Controller, `SilentApu`, power-on, save and restore | SMB boots to the title and plays from a recorded input; a trace shows no unofficial opcode, no IRQ, no DMC fetch | 1 day |
| E5 | **Parity with `nes-py`:** its frame boundary measured and matched; RAM every frame over the driver's 32 levels, random play and the control's runs | no divergence; or the fallback, recorded | **3-6 days** (the uncertain part) |
| E6 | Batch, threads, PyO3; SMB's observation and episode in Rust | the observation's bits against `SMB.observe`; the batch against N single consoles | 2 days |
| E7 | Into indrajala-rl: a `Console` and a `Rollouts` | stage 2's tests on the new console; the vector runner's bit test; a resumed run equal | 1 day |
| E8 | Measured: the probe's emulation rows and a PPO iteration, before and after | D10's reading again, with the numbers | ½ day |
| | **Total** | | **~13-18 days** |

**Sound, later:** an `Apu` implementation with the two pulse channels, triangle, noise and DMC, its
frame counter, mixing and sample output; blargg's APU tests as gates. Its DMC fetches would then steal
CPU cycles as the hardware's do, which the CPU's DMA path is built to allow. About a week, with no change
to the CPU, PPU or mapper.

## Risks

| Risk | Effect | Answer |
|---|---|---|
| `nes-py` parity needs its quirks reproduced | E5 runs long | its boundary measured and matched first; the black-box second oracle as fallback |
| The sprite-0 overlap is subtly off | the game hangs or the split comes a line late | `ppu_sprite_hit`; the hang is loud; RAM parity catches lateness |
| SMB uses something "not needed" above | drift | traps on unofficial opcodes; traces for IRQ, DMC and open bus in E4 |
| The test ROMs' licences | can't be committed or shipped | fetched by script, gitignored, terms checked first |
| The gain is smaller than estimated | under D10's 1.5× | E8 measures it; at worst we keep the other gains |
| Learning is the bottleneck anyway | the emulator's gain capped near 1.8× | expected; the network is the next work |

## Sources

- [NeSLE](https://github.com/hbofz/NeSLE): design, figures and lessons quoted above.
- [nes-py's LICENSING.md](https://github.com/Kautenja/nes-py/blob/master/LICENSING.md): the SimpleNES
  provenance.
- [SMB and sprite 0 hit (NESdev forum)](https://nesdev.nes.science/f3/t12185.xhtml) and
  [How the score bar doesn't scroll (NESdev forum)](https://nesdev.nes.science/f2/t15894.xhtml).
- [NESdev wiki: emulator tests](https://www.nesdev.org/wiki/Emulator_tests): the test ROMs and their
  authors (no licence terms given).
- Our own: stage 0's probe, stage 2.2's pad finding, D10's first reading (stage 3.2's Findings).
