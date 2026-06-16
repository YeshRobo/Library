# Library

Library is a source-grounded knowledge library for turning raw project material into organized, traceable, need-based knowledge outputs.

The current milestone is `v1-knowledge-library`: a file-based knowledge-target structure, public templates, one neutral example target, and a local validation CLI.

## What It Provides

- `library/knowledge/01_sources/` for raw or lightly processed source material
- `library/knowledge/02_artifacts/` for compact source-derived draft artifacts
- `library/knowledge/03_seeds/` for proposed knowledge targets
- `library/knowledge/04_targets/` for accepted target routing pages
- `library/knowledge/05_maps/` for source-and-artifact membership by target
- `library/knowledge/06_briefs/` for compact synthesis
- `library/knowledge/07_books/` for optional long-form treatment
- `library/knowledge/08_feedback/` for use feedback, contradictions, and revision triggers
- `library/templates/` for creating new knowledge surfaces

The numeric prefixes keep the folders sorted in source-to-book order in file browsers and simple directory listings.

## Validate The Library

Run validation from the repository root:

```bash
PYTHONPATH=src python3 -m library_cli validate .
```

Expected result:

```text
Library validation passed.
```

Run the test suite:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Run The Source Artifact Agent

Preview draft source artifacts without writing files:

```bash
PYTHONPATH=src python3 -m library_cli source-artifact library/knowledge/01_sources/project_release_notes_source.md
```

Write draft artifacts and a local run record:

```bash
PYTHONPATH=src python3 -m library_cli source-artifact library/knowledge/01_sources/project_release_notes_source.md --write
```

Draft artifacts are written under `library/knowledge/02_artifacts/`. Run records are written under `runs/`, which is local by default. Generated artifacts still require human approval before they become accepted library content.

Artifacts are meant to be smaller than their sources so humans and language models can load multiple source packets in one working context while preserving links back to the original files.

## Run The Read-Only Console

Install the backend console extra and start the API from the repository root:

```bash
python3 -m pip install -e ".[console]"
LIBRARY_REPO_ROOT=. uvicorn library_console.api.app:app --reload
```

Start the frontend in a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend reads the local API at `http://127.0.0.1:8000` by default. Set `VITE_LIBRARY_API_URL` before `npm run dev` to point it at another API host.

## Install Locally

For editable local development:

```bash
python3 -m pip install -e .
library-cli validate .
```

## Build Path

The file-based source-to-book model is the foundation. The read-only console and Source Artifact Agent are early surfaces built around that file model.

See `DESIGN.md` for the public design and open contribution questions.
