# Library Design

## Purpose

Library is a source-grounded section library for turning raw project material into organized, traceable, topic-centered knowledge.

The project starts with one simple idea: useful knowledge should move through clear stages before it becomes guidance, documentation, or implementation work. Library provides those stages as a reusable structure that other projects can adopt, adapt, and improve.

This repository begins as design-only on purpose. The first public goal is to invite feedback on the model before code, templates, or automation harden too early.

## Project Origin

Library will be built from lessons learned in UM2M, an earlier internal project that explored source-grounded knowledge organization, staged review, agent-assisted workflows, and console-driven navigation.

The public project should not require users to understand UM2M. UM2M is the starting prototype and learning source; Library is the standalone community version. Public contributors should feel free to simplify, rename, challenge, or replace inherited ideas when a clearer design emerges.

## Design Goals

Library should be:

- easy to understand without special terminology
- useful for small projects and large knowledge bases
- source-grounded, with clear traceability back to original material
- friendly to human readers and AI-assisted workflows
- structured enough to support automation
- flexible enough to support different domains
- public, practical, and community-improvable

Library should avoid:

- hidden framework assumptions
- project-specific vocabulary
- binding claims that cannot be traced to source material
- forcing every project into the same folder layout before the pattern is proven
- turning early notes directly into final decisions

## Core Idea

Library organizes knowledge through a staged flow:

```text
sources -> sections -> briefs -> guides -> decisions
```

Each stage has a different job.

`sources` preserve raw or lightly processed material.

`sections` identify stable topics and gather related source material.

`briefs` summarize what is currently understood about a section.

`guides` expand mature sections into long-form, readable knowledge.

`decisions` capture accepted direction, policy, or implementation intent after review.

The stages are deliberately separate. A source is not a decision. A brief is not a final guide. A guide is not automatically project policy. This separation keeps knowledge useful without making it prematurely authoritative.

## Proposed Repository Shape

The future repository may grow into this shape:

```text
Library/
  DESIGN.md
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
  console/
    backend/
    frontend/
    catalog/
    runs/
  docs/
  tests/
```

This is a proposed shape, not a locked contract. The public discussion should decide what belongs in the first implementation.

## Library Components

### Sources

Sources are the raw inputs to the library. They may include notes, reports, transcripts, issue summaries, research excerpts, design sketches, audit results, or other source material.

A source should preserve context rather than rewrite it too aggressively. The goal is to keep later library work traceable.

### Section Seeds

A section seed proposes that a topic deserves organized treatment.

A good seed answers:

- What is the topic?
- Why does it deserve a section?
- Which source files support it?
- What questions should the section answer?
- What should remain out of scope?

Seeds are intentionally lightweight. They help avoid creating a full section before there is enough evidence that the topic matters.

### Section Index

A section index is the routing page for a topic.

A good index answers:

- What is this section about?
- Where did the section come from?
- Which briefs, guides, maps, and source files belong to it?
- What is the current maturity level of the section?

The index should be fast to scan. It should help humans and tools find the right material without reading the whole library.

### Source Maps

A source map gathers all files related to a section and explains why each file belongs.

A good source map answers:

- Which sources support this section?
- What does each source contribute?
- Which files are primary evidence?
- Which files are secondary context?
- Which files are related but out of scope?

A source may appear in more than one section when justified. The map should make that relationship visible instead of hiding it.

### Briefs

A brief is the required compact synthesis for a section.

A good brief answers:

- What do we currently understand?
- What evidence supports that understanding?
- What constraints or tensions matter?
- What remains uncertain?
- What should a reader consult next?

Briefs should be short enough to retrieve quickly and rich enough to preserve important distinctions.

### Guides

A guide is an optional long-form treatment of a mature section.

A good guide answers:

- What is the complete topic narrative?
- How do the sources relate to each other?
- What patterns, constraints, and tradeoffs appear?
- What does the reader need to know before acting on this topic?
- What questions remain open?

Guides should not turn into final policy by accident. They are deep knowledge surfaces, not automatic decisions.

### Reviews

Reviews capture proposed improvements, gaps, corrections, and disputes.

A good review answers:

- What is missing or unclear?
- Which section is affected?
- What source material supports the concern?
- What change is proposed?
- What should happen before acceptance?

Reviews make the library safer to improve in public because they separate suggested change from accepted change.

### Decisions

Decisions capture accepted direction after review.

A good decision answers:

- What has been accepted?
- Why was it accepted?
- Which sources, briefs, guides, or reviews support it?
- What changes because of this decision?
- What remains open?

Decisions should be explicit and traceable. The library should help teams understand not only what was decided, but why.

## Console Concept

Library should eventually include its own console.

The console should be a practical interface for browsing, querying, reviewing, and improving a section library. It should not replace the file-based structure. The files remain the durable project surface; the console makes that surface easier to use.

The console may include:

- a section browser
- source traceability views
- brief and guide readers
- review queues
- maturity indicators
- search and query tools
- provider adapters for AI-assisted workflows
- run records for generated or reviewed outputs

The console should be data-driven. Project-specific behavior should live in configuration, not hardcoded assumptions.

## Automation Model

Automation should support the library without taking ownership away from maintainers.

Possible automation:

- propose section seeds from new source material
- detect source files that may belong to existing sections
- draft briefs from mapped sources
- compare briefs against source evidence
- identify stale sections
- suggest review items
- generate run records for AI-assisted work

Automation should always preserve traceability. If a tool writes or proposes content, readers should be able to see what source material was used and what review state the output is in.

## Agent Improvement Model

Library should invite contributors to improve the agents that help maintain, query, review, and extend the library.

Agents may eventually help with:

- discovering candidate sections from source material
- building and checking source maps
- drafting briefs and guides
- finding missing evidence
- identifying unclear or unsupported claims
- preparing review items for humans
- explaining why a section changed over time
- helping maintainers navigate the console

Agent contributions should be judged by usefulness, traceability, clarity, and safety. An agent should make the library easier to understand and improve; it should not hide uncertainty, invent unsupported claims, or bypass human review.

Useful agent contributions may include prompt designs, workflow definitions, evaluation cases, test libraries, review protocols, UI ideas, provider adapters, and examples of failed agent behavior that the project should learn from.

## Maturity Model

Sections may move through maturity levels:

```text
seeded -> indexed -> mapped -> briefed -> guided -> decision-linked
```

A section does not need to reach every level. Some topics may only need a seed and a brief. Others may justify a full guide and decisions.

The maturity model should be useful, not ceremonial.

## Public Contribution Model

This project should be designed in public.

Useful contributions may include:

- naming improvements
- simpler folder layouts
- better templates
- example libraries
- console design feedback
- agent workflow improvements
- agent evaluation examples
- accessibility feedback
- automation ideas
- review workflow improvements
- documentation edits
- concerns about complexity

Contributors should feel welcome to challenge the design. The goal is not to preserve the first draft. The goal is to build a practical public library system that other people would actually use.

## Questions For Contributors

1. Is "section library" the clearest name for this pattern, or should the project use another term?
2. Are the proposed stages too many, too few, or just enough?
3. Should `briefs` and `guides` be separate, or should they be one document type with different lengths?
4. What is the smallest useful version of this system?
5. What should the first console view be?
6. Should the console be included in this repo from the start, or should it remain a later package?
7. What file formats should be supported first: Markdown, YAML, JSON, or something else?
8. How should AI-generated content be labeled and reviewed?
9. What makes a section mature enough to become a decision?
10. What license and governance model would best support public reuse and contribution?
11. Which agent roles would be most useful first: section discovery, source mapping, brief drafting, review support, or console navigation?
12. What tests should an agent pass before its output is trusted by maintainers?

## First Implementation Proposal

The first implementation should stay small:

1. Define templates for seeds, indexes, maps, briefs, guides, reviews, and decisions.
2. Add one complete example library with neutral sample content.
3. Build a read-only console that can browse the example library.
4. Add validation for required fields and broken links.
5. Add write workflows only after the read-only model is clear.

This order keeps the project understandable while giving contributors something concrete to test.

## Open Design Principle

Library should be built with enough structure to be useful and enough humility to change.

The design is intentionally unfinished. Public feedback is part of the architecture.
