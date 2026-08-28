from __future__ import annotations

import itertools
import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from specgrain import (
    ContextBudgetError,
    ContextBudgetIssueCode,
    ContextBudgetPolicy,
    ContextRequirement,
    ContextSource,
    ContextValidationError,
    RepositoryMap,
    evaluate_context_budget,
    repository_map_context_source,
    require_context_budget,
    scan_repository,
    validate_context_sources,
)


def source(
    source_id: str,
    *,
    requirement: str = "required",
    size_bytes: int = 10,
    token_cost: int = 5,
    priority: int = 0,
    revision: str | None = None,
) -> ContextSource:
    return ContextSource(
        source_id=source_id,
        provenance=f"fixture:{source_id}",
        selection_reason=f"needed for {source_id}",
        revision=revision or f"sha256:{source_id}",
        size_bytes=size_bytes,
        token_cost=token_cost,
        requirement=requirement,
        priority=priority,
    )


def codes(report: object) -> set[ContextBudgetIssueCode]:
    return {issue.code for issue in report.issues}  # type: ignore[attr-defined]


@pytest.mark.parametrize("field", ["source_id", "provenance", "selection_reason", "revision"])
def test_context_source_requires_non_empty_text(field: str) -> None:
    values: dict[str, object] = {
        "source_id": "x",
        "provenance": "fixture:x",
        "selection_reason": "needed",
        "revision": "rev",
        "size_bytes": 0,
        "token_cost": 0,
    }
    values[field] = "   "
    with pytest.raises(ContextValidationError, match=field):
        ContextSource(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize("field", ["size_bytes", "token_cost", "priority"])
@pytest.mark.parametrize("value", [-1, True, 1.5, "1"])
def test_context_source_cost_fields_are_non_negative_integers(
    field: str, value: object
) -> None:
    values: dict[str, object] = {
        "source_id": "x",
        "provenance": "fixture:x",
        "selection_reason": "needed",
        "revision": "rev",
        "size_bytes": 0,
        "token_cost": 0,
        "priority": 0,
    }
    values[field] = value
    with pytest.raises(ContextValidationError, match=field):
        ContextSource(**values)  # type: ignore[arg-type]


def test_public_records_are_frozen_and_slotted() -> None:
    item = source("x")
    policy = ContextBudgetPolicy(max_tokens=10)
    report = evaluate_context_budget([item], policy)
    assert "__dict__" not in dir(item)
    assert "__dict__" not in dir(policy)
    assert "__dict__" not in dir(report)
    with pytest.raises(FrozenInstanceError):
        item.source_id = "changed"  # type: ignore[misc]


def test_context_source_accepts_canonical_requirement_and_zero_cost() -> None:
    item = source("x", size_bytes=0, token_cost=0, requirement="optional")
    assert item.requirement is ContextRequirement.OPTIONAL
    assert item.to_dict()["requirement"] == "optional"


def test_context_source_rejects_unknown_requirement() -> None:
    with pytest.raises(ContextValidationError, match="requirement"):
        source("x", requirement="maybe")


@pytest.mark.parametrize("value", [0, -1, True, "10"])
def test_policy_requires_positive_max_tokens(value: object) -> None:
    with pytest.raises(ContextValidationError, match="max_tokens"):
        ContextBudgetPolicy(max_tokens=value)  # type: ignore[arg-type]


@pytest.mark.parametrize("field", ["max_bytes", "max_sources"])
@pytest.mark.parametrize("value", [0, -1, True, "10"])
def test_optional_policy_ceilings_are_positive_when_present(
    field: str, value: object
) -> None:
    kwargs: dict[str, object] = {field: value}
    with pytest.raises(ContextValidationError, match=field):
        ContextBudgetPolicy(max_tokens=10, **kwargs)  # type: ignore[arg-type]


def test_policy_allows_unbounded_optional_dimensions() -> None:
    policy = ContextBudgetPolicy(max_tokens=10)
    assert policy.to_dict() == {"max_bytes": None, "max_sources": None, "max_tokens": 10}


def test_collection_validation_is_sorted_and_rejects_duplicates() -> None:
    a, b = source("a"), source("b")
    assert validate_context_sources([b, a]) == (a, b)
    with pytest.raises(ContextValidationError, match="duplicate source_id values: a"):
        validate_context_sources([a, a])


def test_collection_validation_rejects_non_source_member() -> None:
    with pytest.raises(ContextValidationError, match=r"sources\[1\]"):
        validate_context_sources([source("a"), object()])  # type: ignore[list-item]


def test_evaluator_requires_policy_instance() -> None:
    with pytest.raises(ContextValidationError, match="policy"):
        evaluate_context_budget([], object())  # type: ignore[arg-type]


def test_empty_context_fits() -> None:
    report = evaluate_context_budget([], ContextBudgetPolicy(max_tokens=1))
    assert report.fits
    assert report.selected_ids == report.required_ids == report.omitted_optional_ids == ()
    assert report.selected_tokens == report.selected_bytes == 0
    assert report.plan_digest.startswith("sha256:")


def test_required_sources_fit_and_are_canonical() -> None:
    a = source("a", size_bytes=3, token_cost=2)
    b = source("b", size_bytes=4, token_cost=3)
    report = evaluate_context_budget(
        [b, a], ContextBudgetPolicy(max_tokens=5, max_bytes=7, max_sources=2)
    )
    assert report.fits
    assert report.required_ids == ("a", "b")
    assert report.selected_ids == ("a", "b")
    assert report.required_tokens == report.selected_tokens == 5
    assert report.required_bytes == report.selected_bytes == 7
    assert report.required_source_count == report.selected_source_count == 2


def test_required_token_overflow_is_blocking() -> None:
    report = evaluate_context_budget(
        [source("a", token_cost=11)], ContextBudgetPolicy(max_tokens=10)
    )
    assert not report.fits
    assert codes(report) == {ContextBudgetIssueCode.REQUIRED_TOKENS_EXCEEDED}
    assert report.selected_ids == ("a",)


def test_required_byte_and_source_count_overflow_are_blocking() -> None:
    report = evaluate_context_budget(
        [source("a", size_bytes=6), source("b", size_bytes=6)],
        ContextBudgetPolicy(max_tokens=100, max_bytes=10, max_sources=1),
    )
    assert not report.fits
    assert codes(report) == {
        ContextBudgetIssueCode.REQUIRED_BYTES_EXCEEDED,
        ContextBudgetIssueCode.REQUIRED_SOURCE_COUNT_EXCEEDED,
    }


def test_required_overflow_omits_all_optional_sources() -> None:
    report = evaluate_context_budget(
        [
            source("required", token_cost=11),
            source("optional", requirement="optional", token_cost=0),
        ],
        ContextBudgetPolicy(max_tokens=10),
    )
    assert not report.fits
    assert report.selected_ids == ("required",)
    assert report.omitted_optional_ids == ("optional",)


def test_optional_sources_pack_by_priority_then_id() -> None:
    items = [
        source("required", token_cost=1),
        source("z", requirement="optional", token_cost=4, priority=1),
        source("a", requirement="optional", token_cost=4, priority=1),
        source("first", requirement="optional", token_cost=4, priority=0),
    ]
    report = evaluate_context_budget(items, ContextBudgetPolicy(max_tokens=9))
    assert report.fits
    assert report.selected_ids == ("a", "first", "required")
    assert report.omitted_optional_ids == ("z",)


def test_later_smaller_optional_can_fit_after_large_omission() -> None:
    report = evaluate_context_budget(
        [
            source("required", token_cost=5),
            source("large", requirement="optional", token_cost=6, priority=0),
            source("small", requirement="optional", token_cost=5, priority=1),
        ],
        ContextBudgetPolicy(max_tokens=10),
    )
    assert report.selected_ids == ("required", "small")
    assert report.omitted_optional_ids == ("large",)


def test_optional_packing_obeys_all_configured_dimensions() -> None:
    report = evaluate_context_budget(
        [
            source("required", size_bytes=2, token_cost=2),
            source("bytes", requirement="optional", size_bytes=9, token_cost=1),
            source("count", requirement="optional", size_bytes=1, token_cost=1, priority=1),
        ],
        ContextBudgetPolicy(max_tokens=10, max_bytes=3, max_sources=1),
    )
    assert report.selected_ids == ("required",)
    assert report.omitted_optional_ids == ("bytes", "count")


def test_evaluation_is_input_order_invariant() -> None:
    items = [
        source("r", token_cost=2),
        source("a", requirement="optional", token_cost=3, priority=1),
        source("b", requirement="optional", token_cost=3, priority=0),
    ]
    expected = evaluate_context_budget(items, ContextBudgetPolicy(max_tokens=5)).to_dict()
    for permutation in itertools.permutations(items):
        actual = evaluate_context_budget(
            permutation, ContextBudgetPolicy(max_tokens=5)
        ).to_dict()
        assert actual == expected


def test_plan_digest_changes_with_policy_source_and_selection_facts() -> None:
    item = source("a", token_cost=2)
    first = evaluate_context_budget([item], ContextBudgetPolicy(max_tokens=2))
    policy_changed = evaluate_context_budget([item], ContextBudgetPolicy(max_tokens=3))
    source_changed = evaluate_context_budget(
        [source("a", token_cost=1)], ContextBudgetPolicy(max_tokens=2)
    )
    assert first.plan_digest != policy_changed.plan_digest
    assert first.plan_digest != source_changed.plan_digest


def test_require_context_budget_preserves_exact_report() -> None:
    sources = [source("a", token_cost=11)]
    policy = ContextBudgetPolicy(max_tokens=10)
    report = evaluate_context_budget(sources, policy)
    with pytest.raises(ContextBudgetError) as caught:
        require_context_budget(sources, policy)
    assert caught.value.report == report


def test_require_context_budget_returns_passing_report() -> None:
    sources = [source("a", token_cost=1)]
    policy = ContextBudgetPolicy(max_tokens=1)
    assert require_context_budget(sources, policy) == evaluate_context_budget(sources, policy)


def test_repository_map_bridge_binds_digest_and_normalized_size(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("x=1\n", encoding="utf-8")
    repository_map = scan_repository(tmp_path)
    item = repository_map_context_source(
        repository_map,
        token_cost=7,
        selection_reason="brownfield baseline",
        source_id="repo-facts",
        requirement="optional",
        priority=2,
    )
    encoded = json.dumps(
        repository_map.to_dict(),
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")
    assert item.source_id == "repo-facts"
    assert item.provenance == f"repository-map:{tmp_path.name}"
    assert item.revision == f"sha256:{repository_map.content_digest}"
    assert item.size_bytes == len(encoded)
    assert item.token_cost == 7
    assert item.requirement is ContextRequirement.OPTIONAL
    assert item.priority == 2


def test_repository_map_bridge_requires_map() -> None:
    with pytest.raises(ContextValidationError, match="RepositoryMap"):
        repository_map_context_source(  # type: ignore[arg-type]
            object(), token_cost=1, selection_reason="x"
        )


def test_repository_map_bridge_does_not_rescan_or_mutate(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("x=1\n", encoding="utf-8")
    repository_map = scan_repository(tmp_path)
    before = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    item = repository_map_context_source(
        repository_map, token_cost=1, selection_reason="use normalized facts"
    )
    after = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    assert before == after
    assert isinstance(repository_map, RepositoryMap)
    assert item.revision.endswith(repository_map.content_digest)
