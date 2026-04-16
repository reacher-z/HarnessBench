"""Coze Studio harness spec.

Upstream: https://github.com/coze-dev/coze-studio

Cloud-opt-in: Coze Studio workflows execute against a Coze instance
(self-hosted or managed). Auto-skips unless both COZE_INSTANCE_URL and
COZE_API_TOKEN are present.
"""

from __future__ import annotations

from harnessbench.harnesses._schema import HarnessSpec


spec = HarnessSpec(
    name="coze-studio",
    description="Coze Studio workflows; requires a Coze instance (self-hosted or managed).",
    runtime="web",
    dockerfile="Dockerfile",
    setup_script="setup.sh",
    run_script="run.sh",
    container_isolation="dedicated",
    requires_credentials=("COZE_INSTANCE_URL", "COZE_API_TOKEN"),
    upstream_url="https://github.com/coze-dev/coze-studio",
    upstream_license="Apache-2.0",
)
