# Kernel

I don't like the term Kernel as a final terminology for the subsystem interfaces, as a true kernel must interface with lower hardware. In this case the kernels lowest point of operation is the HOST and the supplied configuration.
However all aspects of a kernel are applied to this management unit.

## Quack.

https://www.engineersgarage.com/tutorials/what-is-kernel-programming

1. Process management subsystem
2. Memory management subsystem
3. File management subsystem
4. Inter process communication subsystem
5. Network management subsystem
6. Device driver subsystem


## Application

To apply this into the HOST container CORE anology, some of the above Linux routines are moved or renamed. Creating a similar hybrid monolithic kernel.

Monolithing the main kernel is an option through built-in C compilation.


### Process Management

Maintained by a ring 0 stack - isolated from the main system to actively manage internal processess and threads. Each item is a task[let] running an high-level language integration or Straight C exe


### Memory Management

On a HOST the MM module manifests as

+ a large virtual table for mapping allocated RAM to tasks
+ RAM <> Local disk (mem swapping and virtual tables)


### Filesystem

In VOL it's a little more complex. Three stages of initial integration persist within a VOL runtime, then layers of user application

+ HOST initial integration for init config
+ Standard internal VOL mem (Graph)
+ Compiled network or additional disc

Followed by the user api - cloud, ipfs etc.


### Interprocess communication (Membranes)

Each task or thread will naturally provide an API for inter process communication
isolated from the a central event core. Events can register and wait on a state machine

The central trigger performs a monitor list on inbound events and calls a compiled/cached source to run on the event name.

The name of the event can be anything, but I'm considering one of two methods:


#### dotted notation

Standard dotted notation through a namespace taxonomy to a chosen event name or event range:

    inputs.mouse.buttons.click.left
    inputs.mouse.buttons.click.*


#### Vector based notation

Using the new key mapping for data naming, the events by name could be 3 tag notation - or a word vector:

    mouse   click   left
    mouse   buttons  click
    mouse   *

Each depict the dotted notation. The simplication by removing taxonomy chains but keeping granulity with less text.


---

Event source can be pre cached
