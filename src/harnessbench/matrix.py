"""Matrix runner: expand harness x model x task, gate cloud harnesses on credentials.

The primary HarnessBench axis is *fix the base model, vary the harness*. The
matrix module produces a flat list of run triples from user-provided axes,
with each cloud-bound harness entry marked ``skipped`` when its required
credentials are missing from the environment.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence


@dataclass
class RunSpec:
    """One cell in the harness x model x task matrix."""

    harness: str
    model: str
    case: Mapping[str, Any]
    status: str = "eligible"
    skip_reason: str | None = None

    @property
    def is_eligible(self) -> bool:
        return self.status == "eligible"

    @property
    def case_id(self) -> str:
        return str(self.case.get("id", ""))


@dataclass
class HarnessRegistration:
    """A harness discovered via ClawBench's entry-point group.

    ``missing_credentials`` is checked against ``os.environ`` at matrix
    expansion time. Any missing variable marks the harness' row as
    ``skipped:missing_credential:<VAR>`` rather than failing the run.
    """

    spec: Any
    requires_credentials: Sequence[str] = field(default_factory=tuple)

    def missing_credentials(self, env: Mapping[str, str] | None = None) -> list[str]:
        env = env if env is not None else os.environ
        return [var for var in self.requires_credentials if not env.get(var)]


def discover_registrations() -> list[HarnessRegistration]:
    """Return all HarnessBench-bundled harness registrations.

    Once ClawBench ships the plugin surface, this delegates to
    ``clawbench.harnesses.discover_harnesses``. Until then it imports the
    six bundled modules directly so the CLI and tests are exercisable.
    """
    from harnessbench.harnesses import (
        browser_use,
        claw_code,
        coze_studio,
        hermes,
        openclaw,
        stagehand,
    )

    out: list[HarnessRegistration] = []
    for mod in (openclaw, hermes, claw_code, stagehand, browser_use, coze_studio):
        spec = getattr(mod, "spec", None)
        if spec is None:
            continue
        out.append(
            HarnessRegistration(
                spec=spec,
                requires_credentials=tuple(spec.requires_credentials or ()),
            )
        )
    return out


def _by_name() -> dict[str, HarnessRegistration]:
    return {r.spec.name: r for r in discover_registrations()}


def expand(
    harnesses: Iterable[str],
    models: Iterable[str],
    cases: Iterable[Mapping[str, Any]],
    *,
    env: Mapping[str, str] | None = None,
) -> list[RunSpec]:
    """Cartesian-expand harness x model x case, gating cloud harnesses on env.

    Duplicate harness names are collapsed. Unknown harnesses raise ``KeyError``.
    """
    registrations = _by_name()
    harnesses = list(dict.fromkeys(harnesses))
    models = list(dict.fromkeys(models))
    cases = list(cases)

    for h in harnesses:
        if h not in registrations:
            raise KeyError(f"unknown harness: {h!r}")

    triples: list[RunSpec] = []
    for h in harnesses:
        reg = registrations[h]
        missing = reg.missing_credentials(env)
        for m in models:
            for c in cases:
                if missing:
                    reason = f"missing_credential:{','.join(missing)}"
                    triples.append(
                        RunSpec(harness=h, model=m, case=c, status="skipped", skip_reason=reason)
                    )
                else:
                    triples.append(RunSpec(harness=h, model=m, case=c))

    return triples


def summarize(specs: Sequence[RunSpec]) -> dict[str, int]:
    """Roll up matrix counts by status for the CLI's pre-flight output."""
    counts: dict[str, int] = {"eligible": 0, "skipped": 0, "total": len(specs)}
    for s in specs:
        counts[s.status] = counts.get(s.status, 0) + 1
    return counts
