# Architectural map (preliminary, not a specification)

These are starting points from the historical repository. **Current VOL Zero equivalents are not yet verified.**

| Theme | Historical source | Idea to preserve | Investigation |
| --- | --- | --- | --- |
| Genesis / Origin | [Genesis-Origin.md](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/docs/Genesis-Origin.md) | Start with a nearly functionless origin space. | How does VOL Zero establish its root and first capabilities? |
| Radicle | [Radicle.md](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/docs/Radicle.md) | Seed the origin with root runtime capabilities. | Is there an equivalent initializer or split sequence? |
| Graph execution | [Procedure Graph.md](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/docs/core/Procedure%20Graph.md), [graph stepper.md](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/docs/core/graph%20stepper.md) | Keep graph, pointer, stepper, and machine conceptually distinct. | Inspect modern node addressing and execution control. |
| Context / Frame | [frame-context.md](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/docs/core/frame-context.md) | Execution occurs within a scoped context. | Map actual context ownership, isolation, and lifetimes. |
| Tape / Phase 0 | [tape.md](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/docs/tape.md), [phase-0.md](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/docs/root-monolith/phase-0.md) | Protect boot/root graph entry and guide startup execution. | Compare with Limine handoff and root stepping. |
| Membranes / Mesh | [mesh.md](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/docs/mesh.md) | Boundaries for cells, communications, and negotiated onboarding. | Identify implemented transport boundaries, if any. |
| Data particles / grains | [grains.md](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/docs/fs/grains.md) | Logical data assembled from distributed/independent pieces. | Keep separate from presently implemented memory allocator. |
| Experimental storage | [memory-as-weights-and-biases.md](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/docs/concepts/memory-as-weights-and-biases.md) | Research question: can a learned representation reconstruct stored data? | Evaluate exact fidelity, size, security and cost; not established design. |

## AI-assistance caution

[AI docs gap index](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/ai-docs/active-gaps-index.md) flags unresolved ordering, pointer return, caching, security and filesystem details. [AI docs 2 filesystem overview](https://github.com/Strangemother/Virtual-Operating-Layer/blob/primary/ai-docs-2/fs/overview.md) describes a proposed model rather than a fixed protocol. Use these as navigation aids, not authority over original notes.
