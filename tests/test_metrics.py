from __future__ import annotations

import itertools

import pytest

from specgrain.metrics import (
    METRICS_VERSION,
    DeliveryObservation,
    DriftSignalCode,
    MetricsValidationError,
    Ratio,
    aggregate_delivery_metrics,
    analyze_change_scope,
    detect_drift,
)


def observation(**overrides: object) -> DeliveryObservation:
    values: dict[str, object] = {
        "spec_id": "SG-000012",
        "verification_attempts": 1,
        "first_pass_verified": True,
        "rework_events": 0,
        "cycle_seconds": 30,
        "selected_context_tokens": 100,
        "useful_context_tokens": 80,
        "changed_path_count": 4,
        "in_scope_path_count": 3,
        "drift_detected": False,
    }
    values.update(overrides)
    return DeliveryObservation(**values)


def test_metrics_version_is_stable() -> None:
    assert METRICS_VERSION == 1


def test_change_scope_literal_prefix_semantics_and_digest_are_deterministic() -> None:
    report = analyze_change_scope(
        ["src/specgrain", "README.md"],
        ["README.md", "src/specgrain/x.py", "tests/test_x.py"],
    )
    assert report.in_scope_paths == ("README.md", "src/specgrain/x.py")
    assert report.unscoped_paths == ("tests/test_x.py",)
    assert report.is_scoped is False
    reversed_report = analyze_change_scope(
        ["README.md", "src/specgrain"],
        ["tests/test_x.py", "src/specgrain/x.py", "README.md"],
    )
    assert report.to_dict() == reversed_report.to_dict()
    assert report.digest == reversed_report.digest


@pytest.mark.parametrize("path", ["../x", "/x", "./x", "a\\b", ""])
def test_change_scope_rejects_non_canonical_paths(path: str) -> None:
    with pytest.raises(MetricsValidationError):
        analyze_change_scope(["src"], [path])


def test_change_scope_rejects_empty_surface_and_duplicates() -> None:
    with pytest.raises(MetricsValidationError):
        analyze_change_scope([], ["a"])
    with pytest.raises(MetricsValidationError):
        analyze_change_scope(["src", "src"], ["src/a.py"])


def test_drift_is_exact_and_does_not_guess_cause() -> None:
    report = detect_drift(
        baseline_spec_revision="spec-a",
        current_spec_revision="spec-b",
        baseline_repository_revision="repo-a",
        current_repository_revision="repo-a",
        baseline_context_digest="ctx-a",
        current_context_digest="ctx-b",
    )
    assert [signal.code for signal in report.signals] == [
        DriftSignalCode.CONTEXT_PLAN,
        DriftSignalCode.SPEC_REVISION,
    ]
    assert report.has_drift is True
    assert report.digest.startswith("sha256:")


def test_no_drift_is_empty_and_context_pair_must_be_complete() -> None:
    report = detect_drift(
        baseline_spec_revision="same",
        current_spec_revision="same",
        baseline_repository_revision="repo",
        current_repository_revision="repo",
    )
    assert report.has_drift is False
    assert report.signals == ()
    with pytest.raises(MetricsValidationError, match="supplied together"):
        detect_drift(
            baseline_spec_revision="same",
            current_spec_revision="same",
            baseline_repository_revision="repo",
            current_repository_revision="repo",
            baseline_context_digest="ctx",
        )


def test_ratio_is_exact_and_bounded() -> None:
    assert Ratio(1, 3).to_dict() == {"denominator": 3, "numerator": 1}
    with pytest.raises(MetricsValidationError):
        Ratio(2, 1)
    with pytest.raises(MetricsValidationError):
        Ratio(0, 0)


def test_observation_validation_rejects_impossible_counts() -> None:
    with pytest.raises(MetricsValidationError, match="useful_context_tokens"):
        observation(selected_context_tokens=2, useful_context_tokens=3)
    with pytest.raises(MetricsValidationError, match="in_scope_path_count"):
        observation(changed_path_count=1, in_scope_path_count=2)
    with pytest.raises(MetricsValidationError, match="canonical SpecGrain ID"):
        observation(spec_id="ticket-12")


def test_aggregate_metrics_use_integer_ratios_and_no_actor_identity() -> None:
    items = [
        observation(),
        observation(
            spec_id="SG-000013",
            first_pass_verified=False,
            rework_events=2,
            cycle_seconds=90,
            selected_context_tokens=50,
            useful_context_tokens=25,
            changed_path_count=2,
            in_scope_path_count=1,
            drift_detected=True,
        ),
    ]
    report = aggregate_delivery_metrics(items)
    assert report.grain_count == 2
    assert report.first_pass_verification_rate == Ratio(1, 2)
    assert report.rework_ratio == Ratio(2, 4)
    assert (report.mean_cycle_seconds_numerator, report.mean_cycle_seconds_denominator) == (120, 2)
    assert report.context_efficiency == Ratio(105, 150)
    assert report.change_scope_accuracy == Ratio(4, 6)
    assert report.spec_drift_rate == Ratio(1, 2)
    assert report.unscoped_path_count == 2
    payload = report.to_dict()
    assert "user" not in str(payload).lower()
    assert "developer" not in str(payload).lower()
    assert "productivity" not in str(payload).lower()


def test_aggregate_is_permutation_invariant() -> None:
    items = [
        observation(spec_id="SG-000012"),
        observation(spec_id="SG-000013", rework_events=1, first_pass_verified=False),
        observation(spec_id="SG-000014", drift_detected=True),
    ]
    expected = aggregate_delivery_metrics(items).to_dict()
    for permuted in itertools.permutations(items):
        assert aggregate_delivery_metrics(list(permuted)).to_dict() == expected


def test_context_and_scope_ratios_are_none_when_denominator_is_zero() -> None:
    report = aggregate_delivery_metrics(
        [
            observation(
                selected_context_tokens=0,
                useful_context_tokens=0,
                changed_path_count=0,
                in_scope_path_count=0,
            )
        ]
    )
    assert report.context_efficiency is None
    assert report.change_scope_accuracy is None


def test_aggregate_rejects_empty_or_wrong_values() -> None:
    with pytest.raises(MetricsValidationError):
        aggregate_delivery_metrics([])
    with pytest.raises(MetricsValidationError):
        aggregate_delivery_metrics([object()])
