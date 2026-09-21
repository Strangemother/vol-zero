#ifndef VOL_KERNEL_LIMINE_REQUESTS_H
#define VOL_KERNEL_LIMINE_REQUESTS_H 1

#include <stdint.h>
#include <limine.h>

extern volatile uint64_t limineBaseRevision[];
extern volatile struct limine_hhdm_request hhdmRequest;
extern volatile struct limine_framebuffer_request framebufferRequest;
extern volatile struct limine_flanterm_fb_init_params_request flantermRequest;
extern volatile struct limine_memmap_request memoryMapRequest;
extern volatile struct limine_tsc_frequency_request tscFrequencyRequest;
extern volatile struct limine_date_at_boot_request dateAtBootRequest;

struct allocation_state {
    uint64_t entry_index;
    uint64_t address;
};

uint64_t limine_hhdm_offset(void);
uint64_t limine_hhdm_available(void);
uint64_t limine_allocate_physical(uint64_t size);

#endif
