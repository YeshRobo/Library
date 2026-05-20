# Book: Project Release Notes

## Scope

This book explains a small section-library workflow for release notes. It is intentionally neutral and compact so it can serve as the first public example of the Library model.

## Reading Map

- Expands `library/sections/briefs/project_release_notes.md`.
- Anchored by `library/sources/project_release_notes_source.md`.
- Intended for maintainers and contributors who need a repeatable way to collect release note knowledge before final publication.

## Sources

- `library/sources/project_release_notes_source.md`

## Questions

- How should a project preserve release note evidence before publishing final announcement text?
- How can scattered source notes become a reusable release notes book?

## Detailed Synthesis

Release notes often start as scattered fragments: commit messages, pull request notes, issue comments, maintainer reminders, and local release planning notes. The problem is not only writing the final announcement. The deeper problem is preserving the path from source material to reusable release knowledge.

The section-library workflow separates that path into stages. Source notes preserve the original material. A section seed names the concern before the project overbuilds around it. A section index gives readers a routing page. A source map explains which files belong to the section and why. A brief captures the current understanding. A book is added when the topic needs long-form treatment.

For release notes, this staging keeps the final announcement grounded without treating scattered notes as finished prose. A contributor can add source material. A maintainer can map that material to the release note section. The brief can summarize the release-note implications. The book can then explain the reusable release note workflow from grounded, mapped material.

## Evidence And Traceability

- The source note states that release notes are scattered across commit messages, issue comments, and local notes.
- The source note identifies the need to separate user-visible changes from internal maintenance.
- The source note identifies maintainer briefs as a distinct need.
- The recommendation to stage source, map, brief, and book surfaces is an inference from the Library model applied to the source note.

## Constraints And Tensions

- The workflow must be light enough that maintainers will actually use it.
- The workflow must preserve source evidence instead of producing unsupported announcement text.
- The final release announcement remains outside this book; the book explains the reusable knowledge process.

## Open Questions

- Should each release version become its own section, or should one section cover the release note workflow across versions?
- Should the validation CLI eventually check that every book claim has source evidence?
- What metadata is needed for release books across multiple versions?

## Next Use

Use this book to test source-to-book validation and to shape the future console's section detail view.