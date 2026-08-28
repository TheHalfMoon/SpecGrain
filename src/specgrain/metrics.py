"""Deterministic change-scope, drift, and delivery metric primitives."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Any

from .model import is_spec_id

METRICS_VERSION = 1


class MetricsValidationError(ValueError):
    """Raised when metric or drift inputs violate the deterministic contract."""


class DriftSignalCode(StrEnum):
    """Stable exact-revision drift signal codes."""

    SPEC_REVISION = "SPEC_REVISION_DRIFT"
    REPOSITORY_REVISION = "REPOSITORY_REVISION_DRIFT"
    CONTEXT_PLAN = "CONTEXT_PLAN_DRIFT"


@dataclass(frozen=True, slots=True, order=True)
class DriftSignal:
    """One exact before/after revision mismatch."""

    code: DriftSignalCode
    baseline: str
    current: str

    def to_dict(self) -> dict[str, str]:
        return {
            "baseline": self.baseline,
            "code": self.code.value,
            "current": self.current,
        }


@dataclass(frozen=True, slots=True)
class DriftReport:
    """Deterministic drift report for exact spec/repository/context revisions."""

    signals: tuple[DriftSignal, ...]

    @property
    def has_drift(self) -> bool:
        return bool(self.signals)

    def to_dict(self) -> dict[str, object]:
        return {
            "has_drift": self.has_drift,
            "signals": [signal.to_dict() for signal in self.signals],
            "version": METRICS_VERSION,
        }

    @property
    def digest(self) -> str:
        return _digest(self.to_dict())


@dataclass(frozen=True, slots=True)
class ChangeScopeReport:
    """Observed changed paths partitioned by the authorized change surface."""

    authorized_surface: tuple[str, ...]
    changed_paths: tuple[str, ...]
    in_scope_paths: tuple[str, ...]
    unscoped_paths: tuple[str, ...]

    @property
    def is_scoped(self) -> bool:
        return not self.unscoped_paths

    def to_dict(self) -> dict[str, object]:
        return {
            "authorized_surface": list(self.authorized_surface),
            "changed_paths": list(self.changed_paths),
            "in_scope_paths": list(self.in_scope_paths),
            "is_scoped": self.is_scoped,
            "unscoped_paths": list(self.unscoped_paths),
            "version": METRICS_VERSION,
        }

    @property
    def digest(self) -> str:
        return _digest(self.to_dict())


@dataclass(frozen=True, slots=True)
class Ratio:
    """Exact integer ratio used instead of environment-dependent floating point."""

    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        _require_non_negative_int(self.numerator, "numerator")
        _require_positive_int(self.denominator, "denominator")
        if self.numerator > self.denominator:
            raise MetricsValidationError("ratio numerator must not exceed denominator")

    def to_dict(self) -> dict[str, int]:
        return {"denominator": self.denominator, "numerator": self.numerator}


@dataclass(frozen=True, slots=True)
class DeliveryObservation:
    """One measured Grain-delivery observation without actor identity."""

    spec_id: str
    verification_attempts: int
    first_pass_verified: bool
    rework_events: int
    cycle_seconds: int
    selected_context_tokens: int
    useful_context_tokens: int
    changed_path_count: int
    in_scope_path_count: int
    drift_detected: bool = False

    def __post_init__(self) -> None:
        if not is_spec_id(self.spec_id):
            raise MetricsValidationError("spec_id must be a canonical SpecGrain ID")
        _require_positive_int(self.verification_attempts, "verification_attempts")
        _require_non_negative_int(self.rework_events, "rework_events")
        _require_non_negative_int(self.cycle_seconds, "cycle_seconds")
        _require_non_negative_int(self.selected_context_tokens, "selected_context_tokens")
        _require_non_negative_int(self.useful_context_tokens, "useful_context_tokens")
        _require_non_negative_int(self.changed_path_count, "changed_path_count")
        _require_non_negative_int(self.in_scope_path_count, "in_scope_path_count")
        if not isinstance(self.first_pass_verified, bool):
            raise MetricsValidationError("first_pass_verified must be boolean")
        if not isinstance(self.drift_detected, bool):
            raise MetricsValidationError("drift_detected must be boolean")
        if self.useful_context_tokens > self.selected_context_tokens:
            raise MetricsValidationError(
                "useful_context_tokens must not exceed selected_context_tokens"
            )
        if self.in_scope_path_count > self.changed_path_count:
            raise MetricsValidationError(
                "in_scope_path_count must not exceed changed_path_count"
            )


@dataclass(frozen=True, slots=True)
class DeliveryMetrics:
    """Aggregate deterministic delivery metrics for a set of Grain observations."""

    grain_count: int
    first_pass_verification_rate: Ratio
    rework_ratio: Ratio
    mean_cycle_seconds_numerator: int
    mean_cycle_seconds_denominator: int
    context_efficiency: Ratio | None
    change_scope_accuracy: Ratio | None
    spec_drift_rate: Ratio
    unscoped_path_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "change_scope_accuracy": (
                None if self.change_scope_accuracy is None else self.change_scope_accuracy.to_dict()
            ),
            "context_efficiency": (
                None if self.context_efficiency is None else self.context_efficiency.to_dict()
            ),
            "first_pass_verification_rate": self.first_pass_verification_rate.to_dict(),
            "grain_count": self.grain_count,
            "mean_cycle_seconds": {
                "denominator": self.mean_cycle_seconds_denominator,
                "numerator": self.mean_cycle_seconds_numerator,
            },
            "rework_ratio": self.rework_ratio.to_dict(),
            "spec_drift_rate": self.spec_drift_rate.to_dict(),
            "unscoped_path_count": self.unscoped_path_count,
            "version": METRICS_VERSION,
        }

    @property
    def digest(self) -> str:
        return _digest(self.to_dict())


def _require_non_empty_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MetricsValidationError(f"{field_name} must be non-empty text")
    return value


def _require_non_negative_int(value: object, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise MetricsValidationError(f"{field_name} must be a non-negative integer")
    return value


def _require_positive_int(value: object, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise MetricsValidationError(f"{field_name} must be a positive integer")
    return value


def _normalize_path(value: object, field_name: str) -> str:
    text = _require_non_empty_text(value, field_name)
    if "\\" in text:
        raise MetricsValidationError(f"{field_name} must use repository-relative POSIX paths")
    path = PurePosixPath(text)
    if path.is_absolute() or ".." in path.parts or text.startswith("./"):
        raise MetricsValidationError(f"{field_name} must be a normalized repository-relative path")
    normalized = path.as_posix()
    if normalized in {"", "."}:
        raise MetricsValidationError(f"{field_name} must not be the repository root")
    return normalized.rstrip("/")


def _normalize_paths(values: object, field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes, bytearray)) or not isinstance(values, (list, tuple)):
        raise MetricsValidationError(f"{field_name} must be a sequence of paths")
    normalized = tuple(_normalize_path(value, field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise MetricsValidationError(f"{field_name} must not contain duplicate paths")
    return tuple(sorted(normalized))


def _path_authorized(path: str, surfaces: tuple[str, ...]) -> bool:
    return any(path == surface or path.startswith(f"{surface}/") for surface in surfaces)


def _digest(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def analyze_change_scope(
    authorized_surface: object,
    changed_paths: object,
) -> ChangeScopeReport:
    """Partition observed paths using literal repository-relative path/prefix authorization."""

    surfaces = _normalize_paths(authorized_surface, "authorized_surface")
    changed = _normalize_paths(changed_paths, "changed_paths")
    if not surfaces:
        raise MetricsValidationError("authorized_surface must not be empty")
    in_scope = tuple(path for path in changed if _path_authorized(path, surfaces))
    unscoped = tuple(path for path in changed if path not in in_scope)
    return ChangeScopeReport(surfaces, changed, in_scope, unscoped)


def detect_drift(
    *,
    baseline_spec_revision: str,
    current_spec_revision: str,
    baseline_repository_revision: str,
    current_repository_revision: str,
    baseline_context_digest: str | None = None,
    current_context_digest: str | None = None,
) -> DriftReport:
    """Return exact revision drift signals without guessing cause or severity."""

    pairs = (
        (
            DriftSignalCode.SPEC_REVISION,
            _require_non_empty_text(baseline_spec_revision, "baseline_spec_revision"),
            _require_non_empty_text(current_spec_revision, "current_spec_revision"),
        ),
        (
            DriftSignalCode.REPOSITORY_REVISION,
            _require_non_empty_text(
                baseline_repository_revision, "baseline_repository_revision"
            ),
            _require_non_empty_text(
                current_repository_revision, "current_repository_revision"
            ),
        ),
    )
    signals = [
        DriftSignal(code, baseline, current)
        for code, baseline, current in pairs
        if baseline != current
    ]
    if (baseline_context_digest is None) != (current_context_digest is None):
        raise MetricsValidationError("context digests must be supplied together")
    if baseline_context_digest is not None and current_context_digest is not None:
        baseline = _require_non_empty_text(baseline_context_digest, "baseline_context_digest")
        current = _require_non_empty_text(current_context_digest, "current_context_digest")
        if baseline != current:
            signals.append(DriftSignal(DriftSignalCode.CONTEXT_PLAN, baseline, current))
    return DriftReport(tuple(sorted(signals)))


def aggregate_delivery_metrics(observations: object) -> DeliveryMetrics:
    """Aggregate reproducible process metrics without actor-level scoring."""

    if isinstance(observations, (str, bytes, bytearray)) or not isinstance(
        observations, (list, tuple)
    ):
        raise MetricsValidationError("observations must be a sequence")
    items = tuple(observations)
    if not items:
        raise MetricsValidationError("observations must not be empty")
    if not all(isinstance(item, DeliveryObservation) for item in items):
        raise MetricsValidationError("observations must contain DeliveryObservation values")

    count = len(items)
    first_pass = sum(1 for item in items if item.first_pass_verified)
    rework = sum(item.rework_events for item in items)
    implementation_attempts = count + rework
    cycle = sum(item.cycle_seconds for item in items)
    selected = sum(item.selected_context_tokens for item in items)
    useful = sum(item.useful_context_tokens for item in items)
    changed = sum(item.changed_path_count for item in items)
    in_scope = sum(item.in_scope_path_count for item in items)
    drifted = sum(1 for item in items if item.drift_detected)

    return DeliveryMetrics(
        grain_count=count,
        first_pass_verification_rate=Ratio(first_pass, count),
        rework_ratio=Ratio(rework, implementation_attempts),
        mean_cycle_seconds_numerator=cycle,
        mean_cycle_seconds_denominator=count,
        context_efficiency=None if selected == 0 else Ratio(useful, selected),
        change_scope_accuracy=None if changed == 0 else Ratio(in_scope, changed),
        spec_drift_rate=Ratio(drifted, count),
        unscoped_path_count=changed - in_scope,
    )
