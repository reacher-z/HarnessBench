# Adding a Harness

A harness adapter is three files plus one `pyproject.toml` entry. That's it.

## The 3-file pattern

```
src/harnessbench/harnesses/<slug>/
    __init__.py      # re-exports `spec`
    spec.py          # HarnessSpec dataclass
    Dockerfile       # FROM ghcr.io/reacher-z/clawbench-base:latest + your runtime
    setup.sh         # one-shot install of your harness + its deps
    run.sh           # invoke the harness against the task; attach to Chrome on CDP 9222
```

## 1. `spec.py`

```python
from harnessbench.harnesses._schema import HarnessSpec

spec = HarnessSpec(
    name="my-harness",
    description="One-line description.",
    runtime="python",            # "python" | "node" | "rust" | "web"
    dockerfile="Dockerfile",
    setup_script="setup.sh",
    run_script="run.sh",
    container_isolation="dedicated",   # or "shared" if you reuse clawbench-base verbatim
    requires_credentials=None,          # or ("MY_API_KEY",) for cloud-opt-in
    upstream_url="https://github.com/...",
    upstream_license="Apache-2.0",
)
```

## 2. `Dockerfile`

```dockerfile
FROM ghcr.io/reacher-z/clawbench-base:latest

COPY setup.sh /opt/harness/setup.sh
COPY run.sh   /opt/harness/run.sh
RUN chmod +x /opt/harness/setup.sh /opt/harness/run.sh && /opt/harness/setup.sh

ENTRYPOINT ["/opt/harness/run.sh"]
```

The base image ships Chrome, Xvfb, FFmpeg, the extension-server, and the CDP-intercept wiring. You only need to add your harness runtime on top.

## 3. `setup.sh` and `run.sh`

`setup.sh` runs at image build time. Install whatever your harness needs.

`run.sh` runs at eval time. Read `$TASK_FILE` (default `/opt/clawbench/shared/task.json`), attach to Chrome at `http://localhost:9222`, drive the task to completion, exit 0. The scoring pipeline reads the resulting `RecordingBundle` from `/opt/clawbench/recording`.

## 4. Register the entry point

In HarnessBench's `pyproject.toml`:

```toml
[project.entry-points."clawbench.harnesses"]
hb-my-harness = "harnessbench.harnesses.my_harness:spec"
```

Or, for an out-of-tree package, put the stanza in your own `pyproject.toml` and `pip install .` it alongside `harnessbench`.

## 5. Verify

```bash
harnessbench harnesses | grep my-harness
harnessbench matrix --harnesses my-harness --models gpt-4o-mini
harnessbench run --harness my-harness --model gpt-4o-mini --case fixtures/smoke.json
```

## Cloud-opt-in harnesses

If your harness requires credentials, set `requires_credentials=("VAR_A", "VAR_B")` in the spec. HarnessBench gates matrix expansion on env; missing vars produce `status="skipped:missing_credential:<VAR>"` entries — never silent zeros.

## License compatibility

Only Apache-2.0 / MIT / BSD upstreams. AGPL, SSPL, "Sustainable Use", and custom non-OSI licenses are rejected. Document the upstream license on the spec and link to it in the PR.
