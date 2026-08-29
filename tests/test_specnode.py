from __future__ import annotations

import math

import pytest

from specgrain import SPECNODE_SCHEMA_VERSION, SpecNode, SpecValidationError, is_spec_id


def make_node(**overrides: object) -> SpecNode:
    values: dict[str, object] = {
        "id": "SG-000001",
        "title": "Session expiration",
        "outcome": "Expired sessions are rejected deterministically.",
        "rationale": "Reduce stale authenticated sessions.",
        "scope_in": ["session expiry", "401 response"],
        "scope_out": ["token refresh"],
        "acceptance": ["Expired sessions return 401", "Active sessions remain valid"],
        "dependencies": ["SG-000002", "SG-000003"],
        "risk": {"level": "medium", "rollback": {"required": True}},
        "context": {"budget": 12000, "sources": ["src/session.py", "tests/test_session.py"]},
        "change_surface": ["src/session.py", "tests/test_session.py"],
        "evidence": {"required": ["tests", "diff"]},
        "method": "dmadv-lite",
        "state": "SHAPED",
        "children": ["SG-000004"],
        "labels": ["auth", "security"],
        "metadata": {"owner": "platform", "priority": 1},
    }
    values.update(overrides)
    return SpecNode(**values)


def test_spec_id_contract() -> None:
    assert is_spec_id("SG-000001")
    assert is_spec_id("SG-999999")
    for value in ("SG-1", "SG-00001", "SG-0000001", "sg-000001", "AS-000001", 1, None):
        assert not is_spec_id(value)


@pytest.mark.parametrize("field", ["id", "parent_id"])
def test_invalid_direct_ids_raise_stable_error(field: str) -> None:
    kwargs: dict[str, object] = {field: "bad"}
    if field == "parent_id":
        kwargs["id"] = "SG-000001"
    with pytest.raises(SpecValidationError, match="must match"):
        SpecNode(title="x", outcome="y", **kwargs)


@pytest.mark.parametrize("field", ["dependencies", "children"])
def test_invalid_reference_ids_raise(field: str) -> None:
    with pytest.raises(SpecValidationError, match="must match"):
        make_node(**{field: ["bad"]})


def test_title_and_outcome_must_have_non_whitespace_content() -> None:
    with pytest.raises(SpecValidationError, match="title must not be empty"):
        make_node(title="   ")
    with pytest.raises(SpecValidationError, match="outcome must not be empty"):
        make_node(outcome="\n\t")


def test_set_like_fields_reject_duplicates() -> None:
    with pytest.raises(SpecValidationError, match="duplicate"):
        make_node(labels=["security", "security"])
    with pytest.raises(SpecValidationError, match="duplicate"):
        make_node(dependencies=["SG-000002", "SG-000002"])


def test_caller_owned_inputs_cannot_mutate_node_or_digest() -> None:
    risk = {"matrix": {"likelihood": 1}, "tags": ["a"]}
    dependencies = ["SG-000002"]
    node = make_node(risk=risk, dependencies=dependencies)
    digest = node.revision_digest

    risk["matrix"]["likelihood"] = 99
    risk["tags"].append("b")
    dependencies.append("SG-000003")

    assert node.to_dict()["risk"] == {"matrix": {"likelihood": 1}, "tags": ["a"]}
    assert node.dependencies == ("SG-000002",)
    assert node.revision_digest == digest


def test_to_dict_is_detached_from_node() -> None:
    node = make_node()
    exported = node.to_dict()
    exported["risk"]["level"] = "critical"
    exported["dependencies"].append("SG-000099")

    assert node.to_dict()["risk"]["level"] == "medium"
    assert "SG-000099" not in node.dependencies


def test_nested_json_requires_string_keys_and_finite_numbers() -> None:
    with pytest.raises(SpecValidationError, match="non-string object key"):
        make_node(metadata={1: "bad"})

    for value in (math.nan, math.inf, -math.inf):
        with pytest.raises(SpecValidationError, match="non-finite float"):
            make_node(metadata={"value": value})


def test_nested_unsupported_json_type_is_rejected() -> None:
    with pytest.raises(SpecValidationError, match="unsupported JSON value type"):
        make_node(metadata={"bad": {1, 2}})


def test_semantically_set_like_order_does_not_change_digest() -> None:
    first = make_node(
        dependencies=["SG-000003", "SG-000002"],
        acceptance=["B", "A"],
        labels=["z", "a"],
        risk={"z": 1, "a": 2},
    )
    second = make_node(
        dependencies=["SG-000002", "SG-000003"],
        acceptance=["A", "B"],
        labels=["a", "z"],
        risk={"a": 2, "z": 1},
    )

    assert first.canonical_content_json() == second.canonical_content_json()
    assert first.revision_digest == second.revision_digest


def test_nested_list_order_remains_content_significant() -> None:
    first = make_node(metadata={"steps": ["a", "b"]})
    second = make_node(metadata={"steps": ["b", "a"]})
    assert first.revision_digest != second.revision_digest


def test_state_is_excluded_from_content_revision_digest() -> None:
    shaped = make_node(state="SHAPED")
    ready = make_node(state="READY")
    assert shaped.to_dict()["state"] != ready.to_dict()["state"]
    assert shaped.revision_digest == ready.revision_digest


def test_content_change_changes_revision_digest() -> None:
    first = make_node(title="Session expiration")
    second = make_node(title="Session expiry")
    assert first.revision_digest != second.revision_digest


def test_unicode_and_round_trip_are_deterministic() -> None:
    node = make_node(
        title="جلسة المستخدم",
        outcome="تنتهي الجلسة بأمان ✓",
        metadata={"note": "café — 東京"},
    )
    rebuilt = SpecNode.from_dict(node.to_dict())

    assert rebuilt.to_dict() == node.to_dict()
    assert rebuilt.revision_digest == node.revision_digest
    assert "جلسة".encode() in node.canonical_content_json()


def test_from_dict_rejects_unknown_and_missing_fields() -> None:
    with pytest.raises(SpecValidationError, match="unknown fields"):
        SpecNode.from_dict({"id": "SG-000001", "title": "x", "outcome": "y", "extra": True})
    with pytest.raises(SpecValidationError, match="missing required fields"):
        SpecNode.from_dict({"id": "SG-000001", "title": "x"})


def test_from_dict_rejects_non_string_root_key() -> None:
    with pytest.raises(SpecValidationError, match="non-string object key"):
        SpecNode.from_dict({"id": "SG-000001", "title": "x", "outcome": "y", 1: "bad"})


def test_schema_version_is_explicit_and_digest_significant() -> None:
    node = make_node()
    assert node.schema_version == SPECNODE_SCHEMA_VERSION == 1
    assert node.to_dict()["schema_version"] == 1
    assert node.canonical_content_dict()["schema_version"] == 1


@pytest.mark.parametrize("value", [2, 0, True, "1"])
def test_unsupported_schema_version_is_rejected(value: object) -> None:
    with pytest.raises(SpecValidationError, match="schema_version|unsupported"):
        make_node(schema_version=value)


def test_canonical_json_v1_golden_vector() -> None:
    node = SpecNode(
        id="SG-000123",
        title="Canonical ✓",
        outcome="Stable bytes",
        scope_in=("z", "a"),
        acceptance=("second", "first"),
        risk={"z": 1e-7, "a": 1.25},
        metadata={"note": "café — 東京", "steps": ["b", "a"]},
        state="READY",
    )
    expected = (
        '{"acceptance":["first","second"],"change_surface":[],"children":[],'
        '"context":{},"dependencies":[],"evidence":{},"id":"SG-000123","labels":[],'
        '"metadata":{"note":"café — 東京","steps":["b","a"]},"method":"quick",'
        '"outcome":"Stable bytes","parent_id":null,"rationale":"","risk":{"a":1.25,'
        '"z":1e-07},"schema_version":1,"scope_in":["a","z"],"scope_out":[],'
        '"title":"Canonical ✓"}'
    ).encode()

    assert node.canonical_content_json() == expected
    assert node.revision_digest == (
        "sha256:30ce9cd0616d9d5ed87e181265b73f8fad61e8dd5a1b3309a8f3f8b61a357b1c"
    )
