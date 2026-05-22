# Internal Source Artifact Agent Design

Status: internal design document
Audience: maintainers and coding agents building Library agents
Public status: do not push unless explicitly approved

## Purpose

This document defines the design of the Library Source Artifact Agent.

The agent is the first automation step in the target-centered Library flow:

```text
sources -> artifacts -> seeds -> targets -> maps -> briefs -> books -> feedback
```

Its job is narrow: turn one source file into one durable source artifact packet that later agents and maintainers can inspect, cite, and reuse. It does not create seeds, target indexes, maps, briefs, books, or feedback records.

## Reference Inputs

This design is based on:

- `library/knowledge/01_sources/library_knowledge_architecture_explanation.md`
- the source artifact runtime in `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1`
- the current Library implementation under `src/library_agents/source_artifact_agent/`

The reference repo is an implementation reference only. Library should keep neutral public vocabulary, avoid private framework terms in public surfaces, and avoid importing from the reference repo at runtime.

## Core Design Rule

The architecture source says:

```text
One source file -> one artifact file
```

Library v1 should interpret that as:

```text
One source file -> one artifact packet
```

The packet is the durable source-level representation. It may be stored as a folder with multiple small files because that is easier to inspect, validate, and partially reuse than one large generated blob. The packet still has one identity, one source link, one manifest, and one provenance trail.

Canonical packet path:

```text
library/knowledge/02_artifacts/<source_slug>/
```

Required packet files:

```text
source_card.yaml
source_summary.md
evidence_ledger.yaml
questions.md
candidate_tags.yaml
artifact_manifest.yaml
```

Future versions may add optional files such as `terms_entities.yaml`, `possible_knowledge_uses.md`, `contradictions.md`, or `confidence_limitations.md`, but those should not be required until validation and console display can handle them.

## Why The Agent Exists

Raw sources are often too long, messy, or uneven for downstream agents to load repeatedly. The artifact packet makes each source easier to use without pretending it is accepted knowledge.

The artifact packet should answer:

- What is this source about?
- Which details may matter later?
- Which lines or excerpts should remain traceable?
- Which questions, tensions, or limits does the source raise?
- Which future knowledge targets might use this source?
- What should downstream agents avoid assuming?

Artifacts reduce repeated source reading, but they do not replace sources. Downstream maps, briefs, and books should still be able to trace claims back through artifact evidence to the original source path and source hash.

## Boundaries

The Source Artifact Agent may:

- read an allowed source file under `library/knowledge/01_sources/`
- read its workflow prompt and workflow catalog entry
- inspect existing artifact files for the same source
- generate a draft artifact packet
- write draft artifact files under `library/knowledge/02_artifacts/`
- write a run record under `runs/`

The Source Artifact Agent must not:

- rewrite source files
- accept an artifact as final truth
- create seeds, target indexes, maps, briefs, books, or feedback
- mutate accepted target, map, brief, or book files
- read files outside the workflow read policy
- write outside the workflow draft root or run record root
- bypass human approval

## Architecture Pattern

The reference implementation uses a clean domain split that Library should keep:

```text
source_artifact_agent/
  common/
  perception/
  mind/
  action/
  orchestrator.py
  cli.py
```

### Common

Common owns shared data contracts and errors.

Library common types should include:

- request type
- source observation type
- provider prompt packet
- provider response type
- outcome type
- validation error type
- action error type

Common must not read files, call providers, or write output.

### Perception

Perception reads allowed repository surfaces and emits neutral observations.

It should collect:

- source path
- source text
- source hash
- prompt text
- existing artifact paths for the same source
- optional existing artifact parse results
- optional prior run record or ledger state

Perception should not decide whether a source is actionable. It should not classify missing, stale, invalid, or covered states. It should not call providers or write files.

### Mind

Mind owns interpretation and candidate quality.

It should:

- compute the source slug
- build the provider prompt packet
- select or call the provider
- validate candidate payloads
- classify source state when repository-wide discovery is added
- decide whether stale or invalid artifacts are actionable under the request policy

Mind must not write files.

### Action

Action writes only already-validated draft output and run records.

It should:

- compute planned artifact paths
- enforce draft-root and extension policy
- refuse overwrite unless explicitly allowed
- render YAML and Markdown files
- write the artifact manifest
- write the run record

Action must not classify source state, call providers, or inspect broad repository state.

### Orchestrator

The orchestrator wires the domains together:

```text
load workflow -> perceive source -> build prompt -> provider -> validate -> plan -> write or dry-run -> run record
```

It should remain glue code. If the orchestrator starts owning policy, prompt design, validation, or write formatting, that logic should move back into the domain module that owns it.

### CLI

The CLI is a thin user interface.

It should:

- parse `source_path`, `--repo-root`, `--write`, `--overwrite`, and provider flags
- default to dry-run
- print read paths, planned draft paths, and run record status
- map user-facing errors to nonzero exit codes
- never hide which files may be read or written

## Workflow Contract

The workflow catalog entry is the executable contract for the agent.

Minimum shape:

```yaml
workflow_id: source_artifact
name: Source Artifact Agent
agent_module: library_agents.source_artifact
mode: draft_only
prompt_path: catalog/prompts/source_artifact.md
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

The read policy includes `02_artifacts` so the agent can inspect existing artifact packets for the selected source. A source input itself must still be under `01_sources`; artifact paths must be rejected as source inputs.

## Artifact Packet Schema

### `source_card.yaml`

Required fields:

```yaml
source_slug: project_release_notes_source
source_title: Project Release Notes Source
source_path: library/knowledge/01_sources/project_release_notes_source.md
source_type: md
artifact_status: draft
source_sha256: <sha256>
```

Future fields:

```yaml
artifact_schema_version: 1
created_at: <iso timestamp>
source_imported_at: <iso timestamp or unknown>
bias_lens: <provider or agent lens, if known>
confidence: low|medium|high
limitations: []
```

### `source_summary.md`

Required sections:

```markdown
# Source Summary: <title>

## Summary

## Notable Points
```

The summary should be compact. It should preserve what the source says, not what the Library has accepted as truth.

### `evidence_ledger.yaml`

Required fields:

```yaml
source_path: library/knowledge/01_sources/project_release_notes_source.md
source_sha256: <sha256>
excerpts:
  - line: 12
    text: Exact or near-exact source excerpt.
```

Future fields:

```yaml
excerpts:
  - line: 12
    text: Exact or near-exact source excerpt.
    role: definition|claim|example|constraint|question|contradiction|context
    confidence: low|medium|high
```

### `questions.md`

This file records questions the source raises. Questions may later trigger seeds, map updates, brief revisions, or feedback records.

### `candidate_tags.yaml`

This file records lightweight retrieval tags. Tags are hints, not accepted classification.

### `artifact_manifest.yaml`

Required fields:

```yaml
artifact_status: draft
run_id: source_artifact_YYYYMMDD_HHMMSS_project_release_notes_source
provider: mock
model: mock-local
source_path: library/knowledge/01_sources/project_release_notes_source.md
source_sha256: <sha256>
artifact_files: []
human_approval:
  required: true
  approved: false
```

The manifest is the packet identity and provenance surface. It should make the artifact's draft status obvious.

## Source State Model

The current Library implementation processes one explicit source path. The reference implementation adds a useful repository-wide state model that Library should adopt when the agent grows.

Recommended states:

- `missing`: source has no artifact packet
- `covered`: source has a valid artifact packet matching the current source hash
- `stale`: source hash changed since the artifact packet or run record baseline
- `invalid`: artifact packet exists but fails schema, parse, source-link, or hash checks
- `blocked`: source cannot be processed because of path policy, missing prompt, provider refusal, or unsupported type

Policy rules:

- `missing` is actionable.
- `covered` is skipped unless explicit refresh is requested.
- `stale` is actionable only with explicit refresh and overwrite approval.
- `invalid` is actionable only for a selected source or with explicit repair approval.
- `blocked` is never written; it reports the reason.

## Provider Strategy

The default provider should remain `mock`.

The mock provider is important because it makes tests deterministic and lets contributors run the workflow without API keys.

External providers may be added later, but they must follow the same interface:

- receive a structured prompt packet
- receive only files allowed by the workflow read policy
- return a structured candidate payload
- include model and usage metadata when available
- allow tests to replace the provider without network access

The provider should not write files. The provider should not decide whether output is accepted. The provider only returns a candidate.

## Prompt Strategy

The prompt should be bounded and inspectable.

Required prompt inputs:

- workflow rules from `catalog/prompts/source_artifact.md`
- selected source path
- selected source hash
- selected source text
- existing artifact paths for the same source

Optional future prompt inputs:

- source template
- artifact template
- current public design excerpt
- target vocabulary rules
- artifact schema description

The prompt should tell the provider:

- stay grounded in the selected source
- preserve line references when possible
- mark output as draft
- do not create seeds, targets, maps, briefs, books, or feedback
- leave uncertainty visible
- avoid turning source interpretation into accepted knowledge

## Validation Strategy

Candidate validation is the gate between provider output and file writes.

Validation must check:

- payload is a mapping
- `source_card.source_slug` matches the selected source path
- `source_card.source_path` matches the selected source path
- `source_card.source_sha256` matches the selected source hash
- `source_card.artifact_status` is `draft`
- source slug is lowercase snake case
- source summary has a title, summary, and notable points
- evidence ledger points to the same source path and hash
- evidence excerpts have positive line numbers and non-empty text
- questions and candidate tags are non-empty string lists

Write validation must check:

- all draft paths are under `library/knowledge/02_artifacts/`
- all draft files use allowed extensions
- existing draft files are not replaced without `--overwrite`
- run record paths stay under `runs/`

Future validation should include:

- artifact packet schema validation in `library-cli validate`
- manifest references all packet files
- packet source hash matches the current source hash or is marked stale
- evidence excerpt line numbers exist in the source file
- no accepted map references a missing artifact packet

## Run Record Contract

Every write run should produce a run record.

Minimum fields:

```yaml
run_id: source_artifact_YYYYMMDD_HHMMSS_project_release_notes_source
workflow_id: source_artifact
agent_name: Source Artifact Agent
provider: mock
model: mock-local
status: completed
started_at: <iso timestamp>
finished_at: <iso timestamp>
read_paths: []
draft_paths: []
validation:
  ok: true
  findings: []
human_approval:
  required: true
  approved: false
usage: {}
```

The run record is separate from the artifact manifest. The manifest travels with the artifact packet. The run record describes the execution event.

## Downstream Integration

Artifacts are source-level support surfaces.

Seed Discovery Agent should read artifact packets and propose seeds when a need, pattern, question, task, or contradiction emerges.

Map Agent should reference artifacts first and raw sources second. Maps explain why an artifact belongs to a target.

Brief and Book agents should cite maps, which cite artifacts, which cite sources.

Feedback should be able to mark artifacts as stale, insufficient, contradicted, or useful for a new target.

Traceability should remain:

```text
brief/book -> map -> artifact packet -> source
```

## Safety Rules

The agent must preserve these rules:

1. Default to dry-run.
2. Reject absolute paths, parent-directory traversal, and paths outside the repo root.
3. Reject artifact paths as source inputs.
4. Read only workflow-approved roots.
5. Write only under the draft root and run record root.
6. Never mutate accepted target, map, brief, book, or feedback surfaces.
7. Validate provider output before writing.
8. Mark all artifacts as draft.
9. Require human approval before downstream accepted content treats an artifact as reliable.
10. Record provider, model, source hash, read paths, and draft paths.

## CLI Design

Current CLI behavior should stay small:

```bash
library-cli source-artifact library/knowledge/01_sources/project_release_notes_source.md
library-cli source-artifact library/knowledge/01_sources/project_release_notes_source.md --write
library-cli source-artifact library/knowledge/01_sources/project_release_notes_source.md --write --overwrite
```

Future CLI flags:

```text
--scan
--limit N
--refresh-stale
--provider <name>
--model <name>
--json
```

`--scan` should use the source state model. It should report covered, missing, stale, invalid, and blocked sources without writing unless combined with explicit write flags.

## Console Design

The read-only console should eventually show:

- source list with artifact coverage state
- selected source text preview
- artifact packet files
- source hash and artifact hash
- run record history
- stale or invalid artifact warnings
- planned read and write paths before a workflow run

Workflow triggering from the console should wait until CLI workflow behavior, tests, and run records are stable.

## Test Matrix

Required tests:

- workflow catalog loads
- dry-run plans artifact paths without writing
- write creates all packet files and a run record
- accepted target/map/brief/book files are not mutated
- path traversal is rejected
- absolute paths are rejected
- artifact paths are rejected as source inputs
- malformed provider payload is rejected before write
- overwrite refuses existing files unless explicitly allowed
- prompt path must exist

Future tests:

- repository scan classifies missing, covered, stale, invalid, and blocked states
- stale source refresh requires both refresh and overwrite approval
- evidence ledger line numbers point to real source lines
- run record records failed validation and provider refusal
- console can display artifact coverage state without write access

## Implementation Status

Implemented now:

- workflow catalog loader
- path policy helpers
- mock provider
- single-source dry-run
- single-source draft write
- run record writer
- packet files under `library/knowledge/02_artifacts/<source_slug>/`
- validation before write
- tests for path safety, dry-run, write, and malformed provider payloads

Next recommended iteration:

1. Add artifact packet validation to `library-cli validate`.
2. Add source scan and source state classification.
3. Add stale detection through source hash and latest run record.
4. Add optional richer artifact fields for possible knowledge uses, contradictions, terms, and limitations.
5. Add read-only console display for artifact coverage and packet contents.
6. Add an external provider adapter behind the existing provider interface.

## Open Questions

1. Should Library eventually enforce a single artifact file, or keep the current packet folder as the canonical artifact unit?
2. Should artifacts require explicit human approval before maps may reference them?
3. Should artifact confidence start as text, a small enum, or a structured scoring model?
4. How should the agent represent non-text sources such as PDFs, images, transcripts, or extracted code?
5. Should `candidate_tags` remain a lightweight retrieval aid, or become a controlled vocabulary later?
6. Should stale artifacts remain visible to downstream agents with warnings, or be blocked until refreshed?
