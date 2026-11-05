# Workplan: how far can one network take Super Mario Bros?

**Status: drafted 2026-11-05 at the owner's direction, high level.** The owner: "lets write it up - gated on successfully learning 1-1 -
we are only interested as to how far we can take 1 network - using tiles, not pixels". It replaces the unseen-levels plan the same day
(`git show 214b849:docs/workplans/nes-unseen-levels-workplan.md`, kept for its literature and its budget). D1-D9 are settled under the
owner's standing delegation ("you decide whats best (fastest, parallelisable, I guess)"). **O1-O2 are the owner's.** Nothing is built.

**The question.** Train **one network**, on tiles, over the known levels of NES Super Mario Bros under sticky actions. **How many of the 32
levels can it clear?** The answer is a count, so a partial result is still a result.

**The gate.** Nothing past stage 4 is planned or started until the network clears 1-1.

## In and out of scope

- **In:** one network; tile observations; known levels; sticky actions; CPU.
- **Out, by the owner's decision:** pixels; one network per level, including as a fallback; held-out levels, generated levels and
  generalisation. Those can return later, but nothing here is built for them.

## The IDs, in time order

| ID | When | Short label | What it is |
|---|---|---|---|
| D1 | 2026-11-05 | the observation | Mario's own tile buffer and sprite table, read from RAM |
| D2 | 2026-11-05 | the network | a small conv net over embedded tiles with policy and value heads, one size up if needed |
| D3 | 2026-11-05 | the algorithm | PPO with one fixed configuration across all levels |
| D4 | 2026-11-05 | the emulator | `nes-py` directly, without `gym-super-mario-bros` |
| D5 | 2026-11-05 | sticky actions | a held button with a fixed chance of repeating, so a button sequence can't be memorised |
| D6 | 2026-11-05 | the ladder | one network grown over the levels, every earlier level retested |
| D7 | 2026-11-05 | the repositories | indrajala-ml's primitives, one new repo, indrajala-rl; runs in indrajala-studies |
| D8 | 2026-11-05 | the remedies | one at a time and only for a named stall: size, level sampling, memory, an exploration bonus |
| D9 | 2026-11-05 | the parallel layout | emulators in parallel within a machine, seeds in parallel across machines, no training across the network; the Pi 4 for playback only |
| O1 | open | the ROM | the owner supplies Super Mario Bros; it goes in no repository or record |
| O2 | open | the start | the owner's go, and its place against the paused plans |

## What the evidence says

Most of these are project READMEs or summaries, read as such. None is a controlled study.

- **Per-level networks nearly finish the game.** The best-known PPO project reports
  [31 of 32](https://github.com/vietnh1009/Super-mario-bros-PPO-pytorch), tuning the learning rate per level. A
  [mirror](https://github.com/numz/Super-mario-bros-PPO-pytorch) reports 29, and says 1-3 failed 70 times before training. A
  [summary](https://www.sourcepulse.org/projects/1539793) says 8-4 went unsolved, for its puzzle-like path choices.
- **One network over the whole game: I found no result.** The nearest analogue is Sonic, where joint training took "hundreds of millions of
  timesteps" to converge (`nichol-2018-gotta-learn-fast-generalization-rl`).
- **1-1 is well within reach.** A [student comparison](https://cs224r.stanford.edu/projects/pdfs/CS224R_Project-1.pdf) reports 96% clears with
  PPO, and a [public model](https://huggingface.co/tsilva/SuperMarioBros-NES_Level1) has a 4.5M-step checkpoint.
- **I found no full-game result using sticky actions or tiles.** Both are untested here.

**My judgement of the odds, not a measurement:** 1-1 ~95%; World 1 ~75%; most levels ~40-50%; all 32 ~10-15%. Worth setting beside them: this
network can't take the per-level tuning that the 31 of 32 relied on.

## Decisions

- **D1. The observation.** `nes-py` exposes RAM and the screen, but not the PPU's tile memory.
  - (a) *Chosen.* The game's level tile buffer and the sprite table in RAM, cropped to the visible screen by the scroll position. Sprite attributes are
    kept as they distinguish enemies drawn alike, such as red and green Koopas, which behave differently. Pros: no emulator change; small; no colour.
    Cons: Mario only, which is now all we need; addresses to verify (from general knowledge, the tile buffer at `$0500-$069F`); it may reveal hidden blocks
    a player can't see, which is acceptable for known levels but must be stated.
  - (b) A patched `nes-py` exposing the PPU's nametable. Pros: generic across NES games. Cons: a fork to maintain, for a generality this plan doesn't use.
  - **Stage 2 checks it:** the decoded grid compared with rendered frames across all 32 levels, before any training.
- **D2. The network.**
  - (a) *Chosen.* Tile embedding, 3 conv layers with pooling, a dense layer, policy and value heads. Pros: runs in the library nearly as it is. Cons: capacity
    may run short over 32 levels, so size is D8's first remedy.
  - (b) IMPALA-style residual encoder from the start. Pros: more capacity, and the best evidence on generalisation. Cons: needs conv padding and conv residuals,
    for a benefit shown on unseen levels, which we've dropped. Built only if (a) stalls for capacity.
- **D3. The algorithm.**
  - (a) *Chosen.* PPO, one fixed configuration throughout. Pros: Sonic's best joint baseline; no replay memory on small machines. Cons: needs many samples; no
    per-level tuning.
  - (b) The Rainbow family. Pros: can need fewer samples. Cons: replay memory; lost to joint PPO on Sonic.
- **D4. The emulator.**
  - (a) *Chosen.* `nes-py` 9.0 (MIT), behind our own thin environment. Pros: maintained, with wheels for Python 3.14 on x86-64 and aarch64. Cons: we write the rewards and level starts.
    **Install the wheel only (about 150 KB, too small to hold more than a little), and never clone its repository, which has commercial game ROMs under `nes_py/tests/games/`.**
  - (b) `gym-super-mario-bros`. Pros: those already written. Cons: **its repository commits Nintendo ROM files, and its own notice grants no licence to them.** We don't
    install it. Its source is MIT, and may be read for reference.
- **D5. Sticky actions.** Otherwise a deterministic console rewards a memorised button sequence, and a count of levels would prove little.
  - (a) *Chosen.* At each decision the previous action repeats with a fixed chance, 0.25 as the usual setting (to be confirmed at stage 3). Pros: forces reacting; cheap.
    Cons: precise jumps get harder, and published numbers aren't comparable.
  - (b) None. Pros: easier. Cons: the owner's goal asks for them.
- **D6. The ladder.** Each rung adds levels to the same network, which is never reinitialised. Every earlier level is retested at every rung, so forgetting
  counts against the score. Rungs follow game order: 1-1 (the gate), World 1, then a world at a time.
  - **A level that stalls past its budget** is recorded and set aside, and the ladder carries on. The result counts what's cleared.
- **D7. The repositories.**
  - (a) *Chosen.* **indrajala-ml:** a learning entry taking an output gradient, two output heads, and batch memory fitting 4.5 GB. **indrajala-rl (new):** rollouts, PPO, the Mario
    environment and the tile decoder, no ROMs. **indrajala-studies:** the runs. Pros: one new repository; ml stays a library. Cons: game code beside the RL core, to split out if another game ever comes.
  - (b) Separate RL and NES repositories. Pros: a clean split. Cons: more pinning for one game.
- **D8. The remedies.** One at a time, each for a stall it could explain, adopted on fresh seeds rather than by rescuing chosen ones:
  1. a larger network, for forgetting or a plateau across levels;
  2. level sampling weighted to the levels still being learned;
  3. memory, for the castle mazes that loop until the right path is taken (4-4, 7-4, 8-4, from general knowledge);
  4. an exploration bonus, for 8-4's path choices.

- **D9. The parallel layout.** Fastest for the fleet we have, the owner's criterion.
  - (a) *Chosen.* **Within a machine:** one emulator process per core, with the network's inference batched across them and gradients on the crate's threads, alternating so each phase has the cores.
    **Across machines:** whole seeds, one to a machine at a time. Pros: emulation scales almost freely, as each console is independent; PPO needs no replay; seeds are what the gate and the ladder need anyway;
    no network in the loop. Cons: one run is limited to one machine's cores.
  - (b) One run across machines. Pros: more steps a second for one run. Cons: gradients or weights on the wire every update, and copying this project's addendum to `klip` managed only a few MB/s; a large build for a fleet of two.
  - (c) A batched Rust emulator. Pros: would remove the Python per step, and suits the crate. Cons: an emulator is a project of its own. Stage 2 measures it: built only if emulation, not gradients, is what limits a run.
  - (d) The Pi 4 for rollouts. Pros: more hardware. Cons: slowest in the fleet, and litshe, a Pi 5, is already limited by its memory bus; a network hop per step, or a copy of the network on it, which only adds a little to the emulation that isn't the
    larger cost. **Not for training. It's used after the gate for playing the trained network in an emulator, as a demonstration:** at about 15 decisions a second it should fit, though unmeasured. `nes-py` has an aarch64 wheel.

## The budget (feasibility)

**Measured** on `klip` (2026-11-05, one rough probe on pixels, an old crate, list conversion included): about 1 billion conv operations a second. `stone` wasn't measured; `jebel` is
out of service.

**Estimated:** the sketched network is about 1M conv operations a sample, so roughly 1,000 samples/s, ignoring the embedding and dense layers. Emulation at 132 steps/s a core
([NeSLE](https://github.com/hbofz/NeSLE)'s self-reported figure) over 8 cores is about 1,050 steps/s. Both unverified. At 3 PPO epochs:

| Steps | Gradients | Emulation | One run |
|---|---|---|---|
| 10M (the gate) | ~8 hours | ~3 hours | ~half a day |
| 100M (a late rung, if Sonic is a guide) | ~3.5 days | ~1 day | ~5 days |
| 300M | ~10 days | ~3 days | ~2 weeks |

Gradients and emulation share the CPU, so these are lower bounds. With D9, the gate's 5 seeds take about 1.5 days on `klip` and `stone` together, if `stone` keeps pace. **Budgets are in environment steps.** Stage 0 replaces these numbers with measured ones.

## Stages

Each stage gets its own plan and PRs, nothing stacked. Crate changes land in indrajala-math-rust first, then a Bump.

0. **The owner's answers,** and throughput measured on `klip` and `stone` with a current crate.
1. **Library primitives** (indrajala-ml): D7's three. Golden run unchanged, or re-recorded with approval.
2. **The environment** (indrajala-rl): `nes-py`, level starts, the reward, sticky actions, the tile decoder checked against rendered frames on all 32 levels, determinism tested,
   emulator steps/s measured.
3. **PPO and its control** (indrajala-rl): checked against a published reference implementation on a small task needing no ROM (MiniGrid, MIT, or similar). A silent PPO bug would look
   just like a hard level, so this comes first.
4. **THE GATE: 1-1.** Short probes, varied on the fly, then a batch of fresh seeds.
   - **Passes** when a clear majority of 5 fresh seeds each clear 1-1 in at least 90% of 100 attempts under sticky actions, within 10M steps.
   - Random-play and always-right controls beside it, each on the same score.
   - **If it fails,** report it to the owner with a diagnosis, whether that's the tile observation, the network or PPO. No further stage starts.

**Only after the gate, each planned then:**

5. **World 1.** The go/no-go on one network holding several levels, with 1-3 the known awkward one.
6. **World by world,** with D8's remedies as stalls call for them, until the stopping rule.
7. **The reading.** Fresh seeds at the final configuration. The result is a note: levels cleared per seed, by clear rate, what each remedy did, and a full playthrough, shown running on the Pi 4 (D9).

## What the result is

- **The number:** levels cleared in at least 90% of 100 sticky attempts, by the best network and across seeds, also at 50%. Every level's furthest distance beside it, and a run through the
  game from 1-1 as a stretch reading.
- **The stopping rule:** the ladder stops when a rung adds no level within its budget after the remedies that could explain the stall, or when a run passes 300M steps, which then goes back to the
  owner. Whatever is cleared by then is the answer.
- **Not claimed:** generalisation, or any statement about levels it hasn't trained on.

## Risks

- **Forgetting across levels,** the risk specific to one network. D6's retests measure it, and D8's first two remedies answer it.
- **Fixed configuration:** the 31 of 32 needed per-level tuning, which is unavailable here. This is why the count may stop well short.
- **The tile decoder** may omit something play depends on. Stage 2 checks that it matches the screen, but not that it's enough to play on; the gate tests that.
- **Long runs on a thin fleet:** `jebel` out, `stone` at 70%.
- **Unverified here:** the throughput figures, the RAM addresses, the castle mechanics.

## Open for the owner

- **O1. The ROM.** Stage 2 onward needs Super Mario Bros as a file you're entitled to use, supplied to the machines that run it. It goes in no repository or Zenodo record, and I won't fetch one, nor install a package that
  bundles it. Others could reproduce the work only with their own copy.
- **O2. The start.** This is a new direction beside machine discovery, and the certificate doesn't apply to it. The general algebras, arbitrary-length addition and factorisation plans stay paused unless you say otherwise. Stages 0-4 are about one to two weeks of
  building, plus days of machine time.
