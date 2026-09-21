import pytest

from lat import ASM, Immediate, Reader, Registers


def render_mov(build):
    asm = ASM()
    build(asm)
    return Reader(asm).flat_resolve()


class TestCurrentMovAPI:
    def test_positional_register_operands(self):
        registers = Registers()

        output = render_mov(lambda asm: asm.mov(registers.eax, 10))

        assert output == "mov eax, 10"

    def test_positional_string_operands(self):
        output = render_mov(lambda asm: asm.mov("eax", 10))

        assert output == "mov eax, 10"

    def test_named_value_and_into_with_string_destination(self):
        output = render_mov(lambda asm: asm.mov(value=10, into="eax"))

        assert output == "mov eax, 10"

    def test_named_value_and_into_with_register_destination(self):
        registers = Registers()

        output = render_mov(lambda asm: asm.mov(value=10, into=registers.eax))

        assert output == "mov eax, 10"

    def test_named_form_preserves_zero_immediate(self):
        output = render_mov(lambda asm: asm.mov(value=0, into="eax"))

        assert output == "mov eax, 0"

    def test_register_to_register_move(self):
        registers = Registers()

        output = render_mov(lambda asm: asm.mov(registers.eax, registers.edx))

        assert output == "mov eax, edx"


class TestFutureMovAPI:
    # @pytest.mark.skip(reason="Future keyword alias: to")
    def test_value_with_to_alias(self):
        registers = Registers()

        output = render_mov(lambda asm: asm.mov(10, to=registers.eax))

        assert output == "mov eax, 10"

    # @pytest.mark.skip(reason="Future canonical keyword API: destination/source")
    def test_destination_and_source_keywords(self):
        output = render_mov(
            lambda asm: asm.mov(destination="eax", source=10),
        )

        assert output == "mov eax, 10"

    def test_array_typed_memory_with_register(self):
        registers = Registers()
        output = render_mov(
            lambda asm: asm.mov([registers.eax], 10),
        )

        assert output == "mov [eax], 10"

    def test_typed_memory_only(self):
        from lat import Memory

        output = render_mov(
            lambda asm: asm.mov(Memory("eax"), 10),
        )

        assert output == "mov [eax], 10"

    def test_typed_memory_and_immediate_operands(self):
        from lat import Memory

        output = render_mov(
            lambda asm: asm.mov(Memory("eax"), Immediate(10)),
        )

        assert output == "mov [eax], 10"

    def test_immediate_preserves_source_spelling(self):
        output = render_mov(lambda asm: asm.mov("eax", Immediate("1010b")))

        assert output == "mov eax, 1010b"

    @pytest.mark.skip(reason="Future register convenience API: set")
    def test_register_set_convenience(self):
        registers = Registers()

        output = render_mov(lambda asm: registers.eax.set(10))

        assert output == "mov eax, 10"

    @pytest.mark.skip(reason="Future register convenience API: mov")
    def test_register_mov_convenience(self):
        registers = Registers()

        output = render_mov(lambda asm: registers.eax.mov(10))

        assert output == "mov eax, 10"

    @pytest.mark.skip(reason="Future parser API")
    def test_parse_mov_text(self):
        asm = ASM()
        operation = asm.parse("mov eax, 10")

        assert operation.opcode == "mov"
        assert operation.destination == "eax"
        assert operation.source == 10

    @pytest.mark.skip(reason="Future target renderer API")
    def test_render_mov_as_att(self):
        registers = Registers()
        asm = ASM()
        operation = asm.mov(registers.eax, 10)

        assert operation.string("at&t") == "movl $10, %eax"
