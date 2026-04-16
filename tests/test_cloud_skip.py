"""Cloud-opt-in gating must skip, not fail, when credentials are missing."""

from __future__ import annotations

from harnessbench.matrix import expand


def _cases():
    return [{"id": "smoke-1"}]


def test_stagehand_skipped_without_browserbase_key():
    specs = expand(
        harnesses=["stagehand"],
        models=["gpt-4o-mini"],
        cases=_cases(),
        env={},
    )
    assert len(specs) == 1
    s = specs[0]
    assert s.status == "skipped"
    assert s.skip_reason
    assert "BROWSERBASE_API_KEY" in s.skip_reason


def test_stagehand_eligible_with_browserbase_key():
    specs = expand(
        harnesses=["stagehand"],
        models=["gpt-4o-mini"],
        cases=_cases(),
        env={"BROWSERBASE_API_KEY": "bb_live_test"},
    )
    assert specs[0].status == "eligible"


def test_coze_studio_requires_both_vars():
    only_url = expand(
        harnesses=["coze-studio"],
        models=["gpt-4o-mini"],
        cases=_cases(),
        env={"COZE_INSTANCE_URL": "https://coze.example"},
    )
    assert only_url[0].status == "skipped"
    assert "COZE_API_TOKEN" in only_url[0].skip_reason

    both = expand(
        harnesses=["coze-studio"],
        models=["gpt-4o-mini"],
        cases=_cases(),
        env={
            "COZE_INSTANCE_URL": "https://coze.example",
            "COZE_API_TOKEN": "pat_test",
        },
    )
    assert both[0].status == "eligible"


def test_local_harnesses_unaffected_by_missing_cloud_vars():
    specs = expand(
        harnesses=["openclaw", "hermes", "browser-use", "claw-code"],
        models=["gpt-4o-mini"],
        cases=_cases(),
        env={},
    )
    for s in specs:
        assert s.status == "eligible", f"{s.harness} should be eligible"
