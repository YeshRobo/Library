# Guide: Project Release Notes

## Scope

This guide explains a small section-library workflow for release notes. It is intentionally neutral and compact so it can serve as the first public example of the Library model.

## Reading Map

- Expands `library/sections/briefs/project_release_notes.md`.
- Anchored by `library/sources/project_release_notes_source.md`.
- Intended for maintainers and contributors who need a repeatable way to collect release note knowledge before final publication.

## Sources

- `library/sources/project_release_notes_source.md`

## Questions

- How should a project preserve release note evidence before publishing final announcement text?
- How can contributors propose entries without making those entries accepted by default?

## Detailed Synthesis

Release notes often start as scattered fragments: commit messages, pull request notes, issue comments, maintainer reminders, and local release planning notes. The problem is not only writing the final announcement. The deeper problem is preserving the path from source material to accepted release knowledge.

The section-library workflow separates that path into stages. Source notes preserve the original material. A section seed names the concern before the project overbuilds around it. A section index gives readers a routing page. A source map explains which files belong to the section and why. A brief captures the current understanding. A guide is added only when the topic needs long-form treatment.

For release notes, this staging keeps contributor proposals useful without treating every proposal as final. A contributor can add or suggest source material. A maintainer can map that material to the release note section. The brief can summarize the release-note implications. The final announcement can then be written from grounded, reviewed material rather than memory.

## Evidence And Traceability

- The source note states that release notes are scattered across commit messages, issue comments, and local notes.
- The source note identifies the need to separate user-visible changes from internal maintenance.
- The source note identifies contributor proposals and maintainer briefs as distinct needs.
- The recommendation to stage source, map, brief, and guide surfaces is an inference from the Library model applied to the source note.

## Constraints And Tensions

- The workflow must be light enough that maintainers will actually use it.
- The workflow must not hide rejected or postponed release note entries.
- The final release announcement should remain a maintainer decision, not an automatic output of source gathering.

## Open Questions

- Should release note proposals live under `library/reviews/` or under a dedicated future release workflow?
- Should the validation CLI eventually check that every accepted release note has source evidence?
- What metadata is needed for release notes across multiple versions?

## Next Use

Use this guide to design review proposals for release note entries and to test the future read-only console's section detail view.
