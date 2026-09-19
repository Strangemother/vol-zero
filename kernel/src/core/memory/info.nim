#[
Provides functions and constants for querying memory information.

This module interfaces with the Limine bootloader to retrieve memory
information, including usable memory and memory categorized by type.
]#

#[

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



const
    memoryTypeUsable* = 0
    memoryTypeReserved* = 1
    memoryTypeAcpiReclaimable* = 2
    memoryTypeAcpiNvs* = 3
    memoryTypeBadMemory* = 4
    memoryTypeBootloaderReclaimable* = 5
    memoryTypeExecutableAndModules* = 6
    memoryTypeFramebuffer* = 7
    memoryTypeReservedMapped* = 8


proc memory_bytes_by_type(memoryType: uint64): uint64 {.importc: "limine_memory_bytes_by_type".}

proc usable_memory_bytes_sector*(memoryType: int): uint64 =
    memory_bytes_by_type(uint64(memoryType))

proc usable_memory_bytes*(): uint64 =
    usable_memory_bytes_sector(memoryTypeUsable)
