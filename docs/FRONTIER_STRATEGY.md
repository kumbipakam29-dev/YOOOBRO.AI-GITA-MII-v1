# Frontier Challenge Strategy

## Research tracks
1. Hard mathematical reasoning and proof verification.
2. Formal theorem proving with machine-checkable proof objects.
3. Repository-level software engineering with tests and sandboxed execution.
4. Interactive adaptation and long-horizon planning.
5. Scientific replication with cited evidence and reproducible scripts.
6. Sanskrit source-grounding and translation comparison.

## Evaluation rules
- Pin exact benchmark version, split, license, verifier and evaluation command before running.
- Separate public benchmark results from MIi's own independent runs.
- Record commit SHA, environment, seed, runtime, output hash and verifier result.
- Never claim an unsolved task is solved from a model's self-report.
- Respect gated or restricted benchmark data and terms; do not scrape protected tasks.
- Baseline first, then compare candidate model/adapter versions on the same evaluation set.
- Report failures and compute limits alongside successes.

## Compute realism
GitHub-hosted CPU runners are for small tests, data validation and bounded experiments. They are not assumed to support full pretraining of frontier-scale models. Virtual GPU/TPU/infinity profiles are simulations only.
