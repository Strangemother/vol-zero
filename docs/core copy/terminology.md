# Additional Modules

When implementing core units, they may be defined by name - through their layer of work.


+ Chamber

    At the _root_ within the monolith core libraries provide the kernal base procedures and data to initiate a runtime. A `Chamber` identifies a directory of _magmatic_ libraries; literal code in source code files, processed as "fundamental build components" of the monolith - The `Mantle`.

    As a group the `Chambers` directory contains the root fundamentals `mantle` and `igneous` packages, each with sub files of "modules". Each "module" assigns _code_ and _configuration_ when imported.

+ Magmatic

    A group of mantle and other core components is defined as a `Magmatic`, or a _magma_ for short. One Magma identifies packages, modules _mantles_ and proceeding _chambers_. All manifest as real files within the HOST and accessed through the `vol._vpt` file

+ alt-magma

    A short-term for "alternative magmatic" the `alt-magma` provide a fundamentally alternative suite of tools for the root monolith. As an example the "alt-magma/python-38-core" may replace the `magmatic/mantle` to provide a real python core, rather an a thinner VOL runtime.

+ Mantle

    A (or _the_) mantle assigns many modules, packages, and chambers within a single installable library store. All assets within this directory should be a direct import - or a chamber of magnatics, with this same layout.

    It's not recommended to nest chambers within mantles in the physical form, as this may lead to deep directory nesting. You'll notice this is done within the _scratch_ directory.

+ Igneous

    One of many possible root monolith builds for the VOL, allowing the continuation from a basic input output system utilising the installed suite. This relys upon a stable mantle (A prepared runtime), and may run on the #0 zero graph mode, allowing configuration of core graph data.
