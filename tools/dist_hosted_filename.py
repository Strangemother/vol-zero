"""Return the hosted development executable filename."""

from typing import Any

try:
    from .version import kernel_version
except ImportError:
    from version import kernel_version


def hosted_filename(asset_knowledge: dict[str, Any]) -> str:
    version = kernel_version()
    count = asset_knowledge.get("build_count", 0)
    return f"vol-hosted-{version}-{count}"