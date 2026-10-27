"""Matrix runner: expand harness x model x task, gate cloud harnesses on credentials.

The primary HarnessBench axis is *fix the base model, vary the harness*. The
matrix module produces a flat list of run triples from user-provided axes,
with each cloud-bound harness entry marked ``skipped`` when its required
credentials are missing from the environment.
"""

from __future__ import annotations

import os
import warnings
from importlib.metadata import entry_points
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
    """Discover installed specs, retaining bundled specs in source checkouts.

    Loading entry points imports trusted installed Python packages. Conflicting
    external names are excluded instead of allowing installation order to choose
    a harness. Bundled names cannot be overridden by external packages.
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
    bundled = {reg.spec.name: reg for reg in out}
    external: dict[str, list[HarnessRegistration]] = {}
    for entry in sorted(entry_points(group="clawbench.harnesses"),
                        key=lambda ep: (ep.name, ep.value)):
        try:
            spec = entry.load()
            credentials = _validate_plugin_spec(spec)
        except Exception as exc:
            # Exception messages can contain credentials or private paths.
            warnings.warn(
                f"Ignoring harness entry point {entry.name!r}: {type(exc).__name__}",
                RuntimeWarning, stacklevel=2,
            )
            continue
        if spec.name in bundled:
            if spec is not bundled[spec.name].spec:
                warnings.warn(
                    f"Ignoring harness entry point {entry.name!r}: bundled name {spec.name!r}",
                    RuntimeWarning, stacklevel=2,
                )
            continue
        external.setdefault(spec.name, []).append(HarnessRegistration(spec, credentials))
    for name, registrations in sorted(external.items()):
        if len(registrations) > 1:
            warnings.warn(
                f"Ignoring conflicting harness registrations for {name!r}",
                RuntimeWarning, stacklevel=2,
            )
        else:
            out.extend(registrations)
    return out


def _validate_plugin_spec(spec: Any) -> tuple[str, ...]:
    """Validate the local spec contract before a plugin affects preflight."""
    from harnessbench.harnesses._schema import HarnessSpec

    if not isinstance(spec, HarnessSpec):
        raise TypeError("entry point must export a HarnessSpec")
    for name in ("name", "description", "dockerfile", "setup_script", "run_script"):
        value = getattr(spec, name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError("required fields must be nonempty strings")
    if spec.runtime not in ("python", "node", "rust", "web"):
        raise ValueError("unsupported runtime")
    if spec.container_isolation not in ("shared", "dedicated"):
        raise ValueError("unsupported container isolation")
    credentials = spec.requires_credentials
    if credentials is None:
        return ()
    if not isinstance(credentials, (list, tuple)) or any(
        not isinstance(value, str) or not value.strip() for value in credentials
    ):
        raise TypeError("credentials must be a list or tuple of nonempty strings")
    return tuple(credentials)


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
