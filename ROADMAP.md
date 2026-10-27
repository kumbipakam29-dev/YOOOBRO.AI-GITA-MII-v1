# MIi Research Roadmap

## Stage 0 — Repo and evidence foundation
- [x] Create dedicated research repository, separate from Android app.
- [x] Add proposed Sanskrit generation registry and Gita verse references.
- [x] Add tiny synthetic CPU classifier and virtual compute simulation.
- [x] Add CI, manual CPU training, simulation and hourly status workflows.
- [ ] Confirm first successful GitHub Actions run and fix any runner failures.
- [ ] Add immutable dataset manifests and independently reviewed source citations.

## Stage 1 — MIi v1: विवेक (Viveka)
- Build source provenance and uncertainty benchmarks.
- Evaluate train/validation/test splits with no leakage.
- Require independent verification for release candidates.

## Stage 2 — MIi v2: कर्मयोग (KarmaYoga)
- Add bounded tool-use and planning evaluations.
- Use permission gates and human approval for high-impact actions.

## Stage 3 — MIi v3: ज्ञानयोग (JnanaYoga)
- Add Sanskrit/Hindi source-grounded retrieval and translation comparison.
- Separate scripture, translation, commentary and engineering interpretation.

## Later generations
- AbhyasaYoga: repeatability, checkpointing, regression tests.
- Samatva: robustness, perturbation tests and bias checks.
- Maitri: respectful assistance and support boundaries.
- Abhaya-Satya: transparent limits, security and failure reporting.

## Release discipline
A registry entry or prompt change is not a trained model. A model release requires pinned data, exact model revision, recorded training method, artifact hashes, independent evaluation and human approval.
