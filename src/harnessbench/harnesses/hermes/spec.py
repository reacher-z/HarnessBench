"""Hermes-Agent (Nous Research) harness spec.

Upstream: https://github.com/nousresearch/hermes-agent
"""

from __future__ import annotations

from harnessbench.harnesses._schema import HarnessSpec


spec = HarnessSpec(
    name="hermes",
    description="Nous Research Hermes-Agent driving Chromium via Playwright over CDP.",
    runtime="python",
    dockerfile="Dockerfile",
    setup_script="setup.sh",
    run_script="run.sh",
    container_isolation="dedicated",
    requires_credentials=(),
    upstream_url="https://github.com/nousresearch/hermes-agent",
    upstream_license="MIT",
)
