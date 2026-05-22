# Internal Implementation Plan

Status: internal planning document
Audience: coding agents and maintainers building Library
Public status: do not push unless explicitly approved

## Purpose

This document turns `DESIGN.md` into an internal build plan for Library.

Library is now a target-centered, source-grounded knowledge system. Its job is to create useful briefs, books, and other knowledge outputs from organized source material. The current canonical flow is:

```text
sources -> artifacts -> seeds -> targets -> maps -> briefs -> books -> feedback
```

Use the local internal project and console repos as references for implementation patterns only. Do not copy private vocabulary, private content, or runtime imports from those repos.

## Required Reference Repos

Coding agents may consult these local repos while building Library:

- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console`

Primary library references:

- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/unmanifest/avyakta/library/README.md`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/layers/02_avyakta/library/library_build_rules.md`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/layers/02_avyakta/library/templates/topic_seed_template.yaml`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/layers/02_avyakta/library/templates/topic_index_template.md`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/layers/02_avyakta/library/templates/topic_map_template.yaml`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/layers/02_avyakta/library/templates/topic_summary_template.md`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/layers/02_avyakta/library/templates/topic_book_template.md`

Primary console references:

- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/README.md`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/docs/agent_console_implementation_plan.md`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/frontend/src/`

## Reference Use Rules

Use the internal project repo to understand the staged source-to-knowledge model.

Use `um2m_console` to understand data-driven backend/frontend architecture.

Do not import from reference repos at runtime. Library must run without sibling repos present.

Do not hard-code local absolute paths into public code, public docs, tests, or catalog files.

Do not carry over intent, direction, stewardship, gap handling, accepted decisions, or private project vocabulary as public Library concepts. Library is about creating knowledge outputs from organized library material.

## Public Vocabulary Mapping

Use this mapping when adapting reference concepts:

| Reference concept | Library public concept |
| --- | --- |
| staged project library | Knowledge library |
| source | Source |
| source-derived card/summary | Artifact |
| topic seed | Seed |
| topic index | Target index |
| topic map | Map |
| topic summary | Brief |
| topic book | Book |
| use review / contradiction note | Feedback |
| workflow catalog | Workflow catalog |
| run record | Run record |

If a public-facing term feels unclear during implementation, prefer the clearest common-language term and record the choice before expanding the pattern.

## Canonical File Structure

```text
library/
  knowledge/
    01_sources/
    02_artifacts/
    03_seeds/
    04_targets/
    05_maps/
    06_briefs/
    07_books/
    08_feedback/
  templates/
```

Validation, console readers, workflows, and examples should all use this shape.

## Non-Goals For The Current Direction

Do not build internal intent or direction surfaces.

Do not build gap, steward, or review workflows as first-class public Library concepts.

Do not build decision surfaces.

Do not build autonomous writes.

Do not add external provider calls as the default path.

Do not build multi-project support before one local Library project works.

Do not migrate private internal content into public examples.

Do not add broad abstractions before one end-to-end source-to-book slice exists.

## Phase 0: Repo Hygiene

Goal: keep the public repository safe to build on.

Tasks:

1. Keep public files free of local absolute paths.
2. Keep internal routing in internal docs unless explicitly approved for publication.
3. Keep `.gitignore` current for Python, Node, build outputs, virtualenvs, and local run artifacts.
4. Keep README, design, and license public-friendly.

Acceptance criteria:

- Public repo has a small, understandable surface.
- Internal-only planning does not leak into public Git history unless explicitly approved.

## Phase 1: File-Based Knowledge Core

Goal: implement the target-centered file model without requiring the console.

Tasks:

1. Maintain templates for sources, artifacts, seeds, target indexes, maps, briefs, books, and feedback.
2. Keep templates small and readable.
3. Maintain one neutral example target with source, seed, target index, map, brief, and book.
4. Validate required fields, required headings, safe relative paths, and broken references.
5. Keep `08_feedback` available as a first-class layer even if the first example only documents the pattern.

Acceptance criteria:

- A fresh reader can understand the library structure from public files.
- One example target validates end to end.
- No public file requires private project knowledge.
- No public file introduces internal intent, direction, gap, or decision surfaces.

## Phase 2: Validation CLI

Goal: give maintainers and agents a simple local way to validate a Library repo.

Recommended implementation:

- Python package using `PyYAML` for structured validation.
- CLI command `library-cli validate .`.

Tasks:

1. Validate YAML shape for seeds and maps.
2. Validate Markdown files for required headings.
3. Validate relative links and referenced paths.
4. Reject absolute paths and parent-directory traversal.
5. Report findings in concise human-readable output.
6. Add tests for valid and invalid example libraries.

Acceptance criteria:

- Validation passes for the neutral example library.
- Validation fails clearly for missing required fields.
- Validation refuses path traversal and absolute-path references in public library content.

## Phase 3: Read-Only Library Console

Goal: create a read-only browser UI for exploring the file-based library.

Recommended architecture:

```text
src/library_console/
  api/
  repository.py
frontend/
  src/
catalog/
  projects/
  providers/
  ui/
runs/
```

Use the `um2m_console` architecture as reference, but rename and simplify.

Tasks:

1. Create FastAPI health, summary, validation, target list, and target detail endpoints.
2. Read only from the current Library repo.
3. Create API endpoints for knowledge targets, sources, maps, briefs, and books.
4. Build a React/Vite frontend.
5. Build first views: target list, target detail, map, brief reader, book reader.
6. Show validation state in the UI.
7. Keep all write flows disabled in this phase.

Acceptance criteria:

- Backend health endpoint works.
- UI loads live data from the local Library repo.
- The console can browse the example target without provider keys.
- No write endpoint mutates library content.

## Phase 4: Agent-Assisted Source And Book Workflows

Goal: introduce draft-only workflows that help create and improve knowledge outputs.

Detailed agent implementation routing lives in `INTERNAL_AGENT_IMPLEMENTATION_PLAN.md`.

Tasks:

1. Maintain a workflow catalog structure for source-to-book work.
2. Keep workflows read-only or draft-only by default.
3. Start with the Source Artifact Agent.
4. Add future workflows for seed discovery, target indexing, map drafting, brief drafting, book drafting, and feedback recording.
5. Define workflow metadata: inputs, allowed roots, draft output paths, provider requirements, expected output, and run records.
6. Add prompt files beside workflow definitions.
7. Add run records for all agent-assisted attempts.

Acceptance criteria:

- A mock provider can run workflows without external API keys.
- Outputs are saved as run records or drafts, not silently applied to accepted book files.
- Every workflow displays what it will read and what it may draft.

## Agent Build Instructions

A coding agent implementing this plan should follow this order:

1. Read `DESIGN.md` in this repo.
2. Read this internal plan.
3. Read relevant reference files only for the phase being implemented.
4. Build the smallest file-based source-to-book core before expanding console or workflow work.
5. Validate every public-facing name against the public vocabulary mapping.
6. Keep source-derived patterns, but remove source-specific assumptions.
7. Run tests, validation, and frontend builds after changes that touch those surfaces.
8. Commit only public-ready files unless explicitly asked to commit internal files.
9. Never push internal docs or local path references without explicit approval.

## Safety And Boundary Rules

Public code should not depend on private local paths.

Public examples must be neutral and free of private project content.

Agent-generated content must be labeled with run metadata before it is considered for accepted library inclusion.

Write-capable flows must start as draft-only.

The console must show path access before a workflow runs.

The backend must reject absolute paths, parent-directory traversal, and writes outside the repository root.

## Initial Technical Stack Recommendation

Backend:

- Python 3.11+
- FastAPI for the backend
- PyYAML for structured validation
- standard-library unittest or pytest for tests

Frontend:

- Vite
- React
- TypeScript
- lucide-react

## Current Milestone Definition

Milestone: `v1-knowledge-library`

Deliverables:

- public templates
- one neutral example knowledge target
- one complete book example
- validation CLI
- read-only console
- source artifact agent
- feedback layer scaffold
- tests for the example and failure cases
- public README and design

Not included:

- external provider calls by default
- autonomous write flows
- multi-project support

## Immediate Next Action

Keep the repository aligned to the target-centered `library/knowledge` model. Do not reintroduce old section folders or internal direction/review/gap surfaces.
