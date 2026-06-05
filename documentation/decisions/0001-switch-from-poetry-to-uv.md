---
status: proposed
date: 2026-06-10
deciders: Lars Heppler
consulted: ESMF SDK Python working group
informed: all contributors
---
# Switch Dependency and Packaging Tool from Poetry to uv

## Context and Problem Statement

The ESMF SDK Python Aspect Model Loader used [Poetry](https://python-poetry.org/) as its
dependency manager and packaging tool since the project's inception. As the Python ecosystem
has matured, a new generation of tooling has emerged. Poetry has several pain points that
affect developer experience and CI reliability:

* Poetry's resolver is significantly slower than newer alternatives on cold-cache environments
  (e.g., fresh CI runners).
* The Poetry action (`abatilo/actions-poetry`) is a third-party wrapper with its own release
  cadence, adding an extra supply-chain dependency in CI.
* Poetry uses its own metadata format (`[tool.poetry]`) rather than the PEP 621 standard
  `[project]` table, making the project less interoperable with other tooling.
* `tox` was erroneously declared as a runtime dependency in `[tool.poetry.dependencies]`
  instead of a development-only dependency.

How should the project manage dependencies and packaging going forward?

## Decision Drivers

* **Speed**: Faster dependency resolution and installation in CI and developer machines.
* **Standards compliance**: Prefer PEP 517/518/621-compliant tooling to maximise
  interoperability and reduce lock-in.
* **Supply-chain security**: Fewer third-party CI actions mean a smaller attack surface.
* **Active maintenance**: The chosen tool must be actively maintained with a large community.
* **Lockfile support**: Deterministic, reproducible installs must be achievable via a lockfile
  committed to version control.

## Considered Options

* **Keep Poetry** – continue with the existing setup.
* **Switch to [uv](https://docs.astral.sh/uv/)** – a Rust-based, all-in-one Python package
  manager developed by Astral (the team behind Ruff).
* **Switch to [PDM](https://pdm-project.org/)** – a PEP 582/621-compliant dependency manager.
* **Switch to pip + pip-tools** – use the de-facto standard pip together with pip-tools for
  lockfile generation.

## Decision Outcome

Chosen option: **"Switch to uv"**, because it meets all decision drivers better than the
alternatives:

* It is the fastest Python package installer and resolver available at decision time
  (benchmarks show 10–100× faster than pip/Poetry).
* It natively supports PEP 621 (`[project]` table) and PEP 735 (`[dependency-groups]`),
  making the `pyproject.toml` fully standards-compliant.
* The official `astral-sh/setup-uv` GitHub Action removes the dependency on the third-party
  `abatilo/actions-poetry` action.
* uv generates a `uv.lock` lockfile that can be committed to version control, providing
  reproducible installs identical to Poetry's `poetry.lock` approach.
* uv is designed as a drop-in replacement for `pip`, `pip-tools`, `pipx`, `poetry`, and
  `virtualenv`, providing a unified interface with a low migration overhead.

### Consequences

* Good, because CI pipelines run faster due to uv's superior resolver and caching.
* Good, because `pyproject.toml` now uses the standardised `[project]` table (PEP 621),
  improving compatibility with IDEs, linters, and other tooling.
* Good, because `tox` is correctly classified as a development-only dependency in
  `[dependency-groups] dev` (PEP 735), removing it from the published package's runtime
  requirements.
* Good, because the number of third-party CI actions is reduced, shrinking the supply-chain
  attack surface.
* Bad, because contributors who have only used Poetry need to install uv and update their
  local workflows (migration cost is low but non-zero).
* Bad, because uv is a younger project than Poetry; some edge-case behaviours may not be
  as well-documented yet.

## Validation

* All CI workflows (push-request check and tagged release) must pass with uv.
* `uv run tox` must execute the full test suite (`py310`) and PEP 8 checks (`pep8`) without
  errors.
* `uv build` must produce a valid wheel and sdist that can be published to PyPI.
* The `uv.lock` file must be committed and kept up to date with `pyproject.toml`.

## Pros and Cons of the Options

### Keep Poetry

* Good, because no migration effort is required.
* Good, because the team is already familiar with Poetry's workflow.
* Bad, because Poetry uses a non-standard `[tool.poetry]` metadata format (not PEP 621).
* Bad, because Poetry's resolver is significantly slower than uv, increasing CI times.
* Bad, because the third-party `abatilo/actions-poetry` action adds a supply-chain risk.
* Bad, because `tox` was incorrectly listed as a runtime dependency — fixing this in Poetry
  is possible but requires restructuring dependency groups.

### Switch to uv

* Good, because it is the fastest Python resolver/installer available.
* Good, because it is PEP 517/518/621/735-compliant out of the box.
* Good, because the official `astral-sh/setup-uv` action is maintained by the same team.
* Good, because `uv.lock` provides reproducible builds equivalent to `poetry.lock`.
* Neutral, because uv is younger than Poetry (first stable release in 2024), but it is
  backed by Astral and has very rapid adoption in the Python ecosystem.
* Bad, because contributors must install and learn a new tool.

### Switch to PDM

* Good, because PDM is PEP 621-compliant.
* Neutral, because PDM's adoption is smaller than both Poetry and uv.
* Bad, because PDM is slower than uv.
* Bad, because there is no widely used official CI action for PDM.

### Switch to pip + pip-tools

* Good, because pip is universally available and requires no additional tooling.
* Bad, because pip-tools does not provide a unified workflow for packaging (building/publishing).
* Bad, because managing virtual environments manually adds complexity.
* Bad, because the resolver is slower than uv.

## More Information

* [uv documentation](https://docs.astral.sh/uv/)
* [uv GitHub repository](https://github.com/astral-sh/uv)
* [astral-sh/setup-uv GitHub Action](https://github.com/astral-sh/setup-uv)
* [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
* [PEP 735 – Dependency Groups in pyproject.toml](https://peps.python.org/pep-0735/)

