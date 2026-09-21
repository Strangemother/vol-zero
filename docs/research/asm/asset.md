An asset defines content to be applied through compile time, not at runtime or translation phase.

The source code is converted to a binary through ASM compilation. The original file steps through phases before final compilation.

+ source as `*.py`
    pre-parsed python based statements as source
+ execution phase
    The intial execution of the source generating a AST graph
+ translation phase
    A production of linear executions in graph state for injection and live-reading
+ ASM generation phase
    Create the finished .asm files
+ compiler phase
    convert the ASM to a binary using the chosen compiler
+ runtime
    run the appliction in its native state.

The runtime is the final binary build through the chosen ASM compiler. The ASM is applied through the terse translation of the source code.

An `asset` applies content such as text to "compile time" for the translation phase to read as standard executions. It may point to an external file with content apply into the asm:

    asm.db('message', "Welcome to the first message of th...")

convert to an assert for external appliance; the execution phase will collect an inject the asset accordingly.

    # message.txt
    Welcome to the first ...

    # asm.py
    asm.db('message', asset('assets/message.txt'))

You must consider the content applied to the asm operator - this does not fix data overflows.
