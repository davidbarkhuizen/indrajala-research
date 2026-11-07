# Workplan: pixel mode for the Rust NES, and a viewer

**Status: drafted 2026-11-06; V1-V4 settled with the owner the same day. X1-X4 done the same day (indrajala-nes #11-#15; Findings): the pixel mode draws the background and sprites, models V2's extras, and equals the tile mode on all 34 FCEUmm traces. X5-X7 done 2026-11-07 (indrajala-nes #16-#18, indrajala-rl #22-#24; Findings): every pixel of 37,134 FCEUmm screens agrees under the palette map; `nes-view` replays a driven run with its observation; the no-ROM checks refuse images and videos. The palette as generated is kept (the owner), with a hue option. Every stage done; the plan can retire once the hue option merges.** A
sub-plan of the emulator workplan (`nes-rust-emulator-workplan.md`). The emulator today has no frame buffer
(D4): it keeps only what the CPU can see. This plan adds a second PPU mode that draws every pixel as the
hardware does, keeps the tile mode as it is for training, and builds a viewer for demonstration and for
inspection. IDs continue the parent's (D1-D26, O1-O4).

**The owner:** asked what a visualiser would take ("not for general use, but for demo purposes and for
human-inspection purposes"); of the options (a frame snapshot, a snapshot with per-line scroll, a real pixel
pipeline), "can we not go with c - but then support both tile and pixel modes - so that we can use our
existing tile-based infra for the moment ?"; then "i think this is the right direction - write up a detailed
plan - and let's resolve any important decisions through dialog".

## What it gives

1. **Pictures, exactly as the hardware draws them,** for demos and for looking at what the agent and the
   level driver do.
2. **A second, independent model of the PPU.** The tile mode predicts sprite 0's hit and moves the scroll
   registers by events (D4, D5); the pixel mode runs every dot. Wherever a program reads none of the pixel mode's extras (V2), both must
   give the CPU the same behaviour, so
   replaying every trace in both and finding RAM equal on every frame checks the tile mode's predictions
   against a literal model, the timing that E5's frame-65 case turns on included (the parity sub-plan).
3. **A picture check against FCEUmm:** stable-retro returns its screen, so the PPU's palette, sprite priority,
   clipping and scrolling, which RAM never shows, can be compared, as numbers.
4. **Later, if ever wanted:** pixel observations. Not in the NES plan's scope ("tiles, not pixels"); this
   plan builds nothing for training.

## The design

**One PPU, two renderers, chosen by a type parameter** (as `Mapper` is, D16): `Ppu<R: Render>`,
`Console<M, R = NoPixels>`.

- **`NoPixels`** (tile mode): today's PPU, unchanged. Zero-sized; every hook an empty inline function, so the
  compiled tile mode is the same code (checked: E7's frames a second within noise, and its bits unchanged).
- **`Pixels`** (pixel mode): the dot-by-dot pipeline below, writing a 256×240 frame of palette indices (6
  bits each, plus the emphasis bits from `$2001`), double-buffered so a finished frame is readable while the
  next is drawn. Catch-up (`run_to`) steps every dot of a visible or pre-render line with rendering on, and
  keeps its fast path for VBlank and for rendering off.

**The pipeline** (the NESdev wiki's "PPU rendering", "PPU sprite evaluation", "PPU scrolling", "PPU
palettes"; MIT or Apache code, such as TetaNES's PPU, read for reference with its notice, D19):
- **Background:** dots 1-256 and 321-336 fetch, every 8 dots, the name-table byte, the attribute byte and
  the pattern's low and high planes; two 16-bit pattern shift registers and two attribute shift registers
  (with their 1-bit latches) shift each dot from 2-257 and 322-337; fine X selects the bit; the left 8
  pixels clip per `$2001`. Dots 337-340 make the two dummy name-table fetches.
- **Sprites:** secondary OAM cleared on dots 1-64; evaluation on dots 65-256 (up to 8 sprites on the next
  line, 8×8 or 8×16 per `$2000`); fetches on dots 257-320 into 8 sprite units (X counters, attribute latches,
  pattern shift registers, flipped as needed); the leftmost opaque sprite pixel wins; priority against the
  background per its attribute bit; the left 8 pixels clip per `$2001`.
- **Sprite 0's hit:** where sprite 0's opaque pixel meets an opaque background pixel, at that pixel's dot,
  with the same rules the tile mode encodes (never at x = 255, the left clip, both layers on, once a frame).
- **The scroll** (`v` moving per dot) is the tile mode's own code: one implementation of it, not two.
- **Output:** pixel x on dot x + 1 (the pipeline's delay as the wiki gives it), the palette index looked up
  in palette RAM at the dot (the backdrop's mirrors, greyscale per `$2001`).

**What the CPU sees (V2, the owner: pixel mode fuller):** pixel mode also models what the tile mode leaves
out because no pixel was drawn: **sprite overflow** (the flag, with the hardware's faulty evaluation after
the eighth sprite), **`$2004` reads during rendering** (the evaluation's bus value), and **`$2007` accesses
during rendering** (the coarse X and Y increments in place of the normal one). The tile mode stays as it is.
So the modes are equal for every program that reads none of these (SMB: E4's audit; the pinned test ROMs
outside those features), and the gate (D28) is drawn on exactly that set; each extra has its own tests.

**The palette** (D29): generated in our code from the NESdev wiki's account of the 2C02's NTSC signal
(its levels and phases, decoded to RGB as the wiki's "NTSC video" describes), so no third party's palette
file and its terms enter the repository; emphasis applied as the wiki describes. A palette is a table of 64
(×8 with emphasis) colours; the viewer can swap it.

## The IDs, in time order

| ID | When | Short label | What it is |
|---|---|---|---|
| O5 | 2026-11-06 | the pixel mode's go | the owner: option (c), a real pixel pipeline, with tile and pixel modes |
| D27 | 2026-11-06 | the render mode | a type parameter on the machine, the renderer beside the PPU (`NoPixels`, `Pixels`), monomorphised: tile mode unchanged |
| D28 | 2026-11-06 | the gate | both modes' RAM equal on every frame where no extra is read (SMB's traces, the test ROMs outside them); the extras by their own tests; pixels against FCEUmm's, as numbers |
| D29 | 2026-11-06 | the palette | generated from the wiki's NTSC account, in our code |
| V1 | 2026-11-06 | the viewer's home | Rust (`eframe`/`egui`, a `nes-view` crate); Python's layers reach it through an episode file (the owner) |
| V2 | 2026-11-06 | what the CPU sees | pixel mode fuller: sprite overflow, `$2004` and `$2007` during rendering (the owner) |
| V3 | 2026-11-06 | demo output | on screen, plus local recordings in a gitignored directory, never committed or published (the owner) |
| V4 | 2026-11-06 | the order | after the parity sub-plan's P1-P2, before its P3-P5 (the owner) |

## Decisions

Each has its options with pros and cons; the chosen one is marked.

- **O5. The go** (the owner, 2026-11-06): option (c) in two modes; this plan, its open decisions by dialog.

- **D27. The render mode.**
  - **As built (X1):** the renderer is a type parameter of `Machine` and `Console`, held beside the PPU, not
    `Ppu<R>`: a generic `Ppu` had its methods compiled in each calling crate and cost the tile mode 6-9% (A/B,
    `pyramidon`); beside it, the A/B is equal. Pixel mode reaches the PPU through the renderer's `run_to`,
    `read_register` and `write_register`, whose tile-mode versions are the PPU's own, inlined.
  - (a) *Chosen.* **A type parameter, monomorphised.** Pros: tile mode compiles to today's code, no branch on
    the hot path; the pattern `Mapper` already uses (D16); no dependency (D17). Cons: two console types; the
    Python module exposes them as two classes (or the pixel class only where V1 needs it).
  - (b) A runtime flag. Pros: one type; switch modes on a live console. Cons: a branch per dot event in
    training; the pixel state carried by every console.
  - (c) A separate pixel PPU. Pros: no shared code to disturb. Cons: two scroll and timing implementations
    to keep equal by test alone; the cross-check loses its point.

- **D28. The gate.**
  - (a) *Chosen.* **Both modes equal, then pixels against FCEUmm.** Every E5 trace and every test ROM that
    reads none of pixel mode's extras (V2) run in both modes: RAM equal on every frame (and, with the parity sub-plan's write log, every write at the same
    cycle). Then pixel mode's frames against FCEUmm's screen on the traces, compared as numbers on the
    runner: each of our palette indices must map to one FCEUmm colour (its palette isn't ours), and every
    pixel must agree under that map. Pros: checks the tile mode's predictions and the renderer together;
    no image leaves the machine. Cons: FCEUmm's own renderer may err where its timing does (a mid-frame
    split's line); such a line is diagnosed, as in the parity sub-plan.
  - (b) Test ROMs only. Pros: quick. Cons: SMB's own scenes untested.

- **D29. The palette.**
  - (a) *Chosen.* **Generated from the wiki's NTSC account,** in our code. Pros: no third-party terms; one
    table we can explain. Cons: colours a little different from any favourite palette (cosmetic).
  - (b) A published palette file. Pros: familiar colours. Cons: most carry unclear or restrictive terms;
    Mesen's and FCEUX's are GPL (D19).

- **V1. The viewer's home** (settled by the owner: "viewer in rust", "python has bad graphics infra options", "and will be slower").
  - (a) Python (`pyglet` on the Python module's frames). Pros: indrajala-rl's observation, runs and networks at
    hand. Cons: Python's graphics options are poor, and it would be slower (the owner); panels plainer.
  - (b) *Chosen (the owner).* **Rust: a `nes-view` crate on `eframe`/`egui`** (MIT/Apache), its own binary, so
    no GUI dependency reaches `nes-core` or the Python module. **Python's layers reach it through an episode
    file:** indrajala-rl writes, per decision, the action, the observation (tile ids and kinds), the reward
    and, later, a policy's action probabilities; the viewer replays the actions on its own console (bit
    for bit the console Python ran, E6) and draws what the file holds over the picture. Pros: native
    graphics and panels; nothing of SMB or the network ported to show them; the same file serves any later
    policy. Cons: the overlay comes from a file, not live, until E8 puts SMB's layer in Rust.
  - (c) A Rust window driven live from Python through the module. Pros: live overlays. Cons: a GUI event loop
    inside a Python extension (main-thread rules, packaging); more than a demo needs.

- **V2. What the CPU sees** (settled by the owner: pixel mode fuller).
  - (a) One model. Pixel mode adds pixels only; anything it could make visible to the CPU
    beyond today's model (sprite overflow, `$2004` and `$2007` during rendering) goes into both modes or
    neither (SMB reads none of them: E4's audit). Pros: the modes equal by construction, so the gate is a
    real check; no game behaves differently by mode. Cons: pixel mode isn't the full hardware for games
    that read those.
  - (b) *Chosen (the owner).* **Pixel mode fuller.** Pros: closer to the hardware where it's cheap there; the
    console the owner plans later (below) wants the fuller PPU. Cons: the modes can then differ for some
    games, and "both equal" holds only for programs that don't read the extras, so the gate names that set
    (D28) and the extras get their own tests (X3).

- **V3. Demo output** (settled by the owner: local recordings). The rule so far: no frame of the game leaves the machine that made it.
  - (a) On screen only, on `pyramidon`. Pros: the rule as it stands. Cons: nothing to show anyone remotely.
  - (b) *Chosen (the owner).* **On screen, plus local recordings** (PNG frames, GIF or MP4 via the `ffmpeg` binary)
    kept in a gitignored directory on the machine, never committed or published. Pros: replays to look at
    later. Cons: files to keep track of.
  - (c) As (b), and shareable recordings only of test ROMs or openly licensed homebrew. Pros: a public demo
    with no game art. Cons: a homebrew ROM to pick and pin.

- **V4. The order** (settled by the owner: after P1-P2).
  - (a) *Chosen (the owner).* **After the parity sub-plan's P1-P2 (the offset check and E5's rerun), before its
    P3-P5 (Mesen):** the pixel mode's own cross-check then informs the timing work. Pros: the cheap parity
    step first; pixel mode early enough to help. Cons: Mesen's comparison waits a few days.
  - (b) After the whole parity sub-plan. Pros: one thing at a time. Cons: the cross-check comes after the
    timing question it could help settle.
  - (c) Before the parity sub-plan. Pros: pictures soonest. Cons: E5 stays open longer.
  - The NES plan's gate runs take the runners first either way.

## Stages, PR by PR

| # | Repository | PR or run | Done when |
|---|---|---|---|
| X0 | indrajala-research | This plan (V1-V4 settled with the owner); the parent's IDs and stages point here | merged |
| X1 | indrajala-nes | `Render`, `NoPixels`, `Console<M, R>`; no behaviour change | all tests, bits unchanged; E7's frames a second within noise |
| X2 | indrajala-nes | `Pixels`: the background pipeline, the frame buffer | synthetic scenes and scrolls render to hand-worked frames |
| X3 | indrajala-nes | Sprites, priority, sprite 0's hit from pixels; the extras (V2) | synthetic scenes; `sprite_hit_tests` in pixel mode; the extras' tests |
| X4 | indrajala-nes, then `klip` | The two modes cross-checked | every test ROM and E5 trace: RAM equal every frame in both modes |
| X5 | indrajala-nes, then `klip` | The palette (D29); pixels against FCEUmm | the palette map one-to-one and every pixel equal on the traces |
| X6 | indrajala-nes, then indrajala-rl | `nes-view` (V1); the episode file and its writers | the viewer replays a driven run with its observation on `pyramidon` |
| X7 | indrajala-nes | Local recordings (V3) | PNG frames and a GIF or MP4 of a replay, in a gitignored directory; images refused by the no-ROM check |

### X1: the seam (½ day)
- `trait Render` with hooks the PPU calls where pixels happen (a line's start, a dot's output, a frame's
  end) and the frame's accessor; `NoPixels` implements them as no-ops. `Ppu<R>`, `Machine<M, A, R>`,
  `Console<M, R>` with `R = NoPixels` defaults, so no caller changes. The state's byte form unchanged in tile
  mode; pixel mode's extra state (shift registers, secondary OAM, sprite units) appended under a version flag
  (D9), so a pixel console can restore a tile console's state and draw from the next line on.
- **Gate:** every test unchanged; E7's development throughput on `pyramidon` within noise; one SMB trace's
  bits unchanged.

### X2: the background (1 day)
- The fetches, shift registers and fine-X selection; catch-up runs every dot on rendering lines in pixel
  mode; the frame buffer; the left clip; greyscale and emphasis bits carried.
- **Tests** (synthetic: pattern tables and name tables written through the bus, no ROM): a checkerboard of
  two tiles renders to the expected 256×240 indices; a coarse and a fine X scroll shift it by the expected
  pixels; a vertical scroll and a name-table switch; attribute quadrants; a mid-frame `$2005`/`$2006` split
  (SMB's kind) draws the lines above and below from their own scroll.

### X3: sprites (1-1½ days)
- Secondary OAM, evaluation (eight a line, the sprite-0 flag carried), fetches, sprite units, flips, 8×16,
  priority, the left clip; sprite 0's hit from the pixels.
- **Tests:** synthetic sprite scenes (priority both ways, overlapping sprites' order, flips, 8×16 halves);
  the hit's dot equals the tile mode's prediction in each synthetic case; the pinned `sprite_hit_tests`
  ROMs pass in pixel mode (they already pass in tile mode).
- **The extras (V2):** sprite overflow with the hardware's faulty evaluation (the wiki's "PPU sprite
  evaluation": after eight sprites, `m` increments with `n`), set at its dot; `$2004` during rendering returns
  the evaluation's bus value (`$FF` on dots 1-64, then the byte being evaluated); `$2007` during rendering
  increments coarse X and Y in place of the normal increment. Tests: synthetic scenes for each, and blargg's
  `sprite_overflow_tests` fetched and pinned like the other test ROMs (`scripts/fetch_test_roms.py`), run in
  pixel mode.

### X4: the cross-check (½ day, then a runner hour)
- A test: every pinned test ROM that reads none of the extras (V2) run for its length in both modes, RAM and CPU registers equal at every
  frame. A tool, `nes-trace MODE=pixels`: the E5 traces in pixel mode, RAM equal to tile mode's on every
  frame. On `klip` over the 34 traces (and the driven ones, when recorded).
- **If they differ:** the first differing frame, then the first differing cycle (the write log, if the
  parity sub-plan's P4 is in), diagnosed: the pixel mode's hit or the tile mode's prediction; the wiki
  decides.

### X5: the palette and FCEUmm's pixels (1 day)
- The generated palette (D29) with a test against the wiki's published reference values where the wiki gives
  them. `record_traces.py` gains `--screens`: FCEUmm's screen at each frame end, kept on the runner beside the
  trace (art: never copied off it). A comparison on the runner: our pixel mode's palette indices against
  FCEUmm's RGB, the map index → colour required to be a function, every pixel compared; a summary of
  numbers only leaves the machine.

### X6: the viewer (1-1½ days, per V1)
- **`nes-view`** (indrajala-nes, `crates/nes-view`, `eframe`): the screen at ×3 or ×4, nearest-neighbour;
  keys to pause, step a frame, step a decision, run at 1×, 2× or as fast as it goes; save and restore; panels
  for RAM (changed bytes marked), OAM, the pattern tables, the palette and each line's scroll; a level from
  power-on, or an input file replayed.
- **The episode file** (`.nesepisode`, versioned, little-endian like the trace format): its header names the
  ROM's SHA-1, the console's boundary and lead, the level and its start's RAM pokes; then per decision the
  action (a `smb.ACTIONS` index and its button byte, so the viewer needs no SMB code), the frames it holds,
  and optional blocks: the observation (13×16 tile ids and kinds), the reward, the action probabilities. Written
  by indrajala-rl: `NesEnv` with a recorder (as `RecordingConsole` records traces), `drive_levels.py --episode`
  for driven runs, and `evaluate.py --episodes DIR` for a policy's attempts. The viewer replays the buttons
  and checks its RAM against a hash the file carries every N frames, so a file and a console that disagree
  are caught.
- **Overlays:** the observation's grid over the picture (kinds coloured, tiles numbered on demand); the
  action and its probability bar; the reward's running sum.
- On `pyramidon` only (development, O2): a window there; the runners stay headless.

### X7: recordings (V3)
- PNG frames through the `png` crate or the viewer's own save; GIF or MP4 by the `ffmpeg` binary; into a
  gitignored `recordings/` on the machine; `scripts/check_no_roms.py` extended to refuse image and video
  files in either repository.

## Findings

### X1-X4 (2026-11-06, indrajala-nes #11-#15)

- **X1 (#11):** `Render`, `NoPixels`; the renderer beside the PPU (D27 as built, above); tile mode A/B equal
  (about 8,200 frames/s with idle skip on `pyramidon`, both builds), state bytes unchanged.
- **X2 (#12):** `Pixels`, the background dot by dot. Against a direct per-pixel reference (each pixel's
  scrolled tile, attribute and pattern bit): scrolls coarse and fine, both mirrorings, across name tables, the
  left clip, greyscale, emphasis, rendering off, and a mid-frame `$2005` split (fine X at once, coarse X from
  the next line, as the hardware).
- **X3a (#13):** sprites (evaluation, 8×8 and 8×16, flips, priority, clips) against the reference; sprite 0's
  hit from the pixels. **Its flag equals the tile mode's predicted one at every dot** of two frames in 30
  random scenes, and in blargg's 11 `sprite_hit_tests`, which pass in pixel mode with 0 disagreements.
- **X3b (#15):** V2's extras. Sprite overflow from a live dot-by-dot evaluation with the hardware's faulty
  search: **blargg's 5 `sprite_overflow_tests` pass in pixel mode** (Basics, Details, Timing, Obscure,
  Emulator; newly pinned) and fail in tile mode, which models none. `$2004` and `$2007` during rendering, by
  synthetic tests.
- **X4 (#14):** `nes-trace MODE=pixels`, a tile-mode twin in lockstep. **On `klip`, the 34 FCEUmm traces
  (97,079 frames): the pixel mode's RAM and cycle equal the tile mode's after every frame, 0 hit
  disagreements**, FCEUmm within the slack as in tile mode; again on `pyramidon` after X3b. Output in
  indrajala-studies' gitignored `data/nes-emulator-gates/klip/x4-nes-trace.out`.

### X5-X7 (2026-11-07, indrajala-nes #16-#18, indrajala-rl #22-#24)

- **X5 (indrajala-nes #16, indrajala-rl #22):** `nes_core::palette`, 64 colours × 8 emphasis settings,
  generated from the wiki's account of the composite signal (D29), the burst (hue 8) decoding to −U.
  `record_traces.py --screens N` keeps FCEUmm's screen every N frames beside the trace on the runner;
  `screen-check` compares our palette entries with its RGB. **On `klip`, 34 new FCEUmm traces on the 12
  actions (371,199 frames), screens every 10th frame: 37,134 screens, 1,996,323,840 pixels, 21 palette
  entries seen, 0 pixels breaking the map (entry → colour a function): PASS.** FCEUmm's screen sits at (8, 8)
  in ours. On the same traces: tile mode, 371,196 frames equal at the cut and 3 within the slack (E5's
  check, D20); pixel mode equal to the tile mode on every frame, 0 hit disagreements. Outputs in
  indrajala-studies' gitignored `data/nes-emulator-gates/klip/x5-*.out`, with `x5.sh`.
- **The palette's look (the owner, 2026-11-07: "we can keep that palette", "or offer it as an option"):**
  as generated, `$22` (SMB's sky) is a violet-blue, (166, 121, 255): plain +U, clipped in blue. Nintendo's
  RGB PPU, the 2C03, has `$22` at (146, 146, 255) (the wiki's DAC table), close to ours; TV-derived palettes
  sit about one hue step (−30°) away. Kept as the default; **a hue option** (`palette::ntsc_hue(degrees)`,
  rotating U and V, as the wiki's "add or subtract a value from phase"; `nes-view --hue`, the `h` key cycling
  0°, −15°, −30°) gives the TV look at −30°. The wiki's sample decoder's +3.9 phase constant belongs to its
  scanline context and wasn't used.
- **X6 (indrajala-rl #23, indrajala-nes #18):** the episode file is the trace format, version 2: annotation
  records after each decision (`encode_decision`: chosen and taken action, reward, flags, the observation's
  ids and kinds, action probabilities), the metadata naming the ROM's SHA-1, the grid and the action set's
  buttons; `scripts/record_episode.py` writes it (`--policy random|right-jump|run`). `nes-view` on `eframe`
  0.37: the replay on a pixel-mode console, RAM checked against the file every frame and restore; the
  grid and kinds overlaid; the decision's action, reward, flags and probabilities; RAM (changed bytes),
  OAM and palette panels; frame and decision steps, 1×, 2×, max; live play behind a `Pad` trait; headless
  `--snapshot` and `--gif`. **Done-when, on `pyramidon`: the 12-action 1-1 run (seed 1, 358 decisions)
  recorded on the Rust console and replayed in pixel mode: 1,669 frames, RAM equal to the file's on every
  one;** the owner saw the snapshots and the GIF. Building eframe's tree with 8 jobs at
  `codegen-units = 1` ran `pyramidon` (5 GB, no swap) out of memory: build with `-j 2` under a memory cap.
- **X7 (indrajala-rl #24, indrajala-nes #17, and #18's recordings):** both no-ROM checks refuse images
  and videos by extension and by header (PNG, GIF, JPEG, Matroska/WebM, RIFF, MP4's `ftyp`);
  `recordings/` gitignored. The viewer saves pictures (`p`), videos (`v`, through `ffmpeg` when installed)
  and GIFs (`--gif`, the `gif` crate, no external tool) to `~/nes-recordings`, refused inside a git
  repository.

## Later (the owner): a pure-Rust console with a USB controller

The owner (2026-11-06): "we will also later build a pure-rust console using a usb-controller". Not planned
here; this plan keeps the way open:
- **Input** in `nes-view` goes through a small trait (`Pad`: buttons each frame), with the keyboard, an
  episode file and, later, a USB gamepad (`gilrs`, MIT/Apache) behind it.
- **Pacing:** the viewer can run at the NES's own rate (NTSC: 60.0988 frames a second), not only as fast as
  it goes; the console then needs audio-led or display-synced pacing.
- **Sound:** a playable console needs a real APU behind D15's `Apu` trait (pulse, triangle, noise, DMC,
  the frame counter, mixing, resampling to the output's rate): its own plan when the console is.
- **The fuller PPU (V2)** is what such a console wants for games beyond SMB, as are more mappers (D16).

## Not planned
- Pixel observations for training (a scope change for the NES plan, the owner's).
- Audio (D15's silent APU stays, until the console above).
- A general emulator UI: debugger, cheats, other mappers.
- The NTSC signal itself (artefacts, composite blur): the palette only.

## Risks

| Risk | Effect | Answer |
|---|---|---|
| Pixel mode slows tile mode | training slower | the type parameter (D27); X1's throughput check |
| The modes differ on a CPU-visible point | the gate fails | that's the check working: the wiki decides which mode is wrong |
| FCEUmm's pixels differ at a mid-frame split | X5's gate fails on a line | diagnosed as in the parity sub-plan: whose timing; Mesen's frames as a third view if needed |
| Game art leaves a machine | the ROM rules broken | frames only on screen or in gitignored local directories; the no-ROM check refuses images; a summary of numbers only crosses machines |
| An episode file and the viewer's console disagree | a wrong overlay | the file's RAM (whole, every frame and restore: the trace format) checked as it replays, disagreements counted and shown; the console the same as Python's (E6) |

## Effort
About 6-8 days in all: X1 ½, X2 1, X3 1-1½, X4 ½ plus a runner hour, X5 1, X6 2 (the viewer 1, the episode file and its writers 1), X7 ½.
