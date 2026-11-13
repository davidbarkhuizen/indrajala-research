# Briefing: the SMB world-model plan, and where W6 stands (2026-11-13)

A factual brief, written for an outside analysis. Part 1 describes the plan. Part 2 describes the current
situation of its stage W6 in detail. It records what was built, measured and decided, and leaves interpretation
out where it can. Where a past decision record gave a cause, this brief says it is that record's reading.

The source of record is [smb-world-model-workplan.md](../workplans/smb-world-model-workplan.md): "The revision of
2026-11-10", its decisions D19-D73, the owner's calls O3-O8, and the W6 sections. IDs here are that plan's. The
code is in the private repository indrajala-rl (`main` at `65344c2`). The data is in indrajala-studies'
gitignored `data/smb-world-model/`.

---

## Part 1. The plan

### The aim

The owner's picture (2026-11-08) treats Super Mario Bros (NES) as the simplest platform scroller, and a platform
scroller as the simplest case of motion control: a maze with static obstacles, predictable moving parts
(platforms, enemies), landmarks (the flagpole) and changes the agent causes. The agent is **given** a visual
"organ", built by hand rather than learned. From pixels, the organ finds the avatar, the static landscape, the
moving objects and events. The curriculum is a sense of self first, then play toward goals the agent sets
itself, then the level.

**The question:** given an exact, fixed visual organ, can an agent, from its own play and with no level reward:
1. identify itself;
2. learn a world model accurate enough to plan with;
3. reach goals it chooses?

And does that, reused, clear levels better than learning the level directly? The baseline is an earlier conv
policy trained by PPO: 1-1 greedy at 89-93 of 100, after about 8.5M decisions.

### Standing method rules (the project's)

- **Learn the method, not imitate it:** no hand-given decomposition or traces; train on inputs and answers.
- **Factored, not flat:** the action is factored into axes, and objects keep their identities.
- **Every stage:** one probe, one registration with bars set before the data, one run (D30). A refuted gate takes
  its named fallback once. Refuted again on the oracle's scenes at W4 or W6, the plan stops and goes to the owner.
- **The feasibility rule:** no cell is run that can't succeed on the probe's evidence.
- **Hardware is CPU only:** a numpy-based in-house library (indrajala-ml) and no GPU. Trainings run on one 8-thread
  desktop (`stone`, used at up to 70%).

### Two sources of scenes (O4)

Every layer works on a **scene**: a decision's landscape cells (8 px tiles, each a shape class, a palette, and
whether it is seen) and its objects (identity, kind, box in pixels), plus events. A scene comes from two sources:

- **the organ:** from pixels alone, algorithmic;
- **the oracle:** from RAM and the PPU, holding exactly what a perfect organ would give. Each object's box is the
  box of its visible sprite pixels, from a picture redrawn from PPU memory. Its kind is RAM's slot id. The
  landscape comes from the PPU's background.

Every layer is built and tested on the oracle's scenes first, then on the organ's. **All of W6 so far is on the
oracle's scenes.**

### "Complete" (O3)

The SMB work is complete when this table is filled with registered results:

| | the oracle's scenes | the organ's scenes |
|---|---|---|
| the self (W3) | done | (W12) |
| the world model, held-out play (W4) | done | (W12) |
| the goal battery (W6) | **stopped: see Part 2** | (W12) |
| 1-1 under sticky actions (W7) | | (W12) |

The full aim is the bottom-right cell: 1-1 cleared in at least 90 of 100 greedy attempts with sticky actions
(each decision repeats the previous action with probability 0.25), from pixels alone.

### The stages and their state

| stage | what | state |
|---|---|---|
| W0 | the literature (40 papers) | done |
| W1 | frames and recordings (265 recordings, 376k frames, all 32 levels, including the owner's play) | done |
| W2.1-W2.4 | the organ: the screen, the landscape map, objects, events | done (W2.3′ refuted one claim, by 1.2 points; objects closed by D15) |
| W10 | the scene format and the oracle | done |
| W11 | the reference planner on the emulator, the goal battery, deep play | passed (1-1: 95 of 100 at `exact` 6) |
| W3 | the self, from contingency | done: the self is the player on 99.86% of babbling's decisions and 100% of deep play's |
| W4 | the world model, one step ahead | done: beats the copy baseline per kind and for the self |
| **W6** | **control: the planner on the learned model, against the planner on the emulator** | **stopped, put to the owner (O8)** |
| W5 | play: an archive, self-set goals, the model retrained | not started |
| W7 | the level: the planner on a learned reward | not started |
| W13 | the organ's second round | not started |
| W12 | W3-W7 on the organ's scenes | not started |

### The architecture, in brief

```
scene (oracle) ──▶ the self (RAM's player, on the oracle's scenes: D43)
               ──▶ the world model: each object's next box from its last k boxes, kind, landscape window,
                   one neighbour, and (for the self) the action and past actions
               ──▶ the planner: sampled action sequences rolled in the model, scored, the best first action
                   taken, and planning again every decision
```

---

## Part 2. W6: the current situation

### What W6 tests

W6 swaps the reference planner's world, the exact emulator with save and restore, for the learned model. It keeps
everything else: the planner, its settings, the goals and the judge.

**The gate:** for each goal kind, the model's success count must be at least **80%** of the reference's on the
same attempts. W6 has not been registered: no configuration has passed the gate on the probe states.

### The game and time step

- One **decision** is 4 frames, with the action held.
- The action is factored into axes: horizontal (none, right, left), A (jump), B (run), vertical (none, down, up).
- Sticky actions at 0.25: in each decision, the game repeats the previous action instead of the chosen one with
  probability 0.25.

### The planner (W11's, D25; indrajala-rl `planner.py`)

- **Each decision:** 24 candidate action sequences over a **horizon of 16 decisions** (64 frames). Each sequence
  is made of held segments (`--segment 4`: held 1-7 decisions). The previous best plan, shifted, is kept among the
  candidates.
- **Each candidate is rolled in the model and scored.** Stickiness is taken in expectation over all 2^3 stick
  patterns of its first 3 decisions (`exact 3`); later decisions don't stick (`--rollout-sticky 0.25`).
- **The score:**
  - progress: the goal's distance closed, in cells;
  - a death costs 1,000 (`--death -1000`);
  - reaching the goal ends the rollout well.
- The best candidate's first action is taken in the **real game**, which is never restored. Then the planner plans
  again.
- **The battery's settings:** `--every 480 --limit 60 --sequences 24 --horizon 16 --segment 4 --rollout-sticky 0.25
  --exact 3 --death -1000 --workers 8`.
- **Speed:** the model takes 0.04-0.06 s a decision on one core (about 1,350 model steps a decision); the
  emulator reference takes 0.4-0.7 s.

### The battery (D51, D59)

- **States:** from 100 recorded episodes of 1-1 by the reference planner (L1's), one state every 480 core frames
  with the player standing.
- **Goals:** in each state, one goal of each kind that the scene shows, drawn by seed:
  - **land** on a chosen cell;
  - **bump** a chosen ? block or brick from below;
  - **stomp** a chosen Goomba or Koopa.
- **Rules:** at most 60 decisions an attempt, under sticky actions, with no restore.
- **The judge is RAM's** (W11's `smb_goals.reached`) in the real game. The model only steers.
- **The reference:** the same planner on the emulator, on the same attempts and seeds.
- **Probe 4's reference** is the fixed denominator for every probe since:

| kind | attempts | the reference reached |
|---|---|---|
| land | 193 | 186 |
| bump | 78 | 63 |
| stomp | 63 | 50 |

The probes' states are L1's, and the models trained on L1's episodes, among other data. W6's registration would
run on L1′'s 100 episodes, which no model trained on.

### The model (W4, D22-D23, D44; amended by D58, D66, D68)

**One small dense network shared by every object, one decision ahead.**

- **Inputs, per object:**
  - its kind (one-hot over the 38 commonest, plus "other");
  - its last `k` motions (`k` 8): each decision's change of the top, left, bottom and right edges, clipped to ±16;
  - its size;
  - a self flag, and for the self the action's axes (one-hot);
  - for the self, its last 8 actions (D58);
  - the landscape window's cells (shape index one-hot, 64 shapes plus "other", "unseen" and "outside"): 4×4 cells
    by default;
  - its nearest neighbour's kind and relative box (`n` 1);
  - with D66, the box's offset within its anchor cell (one-hot);
  - with D68, its age, for objects seen fewer than `k` decisions.
- **Outputs:**
  - each of the four edges' motion, as a categorical among -16..16 or beyond either way (35 classes each, chosen
    independently);
  - whether the object vanishes;
  - its next kind.
- **Rollout:** each step takes the **argmax** of each head (deterministic). The four edges are chosen apart, so a
  predicted box can be incoherent (e.g. the top moves while the bottom stays).
- **The current form:** 256×3 hidden, 10 epochs, Adam, cross-entropy per head. It trains in about 5 minutes on 4
  threads and peaks at 8.8-12 GB.
- **Training data:**
  - the W1 corpus;
  - babbling (sticky random actions from states along recorded play);
  - the reference's deep play (L1's 100 episodes of 1-1, and an every-level pass);
  - level 1-3 held out;
  - 340,083 object-steps.
- **The scene model (D48):**
  - its state is the objects in the decision's scene, with their histories;
  - the landscape is frozen at the plan's start, and cells beyond the view are "outside";
  - **no object can appear during a rollout.**
- **The ensemble (D67):** five members (seeds 0-4) each roll every candidate, and a candidate's score is the
  members' mean.

**The oracle's self box** is the visible sprite's box. Its size changes often: width in 37% of steps, height in 15%
(probe 11's traces). The player is 16 px tall when small. The ground's top line in 1-1 is at y 208 (bottom of a
standing self).

**The model's goal tests (D49, D57, D60, D64, D65).** These are the planner's model-side proxies; RAM judges.
- **land:** the feet at the cell's top in a step that doesn't rise, over its column;
- **bump:** the head comes up to the cell's bottom line in a rising step, under its column;
- **stomp:** the feet come down onto the enemy's visible top in a falling step, overlapping in columns;
- **death:**
  - the self vanishes;
  - or its box passes the screen's bottom;
  - or its box overlaps a stompable enemy with its feet below the enemy's top by more than the tolerance.

### W4's offline measures (the registered model, before W6's changes)

Held-out babbling, exactly right next box:

| | the model | the copy baseline |
|---|---|---|
| the other objects | 62.3% | 37.3% |
| the self | 26.3% | 11.0% |

The self's mean rollout error, against copy:
- on babbling: 1.3 px at 1 decision, 10.5 at 8, 18.0 at 16 (copy 2.0, 34.0, 62.0);
- on deep play: 0.9, 9.7 and 19.9 px.

Later models (past actions, 256×3, offset, young) have the self exact on 37.8-40.4% of held-out babbling steps,
and the self's rollout error at 8 and 16 decisions at 5.1 and 8.7 px (the three-layer model).

### The history of W6's probes

Each row is the planner on the model, with the model's success count as a share of the reference's (probe 4's
denominators from probe 3 on; probes 1-2 were smaller batteries).

| probe | what changed | land | bump | stomp |
|---|---|---|---|---|
| 1 | W4's model as registered (24 recordings, 79 attempts) | 90.7% | 32.0% | 0% |
| 3 | the self's past 8 actions (D58); visible goals only (D59) | 93.5% | 65.1% | 18.0% |
| 4 | the stomp as a contact (D60) | 93.5% | 65.1% | 44.0% |
| 5 | the stomp tolerance 2/4/8, and the touch death off | | | 40-48% |
| 7 | the enemy's last box held while out of view (D62 (a)) | | | 44.0% |
| 8 | a larger network (256×3) | 91.4% | 61.9% | 52.0% |
| 9 | rollout training: scheduled sampling / DaD (D63) | 90.3% / 89.2% | 71.4% / 65.1% | 54.0% / 36.0% |
| 10 | bump as a contact (D64) | 90.3% | 74.6% | 54.0% |
| 11 | land as a contact (D65); then the box's offset in its cell (D66) | 91.4% / 93.0% | 74.6% / 66.7% | 54.0% / 56.0% |
| 12 | horizon 8 / 12 / 16 | 87.6 / 93.0 / 93.0% | 76.2 / 63.5 / 66.7% | 46.0 / 68.0 / 56.0% |
| 13 | an ensemble of 5: one member / mean / min (D67) | 95.2 / 97.8 / 83.3% | 73.0 / 73.0 / 50.8% | 50.0 / 60.0 / 30.0% |
| 14 | young objects with their age (D68), mean of 5 | 97.3% | 73.0% | 70.0% |
| 15 | `k` 16, past 16 (D71), mean of 5 | 96.8% | 73.0% | 74.0% |
| 16 | a 6×4 window (D72), mean of 5 | 97.8% | 68.3% | 68.0% |

**Counts for probes 14-16** (the reference: 186, 63, 50):

| probe | land | bump | stomp |
|---|---|---|---|
| 14 | 181 | 46 | 35 |
| 15 | 180 | 46 | 37 |
| 16 | 182 | 43 | 34 |

**Land** has been at or above the gate since probe 13. **Bump** has stayed between 61.9% and 76.2% through every
configuration. **Stomp** has risen from 0% to 68-74%.

### Bump: the facts

**Where the misses are.**
- In probes 13-16, nearly all bump misses are the **high bricks, row 3** of the level's metatile grid:

  | probe | misses on row 3 | all misses (row 7 the rest) |
  |---|---|---|
  | 13 | 15 | 18 |
  | 14 | 16 | 17 |
  | 15 | 16 | 17 |
  | 16 | 19 | 20 |

- The low bricks (row 7) are reached 37 of 38 times (probe 4).
- **Probe 4's split of row 3:**

  | high bricks | the model | the reference |
  |---|---|---|
  | columns 80-84 | 0 of 9 | 5 of 9 |
  | column 131 | 4 of 31 | 20 of 31 |

- In probe 13, the reference reached 25 row-3 goals and the model 10.

**The geometry of column 131** (probe 4's diagnosis):
- The brick's bottom is at line 96.
- Under it there is only a two-wide platform (row 7, columns 129-130), with the staircase's top (row 7, column 137)
  beside it.
- It can't be reached from the ground. The self must first get onto the platform or the stair top (its feet at
  lines 142-144), then jump from there.

**What the model-planned self does in the misses:**
- **probe 4:** the self gets onto the platform or stair top, never jumps from there toward the brick, and walks
  off;
- **probe 14 (D69's reading):** in most traces the self stays below the lower bricks, jumping, and doesn't get
  onto them.

**The climb diagnosis.** Probe 14's ensemble, `planner_battery.py --follow`: the model's path takes the reference's
own recorded actions, and at each decision every member's open-loop rollout of the next 16 actions is traced.
Following the reference's actions, the real game reaches the same 63 bumps.

**Foresight:** the share of members whose rollout puts the self's top within 2 px of the truth at the bump's
decision, from `h` decisions before:

| `h` | 1 | 4 | 8 | 12 | 16 |
|---|---|---|---|---|---|
| row 3, probe 14 | 0.94 | 0.85 | 0.62 | 0.50 | 0.45 |
| row 3, probe 15 (`k` 16) | 0.90 | 0.84 | 0.70 | 0.57 | 0.42 |
| row 3, probe 16 (6×4) | 0.96 | 0.86 | 0.68 | 0.54 | 0.52 |
| other rows, all three | 0.83-1.00 at every `h` | | | | |

**The one-step vertical error by decisions since takeoff** (row 3's attempts; the members' mean of the top and
bottom errors):

| | ages 0-8 | ages 9-16 |
|---|---|---|
| probe 14 | 0.19-0.94 px | 0.43-2.04 px |
| probe 15 | 0.21-1.19 px | 0.52-1.93 px |
| probe 16 | 0.17-0.78 px | 0.42-2.42 px |

**Where row 3's rollouts first leave the truth.** A rollout leaves the truth when its bottom is more than 4 px
off, or its centre more than 4 px off. There were 4,865 rollouts in each probe:

| | probe 14 | probe 16 |
|---|---|---|
| never left the truth | 1,445 | 1,419 |
| in the air, rising | 897 | 1,005 |
| the box changes size | 815 | 826 |
| in the air, falling | 530 | 417 |
| the apex or a head hit | 367 | 411 |
| a landing | 229 | 201 |
| a horizontal stop | | 255 |
| walking off a ledge | | 147 |
| on the ground | | 95 |
| a takeoff | | 89 |

**Arrivals after a fall,** one decision ahead. These are the decisions where the true self's last fall ends; a
fast fall is 4 px or more a decision. Each cell is the members within 1 px of the true bottom, with the median
error:

| | fast, on the ground (140) | fast, on a raised surface (55) | slow, raised (45) |
|---|---|---|---|
| probe 14 | 71% (0 px) | 31% (6 px) | 80% (0 px) |
| probe 15 | 69% (0 px) | 20% (6 px) | 78% (0 px) |
| probe 16 | 73% (0 px) | 44% (4 px) | 56% (0 px) |

**Two particular errors:**
- In recording 1027, the oracle's self box jumps about from step to step (likely the sprite's visibility).
- Apex arrivals on the ledge's top (bottom 144) are predicted to fall through by 8 px.

**The self in the air under A** (probe 4, the D58 model, all kinds). A false rise is a predicted rise of at least
3 px where the self didn't rise:

| the self | A | decisions | mean vertical error | false rises |
|---|---|---|---|---|
| in the air | fresh press | 428 | 3.10 px | 34 |
| in the air | held | 2,217 | 1.20 px | 42 |
| in the air | none | 2,750 | 1.59 px | 39 |
| on the ground | fresh | 412 | 1.02 px | 12 |
| on the ground | held | 191 | 1.13 px | 4 |
| on the ground | none | 2,916 | 0.37 px | 8 |

The same measure on held-out babbling, for probe 14's member `y0` against probe 16's `w0`:

| in the air | `y0` | `w0` |
|---|---|---|
| A fresh (461 steps) | 1.87 px | 1.76 px |
| A held (9,727 steps) | 0.36 px | 0.30 px |
| no A (7,434 steps) | 0.81 px | 0.68 px |

**Probe 10's traces of the self** (before the offset input, D66):
- falling steps: 208 phantom landings (the model stops the self, which falls on), and 375 falls too slow or too
  fast, among about 2,059;
- walking off a ledge: 33% of steps off by 4 px or more;
- the apex or a head hit: 14%.

The offset (probe 11b) cut phantom landings from 231 to 154, and vertical errors of 4 px or more from 789 to 686,
out of about 9,000 decisions.

### Stomp: the facts

- **Probe 4's diagnosis.** 29 attempts were reached by the reference and not by the model:
  - 10 died: the self landed beside the enemy, the boxes overlapping by 1-3 px;
  - 10 lost the enemy from the scene for part of the attempt;
  - 9 had the enemy in view throughout and never reached it.
- **The enemy's own one-step error** is 0.38 px within 32 px of the self (1,055 decisions) and 0.30 px further
  away (834).
- **D53 and D68:** before D68, an object entered the model's state only after `k + 1` decisions in view. 35 of the
  reference's 50 stomps began with the target too young for that. The model, when it got there, took a median of
  39 decisions (the reference: 12).
- **With young objects (probe 14),** stomps reached take a median of 11 decisions.
- **Probe 14's 17 stomp misses:**
  - 6 had the enemy leave the scene. None came back: 2 fell into a pit (last boxes at y 227-239), 3 left by the
    left edge (where the game erases enemies), and in 1 the self left the area.
  - 11 died or ran out of decisions with the enemy in view.
- **Holding the enemy's last box while out of view** (probe 7) left stomp unchanged, at 22 of 63. The unconfirmed
  stomps went from 3 to 12.

### Changes that moved the model's offline measures but not bump

| change | offline effect | bump |
|---|---|---|
| larger network (probe 8) | the self exact 32.2% → 37.8%; 16-decision drift 11.2 → 8.7 px | 65.1% → 61.9% |
| DaD rollout training (probe 9) | the self worse; each round's loss on its new pairs rises | 65.1% |
| scheduled sampling (probe 9) | the self unchanged; the other objects improve | 71.4% |
| the offset (probe 11b) | fewer phantom landings | 66.7% |
| ensemble mean (probe 13) | | 73.0% |
| young objects (probe 14) | the self exact 39.6-40.4% | 73.0% |
| `k` 16 (probe 15) | | 73.0% |
| the 6×4 window (probe 16) | better air errors and raised arrivals | 68.3% |

### What has been decided and what is open

- **D69** (after probe 14): W6 was stopped and put to the owner (O7). The owner chose route 1, one more round:
  object permanence for stomp, and a diagnosis of the ledge climbs for bump.
- **D70:** object permanence was dropped: the targets that left the view never came back.
- **D71** (`k` 16): refuted.
- **D72** (the 6×4 window): refuted for control.
- **D73:** W6 was put to the owner again.
- **O8 (open).** The routes listed for the owner:
  1. the self's motion in the air as rules (D23's last form; DOORMAX-like rule search);
  2. D4's transformer over the scene's objects, with an ensemble and rollout training;
  3. the bump gate (O3's table) is the owner's to set;
  4. W5 and W7 on the model as it is, with W6 reported unregistered.

### Things not tried, as recorded in the plan

- **D4's transformer:** not built. The plan held it back for a diagnosed interaction the small network can't
  express, and none was found (the enemy's error is 0.3 px).
- **D22 (c), a recurrent state:** not built (the function check put the self's open share under 5% at `k` 8).
- **Rules for any object (D23 (c)):** not built.
- **Sampling from the model's categorical outputs:** not tried. Every rollout takes the argmax of each head, and
  the ensemble's members are the only source of spread.
- **A joint output for the box:** not tried. The four edges are separate heads.
- **A planner change for the model:** not tried. The planner is W11's, unchanged: 24 sequences, horizon 16,
  segments of 1-7 decisions. Only the horizon was varied (probe 12).
- **New objects during a rollout, or a moving view:** not possible in the scene model (D48).
- **Training on the battery's own failure states:** not tried. The tables are W4's sources.

### Where the data is

indrajala-studies, `data/smb-world-model/control/w6/`: `probe1` to `probe16`, `climb/` (probe 14 followed),
`models`, `models2`, `dad`, `ensemble`. Each probe directory holds its `run.sh`, its logs, the battery's result
JSON with per-decision traces, and its models. The analysis scripts are indrajala-rl
`scripts/follow_check.py`, `scripts/planner_battery.py` and `scripts/world_check.py`.
