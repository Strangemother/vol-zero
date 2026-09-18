# Node internal vector path compass

Relocated: Consolidated overview: `../../ai-docs/graph-overview.md` (This file preserves original detailed example.)
Backlink: See extracted summaries in ../../ai-docs/sections/procedure-graph.md and ../../ai-docs/sections/glossary.md

A graph node may have many input and output paths, through a sequence of chains.
The chain may define a _required_ stepping path, with other paths within the node being a bad path from the given history:

    CAT
    CAB
    BAT
    MAT

In this case the graph would yield `(C|B|M) -> A -> (T|B)`, however `MAB` is not a valid path.

To rectify this a node may have an _internal compass_ directing the path through the correct chain, given the history of the path:

    CA -> T|B
    BA -> T|B
    MA -> T

To do this witout mapping every possible path within the graph, we mount a compass of vectors, for the input value:

    1 2 3 4 5
    C B A M T

As the graph walks a path, the unique sum is calulated

    CA == 4
    BA == 5
    MA == 7

The internal paths map the ints to the output. The first value is the _sum_ of the incoming path (from above)

    [4,5]: T|B   # CAT, CAB
    7    : T

Invalid input paths return a bad path (or none at all in this case).
Extending the graph may be done by calulating the position and value of valid history paths:

    [9, 10, 11]: S


---

An int relative to the _left_ position of the graph can refer to a layer in the graph, stepping backward to a lesser history. Each int in the vector is an arbitrary (but unique) value, allowing for 3 vectors to quantify a unique position e.g. `[0, 0, 0] => [255, 255,255]`

    [0, 0, 0]: A

## Cascading sums through loops

A path may be recursive and _loop_ through the graph - potentially from a start point. Therefore a pointer value would explode past a calulative point. For this we could `mod` the vector values through the limits of each vector position; ensuring a recycle ends within a target node.

    current_path = [V1 mod 255, V2 mod 255, V3 mod 255]
    [current_path, other_path]| T|B

However this may reduce the flow process when actively generating recursive loops. Collision may occur within the compass; where a mod of an actively looped pointer directs to a valid compass direction, but during _the current_ phase should yield invalid.

This should be mitigated with the intial vector being a "primary vector", and orders direction _from the left_ of a graph. This modulo may be larger or never always rising e.g. A _loop vector_.

