# Arithmetic on written numbers: two problems (internal note)

**2026-11-02, from a discussion with the owner.** Short by design; the plan for the first problem is
[numeral-reader-workplan.md](../workplans/numeral-reader-workplan.md).

The question was whether to write up addition at any length for the length-generalisation literature.
Its conditions differ from ours in two ways: base 10, and operands written as a string, `a + b =`,
rather than as aligned columns. The owner's framing: these are two separate problems.

1. **Reading numerals (operator-independent).** From `a op b =` to the operands' digits paired by
   place value, zero-padded where the lengths differ. Its parameters are the base and the direction
   (the string is written most significant digit first; an operator may need the least significant
   first). It is the same for every binary operator on multi-digit operands, so it is learned (or
   programmed) once and reused.
2. **The operator.** Over aligned columns, each operator is a machine of its own, which is what the
   programme already learns and proves. Addition, subtraction, comparison, and multiplication or
   remainder by a constant are finite-state; general multiplication is not.

**Direction belongs to both.** Addition is a deterministic transducer least significant digit first;
read most significant first, a digit's output waits on a carry that unboundedly many later digits can
decide. So the operator fixes the order it needs, and the reader has to deliver it (and the answer,
emitted least significant first, has to be written back most significant first: a reversal, a reading
problem too).

**Why the reader is different in kind.** Pairing the i-th digit of `a` with the i-th of `b` is not
finite-state: a reader would have to hold all of `a`. It is computed by a finite controller driving two
read heads over the string, and by attention that can match positions; which formal class it falls in
is the plan's first literature question. The literature's strongest length-generalisation results
supply this alignment (position coupling, Abacus embeddings, index hints, reformatted inputs) rather
than learn it.

**What was decided:**

- Write the architecture note (the window-recurrent network as a reference, its controls and the
  library) after the certificate note.
- Leave the operator side (a base-10 addition note) for now; return to it once the reader exists.
- Research the reader in depth, with a detailed workplan:
  [numeral-reader-workplan.md](../workplans/numeral-reader-workplan.md).
