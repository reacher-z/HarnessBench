"""HarnessBench: compare agentic harnesses on everyday online tasks.

Sister project to ClawBench (https://github.com/reacher-z/ClawBench).
ClawBench fixes the harness and varies the base model; HarnessBench does
the inverse.

The evaluation pipeline, container orchestration, submission-interception,
and 5-layer recording are all imported from ``clawbench`` (PyPI
``clawbench-eval``). HarnessBench contributes: per-harness plugin specs,
the matrix runner that expands harness x model x task, the leaderboard
aggregator, and the 3-file adapter pattern documented in
``docs/adding-a-harness.md``.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("harness-bench")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
