# Nuke built-in rules.
.SUFFIXES:

# Delete the target of a failed recipe.
.DELETE_ON_ERROR:

# Default user QEMU flags. These are appended to the QEMU command calls.
QEMUFLAGS := -m 2G

# Internal QEMU flags that should not be changed by the user.
override QEMU_MACHINE_FLAGS := \
    -M q35
override QEMU_UEFI_FLAGS := \
    -drive if=pflash,unit=0,format=raw,file=edk2-ovmf-bins/ovmf-code-x86_64.fd,readonly=on

override DIST_DIR := dist
override KERNEL_VERSION := $(shell tr -d '\r\n' < kernel/VERSION)
override ISO_FILENAME := $(shell python3 tools/dist_iso_filename.py)
override HDD_FILENAME := $(shell python3 tools/dist_hdd_filename.py)
override ISO_IMAGE := $(DIST_DIR)/$(ISO_FILENAME)
override HDD_IMAGE := $(DIST_DIR)/$(HDD_FILENAME)

# User controllable size of the HDD image, in MiB.
HDD_SIZE := 64

# Internal HDD geometry that should not be changed by the user. Older mtools
# require one; 64 heads of 32 sectors make a cylinder exactly 1 MiB in size.
override HDD_HEADS := 64
override HDD_SECTORS_PER_TRACK := 32
override HDD_CYLINDER_SECTORS := $(shell echo $$(( $(HDD_HEADS) * $(HDD_SECTORS_PER_TRACK) )))

# Internal HDD partition layout that should not be changed by the user. sgdisk
# lays the partition out as GPT before converting the table to MBR, so the
# first and last cylinders are left to the GPT structures.
override HDD_PART_START := $(HDD_CYLINDER_SECTORS)
override HDD_PART_SECTORS := $(shell echo $$(( ($(HDD_SIZE) - 2) * $(HDD_CYLINDER_SECTORS) )))
override HDD_PART_END := $(shell echo $$(( $(HDD_PART_START) + $(HDD_PART_SECTORS) - 1 )))
override HDD_PART_OFFSET := $(shell echo $$(( $(HDD_PART_START) * 512 )))

# Toolchain for building the 'limine' executable for the host.
HOST_CC := cc
HOST_CFLAGS := -g -O2 -pipe
HOST_CPPFLAGS :=
HOST_LDFLAGS :=
HOST_LIBS :=

.PHONY: all
all: $(ISO_IMAGE)

.PHONY: all-hdd
all-hdd: $(HDD_IMAGE)

.PHONY: run
run: $(ISO_IMAGE)
	qemu-system-x86_64 \
		$(QEMU_MACHINE_FLAGS) \
		-cdrom $(ISO_IMAGE) \
		-boot d \
		$(QEMUFLAGS)

.PHONY: run-uefi
run-uefi: edk2-ovmf-bins $(ISO_IMAGE)
	qemu-system-x86_64 \
		$(QEMU_MACHINE_FLAGS) \
		$(QEMU_UEFI_FLAGS) \
		-cdrom $(ISO_IMAGE) \
		-boot d \
		$(QEMUFLAGS)

.PHONY: run-hdd
run-hdd: $(HDD_IMAGE)
	qemu-system-x86_64 \
		$(QEMU_MACHINE_FLAGS) \
		-hda $(HDD_IMAGE) \
		$(QEMUFLAGS)

.PHONY: run-hdd-uefi
run-hdd-uefi: edk2-ovmf-bins $(HDD_IMAGE)
	qemu-system-x86_64 \
		$(QEMU_MACHINE_FLAGS) \
		$(QEMU_UEFI_FLAGS) \
		-hda $(HDD_IMAGE) \
		$(QEMUFLAGS)

.INTERMEDIATE: edk2-ovmf-bins.tar.gz
edk2-ovmf-bins.tar.gz:
	curl -fL -o $@ https://github.com/osdev0/edk2-ovmf-stable-bins/releases/latest/download/edk2-ovmf-bins.tar.gz

edk2-ovmf-bins: edk2-ovmf-bins.tar.gz
	rm -rf edk2-ovmf-bins
	gunzip < edk2-ovmf-bins.tar.gz | tar -xf -

.INTERMEDIATE: limine-binary.tar.gz
limine-binary.tar.gz:
	curl -fL -o $@ https://github.com/Limine-Bootloader/Limine/releases/latest/download/limine-binary.tar.gz

limine-binary/limine: limine-binary.tar.gz
	rm -rf limine-binary
	gunzip < limine-binary.tar.gz | tar -xf -
	$(MAKE) -C limine-binary \
		CC="$(HOST_CC)" \
		CFLAGS="$(HOST_CFLAGS)" \
		CPPFLAGS="$(HOST_CPPFLAGS)" \
		LDFLAGS="$(HOST_LDFLAGS)" \
		LIBS="$(HOST_LIBS)"

kernel/.deps-obtained:
	sh ./kernel/get-deps

.PHONY: kernel
kernel: kernel/.deps-obtained
	$(MAKE) -C kernel

$(ISO_IMAGE): limine-binary/limine kernel kernel/VERSION limine.conf
	mkdir -p $(DIST_DIR)
	rm -rf iso_root
	mkdir -p iso_root/boot
	cp -v kernel/bin/kernel iso_root/boot/
	mkdir -p iso_root/boot/limine
	sed 's/@VERSION@/$(KERNEL_VERSION)/g' limine.conf > iso_root/boot/limine/limine.conf
	cp -v limine-binary/limine-bios.sys limine-binary/limine-bios-cd.bin limine-binary/limine-uefi-cd.bin iso_root/boot/limine/
	mkdir -p iso_root/EFI/BOOT
	cp -v limine-binary/BOOTX64.EFI iso_root/EFI/BOOT/
	cp -v limine-binary/BOOTIA32.EFI iso_root/EFI/BOOT/
	xorriso -as mkisofs -R -r -J -b boot/limine/limine-bios-cd.bin \
		-no-emul-boot -boot-load-size 4 -boot-info-table -hfsplus \
		-apm-block-size 2048 --efi-boot boot/limine/limine-uefi-cd.bin \
		-efi-boot-part --efi-boot-image --protective-msdos-label \
		iso_root -o $(ISO_IMAGE)
	./limine-binary/limine bios-install $(ISO_IMAGE)
	rm -rf iso_root

$(HDD_IMAGE): limine-binary/limine kernel kernel/VERSION limine.conf
	mkdir -p $(DIST_DIR)
	rm -f $(HDD_IMAGE)
	dd if=/dev/zero bs=1024k count=0 seek=$(HDD_SIZE) of=$(HDD_IMAGE)
	PATH=$$PATH:/usr/sbin:/sbin sgdisk $(HDD_IMAGE) -n 1:$(HDD_PART_START):$(HDD_PART_END) -t 1:ef00 -m 1
	./limine-binary/limine bios-install $(HDD_IMAGE)
	mformat -i $(HDD_IMAGE)@@$(HDD_PART_OFFSET) -T $(HDD_PART_SECTORS) -h $(HDD_HEADS) -s $(HDD_SECTORS_PER_TRACK) ::
	mmd -i $(HDD_IMAGE)@@$(HDD_PART_OFFSET) ::/EFI ::/EFI/BOOT ::/boot ::/boot/limine
	mcopy -i $(HDD_IMAGE)@@$(HDD_PART_OFFSET) kernel/bin/kernel ::/boot
	sed 's/@VERSION@/$(KERNEL_VERSION)/g' limine.conf > /tmp/limine.conf
	mcopy -i $(HDD_IMAGE)@@$(HDD_PART_OFFSET) /tmp/limine.conf limine-binary/limine-bios.sys ::/boot/limine
	rm -f /tmp/limine.conf
	mcopy -i $(HDD_IMAGE)@@$(HDD_PART_OFFSET) limine-binary/BOOTX64.EFI ::/EFI/BOOT
	mcopy -i $(HDD_IMAGE)@@$(HDD_PART_OFFSET) limine-binary/BOOTIA32.EFI ::/EFI/BOOT

.PHONY: clean
clean:
	$(MAKE) -C kernel clean
	rm -rf iso_root $(DIST_DIR)

.PHONY: distclean
distclean: clean
	$(MAKE) -C kernel distclean
	rm -rf limine-binary limine-binary.tar.gz edk2-ovmf-bins edk2-ovmf-bins.tar.gz
