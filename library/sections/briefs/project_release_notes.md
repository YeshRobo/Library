# Brief: Project Release Notes

## Scope

This brief explains how a project can organize release note knowledge before a maintainer writes a final release announcement.

## Sources

- `library/sources/project_release_notes_source.md`

## Current Understanding

Release notes become more useful when source material is staged instead of collapsed directly into announcement text. The source notes show three durable needs: separate user-visible changes from internal maintenance, preserve evidence for each change, and give maintainers a compact synthesis before final writing.

The section-library model supports that by keeping raw notes in `sources`, section identity in `seeds` and `index`, evidence membership in `maps`, compact synthesis in `briefs`, and long-form treatment in `books`.

## Constraints And Tensions

- Maintainers need a compact view, but the compact view must still point back to source material.
- Larger releases may justify a book, while smaller releases may only need a brief.

## Next Use

Use this brief to draft the release notes book and to shape future console views for source traceability.
