# Pointer

Status: Source
Relocated: Consolidated overview: `../../ai-docs/graph-overview.md` (Original retained; this file remains source of record.)

The Pointer is a header element, serving actions to the graph and the stepper. As the stepper walks the graph, the pointer is called to execute upon its action. This may yield a pointer, memory or other functional work.

The pointer name should be identifiable, such as "current|next". The stepper resolves the pointer name at runtime.

The pointer lives _off_ the walker graph and can alter the SES content of its address when executes. The next steps (and SES) may read the expected actions of the pointer from the shared context.

---

In this example the graph is a simple key(str): value(pointer), where the pointer is a literal class containing assets or a string of SES, however the pointer may of any content type:

+ bytes (file, literal)
+ compiled source (bytes) or API source
+ repointers/addresses/memory
+ Streams or live inputs.

---

"In memory" content has no delay thus pointer calls may be instant. However calls to a persistent service may be delayed, thus accessed (and cached) early.

The pointer (in _text_ form for clarity) should provide a 'header' for the self executing structure within.

```py
0x0: Pointer():
    name: 0x0
    position: 0,0,0
    created 2022-02-02 10:19:19
    last-access: 2022-02-02 10:19:19
    code: #A byte string of source#
    address: 0x0, some-name
```


## Naming (Extended)

The naming convention plays a role for presenting the path of the chosen next step.

Every pointer and SES has a position, defined as a vector. The vector shared the space across an active graph. In the simple method, the name of the pointer is any arbitrary string:

```py
0x0: Pointer(First)
    name: First
    address: 0x0
    next: 0x1
```

However in this case, the pointer content must be inspected to yield the next key. To circumvent this, we can apply the next key within the name


```py
0x0|0x1: Pointer(First)
         name: First
         address: 0x0
         next: 0x1
```

## Named Next Position

Therefore when stepping the graph we can understand the next position, without inspecting the pointer. However this yields some complexity when aquiring the next key, as this also includes a forward step:


```py
0x0|(0x1|0x2): Pointer(First)
                name: First
                address: 0x0
                next: 0x1

0x1|0x2: Pointer(Second)
                name: Second
                address: 0x1
                next: 0x2
```

## Backward Rippling

A rippling effect through pointer addresses during a write phase. This may not be possible as _deep_ chains would result in excessively large address names.


```py
0x0|(0x1|(0x2|0x03)): Pointer(First)
0x1|(0x2|(0x3|(0x4|0x5))): Pointer(Second)
0x3|(0x4|0x5): Pointer(Second)
...
```

unless the key was a graph of its own - but this wasteful


## Named Previous Position

Note: This also doesn't work ... as the pointer data must be executed to analyse the _next_ step

A more predicable and iterable naming method may be 'previous|current' - as a graph may read forward with the _current_ node name, from a _previous_ node name.


```py
0x0: Pointer(First)
0x0|0x1: Pointer(Second)
0x1|0x2: Pointer(First)
0x2|0x3: Pointer(Third)
0x3|0x4: Pointer(Forth)
```

As such when pointer `0x0` steps forward; it understand the next pointer `0x1`, Moving to address `0x0|0x1`.  This yield pointer `Second`.


## Pointer Tape

A 'Tape' defines the walk of keys for a stepper. This would recite an 'app'

```py
0x0, 0x1, 0x2, 0x3, 0x4
```


## Simple hyperspace hashing in three dimensions.

Each plane represents a query on a single attribute. The plane orthogonal to the axis for “Last Name” passes through all points for last_name = ‘Smith’, while the other plane passes through all points for first_name = ‘John’.

Together they represent a line formed by the intersection of the two search conditions; that is, all phone numbers for people named “John Smith”. The two cubes show regions of the space assigned to two different servers. The query for “John Smith” needs to contact only these servers.

- HyperDex: A Distributed, Searchable Key-Value Store

