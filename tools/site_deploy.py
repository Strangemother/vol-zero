from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

from tools.site_export import ExportConfig, SiteExportError, export_site, load_config, path_from_config


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def git(arguments: list[str], *, env: dict[str, str] | None = None, capture: bool = False) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=PROJECT_ROOT,
        env=env,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return result.stdout.strip() if capture and result.stdout else ""


def ref_exists(ref: str) -> bool:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", ref],
        cwd=PROJECT_ROOT,
        check=False,
    )
    return result.returncode == 0


def fetch_branch(remote: str, branch: str) -> str | None:
    remote_ref = f"refs/remotes/{remote}/{branch}"
    result = subprocess.run(
        ["git", "ls-remote", "--exit-code", "--heads", remote, branch],
        cwd=PROJECT_ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        return None
    git(["fetch", remote, f"{branch}:{remote_ref}"])
    return remote_ref


def build_tree(output_root: Path) -> str:
    with tempfile.NamedTemporaryFile(prefix="vol-site-index-", delete=False) as temporary_index:
        index_path = temporary_index.name

    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = index_path
    try:
        git(["read-tree", "--empty"], env=env)
        git([f"--work-tree={output_root}", "add", "-A", "."], env=env)
        return git(["write-tree"], env=env, capture=True)
    finally:
        Path(index_path).unlink(missing_ok=True)


def create_deploy_commit(tree: str, parent_ref: str | None, message: str) -> str:
    arguments = ["commit-tree", tree, "-m", message]
    if parent_ref:
        arguments.extend(["-p", parent_ref])
    return git(arguments, capture=True)


def deploy_site(
    config: ExportConfig,
    *,
    remote: str,
    branch: str,
    message: str,
    dry_run: bool,
) -> str:
    written = export_site(config)
    print(f"exported {len(written)} files")

    parent_ref = fetch_branch(remote, branch)
    tree = build_tree(config.output_root)
    commit = create_deploy_commit(tree, parent_ref, message)

    if dry_run:
        print(f"would deploy {commit} to {remote}/{branch}")
        return commit

    local_ref = f"refs/heads/{branch}"
    git(["update-ref", local_ref, commit])
    git(["push", remote, f"{local_ref}:{branch}"])
    print(f"deployed {commit} to {remote}/{branch}")
    return commit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export and publish the static documentation site.")
    parser.add_argument("config", nargs="?", help="JSON export configuration file")
    parser.add_argument("--base-url", help="override the configured Flask docs site URL")
    parser.add_argument("--output-dir", help="override the configured output directory")
    parser.add_argument("--max-pages", type=int, help="override the configured crawl page limit")
    parser.add_argument("--remote", default="origin", help="git remote to push (default: origin)")
    parser.add_argument("--branch", default="gh-pages", help="deployment branch (default: gh-pages)")
    parser.add_argument("--message", default="Deploy static site", help="deployment commit message")
    parser.add_argument("--dry-run", action="store_true", help="export and create a commit without updating refs or pushing")
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
        deploy_site(
            config,
            remote=parsed.remote,
            branch=parsed.branch,
            message=parsed.message,
            dry_run=parsed.dry_run,
        )
    except SiteExportError as error:
        print(error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())