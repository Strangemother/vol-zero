# Coding Conventions

This document outlines the coding conventions followed in the Vol-Zero project. 

[TOC]

## Indentation

- Use 4 spaces per indentation level.
- Do not use tabs for indentation.

## Naming Conventions

- Use `snake_case` for variable and function names.
- Use `CamelCase` for type names.
- Use `ALL_CAPS` for macros and constants.


## Root-Level Procs

Any proc defined at the root level of a module should spaced two lines apart from other procs.

```nim
proc example*(): uint64 {.importc: "my_export_example".}


proc another*(): uint64 {.importc: "my_export_thing".}


proc write_line*(message: cstring) =
    write(message)
    write("\r\n")

```

