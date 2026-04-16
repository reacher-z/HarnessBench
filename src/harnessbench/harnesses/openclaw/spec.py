"""OpenClaw — the reference harness, re-exported from ClawBench for consistency.

This keeps ``harnessbench run --harness openclaw`` producing byte-identical
traces to ``claw-bench run ... openclaw``: both resolve to the same
Dockerfile + setup + run triple.
"""

from __future__ import annotations

from harnessbench.harnesses._schema import HarnessSpec


spec = HarnessSpec(
    name="openclaw",
    description="Reference harness: OpenClaw driving Chromium via CDP. Matches ClawBench's default.",
    runtime="python",
    dockerfile="Dockerfile",
    setup_script="setup.sh",
    run_script="run.sh",
    container_isolation="shared",
    requires_credentials=(),
    upstream_url="https://github.com/reacher-z/ClawBench",
    upstream_license="Apache-2.0",
)
