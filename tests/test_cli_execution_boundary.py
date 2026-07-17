"""The unreleased execution bridge must fail before creating run artifacts."""

from __future__ import annotations

import sys
import types

import pytest
from click.testing import CliRunner

from harnessbench.cli import main


@pytest.mark.parametrize(
    ("command", "args"),
    [
        (
            "run",
            ["--harness", "openclaw", "--model", "test-model", "--case", "test-case"],
        ),
        (
            "batch",
            ["--harness", "openclaw", "--model", "test-model", "--case", "test-case"],
        ),
    ],
)
def test_execution_stops_before_creating_output_without_public_runner(
    command, args, tmp_path, monkeypatch
):
    monkeypatch.setitem(sys.modules, "clawbench", types.ModuleType("clawbench"))
    output_dir = tmp_path / "harness-output"

    result = CliRunner().invoke(
        main,
        [command, *args, "--output-dir", str(output_dir)],
    )

    assert result.exit_code == 10
    assert "execution is unavailable" in result.output.lower()
    assert not output_dir.exists()
