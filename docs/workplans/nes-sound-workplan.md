# Workplan: sound for the Rust NES — the whole 2A03 APU

**Status: drafted 2026-11-07 on the owner's ask (O9); decisions D36-D43 settled under the owner's delegation;
detailed for a new session the same day on the owner's word (O10): S1 starts in the next session, from
"Starting the work" below.** A sub-plan of the emulator workplan (`nes-rust-emulator-workplan.md`),
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
| O10 | 2026-11-07 | the go, in a new session | the owner: "write up a detailed workplan so that we can start the work in a new session" |
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

- **O10. The go, in a new session** (the owner, 2026-11-07): "write up a detailed workplan so that we can start
  the work in a new session". This plan is that write-up; S1 is the next session's first PR.

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
  - (a) *Chosen.* **Integers throughout:** the mixer's tables as fixed-point integers (the pulse's 31 entries;
    the tnd group's from the exact three-input formula, not the 4% one-index approximation: S4 decides
    between a 16 × 16 × 128 table and the formula in fixed point by measuring both), generated once from the
    wiki's exact formulas by a script whose output is committed with its
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

## Starting the work (a new session's checklist)

1. **Read first:** this plan, all of it; the parent's O8 (the goal) and its "Leftovers"; indrajala-nes'
   `CLAUDE.md` (the seams, D19's sources); indrajala-ml's `docs/handover.md` (machines, state).
2. **State at writing** (check it hasn't moved): indrajala-nes `main` `db71831` (#24); indrajala-rl `main`
   `e7778bd` (`nes/` at `4745c5d`); indrajala-research `main` (this plan merged). `klip`: Mesen at
   `~/oracles/mesen`, indrajala-nes and indrajala-rl updated by bundle (no GitHub key on `klip`).
3. **The baseline before S1's first change** (keep the outputs in the PR): on `pyramidon`,
   `cargo run --release -p nes-tools --bin smb-check -- ~/roms/super-mario-bros-world.nes` (frames per
   second with idle skip on and off: a development reading) and `nes-writes ~/roms/super-mario-bros-world.nes
   - 0 600 > smb-main.txt` (built with `--features write-log`): S1 must leave SMB's writes byte-identical.
4. **Fetch the new test ROMs** after adding their pins (below): `python scripts/fetch_test_roms.py`.
5. **Run the new ROMs once on `main` before changing anything,** to record which fail and how (expected:
   the length-counter and reset tests fail; the frame-IRQ ones pass, as today).
6. **Traps** (from earlier sessions): build Rust on `pyramidon` with `-j 2`-`4` under `systemd-run --user
   --scope -q -p MemoryMax=3G`; on `klip` cargo is in `~/.cargo/bin` (not on ssh's `PATH`); Mesen runs
   *outside* `ulimit -v` (.NET reserves more than it uses); `./cli build-nes` in indrajala-rl builds the
   Python module only, not `nes-tools`; never `pkill -f` a pattern inside an ssh command (it matches the
   shell): kill by PID.

## The hardware's numbers (the NESdev wiki, fetched 2026-11-07)

- **Length table** (index from a `$4003/$4007/$400B/$400F` write's bits 7-3): `10, 254, 20, 2, 40, 4, 80, 6, 160,
  8, 60, 10, 14, 12, 26, 14, 12, 16, 24, 18, 48, 20, 96, 22, 192, 24, 72, 26, 16, 28, 32, 30`. Loaded only while
  the channel is enabled; `$4015` clearing a channel's bit forces its counter to 0 and keeps it there; setting
  it has no immediate effect. Clocked (decremented unless 0 or halted) on half-frame clocks. Halt: bit 5 of
  `$4000/$4004/$400C`, bit 7 of `$4008` (shared with the envelope's loop and the linear counter's control).
- **Frame counter, NTSC, in APU cycles (2 CPU cycles each) from the sequence's start:** 4-step: 3728.5
  quarter; 7456.5 quarter and half; 11185.5 quarter; 14914 IRQ flag; 14914.5 quarter, half and IRQ flag; 14915
  (0) IRQ flag; period 14915 (29,830 CPU cycles). 5-step: 3728.5 quarter; 7456.5 quarter and half; 11185.5
  quarter; 14914.5 nothing; 18640.5 quarter and half; period 18641; no IRQ. **In CPU clocks after a `$4017`
  write** (blargg's 2005 readme, measured on hardware): mode 0 steps at 7459, 14915 (quarter and half),
  22373, and the IRQ flag at 29830, 29831 (with quarter and half) and 29832; the next step 1 at 37289. A
  `$4017` write takes effect 3 or 4 CPU cycles later by parity (ours: `cycle + 3 + (cycle & 1)`); with bit 7
  set, quarter and half clocks at once; bit 6 clears the IRQ flag. **Ours today:** the flag at `sequence_start
  + 29_828` (`FRAME_IRQ_AT`), every 29,830; S1 adds the clocks on the same base, fixed by the suites, not by
  arithmetic alone. **Power-on and reset** (`apu_reset`): as if `$00` were written to `$4017` (at reset, its
  last value), then 9-12 clocks before the reset vector runs; `$4015` cleared; length counters enabled (the
  triangle's unaffected at reset).
- **Envelope** (quarter-frame): a start flag (set by `$4003/$4007/$400F`) → decay 15, divider reloaded to V;
  else the divider counts down from V, and at 0 reloads and steps the decay level down (from 0 to 15 when
  looping). Output: V if constant volume (bit 4), else the decay level.
- **Sweep** (half-frame): the target is `period ± (period >> shift)`, pulse 1 negating in ones' complement
  (−c − 1), pulse 2 in two's (−c); recomputed whenever the period changes; **mutes when the target exceeds
  `$7FF` even with the sweep disabled**, or when the period is below 8. At a half-frame clock: if the divider
  is 0, the sweep enabled, the shift nonzero and the channel not muted, the period becomes the target; then
  if the divider is 0 or the reload flag set, divider = P and the flag clears, else it counts down. A write to
  `$4001/$4005` sets the reload flag.
- **Pulse:** duties (sequencer output, steps 0-7): `0 1 0 0 0 0 0 0`, `0 1 1 0 0 0 0 0`, `0 1 1 1 1 0 0 0`, `1 0 0 1 1
  1 1 1`; the sequencer counts down (reads 0, 7, 6, ..., 1); a `$4003/$4007` write resets it to 0 (the
  timer's divider isn't reset). Timer clocked every APU cycle; period `16 (t + 1)` CPU cycles a waveform.
  Output 0 if the sequencer's bit is 0, the length is 0, `t < 8`, or the sweep mutes; else the envelope.
- **Triangle:** sequence `15 14 ... 1 0 0 1 ... 14 15`; timer every CPU cycle, period `32 (t + 1)`; the
  sequencer steps only while both the length and linear counters are nonzero; the linear counter on quarter
  frames: reload if the reload flag (set by `$400B`) is set, else decrement if nonzero; the reload flag clears
  unless the control bit is set. At `t` 0 or 1 the output is ultrasonic and filters to about half amplitude:
  **ours holds the mid level (7.5, as 7 and 8 alternating, averaged) there** rather than synthesise 56 kHz.
- **Noise:** NTSC periods `4, 8, 16, 32, 64, 96, 128, 160, 202, 254, 380, 508, 762, 1016, 2034, 4068` CPU cycles;
  a 15-bit LFSR, power-up 1, feedback bit 0 XOR bit 1 (mode 0) or bit 0 XOR bit 6 (mode 1), shifted right into
  bit 14; silent while bit 0 is 1 or the length is 0; else the envelope.
- **DMC:** done (E10); its output level steps on its timer clocks and `$4011`.
- **Mixer:** exact `pulse_out = 95.88 / (8128 / (p1 + p2) + 100)` and `tnd_out = 159.79 / (1 / (t/8227 +
  n/12241 + d/22638) + 100)` (0 for a zero sum); tables `pulse_table[n] = 95.52 / (8128/n + 100)`,
  `tnd_table[n] = 163.67 / (24329/n + 100)` with `n = 3t + 2n + d`. **Filters (NES):** high-pass 90 Hz and
  low-pass 14 kHz, first order.

## The test ROMs to pin (S1, S4)

All from `christopherpow/nes-test-roms` at `95d8f621`, the commit `scripts/fetch_test_roms.py` already pins.
SHA-256 taken 2026-11-07; paste into `FILES`:

```python
    # blargg's APU tests, CPU-visible (the sound sub-plan's S1): length counters, the frame counter, IRQ timing
    "apu_test/rom_singles/1-len_ctr.nes": "aacf86c1d773badd11392e54506a43a06a3dd0b67a4c255909d1daf770a4a1e2",
    "apu_test/rom_singles/2-len_table.nes": "c002ff1483b4dfb36a6eb004d49739cd58a2dff16e0bac167d5a7c12235caeeb",
    "apu_test/rom_singles/3-irq_flag.nes": "dd888551665937391a2d691b1f96d1858316dbfce4951306146e9e396367f079",
    "apu_test/rom_singles/4-jitter.nes": "bff573d72d0f134fe307f0bb8b968b8d2ffdb85e8aadad9c152839068d6db32a",
    "apu_test/rom_singles/5-len_timing.nes": "4d88f8cc0b21303dc151af4d0f4169d79284634a73082d7ea1ae5cfafedd1e46",
    "apu_test/rom_singles/6-irq_flag_timing.nes": "fc1daff82dd1a49c7c1242392ffbf1c6f44fb70156868582117f2a844cc4dffd",
    # blargg's 2005 frame counter tests, measured on hardware (S1); a result code on screen, 1 passes
    "blargg_apu_2005.07.30/01.len_ctr.nes": "e1e3a29ab5369ab84a6f5f2f426c64bde86b9a1d26a906739d43fbf624bb8829",
    "blargg_apu_2005.07.30/02.len_table.nes": "63cc6a57fae3da5e30df9520d02b723c5b93789e8a6eef6793f876345b245b51",
    "blargg_apu_2005.07.30/03.irq_flag.nes": "6f71c7e3de4b6c00da92c20a86c1c2095196a55dc201ee3286004ecf33a08c2f",
    "blargg_apu_2005.07.30/04.clock_jitter.nes": "46fa69b26fe8c24dc1d0b5908f90ab0141972eeb607bd563d28f53d6f4543fe6",
    "blargg_apu_2005.07.30/05.len_timing_mode0.nes": "606802d6849ccfcf74e907a8512c03a50d443752d1f616e62a242a1fa7eca0ff",
    "blargg_apu_2005.07.30/06.len_timing_mode1.nes": "0f34e26d56ad235d8d6d63565ed4728fbd0b9b8590a4fd4048eaf64283b429d4",
    "blargg_apu_2005.07.30/07.irq_flag_timing.nes": "851c9698941d51da34b4bfbc9644aa08ee41b39c6c814cc9b8412c204ea68085",
    "blargg_apu_2005.07.30/08.irq_timing.nes": "0a20a2b9ca9a8e78d65b500b161294c889399f0ff048edd104b07b15255946ca",
    "blargg_apu_2005.07.30/09.reset_timing.nes": "bb04f8328a51abb2d17e6e5362b8375f3cbfbf0641733d068b22f23e7dc588e6",
    "blargg_apu_2005.07.30/10.len_halt_timing.nes": "cbdaa9a5cf9c19ba2360d3349a47922eec25a3e610374d963c422f2b67c57ac9",
    "blargg_apu_2005.07.30/11.len_reload_timing.nes": "40e633285a4a8710780bfd80d346dee62406f4be161eb75615f469cd9e84e132",
    # blargg's APU reset tests (S1): power-on and reset state, through the harness's reset button
    "apu_reset/4015_cleared.nes": "ef83bc2831f0ddb9e563ac5cbcfa21b129f092911ef42adabae7d47b3e990d95",
    "apu_reset/4017_timing.nes": "0e6072c6dcee98fb73dc7f3af2e48face78be300e8510515ed48dc75d15c1f13",
    "apu_reset/4017_written.nes": "022bd3b45a733179d9a0a9bf0311d09ca81419d7e7434e6f559e42650b39616b",
    "apu_reset/irq_flag_cleared.nes": "e2435b213bf21065b7c9c645359500c1c860a7395d12d051232ab14dad1b0bb5",
    "apu_reset/len_ctrs_enabled.nes": "e05546cbfaa1414d9193b0212084b324ea6b13130af5f171a34c9e574f5ac373",
    "apu_reset/works_immediately.nes": "c750113762ee375319b1bfbf65c457875dbb194649d7e7b3594fba38eb8eefa1",
    # blargg's mixer tests (S4): a tone against its inverse through the DMC's DAC; measured, not by ear
    "apu_mixer/dmc.nes": "036e7a3222f56e7a823b693bae0243e6c8c7ae032defbbd15c8631da468d6ea7",
    "apu_mixer/noise.nes": "47b637cc911dc4416f55891c67976780e0985b6729b339a3f1db277ef6bd4910",
    "apu_mixer/square.nes": "b16e333a2d3698201fc45c21375507a80981928562d3b10f865e23da3922696a",
    "apu_mixer/triangle.nes": "3756d4be75126ab51b40e013e60a125e0f6f198307dcfb9612cd4477f6762279",
```

The 2005 suite's ROMs report on screen (and by beeps); whether they also leave the code in RAM (the 2005 sprite
tests leave it at `$F8`) is checked on the first run, with E10's screen reader as the fallback. The hardware
recordings (`apu_mixer_recordings/*.mp3`, `volume_tests/recordings/nes-001.ogg`) are fetched by S6 into a
gitignored folder, never committed (audio is refused by `check_no_roms.py` from S5).

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

### S1: the CPU-visible APU (1-1½ days; indrajala-nes, one PR)

**Types** (`crates/nes-core/src/apu.rs`, which may split into `apu/{mod,frame,length,envelope,sweep,dmc}.rs`):

```rust
pub trait Sound: Clone + Send + Sync + Persist + 'static {
    const ON: bool;                                    // NoSound: false; the synthesis compiles out (S3)
}
#[derive(Clone, Default)] pub struct NoSound;          // a unit type; Persist writes nothing
pub struct Apu2a03<S: Sound = NoSound> {
    frame: FrameCounter,                               // mode, inhibit, IRQ flag, sequence start, next clock
    pulse: [PulseState; 2], triangle: TriangleState, noise: NoiseState,
    dmc: Dmc,                                          // as E10
    sound: S,
}
pub type SilentApu = Apu2a03<NoSound>;                 // the old name kept as an alias for one release
```

- **The frame counter** keeps `sequence_start` and its mode; `next_clock: u64` is the next quarter- or
  half-frame (or IRQ) cycle. `run_to(cycle)` steps through due clocks, at most a few per frame, applying
  quarter (envelopes, linear counter) and half (length counters, sweeps) in order. It's run lazily: at a
  `$4015` read, any `$4000-$4017` write (before applying it), a frame's end, and `irq()`. `next_irq_change`
  keeps today's contract; idle skip's horizon needs no change, as the clocks change no CPU-visible line
  except the IRQ flag, already covered.
- **Length counters** (four): `length: u8`, `halt: bool`, `enabled: bool`. Writes per the table above; `$4015`
  bits 0-3 read `length > 0`. **The edges** the 2005 suite checks: a length reload written on the cycle of a
  half-frame clock (`11.len_reload_timing`) and a halt change on it (`10.len_halt_timing`): the order of
  "write" and "clock" within a cycle is the rule to find, from the tests' own sources (test code, readable:
  `blargg_apu_2005.07.30/source/`) and the wiki's frame-counter talk.
- **Envelope, sweep, linear counter, LFSR, timers:** S1 keeps only their *registers and counters* (cheap, and
  the sweep's mute needs the period). Their per-cycle output is S3's.
- **Power-on and reset:** power-on as `$4015 = 0`, `$4017 = 0`, with the 9-12-clock delay `4017_timing`
  prints (ours: the reset's 7 cycles plus the frame counter's write delay; find the constant that prints a
  delay within 9-12, i.e. matches hardware, and record it); reset as `$4015 = 0` and `$4017` rewritten with its
  last value (inhibit sometimes cleared: take "cleared" as the tests accept).
- **The rename's reach:** nes-tools (`nes-trace`, `nes-writes`, `smb-check`, `audit.rs`), nes-python (the
  `Console` type, unchanged API), nes-view; `SilentApu` kept as a type alias for one release, then dropped.
- **State:** `VERSION` 3; save and load the new fields.

**Tests** (`crates/nes-core/tests/`):
- `blargg.rs`: `apu_test()` (1-6 and today's 7-8, `$6000`), `blargg_apu_2005()` (01-11, by result code, RAM or
  screen), `apu_reset()` (six, with the harness's reset button, as `cpu_interrupts_v2` uses it today).
- `apu.rs` (new, synthetic programs, no ROM): the length table read back through `$4015` (a write of each index,
  then counting half-frames until bit clears: the counts equal the table); halt freezes it; `$4015` disable
  clears and blocks reload; `$4017 = $80` clocks at once and `$00` doesn't. (The sweep's mute isn't visible to
  the CPU; S3 tests it as a level of 0.)
- `console.rs`: the idle-skip equality test gains a program that plays the pulses with length counters and
  polls `$4015` (on and off equal, as the DMC test does).

**Done when:** every new ROM passes; every earlier test passes; on `pyramidon`, SMB's 600-frame write log
byte-identical to the baseline (step 3) and `smb-check` unchanged; CI green on both architectures. Then S2 on
`klip`: E5's 34 traces (`nes-trace ROM 0`) and E11's `state.sh` on a few, as before.

### S3: the generators (1½-2 days; indrajala-nes)

- `Sound` gains the step sink: `fn step(&mut self, cycle: u64, channel: Channel, level: u8)` (`Channel` an enum
  of the five), inlined to nothing in `NoSound`. Each channel's generator has `next_change: u64` (the cycle of
  its next output change) and `level`; `run_channels_to(cycle)` advances each from change to change, calling
  `step` only when its level changes. With `S::ON` false, `run_channels_to` isn't called at all: the only
  generator state kept is S1's.
- **Pulse:** sequencer position 0-7, the timer's divider (counts `t + 1` APU cycles), duty; level = envelope
  output × duty bit, 0 when muted (length 0, `t < 8`, sweep target > `$7FF`). A `$4003/$4007` write resets the
  position (not the divider) and starts the envelope.
- **Triangle:** position 0-31, timer at CPU rate; steps only while both counters are nonzero; at `t < 2` the
  level is held at the mid value (D36's note) and no steps are emitted.
- **Noise:** LFSR (15 bits, 1 at power-on), mode, period from the table; level = envelope output unless bit 0
  is 1 or length 0.
- **DMC:** its output level (E10's `level`) emits a step at each timer clock that changes it and at `$4011`.
- **The bulk run:** between register writes nothing external changes a generator, so `run_channels_to` jumps
  from change to change; a frame of a 440 Hz pulse is about 30 changes, of noise at period 4 about 7,000 (the
  worst case: still under a quarter of a frame's cycles).

**Tests:** per generator, a synthetic program writes its registers and the test reads the emitted steps
(via a test-only `Sound` that records them): the pulse's 8 duty patterns and period (`16 (t + 1)` cycles a
cycle of the pattern); the sweep's target in both complements and the mute (now visible as level 0); the
envelope's decay at V = 0 and 15 with and without loop; the triangle's 32 levels and its hold when halted
and at `t < 2`; the LFSR's first 20 outputs in each mode from 1 (hand-computed); the DMC's output steps from a
known sample byte. **Silent and sounding equal** in CPU-visible state (`save_bytes` minus the sound's part)
over SMB's 600 frames and every APU ROM.

### S4: the mixer and the output (1½-2 days; indrajala-nes)

- `Audio<const RATE: u32>` (48,000 or 44,100) implements `Sound` with `ON = true`: it keeps the five channels'
  levels, recomputes the mixed value at each step from two tables, and adds the change into a ring buffer as a
  band-limited step.
- **Tables** (`scripts/gen_mixer_tables.py` → `crates/nes-core/src/apu/mixer_tables.rs`, committed with the
  generator): `PULSE[31]`, `TND[203]` from the wiki's *exact* formulas (not the 4% approximation: 203 entries
  hold `3t + 2n + d` only approximately, so the exact two-argument tnd is a table indexed by (t, n, d):
  16 × 16 × 128 = 32,768 `u16` entries, 64 KB, or computed per change from the formula in fixed point: decide
  in S4 by measuring both against the float formula; the plan's default is the exact 3-D table).
- **Fixed point:** mixed output in units of 2^-16 of full scale (`u32` working, `i16` out after the
  high-pass removes DC).
- **Band-limited step:** the step response of a Blackman-windowed sinc, cutoff 0.45 × the audio rate, 16
  taps a side, 64 phases, as `i32` (generated with the mixer tables). Each change at CPU cycle `c` lands at
  audio time `c × RATE / 1,789,773` (an exact rational: `RATE × 3 × 4` and the NTSC master clock), split into
  sample index and phase.
- **Filters** at the audio rate, first order, fixed point: high-pass 90 Hz, low-pass 14 kHz (coefficients
  from the bilinear transform, generated).
- **A frame's samples:** `samples(&mut self) -> &[i16]` drains what's complete up to the last call's cycle.

**Tests:** the tables against the formulas (max error ≤ 1 unit); the step kernel's sum (DC gain 1 within a
unit); a DC step through the filters (the high-pass's decay constant within 2%); a 440 Hz pulse (`t = 253`)
over 1 second: its fundamental in the right DFT bin (a small DFT in the test) and its largest alias below
−60 dB; `apu_mixer`'s four ROMs: the residual RMS during the test sound below a bar set from a float model
before the run (record the bar in the test); samples equal on x86-64 and arm64 (a hash of a 10-second stream
from a synthetic program, the same in both CI jobs).

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
