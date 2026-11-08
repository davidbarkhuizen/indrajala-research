# Workplan: motion control from a world model, with Super Mario Bros as the simplest platform scroller

**Status (2026-11-08): a rough draft, at the owner's request ("write up a rough draft of the plan ... research
each aspect individually against the literature ... then form the best overall synthesis"). The owner settled
the organ's input, how it is built, and the scope (D1-D3); the rest is under the owner's delegation ("I leave
the planning in your hands"), each with its options below. Nothing is built yet; W0 (the literature) is
first.** This plan is its own, not a sub-plan of the NES plan's; it uses that plan's emulator, game layer and
runners. Its IDs are its own (D1-D11, W0-W9).

## The owner's picture (2026-11-08)

"Use SMB as an example of a platform scroller, and a platform scroller as the simplest version of motion
control / self driving ... essentially as a maze (geospatial environment) with static geospatial challenges
(holes to jump over, pipes to jump over and go into, a stepped slope to climb before the final flag), dynamic
adversarial components (moving platforms, hostile actors ... technically also just dynamic but predictable
environmental features)." The network is given **an optical pre-processing organ**, not expected to develop
one, which lets it determine:

1. what **its avatar** is (identity);
2. the truly **static landscape** it must navigate;
3. the **dynamic** features (moving platforms, creatures);
4. **unique landscape features** (the flagpole);
5. **changes caused by the avatar's actions** (a broken block grows a mushroom).

The network builds a **spatio-temporal world model** from its exploration. The curriculum:
- **first, a sense of self:** it understands that it is the avatar;
- **then play,** apart from any goal of finishing a level: comprehend the environment through the organ, and
  learn to control the avatar to reach intermediate goals it is set ("pick a platform and jump onto it, hit a
  target block with your head");
- **then the level.**

The owner, on the organ: "first algorithmic to remove it as a source of variation / failure, then if/when that
works, we go back and try again with the learned organ."

## The question

Given an exact, fixed visual organ, can an agent, from its own play and no level reward:
1. identify itself;
2. learn a world model accurate enough to plan with;
3. reach goals it chooses in that world;

and does that, reused, clear levels faster and more reliably than learning the level directly (the NES plan's
conv policy: 1-1 greedy 89-93 of 100 at about 8.5M decisions)?

## Why this framing, and what it changes

- **The NES plan's network learned a policy from reward alone.** It cleared 1-1 well, but it has no model:
  nothing it learned about Goombas on 1-1 is stated anywhere it could reuse on 1-2, and its failures (the
  staircase trap) were invisible until they happened.
- **The machine-policy plan's control failed at a one-bit memory under PPO** (its M4: the greedy machine was a
  fixed turn, 2M decisions). Reward carried back to a cue seen once is a weak signal. A world model learns from
  **every frame's next frame**, a dense supervised signal, which is the setting where the snapped networks
  certified machines (the papers).
- **Motion control in general** (driving, robots) is perceive, model, plan; a scroller is the smallest real
  case with self, static terrain, moving agents, landmarks and caused change all present.

## The literature, aspect by aspect

### 1. The organ: an exact object-centric reading of a 2D game

- **Object-centric states for Atari are an established research input.** OCAtari (Delfosse et al. 2024, RLJ;
  arXiv:2306.08649) extracts objects from Atari games, from RAM and by a vision mode, for object-centric RL and
  for scoring object discovery. Ours does the vision side, with RAM as the check, as OCAtari does.
- **Learning a game's rules from the frames of SMB has been done:** Guzdial, Li & Riedl (2017, IJCAI, "Game
  Engine Learning from Video") parsed SMB gameplay video into sprites and searched for an engine that predicts
  the next frame. It beat a CNN's frame prediction. Its parsing is our organ's job, made exact.
- **The NES makes an exact organ possible:** the background is 8×8 tiles on a grid (SMB builds 16×16 blocks of
  them), sprites are 8×8 or 8×16, the camera scrolls by whole pixels, and the status bar is a fixed split. What
  a general organ must still handle: palette cycling (question blocks, coins), sprites behind the background
  (a Piranha plant in its pipe), overlapping sprites, and objects at rest.

### 2. Self: contingency

- **Contingency awareness** (Bellemare, Veness & Bowling 2012, AAAI): the screen regions whose next value
  depends on the last action. Used as features, it helped across 46 Atari games.
- **Learned, from the agent's own actions:** Choi et al. (2019, ICLR, "Contingency-Aware Exploration") train an
  attentive dynamics model to predict the action taken between two frames. Its attention finds the controllable
  character; with count-based exploration on that location, it reached over 11,000 on Montezuma's Revenge
  without demonstrations or RAM.
- **Keypoints the agent controls:** Kulkarni et al. (2019, NeurIPS, Transporter) learn keypoints from pixels
  and explore by learning to move each one.
- **What this gives the plan:** "a sense of self" has an operational test with precedent. The self is the
  object whose motion the action predicts, found by an inverse model, and checked against RAM's player.

### 3. The world model

Candidates, each judged for this setting (an exact organ that gives objects; a deterministic game; sticky
actions on the agent's side; planning to chosen goals):

- **(a) Latent recurrent models, Dreamer** (Hafner et al. 2020, DreamerV2; 2023, DreamerV3, both in our
  bibliography). The strongest general agent across Atari, control and Minecraft. Its strength is learning the
  representation from pixels, which the organ makes moot; its latent is a fixed vector, not a set of objects,
  and opaque.
- **(b) Token and diffusion models over frames:** IRIS (Micheli et al. 2023), STORM (Zhang et al. 2023),
  DIAMOND (Alonso et al. 2024); Genie (Bruce et al. 2024, ICML) learned an action-controllable model from
  unlabelled 2D platformer videos. They model pixels, which the organ has already abstracted.
- **(c) Value-equivalent models, MuZero** (Schrittwieser et al. 2020): no model of the world, so nothing for
  self-chosen goals; it fails the play phase by design.
- **(d) Object-centric, relational models:** Interaction Networks (Battaglia et al. 2016, NeurIPS: per-object
  and per-relation functions, generalising to any number of objects); C-SWM (Kipf, van der Pol & Welling 2020,
  ICLR: objects and relations by a graph network, trained contrastively); Schema Networks (Kansky et al. 2017,
  ICML: object-oriented causal rules that transferred zero-shot across Breakout variants where A3C broke);
  object-oriented MDPs (Diuk, Cohen & Littman 2008, ICML: a polynomial sample bound for deterministic
  object-oriented models). Recent: OC-STORM (Zhang et al. 2025, arXiv:2501.16443: object features beside
  pixels beat STORM on 18 of 26 Atari 100k games); AXIOM (Heins et al. 2025, arXiv:2505.24784: objects with
  piecewise-linear motion and sparse interactions, growing online, games mastered in 10,000 steps without
  gradients).
- **(e) Rules as programs:** EMPA (Tsividis et al. 2021, arXiv:2107.12544: game rules as programs inferred by
  Bayesian inference, human-level learning speed on 90 Atari-style games, where DDQN made little progress);
  WorldCoder (Tang, Key & Ellis 2024, NeurIPS: an LLM writes the world model as Python).
- **The verdict:** (d). It matches the organ's output exactly; one rule per kind of object generalises across
  levels by construction (a Goomba is a Goomba on 1-2); next-state prediction is dense and supervised; it is
  readable per object; it plans to object goals naturally. (e) is the step up if (d)'s rules turn out crisp;
  (a) is the external baseline. Known risk: errors compound over long rollouts; rare events are few in the data.

### 4. Play: exploration that builds the model

- **Curiosity on SMB itself:** Pathak et al. (2017, ICM) and Burda et al. (2018, large-scale curiosity, which
  played SMB's levels with no reward), both in our bibliography. Their curiosity is a prediction error, which
  a deterministic game's noise can't fool, but which also fades once predicted.
- **Exploring for the model:** Plan2Explore (Sekar et al. 2020, ICML) plans towards where an ensemble of models
  disagrees, then solves later tasks zero-shot from the model.
- **Self-set goals:** intrinsically motivated goal exploration (Forestier, Portelas, Mollard & Oudeyer 2022,
  JMLR: goals sampled by learning progress, with object-centred modularity); the autotelic survey (Colas,
  Karch, Sigaud & Oudeyer 2022, JAIR); SMORL (Zadaianchuk, Seitzer & Martius 2021, ICLR: goals set per object
  in an object-centric representation).
- **Return, then explore** (Ecoffet et al. 2021, Nature, Go-Explore): an archive of reached states, returned to
  (on an emulator, by restoring them) before exploring further.

### 5. Control: reaching a chosen goal

- **Planning with a model:** model-predictive control by sampled action sequences (PETS: Chua et al. 2018,
  NeurIPS; TD-MPC2: Hansen, Su & Wang 2024, ICLR). **On Mario specifically:** Baumgarten's A* on the game's
  forward model won the 2009 Mario AI Competition and cleared every level (Togelius, Karakovskiy & Baumgarten
  2010, CEC). An accurate model plus search is enough for a platformer; our model is learned, not given.
- **Amortising it into a policy:** hindsight relabelling (Andrychowicz et al. 2017, NeurIPS, HER: a missed goal
  is a reached goal for where it ended); learning goal-conditioned control from play (Lynch et al. 2019, CoRL).

### 6. The learned organ (later)

- **Objects from pixels without labels:** SPACE (Lin et al. 2020, ICLR, which separated objects from background
  on Atari); Slot Attention (Locatello et al. 2020, NeurIPS); for video, SAVi (Kipf et al. 2022, ICLR) and STEVE
  (Singh, Wu & Ahn 2022, NeurIPS); Transporter's keypoints (above).
- **Scoring it against RAM:** AtariARI (Anand et al. 2019, NeurIPS) probes learned representations for RAM's
  state variables, 22 games; OCAtari scores object discovery. We score it against RAM and against the given
  organ.

### What nobody has, that this plan would

No work found combines an exact organ, a learned object-centric world model and self-set goals on SMB. LeMario
(a 2026 blog post, not a paper) trained a JEPA model on SMB's frames and found planning worked for near goals
and failed past obstacles. Guzdial et al. learned SMB's engine but didn't control with it.

## The synthesis

```
pixels ─▶ organ (exact, fixed) ─▶ scene: landscape map · objects (tracks) · events
                                      │
                        self ◀── inverse model (which object do my actions move?)
                                      │
                world model ◀── next scene from scene + action, per object
                                      │
          play: goals from the map; explore where the model is unsure; archive and return
                                      │
          control: plan to the goal with the model, then distil to a goal-conditioned policy
                                      │
          the level: choose the next goal towards the clear; the level's reward only here
```

- **Each layer is tested on its own, against the truth, before the next rests on it:** the organ against RAM;
  the self against RAM's player; the model's rollouts against the emulator's; control on a fixed battery of
  goals; the level on the NES plan's bar.
- **No layer sees RAM.** RAM is the test oracle only.
- **Each layer is game-agnostic where it can be:** nothing in the organ, the self or the model names SMB; the
  goals are objects and map cells.

## Where machine discovery fits

**A good fit, but as a branch, not the main line.** The game is a finite machine; its objects' behaviours are
small machines over what they touch (a Goomba walks, turns at a wall, falls off a ledge; a moving platform
cycles). Learning those per-object rules from behaviour, given the organ as known structure, and reading each
off exactly, is stage E of the discovery note (raw inputs) on a real system (stage F), with RAM to check the
find. So:
- the main line builds (d) plain, so this plan's results don't hang on the snap;
- **W8** then replaces (d)'s per-object update by the snapped window-recurrent cell and reads each class's
  machine off. That is the discovery result, checked against RAM's object state, and a comparison against (d)'s
  accuracy.

## Decisions

### Settled by the owner (2026-11-08)

- **D1. The organ's input.**
  - (a) *Chosen.* **Pixels only; RAM is the test oracle.** Pros: the motion-control framing holds (a camera,
    not a memory dump); generic across games; honest. Cons: the organ is real work, overlapping objects most.
  - (b) The PPU's layers (background against sprite pixels) from the emulator. Pros: separation for free. Cons:
    a hardware shortcut no camera has; NES-bound.
  - (c) RAM's tile grid and sprites, as the NES plan does. Pros: built. Cons: no vision; the organ moot.
- **D2. How the organ is built.**
  - (a) *Chosen.* **Algorithmic and exact first; a learned organ later (W9), scored against it and RAM.** Pros:
    removes the organ as a source of failure while the layers above are built; certifiable against RAM; fast;
    nothing to train. Cons: NES-shaped; a second game must test its generality.
  - (b) Fixed conv filters feeding the network. Cons: leaves segmentation to the network.
  - (c) Learned from the start. Cons: its failures tangle with the curriculum's.
- **D3. Scope.**
  - (a) *Chosen.* **SMB's levels for self, play and control, the organ game-agnostic; a second scroller only
    after control works (W6).** Pros: the fastest first result. Cons: generality checked late.
  - (b) Two games from the start. Cons: slower to a first result.

### Under the owner's delegation

- **D4. The world model's form.**
  - (a) *Chosen.* **Object-centric (literature, section 3 (d)):**
    - tokens are the organ's objects (class, position, velocity, the self flag), each with the landscape patch
      around it;
    - a transformer over them (interaction by attention, which learns which pairs matter), then each object's
      next state, and events (a map cell's class changing);
    - deterministic given the action taken;
    - trained on multi-step rollouts, not one step, against compounding error.

    Pros: section 3's verdict. Cons: drift on long rollouts; rare events; new library work.
  - (b) DreamerV3 on the organ's output (the objects padded to a vector). Pros: proven, off the shelf in
    principle. Cons: not ours to read; the organ's structure flattened (against our factored rule).
  - (c) Rules as programs (EMPA's kind). Pros: exact, very sample-efficient. Cons: a hand-made rule language;
    search; brittle beyond it.
  - (d) The snapped window-recurrent network from the start. Pros: the discovery goal directly. Cons: ties the
    main line to the snap (M4's open diagnosis); kept for W8.
- **D5. The self.**
  - (a) *Chosen.* **Learned contingency: an inverse model, trained on motor babbling, predicts the action from
    each tracked object's motion; the self is the object that predicts it best** (Choi et al.'s method on
    objects, not pixels). Pros: the agent finds itself, as the owner asked; precedent; checkable against RAM's
    player across power-ups and levels. Cons: other objects can move with the action (a carried shell; the
    camera, which the organ's scroll estimate must remove first).
  - (b) A fixed statistical test (each track's motion correlated with the buttons). Pros: no training. Cons:
    given, not learned; it is the organ deciding.
  - (c) Given (the organ flags the player). Cons: no sense of self to develop.
- **D6. Exploration in play.**
  - (a) *Chosen.* **Goals from the map, chosen by learning progress (IMGEP), plus planning towards where an
    ensemble of models disagrees (Plan2Explore), from an archive of reached states restored on the emulator
    (Go-Explore).** Pros: each part has a strong precedent, and each answers a different need (what to try,
    where the model is weak, getting back to the frontier); the restore is exact. Cons: three mechanisms; the
    first probe may need only one (existence first).
  - (b) Curiosity by prediction error (ICM, RND). Pros: simple; shown on SMB. Cons: no goals, so no control
    learned; it fades once predicted.
  - (c) Random babbling only. Pros: the simplest. Cons: never leaves the start of a level.
- **D7. Control.**
  - (a) *Chosen.* **Plan with the model first (sampled action sequences or a beam search over the model, scored
    by distance to the goal), then distil the plans into a goal-conditioned policy with hindsight relabelling.**
    Pros: planning works as soon as the model does, with no policy to train (Baumgarten's A* is the existence
    proof for platformers); the distilled policy is fast at play time. Cons: planning is slow per decision;
    sticky actions mean a plan must be replanned each decision, as MPC does.
  - (b) Model-free goal-conditioned PPO with hindsight. Pros: our trainer exists. Cons: the control M4 showed
    how weak reward is alone; ignores the model.
  - (c) Train the policy in imagination (Dreamer's way). Pros: no planning at run time. Cons: drift; later.
- **D8. The level.**
  - (a) *Chosen.* **A high-level chooser over play's goals (the next map cell or object to reach), trained on
    the level's reward; control below it.** Pros: the level reward meets a short decision chain (a few goals a
    screen), not thousands of button presses; skills reused. Cons: the goal space must reach every move the
    level needs (pipes, the flag).
  - (b) Plan to the flagpole directly with the model. Pros: no learning at all if the model is good. Cons:
    long horizons; the flagpole must be known as the goal, which only the level's reward can say.
  - (c) The NES plan's PPO with play's representation as its input. Pros: simple. Cons: drops control's skills.
- **D9. The library.**
  - (a) *Chosen.* **indrajala-ml's library, with what it lacks added there** (a set-of-tokens input, the
    per-object output, an ensemble); the planner and the play loop in indrajala-rl. Pros: one stack, Rust
    kernels, our tests and the reader; durable. Cons: building layers a framework has.
  - (b) A general framework on the CPU. Pros: everything at once. Cons: a second stack; no reader; off the
    programme's code.
- **D10. Machines and budget.**
  - (a) *Chosen.* **The organ and its tests on `pyramidon` (cheap, no training); data collection and the
    model's training on `stone` and `klip`; budgets in frames played and training epochs, set by each stage's
    first probe.** Pros: the standing machine rules. Cons: none new.
- **D11. Relation to the other plans.**
  - (a) *Chosen.* **The machine-policy plan pauses after M4** (M5, M6 not run; M4's diagnosis, PPO against the
    snap, stays open there); the NES plan's results stay the baseline; **crystallisation's order is the owner's
    to confirm (O1, below).**

## Open for the owner

- **O1. Crystallisation's place.** The owner said (2026-11-08) to return to crystallisation after the NES
  machine policy, or sooner if it stalled at the snap. M4 failed, but before the snap took over (above). This
  plan's main line doesn't need the snap until W8. **The proposal:** this plan's W0-W3 first (no snap in
  them), crystallisation before W8.

## Stages

| # | What | Where | Done when |
|---|---|---|---|
| W0 | **The literature:** fetch and persist the core papers (sections 1-6), bib entries in indrajala-literature (PDFs where licensed), notes in this plan | indrajala-literature, here | each paper read for its method and its numbers; the plan's citations checked against them |
| W1 | **Frames:** the finished frame (palette entries) from the Rust console's Python binding; recorded play (human play from `nes-console`, the NES plan's policies, random babbling) as frames, actions and RAM, gitignored | indrajala-nes, indrajala-rl, indrajala-studies' data | frames bit-identical to the viewer's; recording and replay exact |
| W2 | **The organ**, game-agnostic: the scroll; the screen-fixed region (the status bar); the landscape as 8×8 tile classes by exact pattern, with palette cycles as one class; objects as what the landscape doesn't explain, as connected components, tracked; events as a cell's class change; the landscape map in world coordinates | indrajala-rl (a module of its own) | against RAM on recorded play, over several levels: the scroll exact; the map's classes a consistent function of RAM's tiles; objects matched to RAM's within a pixel at stated recall and precision; every miss classed (overlap, behind the background, at rest) |
| W3 | **The self (D5):** motor babbling, the inverse model, the self found | indrajala-rl | the self is RAM's player on at least 99% of frames, on held-out levels and every power-up state |
| W4 | **The world model (D4):** data from W3's babbling and recorded play; the model; rollouts | indrajala-ml, indrajala-rl, `stone` | k-step rollouts within a pixel per object at stated rates, on held-out levels; against a flat model of the same organ output (the object claim) |
| W5 | **Play (D6):** goals from the map, exploration, the archive | indrajala-rl, `stone`, `klip` | the model's held-out error falls with play; coverage of the levels rises; the goals reached are recorded |
| W6 | **Control (D7):** the goal battery (land on a chosen platform, hit a chosen block, cross a gap, stomp an enemy) by planning, then the distilled policy; then a second scroller's organ check (D3) | indrajala-rl | the battery at stated rates on held-out levels, under sticky actions |
| W7 | **The level (D8):** the chooser, the level's reward | indrajala-rl, `stone`, `klip` | the NES plan's bar on 1-1 (greedy 90 of 100, sticky, confirmed on fresh seeds); against the conv policy's frames to the bar |
| W8 | **Discovery (the branch):** each object class's rule as a snapped machine, read off; against RAM's object state | indrajala-ml, indrajala-rl | each class's machine read off, minimised, and checked; its accuracy against W4's |
| W9 | **The learned organ (D2):** a slot or keypoint model from pixels, scored against RAM and W2's organ (AtariARI's probes), then swapped in under W3-W7 | indrajala-rl | its scores against the given organ's; the stages' results with it |

Each stage registers its claims and their refutations before its data, with its feasibility table (the
experiment design, sections 1-2). Each stage's thresholds are set at its registration, from its first probe,
not here.

## Feasibility (rough, for the draft)

| check | the claim | why it can succeed |
|---|---|---|
| the organ sees what it must | the scene is a function of the frames | the NES draws everything a frame shows from tiles and sprites on known grids; what it can't see (a Piranha plant inside its pipe) the RAM check classes as a miss, not a failure |
| the self is identifiable | exactly one object's motion the buttons predict | in SMB only the player answers the pad; the camera's response is removed by the scroll estimate first |
| the model can be accurate | the next scene is a function of the scene and the action | the game is deterministic; sticky actions act on the agent's choice, not the world, so the action taken is known; what the screen hides (an enemy off-screen) bounds the rollout's horizon, stated per stage |
| control can succeed | each battery goal is reachable from its start | goals are drawn from cells and objects the archive has reached (W5) |
| no memorising | levels held out at every test | the model and the control are scored on levels they never trained on |

## Findings

None yet.
