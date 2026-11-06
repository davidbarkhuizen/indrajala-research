# Workplan: how far can one network take Super Mario Bros?

**Status: detailed 2026-11-05 through the gate (stages 0-4), with a PR-by-PR execution plan; later stages stay brief until it's passed. Stages 0 and 1 done 2026-11-05; stage 2 done 2026-11-06 (2.3, the vector runner, with D15), and stage 3's 3.1, 3.2 and 3.3: **the control passed** with split networks (D17) on CartPole and DoorKey; **D18: split on 1-1 too** (C3 passed, 2.23 × shared's score), so SMB's network is split (Findings).** The owner: "lets write it up - gated on
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
| D13 | 2026-11-05 | the input path | tile ids to the crate, one-hot planes built in Rust by a generic op; a buffer path for float channels |
| D14 | 2026-11-05 | the input embedding | one-hot planes for every tile value and kind, then a learned `Conv(1, 16)`, in place of D1's grouping |
| D15 | 2026-11-06 | the lockstep runner | the vector runner steps in lockstep, deterministic; overlap and uneven cores are stage 3's to measure |
| D16 | 2026-11-06 | the control's registration | CartPole, then MiniGrid DoorKey-5x5, against CleanRL's PPO at its settings; ours within 90% of its score, on 5 seeds |
| D17 | 2026-11-06 | the control again, split | T1's refutation diagnosed (the shared trunk); the control re-registered with separate policy and value networks for ours, on fresh seeds |
| D18 | 2026-11-06 | shared or split, measured on 1-1 | D2's shared trunk against split policy and value networks, 1M decisions, 5 seeds an arm; the network chosen by the registered rule |
| O1 | 2026-11-05 | the start | the owner's go: stages 0-3 start now, ahead of the paused plans |
| O2 | 2026-11-06 | the Rust go | the owner's go for stage E now, ahead of D10's reading; planned in `nes-rust-emulator-workplan.md` |

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
    - **Tiles:** one-hot over the values seen, grouped only if the census exceeds about 32. Stage 2's census of all 32 levels fixes this. **Changed by D14:** never grouped; every value and kind gets its own plane, and the network learns the embedding.
    - **Sprites, for each of the last 4 decisions:** presence, plus **offset within its cell in x and y as values in those channels.** A 16-pixel grid alone would lose the precision that jumps need.
    - **Enemy kind:** sprite attributes are kept, as red and green Koopas are drawn alike and behave differently.
    - **Mario's size** as a constant plane.
    - **Why tiles aren't stacked:** they rarely change, and stacking would multiply the channels.
- **D2. The network.**
  - (a) *Chosen.* `Conv(3,16), Pool(2), Conv(3,32), Dense(256,"relu")`, then one linear output layer of `actions + 1` columns, the last being the value. Pros: runs on today's layers, with no conv padding or second head. Cons: capacity may run short, D8's first remedy.
  - (b) IMPALA-style residual. Pros: more capacity. Cons: needs padding and conv residuals. Only if (a) stalls for capacity.
  - **Changed by D14:** a `Conv(1, 16)` goes first, so the network is `Conv(1,16), Conv(3,16), Pool(2), Conv(3,32), Dense(256,"relu")`, then the output layer.
  - **Changed by D18 (C3 passed, 2026-11-06):** split, two networks of that body, one ending in the logits and one in the value (`SplitNetwork`); 2.23 × shared's score on 1-1 at 1M decisions (Findings).
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
  - **Overtaken by the owner's go (O2, 2026-11-06):** "start building the nes emulator in rust according to the plan while we wait". Stage E starts now, planned in `nes-rust-emulator-workplan.md`. D10's reading at 3.4 is still made, from D18's timings, as the measure the emulator is judged against.
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

- **D13. The input path** (the owner agreed, 2026-11-05, after stage 0's finding). The crate's `Array` is built from Python by extracting each element as a Python float (`src/array.rs`), about 90 ns an element; D1's one-hot input is 6,656 doubles a sample, so it costs as much as the network's forward pass.
  - (a) `Array.from_buffer(ndarray)`, a memcpy. Pros: small, general. Cons: still 53 KB a sample of mostly zeros, built in numpy.
  - (b) *Chosen, with (a) under it for the float channels.* The game layer hands the crate tile ids (208 bytes a sample) and the few sprite values; a **generic** crate op writes the one-hot planes straight into the input `Array`. Pros: about 250× less data crosses; no one-hot outside Rust; the op knows no game, so D12's seam holds; it leads into stage E's observation in place. Cons: one more op, with its implementations and parity tests.
  - (c) The whole decode in Rust, from RAM. Cons: SMB's RAM layout in the math crate, against D12. Stage E's, if D10 fires.
  - **Later, not planned:** an embedding over tile ids in place of the first conv over one-hot planes, which is a lookup in disguise. It changes D2's network, so only if capacity or speed calls for it.

- **D14. The input embedding** (2026-11-05, stage 2.2; the owner delegates D choices). The census so far has 53 tile values and 39 object kinds (with the player's statuses), so one plane each, with the value planes, is about 140 channels, well over D1's grouping threshold of about 32.
  - **Measured** on `stone` (8 threads, ml `61db273`, crate `f73d652`), `probe_throughput.py --embed E`, D2's network on (13, 16, channels), batch 256, median of 5. A step at 3 epochs, in ms a decision, takes forward once and learning three times, plus stage 0's emulation (0.81 ms):

    | Input | Forward, learning (samples/s) | Network, ms a decision | Step, ms a decision | Against 32 grouped |
    |---|---|---|---|---|
    | 32 channels (grouped) | 11,817, 7,562 | 0.48 | 1.29 | 1.00 |
    | 140 planes, no embedding | 3,143, 2,041 | 1.79 | 2.60 | 2.01 |
    | 140 planes, `Conv(1, 8)` first | 10,661, 4,354 | 0.78 | 1.59 | 1.23 |
    | 140 planes, `Conv(1, 16)` first | 8,996, 3,687 | 0.92 | 1.74 | 1.34 |
    | 140 planes, `Conv(1, 32)` first | 5,996, 2,594 | 1.32 | 2.14 | 1.66 |

    The 32-channel row repeated within 4%. Readings: indrajala-studies' gitignored `data/nes-probe/d14/`, in its manifest. (The 32-channel row against stage 0's, 11,817 against 5,577 forward, includes D11's threads; provisional, no speedup claimed, as `jebel` is out.)
  - (a) *Chosen.* **One plane for every value and kind, then a learned `Conv(1, 16)`.** Pros: no grouping by hand, so nothing about the game is chosen for the network (D12's seam, and learning the method rather than being told it); every distinction reaches the network, including the ones D1 itself raised (red and green Koopas); the width is one number, which D8's larger-network remedy can raise. Cons: a step costs 1.34× grouping's, on this measure; a 1×1 conv over mostly zero planes is a lookup done the dense way.
  - (b) Group to about 32 channels, as D1 planned. Pros: the fastest (1.00). Cons: the groups are chosen by hand from knowledge of the game; a wrong merge (two kinds that behave differently) fails silently.
  - (c) The planes straight into `Conv(3, 16)`. Pros: no extra layer. Cons: twice grouping's step (2.01).
  - (d) A true embedding layer, a gather by id (D13's "later, not planned"). Pros: the cheapest of the learned options. Cons: a new layer in the crate with its three implementations, before anything shows the network is the bottleneck. Revisit at stage 3.4's D10 reading if the network dominates a step.
  - **The width:** 8 costs 1.23×, 16 1.34×, 32 1.66×. 16 is chosen: about 100 one-hot classes into 8 dimensions risks merging what matters, and 32 costs half again for capacity the gate may not need. 140 is the probe's estimate; the census fixes the count, which changes only the first layer's cost.
- **D15. The lockstep runner** (2026-11-06, at stage 2.3; Findings). The runner steps every environment together, so a step waits for its slowest worker. On `klip` (4 like cores) that costs 4.5% against bare emulation; on `stone`, whose i7-1255U has 2 performance and 8 efficiency cores, 10.5% at 8 workers, just outside 2.3's 10%, and 18% at 4. The loss is lockstep's: free-running environments come within 2.4% of bare emulation on both.
  - (a) *Chosen.* **Keep the lockstep runner as it is; measure the loss in the whole loop at 3.4 and remedy it there if it matters.** Pros: determinism by construction (each environment's bits are a serial run's, tested); the PPO loop's own wait, emulators idle while the network decides, is the same kind of loss and has the same remedy, two runners of half the workers each, alternated so one emulates while the network runs on the other, which needs no change here; `klip` meets the exit. Cons: `stone` gives up about 10% of emulation until then; the remedy is unmeasured.
  - (b) Uneven shares, more environments on workers pinned to the fast cores. Pros: recovers part of `stone`'s loss now. Cons: tied to one machine's cores and the scheduler's placement; a change of load breaks it; still lockstep.
  - (c) Asynchronous batching: decide for whichever environments are ready. Pros: no wait for the slowest. Cons: a decision's batch then depends on timing, so its bits do unless the network's rows are independent of their batch, which nothing here tests; more machinery before PPO exists.
- **D16. The control's registration** (2026-11-06, before any data; stage 3.3). The control asks one thing: does our PPO train as well as a published one on tasks with no ROM, so a silent bug in ours can't pass for a hard level?
  - **The reference:** CleanRL's single-file `ppo.py` (MIT), fetched at a pinned commit into a scratch venv on `klip` with PyTorch (CPU) and never committed: `cleanrl/ppo.py` at `e421c2e` (2023-11-28), SHA-256 `d8dfbb7a…e459ae`. **Its changes, applied by script and recorded, none to the algorithm:** `Tanh` to `ReLU` in its two networks, as indrajala-ml has no tanh and our network is ReLU (D2); on MiniGrid, its environment wrapped so its input is our codec's one-hot vector, the same bits ours sees; **and a port to gymnasium 1.2.2**, as it was written for 0.29, whose vector environments reset an ended episode in the same step, where 1.x's reset on the next one (that step's action ignored) and report episodes in a vectorised info: its vector environment made with `autoreset_mode=SAME_STEP`, its episode printing read from 1.x's info. (0.29 itself doesn't run on NumPy 2, the only NumPy with Python 3.14 wheels.) Its GAE treats a truncation as an end, where ours bootstraps it (3.1): a difference of method, kept.
  - **The tasks** (gymnasium 1.2.2, minigrid 3.2.0, both MIT): **T1, CartPole-v1, 500,000 steps** (CleanRL's default budget); **T2, MiniGrid-DoorKey-5x5-v0, 1,000,000 steps**, the agent's 7×7 view as three id grids (object, colour, state: 11, 6 and 3 ids), so the one-hot path ours uses on SMB is in the control. T2 runs only after T1 passes.
  - **The settings, both sides:** CleanRL's defaults (4 environments, 128 steps a rollout, 4 epochs, 4 minibatches, learning rate 2.5e-4, γ .99, λ .95, clip .2, value clip .2, entropy .01, value .5, gradient norm .5, advantages normalised, Adam ε 1e-5), with its learning-rate annealing off, as ours is constant (D3). **The networks:** the reference's own, two MLPs of 64 and 64 (actor and critic), its orthogonal init; ours D2's form, one trunk of `Dense(64, "relu")` twice, then the linear output of logits and the value, its fan-in init. These differences are kept: the control tests the method as we use it.
  - **The score,** per run: the mean return of the episodes ending in the last 10% of its steps.
  - **Seeds:** 0 to 4 on each side, fixed now.
  - **Claim C1 (per task): ours trains as well as the reference.** **PASSES** when ours' mean score over its 5 seeds is at least 90% of the reference's. **Void** when the reference's own mean misses its bar (T1 400 of CartPole's 500; T2 0.8, a solve in about a fifth of the episode limit): then the reference couldn't do the task at these settings, and that's diagnosed, not scored. **Refuted** when ours is below 90%; then a diagnosis to the owner, as the plan says, before stage 4 (the difference in network structure is the first suspect, then a bug).
  - **Reported beside it,** exploratory (5 seeds a side is a screen, the experiment design's §3): Mann-Whitney, two-sided, on the 5 scores against 5.
  - **Probes first, claiming nothing:** one seed of each side on T1 to check that both run and learn, and of the reference on T2 to check its budget is feasible. If the reference can't reach T2's bar on its probe, T2's budget is raised once, before registration's runs start, and recorded here.
  - **Where:** `klip`, under the thermal guard. Ours with the Rust backend.
- **D17. The control again, with split networks** (2026-11-06, after T1's refutation and its diagnosis, before these runs; Findings, 3.3's diagnosis). The diagnosis found no bug: our update equals PyTorch's with CleanRL's loss to about 1e-11 on both backends, and our GAE equals CleanRL's. It found the cause: our shared trunk, which slows CleanRL itself to half its pace. Split networks bring ours to the reference's pace. **The one change from D16: ours trains a policy network and a value network** (`SplitNetwork`: each two `Dense(64, "relu")`, then its own linear output; each clips its own gradient norm at 0.5, as ml clips per network, where CleanRL clips the two jointly). Everything else is D16's: the reference and its edits, the tasks and budgets, the settings, the score, the bars, the rule.
  - **Seeds: 10 to 14 on each side,** fresh. T1's seeds and the diagnosis's probe seeds (100-102) aren't reused.
  - **Claim C2 (per task): ours, split, trains as well as the reference.** **PASSES** at 90% or more of the reference's mean score over 5 seeds; **void** if the reference misses its bar (T1' 400, T2' 0.8); **refuted** below 90%, then a diagnosis before stage 4. Mann-Whitney, two-sided, exploratory, beside it.
  - **T1' (CartPole) first; T2' (DoorKey-5x5, 1M steps) only if T1' passes.** On `klip`, one thread a run, Rust.
  - **For SMB, not decided here:** D2's network shares its trunk. Whether it splits too is a question once the control passes, with its cost (two networks' learning, about half again on a step), to the owner then.
- **D18. Shared or split, measured on 1-1** (2026-11-06, before any run; the owner: "surely we need to test both and make the decision on a quantitative basis"). The control found a shared trunk halves PPO's pace on CartPole (3.3's diagnosis). That was a 4-input MLP; SMB's trunk is convolutional over 125 planes, where sharing is the usual practice. So it's measured on SMB itself, short, before the gate.
  - **The arms:** **shared**, D2's network as it is (D14's `Conv(1, 16)`, `Conv(3, 16)`, `Pool(2)`, `Conv(3, 32)`, `Dense(256, "relu")`, then logits and value); **split**, two networks of that body, one with the logits and one with the value (`SplitNetwork`, each clipping its own gradient norm at 0.5).
  - **Everything else fixed:** 1-1; D3's settings (256 steps a rollout, 3 epochs, 8 minibatches, learning rate 5e-4, γ .99, λ .95, clip .2, value clip .2, entropy .01, value .5, gradient norm .5); 8 workers × 4 environments; sticky actions .25; a decision limit of 4,000; the Rust backend; `scripts/train.py`.
  - **The budget:** 122 iterations a run, 999,424 decisions, compared at equal decisions (epochs, not wall-clock).
  - **Seeds:** 30 to 34 for each arm, fresh. **Machines:** `stone` runs seeds 30-32 of both arms and `klip` 33-34 of both, arms alternating on each, so neither arm has a machine to itself (the crate's bits don't depend on the machine; each run's host is in its config).
  - **The score,** per run: the mean reward of the episodes ending in the last 10% of its decisions (the control's). Reported beside it: the mean reward in each tenth of the run, clears, and the seconds an iteration takes, rollout and update apart, for 3.4.
  - **Claim C3: split learns faster on 1-1 at this budget.** **PASSES** when split's mean score over its 5 seeds is at least 1.1 × shared's **and** a one-sided Mann-Whitney test (the direction registered: split higher, as the control's evidence predicts) gives p ≤ 0.05 on the 5 scores against 5. **Then SMB's network is split** (D2 amended). Otherwise **shared stays:** cheaper by about half a step's learning, and the usual practice for a conv trunk. **Void** if neither arm learns (both arms' last tenth no better than their first): then that's diagnosed first (existence, the experiment design's §2).
  - **The cost per arm** is recorded, not part of the rule: a split network costs more a step, and the rule compares at equal decisions; if split passes, its wall-clock price goes to the owner beside it.

## Stages to the gate

Each is its own PRs, nothing stacked. Crate changes land in indrajala-math-rust first, then a Bump in indrajala-ml, then in indrajala-studies.

### Stage 0: tools and the fuller measure

- **indrajala-rl created,** private until there's something to release: `pyproject`, CI (ruff, pyright, pytest), a `.gitignore` for `*.nes`, and a CI check that fails on any `*.nes` in the tree. CI has no ROM, so ROM-backed tests skip there and run on the machines.
- **The ROM:** `~/roms/super-mario-bros.nes` on `pyramidon`, copied to runners into a private `~/roms`. Tools check its SHA-1 (`ab30029efec6ccfc5d65dfda7fbc6e6489a80805`) and refuse anything else.
- **The probe as a tool:** `scripts/probe_throughput.py`, reporting emulation, forward and learning times, on `klip` and `stone`.
- **Exit:** both machines measured with a current crate.

### Stage 1: library (indrajala-ml, indrajala-math-rust)

1. **Thread conv's forward pass** (D11): the crate, tests of bits at 1 to 8 threads, the Bump, golden run.
2. **A learning entry from an output gradient:** `learn_batch_output_gradient(learning_rate, X, gradient, clip_norm)`, where `gradient(Y)` maps the step's own forward outputs to the loss's gradient at them, `(batch, outputs)`, on the array networks, numpy and Rust. **Built as a function, not the `G` first planned** (2026-11-05): one forward pass then serves both the loss and the step, as PPO's loss depends on the outputs of the very pass it trains. The output layer is `Dense(n, "linear", output=True, loss="given")`.
   - **Tests:** with `G` set to cross-entropy's gradient, bit-identical to `learn_batch`; a finite-difference check on a small network; a run on numpy against Rust.
   - **Not added to pure Python:** it's a training entry for array networks, not a layer. Pros: less to build. Cons: a small break from the three-implementations habit, recorded here.
3. **The input path (D13):** a generic crate op building one-hot planes from tile ids, and `Array.from_buffer` for float channels, in place of the crate's element-by-element constructor. **Needed, by stage 0's measure:** that conversion costs as much as a forward pass, and after D11 about 30% of a step on `klip` (Findings).

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

## Stage E: the Rust emulator (the owner's go, O2)

**Planned in detail in `nes-rust-emulator-workplan.md` (2026-11-06), which replaces the sketch below and the analysis's E1-E8 table.** The sketch is kept as the reasoning before that plan.

**The detailed analysis** (2026-11-06): `docs/research-notes/nes-rust-emulator-analysis.md`: about 13-18 days at the plan's rate, about 1.8× on a PPO iteration at D10's first reading, with gains D10 doesn't measure. **How much work, first sketch.** About **1-2 weeks** for a headless emulator that runs only Super Mario Bros, in a new repository, `indrajala-nes`. A general emulator, with audio and many mappers, is months and isn't proposed. The first game is mapper 0, the simplest case. My estimate, and the debugging is its most uncertain part:

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
| [`nes-py`](https://github.com/Kautenja/nes-py) | MIT declared; core derived from **GPL-3.0** SimpleNES, provenance unresolved (its LICENSING.md, found 2026-11-06) | **the parity oracle only, run as a black box; its C++ not read** |
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

Stage 2.2's level table went to the owner on 2026-11-06 (Findings). Nothing else is open for the owner.

## Findings

Stage 0's scratch probe, above. Findings from each stage go here.

### D18: shared or split on 1-1 (2026-11-06) — C3 passes: SMB's network is split

As registered in D18 (#164): `scripts/train.py` on 1-1, D3's settings, 8 workers × 4 environments, 122 iterations (999,424 decisions) a run; `stone` seeds 30-32 and `klip` 33-34 of each arm. All 10 runs ended cleanly. **Run on the old ROM dump** (O3): the result stands as made, a structural reading (shared or split); runs the plan needs on the canonical dump are redone there.

| seed | 30 | 31 | 32 | 33 | 34 | mean |
|---|---|---|---|---|---|---|
| shared | 47.0 | 47.2 | 45.9 | 47.8 | 56.7 | **48.9** |
| **split** | 92.0 | 110.7 | 115.3 | 106.7 | 120.0 | **108.9** |

- **C3 passes:** split's mean score is **2.23 ×** shared's (the bar 1.1 ×), and every split score is above every shared score: **U = 25 of 25, exact one-sided p = 1/252 = 0.004**, the smallest 5 against 5 can give (the bar 0.05). **SMB's network is split** (D2 amended). Not void: both arms learn (their first tenths 39.2 and 39.1).
- **The curves** (the mean reward in each tenth, the arm's mean over seeds): shared 39.2, 41.1, 40.9, 42.4, 43.1, 43.7, 44.6, 46.1, 46.4, 48.9; split 39.1, 41.1, 43.3, 49.2, 63.0, 76.6, 88.8, 95.7, 100.7, 108.9. They part at the fourth tenth (about 400k decisions), and split is still climbing at the end.
- **Clears of 1-1** (episodes reaching the flag, the whole run): shared 7, 11, 11, 4, 12; split 82, 122, 157, 203, 255. In the last tenth: shared 0-5 a run, split 25-78. That isn't the gate (stage 4's rule), but 1-1 is cleared by every split run inside 1M decisions.
- **The cost per arm** (the median seconds an iteration, rollout + update): `klip` shared 18.4 + 17.7, split 20.1 + 32.0 (split 1.45 × a step); `stone` shared 8.7 + 7.1 for seed 30, then 15.3-15.6 + 10.8-10.9, split 12.0 + 16.0 for seed 30, then 17.1 + 22.5. `stone`'s later runs were slower in both arms alike (its load varied; the arms alternated, so neither gained). At equal decisions split costs about half again in wall-clock, and reaches in 500k decisions the score shared has at 1M.
- Readings: indrajala-studies' gitignored `data/nes-d18/` (`stone/`, `klip/`: config, log and last checkpoint of each run, the scripts and statuses), in its `MANIFEST.sha256`.

### Stage 3.3: the control again, split (2026-11-06) — C2 passes on both tasks

As registered in D17 (#163): ours with split policy and value networks; seeds 10-14 a side; `klip`, one thread a run.

| task | ours, split (5 seeds) | reference (5 seeds) | ours / reference | Mann-Whitney (exploratory) |
|---|---|---|---|---|
| **T1', CartPole-v1** | 500.0, 425.8, 487.8, 468.2, 486.3: **473.6** | 390.3, 500.0, 494.0, 486.5, 500.0: **474.2** | **99.9%** | U = 9, p = 0.54 |
| **T2', DoorKey-5x5** | 0.965, 0.960, 0.960, 0.950, 0.960: **0.959** | 0.960, 0.960, 0.964, 0.960, 0.960: **0.961** | **99.8%** | U = 14, p = 0.84 |

- **C2 passes on both tasks** (the bar 90%; each reference met its bar, 400 and 0.8). **The control is passed: stage 3.3 is done.**
- **The curves agree too.** On CartPole ours is ahead in the first tenth (about 100 against 73) and both are near 470-490 by the fourth. On DoorKey both solve it within the first tenth of 1M steps, every seed of both.
- **What T2' can and can't show:** DoorKey-5x5 is easy for both at this budget, every run at its ceiling of about 0.96, so it confirms the one-hot id path and a sparse reward work end to end but doesn't separate the sides finely. CartPole did that, and is where T1 failed.
- **What this says about PPO here:** the implementation was right before the change (3.3's diagnosis: its update equals PyTorch's to 1e-11); the structure, one trunk for policy and value, was the cost. Whether SMB's conv network splits too is D18's to measure.
- Readings: indrajala-studies' gitignored `data/nes-control/t1b/` and `t2b/`, in its manifest.

### Stage 3.3: the diagnosis (2026-11-06) — the shared trunk

indrajala-rl#13. Probes, claiming nothing; seeds 100-102.

- **No bug in the update:** `scripts/probe_ppo_parity.py` takes our update steps and PyTorch's (float64, CleanRL's loss as it writes it) on the same network and minibatches of a real CartPole rollout. **They agree to about 1e-11** under SGD and Adam, on numpy and on Rust; every layer's change has ratio 1.0000, cosine 1.0000 and no sign flipped. (A first Adam comparison disagreed because the probe carried our Adam's state into a fresh PyTorch Adam.) Our GAE equals CleanRL's formula exactly on six real rollouts. The ddof of the advantages' deviation changes nothing that matters (1e-6).
- **The cause, the shared trunk.** Mean curves (the mean return in each tenth of a run):

  | configuration | runs | mean score | first four tenths |
  |---|---|---|---|
  | reference, separate actor and critic | 8 | 485 | 71, 229, 289, 423 |
  | reference with our shared trunk (R1) | 3 | 493 | 34, 122, 170, 221 |
  | ours, shared, CleanRL's init (O1) | 3 | 350 | 35, 126, 155, 145 |
  | ours, shared, fan-in (as T1) | 8 | 419 | 33, 120, 118, 119 |
  | **ours, split policy and value (S1)** | 3 | **486** | **103, 270, 416, 468** |

  The shared trunk halves the reference's pace; init isn't the remedy; split networks bring ours to the reference's pace or better. Ours shared still trails R1 at 3 seeds; with the pipelines shown identical, that's read as seed variance, not a cause. **D17 re-registers the control with split networks.**
- Readings: indrajala-studies' gitignored `data/nes-control/diag/`, in its manifest.

### Stage 3.3: the control, T1 (2026-11-06) — C1 refuted on CartPole

indrajala-rl#12, as registered in D16 (#161). On `klip`, one thread a run, five at a time under the guard (peak 59 C).

- **Probes first** (seed 100, claiming nothing): the reference scores 500 on CartPole and 0.964 on DoorKey-5x5, solving DoorKey within the first tenth of its 1M steps, so T2's budget stands. Ours scores 479 on CartPole, but only in its last tenth. The reference reaches 500 halfway through, so the slow curve was flagged; nothing was changed, as D16 was registered.
- **T1, seeds 0-4 a side.** Scores (the mean return of episodes ending in the last 10% of 499,712 steps):

  | seed | 0 | 1 | 2 | 3 | 4 | mean |
  |---|---|---|---|---|---|---|
  | ours | 500.0 | 267.1 | 136.1 | 500.0 | 489.8 | **378.6** |
  | reference | 500.0 | 487.5 | 500.0 | 500.0 | 398.0 | **477.1** |

  **Ours is 79.4% of the reference: C1 is refuted on T1** (the bar is 90%; the reference met its bar of 400, so the comparison stands). Mann-Whitney, exploratory: U = 9, exact two-sided p = 0.52, undecided at 5 a side.
- **The curves** (mean return in each tenth of the run): every reference seed is near 470 by its fourth tenth. Ours sits at 95-125 from its second tenth to its fifth on every seed, then climbs at different rates: seeds 0 and 3 reach 500, seed 4 490, seed 1 267, and seed 2 stays near 130 throughout. So ours learns, but far more slowly, and with much more spread.
- **By D16, T2 doesn't run and stage 4 doesn't start.** A diagnosis goes to the owner. The suspects, in D16's order:
  1. **The network's structure:** one shared trunk for policy and value, where the reference has two networks. A value loss with large returns (CartPole's reach 500, γ .99 gives targets near 100) can swamp the policy's gradient in a shared trunk.
  2. **The init:** fan-in, where the reference is orthogonal with its policy head scaled by 0.01 (a near-uniform start) and its value head by 1.
  3. **A bug:** losses and GAE are tested against hand-worked cases and finite differences (3.1), and the loop learns the fake level; neither excludes a subtle fault in how they're combined.
- Readings: indrajala-studies' gitignored `data/nes-control/`, with its manifest.

### Stage 3.2: the PPO loop (2026-11-06)

indrajala-rl#11: `ppo/train.py`, `ppo/inputs.py`, `ppo/network.py`, `scripts/train.py`; indrajala-ml#1279 first (bumped in indrajala-rl#10).

- **The loop:** rollouts sampled by inverse CDF on the trainer's own generator, GAE, then D3's epochs of shuffled minibatches through `learn_batch_output_gradient`, with the global gradient-norm clip at 0.5 (baselines'). The trainer reaches environments through a small protocol, which the vector runner meets, so 3.3's control can bring CartPole and MiniGrid through an adapter.
- **Checkpoints resume by replay.** nes-py's snapshot doesn't serialise (a native object with no pickle support), so a checkpoint holds the network in format 2, the trainer's state, and each environment's episode as a record: its generator's state at reset and the actions chosen since. Resuming replays them, which is exact because the environment is deterministic, and costs at most one episode's decisions an environment. The run isn't changed, as cutting every episode at a checkpoint would change it.
- **Found and fixed:** a given-loss network saved in format 2 lost its output layer's bias Adam state, because the names for a bias-free linear layer were given to a layer with a bias. A loaded network failed at its first step. Fixed in indrajala-ml#1279 with a test that training on from a saved file equals training on, on both backends; golden run bit-identical on `pyramidon`.
- **The exit, a run resumed equals one never stopped:** met on the fake game in CI (numpy and Rust, the checkpoint inside episodes), and **on the ROM**: on `stone`, 1-1, 32 environments, D3's settings, Rust, a run checkpointed after 2 iterations and resumed to 3 has the same log, network file and trainer state as a run of 3 never stopped.
- **A first look at the step** (`stone`, 8 workers × 4 environments, one run, not 3.4's measure): an iteration of 8,192 decisions takes 16 s, the rollout 8.7 s and the update 7.1 s, with a peak RSS of 1.58 GB in the trainer's process and a 6 MB checkpoint. The rollout's 940 decisions/s is below the runner's 1,100 alone, as the network decides between steps while the emulators wait (D15's remedy covers it).
- **On the fake game,** PPO learns level 3: under 90% of episodes cleared in the first 5 iterations, over 90% in the last 5 of 40.

### Stage 3.1: the losses and GAE (2026-11-06)

indrajala-rl#9: `ppo/gae.py` and `ppo/losses.py`, NumPy, forward-only.

- **GAE** over the runner's (T, N) rollouts: termination doesn't bootstrap; truncation bootstraps from V of the episode's final observation, not the next episode's start, which the rollout holds next; the sum is cut at every end. Tested on hand-worked cases, the Monte Carlo return at γ = λ = 1, and environments' independence.
- **PPO's loss** on the network's outputs (D2: logits, then the value): the clipped policy loss, the entropy bonus, the clipped value loss (baselines'), advantages normalised per minibatch, with each row's exact gradient at the outputs for the library's entry. Tested against central finite differences under three settings (rtol 1e-6) on a case shown to reach every region, plus hand-worked rows, the flat regions past the clip, and one step through `learn_batch_output_gradient` lowering the loss.

### Stage 2.3: the vector runner (2026-11-06)

indrajala-rl#8: `vector.py`, one process a worker (spawned), every observation and result in one shared-memory block, one byte each way a step, nothing pickled a step. Consoles and games are built in each worker from picklable factories. An episode that ends resets in its step, its last observation kept for the truncation bootstrap.

- **Same bits as serial:** on the fake game in CI, at 1, 2 and 5 workers, rewards, flags, actions taken, observations and final observations equal serial `NesEnv`s'; two runs are the same. On the ROM (1-1, sticky actions, 2 workers, 3 environments) the same against serial; `./cli test --emulate` on `stone`, 120 passed. Stage 2's determinism tests are now complete.
- **Speed** (`scripts/probe_throughput.py`'s new `--env`, `--runner`, `--per-process`; each seed's decisions one stream, so the free-running and runner rows do the same work; median of 3 runs of 10 s), decisions/s on 1-1 with random decisions:

  | | bare emulation | free-running `NesEnv` | runner, 1 a worker | runner, 4 a worker |
  |---|---|---|---|---|
  | `klip`, 4 workers | 394 | 392 | 379 | 387 (−1.8%) |
  | `klip`, 8 workers | 530 | 521 | 483 | **506 (−4.5%)** |
  | `stone`, 4 workers | 790 | 771 | 642 | 644 (−18%) |
  | `stone`, 6 workers | 1,030 | 1,007 | 884 | 887 (−14%) |
  | `stone`, 8 workers | 1,229 | 1,200 | 1,079 | **1,100 (−10.5%)** |

  The bare rows repeat stage 0's within 1.1% (536 and 1,242). **The exit, within 10% of the probe: met on `klip`, missed narrowly on `stone`.** The environment itself (observation, reward, resets) costs 2.4% at most. A round trip costs 20 µs on the fake console, so the pipes aren't the loss; with one worker the runner still loses 7% on `stone` (241 against 258), the wake-up of a parent that slept through the step. More environments a worker barely help (1,079 to 1,100), so the rest is lockstep: on `stone`'s mixed cores every step goes at an efficiency core's pace. D15 decides it. Readings: indrajala-studies' gitignored `data/nes-probe/vector/`, in its manifest.
- **Defaults from this:** 4 environments a worker, 8 workers on `klip`, 8 on `stone` (its 70%).
- **A trap:** workers start by `spawn`, so the parent's main module must be a file; code read from stdin kills each worker at start-up (raised as a `WorkerError`).

### Stage 2.2: the observation and the level table (2026-11-06)

indrajala-rl#6 (the pad fix) and #7 (the observation and the level driver); D14 in #156. On `klip` and `stone` with `--emulate`: 107 passed.

- **The level driver** (`scripts/drive_levels.py`): a save-state random search with a receding horizon (24 candidate plans of 16 decisions; commit half the best, at a boundary that restores exactly; back up two commitments on a stall), 150,000 decisions searched a level at most. Each run is then replayed through `NesEnv`, which records the census, and the game itself confirms a clear (it reaches the next level) and both kinds of death (it takes a life).
- **26 of 32 levels cleared,** each replayed to a clear and confirmed by the game. **Six stopped at the budget:** 4-2, 4-4, 6-2, 7-2, 7-4 and 8-4, including the three castle mazes. Rerun after the pad fix, they reached exactly the same points, so the search is deterministic and the six are the driver's limits, not the environment's. A death of each kind was confirmed on every level (6-2's fall excepted: the search met none).
- **nes-py's snapshot leaves out the pads,** reported upstream as [Kautenja/nes-py#110](https://github.com/Kautenja/nes-py/issues/110). A frame is a fixed count of CPU cycles, so a boundary can fall inside the game's pad read, and a restore there resumes the read from a drained shift register: the run diverged at about 1 boundary in 150. `NesPyConsole` now saves and restores each pad's 3 bytes beside the snapshot, guarded by a layout check (nes-py pinned at 9.0.1). An emulated test pins 3-1's mid-read boundary. The rerun had 0 inexact boundaries. **Training never restored mid-level** (reset is a power-on restore, always exact), so stage 1's readings stand. 12 levels kept from the run before the fix replay exactly under it.
- **The census:** 55 nonzero tile values and 39 object kinds over all 32 levels, now `TILE_VALUES` and `OBJECT_KINDS`; anything unseen maps to `UNSEEN`. With D14's one plane per value and the value planes over 4 decisions, **125 channels**. Low counts on 7-2 and 7-4 reflect where the driver stopped: castle and water areas use few metatiles (7-4's buffer there holds only castle brick, `0x62`).
- **The player was always small:** the driver never took a mushroom. Big Mario's placement was checked separately on `klip`, with his size and status written to RAM, against the sprites the game draws (OAM), as numbers, so no art left the machine. x is exact; the decoder's box is 1 line above the drawn sprite's lower 16 lines, for small and big alike, a constant sixteenth of a cell, left as is.
- **Shared cells:** 1.0% of decisions (203 of 20,314) have two entities in one cell, where the kind plane keeps one; most in 7-2 (88), 5-4 (26) and 8-4 (25).
- **Data:** each level's JSON (the actions as digits, the census, the checks; no art), in indrajala-studies' gitignored `data/nes-levels/` with a `MANIFEST.sha256`. Contact frames stay on `klip`.

**The level table.** Progress is pixels walked right, summed over areas. Areas counts the distinct areas entered.

| Level | Result | Decisions | Searched | Progress (px) | Areas | Tile values | Object kinds | Decisions with a shared cell |
|---|---|---|---|---|---|---|---|---|
| 1-1 | cleared | 301 | 13,744 | 3,121 | 1 | 18 | 3 | 3 |
| 1-2 | cleared | 326 | 14,255 | 2,864 | 3 | 25 | 8 | 4 |
| 1-3 | cleared | 239 | 17,801 | 2,385 | 1 | 10 | 7 | 3 |
| 1-4 | cleared | 208 | 9,778 | 2,219 | 1 | 6 | 5 | 4 |
| 2-1 | cleared | 673 | 37,349 | 3,134 | 3 | 22 | 6 | 5 |
| 2-2 | cleared | 546 | 25,355 | 3,121 | 1 | 14 | 5 | 0 |
| 2-3 | cleared | 314 | 18,149 | 3,553 | 1 | 11 | 2 | 2 |
| 2-4 | cleared | 208 | 10,729 | 2,204 | 1 | 8 | 8 | 1 |
| 3-1 | cleared | 364 | 14,863 | 3,129 | 3 | 22 | 7 | 3 |
| 3-2 | cleared | 304 | 12,564 | 3,297 | 1 | 14 | 5 | 1 |
| 3-3 | cleared | 244 | 23,707 | 2,369 | 1 | 10 | 7 | 0 |
| 3-4 | cleared | 208 | 9,730 | 2,221 | 1 | 8 | 6 | 1 |
| 4-1 | cleared | 352 | 15,779 | 3,553 | 1 | 18 | 4 | 0 |
| 4-2 | budget | 1,992 | 150,077 | 2,817 | 4 | 24 | 7 | 8 |
| 4-3 | cleared | 217 | 31,726 | 2,305 | 1 | 10 | 5 | 0 |
| 4-4 | budget | 1,976 | 150,192 | 999 | 1 | 5 | 2 | 3 |
| 5-1 | cleared | 335 | 16,950 | 3,132 | 2 | 16 | 5 | 2 |
| 5-2 | cleared | 323 | 17,464 | 3,132 | 3 | 25 | 10 | 2 |
| 5-3 | cleared | 279 | 113,702 | 2,385 | 1 | 10 | 8 | 2 |
| 5-4 | cleared | 240 | 10,897 | 2,220 | 1 | 8 | 11 | 26 |
| 6-1 | cleared | 305 | 13,963 | 2,929 | 1 | 17 | 3 | 0 |
| 6-2 | budget | 1,976 | 150,158 | 831 | 2 | 12 | 4 | 5 |
| 6-3 | cleared | 304 | 31,147 | 2,625 | 1 | 12 | 7 | 0 |
| 6-4 | cleared | 222 | 13,781 | 2,227 | 1 | 6 | 6 | 2 |
| 7-1 | cleared | 287 | 11,942 | 2,805 | 2 | 22 | 7 | 1 |
| 7-2 | budget | 1,976 | 150,047 | 2,563 | 2 | 3 | 3 | 88 |
| 7-3 | cleared | 322 | 19,290 | 3,553 | 1 | 11 | 6 | 0 |
| 7-4 | budget | 1,984 | 150,083 | 1,266 | 1 | 1 | 2 | 0 |
| 8-1 | cleared | 639 | 27,556 | 5,957 | 2 | 19 | 7 | 6 |
| 8-2 | cleared | 341 | 17,156 | 3,397 | 2 | 21 | 10 | 4 |
| 8-3 | cleared | 317 | 16,620 | 3,377 | 1 | 16 | 5 | 2 |
| 8-4 | budget | 1,992 | 150,094 | 1,288 | 2 | 7 | 3 | 25 |

### Stage 2.1b: SMB's layer (2026-11-05)

indrajala-rl#4: `games/smb.py`'s `SMB` implements `Game`, all but the observation (2.2's). Checked on `klip` with `--emulate`: 101 passed (peak 37 C).

- **Level starts:** the world, level and area registers are written through the title, then START. **Written later, during the intermission (as the reference does), they change the HUD and not the area:** the area pointer stayed the title's. Through the title, all 32 starts read their registers back and load distinct areas; their first screens were checked by eye (1-2 underground past the walk to the pipe, 2-2 and 7-2 water, every x-4 a castle). The start is the first frame of the game's core with the player in its normal state, about 207 frames from power-on.
- **`power_on` was wrong, now fixed:** nes-py's native reset is the reset button, not a power-on, so RAM survived it, and a second one sent the game elsewhere. `NesPyConsole` now restores the state saved after its first reset; a test checks that a reused console matches a fresh one.
- **The reward, as written (fixed from here):** in tiles of 16 pixels; new progress right **per area** (entering an area, or a jump of over 48 pixels in a decision, moves the mark unrewarded, so the total is distance walked); the game clock at 1/16 a tick; death 25/16, clear 50/16. These are the reference's values in tiles, without its score, coin and power-up terms. **A change from stage 2's text: bounded by construction instead of clipped,** as every term has a bound (at most about 6 a decision), so a clip could only cut a legitimate clear.
- **Episodes:** one life; busy stretches (areas loading, pipes, vines, the game's walks) are run through with no buttons, by frames rather than by writing the reference's timers.
- **Checked on the game:** death (running right in 1-1 dies at the first enemy, its reward matching x walked and the clock); determinism across two consoles under sticky actions; the sticky rate. **Not yet checked:** a clear (the flagpole slide and the end-of-world mode), falling below the screen, and an area change by a pipe. Each address's source and check are in `smb.ADDRESSES`. 2.2's driven runs check the rest.

### Stage 1: the library (2026-11-05)

| PR | What | Checked |
|---|---|---|
| indrajala-math-rust#117, indrajala-ml#1275 | conv's forward threaded over whole examples (D11) | same bits at 1-8 threads; golden bit-identical on `pyramidon` (164); on `litshe` every Rust network, its two numpy differences the same with the old crate (machine-specific BLAS) |
| indrajala-ml#1276 | `learn_batch_output_gradient`, the given-loss output layer, `forward_batch` | with softmax cross-entropy's gradient, `learn_batch`'s steps bit for bit on both backends; finite differences; golden bit-identical on `pyramidon` |
| indrajala-math-rust#118, indrajala-ml#1277 | the input path (D13): `Array.from_buffer`, `one_hot_planes` | bits against the list constructor and numpy; golden bit-identical on `pyramidon` |

**D11's effect, provisional** (`jebel` out, no claim; the probe on `klip`, same machine and venv, the crate rebuilt): forward 1,657 to 4,823 samples/s and learning 1,354 to 3,257 at 32 channels; 859 to 2,516 and 730 to 1,860 at 64. **So the network is no longer the larger cost on `klip`:** emulation would be about 60% of a step once D13's path replaces the conversion, past D10's half. Stage 3 reads D10 on the whole loop.

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
