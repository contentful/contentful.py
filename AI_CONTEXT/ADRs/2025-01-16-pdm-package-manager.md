# PDM as Package Manager and Build Tool

## Status

Accepted

## Context

Prior to January 2025, `contentful.py` used `setup.py` / `setup.cfg` for packaging and lacked a lockfile-based dependency workflow. This created inconsistency between local dev environments and CI, made it harder to pin test dependencies precisely, and required manual PyPI publishing steps.

The DX team was also standardizing Python SDK tooling across repos (`contentful.py`, `contentful-management.py`, `rich-text-renderer.py`) to reduce per-repo maintenance overhead.

Alternatives considered: `poetry` (used in some DX repos), `pip + requirements.txt`, `hatch`. Context not found in Glean for why these were rejected — likely a default/inherited choice based on team familiarity and PDM's native `pyproject.toml` support.

## Decision

Migrated to [PDM](https://pdm.fyi/) as the canonical dependency manager, build backend, and release tool (PR #97, commit `025d5d4`, January 2025).

Configuration lives entirely in `pyproject.toml`:
- `[project]` — package metadata (replaces `setup.py`)
- `[tool.pdm]` — version source, includes
- `[tool.pdm.scripts]` — all dev/build/release commands
- `[dependency-groups]` — optional groups: `test`, `docs`

`pdm.lock` is committed and provides a reproducible environment across local, CI, and release contexts.

Source: PR #97 (`025d5d4`), subsequent fixes in PRs #102, #104, #113, #116; confirmed by the internal Python SDK runbook [internal-doc].

## Consequences

- All commands go through `pdm run <script>`: `pdm run lint`, `pdm run test`, `pdm run coverage`, `pdm run release`
- `pdm.lock` must be kept up to date — stale lockfiles cause "Requested groups not in lockfile" errors at install/publish time. Run `pdm lock -d` if this occurs
- PyPI publishing is via `pdm publish` (uses twine under the hood) — credentials must be in `.pypirc` from [internal-credentials-vault]
- `pdm run release` is a composite script: `clean` → Sphinx doc generation (amends last commit) → publish → push tags. This means the last commit on `master` before release is amended by `git-docs` — reviewers should be aware this modifies commit history
- The `tox.ini` matrix still exists for cross-version testing (`pdm run test-all`) but CI uses the devcontainer + `pdm run coverage` path
