"""Local schema for harness specs while the ClawBench plugin surface is in flight.

Once ``clawbench.HarnessSpec`` is a public toolkit type, each ``spec.py`` will
``from clawbench import HarnessSpec`` and delete this shim. Keeping a local
dataclass lets HarnessBench's tests and matrix expansion run today against
the six plugins without a hard dependency on a version of ClawBench that
hasn't published yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


Runtime = Literal["python", "node", "rust", "web"]


@dataclass(frozen=True)
class HarnessSpec:
    name: str
    description: str
    runtime: Runtime
    dockerfile: str  # relative path within the harness package directory
    setup_script: str
    run_script: str
    container_isolation: Literal["shared", "dedicated"] = "dedicated"
    requires_credentials: tuple[str, ...] = field(default_factory=tuple)
    upstream_url: str | None = None
    upstream_license: str | None = None
