from __future__ import annotations

import argparse
import fnmatch
import json
import posixpath
import re
import shutil
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE_URL = "http://127.0.0.1:9050/"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "github-pages"
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "doc_site" / "config.json"
LINK_PATTERN = re.compile(r"\b(?P<attr>href|src)=(?P<quote>['\"])(?P<url>.*?)(?P=quote)", re.IGNORECASE)


class SiteExportError(Exception):
    pass


@dataclass(frozen=True)
class Route:
    path: str
    fragment: str = ""


@dataclass(frozen=True)
class ExportConfig:
    base_url: str = DEFAULT_BASE_URL
    output_dir: Path = DEFAULT_OUTPUT_DIR
    max_pages: int = 300
    stylesheet_path: str = "/static/style.css"
    stylesheet_output: str = "style.css"
    manifest_file: str = ".generated-pages.json"
    ignore_patterns: tuple[str, ...] = (".git", ".git/**", "**/.git", "**/.git/**")

    @property
    def output_root(self) -> Path:
        return self.output_dir.resolve()

    @property
    def manifest_path(self) -> Path:
        return self.output_root / self.manifest_file


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "vol-zero-static-export/1.0"})
    with urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset)


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "vol-zero-static-export/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read()


def fetch_required_text(url: str) -> str:
    try:
        return fetch_text(url)
    except HTTPError as error:
        raise SiteExportError(f"Could not fetch {url}: HTTP {error.code} {error.reason}") from error
    except URLError as error:
        if isinstance(error.reason, ConnectionRefusedError):
            raise SiteExportError(
                f"Connection refused for {url}.\n"
                "Have you run the docs site? Start it with: tool site run\n"
                "Then retry: tool site export or tool site deploy"
            ) from error
        raise SiteExportError(f"Could not fetch {url}: {error.reason}") from error


def path_from_config(value: str | None, config_path: Path | None) -> Path:
    if not value:
        return DEFAULT_OUTPUT_DIR
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    base = config_path.parent if config_path else PROJECT_ROOT
    return (base / path).resolve()


def load_config(config_path: Path | None) -> ExportConfig:
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH if DEFAULT_CONFIG_PATH.is_file() else None
    if config_path is None:
        return ExportConfig()

    data = json.loads(config_path.read_text(encoding="utf-8"))
    return ExportConfig(
        base_url=data.get("base_url", DEFAULT_BASE_URL),
        output_dir=path_from_config(data.get("output_dir"), config_path),
        max_pages=int(data.get("max_pages", 300)),
        stylesheet_path=data.get("stylesheet_path", "/static/style.css"),
        stylesheet_output=data.get("stylesheet_output", "style.css"),
        manifest_file=data.get("manifest_file", ".generated-pages.json"),
        ignore_patterns=tuple(data.get("ignore_patterns", (".git", ".git/**", "**/.git", "**/.git/**"))),
    )


def relative_to_output(path: Path, config: ExportConfig) -> str:
    return path.relative_to(config.output_root).as_posix()


def is_ignored(relative_path: str, config: ExportConfig) -> bool:
    clean_path = relative_path.strip("/")
    if not clean_path:
        return False
    return any(fnmatch.fnmatch(clean_path, pattern) for pattern in config.ignore_patterns)


def ignored_route(raw_url: str, base_url: str, config: ExportConfig) -> bool:
    base = urlparse(base_url)
    absolute = urlparse(urljoin(base_url, raw_url))
    if absolute.scheme not in {"http", "https"} or absolute.netloc != base.netloc:
        return False
    clean_url, _fragment = urldefrag(absolute.geturl())
    clean = urlparse(clean_url)
    path = clean.path or "/"
    return is_ignored(output_file_for(path, config).relative_to(config.output_root).as_posix(), config)


def normalize_route(raw_url: str, base_url: str, config: ExportConfig) -> Route | None:
    if not raw_url or raw_url.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None

    base = urlparse(base_url)
    absolute = urlparse(urljoin(base_url, raw_url))
    if absolute.scheme not in {"http", "https"}:
        return None
    if absolute.netloc != base.netloc:
        return None
    if absolute.path.startswith(posixpath.dirname(config.stylesheet_path.rstrip("/")) + "/"):
        return None

    clean_url, fragment = urldefrag(absolute.geturl())
    clean = urlparse(clean_url)
    path = clean.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/") + "/"
    if is_ignored(output_file_for(path, config).relative_to(config.output_root).as_posix(), config):
        return None
    return Route(path=path, fragment=fragment)


def output_file_for(path: str, config: ExportConfig) -> Path:
    clean_path = path.strip("/")
    if not clean_path:
        return config.output_root / "index.html"
    return config.output_root / clean_path / "index.html"


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


def normalize_asset(raw_url: str, current_path: str, base_url: str, config: ExportConfig) -> str | None:
    if not raw_url or raw_url.startswith(("#", "data:", "mailto:", "tel:", "javascript:")):
        return None

    base = urlparse(base_url)
    page_url = urljoin(base_url, current_path.lstrip("/") or "")
    absolute = urlparse(urljoin(page_url, raw_url))
    if absolute.scheme not in {"http", "https"} or absolute.netloc != base.netloc:
        return None

    clean_url, _fragment = urldefrag(absolute.geturl())
    clean = urlparse(clean_url)
    path = clean.path.strip("/")
    if not path or path.endswith("/") or clean.path == config.stylesheet_path:
        return None
    if is_ignored(path, config):
        return None
    return path


def rewrite_links(html: str, current_path: str, base_url: str, config: ExportConfig) -> str:
    stylesheet_url = urljoin(base_url, config.stylesheet_path)

    def replace(match: re.Match[str]) -> str:
        attr = match.group("attr")
        quote = match.group("quote")
        raw_url = match.group("url")

        if raw_url == config.stylesheet_path or raw_url == stylesheet_url:
            new_url = relative_asset_href(current_path, config.stylesheet_output)
            return f"{attr}={quote}{new_url}{quote}"

        if attr.lower() == "src":
            asset_path = normalize_asset(raw_url, current_path, base_url, config)
            if asset_path is not None:
                new_url = relative_asset_href(current_path, asset_path)
                return f"{attr}={quote}{new_url}{quote}"
            return match.group(0)

        if attr.lower() == "href" and ignored_route(raw_url, base_url, config):
            return f"{attr}={quote}#{quote}"

        route = normalize_route(raw_url, base_url, config)
        if route is None:
            return match.group(0)

        new_url = relative_page_href(current_path, route)
        return f"{attr}={quote}{new_url}{quote}"

    return LINK_PATTERN.sub(replace, html)


def asset_paths_from(html: str, current_path: str, base_url: str, config: ExportConfig) -> list[str]:
    assets = {
        asset_path
        for match in LINK_PATTERN.finditer(html)
        if match.group("attr").lower() == "src"
        for asset_path in [normalize_asset(match.group("url"), current_path, base_url, config)]
        if asset_path is not None
    }
    return sorted(assets)


def page_routes_from(html: str, base_url: str, config: ExportConfig) -> list[Route]:
    routes: list[Route] = []
    for match in LINK_PATTERN.finditer(html):
        if match.group("attr").lower() != "href":
            continue
        route = normalize_route(match.group("url"), base_url, config)
        if route is None:
            continue
        routes.append(Route(path=route.path))
    return routes


def write_page(route: Route, html: str, base_url: str, config: ExportConfig) -> Path:
    output_path = output_file_for(route.path, config)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rewrite_links(html, route.path, base_url, config), encoding="utf-8")
    return output_path


def write_asset(asset_path: str, content: bytes, config: ExportConfig) -> Path:
    output_path = config.output_root / asset_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)
    return output_path


def cleanup_previous_run(config: ExportConfig) -> None:
    if not config.manifest_path.is_file():
        return

    previous_paths = json.loads(config.manifest_path.read_text(encoding="utf-8"))
    for relative_path in previous_paths:
        path = (config.output_root / relative_path).resolve()
        try:
            path.relative_to(config.output_root)
        except ValueError:
            continue
        if path.is_file():
            path.unlink()

    for relative_path in sorted(previous_paths, key=lambda value: value.count("/"), reverse=True):
        parent = (config.output_root / relative_path).parent
        while parent != config.output_root and parent.exists():
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent


def cleanup_ignored_paths(config: ExportConfig) -> None:
    if not config.output_root.exists():
        return

    paths = sorted(config.output_root.rglob("*"), key=lambda path: len(path.parts), reverse=True)
    for path in paths:
        relative_path = relative_to_output(path, config)
        if not is_ignored(relative_path, config):
            continue
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def write_manifest(paths: list[Path], config: ExportConfig) -> None:
    relative_paths = sorted(relative_to_output(path, config) for path in paths)
    config.manifest_path.write_text(json.dumps(relative_paths, indent=2) + "\n", encoding="utf-8")


def export_site(config: ExportConfig) -> list[Path]:
    base_url = config.base_url.rstrip("/") + "/"
    seen: set[str] = set()
    pending: deque[Route] = deque([Route("/")])
    written: list[Path] = []

    css = fetch_required_text(urljoin(base_url, config.stylesheet_path))
    first_page = fetch_required_text(base_url)

    config.output_root.mkdir(parents=True, exist_ok=True)
    cleanup_previous_run(config)
    cleanup_ignored_paths(config)

    stylesheet_path = config.output_root / config.stylesheet_output
    stylesheet_path.parent.mkdir(parents=True, exist_ok=True)
    stylesheet_path.write_text(css, encoding="utf-8")
    written.append(stylesheet_path)

    while pending and len(seen) < config.max_pages:
        route = pending.popleft()
        if route.path in seen:
            continue

        url = urljoin(base_url, route.path.lstrip("/"))
        if route.path == "/":
            html = first_page
        else:
            try:
                html = fetch_text(url)
            except (HTTPError, URLError) as error:
                print(f"skip {route.path}: {error}")
                seen.add(route.path)
                continue

        seen.add(route.path)
        written.append(write_page(route, html, base_url, config))

        for asset_path in asset_paths_from(html, route.path, base_url, config):
            output_path = config.output_root / asset_path
            if output_path in written:
                continue
            try:
                content = fetch_bytes(urljoin(base_url, asset_path))
            except (HTTPError, URLError) as error:
                print(f"skip asset {asset_path}: {error}")
                continue
            written.append(write_asset(asset_path, content, config))

        for next_route in page_routes_from(html, base_url, config):
            if next_route.path not in seen:
                pending.append(next_route)

    if pending:
        print(f"stopped after {config.max_pages} pages; {len(pending)} routes remain")
    cleanup_ignored_paths(config)
    write_manifest(written, config)
    return written


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export the Flask documentation site as static files.")
    parser.add_argument("config", nargs="?", help="JSON export configuration file")
    parser.add_argument("--base-url", help="override the configured Flask docs site URL")
    parser.add_argument("--output-dir", help="override the configured output directory")
    parser.add_argument("--max-pages", type=int, help="override the configured crawl page limit")
    return parser


def main(arguments: list[str] | None = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(arguments)
    config_path = Path(parsed.config).resolve() if parsed.config else None
    config = load_config(config_path)
    if parsed.base_url:
        config = ExportConfig(**{**config.__dict__, "base_url": parsed.base_url})
    if parsed.output_dir:
        config = ExportConfig(**{**config.__dict__, "output_dir": path_from_config(parsed.output_dir, config_path)})
    if parsed.max_pages:
        config = ExportConfig(**{**config.__dict__, "max_pages": parsed.max_pages})

    try:
        written = export_site(config)
    except SiteExportError as error:
        print(error)
        return 1
    for path in written:
        print(relative_to_output(path, config))
    print(f"wrote {len(written)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())