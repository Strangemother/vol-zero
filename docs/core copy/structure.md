# Stucture

I'm not sure why this doesn't exist yet. An architectural overview of components from the core machine to _desktop_.

# FS: Filesystem

VOL filesystem. At the moment just called VFS. It couples two stages of interaction

Host:
    HOST read write file structure, such as reading NTFS files.
    This will be a simple "port" to the HOST. If the host exists.

VFS:
    A custom virtual file system implementing graph data with automatic history
    and transaction references.
    Permissions are not integrated to the base FS - instead defined by a sibling record.


## Root

The root file system includes base content for container and HOST configuration, followed by VOL implementation for HOST then runtime configuration.
Once the Base can read write the 'machine', the VOL may _boot_ the session application and routines. Each mesh DEVICE has its own HOST config and so on.

The root data persists in the HOST (such as windows), a boot config and 'bios' for the VFS, and a final 'runtime config'. This information is accessible to the the CORE runtime but not necessarily available in the high-level routines.


## HEADER

The entire file system (bridging HOST and VFS) maintains a separate record of file meta data. inclusive of

+ Permissions
+ Date
+ Location - such as:
    + disc header location
    + transaction address
    + HOST FS
+ Other meta.

At the moment this can be both a graph and standard key value - such as a binary SQLite.
Each header should chain to a key of other headers. (Yes a blockchain) and probably stored locally to the VOL runtime; such as within its CORE os.

Evolving to running natively (as the root file system) - at the moment it's just prototype raid simulation.


## VFS

The VFS three stages of implementation:

+ http://elm-chan.org/fsw/ff/00index_e.html
+ https://github.com/althonos/fs.sshfs

### Bios TAPE

read more tape.md

Although currently (poorly) implemented, the TAPE is a TYPEA file system type containing procedural instructions as transaction for CPU or higher level instructions 'taped' into the BIOS or other accepting runtime. Taking the 'Tape' analogy from literal magnetic tapes, where they read start to finish.

**Note:** _This touches on a definitive topic of 'file pointers'_

Todays method of sequential reading defines a walking 'pointer' for socket and general streams (and other stuff like collections). Through the three-phases of VFS and the higher-level of GRAPH db, a pointer becomes a BLOCK, and reading data in CHUNKS across the entire architecture


### Sector data

Considering the runtime, standard apps will have a standard file to IO. The VFS records through a HOST container translator as VFS data records. Normal _files_ on a Win or Linux system but readable only through a VFS mounting.

+ VFS data will be blocks of data as chunks of sequential _n_ size.
+ An  example 100mb of text content is broken into segments, written as VFS formatted files on the HOST or some device location (network for example).
+ A record of the file exists in the HEADER - along with its permissions and filename. Yes loosing the HEADER record will probably render the chunk useless.
+ Encryption at this level would work - as each file (VOL block segment) can have its own encryption routine.


### Network / Remote

The `Sector data` methodology is translated to remote network content. As VOL is mesh capable at the root, a user can map a remote device and "flag" it as an expandable unit - including it to the CORE ring of devices.


### VFS-Graph

The content written through VFS protocols is an automatic graph and self-evident chain of transactions. By applying a record of transaction as a single HEADER entry and VFS sector file, the GRAPH defines a tree record. Persisting history is easy. but defining a start node in this method is not efficient.

Consider a file of 100gb, and attempting to read the sequential data changes. Walking the headers is quick but building a file from this is hard.

1. Store a transaction of changes in graph descending order. Reading changes from start to finish can read a full graph.
2. Store a an order of transactions relative to byte order. Ensuring iteration from top to bottom through end leaf shards

+ A file starts as inputted bytes. Written through a VOL GUI - such as 100mb of TEXT.
+ The file content is persistent text data (local segment or remote segment - but each as one or more BLOCKS of text) written though the VFS as a simple file.
+ The transaction ID is stored in the HEADER record - stored in the graph.
+ The VFS-graph has the HEADER record with its file reference (VFS Segment block), permission and byte start stop relative to the given content..
  This may be `0 - 100mb` or `0 - 50mb` proceeding to another graph node.
+ A 'order' record persists graph ID records, in order of bytes. Leading to a pointer file of many IDS to sequentially read.

After 3 file edits (Load>save 50mg, prepend>save 30mb, append>save 20mb) we have an out of order header graph.
As such an edit to the _top_ of a file generates a LEAF (last node in a graph chain) to the file graph, with the last changes.

Reading the _graph leaf id sequential order_ file, we can rebuild the procedural file from partially distributed content.
In addition this content _must_ yield in a segmented fashion.


# NN: Neural Net

Built into the core is a Neural Net and basic perceptron setup, allowing integration with the core system
to use by the developer (high-level) and low-level health-care.


# Scheduling

Core routine start, stop and execution of application. requesting routine work at the correct time.


+ maintains an order of start stop executables
+ It's not a 'time' clock -
+ It does not handle OS CPU execution


# Sublet

The main System maintains one thread of execution leaving others free for system utils. Notably any interfacing of the core routine should occur through a translator.
Each task the system runs executes within an isolated sandbox and/or thread. Defined as a 'sublet'


# Multiprocessing

Spawn sublets, headless and threaded process cores through a central routine and asynchronous API - such as purpose built API for thread talk.
A sublet has a strengthened container forbidding some functionality.


# Permissions

The current start of system _permissions_ is pretty well applied. Some considerations for how permissions persist across machines is the biggest concern.

With VOL - the base system, FS Header and user defined content have a physical divide governed by implementation
