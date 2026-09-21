A simple example usecase to make some ASM:

    section .text
       global _start     ;must be declared for linker (ld)

    _start:             ;tells linker entry point
       mov  edx,len     ;message length
       mov  ecx,msg     ;message to write
       mov  ebx,1       ;file descriptor (stdout)
       mov  eax,4       ;system call number (sys_write)
       int  0x80        ;call kernel

       mov  eax,1       ;system call number (sys_exit)
       int  0x80        ;call kernel

    section .data
    msg db 'Hello, world!', 0xa  ;string to be printed
    len equ $ - msg     ;length of the string

it mat be define literally, but that's no better than ASM

    asm.section('text')
    asm.global(_start')     #must be declared for linker (ld)

    asm.label('_start')
    asm.mov(edx,len)   # message length
    asm.mov(ecx,msg)   # message to write
    asm.mov(ebx,1)   # file descriptor (stdout)
    asm.mov(eax,4)   # system call number (sys_write)
    asm.int(0x80)   # call kernel

    asm.mov(eax, 1)     # system call number (sys_exit)
    asm.int(0x80)   # call kernel

    asm.section('data')
    asm.db('Hello, world!', 0xa  label='msg') # string to be printed
    asm.equ("$ - msg", label='len') # length of the string


With sugar:


    def main():
        with asm.section.text:
           asm.global('_start')

        start()

        with asm.section.data:                    # section .data
            msg = asm.db('msg', 'Hello World')    # msg db 'Hello, world!', 0xa  #string to be printed
            asm.equ('len', asm.$, asm.sub, msg)   # len equ $ - msg     ;length of the string
            # asm.equ('len', f"$ - {msg}")

    def start():

        with asm.label('_start') as _s:     # tells linker entry point
           reg.edx = len                    # mov  edx,len     # message length
           reg.ecx = msg                    # mov  ecx,msg     # message to write
           reg.ebx = 1                      # mov  ebx,1       # file descriptor (stdout)
           reg.eax = 4                      # mov  eax,4       # system call number (sys_write)
           asm.int(128)                     # int  0x80        # call kernel
           reg.eax = 1                      # mov  eax,1       # system call number (sys_exit)
           asm.int(128)                     # int  0x80        # call kernel


A better future scope:

        import asm
        reg = asm.Register('x64')

        @asm.label                          # with asm.label('_start') as _s:
        def _start(name='msg'):             # tells linker entry point
           reg.edx = 'len'                  # mov  edx,len     # message length
           reg.ecx = name                   # mov  ecx,msg     # message to write
           reg.ebx = 1                      # mov  ebx,1       # file descriptor (stdout)
           reg.eax = 4                      # mov  eax,4       # system call number (sys_write)
           asm.interrupt.kernel()           # int  0x80        # call kernel
           reg.eax = 1                      # mov  eax,1       # system call number (sys_exit)
           asm.interrupt.kernel()           # int  0x80        # call kernel

        @asm.section.text
        def text_section():
            asm.global(_start)


        @asm.section.data
        def my_data_section():
            hw = asm.db('msg', 'Hello World')   # msg db 'Hello, world!', 0xa  ;string to be printed
            asm.equ.len = asm.last - hw         # len equ $ - msg     ;length of the string


---

        import asm
        reg = asm.Register('x64')
        sec = asm.section

        def main():
            my_section(sec.data)
            asm.ordered_write(sec.text, _start, sec.data)

        def my_section(data):
            data.msg = 'Hello World'             # # msg db 'Hello, world!', 0xa
            data.len = asm.equ(asm.$ - data.msg) # len equ $ - msg

        @asm.global(sec.text)
        def _start(name='msg'):             # tells linker entry point # with asm.label('_start')
           reg.edx = sec.data.len           # mov  edx,len     # message length
           reg.ecx = name                   # mov  ecx,msg     # message to write
           reg.ebx = 1                      # mov  ebx,1       # file descriptor (stdout)
           reg.eax = 4                      # mov  eax,4       # system call number (sys_write)
           asm.interrupt.kernel()           # int  0x80        # call kernel
           reg.eax = 1                      # mov  eax,1       # system call number (sys_exit)
           asm.interrupt.kernel()           # int  0x80        # call kernel

the global receives a place to write.. As global defines a section, the function is written as a section global can call. In ordered_write stage, the start values are printed to the file after the text section.

        @asm.global(sec.text)

add the incoming function as a `global func_name` statement with the `asm.section.text`. This is held in the until write time. when written the compiler will write the `section .text` section automatically; as it has an attached `global` statement.

It's possible to break the application through automation here; as nothing notes the `_start_` function and its content should be applied to the code. Indeed a _magic_ check of all statements, noting global needs a function and the function is named on the compiler stack. But assuming a block should be written may yield later problems.

As such an explicit method should be applied in the code - or another decorator.

        @asm.global(sec.text)
        @asm.label(write_here=True)
        def _start(name='msg'):
            ...

being a label, it should also write to space, unless explicity defined elsewhere.

A better ordered scope:

        import asm
        reg = asm.Register()

        def main():
            d=asm.section.data
            vitem = d.db('vers', 'version 1.0')
            d.len = asm.last - vitem

            ordered = asm.compile(
                    asm.section.text(),
                    _start(vers),
                    # _start('vers'),
                    asm.section.data(),
                )
            ordered.write('hello.asm')
            # asm.write('hello.asm')

