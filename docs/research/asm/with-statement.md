the python 'with' statement provides indentation to the written asm code, allowing for nested syntax such as `label` and `section`. Each asm module will utilise the with statmemt as required.

    with asm.section('.data'):
        asm.db('some string', 10, 0, label='myString')
        asm.equ('$', op.sub, 'myString', label='len'))

        otherLabelThing db "some string", 10, 0
        len2 equ $ - otherLabelThing

produces asm:

    section .data
        labelThing db "some string", 10, 0
        len equ $ - labelThing
        # len equ 40        # could hard code string length.
<!--
        otherLabelThing db "some string", 10, 0
        len2 equ $ - otherLabelThing
 -->
