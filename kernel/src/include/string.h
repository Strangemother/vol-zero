/* Freestanding declarations for the memory routines supplied by the kernel. */
#ifndef __VOL_KERNEL_STRING_H
#define __VOL_KERNEL_STRING_H 1

#include <stddef.h>

#ifndef NIM_INTBITS
void *memcpy(void *restrict destination, const void *restrict source, size_t size);
void *memset(void *destination, int value, size_t size);
void *memmove(void *destination, const void *source, size_t size);
int memcmp(const void *first, const void *second, size_t size);
#endif

#endif