# Internal Agent Implementation Plan

Status: internal planning document
Audience: coding agents and maintainers building Library agents
Public status: do not push unless explicitly approved

## Purpose

This document defines how Library should implement agent-assisted workflows for the target-centered knowledge model.

The current canonical flow is:

```text
sources -> artifacts -> seeds -> targets -> maps -> briefs -> books -> feedback
```

Agents should help maintainers move through this flow while preserving traceability and human approval. Generated output must begin as draft-only unless an explicit approval workflow is added later.

## Reference Source

Use the following internal files as implementation references only:

- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/agent/runtimes/l02_avyakta/tooling/source/artifact.py`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/agent/runtimes/l02_avyakta/tooling/source/artifact_agent/README.md`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/agent/runtimes/l02_avyakta/tooling/library/topic_discovery.py`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/agent/runtimes/l02_avyakta/tooling/library/topic_index.py`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/agent/runtimes/l02_avyakta/tooling/library/topic_map.py`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/agent/runtimes/l02_avyakta/tooling/library/topic_summary.py`
- `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1/agent/runtimes/l02_avyakta/tooling/library/topic_book.py`

Do not import from those files at runtime. Do not copy private source content or framework-specific vocabulary into public Library surfaces.

## Vocabulary Mapping

| Reference concept | Library concept |
| --- | --- |
| source artifact agent | Source Artifact Agent |
| topic discovery agent | Seed Discovery Agent |
| topic seed | Seed |
| topic index agent | Target Index Agent |
| topic map agent | Map Agent |
| topic summary agent | Brief Drafter Agent |
| topic book agent | Book Drafter Agent |
| review/use note | Feedback Agent |
| worklog ledger | Run record |

Avoid framework-specific layer names in public code, catalog entries, CLI help, prompts, and generated draft outputs.

## Agent Architecture Pattern

Each Library agent should keep the same small domain split:

```text
agent_package/
  common/
  perception/
  mind/
  action/
  orchestrator.py
  cli.py
```

Responsibilities:

- `common/` defines config, path constants, request types, outcome types, and errors.
- `perception/` reads allowed repository surfaces and returns neutral observations.
- `mind/` classifies state, builds prompt context, calls a provider or mock provider, and validates candidate payloads.
- `action/` writes only the allowed draft artifact and run record.
- `orchestrator.py` wires perception, mind, and action without owning policy.
- `cli.py` parses arguments, supports dry-run, prints summaries, and maps errors to exit codes.

Facade modules should stay small and stable:

```text
src/library_agents/source_artifact.py
src/library_agents/seed_discovery.py
src/library_agents/target_index.py
src/library_agents/map_draft.py
src/library_agents/brief_draft.py
src/library_agents/book_draft.py
src/library_agents/feedback.py
```

Each facade should call its matching package implementation under `src/library_agents/<agent_name>_agent/`.

## Proposed Repository Shape

```text
catalog/
  workflows/
    source_artifact.yaml
    seed_discovery.yaml
    target_index.yaml
    map_draft.yaml
    brief_draft.yaml
    book_draft.yaml
    feedback_record.yaml
    evidence_check.yaml
  prompts/
    source_artifact.md
    seed_discovery.md
    target_index.md
    map_draft.md
    brief_draft.md
    book_draft.md
    feedback_record.md
    evidence_check.md
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
  drafts/
    agent_outputs/
runs/
src/
  library_agents/
tests/
```

Notes:

- `catalog/workflows/` and `catalog/prompts/` are tracked configuration surfaces.
- `library/knowledge/01_sources/` holds raw or lightly processed source material.
- `library/knowledge/02_artifacts/` holds source-derived artifacts that maintainers can inspect and later use.
- `library/drafts/agent_outputs/` holds draft outputs that are not accepted library content.
- `runs/` holds local run records and may remain ignored until the project decides which examples should be public.

## Workflow Catalog Contract

Each workflow definition should be a YAML file with this minimum shape:

```yaml
workflow_id: source_artifact
name: Source Artifact Agent
agent_module: library_agents.source_artifact
mode: draft_only
inputs:
  - name: source_path
    type: repo_path
    required: true
read_policy:
  allowed_roots:
    - library/knowledge/01_sources
    - library/knowledge/02_artifacts
  required_files: []
write_policy:
  draft_root: library/knowledge/02_artifacts
  allowed_extensions:
    - .yaml
    - .md
run_record:
  root: runs
  required: true
provider:
  default: mock
expected_output:
  type: source_artifact
  validator: source_artifact
```

The backend and CLI must show the read policy and write policy before a workflow runs.

## Agent Order

Implement agents in this order.

### 1. Source Artifact Agent

Detailed design lives in `INTERNAL_SOURCE_ARTIFACT_AGENT_DESIGN.md`.

Purpose: create structured source-derived artifacts from raw or lightly processed source files.

Reads:

- `library/knowledge/01_sources/`
- existing artifacts under `library/knowledge/02_artifacts/`
- source artifact workflow prompt and validation schema

Writes draft outputs only:

- source card
- source summary
- evidence ledger
- questions
- candidate tags
- artifact manifest
- run record

Canonical artifact path:

```text
library/knowledge/02_artifacts/<source_slug>/
```

This agent does not create seeds, briefs, or books.

### 2. Seed Discovery Agent

Purpose: propose seeds from source artifacts, questions, tasks, contradictions, or repeated patterns.

Reads:

- `library/knowledge/02_artifacts/`
- existing `library/knowledge/03_seeds/`
- existing `library/knowledge/04_targets/`

Writes draft outputs only:

- candidate seed YAML under `library/drafts/agent_outputs/seeds/`
- run record

Accepted seeds must still be moved or copied into `library/knowledge/03_seeds/` by a human or explicit approval flow.

### 3. Target Index Agent

Purpose: draft a target index from an accepted seed.

Reads:

- selected seed
- referenced source artifacts
- existing target index, if present

Writes draft outputs only:

- candidate target index Markdown under `library/drafts/agent_outputs/targets/`
- run record

### 4. Map Agent

Purpose: draft a map for one target.

Reads:

- selected seed
- selected target index
- referenced source artifacts
- raw source files named by those artifacts

Writes draft outputs only:

- candidate map YAML under `library/drafts/agent_outputs/maps/`
- run record

The map agent should preserve artifact-gated source access: raw source files may be read only when named by selected source artifacts or existing accepted target surfaces.

### 5. Brief Drafter Agent

Purpose: draft a compact brief from a map and supporting files.

Reads:

- selected map
- source artifacts named by the map
- raw source files named by the source artifacts
- existing brief, if present

Writes draft outputs only:

- candidate brief Markdown under `library/drafts/agent_outputs/briefs/`
- run record

### 6. Book Drafter Agent

Purpose: draft a long-form book from a map, source artifacts, raw source files, and a brief.

Reads:

- selected map
- selected brief
- source artifacts named by the map
- raw source files named by those artifacts
- existing book, if present

Writes draft outputs only:

- candidate book Markdown under `library/drafts/agent_outputs/books/`
- run record

### 7. Feedback Agent

Purpose: record how a target, brief, book, or other output performed during use.

Reads:

- selected target surface
- optional user-supplied use context
- optional evidence or contradiction references

Writes draft outputs only:

- feedback Markdown or YAML under `library/drafts/agent_outputs/feedback/`
- run record

Accepted feedback must still be moved into `library/knowledge/08_feedback/` by a human or explicit approval flow.

### 8. Evidence Checker Agent

Purpose: report unsupported, unclear, or weakly grounded claims in a draft brief or book.

Reads:

- selected draft or accepted brief/book
- map
- source artifacts
- raw source files named by those artifacts

Writes draft outputs only:

- evidence check report under `library/drafts/agent_outputs/evidence_checks/`
- run record

This agent should not rewrite the brief or book. It reports findings for human action.

## Provider Strategy

Start with a mock provider.

The mock provider should generate deterministic output from fixture data or simple local transformations so tests do not require external API keys. External providers can be added later behind the same provider interface.

Provider interface requirements:

- receives a structured prompt packet
- returns structured candidate payload plus optional usage metadata
- never receives files outside the workflow read policy
- can be replaced by tests without network access

## Run Records

Every agent-assisted attempt must produce a run record before or alongside any draft output.

Minimum run record fields:

```yaml
run_id: source_artifact_YYYYMMDD_HHMMSS_slug
workflow_id: source_artifact
agent_name: Source Artifact Agent
provider: mock
model: mock-local
status: completed
started_at: ISO-8601 timestamp
finished_at: ISO-8601 timestamp
read_paths: []
draft_paths: []
validation:
  ok: true
  findings: []
human_approval:
  required: true
  approved: false
```

Run records should make it obvious that generated content is not accepted library content until a human approves it.

## Safety Rules

All agent flows must follow these rules:

1. Default to dry-run or draft-only.
2. Reject absolute paths, parent-directory traversal, and paths outside the repository root.
3. Read only declared paths and declared roots for the selected workflow.
4. Write only under the workflow draft root or run-record root.
5. Never silently mutate accepted files in `library/knowledge/`.
6. Label generated content with run metadata.
7. Validate candidate payloads before writing.
8. Keep raw provider output out of accepted library content.
9. Keep public names neutral and source-to-book focused.
10. Do not add autonomous approval flows in the first implementation.

## Validation Additions

The validation CLI should eventually validate:

- workflow catalog shape
- prompt file existence
- source artifact schema
- draft output path safety
- run record shape
- no accepted target surface points to missing source artifacts

Do not make broad validation additions before the first source artifact workflow is stable.

## Console Additions

The read-only console should later show:

- workflow catalog list
- selected workflow read policy
- selected workflow draft policy
- dry-run preview
- run records
- draft outputs awaiting human approval

The first console integration should be read-only display of workflows and run records. Triggering workflows from the console should come after CLI workflows and tests are stable.

## Tests

Use standard-library `unittest` unless the project has installed a broader test stack.

Initial tests should cover:

- workflow catalog validation
- path traversal rejection
- mock provider run for Source Artifact Agent
- draft output goes to the expected draft root
- accepted library files are not mutated by an agent run
- run record is written with read and draft paths
- malformed candidate payload is rejected before write

## Current Implementation Slice

The implemented slice should remain focused on:

1. Workflow catalog loader and validator.
2. Shared path policy helpers.
3. Shared run record writer.
4. Mock provider interface.
5. Source Artifact Agent with dry-run and draft-only write.
6. Tests for the above.

Do not implement all agents at once. The source artifact slice establishes the contract that the rest of the agents reuse.

## Open Questions

1. Should source artifacts be accepted support surfaces immediately, or should all artifacts begin in `library/drafts/agent_outputs/source_artifacts/` until approved?
2. Should selected run records become tracked public examples later?
3. Should provider prompts be Markdown only, or YAML metadata plus Markdown body?
4. What is the smallest useful source artifact schema for public contributors?
5. What feedback format is easiest for maintainers to create and for agents to learn from?
