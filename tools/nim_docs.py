#!/usr/bin/env python3
"""Extract project documentation blocks and declarations from Nim source files.

This is intentionally a lightweight source parser, not a full Nim compiler. It
keeps the project's ``#[ ... ]#`` documentation style and associates each block
with the next declaration at the same or a deeper indentation level.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


DECLARATION_RE = re.compile(
    r"^(?P<indent>\s*)(?P<kind>proc|func|method|iterator|template|macro|converter|"
    r"type|const|var|let|const\s+|concept)\b(?P<rest>.*)$"
)
NAME_RE = re.compile(r"^\s*(?P<name>[A-Za-z_][A-Za-z0-9_']*)(?P<export>\*)?")
DEPENDENCY_RE = re.compile(
    r"^(?P<name>.+?)(?:\s+as\s+(?P<alias>[A-Za-z_][A-Za-z0-9_']*))?$"
)


@dataclass
class NimDeclaration:
    """A declaration and the documentation block attached to it."""

    kind: str
    name: str
    exported: bool
    signature: str
    documentation: str
    line: int


@dataclass
class NimDependency:
    """An import or include target referenced by a Nim module."""

    name: str
    alias: str | None
    filename: str
    line: int


@dataclass
class NimModule:
    """Documentation metadata extracted from one Nim module."""

    path: str
    module_name: str
    declarations: list[NimDeclaration] = field(default_factory=list)
    imports: list[NimDependency] = field(default_factory=list)
    includes: list[NimDependency] = field(default_factory=list)
    file_documentation: str = ""

    @property
    def public_declarations(self) -> list[NimDeclaration]:
        return [declaration for declaration in self.declarations if declaration.exported]

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["public_declarations"] = [asdict(item) for item in self.public_declarations]
        return result


@dataclass
class DocumentationBlock:
    text: str
    end_line: int


def _clean_documentation(lines: Iterable[str]) -> str:
    cleaned = [line.rstrip() for line in lines]
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    return "\n".join(cleaned)


def _read_block_comment(lines: list[str], start: int) -> tuple[DocumentationBlock, int]:
    first = lines[start]
    content = first.split("#[", 1)[1]
    collected: list[str] = []
    if "]#" in content:
        body, _ = content.split("]#", 1)
        collected.append(body)
        return DocumentationBlock(_clean_documentation(collected), start + 1), start + 1

    collected.append(content)
    index = start + 1
    while index < len(lines):
        line = lines[index]
        if "]#" in line:
            body, _ = line.split("]#", 1)
            collected.append(body)
            return DocumentationBlock(_clean_documentation(collected), index + 1), index + 1
        collected.append(line)
        index += 1
    raise ValueError(f"Unclosed #[ documentation block at line {start + 1}")


def _read_line_comments(lines: list[str], start: int) -> tuple[DocumentationBlock, int]:
    collected: list[str] = []
    index = start
    while index < len(lines) and lines[index].lstrip().startswith("##"):
        line = lines[index].lstrip()[2:]
        if line.startswith(" "):
            line = line[1:]
        collected.append(line.rstrip())
        index += 1
    return DocumentationBlock(_clean_documentation(collected), index), index


def _declaration_header(lines: list[str], start: int) -> str:
    """Collect a declaration signature through a Nim line continuation."""

    first = lines[start].strip()
    header = [first]
    balance = 0
    for character in first:
        if character in "([{":
            balance += 1
        elif character in ")]}":
            balance = max(0, balance - 1)

    index = start + 1
    while index < len(lines):
        current = lines[index]
        stripped = current.strip()
        if not stripped:
            break
        if balance == 0 and (current[:1].isspace() is False or stripped.startswith("#")):
            break
        if balance == 0 and "=" in header[-1]:
            break
        header.append(stripped)
        for character in stripped:
            if character in "([{":
                balance += 1
            elif character in ")]}":
                balance = max(0, balance - 1)
        index += 1
        if balance == 0 and ("=" in stripped or stripped.endswith(":") is False):
            break
    return " ".join(header)


def _parse_declaration(
    lines: list[str], index: int, *, allow_indented: bool = False
) -> NimDeclaration | None:
    # Module documentation describes module-level symbols. Indented `let`,
    # `var`, and object fields belong to the surrounding declaration or proc.
    if not allow_indented and lines[index].startswith((" ", "\t")):
        return None

    match = DECLARATION_RE.match(lines[index])
    if match is None:
        return None

    kind = match.group("kind").strip()
    rest = match.group("rest")
    name_match = NAME_RE.match(rest)
    if name_match is None:
        return None

    name = name_match.group("name")
    exported = bool(name_match.group("export"))
    signature = _declaration_header(lines, index)
    return NimDeclaration(
        kind=kind,
        name=name,
        exported=exported,
        signature=signature,
        documentation="",
        line=index + 1,
    )


def _directive_header(lines: list[str], start: int) -> str:
    """Collect an import/include statement spanning comma or bracket lines."""

    header = [lines[start].strip()]
    balance = 0
    for character in header[0]:
        if character in "([{":
            balance += 1
        elif character in ")]}":
            balance = max(0, balance - 1)

    index = start + 1
    while index < len(lines) and (balance > 0 or header[-1].rstrip().endswith(",")):
        current = lines[index].strip()
        if not current or current.startswith("#"):
            break
        header.append(current)
        for character in current:
            if character in "([{":
                balance += 1
            elif character in ")]}":
                balance = max(0, balance - 1)
        index += 1
    return " ".join(header)


def _split_dependency_names(value: str) -> list[str]:
    names: list[str] = []
    current: list[str] = []
    balance = 0
    for character in value:
        if character in "([{":
            balance += 1
        elif character in ")]}":
            balance = max(0, balance - 1)
        if character == "," and balance == 0:
            names.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    if current:
        names.append("".join(current).strip())
    return [name for name in names if name]


def _dependency_entries(value: str, line: int) -> list[NimDependency]:
    entries: list[NimDependency] = []
    for item in _split_dependency_names(value):
        match = DEPENDENCY_RE.match(item)
        if match is None:
            continue
        name = match.group("name").strip()
        alias = match.group("alias")
        grouped_match = re.fullmatch(r"(?P<prefix>[^[]+)/\[(?P<names>[^]]+)\]", name)
        names = _split_dependency_names(grouped_match.group("names")) if grouped_match else [name]
        for grouped_name in names:
            dependency_name = (
                f"{grouped_match.group('prefix').rstrip('/')}/{grouped_name}"
                if grouped_match
                else grouped_name
            )
            entries.append(
                NimDependency(
                    name=dependency_name,
                    alias=alias,
                    filename=f"{dependency_name}.nim",
                    line=line,
                )
            )
    return entries


def parse_nim_source(path: str | Path) -> NimModule:
    """Extract documentation blocks and declarations from a Nim source file."""

    source_path = Path(path)
    lines = source_path.read_text(encoding="utf-8").splitlines()
    module = NimModule(path=source_path.as_posix(), module_name=source_path.stem)
    pending: DocumentationBlock | None = None
    conditional_indent: int | None = None
    index = 0

    if lines and lines[0].strip().startswith("#["):
        first_comment, comment_end = _read_block_comment(lines, 0)
        if comment_end > 1:
            module.file_documentation = first_comment.text
            index = comment_end
    elif lines and lines[0].strip().startswith("##"):
        first_comment, comment_end = _read_line_comments(lines, 0)
        if comment_end > 1:
            module.file_documentation = first_comment.text
            index = comment_end

    while index < len(lines):
        stripped = lines[index].strip()
        indentation = len(lines[index]) - len(lines[index].lstrip())
        if stripped.startswith("#["):
            pending, index = _read_block_comment(lines, index)
            continue
        if stripped.startswith("##"):
            pending, index = _read_line_comments(lines, index)
            continue

        directive_match = re.match(r"^(import|include)\s+(.+)$", stripped)
        if directive_match is not None:
            dependencies = _dependency_entries(
                _directive_header(lines, index).split(None, 1)[1], index + 1
            )
            if directive_match.group(1) == "import":
                module.imports.extend(dependencies)
            else:
                module.includes.extend(dependencies)
            index += 1
            continue

        if stripped.startswith("when ") and indentation == 0:
            conditional_indent = indentation
            index += 1
            continue

        if (
            conditional_indent is not None
            and stripped
            and indentation <= conditional_indent
        ):
            is_conditional_branch = indentation == conditional_indent and (
                stripped.startswith("else") or stripped.startswith("elif")
            )
            if not is_conditional_branch:
                conditional_indent = None

        declaration = _parse_declaration(
            lines,
            index,
            allow_indented=conditional_indent is not None,
        )
        if declaration is not None:
            if pending is not None:
                declaration.documentation = pending.text
                pending = None
            module.declarations.append(declaration)
        elif stripped and not stripped.startswith("#"):
            pending = None
        index += 1

    return module


def parse_paths(paths: Iterable[str | Path]) -> list[NimModule]:
    """Parse several Nim files in order."""

    return [parse_nim_source(path) for path in paths]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Nim files to parse")
    parser.add_argument("--json", action="store_true", help="write JSON instead of a summary")
    parser.add_argument("--pretty", action="store_true", help="indent JSON output")
    return parser


def main() -> int:
    arguments = _build_parser().parse_args()
    modules = parse_paths(arguments.paths)
    if arguments.json:
        payload: object = modules[0].to_dict() if len(modules) == 1 else [module.to_dict() for module in modules]
        print(json.dumps(payload, indent=2 if arguments.pretty else None))
        return 0

    for module in modules:
        print(f"{module.module_name}: {len(module.declarations)} declarations")
        for declaration in module.declarations:
            visibility = "public" if declaration.exported else "private"
            documented = "documented" if declaration.documentation else "undocumented"
            print(f"  {declaration.line}: {visibility} {declaration.kind} {declaration.name} ({documented})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
