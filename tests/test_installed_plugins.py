"""Installed metadata discovery, using real distributions and module imports."""
from __future__ import annotations

import importlib
import warnings
from uuid import uuid4

import pytest
from click.testing import CliRunner

from harnessbench.cli import main
from harnessbench.matrix import discover_registrations, expand


@pytest.fixture
def installed(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(tmp_path))

    def install(name, body, target="spec"):
        module = "hb_test_" + name + "_" + uuid4().hex
        (tmp_path / (module + ".py")).write_text(body)
        dist = tmp_path / (module + "-1.0.dist-info")
        dist.mkdir()
        (dist / "METADATA").write_text(f"Metadata-Version: 2.1\nName: {module}\nVersion: 1.0\n")
        (dist / "entry_points.txt").write_text(
            f"[clawbench.harnesses]\n{name} = {module}:{target}\n"
        )
        importlib.invalidate_caches()

    return install


def spec_source(name="installed-example", credentials="()"):
    return (
        "from harnessbench.harnesses._schema import HarnessSpec\n"
        f"spec = HarnessSpec(name={name!r}, description='Installed example', "
        "runtime='python', dockerfile='Dockerfile', setup_script='setup.sh', "
        f"run_script='run.sh', requires_credentials={credentials})\n"
    )


def test_real_distribution_visible_in_cli_and_credential_matrix(installed, monkeypatch):
    installed("cloud_example", spec_source(credentials="['HB_EXAMPLE_KEY']"))
    monkeypatch.delenv("HB_EXAMPLE_KEY", raising=False)
    result = CliRunner().invoke(main, ["harnesses"])
    assert result.exit_code == 0
    assert "installed-example" in result.output
    assert "skipped: set HB_EXAMPLE_KEY" in result.output
    result = CliRunner().invoke(main, [
        "matrix", "--harness", "installed-example", "--model", "example", "--case", "case-a",
    ])
    assert result.exit_code == 0
    assert "total=1 eligible=0 skipped=1" in result.output
    row = expand(["installed-example"], ["example"], [{"id": "a"}],
                 env={"HB_EXAMPLE_KEY": "present"})[0]
    assert row.is_eligible


@pytest.mark.parametrize("credentials", ["None", "()", "[]", "('HB_A', 'HB_B')"])
def test_supported_credential_shapes(installed, credentials):
    installed("credential_shape", spec_source(credentials=credentials))
    regs = {r.spec.name: r for r in discover_registrations()}
    assert "installed-example" in regs
    assert regs["installed-example"].requires_credentials == (
        ("HB_A", "HB_B") if "HB_A" in credentials else ()
    )


@pytest.mark.parametrize("body", [
    "raise RuntimeError('super-secret-value')",
    "spec = object()",
    spec_source(credentials="'HB_KEY'"),
    spec_source(credentials="[123]"),
    spec_source(credentials="['']"),
    spec_source(name=""),
    spec_source().replace("runtime='python'", "runtime='unsupported'"),
])
def test_broken_or_invalid_specs_warn_without_exception_details(installed, body):
    installed("broken_example", body)
    with pytest.warns(RuntimeWarning, match="broken_example") as caught:
        regs = discover_registrations()
    assert "super-secret-value" not in str([w.message for w in caught])
    assert {r.spec.name for r in regs} >= {"openclaw", "hermes", "stagehand"}
    assert "installed-example" not in {r.spec.name for r in regs}


def test_builtin_installed_reexport_is_quiet(installed):
    installed("builtin_reexport", "from harnessbench.harnesses.openclaw import spec\n")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        regs = discover_registrations()
    assert not caught
    assert sum(r.spec.name == "openclaw" for r in regs) == 1


def test_external_package_cannot_replace_builtin(installed):
    installed("builtin_override", spec_source(name="openclaw", credentials="['HB_BAD']"))
    with pytest.warns(RuntimeWarning, match="bundled name 'openclaw'"):
        regs = discover_registrations()
    reg = next(r for r in regs if r.spec.name == "openclaw")
    assert reg.requires_credentials == ()


def test_all_conflicting_external_names_excluded(installed):
    installed("duplicate_b", spec_source())
    installed("duplicate_a", spec_source())
    with pytest.warns(RuntimeWarning, match="conflicting harness registrations"):
        regs = discover_registrations()
    assert "installed-example" not in {r.spec.name for r in regs}


def test_source_checkout_retains_six_builtins():
    assert {r.spec.name for r in discover_registrations()} >= {
        "openclaw", "hermes", "claw-code", "stagehand", "browser-use", "coze-studio",
    }


def test_valid_plugins_survive_broken_neighbors_in_sorted_order(installed):
    installed("valid_z", spec_source(name="z-example"))
    installed("valid_a", spec_source(name="a-example"))
    installed("missing_export", "other = 1\n")
    with pytest.warns(RuntimeWarning, match="missing_export.*AttributeError"):
        regs = discover_registrations()
    names = [r.spec.name for r in regs]
    assert names.index("a-example") < names.index("z-example")
