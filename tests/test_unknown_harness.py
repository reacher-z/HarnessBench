from click.testing import CliRunner
import pytest

from harnessbench.cli import main


@pytest.mark.parametrize("command", ["matrix", "batch"])
def test_unknown_harness_is_an_actionable_usage_error(command, tmp_path):
    args = [command, "--harness", "openclaww", "--model", "test-model", "--case", "smoke"]
    if command == "batch":
        args += ["--output-dir", str(tmp_path / "results")]
    result = CliRunner().invoke(main, args)
    assert result.exit_code == 2, result.output
    assert "--harness" in result.output
    assert "unknown harness" in result.output
    assert "openclaww" in result.output
    assert not (tmp_path / "results").exists()


@pytest.mark.parametrize("command", ["matrix", "batch"])
def test_known_harness_previews_remain_supported(command):
    args = [command, "--harness", "openclaw", "--model", "test-model", "--case", "smoke"]
    if command == "batch":
        args.append("--dry-run")
    result = CliRunner().invoke(main, args)
    assert result.exit_code == 0, result.output
    assert "openclaw" in result.output
