# Workplan: a finite-state machine that clears 1-1

**Status (2026-11-08): drafted. A sub-plan of the NES plan (`nes-one-network-workplan.md`); IDs continue its
own (D1-D23, O1-O2). The owner's switch (O3) set the conv network's gate aside for this. Decisions D24-D31
settled under the owner's delegation, with their options below. M1 (the library) done 2026-11-08 (indrajala-ml
#1282-#1286, crate #119; below, M1's result); M2 (recurrent PPO) next.**

**The owner (O3, 2026-11-08):** after the first 1-1 probe's diagnosis: "because the game environment itself is
actually a finite state machine - with a small number of optimal solutions - which are in fact themselves
finite state machines ... can we not rather reformulate this as an experiment in finding a winning finite state
machine using our gradient descent snapped/finite state windowed network architecture?"; "for just e.g. 1-1";
"we don't have to enumerate the env, we just play until we die or win ... over and over again"; "we know when
we have a valid machine because it passes the level"; then "let's just switch to the finite state machine
approach".

**The question.** Can PPO, through our snapped recurrent architecture, find a policy that is exactly a
finite-state (Mealy) machine, from observations to the 12 actions, and that clears 1-1 under sticky actions?
How small is the machine it finds, read off and minimised?

**Why it is the right next question** (the probe's diagnosis, the NES plan's Findings):
- The conv network has no state. Its input holds 4 decisions of positions, nothing more.
- **10 of the 19 greedy failures** at checkpoint 1,037 are one trap. On 1-1's final staircase, one step from
  the top, it holds Right+A (or Right+A+B) for 1,800 decisions until time runs out.
- **The NES jumps only on a fresh press of A,** so a series of jumps needs press, release, press. That's a
  two-state machine. A policy with no state, facing an unchanging screen, gives the same output forever.
- A learned finite state is the general remedy; a hand-fed previous action would be a special case of it.

## What "a valid machine" means here

1. **It is a finite machine, exactly.** The snap replaces the policy's state by one of `m` codes, so the
   policy is a Mealy machine whose states are codes and whose inputs are observations. This holds at every
   step where the snap has no near tie (a margin of 1.05, as the certificate's).
   - We read the machine **on the observations it meets.** Over the evaluation's episodes we tabulate each
     visited (code, observation) pair's next code and action, then minimise the table by partition
     refinement over the observed inputs.
   - **The input alphabet is the set of observations, which we can't enumerate.** So the claim is exactness
     on the visited set, every visited step checked for near ties, not a certificate over all inputs. A
     symbolic certificate isn't possible for an alphabet of grids.
2. **It passes the level, by playing** (the owner's "we know when we have a valid machine because it passes
   the level"):
   - **The bar:** at least 90 of 100 attempts, sticky actions on.
   - **Greedy play is the machine itself:** each code and observation gives the most likely action.
   - **A pass is confirmed** on a fresh evaluation seed: one look at a policy whose true rate is 85% passes
     90 with chance about 0.10, and the probe's 93 fell to 81 on new seeds.
   - **No enumeration of the game:** we play until Mario dies or wins, over and over.

**Sticky actions stay (D5).** Without them, a counter of about 358 states replaying one button sequence
would win. That's memorising, and sticky actions are this plan's guard against it, in place of the
exclusion bound, which needs a target machine we don't have.

## Decisions (settled under the owner's delegation; options with pros and cons)

- **D24. The bar.**
  - (a) *Chosen.* **Greedy play, at least 90 of 100 sticky attempts, confirmed by a second 100 on a fresh
    evaluation seed; within 10M decisions (the gate's cap); the machine read off (codes used, states
    after minimising, near ties on the visited set: none).** Pros: greedy is the machine; the confirmation
    removes the first-look bias the probe showed. Cons: two evaluations a checkpoint; greedy play can't
    break a loop by luck, which is the point: the machine must.
  - (b) Sampled play. Cons: a sampled policy isn't a machine; its noise is a training device.
- **D25. The network.**
  - (a) *Chosen.* **Split (D18), with only the policy recurrent.**
    - The policy keeps today's body, `Conv(1,16), Conv(3,16), Pool(2), Conv(3,32), Dense(256,"relu")`, as
      the step's window. The snapped state enters it through a StateInput, and the state's factors are
      pooled and snapped as in the library's window-recurrent network (GRU cell, codes).
    - The value network stays today's feed-forward body.
    - Pros: the machine is the policy alone; the value's job, already working, is unchanged; the window is
      the body that cleared 1-1 89-93 times in 100, greedy.
    - Cons: the window is a conv stack, not the library's token window, so the library needs a new window
      kind (M1).
  - (b) The paper's window: transformer blocks over the 208 tile cells as tokens. Pros: the architecture as
    published. Cons: about 208 tokens through 3 blocks every decision, many times today's step; no evidence
    it sees the level better.
  - (c) A recurrent value too. Pros: one recurrence. Cons: the value needn't be a machine; doubles the new
    cost (D18's split doubled the update already).
- **D26. The observation.**
  - (a) *Chosen.* **As now, 4 decisions of positions** (`HISTORY` 4). Pros: existence first, from what worked
    (the experiment design, section 1); the machine's states then carry only what the window can't (the
    press-release, the trap). Cons: some memory sits outside the machine, so "the machine's states" aren't
    all the policy's memory; the refinement (`HISTORY` 1) comes after a machine exists.
  - (b) `HISTORY` 1. Pros: all memory in the machine. Cons: speed must be learned into the state first; a
    harder first probe.
- **D27. The state.**
  - (a) *Chosen.* **Two factors of 8 codes each** (64 joint codes), **state width 32 each** (register row 9).
    Pros: factored, not flat (each factor can hold one thing: the press-release, the trap); generous for
    existence, about 30 times the 2 states the jump needs (the surplus rule of 3-5 times, row 1, is against
    an unknown need here, so it errs high). Cons: more codes to read off; minimising shrinks them.
  - (b) One factor of 8. Pros: the smallest readable machine. Cons: against the factored rule; one factor
    holding everything.
- **D28. The snap under PPO.**
  - (a) *Chosen.* **The library's coupling and commitment** (register rows 8 and 16): the continuous path
    first, the codes taking the state over as they sharpen, `(1 - l) h + l q`. Pros: the mechanism every
    certified network used; an abrupt snap lost formed states. Cons: tuned on supervised tasks; PPO's
    gradient is noisier.
  - (b) A hard snap from the start (straight-through). Pros: a machine at every step. Cons: S4 lost a formed
    state to an abrupt snap (row 16).
- **D29. Recurrent PPO.**
  - (a) *Chosen.* **Each environment carries its policy state through its rollout of 256 decisions;
    minibatches are sequences of 32 decisions, each starting from the state stored at its start, with
    backpropagation through the 32.** Pros: the standard stored-state recipe (R2D2's); 32 decisions is over
    two seconds of play, more than the press-release needs; the minibatch count (8) is kept. Cons: the stored
    state is from before the update (stale); no burn-in at first.
  - (b) Whole rollouts as sequences. Pros: no stale states. Cons: 256 steps of backpropagation, memory and
    time; fewer, larger minibatches.
- **D30. The control** (D16's role: does recurrent PPO work before 1-1).
  - (a) *Chosen.* **A memory task with a known machine:** a corridor where a cue at the start (left or
    right) decides the correct turn at the end, the corridor's length drawn per episode. Its minimal winning
    controller has 2 states. **Passes when it clears at least 95 of 100 greedy and its machine, read off,
    minimises to the known 2 states.** Pros: tests the whole path, training, snap and reading off, against a
    known answer (certify where a model admits proof); fast. Cons: our own task, not a published reference.
  - (b) A published recurrent PPO (CleanRL's LSTM) on a POMDP. Pros: an external yardstick. Cons: an LSTM
    isn't our snapped cell; it says nothing about reading a machine off.
- **D31. Order and machines.**
  - (a) *Chosen.* **The library (M1), then PPO (M2), the reader (M3), the control (M4), then 1-1's probes
    (M5) and the registered batch (M6).** Development on `pyramidon`; the control and probes on `klip` and
    `stone` (the NES plan's machine rules). Pros: each layer tested before the next rests on it. Cons: days of
    building before 1-1 is tried.

## Feasibility (the register, written beside the cell)

| check | the 1-1 cell | the control |
|---|---|---|
| codes against the states needed (row 1) | 64 joint against at least 2 (the press-release); the rest unknown: the reader measures it | 64 (2 factors × 8) against 2 |
| memory span | the press-release needs 1 decision, the trap a few; sequences of 32 | the corridor's longest length, at most 32, within one sequence |
| memorising | sticky .25 (D5): an open-loop tape fails | the corridor's length drawn per episode: no fixed tape |
| the window's width (row 3) | today's body, which cleared 1-1 (greedy 89-93/100) | the same body, on a small grid |
| the decision limit | 4,000 against a clear's 358 | the corridor's length plus 2 |
| the reader sees the machine (row 14) | every visited step's code and near ties | every state of the 2 reached in each episode |

## Stages

| # | What | Where | Done when |
|---|---|---|---|
| M0 | This plan | indrajala-research | merged |
| M1 | A window-recurrent network with a window of array layers (a conv body on planes), learning from a given output gradient at every step of a sequence | indrajala-ml (the crate first if Rust changes) | tests: the token window unchanged (golden run bit-identical); finite differences through the sequence and the snap; numpy against Rust; a saved network round-trips |
| M2 | Recurrent PPO (D29): stored states, sequence minibatches, the split policy | indrajala-rl | a resumed run equals an uninterrupted one; the losses' gradients by finite differences; the conv policy's path bit-identical to today's |
| M3 | The reader: a greedy policy's machine from evaluation episodes, near ties flagged, minimised by partition refinement | indrajala-rl | a hand-built 2-state policy read back exactly; a near tie reported |
| M4 | The control (D30) | indrajala-rl, `klip` | passes, or a diagnosis |
| M5 | Probes on 1-1 (existence first), one seed to the cap, varied on the fly | `klip` | one machine passes D24's bar, or a diagnosis to the owner |
| M6 | Registration (5 fresh seeds), the batch, the result | indrajala-research, `klip` and `stone` | registered before the data; the result or a diagnosis to the owner |

**M1's result (2026-11-08).** indrajala-ml's window-recurrent network takes a window of array layers (a Conv or
Dense first; the state as one token after the conv stack, D2 there). What M2 calls:
- `run_steps(X, *, state=None, starts=None, machine=False) -> Steps(outputs, states, codes, cells)`. The default
  reading is the training step's, so PPO's first ratio is exactly 1 on the same rows; `machine=True` gives the
  hard-snapped machine and each step's codes (M3's input).
- `learn_batch_output_gradient(lr, X, gradient, clip_norm, *, state=None, starts=None)`. `gradient(Y)` is called
  once on every step's outputs `(N, S * n)` of the step's own forward pass. The codes' losses are weighted 1/S, so
  a loss that is each row's mean over its steps keeps their tuned share.
- `state` is the stored state before the first step (it takes no gradient). `starts` `(N, S)` flags the steps
  where an episode began.

On Rust, the policy's window (conv, conv, pool, conv, StateInput, ReLU, given output) runs as one crate call per
pass. The workplan, retired, is `git show 32d4d23:docs/workplans/library/array-window-workplan.md` in
indrajala-ml.

**For M2's recipe:** a 2-step memory toy (a cue, then a blank screen) was learned to 100% with every factor
snapped only through the coupling's handover (0 to 1 over 300 steps: 8 of 8 seeds). With hard codes from the
first step, 2 of 3 seeds collapsed both cues onto one code. That is D28's risk, seen in small.

**Budget:** measured at M2's first probe (decisions a second against the conv probe's, about 215 on `klip`: 8,192 in about 38 s), then M5's and
M6's in decisions; 10M decisions a seed, as the gate.

## Findings

None yet.
