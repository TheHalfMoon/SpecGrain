# Closeout — Specification 017 Native DRAFT CLI

## Product PR evidence

- Shaping PR: `#20`.
- Exact shaping head: `c700f5dcda9b82619bbae5fd920ab1b01b3d76de`.
- Canonical shaping merge: `5c7783dde897c975b3519b37bfd45b547244b273`.
- Product PR: `#21` — `feat: add native root DRAFT authoring`.
- Exact reviewed product head: `1255a9187f85591edd041a3125359e70d2eea379`.
- Exact final-head CI run: `33235889444` — `success`.
- Final-head CI completed all five permanent matrix jobs successfully.
- Submitted GitHub reviews at merge readiness: none.
- Inline review threads at merge readiness: none.
- Qodo was billing/trial blocked; no Qodo approval is claimed.
- CodeRabbit skipped automatic review because the repository had fewer than 10 stars; no CodeRabbit approval is claimed.
- Cubic supplied an automated summary only; it was not a submitted review.

## Canonical product merge evidence

- Product merge commit: `dedb9ee30a6b8856c9c06439c68f3a37225f0563`.
- First parent: shaped canonical base `5c7783dde897c975b3519b37bfd45b547244b273`.
- Second parent: exact reviewed product head `1255a9187f85591edd041a3125359e70d2eea379`.
- Merge used expected-head protection against `1255a9187f85591edd041a3125359e70d2eea379`.
- Canonical product tree: `dbb5f12296f0412dfdfb0b829392e9c87c434c00`.

## Canonical post-merge CI evidence

Canonical `main` CI run `33236142514` completed with conclusion `success` on exact head `dedb9ee30a6b8856c9c06439c68f3a37225f0563`.

All five permanent matrix jobs completed successfully:

- Ubuntu / Python 3.11 — job `99057354064`;
- Ubuntu / Python 3.12 — job `99057354191`;
- Ubuntu / Python 3.13 — job `99057354207`;
- macOS / Python 3.11 — job `99057354224`;
- Windows / Python 3.11 — job `99057354192`.

The jobs include Ruff source/tests/examples, editable installation, full regression, tracked-tree cleanliness, compileall, CLI smoke, package build, built-wheel installation, and installed-CLI smoke.

## Product boundary after 017

Current `main` now supports deterministic native root-DRAFT authoring through `create_draft_spec` and `specgrain draft`. It still does not expose recursive child refinement, lifecycle promotion, WorkPacket/executor orchestration, provider execution, hosted services, or empirical benchmark superiority work.

The published `v0.1.0` release remains at `5eb46db0479cb8707afe070027dab4f3c558849a` and predates `specgrain draft`. This closeout does not claim a new release or PyPI publication.

## Frontier re-audit

A fresh product-frontier audit at `docs/research/post-017-product-audit-2026-08-29.md` records current repository, release, adoption, and product-surface truth. It does not authorize a successor specification by itself.

## Canonicalization boundary

This closeout PR is documentation-only. Its future merge SHA is intentionally not fabricated here.

The `CLOSED_CANONICAL` status carried by this closeout tree becomes authoritative only if:

1. the exact closeout PR head containing this file completes required exact-head CI/review checks;
2. that exact head is merged with expected-head protection; and
3. live GitHub proves canonical `main` contains that exact closeout head as the merge second parent and the required post-closeout CI succeeds.
