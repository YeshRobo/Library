# Portfolio Project Brief: Library

Use this document as source material for a portfolio website, case study, or project page about Library.

## Project Name

Library

## One-Line Description

Library is a source-grounded knowledge system that turns scattered project material into traceable briefs, books, and feedback-driven knowledge outputs.

## Short Portfolio Summary

Library is a file-first knowledge library for organizing raw sources into useful, reviewable outputs. It defines a clear pipeline from original source material to compact artifacts, proposed knowledge targets, maps, briefs, long-form books, and feedback records. The project is designed for humans and AI-assisted workflows, but it keeps generated content draft-only until a human approves it.

The current implementation includes a structured repository model, reusable templates, a validation CLI, a read-only console API and React frontend, and a draft-only Source Artifact Agent that creates traceable source packets and run records.

## Problem

AI-assisted documentation and research workflows often produce outputs that are hard to trust because the final answer is separated from the material that supported it. Notes, transcripts, reports, design decisions, and release details can become scattered across files, making it difficult to answer:

- Where did this claim come from?
- Which source files support this summary?
- What is accepted knowledge versus a draft?
- What needs review, revision, or feedback?
- Can an AI agent help without silently rewriting accepted content?

Library addresses this by making traceability part of the core file model.

## Solution

Library organizes knowledge through a staged flow:

```text
sources -> artifacts -> seeds -> targets -> maps -> briefs -> books -> feedback
```

Each stage has a distinct role:

- Sources preserve raw or lightly processed material.
- Artifacts compress source material into smaller, traceable packets.
- Seeds propose possible knowledge targets.
- Targets register accepted knowledge needs and route readers to related files.
- Maps connect targets to supporting sources and artifacts.
- Briefs provide compact synthesis.
- Books expand mature targets into long-form knowledge.
- Feedback records use, failures, contradictions, and revision triggers.

This structure helps humans and language models work with the same knowledge base while preserving provenance and review boundaries.

## What I Built

- A public, file-based knowledge library structure under `library/knowledge/`.
- Templates for sources, artifacts, seeds, target indexes, maps, briefs, books, and feedback.
- A neutral example target that demonstrates the complete source-to-book flow.
- A Python validation CLI for required folders, templates, YAML structure, Markdown headings, valid lifecycle stages, safe relative paths, and missing references.
- A read-only FastAPI console backend with health, summary, validation, target list, and target detail endpoints.
- A Vite, React, and TypeScript frontend for browsing targets, validation status, sources, maps, briefs, and books.
- A draft-only Source Artifact Agent that can preview or write source-derived artifact drafts and run records.
- Safety rules that reject absolute paths, parent-directory traversal, and unsafe reads or writes outside the repository.
- Tests covering validation, console repository reads, unsafe paths, source artifact dry runs, draft writes, and malformed provider output.

## Technical Stack

- Python 3.11+
- PyYAML for structured validation
- FastAPI for the read-only console API
- Vite, React, TypeScript, and lucide-react for the frontend console
- unittest-based test coverage
- File-based Markdown and YAML knowledge surfaces

## Architecture Snapshot

Library is intentionally file-first. The durable project surface is the repository itself, not a database. The console and agents read from that structure instead of replacing it.

Core areas:

- `library/knowledge/`: accepted and draftable knowledge surfaces, organized by stage.
- `library/templates/`: reusable templates for each knowledge surface.
- `src/library_cli/`: command-line validation and agent entry points.
- `src/library_console/`: read-only repository reader and FastAPI API.
- `src/library_agents/`: draft-only agent workflow code and safety policies.
- `frontend/`: local read-only console UI.
- `catalog/`: workflow and prompt definitions for agent-assisted tasks.
- `tests/`: validation, console, and agent behavior tests.

## Product Principles

- Source-grounded output: every accepted knowledge surface should trace back to supporting material.
- Human approval: generated drafts are not accepted knowledge until reviewed.
- File durability: Markdown and YAML files remain useful without a running app.
- Small first implementation: validate the file model before expanding automation.
- Public vocabulary: the project uses clear terms like source, artifact, seed, target, map, brief, book, and feedback.
- Safe automation: agents can help draft and explain, but write-capable flows start as draft-only.

## Current Status

Library is an early v1 implementation. The foundational file model, templates, validation CLI, read-only console path, and Source Artifact Agent are in place. The project is not positioned as a finished SaaS product. It is best presented as an open-source developer tool and knowledge-system prototype with a clear architecture and safety model.

Implemented:

- File-based source-to-book knowledge structure
- Public templates
- Neutral example target
- Local validation CLI
- Read-only console backend and frontend
- Draft-only source artifact agent
- Run records for generated drafts
- Tests for core validation and safety behavior

Not the focus yet:

- Autonomous content acceptance
- Default external provider calls
- Multi-project hosting
- Production user management
- Full collaborative web editing

## Suggested Portfolio Positioning

Present Library as a systems-design and developer-tooling project. The strongest angle is not "an AI chatbot for documents." The stronger story is:

Library creates a trustworthy workflow around AI-assisted knowledge work by separating raw sources, derived artifacts, accepted targets, synthesis, long-form writing, and feedback.

Good portfolio categories:

- AI-assisted knowledge systems
- Developer tooling
- Information architecture
- Source traceability
- Local-first workflows
- Validation and safety systems
- Human-in-the-loop automation

## Suggested Website Sections

1. Hero
   - Title: Library
   - Subtitle: Source-grounded knowledge workflows for traceable briefs, books, and AI-assisted drafting.
   - Visual idea: a source-to-book pipeline with connected files, validation state, and trace links.

2. The Problem
   - Explain that AI-generated knowledge can become unreliable when it loses connection to source material.

3. The System
   - Show the pipeline: sources -> artifacts -> seeds -> targets -> maps -> briefs -> books -> feedback.
   - Briefly explain what each stage does.

4. What I Built
   - Highlight the CLI, templates, read-only console, source artifact agent, and safety model.

5. Architecture
   - Show a simple diagram with the file library at the center, CLI validation on one side, console reading on another, and draft-only agents producing run records.

6. Safety And Trust
   - Explain path validation, read-only console behavior, draft-only agent output, and human approval.

7. Technical Stack
   - List Python, PyYAML, FastAPI, React, TypeScript, Vite, and tests.

8. Outcome
   - Describe the project as a working foundation for traceable knowledge creation, not a finished hosted product.

## Ready-To-Use Website Copy

### Hero Copy

Library is a source-grounded knowledge system for turning scattered project material into traceable, reviewable knowledge outputs.

It organizes raw sources into artifacts, targets, maps, briefs, books, and feedback records so humans and AI agents can work from the same evidence without losing provenance.

### Case Study Intro

I built Library to explore a more trustworthy pattern for AI-assisted knowledge work. Instead of asking an AI model to produce final documentation from loose context, Library breaks the process into clear stages: preserve sources, create compact artifacts, propose targets, map evidence, write briefs, expand mature topics into books, and record feedback after use.

The result is a local-first knowledge system with a validation CLI, a read-only console, and draft-only agent workflows that preserve human review.

### Feature Highlights

- File-based knowledge model that works without a database.
- Source-to-book workflow with explicit traceability.
- CLI validation for structure, required fields, headings, links, and safe paths.
- Read-only console for browsing targets, validation state, and knowledge surfaces.
- Draft-only Source Artifact Agent with run records and human approval metadata.
- Tests for validation, repository reading, unsafe paths, and agent output behavior.

### Technical Highlight

The implementation combines a durable Markdown/YAML repository model with Python validation, a FastAPI read-only API, and a React console. Agent-assisted workflows are intentionally constrained: they can produce drafts and run records, but accepted knowledge remains under human control.

## Visual Direction For The Portfolio Page

The page should feel like a precise developer tool, not a marketing site for a chatbot. Use visuals that suggest structure, trust, and traceability:

- File tree or folder-stage diagram
- Evidence map connecting sources to briefs and books
- Console screenshot-style layout
- Validation status indicators
- Source cards and trace links
- Agent run record preview

Avoid visuals that imply fully autonomous content generation or a generic document chatbot.

## Claims To Avoid

- Do not call Library a production SaaS platform.
- Do not claim it autonomously creates accepted knowledge.
- Do not imply generated books are trusted without human review.
- Do not present the console as a full editing environment.
- Do not describe it as dependent on private repositories or private data.

## Keywords

AI-assisted knowledge management, source traceability, developer tools, local-first documentation, Markdown knowledge base, YAML validation, FastAPI, React, TypeScript, Vite, human-in-the-loop automation, knowledge synthesis, evidence mapping, draft-only agents.
