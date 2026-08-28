# Plan 000 — Foundation

## Strategy

This specification is documentation-only. It creates the control documents required before product code begins.

## Artifact map

| Concern | Canonical artifact |
| --- | --- |
| Repository execution rules | `AGENTS.md` |
| Product invariants | `.specify/memory/constitution.md` |
| Active repository front | `specs/CURRENT.md` |
| Product purpose and boundaries | `docs/product-thesis.md` |
| Core entities and relationships | `docs/domain-model.md` |
| Delivery philosophy | `docs/methodology.md` |
| Component boundaries | `docs/architecture.md` |
| External positioning | `docs/competitive-positioning.md` |
| Benchmark claims and method | `docs/benchmark-strategy.md` |
| External code/research provenance | `docs/donor-policy.md` |
| Progressive sequence | `docs/roadmap.md` |
| Public adoption strategy | `docs/launch-strategy.md` |
| Durable architecture choices | `docs/adr/` |

## Review method

Perform a cross-document consistency review against:

- terminology;
- product scope;
- deterministic/probabilistic boundary;
- state names;
- next-spec ordering;
- Spec Kit relationship;
- methodology claims;
- benchmark claim discipline.

No product tests are required because this spec adds no executable product code. Repository changes should still be reviewed as one bounded foundation PR.

## Exit

When acceptance criteria pass on the exact PR head, merge the PR, re-read canonical `main`, update `specs/CURRENT.md`, and begin `001-specnode-schema`.
