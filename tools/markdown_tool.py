"""Centralized Markdown parsing for the VOL documentation tools."""

from markupsafe import Markup
import mistune
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


_FORMATTER = HtmlFormatter()
_INLINE_FORMATTER = HtmlFormatter(nowrap=True)


class _HighlightRenderer(mistune.HTMLRenderer):
    def __init__(self, default_language: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self.default_language = default_language

    def block_code(self, code: str, info: str | None = None) -> str:
        language = (info or "").strip().split(None, 1)[0] if info else self.default_language
        if language:
            try:
                lexer = get_lexer_by_name(language)
            except ClassNotFound:
                lexer = None
            if lexer is not None:
                return highlight(code, lexer, _FORMATTER)
        return super().block_code(code, info)


_MARKDOWN = mistune.create_markdown(renderer=_HighlightRenderer(), escape=True)
_NIM_MARKDOWN = mistune.create_markdown(
    renderer=_HighlightRenderer(default_language="nim"),
    escape=True,
)


def code_to_html(text: str, language: str) -> Markup:
    """Render a source file with syntax highlighting when its language is known."""

    if language.lower() not in {"nim", "nimrod"}:
        return Markup.escape(text)
    lexer = get_lexer_by_name("nim")
    return Markup(highlight(text, lexer, _FORMATTER))


def signature_to_html(signature: str) -> Markup:
    """Render a Nim declaration signature as inline highlighted HTML."""

    lexer = get_lexer_by_name("nim")
    return Markup(highlight(signature, lexer, _INLINE_FORMATTER).strip())


def to_html(text: str | None, language: str | None = None) -> Markup:
    """Convert Markdown text to escaped HTML for templates and documents."""

    if not text:
        return Markup("")
    markdown = _NIM_MARKDOWN if language in {"nim", "nimrod"} else _MARKDOWN
    return Markup(markdown(text))
