# Resource Builder Deserialization Pattern

## Status

Accepted

## Context

The Contentful CDA returns heterogeneous JSON responses: a single response can contain entries, assets, deleted entries, deleted assets, content types, sync pages, and array wrappers — all identified by `sys.type`. Client code needs a way to transform this raw JSON into typed Python objects suitable for consumer use, including:

- Hydrating nested links recursively
- Applying field coercions based on content type schema (date strings → `datetime`, integers, etc.)
- Resolving localized field variants
- Handling errors for unresolvable links gracefully
- Preventing infinite recursion in circular reference graphs

## Decision

All response deserialization is centralized in a single `ResourceBuilder` class (`contentful/resource_builder.py`). `Client` never constructs resource objects directly — it always passes the raw JSON to `ResourceBuilder.build()`, which dispatches to the correct resource class based on `sys.type`.

Field coercion is handled by `ContentTypeField.coerce()` and the type classes in `content_type_field_types.py`, using the in-process `ContentTypeCache` to look up the schema without extra API calls.

Source: Initial architecture committed in `c771b38`; pattern unchanged through v2.5.0.

## Consequences

- A single code path owns the full JSON-to-object transformation, making it easy to add new resource types (e.g., `TaxonomyConcept` in PR #111, `AssetKey` in PR #101)
- `ContentTypeCache` must be populated before any entry deserialization; `Client.__init__` does this by default (`content_type_cache=True`)
- Disabling `content_type_cache=False` means fields fall back to uncoerced raw values — acceptable for raw/tooling use cases but not for typed consumer use
- Recursive link resolution is depth-capped by `max_include_resolution_depth` (default 20) to prevent stack overflows on deeply nested content graphs
- `reuse_entries=True` enables object reuse across a single request's deserialization pass (reduces object allocation for large include graphs); off by default to avoid surprising mutation behavior
