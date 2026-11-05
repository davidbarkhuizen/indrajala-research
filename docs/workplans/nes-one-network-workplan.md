# Workplan: how far can one network take Super Mario Bros?

**Status: detailed 2026-11-05 through the gate (stages 0-4), with a PR-by-PR execution plan; later stages stay brief until it's passed.** The owner: "lets write it up - gated on
successfully learning 1-1 - we are only interested as to how far we can take 1 network - using tiles, not pixels"; then "now write up a detailed version
of the workplan". On parallelism and the emulator: "you decide whats best (fastest, parallelisable, I guess)", and a Rust emulator, "designed from the ground
up for integration with an nn", "based on existing os code and designs", permitted "if the emulator is the bottleneck". On its shape: "build it with a clean mapper interface and a separate per-game observation layer, implement only mapper 0 and SMB at first, and add more when another game is actually wanted. That costs very little extra now." It replaces the unseen-levels
plan (`git show 214b849:docs/workplans/nes-unseen-levels-workplan.md`). Decisions are settled under the owner's delegation. **O1 settled 2026-11-05: the owner's go ("start working through the nes workplan").** Stage 0 under way.

**The question.** Train **one network**, on tiles, over the known levels of NES Super Mario Bros under sticky actions. **How many of the 32 levels can it clear?**
The answer is a count, so a partial result is still a result.

**The gate.** Nothing past stage 4 starts until the network clears 1-1 (stage 4's rule).

## In and out of scope

- **In:** one network; tile observations; known levels; sticky actions; CPU.
- **Out, by the owner's decision:** pixels; one network per level, even as a fallback; held-out and generated levels; generalisation claims.

## The IDs, in time order

| ID | When | Short label | What it is |
|---|---|---|---|
| D1 | 2026-11-05 | the observation | Mario's tile buffer and sprite table from RAM, as one-hot channels |
| D2 | 2026-11-05 | the network | a small conv net; policy and value as columns of one output layer |
| D3 | 2026-11-05 | the algorithm | PPO, one fixed configuration across all levels |
| D4 | 2026-11-05 | the emulator | `nes-py` to the gate; a Rust emulator on a measured trigger (D10) |
| D5 | 2026-11-05 | sticky actions | a repeat chance on each decision, so a button sequence can't be memorised |
| D6 | 2026-11-05 | the ladder | one network grown over the levels, every earlier level retested |
| D7 | 2026-11-05 | the repositories | ml's primitives; one new repo, indrajala-rl; runs in indrajala-studies |
| D8 | 2026-11-05 | the remedies | one at a time, each for a named stall |
| D9 | 2026-11-05 | the parallel layout | emulators in parallel per machine, seeds across machines; the Pi 4 for playback only |
| D10 | 2026-11-05 | the Rust trigger | build it when emulation is over half of a step, after conv is threaded |
| D11 | 2026-11-05 | the conv threads | thread conv's forward pass first: the cheapest speedup in the plan |
| D12 | 2026-11-05 | the seams | a per-game layer from the start; a mapper interface in the Rust emulator; only SMB and mapper 0 implemented |
| O1 | 2026-11-05 | the start | the owner's go: stages 0-3 start now, ahead of the paused plans |

## The probe (2026-11-05, on `klip`)

A scratch probe with the owner's permission; **it installed the `nes-py` 9.0.1 wheel in a scratch venv, ran under the thermal guard (peak 55 C), and was deleted afterwards, with the ROM's copy.**
Stage 0 makes it a repository tool. `klip` has 8 threads on 4 cores; the library was the crate installed there, which predates later work.

| Measured | Result |
|---|---|
| Determinism | same RAM hash after 1,500 frames, run twice |
| Reset to a saved start | 0.04 ms |
| Tile grid decode, in Python | 13 µs |
| Emulation, drawing every frame | 394 frames/s at 1 process, 1,577 at 4, 2,159 at 8: **540 decisions/s at a 4-frame skip** |
| Tile network, 32 channels, conv 16 and 32, batch 256 | **1,392 samples/s** learning, **1,734** forward |
| Same, 64 channels | 793 learning, 909 forward |
| Same, 32 channels, conv 32 and 64 | 882 learning, 1,160 forward |

**Checked by eye against rendered frames, on 1-1 and 1-3:** the buffer `$0500-$069F` as 2 pages of 13 rows by 16 columns, cropped by `$071A`/`$071C`, puts pipes, ground, platforms and coins in the right cells, with its first row at screen line 32.
**Scenery isn't in it** (bushes, hills, tree trunks), so it holds what play depends on. Writing `$075F`, `$075C` and `$0760` reached the right world and stage on all 8 levels tried (1-1 to 1-4, 2-2, 4-4, 7-4, 8-4). Those 8 levels used 27 tile values, over a partial run.

**Not yet checked:** all 32 levels; PPO's whole loop, as Python overhead isn't in these numbers. `stone`: measured at stage 0 (Findings).

## Is the emulator the bottleneck? Not yet, but it's close

One PPO step at 3 epochs, all of `klip`'s threads on each phase in turn, from the table's 32-channel row:

| Phase | Time a step | Share |
|---|---|---|
| Emulation | 1.85 ms | 40% |
| Network forward | 0.58 ms | 13% |
| Network learning | 2.16 ms | 47% |
| **Total** | **4.58 ms (218 steps/s)** | |

| Change | Overall speedup | Emulation's share after |
|---|---|---|
| Emulator 10× faster | 1.57× | 6% |
| Emulator infinitely fast | 1.68× | 0% |
| Network 2× faster | 1.42× | 58% |
| Network 4× faster | 1.81× | 73% |

So the network takes the larger share today, and a perfect emulator gains under 1.7×. **But conv's forward pass isn't threaded yet (the crate's README), so faster network code is likely, and it would make emulation the majority.** This sets the order: D11, then D10.

## Budget

At 218 steps/s on `klip` alone:

| Steps | One run |
|---|---|
| 10M (the gate) | ~13 hours |
| 100M (a late rung, if Sonic is a guide) | ~5 days |
| 300M (the stopping rule) | ~16 days |

The gate's 5 seeds are about 2.6 days on `klip` alone, less with `stone`. If 64 channels are needed the step takes about 6.7 ms, roughly half again. **These leave out PPO's own Python, and stage 3 replaces them.** Budgets are in environment steps.

## What the evidence says

Most of these are project READMEs or summaries, read as such. None is a controlled study.

- **Per-level networks nearly finish the game.** The best-known project reports [31 of 32](https://github.com/vietnh1009/Super-mario-bros-PPO-pytorch), tuning the learning rate per level. A
  [mirror](https://github.com/numz/Super-mario-bros-PPO-pytorch) reports 29, and says 1-3 failed 70 times before training. A [summary](https://www.sourcepulse.org/projects/1539793) says 8-4 went unsolved.
- **One network over the whole game: I found no result.** On Sonic, joint training took "hundreds of millions of timesteps" to converge (`nichol-2018-gotta-learn-fast-generalization-rl`).
- **1-1 is within reach:** a [student comparison](https://cs224r.stanford.edu/projects/pdfs/CS224R_Project-1.pdf) reports 96% clears, and a [public model](https://huggingface.co/tsilva/SuperMarioBros-NES_Level1) has a 4.5M-step checkpoint.
- **I found no full-game result using sticky actions or tiles.**

**My judgement of the odds, not a measurement:** 1-1 ~95%; World 1 ~75%; most levels ~40-50%; all 32 ~10-15%.

## Decisions

- **D1. The observation.**
  - (a) *Chosen.* RAM's tile buffer and sprite table. Pros: no emulator change, verified above, scenery already gone. Cons: Mario only, which is all we need; it may show hidden blocks a player can't see, acceptable for known levels and to be stated.
  - (b) A patched `nes-py` exposing the PPU's nametable. Pros: generic. Cons: a fork, for generality unused here.
  - **The input,** `H, W = 13, 16` cells:
    - **Tiles:** one-hot over the values seen, grouped only if the census exceeds about 32. Stage 2's census of all 32 levels fixes this.
    - **Sprites, for each of the last 4 decisions:** presence, plus **offset within its cell in x and y as values in those channels.** A 16-pixel grid alone would lose the precision that jumps need.
    - **Enemy kind:** sprite attributes are kept, as red and green Koopas are drawn alike and behave differently.
    - **Mario's size** as a constant plane.
    - **Why tiles aren't stacked:** they rarely change, and stacking would multiply the channels.
- **D2. The network.**
  - (a) *Chosen.* `Conv(3,16), Pool(2), Conv(3,32), Dense(256,"relu")`, then one linear output layer of `actions + 1` columns, the last being the value. Pros: runs on today's layers, with no conv padding or second head. Cons: capacity may run short, D8's first remedy.
  - (b) IMPALA-style residual. Pros: more capacity. Cons: needs padding and conv residuals. Only if (a) stalls for capacity.
- **D3. The algorithm.** PPO, with the [Procgen paper](https://arxiv.org/abs/1912.01588)'s settings as the start: λ .95, 256 steps a rollout, 3 epochs, 8 minibatches, clip .2. γ .99, since a decision is 4 frames and that horizon is about 7 seconds. The learning rate and entropy bonus come from its appendix, fixed by stage 3's control.
  - (b) The Rainbow family. Pros: can need fewer samples. Cons: replay memory; lost to joint PPO on Sonic.
- **D4. The emulator.**
  - (a) *Chosen.* `nes-py` (MIT) to the gate, behind a thin environment of our own. Pros: measured here, deterministic, with Python 3.14 wheels on x86-64 and aarch64; ready today. Cons: draws every frame, and Python on each step.
    **Install the wheel only.** Its repository has commercial game ROMs in its tests. `gym-super-mario-bros` also commits Nintendo ROM files with a notice granting no licence, so we don't install it; its MIT source is a reference for RAM addresses and start-up.
  - (b) The Rust emulator now. Pros: the owner's interest, a permanent speedup. Cons: 1-2 weeks before any learning is tested, for at most 1.7× today. Deferred to D10.
- **D5. Sticky actions.**
  - (a) *Chosen.* With chance 0.25 a decision repeats the previous action. Pros: forces reacting, and a count of levels then means something. Cons: precise jumps get harder; published numbers aren't comparable.
  - (b) None. Cons: the NES is deterministic, so a memorised sequence would count.
- **D6. The ladder.** The network is never reinitialised. Every earlier level is retested at every rung, so forgetting counts. Rungs: 1-1, World 1, then a world at a time. A stalled level is recorded and set aside, and the ladder goes on.
- **D7. The repositories.**
  - (a) *Chosen.* **indrajala-ml:** D11's threads and the learning entry. **indrajala-rl (new):** PPO, the generic environment, Mario's layer behind D12's seam, probes as tools; no ROMs, and a `.gitignore` for `*.nes`. **indrajala-studies:** runs and their data. **indrajala-research:** this plan and the note.
    Pros: one new repository; ml stays a library. Cons: game code beside the RL core, kept apart by D12's seam.
  - (b) Separate RL and NES repositories. Cons: more pinning for one game. Taken only if D10 fires, as the emulator would be its own repository.
- **D8. The remedies.** One at a time, each for a stall it could explain, adopted on fresh seeds rather than by rescuing chosen ones: a larger network; level sampling weighted to levels still being learned; memory for the castle mazes (4-4, 7-4, 8-4, from general knowledge); an exploration bonus for 8-4.
- **D9. The parallel layout.**
  - (a) *Chosen.* Within a machine, one emulator process per core, decisions batched across them, gradients on the crate's threads. Across machines, whole seeds. Pros: emulators scale freely, though 8 processes on 4 cores gave only 1.4× over 4; seeds are what the gate needs; no network in the loop. Cons: a run is limited to one machine.
  - (b) One run across machines. Cons: weights on the wire each update, and copying to `klip` managed only a few MB/s.
  - (c) The Pi 4 for rollouts. Cons: slowest in the fleet, and litshe, a Pi 5, is limited by its memory bus. **It's for playback after the gate:** at 15 decisions a second it should fit, unmeasured. `nes-py` has the aarch64 wheel.
- **D10. The Rust trigger.** The owner's permission holds "if the emulator is the bottleneck", read here as:
  - **Build when** emulation is over half of a measured PPO step, after D11, **and** a 10× faster emulator would save at least 1.5× overall. Measured at stage 3, and again at any rung.
  - **Why not simply at 40%:** a perfect emulator would gain under 1.7× today, so the network comes first.
  - Stage E below is the plan for it.
- **D11. The conv threads.**
  - (a) *Chosen.* Thread conv's forward pass in the crate, as attention's and dense's are, before stage 4. Pros: small; the same machinery; bits unchanged by the crate's rule, as work splits by output; helps every later stage. Cons: `jebel` can't time it.
    **It's built for use, with its timings marked provisional and no speedup claimed,** in keeping with the parked plan's rule on claims (`docs/workplans/infrastructure/jebel-parked-workplan.md` in indrajala-ml, its D12). Golden runs on `pyramidon` and `litshe` as `jebel` is out.
  - (b) Leave it. Cons: the network stays the largest cost, at no saving.

- **D12. The seams,** the owner's design rule. Clean boundaries now, one implementation behind each, and more only when another game is actually wanted.
  - **The per-game layer, used from stage 2:** a `Game` protocol holding everything specific to one game: the ROM's hash, level starts, the observation decoder and its channel count, reward, clear and death detection, action set. `games/smb.py` is its only implementation. The environment, vector runner, PPO and evaluation know no RAM address and never import it directly. A test enforces that.
  - **The console layer:** a small `Console` protocol (`step`, `ram`, `save`, `restore`), with `nes-py` behind it now. So stage E swaps one implementation, and **Mario's code doesn't change.** A per-game observation in Rust, if D10 fires, sits behind the same split.
  - **The mapper interface, in stage E only:** CPU and PPU reach the cartridge only through a `Mapper` trait, mapper 0 its only implementation. `nes-py` has its own mappers, so nothing of ours is needed before then.
  - **Not built:** other mappers, games, a plugin system or configuration for any of them. The protocols hold what SMB needs and nothing speculative; a second game may change them, and that's its cost to bear.
  - **Pros:** very little extra now; swapping the emulator stays cheap; a second game, if ever wanted, needs a new layer rather than a rewrite. **Cons:** an extra indirection on the hot path, so the Rust design keeps the mapper call monomorphised (a generic, not a virtual call) and the batched decoder per game. D1's RAM choice stays, now behind the seam.

## Stages to the gate

Each is its own PRs, nothing stacked. Crate changes land in indrajala-math-rust first, then a Bump in indrajala-ml, then in indrajala-studies.

### Stage 0: tools and the fuller measure

- **indrajala-rl created,** private until there's something to release: `pyproject`, CI (ruff, pyright, pytest), a `.gitignore` for `*.nes`, and a CI check that fails on any `*.nes` in the tree. CI has no ROM, so ROM-backed tests skip there and run on the machines.
- **The ROM:** `~/roms/super-mario-bros.nes` on `pyramidon`, copied to runners into a private `~/roms`. Tools check its SHA-1 (`ab30029efec6ccfc5d65dfda7fbc6e6489a80805`) and refuse anything else.
- **The probe as a tool:** `scripts/probe_throughput.py`, reporting emulation, forward and learning times, on `klip` and `stone`.
- **Exit:** both machines measured with a current crate.

### Stage 1: library (indrajala-ml, indrajala-math-rust)

1. **Thread conv's forward pass** (D11): the crate, tests of bits at 1 to 8 threads, the Bump, golden run.
2. **A learning entry from an output gradient:** `learn_batch_output_gradient(learning_rate, X, G, clip_norm)`, where `G` is the loss's gradient at the output, `(batch, outputs)`, on the array networks, numpy and Rust.
   - **Tests:** with `G` set to cross-entropy's gradient, bit-identical to `learn_batch`; a finite-difference check on a small network; a run on numpy against Rust.
   - **Not added to pure Python:** it's a training entry for array networks, not a layer. Pros: less to build. Cons: a small break from the three-implementations habit, recorded here.
3. **Inputs with no element-by-element conversion:** a numpy batch into the crate's array at memory speed, for forward and learning. **Needed, by stage 0's measure:** the conversion today costs as much as a forward pass (Findings).

**Exit:** golden run bit-identical, CI green. Batch 256 at these sizes is expected to fit `klip`'s 4.5 GB, as the probe's did, so no memory work is planned.

### Stage 2: the environment (indrajala-rl)

- **Layout (D12):** `console.py` (the protocol and `nes-py` behind it), `games/base.py` (the `Game` protocol), `games/smb.py` (everything below that's Mario's), `env.py` (generic).
- **`NesEnv(console, game, level, sticky, seed)`:** starts from a saved post-title state, one per level, built once with the game's start-up. Resets by restore (0.04 ms). Skips the same animations as the reference environment.
- **Actions:** 7 (none, right, right+A, right+B, right+A+B, A, left), held for 4 frames. Sticky actions with the env's own seeded generator.
- **Reward, written once and then fixed:** change in furthest x, scaled; a small clock penalty; a death penalty; a clear bonus. Mirrors the reference environment's shape without its score and coin terms. Clipped.
- **Episodes:** one life. Ends on a clear, on death, or at a decision limit, which is truncated rather than terminal, so the value function bootstraps.
- **`SMB.observe(ram) -> array`:** D1's input, in NumPy with no Python per cell.
- **Vector runner:** one process per core over shared memory, with no pickling per step.
- **A boundary test:** nothing outside `games/` holds a RAM address or a Mario term, and a tiny fake `Game` on a fake `Console` runs the environment and the vector runner with no ROM, so CI covers them.
- **Tests with the ROM (on machines):**
  - grid against rendered frames over all 32 levels, by a script producing contact sheets for reading by eye, kept out of the repository (they contain game art);
  - a tile census per level, which fixes the channels;
  - every level reached and its clear detected, driven by a recorded or scripted run where one is feasible; **a level with no driven clear is listed as unverified;**
  - determinism across two runs and across the vector runner;
  - sticky actions' rate.
- **Exit:** a table of all 32 levels: start, decoder check, tile census, clear detection.

### Stage 3: PPO and its control (indrajala-rl)

- **PPO:** rollouts, GAE, clipped policy and value losses, entropy bonus, advantage normalisation; forward-only losses in NumPy, returning `G` for stage 1's entry.
- **Unit tests:** GAE against hand-worked cases; `G` against finite differences of each loss; truncation bootstraps and termination doesn't.
- **The control, with no ROM:** a published reference implementation (CleanRL's PPO, or similar) and ours on the same small tasks: CartPole, then a MiniGrid task (MIT). PyTorch goes in a scratch venv on a runner, for the reference only. **Pass:** ours reaches the reference's return within a stated margin, on 5 seeds each. A silent PPO bug would look just like a hard level, so this comes first.
- **The step measured,** whole loop on `klip` and `stone`, and **D10 read for the first time.**
- **Exit:** control passed; budget table replaced with measured numbers.

### Stage 4: THE GATE, 1-1

Under the experiment design (`docs/protocols/experiment-design.md`). Claim and refutation registered before the data.

- **Feasibility, written beside the config and tested against it:**
  - **Representation:** every tile value in 1-1 has a channel, and the network's input matches.
  - **Budget:** the decision limit exceeds a clear's length, measured from a driven run.
  - **Action set:** the driven clear used only the 7 actions.
  - **Width:** conv 16 and 32 is the start; if probes show it's short, the cell changes before registering.
- **Probes first (D9's rule, existence before matrices):** short runs on `klip`, varied on the fly, until one network clears 1-1 under sticky actions.
- **Controls, each on the same score:** random play, and always-right with periodic jump. Neither should pass.
- **The registered batch:** 5 fresh seeds at the settled configuration, fixed before they start, no changes after. Up to 10M steps each, stopped at the first evaluation that passes, on `klip` and `stone`.
- **The score:** 100 attempts per seed under sticky actions, on an evaluation generator apart from training's. Reported: clear rate, furthest distance, steps to first pass, with Wilson intervals.
- **PASSES when at least 4 of 5 seeds each clear 1-1 in at least 90 of 100 attempts within 10M steps.** A network that passes without sticky actions but not with them doesn't count.
- **If it fails:** a diagnosis to the owner, not a longer run: the observation (does it hold what's needed?), the network, PPO, or the budget. No further stage starts.
- **Records:** the batch's manifest and readings in indrajala-studies' gitignored `data/`, the finding here. Networks in the library's format.

**Size to the gate:** one to two weeks of building, then about 3 days of machine time.

## The execution plan, PR by PR

The stages above say what each must deliver; this says in what order, in which files, and when the owner hears. One chunk a PR, squash-merged on green CI, nothing stacked. Time is my estimate of building, not machine time.

| # | Repository | PR | Touches | Done when | Time |
|---|---|---|---|---|---|
| 0.1 | indrajala-rl (new, private) | Scaffold | `pyproject`, CI, `ml` submodule, `.gitignore` and CI check for `*.nes` | CI green; a planted `*.nes` fails the check | hours |
| 0.2 | indrajala-rl | ROM check and throughput probe | `indrajala_rl/rom.py`, `scripts/probe_throughput.py` | a wrong SHA-1 is refused; `klip` and `stone` measured, into this plan's Findings | hours |
| 1.1 | indrajala-math-rust | Thread conv's forward | `core/src/nn/conv.rs`: `forward_batch`, `linear_forward_batch`, on `for_each_part` as its gradient already is; the README's Threads list | same bits at 1-8 threads; clippy; aarch64 check | 1 day |
| 1.2 | indrajala-ml | Bump `rust/` | the pin; provisional timings in the PR, no claim | golden bit-identical on `pyramidon` and `litshe` | hours |
| 1.3 | indrajala-ml | Learning from an output gradient | `array_network_base.py` (`learn_batch_output_gradient`); `Dense(n,"linear",output=True)` through `layer_specs.py`, `array_layer_builder.py`, `numpy/linear_array_layer.py`, `rust/linear_rust_array_layer.py` | Stage 1's three tests; golden unchanged | 1-2 days |
| 2.1 | indrajala-rl | The seams and the environment (D12) | `console.py`, `games/base.py`, `env.py`, sticky actions; a fake game and console for CI | boundary test; generic env tested with no ROM | 1 day |
| 2.1b | indrajala-rl | SMB's layer | `games/smb.py`: each RAM address with its source and whether verified, level starts, actions, reward, clear and death | determinism and sticky-rate tests, on machines | 1 day |
| 2.2 | indrajala-rl | Tile decoder and level table | `SMB.observe` in `games/smb.py`, census and contact-sheet scripts | all 32 levels read; **table to the owner** | 1-2 days |
| 2.3 | indrajala-rl | Vector runner | `vector.py`, shared memory, one process per core | same bits as serial; emulation speed within 10% of the probe's | 1 day |
| 3.1 | indrajala-rl | Losses and GAE | `ppo/losses.py`, `ppo/gae.py` | hand-worked cases; finite differences | 1 day |
| 3.2 | indrajala-rl | The PPO loop | `ppo/train.py`, checkpoints in the library's format, resume bit-identical | a run resumed equals one uninterrupted | 1-2 days |
| 3.3 | indrajala-rl | The control | reference in a scratch venv, `scripts/control.py` | ours within the stated margin; **result to the owner** | 1 day, then runs |
| 3.4 | indrajala-research | Budget and D10's first reading | this plan | measured table replaces the estimates; **the Rust decision to the owner** | hours |
| 4.1 | indrajala-rl | Evaluation and feasibility | `evaluate.py`, feasibility tests, the controls | the controls score as expected | 1 day |
| — | `klip` | Probes on 1-1 | none; settings into the next PR | one network clears 1-1 under sticky actions | days of machine time |
| 4.2 | indrajala-research, indrajala-studies | Registration | claim and refutation here, config committed with tests against it | merged **before** the batch starts | hours |
| — | `klip`, `stone` | The batch | read at its end only: no early stops beyond the registered rule | 5 seeds ended | ~3 days |
| 4.3 | indrajala-research | The gate's result | Findings; manifest in `data/` | **pass or diagnosis to the owner** | hours |

**Order.** Stage 0, then stages 1 and 2 side by side, as neither needs the other. Stage 3 needs both. Stage E, if D10 fires at 3.4, goes before stage 4 only if the owner chooses.

**Machines.** Development on `pyramidon`; no training or emulation there. Probes and the batch on `klip` (thermal guard, 85 C, `ulimit -v 4500000`, with the emulator processes counted) and `stone` (at most 8 threads, sandboxed: code by bundle, no GitHub, no tokens). A new runner's first step: `~/roms` private, ROM copied, SHA-1 checked.

**Before merging, each time:** tests and lint run with chained exit codes, not through a pipe; `gh pr checks` read only once checks have started (working-notes).

**The owner hears at:** the level table (2.2), the control (3.3), the Rust decision (3.4), the gate (4.3), and at once if anything here proves false.

## After the gate (each planned then)

5. **World 1.** The go/no-go on one network holding several levels, 1-3 being the known awkward one.
6. **World by world,** with D8's remedies as stalls call for them.
7. **The reading:** fresh seeds at the final configuration, then a note: levels cleared per seed, what each remedy did, and a full playthrough, shown on the Pi 4 (D9).

**The result:** levels cleared in at least 90% of 100 sticky attempts, by the best network and across seeds, also at 50%, with each level's furthest distance. **The stopping rule:** a rung adds no level within its budget after the remedies that could explain the stall, or a run passes 300M steps, which goes back to the owner. **Not claimed:** generalisation, or anything about levels it hasn't trained on.

## Stage E: the Rust emulator (only on D10's trigger)

**How much work.** About **1-2 weeks** for a headless emulator that runs only Super Mario Bros, in a new repository, `indrajala-nes`. A general emulator, with audio and many mappers, is months and isn't proposed. The first game is mapper 0, the simplest case. My estimate, and the debugging is its most uncertain part:

| Part | Lines, roughly | Time |
|---|---|---|
| 6502 CPU, bus, `Mapper` trait, mapper 0 | 1,000-1,500 | 2-3 days |
| PPU with no pixels: registers, timing, VBlank NMI, sprite-0 hit, scroll | 500-800 | 2-3 days |
| APU stubbed to what the game reads | ~100 | hours |
| Batched API, PyO3, observation | 300-500 | 1-2 days |
| Parity debugging against `nes-py` | | 2-5 days |

**Its seams (D12):** a `Mapper` trait, with mapper 0 alone; a per-game observation, with SMB alone. Adding either later is a new implementation, not a change to the CPU or PPU. No audio beyond what SMB reads. A second mapper needs its own tests and may need more PPU accuracy than this headless design has; that cost is taken when wanted.

**Designed for a network:**
- **No pixels:** game logic needs VBlank and the status bar's sprite-0 hit, not an image.
- **A batch-first API:** `step(actions, out_obs, out_reward, out_done)` over N consoles in structure-of-arrays form, on the crate's thread pool, with no Python per console.
- **Observation in place:** tiles and sprites decoded straight into the network's input array, with no copy.
- **Reset by copy:** a console's whole state is a few KB, so a restore is a memcpy.
- **Sticky actions and seeds inside,** in the crate's generator. Determinism by construction.

**Expected speed: 10-40× `nes-py` a core, from a console needing about 30,000 CPU cycles a frame. An estimate, not a measure.** NeSLE's notes support the direction: `nes-py` draws every frame, which this skips.

**Based on existing code:**

| Source | Licence | Used for |
|---|---|---|
| [NeSLE](https://github.com/hbofz/NeSLE) | MIT | the design: batched NROM consoles, drawing skipped, RAM observations, its validation approach |
| [`nes-py`](https://github.com/Kautenja/nes-py) | MIT | the C++ structure, and the **parity oracle** |
| [TetaNES](https://github.com/lukexor/tetanes), [pinky](https://github.com/koute/pinky) | Apache-2.0 | Rust CPU and PPU structure |
| [takahirox/nes-rust](https://github.com/takahirox/nes-rust) | MIT | a smaller Rust reference |
| Mesen2, FCEUX, starrhorne/nes-rust | **GPL** | **not read for code.** Hardware behaviour from the NESdev wiki instead |

Licence files are confirmed at the time; MIT and Apache code carries its notices where adapted.

**Verification, the part that makes it trustworthy:**
- **CPU:** the Klaus functional test and `nestest`, as NeSLE gates on. Test ROMs are fetched by a script and never committed; their licences vary.
- **PPU:** `ppu_vbl_nmi` and `sprite_hit_tests`, as far as this headless design needs.
- **The oracle:** RAM hash frame by frame against `nes-py`, on recorded action streams through all 32 levels. **Pass: no divergence.** RAM is all the game and the network see, so this is sufficient for our purpose.
- **Then a gain measured,** with the trigger's numbers before and after.

## Risks

- **Forgetting across levels,** specific to one network. D6's retests measure it; D8's first two remedies answer it.
- **Fixed configuration:** the 31 of 32 needed per-level tuning, unavailable here, so the count may stop well short.
- **The observation** may omit something play needs. Stage 2 checks that it matches the screen, not that it suffices; the gate tests that, and the cell offsets are the likeliest fix.
- **Long runs on a thin fleet:** `jebel` out, `stone` at 70%.
- **Threading with `jebel` out:** golden checked on two machines, not the usual pair.
- **Unverified:** the whole PPO loop's speed; `stone`; the Rust estimates; the castle mechanics; all of the odds.

## Open for the owner (none now)

- **O1. The start. Settled 2026-11-05:** the owner's go, "start working through the nes workplan". Stages 0-3 go ahead of the paused general algebras, arbitrary-length addition and factorisation plans, which stay paused. This is a new direction beside machine discovery, and the certificate doesn't apply to it.

Nothing else is open for the owner before stage 2.2's level table.

## Findings

Stage 0's scratch probe, above. Findings from each stage go here.

### Stage 0: the probe as a tool, on `klip` and `stone` (2026-11-05)

`scripts/probe_throughput.py` in indrajala-rl (PR 0.2), with ml at `879aef6` and the crate at `d9126cb`, both machines on the same commits. Each figure is the median of 5 timed runs.
`klip` under the thermal guard (peak 53 C); `stone` at 8 processes and 8 crate threads, its 70% share. Readings: indrajala-studies' gitignored `data/nes-probe/`, with a manifest.

| Measured | `klip` (4 cores, 8 threads) | `stone` (i7-1255U, 8 of 12 threads) |
|---|---|---|
| Emulation, one console a process: 1, 4, 8 processes | 403, 1,606, 2,144 frames/s | 1,107, 3,219, 4,966 frames/s |
| Decisions/s at 8 processes, 4-frame skip | 536 | 1,242 |
| nes-py's native vector emulator, 1, 8, 32 consoles in one process | 394, 411, 455 frames/s | 1,054, 1,077, 1,134 frames/s |
| Network, 32 channels, conv 16 and 32, batch 256: forward, learning | 1,657, 1,354 samples/s (4 threads) | 5,577, 4,329 samples/s (8 threads) |
| Same, 64 channels | 859, 730 | 2,828, 2,271 |
| numpy batch to the crate's array, 32 and 64 channels | 1,622, 815 samples/s | 5,006, 2,495 samples/s |

- **`klip` repeats the scratch probe** within 3% (536 decisions/s against 540; learning 1,354 against 1,392).
- **nes-py's vector emulator runs its consoles on one thread:** 32 consoles in one process go no faster than 1. D9's one process a core stands.
- **New: the input's conversion costs as much as a forward pass.** The crate's `Array` takes an ndarray but converts element by element: about 0.6 ms a sample on `klip`, 0.2 ms on `stone`. **Stage 1's item 3 is needed, not conditional:** the observation must reach the crate without that conversion.

**One step at 3 epochs, each phase in turn on all threads,** conversion counted once for the rollout's forward and once for learning:

| ms a decision | `klip` | `stone` |
|---|---|---|
| Emulation | 1.87 | 0.81 |
| Network forward | 0.60 | 0.18 |
| Network learning | 2.22 | 0.69 |
| Conversion | 1.23 | 0.40 |
| **Total** | **5.92 (169 steps/s)** | **2.08 (481 steps/s)** |
| Emulation's share | 32% | 39% |

**D10's preliminary reading: not met on either machine,** before D11's threads and the conversion fix, both of which raise emulation's share. Stage 3 reads it on the whole loop. **The budget, still without PPO's Python:** 10M steps is about 16 hours on `klip` and 6 on `stone`, so the gate's 5 seeds are roughly a day and a half on both. `stone` does about 2.8× `klip`'s steps, and takes the larger share of seeds.
