# Library Design

## Purpose

Library is a source-grounded knowledge library for turning scattered project material into useful, traceable, revisable knowledge outputs.

The project starts with one simple idea: useful knowledge should not appear from nowhere. A brief, book, guide, reference page, or agent packet should grow from sources, artifacts, seeds, targets, maps, compact synthesis, and feedback.

This repository begins with a file-based model on purpose. The first public goal is to make the source-to-output workflow clear before the console or agent workflows become larger.

## Project Origin

Library is built from lessons learned in earlier internal work that explored source-grounded knowledge organization, staged synthesis, agent-assisted workflows, and console-driven navigation.

The public project should not require users to understand that earlier work. Library is the standalone community version. Public contributors should feel free to simplify, rename, challenge, or replace inherited ideas when a clearer source-to-knowledge design emerges.

## Design Goals

Library should be:

- easy to understand without special terminology
- useful for small projects and large knowledge bases
- source-grounded, with clear traceability back to original material
- focused on producing need-based knowledge outputs from organized library material
- friendly to human readers and AI-assisted workflows
- structured enough to support automation
- flexible enough to support different domains
- public, practical, and community-improvable

Library should avoid:

- hidden framework assumptions
- project-specific vocabulary
- binding claims that cannot be traced to source material
- forcing every project into the same folder layout before the pattern is proven
- turning early notes directly into long-form books
- treating generated content as accepted knowledge without review

## Core Idea

Library organizes knowledge through a staged flow:

```text
sources -> artifacts -> seeds -> targets -> maps -> briefs -> books -> feedback
```

Each stage has a different job.

`sources` preserve raw or lightly processed material.

`artifacts` compress source-derived material into compact, traceable packets so later work can compare multiple sources in one working context.

`seeds` propose possible knowledge targets based on a need, pattern, question, conflict, task, or perspective.

`targets` register accepted knowledge needs and route readers to the surfaces for one target.

`maps` gather the files that support a target and explain why each file belongs.

`briefs` summarize what is currently understood about a target.

`books` expand mature targets into long-form, readable knowledge.

`feedback` records use, failure, contradiction, confidence changes, and revision triggers.

The stages are deliberately separate. A source is not an artifact. An artifact is not a seed. A seed is not an accepted target. A brief is not automatically a complete book. This separation keeps knowledge traceable and lets outputs mature from grounded material.

## Repository Shape

The file-based core uses this shape:

```text
Library/
  DESIGN.md
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
  src/
  tests/
```

The numeric prefixes keep the folders sorted in the source-to-knowledge flow.

Future console and agent code should serve this file model rather than replace it.

## Knowledge Components

### Sources

Sources are the raw inputs to the library. They may include notes, reports, transcripts, issue summaries, research excerpts, design sketches, audit results, or other source material.

A source should preserve context rather than rewrite it too aggressively. The goal is to keep later briefs, books, and other outputs traceable.

### Artifacts

Artifacts are compact source-derived draft surfaces created from sources.

The main purpose of an artifact is to reduce the size of a source so humans and language models can load multiple artifacts together while still tracing useful claims back to the original source. An artifact is a context packet, not a replacement for the source and not accepted knowledge by itself.

A good artifact set may include:

- a source card
- a source summary
- an evidence ledger
- questions raised by the source
- candidate tags
- an artifact manifest

Artifacts prepare source material for target discovery, mapping, briefs, and books. They should stay smaller than the source, preserve provenance, and avoid becoming long summaries or hidden synthesis.

### Seeds

A seed proposes that a knowledge target may be worth creating.

A good seed answers:

- What knowledge target may be useful?
- What need, pattern, question, conflict, or task triggered the proposal?
- Which sources or artifacts appear to support it?
- What output type may be useful?
- What should remain out of scope?

Seeds are intentionally lightweight. They help avoid creating a full target before there is enough evidence that the target matters.

### Targets

A target is an accepted need, question, pattern, or output area that Library decides is worth organizing around.

A good target index answers:

- What need does this target serve?
- Which seeds created or influenced it?
- What is the current maturity stage?
- Which maps, briefs, books, feedback records, and source files belong to it?
- Where should a reader or tool go next?

The target index should be fast to scan. Its purpose is navigation and identity, not deep synthesis.

### Maps

A map gathers evidence related to a target and explains why each file belongs.

A good map answers:

- Which sources and artifacts support this target?
- What does each source or artifact contribute?
- Which files are primary evidence?
- Which files are secondary context?
- Which files are conflicting, missing, or out of scope?

A source or artifact may appear in more than one map when justified. The map should make that relationship visible instead of hiding it.

### Briefs

A brief is the required compact synthesis for a target.

A good brief answers:

- What do we currently understand?
- What evidence supports that understanding?
- What constraints, tensions, or conflicts matter?
- What remains uncertain?
- What should a reader or agent consult next?

Briefs should be short enough to retrieve quickly and rich enough to preserve important distinctions.

### Books

A book is an optional long-form treatment of a mature target.

A good book answers:

- What is the complete readable treatment of this target?
- How do the sources, artifacts, map, and brief relate to each other?
- What patterns, constraints, and tradeoffs appear?
- What does the reader need to know before acting on this target?
- What questions remain open?

Books are deep knowledge surfaces. They should remain source-grounded and should clearly mark inference when the source material does not directly state a claim.

### Feedback

Feedback records how a knowledge output performs when it is used.

A good feedback record answers:

- Which target or output was used?
- What task or need used it?
- Did it help, fail, mislead, or get contradicted?
- What revision is needed?
- How should confidence change?

Feedback should not silently rewrite accepted knowledge. It should point to the target, brief, book, or map that needs review.

## Confidence Model

Library treats confidence as provisional.

Confidence can increase through source support, source diversity, successful reuse, independent rediscovery by different agents, low contradiction level, and successful reality checks.

Confidence can decrease through contradicted evidence, failed use, stale source material, unsupported synthesis, or stronger replacement outputs.

A book in Library means: this is the current best consolidated understanding for this target, based on available sources, evidence, use, and revision history. It does not mean final truth.

## Console Concept

Library should eventually include its own console.

The console should be a practical interface for browsing, querying, and building knowledge targets. It should not replace the file-based structure. The files remain the durable project surface; the console makes that surface easier to use.

The console may include:

- a target browser
- source traceability views
- map, brief, and book readers
- feedback and confidence views
- maturity indicators
- search and query tools
- provider adapters for AI-assisted workflows
- run records for generated outputs

The console should be data-driven. Project-specific behavior should live in configuration, not hardcoded assumptions.

## Automation Model

Automation should support the library without taking ownership away from maintainers.

Possible automation:

- create artifacts from new source material
- propose seeds from artifacts, questions, tasks, or contradictions
- detect source files that may belong to existing targets
- draft maps
- draft briefs from mapped sources and artifacts
- expand mature briefs into book drafts
- compare briefs and books against source evidence
- identify stale or unsupported claims
- create feedback records after use
- generate run records for AI-assisted work

Automation should always preserve traceability. If a tool writes or proposes content, readers should be able to see what source material was used and what generation state the output is in.

## Agent Improvement Model

Library should invite contributors to improve the agents that help maintain, query, and extend the source-to-knowledge workflow.

Agents may eventually help with:

- creating source artifacts
- discovering candidate targets
- building and checking maps
- drafting briefs
- drafting books
- recording feedback
- finding missing evidence
- identifying unclear or unsupported claims
- explaining why an output changed over time
- helping maintainers navigate the console

Agent contributions should be judged by usefulness, traceability, clarity, and safety. An agent should make the library easier to understand and improve; it should not hide uncertainty, invent unsupported claims, or apply generated books without human approval.

Useful agent contributions may include prompt designs, workflow definitions, evaluation cases, test libraries, UI ideas, provider adapters, and examples of failed agent behavior that the project should learn from.

## Maturity Model

Targets may move through lifecycle stages:

```text
proposed -> accepted -> active -> stable -> contested -> revised -> replaced/deprecated
```

A target does not need to reach every stage. Some targets may only need a seed and a brief. Others may justify a full book.

The maturity model should be useful, not ceremonial.

## Public Contribution Model

This project should be designed in public.

Useful contributions may include:

- naming improvements
- simpler folder layouts
- better templates
- example libraries
- example books
- console design feedback
- agent workflow improvements
- agent evaluation examples
- accessibility feedback
- automation ideas
- documentation edits
- concerns about complexity

Contributors should feel welcome to challenge the design. The goal is not to preserve the first draft. The goal is to build a practical public library system that other people would actually use to make source-grounded knowledge.

## Questions For Contributors

1. Is "knowledge target" the clearest name for this pattern, or should the project use another term?
2. Are the proposed stages too many, too few, or just enough?
3. Should `briefs` and `books` be separate, or should they be one document type with different lengths?
4. What is the smallest useful version of this system?
5. What should the first console view be?
6. Should the console be included in this repo from the start, or should it remain a later package?
7. What file formats should be supported first: Markdown, YAML, JSON, or something else?
8. How should AI-generated content be labeled?
9. What makes a target mature enough to become a book?
10. What license and governance model would best support public reuse and contribution?
11. Which agent roles would be most useful first: source artifact, seed discovery, map drafting, brief drafting, book drafting, feedback recording, or console navigation?
12. What tests should an agent pass before its book output is trusted by maintainers?

## First Implementation Proposal

The first implementation should stay small:

1. Define templates for sources, artifacts, seeds, targets, maps, briefs, books, and feedback.
2. Add one complete example target with neutral sample content.
3. Add validation for required fields and broken links.
4. Build a read-only console that can browse the example target.
5. Add agent-assisted book drafting only after the file model is clear.

This order keeps the project understandable while giving contributors something concrete to test.

## Open Design Principle

Library should be built with enough structure to be useful and enough humility to change.

The design is intentionally unfinished. Public feedback is part of the architecture.
