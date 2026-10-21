"""Coze's preflight gate must match the actual shell launch requirements."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from click.testing import CliRunner

from harnessbench.cli import main
from harnessbench.matrix import expand


REQUIRED = ("COZE_INSTANCE_URL", "COZE_API_TOKEN", "COZE_WORKFLOW_ID")
CREDENTIALS = {
    "COZE_INSTANCE_URL": "https://coze.example",
    "COZE_API_TOKEN": "test-token",
    "COZE_WORKFLOW_ID": "test-workflow",
}


def test_preflight_requirements_match_shell_parameter_checks():
    script = (
        Path(__file__).resolve().parents[1]
        / "src/harnessbench/harnesses/coze_studio/run.sh"
    ).read_text()
    required_by_shell = re.findall(r'\$\{(COZE_\w+):\?', script)
    assert set(required_by_shell) == set(REQUIRED)
    (spec,) = expand(["coze-studio"], ["model"], [{"id": "case"}], env={})
    assert spec.skip_reason == "missing_credential:" + ",".join(required_by_shell)


@pytest.mark.parametrize("missing", REQUIRED)
def test_every_runtime_requirement_gates_matrix(monkeypatch, missing):
    for key, value in CREDENTIALS.items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv(missing)
    env = {key: value for key, value in CREDENTIALS.items() if key != missing}
    (spec,) = expand(["coze-studio"], ["model"], [{"id": "case"}], env=env)
    assert not spec.is_eligible
    assert spec.skip_reason == f"missing_credential:{missing}"



@pytest.mark.parametrize("command", ["harnesses", "run"])
@pytest.mark.parametrize("missing", REQUIRED)
def test_every_runtime_requirement_gates_cli(monkeypatch, tmp_path, command, missing):
    for key, value in CREDENTIALS.items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv(missing)
    calls = []
    monkeypatch.setitem(
        sys.modules, "clawbench", SimpleNamespace(run_case=lambda **kw: calls.append(kw))
    )
    args = [command]
    if command == "run":
        args += [
            "--harness", "coze-studio", "--model", "model", "--case", "case",
            "--output-dir", str(tmp_path / "not-created"),
        ]
    result = CliRunner().invoke(main, args)
    if command == "harnesses":
        assert result.exit_code == 0
        (coze_line,) = (
            line for line in result.output.splitlines() if line.startswith("coze-studio")
        )
        assert f"skipped: set {missing}" in coze_line
    else:
        assert result.exit_code == 3
        assert f"requires {missing}" in result.output
        assert calls == []
        assert not (tmp_path / "not-created").exists()


def test_all_requirements_allow_delegate_without_changing_environment(monkeypatch, tmp_path):
    for key, value in CREDENTIALS.items():
        monkeypatch.setenv(key, value)
    calls = []
    monkeypatch.setitem(
        sys.modules, "clawbench", SimpleNamespace(run_case=lambda **kw: calls.append(kw))
    )
    (spec,) = expand(["coze-studio"], ["model"], [{"id": "case"}], env=CREDENTIALS)
    assert spec.is_eligible
    result = CliRunner().invoke(main, [
        "run", "--harness", "coze-studio", "--model", "model", "--case", "case",
        "--output-dir", str(tmp_path),
    ])
    assert result.exit_code == 0, result.output
    assert len(calls) == 1
    assert calls[0]["harness"] == "coze-studio"
    assert calls[0]["no_upload"] is True
