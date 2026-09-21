+ A block on content stored with an inline label

section .data
    labelThing db "some string", 10, 0
    len equ $ - labelThing
    # could hard code string length.
    len equ 40

    otherLabelThing db "some string", 10, 0
    len2 equ $ - otherLabelThing

Same can be done with 'segment'
