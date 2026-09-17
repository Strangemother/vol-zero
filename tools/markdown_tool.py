"""Centralized Markdown parsing for the VOL documentation tools."""

from markupsafe import Markup
import mistune


_MARKDOWN = mistune.create_markdown(escape=True)


def to_html(text: str | None) -> Markup:
    """Convert Markdown text to escaped HTML for templates and documents."""

    if not text:
        return Markup("")
    return Markup(_MARKDOWN(text))
