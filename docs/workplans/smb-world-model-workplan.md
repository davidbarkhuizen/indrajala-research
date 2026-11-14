# Workplan: motion control from a world model, with Super Mario Bros as the simplest platform scroller

**Status (2026-11-14): stopped by the owner after W6's R3 and retired ("The plan stopped", at the end of W6's
sections).** Before that (2026-11-12): revised after an assessment of the plan and its work so far
([review-2026-11-10-smb-world-model.md](../reviews/review-2026-11-10-smb-world-model.md)), at the owner's direction:
"take them all into account and revise the workplan - we need a plan that will work". The plan in force is
"The revision of 2026-11-10" below: what "complete" is (O3), two sources of scenes (O4, amending D1), W8 after
the SMB work (O5, superseding O2), D19-D61, and stages W10, W11, W2.4, W3, W4, W6, W5, W7 and W12, each with a
gate and a fallback. W10 (the scene and the oracle's source) is done. W11 (the reference planner) is passed: its
level gate (L1) refuted at 82 of 100, its battery (G1-G3) holding, and its fallback (L1′, a wider stick window,
`exact` 6) holding at 95 of 100 (2026-11-11). Its every-level pass cleared 13 of 32 levels, one episode each. W2.4 is done (2026-11-12): every registered claim holds, offline and online (D31-D35). W3 is done (2026-11-12): the self is the player on 99.86% of babbling's decisions and 100% of deep play's (D36-D40). W4 is done (2026-11-12): the model beats copying for every kind and the self (D41-D47). W6 is in its fifth round (D48-D80, O7, O8): its probes put W4's model at 91% of the reference on land, 32% on bump and 0% on stomp; with the fallbacks and the goals' corrections (D57-D60), 93.5%, 65.1% and 44.0%; the diagnosis (D61) puts the misses on the self's motion in the air under A and on objects out of view (D62); a larger network improves the model's own measures but not control (probe 8); rollout training (D63), contacts (D64, D65), the box's offset (D66) and an ensemble (D67) leave bump at 73.0% and stomp at 60.0% at best; young objects with their age (D68) bring stomp to 70.0%, bump unchanged (D69); the owner chose one more round (O7's route 1): object permanence is moot (D70), and a longer history (D71) and a deeper window (D72) leave bump at 68-73% and stomp at 68-74%; the owner then asked for the solutions picked and ordered (O8, 2026-11-13): W6's fifth round (D74-D80, R0-R4): R0 done (the misses are searches that find nothing, not vetoes; the reference's repeats within 80% of seed 0's), R1 refuted on bump (96 candidates: bump 48, stomp 40), R2 under way; the organ's second round (O6) is W13, before W12.**

**Done before it, and standing:** W0 (the literature, 40 papers); W1 (frames and recordings, the owner's play
included); W2.1 (the screen layer: W2.1′, all six claims); W2.2 (the landscape map: W2.2′, one claim refuted by
one kind of event, listed); W2.3 (objects: W2.3′, objects found on machine play refuted at 86.3% against 87.5%,
the rest holding; closed under D15).

**The order among the plans (the owner, 2026-11-10): "I would like to complete the SMB work first - then return
to the machine discovery research".** This plan runs first; [what-is-told-workplan.md](what-is-told-workplan.md)
follows it, and W8 is its stage 6.

This plan is its own, not a sub-plan of the NES plan's. It uses that plan's emulator, game layer and runners.
Its IDs are its own (D1-D80, O1-O8, W0-W13; W6's fifth round has F1-F9, R0-R4 and C1-C3).

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
- **O6. The organ's second round (the owner, 2026-11-12: "do another organ round, when its appropiate").** After
  W2.4's run, D15 having closed the rounds on objects for W2.3′ and W2.4. Placed as **W13, before W12**: W3-W7 run
  on the oracle's scenes first, so they don't wait on it, and W3's organ column adds to its scope. Its scope from
  W2.4's result: objects behind the background and switches (E3 and E4's misses), and the player's split lives.
  The lasting changes (D31) hold online already. One probe, one registration, one run (D30). It comes sooner if W4 or W6 shows the
  organ's errors block them.
- **O7. W6's way on (resolved 2026-11-13: the owner chose route 1, "1").** Put to the owner by D69, after probe
  14: land 97.3%, bump 73.0% and stomp 70.0% of the reference, against a gate of 80% per kind. The owner chose
  D69's first route: object permanence for stomp, with a diagnosis of the ledge climbs for bump, as one more round
  ("W6's fourth round"; D70-D73).
- **O8. W6's way on, after the fourth round (resolved 2026-11-13; put to the owner by D73).** The round left the
  planner on the learned model at land 96.8-97.8%, bump 68.3-73.0% and stomp 68.0-74.0% of the reference (probes
  15 and 16). The routes are under D73.
  **The owner's answer,** on an analysis of the briefing: "you pick which solutions you think we should try, and
  in what order", with a check that the fault isn't in a part not yet looked at. The pick is W6's fifth round
  (D74-D80): measure the planner's view first, then the planner on the model, the planner's own play, the self's
  box factored, and rules last. The gate stays; routes 3 and 4 come back to the owner only if the round ends
  refuted.

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
- **D31. What E1 counts as a block event found.** (New 2026-11-12, W2.4's probes.) The probes found two things.
  A small player's bump moves the block as a sprite that hides its own cell, so no cell the camera sees changes.
  And the organ reads a **lasting** change of the landscape (a question block used, a brick broken) as an object's
  block over the cell's earlier class: W2.3′'s A1 passes a cell showing a class other than its earlier class as that
  class, hidden. So a used block is never a landscape event, and the map never shows it within the shot. On the
  deep play, E1 as first built (the sprite counted for every event) read 98.5%, but 190 of its 201 events were
  found by the sprite alone. The lasting ones were among those 190, although the map never held them.
  - (a) *Chosen.* **Split by the oracle's own kinds.** **E1** claims the **transient** block events: found by an
    organ event or by an organ appearance on the block's cells within `LAG` pictures (its sprite). **E1L** reports
    the **lasting** ones: found by an organ event, or when the map shows them (one of the cells, seen, shows another
    class or its first within `HOLD` and `LAG` pictures). Each route is counted by kind (indrajala-rl #70-#72).
    - Pros: each count says what the organ's scene holds; a sprite over a bump is what a camera sees, but a used
      block left only as an object's block is not landscape; the probes score unchanged from their route counts.
    - Cons: E1L is low on 1-1 (5 of 96 on the deep play) and isn't claimed. That is the organ's state, recorded
      as a finding: its remedy (the map accepting a change that no object moves over) is another round, which D15 rules out
      for W2.4.
  - (b) E1 as first built: any organ event or appearance on the cells, lasting or transient.
    - Pros: one number, 98.5% on the deep play.
    - Cons: it claims block events found that the organ's map never holds.
  - (c) Every block event by the map only.
    - Pros: one strict rule.
    - Cons: a small player's bump changes no cell the camera sees; the rule would count the camera's limit as
      the organ's miss.
- **D32. What W2.4 claims.**
  - (a) *Chosen.* **Claim E1, E3, E4 and E5 by source, and the online organ within a margin of the offline;
    report E1L, E2, E6 and K1.** The probes show the organ's own object events are mostly identity splits and
    merges (E6 3-4%; W2.3′'s P1 and P2), whose remedy is the belief scene (D29, W12). Kinds' purity (K1, 54-82%)
    rests on those identities. E2 counts the objects at rest and the objects' blocks leaving their cells that D16
    classes, and E1L is D31's.
    - Pros: each claim has a probe behind it and a bar the probe sets; what isn't claimed is still measured
      and goes to the layers that read it.
    - Cons: four of the D28 parts are reported, not claimed.
  - (b) Claim every row, with bars from the probes.
    - Pros: everything is on the record as held or refuted.
    - Cons: bars set at 3-5% (E6) or 5% (E1L) claim nothing an agent could use; the registration would only
      record the probes again.
- **D33. The bars: by source, from the probes, less a margin.**
  - (a) *Chosen.* **Machine play** (random, policy) and **deep play** (the planner's) are claimed apart, each
    against its own probe. The margin is about 2.5 standard errors of the probe's count, as W11's were sized by
    their samples. Machine play's appearances and vanishings (E3 68.5%, E4 55.6% on the W1 corpus) are far below
    the deep play's (87.2%, 91.9%): objects behind the background and switches dominate their misses.
    - Pros: a pooled bar would measure the test's mix of sources; each source's bar travels with its recipe.
    - Cons: two bars a claim; the deep play's E3 rests on 117 appearances.
  - (b) One pooled bar per claim.
    - Pros: simpler.
    - Cons: the test's mix (243 machine recordings, 100 planner) differs from the probes' mix.
- **D34. The online look threshold.** The owner chose (b), scaled to the memory's size (2026-11-11).
  - (a) *Chosen.* **`round(1.9006 × frames^0.3583)`**, frames being the memory's own (the manifest's, summed
    per group and added on merge; indrajala-rl #69). The fit is the second sweep's: per memory, the largest
    threshold losing under half a point against threshold 10 on B2, B3 and B4 together (S 80, M 160, L 160 at
    41,060, 145,085 and 318,148 frames). For the W1 memory (375,836 frames) it is 189.
    - Pros: the owner's choice; a ceiling, below which accuracy is the same within half a point; online speed
      within 1.1-1.2 times offline.
    - Cons: the grid steps by 2 times, so the exponent is uncertain, and M and L share a reference; in memory L, E4
      fell from 69% to 65% as the threshold rose (about 100 vanishings).
  - (b) A fixed threshold (20, the deep-play probe's).
    - Pros: probed on the deep play.
    - Cons: 9 times slower than offline with a large memory (5,265 looks); not the owner's choice.
- **D35. The online memory.**
  - (a) *Chosen.* **The W1 corpus's memory alone** (its 35 groups merged, 375,836 frames; sha256
    `c1fc9f75…`). The coverage probe scored the held-out deep-play group `planner/l1-3` online with it and
    with it plus the probe's three other planner groups (472,876 frames, threshold 205): B2 86.9% against 87.0%,
    B3 85.7% against 85.5%, B4 96.9% against 97.0%. The planner's play adds nothing the online organ uses.
    - Pros: the memory is fixed before the test and holds none of the deep play; adding play bought nothing.
    - Cons: the online organ's 5-6 point loss on objects in deep play stays; coverage isn't its cause.
  - (b) The W1 corpus plus the probe's deep play.
    - Pros: covers the planner's play.
    - Cons: no gain in the probe; a larger memory and threshold.
- **D36. W3's babbling.** (New 2026-11-12, W3's plan.)
  - (a) *Chosen.* **Actions held for a random length:** each of the 12 actions drawn uniformly and held for a
    geometric number of decisions (mean 4, at most 16), with the environment's sticky actions (0.25). From every
    level's start: 4 episodes a level, up to 1,000 decisions. Training at seed 5000, the test at seed 5500 (W11 used 1000-4099).
    - Pros: held runs give full jumps and running speed, so the motion covers what the pad can do; the first
      draft's recipe ("random actions held for random lengths"); fresh, so no stage has read it.
    - Cons: a new recorder option and minutes of recording.
  - (b) W1's random play (a uniform action each decision) as the training.
    - Pros: it exists (32 levels, 4 episodes each).
    - Cons: an action changes 11 times in 12 each decision, so long jumps and full speed are rare; the probes
      of W2.1-W2.4 have read it.
  - (c) Human play.
    - Pros: natural.
    - Cons: one player's habits; the owner's time; welcome as a test source, never waited for.
- **D37. The action, factored.** (Our standing rule: factored, not flat.)
  - (a) *Chosen.* **The action as its axes:** horizontal (none, right, left), A, B, vertical (none, down, up),
    each its own head in the inverse model and its own term in the self's score.
    - Pros: motion answers the axes separately (horizontal motion answers right and left, rising answers A);
      a flat 12-way label would mix them; the score reads each axis's information.
    - Cons: the heads can give combinations SMB's 12 actions lack; harmless, since the score reads the actions
      taken.
  - (b) The 12 actions as one label.
    - Cons: flat; "B with right" and "right" become unrelated classes.
- **D38. The inverse model.**
  - (a) *Chosen.* **A small dense network in indrajala-ml, shared by every object,** trained on every
    object's rows of the training babbling, the self unknown to it (the player's label is never an input). Its
    rows are an object's motion over the last `w` decisions and the next one; its answers are the action's axes
    at the decision. Objects whose motion carries nothing about the action add noise, and the model learns
    from the one that answers.
    - Pros: D5's learned contingency on objects (Choi et al.); one model for every object and level; the
      library's own networks.
    - Cons: training (minutes); pooled rows are mostly objects that don't answer.
  - (b) Counting: per identity, the mutual information between its motion (binned) and each axis over the
    window, no model.
    - Pros: no training; exact on its bins.
    - Cons: not learned (D5); bins are a choice; reported as the probe's baseline, beside (a).
  - (c) Pixel attention (Choi et al. as published).
    - Cons: pixels, not objects; the scene has objects already.
- **D39. W3's settings, from its probe.** (New 2026-11-12.) The probe trained on the training babbling less each
  level's fourth episode and less the castles, and scored the held-out episodes and W11's L1 deep play. It
  varied `w` (1, 2, 4, 8), `after` (1, 2) and the window (8, 16, 32, 64). **The window decides it;** `w` and
  `after` barely matter.

  | window | held-out babbling: S1 | S3 | the counting baseline's S1 | deep play: S1 | S3 |
  |---|---|---|---|---|---|
  | 16 | 96.9% | 96.7% | 95.9% | | |
  | 32 | 98.4% | 98.9% | 98.7% | 99.98% | 93.7% |
  | 48 | 99.3% | | | 100% | 96.0% |
  | 64 | 99.76% (5 of 2,068 wrong) | 99.95% | 100% | 100% (24,897) | 97.7% |

  (`w` 1, `after` 1.) The wrong selves at short windows are mostly where the pad moves nothing: the player's
  information is negative and an enemy's is a little above zero (one held-out episode of 1-2 held 67 of the 109
  at window 16).
  - (a) *Chosen.* **The probe's model, fixed** (`w` 1, `after` 1, two dense layers of 64, 20 epochs, seed 0,
    the castles left out; sha256 `ba93439f…`), **at a window of 64 decisions.**
    - Pros: S1 is above the gate on both sources, with room; the test scores exactly the model the probe read.
    - Cons: no self in a life's or a shot's first 64 decisions (D40); the model is trained on 190 of the 222
      training recordings.
  - (b) A window of 32.
    - Pros: a self sooner (83% of the deep play's decisions with the player, against 77%).
    - Cons: S1 at 98.4% on babbling, under the gate.
  - (c) Retrain on all 222 training recordings.
    - Pros: a little more data.
    - Cons: a model no probe has read.
- **D40. Coverage: reported, not claimed.**
  - (a) *Chosen.* **S4,** the decisions with the player in the scene where the self is chosen and is the player,
    is reported. At a window of 64 it is 55.2% on the held-out babbling and 77.0% on the deep play: every pipe,
    death and level start opens a new shot whose first 64 decisions have no self, and babbling's lives are
    short. The gate (the self is the player where it is chosen) is S1; S3 says how often a full window chooses one.
    - Pros: the gate measures what W3 claims, that the self found is the player; the cost is on the record.
    - Cons: an agent needs a self from a shot's first decision. That remedy is a later refinement, not W3's
      bar: carry the self across a cut, or decide sooner by a sequential test (choose an identity once its
      information leads by a margin).
  - (b) Claim coverage too, with a bar from the probe.
    - Pros: one more number held or refuted.
    - Cons: it measures the shots' lengths in the test as much as the self.
- **D41. W4's data.** (New 2026-11-12, W4's plan.)
  - (a) *Chosen.* **Training:**
    - the W1 corpus: random play at seed 0, the policy's 1-1, and the owner's two sessions;
    - W3's training babbling (seed 5000);
    - W11's deep play: L1's 100 episodes of 1-1, and its every-level pass;
    - **less one held-out level, 1-3,** in all of them.

    **The probe:** W3's test babbling (seed 5500). It was read for the self only, never for a model.

    **The test:**
    - fresh babbling at seed 6000, every level, 1-3 included and reported apart;
    - L1′'s 100 episodes of deep play: read by W2.4 for the organ and by W3 for the self, never for a model.
    - Pros: each source the model meets later (babbling for W5, the planner's play for W6 and W7) is in training
      and test; the held-out level is the first draft's; fresh babbling at minutes of recording.
    - Cons: the test's deep play is 1-1 only, a level the model trains on (from other episodes); held-out play
      on another level is only babbling's 1-3.
  - (b) Babbling only.
    - Pros: one source, simple.
    - Cons: no long runs, no skilled play: W6's planner would plan in states the model never saw.
  - (c) Fresh deep play for the test too (the planner on new seeds).
    - Pros: unread episodes.
    - Cons: hours of planning on `stone` for episodes that differ from L1′'s only in their seeds; L1′'s are
      unread for any model.
- **D42. The function check's measure.**
  - (a) *Chosen.* **Fitted on one part, read on another.** Each transition is keyed: the object's kind, its last
    `k` motions, whether it is the self and the action if so, the shapes of the landscape's cells in a window
    around it, and the kinds and relative boxes of its `n` nearest objects. Its outcome is the object's next
    motion and whether it vanishes. Over the training data, each key's commonest outcome. On the probe data:
    - **open:** the share of transitions whose key was seen and whose outcome isn't its commonest;
    - **unseen:** the share whose key never was.

    Read for `k` from 1 to 16, windows from none to 6 by 4 cells, `n` from 0 to 3, by kind and for the self.
    `k`, the window and `n` are the smallest whose open share stops falling. If none leaves the self's open
    share under about 5%, D22 (c), the recurrent state, is the fallback.
    - Pros: the review's measure (P7), without its flaw (read on its own data, over keys seen twice, a subset
      that shrinks as keys grow); open and unseen apart, so a key too fine for the data shows as unseen, not as
      determined.
    - Cons: exact keys over-split: two motions a pixel apart are different keys. The model generalises where the
      check can't; the check bounds what history leaves open, not what a model learns.
  - (b) The review's measure as it was.
    - Pros: comparable with P7's figures.
    - Cons: in-sample; reported beside (a) for the self, for that comparison.
- **D43. The self on the oracle's scenes.**
  - (a) *Chosen.* **RAM's player is the self in the oracle's column;** W3's self is in the organ's (W12). The
    oracle's column holds what a perfect organ would give (O4, D20), and W3 showed the self found from behaviour
    is the player wherever it is chosen (99.86% and 100%).
    - Pros: W4 isn't held back by W3's coverage (no self in a shot's first 64 decisions); the oracle's column
      stays a column of perfect perception; W12 swaps W3's method in and reports the cost.
    - Cons: the oracle's column assumes a self an agent finds only after 64 decisions of a shot.
  - (b) W3's self in both columns.
    - Pros: the agent's own self everywhere.
    - Cons: a quarter of the decisions with no self, and the model's error mixed with W3's coverage.
- **D44. The token, encoded.**
  - (a) *Chosen.* **Kinds and shapes as indices among the training's commonest, the rest one "other" each;**
    numeric boxes.
    - **An object:** its kind (one-hot); its last `k` motions (each step's change of top, left, bottom and
      right, clipped to 16 pixels); its size; the self flag; and the action's axes if it is the self (D37).
    - **The landscape window:** each cell's shape index, one-hot, with "unseen" and "outside" its own indices.
    - **Neighbours:** the `n` nearest objects' kinds and their boxes relative to the object.
    - **Outputs:** the next motion as two categorical choices (rows and columns, -16 to 16 pixels and
      "beyond"); whether it vanishes; its next kind.
    - Pros: D23 with nothing new in the library; game-agnostic; every input a camera gives; shapes, not colours
      (D28).
    - Cons: the one-hot window is wide (cells times shapes); a shape first met in a held-out level is "other".
  - (b) Shapes embedded (a learned vector per shape).
    - Pros: narrower inputs; shapes that act alike can share.
    - Cons: an embedding layer to add or emulate; kept for a diagnosed need.
- **D45. What W4 claims.**
  - (a) *Chosen.* **The plan's gate:** on held-out play, per kind with enough transitions, the model's next box
    is exactly right more often than the copy baseline's (each object keeps its last motion). **Reported:** the
    error after `h` decisions of rollout against the copy baseline (`h` 1 to 16), vanishings predicted, the
    held-out level apart, and the function check. W4's gate proper is W6's (D24): control.
    - Pros: a bar the probe can set; the measures W6 and W5 need, on the record.
    - Cons: next-box accuracy is pixels, not control; D24 says so, and W6 reads control.
  - (b) Rollouts within a pixel at stated rates (the first draft).
    - Cons: as D24 (b).
- **D46. W4's settings, from its probes.** (New 2026-11-12.)
  - **The function check** (indrajala-rl `ee91387`; fitted on the W1 corpus, W3's training babbling, W11's L1
    100 and its every-level pass, less 1-3; read on W3's test babbling). Its first run read the self's action
    a decision early (fixed in #82; the self was open in 62% of its seen keys at `k` 1). Corrected, among keys
    seen in training:
    - **history keeps helping up to `k` 16:** the self is open in 62% at `k` 1, 26% at 4, 4% at 8 (window 4×4,
      one neighbour) and under 1% at 16;
    - **a 4×4 window helps and 4×6 adds little; one neighbour helps and a second adds nothing.**
    - **Exact keys over-split:** past `k` 4 most keys read are unseen (98% of the self's at `k` 8), so the check
      bounds history but can't choose among `k` 8 and 16. The self's open share is under 5% from `k` 8, so D22
      (c), the recurrent state, isn't needed.
  - **The model's probe:** `k` 4, 8 and 16 (window 4×4, one neighbour; dense 128 and 128; 10 epochs; 38 kinds and
    64 shapes kept), read on W3's test babbling.

    | `k` | all: model, copy | the self: model, copy | kinds above copy | the self's rollout error at 8 and 16 decisions (copy) |
    |---|---|---|---|---|
    | 4 | 41.9%, 23.4% | 26.2%, 11.3% | 12 of 12 | 12.2 and 22.7 px (34.0 and 65.2) |
    | 8 | 43.0%, 22.9% | 27.5%, 11.1% | 12 of 12 | 11.1 and 20.0 px (33.8 and 66.5) |
    | 16 | 42.2%, 21.9% | 26.7%, 11.1% | 11 of 12 (bubbles under) | 12.7 and 23.4 px (34.2 and 65.7) |

  - (a) *Chosen.* **`k` 8, a 4×4 window, one neighbour: the probe's model, fixed** (sha256 `5d59b007…`).
    - Pros: the best of the three on every measure but the rest's short rollouts; every kind above copy; the
      test scores what the probe read.
    - Cons: the self's next box is exactly right only 27% of the time, and its rollout drifts 11 pixels in 8
      decisions. W6 reads whether that is enough to plan with.
  - (b) Improve the self first: its past actions in the token (how long a button is held sets a jump's height),
    and more epochs (the loss still fell at the tenth).
    - Pros: likely a better self.
    - Cons: W4's gate is met without it; whether control needs it is W6's question. These are W6's first
      fallbacks (D30).
- **D47. W4's claims and bars.**
  - (a) *Chosen.* **Claimed on babbling,** the source the probe read; **deep play reported.** W11's L1 100 is
    in training (D41), so no deep play outside training was probed.
    - **M1, the other objects:** pooled (the self left out), the model is exactly right at least 15 points more
      often than copy. The probe: 59.5% against 35.4%, +24.1.
    - **M1′, per kind:** every kind (not the player) with at least 500 test steps is no more than 1 point under
      copy. Some kinds are nearly still, and copy is nearly perfect on them (slot 32: 99.75% against 99.69%),
      so "above" would be a coin flip there.
    - **M2, the self:** at least 10 points over copy. The probe: +16.4.
    - Pros: W4's gate as planned ("better than the copy baseline on held-out play, per kind"), read so that a
      kind that barely moves can't refute it by chance.
    - Cons: deep play isn't claimed.
  - (b) "Above copy" for every kind.
    - Cons: refuted by noise on the kinds that barely move.
- **D48. The model as the planner's world.** (New 2026-11-12, W6's plan.)
  - (a) *Chosen.* **A scene model behind D25's `Model` protocol** (`save`, `restore`, `step`):
    - **its state:** each object in the decision's scene with its last `k` boxes, its kind and whether it is the
      self, and the landscape of the scene's view;
    - **a step:** the action applies to the self; W4's model moves every object one decision; a predicted
      vanishing removes it;
    - **cells beyond the view** are outside, as at the view's edge in training;
    - **objects** that would appear later aren't there.
    - Pros: the planner unchanged (D25: one planner for the emulator and the model); what W4 claims is what is
      rolled.
    - Cons: no new objects in a rollout (an enemy that walks in unseen); the camera's view frozen at the plan's
      start.
  - (b) A model of the whole screen (the view moving with the self).
    - Cons: W4's model has no view; that is the transformer's (D4) or a later stage's.
- **D49. What a rollout scores on the model.**
  - (a) *Chosen.* **W11's score from the self's predicted box:**
    - **progress:** the goal's distance, as W11's `distance`, closed each decision, in cells;
    - **reaching** a goal in the model:
      - land: the self's feet on the cell's top, its centre over the column, and no vertical motion for a step;
      - bump: the self's head at the cell's bottom while rising, then not rising;
      - stomp: the self's feet within a few pixels of the enemy's top as the model says the enemy vanishes or
        changes kind;
    - **death:** the self vanishes, or its box passes the screen's bottom.

    **The judge is RAM's:** an attempt reaches its goal when W11's `reached` says so in the real game.
    - Pros: W11's goals and judge unchanged; the model only steers.
    - Cons: the model-side tests are proxies (a bump's block change isn't modelled); a proxy that fires early
      wastes decisions, not the goal.
  - (b) A learned reward head (D26's) for each goal.
    - Cons: D26 is W7's; three heads to train before control is tried.
- **D50. The cost.**
  - (a) *Chosen.* **Candidates rolled together:**
    - each horizon step is one forward pass over every candidate's objects, with the features built in arrays;
    - stickiness expected by `exact` 3, W11's battery setting;
    - the budget is the probe's, held under about a second a decision on one core.
    - Pros: W11's battery, 381 attempts of up to 60 decisions, then takes hours on `stone`, not days.
    - Cons: a batched rollout to write and test against the unbatched one.
  - (b) The unbatched rollout (`world_model.rollout`, as W4 scored).
    - Cons: about 8 seconds a decision by estimate; days for the battery.
- **D51. The battery and the reference.**
  - (a) *Chosen.* **W11's battery recipe on L1′'s 100**, which W4 didn't train on:
    - a state every 480 core frames with the player standing, one goal of each kind in view drawn by seed, at
      most 60 decisions an attempt, sticky 0.25, the real game stepped forward and never restored;
    - **the reference** is W11's planner on the emulator, on the same attempts and seeds, in the same run.

    **The gate (the revision's):** per kind, the model's rate at least 80% of the reference's.
    - Pros: the gate's ratio read on matched attempts; goals from play the model never trained on.
    - Cons: the battery's states are 1-1's, a level the model trained on (other episodes). The every-level pass's
      states would test other levels, but the model trained on that pass too (D41).
  - (b) The reference's rates from W11's run (L1's states).
    - Cons: different states, and L1 is the model's training.
- **D52. The scene and the self while acting.**
  - (a) *Chosen.* **The oracle's scene at each decision, RAM's player as the self** (D43). The organ's column is
    W12's (the online organ, the belief scene and W3's self).
    - Pros: control is tested on perfect perception first (O4).
    - Cons: as D43.
- **D53. The objects in the model's state.** (New 2026-11-12, W6's first PR, indrajala-rl #84.) A rollout needs
  `k` motions for each object, and an enemy that came into view in the last `k` decisions (32 frames) doesn't have
  them yet.
  - (a) *Chosen.* **Only the objects seen at every one of the last `k + 1` decisions;** a stomp goal's enemy
    without that history is **a fixed place:** the planner closes in on its box at the decision, and the model
    can't say it is stomped. It is in the state from its `k + 1`th decision in view, since the state is made
    again every decision.
    - Pros: every object rolled is one W4 scored (its inputs as in training); nothing invented.
    - Cons: a newly arrived enemy is neither a neighbour nor a mover in the rollout for its first 8 decisions;
      a stomp goal drawn on one is steered by a frozen box until then.
  - (b) Pad the missing history with the earliest box (no motion).
    - Pros: every object in view is in the rollout.
    - Cons: an object with no motion in its history and then a jump is what W4 never saw; its predictions are
      unscored.
- **D54. The oracle's boxes against RAM's places.** (New 2026-11-12, from a probe: indrajala-rl
  `scripts/scene_coordinates.py`, the greedy policy's 1-1 recordings, 6,877 decisions.) The goals are written in
  RAM's places (W11) and the model's boxes are the oracle's visible pixels, drawn from the RAM one frame before the
  picture.
  - **The player:** the oracle's bottom is `player_box`'s bottom + 1 on every decision but one; its centre is
    within half a pixel; its top is 1-2 lines lower (3 when big). Against the RAM after the picture, the box lags
    by a frame's motion. The dying player's sprite is shorter.
  - **Enemies:** the visible top is no fixed offset from RAM's `y` (a Goomba's `y + 9`, a Koopa's `y + 1` or
    `+ 2`).
  - (a) *Chosen.* **The feet's line is the oracle box's bottom, the head its top less 1, the centre as it is; a
    stomp is read against the enemy box's top** (where the feet land), not RAM's `y`. The player's offsets are
    tested on 1-1 (`--emulate`).
    - Pros: the model-side tests read where things are on the screen; one offset for every enemy kind.
    - Cons: the stomp's distance differs from W11's by a kind's offset; the model only steers, and RAM judges.
  - (b) A table of offsets per enemy kind, to reproduce W11's `distance` exactly.
    - Cons: a game table for a proxy; kinds not in 1-1 unmeasured.
- **D55. The batched planner's first decision.** (New 2026-11-12.) With no previous action (an attempt's first
  decision), W11's unbatched planner scores `exact`'s candidates by random sticky draws after the first decision (a
  quirk of its code, registered as it is). A batched model can't draw (one rollout a pattern).
  - (a) *Chosen.* **The batched path expects the sticks of the next `exact - 1` decisions exactly** (the first
    can't stick: nothing to repeat); from the second decision on, both paths give the same scores (tested). The
    reference keeps W11's planner unchanged.
    - Pros: the right expectation; W11's registered planner untouched.
    - Cons: the model's and the reference's first decisions are scored a little differently.
  - (b) Change W11's planner to match.
    - Cons: changes a registered planner after its result.
- **D56. After W6's probe: the run with W4's model as it stands.** (New 2026-11-12, from the probe: "W6's probe"
  below.) The probe put the model at 91% of the reference on land, 32% on bump and 0% on stomp, against a gate of
  80% for each kind.
  - (a) *Chosen.* **No registered run with W4's model as it stands; its fallbacks first (D30: D46 (b)), with
    D57's death on the model, then a probe and the registration.** A cell that can't succeed isn't run (the
    feasibility rule), and bump at 32% of the reference can't reach 80% on 100 recordings.
    - Pros: no hours spent on a known refutation; the probe's diagnosis says what to fix.
    - Cons: no registered figure for W4's model as it stands; the probe's 79 attempts (L1's states, in the model's
      training) are its record.
  - (b) Register and run C1-C3 now, then the fallbacks.
    - Pros: a registered refutation.
    - Cons: an hour of `stone` for a result the probe already gives; runs a cell that can't succeed.
- **D57. Death on the model: an enemy's touch.** The oracle's player doesn't vanish when an enemy hits it (its
  dying sprite stays in view, and falls off the screen's bottom only after the horizon), so D49's death can't see
  the probe's deaths at enemies (5 of 8 stomp attempts died).
  - (a) *Chosen.* **The self also dies in the model when its box overlaps an enemy's (a kind the battery can
    stomp: `smb_goals.STOMPABLE`) with its feet below the enemy's top by more than the stomp tolerance;** a stomp
    is tested first. The kinds are the battery's (1-1's enemies), in the game's goal module.
    - Pros: the planner sees a touch as the death it is in the game; one geometric test, as land and bump are.
    - Cons: a proxy (the game's hit boxes differ from the drawn ones); kinds outside the battery not covered.
  - (b) Learn it: the model predicting the self's death (a head, or the dying sprite as a kind).
    - Cons: deaths are rare in training; D26's reward heads are W7's.
- **D58. The self's past actions (D46 (b)).** The probe's traces: the model gets a jump's onset wrong both ways.
  A fresh A press that jumps is predicted not to rise (48 decisions), and an A held from the decision before,
  which can't jump in the game, is predicted to rise (41). Whether A was held is not in its inputs.
  - (a) *Chosen.* **The self's last `k` actions in its token** (each decision's axes, one-hot, the actions that
    made its last `k` motions), trained on W4's tables unchanged; **three models, so the two changes are read
    apart:** W4's inputs at 30 epochs, the actions at 10 and the actions at 30. Each is scored as W4 was (M1,
    M2, rollouts on W3's test babbling), then probed on W6's battery (L1's states). The best goes to W6's
    registration, with W4's claims re-read for it.
    - Pros: general (no game's rule about held buttons); the history the motions already have; the actions
      and the epochs read apart.
    - Cons: 80 more inputs; three trainings (about 2.5 hours each on one core, run together).
  - (b) Only the previous decision's action.
    - Pros: smaller; enough for a fresh press.
    - Cons: a jump's height depends on A held for longer.
  - (c) A count of decisions each button has been held.
    - Cons: a hand-made feature; (a) can learn it.
- **D59. Only goals the scene shows.** (New 2026-11-12, W6's probe's second round.) W11's goals come from RAM's
  metatiles, and in 1-1 one of them is the hidden 1-up block (row 6, column 64). Its cells are drawn as the sky's
  shape, so no scene, the oracle's or the organ's, shows it. It was 16 of the probe's 28 bump attempts. The
  reference reached 15 of them through RAM; the model 3, by chance.
  - (a) *Chosen.* **The battery draws only goals the scene shows:** a land or bump cell drawn unlike the empty
    metatile beside it, and a stomp target that is drawn. Both paths draw from the same goals, by the same seeds
    (indrajala-rl #89).
    - Pros: control is tested on what a model of scenes can know; the reference stays matched.
    - Cons: W6's battery differs from W11's (its rates aren't W11's); a cell drawn like its empty neighbour for
      another reason would be left out too.
  - (b) Keep them and report hidden goals apart.
    - Cons: the gate's ratio would hold a kind of goal no scene shows.
- **D60. A stomp on the model is the contact.** (New 2026-11-12.) A stomped enemy keeps its kind and stays in view
  (flattened) for a while in the oracle's scenes. So D49's stomp test (the enemy vanishing or changing kind as the
  feet are on it) never fired in a rollout: probe 3's 63 stomp attempts had no model-side stomp at all. With
  D57's touch, an enemy was only a danger, and 48 ran out of decisions.
  - (a) *Chosen.* **The self falls in the step with its feet coming down onto the enemy's top** (from at most the
    stomp tolerance below it before, to at least the tolerance above it after), the two overlapping in columns;
    a target without history (D53) can be landed on too (indrajala-rl #90).
    - Pros: the contact the game registers; it doesn't depend on the model predicting the squash.
    - Cons: a proxy; an enemy the game doesn't let be stomped (none in the battery) would pass it.
  - (b) Learn the squash: a stomped enemy's flattened box as its own kind.
    - Cons: a change to the oracle's kinds and W4's training, for what a contact test reads directly.
- **D61. After the second round.** (New 2026-11-12.) With the self's past actions (D58), visible goals (D59), the
  stomp as a contact (D60) and the touch as a death (D57), the probe holds land at 93.5% of the reference, bump
  at 65.1% and stomp at 44.0%. The tests' tolerances don't change stomp much (probe 5).
  - (a) *Chosen.* **D30's next fallback: D4's transformer over the scene's objects, planned as its own round**
    (its decisions, a probe, then W6's registration with it). **First, a diagnosis** that settles what it must
    fix: the enemy's predicted boxes traced in stomp attempts beside the self's (is the miss the enemy's motion
    near contact, the self's arc, or the planner's horizon?), and the high bricks' climbs traced in bump.
    - Pros: the plan's order; the model is what's left, and the diagnosis keeps the next model's plan to what
      the misses show.
    - Cons: a new model and its training before W6's registration.
  - (b) Register W6 now at the gate (80% per kind).
    - Cons: bump and stomp can't reach it on the probe's evidence (the feasibility rule).
  - (c) Lower the gate.
    - Cons: the gate is the revision's (O3's table); not a choice made after the data.
- **D62. A stomp's enemy out of view.** (New 2026-11-12, D61's diagnosis.) In 10 of the 19 stomp attempts that the
  reference reached and the model ran out of decisions on (or left unconfirmed), the enemy was out of the scene for
  part of the attempt. Then the model has no target, and the distance is 0, so the planner has no direction. The
  reference reads RAM and goes on.
  - (a) Hold the enemy at its last box in a scene, as a target without history is held where it is (D53).
    *Tried in probe 7 and refuted:* stomp 22 of 63 again, and the unconfirmed went from 3 to 12 (the planner
    "stomps" the stale place). Not merged.
  - (b) *Chosen.* **Object permanence in the model:** the next model's round (D61's (a)) keeps an object that leaves
    the view, rolled on by the model, and the battery stays as it is meanwhile.
    - Pros: it is a world model's job; one fix serves planning around anything off-screen, not only stomps.
    - Cons: the state must carry unseen objects (the scene format, the training's targets); more to build in that
      round.
  - (c) Roll the last box on at its last velocity, in the battery.
    - Cons: a hand-made motion model beside the learned one; it is wrong at walls and turns.
  - (d) Leave out the attempts whose enemy leaves the view.
    - Cons: a filter chosen after the data and tied to failure; the reference would no longer be matched in kind.
- **D63. The next fallback: rollout training (amends D61's (a)).** (New 2026-11-12, from models2 and probe 8.) D23
  kept D4's transformer for a diagnosed *interaction* the small network can't express. The diagnosis found none:
  the enemy's error is 0.3 px. A larger network (three layers of 256) gives the self's one-step and rollout
  measures a lift, but no lift in control (probe 8). So the model's one step is not what fails; its rollouts are,
  and the planner reads 16 decisions of them. W6's fallback is "W4's fallbacks, chosen by where the rollouts
  break", and their order is: more history (done: `k` 16 and the past actions), **rollout training**, D4's
  transformer, the recurrent state, rules.
  - (a) *Chosen.* **Rollout training by DaD** (Data as Demonstrator; Venkatraman, Hebert and Bagnell, AAAI
    2015), on the current form with the past actions.
    - The method:
      - train one step, as W4 does;
      - roll the model along the training recordings (their actions, the shot's map);
      - pair each state the model reached with the target that leads back to the recording (the true next box
        less the predicted box);
      - add those pairs to the data, retrain, and repeat for a few rounds.
    - The training tables are written again with their maps (`--maps`), which a rollout needs.
    - Judged first offline (the self's rollout error at 8 and 16 decisions, the self in the air), then by the
      battery.
    - Pros: the plan's order; it targets compounding error directly; no gradient through a rollout is needed
      (the steps are argmax over categories), and nothing new in the library.
    - Cons: a correction target can be a motion the game never makes (a step back toward the recorded arc);
      several rounds of rollouts and training.
  - (b) Scheduled sampling: the model's own states as inputs, the true motion as the target.
    - Pros: every target is a motion the game makes.
    - Cons: nothing pulls a drifted state back, so its errors remain; kept as the variant if (a)'s targets
      mislead.
  - (c) D4's transformer now (D61's (a) as written).
    - Cons: no interaction need was found; it is library work, and rollout training would still be needed (D4
      trains on rollouts).
  - (d) Stop and put it to the owner (D30).
    - Cons: W6 isn't registered or refuted, and the plan's fallbacks aren't spent.
- **D64. A bump on the model is the contact.** (New 2026-11-12, probe 9's traces.) The game registers a bump
  inside the decision the head reaches the block, while the self still rises. D49's test waited for the rise to
  stop with the head at the cell's bottom, so it fired a decision late, and only where the model predicted the
  stop. In probe 9 the model claimed 5 of the 45 bumps reached, with its boxes within a pixel of the truth.
  - (a) *Chosen.* **The head comes up to the cell's bottom line in a rising step** (from below it to within the
    tolerance under it, or past), or (D49) the rise stops with the head there; under the cell's column
    (indrajala-rl #95).
    - Pros: the contact the game registers, as D60 for the stomp; it doesn't need the model to predict the stop.
    - Cons: a head passing the line beside a block within `bump_columns` would count.
  - (b) Keep D49's test and widen its tolerances.
    - Cons: the lag stays; probe 5 found tolerances matter little.
- **D65. A landing on the model is the contact.** (New 2026-11-12.) The same lag: D49's land test wanted a step
  with no vertical motion, while the game has landed in the decision the feet arrive. In probe 9, 75 of the 168
  landings reached were never claimed.
  - (a) *Chosen.* **The feet at the cell's top in a step that doesn't rise** (arriving or standing), over its column
    (indrajala-rl #95).
    - Pros: as D64.
    - Cons: a fall that only grazes the line within the tolerance counts.
  - (b) Keep D49's still step.
    - Cons: the lag.
- **D66. The box's place within its cell in the token.** (New 2026-11-12, probe 10's traces.) The token holds
  each object's window of landscape cells (8-pixel tiles), but not where its box sits within the window's anchor
  cell. So the model can't tell a box one pixel over a ledge from one seven pixels over, and contacts at edges
  are decided by exactly that. Probe 10's traces of the self:
  - falling steps: 208 phantom landings (the model stops the self, which falls on) and 375 falls too slow or fast,
    among about 2,059;
  - walking off a ledge: 33% of steps off by 4 px or more;
  - the apex or a head hit: 14%.

  A larger network and rollout training (probes 8 and 9) didn't move control, which fits an input that is
  missing. The function check (D46) keyed on the same inputs and so couldn't see the gap: a feasibility miss
  (`information-flow.md`'s rule), recorded here.
  - (a) *Chosen.* **The top line's and the left column's offsets within the anchor cell, one-hot**
    (`Settings.offset`; indrajala-rl #96), from the grid's top line (the views'; the planner's `Landscape.top`).
    - Pros: the exact position a camera gives; game-agnostic; 16 inputs.
    - Cons: a model retrained; old models have no offset (they load unchanged).
  - (b) The window at pixel resolution.
    - Cons: 64 times the window's inputs, for what two offsets say.
  - (c) The absolute box.
    - Cons: not translation-invariant; a level's place is not the physics.
- **D67. An ensemble first, then the transformer.** (New 2026-11-12, after probes 11 and 12.) Six models, two
  test fixes (D64, D65), an input (D66) and three horizons all leave the model in one band: land about 90%, bump
  62-76%, stomp 36-68% of the reference. D4's form has three parts: the transformer, an ensemble for
  disagreement (D6; PETS's particles), and rollout training (tried, D63). The probes found no interaction for a
  transformer to fix. They did find a planner acting on one model's argmax errors (phantom landings, false rises,
  incoherent boxes), and different seeds' members differ (the self exact from 32.9% to 39.7%).
  - (a) *Chosen.* **An ensemble of five one-step members** (256x3, past 8, offset, seeds 0-4). Each candidate
    sequence is rolled in every member, and its score is the members' mean (or their minimum: pessimism)
    (indrajala-rl #97). Probe 13: a member alone, the mean and the minimum.
    - Pros: D4's own remedy for model error the planner exploits; nothing new in the library; members train in
      about 10 minutes, three at a time (7.5 GB each).
    - Cons: five times the model's work a decision.
  - (b) D4's transformer now.
    - Cons: no diagnosed need; it is library work.
  - (c) Stop and put W6 to the owner (D30).
    - Cons: D4's remaining parts are untried, and W6 isn't registered.

- **D68. Young objects in the model, with their age (amends D53).** (New 2026-11-12, probe 13.) The ensemble
  (D67) lifts land to 97.8% of the reference and stomp to 60.0%, but bump stays at 73.0%. The traces put most
  stomp misses on D53's rule: an object enters the model's state only with boxes at its last `k + 1` decisions
  (9 decisions at `k` 8). Before then, a stomp target is held where it is and no other object sees it as a
  neighbour.
  - Of the 50 stomps the reference reaches, 35 begin with the target too young for the model. The reference
    stomps those in a median of 12 decisions; the model, when it gets there, in 39.
  - Of the 20 misses, 16 begin that way. In 7, the enemy leaves the scene later (D62's case).
  - Of bump's 18 misses, 15 are high bricks (row 3). The self's one-step error in them is 0.1-1.3 px, and many
    climbs come within a few pixels of the height that bumps. That is planning on a model that is close, not a
    missing input.

  The options:
  - (a) *Chosen.* **Every object in view is in the model's state, with its age** (the motions it has, up to `k`).
    A young object's missing motions are zero, and its age is one-hot (`k + 1` values). Training reads young
    steps in the same way (`train --young`). In the planner, an object's age grows by one a step. This is D4's
    own token, which holds an object's age. Then probe 14: the ensemble retrained so, with the battery as in
    probe 13.
    - Pros: aimed at the cause of most stomp misses; nothing new in the library; members train in about 10
      minutes each; a newly seen enemy also becomes a danger the model can see.
    - Cons: a young object's motion is guessed from fewer steps; more training rows; it doesn't touch the
      high bricks, which need bump to rise from 73% on its own.
  - (b) D4's transformer with object permanence (D62 (b)), as D67 ordered it.
    - Cons: no interaction is diagnosed; permanence reaches 7 of the 20 stomp misses; library work. The young
      targets would still be left out.
  - (c) Stop and put W6 to the owner (D30).
    - Cons: a cheap remedy aimed at the main cause is in sight.
  - (d) Register W6 with the mean ensemble.
    - Cons: bump and stomp are below the gate on the probe's states (the feasibility rule).
- **D69. W6 to the owner (D30).** (New 2026-11-13, probe 14.) With young objects (D68), stomp rose from 60.0%
  to 70.0% of the reference, and its stomps now take the reference's time (a median of 11 decisions against 12).
  Land holds at 97.3%. Bump stays at 73.0%. Bump has stayed between 62% and 76% through nine configurations:
  - three sizes of network;
  - rollout training (D63);
  - the contact tests (D64, D65);
  - the box's offset (D66);
  - three horizons;
  - the ensemble (D67);
  - young objects (D68).

  What is left:
  - **Bump:** 16 of the 17 misses are the high bricks (row 3), which are reached only by climbing onto the
    lower bricks first and jumping from there. In most of the traces the self stays below the lower bricks,
    jumping, and doesn't get onto them; the reference climbs on. The self's one-step error is about a pixel. That is
    a detour onto a ledge, planned on a model that is close but wrong at exactly the ledge's contacts (D66's
    traces). No fix diagnosed so far reaches it.
  - **Stomp:** 6 of the 17 misses are D62's (the enemy leaves the scene). If permanence reached all of them,
    stomp would be 41 of 50, 82%. The other 11 die or run out of decisions with the enemy in view.

  The options:
  - (a) *Chosen.* **Stop W6 here and put it to the owner (D30, O7),** with what the fallbacks showed (this
    round). The routes the owner can choose between:
    - object permanence (D62 (b)) for stomp, with a diagnosis of the ledge climbs for bump, as one more round;
    - D4's transformer;
    - the gate for bump (O3's table) is the owner's to set;
    - W5 and W7 on the model as it is, with W6 reported unregistered.
    - Pros: D30's rule for a stage that its fallbacks haven't carried through on the oracle's scenes; no route
      left in the plan is aimed at a diagnosed bump cause; the remaining choices change the plan's scope or gate.
    - Cons: a stage stops with stomp's remedy (permanence) in sight.
  - (b) Object permanence now, then put it to the owner.
    - Cons: at best it brings stomp to the gate; bump would still be under it, so W6 could not be registered,
      and the owner's call would be the same, after a round of building (the state, the scene format and the
      training's targets for unseen objects: D62 (b)'s cons).
  - (c) D4's transformer.
    - Cons: no interaction is diagnosed for it to learn, for bump or stomp; library work.
  - (d) Register W6 with the young ensemble.
    - Cons: bump and stomp are below the gate on the probe's states (the feasibility rule).

- **D70. Object permanence dropped (amends D62 (b)).** (New 2026-11-13, O7's route 1.) Of probe 14's 17 stomp
  misses, 6 had the enemy leave the scene. In none of them did it come back:
  - 2 enemies fell into a pit (their last boxes at y 227-239);
  - 3 left by the screen's left edge, where the game erases enemies;
  - in 1, the self left the area (its x jumped to 26).

  So an object kept by the model would be one the game has removed. Permanence has no target here.

  The options:
  - (a) *Chosen.* **Drop permanence from the round.** These 6 misses are the planner's: the reference reaches the
    enemy before it leaves. The round's work goes to bump.
    - Pros: nothing built without a target; the round goes to the kind furthest from the gate.
    - Cons: the 6 misses stay, with no remedy named.
  - (b) Build permanence as D62 (b) planned it.
    - Cons: the targets are gone in the game too; a kept object would be a stale target, the failure of D62 (a)
      (probe 7).
  - (c) Leave those attempts out of the battery.
    - Cons: D62 (d)'s: a filter chosen after the data and tied to failure.
- **D71. A longer history for the jump (`k` 16, past 16).** (New 2026-11-13, the climb diagnosis.) Following the
  reference's actions on bump, the model's foresight of the high bricks falls from 0.94 one decision ahead to
  0.45-0.50 at 12-16 (the other rows: 0.86-1.00 throughout). The self's one-step vertical error in those climbs
  rises from 0.2-0.9 px in a jump's first 9 decisions to 0.4-2.0 px after. The hypothesis is that at `k` 8 the
  takeoff has left the self's history by then, so the model no longer knows where in the jump the self is.
  - (a) *Chosen.* **`k` 16 and past 16**, the young ensemble otherwise as probe 14's; probe 15, with the
    foresight check (`follow_check.py`).
    - Pros: two flags; tests the hypothesis directly; W4's function check offered `k` 16.
    - Cons: wider inputs; 9.5 GB a training.
  - (b) The decisions since takeoff as an input.
    - Cons: a hand-made feature that names the game's physics (the plan learns the method, it doesn't hand it in).
  - (c) D22's recurrent state.
    - Cons: library work, before the cheap test of the same idea.

  *Refuted* (probe 15): foresight and the late-jump error barely move, and bump stays at 73.0%.
- **D72. A deeper window below the self (`--window 6x4`).** (New 2026-11-13, probe 15's traces.) Arriving from a
  fast fall (4 px or more a decision), the members put the self's bottom within 1 px of the truth on 71% of
  arrivals on the ground but 31% on raised surfaces (median error 6 px; probe 14). The 4x4 window (`sub_window`: one row
  above the self's top cell) shows at most one 8 px row below a 16 px self, and none when the box's top sits
  partway into its cell. The self falls up to 16 px a decision, so the surface it lands on can be out of the
  window. W4's function check never varied the rows (0x0, 2x2, 4x4, 4x6). That is a gap of the kind the
  information-flow register's row 18 names: an input the cell can't see.
  - (a) *Chosen.* **A window of 6 rows by 4 columns**, from the tables' stored 6x8 (16 px below the box and above
    it). Probe 16: the young ensemble so, with the foresight and arrival checks.
    - Pros: inputs the tables already hold; aimed at a diagnosed blind spot.
    - Cons: 1,840 features against 1,304; 12.0 GB a training, one at a time.
  - (b) Eight rows or more.
    - Cons: the tables hold six; they would be built again (`dad/tables/run.sh`).
  - (c) Leave the window.
    - Cons: a feasibility gap left in place.

  *Refuted for control* (probe 16): raised arrivals improve (44%, median 4 px), and foresight and bump don't.
- **D73. W6 to the owner again (D30).** (New 2026-11-13, probes 15 and 16.) The round's two remedies were each
  aimed at a diagnosed cause, and neither moved control:

  | model | land | bump | stomp |
  |---|---|---|---|
  | young, `k` 8, 4x4 (probe 14) | 97.3% | 73.0% | 70.0% |
  | `k` 16 (probe 15, D71) | 96.8% | 73.0% | 74.0% |
  | 6x4 window (probe 16, D72) | 97.8% | 68.3% | 68.0% |

  Bump has now stayed between 62% and 76% through eleven configurations. Its misses are the high bricks (16-19
  of 17-20). Rollouts of the reference's own climbs leave the truth mostly in the air (rising, falling, the
  apex) and where the sprite's box changes size, not at the contacts the round aimed at.

  The options:
  - (a) *Chosen.* **Stop W6 and put it to the owner (D30, O8),** with this round's findings. The routes:
    - the self's motion in the air as rules (D23; D63's last fallback);
    - D4's transformer;
    - the gate for bump (O3's table) is the owner's to set;
    - W5 and W7 on the model as it is, with W6 reported unregistered.
    - Pros: D30's rule; the round the owner chose is spent; each route left changes the model's form, the
      gate or the plan's scope.
    - Cons: a stage stops again.
  - (b) Register W6 with probe 15's ensemble.
    - Cons: bump and stomp are below the gate on the probe's states (the feasibility rule).
  - (c) Another cheap probe (`k` 16 with the 6x4 window).
    - Cons: each moved its own measure a little and control not at all; a growing matrix of probes.
  - (d) The self's air motion as rules now.
    - Cons: it changes the plan's form, from a learned model to a partly given one: the owner's call.
- **D74. O8 answered: W6's fifth round.** (New 2026-11-13.) The owner, on an analysis of the briefing
  ([briefing-2026-11-13-smb-w6.md](../reviews/briefing-2026-11-13-smb-w6.md)) and of the probes' traces: "you
  pick which solutions you think we should try, and in what order", and "check that the solution doesn't rather
  lie in an unrelated part that we haven't been looking at". The analysis is "W6's fifth round" under the stages,
  findings F1-F9. In short: the bump shortfall is one brick approached from one side (F1); its climb is a jump
  that clears the ledge by 1-2 lines, which half the members foresee (F2); the planner then stands still (F3);
  and the planner's own scoring, never looked at, lets one member's false death outweigh a reach (F7).
  - (a) *Chosen.* **A fifth round in five steps, cheapest and most informing first, each step run only if the
    one before leaves the gate unmet:** R0 measure (D75); R1 the planner on the model (D76); R2 the model
    retrained on the planner's own play (D77); R3 the self's box factored (D78); R4 the self's air motion as
    rules (D79). The transformer is dropped and the gate stays (D80). The first step whose probe meets every
    bar goes to W6's registration on L1′ (D30).
    - Pros: R0 and R1 cost minutes and no training, and R0 says which later steps have a target (the
      feasibility rule); each step is one probe with its bars set here, before its data; the order keeps the
      model's learned form as long as it can; the round ends with an answer either way.
    - Cons: up to five steps before the form changes; the step likeliest to fix the climb alone (R4, in the
      analysis's estimate) comes last.
  - (b) Rules first (O8's route 1).
    - Pros: the only route that can be exact at the apex.
    - Cons: the model becomes partly given before the cheap causes are excluded; if F7 is the cause, an exact
      self still loses to another object's false touch.
  - (c) The planner's own play first (R2).
    - Cons: a training round before a measure that costs minutes; its probe can't tell a model gain from a
      planner fault.
  - (d) Stop: set the gate or go on unregistered (O8's routes 3 and 4).
    - Cons: the owner asked for solutions; nothing learned about the model.
- **D75. Measure first: the planner's view, and the reference against itself (R0).** (New 2026-11-13.) The traces
  hold what the self did and what the first member predicted. They don't hold what the planner saw: how many
  candidates reached the goal in any member, how many died in any member and of what, or what standing still
  scored. And the gate is a ratio to one run of the reference, whose own spread from seed to seed isn't known
  (it reaches the stair-side brick 8 times in 19).
  - (a) *Chosen.* **Both, as tools:** `planner_battery.py --trace` also writes each decision's candidates
    (per member: reached, died and the death's kind (vanished, the bottom, a touch), the score; and the chosen
    one's), and a new reading in `follow_check.py` sorts every decision where the self stands still, and every
    missed attempt, into F8's classes. The reference runs twice more on bump and stomp with other seeds.
    - Pros: durable measures, built into the work in hand; R1's cells are chosen by data, not by guess; the
      gate's noise is known before anything is registered against it.
    - Cons: one PR and about an hour of `stone` before any remedy.
  - (b) Go straight to R1's cells.
    - Cons: three cells run blind, and a pass or a failure that can't be read.
- **D76. The planner on the model: what W6 holds fixed, and R1's cells (amends D48 and D51).** (New 2026-11-13.)
  W6 "keeps everything else", the planner's settings included. But the settings were W11's, set for an exact,
  single world. On an ensemble of inexact members, three of them are choices nobody made: the members' mean
  with a death at -1,000 (F7), 24 candidates, and the bump test's width (F5).
  - (a) *Chosen.* **W6 holds fixed the goals, the judge, the attempts and seeds, the limit of 60 decisions,
    the horizon, the stickiness and the real game's frames. How a candidate is scored across members, how many
    candidates are rolled and the model-side tests belong to the model's side and may differ from the
    reference's.** Every result states them, and the planner's seconds a decision beside the reference's.
    R1's cells, each run only where R0 shows its target (the bars are in R1):
    - **C1, split combining:** a candidate reaches where at least one member reaches; it dies where a
      majority of members die; its progress is the mean. (`Settings.ensemble`: `"split"`.)
    - **C2, more candidates:** `--sequences 96`.
    - **C3, the bump test narrowed:** `--reach-bump 2 --reach-bump-columns 6`.
    - Pros: no training; each aims at a measured class; the real game corrects a wrong hope at the next
      decision, as it does now.
    - Cons: W6's comparison is no longer "the same planner"; C2 costs four times the planning; C1 can raise
      stomp's deaths (stomp's count shows it).
  - (b) Hold the settings as W11's and change only the model.
    - Cons: F7's veto stays whatever the model; the settings were never chosen for an ensemble.
  - (c) Sampling from the heads in place of the argmax.
    - Cons: the ensemble already gives the spread; noisier scores; kept out unless R0 shows members agreeing
      and wrong.
- **D77. The model retrained on the planner's own play (R2; W5's loop, early).** (New 2026-11-13.) Every model so
  far trained once, on the reference's play and babbling from it. The model's planner goes where the reference
  doesn't (F3, F4), and no table holds those states.
  - (a) *Chosen.* **One round of the loop:** the model's planner (R1's best form) plays the battery's goals
    from L1's recordings at states the probes don't use (`--every 480` with a phase of 240) and other seeds;
    babbling runs from states along that play (D27's way); both go to tables beside the four; five members
    train as probe 14's on all six.
    - Pros: the loop every planner on a learned model runs (the literature's section 5), and W5's own, so
      the tools stay; no change of the model's form; nothing hand-chosen (the states are the agent's).
    - Cons: the probe's states and the new tables share recordings and the level, so the probe flatters the
      model: only L1′ decides, and R2's bars sit above the gate for that; one round may not make a 1-2 line
      margin exact.
  - (b) Babbling aimed at ledges by hand.
    - Cons: a hand-given curriculum (learn the method, not imitate it).
  - (c) Train on the probes' own attempts.
    - Cons: the test's states in the training.
- **D78. The self's box factored: its anchor and its size (R3; amends D44).** (New 2026-11-13.) The oracle's self
  box is the visible sprite's: its width changes on 37% of steps and its height on 15%, and the four edges are
  chosen apart. "The box changes size" is the second commonest place where a rollout leaves the truth (815 of
  4,865), landings at a ledge's edge are the ones the members miss (F2), and stomp's deaths land 1-3 px beside
  the enemy.
  - (a) *Chosen.* **Each object's token and outputs as two factors:** the anchor's motion (the bottom line and
    the centre column, two heads) and the size (height and width, two heads). The scene format, the oracle and
    the goal tests stay; the box is put back together from the two.
    - Pros: motion no longer carries the sprite's animation; a box can't come apart; factored, not flat; the
      one step aimed at stomp.
    - Cons: new tables and a training round; the centre is a half-pixel quantity when the width is even
      (kept in half pixels).
  - (b) A joint head over the four edges.
    - Cons: 35^4 classes, or a flat code of them.
  - (c) A fixed-size box from RAM.
    - Cons: not what an organ gives; W12 couldn't follow.
- **D79. The self's motion in the air as rules (R4; D23 (c), O8's route 1).** (New 2026-11-13.) The last step,
  taken only if R1 to R3 leave bump under the gate and R0's classes still put the misses on the members'
  foresight (F8's class M).
  - (a) *Chosen.* **Rules searched from the same tables, for the self, where no contact changes its motion:**
    first a function check (is the self's next vertical motion a function of its last `k` motions and actions,
    within a line, on held-out babbling?), then the search, then the network kept for contacts, the ground and
    every other object.
    - Pros: exact where the network is a line out; searched from data, not given.
    - Cons: a second form inside the model; a rule language to design; contacts stay learned, and the ledge's
      edge is a contact.
  - (b) Rules for everything.
    - Cons: a plan of its own.
- **D80. Not in the round: the transformer, and the gate.** (New 2026-11-13.)
  - (a) *Chosen.* **D4's transformer is dropped from W6's fallbacks, and the gate stays at 80% for each kind.**
    The misses are the self's own motion and the planner's scoring; no interaction between objects was found
    in five rounds (the enemy's error is 0.3 px). If R4 ends refuted, W6 ends with its failure placed (D30) and
    O8's routes 3 and 4 (the gate; W5 and W7 with W6 unregistered) go back to the owner, with R0's measure of
    the reference against itself beside them.
    - Pros: the largest build is the least supported; the gate isn't moved by the party it binds.
    - Cons: if an interaction shows later, the transformer comes back as a new decision.
  - (b) Keep the transformer as R5.
    - Cons: a growing list with no evidence behind its last item.

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
| W13 | The organ's second round (O6): objects behind the background, switches, the player's split lives | from its probe, at its registration | D30 |
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
- **W13. The organ's second round (O6).** Before W12: its probe on W2.4's test, its scope from W2.4's misses and
  W3's organ column, its claims registered from the probe.
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

#### W2.4's registration (2026-11-12, before the registered run)

**The organ and the scorer:** indrajala-rl `b917a3e` (#63-#72). The events (`organ/events.py`), the oracle's block
events and objects (`smb.BlockEvents`, the slots' flags), kinds (`organ/kinds.py`), the online mode (`Memory`,
`--memory`) and the scoring (`organ_events.py` inside `organ_objects.py`'s pass), with the probes' changes:
- **E1 and E1L by D31:** transient block events found by an organ event or as their sprite; lasting ones by an organ
  event or when the map shows them.
- **Sources apart (D33):** machine play (`random/`, `policy/`) and deep play (`planner/`), each with its own bars.
- **The online look threshold by D34,** from the memory's frames.
- **Oracle objects keyed by slot:** RAM rewrites a slot's enemy ID as the game clears it.
- **Planner recordings replayed from their tile-mode level start** on a pixel console, with the same RAM required.

**The data.** The test is D17's, with the revision's held-out deep play:
- **Fresh recordings by W1's recipe,** made on `stone` on 2026-11-12 and opened by nothing before this run:
  - random play on all 32 levels (4 episodes each, up to 1,000 decisions, seed 2000);
  - the conv policy's sampled episodes on 1-1 (20, seed 2000).
- **W11's L1′ episodes,** held out: 100 episodes of 1-1 on seeds 4000-4099 (`exact` 6). No probe has read them.
- 343 recordings and 369,447 frames, all replaying exactly; manifest sha256 `93748790…`:
  - machine play: 243 recordings, 230,131 frames;
  - deep play: 100 recordings, 139,316 frames.
- **No human play:** the owner recorded no play after W2.3′'s test session, whose objects results have been read.

**The probes.**
- **Machine play:** the W1 corpus's 34 random and policy groups (manifest sha256 `66165a3e…`).
- **Deep play:** W11's L1 100 episodes (seeds 1000-1099, manifest sha256 `003b84d6…`).
- Both scored offline at `ec536dc`, which counts the same as the run's code (#72 reads the counts and changes none).
- **The online mode:**
  - on the deep play at threshold 20, with the W1 memory;
  - on the held-out `planner/l1-3` at threshold 189, with the W1 memory, and with that memory plus the other
    three planner groups (D35).

**The runs,** on `stone` with 8 workers:
- **Offline:** each group's band, vocabulary and looks are its own, `--least 2`.
- **Online:** `--memory`, the W1 memory (sha256 `c1fc9f75…`, 375,836 frames), at its threshold of 189.
- **Read with** `--score ONLINE --against OFFLINE`.

**The offline claims, by source (D32, D33).** Each is refuted when the run's figure falls under the bar (E5: above).

| claim | the test | machine play: refuted by | its probe | deep play: refuted by | its probe |
|---|---|---|---|---|---|
| E1. Transient block events found | the oracle's transient block events on the organ's whole cells, each matched by an organ event on its cells within 2 pictures (or its hidden range holding it), or by an organ appearance on its cells within 2 pictures | under 97% | 100% (127 of 127) | under 97% | 100% (105 of 105) |
| E3. Appearances found | oracle appearances in view matched by an organ appearance of the identity holding the object, within 1 picture | under 63% | 68.5% (300 of 438) | under 79% | 87.2% (102 of 117) |
| E4. Vanishings found | oracle vanishings in view matched by an organ vanishing of the identity that held it, within 1 picture plus `PATIENCE` | under 49% | 55.6% (189 of 340) | under 88% | 91.9% (419 of 456) |
| E5. Every miss classed | misses of E1, E1L, E3 and E4 classed "other", over their events | more than 2% | 0% (0 of 963) | more than 2% | 0% (0 of 774) |

**The margins** are about 2.5 standard errors of each probe's count. E1's bar lets 3 of every 100 transient events
go missed where its probes missed none.

**The online claims (D32):** the online organ's figure less the offline one on the same pictures. Each is refuted
when it loses more than the margin, over all the test's groups and over each source.

| claim | refuted by a loss over | the probe (deep play, threshold 20; `l1-3` at 189) |
|---|---|---|
| B2. Objects found | 7.5 points | -4.3; -5.5 |
| B3. Objects real | 9.5 points | -7.5; -6.1 |
| B4. Identities kept | 2 points | -0.8; -1.1 |
| E1. Transient block events found | 3 points | none of the 105 lost (the probe's online run read E1 before D31; its misses were lasting events hidden at the time) |
| E3. Appearances found | 5 points | 0; 0 |
| E4. Vanishings found | 5 points | +3.7; -3.5 |

**Caveats:**
- The online probe covered deep play only. Machine play's online margins rest on the W1 memory holding W1's
  random and policy play of the same recipe (other seeds).
- The deep play's E3 rests on 117 appearances.

**Reported, not claimed (D32):**
- **E1L,** lasting block events found. The probes: 5 of 96 on the deep play, 31 of 58 on machine play. The organ
  reads a used block as an object's block over its earlier class (D31).
- **E2,** block events real. The probes: 0.5% on the deep play, 7.3% on machine play. The rest are classed: objects
  at rest, and objects' blocks leaving cells first seen under them.
- **E6,** object events real. The probes: 3.8% and 3.5%; the rest are mostly identity splits and switches.
- **K1,** kinds' purity. The probes: 54% and 82%.
- **Objects' lives;** events by kind, level and route; the lag between RAM's change and the organ's; appearances out
  of events.
- **W2.3′'s claims (B1-B5)** from the same run, offline: objects were closed under D15, so they're a check.

**Feasibility:**
- every transient block event's sprite or cell change is drawn on the next picture or two (W2.4's plan);
- the probes found every one of them, on both sources;
- E3's and E4's bars sit under each probe's figure by its sampling error;
- the online organ reads each picture once with a fixed memory, as the probes did.

**If refuted (D30):** the organ's misses that refute it are listed by kind. W2.4 has one round (D15's rule), and W3
follows either way. Whether the organ gets another round (D31's lasting changes among them) is the owner's.

#### W2.4's result (2026-11-12): every registered claim holds

**The run.** On `stone`, at indrajala-rl `b917a3e`, with 8 workers, as registered:
- offline: 37 groups in 87 minutes;
- online, with the W1 memory at threshold 189: 31 minutes. The online organ skips the band and vocabulary passes,
  so it ran at 2.8 times the offline organ's speed.

The data is home in indrajala-studies' gitignored `data/smb-world-model/organ/w24/run/`: results, logs and both
claims reports. The test corpus is in `data/smb-w24-test/`.

**The offline claims, by source:**

| claim | machine play (33 groups) | bar | holds | deep play (L1′'s 100) | bar | holds |
|---|---|---|---|---|---|---|
| E1. Transient block events found | 100% (83 of 83) | 97% | yes | 100% (108 of 108) | 97% | yes |
| E3. Appearances found | 73.6% (240 of 326) | 63% | yes | 82.2% (74 of 90) | 79% | yes |
| E4. Vanishings found | 59.3% (115 of 194) | 49% | yes | 91.3% (408 of 447) | 88% | yes |
| E5. Every miss classed | 0% (0 of 643) | 2% | yes | 0.14% (1 of 716) | 2% | yes |

**The online claims:** the online organ's figure less the offline one, refuted by a loss over the margin.

| claim | margin | all (37 groups) | machine play | deep play |
|---|---|---|---|---|
| B2. Objects found | 7.5 | -2.70 | -0.92 | -4.89 |
| B3. Objects real | 9.5 | -3.37 | -0.38 | -6.74 |
| B4. Identities kept | 2 | -0.57 | -0.13 | -1.11 |
| E1. Transient block events found | 3 | 0 | 0 | 0 |
| E3. Appearances found | 5 | -0.24 | -0.31 | 0 |
| E4. Vanishings found | 5 | -1.25 | -2.06 | -0.89 |

All hold. The online organ loses most on the deep play's objects (B2 and B3 by 5-7 points), as its probe did;
on machine play it is within a point.

**The finding the run adds: online, the organ holds the lasting changes.**
- **E1L,** lasting block events found:
  - offline: 57.5% on machine play (23 of 40) and 23.9% on the deep play (17 of 71);
  - **online: 97.5% (39 of 40) and 95.8% (68 of 71).**
- **The online routes on the deep play:** 46 by a landscape event in time, 11 by their hidden range, 11 by the
  map showing them; 3 missed.
- **Why:** the online vocabulary comes from the whole W1 corpus, where used blocks and broken bricks are known
  landscape, so a cell's change to one is the landscape's. The offline organ learns each group alone: there a
  used block is new and rare, so W2.3′'s A1 reads it as an object's block over the cell's earlier class (D31).
- **So D31's gap is the offline organ's.** The online organ, the one an agent uses (D28), holds what changes in
  the landscape.

**Misses by class** (offline; online alike):
- **E3:** machine play: behind the background 55, switched 30, overlap 1; deep play: switched 16.
- **E4:** machine play: behind the background 59, switched 14, over a cell showing a landscape block 6; deep
  play: switched 21, over a landscape block 13, overlap 3, other 1, over a filled cell 1.

**Reported:**

| | machine play, offline | online | deep play, offline | online |
|---|---|---|---|---|
| E1L. Lasting block events found | 57.5% | 97.5% | 23.9% | 95.8% |
| E2. Block events real | 7.9% | 5.2% | 1.4% | 2.2% |
| E6. Object events real | 3.6% | 3.3% | 3.8% | 2.7% |
| K1. Kinds' purity | 82.8% | 53.6% | 53.7% | 51.8% |

- **E2 and E6** are low for the reasons the probes gave: objects at rest and objects' blocks leaving their cells
  (E2), and identity splits and switches (E6).
- **K1 online** is the memory's kinds (one set over all groups), and they are less pure than the groups' own
  kinds on machine play.
- **Lives** (offline): the player's main identity held 63.2% of the player's pictures, and 123 of its 341 lives
  were held by one identity throughout. For the other objects, 79.8% of pictures were held by the main
  identity, and 1,157 of 2,944 lives by one identity. Online: 64.0% and 76.0%.
- The player's life is broken by splits more often than any other object's. W3's self is "the identity
  predicted best over a window" (the revision), so W3 must read a window across them, as the belief scene
  (D29) would.
- **W2.3′'s claims from the same run** (offline): B1-B5 all hold over the 37 groups. Objects found is 90.2%:
  89.1% on machine play and 91.5% on the deep play.

**What follows:**
- **W2.4 is done.**
- **W3, the self,** is next.
- **The organ's second round (O6) is now W13,** before W12. Its scope narrows: the lasting changes hold online.
  What is left: objects behind the background and switches (the E3 and E4 misses), the player's split lives,
  and what W3's organ column shows. Splits stay with the belief scene (D29).

#### W3's plan (2026-11-12)

**What it gives the stages above:** the self, the object the agent's actions move, found from behaviour and
checked against RAM:
- **W4's model** reads the action only for the self (D22, D23);
- **W6 and W7** set their goals relative to the self, and W5's archive keys cells by the self's place (D6).

W3 is built and claimed on the oracle's scenes (O4). The organ's column, offline on the same recordings, is
W12's.

**The method (D5, as decided):**
- **An inverse model,** trained on babbling, predicts the action from an object's motion.
- **The self** is the identity whose motion predicts the actions best over a window of decisions.
- **Two checks, tests only, never the agent's input:**
  - RAM's player;
  - the exact counterfactual by restore: restore a state, take each action for one decision, and see which
    objects' next boxes differ.

**The pieces (game-agnostic where they can be; nothing in the self names SMB):**
- **Babbling (D36):** `record_play.py --policy babble`.
- **The rows:** per decision (4 frames, the oracle's scenes merged by `scene.decisions`), per identity in view:
  - its box's change over the last `w` decisions and the next one (top, left, bottom and right, in pixels,
    clipped to ±16);
  - the action taken, as its axes (D37).
- **The inverse model (D38):** a small dense network in indrajala-ml (its numpy backend, float64; corrected 2026-11-12 from "float32"), one shared by
  every object. It reads an object's rows and gives each action axis a distribution.
- **The self:**
  - per identity in view, over the last `W` decisions, the mean information its motion gives about the actions
    taken: each axis's log-likelihood under the model, less its log-likelihood under the axis's frequencies;
  - the self is the identity scoring highest, among those in view for all `W` decisions;
  - `w` and `W` come from the probe, starting from 2 and 16.
- **The checks:**
  - **RAM's player:** the oracle's identity of slot "player".
  - **The counterfactual:** at sampled states of the test, a restore and each of the 12 actions for one
    decision. The contingent objects are those whose next box differs between actions. The self must be one
    of them, and the others are listed: a bumped block, a kicked shell.
- **The scorer:** `scripts/self_check.py`. It replays a corpus through the oracle's scenes, trains or loads the
  inverse model, finds the self, scores it, and runs the counterfactual on a sample.

**The claims, sketched** (bars from the probe, at the registration):

| claim | the test | starts from |
|---|---|---|
| S1. The self is the player | decisions where the scene holds the player and a self is chosen: the self is RAM's player | 99% (the plan's gate) |
| S2. The counterfactual agrees | sampled states: the self is among the objects contingent on the action | from the probe |
| S3. A self is chosen | decisions where the scene holds the player for `W` decisions: some identity is chosen | from the probe |

**Reported, not claimed:**
- S1 by level, held-out levels apart, and by the player's power state (RAM's, for the report only);
- the objects other than the self that the counterfactual finds contingent, and the decisions where the self
  is another object, by its kind;
- the inverse model's accuracy per axis, on the self and on the rest;
- a counting baseline (D38's (b)) beside the model.

**The data:**
- **Training:** babbling on every level but the held-out ones.
- **The probe:** a part of the training recordings, held out.
- **The test:** fresh babbling on every level, the held-out levels included, plus W2.4's test deep play
  (L1′'s 100). Deep play holds power-ups babbling rarely reaches, and it is play the model never trained on.
- **The held-out levels:** the fourth of each world (x-4, the castles: 8 levels), whose look and objects
  (fire bars, Bowser, lava) differ most from the rest.

**The PRs:**
1. **indrajala-rl, babbling:** `--policy babble` (D36), with tests (held lengths, sticky, seeds).
2. **indrajala-rl, the self:** `indrajala_rl/self.py` (the rows, the self from a model's scores) and
   `scripts/self_check.py` (the oracle's scenes, training through indrajala-ml, scoring, the counterfactual),
   with tests on synthetic scenes: one object moving with the action, one not, one moving only after contact.
3. **The recordings,** on `stone`: training at seed 5000 and the test at seed 5500, each with its manifest.
4. **The probe:** `w` and `W`, the baseline, varied on the fly.
5. **indrajala-research, the registration,** merged before the run.
6. **The registered run,** then the findings. If S1 is refuted, its fallback (a longer window, D30) is
   registered apart.

**Feasibility:**
- in SMB only the player answers the pad;
- the scroll removes the camera before the scenes;
- things the player moves (a shell, a bumped block) answer only after contact, which a window of decisions
  separates (D5);
- the oracle's scene holds the player whenever it draws a visible pixel (W10);
- held actions give the player its full range of motion (D36);
- **where it can fail:** a player blocked by a wall, whose motion doesn't answer the pad for a while. S1 is over
  decisions where a self is chosen, and S3 counts how often none is.

#### W3's registration (2026-11-12, before the registered run)

**The code:** indrajala-rl `8f9ebc4`:
- `record_play.py --policy babble` (#73);
- `indrajala_rl/self.py` and the pad's axes in `games.base` (#74);
- `scripts/self_check.py`: `boxes`, `train`, `score` (#75), `counterfactual` (#76, #77), S4 (#78).

**The model (D39):** the probe's, fixed, sha256 `ba93439f…`:
- `w` 1, `after` 1; dense 64 and 64; 20 epochs; seed 0;
- trained on the training babbling (seed 5000) less each level's fourth episode and less the castles (x-4):
  44,273 rows.

**The self:** a window of 64 decisions; the identity whose rows over it gave the most information about the
actions taken, if above zero.

**The data:**
- **Babbling, the test** (D36): seed 5500, every level, 4 episodes each, recorded on `stone` 2026-11-12 and opened
  by nothing before this run. 222 recordings, 147,202 frames, all replaying; manifest sha256 `da921e60…`. The
  training corpus (seed 5000) is 222 recordings and 133,386 frames, manifest `0762c0b6…`.
- **Deep play:** L1′'s 100 episodes (W11; seeds 4000-4099), from W2.4's test corpus, `planner/l1prime-*`. W2.4
  read them for the organ, never for the self, and no W3 probe has.
- **The castles (x-4)** are held out of training; they are scored with the rest and reported apart.

**The runs,** on `stone` with 8 workers:
- `self_check.py boxes` on each test corpus;
- `counterfactual --per 4 --seed 0` on each;
- `score --window 64 --held-out 1-4 2-4 3-4 4-4 5-4 6-4 7-4 8-4 --counterfactual ...`, each source apart.

**The claims, by source.** Each is refuted when the run's figure falls under the bar.

| claim | the test | babbling: refuted by | its probe | deep play: refuted by | its probe |
|---|---|---|---|---|---|
| S1. The self is the player | decisions where the scene holds the player and a self is chosen: the self is RAM's player | under 99% | 99.76% (2,063 of 2,068) | under 99% | 100% (24,897) |
| S2. The counterfactual agrees | sampled decisions (4 a recording) with a self chosen: the self is among the objects whose box after the next two decisions differs between the 12 actions | under 90% | 100% (25 of 25) | under 96% | 99.07% (318 of 321) |
| S3. A self is chosen | decisions where the player has rows for the whole window: some identity is chosen | under 98.5% | 99.95% (2,068 of 2,069) | under 96.5% | 97.7% (24,897 of 25,478) |

**The bars and margins:**
- **S1's bar is the plan's gate.**
- **S2's and S3's** are the probes' figures less a margin for runs of decisions that share a window, which are
  not independent. Babbling's S2 rests on 25 samples, so its margin is wide.

**Reported, not claimed:**
- **S4,** coverage (D40). The probes: 55.2% and 77.0%.
- S1 on the castles, which were left out of training (probe, window 16: 99.0%, 396 of 400).
- S1 by level and power state.
- The wrong selves by kind.
- The player's contingency in the counterfactual's samples (probes: 118 of 128 and 395 of 400), and the
  contingent objects that aren't the player, by kind.
- Each axis's accuracy on the player's rows and the rest's.
- The counting baseline (D38 (b)).

**Feasibility:**
- in SMB only the player answers the pad;
- the window separates the things it moves only after contact (D5);
- both probes held S1 at the gate at this window: on babbling, the source whose wrong selves the window
  removes, and on deep play, the source with the long shots.

**If refuted (D30):** the fallback, a longer window, is registered apart, and its cost in coverage is stated.

#### W3's result (2026-11-12): every registered claim holds

**The run.** On `stone`, at indrajala-rl `8f9ebc4`, with the probe's model (sha256 `ba93439f…`, checked before
the run), as registered. The data is home in indrajala-studies' gitignored
`data/smb-world-model/self/w3/run/`: tables, counterfactual samples, results and logs. The probe is in `probe/`.

| claim | babbling (seed 5500) | bar | holds | deep play (L1′'s 100) | bar | holds |
|---|---|---|---|---|---|---|
| S1. The self is the player | **99.86%** (25,182 of 25,217) | 99% | yes | **100%** (27,412 of 27,412) | 99% | yes |
| S2. The counterfactual agrees | 95.6% (280 of 293) | 90% | yes | 98.8% (321 of 325) | 96% | yes |
| S3. A self is chosen | 99.37% (25,215 of 25,374) | 98.5% | yes | 99.08% (27,412 of 27,667) | 96.5% | yes |

**W3's gate is passed:** on the oracle's scenes, the self found from behaviour alone is RAM's player on at least
99% of the decisions where one is chosen, on babbling and on deep play. The counterfactual by restore agrees.

**Reported:**
- **S4, coverage:** 72.4% of babbling's decisions with the player (25,182 of 34,777) and 79.2% of the deep
  play's (27,412 of 34,601). The rest are each life's or shot's first 64 decisions (D40).
- **The castles,** left out of training: the self was the player on 2,528 of 2,529 decisions.
- **The wrong selves** (babbling only), by level:
  - 2-2, the underwater level: 33 of 3,113, all slot 07. Most likely the Blooper, which chases the player, so its
    motion answers the pad second-hand.
  - 4-3: 1 of 681. 7-4: 1 of 377.
- **The counterfactual's samples:**
  - the player is contingent in 485 of 519 babbling samples and 395 of 400 deep-play ones;
  - other contingent objects are mostly enemies the player stomps or bumps within the two decisions (Goombas: 69
    in the deep play), bubbles under water, and a bumped block.
- **The counting baseline** (D38 (b)) did as well: S1 99.95% and 100%. At a window of 64, counting the motion's
  signs against the actions is enough in SMB; the learned model's case is the shorter windows and other games,
  not this result.
- **Each axis's accuracy** on the player's rows: horizontal 0.70 and 0.59, A 0.76 and 0.79 (the rest of the
  objects: 0.34-0.56 and 0.51-0.57).
- **A gap: every scored decision has the player small,** on both sources. Babbling rarely reaches a power-up, and
  L1′'s planner took none. The first draft's "every power-up state" is untested. It waits for play that reaches
  them (W5), where S1 is read again by power state.

**What follows:**
- **W3 is done.**
- **W4 is next:** the function check (`scene_function`) first, then the model. The self's flag in W4's tokens
  comes from this method.
- **W12 reads W3 again on the organ's scenes.**
- The coverage remedy (carrying the self across a cut, or a sequential test: D40) is taken up when an agent
  first needs a self in a shot's first decisions (W6).

#### W4's plan (2026-11-12)

**What it gives the stages above:** a model of how each object moves, one decision ahead, from what a camera sees.
W6's planner rolls it out in place of the emulator, and W5's play trains it further. It is built and judged on
the oracle's scenes (O4), with RAM's player as the self (D43). The organ's column is W12's.

**The pieces** (game-agnostic where they can be; nothing in the model names SMB):
- **Transitions:** per decision, per object in view, the token (D22, D44) and its outcome: the next decision's
  motion, whether it vanishes, its next kind. They come from the oracle's scenes, as W3's boxes do, plus each
  decision's landscape around each object. One replay writes them, as a table.
- **The function check** (`scene_function`, a tool; D42): exact keys from the tokens, fitted on training and read
  on the probe. It fixes `k`, the window and `n` before the model is built.
- **The model** (D23, D44): one small dense network in indrajala-ml shared by every object, a categorical head per
  output, trained one step ahead.
- **The baselines:**
  - **copy:** each object repeats its last motion;
  - **still:** each object stays.
- **Rollouts:** the model stepped `h` decisions on its own outputs, from recorded states, against the recording,
  for D45's reports. A rollout's objects are those in view at its start; one that vanishes is gone. Objects
  that appear during it aren't predicted (that is W6's or W5's question).

**The claims, sketched** (bars from the probe, at the registration):

| claim | the test | starts from |
|---|---|---|
| M1. Better than copying | per kind with at least 500 test transitions, the model's next box exactly right more often than the copy baseline's | every such kind |
| M2. The self | the self's next box exactly right | from the probe |

**Reported:** the rollout error after `h` decisions against copy; vanishings predicted; the held-out level apart;
deep play and babbling apart; the function check's open and unseen shares.

**The data (D41):**
- **Training:** the W1 corpus, W3's training babbling, and W11's deep play, less 1-3.
- **The probe:** W3's test babbling (seed 5500).
- **The test:** fresh babbling (seed 6000) and L1′'s 100.

**The PRs:**
1. **indrajala-rl, the transitions:** `indrajala_rl/world.py` (tokens from scenes, game-agnostic) and
   `scripts/world_check.py transitions` (the oracle's scenes to a table). Tests on synthetic scenes.
2. **indrajala-rl, the function check:** `world_check.py function`. Tests: a deterministic toy is all
   determined; a key with a coin flip in it is open; a key too fine is unseen.
3. **The function check's probe,** on `stone`, which fixes `k`, the window and `n`: recorded in the plan.
4. **indrajala-rl, the model and its measures:** `world_check.py train`, `score` (M1, M2, the baselines,
   rollouts).
5. **The recordings** (babbling at seed 6000) and the model's probe.
6. **The registration, then the run.**

**Feasibility:**
- the game is deterministic in its RAM;
- what a camera lacks (sub-pixel speeds, how long a button is held) is in the motion's history: the review
  measured the player's next motion open in 3.3% of decisions from 8 steps of history, before the landscape;
- the function check measures the rest before anything is trained;
- the copy baseline is beaten wherever motion changes for a reason the token holds: a wall, a landing, a
  turn at an edge, a jump's arc.

**If refuted (D30):** the function check's fallbacks first (more history, D22 (c)'s recurrent state), then D23's
second form, the transformer over the set (D4).

#### W4's registration (2026-11-12, before the registered run)

**The code:** indrajala-rl `ee91387`:
- `world.py` and `world_check.py transitions` and `function` (#79);
- `world_model.py` and `train` and `score` (#80);
- rollouts and shot maps (#81);
- the action's alignment (#82).

**The model (D46):** the probe's, fixed, sha256 `5d59b007…`:
- `k` 8, a 4×4 window, one neighbour; dense 128 and 128; 10 epochs; seed 0;
- trained on the W1 corpus, W3's training babbling, W11's L1 100 and its every-level pass, less 1-3: 286,723 steps.

**The data (D41):**
- **Babbling, the test:** seed 6000, every level, 4 episodes each, recorded on `stone` 2026-11-12 and opened by
  nothing before this run. 222 recordings, 127,746 frames, all replaying; manifest sha256 `9e167ac4…`.
- **Deep play:** L1′'s 100 (seeds 4000-4099; W2.4's test corpus, `planner/l1prime-*`). Read for the organ (W2.4)
  and the self (W3), never for a model.
- **1-3,** left out of training, is reported apart.

**The runs,** on `stone`:
- `world_check.py transitions --maps` on each test source;
- `score --held-out 1-3`;
- `rollouts --horizon 16 --per 4 --seed 0`.

**The claims, on babbling (D47).** Each is refuted when the run's figure falls short of the bar.

| claim | the test | refuted by | the probe |
|---|---|---|---|
| M1. The other objects | pooled, the self left out: the next box exactly right, the model against copy | under +15 points | 59.5% against 35.4%, +24.1 |
| M1′. Each kind | every kind (not the player) with at least 500 test steps: the model's share against copy's | more than 1 point under copy for any kind | every kind above copy (smallest margin slot 32, +0.06) |
| M2. The self | the self's next box exactly right, the model against copy | under +10 points | 27.5% against 11.1%, +16.4 |

**Reported:**
- the same on deep play;
- 1-3 apart;
- the rollout error per horizon (1 to 16) against copy, the self and the rest apart;
- vanishings (the probe: recall 72%, precision 56%);
- each edge's motion right;
- each kind's figures.

**Feasibility:**
- the function check leaves the self open in 4% of its seen keys at this history;
- the probe's model holds every claim with room;
- the test is babbling of the probe's recipe, at a fresh seed.

**If refuted (D30):** D46 (b)'s improvements (the self's past actions, more training), then the transformer over
the set (D4), registered apart. **Either way, W6 reads whether the model is good enough to control with.**

#### W4's result (2026-11-12): every registered claim holds

**The run.** On `stone`, at indrajala-rl `ee91387`, with the probe's model (sha256 `5d59b007…`, checked before
the run), as registered. The data is home in indrajala-studies' gitignored
`data/smb-world-model/world/w4/run/`. The function check is in `function/`, the model's probe in `model/`.

**The claims, on babbling (seed 6000):**

| claim | the run | bar | holds |
|---|---|---|---|
| M1. The other objects | 62.3% against copy's 37.3% (26,429 steps): **+25.0 points** | +15 | yes |
| M1′. Each kind | no kind under copy; the closest is slot 32, 100% against 100% (1,142 steps) | -1 point | yes |
| M2. The self | 26.3% against copy's 11.0% (28,512 steps): **+15.3 points** | +10 | yes |

**W4's gate is passed:** on the oracle's scenes, the model is better than copying, per kind and for the self, on
fresh play.

**Reported:**
- **Deep play** (L1′'s 100; not claimed, D47):
  - the self exactly right in **58.9%** (33,433 steps) against copy's 10.9%;
  - the other objects in 87.2% against 75.1%;
  - every kind above copy;
  - vanishings: recall 76%, precision 77%.
- **1-3, left out of training** (babbling): 28.6% against 8.9% (597 steps, all the self's).
- **Rollouts,** the mean box error in pixels against copy:

  | after | babbling: the self | the rest | deep play: the self | the rest |
  |---|---|---|---|---|
  | 1 decision | 1.3 (copy 2.0) | 0.3 (0.6) | 0.9 (2.7) | 0.1 (0.3) |
  | 8 | 10.5 (34.0) | 2.1 (5.6) | 9.7 (46.0) | 2.1 (3.6) |
  | 16 | 18.0 (62.0) | 4.8 (12.6) | 19.9 (90.9) | 4.8 (7.8) |

- **The hardest kinds** on babbling: slot 14 (5.97% against 0%), slot 0e (29% against 0%), and bubbles (39%
  against 34%).
- **Vanishings** on babbling: recall 74%, precision 56%.

**What it means for W6.**
- The model is far better than copying, but it isn't exact. The self drifts about 10 pixels in 8 decisions,
  more than half a block.
- W6's planner looks 16 decisions ahead (W11). It can replan every decision, as it does under sticky actions,
  so a drift is corrected by each new observation, not carried.
- Whether that is enough to reach W6's goals is W6's question. D46 (b) (the self's past actions, more
  training) is its first fallback.

**What follows:**
- **W4 is done. W6, control,** is next: the reference planner (W11) planning on the model instead of the
  emulator, the battery of goals under sticky actions, without restore.
- W5 (play) follows W6.

#### W6's plan (2026-11-12)

**What it asks:** can the agent control the player by planning on its learned model, not on the emulator? This is
the plan's first real test (D24: a model is judged by the control it gives). The reference planner (W11) reaches
the battery's goals by searching the exact game with restore. W6 swaps the exact game for W4's model and keeps
everything else.

**The pieces:**
- **`SceneModel`** (D48), in indrajala-rl:
  - made from the decision's oracle scene and the last `k` scenes;
  - `save` and `restore` copy the state;
  - `step` runs W4's model one decision;
  - **a batched form** (D50) steps every candidate's copy together.
- **Goals on the model** (D49): W11's `distance` from the self's predicted box, the model-side reaching tests and
  death; the goal's place in world pixels, as the oracle's scene gives.
- **The battery's driver:**
  - W11's `planner_battery.py` with the model in place of the emulator;
  - each attempt runs the real game forward, plans on the model each decision, and asks RAM whether the goal is
    reached;
  - the reference (the emulator) runs on the same attempts.

**The claims, sketched** (bars at the registration, from the probe):

| claim | the test | starts from |
|---|---|---|
| C1. Land on the model | goals reached, against the reference's on the same attempts | at least 80% of the reference's rate |
| C2. Bump on the model | as C1 | 80% |
| C3. Stomp on the model | as C1 | 80% |

**Reported:**
- frames-equivalent and seconds a decision;
- the misses by cause: out of decisions, died, a model-side reach the game didn't confirm;
- the rates against the self's rollout error in each attempt;
- the reference's rates.

**The data:**
- **The probe:** the battery on states of L1's 100 (in W4's training: settings only).
- **The test:** the battery on L1′'s 100 (D51).

**The PRs:**
1. **indrajala-rl, the scene model:** `SceneModel` (unbatched, then batched), with tests that the batched rollout
   equals the unbatched one and that `save` and `restore` are exact.
2. **indrajala-rl, goals on the model and the battery's driver,** with tests on synthetic scenes.
3. **The probe** on `stone`: speed first, then a small battery, varied on the fly (`exact`, horizon, the
   reaching tests).
4. **The registration, then the run.**

**Feasibility:**
- W11's planner reaches 80-96% of these goals on the exact game;
- W4's model moves the self within about 1 pixel a decision and 10 in 8 (deep play), against copy's 46;
- replanning every decision corrects the drift with each new scene;
- the goals are a few cells away (W11: most reached within 20 decisions).

**Where it can fail:**
- objects the model can't see coming;
- the self's error compounding over a jump's arc;
- the model-side tests firing wrongly.

**If refuted (D30):** D46 (b) (the self's past actions, more training), then D4's transformer. Refuted again on the
oracle's scenes, the plan stops and goes to the owner with what the fallbacks showed.

#### W6's probe (2026-11-12)

**Built:**
- indrajala-rl #84: the scene world, goals on the model, and the batched planner;
- #85: the battery's driver, `planner_battery.py --model`;
- #86: the planner's `Score` refuses a positive death.

The first probe ran with `--death 1000`, a misreading of W11's `-1000`, and both planners sought death.

**Speed** (`stone`, one core): **0.04-0.06 s a decision** on the model (about 1,350 model steps and 16 forward
passes a decision), against the budget's 1 s; the reference took 0.4-0.7 s a decision.

**The small battery** (24 of L1's recordings, every fourth; W11's settings, `--death -1000`; 79 attempts):

| kind | the reference | the model | the model's share of the reference's |
|---|---|---|---|
| land | 43 of 43 | 39 of 43 | 90.7% |
| bump | 25 of 28 | 8 of 28 | 32.0% |
| stomp | 4 of 8 | 0 of 8 | 0% |

**The misses:**
- **Land:** 3 out of decisions, 1 died. Three of the four are one goal (row 8, column 136), which the reference
  reaches in about 24 decisions.
- **Bump:** 11 out of decisions, 5 died, 4 unconfirmed (the model said the action reached the goal; RAM didn't).
  14 of the 20 are the high ? block (row 6, column 64).
- **Stomp:** 5 died, 3 out of decisions; the model never said an enemy was stomped.

**The self's one-step error:**
- **Along a recording, under its own actions** (`planner_battery.py`'s pipeline): 0.64 pixels, and 60% exact.
- **In the attempts:** a mean of 1.2-1.4 pixels, with runs of about 8.
- **The traces:** the planner's own actions show the model's blind spot, the onset of a jump (D58). The deaths at
  enemies are D57's.

**What follows:** D56-D58: W4's fallback D46 (b) and the death on the model, then the probe again, then the
registration.

#### W6's probe, second round (2026-11-12)

**D58's three models** (W4's tables, `k` 8, a 4×4 window, one neighbour; two threads each on `stone`):

| model | the self exact, W3's test babbling | the self's rollout error at 8 and 16 decisions |
|---|---|---|
| W4's (10 epochs, no past actions) | 27.5% | 11.1 and 20.0 px |
| W4's inputs, 30 epochs | 32.2% | 20.5 px at 16 |
| the self's last 8 actions, 10 epochs | 35.3% | 11.3 px at 16 |
| the self's last 8 actions, 30 epochs | 41.6% | 10.8 px at 16 |

The past actions halve the self's drift at 16 decisions; more epochs alone don't.

**A bug found and fixed** (indrajala-rl #88): in attempts, the past actions read every pad as 0 after the replay's,
because the watched console didn't pass its buttons on. The two past-action models' batteries were run again.

**The small battery again** (24 recordings, as the first round; the model's share of the reference's, the hidden
block left out by hand, D59): W4's model with the touch (D57): land 91%, bump 30%, stomp 50%; the 10-epoch
past-action model: 98%, 60%, 50%; the 30-epoch one: 93%, 50%, 0%. Twelve bump and eight stomp attempts are too
few to choose by; **the 10-epoch past-action model goes on** (the best on every kind there).

**Probe 3** (all 100 of L1's recordings, visible goals only, D59; the 10-epoch past-action model; 25 minutes):

| kind | the reference | the model | the model's share |
|---|---|---|---|
| land | 186 of 193 | 174 of 193 | 93.5% |
| bump | 63 of 78 | 41 of 78 | 65.1% |
| stomp | 50 of 63 | 9 of 63 | 18.0% |

- **Stomp:** no rollout ever scored a stomp (D60); 48 ran out of decisions.
- **Bump:** 27 of the 37 misses are one goal, the high bricks (row 3, column 131), reached from a platform; the
  reference also misses it 12 times.
- **Land:** 13 died: 8 fell into 1-1's pits, 5 ended the level at the flagpole (x 3164), which the model can't see
  as an end.

**Probe 4** (probe 3 again with D60's stomp; indrajala-rl `6f46aed`): land and bump as probe 3 (93.5%, 65.1%);
**stomp 22 of 63, 44.0% of the reference's** (26 out of decisions, 12 died, 3 unconfirmed; 46 model-side stomps).

**Probe 5** (stomp only, the model only, as probe 4):

| variation | stomps reached of 63 | died |
|---|---|---|
| tolerance 2 | 24 | 13 |
| tolerance 4 (probe 4) | 22 | 12 |
| tolerance 8 | 20 | 15 |
| no touch death (D57 off) | 19 | 22 |

The tests' tolerances don't matter much, and the touch saves lives. **What's left is the model's prediction near an
enemy and over a climb:** stomp at 44% and bump at 65% of the reference, against the gate's 80% (D61).

Data: indrajala-studies' `data/smb-world-model/control/w6/` (probes 1-5, the D58 models and their scores).

#### W6's diagnosis (D61, 2026-11-12)

From probe 4's traces, and from **probe 6**: probe 4's stomp attempts on the model again, with the enemy's boxes in
the trace (indrajala-rl #91). It reproduced probe 4 exactly (22 reached, 12 died, 26 out of decisions, 3
unconfirmed).

**The enemy's motion is not the limit.** Its one-step error is 0.38 px on average within 32 px of the self (1,055
decisions) and 0.30 px further away (834).

**Neither is the planner's horizon.** The reference reaches these goals on the same horizon, 16 decisions.

**The self's vertical motion in the air under A is the limit.** Probe 4's traces, all kinds:

| the self | A | decisions | mean vertical error (px) | false rises |
|---|---|---|---|---|
| in the air | fresh | 428 | 3.10 | 34 (7.9%) |
| in the air | held | 2,217 | 1.20 | 42 |
| in the air | none | 2,750 | 1.59 | 39 |
| on the ground | fresh | 412 | 1.02 | 12 |
| on the ground | held | 191 | 1.13 | 4 |
| on the ground | none | 2,916 | 0.37 | 8 |

- **Definitions:**
  - on the ground: the self's bottom didn't move over the decision before;
  - a false rise: a predicted rise of at least 3 px where the self didn't rise.
- **The cause:** the model often has a fresh A in the air lift the self, which the game never does. With A held,
  it predicts falls short.
- **The input is not what's missing:** the self's last 8 boxes and actions give its speed and whether A is held,
  so the miss is the model's form or size (sub-pixels aside).

**Where it costs.**
- **Bump:** the low bricks (row 7) are reached 37 of 38 times. The high bricks (row 3) are not:
  - columns 80-84: the model 0 of 9, the reference 5 of 9;
  - column 131: the model 4 of 31 (and 2 unconfirmed), the reference 20 of 31.

  Column 131's brick has its bottom at line 96. Under it there is only a two-wide platform (row 7, columns
  129-130), with the staircase's top (row 7, column 137) beside it, and from the ground it can't be reached. In
  the misses, the self gets onto the platform or the stair top (its feet at lines 142-144). It never jumps from
  there toward the brick, and it walks off.
- **Stomp:** 29 attempts were reached by the reference and not by the model.
  - **10 died.** The self lands beside the enemy, the boxes overlapping by 1-3 px. The touch is predicted only
    at the last decision. Earlier, the fall under a held A was predicted 5-6 px short.
  - **10 lost the enemy from the scene** for part of the attempt (in the scene on 0-59 of 55-60 decisions):
    D62.
  - **9 had the enemy in view throughout** and never reached it.

  Even with every out-of-view stomp reached, stomp would be at most 32 of the reference's 50 (64%), so the self's
  motion must be fixed for the 80% gate.

**Probe 7** (D62's (a), the enemy's last box held while out of view; the code was not merged): stomp 22 of 63, no
change; unconfirmed 12 (3 before).

**What D4's round must fix:**
- the self's vertical motion in the air under A, judged by the table above against W4's;
- objects that leave the view, which the model must keep (D62).

Data: indrajala-studies' `data/smb-world-model/control/w6/probe6/`, `probe7/`.

**Models2** (three variants of the 10-epoch past-action model, scored on W3's test babbling with the self in the
air, indrajala-rl #92):

| model | the self exact | in the air, A fresh: error, false rises | the self's rollout error at 8 and 16 decisions |
|---|---|---|---|
| W4's (no past actions) | 27.5% | 4.33 px, 17 (and 1,379 false rises on the ground with A held) | 11.1 and 20.0 px |
| past 8, 128 and 128 (`m-p8-e10`) | 32.2% | 2.35 px, 34 | 5.7 and 11.2 px |
| past 8, 256 and 256 | 35.3% | 1.72 px, 23 | 5.4 and 9.5 px |
| past 8, three layers of 256 | 37.8% | 1.88 px, 16 | 5.1 and 8.7 px |
| `k` 16, past 16 | 31.0% | 2.44 px, 26 | 5.8 and 11.2 px |

**Probe 8** (the battery on the three-layer model, as probe 4, the model only; probe 4's reference):

| kind | the model (probe 8) | the model (probe 4) | the reference | probe 8's share |
|---|---|---|---|---|
| land | 170 of 193 | 174 | 186 | 91.4% |
| bump | 39 of 78 | 41 | 63 | 61.9% |
| stomp | 26 of 63 | 22 | 50 | 52.0% |

The model's own measures improve, but control doesn't: within noise of probe 4. The model's step isn't the limit;
its rollouts are (D63).

Data: indrajala-studies' `data/smb-world-model/control/w6/models2/`, `probe8/`.

#### W6's third round (2026-11-12)

**Rollout training (D63).** The four training tables were written again with their maps
(`~/labour/w6/dad/tables`, the same boxes as W4's), and DaD (indrajala-rl #93) and its scheduled-sampling variant
(#94) were trained on them: 10 epochs, then 3 rounds, each from 8 starts a recording over 16 decisions, followed by
3 epochs. Each training peaked at 14.5 GB; two at once swapped and were stopped.

| model | the self exact | the self's rollout error at 4, 8 and 16 decisions | the rest's at 16 | in the air, A fresh |
|---|---|---|---|---|
| 256x3 (models2) | 37.8% | 2.5, 5.1, 8.7 px | 5.7 px | 1.88 px, 16 false rises |
| 128x2, DaD | 31.3% | 3.7, 7.3, 14.3 | 5.5 | 3.14, 33 |
| 256x3, DaD | 35.8% | 3.3, 6.5, 13.2 | 3.3 | 1.96, 14 |
| 256x3, scheduled sampling | 35.8% | 2.6, 4.9, 9.2 | 4.4 | 1.94, 19 |

- **DaD's correction targets make the self worse:** each round's loss on its new pairs rises. This is the con
  D63 named.
- **Scheduled sampling leaves the self where it was.**
- **Both improve the other objects.**

**Probes 9 and 10** (the battery as probe 8; probe 4's reference):

| model | land | bump | stomp |
|---|---|---|---|
| 256x3, scheduled sampling (probe 9) | 168, 90.3% | 45, 71.4% | 27, 54.0% |
| 256x3, DaD (probe 9) | 166, 89.2% | 41, 65.1% | 18, 36.0% |
| scheduled sampling with D64's bump (probe 10) | 168, 90.3% | 47, 74.6% | 27, 54.0% |

**Four models, one band.** Probes 4, 8 and 9 put four models of different one-step accuracy and drift within a
few attempts of each other. So the limit was not in what those changes reach.

**Two things the traces showed:**
- **The model-side tests lagged the game** (D64, D65). In probe 9 the model claimed 5 of 45 real bumps, its boxes
  within a pixel of the truth. With D64, it claimed 42 of 47 (probe 10). The high bricks still fail (10 of 40,
  against the reference's 25), so seeing the bump wasn't enough.
- **The self's errors are at contacts with the landscape's edges** (probe 10's traces):
  - the landing step itself: 0.26 px;
  - falling: 2.95 px, with 208 phantom landings;
  - walking off a ledge: 2.90 px.

  The token doesn't hold the box's place within its cell (D66).

Data: indrajala-studies' `data/smb-world-model/control/w6/dad/`, `probe9/`, `probe10/`.

**Probe 11** (D65's land with D64's bump; then D66's offset, in a model trained as the scheduled-sampling one with
`--offset`, indrajala-rl #95, #96):

| model | land | bump | stomp |
|---|---|---|---|
| scheduled sampling, D64 and D65 (11a) | 170, 91.4% | 47, 74.6% | 27, 54.0% |
| the same with the offset (11b) | 173, 93.0% | 42, 66.7% | 28, 56.0% |

- **Offline:** the offset model has the self 38.1% exact, drift 9.8 px at 16 decisions, and the rest 3.3 px.
- **In the battery's traces:**
  - phantom landings fell from 231 to 154;
  - vertical errors of 4 px or more fell from 789 to 686, out of about 9,000 decisions.
- **What remains:** many of the large errors are incoherent boxes, because the four edges' heads choose apart
  (a top that moves while the bottom stays). The oracle's box is the visible sprite, so its size changes in many
  steps (width in 37%, height in 15%), which a model of four edges must follow.

**Probe 12** (the offset model; the planner's horizon):

| horizon | land | bump | stomp |
|---|---|---|---|
| 8 | 163, 87.6% | 48, 76.2% | 23, 46.0% |
| 12 | 173, 93.0% | 40, 63.5% | 34, 68.0% |
| 16 (11b) | 173, 93.0% | 42, 66.7% | 28, 56.0% |

No horizon gives 80% on bump and stomp together.

Data: indrajala-studies' `data/smb-world-model/control/w6/probe11/`, `probe12/`, `ensemble/`.

**Probe 13** (D67: five one-step members, 256x3, past 8, offset, seeds 0-4; the battery as probe 8; probe 4's
reference):

| model | land | bump | stomp |
|---|---|---|---|
| member `e0` alone | 177, 95.2% | 46, 73.0% | 25, 50.0% |
| the ensemble, mean | 182, 97.8% | 46, 73.0% | 30, 60.0% |
| the ensemble, minimum | 155, 83.3% | 32, 50.8% | 15, 30.0% |

- **The mean helps land and stomp; the minimum hurts every kind.** Pessimism over five members leaves the
  planner too few sequences it trusts: 25 land attempts ran out of decisions, against 3.
- **Bump:** 15 of the mean's 18 misses are high bricks (row 3: the reference reaches 25, the model 10).
- **Stomp:** 16 of the 20 misses start with the target too young for the model's state (D68), and the 7 with
  the enemy leaving the scene are among them.

Data: indrajala-studies' `data/smb-world-model/control/w6/probe13/`.

**Probe 14** (D68: five members as probe 13's, with young objects; their mean; the battery as probe 13):

| model | land | bump | stomp |
|---|---|---|---|
| the young ensemble, mean | 181, 97.3% | 46, 73.0% | 35, 70.0% |

- **Offline:** each member has the self 39.6-40.4% exact (probe 13's members: 32.9-39.7%). Each training peaked
  at 8.8 GB, two at a time.
- **Stomp:** the young targets no longer wait. Stomps reached take a median of 11 decisions, against the
  reference's 12. Of the 17 misses, 6 have the enemy leave the scene.
- **Bump:** unchanged. 16 of the 17 misses are the high bricks, the self mostly not getting onto the lower
  bricks (D69).

Data: indrajala-studies' `data/smb-world-model/control/w6/probe14/` (the members `y0-y4.json` too).

#### W6's fourth round (2026-11-13, O7's route 1)

The owner chose route 1 (O7): object permanence for stomp, with a diagnosis of the ledge climbs for bump.

**Permanence** has no target (D70): the 6 enemies that left the scene never came back.

**The climb diagnosis** (indrajala-rl #99, #100). The battery's model path can follow the reference: with
`planner_battery.py --follow`, each emulator attempt reports its actions, and the model's path takes them and
traces, at each decision, every member's open-loop rollout of the next 16. `scripts/follow_check.py` reads the
trace:
- **foresight:** the share of members that foresee the bump (the self's top within 2 px) from 1 to 16 decisions
  before it;
- **jump age:** the self's one-step vertical error by decisions since takeoff;
- **divergence:** where each rollout first leaves the truth (by more than 4 px), by what the true self does then;
- **arrivals:** the self's bottom one decision ahead where a fall ends, by the fall's speed and the surface (#101).

Following the reference's actions, the model's path reaches the reference's 63 bumps, so the following is
faithful.

| high bricks (row 3), foresight at | 1 | 4 | 8 | 12 | 16 |
|---|---|---|---|---|---|
| probe 14's young ensemble | 0.94 | 0.85 | 0.62 | 0.50 | 0.45 |
| `k` 16 (probe 15) | 0.90 | 0.84 | 0.70 | 0.57 | 0.42 |
| 6x4 window (probe 16) | 0.96 | 0.86 | 0.68 | 0.54 | 0.52 |

On the other rows, foresight is 0.83-1.00 at every distance, in all three.

| one decision ahead, within 1 px of the bottom (median error) | fast, ground (140) | fast, raised (55) | slow, raised (45) |
|---|---|---|---|
| probe 14 | 71% (0 px) | 31% (6 px) | 80% (0 px) |
| probe 15 | 69% (0 px) | 20% (6 px) | 78% (0 px) |
| probe 16 | 73% (0 px) | 44% (4 px) | 56% (0 px) |

(Member-arrivals, on the bumps the reference reached: a decision where the true self's last fall ends; fast is 4
px or more a decision. `follow_check.py`'s arrivals, indrajala-rl #101.)

- **The jump's late steps:** the one-step vertical error is 0.2-1.2 px over a jump's first 9 decisions and 0.4-2.4
  px after, in all three models. A longer history (D71) doesn't change it.
- **Where rollouts leave the truth** (row 3, 4,865 rollouts; 1,419-1,467 never leave it): in the air
  rising (897 in probe 14, 1,005 in probe 16), the box changing size (815, 826), in the air falling (530, 417),
  the apex or a head hit (367, 411), landings (229, 201).
- **Two particular errors:** recording 1027's oracle box jumps about from step to step (likely the sprite's
  visibility), and arrivals at an apex on the ledge's top (bottom 144) are predicted to fall through by 8 px.

**Probe 15** (D71: five young members, `k` 16, past 16, offset, 256x3; their mean): land 180, 96.8%; bump 46,
73.0%; stomp 37, 74.0%. Each training peaked at 9.5 GB.

**Probe 16** (D72: as probe 14's with `--window 6x4`): land 182, 97.8%; bump 43, 68.3%; stomp 34, 68.0%.
- **Offline:** member `w0` is a little better than probe 14's `y0`: in the air without A, 0.68 px against 0.81;
  vanishings' precision 0.68 against 0.59. Each training peaked at 12.0 GB.
- **Bump:** 19 of its 20 misses are the high bricks.

**The round's finding:** the model is close (about a pixel a step) and the planner's high-brick climbs still
fail. Neither the jump's history nor the view below the feet is what limits them. W6 goes to the owner again
(D73, O8).

Data: indrajala-studies' `data/smb-world-model/control/w6/climb/` (probe 14 followed), `probe15/`, `probe16/`
(the members `k0-k4.json`, `w0-w4.json`).

#### W6's fifth round: the analysis and the plan (2026-11-13, O8, D74-D80)

The owner asked for an analysis of the briefing, the solutions picked and ordered, and a check that the fault
isn't in a part nobody looked at (D74). No probe was run for it. Its figures are read from probe 4's reference
(`probe4/r.json`), probe 14's battery (`probe14/r-mean.json`) and the followed rollouts (`climb/r-follow.json`,
`probe16/r-follow.json`), by one-off scripts; R0 builds the same readings into the tools.

**The analysis's findings.**

- **F1. The bump shortfall is one brick from one side.** The gate needs 51 of the reference's 63; probe 14 has
  46: five short. Low bricks: 37 of 38. High bricks: the reference 25 of 40, the model 9.

  | high bricks, probe 14 | attempts | the reference | the model |
  |---|---|---|---|
  | column 131, the self starting on the ground to its left | 12 | 12 | 8 |
  | column 131, the self starting on the stair side | 19 | 8 | 0 |
  | columns 80-84 | 9 | 5 | 1 |

- **F2. The climb is a jump with 1-2 lines to spare.** The reference's route from the stair side: down to the
  ground, a jump up onto the two-wide platform (feet from line 208 to 144), a jump from it into the brick. The
  first jump's apex has the feet at line 142-143, over a ledge at 144. Of the members' rollouts from the takeoff
  (32 such jumps, 5 members), 54% (probe 14) and 57% (probe 16) land on the ledge; 43% and 36% fall through.
  By where the self lands: well onto the platform (left edge at 2080) 20 of 25; at its ends (2096, 2208) 1 of
  10.
- **F3. The planner then stands still.** In 30 of the 31 high-brick misses the model never claimed a reach. The
  self stands still 6.9-8.9 decisions an attempt in the misses (4.2 in the high bricks reached, 1.8 in the low).
- **F4. The limit binds, on bump alone.** The reference's high-brick successes take 37-40 of the 60 decisions.
  Among attempts both reached, the model's median decisions against the reference's: land 13 against 14, stomp
  11 against 12, bump 29 against 18.
- **F5. The bump test over-claims.** On the low bricks reached, the first member claims a bump 2.7 times an
  attempt for the one the game registers. The slow traces show the self jumping as it arrives and bumping the
  brick beside the goal's, or rising to within the test's 4 lines without touching. D64's test takes the head
  within 4 lines under the brick and the centre within 8 columns; the game takes the head's column at the
  contact.
- **F6. Not the screen's edge.** From the stair side the platform sits at the screen's left edge, where the
  landscape is "outside". The members' foresight of landings there (5-6 of 15) is that of the same landings
  with the platform in full view (6-7 of 15).
- **F7. One member's death outweighs a reach (from the code; not yet measured).** A candidate's score is the
  members' mean (D67), a death is -1,000 and a reach +100. So one member of five predicting a death takes 200
  from a candidate, more than a reach in all five gives. On the reference's own surviving play, a member's
  rollout predicts the self vanishing or leaving the bottom in 0.4-1.3% of rollouts, and 2-5% of decisions have
  such a member. **A touch death (D57) needs the other objects, which the traces don't hold: unmeasured.** The
  vanishing head's precision is 0.59-0.68.
- **F8. What the traces can't say.** They hold the self's path and the first member's one-step prediction, not
  the candidates. R0's classes, for a decision where the self stands still or an attempt is missed:
  - **S, search:** no candidate reaches in any member;
  - **V, veto:** a candidate reaches in a member and loses to the chosen one by its deaths in other members;
  - **D, doubt:** a candidate reaches in a member, without deaths, and its mean loses;
  - **C, claim:** the chosen candidate reaches in the model at its first decision and the game doesn't;
  - **M, foresight:** the followed rollouts' share that foresee the reference's contact (the fourth round's).
- **F9. The planner is otherwise sound on the model:** land and stomp reach at the reference's pace (F4), and
  the action shares and switches a decision are the reference's (0.37 against 0.30).

**Where the solution may lie (the owner's second question).** Three parts were never looked at: the planner's
scoring across members (F7), the model-side bump test's width (F5), and the gate's own noise (the reference
against itself). The first two are in the planner's seat, not the model's, and five rounds changed only the
model and its tests' timing. F2 says the model also has a real limit at the climb. R0 tells them apart before
anything is trained.

**The steps.** Each is one probe on L1's states (probe 4's denominators) with its bars set here. A step whose
probe meets every bar goes to W6's registration; one that doesn't hands to the next. All battery runs: `--every
480 --limit 60 --horizon 16 --segment 4 --rollout-sticky 0.25 --exact 3 --death -1000 --workers 8`.

| step | what | trains | PRs | cost on `stone` |
|---|---|---|---|---|
| R0 | the planner's view; the reference twice more (D75) | no | rl: the trace and `follow_check`'s classes | 1 h |
| R1 | the planner on the model: C1-C3 (D76) | no | rl: `Settings.ensemble` `"split"` | at most 4 runs, 2 h |
| R2 | the planner's own play, one round (D77) | 5 members, 10 epochs | rl: `--phase`, play to tables | 4 h |
| R3 | the self's box factored (D78) | 5 members, 10 epochs | rl: the token and heads | 3 h |
| R4 | the self's air motion as rules (D79) | a search | its own plan, from its check | set by its check |

**R0. Measure.**
- **Built:** D75's trace and classes; `follow_check.py` also reports F1's table, F2's landings by place, F4's
  paces and F5's claims, so each later probe prints them.
- **Run 1:** probe 14's ensemble again with the trace, bump and stomp (`--kinds bump,stomp`, 141 attempts). It
  must give 46 and 35 again (the seeds are the same); if not, the difference is found first.
- **Run 2:** the reference on bump and stomp, seeds 1 and 2.
- **Read:**
  - the share of each of S, V, D and C among the still decisions of missed attempts, bump and stomp apart;
  - the deaths in candidates by kind (vanished, the bottom, a touch), and how many the real game bore out;
  - each repeat of the reference as a share of seed 0's 63 and 50.
- **What follows from it:**
  - C1 runs if V and D together hold at least a quarter of those decisions; C2 if S does; C3 if C holds at
    least one claim a reached bump (F5 has it at 1.7 by the first member);
  - if none runs, R1 is skipped and R2 follows;
  - if a repeat of the reference falls under 80% of seed 0's on a kind, that kind's gate can't hold a
    registration as it stands (the feasibility rule): the round goes on, and the gate's noise goes to the owner
    with whatever passes.

**R1. The planner on the model.**
- **Runs:** each cell R0 points to, alone, on bump and stomp with probe 14's ensemble; then those that gained,
  together; then the best with land. At most four runs before the land run.
- **Bars:** bump at least 51 of 63, stomp at least 40 of 50, land at least 149 of 186.
- **Reported beside them:** F1's table, the classes again, deaths by kind, seconds a decision against the
  reference's.
- **If the bars hold:** W6's registration with that planner and probe 14's ensemble.
- **If not:** the best form is R2's planner. A cell that lowered a kind is dropped.

**R2. The planner's own play.**
- **Play:** R1's best planner on probe 14's ensemble, the battery's three kinds from L1's recordings with
  `--every 480 --phase 240`, seeds 1 to 3 (about 1,000 attempts; the reference isn't run).
- **Babbling:** D27's, from states along that play, to the same count of object-steps.
- **Tables:** `t-play.npz` and `t-play-babble.npz`, level 1-3 left out as before; nothing from L1′.
- **Trained:** five members as probe 14's (`--k 8 --window 4x4 --n 1 --past 8 --offset --young`, 256x3, 10
  epochs, seeds 0-4) on the six tables.
- **Bars** (above the gate: the probe's states share recordings with the play):
  - bump at least 54 of 63 and stomp at least 42 of 50, land at least 149;
  - offline, on the followed rollouts: landings foreseen from the takeoff (F2) at least 75% (54%), and row 3's
    foresight at 8 decisions at least 0.80 (0.62).
- **If the control bars hold:** the registration. **If only the offline bars hold:** R3 trains on the six
  tables. **If neither:** R3 trains on the four, and the play's tables are set aside.

**R3. The self's box factored.**
- **Built:** D78's token and heads in `world_model.py` and `scene_model.py`, the tables written again.
- **Trained:** five members as R2's, on the tables R2 leaves.
- **Bars:** bump at least 51 (54 on R2's tables), stomp at least 40 (42), land at least 149; offline, the
  self's exact next box on held-out babbling no lower than probe 14's 39.6%, and stomp's deaths beside the
  enemy (the touch within 3 px of the enemy's edge) at most half of R0's count.
- **If refuted:** R4, where R0's classes (read again on R3's probe) still put the bump misses on M.

**R4. Rules for the self in the air.**
- **The check first** (offline, the tables as they are): the share of held-out babbling's air steps without a
  contact where the self's next vertical motion is fixed, within a line, by its last 8 motions and actions.
  **Its bar:** at least 95%. Under it, the rules have no function to find and R4 isn't built.
- **Then** its own plan and registration (the rule language, the search, the bars), written from the check.
- **If refuted or not built:** W6 ends with its failure placed (D30, D80), and the gate and W5 go to the owner.

**The registration** (whichever step passes): the battery on L1′'s 100 episodes, all three kinds, the reference
beside it on the same attempts, the gate 80% a kind, once (D30). No model in it trained on L1′.

**Feasibility.** Bump needs 5 more of the 17 the reference reached and the model missed; stomp needs 3 to 5 more
of 15. R1's cells run only where R0 shows their class. R2's and R3's bars are reachable on F2's figures (a
landing foreseen by half the members now). R4 is gated by its own check.

**Machines.** `stone` at 70% (8 threads), on AC power, two trainings at a time (each peaked at 8.8-12 GB);
battery runs with `--workers 8` and one thread each. Development and the tools' tests on `pyramidon`. Nothing
on `jebel`.

#### W6's fifth round: R0 and R1's results (2026-11-13)

**Built** (indrajala-rl #102, #103): `planner_battery.py --trace` writes each planned decision's candidates (by
member: the chance of reaching, of dying and of what, of reaching at the first step; the chosen one);
`follow_check.py` reads F1, F4, F5, the classes and, on a followed result, F2; `--repeat R` keeps the goals and draws
the planning and sticks afresh. **One change to R0 as planned:** run 2 was "the reference on seeds 1 and 2", but the
seed also draws the goals, and a run without `--model` skips D59's filter (seed 1 attempted 125 bumps against seed
0's 78). Run 2 became the reference and the model together, `--repeat 1` and `2`, on probe 14's 141 attempts. A
class P (pursuit: the chosen candidate reaches later in a member) is read beside F8's four.

**R0, run 1** (probe 14's ensemble, bump and stomp, traced): 46 and 35, as probe 14; F1's table is the analysis's.

| still decisions of missed attempts | C | P | V | D | S | decisions |
|---|---|---|---|---|---|---|
| bump | 0.00 | 0.08 | 0.03 | 0.01 | 0.88 | 522 |
| stomp | 0.00 | 0.16 | 0.13 | 0.00 | 0.71 | 404 |

- **S rules:** where the self stands still, no candidate of 24 reaches the goal in any member. F7's veto (V) is 3%
  and 13%.
- **Deaths in candidates** are mostly touches (12,159 of the members' summed chances, vanishings 3,255, the bottom
  50). Of 427 decisions whose chosen candidate dies in a member, the game died within 16 decisions after 58.
- **Claims before the reach:** 1.43 a bump reached (F5's over-claim), 0.69 a stomp.

**R0, run 2: each path against itself.**

| | seed 0 | repeat 1 | repeat 2 |
|---|---|---|---|
| the reference, bump (of 78) | 63 | 57 | 56 |
| the reference, stomp (of 63) | 50 | 52 | 47 |
| the model, bump | 46 | 42 | 45 |
| the model, stomp | 35 | 34 | 28 |
| the reference, column 131 from the stair side (of 19) | 8 | 6 | 3 |

The repeats are 89-90% of seed 0's 63 bumps and 94-104% of its 50 stomps: no repeat falls under 80%, so the gate
can hold a registration as it stands. The model's own spread is 4 bumps and 7 stomps; within one run, the model
against the reference is 73.7-80.4% on bump and 60.0-70.0% on stomp.

**What R0 decides:** C1 (split combining) doesn't run (V and D together 4% and 13%, under a quarter); C2 (96
candidates) runs (S 88% and 71%); C3 (the bump test narrowed) runs (1.43 claims a reached bump, at least 1).

**R1** (on `klip`, model path only, against seed 0's reference; bars bump 51, stomp 40):

| cell | bump | stomp | S among bump's still decisions | stair side (of 19) | claims a bump reached |
|---|---|---|---|---|---|
| probe 14 (run 1) | 46 | 35 | 0.88 | 0 | 1.43 |
| C3, `--reach-bump 2 --reach-bump-columns 6` | 45 | 35 | 0.82 | 0 | 0.69 |
| C2, `--sequences 96` | 48 | **40** | 0.70 | 3 | 1.23 |

- **C3** halves the claims and gains nothing: dropped.
- **C2** meets stomp's bar, above the model's own range (28-35), and fewer still decisions find nothing; bump's
  48 is within the model's spread and under 51. Nothing to combine.
- **R1 is refuted on bump.** By its rule, C2 is R2's planner.

**R2 under way** (indrajala-rl #104: `--phase`, `--record`, `babble_from.py`). The play is C2's planner on probe
14's ensemble, the three kinds, `--every 480 --phase 240`, seeds 1-3, each attempt recorded from 36 frames before
its state so its tables hold the model's history. Seeds 1 and 2 run on `stone`, 3 on `klip`. **Its cost is above
the plan's 4 hours:** C2 plans four times as much, about 7 hours on the two machines. The rest as R2 says.

#### W6's fifth round: R2's results (2026-11-14)

**The play** (C2's planner on probe 14's ensemble, `--every 480 --phase 240`, seeds 1-3): 623 attempts a seed,
1,869 in all. Reached, by seed: land 260, 234 of 271; bump 65, 86 of 130; stomp 136, 141 of 222. Seed 3 was split
by machine (`klip` about 6x slower a decision than `stone`): recordings 1050-1099 on `stone` reached land 124 of
138, bump 16 of 68, stomp 72 of 115; 1000-1049 on `klip` (its log only).

**Babbling** (D27, `--every 20 --length 20`): 2,531 branches; the tables hold 223,974 boxes against the play's
211,042 (6% more: the same count within the plan's sense).

**Trained:** five members as probe 14's on the six tables (760,769 steps). Each peaked at 15-20 GB (8.8 GB on
the four); two at once were OOM-killed on `stone`, and seeds 1 and 2 were trained again alone, with the same
settings. Offline, the self's exact next box on held-out babbling: 44.8-46.5% (probe 14's members: 39.6-40.4%).

**Control** (C2's planner on their mean, probe 4's states, seed 0):

| kind | R2 | bar | R1's C2 (probe 14) |
|---|---|---|---|
| land | 184 of 193 | 149 | - |
| bump | 54 of 78 | 54 | 48 |
| stomp | 39 of 63 | 42 | 40 |

**Offline** (`--follow` on bump, the reference's actions, `follow_check.py --row 3`):
- F2, row 3's landings foreseen from the takeoff: 56 of 120, **46.7%** (bar 75%; probe 14: 54%).
- Row 3's foresight at 8 decisions: **0.71** (bar 0.80; probe 14: 0.62). The other goals' stays at 0.96.
- Row 3's rollouts that leave the truth first do so at a box size change (853 of 3,085), then rising (734) and the
  rise's end (405).

**R2's rule: neither holds.** Bump reaches its bar exactly; stomp is 3 under its own, and both offline bars fail.
By the rule, **R3 trains on the four tables, and the play's tables are set aside.** The play's gain in the self's
exact next box (about 6 points) did not carry to the landings from the takeoff, which fell. The leading first
departure, the box's size changing, is what D78 factors: R3 follows as planned.

Data: indrajala-studies' `data/smb-world-model/control/w6/r2/` (the tables and the corpus stay on `stone`:
`~/labour/w6/r2/tables/`, `~/labour/corpus/smb-w6-r2/`).

**R3 under way** (2026-11-14). **Built** (indrajala-rl #105, #106):
- `Settings.factored` (`world_check.py train --factored`): the history's motions and the four motion heads are the
  bottom's motion, the centre column's (half pixels, clipped at 32), the height's and the width's changes;
  `world_model.moved` rebuilds the box (height and width at least 1; where the centre and the width disagree in
  parity, the box sits half a pixel left), for the rollout, the scene model and the scores alike.
- **One change to R3 as planned:** the tables aren't written again. The factors are taken from the boxes when
  they are encoded, so probe 14's four tables serve.
- An unfactored model is unchanged (probe 14's `y0` re-scored: the same report, but "edges right" is now read from
  the rebuilt boxes' pixels, so a "beyond the clip" class no longer counts as right whatever the motion; the old
  figure is "heads right").
- `follow_check.py` reports stomp's deaths from a traced result's last decision: falls, and touches with their
  horizontal overlap. **R0's count:** 8 deaths, falls 3, touches 5 (overlaps 3, 3, 4, 5, 8 px), **beside the
  enemy (at most 3 px) 2**: R3's bar is at most 1. (R2's: 4 touches, 5-9 px, none beside.)

**Run:** five members on the four tables, seeds 0-4; C2's planner on their mean, the three kinds, traced; then the
follow (bump) for F2 beside the bars.

Data: indrajala-studies' `data/smb-world-model/control/w6/r0/` and `r1/`.

#### W6's fifth round: R3's results (2026-11-14)

**Trained:** five members with the factored box (D78) on probe 14's four tables, seeds 0-4, as planned; each
peaked at 8.8 GB. Offline, the self's exact next box on held-out babbling: 46.7-47.7% (probe 14's: 39.6-40.4%;
R2's: 44.8-46.5%).

**Control** (C2's planner on their mean, probe 4's states, seed 0, traced):

| kind | R3 | bar | R2 | R1's C2 (probe 14) |
|---|---|---|---|---|
| land | 177 of 193 | 149 | 184 | - |
| bump | **46** of 78 | 51 | 54 | 48 |
| stomp | **39** of 63 | 40 | 39 | 40 |

- **Stomp's deaths:** 9; falls 2, touches 7 (overlaps 4-9 px); **beside the enemy (at most 3 px) 0** (bar at most
  1; R0's 2). The factored box did what it was aimed at here, and stomp's count didn't move.
- **The planner's view** (still decisions of missed attempts): S 0.61 on bump (R0: 0.88), 0.64 on stomp (0.71).
- **The follow** (bump, `--row 3`): row 3's landings foreseen from the takeoff 56 of 120, **46.7%**, as R2's; row
  3's foresight at 8 decisions **0.70** (the other goals' 0.97). The first departures of row 3's rollouts: rising
  934, the box's size changing 797 (R2: 853), falling 481.

**R3 is refuted on control** (bump 5 under its bar, stomp 1), with both offline bars holding. R0's classes still put
the bump misses on the members' foresight (M), so by the plan R4's check came next.

Data: indrajala-studies' `data/smb-world-model/control/w6/r3/` (the members, the battery and the follow, and
`c2-check.txt`, `follow-check.txt`).

#### The plan stopped (2026-11-14)

**The owner stopped the plan after R3:** "stop the smb-world work, and clean up"; "clean up fully. this is going
nowhere, and blocking other real work"; "also retire the workplan". R4 (its check included), W6's registration
on L1′, W5, W7, W13 and W12 are not run, and nothing of them is carried forward.

**Where it stood.** The layers below the model hold (W10, W11, W2.4, W3, W4). Control on the learned model, on
probe 4's states and the oracle's scenes, reached land at 92-98% of the reference, bump at 59-80% and stomp at
60-80% across five rounds, under the 80% gate on bump and stomp in every round's registered probe. The limit
found is the self's motion at the climb: jumps with 1-2 lines to spare, where half the members' rollouts foresee
the landing; larger networks, rollout training, an ensemble, longer histories, the planner's own play and the
factored box each moved it a few points at most. Nothing was run on the organ's scenes above W4, nor on another
level's states or another game.

**What stays:** the code in indrajala-rl (the scene, the oracle, the organ, the self, the world model, the
planner and its battery, `follow_check.py`, `render_recording.py`) and indrajala-nes; the data in
indrajala-studies' gitignored `data/smb-world-model/`. The runners' copies (corpora, tables, models, worktrees)
were deleted on 2026-11-14. Studies keeps W1's corpus and W11's deep play as recordings; the babbling corpora,
the test sets, R2's play and the tables built from them are gone.
W8 stays the told plan's stage 6, without this plan's organ tracks as a dependency.

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

#### W11's fallback: the result (2026-11-11)

Run on `stone`, 8 workers, as registered (indrajala-rl `8bd680d`), 06:35-12:14. **L1′ holds: 1-1 is cleared at
95 of 100. W11's gate is passed: L1′ for the level, G1-G3 for the battery.**

| claim | the test | refuted by | the result |
|---|---|---|---|
| L1′. 1-1 cleared | episodes cleared of 100 | under 90 | **95 of 100: holds** |

**The level:**
- 95 cleared, 5 died, none out of decisions. Cleared episodes took 328-394 decisions (median 357).
- **Deaths, 4 fell and 1 hit:**

  | seed | cause | x | decisions |
  |---|---|---|---|
  | 4055 | hit | 676 | 74 |
  | 4094 | fell | 1132 | 149 |
  | 4063 | fell | 1443 | 157 |
  | 4074 | fell | 1446 | 149 |
  | 4007 | fell | 2481 | 297 |

  Each is at a place where L1's deaths were: the falls at 1-1's three pits, the hit at the first Goomba.
  L1's six hits at x 1791-2021 are gone.
- **Frames a decision:** 17,179-18,248, mean 17,907; a median of 28 minutes an episode on one of 8 workers.
- **The fallback's runs agree:** the `exact` 6 probe and L1′ each cleared 95 of 100, so 190 of 200 at these
  settings (95%), against L1's 82 of 100 at `exact` 3.

**The `exact` 6 probe's five deaths, traced** (`planner_trace.py`, on `klip`; every replay matched its episode):
- **3 met the window's edge** (seeds 3018, 3039, 3042): the score stays about +9 until a run of sticks longer
  than 6 decisions, or a press the plan needs past its 6th, is reached; then it drops to about -243 and to death,
  as `exact` 3's 6 sudden drops did.
- **2 were long runs of sticks** (3043, 3072): the action repeated past what a window of 6 counts, at odds of
  about 1 in 4,096 or less.
- So the residual deaths are the same mechanism at a smaller rate, not a new one. A wider window or a sticky tail
  (D30) would shrink it further, at about 1.5 times the frames a step of `exact`.

**L1′'s five deaths, traced** (`planner_trace.py` on `stone`, `l1btrace/`; every replay matched its episode's cause
and place). Each was a stick or a run of sticks, as the probe's:
- **4055 (hit, x 676) and 4094 (fell, x 1132): the score fell with no stick,** from +7.4 to -8.3 and from +5.7 to
  -199: a danger entered the 6-decision window from beyond it.
- **4063 and 4074 (fell, x 1443 and 1446): one stick took the score from about +8 to -58, two more killed;** both
  near x 1300, before the second pit.
- **4007 (fell, x 2481): four decisions at a rated risk** (best scores -19 to +1, at the third pit), then three
  sticks in a row.

**The data:** L1′'s 100 recordings (seeds 4000-4099) replay to their own final RAM under `corpus_manifest.py`;
with W11's 100 they make 200 episodes of deep play. Both probes' logs, the `exact` 6 probe's recordings and
traces and L1′'s traces are with them in indrajala-studies' gitignored `data/smb-world-model/planner/w11/`
(`l1b/`, `l1btrace/`, `x4/`, `x6/`, `x6trace/`).

#### W11's every-level pass (2026-11-11)

One episode on each of the 32 levels at L1′'s settings (indrajala-rl `8bd680d`, seed 5000, sticky 0.25, up to
3,000 decisions), on `klip`, 8 workers. **13 of 32 cleared.** Reported, not claimed: one episode a level tells
which levels the planner can clear, not its rate on them.

| level | outcome | x | decisions | | level | outcome | x | decisions |
|---|---|---|---|---|---|---|---|---|
| 1-1 | cleared | 3161 | 356 | | 5-1 | cleared | 3177 | 404 |
| 1-2 | cleared | 3161 | 528 | | 5-2 | fell | 1083 | 135 |
| 1-3 | fell | 1486 | 195 | | 5-3 | fell | 1543 | 200 |
| 1-4 | cleared | 2265 | 266 | | 5-4 | fell | 440 | 48 |
| 2-1 | fell | 1561 | 194 | | 6-1 | cleared | 2969 | 338 |
| 2-2 | fell | 2514 | 706 | | 6-2 | cleared | 3449 | 658 |
| 2-3 | cleared | 3593 | 419 | | 6-3 | fell | 916 | 209 |
| 2-4 | fell | 436 | 48 | | 6-4 | cleared | 2260 | 286 |
| 3-1 | hit | 2435 | 371 | | 7-1 | cleared | 2857 | 336 |
| 3-2 | cleared | 3337 | 351 | | 7-2 | hit | 2561 | 1253 |
| 3-3 | fell | 1005 | 125 | | 7-3 | fell | 2920 | 354 |
| 3-4 | cleared | 2260 | 270 | | 7-4 | hit | 443 | 2406 |
| 4-1 | cleared | 3593 | 519 | | 8-1 | fell | 5829 | 694 |
| 4-2 | fell | 2946 | 855 | | 8-2 | fell | 2438 | 398 |
| 4-3 | fell | 1256 | 1393 | | 8-3 | cleared | 3417 | 417 |
| 4-4 | hit | 421 | 2406 | | 8-4 | fell | 1206 | 142 |

- **Of 19 not cleared, 15 fell and 4 were hit.** A fall is the planner's one common way to die, as on 1-1.
- **The castles' early falls** (2-4 and 5-4 at about x 440 after 48 decisions): their first pits come within the
  first screens.
- **The maze castles (4-4, 7-4) defeat a planner scored by progress in x:** about 2,400 decisions each, still at
  x 421 and 443 when hit. A wrong path sends the player back, and nothing in the score says which path is right.
- **Frames a decision:** 15,073-21,223 (17,000-18,500 on most levels; the maze castles' longest).
- **What it tells the plan:** W11's gate is 1-1's (L1′); the other levels are where W7's level stage (the planner
  on the model's predicted reward) will be read against this one. A level the reference planner can't clear
  can't be a gate for a learned model's.
- **The data:** the 32 recordings (69,292 frames) replay to their own final RAM under `corpus_manifest.py`;
  `levels/` beside the rest (logs, `deep/` with its manifest).

**What follows:** W2.4 as amended (D28), on the deep play.

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
