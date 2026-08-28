from __future__ import annotations

import pytest

from specgrain.method import (
    METHOD_PROFILE_VERSION,
    MethodIssueCode,
    MethodProfileName,
    MethodReadinessError,
    evaluate_method_profile,
    evaluate_method_readiness,
    get_method_profile,
    require_method_readiness,
)
from specgrain.model import SpecNode


def node(**overrides: object) -> SpecNode:
    values: dict[str, object] = {
        "id": "SG-000011",
        "title": "Method profile",
        "outcome": "Route proportionate deterministic requirements.",
        "scope_in": ["method routing"],
        "acceptance": ["profile passes"],
        "risk": {"level": "low", "recovery": "revert"},
        "context": {"budget_tokens": 100, "estimated_tokens": 20},
        "change_surface": ["src/specgrain/method.py"],
        "evidence": {"required": ["tests"]},
        "method": "quick",
        "state": "REFINING",
        "metadata": {
            "readiness": {
                "version": 1,
                "unresolved_decisions": [],
                "minimality": {"choice": "new-code", "rationale": "bounded module"},
                "safety": {"status": "none-identified", "requirements": []},
            }
        },
    }
    values.update(overrides)
    return SpecNode(**values)


def method_metadata(**values: object) -> dict[str, object]:
    return {
        "readiness": {
            "version": 1,
            "unresolved_decisions": [],
            "minimality": {"choice": "new-code", "rationale": "bounded module"},
            "safety": {"status": "none-identified", "requirements": []},
        },
        "method": values,
    }


def test_profile_version_and_names_are_stable() -> None:
    assert METHOD_PROFILE_VERSION == 1
    assert [item.value for item in MethodProfileName] == [
        "quick", "dmaic-lite", "dmadv-lite", "experiment", "controlled"
    ]


def test_quick_adds_no_ceremony() -> None:
    report = evaluate_method_profile(node())
    assert report.is_ready is True
    assert report.profile is MethodProfileName.QUICK
    assert report.issues == ()


def test_unknown_profile_fails_deterministically() -> None:
    report = evaluate_method_profile(node(method="waterfall"))
    assert [issue.code for issue in report.issues] == [MethodIssueCode.PROFILE_INVALID]
    with pytest.raises(ValueError, match="unknown method profile"):
        get_method_profile("waterfall")


@pytest.mark.parametrize(
    ("profile", "metadata", "evidence"),
    [
        (
            "dmaic-lite",
            {"baseline": "repro", "cause": "root cause", "control": "regression guard"},
            ["tests", "baseline", "regression"],
        ),
        (
            "dmadv-lite",
            {
                "value": "user value",
                "baseline": "today",
                "analysis": "constraints",
                "design": "choice",
            },
            ["tests", "baseline", "verification"],
        ),
        (
            "experiment",
            {
                "hypothesis": "A beats B",
                "resource_boundary": "one hour",
                "decision_rule": "accept if metric improves",
                "non_production": True,
            },
            ["tests", "experiment-result"],
        ),
        (
            "controlled",
            {
                "rollback": "restore snapshot",
                "review_separation": "independent reviewer",
                "control": "post-check",
            },
            ["tests", "rollback", "independent-review"],
        ),
    ],
)
def test_non_quick_profiles_pass_with_only_bounded_required_fields(
    profile: str, metadata: dict[str, object], evidence: list[str]
) -> None:
    report = evaluate_method_profile(
        node(method=profile, metadata=method_metadata(**metadata), evidence={"required": evidence})
    )
    assert report.is_ready is True


def test_profile_missing_metadata_and_evidence_are_explicit() -> None:
    report = evaluate_method_profile(node(method="controlled"))
    codes = {issue.code for issue in report.issues}
    assert MethodIssueCode.METADATA_INVALID in codes
    assert MethodIssueCode.METADATA_MISSING in codes
    assert MethodIssueCode.EVIDENCE_MISSING in codes


def test_method_readiness_composes_core_and_profile_gates() -> None:
    candidate = node(method="experiment")
    report = evaluate_method_readiness(candidate, [candidate])
    assert report.core.is_ready is True
    assert report.method.is_ready is False
    assert report.is_ready is False
    with pytest.raises(MethodReadinessError):
        require_method_readiness(candidate, [candidate])


def test_profile_required_evidence_flows_through_existing_node_contract() -> None:
    candidate = node(
        method="dmaic-lite",
        metadata=method_metadata(baseline="repro", cause="cause", control="guard"),
        evidence={"required": ["tests", "baseline"]},
    )
    report = evaluate_method_profile(candidate)
    assert [(issue.code, issue.message) for issue in report.issues] == [
        (MethodIssueCode.EVIDENCE_MISSING, "dmaic-lite requires evidence identifier 'regression'")
    ]
