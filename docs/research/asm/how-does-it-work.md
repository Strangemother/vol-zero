# How Does It Work?

When writing to the tool - through the reg or asm interfaces - you are essentially generating assembly instructions that will be executed by the underlying system. The tool is designed to "emit" instructions. 
The instructions are destined to an asm file, which can then be assembled and executed by the system.

When writing to an object, the instructions are written to a output list, cached during compilation and _drained_ to the file.
Fundamentally, it's a literal transpiler and _could_ write immediately to a file. However, caching instructions allows for optimizations and better control over the output.

```py
# Example of writing to the tool
asm.eax = 1
asm.eax += 2
```

Under the hood this will create an intermediate representation:

```
Instructions(
    ...
    Mov("eax", 1),
    Add("eax", 2)
    ...
)
```

Resulting in:

```asm
mov eax, 1
add eax, 2
```