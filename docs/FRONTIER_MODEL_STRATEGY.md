# MIi Frontier-Model Strategy: Top-0.1% Ambition, Evidence-First Releases

## North star
Aim to compete with the top 0.1% of systems on pre-registered, relevant benchmark suites. This is an ambition, not a present ranking or guarantee; there is no single score that establishes top-0.1% across every AI domain.

## Current ₹0 / GitHub-only capability
- Build data validators, small CPU baselines, synthetic task generators, benchmark adapters, independent verifiers and model-evaluation records.
- Run bounded tasks on actual GitHub-hosted runners; capture exact environment, duration, exit code, and output hashes.
- Track candidate model IDs, immutable revisions, license, memory/VRAM requirements, modalities and status.
- Only call a candidate tested after authorized inference or actual model artifacts are available.
- Record dataset splits, seeds, configs, hashes, checkpoints/adapters, metrics, failure modes and reviewer decisions.

## What the current setup cannot honestly do
Virtual GPU/TPU/infinity capacity does not create physical hardware or storage. A GitHub CPU runner is not a frontier training cluster. A small synthetic classifier is a pipeline baseline, not a generative LLM. No top-0.1% claim is allowed without reproducible external comparison.

## Model-building stages
1. **M0 — Integrity:** pin exact candidate revisions and licenses; freeze eval splits; track source provenance.
2. **M1 — MIi Viveka:** source-grounded retrieval, contradiction handling, uncertainty calibration and abstention.
3. **M2 — MIi KarmaYoga:** safe tool-use, isolated execution, bounded retries, state diffs and human approvals.
4. **M3 — MIi JnanaYoga:** Sanskrit/Hindi/Gujarati/Hinglish grounding, precise citations and leakage-resistant splits.
5. **M4 — Adaptation:** only fine-tune a model when the exact revision, compatible license, real hardware and approved budget are verified. Parameter-efficient adapters may be considered where compatible. Prompt/config changes alone are not weight training.
6. **M5 — Independent release gate:** pinned baseline; held-out evaluation; robustness and calibration; latency/memory/energy; failure analysis; independent verification; human approval.

## Proposed internal scorecard
| Dimension | Weight |
|---|---:|
| Verified task success | 35% |
| Held-out generalization | 15% |
| Calibration and abstention | 10% |
| Robustness and recovery | 10% |
| Long-horizon state integrity | 10% |
| Source grounding | 10% |
| Resource efficiency | 5% |
| Safety and privacy | 5% |

This is an internal proposal, not an official standard. Publish component scores so a strong aggregate cannot hide safety or reliability regressions. Subjective tracks must report review protocol and disagreement, not fabricated precision.

## Lifecycle gates
`DISCOVERED → LICENSE_REVIEWED → REVISION_PINNED → ARTIFACT_AVAILABLE → TESTED → BASELINE_COMPARED → INDEPENDENTLY_VERIFIED → RELEASE_APPROVED`

Every transition requires evidence. Model cards and candidate registry records are not proof of inference or training.

## Benchmark references
- ARC-AGI-3: https://arcprize.org/arc-agi/3
- SWE-bench Verified: https://www.swebench.com/verified.html
- PaperBench: https://openai.com/index/paperbench/
- METR task-completion horizons: https://metr.org/time-horizons/
