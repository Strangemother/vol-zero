# Pointer Keys

Relocated: Consolidated overview: `../../ai-docs/graph-overview.md` (Detailed key semantics retained here.)

The 'address' of the pointer should be predicatable and computed by the previous
unit + the current unit, resolving the next pointer.

    A + B == C

Where A is the first node, B is the current, resolving to C the _next_. A node may be bound in place though its graph position, the values within the position vector correspond to _layer_ and _ownership_.

> A 'layer' and 'ownership' are undefined at this point, but the corresponding vector points may be any data-associated int; In this case we refer to the left index of a graph and a 'permission' bit.

    Layer = 0 # representing 'root'
    Sysbit = 1 # user permission?
    position = 7 # an index counter for first positions.

    A = [layer, sysbit, position]
    B = [layer, sysbit, position + 1]
    dot([0, 1, 7], [0, 1, 8])
    57


## Vector Name

Once resolved, the name of the pointer will be a 'vector' `x,y,z`. Each being a number for the pointer location. Although still under research, some concepts seem useful:

+ #1: Layer bit: Each graph exists within a 'layer' the graph may execute
+ #2: Graph bit: Identity of the graph; such that a later can contain many unique graphs
+ #3: Position bit: The location of the entry, within a contigious layer of SES

    current|to  SES
    #[layer, graph, position]|#[layer, graph, position+1]   functional

    #[0, 0, 1]#[0, 0, 2]   echo('hello')


the SES may be locked to the layer or graph it lives within. E.g. a pointer may step a graph but not a layer.
The layer contains the functionality needed to work. If the SES requires its layer, the references will not match the corresponding source (and break.)
The user could cheat, and move the SES into another vector, but the function would simply run the wrong graph within the same layer


Considerations for _pointer returns_ and contigious tape keys.

## Pointer return

A pointer may return an address, thus a forward address in the name would not be valid.

## Tape keys

The direction of a pointer may be given through a sequence of keys as a 'tape' of steps.
Each step is done in-order. This would override any key addressing - opting for named placements.

## Key names

The main graph binds a key (the name) to a pointer. The pointer may be complex or a simple bytes load.

The name of the key within the graph defines the position, and the forward solution for the pointer. Rather than inspecting the pointer content, we can inspect the pointer _name_ and infer a lot of processing.

The name may be any string; parsed at runtime for graph actions. In the simplest form it's a key with a forward key. In a more complex setup, the string may define other parameters of the pointer; such as live re-addressing or evals.


"From Current To" key names

    {
        "from|current|to": functional
        "to|current|other": functional
        "other|current|null": functional
    }

with pointer attributes and vectors:

    {
        "[0,1]#[0,0,0]#[0,2]": functional
        "[0,2]#[0,0,1]#[0,3] |async": functional
        "[0,3]#[0,0,2]#null  |returns": functional
    }

When traversing names, the stepper can parse and analyse the future steps before execution.

---

Notably this could be a security issue, as all addresses are written as visible addresses through the system. In this case the _key_ may be encrypted; and decrypted by the stepper at runtime.

### Name changes

The name of a key may change, to address updates in the graph. Given the key is a pointer, it may _parse_ a more complex pointer; such as _from nowhere_ or _expect pointer return_.

They key name dynamically changes and updates the graph addressing on-the-fly. The pointer addresses some self-exectuting code, providing the _chain_ and other context as a frame of information to the exectutor.

### Friendly names

The name of the key becomes predicable but unreadable, e.g. `#0,0#1,232#[2]:#0x4e4`. Therefore a _friendly_ name should address this key, and the friendly name always address this key, as the name changes.

## Notes

a Dot or Cross product of two vectors isn't enough.
+ The name of the pointer should direct the graph to the _next_, and _previous_
+ sometimes a pointer will need a real name, address though a live shortcut.
+ changing the name to 'current/next' may yield faster results when unpredicably stepping


    {
        "current|to": functional
        "to|other": functional
        "other|null": functional
    }

TODO: Find a formula to compute the _next_ key, given the name of the current key, without exceeding thresholds, without collisions - within the space - e.g. polar coordinates


# Graph functions

A function may require another pointer action. The code is parsed to yield the dependant pointers and the graph pointer data can reflect this dependency in the name


    {
        "[0,1]#[0,0,0]#[0,2]": functional
        "[0,2]#[0,0,1]#[0,3] ([0,2,2])|async": functional
        "[0,3]#[0,0,2]#null  |returns": functional
    }
Asset "L1 3x3 Detached02" was successfully dumped to:
C:\Users\jay\AppData\Local\Colossal Order\Cities_Skylines\Addons\Import
