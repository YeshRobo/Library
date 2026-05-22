# Source: Library Structure Design Proposal

Status: source material; target-centered migration applied
Audience: maintainers, contributors, and agents updating `library/`

## Purpose

This source proposes the next `library/` structure based on the current repository and the source document `library/knowledge/01_sources/library_knowledge_architecture_explanation.md`.

The goal was to decide how Library should organize source material, artifacts, seeds, accepted knowledge targets, maps, briefs, books, and feedback before changing folders, validators, templates, console code, or agent workflows.

Implementation note: the repository now follows the target-centered structure proposed here. Earlier sections that describe the old structure are retained as migration evidence.

## Pre-Migration Structure

The pre-migration file model was section-centered:

```text
library/
  README.md
  sections/
    01_sources/
    02_artifacts/
    03_seeds/
    04_index/
    05_maps/
    06_briefs/
    07_books/
  templates/
```

The earlier implementation assumed this layout in several places:

- the validation CLI requires the seven `library/knowledge/` folders
- the read-only console discovers sections from `03_seeds/`
- the console builds paths for `04_index/`, `05_maps/`, `06_briefs/`, and `07_books/`
- the Source Artifact Agent reads `01_sources/` and writes draft artifacts to `02_artifacts/`
- templates still use section-oriented terms such as section seed, section index, and source map

This structure worked for the first source-to-book slice, but the architecture source raised a useful concern: `section` was too rigid for a need-based knowledge system.

## Design Direction

Library should move from a section-centered model toward a knowledge-target model.

A knowledge target is an accepted need, question, pattern, or output area that Library decides is worth organizing around. A target may produce a brief, book, guide, reference page, agent packet, research note, comparison, or another useful knowledge product.

This keeps the useful staged flow while avoiding the assumption that every unit is a fixed topic section.

The core flow becomes:

```text
sources -> artifacts -> seeds -> targets -> maps -> briefs -> books -> feedback
```

## Recommended Structure

The recommended v1 structure is:

```text
library/
  README.md
  knowledge/
    01_sources/
      library_structure_design_source.md
    02_artifacts/
    03_seeds/
    04_targets/
    05_maps/
    06_briefs/
    07_books/
    08_feedback/
  templates/
    source_template.md
    artifact_template.md
    seed_template.yaml
    target_index_template.md
    map_template.yaml
    brief_template.md
    book_template.md
    feedback_template.md
```

`library/knowledge/` is recommended instead of putting numbered folders directly under `library/` because it keeps knowledge surfaces grouped while leaving room for root-level docs, templates, draft outputs, examples, and future tooling metadata.

## Layer Contracts

### 01 Sources

Purpose: preserve raw or lightly processed material before Library decides what it means.

This layer answers:

- What did the project collect?
- Where did later claims, questions, or targets come from?
- What original context should remain available for audit?

Rules:

- sources should not be overwritten by interpretation
- sources may be messy, duplicated, incomplete, or unorganized
- later layers must be able to trace back to sources

### 02 Artifacts

Purpose: create structured, AI-readable representations of sources.

This layer answers:

- What is this source about?
- What important points, questions, terms, entities, or patterns appear?
- What future targets or outputs might this source support?
- What uncertainty or limitation should remain visible?

Recommended unit: one source should produce one artifact packet. The packet may be one file or a folder containing files such as a source card, source summary, evidence ledger, questions, candidate tags, and artifact manifest. This preserves the current Source Artifact Agent design while honoring the architecture rule that every source should have one durable artifact representation.

Rules:

- artifacts are source-level working representations
- artifacts are not accepted knowledge by themselves
- artifacts must cite their source path

### 03 Seeds

Purpose: propose possible knowledge targets.

This layer answers:

- What knowledge target may be useful?
- What need, pattern, question, conflict, or task triggered the proposal?
- Which sources or artifacts appear relevant?
- What output type may be useful?

Rules:

- seeds are proposals, not accepted knowledge
- seeds may come from artifact review, user queries, agent task needs, repeated patterns, contradictions, or underused ideas
- seeds should record origin and lens when created by an agent

### 04 Targets

Purpose: register accepted knowledge targets and provide their navigation surface.

This layer replaces the current `04_index/` folder.

This layer answers:

- What need does this target serve?
- Which seeds created or influenced it?
- What stage is it in?
- Which map, brief, book, and feedback records belong to it?
- Where should a human or agent go next?

Rules:

- targets are accepted work areas, not final truth claims
- each target should have a stable slug
- related, overlapping, replaced, or contested targets should be visible

### 05 Maps

Purpose: connect evidence to targets.

This layer answers:

- Which artifacts and sources support this target?
- What role does each item play?
- Which evidence is primary, secondary, conflicting, missing, or out of scope?
- How can one artifact support multiple targets?

Rules:

- maps make evidence membership explicit
- maps should explain why each item belongs, not just list paths
- maps should point to artifacts first when artifacts exist, and sources when raw source access is needed

### 06 Briefs

Purpose: provide compact current knowledge for a target.

This layer answers:

- What does Library currently understand about this target?
- What evidence supports that understanding?
- What constraints, tensions, conflicts, or uncertainties matter?
- What should an agent or reader know before acting?

Rules:

- briefs are the required compact knowledge output for active targets
- briefs should be small enough to retrieve and use quickly
- briefs should mark limits and avoid pretending to be final truth

### 07 Books

Purpose: provide optional long-form synthesis for mature targets.

This layer answers:

- What is the complete readable treatment of this target?
- How do the sources, artifacts, map, and brief fit together?
- What patterns, tradeoffs, and open questions should a reader understand?
- Which claims are source-grounded, and which are inference?

Rules:

- books are optional
- books should be revisable
- books should cite maps, artifacts, and sources clearly

### 08 Feedback

Purpose: record usage, failure, contradiction, confidence changes, and revision triggers.

This layer answers:

- Which target or output was used?
- For what task or need?
- Did it help, fail, mislead, or get contradicted?
- What revision is needed?
- How should confidence change?

Rules:

- feedback should reference the target and output it affects
- feedback should not rewrite the source, artifact, brief, or book directly
- feedback should be able to trigger a new seed, map update, brief revision, or book revision

## Naming And Data Model

The v1 structure should prefer target-oriented names:

| Current term | Proposed term |
| --- | --- |
| section | knowledge target or target |
| section seed | seed |
| section index | target index |
| source map | map |
| section title | target title |
| section slug | target slug |
| section stage | target stage |

Recommended YAML fields for target-oriented files:

```yaml
target_slug: example_target
target_title: Example Target
target_purpose: One short statement of the need this target serves.
status: active
origin_seeds:
  - library/knowledge/03_seeds/example_seed.yaml
output_types:
  - brief
  - book
```

The migration may temporarily support current `section_*` fields, but new templates should use `target_*` once the structure is approved.

## Traceability Rules

Every accepted output should be traceable backward:

```text
book or brief -> map -> artifacts -> sources
```

Every maintenance action should be traceable forward:

```text
feedback -> affected target -> affected brief/book -> required revision
```

AI-created outputs should record provenance:

- model or provider family when known
- agent role
- prompt or task summary
- date
- lens or intended bias
- known limitations

## Confidence Model

Library should treat confidence as provisional.

Confidence can increase through:

- source support
- source diversity
- successful reuse
- independent rediscovery by different agents
- low contradiction level
- successful reality checks

Confidence can decrease through:

- contradicted evidence
- failed use
- stale source material
- unsupported synthesis
- stronger replacement outputs

Confidence does not need to become a large scoring system in the first migration. It can start as structured text in targets, briefs, books, and feedback records.

## Lifecycle

Targets and outputs should support this lifecycle:

```text
proposed -> accepted -> active -> stable -> contested -> revised -> replaced/deprecated
```

Not every target must pass through every stage. The point is to make current status visible.

## Migration Plan

### Phase 1: Approve The Structure

Decide these open questions:

- Should the canonical root be `library/knowledge/`?
- Should `04_index/` become `04_targets/`?
- Should `08_feedback/` be added now or after target migration?
- Should artifacts remain artifact packets or become single files?
- Should maps be required before a brief is accepted?

### Phase 2: Add New Templates

Create target-oriented templates:

- `source_template.md`
- `artifact_template.md`
- `seed_template.yaml`
- `target_index_template.md`
- `map_template.yaml`
- `brief_template.md`
- `book_template.md`
- `feedback_template.md`

### Phase 3: Move The Current Example

Move the current example from:

```text
library/knowledge/...
```

to:

```text
library/knowledge/...
```

Rename current paths as follows:

```text
library/knowledge/01_sources/  -> library/knowledge/01_sources/
library/knowledge/02_artifacts/ -> library/knowledge/02_artifacts/
library/knowledge/03_seeds/     -> library/knowledge/03_seeds/
library/knowledge/04_targets/     -> library/knowledge/04_targets/
library/knowledge/05_maps/      -> library/knowledge/05_maps/
library/knowledge/06_briefs/    -> library/knowledge/06_briefs/
library/knowledge/07_books/     -> library/knowledge/07_books/
```

Then add:

```text
library/knowledge/08_feedback/
```

### Phase 4: Update Code Contracts

Update the validator, console reader, workflow catalog, Source Artifact Agent help text, tests, and README files to use the approved paths.

The validator should check:

- required directories
- required templates
- target-oriented YAML fields
- safe relative paths
- broken references
- required markdown headings for target indexes, briefs, books, and feedback records

### Phase 5: Update Public Design Docs

Update root public docs so new contributors see one coherent model:

- `DESIGN.md`
- `README.md`
- `library/README.md`
- `catalog/workflows/source_artifact.yaml`
- templates and examples

## Compatibility Option

If the project wants a smaller migration, keep `library/knowledge/` for one more version and only change the inner model:

```text
library/knowledge/
  01_sources/
  02_artifacts/
  03_seeds/
  04_targets/
  05_maps/
  06_briefs/
  07_books/
  08_feedback/
```

This reduces path churn but leaves the old `sections` framing in place. It is easier technically but less aligned with the architecture source.

## Recommended Decision

Use `library/knowledge/` as the new canonical root and move to eight layers:

```text
01_sources -> 02_artifacts -> 03_seeds -> 04_targets -> 05_maps -> 06_briefs -> 07_books -> 08_feedback
```

This keeps the existing staged source-to-book flow, replaces rigid section language with knowledge-target language, and adds feedback so Library can revise knowledge through use.

## Acceptance Criteria For The Structure Update

The structure update is complete when:

- `library/knowledge/` contains all approved layers
- public docs describe the target-centered model consistently
- templates use target-oriented vocabulary
- the validator passes on the migrated example
- the read-only console can list and open targets
- the Source Artifact Agent reads from `01_sources/` and writes to `02_artifacts/`
- feedback records can be created without changing accepted briefs or books directly
- no public file requires private project vocabulary to understand the model