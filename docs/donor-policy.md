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
- `github/spec-kit` at `5aa8bea7823dcd056f111f847bf2d576bad3f0a5`.

The design synthesis and exact reviewed paths are recorded in `docs/research/planning-donor-synthesis-2026-08-28.md`.

No source code from these reviews is copied by that research change. Future copied or closely adapted material still requires the provenance process below.

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
