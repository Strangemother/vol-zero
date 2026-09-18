# Procedure Graph

Status: Source
Relocated: See extracted summary in ../../ai-docs/sections/ (graph-overview.md)

The "procedure graph" applies a linear ordered function set in a graph chain, consequently performing a "program" or application. every application exists as a key reference within a graph - namely the function name.

Initially this serves little function, other than a handy key reference. However futher abstracting this with a linear execution chain, An application may yield chain actions in parallell or linearly, through a combination of async execution and socket communication across all nodes within the a VOL ecosystem.

Later this is abstracted in to a VOL _AST_ like methodology, where routines are executed in a graph-like fashion and coded with application to utilise the "Graph nodes" lingistics.

1. A system has many functions
2. A user write linear instructions
3. The system accepts the text bytes and tokensizes to AST
4. Execution occur off the visual thread, communicating through sockets.

---

From the base we can introduce the base language construct, stepping from the turing complete _bios_ to the +1 layer - user space and local allocations. This layer initialises the "first run" routines such as an async event routine.

The fundamental application intiates a two step graph "A>B" and repeat. This is essentially a forever loop - without the loop. We then build AOP prodecures on top of the event loop, stacking vertically

Graph:

    #0: Step to #1
    #1: Step to #0


# Graph Layering (Security Rings)

The lower order graph nodes maintain a special place allowing or refusing protected procedures. If a function emits from #0/#0, The functions are in a protected mode with lesser drivers but a raised security level.

Consider this like "protected mode" in standard archiecture, where 16bit machinery and lower live within a protected security ring 0 to ensure higher level application. This is important within the Procedure graph, where the secure driven elements exist within frames without upper access

1. The system integration refers to at graph position #0
2. a user executes from a "Origin number" the existing graph origin

---

The user steps the graph manually - or flows through the nodes during each event phase, digesting the result for each step into a colloid.

    byte byte > Step > yield > byte byte > step > ...

As the user inputs bytes, the key is potentially tested and stepped. When the step occurs, the result is cached, digested, or immediately executed.


## Understanding

The entire system runs as a graph of pinned statements, yielding a pointer or null for a natural step. Each step runs within a 'live' step - some steps will be deeper than others.

For example the entire machine runs as #0 step, and will step to #1. All pointers in #1 will iterate and action changes - and the pointer steps to back to the original.

With nested steps the loop monitors its current positions and graphs within, stepping async or sync.

    root #0
    system: #1
        alpha: #0
        beta: #1
        charlie: #2
            echo: #0
                fox: #0
            gamma: #1
        delta: #3

    Thus a linear root:

        #0
        #1 #0
        #1 #0
        #1 #1
        #1 #2
        #1 #2 #0 #0
        #1# 2 #1
        #1 #3

each step corresponds to a position pointer

## Executable Pointers

Each step within the graph resolves an executable data structure of which has an overview of the current space (user layers), the reference structures and others pointers. Upon execution a _step_ executes its transaction pushing changes into a shared space, yielding pointers, or performing other executions without any graph alterations.

The executing pointer may return a redirect, allowing _stepper_ to move into another part of the graph. From our example above this could be a pointer (#1#1 "beta") redirecting skipping a graph to the end (#1#3).

Functionally this serves:

+ A reprogammable kernel
+ _self-traversing_ data structures (inline pointers)
+ Instruction optimisation

In all cases a _pointer_ on the graph may _alter_ the live graph state. In addition a single system may run may graphs in parrallel, serving many CPUs and one shared memory space, or discreet units of async processes (background graphs).

> The fundamental idea of kernel code synthesis is to capture
frequently visited system states in small chunks of code. Instead
of traversing the data structures, we branch to the synthesized
code directly. In this section, we describe three methods to
synthesize code: Factoring Invariants, Collapsing Layers, and
Executable Data Structures.

    The Synthesis Kernel
        Calton Pu, Henry Massalin and
        John Ioannidis Columbia University


# Topology

> All terminology here will change, and is documented using classical vernacular for easier reading.

+ SES: Self executing statements; the function, or the content within the pointer action.
+ Pointer: A single reference within the entire system graph; as also defines will action a process, such as move.

The graphing system applies a pseudo concept of system stepping and runtime layers.

The kernal provides an API of layers, functions and an pointer (and events) stepper. The system executes upon the graph, The goal of the system is to _reach #1+_ where #0 is the linear root point, and any step within is a traversal down the tree.

At any instance, the walker may be _moved_ into a new branch of SES by order of a pointer return.


## Runtime References

1. Loop: The walking _graph_ and its functional pointers
2. code: The self executing statements, or _functions_ from pointers
3. memory: runtime memory (RAM) for the system and _apps_

The primary stepping solution drives the direction of the linear walker. It reads as an instruction manual for steps but the primary graph yields root steps, of which sub graphs yield user work.

This allows a primary graph to interate independantly of other management sub graphs:

+ bios runtime
+ System
+ Presentation
+ membranes
+ remote processes

Each may exist within a discreet process:

+ A cell or layer
+ CPUs or mesh clients
+ remote services

## Loop

The primary system loadout steps a graph; an initial graph of #0 (one) nodes.
The loop walks a tree of pointers. Each pointer executes code.

The system will have many _graphs_ - but one primary graph executes by system demand and cannot be frozen by a standard user. This root graph step includes the system runtime.

A loop executes within a space through layers

## code

The pointers a functional executors, also known as Self executing functions. They provide the _code_ for actions of the graph. Each function is a micro or macro solution, governing changes to the graph or memory block of the 'app'

## memory

Generally the graphing system has two types of persistence content to ferry. The 'memory block' allocates a set bytes range, and a transient memory runtime for message trafficing between graph steps. Fundamentally they are the same thing; as a pointer has access to both. However in some cases the pointer returns a value (such as an inline injection) - of which is stored within the transient "app" memory.

Though the graphing solution, a SES may only access the graph range defined in its _space_ or cell. the process may poke outside their references, but this is done through a authorised membrane.

---

Thus the loop steps pointers. The pointers execute SES with memory references.
A Pointer may alter the graph, but rarely alter the primary (root) graph.
Memory exists as one wholesome state, membranes and the FS cares for _where_ and how it's stored.


## Layout (presentation and calculating)

The topology of the graph is a left to right, top to bottom executing chain. Each origin yields a list of statements for _work_.

The stepper speed can be considered as _FPS_, and within one upper frame a single step is entered and executed. Many single steps within a period (Seconds) yields a speed and a size of work.

    #0 root
    #1 system       // 1 frame
        #1 #0       // 30%
        #2 #0       // 20%
            #2 #1
        #3 #0       // 50%

The count of nodes from root to the leaf node `#1 #2 #1` is the root distance, where a relative distance is from an origin (#1#2) to it leaf within. Each pointer represents some _work_.

# Forward feed branch data

The graph may be _split_ to have parts of the graph execute within a remote location. This may be local - such as a membrane cell or remote processor.

The execution chain is send as an instruction, starting a relative root pointer and all its children. The entire sub graph may not be _disectable_ and pointers within the sub graph refer back to the original graph data, or async attributes from moved branch calls.

This means when the _other chain_ executes steps are missing and must callback to the original data-source. If this is over-the-wire, it may be expensive.

To mitigate this, a graph pointer should reference its _other_ references - and be inpected upon runtime sendoff. If attributes are static, the executor may _push_ this information along with the sub graph - perhaps even rewrite the graph before submission.

For async pointers; live _references_ may wait for the result to occur, placing the result within a membrane for transport to the target graph. This information doesn't need to be sent _by request_, rather the origin graph may _offer_ this data to the sub graph at the best best

---

The origin graph may feed the pre-requested information, before the sub-graph requires the content. If the stepping of the graph is ordered, the forward feed of the reference pointer can occur before the information is required.


# Graph handoff.

A low-priority or lesser used graph of action may be stored away as a SES for execution when required. As an example onboarding a hardware device. The instructions for this may exist within a graph of many pointers. The origin graph can make a request to _execute a stored graph_ (in this case hardware onboarding) and inject the flow into the executing chain.

The process of _asking for_ and _providing references_ to a new chain is a "graph handoff" - and may be done upon request of a pointer. The low-priority graph may perform its action and be closed for later.

    ...
    #1: async pointer(system)
        #0 pointer(alpha)
            #0:pointer(open hardware)         -|
                #1: open(bluetooth)            |
                #2: send(.#1) ref(0x249475)    |   all these functions
                                               |   as a sub graph (open hardware)
                #3: async wait(#2)             |
                #4: close(#1)                 _|
                #5: async send(..) ref(#3)
            refers:
                - bluetooth
        #1 pointer(alt-alpha)
            #0: async handoff graph(open hardware)     // in this case we present a pointer with a subgraph
                #1: async send(..) ref(.)             // once the parent is done, the result executes within
            refers:
                - bluetooth
    ...

# Parallel Graphing

+ Multiple graphs running asyncronously. They communicate through leaf nodes (pointers with references) or membranes.


# Best fit inspection

Some pointer may require certain hardware or functionality, of which exists within a subset of the topology - such as a mesh client with bluetooth.

The sub graph should be sent to the _best fit_ within the network of available units, to produce work and return a result. this should be done through pointer referencing, and understanding _what_ that pointer utilises.

---

In this case, the runtime api may yield a pre-inspection of the SES. Failing this header references on that pointer can refer to requirements:

    #0: parallel(0) pointer(bios)
        refers:
            - bluetooth
            - wifi
            - CRC
    #1: async pointer(system)
        #0 pointer(alpha)
            #0:pointer(open hardware)
                #1: open(bluetooth)
                #2: send(.#1) ref(0x249475)   // Send memory content through the open
                                              // port
                #3: async wait(#2)            // wait for the result
                #4: close(#1)                 // close the socket
                #5: async send(..) ref(#3)    // send the value of #3 up the tree
            refers:
                - bluetooth
        #1 pointer(beta)
            #0 dispatch(#(in)) to membrane(system)
            refers:
                - #(alpha)
