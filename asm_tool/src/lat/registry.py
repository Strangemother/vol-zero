"""Register values used as assembly operands."""

from .instructions import Instruction

class Register:
    """Represent a single CPU register.

        reg = Register('EAX')
        reg.name == 'eax'
    """

    def __init__(self, name, parent=None):
        self.name = name
        self.instructions = {}
        self.parent = parent
  
    def __repr__(self):
        return self.name.lower()
    
    def __getattr__(self, name):
        """Dynamically handle attribute access for instructions.

            reg = Register('EAX')
            reg.mov(20)
        """
        instruction_class = self.get_instruction_class(name)
        owner = self
        if self.parent is not None and self.parent.asm is not None:
            owner = self.parent.asm
        instruction = instruction_class(owner, name)
        instruction.bound_operands = (self,)
        return instruction
  
    def get_instruction_class(self, name):
        instr = self.instructions.get(name)
        if instr is not None:
            return instr
        # if self.parent is not None and self.parent is not self:
        #     return self.parent.get_instruction_class(name)
        return Instruction
    
class Memory:
    """Represent a memory operand, typically used with square brackets."""

    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return f"[{self.address}]"


class Immediate:
    """Represent a literal operand without changing its source spelling."""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class Registers:
    """Lazily create register operands by attribute access."""
    asm = None 
    
    def __init__(self, asm=None):
        self._registers = {}
        self.asm = asm

    def __getattr__(self, name):
        register_name = name.lower()
        if register_name not in self._registers:
            self._registers[register_name] = Register(name, parent=self)
        return self._registers[register_name]
    
    # def get_instruction_class(self, name):
    #     if self.asm is not None:
    #         return self.asm.get_instruction_class(name)
    #     return Instruction