#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import posixpath
import re
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://animated-broccoli-6wx47wpqpf494w-9050.app.github.dev/"
OUTPUT_ROOT = Path(__file__).resolve().parent
MANIFEST_FILE = OUTPUT_ROOT / ".generated-pages.json"
LINK_PATTERN = re.compile(r"\b(?P<attr>href|src)=(?P<quote>['\"])(?P<url>.*?)(?P=quote)", re.IGNORECASE)


@dataclass(frozen=True)
class Route:
    path: str
    fragment: str = ""


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "vol-zero-static-converter/1.0"})
    with urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset)


def normalize_route(raw_url: str, base_url: str) -> Route | None:
    if not raw_url or raw_url.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None

    base = urlparse(base_url)
    absolute = urlparse(urljoin(base_url, raw_url))
    if absolute.scheme not in {"http", "https"}:
        return None
    if absolute.netloc != base.netloc:
        return None
    if absolute.path.startswith("/static/"):
        return None

    clean_url, fragment = urldefrag(absolute.geturl())
    clean = urlparse(clean_url)
    path = clean.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/") + "/"
    return Route(path=path, fragment=fragment)


def output_file_for(path: str) -> Path:
    clean_path = path.strip("/")
    if not clean_path:
        return OUTPUT_ROOT / "index.html"
    return OUTPUT_ROOT / clean_path / "index.html"


def output_dir_for(path: str) -> str:
    clean_path = path.strip("/")
    return clean_path if clean_path else "."


def relative_page_href(from_path: str, to_route: Route) -> str:
    from_dir = output_dir_for(from_path)
    target_dir = output_dir_for(to_route.path)
    relative = posixpath.relpath(target_dir, from_dir)
    if relative == ".":
        relative = "./"
    else:
        relative = relative.rstrip("/") + "/"
    if to_route.fragment:
        relative += f"#{to_route.fragment}"
    return relative


def relative_asset_href(from_path: str, asset_name: str) -> str:
    from_dir = output_dir_for(from_path)
    relative = posixpath.relpath(asset_name, from_dir)
    return asset_name if relative == "." else relative


def rewrite_links(html: str, current_path: str, base_url: str) -> str:
    def replace(match: re.Match[str]) -> str:
        attr = match.group("attr")
        quote = match.group("quote")
        raw_url = match.group("url")

        if raw_url == "/static/style.css" or raw_url == urljoin(base_url, "/static/style.css"):
            new_url = relative_asset_href(current_path, "style.css")
            return f"{attr}={quote}{new_url}{quote}"

        route = normalize_route(raw_url, base_url)
        if route is None:
            return match.group(0)

        new_url = relative_page_href(current_path, route)
        return f"{attr}={quote}{new_url}{quote}"

    return LINK_PATTERN.sub(replace, html)


def page_routes_from(html: str, base_url: str) -> list[Route]:
    routes: list[Route] = []
    for match in LINK_PATTERN.finditer(html):
        if match.group("attr").lower() != "href":
            continue
        route = normalize_route(match.group("url"), base_url)
        if route is None:
            continue
        routes.append(Route(path=route.path))
    return routes


def write_page(route: Route, html: str, base_url: str) -> Path:
    output_path = output_file_for(route.path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rewrite_links(html, route.path, base_url), encoding="utf-8")
    return output_path


def cleanup_previous_run() -> None:
    if not MANIFEST_FILE.is_file():
        return

    previous_paths = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    for relative_path in previous_paths:
        path = (OUTPUT_ROOT / relative_path).resolve()
        try:
            path.relative_to(OUTPUT_ROOT)
        except ValueError:
            continue
        if path.is_file():
            path.unlink()

    for relative_path in sorted(previous_paths, key=lambda value: value.count("/"), reverse=True):
        parent = (OUTPUT_ROOT / relative_path).parent
        while parent != OUTPUT_ROOT and parent.exists():
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent


def write_manifest(paths: list[Path]) -> None:
    relative_paths = sorted(path.relative_to(OUTPUT_ROOT).as_posix() for path in paths)
    MANIFEST_FILE.write_text(json.dumps(relative_paths, indent=2) + "\n", encoding="utf-8")


def convert(base_url: str, max_pages: int) -> list[Path]:
    base_url = base_url.rstrip("/") + "/"
    seen: set[str] = set()
    pending: deque[Route] = deque([Route("/")])
    written: list[Path] = []

    cleanup_previous_run()

    css = fetch_text(urljoin(base_url, "/static/style.css"))
    (OUTPUT_ROOT / "style.css").write_text(css, encoding="utf-8")
    written.append(OUTPUT_ROOT / "style.css")

    while pending and len(seen) < max_pages:
        route = pending.popleft()
        if route.path in seen:
            continue

        url = urljoin(base_url, route.path.lstrip("/"))
        try:
            html = fetch_text(url)
        except (HTTPError, URLError) as error:
            print(f"skip {route.path}: {error}")
            seen.add(route.path)
            continue

        seen.add(route.path)
        written.append(write_page(route, html, base_url))

        for next_route in page_routes_from(html, base_url):
            if next_route.path not in seen:
                pending.append(next_route)

    if pending:
        print(f"stopped after {max_pages} pages; {len(pending)} routes remain")
    write_manifest(written)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Flask docs site as static GitHub Pages files.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Flask docs site URL to render")
    parser.add_argument("--max-pages", type=int, default=300, help="maximum number of HTML pages to crawl")
    args = parser.parse_args()

    written = convert(args.base_url, args.max_pages)
    for path in written:
        print(path.relative_to(OUTPUT_ROOT))
    print(f"wrote {len(written)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())