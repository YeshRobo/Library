# Library Knowledge Architecture

## 1. Core Purpose

Library is a system for turning scattered source material into useful, traceable, revisable knowledge outputs.

The main problem Library solves is not simply file storage. The problem is that useful knowledge for a task is often scattered across many different source files. A single answer, explanation, guide, or book may require pieces from multiple sources. If those pieces remain isolated, an AI agent or human reader must repeatedly search through raw material, re-read context, and reconstruct the same understanding again and again.

Library exists to prevent that waste.

It collects raw source material, converts each source into an AI-readable artifact, creates need-based seed proposals, maps relevant evidence, and produces compact or long-form knowledge outputs. These outputs remain traceable back to the sources that shaped them, and they remain revisable as new evidence, use cases, conflicts, and reality checks appear.

A simple description:

```text
Library converts scattered source material into need-based knowledge products.
```

A more complete description:

```text
Library is a multi-agent, source-grounded, need-driven knowledge system that learns toward truth through repeated use, feedback, contradiction, and revision.
```

## 2. What Library Is Not

Library is not a normal folder of notes.

Library is not only an encyclopedia.

Library is not a fixed topic hierarchy.

Library is not a system where one source file becomes one final book.

Library is also not a system where one AI reads everything once and declares final truth.

The Library assumes:

- sources are incomplete
- AI agents have bias
- different models notice different things
- knowledge needs change depending on the task
- useful answers may combine many kinds of knowledge
- a small set of sources can produce many different outputs
- current knowledge can later be disproven, refined, replaced, or split
- truth is approached over time, not declared upfront

## 3. Core Philosophy

### 3.1 Knowledge Is Need-Based

Knowledge should be retrieved and organized based on the need of the agent or user.

A knowledge output is created because someone or something needs it:

- a user asks a question
- an agent needs context for a task
- multiple artifacts reveal a recurring pattern
- a contradiction needs investigation
- an underused idea deserves exploration
- an existing knowledge output needs refinement
- a book or guide is needed for repeated future use

This means the Library should not start by assuming a perfect topic structure. It should allow topics, books, briefs, guides, and other knowledge units to emerge from actual needs.

### 3.2 One Source Pool Can Produce Many Knowledge Outputs

A few source files can support many different outputs.

For example:

```text
5 source files
↓
10 books, briefs, guides, or knowledge units
```

This is because each output may be asking a different question of the same material.

The same artifact may support:

- a practical guide
- a theoretical explanation
- a conflict analysis
- a character design brief
- a worldbuilding book
- an agent instruction document
- a glossary
- a decision record
- a skeptical review
- a future research seed

So the Library should avoid thinking in terms of one fixed “section” per topic. A better abstraction is a **knowledge target** or **knowledge output**.

### 3.3 Knowledge Is a Combination

Any particular knowledge output may combine several kinds of knowledge.

For example, to answer one question, an agent may need:

- definitions
- examples
- source evidence
- constraints
- design intent
- historical decisions
- contradictions
- usage patterns
- agent instructions
- open questions

These may be scattered across many files. Library consolidates them into one usable place.

### 3.4 Truth Is Provisional Confidence

Library should not treat any AI output, book, or brief as absolute truth.

A better rule:

```text
Repeated support and successful use increase confidence, not certainty.
```

Knowledge becomes more reliable when:

- many artifacts support it
- different agents independently rediscover it
- multiple tasks successfully use it
- later outputs cite or depend on it
- reality checks do not break it
- contradictions are addressed
- revisions improve it over time

But even highly trusted knowledge remains revisable.

A book in Library should mean:

```text
This is the current best consolidated understanding for this need, based on available sources, evidence, use, and revision history.
```

It should not mean:

```text
This is final truth.
```

### 3.5 Bias Is Not Only a Problem

Bias can be dangerous when it is hidden and singular.

But bias can also help the Library approach truth when it is visible, diverse, and tested.

Different models and agents notice different things. Gemini, OpenAI, Claude, local models, and other systems may prioritize different patterns because their training, alignment, reasoning style, and defaults differ. Even within the same model, different agent roles will notice different things.

Library should not pretend there is one neutral AI viewpoint.

Instead, it should use multiple biased perspectives intentionally.

The key principle:

```text
Truth is approached not by removing all bias, but by exposing many biases and testing their outputs against evidence, use, contradiction, and reality.
```

## 4. Main Objects in the Library

The Library can be built around these core objects:

```text
Sources → Artifacts → Seeds → Knowledge Targets → Maps → Briefs → Books → Feedback
```

The old model used “sections,” but “section” may be too rigid. The better model is based on **knowledge targets** or **knowledge units**.

A knowledge target is a need-based object: a thing the Library may consolidate knowledge around.

It may become:

- a brief
- a book
- a guide
- a reference page
- a concept packet
- a workflow document
- an answer packet
- an agent instruction packet
- a research note
- a comparison document

## 5. Layer 01: Sources

### Purpose

Sources preserve raw or lightly processed material before Library decides what the material means.

This layer answers:

- What did the project collect?
- Where did later claims, questions, or ideas come from?
- What original context should be preserved?
- What should remain available for audit and review?

Sources may be messy, duplicated, incomplete, or unorganized. That is acceptable. Their job is preservation, not synthesis.

### Rule

Sources should not be overwritten by interpretation.

They are the original evidence pool.

### Examples

Sources may include:

- raw notes
- pasted conversations
- design documents
- PDFs
- transcripts
- code files
- worldbuilding notes
- research papers
- extracted text from images
- meeting notes
- prompt drafts
- old versions of files

### Suggested Metadata

Each source can track:

```markdown
# Source: <source name>

## Source ID

## Source Type

## Created / Imported Date

## Origin

Where this source came from.

## Raw Material

The original content or a pointer to it.

## Processing Notes

Any notes about formatting, cleanup, extraction, or uncertainty.
```

## 6. Layer 02: Artifacts

### Purpose

Artifacts are structured, AI-readable representations of individual source files.

The rule is:

```text
One source file → one artifact file
```

An artifact exists because raw sources may be too long, messy, or difficult for an AI agent to use directly. The artifact compresses and structures one source so that agents can load many artifacts into context without loading every raw source.

### What an Artifact Does

An artifact answers:

- What is this one source about?
- What important material does it contain?
- What claims, facts, questions, entities, terms, and patterns appear?
- What future knowledge outputs might this source support?
- What uncertainty or limitation should remain visible?
- Where does this artifact trace back to?

### Important Boundary

An artifact is not accepted knowledge.

It is not a final answer.

It is a source-level working representation.

### Suggested Artifact Structure

```markdown
# Artifact: <artifact name>

## Source Link

Original source file:

## Artifact Purpose

Why this artifact exists.

## Source Summary

Compact summary of the source.

## Key Extracted Points

- Point 1
- Point 2
- Point 3

## Important Terms / Entities

- Term or entity — meaning in this source

## Possible Knowledge Uses

What future needs, books, briefs, or knowledge targets this source may support.

## Questions Raised

Questions the source creates or leaves unresolved.

## Contradictions / Tensions

Anything that conflicts internally or with known Library material.

## Evidence Notes

Specific details that may matter later.

## Confidence / Limitations

How reliable, complete, or ambiguous this artifact is.
```

## 7. Layer 03: Seeds

### Purpose

Seeds are proposed knowledge targets.

A seed says:

```text
This may be a useful knowledge object worth creating.
```

A seed does not have to come only from artifact review. It can be created from many triggers:

- an AI reviews multiple artifacts and notices a pattern
- a user asks a question
- an agent needs context for a task
- a maintainer notices a recurring issue
- a conflict appears between sources
- an underused idea looks promising
- an existing brief or book exposes a gap

### Seeds Are Need-Based

A seed should not be defined only as a “topic.”

A better definition:

```text
A seed is a proposed knowledge target created because a need, pattern, question, or perspective suggests that some scattered knowledge should be consolidated.
```

### Seeds Can Have Multiple Origins

A seed may originate from:

- multiple artifacts
- one query
- multiple queries
- artifact review plus user request
- one agent’s task failure
- repeated use of related knowledge
- a model-specific discovery

So the seed should support multiple origin records.

### Suggested Seed Structure

```markdown
# Seed: <seed name>

## Proposed Knowledge Target

What knowledge object may need to be created?

## Seed Trigger

What caused this seed to be proposed?

## Origins

- Type: artifact review
  Items:
  - artifact_001.md
  - artifact_004.md
  Reason: These artifacts point toward the same knowledge need.

- Type: user query
  Items:
  - "<query text>"
  Reason: The query revealed a need for consolidated knowledge.

## Why This Matters

Why this seed may be useful.

## Intended Use

What task, question, or future agent need this knowledge would support.

## Supporting Artifacts

Artifacts that currently appear relevant.

## Possible Output Type

- brief
- book
- guide
- reference
- agent packet
- comparison
- research note

## Proposed Scope

What this knowledge target should include.

## Exclusions

What should not be included.

## Open Questions

What needs clarification.

## Created By

Model:
Agent role:
Prompt / task:
Date:

## Bias / Lens

What perspective shaped this seed?

## Status

weak / promising / strong / accepted / rejected / merged
```

## 8. Layer 04: Knowledge Targets / Index

### Purpose

Once a seed is accepted, it becomes a registered knowledge target.

This replaces the older idea of an accepted “section.”

A knowledge target is the Library’s way of saying:

```text
This need is worth organizing around.
```

The index is the navigation and identity page for that target.

It answers:

- What is this knowledge target?
- What need does it serve?
- What stage is it in?
- Which maps, briefs, books, and feedback records belong to it?
- Where should a human or agent go next?

### Why This Layer Exists

Seeds are proposals.

Knowledge targets are accepted work areas.

The index prevents confusion by giving each accepted target a stable identity.

### Suggested Index Structure

```markdown
# Knowledge Target Index: <name>

## Target ID

## Current Name

## Purpose

What need this target serves.

## Accepted From Seeds

- seed_001.md
- seed_017.md

## Current Status

proposed / active / stable / contested / deprecated / replaced

## Output Types

- brief
- book
- guide
- reference

## Active Map

Link to current map.

## Current Brief

Link to latest brief.

## Current Book

Link to latest book, if one exists.

## Related Targets

Other targets that overlap or conflict.

## Revision History

Major changes to this target.

## Notes for Agents

How agents should use this target.
```

## 9. Layer 05: Maps

### Purpose

Maps gather evidence and explain why sources or artifacts belong to a knowledge target.

If artifacts are source-level representations, maps are target-level evidence membership.

A map answers:

- Which artifacts support this knowledge target?
- What role does each artifact play?
- Which sources are primary evidence?
- Which are secondary context?
- Which are related but out of scope?
- Which artifacts conflict?
- How does one artifact support multiple outputs?

### Why Maps Matter

Without maps, briefs and books may cite a vague pile of material.

Maps make the evidence trail explicit.

They help an agent understand not only what files are relevant, but why they are relevant.

### Suggested Map Structure

```markdown
# Map: <knowledge target name>

## Target Link

## Map Purpose

What this map organizes.

## Primary Artifacts

- artifact_001.md
  Role: primary evidence
  Why it matters:
  Key fragments:

- artifact_002.md
  Role: primary evidence
  Why it matters:
  Key fragments:

## Secondary Artifacts

Artifacts useful for context but not central.

## Related but Out of Scope

Artifacts that are nearby but should not shape this output unless scope changes.

## Conflicting Evidence

Artifacts or source points that disagree.

## Missing Evidence

What evidence would strengthen this target.

## Reuse Links

Other knowledge targets that use the same artifacts.

## Map Confidence

low / medium / high

## Last Reviewed
```

## 10. Layer 06: Briefs

### Purpose

Briefs are compact knowledge outputs.

A brief is the current short answer to the knowledge target.

It should be small enough for retrieval and agent use, but grounded enough to support future work.

A brief answers:

- What does the Library currently understand about this knowledge target?
- What evidence supports that understanding?
- What constraints or tensions matter?
- What is uncertain?
- What should an agent know before acting?

### Why Briefs Are Important

Most knowledge targets should not need a full book immediately.

A brief can be useful earlier.

It lets the Library become useful before everything is mature.

### Suggested Brief Structure

```markdown
# Brief: <knowledge target name>

## Target Link

## Current Answer

The compact answer or synthesis.

## Key Points

- Point 1
- Point 2
- Point 3

## Evidence Base

Main artifacts or map entries used.

## Important Constraints

What limits or shapes this knowledge.

## Tensions / Conflicts

Where the evidence disagrees or remains uncertain.

## Use Guidance

How an agent should use this brief.

## Do Not Assume

Things the brief does not prove.

## Confidence

low / medium / high, with reason.

## Next Reading

Map, book, related targets, or source artifacts.
```

## 11. Layer 07: Books

### Purpose

Books are long-form treatments of mature knowledge targets.

A book is optional.

Not every knowledge target needs one.

A book answers:

- What is the complete readable treatment of this target?
- How do the sources, artifacts, map, and brief fit together?
- What patterns, tradeoffs, and open questions should a reader understand?
- What claims are grounded in source material?
- What claims are inference?
- What remains uncertain?

### Important Rule

A book is not final truth.

It is the current best long-form synthesis.

It should remain revisable.

### Suggested Book Structure

```markdown
# Book: <knowledge target name>

## Book Purpose

Why this book exists and what need it serves.

## Reader / Agent Use Case

Who should use this book and for what.

## Core Thesis

The main current understanding.

## Background

Important context.

## Main Explanation

Long-form synthesis.

## Evidence Trail

How the book depends on maps, artifacts, and sources.

## Patterns

Repeated ideas or structures found across evidence.

## Tradeoffs

Competing interpretations or design choices.

## Open Questions

What is still unresolved.

## Confidence and Limits

What is strong, weak, contested, or speculative.

## Revision Notes

How this book may need to change later.
```

## 12. Layer 08: Feedback / Usage / Reality Testing

### Purpose

If Library learns toward truth through use, then usage and feedback need their own layer.

This layer tracks how knowledge outputs perform when agents or users use them.

It answers:

- Which knowledge outputs were used?
- For what task?
- Did they help?
- Did they fail?
- Were they cited by later outputs?
- Were they contradicted?
- Were they replaced?
- Which agents agreed or disagreed?

### Why This Layer Matters

Without feedback, Library is only a writing system.

With feedback, Library becomes a learning system.

This is where the reinforcement-learning-like truth process happens.

A knowledge output is proposed, used, tested, rewarded, weakened, revised, or replaced.

### Suggested Feedback Structure

```markdown
# Feedback Record: <target or output name>

## Knowledge Output Used

Brief/book/guide/reference used.

## Used By

User, agent, model, or workflow.

## Task / Need

What the knowledge was used for.

## Result

helpful / partially helpful / failed / contradicted / unclear

## Evidence of Success or Failure

What happened?

## Required Revision

What should change?

## Confidence Impact

increase / decrease / no change

## Related Outputs Affected

Other briefs, books, or targets that may need review.

## Date
```

## 13. Multi-Agent Knowledge Discovery

As the Library grows, a single LLM cannot understand the whole context. Even if retrieval helps, one model will still bring one model-specific bias.

So Library should use multiple agents with different biases.

This is not a weakness. It is part of the design.

Different agents can inspect the same artifacts and propose different seeds or revisions.

### Useful Agent Types

#### 13.1 Pattern Finder

Looks for repeated ideas across many artifacts.

Good for discovering central knowledge.

Risk: may over-prioritize common ideas and miss rare but important ones.

#### 13.2 Novelty Seeker

Looks for underused, under-cited, or ignored knowledge.

Good for creating new knowledge outputs.

Risk: may chase weak or irrelevant fragments.

#### 13.3 Skeptic

Looks for contradictions, unsupported claims, and overconfident synthesis.

Good for improving truth quality.

Risk: may block useful provisional knowledge if too strict.

#### 13.4 Task Agent

Creates or requests knowledge based on an immediate task.

Good for need-based retrieval.

Risk: may create narrow outputs that do not generalize.

#### 13.5 Historian

Tracks how an idea changed over time.

Good for versioned knowledge and decision history.

Risk: may over-focus on chronology rather than current usefulness.

#### 13.6 Mapper

Connects artifacts to knowledge targets.

Good for traceability.

Risk: may create too much process overhead.

#### 13.7 Synthesizer

Turns maps and briefs into readable knowledge outputs.

Good for books and guides.

Risk: may smooth over contradictions too much.

#### 13.8 Refiner

Updates existing outputs with new evidence and feedback.

Good for maintenance.

Risk: may preserve old structures when replacement would be better.

### Agent Provenance

Every AI-created seed, map, brief, or book should record:

```markdown
## Created By

Model family:
Model version:
Agent role:
Prompt / task:
Date:

## Bias / Lens

What this agent was optimized to notice.

## Known Limitations

What this agent may miss.
```

This helps future agents interpret the output as a perspective, not as neutral truth.

## 14. Confidence Model

Library should track confidence as a profile, not as a single absolute number.

A knowledge output can have different kinds of strength:

- evidence strength
- reuse strength
- agent consensus
- reality-test success
- contradiction level
- maturity
- freshness

### Suggested Confidence Profile

```markdown
# Confidence Profile

## Evidence Support

How many sources/artifacts support this?

## Source Diversity

Does support come from different kinds of sources or only one cluster?

## Reuse Count

How often has this knowledge been used?

## Successful Use Cases

Where did this knowledge help?

## Failed Use Cases

Where did it fail or mislead?

## Independent Rediscovery

Did different agents/models propose similar knowledge?

## Conflict Level

none / low / medium / high

## Current Confidence

low / medium / high

## Status

provisional / active / stable / contested / deprecated / replaced
```

### Confidence Principle

```text
Confidence grows through evidence, reuse, independent rediscovery, and successful reality testing.
Confidence weakens through contradiction, failed use, stale evidence, or stronger replacement.
```

## 15. Knowledge Lifecycle

A knowledge target or output should move through stages.

Suggested lifecycle:

```text
proposed → accepted → active → stable → contested → revised → replaced/deprecated
```

### Proposed

A seed exists, but the Library has not accepted it as a target yet.

### Accepted

The seed becomes a knowledge target.

### Active

Maps, briefs, or books are being created.

### Stable

The knowledge is repeatedly useful and has no major unresolved conflict.

### Contested

New evidence, agent disagreement, or failed use challenges the knowledge.

### Revised

The output is updated to handle new evidence or feedback.

### Replaced / Deprecated

A better knowledge output replaces the old one, but the old one may remain for history and traceability.

## 16. Suggested Folder Structure

The current structure is:

```text
library/knowledge/
01_sources
02_artifacts
03_seeds
04_index
05_maps
06_briefs
07_books
```

Because “sections” may be too rigid, consider changing to:

```text
library/
01_sources/
02_artifacts/
03_seeds/
04_targets/
05_maps/
06_briefs/
07_books/
08_feedback/
```

Or:

```text
library/knowledge/
01_sources/
02_artifacts/
03_seeds/
04_targets/
05_maps/
06_briefs/
07_books/
08_feedback/
```

### Why This Is Better

- `sources` preserve raw material
- `artifacts` make each source AI-readable
- `seeds` propose possible knowledge targets
- `targets` register accepted needs
- `maps` connect evidence to targets
- `briefs` provide compact usable knowledge
- `books` provide mature long-form synthesis
- `feedback` tracks use, failure, revision, and confidence

## 17. Full Flow Example

### Step 1: Source Collection

The user imports five source files:

```text
source_a.md
source_b.md
source_c.md
source_d.md
source_e.md
```

### Step 2: Artifact Creation

Each source creates one artifact:

```text
source_a.md → artifact_a.md
source_b.md → artifact_b.md
source_c.md → artifact_c.md
source_d.md → artifact_d.md
source_e.md → artifact_e.md
```

### Step 3: Seed Creation

Different agents read the artifacts.

Pattern Finder proposes:

```text
seed_001: repeated concept across artifacts A, B, C
```

Novelty Seeker proposes:

```text
seed_002: overlooked idea in artifacts D and E
```

Task Agent proposes:

```text
seed_003: knowledge needed to answer a user query
```

Skeptic proposes:

```text
seed_004: contradiction between artifacts B and D
```

### Step 4: Target Acceptance

Maintainer or agent accepts some seeds as knowledge targets:

```text
target_001
target_002
target_003
```

### Step 5: Mapping

Each target gets a map explaining which artifacts matter and why.

### Step 6: Brief Creation

Each target may get a brief:

```text
brief_001 = compact answer for target_001
brief_002 = compact answer for target_002
```

### Step 7: Book Creation

Only mature targets get books:

```text
book_001 = long-form treatment of target_001
```

### Step 8: Feedback

Agents use the briefs/books in real tasks.

Feedback updates confidence and may trigger revision.

## 18. Key Rules for Building Library

### Rule 1: Preserve Sources

Never destroy the original evidence.

### Rule 2: One Source, One Artifact

Every source should have one structured artifact.

### Rule 3: Seeds Are Proposals, Not Truth

A seed is a possible knowledge target, not an accepted fact.

### Rule 4: Knowledge Is Need-Based

Create seeds and outputs based on actual needs, not only predefined topics.

### Rule 5: One Artifact Can Support Many Outputs

Do not force a source into only one category.

### Rule 6: Track Bias

Every AI-created output should record model, role, prompt, and lens.

### Rule 7: Use Multiple Agents

Different biases reveal different knowledge.

### Rule 8: Confidence Is Provisional

Repeated use increases confidence, not certainty.

### Rule 9: Feedback Is Part of Knowledge

Usage, failure, and contradiction must feed back into the system.

### Rule 10: Books Are Optional

Briefs may be enough for many knowledge targets.

## 19. Recommended Minimal Version

To start simply, build only five things first:

```text
01_sources
02_artifacts
03_seeds
04_targets
06_briefs
```

Then add maps and feedback once the system grows.

But if traceability matters from the beginning, use:

```text
01_sources
02_artifacts
03_seeds
04_targets
05_maps
06_briefs
```

Add books only when a brief becomes mature enough for long-form treatment.

Add feedback as soon as agents start using knowledge outputs repeatedly.

## 20. Final Definition

Library is a need-based knowledge consolidation system.

It starts with scattered sources, converts each source into an AI-readable artifact, uses diverse biased agents and user needs to propose seeds, accepts useful seeds as knowledge targets, maps evidence to those targets, produces compact briefs and optional books, and then updates confidence through repeated use, contradiction, feedback, and reality testing.

Library does not claim absolute truth.

It learns toward truth.

Its strength comes from preserving evidence, exposing bias, comparing perspectives, consolidating scattered knowledge, and revising outputs when reality pushes back.

