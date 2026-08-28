# Brownfield scan examples

These examples use real public repositories pinned to exact revisions. They demonstrate reproducible `specgrain scan` inputs; this document intentionally does not publish precomputed scan output. Run the commands locally to inspect the exact repository state with the installed SpecGrain version.

SpecGrain's scanner reads bounded repository facts and does not execute repository commands, package scripts, tests, builds, or model calls.

## Python — pallets/itsdangerous

Pinned revision: `672971d66a2ef9f85151e53283113f33d642dabd`

```bash
git clone https://github.com/pallets/itsdangerous.git
cd itsdangerous
git checkout --detach 672971d66a2ef9f85151e53283113f33d642dabd
specgrain scan .
specgrain scan . --json > specgrain-scan.json
```

## Node.js — sindresorhus/p-map

Pinned revision: `22dda61ea29037ba85af25e84bc5efba77e62f44`

```bash
git clone https://github.com/sindresorhus/p-map.git
cd p-map
git checkout --detach 22dda61ea29037ba85af25e84bc5efba77e62f44
specgrain scan .
specgrain scan . --json > specgrain-scan.json
```

## Rust — BurntSushi/byteorder

Pinned revision: `5a82625fae462e8ba64cec8146b24a372b4d75c6`

```bash
git clone https://github.com/BurntSushi/byteorder.git
cd byteorder
git checkout --detach 5a82625fae462e8ba64cec8146b24a372b4d75c6
specgrain scan .
specgrain scan . --json > specgrain-scan.json
```

## What to compare

Use the JSON output to inspect repository identity, file counts, manifests, language signals, dependency signals, component/reuse signals, Git facts, skipped symlinks, and the normalized repository-map digest. A scan is repository understanding evidence, not proof that the external project builds or passes its own tests.

These repositories remain governed by their own licenses and maintainers. SpecGrain does not vendor or redistribute their source code.
