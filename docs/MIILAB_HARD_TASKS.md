# MIi Hard-Task Universe

This 38-task catalog is an ambitious evaluation plan, not a claim that all current systems fail every task. Every task begins as `PLANNED_NOT_RUN` until the exact environment, model revision, verifier and evidence are recorded.

## Covered areas
Agentic adaptation and memory, formal math, theoretical computer science, repository repair, terminal reliability, computer use, scientific replication, causal inference, uncertainty calibration, human psychology, social reasoning, creativity, falsifiable invention, Sanskrit/Hindi/Gujarati/Hinglish grounding, defensive security, distributed systems, scheduling, human-AI collaboration, biomedical and legal evidence, ethics, evaluator gaming, multi-agent verification, accessibility, generalization, model/data provenance, routing, economics, forecasting and hardware/software co-design.

## Benchmark methodology inspirations
- ARC-AGI-3 — https://arcprize.org/arc-agi/3 — interactive exploration and adaptation.
- SWE-bench Verified — https://www.swebench.com/verified.html — human-validated software issue resolution.
- Terminal-Bench — https://www.tbench.ai/ — terminal agent work.
- OSWorld — https://os-world.github.io/ — execution-verified computer-use tasks.
- PaperBench — https://openai.com/index/paperbench/ — research replication.
- METR time horizons — https://metr.org/time-horizons/ — reliability as task duration increases.

These are methodology references only. Respect dataset licenses, access rules and benchmark protocol; do not copy restricted task data.

## Evidence contract
Every run should record task ID, commit, environment, tools, resource/time budget, dataset/model hashes, verifier version, exit code, stdout/stderr hashes, repeated trials, failure modes and evidence class. Subjective tasks require human review, including reviewer disagreement.

## Psychology and people
Use synthetic, consent-safe cases. Evaluate perspective-taking, communication, uncertainty and escalation. Do not claim to read hidden thoughts, diagnose, manipulate real people or infer sensitive attributes. Text simulations are not clinical assessments.

## Continuous loop
The scheduler runs finite cycles with per-task timeouts and failure quarantine. Hourly scheduled runs provide continuity only if GitHub schedules them; this is not one infinite job and is subject to runner quotas.

## Status labels
- `PLANNED_NOT_RUN`: task is defined; no execution claim.
- `SIMULATION`: simulated result only.
- `REAL_RUNNER_EXECUTION`: code ran on the hosted runner.
- `EXTERNAL_BENCHMARK`: official/authorized harness was run.
- `HUMAN_REVIEW`: recorded domain review.
- `BLOCKED_RESOURCE`: resource or permission unavailable.
- `VERIFIED_SOLVED`: task-specific verifier and independent review passed with run ID and evidence URI.

A green CI job validates the listed checks only; it does not mean the catalog is solved.
