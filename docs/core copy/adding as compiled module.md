# Add a compiled module

The main runtime, bios and system modules are pre-compiled for import in the VOL. Documenting the `head` module

1. Add a new folder/fileset to `runtime-libs`

    in this case `runtime-libs/head/` contains:

    + `__init__.py` importing all
    + `head.pyx` mimiking __init__ for C importer

2. in `config/build/bios.py`, add to `COMPILED_FILES`

    Compilation of a file into the env lib:

        COMPILE_FILES = (
            ("COMPILED.head", [
                    "runtime-libs/head/head.pyx",
                ]),
        )

The compiled result binary is put into `build/bios_runtime/libs/build_libs/` for natural referernce.


## Notes

The compiled entity has it's own structure; it doesn not act like a python module:

+ All imports `include` result in a flat namespace. Therefore taxonomy and positional imports are ignored. Be careful of named method collisions.
+ __init__ py allows for python abstraction, but the unit is compiled using the pyx and only considers the COMPILE_FILES reference when compiling.
