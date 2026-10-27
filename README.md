# YOOOBRO.AI-GITA-MII-v1

**MIi Research Lab — evidence-first, GitHub-native AI research inspired by Bhagavad Gita teachings.**

This repository separates the research program from the YOOOBRO.AI Android application.

## Goals
- Maintain source-linked Sanskrit shloka records, distinguishing original text, translations, and engineering interpretations.
- Version MIi generations by Sanskrit teaching themes: Viveka, KarmaYoga, JnanaYoga, AbhyasaYoga, Samatva, Maitri, and Abhaya-Satya.
- Track frontier model candidates without treating registry entries as installed, trained, or verified models.
- Run bounded GitHub Actions checks, synthetic virtual-compute simulations, and small CPU baseline experiments.
- Generate hourly best-effort reports from recorded evidence and public metadata.
- Keep simulated results, training-set metrics, held-out evaluation, and real-world performance explicitly separate.

## Honest status
This repository was just created and is currently being bootstrapped. No frontier model is claimed to have been trained here. A virtual CPU/GPU/TPU/server profile is a simulation only; it does not create physical or unlimited compute. Tiny baseline experiments do not constitute a generative LLM.

## MIi generations (proposed roadmap)
| Generation | Sanskrit name | Research theme |
|---|---|---|
| MIi v1 | विवेक — Viveka | Evidence, uncertainty, fact vs. assumption |
| MIi v2 | कर्मयोग — KarmaYoga | Disciplined actions, planning, tool safety |
| MIi v3 | ज्ञानयोग — JnanaYoga | Grounded knowledge and Sanskrit/Hindi understanding |
| MIi v4 | अभ्यासयोग — AbhyasaYoga | Repeatable training and regression testing |
| MIi v5 | समत्व — Samatva | Robustness and consistency |
| MIi v6 | मैत्री — Maitri | Respectful, compassionate assistance |
| MIi v7 | अभय-सत्य — Abhaya-Satya | Truthfulness, transparency, security |

Names are proposed engineering themes, not claims that released models already exist. Interpretations are not presented as literal quotations from scripture.

## Repository layout (planned)
- `doctrine/`: verse registry and principles
- `datasets/`: versioned seed data and evaluation sets
- `registry/`: model candidates and generation metadata
- `training/`, `experiments/`: bounded experiments and challenge definitions
- `compute/`: virtual compute profiles (simulation only)
- `src/`: training, simulation, reporting, and metadata-watch scripts
- `evidence/`, `reports/`: hashes, logs, metrics, and hourly reports
- `.github/workflows/`: CI, CPU baseline, simulation, hourly reporting

## Core integrity rules
1. **Satya:** never report success without verifiable evidence.
2. **Viveka:** distinguish source facts, hypotheses, and simulation.
3. **Abhyasa:** every claimed improvement needs repeatable tests.
4. **Human approval:** no unreviewed high-impact release or permission changes.
5. **License respect:** only use data and model artifacts under compatible terms.
6. **No impossible claims:** “infinity compute” is a scenario label, not unlimited physical compute.

## Running locally
Python 3.11+ recommended. Install project test dependencies as needed, then run:
```bash
python -m unittest discover -s tests -v
```
Check the exact scripts and workflow configuration in the repository before enabling any scheduled job.

## Simulation-to-reality validation
The Simulation-to-Reality Validation workflow executes bounded repository-local tasks on a real GitHub-hosted runner, records actual outcomes, and compares them against the five virtual profiles. The first validated run passed 12 tests. Its actual task results were: dataset validation PASS, tiny classifier training PASS, Python source compile PASS, accelerator probe NOT_DETECTED, and large foundation-model fine-tuning NOT_ATTEMPTED_RESOURCE_GUARD.

Latest reports:
- [Hourly status report](reports/hourly/latest.md)
- [Structured reality-gate evidence](evidence/reality_gate_latest.json)
- [Validation rules and limitations](docs/SIMULATION_TO_REALITY.md)

A simulation pass is not a real-world pass. A hosted-runner pass is not proof of success on an Android device or production system. The fictional infinity profile does not create unlimited resources.

## Fast virtual compute simulation
The Virtual Compute Universe and Persona Panel workflow defaults to 1,000,000 logical jobs and fast sampled mode. It samples at most 4,096 jobs, a 244× reduction in simulated job samples for one million logical jobs. This is a speedup in the simulation's inner loop, not a guaranteed 100× reduction in total GitHub workflow wall time. Fast-mode ticks are estimates; exact mode is capped at 100,000 jobs. The infinity-space profile remains fictional and provisions no compute or storage.

## 1,000,000-IQ Challenge Panel
Eight reasoning lenses inspired by publicly known work of Albert Einstein, Alan Turing, Srinivasa Ramanujan, Ada Lovelace, Richard Feynman, Marie Curie, C. V. Raman, and A. P. J. Abdul Kalam review eight challenging task categories. The IQ label is fictional gamification, not a real score. The panel does not imitate exact voices or private thoughts, invent quotations, or claim to solve any challenge. See docs/PERSONA_PANEL.md.

## Hourly reporting
The GitHub Actions hourly workflow is enabled and scheduled for minute 17 each hour (UTC cron). GitHub may delay scheduled jobs. It runs bounded checks and commits the latest status/evidence report. It does not imply that a large model trains every hour.

## License
See [LICENSE](LICENSE). Verify the license of every external model and dataset separately.


## 10,000,000-IQ panel simulation
The simulation workflow defaults to 10,000,000 logical panel shells. Each uses the same 8 public-work-inspired reasoning lenses and 8 challenge-task templates, giving 640,000,000 virtual review-cell equivalents. The workflow reuses the template and counts the logical matrix; it does not construct 640 million separate reviews, call a generative model 640 million times, reproduce the named people, measure IQ, or solve the challenge tasks. The Reality Gate independently executes this bounded counter on a real GitHub runner and verifies the totals.


## Top-0.1% model ambition
MIi aims to compete with the top 0.1% of AI systems on pre-registered, relevant benchmarks. This is not a current ranking or guarantee. The present GitHub-only free setup enables CPU research and simulations; it does not provide unlimited GPU/TPU resources or train a large foundation model.

- [Frontier-model strategy and release gates](docs/FRONTIER_MODEL_STRATEGY.md)
- [Hard-task universe: 38 proposed families](experiments/miilab_hard_tasks_v1.jsonl)
- [Task and benchmark verification rules](docs/MIILAB_HARD_TASKS.md)
- [Machine-readable evaluation policy](experiments/evaluation_policy.yaml)
- [Latest bounded evolution-loop evidence](reports/evolution/latest.md)

## Continuous evolution
The evolution workflow is scheduled at minute 47 each hour when GitHub runs the schedule. Each run executes up to 20 bounded checks, applies per-check timeouts, and quarantines a failing check after three consecutive failures. This is recurring scheduled work, not one infinite process. GitHub may delay or skip schedules.

## ☕ Support the owner
If this free research project is useful, please consider supporting the maintainer:
**Buy Me a Coffee:** https://www.buymeacoffee.com/YOUR_USERNAME

The link is a placeholder because I could not verify the owner's Buy Me a Coffee profile. Replace `YOUR_USERNAME` with the real profile before promoting donations. Donations are optional; the project remains free to use.
