# Workplan: motion control from a world model, with Super Mario Bros as the simplest platform scroller

**Status (2026-11-08): final. W0 (the literature) is done: 40 papers fetched, persisted in indrajala-literature
(9 held there under CC BY, the rest in the private archive) and read for their method and numbers. The plan's
citations were corrected against them (below, "What the papers said"); the decisions and stages were redrawn
from what they showed.** The owner settled the organ's input, how it is built, and the scope (D1-D3), and
confirmed them option by option on 2026-11-08. The rest is under the owner's delegation ("I leave the planning
in your hands"): D4-D13, each decided with its options. **W1 (frames and recordings) is done (2026-11-08), the owner's
play included; W2 (the organ) is under way: W2.1's first run is in the findings, its follow-up next. The order
after W2.4 is W8, then W3 (O2).** This plan is
its own, not a sub-plan of the NES plan's. It uses that plan's emulator, game layer and runners. Its IDs are its
own (D1-D13, O1, W0-W9).

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
3. reach goals it chooses in that world?

And does that, reused, clear levels faster and more reliably than learning the level directly? The baseline is
the NES plan's conv policy: 1-1 greedy 89-93 of 100, at about 8.5M decisions.

## Why this framing, and what it changes

- **The NES plan's network learned a policy from reward alone.** It cleared 1-1 well, but it has no model:
  nothing it learned about Goombas on 1-1 is stated anywhere it could reuse on 1-2. Its failures (the staircase
  trap) were invisible until they happened.
- **The machine-policy plan's control failed at a one-bit memory under PPO** (its M4: the greedy machine was a
  fixed turn, 2M decisions). Reward carried back to a cue seen once is a weak signal. A world model learns from
  **every frame's next frame**, a dense supervised signal. That is the setting in which the snapped networks
  certified machines (the papers).
- **Motion control in general** (driving, robots) is perceive, model, plan. A scroller is the smallest real
  case with self, static terrain, moving agents, landmarks and caused change all present.

## The literature, aspect by aspect

Each paper below was read in full or in its method and results sections (W0). Where the draft had the facts
wrong, the correction is listed in the next section. Keys are `library.bib`'s.

### 1. The organ: an exact object-centric reading of a 2D game

- **Object-centric states for Atari are an established research input.** OCAtari
  (`delfosse-2023-ocatari-object-centric-atari`, RLJ 2024) gives each game's objects by two methods: from RAM
  (REM) and by vision (VEM, from colours on known frames). It evaluates VEM's detection against REM's. Our
  organ is a VEM made exact, with RAM as the check, as OCAtari does it.
- **Learning SMB's rules from frames has been done, with a given sprite sheet.** Guzdial, Li & Riedl
  (`guzdial-2017-game-engine-learning-from-video`, IJCAI 2017) were given a fan-made sprite sheet. They located
  its sprites in each frame with OpenCV, matched each sprite to its nearest in the next frame greedily, and
  searched for an engine of rules (velocity, collision, animation) that predicts the next frame. They trained on
  1,569 frames from one player's 1-1 video and tested on another's. They beat a CNN's frame prediction and a
  copy-the-last-frame baseline on pixel error, and used the engine to train an agent. **Our organ is given no
  sprite sheet:** it finds the classes itself from the frames, which is what keeps it game-agnostic (D3).
- **The NES makes an exact organ possible.** The background is 8×8 tiles on a grid (SMB builds 16×16 blocks
  from them); sprites are 8×8 or 8×16; the camera scrolls by whole pixels; the status bar is a fixed split. The
  core's finished frame is 256×240 palette entries (6 bits, with `$2001`'s emphasis bits; `render.rs`,
  `Pixels::frame`). What a general organ must still handle:
  - palette cycling (question blocks, coins);
  - sprites behind the background (a Piranha plant in its pipe; the player entering a pipe);
  - overlapping sprites;
  - objects at rest;
  - transient effects drawn as sprites (brick debris, a coin's pop, the floating score).

### 2. Self: contingency

- **Contingency awareness** (`bellemare-2012-investigating-contingency-awareness-atari`, AAAI 2012) defines the
  contingent regions: the pixels whose next value depends on the action. **On the deterministic Atari with
  resets, the authors computed them exactly:** restore the state, take each action, and compare the next
  frames. They then learned a logistic predictor of them (on 5×5 blocks, predicting whether a pixel changes
  colour) and used it to build features. Tested on 46 unseen games, it helped model-free agents.
- **Learned from the agent's own actions:** Choi et al. (`choi-2019-contingency-aware-exploration`, ICLR 2019)
  train an attentive dynamics model to predict the action taken between two frames. Its spatial attention over
  a grid finds the controllable character. With count-based exploration on that location, A2C reached over
  11,000 on Montezuma's Revenge without demonstrations or RAM. That took 100M steps (400M frames), averaged over
  3 seeds.
- **Keypoints the agent controls:** Kulkarni et al. (`kulkarni-2019-transporter-keypoints-control`, NeurIPS
  2019, Transporter) learn keypoints from pixels. They predict the most controllable keypoint, which is usually
  the avatar. Exploration uses options that learn to move each keypoint.
- **Self-models and inverse objectives:** Haber et al. (`haber-2018-intrinsically-motivated-self-aware-agents`)
  train a world model and a self-model that predicts the world model's errors and steers play towards them.
  PlaySlot (`villar-corrales-2025-playslot-inverse-latent-dynamics`) infers each object slot's latent action
  from unlabelled video by inverse dynamics.
- **What this gives the plan:** "a sense of self" has an operational test with precedent. The self is the
  object whose motion the action predicts, found by an inverse model on the organ's tracks. The emulator's
  restore gives Bellemare's exact counterfactual as a second check, beside RAM's player (D5).

### 3. The world model

The candidates, each judged for this setting: an exact organ that gives objects; a deterministic game; sticky
actions on the agent's side; planning to chosen goals.

- **(a) Latent recurrent models, Dreamer** (`hafner-2020-dreamerv2-discrete-world-models`,
  `hafner-2023-dreamerv3-world-models`). The strongest general agent across Atari, control and Minecraft. Its
  strength is learning the representation from pixels, which the organ makes moot. Its latent is a fixed
  vector, not a set of objects, and opaque.
- **(b) Token and diffusion models over frames**, all on Atari 100k (26 games, 100k decisions):
  - IRIS (`micheli-2023-iris-transformers-world-models`): mean human-normalised 1.046; above humans on 10 of
    the 26.
  - STORM (`zhang-2023-storm-stochastic-transformer-world-model`): 126.7%.
  - DIAMOND (`alonso-2024-diamond-diffusion-world-modeling`): 1.46.
  - Genie (`bruce-2024-genie-generative-interactive-environments`, ICML 2024): an 11B-parameter model trained
    on 30,000 hours of Internet video from hundreds of 2D platformers (filtered from 200,000 hours; 160×90 at
    10 fps), with 8 latent actions learned unsupervised.

  They model pixels, which the organ has already abstracted. Genie's scale is beyond us. Its result is evidence
  that a platformer's controllable character is recoverable from unlabelled video.
- **(c) Value-equivalent models, MuZero** (`schrittwieser-2020-muzero-planning-learned-model`): it models
  value, policy and reward, not the world, so it has nothing to offer self-chosen goals and fails the play phase
  by design. COMET (`vakhitov-2026-comet-causal-object-centric-mcts`) runs MuZero-style tree search over a
  frozen object-centric encoder's slots: object structure helps search early in training.
- **(d) Object-centric, relational models:**
  - Interaction Networks (`battaglia-2016-interaction-networks`): per-object and per-relation functions,
    accurate over thousands of steps on n-body and rigid-body physics, and general over any number of objects.
  - C-SWM (`kipf-2020-contrastive-structured-world-models`, ICLR 2020): a graph network over object slots,
    trained contrastively, on grid worlds, Pong, Space Invaders and 3-body physics.
  - Schema Networks (`kansky-2017-schema-networks`, ICML 2017): object-oriented causal rules that transferred
    zero-shot across Breakout variations where A3C and Progressive Networks broke.
  - Object-oriented MDPs (`diuk-2008-object-oriented-representation-efficient-rl`, ICML 2008): DOORMAX, with a
    polynomial sample bound for deterministic object-oriented models. It assumes one effect type per action and
    attribute, with conditions as conjunctions of relations between objects.
  - SlotFormer (`wu-2023-slotformer-object-centric-dynamics`, ICLR 2023): a transformer over object slots,
    autoregressive in time, with better long-horizon rollouts than earlier dynamics models, used for
    goal-conditioned planning. **The nearest architecture to D4's.**
  - Dyn-O (`wang-2025-dyn-o-object-centric-world-models`): object-centric models on Procgen that beat
    DreamerV3's rollout accuracy.
  - OC-STORM (`zhang-2025-oc-storm-object-centric-world-models`, ICLR 2026): object features from a pretrained
    segmenter (SAM2 or Cutie, from a few annotated frames) beside downsampled pixels. It beat STORM on Atari
    100k and in Hollow Knight. **The gain was in games where the segmenter found every decision-relevant
    object; elsewhere it only matched the baseline.**
  - AXIOM (`heins-2025-axiom-object-centric-games`): gradient-free mixture models of objects with
    piecewise-linear motion and sparse interactions, grown and pruned online. On its own Gameworld 10k suite
    (10 simple games, 10,000 interactions) it beat BBF and DreamerV3.
  - DLPWM (`ferraro-2025-dlpwm-object-centric-world-models-policy`, a short preprint): unsupervised object
    latents reconstructed and predicted well, but policies on them underperformed DreamerV3 on robot lifting.
    The object latents drifted at contact.
- **(e) Rules as programs:**
  - EMPA (`tsividis-2021-empa-human-level-atari-theory`): game rules as VGDL programs inferred by Bayesian
    inference, with human-like learning speed on 90 Atari-style VGDL games, where DDQN and Rainbow made little
    progress.
  - WorldCoder (`tang-2024-worldcoder-model-based-llm-agent`, NeurIPS 2024): an LLM writes the world model as
    Python, optimistic about reward; gridworlds and task planning.
  - PoE-World (`piriyakulkij-2025-poe-world-programmatic-experts`, NeurIPS 2025): a product of many small
    LLM-written programs over OCAtari's objects, learned from a demonstration under a minute long. It planned
    in Pong and Montezuma's Revenge and generalised to unseen levels. It does not explore.
- **The verdict:** (d), as the draft had it, now with stronger grounds:
  - it matches the organ's output exactly;
  - one rule per kind of object generalises across levels by construction (a Goomba is a Goomba on 1-2);
  - next-state prediction is dense and supervised;
  - it is readable per object, and it plans to object goals naturally;
  - OC-STORM's and DLPWM's results say that object models pay when the objects are complete and stable. An
    exact organ with tracked identities gives exactly that, which removes DLPWM's failure (drift at contact)
    from the model's inputs.

  (e) is the step up if (d)'s rules turn out crisp (and W8's machines are its learned form). (a) is the
  external baseline. Known risks: errors compound over long rollouts; rare events are few in the data.

### 4. Play: exploration that builds the model

- **Curiosity on SMB itself:**
  - Pathak et al. (`pathak-2017-curiosity-self-supervised-prediction`, ICM) crossed a large part of 1-1 with no
    reward and explored 1-2 faster after it.
  - Burda et al. (`burda-2018-large-scale-curiosity`) found 11 levels of SMB with no reward and no
    end-of-episode signal, given 2,048 parallel environments; learned features generalised to new levels better
    than random ones.

  Their curiosity is a prediction error, which a deterministic game's noise can't fool, but which fades once
  the game is predicted.
- **Exploring for the model:** Plan2Explore (`sekar-2020-plan2explore-self-supervised-world-models`, ICML 2020)
  trains an exploration policy in the model's imagination. Its reward is an ensemble of one-step predictors'
  disagreement. Later tasks are then solved zero- or few-shot from the model (DM Control).
- **Self-set goals:**
  - IMGEP (`forestier-2022-imgep-intrinsically-motivated-goal-exploration`, JMLR 2022): goals sampled by
    learning progress, with object-centred modularity (one goal space per object), shown on a real humanoid.
  - The autotelic survey (`colas-2022-autotelic-agents-survey`, JAIR 2022).
  - SMORL (`zadaianchuk-2021-smorl-self-supervised-object-centric-rl`, ICLR 2021): goals set for one object at
    a time, in an object-centric representation.
- **Return, then explore** (`ecoffet-2021-go-explore-first-return-then-explore`, Nature 2021, Go-Explore):
  - an archive of reached cells, returned to by restoring the emulator, then explored from;
  - then made robust by learning from the archive's best trajectories;
  - a goal-conditioned variant returns by policy instead, which also handles stochasticity.

### 5. Control: reaching a chosen goal

- **Planning with a model:**
  - PETS (`chua-2018-pets-probabilistic-dynamics-models`, NeurIPS 2018): an ensemble of probabilistic models
    and trajectory sampling, with plans chosen by the cross-entropy method (CEM).
  - TD-MPC2 (`hansen-2024-td-mpc2-scalable-world-models`, ICLR 2024): MPPI over a decoder-free latent model,
    104 continuous-control tasks with one set of hyperparameters.

  Both act in continuous actions. Ours are 12 discrete actions held 4 frames each, so the planner is a beam
  search, or a CEM over categorical action sequences.
- **On Mario specifically:** Baumgarten's A* won the 2009 Mario AI Competition
  (`togelius-2010-mario-ai-competition`, CEC 2010). The game was Infinite Mario Bros, an open-source Java clone
  with generated levels, not the NES game. **The A* searched a copy of the game's own physics engine.**
  Enemies' speeds had to be derived from consecutive observations. In the competition's second phase, two
  controllers cleared all levels for some seeds, which made the organisers add levels and tiebreakers. An exact
  model plus search is enough for a platformer. Ours is learned, not copied: the emulator-backed planner (D12)
  is our copy, and the upper reference.
- **Amortising it into a policy:**
  - hindsight relabelling (`andrychowicz-2017-hindsight-experience-replay`, NeurIPS 2017, HER): a missed goal
    is a reached goal for where the episode ended;
  - goal-conditioned control learned from **human-teleoperated play** with relabelling
    (`lynch-2019-learning-latent-plans-from-play`, CoRL 2019): W1's human play from `nes-console` is that kind
    of data.

### 6. The learned organ (later)

- **Objects from pixels without labels:**
  - SPACE (`lin-2020-space-object-oriented-scene-representation`, ICLR 2020): foreground objects and background
    segments, on Atari and 3D rooms;
  - Slot Attention (`locatello-2020-slot-attention`, NeurIPS 2020);
  - for video, SAVi (`kipf-2022-savi-conditional-object-centric-video`, ICLR 2022), which needs hints in the
    first frame (objects' centres) to segment well, and STEVE (`singh-2022-steve-slot-transformer-videos`,
    NeurIPS 2022);
  - Transporter's keypoints (above).

  **SAVi's hints are what W2's organ can supply,** so W9 can start conditioned and drop the hints after.
- **Scoring it against RAM:** AtariARI (`anand-2019-atariari-unsupervised-state-representation`, NeurIPS 2019)
  probes learned representations for RAM's state variables, annotated from the games' source, on 22 games.
  OCAtari scores object discovery. We score the learned organ against RAM and against W2's organ.

### What nobody has, that this plan would

No work found combines an exact organ, a learned object-centric world model and self-set goals on SMB.
- Guzdial et al. learned SMB's engine from a given sprite sheet and didn't control with it beyond a demo agent.
- PoE-World is the nearest in spirit (objects given by a detector, a learned model, planning on Atari), with an
  LLM writing the model.
- LeMario, a 2026 blog post by Benjamin Bai (not a paper; its text was not retrieved, only secondary accounts),
  trained a JEPA (LeWorldModel) on about 737,000 SMB frames. Reward-free planning reached near goals and failed
  past obstacles. It is cited as an anecdote only.

## What the papers said, against the draft (W0's corrections)

| the draft said | the paper says | effect on the plan |
|---|---|---|
| Guzdial et al. "parsed SMB gameplay video into sprites" | from a given fan-made sprite sheet, by OpenCV template matching; 1,569 training frames of one 1-1 video | our organ's claim is stronger (no sheet); W2 must not be given SMB's sprites |
| Bellemare et al.: contingent regions "depend on the last action" | yes, and **computed exactly with resets on the deterministic Atari**, then learned | D5 gains an exact counterfactual check by restore |
| (handover) "Diuk's Pitfall" | the first Pitfall screen, six object types (man, hole, ladder, log, wall, tree) given by hand, objects from the image; the bound under DOORMAX's assumptions | cited for the bound and its assumptions only |
| OC-STORM "beat STORM on 18 of 26 Atari 100k games" | the published version (v2, ICLR 2026, retitled) gives no such count; it beat STORM overall, by much where the segmenter saw every decision-relevant object, and only matched it elsewhere | "18 of 26" removed; the conditional result supports D1-D2 |
| AXIOM: "games mastered in 10,000 steps" | on its own 10-game Gameworld 10k suite, beating BBF and DreamerV3 there; not Atari | qualified |
| Genie "learned from unlabelled 2D platformer videos" | yes: 30,000 hours, hundreds of platformers, 11B parameters | scale stated |
| Plan2Explore "plans towards where an ensemble disagrees" | trains an exploration policy in imagination on the disagreement | D6 uses disagreement as the planner's score, not an imagined policy (our variant, stated as such) |
| PETS "sampled action sequences" | CEM over continuous actions, with probabilistic ensembles | D7's planner is categorical CEM or beam search |
| Baumgarten's A* "on the game's forward model ... cleared every level" | Infinite Mario Bros (a Java clone), a copied engine; two entries cleared all levels for some seeds | corrected; D12's emulator planner is our equivalent |
| EMPA "90 Atari-style games" | 90 games written in VGDL | qualified |
| Choi et al.: over 11,000 on Montezuma | yes, at 100M steps (400M frames) | its cost stated |

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

- **Each layer is tested on its own, against the truth, before the next rests on it:**
  - the organ against RAM;
  - the self against RAM's player and the counterfactual by restore;
  - the model's rollouts against the emulator's, from the same restored states;
  - control on a fixed battery of goals, against the emulator-backed planner (D12);
  - the level on the NES plan's bar.
- **No layer sees RAM.** RAM is the test oracle only.
- **The emulator's restore is the agent's** in play (Go-Explore's return) and in the reference planner. Neither
  the self nor the model may use it as an input: a camera can't rewind.
- **Each layer is game-agnostic where it can be:** nothing in the organ, the self or the model names SMB; the
  goals are objects and map cells.

## Where machine discovery fits

**A good fit, as a branch off the main line, taken early (O2).** The game is a finite machine. Its objects' behaviours are
small machines over what they touch: a Goomba walks, turns at a wall, falls off a ledge; a moving platform
cycles. Learning those per-object rules from behaviour, with the organ as known structure, and reading each off
exactly, is stage E of the discovery note (raw inputs) on a real system (stage F), with RAM to check the find.
DOORMAX's assumptions (one effect type per action and attribute; conditions as conjunctions of relations) are a
stated, checkable form of "small machine over what it touches".
- The main line builds (d) plain, so this plan's results don't hang on the snap.
- **W8** learns each object class's update as the snapped window-recurrent cell, from the organ's tracks
  (W2.3, W2.4), and reads each class's machine off. That is the discovery result, checked against RAM's object
  state. Its cells go through the feasibility register (`docs/protocols/information-flow.md`) at registration.
- **It runs before W3 (O2, the owner, 2026-11-08),** so its machines are there when W4 comes. W4's (d) is
  then scored against them per object, the comparison this section first put the other way round.

## Decisions

### Settled by the owner (2026-11-08; confirmed option by option the same day)

- **D1. The organ's input.**
  - (a) *Chosen.* **Pixels only; RAM is the test oracle.**
    - Pros: the motion-control framing holds (a camera, not a memory dump); generic across games; honest.
    - Cons: the organ is real work, overlapping objects most.
  - (b) The PPU's layers (background against sprite pixels) from the emulator.
    - Pros: separation for free.
    - Cons: a hardware shortcut no camera has; NES-bound.
  - (c) RAM's tile grid and sprites, as the NES plan does.
    - Pros: built.
    - Cons: no vision; the organ moot.
- **D2. How the organ is built.**
  - (a) *Chosen.* **Algorithmic and exact first; a learned organ later (W9), scored against it and RAM.**
    - Pros: removes the organ as a source of failure while the layers above are built; certifiable against
      RAM; fast; nothing to train. W0 adds that object models pay only when the objects are complete (OC-STORM)
      and stable (DLPWM).
    - Cons: NES-shaped; a second game must test its generality.
  - (b) Fixed conv filters feeding the network.
    - Cons: leaves segmentation to the network.
  - (c) Learned from the start.
    - Cons: its failures tangle with the curriculum's.
- **D3. Scope.**
  - (a) *Chosen.* **SMB's levels for self, play and control, the organ game-agnostic; a second scroller only
    after control works (W6).**
    - Pros: the fastest first result.
    - Cons: generality checked late.
  - (b) Two games from the start.
    - Cons: slower to a first result.
  - (c) 1-1 only.
    - Pros: the smallest.
    - Cons: no held-out levels, so the model's generalisation (a Goomba is a Goomba on 1-2) can't be tested.

### Under the owner's delegation (decided; options with pros and cons)

- **D4. The world model's form.**
  - (a) *Chosen.* **Object-centric (section 3 (d)), SlotFormer's shape on exact tokens:**
    - tokens are the organ's tracked objects (class, position, velocity, age, the self flag), each with the
      landscape patch around it (the map's cell classes in a fixed window). Identities come from the organ's
      tracker, never re-inferred, which is DLPWM's failure removed;
    - a transformer over the set, with no order among objects (positions are features). Interaction by
      attention learns which pairs matter;
    - it predicts each object's next state, appearances and disappearances, and events (a map cell's class
      changing);
    - it is deterministic given the action taken, with an ensemble of 5 for disagreement (D6) and for PETS's
      epistemic spread;
    - it is trained on multi-step rollouts (its own predictions fed back, the loss at every step), not one step,
      against compounding error.

    It is scored against three baselines, each on the same organ output:
    - **copy:** every object holds its velocity (Guzdial's naive baseline, made physical);
    - **flat:** the objects padded to one vector, an MLP (the object claim);
    - **DreamerV3's world model on the same vector** (the external baseline, run only if (a) passes).

    - Pros: section 3's verdict; readable; reusable across levels.
    - Cons: drift on long rollouts; rare events; library work (D9).
  - (b) DreamerV3 on the organ's output (the objects padded to a vector).
    - Pros: proven; off the shelf in principle.
    - Cons: not ours to read; the organ's structure flattened (against our factored rule). Kept as a baseline.
  - (c) Rules as programs (EMPA's, PoE-World's kind).
    - Pros: exact; very sample-efficient.
    - Cons: a hand-made rule language, or an LLM in the loop; search; brittle beyond its language.
  - (d) The snapped window-recurrent network from the start.
    - Pros: the discovery goal directly.
    - Cons: ties the main line to the snap (M4's open diagnosis). Kept for W8.
- **D5. The self.**
  - (a) *Chosen.* **Learned contingency.** An inverse model, trained on motor babbling, predicts the action from
    each tracked object's motion. The self is the object that predicts it best: Choi et al.'s method, on
    objects, not pixels. **Two checks:** RAM's player, and Bellemare's exact counterfactual (restore the state,
    take each of the 12 actions, see which object's next state differs). The second is a test only, never the
    agent's input.
    - Pros: the agent finds itself, as the owner asked; precedent; two independent checks across power-ups and
      levels.
    - Cons: other objects can move with the action: a carried or kicked shell; a block bumped from below; the
      camera, which the organ's scroll removes first. A bumped block is contingent but not the self: the
      inverse model's score over a window of decisions, not one, separates them.
  - (b) The counterfactual by restore, as the method.
    - Pros: exact; no training.
    - Cons: needs a rewind no camera has; it is the emulator deciding.
  - (c) Given (the organ flags the player).
    - Cons: no sense of self to develop.
- **D6. Exploration in play.**
  - (a) *Chosen.* **Go-Explore's archive and return as the base, goals chosen from it, and the rest added only on
    a diagnosed need.** Cells are the self's map cell plus its power state; returning is a restore; from a
    returned cell the agent pursues a goal drawn from the map and objects near the frontier.
    - **Existence first:** the first probe is the archive with random goals.
    - **Then, only if coverage stalls:** goals by learning progress (IMGEP, one goal space per object class).
    - **Then, only if the model's held-out error stalls while coverage rises:** the ensemble's disagreement as
      the planner's score (Plan2Explore's signal, used by our planner, not by an imagined policy).
    - Pros: each part has a strong precedent and answers a different need (getting back to the frontier, what
      to try, where the model is weak); the restore is exact; one mechanism at a time, each kept only on
      evidence.
    - Cons: a restore no real robot has (stated; W7's level and W6's battery run without it).
  - (b) Curiosity by prediction error (ICM, RND).
    - Pros: simple; shown on SMB (11 levels with 2,048 environments).
    - Cons: no goals, so no control learned; it fades once predicted; its scale is beyond our machines.
  - (c) Random babbling only.
    - Pros: the simplest.
    - Cons: never leaves the start of a level.
- **D7. Control.**
  - (a) *Chosen.* **Plan with the model first, then distil.**
    - The plan: model-predictive control by categorical CEM (or a beam search) over sequences of the 12 actions,
      scored by the goal's distance and the self's survival, replanned every decision because of sticky actions.
    - The distillation: the plans into a goal-conditioned policy, with hindsight relabelling of every reached
      cell and object state (HER, Lynch et al.), on human play and the planner's episodes.
    - Pros: planning works as soon as the model does, with no policy to train (Baumgarten's A* is the existence
      proof on a copied engine; D12 is ours); the distilled policy is fast at play time.
    - Cons: planning is slow per decision (budgeted in model steps); sticky actions mean a plan must be
      replanned each decision.
  - (b) Model-free goal-conditioned PPO with hindsight.
    - Pros: our trainer exists.
    - Cons: the control M4 showed how weak reward alone is; ignores the model.
  - (c) Train the policy in imagination (Dreamer's way).
    - Pros: no planning at run time.
    - Cons: drift; later.
- **D8. The level.**
  - (a) *Chosen.* **A high-level chooser over play's goals (the next map cell or object to reach), trained on the
    level's reward, with control below it.**
    - Pros: the level reward meets a short decision chain (a few goals a screen), not thousands of button
      presses; skills reused.
    - Cons: the goal space must reach every move the level needs (pipes, the flag). W6's battery is drawn to
      cover them.
  - (b) Plan to the flagpole directly with the model.
    - Pros: no learning at all if the model is good.
    - Cons: long horizons; the flagpole must be known as the goal, which only the level's reward can say.
  - (c) The NES plan's PPO with play's representation as its input.
    - Pros: simple.
    - Cons: drops control's skills.
- **D9. The library.**
  - (a) *Chosen.* **indrajala-ml's library, with what it lacks added there:** a set-of-tokens input (no
    positional encoding across objects), per-token outputs, rollout training, an ensemble. The organ, the
    planner and the play loop go in indrajala-rl.
    - Pros: one stack, Rust kernels, our tests and the reader; durable.
    - Cons: building layers a framework has.
  - (b) A general framework on the CPU.
    - Pros: everything at once.
    - Cons: a second stack; no reader; off the programme's code.
- **D10. Machines and budget.**
  - (a) *Chosen.* **The organ and its tests on `pyramidon` (cheap, no training); data collection and the model's
    training on `stone` (60% from 2026-11-09 08:00) and `klip` (under the thermal guard); budgets in frames
    played and training epochs, set by each stage's first probe.** `jebel` stays out until the owner says.
    - Pros: the standing machine rules.
    - Cons: none new.
- **D11. Relation to the other plans.**
  - (a) *Chosen.* **The machine-policy plan pauses after M4** (M5 and M6 not run; M4's diagnosis, PPO against
    the snap, stays open there); the NES plan's results stay the baseline; crystallisation is out for now (O1).
- **D12. A reference planner on the emulator itself.** (New from W0: Baumgarten's A* searched a copied engine.)
  - (a) *Chosen.* **The same planner as D7, with the emulator (restore, step) in place of the learned model,
    scored on the same organ output.** It is used:
    - to check that each battery goal is reachable, and in how many decisions (W6's feasibility);
    - as the upper bound the learned model's control is compared with;
    - as a source of goal-reaching episodes for the distillation, labelled as such.
    - Pros: control's feasibility settled before the model exists; separates "the model is wrong" from "the
      planner is weak".
    - Cons: costs emulator steps (cheap: the core steps a frame in microseconds); a reference only, never in
      the agent's loop at W7.
  - (b) None: judge control only by its success rate.
    - Cons: a failure can't be placed in the model or in the planner.
- **D13. How play is recorded.** (New from W1's needs.)
  - (a) *Chosen.* **As inputs, replayed into frames.** A recording is the start (power-on, or a level's start
    state) and each frame's pad byte. Frames, RAM and the organ's output are made by replaying it through
    nes-python, which is deterministic. Human play needs `nes-console` to write its input log; the NES plan's
    policies and babbling already give actions.
    - Pros: tiny files; any later organ can be re-run on old play; exact by construction (checked by
      replaying).
    - Cons: a replay costs emulation time (small); frames kept for a stage's data are stored compressed beside
      it.
  - (b) Store every frame.
    - Pros: no replay.
    - Cons: 61 KB a frame raw; frozen to the recorder's version.

## The owner's calls

- **O2. W8 before W3: resolved (the owner, 2026-11-08).** Asked what I would most like to work on next, I
  chose W8 (each object's rule as a machine, read off and proved against RAM), run once the organ's objects
  and events (W2.3, W2.4) exist. The reasons:
  - it is the project's founding aim (machine discovery) on machines the learner doesn't know and RAM can check;
  - it gives W4's world model an exact target per object.

  The costs:
  - it delays the main line by a stage;
  - some objects may not be finite-state from what the screen shows (a hidden RNG, an off-screen spawn).
    Those are classed limits.

  The owner: "we will go with your choice - W8 - which I am happy with, and I agree with your approach". **The
  order is W2.1-W2.4, then W8, then W3-W7, then W9.**
- **O1. Crystallisation's place: resolved (the owner, 2026-11-08): "let's leave crystallization out for the
  moment".** The main line needs no snap before W8; crystallisation's place is revisited, if at all, when W8
  comes.

## Stages

Each stage is its own PR (or PRs) in the repositories named, merged before the next. Each stage that makes
claims from data registers them and their refutations before its data, with its feasibility table (the
experiment design, sections 1-2). Each stage's thresholds are set at its registration, from its first probe, not
here; the figures in "done when" are the bars the registration starts from.

### W0. The literature (done 2026-11-08)

- 40 papers fetched: 36 from arXiv (the latest version, its stamp checked) and 4 from their proceedings or
  authors' pages.
- Bib entries for all in `indrajala-literature`'s `library.bib`. The 9 under CC BY are held there (PDF and
  `.txt`); the rest are in `indrajala-literature-private`. Also checked from that archive: Pathak 2017, Burda
  2018 and DreamerV2.
- The plan's citations corrected (the table above).

### W1. Frames and recordings (D13): done 2026-11-08

The results are in the findings below. PRs: indrajala-nes #37 (W1.1), #38 (W1.2); indrajala-rl #36 (W1.3), #37 (W1.4's
tools).

| # | What | Where | Done when |
|---|---|---|---|
| W1.1 | `frame()` on nes-python's console: the finished frame as a 240×256 `uint16` array (palette entry and emphasis bits), from `Pixels::frame` | indrajala-nes | equal, frame for frame, to the viewer's picture on SMB's recorded run; a restored console's first frame after a restore is stated (the core draws a whole picture only from the next frame) and tested |
| W1.2 | The input log in `nes-console`: each frame's pad byte from power-on or a save state, written beside the recordings directory | indrajala-nes | a logged session replays through nes-python to the console's own final RAM, bit for bit |
| W1.3 | The recording format and replay in indrajala-rl: a recording (start, pad bytes, its source), replay to frames, RAM and actions; the game layer's level starts as start states | indrajala-rl | replay is exact against a recorded RAM trace; a test on the fake game |
| W1.4 | The first corpus, gitignored in `indrajala-studies/data/smb-world-model/` with a manifest: the owner's human play (any levels), the NES plan's conv policy on 1-1, random babbling on every level's start | indrajala-studies' data | the manifest lists each recording's source, frames and levels; every recording replays |

### W2. The organ (game-agnostic; nothing in it names SMB)

| # | What | Done when |
|---|---|---|
| W2.1 | **The screen-fixed region and the scroll:** rows that never move against the rest (the status bar), found from the data; the horizontal scroll per frame by matching the background's tile grid between frames | the scroll equals RAM's camera position on every frame of the corpus |
| W2.2 | **The landscape map:** 8×8 cells in world coordinates, each cell's class its exact pixel block; blocks that cycle in time (palette cycling) merged into one class by their cycle; cells hidden by objects filled from earlier frames | the map's classes a consistent function of RAM's metatiles on every level in the corpus (one class to one metatile up to the 8×8 split and palette cycles; every exception listed) |
| W2.3 | **Objects:** what the map doesn't explain, as connected components on the grid of non-background pixels, split and merged by appearance classes learned from the data (exact blocks again), tracked frame to frame by nearest match with persistent identities | matched to RAM's objects (player, enemies, power-ups, platforms) within a pixel, at a recall and precision set from the first probe, starting from 99%; **every miss classed** (overlap, behind the background, at rest, off-screen, a transient effect) |
| W2.4 | **Events:** a cell's class changing (a block broken, a question block used), objects appearing and vanishing | matched to RAM's block-buffer changes and object slots |
| W2.5 | **A second scroller's frames** recorded through W1, the organ run unchanged (D3's check, brought forward as a smoke test only; the claim is W6's) | runs without code changes; the failures listed |

**Feasibility:** the NES draws everything it shows from tiles and sprites on known grids. What can't be seen (a
Piranha plant inside its pipe; an enemy before it spawns on-screen) is a classed miss, not a failure.

#### W2.1's registration (2026-11-08, before the corpus run)

**The organ** (indrajala-rl's `indrajala_rl/organ/screen.py`, game-agnostic under the seam test):
- **Fixed bands.** Each pair of consecutive pictures in which the screen moved votes, row by row: fixed (fits
  zero, not the moving shift) or moving. The screen moved when more non-uniform rows fit one non-zero shift
  than fit zero. The bands are the top and bottom runs of rows that best separate the votes.
- **The shift** between pictures: the shift (within 32 pixels) under which the most columns of the scrolling
  rows are equal, by column hashes.
  - a best fitting under half the columns is a **cut**;
  - a tie for the best is **ambiguous** (a featureless screen).
- **Shots:** runs of pictures joined by shifts. A shot's position starts at 0 and moves by each shift. Its
  grid (where the 8-pixel tiles start) is the column offset whose 8×8 blocks are fewest, summed over the shot's
  pictures in its own coordinates.

**The oracle:** the scroll the game writes to the PPU for the playfield, from RAM.
- It is the name-table bit of `Mirror_PPU_CTRL_REG1` times 256, plus `HorizontalScroll`.
- It is read one frame before each picture: the NMI writes it before the picture's lines.
- **Why not the world camera** (`ScreenLeft`): the first probe found that the camera departs from the picture
  on transitions and on the game-over screen, where the picture didn't move.
- **The claims bind only in the game's core** (`OperMode` 1, `OperMode_Task` 3). In a transition, the game
  can change RAM's copy of the scroll without writing it. The probe's one case: at a world's end, going into
  an area's setup, the copy changed by a pixel while the picture stayed put. RAM is no oracle there.
- Outside the core, the same checks are counted and reported, not claimed.

**The data:** the whole W1 corpus (265 recordings, 375,836 frames), as 35 groups:
- each level's random play;
- the policy's greedy and sampled episodes;
- the owner's session.

Each group's band is found from its own pairs. The check is indrajala-rl's `scripts/organ_scroll.py`, run on
`stone`.

**The first probe** (before this registration) used the owner's session, random play on 1-1 and 8-4, and one
greedy 1-1 episode. Those three groups are reported apart from the 32 that no probe saw.

| claim | the test (in the core, on every picture) | refuted by |
|---|---|---|
| R1. One fixed band | every group's band is rows 0-31 fixed, 32-239 scrolling (the probe's) | any group's band differing |
| R2. Shifts exact | each pair classed as a shift has the drawn scroll's change (mod 512) | one pair |
| R3. Positions exact | each placed picture's position less the drawn scroll is constant (mod 512) within its shot | one picture |
| R4. The grid exact | each placed picture's phase, from its shot's grid, is the drawn scroll's mod 8; every shot with a core picture has a grid | one picture or shot |
| R5. Coverage | unplaced core pictures (in no shot) | more than 0.1% of core pictures (the probe: 0 of 65,831) |
| R6. Breaks only at changes of scene | each break of a shot in the core (a cut or an ambiguous pair) is a jump of the drawn scroll (over 32 pixels), or touches a picture of one colour (a level's start from black) | any other; each is listed and examined |

**Reported, not claimed:**
- the running phase (from the shot's pictures so far): how often it is right;
- the checks outside the core;
- in the core, whether the drawn scroll is the world camera mod 512.

**Feasibility:**
- The NES scrolls the playfield by whole pixels and draws the background from 8×8 tiles on a fixed grid. So
  one picture against the next shows the shift exactly wherever the scrolling rows hold a non-uniform column.
  A featureless screen is ambiguous by design, never a guess.
- The probe's pictures were exact on all six claims: 72,818 frames, 65,831 in the core.

### W3. The self (D5)

- Babbling: random actions held for random lengths, sticky as in the environment, from every level's start and
  from human play's states.
- The inverse model: per tracked object, its motion over the last k decisions to the action taken, a small
  classifier in indrajala-ml.
- Done when **the self is RAM's player on at least 99% of frames**, on held-out levels and in every power-up
  state; and it agrees with the counterfactual check (restore, each action) on a sample of states. The disagreements
  (a kicked shell, a bumped block) are listed.

### W4. The world model (D4)

- Data: W3's babbling, human play, the conv policy's episodes, as organ output.
- **First probe (existence):** 1-1 and 1-2 to train, 1-3 held out; one-step and k-step rollouts.
- Done when **k-step rollouts are within a pixel per object at stated rates on held-out levels** (k and the rates
  from the probe), and better than the copy and flat baselines. The rollout is checked against the emulator from
  the same restored states. Events are predicted at a stated recall.
- The ensemble's disagreement is reported against the actual error (it must rank states by error to serve D6).

### W5. Play (D6)

- The archive (cells: the self's map cell and power state), return by restore, goals near the frontier, the
  model retrained on what play gathers.
- Done when **the model's held-out error falls with play** and **coverage of the levels rises** against babbling
  at equal frames. The goals reached are recorded. Each added mechanism (learning progress, then disagreement)
  only on its stated stall.

### W6. Control (D7, D12)

- **The goal battery,** drawn from the archive's reached cells and objects, held-out levels included:
  - land on a chosen platform;
  - hit a chosen block from below;
  - cross a gap;
  - stomp an enemy;
  - enter a pipe;
  - climb the staircase.
- **The reference planner (D12) first:** each goal's reachability and decisions. A goal the emulator planner
  can't reach leaves the battery, with its reason.
- **Then the learned model's planner,** then the distilled policy, each under sticky actions and without
  restore. Done when **the battery is reached at stated rates on held-out levels**, reported against the
  reference planner's.
- **Then a second scroller's organ check (D3).**

### W7. The level (D8)

- The chooser over play's goals, trained on the level's reward, control below it.
- Done when **the NES plan's bar on 1-1 is met** (greedy 90 of 100, sticky, confirmed on fresh seeds). It is
  reported against the conv policy's frames to the bar (all play counted), and on held-out levels.

### W8. Discovery (after W2.4, before W3: O2)

- Each object class's update as a snapped machine, read off, minimised, and checked against RAM's object state.
- Its accuracy is compared with W4's. Its cells go through the feasibility register at registration.

### W9. The learned organ (D2)

- A slot or keypoint model from pixels (SAVi conditioned on W2's hints first, then unconditioned; Transporter as
  the second), scored against RAM (AtariARI's probes) and against W2's organ.
- Then swapped in under W3-W7, and the stages' results reported with it.

## Feasibility

| check | the claim | why it can succeed |
|---|---|---|
| the organ sees what it must | the scene is a function of the frames | the NES draws everything it shows from tiles and sprites on known grids; what it can't see (a Piranha plant inside its pipe) is a classed miss, not a failure |
| the self is identifiable | exactly one object's motion the buttons predict, over a window | in SMB only the player answers the pad; the camera is removed by the scroll first; things the player moves (a shell, a bumped block) answer only after contact, which a window separates; the counterfactual by restore confirms it |
| the model can be accurate | the next scene is a function of the scene and the action | the game is deterministic; sticky actions act on the agent's choice, not the world, so the action taken is known; what the screen hides (an enemy off-screen, an RNG-driven choice) bounds the rollout's horizon, stated per stage |
| control can succeed | each battery goal is reachable from its start | the reference planner on the emulator (D12) reaches it first; goals it can't reach leave the battery |
| no memorising | levels held out at every test | the model and the control are scored on levels they never trained on; sticky actions at every control test |

## Findings

- **W0 (2026-11-08):** the draft's facts were corrected against the papers (the table above). None of the
  corrections overturns a decision. Three sharpen the plan:
  - the exact counterfactual by restore (Bellemare) gives the self a second check (D5);
  - object models pay when the objects are complete and stable (OC-STORM, DLPWM), which argues for D1-D2's
    exact organ with tracked identities;
  - Baumgarten's A* searched a copied engine, so the emulator-backed planner (D12) is the upper reference that
    places a control failure in the model or the planner.
- **W1 (2026-11-08): frames and recordings.**
  - **W1.1, pictures:** `Console(rom, pixels=True)` on nes-python runs the viewer's console; `frame()` is each
    step's picture.
    - **After a restore** there is no picture until the next step (`frame()` refuses), and that step's picture is
      whole.
    - **The check:** equal, frame for frame, to the viewer's (hashes from `frame-hashes`) on SMB's recorded run
      (3,829 frames, 5 restores) and on 1-2, 4-4 and 8-4, RAM equal to the traces' throughout.
  - **W1.2, the input log:**
    - **The format** (`nes_host::inputs`, `INESINP1`): one segment of play, as its start (power-on, or a state in
      the saves container), JSON metadata (its source), each frame's pad bytes, the final RAM and its length, and
      a CRC.
    - **`nes-console` logs by default:** a reset, power cycle or load starts the next file; each is rewritten
      whole every 600 frames.
    - **The check:**
      - SMB's recorded run as 6 logs (37 KB against the trace's 1.1 MB) replays through nes-python to each
        log's RAM;
      - a console session with a save, reset, load and power cycle replays;
      - a 20-frame change is caught.
    - **A limit:** the final RAM alone missed a single flipped A press (SMB's RAM converged); W1.3's check is
      per frame.
  - **W1.3, recordings in indrajala-rl** (`recording.py`):
    - **One format:** the same input log, so human play, policies and babbling are one kind of file.
    - **`LoggingConsole`** starts a segment at each power-on, restore and write of RAM from outside. SMB's level
      start writes the level's registers at the title, so **a level's start is a start state**; each episode is
      one recording.
    - **The check:** replay is exact against a trace recorded at the same time, frame by frame, on the fake game
      and on SMB in both modes (600 decisions: 5 recordings, 2,637 frames).
    - **States load only into their own console variant** (mapper, render mode, sound rate), while power-on
      segments replay alike in both modes. **So recordings meant for pictures are made on the pixel console.**
  - **W1.4, the first corpus** (`stone`; `record_play.py`, `corpus_manifest.py`): gitignored in
    indrajala-studies' `data/smb-world-model/`, 2.8 MB, its `manifest.json`.
    - **Random play from every level's start:** 32 levels, 4 episodes each (up to 1,000 decisions), 222
      recordings, 261,582 frames.
    - **The NES plan's conv policy (checkpoint 1,037) on 1-1:** 20 greedy episodes (19 cleared; 27,897 frames)
      and 20 sampled (16 cleared; 28,669 frames).
    - **Every one of the 264 recordings replays exactly.** All 32 levels are in play in it, with 2,248 to
      69,443 frames each.
    - **The owner's own play** (2026-11-08, `nes-console`, 16 minutes): one log, 57,688 frames from power-on, in
      play on 1-1 to 2-2, in `human/`.
      - It replays exactly through nes-python's sounding pixel console. **That closes W1.2's check on a real
        console session on SMB.**
      - The corpus is now 265 recordings and 375,836 frames, all replaying.
    - **Lost:** an earlier 12-minute session wasn't logged. The release `nes-console` binary was from before
      #38 and hadn't been rebuilt after the merge.
- **W2.1, the registered run (2026-11-08):** `stone`, 807 s, indrajala-rl `cbc3f78` (#38's branch), the corpus
  (manifest sha256 `66165a3e…`), all 35 groups, 375,836 frames. The results are in
  `stone:~/labour/w2/w2-1.json` (sha256 `0a939782…`), copied to `pyramidon`.
  - **R2, R3, R4 and R5 hold, with none wrong:**
    - every core pair classed as a shift had the drawn scroll's change (360,935);
    - every core picture was placed, its position exact within its shot and its phase exact (361,169);
    - none was left unplaced.
    - The 32 groups no probe saw: 295,338 core pictures, all exact. In the core, the drawn scroll was the
      world camera mod 512 on every frame.
    - The running phase was right on all but 28 core pictures (12 wrong, 16 undecided), all early in shots of
      the castles 2-4, 3-4, 5-4 and 7-4. It is reported, not claimed.
  - **R1 is refuted as registered:** 34 groups gave rows 32-240 and 3-4 gave 32-239.
    - Row 239 tied in 3-4 (one vote each way). The code takes the first of equally good bands, the narrowest
      scrolling one, where its own docstring says the widest.
    - This is an implementation fault, not a fault of the rule.
  - **R6 is refuted as registered:** 66 breaks of shots in the core.
    - 59 were changes of scene: 4 jumps of the drawn scroll, and 55 touching a picture of one colour.
    - **7 were false cuts:** 5 in the owner's play (1-4 and 2-1), 2 in 3-4's random play. The scroll was
      unchanged (best at shift 0), but objects changed just over half the columns (best fit 0.465-0.496,
      718-15,548 pixels changed). A column fails on a single pixel.
    - Each false cut breaks a shot; no value is wrong, and the next shot's positions are exact.
  - **My error in the registration:** it said the probe was exact on all six claims. The probe had 28 core
    cuts without a jump. I examined one (a level's start from black) and generalised; the probe was never
    re-run with the break classes. 5 of the 7 false cuts are in the probe's own data.
  - **Next:** W2.1′, a separately registered follow-up with the two fixes (the band's tie-break as
    documented; a cut test that moving objects can't trip). Each fix touches one claim's mechanism only.
