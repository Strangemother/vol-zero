import sys
import json
from pathlib import Path

from flask import Flask, abort, render_template


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = PROJECT_ROOT / "kernel" / "src"
DOCS_ROOT = PROJECT_ROOT / "docs"
CACHE_ROOT = PROJECT_ROOT / "doc_site" / "cache"
VERSION = (PROJECT_ROOT / "kernel" / "VERSION").read_text(encoding="utf-8").strip()
GITHUB_URL = "https://github.com/Strangemother/vol-zero"
sys.path.insert(0, str(PROJECT_ROOT))

from tools.nim_docs import parse_nim_source
from tools.markdown_tool import code_to_html, signature_to_html, to_html


app = Flask(__name__)
app.jinja_env.globals["md_to_html"] = to_html
app.jinja_env.globals["nim_md_to_html"] = lambda text: to_html(text, "nim")
app.jinja_env.globals["code_to_html"] = code_to_html
app.jinja_env.globals["signature_to_html"] = signature_to_html
app.jinja_env.globals["project_version"] = VERSION
app.jinja_env.globals["github_url"] = GITHUB_URL


@app.get("/")
def home():
	index_path = DOCS_ROOT / "index.md"
	documentation = index_path.read_text(encoding="utf-8") if index_path.is_file() else None
	return render_template(
		"index.html",
		entries=directory_entries(SOURCE_ROOT),
		documentation=documentation,
	)


def _module_cache_path(source_path: Path) -> Path:
	relative_path = source_path.relative_to(SOURCE_ROOT).with_suffix("")
	cache_name = "_".join(relative_path.parts) + ".json"
	return CACHE_ROOT / cache_name


def _load_module(source_path: Path) -> dict:
	cache_path = _module_cache_path(source_path)
	if cache_path.exists():
		return json.loads(cache_path.read_text(encoding="utf-8"))

	module = parse_nim_source(source_path).to_dict()
	CACHE_ROOT.mkdir(parents=True, exist_ok=True)
	cache_path.write_text(json.dumps(module, indent=2) + "\n", encoding="utf-8")
	return module


def _load_supersheet() -> list[dict[str, str]]:
	sheet_cache_path = CACHE_ROOT / "supersheet.json"
	if sheet_cache_path.exists():
		return json.loads(sheet_cache_path.read_text(encoding="utf-8"))["entries"]

	entries: list[dict[str, str]] = []
	directories: set[str] = set()
	for source_path in sorted(SOURCE_ROOT.rglob("*.nim")):
		relative_path = source_path.relative_to(SOURCE_ROOT).with_suffix("")
		module_name = ".".join(relative_path.parts)
		for index in range(1, len(relative_path.parts)):
			directory_name = ".".join(relative_path.parts[:index])
			if directory_name not in directories:
				directories.add(directory_name)
				directory_url = "/" + "/".join(relative_path.parts[:index]) + "/"
				entries.append({
					"kind": "dir",
					"name": directory_name,
					"url": directory_url,
				})

		module_url = "/" + relative_path.as_posix()
		entries.append({"kind": "module", "name": module_name, "url": module_url})
		module = _load_module(source_path)
		for declaration in module["declarations"]:
			entries.append({
				"kind": "declaration",
				"name": declaration["name"],
				"full_name": f"{module_name}.{declaration['name']}",
				"url": f"{module_url}#declaration-{declaration['line']}",
			})

	CACHE_ROOT.mkdir(parents=True, exist_ok=True)
	sheet_cache_path.write_text(
		json.dumps({"entries": entries}, indent=2) + "\n",
		encoding="utf-8",
	)
	return entries


@app.get("/sheet/")
def sheet():
	return render_template("sheet.html", entries=_load_supersheet())


@app.get("/docs/<path:requested_path>")
def documentation_view(requested_path: str):
	path = requested_path.strip("/")
	document_path = (DOCS_ROOT / path).resolve()
	if not document_path.suffix:
		if document_path.is_dir():
			return documentation_directory_view(document_path)
		document_path = document_path.with_suffix(".md")
	try:
		document_path.relative_to(DOCS_ROOT.resolve())
	except ValueError:
		abort(404)
	if not document_path.is_file() or document_path.suffix.lower() != ".md":
		abort(404)

	relative_path = document_path.relative_to(DOCS_ROOT).with_suffix("")
	parent_path = relative_path.parent
	parent_url = "/docs/"
	if str(parent_path) != ".":
		parent_url += parent_path.as_posix().strip("/") + "/"
	return render_template(
		"doc-file.html",
		module=None,
		documentation=document_path.read_text(encoding="utf-8"),
		file_content=None,
		asset_type='markdown-doc',
		file_extension="md",
		parent_url=parent_url,
		source_path=f"docs/{relative_path.as_posix()}",
	)


@app.get("/docs/")
def documentation_root():
	return documentation_directory_view(DOCS_ROOT)


def documentation_directory_view(directory: Path):
	try:
		directory.relative_to(DOCS_ROOT.resolve())
	except ValueError:
		abort(404)
	if not directory.is_dir():
		abort(404)

	relative_path = directory.relative_to(DOCS_ROOT)
	parent_url = "/docs/"
	if str(relative_path) != ".":
		parent_path = relative_path.parent
		if str(parent_path) != ".":
			parent_url += parent_path.as_posix().strip("/") + "/"
	readme_path = readme_path_for(directory)
	return render_template(
		"directory.html",
		directory_path=f"docs/{relative_path.as_posix()}" if str(relative_path) != "." else "docs",
		parent_url=parent_url,
		asset_type='markdown-doc',
		documentation=readme_path.read_text(encoding="utf-8") if readme_path else None,
		entries=documentation_directory_entries(directory),
	)


def documentation_directory_entries(directory: Path) -> list[dict[str, str]]:
	entries = []
	for path in sorted(directory.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())):
		relative_path = path.relative_to(DOCS_ROOT)
		if path.is_dir():
			url = "/docs/" + relative_path.as_posix().strip("/") + "/"
			name = path.name
		elif path.is_file():
			url_path = relative_path.with_suffix("") if path.suffix.lower() == ".md" else relative_path
			url = "/docs/" + url_path.as_posix().strip("/")
			name = path.stem if path.suffix.lower() == ".md" else path.name
		else:
			continue
		entries.append({
			"name": name,
			"kind": "directory" if path.is_dir() else "file",
			"url": url,
		})
	return entries


def source_path_for(requested_path: str) -> Path:
	path = requested_path.strip("/")
	candidate = (SOURCE_ROOT / path).resolve()
	if candidate.is_dir() or candidate.is_file() or Path(path).suffix:
		return candidate
	return (SOURCE_ROOT / f"{path}.nim").resolve()


def readme_path_for(directory: Path) -> Path | None:
	for path in directory.iterdir():
		if path.is_file() and path.name.lower() == "readme.md":
			return path
	return None


def directory_entries(directory: Path) -> list[dict[str, str]]:
	entries = []
	for path in sorted(directory.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())):
		if path.is_dir() or path.is_file():
			relative_path = path.relative_to(SOURCE_ROOT)
			url_path = relative_path if path.is_dir() or path.suffix != ".nim" else relative_path.with_suffix("")
			url = "/" + url_path.as_posix().strip("/")
			if path.is_dir():
				url += "/"
			entries.append({
				"name": path.stem if path.suffix == ".nim" else path.name,
				"kind": "directory" if path.is_dir() else "file",
				"url": url,
			})
	return entries


def parent_url_for(relative_path: Path) -> str:
	parent = relative_path.parent
	if str(parent) == ".":
		return "/"
	return "/" + parent.as_posix().strip("/") + "/"


@app.get("/<path:requested_path>")
def file_view(requested_path: str):
	source_path = source_path_for(requested_path)
	try:
		source_path.relative_to(SOURCE_ROOT.resolve())
	except ValueError:
		abort(404)
	if source_path.is_dir():
		relative_path = source_path.relative_to(SOURCE_ROOT)
		readme_path = readme_path_for(DOCS_ROOT / relative_path) if (DOCS_ROOT / relative_path).is_dir() else None
		documentation = readme_path.read_text(encoding="utf-8") if readme_path else None
		return render_template(
			"directory.html",
			directory_path=relative_path.as_posix(),
			parent_url=parent_url_for(relative_path),
			asset_type='file-doc',
			documentation=documentation,
			entries=directory_entries(source_path),
		)
	if not source_path.is_file():
		abort(404)

	relative_source_path = source_path.relative_to(SOURCE_ROOT)
	relative_path = relative_source_path.with_suffix("")
	display_source_path = (
		relative_path if source_path.suffix == ".nim" else relative_source_path
	)
	doc_path = DOCS_ROOT / relative_path.with_suffix(".md")
	documentation = doc_path.read_text(encoding="utf-8") if doc_path.is_file() else None
	file_content = source_path.read_text(encoding="utf-8", errors="replace")
	module = parse_nim_source(source_path) if source_path.suffix == ".nim" else None
	return render_template(
		"file.html",
		module=module.to_dict() if module else None,
		documentation=documentation,
		file_content=file_content,
		asset_type='file-doc',
		file_extension=source_path.suffix.lstrip(".").lower(),
		parent_url=parent_url_for(relative_path),
		source_path=display_source_path.as_posix(),
	)


def main():
	app.run(debug=True, host="127.0.0.1", port=9050)


if __name__ == "__main__":
	main()
