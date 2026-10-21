"""Opt-in execution against the supported ClawBench command-line contract."""

from types import SimpleNamespace

from click.testing import CliRunner
import pytest

from harnessbench.cli import main


@pytest.mark.parametrize("command", ["run", "batch"])
def test_native_backend_preserves_public_cli_contract(monkeypatch, tmp_path, command):
    calls = []
    monkeypatch.setattr("harnessbench.cli.uuid4", lambda: SimpleNamespace(hex="test-cell"))
    monkeypatch.setattr("shutil.which", lambda name: "/venv/bin/clawbench-run")
    monkeypatch.setattr(
        "subprocess.run",
        lambda argv, **kw: (calls.append((argv, kw)) or SimpleNamespace(returncode=0)),
    )
    case = tmp_path / "case with spaces" / "task.json"
    result = CliRunner().invoke(
        main,
        [
            command,
            "--backend",
            "clawbench-cli",
            "--harness",
            "browser-use",
            "--model",
            "provider/model",
            "--case",
            str(case),
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )
    assert result.exit_code == 0, result.output
    assert calls == [
        (
            [
                "/venv/bin/clawbench-run",
                "--harness",
                "browser-use",
                "--output-dir",
                str(tmp_path / "out" / "cell-test-cell")
                if command == "batch"
                else str(tmp_path / "out"),
                "--no-upload",
                "--",
                str(case),
                "provider/model",
            ],
            {"check": False},
        )
    ]
    assert not (tmp_path / "out").exists()  # ClawBench owns output/metadata creation.


@pytest.mark.parametrize("command", ["run", "batch"])
@pytest.mark.parametrize("harness", ["stagehand", "coze-studio"])
def test_native_backend_rejects_unsupported_harness_before_execution(monkeypatch, command, harness):
    monkeypatch.setenv("COZE_API_TOKEN", "test-only")
    monkeypatch.setenv("COZE_PROJECT_ID", "test-only")
    monkeypatch.setattr("subprocess.run", lambda *a, **k: pytest.fail("must not launch"))
    result = CliRunner().invoke(
        main,
        [
            command,
            "--backend",
            "clawbench-cli",
            "--harness",
            harness,
            "--model",
            "m",
            "--case",
            "case",
        ],
    )
    assert result.exit_code != 0
    assert "not supported by the native ClawBench CLI" in result.output


def test_native_batch_validates_all_harnesses_before_launch(monkeypatch):
    monkeypatch.setattr("subprocess.run", lambda *a, **k: pytest.fail("must not launch"))
    result = CliRunner().invoke(
        main,
        [
            "batch",
            "--backend",
            "clawbench-cli",
            "--harness",
            "openclaw",
            "--harness",
            "stagehand",
            "--model",
            "m",
            "--case",
            "c",
        ],
    )
    assert result.exit_code != 0
    assert "stagehand" in result.output


def test_native_backend_missing_command_is_actionable(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: None)
    result = CliRunner().invoke(
        main,
        [
            "run",
            "--backend",
            "clawbench-cli",
            "--harness",
            "openclaw",
            "--model",
            "m",
            "--case",
            "case",
        ],
    )
    assert result.exit_code != 0
    assert "clawbench-run" in result.output
    assert "PATH" in result.output


@pytest.mark.parametrize("returncode", [1, 2, 3])
def test_native_backend_propagates_exit_status(monkeypatch, returncode):
    monkeypatch.setattr("shutil.which", lambda _: "/bin/clawbench-run")
    monkeypatch.setattr("subprocess.run", lambda *a, **k: SimpleNamespace(returncode=returncode))
    result = CliRunner().invoke(
        main,
        [
            "run",
            "--backend",
            "clawbench-cli",
            "--harness",
            "hermes",
            "--model",
            "m",
            "--case",
            "case",
        ],
    )
    assert result.exit_code == returncode


def test_native_batch_stops_after_failed_case(monkeypatch):
    calls = []
    monkeypatch.setattr("shutil.which", lambda _: "/bin/clawbench-run")
    monkeypatch.setattr(
        "subprocess.run", lambda argv, **k: (calls.append(argv) or SimpleNamespace(returncode=3))
    )
    result = CliRunner().invoke(
        main,
        [
            "batch",
            "--backend",
            "clawbench-cli",
            "--harness",
            "hermes",
            "--model",
            "m",
            "--case",
            "first",
            "--case",
            "second",
        ],
    )
    assert result.exit_code == 3
    assert len(calls) == 1
    assert calls[0][-2] == "first"


def test_dry_run_does_not_require_or_launch_native_cli(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: pytest.fail("no discovery needed"))
    result = CliRunner().invoke(
        main,
        [
            "batch",
            "--backend",
            "clawbench-cli",
            "--dry-run",
            "--harness",
            "browser-use",
            "--model",
            "m",
            "--case",
            "case",
        ],
    )
    assert result.exit_code == 0, result.output


def test_default_backend_retains_existing_run_case_api(monkeypatch, tmp_path):
    import sys

    calls = []
    monkeypatch.setitem(
        sys.modules, "clawbench", SimpleNamespace(run_case=lambda **kwargs: calls.append(kwargs))
    )
    result = CliRunner().invoke(
        main,
        [
            "run",
            "--harness",
            "openclaw",
            "--model",
            "m",
            "--case",
            "c",
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )
    assert result.exit_code == 0, result.output
    assert calls == [
        {
            "case": "c",
            "model": "m",
            "harness": "openclaw",
            "output_dir": tmp_path / "out",
            "no_upload": True,
        }
    ]


def test_native_backend_reports_launch_errors(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: "/bin/clawbench-run")

    def denied(*args, **kwargs):
        raise PermissionError("not executable")

    monkeypatch.setattr("subprocess.run", denied)
    result = CliRunner().invoke(
        main,
        [
            "run",
            "--backend",
            "clawbench-cli",
            "--harness",
            "hermes",
            "--model",
            "m",
            "--case",
            "case",
        ],
    )
    assert result.exit_code == 1
    assert "Could not start clawbench-run" in result.output


def test_native_backend_preserves_option_like_task_and_model(monkeypatch, tmp_path):
    from harnessbench import native

    calls = []
    monkeypatch.setattr("shutil.which", lambda _: "/bin/clawbench-run")
    monkeypatch.setattr(
        "subprocess.run", lambda argv, **k: (calls.append(argv) or SimpleNamespace(returncode=0))
    )
    native.run_case(
        case="--help", model="-model", harness="browser-use", output_dir=tmp_path, no_upload=False
    )
    assert calls[0][-3:] == ["--", "--help", "-model"]
    assert "--no-upload" not in calls[0]


@pytest.mark.parametrize("command", ["run", "batch"])
@pytest.mark.parametrize(
    "option,no_upload", [(None, True), ("--no-upload", True), ("--upload", False)]
)
def test_native_upload_controls_preserve_explicit_choice(monkeypatch, command, option, no_upload):
    calls = []
    monkeypatch.setattr("shutil.which", lambda _: "/bin/clawbench-run")
    monkeypatch.setattr(
        "subprocess.run", lambda argv, **k: (calls.append(argv) or SimpleNamespace(returncode=0))
    )
    args = [
        command,
        "--backend",
        "clawbench-cli",
        "--harness",
        "openclaw",
        "--model",
        "m",
        "--case",
        "case",
    ]
    if option:
        args.append(option)
    result = CliRunner().invoke(main, args)
    assert result.exit_code == 0, result.output
    assert ("--no-upload" in calls[0]) is no_upload


def test_native_batch_retains_same_basename_runs_in_distinct_output_bases(monkeypatch, tmp_path):
    from pathlib import Path

    monkeypatch.setattr("shutil.which", lambda _: "/bin/clawbench-run")

    def native_output(argv, **kwargs):
        # Native ClawBench derives the run folder from case basename, model and
        # second-resolution timestamp. Emulate two runs starting in that second.
        base = Path(argv[argv.index("--output-dir") + 1])
        run = base / "model" / "openclaw-task-model-fixed-second"
        run.mkdir(parents=True, exist_ok=True)
        (run / "run-meta.json").write_text(argv[-2])
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr("subprocess.run", native_output)
    result = CliRunner().invoke(
        main,
        [
            "batch",
            "--backend",
            "clawbench-cli",
            "--harness",
            "openclaw",
            "--model",
            "model",
            "--case",
            "/first/task.json",
            "--case",
            "/second/task.json",
            "--output-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output
    traces = list(tmp_path.rglob("run-meta.json"))
    assert len(traces) == 2
    assert {p.read_text() for p in traces} == {"/first/task.json", "/second/task.json"}
