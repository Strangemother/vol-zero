# Radicle Load

## Secure Boot Notes.

A secure boot location provides a key when seeding a radicle, this is given to
the memory and tested for encrpytion security.

## Updating core crystals

When updating the radicle loadout, the config must match the given key and likely CRC.

To do so, when changes are made to the a secure crystal, the updated module is set in place and digested. thw memory stores the updated config and deletes any original.

1. Add Change to crystal X
2. Compile new Crsyal XY
3. Gather New Key Kxy
4. Apply Kxy to Radicle(key=Kxy)
5. Load crystal update
6. [SYS] store new crystal
7. [SYS] delete XY

Upon reload the memory loads the crystal, including and core adaptations through this process.

1. radicle(key)
3. load crystal
2. load memory
4. install crystal memory based updates
5. assert key
6. ... yield

Each change to the crystal config should bind a module with new key to the radicle.

---

When loading the first crystal execution suite, it should assert commands, driven by the dll, the runtime (edits for the environment), any _updates_ from other crystal, and finally any memory changes in the ramdisk KV.

Once the command set is merged each stash value is executed as part of the radicle loadout.


nim
vol
py