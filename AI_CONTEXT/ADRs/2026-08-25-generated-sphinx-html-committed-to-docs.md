# API Reference Published as Generated Sphinx HTML Committed to `docs/`

## Date

2026-08-25

## Status

Accepted (retroactively recorded)

> This record was written on 2026-08-25 from the repository's configuration and
> commit history. It documents an existing, long-standing decision rather than a
> new one. Where the original rationale could not be established from the repo,
> this record states what is verifiably true and stops.

## Context

`contentful.py` ships a public API reference at
<https://contentful.github.io/contentful.py> (`pyproject.toml → [project.urls].Documentation`).
There are two directories involved:

- `_docs/` — the Sphinx **source** (`conf.py`, `index.rst`, `Makefile`, `_static/`)
- `docs/` — the built **HTML output**, committed to `master`

A project publishing Sphinx docs has several options for where the rendered HTML
lives: a `gh-pages` branch, an external host such as Read the Docs, a CI job that
publishes on push, or the `/docs` folder of the default branch (a GitHub Pages
source option that requires no branch juggling and no CI credentials).

This repo took the last option. The supporting configuration is unambiguous:

- `_docs/conf.py` enables `sphinx.ext.githubpages`, whose only job is to emit
  `.nojekyll` so GitHub Pages serves Sphinx's `_`-prefixed asset directories.
  `docs/.nojekyll` is committed, as are `docs/_static/`, `docs/_modules/`,
  `docs/_images/`, and `docs/_sources/`.
- `.gitignore` ignores `_docs/_build/` (the intermediate Sphinx build dir) but
  deliberately does **not** ignore `docs/`.
- Build output lands in `docs/` on release commits, not on feature commits:
  `git log -- docs` is dominated by "Bump to version X" commits (`25f50db` for
  2.5.0, `b27ca5c` for 2.4.0, `e9c99f4` for 2.0.0, and so on back through the
  available history).

The `sphinx.ext.githubpages` extension predates the history available in a
depth-100 clone (the oldest reachable commit is `d491146`), so the date and
author of the original decision could not be established. What *can* be dated is
the current automation: commit `025d5d4` ("Migrate to pdm (#97)") moved the doc
build into `pyproject.toml → [tool.pdm.scripts]` and wired it into the release
path.

## Decision

The rendered API reference is a **committed build artifact** at `docs/`,
regenerated as part of cutting a release, and served by GitHub Pages from the
`/docs` folder of `master`.

The mechanics, all defined in `pyproject.toml → [tool.pdm.scripts]`:

| Script | What it does |
|---|---|
| `docs` | Deletes `_docs/contentful.rst` and `_docs/modules.rst`, runs `sphinx-apidoc -o _docs/ contentful`, builds with `make -C _docs html`, then **`rm -rf docs`** and `cp -r _docs/_build/html docs` |
| `git-docs` | Composite: `docs` → `git add docs` → `git commit --amend -C HEAD` |
| `release` | Composite: `clean` → `git-docs` → `pdm publish` → `push-tags` |

Two consequences of that wiring are worth stating explicitly, because they are
not obvious from reading either script in isolation:

1. `docs` is **destructive** — `rm -rf docs` removes the whole directory before
   the copy. Nothing may live under `docs/` that is not produced by Sphinx.
2. `release` **amends the last commit on `master`** via `git-docs`, so the
   version tag points at a commit whose contents differ from what was reviewed.

Version stamping is automatic: `_docs/conf.py` does
`from contentful import __version__`, so the published docs track
`contentful/__init__.py`.

For the mechanics as operating documentation rather than as a decision, see
[ARCHITECTURE.md → Documentation Generation](../../ARCHITECTURE.md).

## Consequences

- **`docs/` is not a writable directory.** Any hand-authored file placed there is
  deleted by the next `pdm run docs`. `AGENTS.md` states this as an invariant and
  points contributors at `AI_CONTEXT/` instead.
- **This record therefore lives at `AI_CONTEXT/ADRs/`, not `docs/ADRs/`.** It was
  first drafted under `docs/ADRs/` to match the directory named by the
  organisation-wide AI harness readiness controls
  ([DX-1324](https://contentful.atlassian.net/browse/DX-1324), parent
  [DX-1296](https://contentful.atlassian.net/browse/DX-1296)). That placement
  collides head-on with the `rm -rf docs` step above: the next `pdm run docs` or
  `pdm run release` would have deleted the record silently. Rather than carry a
  file that the release process is guaranteed to destroy — or bend the release
  script to carve out an exception inside generated output — the record was moved
  to `AI_CONTEXT/ADRs/`, which is durable, is already this repo's ADR home, and is
  where `AGENTS.md` points. `docs/` stays exclusively Sphinx output, and the
  invariant above holds without a special case.
- **There is one ADR location, not two.** The repo's four pre-existing decision
  records live at `AI_CONTEXT/ADRs/` (001 CDA-only scope, 002 resource-builder
  deserialization, 003 PDM, 004 devcontainer/CI parity). This record is numbered
  **005**, continuing that sequence in the same directory and the same index, so
  auditing the decisions for this repo means reading one directory.
- Doc freshness is coupled to releases. Between releases, `docs/` reflects the
  last tagged version, not `master`. `docs/index.html` currently reports
  "Contentful 2.5.0 documentation".
- Because `release` amends `HEAD`, reviewers who compare the tag against the
  merged PR will see an extra `docs/` diff they never reviewed. This is expected,
  not tampering.
- Regenerating docs requires the `docs` dependency group (`Sphinx>=6.2.1`), which
  is not installed by the default `pdm install -G test` used by CI. CI never
  builds docs; `.github/workflows/ci.yml` runs only `pdm run lint` and
  `pdm run coverage`. Doc breakage is therefore only caught at release time.
- `pdm run docs` ends with `open docs/index.html`, a macOS-only command. The
  script is written for a developer laptop, not for automation.
- No credentials or CI publishing setup are needed to ship docs, which is the
  main practical benefit of the arrangement and the likeliest reason it has
  survived unchanged.
