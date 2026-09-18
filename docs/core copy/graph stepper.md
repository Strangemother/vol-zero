# Stepper

Relocated: Consolidated overview: `../../ai-docs/graph-overview.md` (This document remains a detailed source.)
Backlink: See extracted summaries in ../../ai-docs/sections/procedure-graph.md and ../../ai-docs/sections/glossary.md

A Stepper walks the graph and manages many chained sequences, as a pointer resolver steps through the layer. For each frame the stepper will read the key, action any functionality and perform any exo-cell actions, before proceeding again upon the next call.

Consider the stepper like a _loop_, but rather than a `while{}`, for each _next_ we aquire the next step from a pointer and resolve until the end.

---

A system consists of a stepper, walking core procedures, loading root binaries and executing SES. Each step may yield a pointer or another action to alter the actioning graph.

---

Functionally a Stepper should be extremely thin. But the abilities of the stepper may be bound to os runtime load changes, and layer abilities.

## Process

The actions for a basic stepper:

1. Load `0x0`
2. Read key and gather the next step.
3. Load `(0x0+x)+n`

Where X is the new current key and N is the resolved key, continuing simply as:

1. Load `X`
2. Read key and gather the next step.
3. Load `(X+x)+n`

The execution of a new graph round is dependant upon the load chain. Under basic conditions the graph would simply _end_. In extended management, the stepper pointer recurses to a preferred key; such as an entry loop.


# Technical

The stepper acts as the 'context head' read/writer for a graph step. For each step the pointer _actions_ the pointer source; presenting actions to the user .

+ The pointer may be frozen as other async actions occur.
+ the pointer expects a _read_ pointer to aquire step positions, and a FS to call upon.
+ The pointer will run upon a system yielding _next_ steps - and action each pointer accordingly.
+ A pointer is async, (cpu, thread, context) bound
+ stepped by the 'stepper machine'

```py
def stepper(address):
    ctx = stepper_context(self)
    source, pointer = get_address(address)
     await execute(source, ctx)
    address = await ponter.get_next()
    await stepper_end_step_process()
    return address
```


## Stepper Machine

The 'machine' for a stepper should action a pointer address step - given from the automation or the pointer data. The machine is locked within a 'cell' (somewhere) and has its own stepping frequenct and synthetic communication suite.

A Stepper machine is built by the _kernel synthetic cell generation unit_ (yet to be named), of which builds a new stepper context and schedules it upon the standard primary machine.

The stepper machine is given the correct context during its instantiation but functionally lives isolated from the primary machine. Without this machine the stepper would require _manual pushing_ - but obviously this isn't a bicycle, so something much action each step.

---

The machine _acts like_ but isn't a loop, as with each iteration is actioned by the primary machines _goto next_ function. This won't work until the primary machine can direct the stepper - or the stepper intiates self-executing-source (debinding the stepping requirement from the primary).


## Machine Parent

Above the 'machine' the system provides a host of runtime api's (facades) for the parent to build _context layers_. Each frameset, for every machine is built specifically for the task.

To convey this in VOL terminology:

ROOT: Many _Facades_. The core featureset maintaining all source
    Machine Parent: A _Cell_ connected through membranes using given facades,
                    hoisting pointer control through a directed graph
        Stepper Machine: (NO NAME): A utility to manage the fequency and movement of stepper
                         within its realm.
                         It provides a graph to the steppers
            Stepper: (NO NAME) A _walking_ entity acting as a loop host,
                     peforming pointer resolution and reloving requests through given facades.

                Pointer: (Named as): A eval and addressing step within the graph.
                        A pointer is a component of any graph


### A Pointer

Explained in other pages, a pointer acts as the actuator for VOL source. In it's simplest form it's a code stepper:

    1. Go to address(1.2.3)
    2. run SES
    3. [optionally] return _next_ pointers.

The pointing position is irrelevant to the pointer:

```py
>>> Pointer(0x000032).run(context={}) # => Execute at path.
Pointer(0x10223)
```

Note the pointer may not perform _the next_ address eval. This is the job of a Stepper.

### A Stepper

Functionally a _stepper_ could live outside a machine, constantly stepping pushed requests through a personal context - such as an attachment to a user terminal.


+ Consider this as the eval engine for executing source. The stepper

### Stepper Machine

The stepper machine handles the _allowances_ of the stepper; and performing any injected routines after every step (consider RTOS).


+ They live in a co-existing sytem of other stepper machines, comminucating across membranes for timing and task sharing.
+ Acts as the _running engine_ for steppers, as they walk an active graph

### Machine parent

The stepper machines are built by a machine parent, and this parent monitors the _life_ of a stepper machine; is it alive; it is stepping etc...

+ May own many stepper machines working in-unison
+ Has access to its (given) entire facade and may volunteer this information to stepper machines
+ Owns the _greater graph_ - a subset of the primary graph relative to the work required within this machine parent.


### Root

They are owned by the root (or primary host) runtime; of which is responsible for generating and yielding work into the machine. Essentially a machine parent is a micromachine of the primary root - a facade of _allowances_ and capacity for the internal service.

+ Generates 'machine parents' similar to sandboxes or VM's of stepper machines
