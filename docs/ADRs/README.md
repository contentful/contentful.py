# Architecture Decision Records

This repository's decision records were originally seeded at
[`AI_CONTEXT/ADRs/`](../../AI_CONTEXT/ADRs/), which holds records 001–004 and its
own index. That directory remains the primary home and is the one
[`AGENTS.md`](../../AGENTS.md) links to.

This directory holds records kept under `docs/` to satisfy the AI harness
readiness controls, which only accept decision records beneath `docs/`.
**Numbering continues the `AI_CONTEXT/ADRs/` sequence** — it does not restart —
so the two indexes together form one unbroken series. Anyone auditing decisions
for this repo must read both.

| ADR | Date | Status | Title |
|---|---|---|---|
| [005](./2026-08-25-generated-sphinx-html-committed-to-docs.md) | 2026-08-25 | Accepted (retroactively recorded) | API Reference Published as Generated Sphinx HTML Committed to `docs/` |

> **:warning: This directory is inside generated build output.** `docs/` is the
> committed Sphinx HTML build (48 generated files on `master`), and
> `pyproject.toml → [tool.pdm.scripts].docs` runs `rm -rf docs` before copying a
> fresh build in. `pdm run release` invokes it via `git-docs`. **The next docs
> build or release will delete this directory**, including record 005 and this
> index. Record 005 documents the hazard in full; it needs a human decision —
> either the `docs` script learns to preserve `docs/ADRs/`, or the control accepts
> `AI_CONTEXT/ADRs/` as a valid path.
