from lat import ASM, RawInstruction, Reader, Registers


class TestInstructionRecording:
    def test_zero_argument_instructions(self):
        asm = ASM()
        asm.hlt()
        asm.pusha()
        asm.again()

        assert Reader(asm).flat_resolve() == "hlt\npusha\nagain"

    def test_instruction_arguments_preserve_order(self):
        asm = ASM()
        asm.mov("eax", 1)
        asm.add("eax", "edx")
        asm.ret()

        assert Reader(asm).flat_resolve() == "mov eax, 1\nadd eax, edx\nret"

    def test_named_operands_render_as_destination_and_source(self):
        asm = ASM()
        asm.mov(value=10, into="eax")

        assert Reader(asm).flat_resolve() == "mov eax, 10"

    def test_reader_exposes_resolved_lines_and_count(self):
        asm = ASM()
        asm.nop()
        asm.ret()
        reader = Reader(asm)

        assert reader.flat_resolve() == "nop\nret"
        assert reader.as_list() == ["nop", "ret"]
        assert reader.total == 2
        assert reader.resolved_lines == "nop\nret"


class TestRawInstruction:
    def test_raw_instruction_preserves_text(self):
        asm = ASM()
        asm.install_instruction(RawInstruction)
        asm.raw("mov eax, 1")
        asm.raw("add $12, %eax")

        assert Reader(asm).flat_resolve() == "mov eax, 1\nadd $12, %eax"

    def test_raw_instruction_accepts_empty_input(self):
        asm = ASM()
        asm.install_instruction(RawInstruction)
        asm.raw()

        assert Reader(asm).flat_resolve() == ""


class TestRegisters:
    def test_registers_are_lazy_and_case_insensitive(self):
        registers = Registers()

        assert registers.eax is registers.EAX
        assert repr(registers.EAX) == "eax"

    def test_registers_render_as_instruction_operands(self):
        asm = ASM()
        registers = Registers()
        asm.pop(registers.BP)
        asm.ret()

        assert Reader(asm).flat_resolve() == "pop bp\nret"
