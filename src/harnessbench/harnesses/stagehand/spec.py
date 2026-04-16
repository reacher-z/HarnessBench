"""Stagehand (BrowserBase) harness spec.

Upstream: https://github.com/browserbase/stagehand

Cloud-opt-in: Stagehand's default runtime targets the BrowserBase cloud, so
this harness is auto-skipped unless BROWSERBASE_API_KEY is set. Users who
want to run Stagehand against a local Chrome can plumb a ``--local`` flag
through ``run.sh`` once upstream exposes one; track via HarnessBench
issues.
"""

from __future__ import annotations

from harnessbench.harnesses._schema import HarnessSpec


spec = HarnessSpec(
    name="stagehand",
    description="BrowserBase Stagehand — Node+TS, cloud-first. Auto-skips without BROWSERBASE_API_KEY.",
    runtime="node",
    dockerfile="Dockerfile",
    setup_script="setup.sh",
    run_script="run.sh",
    container_isolation="dedicated",
    requires_credentials=("BROWSERBASE_API_KEY",),
    upstream_url="https://github.com/browserbase/stagehand",
    upstream_license="MIT",
)
