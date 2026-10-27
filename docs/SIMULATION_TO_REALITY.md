# Simulation-to-Reality Validation Gate

## Purpose
Test whether the same bounded, deterministic repository tasks that a synthetic simulation labels successful can actually execute on the GitHub-hosted runner. Simulation is not treated as proof; actual process results, outputs, hashes, and artifact round trips are captured separately.

## What is genuinely executed
- Parse and validate the checked-in synthetic dataset.
- Train the tiny Naive Bayes baseline in memory, serialize it into a temporary directory, reload it, and rerun predictions.
- Compile Python source strings from the repository.
- Probe the current runner for recognizable accelerator signals without downloading dependencies or running production workloads.

These are real code executions on the runner when the workflow runs. They are not proof of capability on the founder's Android device, a production server, external accounts, or an end-user environment.

## Simulation comparisons
The virtual CPU/GPU/TPU/server/infinity-space profiles use explicit synthetic assumptions. Each comparison records the simulated prediction, actual runner status, comparison class, and whether real execution was attempted.

A simulation/reality gap is reported when the simulated profile assumes an accelerator is available but the actual runner does not detect one. NOT_DETECTED is not proof that no accelerator exists in the underlying infrastructure. The infinity-space profile is fictional; it cannot provision unlimited storage or compute.

## Guarded tasks
Large foundation-model fine-tuning is labelled NOT_ATTEMPTED_RESOURCE_GUARD, not success or failure. It remains blocked until exact weight revisions are pinned, the license is reviewed, accelerator memory and storage are measured, and compute budget is explicitly approved.

## Interpretation rules
- Simulation pass is not a real-world pass.
- Real runner pass is not a production/device pass.
- Training-data accuracy is not held-out accuracy.
- Model metadata is not model weights.
- A role manifest is not a deployed autonomous agent.
- No production, payment, account, device, or destructive action is performed by this workflow.

## Run locally
Set PYTHONPATH to src, then run: python -m unittest discover -s tests -v
Then run: python -m miilab.reality_gate


## 10M persona panel stress validation
The Reality Gate runs a bounded 10,000,000-panel simulation counter on the actual GitHub runner. It verifies that 10,000,000 panel shells are processed and that their template implies 640,000,000 virtual review-cell equivalents. Only the panel-shell loop executes; all repeated lens/task cells reuse the same immutable template. No large model inference is performed, no human IQ is measured, and no frontier challenge is marked solved by this counter.


## Explicit simulation over-promise accounting
If a virtual profile predicts `SIMULATED_SUCCESS` but the same real task is blocked by a resource guard, the gate records `SIMULATED_SUCCESS_REAL_BLOCKED_GUARD`. This is counted as a simulation/reality gap rather than hidden in the not-run bucket. When both the simulator and the real gate agree that a task is unavailable and it is not attempted, it remains `NOT_COMPARABLE_NOT_RUN`.
