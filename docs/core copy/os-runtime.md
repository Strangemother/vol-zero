# modules

Elements living on top of the base (empty) bios runtime to execute a working env.

1. Load host config
2. Load pre-image
3. load internal init config
4. start first phase

## first phase

1. Run pre-checks
2. load pre-scene
    + framebuffer interface
3. load base memory (vram)
    + VOL FS
4. load internal db cache
    + kv db of event triggers
5. configure for environment
    + apply system settings

## Second phase

1. Load drivers
     + Graphics, network (wireless) (first membranes), audio (audio Membrane and hardware), inputs, mesh (other membranes),
2. install presystems
    + Run driver systems using db cache and system settings
3. load init apps
    + First point of contact for user files


Target time < 5 seconds.
Preferred target: < 2 seconds.
