"""Plugin discovery sanity tests.

These tests do NOT spin up any container. They only verify that the
harness metadata is importable and registered.
"""

from __future__ import annotations

import pytest

from harnessbench.matrix import discover_registrations


EXPECTED = {
    "openclaw",
    "hermes",
    "claw-code",
    "browser-use",
    "stagehand",
    "coze-studio",
}


def test_discover_registrations_returns_all_named_harnesses():
    regs = discover_registrations()
    names = {r.spec.name for r in regs}
    missing = EXPECTED - names
    assert not missing, f"missing harnesses: {sorted(missing)}"


@pytest.mark.parametrize("name", sorted(EXPECTED))
def test_each_registration_has_required_fields(name):
    regs = {r.spec.name: r for r in discover_registrations()}
    spec = regs[name].spec
    assert spec.dockerfile
    assert spec.setup_script
    assert spec.run_script
    assert spec.runtime in {"python", "node", "rust", "web"}
    assert spec.container_isolation in {"shared", "dedicated"}
    assert spec.upstream_url.startswith("https://")
    assert spec.upstream_license in {"Apache-2.0", "MIT", "BSD-2-Clause", "BSD-3-Clause"}


def test_cloud_harnesses_declare_credentials():
    regs = {r.spec.name: r for r in discover_registrations()}
    assert regs["stagehand"].spec.requires_credentials, "stagehand must declare credentials"
    assert "BROWSERBASE_API_KEY" in regs["stagehand"].spec.requires_credentials
    assert regs["coze-studio"].spec.requires_credentials, "coze-studio must declare credentials"
    required_coze = set(regs["coze-studio"].spec.requires_credentials)
    assert {"COZE_INSTANCE_URL", "COZE_API_TOKEN"} <= required_coze


def test_local_harnesses_declare_no_credentials():
    regs = {r.spec.name: r for r in discover_registrations()}
    for name in ("openclaw", "hermes", "claw-code", "browser-use"):
        assert not regs[name].spec.requires_credentials, f"{name} must not require credentials"
