# Internal Source Artifact Agent Design

Status: internal design document
Audience: maintainers and coding agents building Library agents
Public status: do not push unless explicitly approved

## Purpose

This document defines the design of the Library Source Artifact Agent.

The agent should not be understood as an independent knowledge worker. It is a pipeline bridge inside the target-centered Library flow:

```text
01_sources -> Source Artifact Agent -> 02_artifacts -> 03_seeds -> 04_targets -> 05_maps -> 06_briefs -> 07_books -> 08_feedback
```

Its job is narrow: take one preserved source file from `library/knowledge/01_sources/` and turn it into one compact, durable source artifact packet under `library/knowledge/02_artifacts/`. The main purpose of that packet is context compression: later LLM agents should be able to load many artifact packets together without context overload, then compare them to propose seeds.

The artifact is therefore not mainly a human summary. It is a source-level context unit for downstream Library agents. It keeps enough identity, orientation, evidence pointers, and limits for later agents to inspect, cite, compare, and reuse the source without loading every raw source file at once.

The agent does not decide what knowledge target should exist. It does not create seeds, target indexes, maps, briefs, books, or feedback records. It prepares the source so Seed Discovery and later steps can work over many smaller, traceable, source-grounded packets instead of repeatedly rereading raw files.

In short:

```text
Source Artifact Agent = one-source compression into multi-artifact LLM context units
```

## Reference Inputs

This design is based on:

- `library/knowledge/01_sources/library_knowledge_architecture_explanation.md`
- the source artifact runtime in `/home/robo/UM2M_MULTIVERSE/repos/um2m_oarm101_isaac_v1`
- the current Library implementation under `src/library_agents/source_artifact_agent/`

The reference repo is an implementation reference only. Library should keep neutral public vocabulary, avoid private framework terms in public surfaces, and avoid importing from the reference repo at runtime.


## Pipeline Position

The Source Artifact Agent sits between raw source preservation and downstream knowledge discovery. Its immediate downstream consumer is usually not a human reader; it is a seed-building or mapping LLM that needs to load many source representations together.

It receives:

- one selected source file from `01_sources`
- workflow rules from the catalog
- the source artifact prompt
- optional existing artifact packet state for the same source

It emits:

- one draft artifact packet in `02_artifacts`
- one artifact manifest that preserves source identity and provenance
- one run record that records what was read, generated, validated, and written

It hands off to:

- Seed Discovery, which loads many artifact packets into one LLM context and proposes seeds from patterns, questions, needs, contradictions, or overlooked fragments
- Target acceptance, which decides which seeds become registered knowledge targets
- Map agents, which connect accepted targets to supporting artifacts and sources
- Brief and Book agents, which synthesize target-level outputs from maps and evidence
- Feedback workflows, which later mark artifacts and outputs as useful, stale, misleading, contradicted, or in need of revision

The agent should therefore be designed around downstream context packing, not autonomy. Its output must be compact enough for multi-artifact loading, stable enough for later steps to consume, and modest enough that it does not pre-decide the work those later steps own.

## Step Boundary Table

| Library step | Receives | Produces | Must not do |
| --- | --- | --- | --- |
| Sources | imported or raw material | preserved source files | overwrite evidence with interpretation |
| Source Artifact Agent | one source file | one draft artifact packet | create seeds, targets, maps, briefs, books, or truth claims |
| Seed Discovery | many artifacts, user needs, agent needs, contradictions, patterns | proposed seeds | treat a seed as accepted knowledge |
| Targets | accepted seeds | stable target identity/index | pretend one source equals one final output |
| Maps | target plus relevant artifacts/sources | target-level evidence map | synthesize final prose as if evidence is settled |
| Briefs | target map and evidence | compact usable answer | claim final truth |
| Books | mature target, maps, briefs, feedback | long-form synthesis | become unrevisable doctrine |
| Feedback | use results, failures, contradictions, revisions | confidence and revision signals | erase provenance |

This boundary table should guide implementation decisions. When in doubt, the Source Artifact Agent should preserve and compress source-level evidence, then stop.

## Primary Design Purpose: Multi-Artifact Context Loading

The most important purpose of the artifact layer is to let an LLM reason over many sources without loading all raw sources into context.

A raw source may be too long, messy, repetitive, or uneven to load alongside many other raw sources. An artifact packet should act as a compact source proxy. It should preserve the source identity and enough orientation for a downstream agent to decide whether the raw source needs to be reopened.

The Seed Discovery Agent should be able to load a bundle like this:

```text
artifact_a + artifact_b + artifact_c + artifact_d + artifact_e + user/agent need
```

and ask:

```text
What seeds might emerge from this collection of source-grounded packets?
```

That means artifact quality should be judged by a practical downstream question:

```text
Can many artifacts fit together in context while still giving a seed agent enough source-grounded signal to notice possible knowledge targets?
```

This is different from asking whether the artifact fully explains the source. It should not. A good artifact is small enough to travel with many other artifacts and grounded enough to point back to the raw source when deeper inspection is needed.

## Core Design Rule

The architecture source says:

```text
One source file -> one artifact file
```

Library v1 should interpret that as:

```text
One source file -> one artifact packet
```

The packet is the durable source-level representation and context-compression unit. It may be stored as a folder with multiple small files because that is easier to inspect, validate, and partially reuse than one large generated blob. The packet still has one identity, one source link, one manifest, and one provenance trail.

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

Raw sources are often too long, messy, or uneven for downstream agents to load repeatedly, especially when seed discovery needs to compare many sources at once. The artifact packet is the first reusable interface between source preservation and later knowledge work. It reduces each source into a smaller, traceable context packet so later LLM agents can load multiple artifacts together without context overload and without pretending the artifacts are accepted knowledge.

The agent exists because seed-building and mapping workflows need source-grounded inputs that are smaller than raw sources but more reliable than loose summaries. It should make a source easier to recognize, retrieve, compare, cite, and revisit while preserving enough compact signal for cross-artifact pattern discovery.

The v0 artifact packet should answer only low-judgment questions:

- What file is this?
- What obvious title or headings does it contain?
- What simple orientation summary helps a reader recognize the source?
- What small deterministic sample of lines can help a reader recognize it?
- Which explicit questions already appear in the source?
- What did the agent avoid inferring?

Artifacts reduce repeated source reading and model-context load, but they do not replace sources. Downstream seeds, maps, briefs, and books should still be able to trace claims back through artifact evidence to the original source path and source hash.

The artifact should usually be much smaller than the source. If an artifact starts copying most of the source, it has failed its main job. The success condition is not "maximum detail preserved"; the success condition is "enough grounded signal preserved for many artifacts to be loaded together and used for seed discovery."

### Handoff Contract

The artifact packet is not an end product. It is a handoff object.

For downstream agents, it should provide:

- enough source identity to find and verify the raw source
- enough orientation to decide whether the source may be relevant
- enough compact signal for cross-artifact seed discovery
- enough line-referenced evidence to support first-pass inspection
- enough limitations to prevent overconfident downstream use
- enough manifest metadata to detect stale, invalid, duplicate, or replaced packets

For upstream source preservation, it should never mutate, rewrite, or replace the original source. The source remains the authority. The artifact is only a compact working representation of that source.

## Working Ideal Artifact Agent

This is the current working picture of an ideal Source Artifact Agent. It is not final doctrine. Library may redefine the ideal after real sources, maps, briefs, books, and feedback show what actually helps.

An ideal artifact agent should turn a source into a durable, inspectable, context-efficient source artifact that helps later seed-building and book-building workflows without pretending the source has already become accepted knowledge.

The ideal agent should eventually be able to:

- identify the source and preserve provenance
- compress the source into a context-sized packet for multi-artifact use
- create a compact source orientation summary
- extract useful evidence with source line references
- separate direct source evidence from interpretation
- identify explicit questions, tensions, terms, entities, and repeated patterns
- propose candidate tags or retrieval handles without treating them as accepted classification
- explain why each extracted item was included
- notice stale, thin, contradictory, or low-quality artifact packets
- learn from downstream maps, briefs, books, and feedback about which artifact fields are useful
- expose uncertainty and limitations instead of hiding them
- keep all generated output draft-only until reviewed or accepted by a human workflow

The ideal agent should not become a book writer, target decider, or truth authority. It should prepare source material so later stages can decide what belongs in seeds, targets, maps, briefs, and books.

The ideal agent is valuable because it makes later agents better. Its success should be judged first by whether Seed Discovery can load many artifacts together and notice useful candidate seeds, and second by whether Map, Brief, Book, and Feedback workflows can use those artifacts with less rereading, less confusion, and better provenance.

## Starting Point: V0 Source Orientation Agent

The v0 agent is the agent to build now. It is intentionally smaller than the ideal agent.

The agent does not know what will matter later. It should not pretend to, and v0 should not try to approximate that judgment.

The Source Artifact Agent should begin as a source orientation and compression tool. It should create a stable source identity, a small source summary, a tiny source preview, and traceability metadata. Its v0 output should be small enough that many artifacts can be packed into one LLM context for seed discovery. It should not decide importance, infer future targets, or claim that any detail matters beyond the source itself.

The practical rule is:

```text
compress the source, identify it, provide a simple orientation summary, preserve a small preview, avoid deeper inference
```

### Allowed V0 Signals

The agent may use only signals that require little or no interpretation:

- source path
- source file extension
- source hash
- source line count and character count
- source text for a short orientation summary
- first Markdown heading, if present
- Markdown headings in order, if present
- first few non-empty lines
- explicit lines ending in `?`
- existing artifact paths for the same source

The agent should not use broad repository guessing. It should not read targets, maps, briefs, or books for v0 artifact creation.

### V0 Extraction Rules

For each artifact question, the agent should use a mechanical rule:

| Artifact question | V0 rule |
| --- | --- |
| What file is this? | Record path, slug, extension, hash, line count, character count, and artifact status. |
| What obvious title or headings does it contain? | Extract Markdown headings exactly as written, plus line numbers. |
| What simple orientation summary helps a reader recognize the source? | Write 1 to 3 draft sentences about what the source appears to contain, using cautious wording. |
| What small sample can help a reader recognize it? | Capture the first 3 to 5 non-empty body lines, excluding repeated blank lines. |
| Which explicit questions appear? | Capture only lines that already end in `?`; do not infer questions. |
| What did the agent avoid inferring? | Write a fixed note: `No target, importance, or truth claim inferred by v0 artifact extraction.` |

### V0 Summary Rule

The v0 summary is allowed because Library has to start somewhere useful.

It must stay at source-orientation level:

```text
This source appears to contain notes about <visible subject>.
```

It must not say:

```text
The important lesson is...
This proves...
This source should support target...
The correct conclusion is...
```

The summary should be treated as a draft label on the source, not as accepted knowledge. If a later map, brief, book, or feedback record shows the summary was misleading, the artifact should be revised.

### V0 Evidence Budget

The agent should not try to preserve important evidence yet.

Default v0 evidence budget:

- first heading, if present
- all headings up to a conservative cap, such as 30 headings
- first 3 to 5 non-empty body lines
- explicit question lines up to a conservative cap, such as 20 questions

This is not enough to support synthesis. It is only enough to identify the source, make it skimmable, and support later tooling.

### V0 Context Budget

V0 should optimize for fitting multiple artifacts into one model context.

This is the main practical reason artifacts exist. A Seed Discovery Agent should be able to load many artifact packets together, compare them, and ask what knowledge targets may be worth proposing. Therefore, each artifact should be treated as a context budget object, not as a full source rewrite.

The agent should:

- keep the summary to 1 to 3 sentences
- keep source excerpts short and capped
- keep questions and tags capped
- avoid copying full sections from the source
- prefer pointers, hashes, line numbers, and compact excerpts over long generated prose
- preserve just enough signal for later agents to decide whether to reopen the raw source

V0 does not need a perfect token budget yet, but every artifact should be visibly smaller than the source except for tiny source files. A rough implementation target can be added later, such as "artifact packet should normally be no more than 5 to 15 percent of the source text," but v0 should start with visible compression and conservative caps rather than a hard token rule.

### No Confidence Claims In V0

V0 should not emit confidence labels about source meaning.

Allowed status language:

- `draft`: generated artifact packet, not reviewed
- `source_orientation`: generated with low-judgment source-orientation rules
- `needs_review`: human or later agent should decide whether the source matters

Do not use `low`, `medium`, or `high` confidence until there is feedback data or an evaluation process.

### No Future Target Guessing In V0

V0 should not answer which future knowledge targets might use a source.

Instead, it should emit only mechanical retrieval labels:

- source slug parts
- heading words, normalized lightly
- file extension
- explicit title words

These labels are search aids, not target proposals.

Seed Discovery and Map agents should be built later, after there is enough artifact data to evaluate whether target prediction is useful at all.

### Later Learning Loop

Selection quality should improve only after there is actual use data.

Later workflows should be able to record:

- which artifact fields were useful in maps, briefs, or books
- which fields were ignored repeatedly
- which details had to be recovered manually from raw sources
- which source previews were misleading or too thin

Only after that data exists should Library add semantic selection, candidate uses, confidence labels, or target prediction.

## Boundaries

The Source Artifact Agent has upstream and downstream boundaries.

Upstream boundary:

- it may read selected source material and approved workflow context
- it must preserve source identity, path, hash, and line references
- it must not rewrite or normalize the source itself

Downstream boundary:

- it may produce a draft artifact packet that later workflows can inspect
- it may include mechanical retrieval labels and explicit source questions
- it must not decide seed acceptance, target membership, map relevance, brief synthesis, book claims, or feedback confidence

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
extraction_mode: mechanical
review_status: needs_review
```

### `source_summary.md`

Required sections:

```markdown
# Source Summary: <title>

## Simple Summary

## Summary Basis

## Not Claims
```

The summary should be compact and cautious. It should orient a reader to what the source appears to contain, not decide what matters.

`Summary Basis` should list the visible inputs used, such as first heading, Markdown headings, first non-empty lines, or explicit repeated phrases.

`Not Claims` should state that the summary does not decide importance, truth, target membership, or downstream use.

### `evidence_ledger.yaml`

Required fields:

```yaml
source_path: library/knowledge/01_sources/project_release_notes_source.md
source_sha256: <sha256>
excerpts:
  - line: 12
    text: Exact or near-exact source excerpt.
```

Future fields after real use data exists:

```yaml
excerpts:
  - line: 12
    text: Exact or near-exact source excerpt.
    extraction_reason: heading|opening_sample|explicit_question
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
- orientation rules from `Starting Point: V0 Source Orientation Agent`

Optional future prompt inputs:

- source template
- artifact template
- current public design excerpt
- target vocabulary rules
- artifact schema description

The prompt should tell the provider:

- stay grounded in the selected source
- preserve line references when possible
- extract source identity, headings, first non-empty lines, and explicit question lines
- write only a short source-orientation summary
- avoid deciding importance or usefulness
- do not infer future target ideas
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
- source summary has a title, simple summary, summary basis, and not-claims note
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

Artifacts are source-level support surfaces. They should be designed as stable inputs for the rest of the Library pipeline, not as isolated summaries.

### Seed Discovery Handoff

Seed Discovery should read many artifact packets together and propose seeds when a need, pattern, question, task, contradiction, or underused idea emerges.

This is the first major downstream use case for artifacts. The Seed Discovery Agent should not have to load every raw source file. It should begin with compact artifact packets, compare them inside one manageable context, and reopen raw sources only when the artifact packet indicates that deeper evidence is needed.

The Source Artifact Agent may preserve explicit questions and lightweight retrieval tags, but it should not decide that those questions are seeds. A seed requires a downstream need or pattern, not only the existence of a source detail.

### Target Handoff

Targets are accepted work areas. The Source Artifact Agent should not create or register them.

A later target workflow may use artifact packets to justify why a seed deserves a stable target identity. That target decision should remain separate from artifact extraction.

### Map Handoff

Map agents should use artifact packets as the first source-level interface and raw sources as the verification layer.

A map should answer why an artifact belongs to a target. The artifact should only make that decision possible by preserving source identity, excerpts, questions, and limitations.

### Brief and Book Handoff

Brief and Book agents should cite maps, maps should cite artifacts, and artifacts should cite sources.

The artifact should therefore preserve enough provenance for this chain:

```text
brief/book -> map -> artifact packet -> source
```

A brief or book may synthesize across many artifacts. The Source Artifact Agent should not do that synthesis.

### Feedback Handoff

Feedback workflows should be able to mark an artifact packet as:

- useful for a target
- too thin
- misleading
- stale
- contradicted
- needing richer extraction
- needing raw source reread
- repeatedly ignored by downstream workflows

This feedback may later justify adding richer fields to artifact packets. Until that use data exists, v0 should remain mechanical and conservative.

### Interface Principle

Each Library step should pass forward a clear object:

```text
source file -> artifact packet -> seed proposal -> target index -> evidence map -> brief/book -> feedback record
```

The Source Artifact Agent owns only the first transformation:

```text
source file -> artifact packet
```

Everything after that is a downstream workflow.

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
4. Add optional richer mechanical fields such as heading index, line counts, and extraction reason.
5. Add read-only console display for artifact coverage and packet contents.
6. Use accumulated map/brief/book/feedback data to decide whether semantic fields are worth adding.
7. Add an external provider adapter behind the existing provider interface.

## Open Questions

1. Should Library eventually enforce a single artifact file, or keep the current packet folder as the canonical artifact unit?
2. Should artifacts require explicit human approval before maps may reference them?
3. Should artifact confidence start as text, a small enum, or a structured scoring model?
4. How should the agent represent non-text sources such as PDFs, images, transcripts, or extracted code?
5. Should `candidate_tags` remain a lightweight retrieval aid, or become a controlled vocabulary later?
6. Should stale artifacts remain visible to downstream agents with warnings, or be blocked until refreshed?
