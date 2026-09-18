# System Core

The system as a whole; including all protocol management in and out the _bios_
can be managed within one thread core.

The system core starts as soon as possible to manage (predominantly) the running
apps and services. Similar to a linux system scheduler - every app booted is
registered within the main system. The same occurs for imports and the FS.

The Health Doctor is also integral at this step for maintaining a garbage collector
for RAM and imports cleanup.

+ Preferrably live within its own CPU core;
+ Isolated from the BIOS, drivers, rendering etc...
+ Manage startup and shutdown of apps
+ Host throughput for:
    + imports
    + FS usage
    + thread management
    + app loadouts
    + Driver hoisting (apps again)
    + Garbage collector

