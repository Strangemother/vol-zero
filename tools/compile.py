from pathlib import Path
import subprocess
import sys
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools import iso_filename
from tools.build_cache import load_cache, save_cache
from tools.nim import ensure_nim


def distribution_iso_path(asset_knowledge: dict) -> Path:
	return PROJECT_ROOT / "dist" / iso_filename(asset_knowledge)


def main(arguments: list[str] | None = None) -> int:
	make_args = sys.argv[1:] if arguments is None else arguments
	ensure_nim()
	dry_run = any(argument in {"-n", "--just-print", "--dry-run"} for argument in make_args)
	asset_knowledge = load_cache()
	if not dry_run:
		asset_knowledge["build_count"] = int(asset_knowledge.get("build_count", 0)) + 1
		asset_knowledge["build_datetime"] = datetime.now().strftime("%y-%m-%d-%H-%M")
		save_cache(asset_knowledge)

	iso_path = distribution_iso_path(asset_knowledge)
	if not dry_run:
		iso_path.unlink(missing_ok=True)

	command = ["make", "-C", str(PROJECT_ROOT), "all", *make_args]
	completed = subprocess.run(command, cwd=PROJECT_ROOT)
	return completed.returncode


if __name__ == "__main__":
	raise SystemExit(main())
