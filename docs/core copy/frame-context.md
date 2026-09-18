# Context Frame

Backlink: See extracted summaries in ../../ai-docs/sections/procedure-graph.md, ../../ai-docs/sections/core-runtime.md, and ../../ai-docs/sections/glossary.md

A Frame acts as a steppers _current view_ of the system, complete with all the knowledge required to run the incoming pointers. The `Context` acts as a parent hosting the `Frame` and all its associated parts.

A Context lives across the life of the stepper as it walks a subset graph. All pointers and SES may view the context as 'the active system' and utilise components and stord data for 'app' tooling.

Within a context some mandatory items:

+ The persistent store (memory) address
+ The live graph
+ Temporary (contextual) memory
+ functions, methods and root API
+ pointer knowledge

## Stepper Implementation

A stepper provides a Context to the pointer when initialised. The pointer (before execution) may utilise any information within the context and is functionally landlocked.

The Pointer, Stepper, and SES may alter some elements of the context, and additional DATA applied is pushed to a newer frame relative to the pointer. The context has a pervue of all frames across all pointers within its stepper machine.

