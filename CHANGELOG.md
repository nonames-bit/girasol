# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Repository scaffolding: folder structure, CI workflows, issue and pull request
  templates, agent configuration, documentation skeleton and ADRs.
- Wiring and data-connection documents: I/O map, power and control schematics,
  OPC UA / Sparkplug data contract and weights UDT layout.
- `ml/src/girasol/config.py`: loader for `ml/configs/girasol.yaml`, so capture and
  geometric constants have a single source instead of being duplicated in code.
- Third-order central moments and the explicit Hu `phi7` formula in
  `docs/02-matematicas.md` §5.4 and §5.6; feature 3 was previously inimplementable.
- Own CAD models under `hardware/cad/` (table, supports and Balluff sensor holder),
  versioned through git-lfs, with measured bounding boxes documented in the folder
  README.
- `hardware/cad/view_cad.py`: local viewer that loads STEP and STL through the OCP
  kernel and renders them in the VS Code OCP CAD Viewer panel.

### Fixed

- `parity.yml` no longer reports success without comparing: its readiness condition now
  matches the test's skip condition (Python **and** ST golden vectors), and the job runs
  with `-p no:cov` so it cannot fail on a coverage gate it does not measure.
- CI coverage now measures the documented target, 85 % on `girasol.features`, and the
  conflicting default coverage options were removed from `pyproject.toml`.
- Issue templates apply the labels of the normative taxonomy (`tipo:bug`,
  `tipo:experimento`), not the English brief's names.
- Corrected the compacidad unit (`P²/A` is dimensionless) and the `rAlpha` description
  (`alpha` is the error level, not the confidence level) in `docs/03-contrato-datos.md`.
- `.gitignore` now ignores credential material (`.env`, keys, certificates), which
  matters because the repository is public.

[Unreleased]: https://github.com/nonames-bit/girasol/commits/main
