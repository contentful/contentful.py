# Architecture Decision Records

The repository's original decision records live in
[`AI_CONTEXT/ADRs/`](../../AI_CONTEXT/ADRs/) and are indexed there. This
directory holds records kept under `docs/` for the AI harness readiness controls.

| ADR | Date | Status | Title |
|---|---|---|---|
| [001](./2026-08-25-generated-sphinx-html-committed-to-docs.md) | 2026-08-25 | Accepted (retroactively recorded) | API Reference Published as Generated Sphinx HTML Committed to `docs/` |

> **Note:** `pdm run docs` runs `rm -rf docs` before copying in the Sphinx build,
> so files in this directory are deleted by the next docs build. See the record
> above for details.
