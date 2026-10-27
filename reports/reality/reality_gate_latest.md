# Simulation-to-Reality Gate

- Generated UTC: 2026-10-27T23:03:39.644141+00:00
- Evidence class: MIXED_SIMULATION_AND_REAL_RUNNER_EXECUTION
- Profiles compared: 5
- Comparison rows: 25
- Matching comparisons: 15
- Simulation/reality gaps or failures: 4
- Not comparable (task intentionally not run): 5

## Actual runner checks

| Task | Actual status | Evidence |
|---|---|---|
| dataset_validation | PASS |  |
| tiny_classifier_training | PASS | True |
| python_source_compile | PASS |  |
| accelerator_probe | NOT_DETECTED | No supported accelerator signal was detected in this runner; do not infer that every underlying host lacks accelerators. |
| large_llm_finetune | NOT_ATTEMPTED_RESOURCE_GUARD | Requires pinned model weights, license review, measured accelerator memory, and an approved compute budget. |

## Interpretation

A simulation result is not a real-world success. Here, real means the same bounded check executed on the hosted CI runner. It does not certify the founder's device, customer systems, production services, or a generative AI model.

Large-model fine-tuning is guarded and not attempted until model revision, license, hardware memory, and compute budget have been qualified.
