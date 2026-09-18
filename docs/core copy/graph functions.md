# Functions

Status: Source
Relocated: Consolidated overview: `../../ai-docs/graph-overview.md` (Original retained as source detail.)

The content within the pointer to execute, yielding graph adaptions or memory alterations.

+ Can be compiled on-the-fly
+ May be bytes, binary, or any lang
+ Can be executed in a sandbox
+ Parallel or async

A function or 'self exceuting source' (SES) acts as standard procedural code, but is plugged into the graph, with a visiblity to the concurrent frame, contigious memory space and it's local graph.

The function may be _standard code_ to alter the API, or runtime pre-compiled source (python), executing upon graph pointers. The code within the SES can be compiled and reapplied back to the tree by the system.


## Pseudo code

The content of a function directly works with the _chain_ and its context space.

```py
class Pointer:
    position = Vector(0,0,1)

    def func(layer,graph):

        # redirect within the concurrent space
        position = 2
        return Vector(layer,graph,position)
```

A more complex pointer would work with the graph
```py
class Pointer:
    position = Vector(0,0,1)

    def func(layer,graph):

        # Execute the SES (below)
        call(Vector(layer, 0, 7))

        position = @[layer, 0, 7] # Refernced from the memory
        return Vector(layer,graph,position)

        # As one line
        return (layer, graph, @[layer, 0, 7])
```

some other action

```py
class Pointer:
    position = Vector(0,0,7)

    def func(layer,graph):
        # resolve value, store in the context
        context@[self] = 10 - 8
```
