from __future__ import annotations

import pytest

from specgrain import (
    GRAIN_READINESS_VERSION,
    GrainReadinessError,
    MinimalityChoice,
    ReadinessIssueCode,
    SafetyStatus,
    SpecNode,
    evaluate_grain_readiness,
    require_grain_readiness,
)


def readiness_metadata(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "version": GRAIN_READINESS_VERSION,
        "unresolved_decisions": [],
        "minimality": {
            "choice": MinimalityChoice.NEW_CODE.value,
            "rationale": "No existing repository capability satisfies the bounded outcome.",
        },
        "safety": {
            "status": SafetyStatus.NONE_IDENTIFIED.value,
            "requirements": [],
        },
    }
    value.update(overrides)
    return value


def grain(**overrides: object) -> SpecNode:
    values: dict[str, object] = {
        "id": "SG-000001",
        "title": "Bounded change",
        "outcome": "The bounded behavior is implemented.",
        "scope_in": ["bounded behavior"],
        "acceptance": ["bounded behavior is verified"],
        "risk": {"level": "low", "recovery": "Revert the implementation commit."},
        "context": {"budget_tokens": 8000, "estimated_tokens": 4000},
        "change_surface": ["src/example.py", "tests/test_example.py"],
        "evidence": {"required": ["tests", "diff"]},
        "metadata": {"readiness": readiness_metadata()},
        "state": "REFINING",
    }
    values.update(overrides)
    return SpecNode(**values)


def codes(report: object) -> set[ReadinessIssueCode]:
    return {issue.code for issue in report.issues}  # type: ignore[attr-defined]


def test_fully_declared_leaf_is_ready_and_bound_to_revision() -> None:
    candidate = grain()
    report = evaluate_grain_readiness(candidate, [candidate])

    assert report.is_ready
    assert report.node_id == candidate.id
    assert report.revision_digest == candidate.revision_digest
    assert report.issues == ()
    assert require_grain_readiness(candidate, [candidate]) == report


def test_evaluation_never_mutates_candidate_state() -> None:
    candidate = grain()
    before = candidate.to_dict()
    report = evaluate_grain_readiness(candidate, [candidate])
    assert report.is_ready
    assert candidate.state == "REFINING"
    assert candidate.to_dict() == before


def test_invalid_refinement_forest_maps_structural_issues_and_stops() -> None:
    candidate = grain(children=["SG-000099"])
    report = evaluate_grain_readiness(candidate, [candidate])
    assert codes(report) == {ReadinessIssueCode.REFINEMENT_INVALID}
    assert "MISSING_CHILD" in report.issues[0].message


def test_candidate_must_exist_in_valid_forest() -> None:
    candidate = grain()
    other = grain(id="SG-000002")
    report = evaluate_grain_readiness(candidate, [other])
    assert codes(report) == {ReadinessIssueCode.CANDIDATE_MISSING}


def test_candidate_revision_must_match_forest_copy() -> None:
    candidate = grain(title="Current")
    stale = grain(title="Stale")
    report = evaluate_grain_readiness(candidate, [stale])
    assert codes(report) == {ReadinessIssueCode.CANDIDATE_REVISION_MISMATCH}


def test_source_state_must_be_refining() -> None:
    candidate = grain(state="SHAPED")
    report = evaluate_grain_readiness(candidate, [candidate])
    assert ReadinessIssueCode.SOURCE_STATE_INVALID in codes(report)


def test_non_leaf_is_blocked_in_valid_forest() -> None:
    parent = grain(children=["SG-000002"])
    child = grain(
        id="SG-000002",
        parent_id="SG-000001",
        title="Child",
        outcome="Child outcome",
    )
    report = evaluate_grain_readiness(parent, [parent, child])
    assert ReadinessIssueCode.NOT_LEAF in codes(report)


@pytest.mark.parametrize(
    ("override", "expected"),
    [
        ({"acceptance": []}, ReadinessIssueCode.ACCEPTANCE_REQUIRED),
        ({"scope_in": []}, ReadinessIssueCode.SCOPE_REQUIRED),
    ],
)
def test_acceptance_and_scope_are_required(
    override: dict[str, object], expected: ReadinessIssueCode
) -> None:
    candidate = grain(**override)
    assert expected in codes(evaluate_grain_readiness(candidate, [candidate]))


def test_change_surface_can_use_explicit_exception() -> None:
    candidate = grain(
        change_surface=[],
        metadata={
            "readiness": readiness_metadata(
                change_surface_exception="Exact path depends on generated migration name."
            )
        },
    )
    assert evaluate_grain_readiness(candidate, [candidate]).is_ready


def test_missing_or_blank_change_surface_exception_blocks() -> None:
    missing = grain(change_surface=[])
    blank = grain(
        change_surface=[],
        metadata={"readiness": readiness_metadata(change_surface_exception="   ")},
    )
    assert ReadinessIssueCode.CHANGE_SURFACE_REQUIRED in codes(
        evaluate_grain_readiness(missing, [missing])
    )
    assert ReadinessIssueCode.CHANGE_SURFACE_REQUIRED in codes(
        evaluate_grain_readiness(blank, [blank])
    )


def test_blank_optional_change_surface_exception_is_invalid_when_present() -> None:
    candidate = grain(
        metadata={"readiness": readiness_metadata(change_surface_exception="")}
    )
    assert ReadinessIssueCode.CHANGE_SURFACE_REQUIRED in codes(
        evaluate_grain_readiness(candidate, [candidate])
    )


@pytest.mark.parametrize("level", ["low", "medium", "high", "critical"])
def test_all_canonical_risk_levels_pass(level: str) -> None:
    candidate = grain(risk={"level": level, "recovery": "revert"})
    assert evaluate_grain_readiness(candidate, [candidate]).is_ready


@pytest.mark.parametrize("level", [None, "LOW", "unknown", 1])
def test_invalid_risk_level_blocks(level: object) -> None:
    candidate = grain(risk={"level": level, "recovery": "revert"})
    assert ReadinessIssueCode.RISK_LEVEL_INVALID in codes(
        evaluate_grain_readiness(candidate, [candidate])
    )


@pytest.mark.parametrize("recovery", ["", "   ", {}, None, []])
def test_recovery_must_be_non_empty_string_or_object(recovery: object) -> None:
    candidate = grain(risk={"level": "low", "recovery": recovery})
    assert ReadinessIssueCode.RECOVERY_REQUIRED in codes(
        evaluate_grain_readiness(candidate, [candidate])
    )


def test_non_empty_recovery_object_passes() -> None:
    candidate = grain(risk={"level": "medium", "recovery": {"action": "rollback"}})
    assert evaluate_grain_readiness(candidate, [candidate]).is_ready


@pytest.mark.parametrize("budget", [0, -1, True, False, "8000", None])
def test_context_budget_must_be_positive_integer(budget: object) -> None:
    candidate = grain(context={"budget_tokens": budget, "estimated_tokens": 1})
    assert ReadinessIssueCode.CONTEXT_BUDGET_INVALID in codes(
        evaluate_grain_readiness(candidate, [candidate])
    )


@pytest.mark.parametrize("estimate", [-1, True, False, "0", None])
def test_context_estimate_must_be_non_negative_integer(estimate: object) -> None:
    candidate = grain(context={"budget_tokens": 10, "estimated_tokens": estimate})
    assert ReadinessIssueCode.CONTEXT_ESTIMATE_INVALID in codes(
        evaluate_grain_readiness(candidate, [candidate])
    )


def test_context_estimate_may_be_zero() -> None:
    candidate = grain(context={"budget_tokens": 10, "estimated_tokens": 0})
    assert evaluate_grain_readiness(candidate, [candidate]).is_ready


def test_context_estimate_cannot_exceed_budget() -> None:
    candidate = grain(context={"budget_tokens": 10, "estimated_tokens": 11})
    assert ReadinessIssueCode.CONTEXT_BUDGET_EXCEEDED in codes(
        evaluate_grain_readiness(candidate, [candidate])
    )


@pytest.mark.parametrize(
    "required",
    [None, [], [""], ["tests", "tests"], "tests", [1]],
)
def test_required_evidence_must_be_unique_non_empty_identifiers(required: object) -> None:
    candidate = grain(evidence={"required": required})
    assert ReadinessIssueCode.EVIDENCE_REQUIRED_INVALID in codes(
        evaluate_grain_readiness(candidate, [candidate])
    )


def test_missing_readiness_object_blocks_fail_closed() -> None:
    candidate = grain(metadata={})
    report = evaluate_grain_readiness(candidate, [candidate])
    assert ReadinessIssueCode.READINESS_DECLARATION_INVALID in codes(report)


@pytest.mark.parametrize("version", [0, 2, True, "1", None])
def test_readiness_version_must_equal_v1_integer(version: object) -> None:
    candidate = grain(metadata={"readiness": readiness_metadata(version=version)})
    assert ReadinessIssueCode.READINESS_VERSION_INVALID in codes(
        evaluate_grain_readiness(candidate, [candidate])
    )


def test_unresolved_decisions_must_be_explicit_and_empty() -> None:
    missing = readiness_metadata()
    missing.pop("unresolved_decisions")
    malformed = readiness_metadata(unresolved_decisions=[1])
    present = readiness_metadata(unresolved_decisions=["Choose API shape"])

    missing_node = grain(metadata={"readiness": missing})
    malformed_node = grain(metadata={"readiness": malformed})
    present_node = grain(metadata={"readiness": present})

    assert ReadinessIssueCode.UNRESOLVED_DECISIONS_INVALID in codes(
        evaluate_grain_readiness(missing_node, [missing_node])
    )
    assert ReadinessIssueCode.UNRESOLVED_DECISIONS_INVALID in codes(
        evaluate_grain_readiness(malformed_node, [malformed_node])
    )
    assert ReadinessIssueCode.UNRESOLVED_DECISIONS_PRESENT in codes(
        evaluate_grain_readiness(present_node, [present_node])
    )


@pytest.mark.parametrize("choice", list(MinimalityChoice))
def test_each_minimality_choice_is_canonical(choice: MinimalityChoice) -> None:
    candidate = grain(
        metadata={
            "readiness": readiness_metadata(
                minimality={"choice": choice.value, "rationale": "bounded rationale"}
            )
        }
    )
    assert evaluate_grain_readiness(candidate, [candidate]).is_ready


def test_minimality_choice_and_rationale_are_independent_gates() -> None:
    candidate = grain(
        metadata={
            "readiness": readiness_metadata(
                minimality={"choice": "magic", "rationale": "   "}
            )
        }
    )
    found = codes(evaluate_grain_readiness(candidate, [candidate]))
    assert ReadinessIssueCode.MINIMALITY_CHOICE_INVALID in found
    assert ReadinessIssueCode.MINIMALITY_RATIONALE_REQUIRED in found


def test_missing_minimality_object_reports_both_required_parts() -> None:
    metadata = readiness_metadata()
    metadata.pop("minimality")
    candidate = grain(metadata={"readiness": metadata})
    found = codes(evaluate_grain_readiness(candidate, [candidate]))
    assert ReadinessIssueCode.MINIMALITY_CHOICE_INVALID in found
    assert ReadinessIssueCode.MINIMALITY_RATIONALE_REQUIRED in found


def test_safety_none_identified_requires_empty_requirements() -> None:
    passing = grain()
    failing = grain(
        metadata={
            "readiness": readiness_metadata(
                safety={"status": "none-identified", "requirements": ["guard"]}
            )
        }
    )
    assert evaluate_grain_readiness(passing, [passing]).is_ready
    assert ReadinessIssueCode.SAFETY_REQUIREMENTS_INVALID in codes(
        evaluate_grain_readiness(failing, [failing])
    )


def test_safety_requirements_defined_requires_at_least_one_requirement() -> None:
    passing = grain(
        metadata={
            "readiness": readiness_metadata(
                safety={"status": "requirements-defined", "requirements": ["validate input"]}
            )
        }
    )
    failing = grain(
        metadata={
            "readiness": readiness_metadata(
                safety={"status": "requirements-defined", "requirements": []}
            )
        }
    )
    assert evaluate_grain_readiness(passing, [passing]).is_ready
    assert ReadinessIssueCode.SAFETY_REQUIREMENTS_INVALID in codes(
        evaluate_grain_readiness(failing, [failing])
    )


def test_invalid_safety_status_and_requirements_are_structured() -> None:
    candidate = grain(
        metadata={
            "readiness": readiness_metadata(
                safety={"status": "unknown", "requirements": ["guard"]}
            )
        }
    )
    found = codes(evaluate_grain_readiness(candidate, [candidate]))
    assert ReadinessIssueCode.SAFETY_STATUS_INVALID in found
    assert ReadinessIssueCode.SAFETY_REQUIREMENTS_INVALID in found


def test_safety_requirements_reject_duplicates_and_blank_entries() -> None:
    for requirements in (["guard", "guard"], [" "]):
        candidate = grain(
            metadata={
                "readiness": readiness_metadata(
                    safety={"status": "requirements-defined", "requirements": requirements}
                )
            }
        )
        assert ReadinessIssueCode.SAFETY_REQUIREMENTS_INVALID in codes(
            evaluate_grain_readiness(candidate, [candidate])
        )


def test_issue_order_is_deterministic_by_code_field_message() -> None:
    candidate = grain(
        acceptance=[],
        scope_in=[],
        risk={},
        context={},
        evidence={},
        metadata={},
        state="SHAPED",
    )
    report = evaluate_grain_readiness(candidate, [candidate])
    keys = [(issue.code.value, issue.field, issue.message) for issue in report.issues]
    assert keys == sorted(keys)


def test_require_error_preserves_exact_report() -> None:
    candidate = grain(acceptance=[])
    report = evaluate_grain_readiness(candidate, [candidate])
    with pytest.raises(GrainReadinessError) as caught:
        require_grain_readiness(candidate, [candidate])
    assert caught.value.report == report


def test_readiness_metadata_is_content_significant() -> None:
    first = grain()
    second = grain(
        metadata={
            "readiness": readiness_metadata(
                minimality={
                    "choice": "reuse-existing",
                    "rationale": "Reuse the existing helper.",
                }
            )
        }
    )
    assert first.revision_digest != second.revision_digest
