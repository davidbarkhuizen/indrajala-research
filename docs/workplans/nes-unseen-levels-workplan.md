# Workplan: a network that plays unseen NES levels

**Status: drafted 2026-11-05 at the owner's direction, high level.** The owner: "we DO want an architecture
sufficient to play unseen levels - re-search on that basis, analyse, then write up a high level workplan for what we
would need to do to get there - using indrajala-ml - but creating additional new repos/functionality as required".
D1-D9 are settled under the owner's standing delegation, each option with its pros and cons. **O1-O3 are the owner's.**
Each stage gets its own detailed plan before code. Nothing here is built yet.

**The target.** A network trained on some levels of NES Super Mario Bros that clears levels it has never seen, zero-shot:
no training on the test level at all.

## The answer in brief

1. **The architecture is the smaller problem.** The literature's recipe is settled enough: a residual convolutional
   encoder, PPO over many levels at once, then level sampling and augmentation.
2. **The level supply is the larger one.** Procgen's authors found agents need "as many as 10,000 levels" to close the
   generalisation gap. Super Mario Bros has 32. Expect a gap, and plan to generate levels.
3. **Compute decides the observation.** Measured here, a pixel encoder would take weeks per run on our CPU-only machines.
   So we start from the console's tile map, which is roughly 18 times cheaper and ignores colour.
4. **The honest expectation is partial.** The closest published result, Sonic with held-out levels, reached 3,128 against a
   human's 7,438, on a benchmark of 58 levels. Clearing most unseen levels may need more levels or GPU time than we have.

## The IDs, in time order

| ID | When | Short label | What it is |
|---|---|---|---|
| D1 | 2026-11-05 | the encoder | a residual conv encoder (IMPALA-style, possibly average-pooled) |
| D2 | 2026-11-05 | the algorithm | PPO, joint over all training levels |
| D3 | 2026-11-05 | the observation | the PPU's tile map first, pixels only once the budget allows |
| D4 | 2026-11-05 | memory | stacked frames first; recurrence only if the castle levels need it |
| D5 | 2026-11-05 | the split | levels held out before any data, near-duplicates kept together, three test rungs |
| D6 | 2026-11-05 | level supply | sampling and augmentation first, then ROM-patched generated levels |
| D7 | 2026-11-05 | the repositories | indrajala-ml for primitives; new indrajala-rl and indrajala-nes; studies in indrajala-studies |
| D8 | 2026-11-05 | the emulator | the maintained nes-py environment first; a batched Rust emulator only if measured as the bottleneck |
| D9 | 2026-11-05 | existence first | one level, then joint training, each as short probes before any registered study |
| O1 | open | the ROMs | the owner supplies and is responsible for the ROMs; none goes in any repository or record |
| O2 | open | GPU | whether to lift the GPU exclusion for this work |
| O3 | open | the queue | where this sits against the paused research workplans |

## What the literature says

Read for this plan and persisted per the literature rule. Papers are cited by bib key in indrajala-literature.

- **The closest analogue is Sonic** (`nichol-2018-gotta-learn-fast-generalization-rl`): 58 levels with held-out test levels.
  - Joint PPO 3,127.9, joint Rainbow 2,969.2, Rainbow 2,748.6, PPO 1,488.8, human 7,438.2. These scores allow 1M steps of
    fine-tuning on each test level, so they are easier than our zero-shot target.
  - Rainbow beats PPO alone, but joint PPO beats joint Rainbow, and joint Rainbow took 32 GPUs.
  - Past about 50M joint steps, training gains stopped reaching the test set. Zero-shot scores barely rose after "the first
    few million". Best transfer was "not much better" than learning from scratch.
- **Level count** (`cobbe-2019-procgen-benchmark`): agents "strongly overfit to small training sets", and closing the gap
  needs up to 10,000 levels. 25M steps at 200 levels is the standard protocol, about 3 GPU-hours.
- **The encoder** (`cobbe-2018-quantifying-generalization-rl`, `espeholt-2018-impala`, `trumpp-2025-impoola-average-pooling`):
  IMPALA's residual encoder beat the Nature DQN encoder at test time on CoinRun; average pooling before the linear layers
  is reported to improve it further on Procgen. Neither is a Mario result.
- **Sampling and augmentation** (`jiang-2020-prioritized-level-replay`, `raileanu-2020-automatic-data-augmentation-rl`,
  `raileanu-2021-decoupling-value-policy-generalization`, `cobbe-2020-phasic-policy-gradient`): Prioritized Level Replay
  plus UCB-DrAC reports 76% better mean test return than uniform PPO on Procgen. Separating the value and policy networks
  (IDAAC, PPG) also helps.
- **Mario itself** (`burda-2018-large-scale-curiosity`, `pathak-2017-curiosity-self-supervised-prediction`): strong transfer
  from 1-1 to 1-2, weak from 1-1 to 1-3, which the authors put down to the shift from day to night colours. Those are
  fine-tuning results on curiosity alone. **I found no published train-and-hold-out result on NES Mario.**
- **On a desktop** (`clark-2024-beyond-the-rainbow`, `hafner-2023-dreamerv3-world-models`): Beyond The Rainbow trains 200M Atari
  frames in 12 hours on an RTX 4090 and i9-14900K. DreamerV3 ran across 150+ tasks with one configuration. Both assume a GPU.

Read as search summaries or abstracts only, so check before relying on them: the student comparison
([CS224R](https://cs224r.stanford.edu/projects/pdfs/CS224R_Project-1.pdf), PPO clearing 1-1 in 96.32% of attempts) and
[NeSLE](https://github.com/hbofz/NeSLE)'s README (132 steps/s for nes-py on one core, self-reported).

## What we have, and what's missing

**indrajala-ml has:** `Conv`, max `Pool`, `Dense`, Adam with clipping and schedules, batch and layer norm, dense `Residual`,
forks and branches, persistence, and bit-identical training on three implementations.

| Gap | Why it matters | Where |
|---|---|---|
| `Conv` has no padding | a deep stack shrinks the image to nothing (the probe's failure) | indrajala-ml |
| `Residual` bodies can't hold conv or pool | IMPALA's blocks are conv residuals | indrajala-ml |
| No average pooling | Impoola's encoder | indrajala-ml |
| Learning takes a class label per sample | PPO needs an arbitrary loss on two heads | indrajala-ml |
| Large activations per batch | batch 256 ran out of memory under klip's 4.5 GB limit | indrajala-ml |
| No RL at all: environments, rollouts, PPO | the whole training loop | indrajala-rl (new) |
| No NES environment or tile observation | the task | indrajala-nes (new) |

## The budget (feasibility)

**Measured** on `klip` (2026-11-05, 8 threads, 84×84×4 input, Adam, one probe, the crate as installed there and predating
later work, conversion from Python lists included, so a rough floor rather than a benchmark): 74 samples/s at batch 32 and 56
at batch 256 with 3 conv layers, 56 at batch 32 with 7; about 1 billion conv operations (GMAC) a second. `stone` wasn't
measured, and `jebel` is out of service.

**Estimated** from that, at 1 GMAC/s, for 25M PPO steps at 3 epochs (75M samples through the backward pass):

| Observation | Conv MACs a sample | Samples/s | One run, gradients only |
|---|---|---|---|
| Pixels, padded IMPALA ×1, 84×84 | 53M | ~19 | ~46 days |
| Pixels, padded IMPALA ×1, 64×64 | 31M | ~33 | ~26 days |
| Tile map, 16×15 cells, 32 embedded channels (a sketch) | ~3M | ~330 | ~2.6 days |

Emulation adds about 6.6 hours per 25M steps at 8 cores, if the 132 steps/s holds and scales, which nobody here has measured.
A study of 5 seeds per arm over a few arms is weeks of machine time even on the tile map. Faster kernels help everything, but
speedup claims wait for `jebel` (the parked plan's D12).

**Every budget is in environment steps,** not wall-clock.

## Decisions

- **D1. The encoder.**
  - (a) *Chosen.* IMPALA-style residual conv, ×1, with average pooling compared at stage 4. Pros: the best evidence on unseen
    levels, and small enough for a CPU. Cons: needs conv residuals and padding.
  - (b) Nature DQN CNN. Pros: nearly buildable today. Cons: lost to IMPALA at test time. Kept as the control.
  - (c) Transformer or world model. Pros: strong general results. Cons: a much larger budget, and no evidence it helps on
    unseen levels. Reconsider if O2 changes.
- **D2. The algorithm.**
  - (a) *Chosen.* Joint PPO. Pros: Sonic's best baseline; on-policy, so no replay memory on small machines; simple. Cons: needs
    many samples.
  - (b) Rainbow family. Pros: fewer samples on one level. Cons: joint Rainbow lost to joint PPO on Sonic, despite 32 GPUs; replay
    needs memory that `klip` lacks.
  - (c) Curiosity on its own. Pros: no reward design. Cons: answers a different question. Added only if an extrinsic-reward agent stalls.
- **D3. The observation.**
  - (a) *Chosen.* The PPU's nametable and sprites as an embedded tile grid, no palette. Pros: ~18× cheaper; **ignores colour,
    the reported cause of the weak transfer to 1-3**; generic to NES games, needing no per-game RAM map. Cons: not "from pixels";
    scroll and sprite decoding must be built; tile IDs may not carry across games.
  - (b) Pixels. Pros: the standard, and general. Cons: weeks per run here. Stage 7 returns to it if the budget allows.
  - (c) Mario's RAM map. Pros: simplest. Cons: one game only, and it hands over structure the network should find.
- **D4. Memory.**
  - (a) *Chosen.* Stacked frames first, which give speed and direction. Pros: simple and cheap. Cons: the castle levels that loop
    until the right path is taken (4-4, 7-4, 8-4, from general knowledge) may need memory. Add a recurrent cell if they do.
  - (b) Recurrent from the start. Pros: covers those levels. Cons: cost and complexity before any evidence of need.
- **D5. The split.** Fixed before any data, by a written rule.
  - **Near-duplicates stay together.** Some stages are reused with changes (from general knowledge, such as 2-2 and 7-2, or 1-3 and
    5-3), and one on each side would leak. Stage 2 finds them by decoding the level data.
  - **Rung 1:** about 8 of the 32 held out, stratified by kind (overworld, underground, underwater, castle), with every kind still
    in training. **Rung 2:** Lost Levels, harder levels on the same engine. **Rung 3:** SMB3, which has different mechanics, as a
    stretch. The maintained environment covers all three.
  - **The score** is zero-shot: completion rate and furthest distance over fresh attempts with sticky actions, as the NES is
    deterministic. Random-play and always-right controls beside it.
- **D6. Level supply.** In order, each only if the last falls short.
  - (a) *Chosen first.* Sampling and augmentation: start from varied mid-level save states, Prioritized Level Replay, and tile-level
    augmentation (mirroring is out: the game scrolls one way). Pros: no new levels needed; established. Cons: 24 levels remain 24.
  - (b) *Chosen second.* Generated levels patched into the owner's ROM, with playability checked by an A\*-style agent. Pros: the
    only route towards the thousands the literature calls for, and the real engine. Cons: the largest piece of new work; engine
    format limits; generated levels may not resemble hand-designed ones; rests on O1.
  - (c) A new platformer of our own design for pre-training. Pros: unlimited fast levels, no ROM needed. Cons: a simulation gap.
    **It must be an original design, never a recreation of Mario.** Not planned.
- **D7. The repositories.**
  - (a) *Chosen.*
    - **indrajala-ml:** the primitives in the gap table, in all implementations and the crate.
    - **indrajala-rl (new):** game-free environment protocol, rollouts, PPO, level sampling, augmentation.
    - **indrajala-nes (new):** the emulator binding, tile observation, save states and level patching. No ROMs.
    - **indrajala-studies:** runs, under the experiment design. **indrajala-research:** this plan and any notes.

    Pros: reusable pieces, and ml stays a library. Cons: more repositories to pin.
  - (b) All in indrajala-ml. Pros: one repository. Cons: ROM-adjacent code and game adapters in the public library, reversing the
    research split.
- **D8. The emulator.**
  - (a) *Chosen.* `gym-super-mario-bros` 9.1 with `nes-py`. Pros: maintained; Python 3.14; covers all three rungs. Cons: per-step Python;
    single-process per environment; no generated levels without our patching.
  - (b) A batched Rust emulator in indrajala-nes. Pros: in-process and fast, in keeping with the crate. Cons: a NES emulator is a project
    of its own. Only if stage 2 measures emulation as the bottleneck.
  - (c) NeSLE. Pros: 13M frames/s reported. Cons: GPU only; depends on O2.
- **D9. Existence first.** The programme's rule: one working network before any matrix, using short probes varied on the fly, then a
  registered study only for claims. No registered study starts before a network clears 1-1 and a joint network clears training levels.

## Stages

Each stage is its own plan and PRs, nothing stacked. Crate changes land in indrajala-math-rust first, then a Bump.

0. **The owner's three answers,** and a proper throughput measure on `klip` and `stone` with a current crate.
1. **Library primitives** (indrajala-ml): conv padding, conv residual blocks, average pooling, a learning entry taking an output gradient,
   two output heads, and batch memory that fits 4.5 GB. Golden run unchanged, or re-recorded with approval.
2. **The NES environment** (indrajala-nes): the binding, tile observation checked against rendered frames, save states, sticky actions,
   determinism tested. Measures emulator steps/s, level duplicates, and D5's split, published before any training.
3. **RL core and its control** (indrajala-rl): the environment protocol, vector rollouts, PPO. **Controlled against a published reference
   implementation on a small task** before any trust in Mario numbers, as a silent PPO bug looks just like a hard task.
4. **Existence ladder** (probes): clear 1-1; then 1-1 to 1-4; then joint over all training levels. Encoder and pooling compared here.
   **Exit: a joint network clearing most training levels.**
5. **First unseen-level result** (registered): joint PPO on rung 1 against the controls. This is the plan's first real answer, and it may
   well show a large gap.
6. **Closing the gap** (registered per remedy): sampling, save-state starts, augmentation, value-policy separation, then memory for the
   castles. Each adopted on fresh seeds, never by rescuing chosen ones.
7. **More levels, if still short** (indrajala-nes): the ROM level format, generator, playability check, then rung 1 again with N generated
   levels. Rungs 2 and 3, and pixels, follow if the budget allows.

## What done means

Set finally at stage 5's registration, from stage 4's readings. Draft:

- **Reached:** a clear majority of seeds clear a clear majority of rung 1's held-out levels zero-shot at least half the time.
- **Partial, and still worth writing up:** a measured curve of held-out performance against the number of training levels, the Procgen
  question on a real game, which we didn't find published for NES Mario.
- **Stop and return to the owner:** if stage 5's result sits near the controls after the budget, or stage 6's remedies each fail. Options
  then are O2 or stage 7, not more of the same.

## Risks

- **Too few levels** is the main risk, and D6 only partly answers it.
- **Run length.** Weeks of machine time on a fleet that's short a machine, and `stone` at 70%.
- **Silent RL bugs.** Stage 3's control is the guard.
- **Tile observation may not hold up.** Levels may rely on sprite or scroll details the grid loses. Stage 2 checks it, and pixels stay possible.
- **Unverified here:** the 132 steps/s; this plan's tile-grid sizes; stage reuse and castle mechanics, stated from general knowledge.

## Open for the owner

- **O1. The ROMs.** The environment needs Super Mario Bros, and later Lost Levels and SMB3, as ROM files. Whatever the package ships, **I won't
  fetch or commit any.** You'd need to supply copies you're entitled to use, kept out of every repository and Zenodo record. Generated levels
  would be published as data or patches only, never as patched ROMs. This also makes the results harder for others to reproduce.
- **O2. GPU.** All backends are CPU today, by your earlier exclusion.
  - **Stay on CPU** (my recommendation until stage 5). Pros: no new hardware or backend, and the tile map keeps runs feasible. Cons: weeks a study; pixels
    stay out of reach; the 10,000-level question stays out of reach.
  - **Add a GPU.** Pros: Procgen's 25M steps takes about 3 GPU-hours against our days; opens pixels, world models and NeSLE. Cons: hardware or cloud cost, and a
    new backend outside the three bit-identical implementations.
- **O3. The queue.** This is a new direction beside machine discovery, and the certificate wouldn't apply to it as it stands. The general algebras,
  arbitrary-length addition and factorisation plans stay paused unless you say otherwise. I recommend stages 1-4 as a time-boxed existence check, deciding
  on the rest from that.

## The size, roughly

| part | time |
|---|---|
| stages 0-3 (primitives, environment, RL core) | one to two weeks of building |
| stage 4 (existence) | days of machine time |
| stage 5 (first unseen result) | one to two weeks of machine time |
| stage 6 (remedies) | weeks |
| stage 7 (generated levels) | weeks of building, then weeks of runs |

These are rough, and rest on the estimated budget above.
