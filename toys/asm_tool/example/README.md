# Assembly Example

This is a 32-bit Linux NASM example that reads an expression such as `2+3`.
The source currently operates on the input bytes directly, so `2+3` produces
the byte `e` rather than the printable number `5`.

## Setup

```bash
cd asm_tool/example
./install.sh
./compile.sh
```

## Run

```bash
./run.sh 2+3
```

The run script supplies the three input characters, limits execution to five
seconds, and prints a newline after the program's single-byte output.