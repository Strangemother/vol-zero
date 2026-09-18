# Contigious addresses.

When walking the graph, the _pointer_ attains an address and reads the _memory_ at the given location. Tthe address is bound to a small chunk of accessible memory allocated by te primary service.

A Stepper machine will access an address 'app' to yield a list of congious addresses for a suite of executions. Given we have _lots of memory_, we should direct the subset of work towards a mapped allocation.

The initial step will be a virtual addressing for the machine, allowing a persistent base for storing graphs and long-term data, and transient memory (ram). A primary machine allocated a subset of this greater memory - such as 50mg of 100mg.

Exposing a Linear address list to the digesting service isn't prudent, as this leads to direct memory overflow when the graph steps pointer (walking 1 dimentionally). Futhermore re-addressing the memory would lead to inner graph faults.

---

The best solution would be some 'perfect hashmap' allowing the allocation of linear memory through a named reference map. Alternatively we use a closed loop algorithm to _lock_ the memory address into a bound space. Therefore when a stepper _walks_ a graph, it can deduce a range of steps without reading memory (pure computation only), and we can allocate "pages" or subsets of graphs to a walking machine.


This would manifest as an algorithm to pick when building a stepping solution:

```py

machine = StepperMachine(globals(), key_function=minkowski_plane)
stepper = machine.stepper(graph, initial_vector=[0,0])
next_minkowski_vector = machine.generate()

while next_minkowski_vector:
    next_minkowski_vector = stepper.pointer(next_minkowski_vector).run()

```

## Methods

+ Minkowski plane projects
+ Euclid line on a 2D projection
+ Hemisphere or subflower vector plots
+ 130x130 (or more) Knights Tour
Self-avoiding walk
