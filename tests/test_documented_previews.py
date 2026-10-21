"""The documented matrix examples must parse without executing a backend."""

from __future__ import annotations

import re
import shlex
from pathlib import Path

import pytest
from click.testing import CliRunner

from harnessbench.cli import main


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = ("README.md", "README.zh-CN.md", "docs/adding-a-harness.md", "docs/cloud-harness-setup.md")


@pytest.mark.parametrize("document", DOCUMENTS)
def test_documented_matrix_and_batch_examples_parse(document, monkeypatch):
    for variable in ("BROWSERBASE_API_KEY", "COZE_INSTANCE_URL", "COZE_API_TOKEN", "COZE_WORKFLOW_ID"):
        monkeypatch.delenv(variable, raising=False)
    text = (ROOT / document).read_text(encoding="utf-8")
    checked = 0
    for block in re.findall(r"```[^\n]*\n(.*?)```", text, flags=re.S):
        block = block.replace("\\\n", " ")
        for line in block.splitlines():
            line = line.removeprefix("$ ")
            if not re.match(r"harness-bench (matrix|batch)\b", line):
                continue
            args = shlex.split(line)[1:]
            # The adapter guide uses the name of the reader's new harness.
            args = ["openclaw" if arg == "my-harness" else arg for arg in args]
            if args[0] == "batch" and "--dry-run" not in args:
                args.append("--dry-run")
            result = CliRunner().invoke(main, args)
            assert result.exit_code == 0, f"{document}: {line}\n{result.output}"
            assert "total=" in result.output
            checked += 1
    assert checked, f"No preview examples checked in {document}"


@pytest.mark.parametrize("document", ["README.md", "README.zh-CN.md"])
def test_fixture_links_in_quickstarts_exist(document):
    text = (ROOT / document).read_text(encoding="utf-8")
    for relative in re.findall(r"\]\((fixtures/[^)]+)\)", text):
        assert (ROOT / relative).is_file(), f"{document}: missing {relative}"
