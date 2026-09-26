from toys.asm_tool.docs.instruction_catalog import (
    parse_c9x,
    parse_c9x_descriptions,
    parse_felix_cloutier,
    parse_felix_descriptions,
    render_markdown,
)


def test_parse_felix_cloutier_uses_instruction_links():
    html = """
    <a href="/x86/mov">MOV</a>
    <a href="/x86/add"><span>ADD</span></a>
    <a href="/x86/">index</a>
    <a href="/other/mov">MOV</a>
    """

    assert parse_felix_cloutier(html) == {"ADD", "MOV"}


def test_parse_c9x_uses_instruction_pages_and_normalises_names():
    html = """
    <a href="html/file_module_x86_id_1.html">mov</a>
    <a href="html/file_module_x86_id_2.html#flags">MOV</a>
    <a href="html/file_module_x86_id_3.html">3DNow!</a>
    <a href="html/other.html">ignore</a>
    """

    assert parse_c9x(html) == {"MOV", "3DNOW!"}


def test_render_markdown_is_a_flat_list():
    from toys.asm_tool.docs.instruction_catalog import Instruction

    markdown = render_markdown([Instruction("ADD", "Add values."), Instruction("MOV", "Move data.")])

    assert "- **ADD**: Add values.\n- **MOV**: Move data." in markdown
    assert "[" not in markdown
    assert "##" not in markdown


def test_parse_felix_descriptions_uses_the_second_table_cell():
    html = """
        <table>
            <tr><td><a href="/x86/mov"><span>MOV</span></a></td><td>Move</td></tr>
        </table>
    """

    assert parse_felix_descriptions(html) == {"MOV": "Move"}


def test_parse_c9x_descriptions_uses_the_second_table_cell():
    html = """
        <table>
            <tr>
                <td><a href="html/file_module_x86_id_1.html">MOV</a></td>
                <td>Move</td>
            </tr>
        </table>
    """

    assert parse_c9x_descriptions(html) == {"MOV": "Move"}