"""Read-only inventory of ClawBench run-meta.json attempts.

The recorded pass flag can be true without a judge result. This module deliberately
reports raw flags and configuration identities, never scores or rankings.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

FLAGS = ("pass", "intercepted", "infra_failure", "judge_match")
MAX_RECORD_BYTES = 16 * 1024 * 1024
STATES = ("true", "false", "missing", "null", "invalid")
NOTICE = (
    "Raw recorded flags; pass=true does not establish judged success. "
    "Every readable attempt is retained. No scores, ranking or comparability are inferred."
)


def flag_state(record: dict[str, Any], key: str) -> str:
    if key not in record:
        return "missing"
    value = record[key]
    if value is True:
        return "true"
    if value is False:
        return "false"
    return "null" if value is None else "invalid"


def _object(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _label(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    return "".join(c for c in value[:200] if c.isprintable())


def _hash(value: Any) -> str | None:
    if isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{64}", value):
        return value.lower()
    return None


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError("non-finite JSON constant")


def inventory(results_dir: Path) -> dict[str, Any]:
    """Load native files only; warnings identify ordinal files, never raw paths/errors."""
    attempts = []
    warnings = []
    for number, path in enumerate(sorted(results_dir.rglob("run-meta.json")), 1):
        try:
            if path.is_symlink():
                warnings.append(f"File {number}: skipped symbolic link")
                continue
            with path.open("rb") as stream:
                content = stream.read(MAX_RECORD_BYTES + 1)
            if len(content) > MAX_RECORD_BYTES:
                warnings.append(f"File {number}: exceeds 16 MiB record limit")
                continue
            raw = json.loads(content.decode("utf-8"), object_pairs_hook=_unique_object,
                             parse_constant=_reject_constant)
            if not isinstance(raw, dict):
                warnings.append(f"File {number}: expected a JSON object")
                continue
        except (OSError, UnicodeError, ValueError, RecursionError):
            warnings.append(f"File {number}: unreadable or invalid JSON")
            continue
        flags = {key: flag_state(raw, key) for key in FLAGS}
        no_judge = flag_state(_object(raw.get("run_flags")), "no_judge")
        provenance = _object(raw.get("provenance"))
        # Fingerprint rather than render provenance: it may contain private paths/URLs.
        try:
            provenance_hash = (
                hashlib.sha256(json.dumps(provenance, sort_keys=True).encode()).hexdigest()
                if provenance else None
            )
        except (ValueError, TypeError, RecursionError):
            provenance_hash = None
            warnings.append(f"File {number}: provenance could not be fingerprinted")
        attempts.append({
            "file_number": number,
            "harness": _label(raw.get("harness")),
            "model": _label(raw.get("model")),
            "task_sha256": _hash(raw.get("task_json_sha256")),
            "flags": flags,
            "judge_mode": {"true": "off", "false": "on"}.get(no_judge, "unknown"),
            "agent_config_sha256": _hash(
                _object(raw.get("model_config")).get("sanitized_config_sha256")
            ),
            "judge_config_sha256": _hash(
                _object(raw.get("judge_config")).get("sanitized_config_sha256")
            ),
            "provenance_sha256": provenance_hash,
        })
    return {
        "notice": NOTICE,
        "attempt_count": len(attempts),
        "flag_counts": {
            key: {state: sum(a["flags"][key] == state for a in attempts) for state in STATES}
            for key in FLAGS
        },
        "judge_mode_counts": dict(Counter(a["judge_mode"] for a in attempts)),
        "warnings": warnings,
        "attempts": attempts,
    }


def _cell(value: Any) -> str:
    if value is None:
        return "unknown"
    # HTML, Markdown links, backslashes and pipes must remain plain table-cell text.
    return html.escape(str(value)).replace("\\", "&#92;").replace("|", "&#124;").replace(
        "[", "&#91;"
    ).replace("]", "&#93;").replace("`", "&#96;").replace("*", "&#42;").replace("_", "&#95;")


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Native attempt inventory", "", report["notice"], "",
             f"Attempts: {report['attempt_count']}", "", "| Flag | True | False | Missing | Null | Invalid |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for key, counts in report["flag_counts"].items():
        lines.append("| " + " | ".join([key, *(str(counts[s]) for s in STATES)]) + " |")
    lines.extend(["", "| File | Harness | Model | Task SHA256 | Pass | Intercepted | Infra failure | Judge match | Judge mode | Agent config SHA256 | Judge config SHA256 | Provenance SHA256 |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"])
    for attempt in report["attempts"]:
        values = [attempt["file_number"], attempt["harness"], attempt["model"],
                  attempt["task_sha256"], *(attempt["flags"][k] for k in FLAGS),
                  attempt["judge_mode"], attempt["agent_config_sha256"],
                  attempt["judge_config_sha256"], attempt["provenance_sha256"]]
        lines.append("| " + " | ".join(_cell(value) for value in values) + " |")
    if report["warnings"]:
        lines.extend(["", "Warnings:", "", *(f"- {w}" for w in report["warnings"])])
    return "\n".join(lines)
