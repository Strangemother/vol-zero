# Context and working agreement

## The two repositories

- [VOL Zero](https://github.com/Strangemother/vol-zero) is the newer practical kernel project: Nim, Limine, low-level systems work, and a graph-oriented runtime. The actual implementation must be verified against the current code before making claims.
- [Virtual Operating Layer](https://github.com/Strangemother/Virtual-Operating-Layer) is the earlier multi-year research/code repository. Its primary documentation source is `docs/`; `ai-docs/` contains assisted extraction, gap analysis, and synthesis; `ai-docs-2/` contains later reorganized explanatory drafts.
- This is a **knowledge recovery and modernization project**, not a request to transplant all old proposals into the kernel.

## Collaboration

Jay is the architectural decision maker. The assistant's job is to read, explain, check coherence, trace provenance, surface contradictions, propose small changes, and prepare reviewed code/documentation work.

Honor the current repository's `AGENTS.md`: use Nim conventions, prefer graph-based structure, teach when design is unresolved, and minimize unwarranted low-level code changes.

## Documentation standard

For each concept, capture: original meaning; original source links; current VOL Zero implementation (file/function references); differences; unresolved questions; explicit decision/status; next test or migration step.

Keep the historical source in place. This workspace is intended for reusable, project-specific notes rather than pretending conversational memory is perfectly durable.

## Immediate initiative

Reconcile **Genesis / Origin / Radicle** with VOL Zero's boot and runtime initialization while protecting the original concept of an initially functionless space. No implementation change is authorized by this note.
