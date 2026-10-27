# 1,000,000-IQ Challenge Panel

## What it is
A structured simulation that places difficult tasks under eight analytical lenses inspired by public historical work: Albert Einstein, Alan Turing, Srinivasa Ramanujan, Ada Lovelace, Richard Feynman, Marie Curie, C. V. Raman, and A. P. J. Abdul Kalam.

The label **1,000,000-IQ** is fictional gamification. It is not an IQ estimate for any of these people or for MIi. The registry does not imitate exact voice, private thoughts, personal identity, or fabricate quotations. It does not claim that any real person is participating or endorsing the project.

## What the panel outputs
For each persona lens × challenge task, the engine emits:
- problem-framing questions;
- a known failure mode to guard against;
- a suggested verification method;
- the verifier required by the task;
- explicit status `PERSPECTIVE_SIMULATION_NOT_SOLVED`.

This is a deterministic checklist generator, not a generative AI model and not a solver for open problems. It may help structure multi-perspective review, but it cannot be used as evidence that a mathematical theorem, scientific claim, or software change has been solved.

## Real-world validation rule
A challenge moves from simulation to real-run validation only when the same task is executed in an appropriate real test environment and its output is checked by the declared verifier. A GitHub runner pass alone does not prove success on production systems, personal devices, or inaccessible external services.


## Ten-million-panel stress mode
The default scaled stress run processes 10,000,000 logical panel shells over the same 8 reasoning lenses and 8 challenge tasks. It calculates 640,000,000 virtual review-cell equivalents while iterating each panel shell; those 640 million review cells are **not** individually materialized, and this is **not** 640 million model calls. The exercise validates loop completion and count integrity only. A task is not solved until an appropriate solver/verifier executes.
