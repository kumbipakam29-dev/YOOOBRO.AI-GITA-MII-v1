# Project Context

MIi means Make in India. Current research tagline: “Made in India. Built to Safeguard Humanity in the Age of AI.” Guiding slogan: “Secure Intelligence. Responsible Autonomy. Human Dignity.”

The research program is inspired by Bhagavad Gita teachings but treats source text, translations, commentary, and engineering design decisions as distinct layers.

## Research scope
- GitHub-native repository and bounded free CI jobs.
- Public model metadata watchlist and license review.
- Small CPU baselines for pipeline validation.
- Synthetic compute scheduler for experiments and education.
- Future model adapters only when actual compute, dataset rights, and evaluation design are available.

## Non-goals and limits
- This repo does not provide infinite compute, unlimited storage, or real GPU/TPU allocation.
- A synthetic classifier is not a generative LLM.
- Frontier benchmark plans are not solved tasks.
- GitHub Actions free quotas are finite; full frontier-model pretraining is not assumed feasible on hosted CPU runners.
- No model should self-approve its own release or high-impact permission changes.

## Evidence classes
- ACTUAL_TRAINING: a training program ran and emitted an artifact plus metadata.
- SIMULATION: computed from synthetic assumptions only.
- PUBLIC_METADATA: retrieved public model-card information, without implying model execution.
- EVALUATION: a recorded test run with exact benchmark, split, command, environment and result.
