# Work queue / unresolved questions

Status as of 2026-10-19: **proposed research tasks, not approved implementation changes**.

## Priority 1 — Genesis and Radicle
- [ ] Read all relevant original Genesis, Radicle, boot, first-moments and zero-suite notes.
- [ ] Inspect VOL Zero boot sequence, node registry, root stepper, and system initialization.
- [ ] Write a provenance-backed comparison: original design / current code / intent / gaps.
- [ ] Ask Jay which functionless-origin invariants must survive in the new architecture.
- [ ] Draft a small, clean canonical documentation page for review.

## Priority 2 — Execution semantics
- [ ] Establish terms and contracts among graph, pointer, stepper, stepper machine, frame and context.
- [ ] Resolve next-pointer precedence, errors, concurrency and graph mutation semantics; mark unknowns, don't assume.
- [ ] Trace what is implemented in VOL Zero and test minimal examples.

## Priority 3 — Filesystem and distributed capabilities
- [ ] Inventory particles, grains, aggregates, phenocrysts and colloids in original sources.
- [ ] Review membranes / mesh / onboarding and distinguish transport from isolation.
- [ ] Separate concepts with prototypes from speculative research.

## Documentation hygiene
- [ ] Create a concept template with source links, code links, confidence level and decisions.
- [ ] Track contradictions with explicit citations and a decision field.
- [ ] Record decisions in the session log only after Jay confirms them.

**Constraint:** Any architecture or code change must be independently reviewed; these notes do not give permission to modify kernel behavior.
