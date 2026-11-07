# Workplan: sound for the Rust NES — the whole 2A03 APU

**Status: drafted 2026-11-07 on the owner's ask (O9); decisions D36-D43 settled under the owner's delegation;
the build waits for the owner's go.** A sub-plan of the emulator workplan (`nes-rust-emulator-workplan.md`),
whose goal is hardware fidelity in everything a game observes (O8). IDs continue the parent's (D1-D35,
O1-O8).

**The owner:** "go ahead with the level table - then, while we are waiting, do research and analysis then
draw up a detailed plan for adding sound to the emulator".

## Where things stand

- **The seam exists (D15):** `trait Apu` in nes-core, one implementation, `SilentApu`. It keeps the frame
  counter's IRQ and, since E10, the whole DMC (reader, output unit and level, timer, IRQ, its DMA). The
  output level is kept but nothing is mixed.
- **A fidelity gap, apart from audio (O8):** `$4015`'s bits 0-3 report the four channels' length counters,
  which games may poll; ours always read 0, as no length counter exists. `apu_test` 1-2 and 5 and
  `blargg_apu_2005` 01-02, 05-06 and 10-11 test them. **SMB never reads `$4015`** (E4's audit: its APU reads
  are of write-only registers and the pads), so SMB's parity can't move, and is checked anyway.
- **What sound needs, beyond that:** the pulse, triangle and noise generators (sequencers, envelopes, sweep,
  linear counter, the noise LFSR), the mixer, the console's output filters, and resampling from the CPU's
  1.789773 MHz to an audio rate; then somewhere to hear or keep it (`nes-view`, files, Python).
- **Training mustn't pay for it:** the learning runs never listen. Sound must cost nothing when off, as the
  pixel mode costs nothing in the tile mode (D27).

## The research (2026-11-07)

**The hardware** (the NESdev wiki: "APU", "APU Mixer", "APU Frame Counter", "APU Length Counter", "APU
Envelope", "APU Sweep", "APU Triangle", "APU Noise", "APU DMC"):

- **Channels:** two pulses (`$4000-$4007`: duty, envelope or constant volume, sweep, 11-bit timer, length),
  a triangle (`$4008-$400B`: linear counter, 11-bit timer, length; 32-step sequence; silenced by halting,
  holding its last value), noise (`$400C-$400F`: envelope, mode, period index, length; a 15-bit LFSR), the
  DMC (done). The triangle's timer is clocked every CPU cycle; the pulse, noise and DMC timers every second.
- **The frame counter:** 4-step (quarter-frame clocks on all four steps, half-frame on 2 and 4, IRQ on 4)
  or 5-step (quarter-frame on 1, 2, 3, 5, half-frame on 2 and 5, no IRQ); writing `$4017` with bit 7 set
  clocks both at once. Quarter-frame clocks the envelopes and the triangle's linear counter; half-frame the
  length counters and sweeps. Ours has the sequence's phase and its IRQ already (`FRAME_IRQ_AT`).
- **Length counters:** a 32-entry table loaded by a write to `$4003/$4007/$400B/$400F`; halted by the halt
  bit; cleared and held at 0 while the channel is disabled in `$4015`.
- **Muting:** a pulse is silent with its length at 0, its period below 8, or its sweep's target past `$7FF`
  (even with the sweep disabled: "APU Sweep"); the triangle needs both counters nonzero.
- **The mixer** (exact): `pulse_out = 95.88 / (8128 / (p1 + p2) + 100)`, `tnd_out = 159.79 / (1 / (t/8227 +
  n/12241 + d/22638) + 100)`, 0 when its inputs are 0; or the tables `pulse_table[n] = 95.52 / (8128/n + 100)`
  (31 entries) and `tnd_table[3t + 2n + d] = 163.67 / (24329/n + 100)` (203 entries, within 4%).
- **The output filters (NES):** first-order high-pass at 90 Hz, first-order low-pass at 14 kHz (a second
  low-pass above hearing, left out). The Famicom: a 37 Hz high-pass only.

**Test ROMs** (all in the pinned nes-test-roms commit `scripts/fetch_test_roms.py` uses):

| Suite | What it checks | How it reports |
|---|---|---|
| `apu_test` 1-6 (blargg) | length counters, length table, frame IRQ flag, jitter, length timing, IRQ timing | `$6000`, automatic |
| `blargg_apu_2005.07.30` 01-11 | the same areas, finer: timing per mode, halt and reload timing, reset timing | screen and a result code; automatic with the screen reader E10 added |
| `apu_reset` (6) | power-on and reset state: `$4015` cleared, `$4017` written and its timing, IRQ flag, length enabled | `$6000`, automatic (with the harness's reset) |
| `apu_mixer` (4: square, triangle, noise, DMC) | relative volumes and the mixer's non-linearity: each plays a tone and its inverse through the DMC's DAC, so a correct mixer gives near silence | on screen "done"; **automatic here by measuring the residual** against the tone; hardware recordings (`apu_mixer_recordings/*.mp3`) for listening |
| `volume_tests` (tepples) | relative channel volumes at `$4011` settings | listening; a recording from an NES-001 included |

**Oracles for the sound itself:** **FCEUmm through stable-retro** exposes its audio (`RetroEmulator.get_audio`,
`get_audio_rate`; the libretro core reports 48,000 Hz): a reference waveform for any trace, on `klip`. Its
resampler and filters aren't ours, so it's compared by measures that survive both (loudness per frame,
pitch, the spectrum), not sample by sample. **Mesen's Lua API has no audio call** (P3's probe listed
`emu`'s names), so Mesen stays a state and timing oracle. The hardware recordings above are the ground
truth for listening.

**Code to read for structure** (D19: MIT or Apache-2.0 only, notice kept): TetaNES (MIT OR Apache-2.0),
pinky (MIT OR Apache-2.0), takahirox/nes-rust (MIT). **Not read:** blip_buf and Blargg's Nes_Snd_Emu (LGPL),
Mesen, FCEUmm, FCEUX, Nestopia (GPL). Band-limited synthesis is a published technique (band-limited steps,
windowed sinc); ours is written from that account.

**Cost** (the analysis): the generators' state changes at most every CPU cycle, and the mixed output only when
a channel's output changes: a pulse at 440 Hz changes about 1,760 times a second, against 1.79 million
cycles. So the output is a sequence of steps, synthesised band-limited at the audio rate, with no
per-cycle work; between register writes each channel is periodic and deterministic, so it can be run in
bulk when sound is asked for, as the PPU is caught up (D4).

## The IDs, in time order

| ID | When | Short label | What it is |
|---|---|---|---|
| O9 | 2026-11-07 | the sound plan's ask | the owner: research, analysis, then a detailed plan for sound; the build on the owner's go |
| D36 | 2026-11-07 | sound's scope | the 2A03's five channels, mixer and the NES's filters, NTSC; no expansion audio, no PAL |
| D37 | 2026-11-07 | the APU's split | the CPU-visible APU (length counters, frame clocks, `$4015`) in every build; synthesis behind a `Sound` type parameter, `NoSound` compiling it out |
| D38 | 2026-11-07 | synthesis | event-driven: output steps, band-limited at the audio rate, run lazily (catch-up) |
| D39 | 2026-11-07 | numbers | integers throughout (fixed-point mixer, filters and kernel), so every machine's samples are equal (D18) |
| D40 | 2026-11-07 | the audio rate | 48,000 Hz by default, 44,100 as an option; a frame's sample count carries its fraction |
| D41 | 2026-11-07 | the sound's checks | the CPU-visible suites must pass; `apu_mixer` by measured residual; FCEUmm's audio by robust measures; hardware recordings by ear |
| D42 | 2026-11-07 | where sound goes | `nes-view` plays it (`cpal`) and writes WAV; `indrajala_nes.Console` returns a frame's samples when asked; recordings stay local |
| D43 | 2026-11-07 | sound and learning | not an observation: no network hears it; a scope change for the NES plan, the owner's |

## Decisions

Each has its options with pros and cons; the chosen one is marked.

- **O9. The ask** (the owner, 2026-11-07): research, analysis and a detailed plan. Building it is a new go.

- **D36. Sound's scope.**
  - (a) *Chosen.* **The 2A03's APU in full: both pulses, the triangle, noise and the DMC's output, the
    nonlinear mixer, and the NES's output filters, NTSC.** Pros: everything a cartridge without expansion
    audio can make heard; the parts are well documented and tested. Cons: about a week's work.
  - (b) Pulses and triangle first. Pros: most of the music. Cons: noise and DMC carry the drums and samples;
    the mixer's non-linearity couples them, so a partial mixer is a wrong mixer.
  - (c) With expansion audio (VRC6, MMC5, N163, FDS, 5B). Pros: the Famicom's library. Cons: each belongs to a
    mapper we don't have (NROM only, D16); it comes with its mapper, behind the `Mapper` seam.
  - **PAL and the Famicom's filter:** not planned (NTSC SMB, D6); a constant table and a filter each, later.

- **D37. The APU's split.**
  - (a) *Chosen.* **Two layers.** The **CPU-visible APU** in every build: the four length counters and their
    table, halt and `$4015` enables, the frame sequencer's quarter- and half-frame clocks (with `$4017`'s
    immediate clock), the sweep's and envelope's state that the length and mute logic need, and `$4015`'s
    bits. That closes O8's gap and passes the CPU-visible suites. The **synthesis** (sequencers, LFSR,
    envelope output, mixer, filters, resampler) behind a type parameter `Sound` on the APU, as `Render` is
    on the PPU (D27): `NoSound` compiles it out, `Sound48k` (or a rate-generic `Audio`) makes samples.
    Pros: fidelity for every build; training pays only for the frame clocks (about 240 a second, computed
    lazily like the frame IRQ); the sound path is a separate type, tested against the silent one for equal
    CPU-visible behaviour, as the pixel mode against the tile mode (X4). Cons: `SilentApu` grows, and the
    name no longer fits: it becomes `Apu2a03<S: Sound = NoSound>`, a rename through nes-tools and
    nes-python.
  - (b) A new `SoundApu` beside `SilentApu`. Pros: the silent one untouched. Cons: two copies of the frame
    counter, length counters and DMC to keep equal; O8's gap stays in the silent one.
  - (c) A runtime switch. Pros: one type. Cons: a branch in the hot path, and the synthesis compiled into
    training (against D27's reasoning).

- **D38. Synthesis.**
  - (a) *Chosen.* **Event-driven, band-limited steps:** each channel's output is a sequence of steps at CPU
    cycles; the mixed output changes only at a step; each change is added to the audio buffer as a
    band-limited step (a windowed-sinc step response, precomputed as a table of phases), then the two
    filters run at the audio rate. Channels run lazily: from the last time sound was asked for up to now,
    stepping each channel's timer from event to event (the next output change), never cycle by cycle;
    register writes bring them up to the write's cycle first. Pros: work in proportion to the output's
    changes (a few thousand a second), not the CPU's 1.79 million cycles; no aliasing from naive
    sampling; the same catch-up shape as the PPU (D4). Cons: the step table and its phase resolution are a
    design to test (D41's spectrum checks).
  - (b) Per-cycle output, then a decimating filter. Pros: the simplest to get right. Cons: 1.79 million
    samples a second through a long filter: far the slowest.
  - (c) Point sampling at 48 kHz. Pros: trivial. Cons: audible aliasing on high notes and noise.

- **D39. Numbers.**
  - (a) *Chosen.* **Integers throughout:** the mixer's two tables (31 and 203 entries) as fixed-point
    integers, generated once from the wiki's exact formulas by a script whose output is committed with its
    generator; the step kernel and the two filters in fixed point; samples as `i16`. Pros: D18's guarantee
    (the same bits on every machine) extends to sound, so tests can compare exact sample streams across
    machines and runs. Cons: fixed-point scaling to choose (headroom, rounding), checked against a float
    reference in tests.
  - (b) Floats. Pros: easy. Cons: equal across x86-64 and aarch64 only with care; D18's checks couldn't
    cover sound.

- **D40. The audio rate.**
  - (a) *Chosen.* **48,000 Hz default, 44,100 Hz as an option**, mono. A frame (29,780.67 cycles) is 798.7
    samples at 48 kHz: the resampler carries the fraction, so a frame yields 798 or 799 and none is lost
    over a run. Pros: what audio devices and FCEUmm's core use; one rational resampler. Cons: none to speak
    of.
  - (b) The CPU's rate, downsampled outside. Pros: exact. Cons: 30,000 samples a frame to move out.

- **D41. The sound's checks.**
  - (a) *Chosen.* **Four kinds, in order:**
    1. **CPU-visible suites, automatic, in CI:** `apu_test` 1-6, `blargg_apu_2005.07.30` 01-11, `apu_reset`
       (6). Every one must pass (a few may need the reset button's timing, which the harness has). With
       D37 these pass in the silent build too.
    2. **Unit tests on the generators:** each channel's step sequence against hand-worked ones (a pulse's
       period and duty, the triangle's 32 steps, the LFSR's first states in both modes, the envelope's decay
       and loop, the sweep's target and its mute, the linear counter's reload), and the mixer's tables
       against the formulas (within the fixed point's rounding). The silent and sounding types give equal
       CPU-visible state over a long run (the X4 check's pattern).
    3. **The mixer, measured:** `apu_mixer`'s four ROMs, residual RMS during the test sound against the
       tone's own RMS (the test's design is cancellation; the bar from a float reference of the wiki's
       formulas, recorded before the run). The step synthesis measured by spectrum: a pulse's fundamental at
       `fCPU / (16 (t + 1))` within a bin, and its aliases below a set level.
    4. **Against the outside world:** FCEUmm's audio (stable-retro) on SMB's title and 1-1's traces and on
       the test ROMs: loudness per frame correlated, note pitches equal, spectra close; the hardware
       recordings (`apu_mixer_recordings`, `volume_tests`' NES-001) by ear and by level: **the owner
       listens** to SMB through `nes-view` beside FCEUmm.
  - (b) Only the ROMs. Pros: automatic. Cons: they test what the CPU sees and the mixer, not the waveform.
  - (c) Exact samples against an oracle. Pros: strict. Cons: no oracle shares our resampler and filters;
    exactness would test those, not the APU.

- **D42. Where sound goes.**
  - (a) *Chosen.* **`nes-view` plays it** through `cpal` (Apache-2.0; nes-view already has eframe, png and
    gif, and isn't a seam crate), with a mute key, and **`--wav FILE`** writes it beside `--gif`. **`indrajala_
    nes.Console(sound=True)`** (a type chosen at construction, D37) returns each step's samples as an `int16`
    numpy array; indrajala-rl's `record_episode.py` keeps them for `nes-view`'s replay. **Recordings stay
    local:** game audio is game art; `check_no_roms.py` refuses audio files (`.wav`, `.ogg`, `.mp3`, `.flac`,
    `.opus`) as it refuses images (X7).
  - (b) WAV only. Pros: no audio device code. Cons: no listening while watching.
  - (c) Audio in Python only. Pros: one place. Cons: `nes-view` is where the owner watches.

- **D43. Sound and learning.**
  - (a) *Chosen.* **Not an observation.** The network sees tiles (the NES plan's D1-D2); nothing hears.
    Training builds use `NoSound`. Pros: no change to the NES plan. Cons: none here; whether a network should
    hear is the owner's scope question, not this plan's.

## Stages, PR by PR

| # | Repository | PR or run | Done when |
|---|---|---|---|
| S0 | indrajala-research | This sub-plan; the parent's IDs and status point here | merged |
| S1 | indrajala-nes | **The CPU-visible APU** (D37's first layer): length counters and table, halt, `$4015` enables and bits 0-3, the frame sequencer's clocks (4- and 5-step, `$4017`'s immediate clock), the sweep's and envelope's state; the rename to `Apu2a03`; the three CPU-visible suites pinned | `apu_test` 1-6, `blargg_apu_2005` 01-11 and `apu_reset` pass; every earlier test; SMB's 600-frame writes byte-identical; E5's traces as before |
| S2 | `klip` | SMB's parity under S1 | E5's 34 traces and E11's Mesen check as before (SMB never reads `$4015`) |
| S3 | indrajala-nes | **The generators** behind `Sound` (D37's second layer, D38): pulse (duty sequencer, envelope, sweep and its mute), triangle (sequencer, linear counter), noise (LFSR, both modes), the DMC's output level as a step source; each a step sequence run lazily | the generators' unit tests (D41.2); silent and sounding builds equal in CPU-visible state over SMB's 600 frames and every APU ROM |
| S4 | indrajala-nes | **The mixer and the output** (D38-D40): the fixed-point tables and their generator, the band-limited step kernel, the 90 Hz and 14 kHz filters, 48 and 44.1 kHz; a frame's samples | the mixer's tables against the formulas; a step's response against a float reference; a pulse's spectrum (D41.3); `apu_mixer`'s residuals under the bar; samples equal on x86-64 and arm64 (CI) |
| S5 | indrajala-nes, then indrajala-rl | **Where sound goes** (D42): `nes-view` playback and `--wav`; `indrajala_nes.Console(sound=True)` and its stub; `check_no_roms.py` refuses audio (both repositories); `record_episode.py` keeps samples | tests pass; a WAV from a test ROM's beep, locally |
| S6 | `klip`, then indrajala-research | **Against FCEUmm and the recordings** (D41.4): stable-retro's audio on SMB's title and 1-1 and on the APU ROMs, ours beside it; the measures; **the owner listens** | Findings; the owner hears SMB on `nes-view` |
| S7 | `klip`, then indrajala-research | **The cost:** `smb-check`'s frames per second with `NoSound` before and after S1 and S3 (no change beyond noise), and with sound on | Findings; the plan retires |

### S1: the CPU-visible APU (1-1½ days)

- `nes-core/src/apu.rs` becomes the APU's whole state model: per channel, the length counter (table, halt,
  enable), and the envelope's and sweep's registers and dividers (their *state* is cheap and needed for the
  sweep's mute and later for sound; their *output* is S3's). The frame sequencer gains its quarter- and
  half-frame clocks, scheduled like the IRQ flag (`next_*` cycles, one comparison when nothing is due), run
  lazily at a `$4015` read, a register write, or a frame's end.
- `$4015` reads bits 0-3 from the length counters; writes clear disabled channels' counters. Reset and
  power-on per `apu_reset` (power-on as a `$00` write to `$4015`; `$4017`'s power-on and reset values).
- The rename (D37): `SilentApu` → `Apu2a03<S: Sound = NoSound>`; `NoSound` is a unit type whose methods are
  empty and inlined. nes-tools, nes-python and indrajala-rl follow (a submodule bump; Python's API
  unchanged).
- Test ROMs pinned: `apu_test` 1-6, `blargg_apu_2005.07.30` 01-11, `apu_reset`'s six; the harness's screen
  reader (E10) for the 2005 suite.
- **Watch:** the frame counter's `$4017` write delay (3 or 4 cycles, already ours) and the length counter's
  reload-during-clock rule (`11.len_reload_timing`) are the classic edges.

### S3: the generators (1½-2 days)

- Each channel keeps its timer's phase as "the cycle of its next output change" and its output value; a
  `run_to(cycle)` emits (cycle, new level) steps into the `Sound`'s buffer. The triangle's 32-step sequence
  at CPU rate, ultrasonic periods (`t < 2`) handled as the wiki advises (held, not aliased into the band).
- The pulses' sweep units: target computed on every period change; the mute applies whether the sweep is
  enabled or not; pulse 1's ones'-complement negate against pulse 2's two's-complement.
- Noise: the LFSR's feedback from bit 1 (mode 0) or bit 6 (mode 1); period table NTSC.
- The DMC's output level (E10) emits steps on its timer clocks and `$4011` writes.

### S4: the mixer and the output (1½-2 days)

- The mixer: `pulse_table` (31) and `tnd_table` (203) in fixed point from the wiki's exact formulas, by a
  script `scripts/gen_mixer_tables.py` whose output is committed as a Rust table with its generator.
- The band-limited step: a windowed-sinc step response (Blackman, 16 taps a side; 64 phases), integer; each
  mixed change adds `delta × kernel[phase]` into a ring buffer at the audio rate; a running sum yields
  samples. Then the 90 Hz high-pass and 14 kHz low-pass, first order, fixed point.
- `Sound::frame_samples()` hands out a frame's samples; the fraction carried (D40).
- **Measures** (D41.3) as tests on synthetic programs (no ROM in CI beyond the pinned test ROMs): a pulse at
  `t = 253` (440 Hz) → a fundamental within one FFT bin (a small DFT in the test, no dependency); aliases
  below −60 dB; a DC step through the filters → its decay time constant within 2%.

### S5-S7

- **S5:** `cpal` in nes-view only (the seams' check keeps nes-core dependency-free). WAV written by our own
  few lines (RIFF header, `i16` mono). Python: `Console(sound=True)` builds the sounding type; `step()`
  fills `console.samples` (a numpy view, as `ram` is).
- **S6, on `klip`:** stable-retro's FCEUmm recorded with `get_audio()` per step on the 34 traces' first
  2,000 frames and the APU ROMs; ours from `nes-writes`-style replay with sound on; loudness envelopes
  correlated (bar: 0.95, set before), pitches equal where a note holds 4 frames or more, spectra by band.
  **The owner listens** to SMB's title and 1-1 on `nes-view` and FCEUmm's beside it (local recordings).
- **S7:** `smb-check` frames per second, `NoSound` on `main` before S1, after S1 and after S3 (the same
  build options; `pyramidon` reading as development, the claim on `klip`); and with sound on, as a number
  for `nes-view`, not a bar.

**Total: about 6-8 days at the plan's rate.**

## Not planned

- Expansion audio (with its mappers, behind `Mapper`); PAL; the Famicom's filter; stereo or "enhanced" output.
- Sound as an observation for learning (D43): the owner's scope.
- Reading LGPL or GPL sound code (D19); matching FCEUmm's or any emulator's samples exactly (D41 (c)).

## Risks

| Risk | Effect | Answer |
|---|---|---|
| The length counter's edge cases (reload during a clock, halt timing) | `blargg_apu_2005` 10-11 fail | the tests name the rule; the wiki's "APU Length Counter"; Mesen's write log on those ROMs (P4's tools) shows where timing departs |
| S1 changes SMB's states | E5 moves | SMB never reads `$4015` (audit); checked by its write log, E5 and E11 anyway (S2) |
| Fixed-point mixing loses quality | audible noise floor | headroom chosen against a float reference; the step test's −60 dB alias bar |
| The sounding build drifts from the silent one in CPU-visible state | a parity hole | the X4-style equality test over SMB and every APU ROM (S3) |
| `cpal` on Linux needs ALSA's development files to build | `nes-view` build fails on a machine | a Cargo feature `audio` on nes-view, default on; `--no-default-features` builds without |
| FCEUmm's audio differs for reasons of its own (its resampler, its filters, its accuracy) | S6's measures disagree | O8: evidence, not a target; the hardware recordings decide by ear |

## Sources

- The NESdev wiki: APU, APU Mixer, APU Frame Counter, APU Length Counter, APU Envelope, APU Sweep, APU
  Triangle, APU Noise, APU DMC, Emulator tests (fetched 2026-11-07).
- blargg's and tepples' test ROMs in christopherpow/nes-test-roms at `95d8f621` (the readmes of `apu_test`,
  `apu_mixer`, `volume_tests`).
- libretro's FCEUmm documentation: the core's audio rate, 48,000 Hz.
- stable-retro: `RetroEmulator.get_audio`, `get_audio_rate` (checked on `pyramidon`'s install).
