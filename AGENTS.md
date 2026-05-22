# Agent Runtime Instructions

This repository is the implementation home for Library, a standalone public knowledge-library system derived from earlier source-grounded knowledge work.

## Read First

When working in this repo, read these files before implementing non-trivial changes:

1. `DESIGN.md`
2. `INTERNAL_IMPLEMENTATION_PLAN.md`
3. The specific source files named in `INTERNAL_IMPLEMENTATION_PLAN.md` for the phase being implemented

`DESIGN.md` is the public-facing design surface. `INTERNAL_IMPLEMENTATION_PLAN.md` is the local implementation routing surface for coding agents.

## Reference Repos

Use the referenced internal and console repos as implementation references only.

- Use the internal project repo to understand the staged source-to-knowledge model.
- Use the console repo to understand the data-driven backend/frontend architecture.
- Do not import from those repos at runtime.
- Do not copy their project-specific vocabulary into public Library surfaces.
- Do not hard-code local absolute paths into public files.

## Build Order

Build in phases:

1. File-based knowledge-library core
2. Validation CLI
3. Read-only console
4. Workflow catalog and agent contracts for book creation
5. Agent-assisted book drafting
6. Public contribution surfaces

Do not start with the full console. The file-based library model must work first.

## Public Vocabulary

Prefer clear public terms:

- knowledge library
- source
- artifact
- seed
- knowledge target
- target index
- map
- brief
- book
- feedback
- Library console
- run record

Avoid legacy framework names in public code, examples, UI text, and documentation unless the reference is explicitly about project origin and has been approved.

## Public And Internal Boundary

Treat this repo as public-facing by default, even when working locally.

Internal docs may contain local reference paths and private implementation routing. Do not push internal docs or local-path references to the public remote unless explicitly approved by the maintainer.

Before pushing, audit changed files for:

- local absolute paths
- private project content
- copied source material from reference repos
- legacy vocabulary that should have been neutralized
- write-capable agent behavior that bypasses human approval

## Agent And Automation Rules

Agent-assisted workflows must preserve traceability.

Agents may help create artifacts, discover targets, map sources, draft briefs, draft books, record feedback, and explain changes. Agent output must not become accepted library content without explicit human approval.

Write-capable flows must begin as draft-only. The backend must reject absolute paths, parent-directory traversal, and writes outside the repository root.

## Technical Stack

For the first implementation, prefer:

- Python 3.11+
- FastAPI for the future backend
- Pydantic and PyYAML for structured validation
- pytest for tests
- Vite, React, TypeScript, and lucide-react for the future frontend

Keep implementation small and testable. Add abstractions only when they remove real duplication or support the next planned phase.

## Commit Guidance

Commit coherent phase-sized changes.

Do not push commits that expose internal planning or local paths unless the maintainer explicitly asks for that. When in doubt, leave local commits unpushed and report the exact status.
