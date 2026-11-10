# The SMB world-model plan and its work so far: an assessment (2026-11-10)

**Status: a dated review, at the owner's request:** "assess the smb-world-view workplan, and the work
so far, and check for problems, then make suggestions"; then "write this analysis up - then take them
all into account and revise the workplan - we need a plan that will work". The plan is
[docs/workplans/smb-world-model-workplan.md](docs/workplans/smb-world-model-workplan.md); its revision
in the light of this review is recorded there (its "The revision of 2026-11-10").

**Who wrote it.** Claude (Fable 5.2), through Claude Code, the reviewer of
[review-2026-11-10-programme-review.md](review-2026-11-10-programme-review.md); it took no part in the
SMB work.

**The short of it.** The lower layers and the way they were tested are sound: the scroll and the tile
grid are exact, the landscape map is exact up to tiles drawn alike, and the oracle (each picture drawn
again from the PPU's memory) is a strong check. The plan as written would still not reach its end. The
layers above the organ assume complete, stable objects with a kind, read as the play goes; the organ
finds 71% of the objects that aren't the player, gives no kinds, and is scored with hindsight over each
recording. The recordings cover the levels' first screens. Three of the later stages' feasibility rows
don't hold. And the parts most likely to fail (a learned model good enough to plan with) come last,
behind stages that don't bear on them.

## Method and limits

- **Read in full:** the workplan (1,348 lines: the literature, D1-D18, O1-O2, the registrations and
  findings of W0-W2.3′, W2.4's plan, W3-W9).
- **Code read (indrajala-rl at `bfd4ef2`):** `organ/landscape.py` in full; `organ/objects.py` (the
  foreground, the tracker, its constants and interfaces); `scripts/organ_objects.py` (the passes over a
  group, the outcomes, the identities, the claims); `games/smb.py` (what it reads from RAM);
  `recording.py` (replay). Not read line by line: `organ/screen.py`, `ppu_picture.py`, the detection's
  matching (`explain`, `detect`).
- **Run:** the organ's unit tests and the seam test (52 pass).
- **Data read:** W2.3′'s result (`w2-3p.json`, sha256 `2299f2c1…`, and its score), in
  indrajala-studies' gitignored `data/smb-world-model/organ/`.
- **Measured here,** by replaying the W1 corpus on `pyramidon` with a scratch script (RAM read as the
  oracle only): how far the player gets in each recording, and the player's pixel position and pad on
  every frame of the policy's 1-1 play. The script was a scratch file and is not in a repository; the
  revised plan makes both readings tools.
- **Not done:** no organ run, no training. The NES emulator and the machine-policy code were not
  reviewed.
- **Every reading here is post hoc.**

**Severity** (the 2026-10-23 audit's scale): **S1** a statement is wrong or unsupported; **S2** a stated
rule is broken, or a claim is weaker than stated; **S3** documents disagree, or a statement is stale.

## Summary

| # | Sev | Finding |
| --- | --- | --- |
| H1-H4 | | What holds: the scroll and grid, the map, the oracle, the method |
| P1 | S2 | "Objects found" is half the player; the other objects are found 71.2% of the time, and whole kinds not at all |
| P2 | S2 | Identities switch on 2-3% of pictures in real play; nothing measures an object's whole life |
| P3 | S2 | The organ is scored with hindsight over each group; it has no online mode and no memory between recordings |
| P4 | S2 | The organ gives an object no kind, which the world model's tokens and W8 need |
| P5 | S2 | Random play reaches a median of 352 pixels into a level; "all 32 levels" are their first screens |
| P6 | S1 | W3's bar can't be met: the organ doesn't have the player on 99% of pictures |
| P7 | S1 | W4's feasibility row is wrong: the player's next motion isn't a function of one picture and the action |
| P8 | S2 | The reference planner can't be scored on the organ's output: the organ is far too slow inside a search |
| P9 | S2 | Tile classes and looks are exact colours, so nothing learned about a tile carries to another palette |
| P10 | S2 | The riskiest stages come last, nothing runs end to end, and "complete" is not defined |
| P11 | S3 | W2.5 left the order without a note; thirteen constants were set on SMB's recordings |

## 1. What holds

- **H1. The scroll and the tile grid are exact** (W2.1′): every core shift, position and grid phase of
  361,169 pictures, against the scroll the game writes.
- **H2. The landscape map is exact up to tiles drawn alike** (W2.2′): no cell on its tile with another
  drawing among 268.5M; 90 wrong fills of 3.96M; its one refuted claim is two frames of a bumped block.
- **H3. The oracle is strong.** Drawing each picture again from the PPU's memory and requiring it to
  equal the console's gives every visible pixel's owner exactly; it differed on 3 of 240,109 test
  pictures.
- **H4. The method is sound.** Claims and bars registered before each run; fresh recordings for
  W2.3′'s test; refutations recorded as refutations, with their kinds; changes ablated one at a time;
  play kept as inputs, so any later organ can be run on old play.

## 2. Problems

### P1 (S2). "Objects found" is half the player

**Where.** W2.3′'s C2 and C3, and "the organ W8 and W3 build on ... the player found 98.6% (machine)
and 92.4% (human), identities kept 98.5%, 94.6% of what it tracks real".

**Evidence** (the test's tracked outcomes, bumped blocks left out as the claims do):

| | All objects | The player | Everything else |
| --- | --- | --- | --- |
| All groups | 405,264 of 481,727 (84.1%) | 229,767 of 235,309 (97.6%) | 175,497 of 246,418 (**71.2%**) |
| Machine play | 86.3% | 98.6% | 127,539 of 176,243 (72.4%) |
| The owner's play | 76.3% | 92.4% | 47,958 of 70,175 (68.3%) |

By kind (the game's slot ids; the plan names those it could):

| Kind | Found | Of |
| --- | --- | --- |
| Koopa (0x00) | 86.6% | 39,700 |
| Goomba (0x06) | 81.1% | 65,127 |
| The power-up (0x2E) | 62.6% | 3,807 |
| Kind 0x28 | 54.9% | 1,025 |
| Piranha plant (0x0D) | 31.2% | 26,985 |
| The flag (0x30) | 26.7% | 7,670 |
| Fireballs | 4.7% | 745 |
| Fire bars (0x1B, 0x1D, 0x1F) | 15 in all | 5,510 |
| Kind 0x29 (7-4 only; not identified in the plan) | 0 | 8,512 |
| Kind 0x32 (not identified in the plan) | 0 | 2,032 |

**The claim.** The player is 49% of the object-pictures, so the headline is mostly the object that is
easiest to find. The objects a world model has to predict are found seven times in ten. Kinds that rest
in place while the screen moves (the flag on its pole, kinds 0x29 and 0x32) are taken into the landscape by
the vocabulary's rule and are never objects; the fire bars are split over cells the vocabulary took in. The plan's own reading of the
literature (its section 3) is that object models pay when the objects are complete and stable.

**On 1-1 the organ is better than its pooled figures.** In the policy's sampled 1-1 episodes of the
test set: the player 96.5%, Goombas 88.1%, the Koopa 93.3%, the flag 88.8%, the power-up 75.3%;
everything but the player 88.7% (32,703 of 36,878).

### P2 (S2). Identities switch often in real play, and an object's whole life is unmeasured

**Evidence.** C5 counts an identity kept from one picture to the next: 6,460 switches in 437,337
(1.48%). By group: random play 0.4% (it meets few objects); the policy's sampled 1-1 episodes 1,297 in
60,350 (2.15%, about 65 an episode); the owner's play 2,725 in 89,467 (3.05%). The switches are not
counted by kind.

**The claim.**
- A world model learns an object's motion from a run of pictures with one identity. Nothing reported
  says how long such runs are: how many identities an object has over its life, or what share of its
  life its main identity holds.
- W2.4 reads an appearance and a vanishing off the tracker's identities. Every switch is then a
  vanishing and an appearance that didn't happen. W2.4's sketched claims (E1-E5) test whether true
  events are found; none tests whether the organ's object events are real.
- 5.4% of tracked objects are no object at all (31,097 of 576,456).

### P3 (S2). The organ is scored with hindsight

**Where.** `scripts/organ_objects.py`, `check_group`; the registrations' "each group's band, shots,
vocabulary and looks are its own".

**Evidence.** For each group of recordings the scorer makes four passes over the same pictures: the
band from every pair; the shots, each shot's grid from all its pictures, and the vocabulary; the looks,
with that vocabulary; then detection and tracking, with those looks, scored. An object's first picture
is recognised with looks learned from its later ones. Nothing is carried from one group to another.

**The claim.** That is a fair way to label recordings for training. It is not the organ an agent can
use while it plays (W5 to W7), and its figures are not that organ's. A small group has little to learn
from (a level's random play), which is part of why the levels' figures range from 49% to 100%; a memory
kept across recordings would know every look the corpus has shown.

### P4 (S2). No kind

**Evidence.** A tracked object is an identity, a box, its pixels and its tracks (`objects.Tracked`); a
detection carries the key of the exact look that explained it, or none. Nothing groups the looks of
one thing (a Goomba's two steps, its flattened form) into a kind. The oracle's kinds are RAM's.

**The claim.** D4's tokens are "class, position, velocity, age, the self flag", W8 learns "each object
class's update", and "a Goomba is a Goomba on 1-2" is the reason given for an object-centric model. The
organ has no class to give.

### P5 (S2). The recordings cover the levels' first screens

**Evidence** (measured here: the furthest the player's position gets, in the core, in each level's
random play of the W1 corpus): a median of 352 pixels over the 32 levels, 145 at the least, 783 at the
most; none past 1,536. The policy's 1-1 episodes reach the flag at 3,161. In the test set, 1-3's group
holds the player and no other object.

**The claim.** "All 32 levels are in play" is true of their starts. Past the first screens the corpus
holds 1-1 (the policy's play) and what the owner's two sessions crossed (1-1 to 2-2 in the first).
The organ's figures for the other levels are for what stands at their starts, and a world model has
nothing to learn deeper levels from. The plan's babbling "from human play's states" (W3) is the right
idea and depends on play that goes deep.

### P6 (S1). W3's bar can't be met

**Where.** W3: "done when the self is RAM's player on at least 99% of frames, on held-out levels and
in every power-up state".

**Evidence.** The organ has the player on 97.6% of its pictures, 92.4% in the owner's play (P1). The
self can't be right where the player isn't among the objects.

### P7 (S1). W4's feasibility row is wrong

**Where.** Feasibility: "the next scene is a function of the scene and the action ... the game is
deterministic". D4's token holds one velocity.

**Evidence** (measured here on the policy's 1-1 play, 55,755 core transitions with the player on
screen). For each history of the player's last `k` pixel motions and pads, with the current pad, the
share of transitions whose next motion isn't that history's commonest:

| History | By frame | By decision (4 frames) |
| --- | --- | --- |
| 1 | 36.7% | 20.5% |
| 2 | 21.3% | 12.8% |
| 4 | 9.1% | 8.1% |
| 8 | 3.9% | 3.3% |
| 16 | 2.2% | 1.8% |

The landscape and the other objects are left out, so part of what remains is theirs (a wall, a
landing), and the figures are an upper bound on what the hidden state alone leaves open. They are over
histories seen more than once, a subset that shrinks as `k` grows.

**The claim.** The game is a function of its RAM, not of a picture. The player's speed has a
sub-pixel part, and a jump depends on how long the button has been held. One picture's motion leaves
over a third of the next motions open; several are needed, or a state the model carries. The same
holds for anything with a timer.

### P8 (S2). The reference planner can't be scored on the organ's output

**Where.** D12: "the same planner as D7, with the emulator ... in place of the learned model, scored on
the same organ output".

**Evidence.** W2.3′'s objects pass ran at 20.6 core pictures a second a worker with its oracle (12 to
13 on the policy's and the owner's play). A search steps thousands of frames a decision; the console
alone steps about 3,300 a second a core. With the organ in the loop the planner would run two orders
of magnitude slower.

### P9 (S2). Exact colours carry nothing across palettes

**Evidence.** A landscape class is the hash of a cell's 64 palette entries, joined to another only when
a cell is seen to change between them in place (a palette's cycle). A look's key packs its exact
colours. The underground's brick and the overworld's are different classes; so are a Goomba's looks in
two palettes.

**The claim.** What a model learns about a class (that it is solid) is learned again for every
palette. Held-out levels with another palette are then a test of something the plan didn't mean to
test.

### P10 (S2). The riskiest stages come last, and "complete" isn't defined

**Evidence.** The order was W2.4, W8, W3, W4, W5, W6, W7, W9. Whether a learned object model predicts
well enough to plan a jump, what planning costs on these machines, and whether the library's additions
(D9) train in reasonable time are first met at W4 and W6. Four rounds went to objects first. No stage
runs the whole chain, even crudely. The plan's question has four parts and its stages include a second
game, a learned organ and discovery; nothing says which of them the SMB work needs to be called done.

### P11 (S3). Smaller things

- **W2.5** (a second scroller's frames through the organ, unchanged) is in W2's table and in neither
  the order ("W2.1-W2.4, then W8") nor the handover.
- **Thirteen constants** in the organ were set on SMB's recordings over four rounds (`MAX_SHIFT` 32,
  `CUT` 0.5, `PIXEL_CUT` 0.9, `CELL` 8, the travel 8, `HOLD` 64, `RARER` 4, `SMALLEST` 16, the looks'
  least 2, `GATE` 16, `PATIENCE` 8, `RIGID` 2, `GAP` 2). "Game-agnostic" is tested by the seam (no game's
  terms in the code), not by a second game.
- **The scorer's printout** still uses W2.3's bars (the handover says so).

## 3. Suggestions

1. **Say what "complete" is.** The 1-1 bar and the goal battery on the levels deep play covers. W8 to
   the machine-discovery plan (the main line doesn't depend on it). The learned organ and the second
   game after.
2. **Two sources of scenes.** One scene format; the organ makes it from pixels, the oracle from RAM
   and the PPU, holding only what a perfect organ would. Every layer above is built and tested on the
   oracle's scenes first, then on the organ's; the difference is the organ's cost. The claims stay on
   the organ's.
3. **The whole chain, thin, on 1-1 first.** The reference planner on the emulator before anything is
   learned: it says whether the control scheme can clear 1-1 at all, and it is the source of deep play.
   Then the model on the oracle's scenes, then planning with it, then the organ in.
4. **Close what the organ gives, not what it finds** (D15 stands): kinds from looks that share a
   track; an online mode with a memory from the corpus, scored beside the offline one; an object's
   whole life measured, and a claim that the organ's object events are real; the player and the rest
   reported apart, by kind; shape classes that ignore the palette, beside the exact ones.
5. **Correct the feasibility rows at each registration:** the self's bar over pictures where the scene
   has the player; the model given several steps of history, one step a decision; the reference
   planner's goals read from the oracle's scene; the organ's rate measured before anything plays
   through it.
