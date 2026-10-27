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

## Hourly reporting
The intended GitHub Actions workflow is best-effort and may be delayed by GitHub. It records status; it does not imply that a large model trains every hour. Enable the workflow only after its files are committed and validated.

## License
See [LICENSE](LICENSE). Verify the license of every external model and dataset separately.
