from __future__ import annotations

import sys
from types import ModuleType

import pytest
from click.testing import CliRunner

from harnessbench.cli import main


@pytest.mark.parametrize("command", ["run", "batch"])
@pytest.mark.parametrize("option,expected", [(None, True), ("--no-upload", True), ("--upload", False)])
def test_upload_is_explicitly_controlled(monkeypatch, tmp_path, command, option, expected):
    calls = []
    clawbench = ModuleType("clawbench")
    clawbench.run_case = lambda **kwargs: calls.append(kwargs)
    monkeypatch.setitem(sys.modules, "clawbench", clawbench)
    args = [command, "--harness", "openclaw", "--model", "test-model", "--case", "smoke",
            "--output-dir", str(tmp_path / "results")]
    if option:
        args.append(option)
    result = CliRunner().invoke(main, args)
    assert result.exit_code == 0, result.output
    assert len(calls) == 1
    assert calls[0]["no_upload"] is expected


def test_dry_run_does_not_upload_or_import_runner(tmp_path):
    result = CliRunner().invoke(main, ["batch", "--harness", "openclaw", "--model", "test-model",
                                     "--case", "smoke", "--upload", "--dry-run",
                                     "--output-dir", str(tmp_path / "results")])
    assert result.exit_code == 0, result.output
    assert not (tmp_path / "results").exists()
