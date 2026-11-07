# Workplan: a stand-alone Rust NES console (SMB first)

**Status (2026-11-07): complete. C0-C5 merged (indrajala-nes #31-#36); the owner played SMB on the console (O13: "plays beautifully"). Decisions D46-D54 settled under the owner's delegation, with their options below; D48 refined twice and D50 changed by the owner; findings at the end. Retires next, its leftovers to the parent's.** A sub-plan of the emulator workplan
(`nes-rust-emulator-workplan.md`), whose pixel sub-plan kept the way open for it ("Later (the owner): a
pure-Rust console with a USB controller", `git show 27d1fad:docs/workplans/nes-pixel-mode-workplan.md`). IDs
continue the parent's (D1-D45, O1-O11).

**The owner (O12, 2026-11-07):** "research and analyse what else we need to build to be able to use our existing
rust-emulator infra as part of a stand-alone rust-nes-console: using keyboard + ps4 controller on usb as inputs;
supporting save game; happy to launch from command line, rather than building additional infra (i.e. console
host supporting rom loading, etc - we will do that next) -> then write up a detailed workplan for this (one last
thing, for the moment we only support smb - in future we will progressively add support for more games)".

**The question.** What has to be added to indrajala-nes so that `nes-console ROM` plays Super Mario Bros at the
NES's own speed, with picture and sound, from the keyboard and a DualShock 4 on USB, with saves? It has to be
built so that adding a game later means adding that game, not changing the console.

**Out of scope here (the owner's "next"):** a host program that browses and loads ROMs, menus, library
management. Also out: games other than SMB, and mappers other than NROM. Each comes with the game that needs it,
behind the seams below.

## Where things stand (indrajala-nes `main` `9be97d3`)

**Already there, and reused as it is:**

- **The whole console, hardware-faithful for SMB:** `nes-core`'s `Console<M: Mapper, A: Apu, R: Render>`. It has
  the pixel mode (`Pixels`, 256×240 palette indices, double-buffered) and the whole 2A03 APU with `Audio<48_000>`
  (an exact integer mixer, band-limited, the NES's filters). SMB's parity holds against FCEUmm and Mesen (E5,
  E6, E11). Sound is heard and approved (O11).
- **Saving the whole machine:** `Console::save_bytes` and `load_bytes` (D9, state version 3). They cover the CPU,
  RAM, the PPU, the APU with its synthesis state, the controller's shift register, the mapper's RAM and the pixel
  pipeline. The ROM is never included. A round trip is tested in `crates/nes-core/tests/console.rs`.
- **Live play exists:** `nes-view ROM` with no episode plays from the keyboard (arrows, `x` A, `z` B, Enter
  START, Tab SELECT). It plays sound through `cpal` (`Speaker`), and its input goes through the `Pad` trait,
  which was made for exactly this ("a USB pad for the owner's later pure-Rust console").
- **Reset and power-on:** `Console::reset` and `Console::new`.
- **The seams:** `Mapper` (D16; NROM alone, monomorphised) and the cartridge parser, which refuses what it can't
  run. The parser also already reads the header's battery bit, and NROM fits PRG RAM at `$6000-$7FFF` when asked.

**Missing (each one checked in the code):**

1. **A second controller port.** `$4017` reads as "no pad" (`console.rs:195`). SMB's two-player game takes
   Luigi's input from pad 2, so two players need it. One controller is fine for one player.
2. **Pacing for play.** `nes-view` paces frames by wall clock ("owed" frames, at most 8 a repaint) on the UI
   thread. Its sound queue drops from the front when it passes a fifth of a second, and plays silence when it
   runs dry. That's fine for a viewer, but in a game you hear pops: the NES runs at 60.0988 Hz, the display at
   about 60 Hz, and the sound card's 48 kHz clock is only near the CPU's clock.
3. **A gamepad.** There is no USB input at all.
4. **Save files.** `save_bytes` is a blob. Nothing records which ROM or which console variant made it, and there
   are no slots, no file handling and no keys bound to saving or loading.
5. **Cartridge save RAM (battery).** There's nowhere to keep battery-backed PRG RAM between runs. SMB has none,
   but most later games that save (MMC1 boards) do.
6. **A game list.** `nes-view` runs any NROM image. The console should run what it supports and refuse anything
   else, saying why.
7. **A console window.** `nes-view` is a research tool, with episodes, overlays, the observation grid and a side
   panel. The console needs only the picture, scaled by a whole number, with fullscreen and a status line.

## The research (2026-11-07)

**Input on Linux.**
- **The DualShock 4 on USB** (`054c:05c4`, `054c:09cc`) is handled by the kernel's `hid-playstation` driver.
  It's present on `pyramidon`'s kernel (7.0): `modinfo hid-playstation` lists the PlayStation device aliases.
  The driver gives an evdev device under `/dev/input/event*`.
- **Access:** those device nodes are `root:input 0660`, and the owner isn't in the `input` group. systemd's
  `70-uaccess.rules` (present on `pyramidon`) gives the logged-in seat user an ACL on joystick devices, so a game
  run from the desktop session can read the pad. That will be checked with the pad plugged in (C3), not assumed.
- **[gilrs](https://docs.rs/crate/gilrs/latest/source/src/lib.rs)** (MIT/Apache-2.0; 0.11.x, rustc 1.84 or
  later) reads evdev on Linux. It has hotplug and the SDL game-controller database's mappings, which name a DS4's
  buttons by position (South, East, ...). Building it needs **`pkg-config` and libudev's `.pc` file**
  ([its README](https://docs.rs/crate/gilrs/0.11.2/source/README.md)). `pkg-config` is installed on `pyramidon`;
  **`libudev-dev` isn't** (checked), so it goes into indrajala-rl's `cli` package list (memory: OS packages
  through the cli) and into indrajala-nes's CI.

**Pacing and sound.**
- The standard answer for an emulator whose frame rate isn't the display's is **dynamic rate control**: stretch
  the audio by at most about 0.5%, steered by how full the output buffer is, aiming at half full. Then neither
  sound nor picture slips, and the pitch change can't be heard. It's described by near
  ([the article](https://archive.ares-emu.net/near.sh/articles/audio/dynamic-rate-control.html)) and libretro
  ([the docs](https://docs.libretro.com/development/cores/dynamic-rate-control/)).
- Without it, sound locked to video slips about once every ten seconds. A PID-style controller is smoother than
  a fixed correction ([one emulator's notes](https://git.halext.org/scawful/yaze/src/branch/master/docs/internal/hand-off/HANDOFF_AUDIO.md)).
- **Here it belongs in the host's speaker, not in `nes-core`:** the console's samples stay the same bits (the
  sound sub-plan's D41 and its CI hash), and only playback is stretched.

**SMB and saving.** SMB has no save of its own and no battery (header flags 6 bit 1 clear). Its only built-in
carry-over is the continue (A+START on the title after a game over). So **"save game" for SMB means saving the
machine's state:** any moment, restored exactly. The battery path (D51) is built for the games that come later
and tested on a synthetic image, since SMB can't exercise it.

## The design

```
nes-console ROM [--scale N] [--fullscreen] [--load SLOT | --resume] [--players 1|2] [--mute] [--config FILE]

  UI thread (eframe)              emulation thread                  audio callback (cpal)
  - keyboard -> InputState        - waits for its next frame time   - DRC speaker: plays the queue,
  - shows the latest frame          (60.0988 Hz on the host clock)    stretched within ±0.5%
  - F-keys -> commands            - reads InputState (+ gilrs)      - counts underruns
                                  - step_frame(pad1, pad2)
                                  - pushes samples, publishes frame
                                  - runs save/load/reset commands
```

- **Crates:** `nes-host` (new, a library) holds what a viewer and a console share: `Pad`, `Speaker` (+ DRC),
  palette-to-RGB, the output-path checks, the gamepad, the save files. `nes-view` moves onto it, behaving as it
  does now. `nes-console` (new, a binary) is the console.
- **One emulation thread** owns the console. Input reaches it through an atomic button state for each port, and
  commands through a channel. Frames leave through a double buffer. A slow repaint therefore never slows the
  game, and saving and loading happen between frames, so a state is always taken at a frame boundary.
- **Input is read once per frame,** just before that frame is emulated, as a real pad is latched at the game's
  strobe within the frame.
- **Game dispatch:** the ROM's SHA-1 is looked up in `games.rs`. An unknown ROM is refused, and the message lists
  what is supported. A known one names its mapper, and `match` picks `run::<Nrom>(…)`. That is monomorphised, so
  the hot path stays generic, as in D16.

## Decisions (settled under the owner's delegation; options with pros and cons)

- **D46. Where the console lives.**
  - (a) *Chosen.* **A new binary crate `nes-console` in indrajala-nes, and a shared library crate `nes-host`**
    factored out of `nes-view`. Pros: one workspace with one pinned toolchain, CI and test ROMs; the core stays
    free of dependencies; the shared host code is written once (memory: factored, not flat); the next step, the
    owner's ROM-loading host, builds on `nes-host`. Cons: one refactor PR (C0) before anything new.
  - (b) Grow `nes-view` into the console. Pros: no new crate. Cons: a research viewer and a game console in one
    program, whose flags and keys get in each other's way; the viewer's overlays and episode code are on the
    console's path.
  - (c) A new repository. Pros: a clean public face later. Cons: two workspaces to keep in step with `nes-core`;
    it can still be split off at publication if wanted.
- **D47. The window and picture.**
  - (a) *Chosen.* **eframe (egui), as `nes-view` uses:** a central picture scaled by a whole number, F11 for
    fullscreen, a one-line status overlay that fades. Pros: already a dependency, built and working on
    `pyramidon`; vsync through its renderer; the owner's host can add menus in the same toolkit. Cons: egui's
    immediate-mode loop is more than a picture needs (small at 256×240).
  - (b) `winit` with `softbuffer`. Pros: the smallest stack, CPU blit only. Cons: no vsync, so tearing on X11; a
    second windowing stack beside `nes-view`'s.
  - (c) SDL2. Pros: window, audio and gamepads in one place. Cons: a C library and a system package; it
    duplicates `cpal` and `gilrs`, which we already use or have chosen.
- **D48. Pacing.**
  - (a) *Chosen.* **The emulation thread runs at 60.0988 Hz on the host's monotonic clock; the speaker uses
    dynamic rate control** (its queue aimed at 50 ms, the ratio steered smoothly by its fill, limited to ±0.5%);
    the UI shows the newest finished frame at each vsync. **Refined at C2:** the target is at least 50 ms and
    at least the largest block the device asks for plus 25 ms, since `pyramidon`'s PipeWire sometimes takes
    2,048 samples at once (its max quantum), which ran a fixed 2,400-sample target dry (7 underruns a minute;
    none after). **Refined at C5:** each run dry raises the target by a quarter of the least target, up to four times it, so a host that sometimes stalls gets more margin and one that never stalls keeps the low latency. Pros: the game runs at the NES's true speed; no sound
    pops; the core's samples untouched; a slow repaint can't slow the game. Cons: a resampler in the host; at 60
    Hz one frame in about 600 is shown twice (about one every 10 s), which can't be seen at this rate.
  - (b) Lock to vsync (one frame each display refresh), DRC on the sound. Pros: perfectly smooth scrolling on a
    60 Hz display. Cons: the game runs 0.16% slow there and at the wrong speed on 75 or 144 Hz displays, or needs
    frame skipping there; the speed depends on the monitor.
  - (c) Let the sound card's clock drive (emulate when the queue runs low). Pros: no resampler. Cons: the game's
    speed follows the sound card's crystal; muted play loses its clock.
- **D49. The gamepad.**
  - (a) *Chosen.* **gilrs.** Pros: MIT/Apache; evdev on Linux; hotplug; SDL mappings, so a DS4, a DualSense or
    an Xbox pad all report positional buttons; the same code works over Bluetooth if wanted. Cons: needs
    `libudev-dev` to build (one OS package; CI installs it).
  - (b) The `evdev` crate directly. Pros: no libudev. Cons: our own button codes for each pad model, and our own
    hotplug.
  - (c) Raw DS4 HID reports (`hidapi`). Pros: the light bar and touchpad. Cons: one pad model only; hidraw
    permissions; nothing the NES needs.
- **D50. The default layout** (remappable, D53). **Changed by the owner at C3 (2026-11-07): NES A (jump) on South (Cross), B (run) on West (Square), with East (Circle) also A and North (Triangle) also B.** The first default, below, is kept as the record.
  - **Pad:** NES **A on East (Circle), B on South (Cross)**, the SNES and RetroArch convention: the two buttons
    sit where the thumb rolls from B to A, as on the NES. Square is also B, Triangle also A, so either hand shape
    works. D-pad, and the left stick past a 50% dead zone, as the NES cross (opposite directions cancel, as a real
    cross can't press both). Options is START, Share is SELECT. The PS button plus a shoulder are console
    commands: PS+L1 save, PS+R1 load, PS+Options reset.
  - **Keyboard:** `nes-view`'s keys (arrows, `x` A, `z` B, Enter START, Tab SELECT). F1-F4 choose the slot (four),
    F5 saves to it, F9 loads it; Ctrl+R resets,
    Ctrl+Shift+R powers off and on, Esc or P pauses, F11 fullscreen, M mute, F12 a picture to
    `~/nes-recordings`, as `nes-view`'s.
  - **Players (`--players`):** 1 (default) gives pad 1 the keyboard **and** the first gamepad, either at once, so
    either can play. 2 gives pad 1 the first gamepad and pad 2 the keyboard, or the second gamepad when one is
    connected.
  - Alternatives weighed: A on South and B on West (the NES's left-to-right order on a modern pad's bottom row;
    as good, a matter of habit, so it's a config line, D53); the left stick off (simpler, but many players use it).
- **D51. Saves.**
  - (a) *Chosen.* **State slots in a container file, and battery RAM in its own file.**
    - A slot file `~/.local/share/indrajala-nes/saves/<ROM SHA-1>/slot-<n>.state` holds a header: magic
      `INESAVE1`, a container version, the ROM's SHA-1, the console variant (mapper, render mode, sound rate),
      the frame count, a UTC time. Then comes `save_bytes`' payload, then a CRC-32 over all of it.
    - It is written to a temporary file, synced, then renamed, so a crash leaves the old slot whole. The previous
      file is kept as `.bak`.
    - Loading checks the ROM, the variant, the version and the CRC first, and on any mismatch it says which and
      changes nothing (`load_bytes` already leaves the console unchanged on error).
    - On quit the state goes to an `auto` slot, and `--resume` starts from it.
    - **Battery RAM:** when the header's battery bit is set, `Mapper::battery_ram()` is written to
      `<ROM SHA-1>.sav` on quit and every 10 s if it changed (the same atomic write), and loaded at power-on.
    - Pros: any moment of SMB is kept exactly; a wrong ROM or a stale build can't load a state silently; later
      games' own saves work by the same path.
    - Cons: a new state version (C1) makes old blobs unloadable, but none exist outside tests.
  - (b) State blobs only, named by slot. Pros: the least code. Cons: nothing stops a slot from another ROM or
    build loading into the wrong game; no battery path.
  - (c) Rewind (a ring of states). Pros: liked by players. Cons: not asked for; it can be added later on (a)'s
    container.
- **D52. Which games run.**
  - (a) *Chosen.* **A list of supported ROMs by SHA-1 (headerless, as the ROM rules already use), with SMB World
    alone;** anything else is refused with what is supported. A game is added with its entry, its mapper and a
    playback test (C5's kind).
    - Pros: the owner's "only SMB for now"; adding a game is a reviewed, tested step; no silent half-working
      games.
    - Cons: another NROM game that would run anyway is refused until listed. `--unlisted` lets a developer try
      one, with a warning, and saves still work.
  - (b) Any image whose mapper is implemented. Pros: more runs today. Cons: untested games appear "supported";
    against the owner's scope.
- **D53. Configuration.**
  - (a) *Chosen.* **The defaults in code, and an optional TOML file** (`~/.config/indrajala-nes/console.toml`,
    or `--config`) that rebinds keys, pad buttons, the dead zone, the scale and the sound buffer. Unknown keys
    are refused, with the line. Pros: works with no file; remapping without a rebuild; the owner's host can edit
    the same file. Cons: a `toml` and `serde` dependency in `nes-host`.
  - (b) Flags only. Pros: no file. Cons: a full remap doesn't fit on a command line.
- **D54. Two pads in the core.**
  - (a) *Chosen.* **`$4017` reads a second port, which is either `Unplugged` (today's behaviour, the default) or
    a standard pad;** state version 4 saves port 2. Training and every parity check keep port 2 unplugged, so
    their bits can't move; it's checked anyway (C1). Pros: SMB's two-player game; Python and the trainer
    unchanged. Cons: one state version bump; `nes-python`'s pinned state tests updated.
  - (b) One player only. Pros: no core change. Cons: SMB's Luigi can't play; every later two-player game needs
    it anyway.

## Stages (each its own PR in indrajala-nes unless named; nothing stacked)

| # | What | Touches | Done when | Time |
|---|---|---|---|---|
| C0 | `nes-host` factored out | new `crates/nes-host` (`Pad`, `Speaker`, `Device`, RGB, path checks); `nes-view` on it | `nes-view`'s tests and its `--snapshot`, `--gif`, `--wav` outputs byte-identical to before | 0.5 day |
| C1 | Port 2 in the core (D54) | `console.rs`, `controller.rs`, `state.rs` (version 4), `nes-python`'s state tests; `step_frame` with both pads' buttons | `cargo test` passes; SMB's `smb-check` and the E5 trace replay (`nes-trace ROM 0`, on a runner) unchanged; the sound CI hash unchanged; indrajala-rl's `--emulate` tests pass on the bumped `nes/` | 0.5-1 day |
| C2 | `nes-console`: window, keyboard, pacing, sound, game list (D47, D48, D50 keyboard, D52) | new `crates/nes-console` (`main.rs`, `emulation.rs` thread, `games.rs`); DRC in `nes-host` | SMB plays from the keyboard on `pyramidon`; a refused ROM's message; **DRC tests:** a simulated device ±0.5% off the CPU's clock keeps the queue within bounds for 10 minutes of samples, with no underrun; **the speed:** 36,059 frames in 600 s ± 1 frame in a headless pacing test; an underrun counter in the status line | 1-2 days |
| C3 | The gamepad (D49, D50 pad, players) | `nes-host::gamepad` (gilrs); `nes-console` input; indrajala-rl's `cli` gets `libudev-dev` (the owner runs `sudo ./cli install-os-packages`); CI's apt list | the mapping tested as pure functions (buttons and stick to NES bits, opposites cancelled); **on `pyramidon` with the DS4 on USB:** detected and hot-plugged, every button in a `--pad-test` readout, played | 1 day |
| C4 | Saves (D51) | `nes-host::saves` (container, CRC, atomic write, `.bak`); keys and pad commands; `--load`, `--resume`; `Mapper::battery_ram` and NROM's | **round trip:** saved mid-level, reloaded, then 600 frames give the same RAM, picture and samples, bit for bit, as without the save; a wrong ROM, version, variant and a flipped byte each refused, the console unchanged; a crash mid-write (killed between write and rename in a test) leaves the slot whole; battery RAM kept across a restart on a synthetic NROM image with the battery bit | 1 day |
| C5 | Configuration and acceptance (D53) | `nes-host::config`; README's "Playing" section; `games.rs`'s SMB playback test (a recorded input file played through the console's input layer reaches E5's RAM) | **the owner plays SMB** with keyboard and DS4, saves and loads; no underrun in a 10-minute session; this plan retires, its leftovers to the parent's | 0.5 day, then the owner's session |

**Order:** C0, then C1 and C2 (independent), then C3 and C4 (independent), then C5. **About 5-6 days of
building.** All development, emulation included, is on `pyramidon` (O2), except C1's E5 trace replay, which runs
on a runner (`klip`). Nothing here touches training. The NES plan's stage 4 runs aren't disturbed: the only core
change is C1's, which keeps port 2 unplugged by default and is checked against the parity traces before
indrajala-rl's `nes/` moves.

**The ROM rules hold:** ROMs never enter a repository. Saves and pictures stay outside repositories (refused
inside one, as recordings are). Save states hold the game's RAM, never its ROM.

## Adding a game later (the owner's "progressively")

Each game is a short checklist, not a redesign:
1. **Its mapper,** if new: a `Mapper` implementation in `nes-core` with its test ROMs (as D16 planned), and its
   `battery_ram` if the board has one. The state carries its registers.
2. **Its entry** in `games.rs`: SHA-1, name, mapper, players.
3. **Its check:** a recorded input file played through the console reaches a known state (C5's kind), and the
   parity method against Mesen if its timing matters.
4. If it needs hardware SMB doesn't use (the parent's leftovers: sprite 0's clear-dot read, open-bus decay, the
   DMC's edges, expansion audio), that work comes with it.

## Risks

- **The pad's permissions** (uaccess) depend on the owner's session; if they fail, the remedy is a udev rule the
  owner installs, which goes through the `cli` too.
- **eframe's vsync and the compositor** may add a frame of display latency. Measured in C5 by eye. If it matters,
  the picture moves to a lower-latency present mode (a D47 revision), with no other change.
- **DRC tuning:** a too-eager controller warbles. The tests bound the ratio's movement, and the owner's ear
  decides (C5).
- **C1 touches the core:** guarded by the parity traces, the sound hash and the Python tests before any training
  checkout moves.

## Open for the owner

None. The owner reports any further underruns as they play; each is read against the quit summary's queue
low point and target.

## Findings

### C0: `nes-host` (2026-11-07, indrajala-nes #31)

`nes-host` holds the console type, `Pad`, the speaker, pictures and the output-path checks; `nes-view` runs on
it. **Its bar held:** `nes-view`'s `--snapshot` (episode and live, with a hue), `--gif` with `--wav`, and
`--wav` gave byte-identical files to `main` `9be97d3` (five SHA-256s, the canonical dump, an S7 episode), and
again after C2's changes to the speaker. One gap closed: `--snapshot` wrote inside a repository; now refused,
as the other outputs were.

### C1: port 2 (2026-11-07, indrajala-nes #32)

`controller::Port` (`Unplugged` by default, or `Standard`); `$4016`'s strobe reaches both ports;
`step_frame_pads`; state version 4. **All its gates passed:** `cargo test` with the sound hash; `smb-check`
equal to `main`'s but for the speed readings; the E5 trace replay on `stone` (34 FCEUmm traces, lead 0, tiles
and pixels) PASS with 97,077 of 97,079 frames equal at the end and 2 within the slack, its output
byte-identical to `main`'s in both modes; indrajala-rl's emulate suite on `stone` (`main` `7809cd5`, `nes/` at
C1, stable-retro 1.0.1): 260 passed, none skipped. (A first replay at lead 1 failed on `main` too, by a frame
from frame 1: lead 0 is the console's since D34.)

### C2: the console (2026-11-07, indrajala-nes #33)

The emulation thread, `games.rs` (SMB World by headerless SHA-1 `facee9c5…`; others refused, `--unlisted`),
the window, and in `nes-host` the pacer and dynamic rate control. **Its checks:** DRC with a device 0.5% off
either way, blocks of 256, 1,024 and 2,048, ten simulated minutes: no underrun, nothing dropped; within the
limit it settles at the target. The pacer: 36,059-36,060 frames started in 600 simulated seconds. **On
`pyramidon`, ten real minutes** (title and attract mode, sound on): 36,059 frames in 600.0 s, 0 underruns, 0
dropped, blocks up to 2,048, the queue down to 2,073 samples, 0 slips. Not yet: the owner playing from the
keyboard (moved into C5's session).

### C4: saves (2026-11-07, indrajala-nes #34)

The checked container, atomic writes with `.bak`, slots 1-4 and the auto slot, `--load`/`--resume`, battery
RAM (`Mapper::battery_ram`, NROM's with the battery bit). **Its checks:** saved through a slot file and
reloaded into a fresh console, 600 frames give the same RAM, picture and samples bit for bit as running on, on
a sounding synthetic program (CI) and on SMB saved at frame 400 mid-1-1 (`pyramidon`); another ROM, another
variant, a flipped byte and another state version each refused with the console unchanged; every single
flipped byte caught; a crash after the write or the backup leaves the old slot whole; battery RAM kept across
a restart on a synthetic battery image.

### C3: the gamepad (2026-11-07, indrajala-nes #35)

`nes-host::gamepad`: gilrs 0.11.2 behind the `gamepad` feature (on by default); the layout as pure functions
(positions, the stick's 50% dead zone, opposites cancelled, Mode's commands, nothing reaching the NES while Mode
is held); the players' split; port 2 plugged for two players and kept through a load; `--pad-test`. CI installs
`libudev-dev`; indrajala-rl #29 added it to the `cli` list. **On `pyramidon` with the owner's DS4 on USB:**
detected, and every button in `--pad-test`. **uaccess is enough:** the desktop session reads the pad
with no udev rule and no `input` group (the risk above didn't arise). **The owner changed D50:** Cross jumps,
Square runs (above).

### C5: configuration and acceptance (2026-11-07, indrajala-nes #36)

`nes-host::config` (the optional TOML file, unknown fields and out-of-range values refused with their line,
flags over the file); D50 as the owner set it; README's "Playing"; **SMB's playback check:** E5's right-jump
trace of 1-1 (FCEUmm) played from power-on through the console's input layer equals the trace's RAM on every
frame, over 3,000 frames. A second commit moved save writes to a writer thread and made the sound target grow
after a run dry (D48, above).

**The owner's sessions on `pyramidon`:**
- **First, on the first commit:** 15 minutes, **1 underrun**: the queue was down to 1,916 samples before a
  2,048-sample block, so a frame was held back about 30 ms (wired sound; a save's sync or background load).
- **Second, on the merged build (`a271883`):** 25,596 frames in 426.0 s (60.0904 a second), **0 underruns**,
  0 samples dropped, blocks up to 2,048, the target 3,248 (2,048 plus 1,200: never grown), the queue down to
  2,092, 0 slips. **7.1 minutes, short of the 10 the bar named;** the owner's verdict, "plays beautifully",
  accepted it, and further underruns come back as the owner meets them.
- **Latency** (a risk above): the owner raised none; D47 stands.
