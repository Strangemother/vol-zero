#[
Provides functions and constants for querying memory information.

This module interfaces with the Limine bootloader to retrieve memory
information, including usable memory and memory categorized by type.
]#

#[

MEMORYTYPE's corresponding values in the Limine bootloader memory map.

Call to `usable_memory_bytes_sector*(memoryType: MEMORYTYPE): uint64` providing
The number of usable memory bytes for the specified memory type.

Limine memory map types map identically to the MEMORYTYPE enum values.

    #define LIMINE_MEMMAP_USABLE                 0
    #define LIMINE_MEMMAP_RESERVED               1
    #define LIMINE_MEMMAP_ACPI_RECLAIMABLE       2
    #define LIMINE_MEMMAP_ACPI_NVS               3
    #define LIMINE_MEMMAP_BAD_MEMORY             4
    #define LIMINE_MEMMAP_BOOTLOADER_RECLAIMABLE 5
    #define LIMINE_MEMMAP_EXECUTABLE_AND_MODULES 6
    #define LIMINE_MEMMAP_FRAMEBUFFER            7
    #define LIMINE_MEMMAP_RESERVED_MAPPED        8

]#
type
    MEMORYTYPE* = enum
        USABLE = 0
        RESERVED = 1
        ACPI_RECLAIMABLE = 2
        ACPI_NVS = 3
        BAD_MEMORY = 4
        BOOTLOADER_RECLAIMABLE = 5
        EXECUTABLE_AND_MODULES = 6
        FRAMEBUFFER = 7
        RESERVED_MAPPED = 8


proc memory_bytes_by_type(memoryType: uint64): uint64 {.importc: "limine_memory_bytes_by_type".}

#[
Returns the number of usable memory bytes for the specified memory type.

This is equivalent to calling 

    memory_bytes_by_type( uint64(ord(memoryType)) )

]#
proc usable_memory_bytes_sector*(memoryType: MEMORYTYPE): uint64 =
    memory_bytes_by_type(uint64(ord(memoryType)))


#[ 
Returns the number of usable memory bytes.
This is equivalent to calling:
    
    usable_memory_bytes_sector*(MEMORYTYPE.USABLE)
]#
proc usable_memory_bytes*(): uint64 =
    usable_memory_bytes_sector(MEMORYTYPE.USABLE)
