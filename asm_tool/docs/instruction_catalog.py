"""Fetch, extract, and render instruction mnemonic catalogs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.request import Request, urlopen


FELIX_CLOUTIER_URL = "https://www.felixcloutier.com/x86/"
C9X_URL = "https://c9x.me/x86/"


@dataclass(frozen=True)
class Instruction:
    name: str
    description: str


class _RowParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[tuple[list[str], str | None]] = []
        self._cells: list[str] = []
        self._cell_text: list[str] = []
        self._cell_href: str | None = None
        self._row_href: str | None = None
        self._in_row = False
        self._in_cell = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self._in_row = True
            self._cells = []
            self._row_href = None
        elif tag == "td" and self._in_row:
            self._in_cell = True
            self._cell_text = []
            self._cell_href = None
        elif tag == "a" and self._in_cell:
            self._cell_href = dict(attrs).get("href")

    def handle_data(self, data: str) -> None:
        if self._in_cell:
            self._cell_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "td" and self._in_cell:
            self._cells.append((_normalise_description("".join(self._cell_text))))
            if len(self._cells) == 1:
                self._row_href = self._cell_href
            self._in_cell = False
        elif tag == "tr" and self._in_row:
            if self._cells:
                self.rows.append((self._cells, self._row_href))
            self._in_row = False


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a" and self._href is None:
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href is not None:
            self.links.append((self._href, "".join(self._text)))
            self._href = None


def _rows(html: str) -> list[tuple[list[str], str | None]]:
    parser = _RowParser()
    parser.feed(html)
    return parser.rows


def _links(html: str) -> list[tuple[str, str]]:
    parser = _LinkParser()
    parser.feed(html)
    return parser.links


def _normalise(value: str) -> str:
    return re.sub(r"\s+", "", value).upper()


def parse_felix_cloutier(html: str) -> set[str]:
    """Extract mnemonics from Felix Cloutier's x86 index page."""
    names = set()
    for href, text in _links(html):
        if href and text.strip() and re.fullmatch(r"/x86/([^/#?]+)", href):
            names.add(_normalise(href.rsplit("/", 1)[-1]))
    return names


def parse_c9x(html: str) -> set[str]:
    """Extract mnemonics from C9x's x86 index page."""
    names = set()
    for href, text in _links(html):
        if href and text.strip() and re.search(r"(?:^|/)html/file_module_x86_id_\d+\.html(?:$|#)", href):
            mnemonic = _normalise(text)
            if re.fullmatch(r"[A-Z0-9][A-Z0-9.!/_-]*", mnemonic):
                names.add(mnemonic)
    return names


def fetch(url: str, timeout: float = 30) -> str:
    request = Request(url, headers={"User-Agent": "vol-zero-instruction-catalog/1.0"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def _normalise_description(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def collect_instruction_names(
    felix_url: str = FELIX_CLOUTIER_URL,
    c9x_url: str = C9X_URL,
) -> list[str]:
    """Fetch both indexes and return one sorted, de-duplicated list."""
    return sorted(parse_felix_cloutier(fetch(felix_url)) | parse_c9x(fetch(c9x_url)))


def collect_instructions(
    felix_url: str = FELIX_CLOUTIER_URL,
    c9x_url: str = C9X_URL,
) -> list[Instruction]:
    """Fetch both index tables into a sorted catalog."""
    felix_html = fetch(felix_url)
    c9x_html = fetch(c9x_url)
    felix_descriptions = parse_felix_descriptions(felix_html)
    c9x_descriptions = parse_c9x_descriptions(c9x_html)
    entries = []
    for name in sorted(set(felix_descriptions) | set(c9x_descriptions)):
        description = felix_descriptions.get(name) or c9x_descriptions.get(name, "")
        entries.append(Instruction(name, description or "No description found."))
    return entries


def _row_descriptions(html: str, href_pattern: str) -> dict[str, str]:
    descriptions = {}
    for cells, href in _rows(html):
        if href and len(cells) > 1 and re.search(href_pattern, href):
            if href.startswith("/x86/"):
                match = re.fullmatch(r"/x86/([^/#?]+)", href)
                name = _normalise(match.group(1)) if match else ""
            else:
                name = _normalise(cells[0])
            if name:
                descriptions.setdefault(name, cells[1])
    return descriptions


def parse_felix_descriptions(html: str) -> dict[str, str]:
    """Extract mnemonic descriptions from Felix's index table."""
    return _row_descriptions(html, r"/x86/([^/#?]+)")


def parse_c9x_descriptions(html: str) -> dict[str, str]:
    """Extract mnemonic descriptions from C9x's index table."""
    return _row_descriptions(html, r"(?:^|/)html/file_module_x86_id_\d+\.html(?:$|#)")


def render_markdown(instructions: list[Instruction] | list[str]) -> str:
    lines = [
        "# x86 Instruction Catalog",
        "",
        "This flat list is de-duplicated and can be regenerated with "
        "`python tools/build_instruction_reference.py`.",
        "",
    ]
    for instruction in instructions:
        if isinstance(instruction, str):
            lines.append(f"- `{instruction}`")
        else:
            lines.append(f"- **{instruction.name}**: {instruction.description}")
    return "\n".join(lines) + "\n"