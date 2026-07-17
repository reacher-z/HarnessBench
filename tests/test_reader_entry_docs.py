"""Reader-facing Markdown links should not lead to missing local files."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_FILES = [
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "AGENTS.md",
    ROOT / "CONTRIBUTING.md",
    *(ROOT / "docs").glob("*.md"),
]
LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target><[^>]+>|[^)\s]+)(?:\s+[^)]*)?\)")


def _local_target(target: str) -> Path | None:
    target = target.strip("<>")
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    resolved = (ROOT / unquote(parsed.path)).resolve()
    if not resolved.is_relative_to(ROOT):
        return None
    return resolved


def test_reader_facing_local_markdown_links_resolve():
    missing: list[str] = []
    for document in MARKDOWN_FILES:
        for target in LINK_RE.findall(document.read_text(encoding="utf-8")):
            local_target = _local_target(target)
            if local_target is not None and not local_target.exists():
                missing.append(f"{document.relative_to(ROOT)} -> {target}")

    assert not missing, "missing local Markdown targets:\n" + "\n".join(missing)
