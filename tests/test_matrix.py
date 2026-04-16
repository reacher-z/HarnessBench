"""Matrix-expansion semantics."""

from __future__ import annotations

from harnessbench.matrix import expand, summarize


def _cases():
    return [{"id": "a"}, {"id": "b"}]


def test_cartesian_expansion_count():
    specs = expand(
        harnesses=["openclaw", "hermes"],
        models=["gpt-4o-mini", "claude-sonnet-4-6"],
        cases=_cases(),
        env={},
    )
    # 2 harnesses x 2 models x 2 cases = 8
    assert len(specs) == 8


def test_dedup_identical_triples():
    specs = expand(
        harnesses=["openclaw", "openclaw"],
        models=["gpt-4o-mini"],
        cases=_cases(),
        env={},
    )
    # duplicate harness collapsed
    assert len({(s.harness, s.model, s.case["id"]) for s in specs}) == 2


def test_summarize_reports_eligible_vs_skipped():
    specs = expand(
        harnesses=["openclaw", "stagehand"],
        models=["gpt-4o-mini"],
        cases=[{"id": "a"}],
        env={},
    )
    summary = summarize(specs)
    assert summary["eligible"] == 1
    assert summary["skipped"] == 1


def test_unknown_harness_raises():
    import pytest

    with pytest.raises(KeyError):
        expand(
            harnesses=["does-not-exist"],
            models=["gpt-4o-mini"],
            cases=_cases(),
            env={},
        )
