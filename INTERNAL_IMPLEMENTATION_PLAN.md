# Internal Implementation Plan

Status: internal planning document
Audience: coding agents and maintainers building Library
Public status: do not push unless explicitly approved

## Purpose

This document turns the public design in `DESIGN.md` into an internal build plan for Library.

Library should be built from the working lessons in UM2M while becoming a standalone public project focused on creating books from source-grounded library material. The implementation should use the local UM2M project repo and console repo as reference implementations, not as code or vocabulary to copy blindly.

## Required Reference Repos

Coding agents should use these local repos while building Library:

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
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/registry/loader.py`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/connectors/`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/engine/`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/providers/`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/catalog/`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/frontend/src/`

## Reference Use Rules

Use `um2m_oarm101_isaac_v1` as the source of the staged library-to-book model.

Use `um2m_console` as the source of the external console architecture.

Do not treat either source repo as something to copy wholesale. Extract patterns, then rename and simplify them for a public standalone Library project.

Do not import from the source repos at runtime. Library must be able to run without sibling repos present.

Do not hard-code local absolute paths into public code, public docs, tests, or catalog files.

Do not carry over Avyakta-only surfaces such as intent, direction, stewardship, gap handling, or accepted decisions. Library is about making books from organized library material.

## Public Vocabulary Mapping

Use this mapping when adapting UM2M-derived ideas:

| Source concept | Library public concept |
| --- | --- |
| Avyakta library | Section Library |
| source | Source |
| topic seed | Section Seed |
| topic index | Section Index |
| topic map | Source Map |
| topic summary | Brief |
| topic book | Book |
| workflow catalog | Workflow catalog |
| run record | Run record |

If a public-facing term feels unclear during implementation, prefer the clearest common-language term and record the choice in this internal plan or an issue before expanding the pattern.

## Non-Goals For The Current Direction

Do not build Avyakta intent or direction surfaces.

Do not build gap, steward, or review workflows as first-class Library concepts.

Do not build decision surfaces.

Do not build autonomous writes.

Do not add external provider calls as the default path.

Do not build multi-project support before one local Library project works.

Do not migrate private UM2M content into public examples.

Do not add broad abstractions before one end-to-end source-to-book slice exists.

## Phase 0: Repo Hygiene

Goal: make the public repository safe to build on.

Tasks:

1. Keep public files free of local absolute paths.
2. Keep internal routing in internal docs unless explicitly approved for publication.
3. Keep `.gitignore` current for Python, Node, build outputs, virtualenvs, and local run artifacts.
4. Keep README and license public-friendly.

Expected result:

- Public repo has a small, understandable surface.
- Internal-only planning does not leak into public Git history unless explicitly approved.

## Phase 1: File-Based Library Core

Goal: implement the section-library structure without a console.

Public structure:

```text
library/
  sources/
  sections/
    seeds/
    index/
    maps/
    briefs/
    books/
  templates/
```

Tasks:

1. Create neutral templates derived from the UM2M library templates.
2. Rename template concepts using the public vocabulary mapping.
3. Keep templates small and readable.
4. Add one neutral example section with source, seed, index, map, brief, and book.
5. Add validation rules for required fields and broken file references.

Acceptance criteria:

- A fresh reader can understand the library structure from the public files.
- One example section can be validated end to end.
- No public file requires UM2M-specific knowledge.
- No public file introduces intent, direction, review, gap, or decision surfaces.

## Phase 2: Validation CLI

Goal: give maintainers and agents a simple local way to validate a Library repo.

Recommended implementation:

- Python package using `PyYAML` for structured validation.
- CLI command such as `section-library validate .`.

Tasks:

1. Validate YAML shape for section seeds and source maps.
2. Validate Markdown files for required headings.
3. Validate relative links and referenced paths.
4. Reject absolute paths and parent-directory traversal.
5. Report findings in a concise human-readable format.
6. Add tests for valid and invalid example libraries.

Acceptance criteria:

- Validation passes for the neutral example library.
- Validation fails clearly for missing required fields.
- Validation refuses path traversal and absolute-path references in public library content.

## Phase 3: Book Builder Workflows

Goal: introduce agent-assisted workflows that help create books from mapped sources and briefs.

Tasks:

1. Define a workflow catalog structure for source-to-book work.
2. Start with read-only or draft-only workflows.
3. Add workflows for section discovery, source mapping, brief drafting, and book drafting.
4. Define workflow metadata: inputs, target paths, read policy, draft output path, provider requirements, expected output.
5. Add prompt files beside workflow definitions.
6. Add run records for all agent-assisted attempts.

Acceptance criteria:

- A mock provider can run workflows without external API keys.
- Outputs are saved as run records or drafts, not silently applied to book files.
- Every workflow displays what it will read and what it may draft.

## Phase 4: Read-Only Library Console

Goal: create a read-only browser UI for exploring the file-based library.

Recommended architecture:

```text
backend/
  api/
  connectors/
  models/
  registry/
  library_reader/
frontend/
  src/
catalog/
  projects/
  providers/
  ui/
runs/
```

Use the `um2m_console` architecture as the reference, but rename and simplify.

Tasks:

1. Create a FastAPI backend with health and catalog endpoints.
2. Create a `LibraryRepoConnector` that reads only from the current Library repo.
3. Create API endpoints for sections, sources, maps, briefs, and books.
4. Create a React/Vite frontend.
5. Build first views: section list, section detail, source map, brief reader, book reader.
6. Show validation state in the UI.
7. Keep all write flows disabled in this phase.

Acceptance criteria:

- Backend health endpoint works.
- UI loads live data from the local Library repo.
- The console can browse the example section without provider keys.
- No write endpoint mutates library content.

## Agent Build Instructions

A coding agent implementing this plan should follow this order:

1. Read `DESIGN.md` in this repo.
2. Read this internal plan.
3. Read the UM2M library references listed above.
4. Read the console references listed above only when console or workflow work begins.
5. Build the smallest file-based source-to-book core before console work.
6. Validate every public-facing name against the public vocabulary mapping.
7. Keep source-derived patterns, but remove source-specific assumptions.
8. Run tests or validation after each phase.
9. Commit only public-ready files unless explicitly asked to commit internal files.
10. Never push internal docs or local path references without explicit approval.

## Safety And Boundary Rules

Public code may mention UM2M only as project origin if the wording is intentional and approved.

Public code must not depend on `/home/robo/UM2M_MULTIVERSE/repos/...` paths.

Public examples must be neutral and free of private project content.

Agent-generated content must be labeled with run metadata before it is considered for book inclusion.

Write-capable flows must start as draft-only.

The console must show path access before a workflow runs.

The backend must reject absolute paths, parent-directory traversal, and writes outside the repository root.

## Initial Technical Stack Recommendation

Backend:

- Python 3.11+
- FastAPI for the future backend
- PyYAML for structured validation
- pytest or standard-library unittest for tests

Frontend:

- Vite
- React
- TypeScript
- lucide-react

## First Milestone Definition

Milestone: `v0-file-library`

Deliverables:

- public templates
- one neutral example library section
- one complete book example
- validation CLI
- tests for the example and failure cases
- public README
- license

Not included:

- browser console
- external provider calls
- agent write flows
- multi-project support

## Immediate Next Action

Keep `v0-file-library` focused on source-to-book validation. Do not add intent, direction, review, gap, or decision surfaces.
