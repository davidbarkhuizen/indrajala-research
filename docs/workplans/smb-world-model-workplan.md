# Workplan: motion control from a world model, with Super Mario Bros as the simplest platform scroller

**Status (2026-11-10): revised after an assessment of the plan and its work so far
([review-2026-11-10-smb-world-model.md](../reviews/review-2026-11-10-smb-world-model.md)), at the owner's direction:
"take them all into account and revise the workplan - we need a plan that will work". The plan in force is
"The revision of 2026-11-10" below: what "complete" is (O3), two sources of scenes (O4, amending D1), W8 after
the SMB work (O5, superseding O2), D19-D30, and stages W10, W11, W2.4, W3, W4, W6, W5, W7 and W12, each with a
gate and a fallback. W10 (the scene and the oracle's source) is done. W11 (the reference planner) is run: its
level gate (L1) refuted at 82 of 100, its battery (G1-G3) holding; its fallback (L1′, a wider stick window) is
registered, its run under way.**

**Done before it, and standing:** W0 (the literature, 40 papers); W1 (frames and recordings, the owner's play
included); W2.1 (the screen layer: W2.1′, all six claims); W2.2 (the landscape map: W2.2′, one claim refuted by
one kind of event, listed); W2.3 (objects: W2.3′, objects found on machine play refuted at 86.3% against 87.5%,
the rest holding; closed under D15). W2.4 (events) is planned, amended by the revision, and not built.

**The order among the plans (the owner, 2026-11-10): "I would like to complete the SMB work first - then return
to the machine discovery research".** This plan runs first; [what-is-told-workplan.md](what-is-told-workplan.md)
follows it, and W8 is its stage 6.

This plan is its own, not a sub-plan of the NES plan's. It uses that plan's emulator, game layer and runners.
Its IDs are its own (D1-D30, O1-O5, W0-W12).

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

## The revision of 2026-11-10 (the plan in force)

**The owner, on the assessment** ([review-2026-11-10-smb-world-model.md](../reviews/review-2026-11-10-smb-world-model.md)):
"take them all into account and revise the workplan - we need a plan that will work". This section is the plan
from here. Everything done stands (W0-W2.3′, below, with their registrations and findings). Where this section
and an older one disagree, this one holds; the older ones say where they are superseded. "The review" is that
assessment, and P1-P11 are its findings.

**What "a plan that will work" means here.** No plan can promise that a learned model plans well enough. This
one is built so that it ends with an answer either way:
- the stage most likely to fail is met early, on the easiest ground, where a failure costs days;
- every layer is tested on exact scenes before it meets the organ's, so a failure is placed in the layer or in
  the organ, never in both;
- every stage has one gate, set before its data, and a named fallback; a gate refuted twice ends the stage with
  its failure placed, and the plan says what follows;
- no bar is set that the layer below can't reach.

### What the assessment changed, in brief

| the review found | the plan now |
|---|---|
| objects that aren't the player are found 71% of the time, whole kinds not at all (P1) | every layer above the organ runs on two sources of scenes, the oracle's exact one first (O4); the organ's cost is measured per layer, not assumed away |
| identities switch on 2-3% of pictures in play; an object's life is unmeasured (P2) | W2.4 measures lives and claims the organ's object events real; the agent's scene is its model's prediction corrected by the organ (D29) |
| the organ is scored with hindsight, per recording (P3) | an online mode with a memory from the corpus, scored beside the offline one (D28) |
| objects have no kind (P4) | kinds from looks that share a track (D28) |
| the recordings cover the levels' first screens (P5) | the reference planner comes first and plays the levels through; its play and babbling from it are the corpus (D27) |
| W3's bar can't be met (P6) | the bar is over the decisions where the scene holds the player; the scene's player rate is reported beside it |
| the next scene isn't a function of one picture (P7) | the model steps once a decision and reads each object's last `k` boxes, `k` measured before the model is built (D22) |
| the reference planner can't be scored through the organ (P8) | its goals are read from RAM inside the search (D20) |
| exact colours carry nothing across palettes (P9) | shape classes, the palette apart (D28) |
| the riskiest stages last, nothing end to end, "complete" undefined (P10) | "complete" defined (O3); the order by risk (D21); gates and fallbacks (D30) |
| W2.5 unrecorded; constants set on SMB (P11) | W2.5 and W9 after completion, recorded; the constants listed for the second game's check |

### The owner's calls (2026-11-10; recorded from "take them all into account")

- **O3. What "complete" is.**
  - (a) *Chosen.* **The SMB work is complete when this table is filled,** each cell a registered result:

    | | on the oracle's scenes | on the organ's scenes |
    |---|---|---|
    | the self (W3) | | |
    | the world model, held-out play (W4) | | |
    | the goal battery (W6) | | |
    | 1-1 under sticky actions (W7) | | |

    **The full aim** is the right-hand column's last cell at the NES plan's bar: greedy play, at least 90 of
    100 sticky attempts on 1-1, confirmed on fresh seeds, from pixels alone, with the frames it took set
    against the conv policy's 8.5M decisions. A cell that falls short is still a result, with its failure
    placed (D30). W8, the learned organ (W9) and the second scroller (W2.5) are not part of it.
    - Pros: one level and one battery, reachable on these machines; the plan's question answered in all four
      parts; the organ's cost stated, not hidden.
    - Cons: one level's bar; held-out levels only inside the battery and the model's test.
  - (b) The first draft's whole list (W2.4 to W9, a second game, discovery).
    - Cons: no end; three research problems beyond the question.
  - (c) The oracle's column alone.
    - Cons: no vision: the owner's picture dropped.
- **O4. Two sources of scenes (amends D1).**
  - (a) *Chosen.* **One scene format, made two ways:** by the organ from pixels alone, and by the oracle from
    RAM and the PPU, holding only what a perfect organ would give (D20). Each layer above is built and tested
    on the oracle's scenes first, then on the organ's. Every result is reported for both. **The plan's claims
    about seeing are the organ's column;** D1 holds for that column unchanged.
    - Pros: the owner's reason for an algorithmic organ ("to remove it as a source of variation / failure")
      met where the organ couldn't meet it; a layer's failure and the organ's told apart; the agent's work no
      longer waits on rounds of the organ.
    - Cons: every stage runs twice; the oracle's column is not vision and is never reported as it.
  - (b) D1 as it was: pixels only, everywhere.
    - Cons: each layer's failures tangled with the organ's (71% of the other objects found; four rounds so far).
  - (c) The oracle's scenes only.
    - Cons: as O3 (c).
- **O5. W8 after the SMB work (supersedes O2).** W8 is machine discovery; the main line never depended on it
  ("the main line builds (d) plain"). It is stage 6 of [what-is-told-workplan.md](what-is-told-workplan.md),
  with the arms that plan lists.

### The shape of it

```
                    ┌─ the organ (pixels only) ──────────────┐
   pictures ────────┤                                        ├──▶ scene: landscape cells · objects (identity,
   RAM, the PPU ────┴─ the oracle (what a perfect organ      ┘         kind, box) · events        (D19)
   (test only)         would give; nothing hidden)   (D20)
                                                                    │
        the self  ◀── which object do my actions move?              │  each layer: on the oracle's
        the model ◀── each object's next box, from its last k       │  scenes first, then the organ's
        the planner ◀── sampled action sequences, rolled in the     │
                        model; first on the emulator itself         │
        play ──▶ goals reached, the model retrained on what play gathers
        the level ──▶ the same planner on the level's reward
```

### Decisions (under the owner's delegation; options with pros and cons)

- **D19. The scene.**
  - (a) *Chosen.* **A scene a decision, in the shot's coordinates:** the landscape's cells in view (each its
    shape class, its palette and whether it is seen, filled or unknown); the objects (identity, kind, box);
    the events since the last scene (landscape: cells, classes before and after, lasting or transient;
    objects: appeared, vanished, in view or at the edge). **Nothing a camera couldn't give:** no speeds, no
    sub-pixels, no timers. In indrajala-rl, game-agnostic (`indrajala_rl/scene.py`).
    - Pros: one contract for both sources and every layer; identities and kinds kept as structure (our
      factored rule); what the model may read is fixed in one place.
    - Cons: a format to keep; the organ's internals must be mapped onto it.
  - (b) Planes, as the NES plan's observation.
    - Cons: identities lost; a flat picture of what the organ gives as objects.
  - (c) The organ's own structures.
    - Cons: the oracle would have to imitate the organ's internals.
- **D20. The oracle's scene.**
  - (a) *Chosen.* **Objects** from W2.3's oracle: each object's visible pixels' box from the picture drawn again
    from the PPU's memory, its kind RAM's slot id, its identity its slot's life. **The landscape** from the
    background the PPU draws under the sprites, through the organ's own cells and classes. **Events** from RAM
    (the block buffer's changes; slots set and cleared). **Inside the reference planner's search,** where
    thousands of frames are stepped a decision, a light form from RAM alone (the game layer's slots and block
    buffer): the search's goal and death tests need no picture.
    - Pros: the oracle is built and tested (W2.3's redraw, equal to the console's on all but 3 of 240,109
      pictures); it is exactly what a camera could see, so moving from it to the organ changes the scene's
      errors and nothing else.
    - Cons: the PPU's memory costs a pixel console (about 370 frames a second through Python); the light form
      is a second, coarser oracle, used only where no scene is scored.
  - (b) RAM's slots everywhere (the NES plan's observation).
    - Pros: fast. Cons: 16-pixel boxes, not what is drawn; the organ's scenes would differ in kind, not only
      in error.
- **D21. The order: by risk.**
  - (a) *Chosen.* **W10** the scene and the oracle's source; **W11** the reference planner and deep play;
    **W2.4** the organ's events and what it gives, scored on deep play; then **W3, W4, W6, W5, W7**, each on
    the oracle's scenes and then on the organ's (**W12**).
    - Pros: W11 says in days, with nothing learned, whether this way of controlling can clear 1-1 at all, and
      it makes the corpus the rest needs; the model (the likeliest failure) is met next, on exact scenes; the
      organ's last round is scored where objects are, not on level starts.
    - Cons: W2.4, planned and next, moves two stages back.
  - (b) W2.4 first, as planned, then the agent.
    - Cons: the organ scored again on the levels' first screens (P5), and the first sight of the model a
      stage later.
  - (c) The first draft's order (W2.4, W8, W3 ...).
    - Cons: the review's P10.
- **D22. The model's step and what it reads.**
  - (a) *Chosen.* **One step a decision** (4 frames, the action held). Each object's token holds its kind, its
    last `k` boxes, whether it is the self, and the landscape's shape classes in a window around it. **`k` is
    measured before the model is built** (W4's function check: on the oracle's scenes, the share of
    transitions not determined by `k` steps of history, the landscape window and the nearest objects), and
    starts from 8: the review measured the player's next motion open in 20.5% of decisions from one step of
    history, 8.1% from four and 3.3% from eight, the landscape left out.
    - Pros: a quarter of the steps a rollout needs; the agent's own choice points; the hidden state (a
      sub-pixel speed, how long a button has been held) is recovered from what a camera sees.
    - Cons: what happens inside a decision is folded into its end.
  - (b) A step a frame.
    - Cons: four times the rollout; one frame of history leaves 37% of the player's motions open.
  - (c) A recurrent state a token, no history.
    - Pros: unbounded memory. Cons: harder to train and to read; the fallback if the function check says no
      `k` is enough.
- **D23. The model's first form (amends D4).**
  - (a) *Chosen.* **Existence first: one small network shared by every object,** reading the object's token
    (D22), the action if it is the self, and its `n` nearest objects' kinds and boxes relative to it. It gives
    the object's next box as two categorical choices (its horizontal and vertical motion in pixels), whether
    it vanishes, and its next kind. **One model, no ensemble.** Trained one step ahead on recorded scenes.
    D4's transformer over the whole set is the second form, built only on a diagnosed need (an interaction
    this form can't express); the ensemble only if play needs disagreement (D6).
    - Pros: nothing new in the library (dense layers on one-hot and numeric features); trains in minutes on a
      core; exact pixels and a likelihood from the categorical outputs; "a Goomba is a Goomba" by the shared
      weights and the kind.
    - Cons: interactions limited to `n` neighbours; rollouts not trained for (the fallback below).
  - (b) D4 (a) from the start (a transformer over the set, an ensemble of 5, rollout training).
    - Cons: library work and five times the training before anything is known to work.
  - (c) Rules searched for (DOORMAX's kind).
    - Pros: exact where the rules are crisp. Cons: a rule language to design; kept as the last fallback.
- **D24. How the model is judged.**
  - (a) *Chosen.* **By the control it gives:** W6's gate is the planner on the model against the same planner
    on the emulator. Reported beside it, per kind and on held-out play: next boxes exactly right; the error
    after `h` decisions of rollout against the copy baseline (every object keeps its motion); vanishings
    predicted.
    - Pros: the measure the plan's question asks for; a model can miss pixels that don't matter and still
      pass, or match pixels and plan badly, and the gate sees which.
    - Cons: the gate needs the planner built first (W11 does that).
  - (b) Rollouts within a pixel at stated rates (the first draft).
    - Cons: a bar on pixels with no known relation to control.
- **D25. The planner (amends D7).**
  - (a) *Chosen.* **One planner for the emulator and the model:** each decision, sample action sequences in
    held segments over a horizon, roll each in the model, score it (the goal's distance, the self's survival;
    at W7 the predicted reward), take the best one's first action, and plan again at the next decision. Its
    budget is model steps a decision, set at W11. **Distilling into a policy comes after the bar, not before:**
    the planner is the agent.
    - Pros: built and tuned once, on the emulator, before any model exists; sticky actions handled by
      planning again every decision.
    - Cons: seconds a decision; no policy until after.
  - (b) Distil first (the first draft's D7).
    - Cons: a second thing to train between the model and the first result.
- **D26. The level's first form (amends D8).**
  - (a) *Chosen.* **The same planner on the level's reward:** a small head predicts the game's reward from a
    scene's change, trained on play; the planner maximises it. The level's reward enters only here. D8's
    chooser over goals is the second form, on a diagnosed need (a level the planner's horizon can't cross).
    - Pros: nothing new but a reward head; 1-1 needs no goal beyond going on.
    - Cons: a level that needs a detour or a pipe is beyond it; those are D8's.
  - (b) D8 (a) from the start.
    - Cons: a second learner over goals before the simple form is tried.
- **D27. Deep play: the corpus from here.**
  - (a) *Chosen.* **The reference planner's episodes** on every level it clears, recorded as inputs (D13);
    **babbling from states along them and along the owner's play** (restore, then sticky random actions);
    the W1 corpus and the test sets as they are. One level with deep play is held out at each registration.
    - Pros: play that crosses the levels, with the deaths and collisions babbling adds; minutes to record.
    - Cons: the planner's play is skilled play, so babbling carries the variety; restore used for data, as D6
      allows in play.
  - (b) More human play.
    - Pros: natural variety. Cons: the owner's time; welcome, never waited for.
- **D28. What the organ gives (in W2.4; D15 stands: no further round on finding objects).**
  - (a) *Chosen.* Beside W2.4's events as planned:
    - **kinds:** looks that follow one another on one identity, in enough tracks, are one kind (the bar on
      their purity against RAM's kinds from the probe);
    - **shape classes:** a cell's or a look's pattern with its colours numbered by first appearance, the
      palette apart; the exact classes stay, for the foreground;
    - **an online mode:** the band, vocabulary, kinds and looks from a memory made on the corpus, each picture
      read once, in order; scored beside the offline organ on the same pictures;
    - **an object's life:** for each of the oracle's objects, how many identities held it and the share its
      main one held; for each identity, how many objects;
    - **object events real:** the organ's appearances and vanishings in view matched by the oracle's, the
      others classed (a switch, a split, at the edge);
    - **reports:** the player and the rest apart, by kind, as the headline.
    - Pros: what the layers above need from the organ, in one registered round; the online organ is the one an
      agent can use.
    - Cons: W2.4 grows from two PRs to about five.
  - (b) W2.4 as planned, the rest when a layer asks.
    - Cons: each layer would stop at the organ in turn.
- **D29. The belief scene (the organ in).**
  - (a) *Chosen.* **On the organ's scenes the agent's scene is its model's prediction, corrected by what the
    organ finds:** an object the organ misses for a few decisions lives on where the model puts it; a
    detection near a predicted object takes its identity; one with no prediction is new.
    - Pros: misses, splits and switches (P1, P2) stop being holes in the scene; the standard remedy.
    - Cons: a wrong prediction can outlive the object; scored against the oracle's scene like the organ.
  - (b) The organ's scene as it comes.
    - Cons: an enemy missed for a decision isn't there for the planner.
- **D30. Gates and fallbacks.**
  - (a) *Chosen.* **Each stage: one probe, one registration, one run.** A gate refuted takes its named
    fallback once, registered apart. Refuted again, the stage ends with its failure placed, and:
    - on the oracle's scenes at W4 or W6: the model's form is the finding; the plan stops there and is put to
      the owner with what the fallbacks showed;
    - on the organ's scenes at any stage: the oracle's column goes on; the organ's misses that cost the stage
      are listed by kind, and whether the organ gets another round is the owner's.
    - Pros: no stage repeats without end; the plan always says what happens next.
    - Cons: a stage may end refuted with a remedy in sight.

### Stages

Each stage is one or more PRs, merged before the next; its claims and bars are registered here before its data,
from its first probe. The gates' figures below are where each registration starts from.

| # | What | Gate | Fallback |
|---|---|---|---|
| W10 | The scene (D19) and the oracle's source (D20) | the oracle's scene equals RAM's objects and block buffer on the W1 corpus | none: a tool |
| W11 | The reference planner on the emulator (D25), the goal battery, deep play (D27) | 1-1 cleared at least 90 of 100 under sticky actions; each battery goal reached at a stated rate; its budget in frames a decision | a wider search (more sequences, a beam with states merged); nothing learned is at stake |
| W2.4 | The organ's events and what it gives (D28), scored on deep play, offline and online | E1-E5 as sketched, E6 (object events real), kinds' purity, lives, the online organ within a stated margin of the offline | none: one round (D15's rule) |
| W3 | The self | the self is RAM's player on at least 99% of the decisions where the scene holds the player; the counterfactual by restore agrees on a sample | a longer window of decisions |
| W4 | The world model (D22-D24): the function check, then the model | better than the copy baseline on held-out play, per kind; its gate proper is W6's | more history; rollout training; D4's transformer; D22's recurrent state; D23's rules |
| W6 | Control: the planner on the model, the battery | each battery goal reached at no less than a stated share of the reference planner's rate (from 80%), under sticky actions, without restore | W4's fallbacks, chosen by where the rollouts break |
| W5 | Play: the archive, goals from it, the model retrained | the model's held-out error falls with play, and coverage rises against babbling at equal frames | recorded as refuted; W7 doesn't wait on it |
| W7 | The level (D26) | 1-1: at least 90 of 100 greedy, sticky, confirmed on fresh seeds; frames against the conv policy's | D8's chooser over goals |
| W12 | Each of W3-W7 on the organ's scenes, with the belief scene (D29) | each stage's gate, at a stated margin under the oracle's column | D30 |

- **W10. The scene.** `scene.py` (the format; nothing in it names a game), the organ's adapter, the oracle's
  in the game layer. Done when the oracle's scenes of the W1 corpus hold RAM's objects and block events (its own
  test), and the organ's scenes score W2.3′'s figures again through the scene (a check that the adapter changed
  nothing).
- **W11. The reference planner.**
  - The planner over a model's interface (`step`, the goal and survival tests), with the emulator behind it.
  - **The battery, first form:** land on a chosen cell (a platform, a gap's far side, a stair); hit a chosen
    block from below; stomp a chosen enemy. Goals are drawn from the scene: cells and objects. Entering a pipe
    is left for after: a pipe is a cut the model can't roll through.
  - **The level:** the same planner on the game's reward, 1-1 first, then every level, recording what it
    clears.
  - Done when the gate is read and the deep play is recorded with its manifest.
  - **Before it:** the console's frames a second a core, headless, on `stone` and `klip` (the development
    reading is 3,300), and from it the budget a decision can afford.
- **W2.4. The organ's events and what it gives.** W2.4's plan below, with D28's parts and two changes: the test
  data is D17's fresh recordings and a held-out part of the deep play; every claim is read for the offline
  organ and the online one.
- **W3. The self.** Babbling as planned. The inverse model: per object, its boxes over the last decisions to
  the action taken. The self is the identity it predicts best over a window. Both sources.
- **W4. The world model.**
  - **The function check first** (a tool: `scene_function`): on the oracle's scenes, for `k` from 1 to 16, the
    share of an object's transitions not determined by its token and neighbours. It fixes `k`, the window and
    `n`, or says no finite history is enough (then D22 (c)).
  - Then D23's model, trained on the corpus less the held-out level; D24's measures.
- **W6. Control.** The planner on the model; the battery under sticky actions, without restore, on the levels
  deep play covers, the held-out one apart.
- **W5. Play.** The archive (cells: the self's map cell and its power state), return by restore, goals from
  the frontier, the planner on the model pursuing them, the model retrained on what play gathers. Disagreement
  and learning progress only on D6's stated stalls.
- **W7. The level.** D26's reward head and the planner; 100 sticky attempts on 1-1, then a second 100 on fresh
  seeds; all frames counted (babbling, play, the level's own).
- **W12. The organ in.** After each of W3 to W7 passes on the oracle's scenes, the same on the organ's: offline
  for W3 and W4 (the organ's scenes of the same recordings), online from W6 on (the organ's online mode and the
  belief scene). **Before W6 on the organ's scenes:** the online organ's pictures a second a core.

**After completion, not part of it:** W8 (O5); W9, the learned organ; W2.5, a second scroller through the
organ unchanged, which is also the check on the organ's thirteen constants (the review's P11); distilling the
planner into a policy (D7's second half); pipes in the battery.

### Feasibility (replaces the table further down)

| stage | the claim | why it can succeed | measured before it |
|---|---|---|---|
| W10 | the oracle's scene is what a camera could see, exactly | the redraw equals the console's picture on all but a few in 100,000; RAM names every slot | nothing new |
| W11 | sampled plans on the emulator clear 1-1 and reach the battery | a search on an exact model with restore; Baumgarten's precedent; planning again each decision absorbs sticky actions | frames a second a core; the budget a decision |
| W2.4 | the organ's events and kinds follow its tracks | the map is exact up to tiles drawn alike; on 1-1 the organ finds 88.7% of the other objects; what it can't see is classed | the probe on deep play |
| W3 | one object's motion answers the pad | only the player does; the bar is over decisions where the scene holds it | the scene's player rate, per source |
| W4 | an object's next box is a function of its last `k`, its kind, the landscape near it and its neighbours | the game is deterministic in its RAM; what a camera lacks is recovered from history (the review's P7: 3.3% open at 8 decisions before the landscape is counted) | the function check, on the oracle's scenes |
| W6 | the planner reaches goals in the model that it reaches on the emulator | W11 has reached them; the model is judged against that | W11's rates |
| W5 | play improves the model | the archive returns to the frontier exactly; babbling is the floor it must beat | babbling's coverage at equal frames |
| W7 | the planner on the predicted reward clears 1-1 | W11 has cleared it on the true reward | W11's clear rate |
| W12 | the same on the organ's scenes | on 1-1 the organ has the player on 96.5% of pictures and the other objects on 88.7%; the belief scene carries objects over misses | the online organ's rate; the organ's scenes against the oracle's on deep play |

**What can't be seen** stays a classed limit: an enemy before it comes into view bounds a rollout's horizon; a
kind the organ takes into the landscape (the flag at rest, the fire bars, kinds 0x29 and 0x32) is absent from
the organ's column on the levels that have it, and present in the oracle's, so its cost is read there.

### The size, roughly (each stage's probe replaces it)

- **W10:** two to three PRs; no long run.
- **W11:** the planner and battery, about a week; 100 sticky attempts at about 6,000 frames a decision is
  about 20 core-hours, an evening on `stone` and `klip`.
- **W2.4:** five PRs and one run of about 75 minutes a set on `stone`, twice (offline, online).
- **W3:** days. **W4:** the check a day; the model trains in minutes to hours. **W6, W7:** as W11's runs, the
  model in place of the console.
- **W12:** each run again, with the organ in front (the objects pass ran at 12 to 21 pictures a second a
  worker with its oracle; the online rate is measured first).

### Machines

As D10: development and the organ's tests on `pyramidon`; runs on `stone` (7 workers) and `klip` (under its
thermal guard); `jebel` out until the owner says.

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

*The first draft's. Since 2026-11-10 the shape of the plan is the revision's ("The shape of it", above): each
layer runs on the oracle's scenes first, then the organ's (O4), and "no layer sees RAM" is the organ's column's
rule.*

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

*Superseded 2026-11-10 by O5 (the revision): W8 follows the SMB work, as stage 6 of
[what-is-told-workplan.md](what-is-told-workplan.md). The text below is the first draft's.*

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

*Amended 2026-11-10 by O4 (the revision): D1 holds for the organ's column; every layer above also runs on the
oracle's scenes.*

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

*Amended 2026-11-10 (the revision): D4's first form is D23's, its step and tokens D22's, its judging D24's; D7 is
amended by D25, D8 by D26, D12 by D20 and D21.*

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
- **D14. What W2.3′ is tested on.** (New from W2.3's diagnosis, 2026-11-09: every group of the W1 corpus has
  now been looked at, so none is unseen.)
  - (a) *Chosen.* **New recordings for the test, by W1's recipe:** random play with new seeds on every level,
    more of the policy's sampled episodes on 1-1, and the owner's new play when there is some. The W1 corpus
    becomes the probe's. Recorded and listed before the registration, and not opened until the run.
    - Pros: an honest unseen test, at W1's cost (inputs, minutes to record); every kind the corpus has is in
      the probe, so the bars are set where the organ will be tested.
    - Cons: random play reaches mostly the levels' first screens; the new owner play depends on the owner's time.
  - (b) Split the corpus: probe on some groups, test on the rest.
    - Pros: no new recordings.
    - Cons: the diagnosis looked at the test groups' misses, so they aren't unseen.
  - (c) Only the owner's new play.
    - Pros: the richest play.
    - Cons: waits on the owner; one player's style.
- **D15. The organ's last round on objects.** (New 2026-11-10, after W2.3′'s first probe: the four changes bought
  2.4 points of objects found over the corpus, and what is left is mostly overlap, objects behind the background
  and cells known only from an object's block. The owner asked when to accept the organ and move on.)
  - (a) *Chosen (the owner, 2026-11-10: "go with (a)").* **W2.3′'s registered test is the last round on objects,
    whatever it shows.** Its result is recorded, held or refuted, and W2.4 (events) follows. The misses left go
    to the open threads, not to planned work.
    - Pros: an honest unseen number for the organ that W8 and W3 build on, in hours; what they need (the player,
      identities kept, every miss named) is there; their errors are measured against RAM, so later stages know
      where the organ is wrong.
    - Cons: objects found may be recorded as refuted.
  - (b) Rounds until objects found reaches its bar.
    - Pros: a cleaner record.
    - Cons: overlap and objects behind the background are research problems of their own; each round needs a new
      unseen test set; days, not hours.
  - (c) Stop now, without the test.
    - Pros: saves about 3 hours.
    - Cons: no unseen measure, and the recordings made for it unused.

- **D16. What a landscape event is, in the organ.** (New 2026-11-10, W2.4's plan.)
  - (a) *Chosen.* **A change of a cell's class from the class it last showed, grouped and timed, lasting or
    transient.** Cells whose shown class changes in the same picture (or within one), 8-connected on the grid,
    are one event: its cells, the classes before and after, its first picture, and whether the cells were hidden
    when it happened (seen changed only when uncovered). It **lasts** when the new classes stay 64 pictures
    (`HOLD`, the map's own test of a change that is the landscape's) or until they leave view, and is
    **transient** when the earlier classes come back sooner (a brick bumped and back; an object at rest).
    - Pros: one rule for every game, from the map the organ already keeps; a used block, a broken brick, a
      coin taken and a bump all fall out of it, distinguished by lasting or not and by their classes; the
      map's own change test (`HOLD`) decides lasting, so no new constant.
    - Cons: objects at rest that the vocabulary took in make transient events too; they are classed by the
      oracle (an object's sprite over the cell), not hidden by the organ.
  - (b) Only changes between classes of a kind (the map's `RARER` test failed: not an object's block).
    - Pros: fewer transient events from objects.
    - Cons: a used block or a broken brick's sky may be 4 times rarer than the block before it (the data
      decides commonness), and would be dropped; a rule tuned to SMB's palette of blocks.
  - (c) Events as RAM-shaped records (metatile cells, 16 pixels).
    - Pros: matches the oracle one to one.
    - Cons: the organ doesn't know the metatile; game knowledge in the organ, against D1.
- **D17. What W2.4 is tested on.** (New 2026-11-10.)
  - (a) *Chosen.* **Fresh recordings by W1's recipe again** (random play on all 32 levels, seed 2000; the
    policy's sampled 1-1, seed 2000; the owner's new play if there is some), recorded and listed before the
    registration. The probe is the W1 corpus; W2.3′'s test set becomes a second probe for events, since its
    objects results have been looked at.
    - Pros: unseen data for every claim, at minutes of recording; the same recipe, so the bars travel.
    - Cons: the test needs the organ's whole pipeline again (about 75 minutes on `stone`).
  - (b) W2.3′'s test set.
    - Pros: no recording.
    - Cons: its objects results are known, and W2.4's object events are built on those tracks.
- **D18. Where events live.** (New 2026-11-10.)
  - (a) *Chosen.* **The organ's events in a module of their own** (`indrajala_rl/organ/events.py`, game-agnostic,
    fed each picture's map and tracked objects), **the oracle in the game layer** (`smb.buffer_events`, already
    merged, and the objects' slots), **the scoring in `organ_objects.py`'s objects pass** (the same replay,
    pictures and tracks, so W2.3′'s claims come out of the same run unchanged).
    - Pros: one replay gives objects and events; W2.3′'s numbers are a check that events changed nothing; W8 reads
      events from the same organ output.
    - Cons: the scorer grows; its events part is its own section and tests.
  - (b) A separate `organ_events.py`.
    - Pros: smaller scripts.
    - Cons: a second replay of the corpus (an hour on `stone`), or the organ's pipeline factored out first.

## The owner's calls

*O3-O5 (2026-11-10) are in the revision above; O5 supersedes O2.*

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

**The stages in force are the revision's (above).** W0-W2.3′ below are done and stand. W2.4's plan is amended
where it says so. W3-W9 below are the first draft's, kept for the record: the revision's stages replace them.

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

#### W2.1′'s registration (2026-11-08, before its run)

The follow-up to W2.1's first run (findings below). It makes two changes, each touching one claim's mechanism:
- **The band's ties** go to the widest scrolling band, as documented. This is R1's mechanism; the first run's
  code took the narrowest.
- **A cut needs its pixels too.** A pair whose best shift fits under half the columns is a cut only if that
  shift also fits under 90% of the overlapping pixels. Otherwise it is that shift. This is R6's mechanism.
  - The 90% comes from the probe of the owner's play and 3-4's random play. The 9 false cuts fit 95.4-98.7%
    of their pixels; the 1,104 pairs classed as shifts with under 70% of their columns fit at least 95.5%.
  - Every true scene change in that probe passed through a picture of one colour.

**Unchanged:** R1-R6, their tests and refutations, the data (all 35 groups), and the run on `stone` (indrajala-rl
#39's commit).

**Reported, not claimed:** the shifts kept by their pixels, with their fits. A kept shift that is wrong would
refute R2 or R3.

#### W2.2's registration (2026-11-08, before the corpus run)

**The organ** (indrajala-rl's `indrajala_rl/organ/landscape.py`, game-agnostic under the seam test), on W2.1′'s
shots:
- **Cells:** each picture's whole 8×8 cells on its shot's grid, in the shot's coordinates, each its exact block
  (a hash of its 64 pixels).
- **The vocabulary** (the landscape's blocks): a block that stays at its cell while the screen travels 8 pixels
  or more.
  - One pair of pictures isn't enough. The probe found a walker at half a pixel a frame keeping its place in the
    world between some pairs while the screen moved: 38,867 cells of 1-2's random play under a sprite were taken
    for landscape, and 929 after the change.
  - 16 pixels of travel took 81 classes of objects for landscape where 8 took 101, and doubled the wrong fills.
- **Cycles:** a change at a cell between consecutive pictures is a recolouring when neither block is one colour
  and one's colours are a function of the other's. A palette's cycle can give two of a tile's values one colour
  at a step, so an equal shape is too strict: the probe's question blocks stayed 3 classes under it. Two
  vocabulary blocks joined by a recolouring are one class.
  - A change to or from one colour is never a recolouring: a broken or bumped block leaves its cell blank.
- **The map:** per shot, each cell's class, from the last picture that showed it a vocabulary block. A cell
  showing any other block is hidden: filled from earlier pictures, or unknown.

**The oracle** (indrajala-rl's `scripts/organ_map.py`, in the core, with RAM one frame before each picture as
W2.1's). Under each cell it takes RAM's metatile quadrant (`MetatileBuffer`) and its drawing from the ROM: the
tile's CHR pattern (pattern table `$1000`) and the palette, by the metatile tables at `$8B08`. Each cell is
accounted for as one of:
- **its tile:** the block's colours are a function of the tile's pattern values, and its value-0 pixels are the
  picture's backdrop colour (the PPU draws every background's value 0 in it). A block of one colour is its tile
  only if the pattern is of one value: while a block bounces as a sprite, the game draws its cell blank and RAM
  still holds the block (the probe's 56 conflicts).
- **in a sprite's box:** not its tile, and a sprite in RAM's sprite page (`$0200`) overlaps the cell.
- **scenery:** neither.

**What the probe found about the oracle:**
- **RAM's buffer holds the terrain only.** Clouds, hills, bushes and castles are drawn where it holds the sky
  (checked cell by cell at 1-1's start).
- **One 8×8 block can be drawn by two metatiles,** for example a pipe's inside and a bush's, or 1-1's castle and a brick.
  Pixels can't tell those apart, so the claims count such cells as **alike** (the class's block is a colouring
  of both patterns), an oracle limit and not an error.

**The data:** the whole W1 corpus as W2.1's (35 groups, 375,836 frames), each group's band, shots and vocabulary
its own, classes joined across groups. The run is on `stone`.

**The first probe** used the policy's greedy 1-1 episodes and random play on 1-2 (32.7M cells in the core).
Those two groups are reported apart from the 33 that no probe saw.

| claim | the test (in the core, every whole cell) | refuted by | the probe |
|---|---|---|---|
| M1. A class is one drawing | each cell seen on its tile has its class's drawing (its most frequent), or one its block is also a colouring of (alike) | one cell | 0 (62,530 alike) |
| M2. One class a drawing in a shot | in each shot, the cells seen on their tile with one drawing have one class | one | 0 |
| M3. Fills right | each filled cell's class has the drawing RAM holds there, where RAM's drawing is unchanged since the cell was last seen | more than 0.01% of fills | 4 of 533,269 |
| M4. Coverage | cells on their tile left unknown | more than 0.01% of cells on their tile | 0 |
| M5. Objects as landscape | the cells seen in classes seen mostly in a sprite's box (objects the vocabulary took in) | more than 0.5% of seen cells | 19,701 (0.06%) |

**Reported, not claimed:**
- fills where RAM's drawing changed under a sprite since the cell was last seen (a block bumped or broken under
  the player; W2.4's events): 1,770 in the probe;
- scenery cells by class;
- each drawing's number of classes;
- every exception with an example (file, frame, cell).

**Feasibility:** the NES draws the background from 8×8 tiles on the grid W2.1′ finds exactly, so a cell not
under a sprite shows its tile, coloured, or scenery, and a landscape block keeps its place while the screen
moves. What a sprite hides is filled only if seen before; the rest is counted (M4 counts only cells on their
tile, which nothing hides).

#### W2.2′'s registration (2026-11-08, before its run)

The follow-up to W2.2's registered run (findings below), which refuted M2 and M3. It makes two changes, each
touching one claim's mechanism:
- **The joins (M2's mechanism):** a recolouring joins two blocks when the one with more colours is the
  vocabulary's (either one, when they have as many colours); W2.2's needed both.
  - The run's conflicts were palette-3 blocks whose cycle passes through a step where two values share a
    colour. While the screen is still, that colouring never joins the vocabulary, so the chain between the
    colourings on either side broke.
  - A sprite over a block makes the finer block, which isn't the vocabulary's, so it joins nothing.
- **M3's test:** a filled cell whose class's drawing differs from RAM's is wrong only when not alike: the class's
  block is a colouring of only one of the two patterns, the rule M1 already applies to seen cells. W2.2's test
  left it out, and 4,332 of its 4,409 wrong fills were in pairs that M1 counts alike.

**Unchanged:** M1-M5, their bars, the data (all 35 groups), the travel (8), and the run on `stone` (indrajala-rl
#41's commit).

**Reported apart:**
- the groups W2.2's probe saw (greedy 1-1, random 1-2);
- the groups W2.2′'s probe saw (random 6-3 and 7-3: all five claims held, 0 conflicts, 0 wrong fills);
- the rest.

#### W2.3's registration (2026-11-09, before the corpus run)

**The organ** (indrajala-rl's `indrajala_rl/organ/objects.py`, game-agnostic; the map's changes in `landscape.py`):
- **The foreground:** the pixels of each whole cell that differ from the landscape there.
  - A hidden cell (filled) is compared with the colouring of its class that agrees with most of its pixels.
  - A cell not yet seen is compared with the landscape block that agrees with most of its pixels, among the
    classes the shot has shown so far.
  - **A changed cell** (new in W2.3): a cell that showed one class and now shows one at least 4 times rarer
    (by the vocabulary's cell-pictures) is compared with the class it showed before, for 64 pictures or until it
    shows that again. The landscape doesn't move, so such a change is an object whose block the vocabulary also
    took in (it stood still somewhere while the screen moved: a stomped Goomba, the flag) or an event.
- **Pieces:** the foreground's 8-connected components.
- **Appearances:** the exact looks of clean pieces (every cell under them filled, away from the area's edge),
  kept when seen twice or more, of 16 pixels or more and more than one colour, the most seen first.
- **Detection:** a clean piece is an object as it is, unless a look seen more often than its own contains it
  all. Any other piece is explained by the exact looks drawn in it (at the area's left and right edges, by
  looks cut there whose pixels inside are drawn exactly); the foreground they leave stays where its cells have
  a reference.
- **Tracking:** each detection is matched to the live track nearest its prediction (its box moved by its last
  motion), nearest pairs first, within 16 pixels of the centres, in the shot's coordinates; a track lives 8
  pictures unseen. **Objects:** tracks that moved alike (or rested together) for 2 pictures, boxes within 2
  pixels, are one object, unless both are known looks (two Goombas walking in step); the parts of one thing
  (a score's digits, a flattened Goomba's two rows) join. An object's identity is its oldest track's.

**The oracle** (indrajala-rl's `scripts/organ_objects.py`, test-only, D1; in the core, RAM one frame before each
picture):
- **The picture drawn again** from the PPU's memory (`ppu_picture.draw`: name tables, attributes, palette, OAM,
  each line's scroll from RAM), which must equal the console's picture; where it does, its account of each
  pixel (background, which sprite drew it, which sprite lost to the background) is the console's.
- **Each sprite's object** from RAM's sprite offsets (`SprDataOffset`), the active owner where ranges overlap.
  An object's sprites are split into groups whose boxes touch (a stomped enemy's body and its score).
- **Visible pixels:** an object's drawn pixels whose colour differs from the background's there. The truth box is
  their box, over the organ's whole cells.

**Tried and dropped in the probes (recorded so they aren't tried again blind):**
- holding a track at rest where its last pixels are still drawn: false pieces of landscape colours lived on
  (tracked objects of no object 3,216 → 1,539 without it, Goombas matched 4,160 → 4,112);
- cutting a clean piece by two or more looks covering it exactly: no effect (+1 Goomba, +1 player of 9,000):
  touching objects overlap pixel for pixel;
- an earlier class kept whenever the new one is rarer at all: the same detections as at 4 times (every such change
  in the probe was by more).

**The data:** the whole W1 corpus (35 groups), each group's band, shots, vocabulary and looks its own. The run is
on `stone`, at indrajala-rl #42's merged commit.

**The first probe** used the policy's greedy 1-1 episodes and random play on 1-2 (40,460 core pictures, 84,315
objects); those groups are reported apart from the 33 no probe saw.

| claim | the test (in the core, over the organ's whole cells) | refuted by | the probe |
|---|---|---|---|
| B1. The redraw is the console's | core pictures drawn again differently (left out of B2-B5) | more than 0.1% of core pictures | 6 (0.015%): the status bar's split written inside line 32, which a redraw of one scroll per line can't express |
| B2. Objects found | the oracle's objects (not bumped blocks: W2.4's events) matched by one tracked object, its box within a pixel of the visible pixels' | under 89% | 90.3% (76,120 of 84,315) |
| B3. Objects real | tracked objects holding some object's visible pixels | under 88% | 89.4% (89,484 of 100,072) |
| B4. Identities kept | an object held by one identity on consecutive pictures (by most of its largest group's visible pixels) keeps it | under 97.5% | 98.1% (78,573 kept, 1,503 switches) |
| B5. Every miss classed | misses of B2 with no class (other) | more than 2% of objects | 1.2% (1,030) |

**The miss classes** (the first that applies): a bumped block (an event); at the edge (the object's pixels
reach the area's edge, or it draws beyond it); behind the background (some of its sprites' pixels lost to the
background's priority); overlap (a piece holds another object's pixels too); over a cell not yet seen; over a cell
showing a landscape block (the vocabulary took the object in: at rest); other.

**The probe's misses by class** (B2's 8,195): overlap 5,009; other 1,030; over a cell showing a landscape block
977; at the edge 577; over a cell not yet seen 511; behind the background 91. By kind: player 97.6% (39,340 of
40,326; overlap 903), Goombas 82.8% (31,051 of 37,483; overlap 4,058), scores and coins 95.5%, the flag 86.1%,
the power-up (id 0x2E) 35.7% (254 of 712; 325 "other": its box differs, not yet examined; it rises out of its block),
Koopas (id 0x00) 97.6%. Bumped blocks (left out of B2): 112 of 1,076. Tracked objects of no object (B3's 10,588): over a
changed cell 6,686, over a cell not yet seen 3,284, other 466, beside a bumped block 152.

**Reported, not claimed:** per kind (player, each enemy id, scores and coins, blocks), the outcomes by class;
the foreground's pixels against the visible pixels, by cell state; tracked objects of no object by cause (over a
changed cell, over a cell not yet seen, beside a bumped block, other); the drawn-differently pictures listed.

**Why the bars are under the plan's 99%:** the probe falls short of it on overlaps (two objects in one piece)
and on objects the vocabulary took in. Both are listed miss classes in W2.3's done-when; the bars are the
probe's, less a margin, so that the 33 unseen groups test the organ, not the probe's luck.

**Feasibility:** the NES draws each picture from its PPU memory alone, which the oracle reads, and the redraw
equals the console's on all but 6 of the probe's 40,460 pictures (the split inside line 32), so each visible
pixel's owner is known exactly.
What no camera can see (a sprite pixel in the background's colour, a sprite behind the background) isn't in the
truth, and the truth box covers only the organ's whole cells (the partial columns at each edge, up to 7 pixels,
are outside both).

#### W2.3′'s registration (2026-11-10, before the test run)

**The organ:** W2.3's, with one change for each mechanism its diagnosis found (indrajala-rl #48, narrowed by
#49 from the first probe; merged at `bfd4ef2`):
- **A1, the earlier class under an object:** a cell with an earlier class (`Landscape.prior`) is compared with
  that class whether it shows another or an object hides it (W2.3: only while it showed another).
- **B, stray pixels:** of a piece's foreground that the looks explaining it leave, a bit under 16 pixels in cells
  with a known reference that touches one of those objects joins it (the first it touches).
- **C, the fuller look first:** in a piece that isn't clean, every look drawn there is found, and the one
  covering more of the piece is taken first (then the looks' order), none overlapping another.
- **D, aligned small pieces:** pieces no look explains, each under 16 pixels (too small to be a look), spanning
  the same rows side by side within 2 pixels, are one object before tracking (a score's digits: evenly spaced and
  alike, their tracks swap among them, so as tracks they never move alike).

**The oracle:** W2.3's, with one miss class more, A2's: **over a cell filled with an object's block** (after "over a
cell not yet seen", before "over a cell showing a landscape block"): a filled cell under the object's visible pixels
or its tracked object's pixels whose reference (its earlier class if it has one, else its class) isn't the class
of the background the PPU draws there (or that background is in no class). The organ can't tell such a cell from
landscape until the object leaves it.

**The data (D14):** **the probe** is the whole W1 corpus (35 groups, 361,169 core pictures; manifest sha256
`66165a3e…`). **The test** is new recordings by W1's recipe, recorded on `stone` 2026-11-10 and opened by nothing
before this run: random play on all 32 levels (4 episodes each, up to 1,000 decisions, seed 1000; W1's was 0),
the conv policy's sampled episodes on 1-1 (20, seed 1000; W1's 100), and the owner's play of 2026-11-10
(`nes-console`, 41,996 frames), 244 recordings and 251,019 frames, all replaying exactly (manifest sha256
`3d8a62ed…`, in indrajala-studies' gitignored `data/smb-world-model-test/`). Each group's band, shots,
vocabulary and looks are its own, as before. The run is on `stone` (7 workers), at `bfd4ef2`.

**Machine play and human play are claimed apart for objects found.** Over the probe, B2 is 88.8% over machine
play's 34 groups and 65.8% on the owner's session (overlaps, many objects at once, cells known only from an
object's block); pooled, it would measure the mix. The other claims are over all groups.

| claim | the test | refuted by | the probe |
|---|---|---|---|
| C1. The redraw is the console's | core pictures drawn again differently (left out of C2-C6) | more than 0.1% | 7 (0.002%) |
| C2. Objects found, machine play | B2's test, over the random and policy groups | under 87.5% | 88.8% (461,507 of 519,837) |
| C3. Objects found, human play | B2's test, over the owner's play | under 60% | 65.8% (79,007 of 120,151) |
| C4. Objects real | B3's test | under 94.5% | 96.1% (785,105 of 817,366) |
| C5. Identities kept | B4's test | under 98% | 98.9% (575,499 kept, 6,630 switches) |
| C6. Every miss classed | B2's misses of no class (other) over all objects | more than 2% | 1.2% (7,960) |

**The margins** are W2.3's, about 1.3 points under the probe for objects found and 1.5 for objects real; C3's is
wider (5.8), since it rests on one session of one player, and the probe's own random groups range from 56% to 100%
by level.

**The probe's misses by class.** Machine play's (58,330): overlap 16,789; behind the background 11,402; over a cell
showing a landscape block 9,246; at the edge 7,624; other 6,888; over a cell not yet seen 5,708; over a cell filled
with an object's block 673. The owner's session's (41,144): over a cell filled with an object's block 14,844; over a
cell showing a landscape block 11,981; overlap 7,888; at the edge 2,239; behind the background 2,078; other 1,072;
over a cell not yet seen 1,042. By kind in machine play: the player 98.7%, Goombas 83.5%, Koopas 85.4%; in the
owner's session: the player 93.5%, Goombas 71.8%, air bubbles 97.3%.

**Reported, not claimed:** as W2.3's, and the claims per group.

**Feasibility:** as W2.3's: the redraw equals the console's on all but 7 of the probe's 361,169 pictures.

#### W2.3′'s result (2026-11-10): C2 refuted by 1.2 points, C1 and C3-C6 hold; objects closed (D15)

The run: 34 groups, 240,109 core pictures, 5,449 s on `stone` (7 workers) at indrajala-rl `bfd4ef2`; result
`w2-3p.json` (sha256 `2299f2c1…`) with its log and score in indrajala-studies' gitignored
`data/smb-world-model/organ/`. Scored with `--score w2-3p.json --apart human` (the "probe" set is the owner's
session, the "unseen" set machine play), against the bars above.

| claim | the test | refuted by | result | |
|---|---|---|---|---|
| C1. The redraw is the console's | pictures drawn again differently | more than 0.1% | 3 of 240,109 (0.001%) | holds |
| C2. Objects found, machine play | 33 random and policy groups | under 87.5% | 325,121 of 376,725 (86.30%) | **refuted** |
| C3. Objects found, human play | the owner's session | under 60% | 80,143 of 105,002 (76.33%) | holds |
| C4. Objects real | all groups | under 94.5% | 545,359 of 576,456 (94.61%) | holds |
| C5. Identities kept | all groups | under 98% | 430,877 kept, 6,460 switches (98.52%) | holds |
| C6. Every miss classed | all groups | more than 2% | 9,038 of 481,727 (1.88%) | holds |

**What refuted C2:** the levels. Machine play's objects found range from 48.8% (random 7-4) to 99.97% by level;
four levels hold most of the shortfall: 7-4 (48.8%, 17,150 objects), 3-4 (68.7%), 4-1 (72.8%), 6-2 (77.1%,
43,310 objects, the largest random group). By kind: the player 98.6%, slot kind 0x06 81.6%, 0x00 89.0%, 0x0D
33.6% (rising out of pipes: behind the background), 0x12 72.4%. The probe's random groups were drawn with seed 0,
the test's with seed 1000, so its levels' mix differs; the bar was set from the probe's pooled 88.8%.

**Machine play's misses by class (51,604):** overlap 12,382; behind the background 11,869; over a cell showing a
landscape block 11,017; at the edge 7,293; other 6,925; over a cell filled with an object's block 1,109; over a
cell not yet seen 1,009. **The owner's session's (24,859):** over a cell showing a landscape block 7,715; overlap
6,331; behind the background 3,547; over a cell filled with an object's block 2,239; at the edge 2,153; other
2,113; over a cell not yet seen 761. The player there 92.4%.

**Human play rose most:** the session of 2026-11-10 scored 76.3% against the probe's session's 65.8%; its cells
filled with an object's block fell from 14,844 misses to 2,239 (A1 and A2's class at work, and a different
session).

**Closed under D15 (the last round on objects).** The organ W8 and W3 build on is `bfd4ef2`'s: the player found
98.6% (machine) and 92.4% (human), identities kept 98.5%, 94.6% of what it tracks real, and all but 1.9% of its
misses named. The misses left (overlap, behind the background, landscape-block cells, the edge) go to the open
threads; later stages measure their own errors against RAM, so they know where the organ is wrong.

#### W2.4's plan (2026-11-10)

**Amended 2026-11-10 (the revision's D21, D28).** W2.4 now follows W10 and W11, and gains D28's parts: kinds,
shape classes, an online mode with a memory from the corpus, an object's life, a claim that the organ's object
events are real (E6), and reports with the player and the rest apart, by kind. Its test data is D17's fresh
recordings and a held-out part of W11's deep play, and every claim is read for the offline organ and the online
one. It no longer leads to W8 (O5): the layers that read its events are W4's model and W6's battery. The plan
below is otherwise as written.

**What it gives the stages above:** W8 learns each object kind's rule from how it moves and what happens to it.
What happens is W2.4's: a block used, broken or bumped, a coin taken, an object appearing (a power-up out of its
block, a score after a stomp, a fireball) or vanishing (stomped, collected, fallen). The organ's tracks (W2.3′) give
the motion; W2.4 gives the events, in the organ's own terms, checked against RAM.

**The organ** (`indrajala_rl/organ/events.py`, game-agnostic, D18):
- **Landscape events (D16):** per shot, from each picture's map (`Landscape.see`'s classes and states and the
  cells' last shown classes): cells whose shown class differs from the one they last showed, joined into one event
  when 8-connected and changed within one picture of each other. Each event: its cells (shot coordinates), the
  classes before and after, its first picture, whether its cells were hidden when it happened (last shown before,
  seen changed on uncovering, so its time is a range), and at its end lasting (the new classes stay `HOLD`, 64
  pictures, or until out of view) or transient (the earlier classes back sooner, with the classes between).
- **Object events,** from the tracker's objects (W2.3′'s identities): an object **appears** in its first picture
  and **vanishes** in its last sighting, once its track expires (8 pictures, `PATIENCE`). Each is **in view** (its
  box at least a cell from the area's edges) or **at the edge** (entering or leaving). An appearance next to a
  landscape event that picture or the one before (boxes within a cell) is marked as **out of** that event (the
  power-up from its block, a brick's fragments).

**The oracle** (indrajala-rl's `games/smb.py`; test-only, D1):
- **Block events:** `smb.buffer_events` (merged, #45): each on-screen metatile change between consecutive frames,
  with `block_event_kind`'s kinds. A bump is the pair `bump` then `bump end` at one metatile; the oracle's event is
  the pair (old block to final block: lasting when they differ, a used block; transient when they're the same, a
  brick bumped by a small player), timed by the bump's start. A `cleared` change is lasting.
- **Where:** a metatile is 2×2 of the organ's cells. The shot's offset from the world (RAM's camera against the
  organ's position, on the shot's first picture) maps the organ's cells to world cells, for the oracle only.
- **Objects appearing and vanishing:** each of the oracle's objects (slot and kind, as W2.3's identities) appears
  in the first picture it has visible pixels after none for `PATIENCE` pictures, and vanishes after its last.
  RAM gives the cause: spawned (its slot's flag set within the last 2 frames, or a misc or power-up slot newly in
  use) or come into view; removed (flag cleared) or gone out of view.

**The claims, sketched** (the bars from the first probe, at the registration):

| claim | the test | starts from |
|---|---|---|
| E1. Block events found | the oracle's block events on the organ's whole cells, each matched by an organ event covering its metatile's cells, its time within 2 pictures (or its hidden range holding it), lasting or transient alike | 99% |
| E2. Block events real | organ landscape events matched by a block event | set from the probe (objects at rest make transient events: classed) |
| E3. Appearances found | oracle appearances in view matched by an organ appearance holding the object, within 1 picture | 95% |
| E4. Vanishings found | oracle vanishings in view matched by an organ vanishing of the object holding it, within 1 picture plus `PATIENCE` | 95% |
| E5. Every miss classed | misses of E1, E3, E4 with no class | 2% |

**Miss classes:** for block events: hidden at the time (an object over the cells), the bump's sprite exactly on
its tile (W2.2′'s case), at the edge, under a cell not yet seen, other; for landscape events of no block event: an
object at rest (an oracle sprite over the cells: the vocabulary took it in), a palette's step, other; for object
events: W2.3′'s classes for the object (overlap, behind the background, at the edge, cells), its identity switched
(W2.3′'s C5 missed it), other.

**Reported, not claimed:** events by kind and level; the lag between RAM's change and the organ's; appearances
out of events by kind (power-ups, fragments, scores); W2.3′'s claims from the same run (a check that the events
change nothing).

**The PRs:**
1. **indrajala-rl, the organ:** `organ/events.py` (`LandscapeEvents`, `ObjectEvents`), with tests on synthetic maps
   and tracks: a lasting change, a transient one, a hidden one, two events apart, an appearance out of an
   event, an object entering at the edge.
2. **indrajala-rl, the oracle and scorer:** `smb.py` (bump pairing; the slots' spawn and removal from RAM),
   `organ_objects.py`'s events section (matching, classes, E1-E5 in its report and `--score`), and the groups
   sorted by the manifest's frames, not file size (a level start's state made random groups look larger, so the
   longest group, the owner's play, started last in W2.3′'s test run).
3. **The first probe** on `stone`: the two probe groups (`policy/greedy`, `random/1-2`) first, varied on the fly;
   then the W1 corpus and W2.3′'s test set (D17), about 75 minutes each.
4. **D17's test recordings,** listed with their manifest.
5. **indrajala-research, the registration** (E1-E5's bars, the classes, the data), merged before the run.
6. **The registered run** on `stone`, then the findings: W2.4 done or refuted, each refuting kind listed. W8
   follows either way: like D15, one round, then on.

**Feasibility:** the NES draws the background from its name tables, which RAM's metatile buffer writes, so every
block event is drawn on the next picture or two; what no camera can see (a change under an object) has a range,
not a time, and is a class. An object's appearance and vanishing are in its visible pixels, which the oracle has
exactly (W2.3's redraw, equal to the console's on all but 7 of 361,169 pictures).

### W10. The scene and the oracle's source (done 2026-11-10)

**Built** (indrajala-rl #50, #51, #54):
- `indrajala_rl/scene.py`, D19's format, game-agnostic:
  - **the terrain:** the whole cells in view on the shot's grid, each with its shape class (its pattern, colours
    numbered by first appearance: D28's shape classes, from the start), its palette and its state;
  - **the objects:** identity, kind and box, with their pixels;
  - **the events:** cell changes, and object appearances and vanishings, in view or at the edge;
  - **decisions** merged from pictures.
- `games/smb_oracle.py`, D20's oracle:
  - **the terrain** is the PPU's background under the sprites. Its shapes are numbered from the pattern values: a
    perfect organ that has joined a palette cycle's steps, as the organ's vocabulary does, would see a flashing
    block as one shape;
  - **the objects** are the sprites' owners' visible pixels, identities a slot's life. A long fire bar (0x1F)
    takes a second object slot, whose sprites draw its outer balls; they are given to the fire bar (#54, found
    by the run below).
- `organ/adapter.py`: the organ's map and tracked objects as scenes. W2.3's scorer now scores through it.
- `scripts/scene_oracle.py`: the gate's check.

**The oracle against RAM** (`klip`, indrajala-rl `32b0884`, the W1 corpus: manifest `66165a3e…`, 361,169 core
pictures, 1,352 s; `scene/w10b.json`, sha256 `16c180a1…`, in indrajala-studies' gitignored
`data/smb-world-model/`). Nothing is left unexplained:

| what | result |
|---|---|
| the terrain against the block buffer | 252,042,296 cells draw RAM's metatile quadrant, value for value; 40,385,057 are scenery (the buffer holds terrain only; clouds, hills and bushes are drawn where it holds the sky); 1,744,389 clipped (the PPU's left 8 pixels); 284 a bumped block's cell; **372 not RAM's, every one at a block event** (the picture a frame or two behind the buffer) |
| RAM's block events on screen | 559 shown at their cells within 3 pictures; 16 whose old and new metatiles draw alike (a brick's clear after its bounce has blanked it; a hidden block's bump): nothing a camera could see. None missed |
| cell changes in the scenes | 2,230, every one at a block event |
| RAM's objects on screen (the player and the active enemy slots) | 598,675 matched by an object of their slot (96.2%); 23,825 whose slot draws no visible pixel (a piranha inside its pipe, the flagpole's object, flicker); 74 below the band, their other things drawn elsewhere (a killed enemy falling out while its score floats up). None drawn away from RAM's place |
| pictures drawn differently from the console's | 7 (the status bar's split, as W2.3's) |

The first run (indrajala-rl `ecff29d`, `scene/w10.json`, sha256 `726ab19b…`) had 1,503 objects drawn away from RAM's
place; 1,429 were 5-4's long fire bar. That gave #54.

**The organ through the adapter:** W2.3′'s test set (manifest `3d8a62ed…`, 34 groups, 240,109 core pictures)
scored through the organ's scenes on `klip` (indrajala-rl `c6f9a10`, 6 workers, about 2 h 50 min) gives
`w2-3p.json`'s figures exactly. Every group's counts and outcomes are equal, and so are the totals (C2 325,121 of
376,725, C4 545,359 of 576,456, C5 430,877 kept and 6,460 switches). The result is `scene/w2-3p-adapter.json`
(sha256 `2eafdc9f…`). The adapter changes nothing.

**W10 is done:** the oracle's scenes hold what RAM holds, every difference classed, and the organ's scenes give
its figures unchanged.



### W11. The reference planner (2026-11-10)

**Built** (indrajala-rl #52, #53, #55-#59):
- `indrajala_rl/planner.py` (D25), game-agnostic:
  - each decision, `sequences` action sequences over `horizon` decisions, each a run of held segments, rolled
    in a model; the best plan, shifted, is kept among the next decision's candidates;
  - **the score:** the rollout's reward, plus a death's cost and a clear's bonus;
  - **the world's stickiness expected** (`exact = k`): a candidate scores its expectation over all `2**k` stick
    patterns of its first `k` decisions, each weighted by its chance. Later decisions don't stick: the next
    decision plans again;
  - `EmulatorModel`: the console and the game's episode, saved together.
- `games/smb_goals.py`: the battery's goals from what is in view (land on a cell, bump a ? block or brick, stomp
  a Goomba or Koopa), their tests and distances read from RAM inside the search (D20's light form).
- `scripts/planner_level.py`, `planner_battery.py`, `console_rate.py`.

**The console's frames a second, headless** (from 1-1's start, random actions held 4 frames, a restore every 64
frames): `stone` 10,940 on one core, 44,861 over 8 processes; `klip` 3,265 on one core, 18,554 over 8.

**The probes** (1-1 under sticky actions, 0.25; 20 episodes each on `stone`, every probe on new seeds after the
first two):

| # | the planner | cleared | deaths |
|---|---|---|---|
| 1 | 16 sequences, horizon 16, rollouts not sticky (970 frames a decision) | 15 of 20 | 5 |
| 2 | 64 sequences, horizon 24 | 14 of 20 | 6 |
| 3 | 32 sequences, sticky draws 2 | 17 of 20 | 1 fell, 2 hit |
| 4a | 32 sequences, sticky draws 4 | 17 of 20 | 3 fell |
| 4b | 32 sequences, horizon 24, sticky draws 2 | 15 of 20 | 3 fell, 2 hit |
| 5 | 4a's, scored by the worst of 1-3 forced repeats too | 11 of 20 | 5 fell, 4 hit |
| 6 | 24 sequences, `exact` 3 (11,800 frames a decision) | 18 of 20 | 2 fell |
| 7 | 6's, a death costing 1,000 (not 100) | **19 of 20** | 1 hit |

- **The search's width was never the limit** (probe 2 at four times probe 1's budget).
- **Stickiness was:** traced decision by decision, every fall had the planner on a pit's edge choosing to jump
  while a run of sticks repeated its last action.
- **Random draws seldom hold such a run.** A forced worst case made every candidate tie where repeats are fatal
  whatever the plan (probe 5).
- **The exact expectation counts runs at their true odds** (probe 6). Its two falls were rational risks at a
  death of 100, about 1.6 points for a few pixels against a level worth about 190 cells and the clear.
- **Probe 7's one death** was four sticks in a row after a crouch at the first Goomba: one beyond `exact` 3,
  about 1 in 256.

**The battery's probe** (probe 7's planner, from states along probe 1's 20 recorded episodes, a state every 480
core frames standing, one goal of each kind in view, at most 60 decisions, sticky, no restore): land 35 of 37
(94.6%), bump 20 of 25 (80.0%), stomp 10 of 12 (83.3%). No attempt died; every miss ran out of decisions.
Medians 14, 23 and 14.5 decisions; 7,200-9,000 frames a decision.

#### W11's registration (2026-11-10, before the registered run)

**The planner:** indrajala-rl `7994379` (#59): 24 sequences, horizon 16 decisions, segments 4 (held for 1 to 7
decisions), rollouts expecting stickiness 0.25 with `exact` 3, a death costing 1,000 and a clear worth 100. **The
budget:** about 12,000 frames a decision on the level, 7,000-9,000 on the battery.

**The data (fresh):** the level, 100 episodes of 1-1 on seeds 1000-1099 (no probe used them), 0.25 sticky, the
first decision never sticky, up to 3,000 decisions; each episode recorded as inputs (D13): the deep play. The
battery runs from states along those 100 recordings, a state every 480 core frames with the player standing, one
goal of each kind in view drawn by seed 0, at most 60 decisions an attempt.

| claim | the test | refuted by | the probe |
|---|---|---|---|
| L1. 1-1 cleared | episodes cleared of 100 | under 90 | 19 of 20 |
| G1. Land | goals reached of those attempted | under 85% | 94.6% (35 of 37) |
| G2. Bump | as G1 | under 65% | 80.0% (20 of 25) |
| G3. Stomp | as G1 | under 65% | 83.3% (10 of 12) |

**L1's bar is the plan's** (the NES plan's 90 of 100). **G1-G3's** are the probe's, less a margin for its small
samples: about 10 points for land and 15 for bump and stomp, whose probes held 25 and 12 attempts.

**Reported, not claimed:**
- deaths by cause (fell, hit) and where;
- decisions an episode, and frames a decision;
- the battery's misses (out of decisions, died), the decisions to reach each kind, and the attempts per level
  region.

**Feasibility:**
- the planner searches the exact game with restore;
- planning again each decision absorbs stickiness, which the rollouts expect at its true odds for 3 decisions;
- the probe cleared 19 of 20, and a 95% true rate passes L1's bar with 99% chance;
- every goal is drawn from what is in view, within the screen's columns, and the probe reached each kind.

**Fallback (D30):** a wider expectation (`exact` 4) and a longer horizon, registered apart. Nothing learned is at
stake.

#### W11's result (2026-11-11)

Run on `stone`, 8 workers, as registered (indrajala-rl `7994379`). **L1 is refuted; G1-G3 hold.**

| claim | the test | refuted by | the result |
|---|---|---|---|
| L1. 1-1 cleared | episodes cleared of 100 | under 90 | **82 of 100: refuted** |
| G1. Land | goals reached of those attempted | under 85% | **95.9% (185 of 193): holds** |
| G2. Bump | as G1 | under 65% | **82.4% (103 of 125): holds** |
| G3. Stomp | as G1 | under 65% | **79.4% (50 of 63): holds** |

**The level (L1):**
- 82 cleared, 18 died, none out of decisions. Cleared episodes took 322-388 decisions (median 353).
- **Deaths, 9 fell and 9 hit.** All falls were at 1-1's three pits: x 1155-1160 (2), 1424-1446 (3) and
  2465-2477 (4). The hits were at x 679-680 (2), 1523, 1791-2021 (6) and 2757.
- **Frames a decision:** 11,216-11,880, mean 11,676; about 16 minutes an episode on one of 8 workers.
- **The probe overstated the rate:** probes 6 and 7 cleared 37 of 40, and the three runs at these settings pool
  to 119 of 140 (85%). Twenty episodes cannot tell 85% from 95%; a fallback's run is registered at 100.

**The battery (G1-G3):**
- 381 attempts from 98 of the 100 recordings.
- **Misses:** 40 ran out of decisions (bump 22, stomp 13, land 5). 3 land attempts died or ended, two of them
  at the first pit (columns 73-74).
- **Decisions to reach,** median: land 13, bump 20, stomp 12. **Frames a decision:** median 8,231.
- **By region** (the goal's x, in 1,024-pixel quarters of the level; stomp goals carry no column):
  - land: 11 of 11, 85 of 87, 86 of 87 and 3 of 8;
  - bump: 85 of 94 in the second quarter, 18 of 31 in the third.

**The recordings' ROM field (fixed after the run):**
- `planner_level.py` gave the recorder the ROM's image where its identity belongs, so the 100 recordings' ROM
  field held the image's first 20 bytes.
- The recorder now refuses an identity that is not 20 bytes (indrajala-rl #61).
- The recordings were rewritten with the identity, their start states' CRC recomputed. Every one replays to its own
  final RAM under `corpus_manifest.py` (100 recordings, 130,196 frames). Their inputs are unchanged, so the
  battery's run from the originals stands.

**The deep play** (100 recordings of 1-1 with its manifest), the level's and the battery's results and logs are in
indrajala-studies' gitignored `data/smb-world-model/planner/w11/`.

**What follows (D30):**
- **The fallback is registered apart, after a diagnosis of the 18 deaths.** Each death is replayed exactly with
  `planner_trace.py` (indrajala-rl #60), decision by decision: the state, the action chosen and the one taken,
  the candidates' scores.
- **The hypothesis to test:** with `exact` 3, a rollout's decisions after its third never stick. So a plan that
  needs a precise press five decisions ahead (a jump at a pit's edge, a hop over an enemy) scores as safe, and
  the planner walks into states that a run of sticks makes fatal.
- **Two candidates:** `exact` 4 (probed on `klip`, 40 episodes on seeds 2000-2039), and later decisions sticking
  at random at 0.25 after the enumerated ones.
- **G1-G3 stand:** the battery's goals are reachable at their stated rates, and W2.4 can use the deep play now.

#### W11's fallback: the diagnosis, the probes and the registration (2026-11-11, before its run)

**The diagnosis.** All 18 deaths were replayed exactly with `planner_trace.py` (indrajala-rl #60): every
replay matched its episode's decisions and place. One cause: **the rollouts can't see a run of sticks longer than
`exact`'s window.**
- **12 deaths walked into a trap:** the best score about +9 (safe), then each stick drops it, about -6, then
  -53, then -243, then death. These are states where a run of 4 sticks kills whatever the planner does next, and
  `exact` 3 counts runs of 3.
- **6 dropped at once:** from about +9 to about -243 in one decision, after one stick or none. A press the plan
  needed at its 4th decision, scored as if it couldn't stick, entered the window.

**The remedy:** a wider window.
- **The cost:** stick patterns that take the same actions now roll once (indrajala-rl #62). A stick that repeats
  what the plan holds changes nothing, and the model is deterministic. The change was tested against brute
  force, and seed 1016's trace was reproduced score for score.
- **Frames a decision** over 60 decisions of seed 1000, before and after #62:

  | `exact` | before | after |
  |---|---|---|
  | 3 | 11,974 | 6,243 |
  | 4 | 23,929 | 8,853 |
  | 5 | 47,805 | 12,623 |
  | 6 | 95,585 | 18,203 |
  | 7 | | 26,884 |

- **Why 6:** a trap that needs k+1 sticks costs about 1,000 × 0.25^(k+1) in the score, too little to steer by.
  It is the window that counts.

**The probes** (1-1, sticky 0.25, the registered planner but for `exact`; fresh seeds each):

| `exact` | seeds | cleared | deaths |
|---|---|---|---|
| 4 (before #62) | 2000-2039 | 39 of 40 | 1 fell (x 2476) |
| 6 (indrajala-rl `8bd680d`) | 3000-3099 | **95 of 100** | 4 fell (x 1139-1156, 1446, 2477), 1 hit (x 1524) |

At `exact` 6, frames a decision were 17,420-18,328 (mean 17,910); cleared episodes took a median of 357 decisions.

**The registration (L1′).**
- **The planner:** indrajala-rl `8bd680d` (#62): 24 sequences, horizon 16, segments 4, rollouts expecting
  stickiness 0.25 with **`exact` 6**, a death costing 1,000 and a clear worth 100.
- **The budget:** about 18,000 frames a decision.
- **The data (fresh):** 100 episodes of 1-1 on seeds 4000-4099 (no run or probe used them), 0.25 sticky, the
  first decision never sticky, up to 3,000 decisions, each recorded as inputs: deep play, added to W11's.

| claim | the test | refuted by | the probe |
|---|---|---|---|
| L1′. 1-1 cleared | episodes cleared of 100 | under 90 | 95 of 100 |

**Its bar is L1's.** G1-G3 held at `exact` 3 and are not claimed again: the battery is not rerun.

**Reported, not claimed:** deaths by cause and place, decisions an episode, frames a decision. Also the five
deaths of the `exact` 6 probe, traced (offline, on `klip`).

**Feasibility:**
- the same exact model with restore;
- the window now counts runs of sticks up to 6, about 1 in 4,096;
- the probe cleared 95 of 100, and a true rate of 95% passes the bar with 99% chance (93%: 91%).

**If refuted (D30):** a longer horizon and the probe's traced deaths, registered apart. Nothing learned is at
stake.

### W3. The self (D5) (the first draft's; see the revision)

- Babbling: random actions held for random lengths, sticky as in the environment, from every level's start and
  from human play's states.
- The inverse model: per tracked object, its motion over the last k decisions to the action taken, a small
  classifier in indrajala-ml.
- Done when **the self is RAM's player on at least 99% of frames**, on held-out levels and in every power-up
  state; and it agrees with the counterfactual check (restore, each action) on a sample of states. The disagreements
  (a kicked shell, a bumped block) are listed.

### W4. The world model (D4) (the first draft's; see the revision)

- Data: W3's babbling, human play, the conv policy's episodes, as organ output.
- **First probe (existence):** 1-1 and 1-2 to train, 1-3 held out; one-step and k-step rollouts.
- Done when **k-step rollouts are within a pixel per object at stated rates on held-out levels** (k and the rates
  from the probe), and better than the copy and flat baselines. The rollout is checked against the emulator from
  the same restored states. Events are predicted at a stated recall.
- The ensemble's disagreement is reported against the actual error (it must rank states by error to serve D6).

### W5. Play (D6) (the first draft's; see the revision)

- The archive (cells: the self's map cell and power state), return by restore, goals near the frontier, the
  model retrained on what play gathers.
- Done when **the model's held-out error falls with play** and **coverage of the levels rises** against babbling
  at equal frames. The goals reached are recorded. Each added mechanism (learning progress, then disagreement)
  only on its stated stall.

### W6. Control (D7, D12) (the first draft's; see the revision)

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

### W7. The level (D8) (the first draft's; see the revision)

- The chooser over play's goals, trained on the level's reward, control below it.
- Done when **the NES plan's bar on 1-1 is met** (greedy 90 of 100, sticky, confirmed on fresh seeds). It is
  reported against the conv policy's frames to the bar (all play counted), and on held-out levels.

### W8. Discovery (after W2.4, before W3: O2) (the first draft's; see the revision)

- Each object class's update as a snapped machine, read off, minimised, and checked against RAM's object state.
- Its accuracy is compared with W4's. Its cells go through the feasibility register at registration.

### W9. The learned organ (D2) (the first draft's; see the revision)

- A slot or keypoint model from pixels (SAVi conditioned on W2's hints first, then unconditioned; Transporter as
  the second), scored against RAM (AtariARI's probes) and against W2's organ.
- Then swapped in under W3-W7, and the stages' results reported with it.

## Feasibility

*Replaced 2026-11-10 by the revision's feasibility table; the first draft's, for the record:*

| check | the claim | why it can succeed |
|---|---|---|
| the organ sees what it must | the scene is a function of the frames | the NES draws everything it shows from tiles and sprites on known grids; what it can't see (a Piranha plant inside its pipe) is a classed miss, not a failure |
| the self is identifiable | exactly one object's motion the buttons predict, over a window | in SMB only the player answers the pad; the camera is removed by the scroll first; things the player moves (a shell, a bumped block) answer only after contact, which a window separates; the counterfactual by restore confirms it |
| the model can be accurate | the next scene is a function of the scene and the action | the game is deterministic; sticky actions act on the agent's choice, not the world, so the action taken is known; what the screen hides (an enemy off-screen, an RNG-driven choice) bounds the rollout's horizon, stated per stage |
| control can succeed | each battery goal is reachable from its start | the reference planner on the emulator (D12) reaches it first; goals it can't reach leave the battery |
| no memorising | levels held out at every test | the model and the control are scored on levels they never trained on; sticky actions at every control test |

## Findings

- **The assessment (2026-11-10):** [review-2026-11-10-smb-world-model.md](../reviews/review-2026-11-10-smb-world-model.md).
  What holds: the scroll and grid, the map, the oracle, the method. What didn't: "objects found" is half the
  player, and the other objects are found 71.2% of the time (88.7% in the policy's 1-1 play); identities switch
  on 2-3% of pictures in real play; the organ is scored with hindsight and gives no kinds; random play reaches
  a median of 352 pixels into a level; W3's bar and W4's feasibility row couldn't hold (the player's next
  motion is open in 37% of frames from one frame of history, 3.9% from eight). The revision above is the plan
  drawn from it.
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
  `stone:~/labour/w2/w2-1.json` (sha256 `0a939782…`), copied to indrajala-studies' gitignored `data/smb-world-model/organ/`.
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
- **W2.1′, the registered follow-up (2026-11-08): all six claims hold. W2.1 is done.**
  - **The run:** `stone`, 797 s, indrajala-rl `1ac1f8a` (#39), the same corpus and groups. The results are in
    indrajala-studies' gitignored `data/smb-world-model/organ/w2-1b.json` (sha256 `f148ee90…`).
  - **R1:** every group's band is rows 32-240.
  - **R2-R4:** every core shift (360,942), position and grid phase (361,169 pictures) exact.
  - **R5:** no core picture unplaced.
  - **R6:** the 59 breaks in the core are all changes of scene. 4 are jumps of the drawn scroll; 55 touch a
    picture of one colour, a level's start from black.
  - **Kept by their pixels:** 9 pairs (8 in the core), all right. They are exactly the probe's 9 false cuts:
    the 32 groups no probe saw had none.
    - So the pixel test is exercised only on the pairs it was set from. Its safety on a direct change between
      similar scenes is untested on SMB, which always passes through black.
    - R2 and R3 would catch a wrong kept shift on any later data.
  - **What the organ gives the layers above:** shots, each with the screen's position and the tile grid,
    exact against the drawn scroll. The world camera is the drawn scroll mod 512 in the core, so a shot's
    positions are the camera's, up to the shot's start.
- **W2.2, the registered run (2026-11-08): M1, M4 and M5 hold; M2 and M3 are refuted.**
  - **The run:** `stone`, 1,216 s, indrajala-rl `7324631` (#40), the corpus (manifest sha256 `66165a3e…`), all 35
    groups. The results are in indrajala-studies' gitignored `data/smb-world-model/organ/w2-2.json` (sha256
    `66041963…`).
  - **The map:** 294.2M whole cells in the core, 1,431 classes. 268.5M cells were on their tile, 20.7M scenery and
    5.0M in a sprite's box.
  - **M1 holds:** no cell on its tile was seen with a class of another drawing it isn't alike. 1,035,610 were
    alike, mostly uniform blocks two metatiles draw the same (a pipe's inside and a bush's).
  - **M4 holds:** 15,970 cells on their tile were unknown (0.006%; the bar is 0.01%).
  - **M5 holds:** 1,144 classes were seen mostly in a sprite's box (objects taken for landscape). They hold
    330,365 seen cells (0.11%; the bar is 0.5%).
  - **M2 is refuted:** 12 conflicts, all on the 33 groups no probe saw, from three objects.
    - A used block in the owner's 1-2 (twice) and coins in 7-3's sky are palette-3 blocks, which cycle colour
      like the question blocks.
    - Their cycle passes through a step where two values share a colour. On 7-3 that step lasted 7 frames
      with the screen still, so it never joined the vocabulary, and the join needed both ends there.
  - **M3 is refuted:** 4,409 wrong fills (0.11% of 3,986,940; the bar is 0.01%).
    - 4,332 of them are three class-and-drawing pairs (a uniform block over 228, 238 and 1) that M1 counts
      alike on seen cells.
    - **My error in the registration:** M3's test judged fills by the exact drawing and left out the alike rule
      that M1 has. The probe's fills held no alike pair, so the probe didn't show it.
  - **Fills where RAM changed under a sprite** (events, reported): 6,997 of another drawing (W2.4's events).
  - **Next:** W2.2′, registered above, with the two changes.
- **W2.2′, the registered follow-up (2026-11-08): M1, M3, M4 and M5 hold; M2 is refuted by one kind of event.
  W2.2 is done, its exceptions listed.**
  - **The run:** `stone`, 1,195 s, indrajala-rl `b1cbecb` (#41), the same corpus and groups. The results are in
    indrajala-studies' gitignored `data/smb-world-model/organ/w2-2b.json` (sha256 `2f6f5155…`).
  - **M1 holds:** none not alike, of 268.5M cells on their tile (1,035,610 alike).
  - **M3 holds:** 90 wrong fills of 3,962,598 (0.002%; the bar is 0.01%). 4,319 alike fills; 6,988 where RAM
    changed under a sprite (events, reported).
  - **M4 holds:** 15,918 cells on their tile unknown (0.006%).
  - **M5 holds:** 1,144 classes of objects taken for landscape, with 331,390 seen cells (0.11%).
  - **M2 is refuted:** 8 conflicts, the four quadrants of a used block at two moments of the owner's 1-2
    (frames 5,954 and 38,671). The two follow-up groups (6-3, 7-3) and the probe's had none.
    - **What they are:** at a bump's end, the bouncing block's sprite lands exactly on its cell for a frame. It
      draws the used block's own pattern in a sprite palette, aligned to the grid, so the oracle accounts it as
      the tile, and its block, which is in the vocabulary from elsewhere, is seen as a second class of that
      drawing in the shot.
    - It is an object exactly over the tile it copies, which pixels alone can't tell from the tile for that
      frame. It belongs to W2.4's events (a bump), where the oracle can also check sprites drawn in the tile's
      own pattern.
  - **No W2.2″.** Changing the organ for two frames of 294M cells would tune it to an edge case. The criterion
    ("every exception listed") is met, with this one listed.
  - **What the organ gives the layers above:** per shot, each 8×8 cell's class (exact block, palette cycles
    joined), with hidden cells filled from earlier pictures:
    - the classes are a function of RAM's metatile quadrants up to blocks two metatiles draw alike;
    - scenery, which RAM's buffer doesn't hold, is classed like the terrain;
    - objects at rest (1,144 classes, 0.11% of seen cells) are listed by class for W2.3.
- **W2.3, the registered run (2026-11-09): B1, B3 and B4 hold; B2 and B5 are refuted on the 33 unseen groups.**
  - **The run:** `stone`, 31,240 s (one worker spent most of it on the owner's session), indrajala-rl `385d718`
    (#42), the whole W1 corpus (35 groups, 361,169 core pictures). The results are in indrajala-studies' gitignored
    `data/smb-world-model/organ/w2-3.json` (sha256 `2048c4ce…`, the corpus manifest `66165a3e…`), scored by
    `organ_objects.py --score` (indrajala-rl #43).

    | claim | the probe's 2 groups | the 33 unseen | bar | verdict |
    |---|---|---|---|---|
    | B1. The redraw is the console's | 6 of 40,460 | 1 of 320,709 (random 5-2) | more than 0.1% | holds |
    | B2. Objects found | 90.3% (76,120 of 84,315) | **80.8%** (448,727 of 555,673) | under 89% | **refuted** |
    | B3. Objects real | 89.4% | 93.4% (814,262 of 872,196) | under 88% | holds |
    | B4. Identities kept | 98.1% | 98.4% (483,910 kept, 7,797 switches) | under 97.5% | holds |
    | B5. Every miss classed | 1.2% | **4.14%** (22,995 "other") | more than 2% | **refuted** |

  - **The refuting kinds (B2):** the unseen misses are 106,946: over a cell showing a landscape block 32,114, other
    22,995, overlap 17,674, behind the background 16,337, at the edge 10,994, over a cell not yet seen 6,832. By
    kind (ids by where they occur):
    - **kinds the probe never had** (its groups are 1-1 and 1-2): the Piranha plant (0x0D, pipe levels) 16.7%,
      15,448 behind the background; fire bars (0x1D, castles 1-4, 3-4, 6-4) 0.1%, over landscape cells or cells
      not yet seen (the vocabulary takes them in); the flag on the flagpole (0x30) 12.1%, at rest over landscape
      cells; an object of 7-4 only (0x29, not identified) 0.1%, over landscape cells; the Blooper (0x07, water
      levels) 34.6%, 7,182 "box differs: other"; air bubbles 86.1% (2,200 overlap); Podoboos (0x0C) 91.3%;
    - **kinds the probe had, in new play:** Goombas (0x06) 70.8% (6,536 other, 3,720 over landscape cells, 3,315
      overlap), mostly in the sampled policy's 1-1 and the owner's session; Koopas (0x00) 83.4%; the player 97.6%.
    - **Over the probe's kinds only,** the unseen groups give B2 90.5% (375,530 of 415,171), over its bar: B2's
      refutation is the kinds the probe didn't hold. Reported, not a claim.
    - **By group:** 24 of the 33 at or over 89%. Under it: the owner's session 55.7%, random 7-4 56.3%, 3-4 68.0%,
      6-2 73.2%, 3-1 74.0%, 5-4 75.6%, 8-1 77.6%, 4-1 81.2%, 5-2 85.2%.
  - **The refuting kinds (B5):** 15,486 of the 22,995 unclassed misses are in the owner's session. By kind: Blooper
    7,485 (7,182 its box differs), Goombas 6,536 (4,257 split, 2,278 box differs), Koopas 2,346, the player 2,284
    (1,696 box differs), air bubbles 505, Podoboos 861. Over the probe's kinds only, B5 is 2.85% (11,819): refuted
    either way. "Other" holds misses the classes don't name: a box off by more than a pixel or an object split, with
    no overlap, edge, background or cell state to explain it.
  - **What held:** the redraw is the console's on all but 7 of 361,169 pictures; 93.4% of tracked objects are real;
    identities are kept on 98.4% of consecutive pictures.
  - **The run's cost** was the objects pass: each picture cost its pieces × the kept looks × a whole-area operation,
    and the owner's six levels keep many looks. indrajala-rl #46 skips looks that can't be drawn and narrows
    matches pixel by pixel, with the same results (equal to the probe's `first-c.json` in every field); the objects
    pass on the owner's session runs about 6.7 times faster.
  - **The objects pass, faster and the same, checked on the owner's session:** indrajala-rl #46's code gives that
    group's result equal in every field to this run's, in 5,652 s.
- **W2.3's diagnosis (2026-11-09): the unclassed misses are four mechanisms of the organ's, one of them in two
  forms.**
  - **How:** indrajala-rl #47's outcome dumps (`organ_objects.py --dump-outcome`, `organ_view.py`), 378 pictures of
    "other" misses from the owner's session and eight smaller groups (random 1-2, 2-2, 3-1, 3-2, 5-1, 5-2, 5-4 and the
    sampled policy's 1-1), up to 12 per kind and outcome. Each miss's true box against the tracked and detected
    boxes, and the landscape's state under the difference.
  - **A. False foreground joins an object ("box differs": the Blooper, Goombas, Koopas, the player, the power-up).**
    One tracked object's box reaches past the true box on one side, by 2-7 pixels. Every overhanging pixel is
    foreground that is no object's visible pixel (none is another object's), in a hidden (filled) cell:
    - **A1, the earlier class unused under an object** (most of them): the cell's class changed to an object's block
      that the vocabulary holds (`Landscape.prior` keeps the earlier class), and the object now hides the cell. The
      foreground uses the earlier class only for cells shown (`changed = prior[1] & ~hidden`), so the hidden cell is
      filled from the object's own block, and the object's old drawing against the landscape becomes foreground.
      In every such cell sampled, the filled class differs from the earlier one. The power-up rising from its block
      (the used block's change) is the same mechanism.
    - **A2, a cell known only as an object's block** (the player's 32 cells and half the Blooper's): the first block
      the cell showed was an object's that the vocabulary took in (W2.2's M5, 0.11% of seen cells), so there is no
      earlier class to use. W2.3's classes name this only for cells shown ("over a cell showing a landscape block").
  - **B. Stray pixels left over (splits: Goombas, Koopas, bubbles, the player).** A known look explains the object
    exactly but for 1-5 of its own visible pixels (the look was learned where they matched the background), and they
    stay as a piece of their own, tracked as a second object. They were one connected piece with it.
  - **C. A partial look first (some Goomba splits).** In a piece that isn't clean, `explain` tries looks most-seen
    first, and a look of half a Goomba (its left 8 columns) takes the piece before the whole one; the other half is
    left over.
  - **D. Score digits that never join (Goomba splits in the sampled policy's stomps).** A stomp's floating score
    ("100", 43 visible pixels) is three pieces of 14 pixels or fewer, under the looks' 16, so none has a key. They
    should join as tracks moving alike, but their tracks swap among the evenly spaced, identical digits (track 93 on
    the middle digit, then the right one), so no two move alike for 2 pictures.
  - **Next: W2.3′,** registered from a first probe, with a change for each:
    - A1: a hidden cell with an earlier class is compared with that class;
    - A2: a miss class of its own ("over a cell filled with an object's block": the oracle's M5 test on the cell's
      class), since the organ can't tell such a cell from landscape until the object leaves;
    - B: a leftover of a piece under 16 pixels that touches one of the objects explaining the piece joins it;
    - C: in a piece that isn't clean, of the looks drawn there, the one covering more of the piece first;
    - D: a tracking tie-break for keyless pieces of one shape, or joining that tolerates a swap.
  - **The test set is used up:** all 35 groups have now been looked at. W2.3′ needs new recordings to test on (D14).
- **W2.3′'s first probe (2026-11-10, `stone`): the four changes, then two narrowed by ablation.**
  - **The changes** (indrajala-rl #48) over the whole W1 corpus, against W2.3's run: objects found 82.0% → 84.4%
    (524,847 → 539,903); unclassed misses 24,025 → 7,953 (3.75% → 1.24%); boxes off by more than a pixel with no
    class 14,052 → 1,579. The owner's session gained most (Goombas matched 32.7% → 71.7%); the power-up rising out
    of its block went from 35.7% to 95.5% (A1). The new class holds 15,428 misses, 14,835 of them in the owner's
    session.
  - **But the first probe's two groups lost 424 matches.** Each change turned off in turn on those groups (B2,
    with all four: 89.78%):

    | turned off | B2 | B3 | Goombas | Koopas | the power-up |
    |---|---|---|---|---|---|
    | none | 89.78% | 93.19% | 80.7% | 93.1% | 95.5% |
    | A1 | 88.67% | 91.60% | 79.4% | 93.1% | 37.1% |
    | B | 90.44% | 92.10% | 82.0% | 97.4% | 93.4% |
    | C | 89.96% | 90.82% | 81.1% | 93.0% | 94.9% |
    | D | 90.50% | 93.16% | 82.3% | 94.1% | 95.5% |

    - **B** joined strays over cells not yet seen (72 Koopa boxes widened: "over a cell not yet seen"). A stray
      there is a guess at the background, as the leftovers there already were: **narrowed to known cells.**
    - **D** joined Goomba-sized parts (splits over shown landscape 409 → 1,021). A score's digits are each under
      16 pixels: **narrowed to pieces under 16 pixels.**
    - A1 and C kept (C costs 0.2 points of B2 on these groups and gives 2.4 of B3).
  - **Narrowed (indrajala-rl #49), the probe again:** the two groups' B2 89.78% → 90.15%; the corpus's 84.46%
    (540,514), B3 96.05%, B4 98.86%, B5 1.24%, 4,587 s. The registration's probe (above).
