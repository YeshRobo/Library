# Source Artifact Agent Prompt

Create source-derived artifacts from one source file.

The artifact should reduce the source into a compact context packet so a later human or language model can load multiple artifacts together.

Rules:

- Stay grounded in the source text.
- Preserve source paths and line references where possible.
- Extract low-judgment facts: source identity, headings, first non-empty lines, and explicit question lines.
- Write a 1 to 3 sentence draft source orientation summary about what the source appears to contain.
- Do not infer importance, usefulness, confidence, or future knowledge targets.
- Do not create seeds, target indexes, briefs, or books.
- Mark all output as draft material that requires human approval.
- Prefer short, inspectable artifacts over long synthesis.
- Do not copy large portions of the source into the artifact.

Expected artifacts:

- source card
- source summary
- evidence ledger
- questions
- candidate tags
- artifact manifest
