# Devcontainer for Reproducible Dev and CI Parity

## Status

Accepted

## Context

DX ticket [DX-822](https://contentful.atlassian.net/browse/DX-822) identified a recurring problem across DX Python SDKs: "works locally but not in CI" failures caused by mismatched Python versions, missing system dependencies, or inconsistent package installation order. Each contributor had to manually set up their local Python environment, and there was no guarantee it matched CI.

The DX team decided to standardize reproducible dev environments across all non-JS SDKs using devcontainers (PR #116, commit `adb0d67`, January 2025).

## Decision

Added a `.devcontainer/` configuration (`devcontainer.json` + `Dockerfile`) that:
- Bases on `mcr.microsoft.com/devcontainers/python:1-${PYTHON_VERSION}-bookworm` with a configurable `PYTHON_VERSION` build arg (defaults to 3.12)
- Installs PDM at container build time
- Runs `pdm install -G test && python -m pip install -e .` on container creation (`postCreateCommand`)

**CI uses the same devcontainer:** `.github/workflows/ci.yml` installs `@devcontainers/cli` and runs all lint/test jobs via `devcontainer up` + `devcontainer exec` — ensuring exact parity with the local dev environment.

Source: PR #116 (`adb0d67`), [DX-822](https://contentful.atlassian.net/browse/DX-822).

## Consequences

- Contributors need Docker installed — adds a dependency for local development
- CI is slower due to container build overhead, but environment parity eliminates a class of "flaky only in CI" bugs
- Python version under test is configurable via the `PYTHON_VERSION` env var — CI passes this via the matrix strategy
- VS Code users get automatic extension and interpreter setup; non-VS Code users use the Dev Container CLI
- The container does not persist state between CI runs — each job does a fresh `devcontainer up`
- External contributors must have Docker and the Dev Container CLI; the `CONTRIBUTING.md` documents this requirement
