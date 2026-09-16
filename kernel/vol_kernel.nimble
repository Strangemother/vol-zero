import os

let kernelVersion = readFile("VERSION").strip()
if kernelVersion.len == 0:
  quit "VERSION must not be empty"

version = kernelVersion
author = "VOL kernel"
description = "Freestanding VOL kernel build task"
license = "MIT"

const nimFlags = "c --noLinking --noMain --mm:none --os:standalone --cpu:amd64 " &
  "-d:release --checks:off --hints:off --warnings:off " &
  # Keep the generated C freestanding and compatible with the kernel ABI.
  "--passC:\"-ffreestanding -fno-stack-protector -fno-stack-check " &
  "-fno-pic -fno-lto -mno-red-zone -mno-sse -mno-sse2 -m64 " &
  "-mabi=sysv -mcmodel=kernel\" " &
  # These headers are needed when Nim emits C that uses freestanding types.
  "--passC:\"-I src/include -I limine-protocol/include -I freestanding-c-hdrs/include\""

# There is intentionally no passL option: --noLinking leaves the final link
# to GNUmakefile, which invokes ld with the Limine linker script.

# Compile the freestanding Nim source and copy its generated object to Make's target.
task buildKernel, "Build the freestanding VOL kernel module":
  let nim = getEnv("NIM", "nim")
  let source = getEnv("NIM_SOURCE", "src/main.nim")
  let nimcache = getEnv("NIMCACHE")
  let output = getEnv("NIM_OUTPUT")
  if nimcache.len == 0 or output.len == 0:
    quit "NIMCACHE and NIM_OUTPUT must be provided"

  # Avoid linking stale objects after modules are moved or renamed.
  exec "rm -rf " & quoteShell(nimcache)
  exec nim & " " & nimFlags & " --define:freestanding --define:kernelVersion=" & kernelVersion &
    " --nimcache:\"" & nimcache & "\" " & source

  # Nim emits one C object per module. Collect every generated object so new
  # imports do not require a corresponding linker-list update here.
  var objects = ""
  for objectPath in walkDirRec(nimcache):
    if objectPath.endsWith(".o"):
      if objects.len > 0:
        objects.add(" ")
      objects.add(quoteShell(objectPath))
  if objects.len == 0:
    quit "No Nim object files were generated in " & nimcache
  exec "ld -r -o " & quoteShell(output) & " " & objects

# Compile the hosted development entry point with Nim's normal runtime.
task buildHosted, "Build the hosted VOL development program":
  let nim = getEnv("NIM", "nim")
  let output = getEnv("HOSTED_OUTPUT", "../dist/vol-hosted")
  exec nim & " c --mm:orc --define:kernelVersion=" & kernelVersion &
    " --out:" & quoteShell(output) & " src/hosted_main.nim"
