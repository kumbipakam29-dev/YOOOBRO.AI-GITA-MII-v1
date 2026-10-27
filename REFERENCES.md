# References and Source Policy

## Bhagavad Gita source discovery
Use these sources to verify exact verse text, chapter/verse numbering, translation, and commentary:
- IIT Kanpur Gita Supersite: https://www.gitasupersite.iitk.ac.in/
- SanskritDocuments Bhagavad Gita: https://sanskritdocuments.org/sanskrit/bhagavadgita/

The repository's generation themes are engineering interpretations inspired by verse topics. They must not be presented as verbatim scripture or definitive religious commentary. Every published verse record should eventually pin a source URL and reviewer status.

## GitHub Actions
- Workflow syntax: https://docs.github.com/actions/writing-workflows/workflow-syntax-for-github-actions
- Scheduled workflows: https://docs.github.com/actions/using-workflows/events-that-trigger-workflows#schedule
- Artifacts: https://docs.github.com/actions/using-workflows/storing-workflow-data-as-artifacts

Scheduled runs are best-effort and may be delayed. A report workflow does not mean a model trains continuously.

## Model and dataset provenance
- Keep exact repository IDs, immutable revisions, license terms and dataset hashes.
- Treat external model-card benchmark scores as claims from their source, not MIi results.
- Never download restricted benchmark data or bypass access conditions.
- A public model metadata entry is not evidence that weights were loaded or inference was performed.
