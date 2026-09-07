# Donor and Provenance Policy

## Purpose

SpecGrain learns from successful open-source projects while remaining independently designed and legally clean.

## GitHub Spec Kit

GitHub Spec Kit is licensed under MIT and is an important donor/reference candidate. SpecGrain may adapt appropriately licensed implementation ideas, but it is not a fork and should not inherit upstream architecture by default.

Reference: <https://github.com/github/spec-kit>

## Current design references

The following projects have influenced planning/research without code adoption:

- `DietrichGebert/ponytail` at `2ed6c52c9d7e5e56942508591085fd45dea277d3`;
- `multica-ai/andrej-karpathy-skills` at `2c606141936f1eeef17fa3043a72095b4765b9c2`;
- `github/spec-kit` at `5aa8bea7823dcd056f111f847bf2d576bad3f0a5`;
- `Tencent/LoopForge` at `09c765286f549624dd95434e1e6ef2249657cbeb`;
- `Tencent/SkillHone` at `7d565839fb4dc74f9c77f09ace660e1c0484e048`.

The initial planning synthesis and exact reviewed paths for Ponytail, the Karpathy-inspired coding guidelines, and GitHub Spec Kit are recorded in `docs/research/planning-donor-synthesis-2026-08-28.md`.

The post-026 LoopForge/SkillHone qualification, exact reviewed paths, fit assessment, retained design lessons, rejected adoptions, and continuation boundary are recorded in `docs/research/post-026-tencent-donor-qualification-2026-09-08.md`.

No source code from these reviews is copied by those research changes. Future copied or closely adapted material still requires the provenance process below.

## Rules before adopting donor material

For any non-trivial copied or closely adapted code, template, test, or documentation:

1. Record source repository and exact revision/tag when practical.
2. Verify the source license for the exact material.
3. Preserve required notices.
4. Record which local files contain the adaptation.
5. Explain why reuse is better than a smaller native implementation.
6. Add tests that define SpecGrain's own expected behavior.

## Provenance record format

Future donor adoptions should be recorded under `docs/provenance/` with:

- source URL;
- source revision;
- source license;
- source paths;
- destination paths;
- nature of adaptation;
- required notice handling;
- reviewer confirmation.

## Design references are not code provenance

Reading a project or paper and independently implementing a general idea should be cited in architecture/research notes when influential, but should not falsely be described as copied code.

## Dependency policy

Prefer mature, small dependencies when they remove substantial maintenance risk. Do not add a dependency solely because an upstream project uses it. Every runtime dependency should have an explicit role and should not undermine offline/local-first operation of the core.
