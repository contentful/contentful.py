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
| `docs` | Deletes `_docs/contentful.rst` and `_docs/modules.rst`, runs `sphinx-apidoc -o _docs/ contentful`, builds with `make -C _docs html`, then **empties every entry directly under `docs/` except `docs/ADRs/`** and copies `_docs/_build/html/.` into `docs/` |
| `git-docs` | Composite: `docs` → `git add docs` → `git commit --amend -C HEAD` |
| `release` | Composite: `clean` → `git-docs` → `pdm publish` → `push-tags` |

Two consequences of that wiring are worth stating explicitly, because they are
not obvious from reading either script in isolation:

1. `docs` is **destructive within its own output** — it empties every entry
   directly under `docs/` before copying the new build in. Exactly one entry is
   carved out of that prune: `docs/ADRs/`. Nothing else may live under `docs/`
   that is not produced by Sphinx.
2. `release` **amends the last commit on `master`** via `git-docs`, so the
   version tag points at a commit whose contents differ from what was reviewed.

Version stamping is automatic: `_docs/conf.py` does
`from contentful import __version__`, so the published docs track
`contentful/__init__.py`.

For the mechanics as operating documentation rather than as a decision, see
[ARCHITECTURE.md → Documentation Generation](../../ARCHITECTURE.md).

## Consequences

- **`docs/` is writable in exactly one place: `docs/ADRs/`.** Any other
  hand-authored file placed under `docs/` is still deleted by the next
  `pdm run docs`. `AGENTS.md` states this as an invariant.
- **The prune carve-out exists because the records have nowhere else to go.** The
  organisation-wide AI harness readiness controls
  ([DX-1324](https://contentful.atlassian.net/browse/DX-1324), parent
  [DX-1296](https://contentful.atlassian.net/browse/DX-1296)) accept decision
  records only under `docs/ADRs/`, `docs/adr/`, `docs/decision-records/` or
  `docs/decisions/`. All four are inside `docs/`, so there is no compliant
  location that a whole-directory `rm -rf docs` would spare. Relocating the
  records outside `docs/` — this repo's previous `AI_CONTEXT/ADRs/` among them —
  keeps them safe from the build at the cost of making them invisible to the
  audit, which is not a fix. The narrower prune is therefore the change that
  resolves the collision, matching how
  [contentful/node-apps-toolkit#857](https://github.com/contentful/node-apps-toolkit/pull/857)
  settled the same conflict: the generator stops owning the whole directory.
- **GitHub Pages constrains the shape of the fix.** `node-apps-toolkit` could give
  its generator a subdirectory (`docs/api/`) because it publishes through a
  workflow whose `publish_dir` is settable. This repo uses legacy Pages serving
  `master:/docs`, and legacy Pages accepts only `/` or `/docs` as a source — not
  `docs/api`. Moving the HTML down a level would 404 the site root and shift every
  published URL under `/api/`, so the generated output stays at the `docs/` root
  and the carve-out is expressed in the prune instead.
- **There is one ADR location, not two.** All five records now live at
  `docs/ADRs/` — 001 CDA-only scope, 002 resource-builder deserialization, 003
  PDM, 004 devcontainer/CI parity, and this record as **005**. They previously
  lived at `AI_CONTEXT/ADRs/`; that directory now holds only `specs/`. Auditing
  the decisions for this repo means reading one directory, and it is the one the
  control looks in.
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
