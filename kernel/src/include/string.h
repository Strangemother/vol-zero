/* Freestanding declarations for the memory routines supplied by the kernel. */
#ifndef __VOL_KERNEL_STRING_H
#define __VOL_KERNEL_STRING_H 1

#include <stddef.h>

void *memcpy(void *destination, void *source, size_t size);
void *memset(void *destination, int value, size_t size);
void *memmove(void *destination, void *source, size_t size);
int memcmp(void *first, void *second, size_t size);

#endif