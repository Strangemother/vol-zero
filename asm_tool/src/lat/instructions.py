"""Instruction objects and assembly line resolution."""


class Instruction:
    """Record a named instruction when called."""

    delim = ", "

    def __init__(self, asm, name):
        self.asm = asm
        self.name = name

    def resolve(self, args, kwargs):
        dest_keys = ['destination', 
                    'dest', 'into', 
                    'to', 'register', 
                    'reg'
                ]
        source_keys = ['source', 'value', 'from']

        def get_from_kwargs(keys, kwargs):
            for key in keys:
                if key in kwargs:
                    return kwargs[key]
            return None
        if len(args) == 2:
            # mov(EAX, 2)
            into, value = args
        elif len(args) == 1:
            # mov(1, into)
            value = args[0]
            into = get_from_kwargs(dest_keys, kwargs)
            print(f"Resolved into: {into}, value: {value}")
        elif len(args) == 0:
            # dict types
            # mov(destination=X, source=X), add(value=X, into=X) ...
            into = get_from_kwargs(dest_keys, kwargs)
            value = get_from_kwargs(source_keys, kwargs)
            
        r = []
        for operand in [into, value]:
            if operand is not None:
                r.append(operand)
        args = r
        # if no arguments were provided, return just the instruction name
        # print(f"Final resolved args: {args}")
        if not args:
            return self.name
        return f"{self.name} " + self.delim.join(map(str, args))

    def emit(self, *args, **kwargs):
        self.asm.instruction_entry(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        bound_operands = getattr(self, "bound_operands", ())
        self.emit(*bound_operands, *args, **kwargs)
        return self


class RawInstruction(Instruction):
    """Emit a caller-supplied assembly line without formatting it."""

    name = "raw"

    def resolve(self, args, kwargs):
        return args[0] if args else ""
