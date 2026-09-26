"""Assembly program recording and dynamic instruction access."""

from .instructions import Instruction


class ASM:
    """Record assembly instructions in source order."""

    def __init__(self):
        self._lines = []
        self.instructions = {}

    def install_instruction(self, instruction, name=None):
        """Register an instruction class for a mnemonic."""
        instruction_name = name or instruction.name
        self.instructions[instruction_name] = instruction

    def instruction_entry(self, item, *args, **kwargs):
        print((item, args, kwargs))
        self._lines.append((item, args, kwargs))

    def __getattr__(self, name):
        instruction_class = self.get_instruction_class(name)
        return instruction_class(name, asm=self)

    def get_instruction_class(self, name):
        instr = self.instructions.get(name)
        if instr is None:
            return Instruction
        return instr