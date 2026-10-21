"""Leaderboard aggregation: partition results by (harness, model, category).

A "result" is a ClawBench RecordingBundle summary (the top-level scores +
metadata that ``clawbench.judge_recording`` writes into the recording
directory). The leaderboard reads these summaries and renders markdown.
"""

from __future__ import annotations

import json
import warnings
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Row:
    harness: str
    model: str
    total: int = 0
    passed: int = 0
    skipped: int = 0
    failed: int = 0

    @property
    def score_pct(self) -> float:
        denom = self.total - self.skipped
        return 100.0 * self.passed / denom if denom else 0.0


def load_results(results_dir: Path) -> list[dict]:
    """Read every ``result.json`` under ``results_dir``.

    HarnessBench writes one per (harness, model, case). The schema matches
    ClawBench's per-case output plus two extra top-level keys: ``harness``
    and ``source="harnessbench"``. Unreadable files and invalid result shapes
    produce warnings so callers can identify an incomplete leaderboard.
    """
    out: list[dict] = []
    for p in sorted(results_dir.rglob("result.json")):
        try:
            result = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            warnings.warn(f"Skipping unreadable result {p}: {exc}", stacklevel=2)
            continue
        if not isinstance(result, dict) or any(
            key in result and not isinstance(result[key], str) for key in ("harness", "model")
        ):
            warnings.warn(
                f"Skipping invalid result {p}: expected an object with string harness/model fields",
                stacklevel=2,
            )
            continue
        out.append(result)
    return out


def aggregate(results: Iterable[dict]) -> list[Row]:
    buckets: dict[tuple[str, str], Row] = defaultdict(lambda: Row(harness="", model=""))
    for r in results:
        key = (r.get("harness", "unknown"), r.get("model", "unknown"))
        row = buckets[key]
        row.harness, row.model = key
        row.total += 1
        status = r.get("status", "unknown")
        if status == "skipped":
            row.skipped += 1
        elif r.get("passed") is True or r.get("score") == 1:
            row.passed += 1
        else:
            row.failed += 1
    return sorted(buckets.values(), key=lambda r: (-r.score_pct, r.harness, r.model))


def render_markdown(rows: list[Row]) -> str:
    if not rows:
        return "_(no results)_\n"
    lines = [
        "| Harness | Model | Passed | Failed | Skipped | Total | Score |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| `{r.harness}` | `{r.model}` | {r.passed} | {r.failed} | {r.skipped} | {r.total} | "
            f"{r.score_pct:.1f}% |"
        )
    return "\n".join(lines) + "\n"
