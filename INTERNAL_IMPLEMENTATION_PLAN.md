# Internal Implementation Plan

Status: internal planning document
Audience: coding agents and maintainers building Library
Public status: do not commit or publish unless explicitly approved

## Purpose

This document turns the public design in `DESIGN.md` into an internal build plan for the first implementation of Library.

Library should be built from the working lessons in UM2M while becoming a standalone public project. The implementation should use the local UM2M project repo and console repo as reference implementations, not as code or vocabulary to copy blindly.

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

Use `um2m_oarm101_isaac_v1` as the source of the section-library model.

Use `um2m_console` as the source of the external console architecture.

Do not treat either source repo as something to copy wholesale. Extract patterns, then rename and simplify them for a public standalone Library project.

Do not import from the source repos at runtime. Library must be able to run without sibling repos present.

Do not hard-code local absolute paths into public code, public docs, tests, or catalog files.

Do not keep legacy project vocabulary in public surfaces unless explicitly discussed in `DESIGN.md` as origin context.

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
| topic book | Guide |
| intent | Decision or Direction |
| steward | Review |
| UM2M connector | Library connector |
| UM2M console | Library console |
| workflow catalog | Workflow catalog |
| run record | Run record |

If a public-facing term feels unclear during implementation, prefer the clearest common-language term and record the decision in a review note or issue before expanding the pattern.

## Non-Goals For The First Build

Do not build the full console before the file model is stable.

Do not add autonomous writes.

Do not add external provider calls as the default path.

Do not build multi-project support before one local Library project works.

Do not preserve every UM2M layer or runtime concept.

Do not migrate private UM2M content into public examples.

Do not add broad abstractions before one end-to-end library slice exists.

## Phase 0: Repo Hygiene

Goal: make the public repository safe to build on.

Tasks:

1. Decide whether this internal plan remains untracked or becomes private project management elsewhere.
2. Add a public `README.md` only after the public design wording is stable.
3. Add a license before inviting broad public reuse.
4. Add `.gitignore` for Python, Node, build outputs, virtualenvs, and local run artifacts.
5. Add basic project metadata after the first implementation language choices are finalized.

Expected result:

- Public repo still has a small, understandable surface.
- Internal-only planning does not leak into public Git history.

## Phase 1: File-Based Library Core

Goal: implement the section-library structure without a console.

Proposed public structure:

```text
library/
  sources/
  sections/
    seeds/
    index/
    maps/
    briefs/
    guides/
  reviews/
  decisions/
  templates/
```

Tasks:

1. Create neutral templates derived from the UM2M library templates.
2. Rename template concepts using the public vocabulary mapping.
3. Keep templates small and readable.
4. Add one neutral example section with source, seed, index, map, brief, and optional guide.
5. Add validation rules for required fields and broken file references.

Reference patterns:

- The staged component list in `layers/02_avyakta/library/library_build_rules.md`.
- The compact working readme in `unmanifest/avyakta/library/README.md`.
- The topic seed, index, map, summary, and book templates under `layers/02_avyakta/library/templates/`.

Acceptance criteria:

- A fresh reader can understand the library structure from the public files.
- One example section can be validated end to end.
- No public file requires UM2M-specific knowledge.

## Phase 2: Validation CLI

Goal: give maintainers and agents a simple local way to validate a Library repo.

Recommended implementation:

- Python package using `pydantic` and `PyYAML`, similar to the console backend dependency style.
- CLI command such as `library validate` or `python -m library_cli validate`.

Tasks:

1. Define typed models for section seeds, indexes, source maps, briefs, guides, reviews, and decisions.
2. Validate YAML shape for structured files.
3. Validate Markdown files for required headings.
4. Validate relative links and referenced paths.
5. Report findings in a concise human-readable format.
6. Add tests for valid and invalid example libraries.

Reference patterns:

- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/registry/loader.py` for typed YAML loading and validation style.
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/models/` for pydantic model organization.

Acceptance criteria:

- Validation passes for the neutral example library.
- Validation fails clearly for missing required fields.
- Validation refuses path traversal and absolute-path references in public library content.

## Phase 3: Read-Only Library Console

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
3. Create API endpoints for sections, sources, maps, briefs, guides, reviews, and decisions.
4. Create a React/Vite frontend.
5. Build first views: section list, section detail, source map, brief reader, guide reader.
6. Show validation state in the UI.
7. Keep all write flows disabled in this phase.

Reference patterns:

- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/api/`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/connectors/base.py`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/connectors/um2m_repo.py`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/frontend/src/App.tsx`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/frontend/src/useConsoleState.ts`

Acceptance criteria:

- Backend health endpoint works.
- UI loads live data from the local Library repo.
- The console can browse the example section without provider keys.
- No write endpoint mutates library content.

## Phase 4: Workflow Catalog And Agent Contracts

Goal: introduce agent-assisted workflows as data, not hardcoded behavior.

Tasks:

1. Define a catalog structure for Library workflows.
2. Start with read-only or proposal-only workflows.
3. Add workflows for section discovery, source mapping, brief drafting, and review support.
4. Define workflow metadata: inputs, target paths, read policy, write policy, provider requirements, expected output.
5. Add prompt files beside workflow definitions.
6. Add run records for all agent-assisted attempts.

Reference patterns:

- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/catalog/projects/um2m_oarm101_isaac_v1/`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/engine/workflow_runner.py`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/engine/prompt_assembler.py`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/engine/run_records.py`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_console/backend/providers/`

Acceptance criteria:

- The catalog loader discovers Library workflows from data files.
- A mock provider can run workflows without external API keys.
- Outputs are saved as run records, not silently applied to library files.
- Every workflow displays what it will read and what it may propose.

## Phase 5: Proposal-Only Writes

Goal: let agents propose changes without directly mutating accepted library surfaces.

Tasks:

1. Define proposal files under `library/reviews/`.
2. Add UI for reviewing proposed seeds, maps, briefs, and guides.
3. Add explicit accept/reject flows.
4. Preserve the source evidence used by each proposal.
5. Keep accepted library updates separate from generated drafts.

Acceptance criteria:

- Agent output can create a review proposal.
- No accepted section file changes without explicit human approval.
- Run records link to proposals and source material.

## Phase 6: Community Contribution Surface

Goal: make the public project easy to improve.

Tasks:

1. Add public contribution guidance.
2. Add issue templates for design questions, agent ideas, example libraries, and bugs.
3. Add a clear governance note for how design changes are accepted.
4. Add public examples of good and bad agent behavior.
5. Add tests that contributors can run locally.

Acceptance criteria:

- A contributor can understand where to suggest design improvements.
- A contributor can add a new example section and run validation.
- A contributor can propose an agent workflow without needing private UM2M context.

## Agent Build Instructions

A coding agent implementing this plan should follow this order:

1. Read `DESIGN.md` in this repo.
2. Read this internal plan.
3. Read the UM2M library references listed above.
4. Read the console references listed above.
5. Build the smallest file-based library core before console work.
6. Validate every public-facing name against the public vocabulary mapping.
7. Keep source-derived patterns, but remove source-specific assumptions.
8. Run tests or validation after each phase.
9. Commit only public-ready files unless explicitly asked to commit internal files.
10. Never push internal docs or local path references without explicit approval.

## Safety And Boundary Rules

Public code may mention UM2M only as project origin if the wording is intentional and approved.

Public code must not depend on `/home/robo/UM2M_MULTIVERSE/repos/...` paths.

Public examples must be neutral and free of private project content.

Agent-generated content must be labeled with run metadata before it is considered for acceptance.

Write-capable flows must start as proposal-only.

The console must show path access before a workflow runs.

The backend must reject absolute paths, parent-directory traversal, and writes outside the repository root.

## Initial Technical Stack Recommendation

Backend:

- Python 3.11+
- FastAPI
- Pydantic
- PyYAML
- pytest

Frontend:

- Vite
- React
- TypeScript
- lucide-react

This mirrors the working console stack closely enough to reuse lessons while staying understandable for public contributors.

## First Milestone Definition

Milestone: `v0-file-library`

Deliverables:

- public templates
- one neutral example library section
- validation CLI
- tests for the example and failure cases
- public README
- license

Not included:

- browser console
- external provider calls
- agent write flows
- multi-project support

## Second Milestone Definition

Milestone: `v1-readonly-console`

Deliverables:

- FastAPI read-only backend
- React/Vite console
- section browser
- source map view
- brief and guide readers
- validation status display
- mock data path for local demos

Not included:

- provider-backed agent runs
- accepted write flows
- public package distribution

## Third Milestone Definition

Milestone: `v2-agent-proposals`

Deliverables:

- workflow catalog
- mock provider workflow execution
- agent proposal records
- review queue
- run records
- human accept/reject path

Not included:

- autonomous accepted writes
- private-source migration
- hardcoded UM2M runtime behavior

## Open Internal Questions

1. Should the public repo name stay `Library`, or should package names use `section-library` to avoid namespace collisions?
2. Should templates use YAML plus Markdown, or Markdown with front matter?
3. Should the first CLI be named `library`, `section-library`, or `libctl`?
4. Should the console live at repo root under `backend/` and `frontend/`, or under `console/` first?
5. Which neutral example domain should prove the first library slice?
6. When should public agent prompts be introduced?
7. Should provider adapters live in the main repo or a later optional package?
8. What license should be used before asking the public to contribute?

## Immediate Next Action

Build `v0-file-library` first. Do not start by copying the console. The console should serve the library model after the model is concrete.
