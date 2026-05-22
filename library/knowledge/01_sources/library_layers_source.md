# Source: Earlier Library Layers

## Context

Library previously used a seven-layer source-to-book proposal under `library/knowledge/`:

```text
01_sources -> 02_artifacts -> 03_seeds -> 04_index -> 05_maps -> 06_briefs -> 07_books
```

This source is historical review material. It explains why each layer existed so maintainers and contributors can decide which parts should remain in the target-centered model.

The design is informed by earlier staged-library experiments, but this document uses standalone Library vocabulary. The goal is not to preserve inherited structure. The goal is to test whether each layer solves a real organization, traceability, or retrieval problem.

## Review Question

Which parts of this seven-layer flow should survive in the target-centered Library model?

Reviewers should look for:

- layers that should be merged
- layers that should be renamed
- layers that create process overhead without improving traceability
- missing boundaries between raw material, structured evidence, section identity, synthesis, and final writing

## Layer Purposes

### 01 Sources

Sources preserve raw or lightly processed material before Library has decided what the material means.

This layer should answer:

- What did the project collect?
- Where did the later claim, question, or section idea come from?
- What context should be preserved before any synthesis happens?

Sources should not become briefs or books directly. They may be messy, partial, or duplicated. Their main job is to keep the original material available for traceability.

### 02 Artifacts

Artifacts are structured draft outputs derived from sources.

This layer should answer:

- What does this source appear to contain?
- What evidence, questions, candidate tags, or summaries can be extracted from it?
- What compact source-derived material can help later section discovery and mapping?

Artifacts create a bridge between raw sources and organized section work. They should remain reviewable and source-grounded. An artifact is not accepted section knowledge by itself.

### 03 Seeds

Seeds propose section identities before a full section is built.

This layer should answer:

- What topic may deserve a section?
- Why does the topic deserve organized treatment?
- Which sources or artifacts appear to support it?
- What should the future section include or exclude?

Seeds keep topic discovery lightweight. They let maintainers name and test a possible section before creating indexes, maps, briefs, or books.

### 04 Index

Indexes are routing pages for accepted or active sections.

This layer should answer:

- What is this section about?
- What is the current maturity stage?
- Which source maps, briefs, books, and source entries belong here?
- Where should a reader or tool go next?

The index should be fast to scan. Its purpose is navigation and orientation, not deep synthesis.

### 05 Maps

Maps gather section membership and explain why each source or artifact belongs.

This layer should answer:

- Which files support this section?
- What role does each file play?
- Which files are primary evidence, secondary context, or related but out of scope?
- How can one source support more than one section without hiding that relationship?

Maps preserve traceability after the section has a name. They keep evidence membership explicit instead of letting briefs and books cite a vague pile of material.

### 06 Briefs

Briefs are compact syntheses of what the section currently understands.

This layer should answer:

- What is the current understanding of the section?
- What evidence supports that understanding?
- What constraints, tensions, or uncertainties matter?
- What should a reader consult next?

Briefs are required because many sections should be useful before they are large enough for a book. A brief should be short enough to retrieve quickly and grounded enough to support later writing.

### 07 Books

Books are optional long-form treatments of mature sections.

This layer should answer:

- What is the complete readable treatment of this section?
- How do the sources, artifacts, map, and brief fit together?
- What patterns, tradeoffs, and open questions should a reader understand?
- What claims are directly grounded in source material, and what claims are inference?

Books should not be required for every section. They are useful when a section has enough durable material to justify long-form synthesis.

## Flow Rationale

The seven-layer flow exists to prevent one large jump from raw source material to final prose.

Each layer gives Library a different checkpoint:

- `01_sources` preserves original material.
- `02_artifacts` extracts reviewable structure from sources.
- `03_seeds` proposes section identity.
- `04_index` routes readers and tools.
- `05_maps` makes evidence membership explicit.
- `06_briefs` creates compact understanding.
- `07_books` expands mature sections into long-form writing.

This separation should make it easier to audit how a book was created. It should also let small projects stop at sources, seeds, maps, or briefs without pretending every topic needs a book.

## Review Questions

- Does `02_artifacts` need to be its own layer, or should artifacts stay inside `01_sources`?
- Should `04_index` come before `05_maps`, or should a map exist before a section index?
- Are `03_seeds` and `04_index` clearly different enough for contributors?
- Is `06_briefs` the right required synthesis layer before `07_books`?
- Should `07_books` remain optional, or should every complete section eventually require a book?
- Do the numeric prefixes make the flow clearer, or do they make the file paths feel too mechanical?
- Are any layer names confusing for public contributors?

## Possible Review Outcomes

Review may decide to:

- keep all seven layers as the current Library model
- merge artifacts into sources for a simpler early model
- merge index and map for small projects
- rename layers while preserving the staged flow
- keep the seven folders but make some layers optional by project size
- replace the flow if reviewers find a clearer source-to-book model

No layer should be kept only because it already exists. Each layer should earn its place by improving traceability, reviewability, retrieval, or book quality.