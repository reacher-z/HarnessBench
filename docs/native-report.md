# Inspect native ClawBench attempts

`harness-bench native-report` inventories the `run-meta.json` files produced by
ClawBench's native runner. It reads existing local results and writes its report
to stdout. It does not run a harness, judge, upload results or modify input files.

```bash
harness-bench native-report --results-dir ./test-output
harness-bench native-report --results-dir ./test-output --format json > attempts.json
```

Each readable JSON object becomes one attempt, including repeated runs of the
same task. Only files named `run-meta.json` are inspected; legacy leaderboard
JSON files remain the responsibility of `harness-bench leaderboard`.

The report shows the raw `pass`, `intercepted`, `infra_failure` and `judge_match`
flags separately, with distinct `true`, `false`, `missing`, `null` and `invalid`
states. Numbers and strings are not coerced into booleans. Totals count recorded
flags, **not task success rates**. ClawBench can record `pass=true` with judging
disabled or with no judge result. An enabled judge policy alone does not establish
that judging completed. No rankings, deduplication or comparability claims are
made.

Every row retains the harness/model labels, task SHA256 and separate agent/judge
sanitized configuration SHA256 values when valid. Judge mode comes from the
strict boolean `run_flags.no_judge`: true means off, false means on, and any
other or missing value means unknown. A SHA256 fingerprint of the supplied
provenance object distinguishes recorded provenance without displaying its raw
fields. Fingerprints are identities of recorded data, not attestations of truth
or proof that two runs are comparable. Unknown hashes remain unknown.

Only these selected fields are emitted. Instructions, emails, input/output paths,
raw configuration, failure messages and raw provenance are omitted. Harness and
model labels are still user-supplied data; review reports before sharing them.
Markdown labels are escaped and limited to 200 printable characters.

Malformed, unreadable, non-object and oversized records are skipped with warnings
inside the report. Duplicate JSON keys and non-finite constants are rejected.
The per-file limit is 16 MiB. Symbolic-link files are skipped; symbolic-link
folders are not traversed. File numbers identify the sorted traversal positions
for this invocation; they are not persistent run IDs. This diagnostic inventory
has no official leaderboard submission or acceptance semantics.

The format is verified against ClawBench revision
`07eb50a3d4c5a799f5ad4eebd57c67c10417787f`:
[`metadata.py`](https://github.com/TIGER-AI-Lab/ClawBench/blob/07eb50a3d4c5a799f5ad4eebd57c67c10417787f/src/clawbench/runner/run_support/metadata.py)
and
[`run.py`](https://github.com/TIGER-AI-Lab/ClawBench/blob/07eb50a3d4c5a799f5ad4eebd57c67c10417787f/src/clawbench/runner/run.py).
The test fixture was generated with that revision's metadata writer and raw
pass expression, with machine/runtime probes stubbed and no benchmark execution.
