"""claw-code (Rust coding-agent) harness spec.

Upstream: https://github.com/ultraworkers/claw-code
"""

from __future__ import annotations

from harnessbench.harnesses._schema import HarnessSpec


spec = HarnessSpec(
    name="claw-code",
    description="Rust-based claw-code coding agent; drives Chrome via generated Playwright scripts.",
    runtime="rust",
    dockerfile="Dockerfile",
    setup_script="setup.sh",
    run_script="run.sh",
    container_isolation="dedicated",
    requires_credentials=(),
    upstream_url="https://github.com/ultraworkers/claw-code",
    upstream_license="Apache-2.0",
)
