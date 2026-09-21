#include <stdint.h>
#include <limine.h>

#include "limine_requests.h"

#define PAGE_SIZE 4096

static uint64_t allocation_entry_index = 0;
static uint64_t allocation_address = 0;

void limine_allocator_reset(void) {
    allocation_entry_index = 0;
    allocation_address = 0;
}

struct allocation_state limine_get_allocation_state(void) {
    return (struct allocation_state) {
        .entry_index = allocation_entry_index,
        .address = allocation_address
    };
}

uint64_t limine_allocate_physical(uint64_t size) {
    if (memoryMapRequest.response == 0 || size == 0) {
        return 0;
    }

    if (size > UINT64_MAX - (PAGE_SIZE - 1)) {
        return 0;
    }

    size = (size + PAGE_SIZE - 1) & ~(PAGE_SIZE - 1);

    while (allocation_entry_index < memoryMapRequest.response->entry_count) {
        struct limine_memmap_entry *entry =
            memoryMapRequest.response->entries[allocation_entry_index];

        if (entry->type != LIMINE_MEMMAP_USABLE) {
            allocation_entry_index++;
            allocation_address = 0;
            continue;
        }

        uint64_t region_end = entry->base + entry->length;
        if (region_end < entry->base) {
            allocation_entry_index++;
            allocation_address = 0;
            continue;
        }

        uint64_t start = allocation_address;
        if (start < entry->base) {
            start = entry->base;
        }

        start = (start + PAGE_SIZE - 1) & ~(PAGE_SIZE - 1);

        if (start <= region_end && size <= region_end - start) {
            allocation_address = start + size;
            return start;
        }

        allocation_entry_index++;
        allocation_address = 0;
    }

    return 0;
}
