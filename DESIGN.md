# Library Design

## Purpose

Library is a source-grounded section library for turning raw project material into organized, traceable books.

The project starts with one simple idea: useful books should not appear from nowhere. They should grow from sources, section seeds, source maps, and compact briefs before becoming long-form readable knowledge.

This repository begins with a file-based model on purpose. The first public goal is to make the source-to-book workflow clear before the console or agent workflows become larger.

## Project Origin

Library will be built from lessons learned in UM2M, an earlier internal project that explored source-grounded knowledge organization, staged synthesis, agent-assisted workflows, and console-driven navigation.

The public project should not require users to understand UM2M. UM2M is the starting prototype and learning source; Library is the standalone community version. Public contributors should feel free to simplify, rename, challenge, or replace inherited ideas when a clearer source-to-book design emerges.

## Design Goals

Library should be:

- easy to understand without special terminology
- useful for small projects and large knowledge bases
- source-grounded, with clear traceability back to original material
- focused on producing readable books from organized library material
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

## Core Idea

Library organizes knowledge through a staged flow:

```text
sources -> section seeds -> section indexes -> source maps -> briefs -> books
```

Each stage has a different job.

`sources` preserve raw or lightly processed material.

`section seeds` identify topics that may deserve organized treatment.

`section indexes` route readers to the surfaces for one section.

`source maps` gather the files that support a section and explain why each file belongs.

`briefs` summarize what is currently understood about a section.

`books` expand mature sections into long-form, readable knowledge.

The stages are deliberately separate. A source is not a book. A seed is not a brief. A brief is not automatically a complete book. This separation keeps knowledge traceable and lets books mature from grounded material.

## Proposed Repository Shape

The file-based core uses this shape:

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
      books/
    templates/
  src/
  tests/
```

Future console and agent code should serve this model rather than replace it.

## Library Components

### Sources

Sources are the raw inputs to the library. They may include notes, reports, transcripts, issue summaries, research excerpts, design sketches, audit results, or other source material.

A source should preserve context rather than rewrite it too aggressively. The goal is to keep later briefs and books traceable.

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
- Which source maps, briefs, books, and source files belong to it?
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

### Books

A book is an optional long-form treatment of a mature section.

A good book answers:

- What is the complete topic narrative?
- How do the sources relate to each other?
- What patterns, constraints, and tradeoffs appear?
- What does the reader need to know before acting on this topic?
- What questions remain open?

Books are deep knowledge surfaces. They should remain source-grounded and should clearly mark inference when the source material does not directly state a claim.

## Console Concept

Library should eventually include its own console.

The console should be a practical interface for browsing, querying, and building section books. It should not replace the file-based structure. The files remain the durable project surface; the console makes that surface easier to use.

The console may include:

- a section browser
- source traceability views
- brief and book readers
- maturity indicators
- search and query tools
- provider adapters for AI-assisted book workflows
- run records for generated outputs

The console should be data-driven. Project-specific behavior should live in configuration, not hardcoded assumptions.

## Automation Model

Automation should support the library without taking ownership away from maintainers.

Possible automation:

- propose section seeds from new source material
- detect source files that may belong to existing sections
- draft source maps
- draft briefs from mapped sources
- expand mature briefs into book drafts
- compare briefs and books against source evidence
- identify stale or unsupported book claims
- generate run records for AI-assisted work

Automation should always preserve traceability. If a tool writes or proposes content, readers should be able to see what source material was used and what generation state the output is in.

## Agent Improvement Model

Library should invite contributors to improve the agents that help maintain, query, and extend the source-to-book workflow.

Agents may eventually help with:

- discovering candidate sections from source material
- building and checking source maps
- drafting briefs
- drafting books
- finding missing evidence
- identifying unclear or unsupported claims
- explaining why a book changed over time
- helping maintainers navigate the console

Agent contributions should be judged by usefulness, traceability, clarity, and safety. An agent should make the library easier to understand and improve; it should not hide uncertainty, invent unsupported claims, or apply generated books without human approval.

Useful agent contributions may include prompt designs, workflow definitions, evaluation cases, test libraries, UI ideas, provider adapters, and examples of failed agent behavior that the project should learn from.

## Maturity Model

Sections may move through maturity levels:

```text
seeded -> indexed -> mapped -> briefed -> booked
```

A section does not need to reach every level. Some topics may only need a seed and a brief. Others may justify a full book.

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

Contributors should feel welcome to challenge the design. The goal is not to preserve the first draft. The goal is to build a practical public library system that other people would actually use to make books from source-grounded knowledge.

## Questions For Contributors

1. Is "section library" the clearest name for this pattern, or should the project use another term?
2. Are the proposed stages too many, too few, or just enough?
3. Should `briefs` and `books` be separate, or should they be one document type with different lengths?
4. What is the smallest useful version of this system?
5. What should the first console view be?
6. Should the console be included in this repo from the start, or should it remain a later package?
7. What file formats should be supported first: Markdown, YAML, JSON, or something else?
8. How should AI-generated book content be labeled?
9. What makes a section mature enough to become a book?
10. What license and governance model would best support public reuse and contribution?
11. Which agent roles would be most useful first: section discovery, source mapping, brief drafting, book drafting, or console navigation?
12. What tests should an agent pass before its book output is trusted by maintainers?

## First Implementation Proposal

The first implementation should stay small:

1. Define templates for seeds, indexes, maps, briefs, and books.
2. Add one complete example library with neutral sample content.
3. Add validation for required fields and broken links.
4. Build a read-only console that can browse the example library.
5. Add agent-assisted book drafting only after the file model is clear.

This order keeps the project understandable while giving contributors something concrete to test.

## Open Design Principle

Library should be built with enough structure to be useful and enough humility to change.

The design is intentionally unfinished. Public feedback is part of the architecture.
