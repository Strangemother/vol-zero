The 'first moment' defines the initial input point for a user or autonomous unit to actuate the root application.

In this case we can assume the VOL is installed and configured to run on the target device. This is achieved by compiling the runtime (VOL.exe), and an initial graph of actions for the platform.

Just before the _graph_ the system must load elements. This may be done by hand throug the first _terminal_,

> The direction will step away from a 'terminal access' or cli for initial entry. However the system will still require a magic reference - without a suite of libraries. Therefore at the root if the runtime, a core feature provides a `get/set` of bytes to inject the root runtime then actuate the magic number.

Once the library is loaded, by capturing the system BIOS and loading our custom rom the **BIOD** (not bios) loads the root suite. This is considered the first (or zero'th) layer containing:

+ The runtime
+ Config
+ Fundamental libs,e.g. a filesystem and networking

Then step into the _first moment_ through reference of a target bytes file e.g. `vol.first.moment`
This contains the initial header to then build upon the root to instantiate a primary machine:

+ core system libraries e.g. Graph, Mesh etc...
+ multiprocessing
+ visual
+ Audio

Once fully loaded the system steps into the second moment, The embodiment of the cluster, and all the parts of a VOL:

+ cluster pointer
+ Graphing
+ networking
+ Starting clocks and the stepping machine
+ Wake-up tasks.

After the base suite is applied throughput the eco-system the user-suite may load:

+ Identities, private management (customs)
+ Logins, apps
+ secondary tasks

---

Focusing on the events after the first-boot, a "first moment" should be the defacto _start_ of the system, allowing user featuresets. A eval'ing pointer can be _placed_ within a memory graph; a range of graph entities bound to these lower dimensions - referenced within the runtime and RAM memory.

If an automatic method cannot be loaded (such as discovering a mounting-point for any existing graphs), the first-moment (Vol version <1.0) initialises a terminal input, expecting a pointer name for a start key.

    .: vol.system.primary
    .. success ..

The runtime will load the pointer data at the referenced location into the current context layer. All dependencies must be loaded manually, before this step.

## input feed concept.

Access user input through the standard terminal, by pointing the current stepper to the pointer designed to procedurally request text then feed that back to the caller.

