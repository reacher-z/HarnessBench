"""A credential-skipped batch does not require the execution backend."""

from __future__ import annotations

import builtins
import sys
from types import SimpleNamespace

from click.testing import CliRunner

from harnessbench.cli import main


def clear_cloud_credentials(monkeypatch):
    for key in ("BROWSERBASE_API_KEY", "COZE_INSTANCE_URL", "COZE_API_TOKEN", "COZE_WORKFLOW_ID"):
        monkeypatch.delenv(key, raising=False)


def test_skipped_only_batch_reports_reasons_without_import_or_output(monkeypatch, tmp_path):
    clear_cloud_credentials(monkeypatch)
    imports = []
    original_import = builtins.__import__

    def no_backend(name, *args, **kwargs):
        if name == "clawbench":
            imports.append(name)
            raise ImportError("execution backend deliberately unavailable")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", no_backend)
    output = tmp_path / "not-created"
    result = CliRunner().invoke(main, [
        "batch", "-h", "stagehand", "-h", "coze-studio", "-m", "model",
        "-c", "first", "-c", "second", "--output-dir", str(output),
    ])
    assert result.exit_code == 0, result.output
    assert "total=4 eligible=0 skipped=4" in result.output
    for case in ("first", "second"):
        stagehand = f"skip: stagehand model {case} (missing_credential:BROWSERBASE_API_KEY)"
        coze = f"skip: coze-studio model {case} (missing_credential:COZE_INSTANCE_URL"
        assert stagehand in result.output
        assert coze in result.output
    assert imports == []
    assert not output.exists()


def test_mixed_batch_delegates_only_eligible_cells(monkeypatch, tmp_path):
    clear_cloud_credentials(monkeypatch)
    calls = []
    monkeypatch.setitem(
        sys.modules, "clawbench", SimpleNamespace(run_case=lambda **kw: calls.append(kw))
    )
    output = tmp_path / "output"
    result = CliRunner().invoke(main, [
        "batch", "-h", "stagehand", "-h", "openclaw", "-m", "model",
        "-c", "first", "-c", "second", "--output-dir", str(output),
    ])
    assert result.exit_code == 0, result.output
    assert "total=4 eligible=2 skipped=2" in result.output
    assert [call["case"] for call in calls] == ["first", "second"]
    assert all(call["harness"] == "openclaw" and call["no_upload"] for call in calls)
    assert all(call["output_dir"] == output for call in calls)
    assert "skip: stagehand model first (missing_credential:BROWSERBASE_API_KEY)" in result.output
    assert output.is_dir()


def test_eligible_batch_still_reports_unavailable_runner(monkeypatch, tmp_path):
    monkeypatch.setitem(sys.modules, "clawbench", None)
    output = tmp_path / "not-created"
    result = CliRunner().invoke(main, [
        "batch", "-h", "openclaw", "-m", "model", "-c", "case",
        "--output-dir", str(output),
    ])
    assert result.exit_code == 10
    assert "does not yet expose `run_case`" in result.output
    assert not output.exists()
