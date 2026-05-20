# Library

Library is a source-grounded section library for turning raw project material into organized, traceable, topic-centered knowledge.

The current milestone is `v0-file-library`: a file-based library structure, public templates, one neutral example section, and a local validation CLI.

## What It Provides

- `library/sources/` for raw or lightly processed source material
- `library/sections/seeds/` for proposed section identities
- `library/sections/index/` for routing pages
- `library/sections/maps/` for source-to-section membership
- `library/sections/briefs/` for compact synthesis
- `library/sections/guides/` for optional long-form treatment
- `library/reviews/` for proposed changes and disputes
- `library/decisions/` for accepted direction
- `library/templates/` for creating new section surfaces

## Validate The Library

Run validation from the repository root:

```bash
PYTHONPATH=src python3 -m library_cli validate .
```

Expected result:

```text
Library validation passed.
```

Run the v0 test suite:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Install Locally

For editable local development:

```bash
python3 -m pip install -e .
section-library validate .
```

## Build Direction

The file-based library model comes first. A read-only console and agent proposal workflows will be built after the library model is concrete and validated.

See `DESIGN.md` for the public design and open contribution questions.
