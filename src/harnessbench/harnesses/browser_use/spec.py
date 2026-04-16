"""browser-use harness spec.

Upstream: https://github.com/browser-use/browser-use
"""

from __future__ import annotations

from harnessbench.harnesses._schema import HarnessSpec


spec = HarnessSpec(
    name="browser-use",
    description="browser-use — Python LLM-to-browser agent, drives Chromium via Playwright CDP attach.",
    runtime="python",
    dockerfile="Dockerfile",
    setup_script="setup.sh",
    run_script="run.sh",
    container_isolation="dedicated",
    requires_credentials=(),
    upstream_url="https://github.com/browser-use/browser-use",
    upstream_license="MIT",
)
