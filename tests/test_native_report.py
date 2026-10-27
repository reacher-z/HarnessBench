"""Inventory raw native metadata without converting it to benchmark scores."""
import json

from click.testing import CliRunner

from harnessbench.cli import main


def test_native_report_command_exists(tmp_path):
    result = CliRunner().invoke(main, ["native-report", "--results-dir", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "Raw recorded flags" in result.output


def write_meta(root, name, value):
    path = root / name / "run-meta.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(value))
    return path


def report_for(root):
    result = CliRunner().invoke(main, ["native-report", "--results-dir", str(root),
                                       "--format", "json"])
    assert result.exit_code == 0, result.output
    return json.loads(result.output)


def test_real_upstream_writer_fixture_is_unjudged_raw_pass():
    from pathlib import Path
    report = report_for(Path(__file__).parent / "fixtures/native-writer")
    attempt, = report["attempts"]
    assert attempt["flags"] == {"pass":"true", "intercepted":"true",
                                 "infra_failure":"false", "judge_match":"missing"}
    assert attempt["judge_mode"] == "off"
    assert attempt["agent_config_sha256"]
    assert attempt["judge_config_sha256"] is None
    assert attempt["task_sha256"] == "a" * 64
    assert attempt["provenance_sha256"]
    assert "PRIVATE_" not in json.dumps(report)
    assert "pass=true does not establish judged success" in report["notice"]


def test_flags_are_strict_and_attempts_are_not_deduplicated(tmp_path):
    for i, value in enumerate([True, False, None, 1, "true", [], {}]):
        write_meta(tmp_path, str(i), {key:value for key in
                   ["pass", "intercepted", "infra_failure", "judge_match"]})
    write_meta(tmp_path, "missing", {})
    write_meta(tmp_path, "duplicate", {"pass":True})
    report = report_for(tmp_path)
    assert report["attempt_count"] == 9
    assert report["flag_counts"]["pass"] == dict(true=2, false=1, null=1, invalid=4, missing=1)
    assert report["flag_counts"]["intercepted"]["missing"] == 2


def test_modes_and_configuration_identities_stay_per_attempt(tmp_path):
    for name, flag, config in [("on", False, "a"), ("off", True, "b"),
                                ("null", None, "c"), ("invalid", 1, "d")]:
        write_meta(tmp_path, name, {"run_flags":{"no_judge":flag},
                   "model_config":{"sanitized_config_sha256":config*64},
                   "judge_config":{"sanitized_config_sha256":"e"*64}})
    report = report_for(tmp_path)
    assert report["judge_mode_counts"] == {"unknown":2, "off":1, "on":1}
    assert len({a["agent_config_sha256"] for a in report["attempts"]}) == 4


def test_malformed_records_warn_without_leaking_contents_or_paths(tmp_path):
    for name, text in [("PRIVATE_PATH", "PRIVATE_ERROR"), ("list", "[]"),
                        ("unicode", "\udcff")]:
        path = tmp_path / name / "run-meta.json"
        path.parent.mkdir()
        path.write_bytes(text.encode('utf-8', errors='surrogateescape'))
    report = report_for(tmp_path)
    assert report["attempt_count"] == 0
    assert len(report["warnings"]) == 3
    assert "PRIVATE_" not in json.dumps(report)


def test_markdown_escapes_untrusted_cells_and_omits_sensitive_metadata(tmp_path):
    write_meta(tmp_path, "one", {"harness":"<img>|[link](evil)\nline",
                               "model":"*bold*`code`", "email_used":"PRIVATE_EMAIL",
                               "instruction":"PRIVATE_INSTRUCTION", "failure_reason":"PRIVATE_ERROR",
                               "task_json_sha256":"PRIVATE_NOT_A_HASH",
                               "model_config":{"api_key":"PRIVATE_SECRET"}})
    result = CliRunner().invoke(main, ["native-report", "--results-dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "PRIVATE_" not in result.output
    assert "&lt;img&gt;&#124;&#91;link&#93;" in result.output
    assert "&#42;bold&#42;&#96;code&#96;" in result.output


def test_symlink_files_are_not_read(tmp_path):
    outside = tmp_path / 'outside.json'
    outside.write_text('{"pass":true}')
    (tmp_path / 'run-meta.json').symlink_to(outside)
    report = report_for(tmp_path)
    assert report['attempt_count'] == 0
    assert report['warnings'] == ['File 1: skipped symbolic link']


def test_other_json_files_are_ignored_and_command_does_not_write(tmp_path):
    (tmp_path / 'legacy.json').write_text('{"pass":true}')
    before = sorted(p.name for p in tmp_path.iterdir())
    assert report_for(tmp_path)['attempt_count'] == 0
    assert before == sorted(p.name for p in tmp_path.iterdir())


def test_provenance_differences_are_preserved_without_rendering_private_fields(tmp_path):
    for name, commit in [('one', 'a'), ('two', 'b')]:
        write_meta(tmp_path, name, {'pass':True, 'provenance':{
            'clawbench':{'commit':commit}, 'private_origin':'PRIVATE_URL'}})
    report = report_for(tmp_path)
    assert len({a['provenance_sha256'] for a in report['attempts']}) == 2
    assert report['attempt_count'] == 2
    assert 'PRIVATE_URL' not in json.dumps(report)


def test_ambiguous_or_nonstandard_json_is_rejected(tmp_path):
    for name, text in [('duplicate', '{"pass":true,"pass":false}'),
                       ('nan', '{"pass":NaN}'), ('infinity', '{"pass":Infinity}'),
                       ('nested_duplicate', '{"run_flags":{"no_judge":true,"no_judge":false}}')]:
        path = tmp_path / name / 'run-meta.json'
        path.parent.mkdir()
        path.write_text(text)
    report = report_for(tmp_path)
    assert report['attempt_count'] == 0
    assert len(report['warnings']) == 4


def test_record_limit_is_enforced(tmp_path, monkeypatch):
    from harnessbench import native_report
    monkeypatch.setattr(native_report, 'MAX_RECORD_BYTES', 20)
    write_meta(tmp_path, 'one', {'model':'x' * 50})
    report = report_for(tmp_path)
    assert report['attempt_count'] == 0
    assert len(report['warnings']) == 1


def test_provenance_encoding_failure_does_not_discard_attempt(tmp_path, monkeypatch):
    from harnessbench import native_report
    write_meta(tmp_path, 'one', {'pass':True, 'provenance':{'nested':'fixture'}})
    original_dumps = native_report.json.dumps

    def limited_dumps(value, **kwargs):
        if value == {'nested':'fixture'}:
            raise RecursionError('PRIVATE_RECURSION_ERROR')
        return original_dumps(value, **kwargs)

    monkeypatch.setattr(native_report.json, 'dumps', limited_dumps)
    report = native_report.inventory(tmp_path)
    assert report['attempt_count'] == 1
    assert report['attempts'][0]['provenance_sha256'] is None
    assert report['warnings'] == ['File 1: provenance could not be fingerprinted']
