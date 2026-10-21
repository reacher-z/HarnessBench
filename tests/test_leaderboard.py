"""Leaderboard accounting and diagnostics must expose incomplete result sets."""

from __future__ import annotations

import json

import pytest

from harnessbench.leaderboard import aggregate, load_results, render_markdown


def write_result(root, name, value):
    directory = root / name
    directory.mkdir()
    path = directory / "result.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_every_result_belongs_to_one_visible_bucket():
    results = [
        {"status": "completed", "passed": True},
        {"status": "completed", "score": 1},
        {"status": "completed", "passed": False},
        {"status": "error"},
        {"status": "timeout"},
        {"status": "crashed"},
        {},
        {"status": "skipped", "score": 1},
    ]
    (row,) = aggregate({"harness": "h", "model": "m", **result} for result in results)
    assert (row.passed, row.failed, row.skipped, row.total) == (2, 5, 1, 8)
    assert row.passed + row.failed + row.skipped == row.total
    assert row.score_pct == pytest.approx(200 / 7)
    markdown = render_markdown([row])
    assert "| Failed |" in markdown
    assert "| `h` | `m` | 2 | 5 | 1 | 8 | 28.6% |" in markdown


def test_skipped_only_results_have_zero_score():
    (row,) = aggregate([{"status": "skipped"}])
    assert row.failed == 0
    assert row.score_pct == 0


def test_empty_results_render_explicit_message():
    assert aggregate([]) == []
    assert render_markdown([]) == "_(no results)_\n"


def test_models_are_separate_and_rows_have_stable_tie_order():
    rows = aggregate(
        [
            {"harness": "z", "model": "b", "passed": True},
            {"harness": "a", "model": "z", "passed": False},
            {"harness": "a", "model": "b", "passed": True},
            {"harness": "z", "model": "a", "passed": True},
        ]
    )
    assert [(row.harness, row.model) for row in rows] == [
        ("a", "b"),
        ("z", "a"),
        ("z", "b"),
        ("a", "z"),
    ]


@pytest.mark.parametrize("payload", ["{broken", b"\xff"])
def test_unreadable_results_warn_and_preserve_valid_results(tmp_path, payload):
    good = {"harness": "h", "model": "m", "passed": True}
    write_result(tmp_path, "a-good", good)
    directory = tmp_path / "b-bad"
    directory.mkdir()
    bad = directory / "result.json"
    bad.write_bytes(payload if isinstance(payload, bytes) else payload.encode())
    with pytest.warns(UserWarning, match="b-bad[/\\\\]result.json"):
        assert load_results(tmp_path) == [good]


@pytest.mark.parametrize(
    "value",
    [None, [], "text", 42, True, {"harness": []}, {"model": {}},
     {"harness": None}, {"model": 1}],
)
def test_invalid_result_shape_warns_instead_of_breaking_aggregation(tmp_path, value):
    write_result(tmp_path, "bad-shape", value)
    with pytest.warns(UserWarning, match="bad-shape[/\\\\]result.json"):
        assert aggregate(load_results(tmp_path)) == []


def test_optional_partition_metadata_keeps_unknown_bucket(tmp_path):
    write_result(tmp_path, "minimal", {"passed": True})
    (row,) = aggregate(load_results(tmp_path))
    assert (row.harness, row.model, row.passed) == ("unknown", "unknown", 1)


def test_oserror_warns_with_path(tmp_path, monkeypatch):
    path = write_result(tmp_path, "unreadable", {})

    def denied(*args, **kwargs):
        raise PermissionError("test permission denied")

    monkeypatch.setattr(type(path), "read_text", denied)
    with pytest.warns(UserWarning, match="unreadable[/\\\\]result.json"):
        assert load_results(tmp_path) == []
