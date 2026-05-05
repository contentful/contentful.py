# CDA-Only Scope: Read vs Write SDK Split

## Status

Accepted

## Context

Contentful exposes two primary APIs with different purposes and access characteristics:

- **Content Delivery API (CDA)** — read-only, publicly distributable tokens, CDN-backed, high-throughput, optimized for frontend and consumer applications
- **Content Management API (CMA)** — read-write, scoped to authorized users/organizations, lower rate limits, used for content operations and tooling

At project inception, the question was whether a single Python SDK should cover both APIs or whether they should be separate libraries (mirroring the pattern established by the JavaScript and Ruby SDKs).

## Decision

`contentful.py` covers the CDA and Content Preview API (CPA) only. Write operations (creating/updating/publishing content) belong to the separate `contentful-management.py` SDK.

This mirrors the split already established for all other Contentful SDK languages (JS, Ruby, PHP, .NET, Swift, Java). The rationale: the two APIs have fundamentally different access patterns, token scopes, rate limits, error handling, and client initialization semantics. Combining them into one library would create a bloated, harder-to-document surface and force CDA users to take a dependency on CMA-specific logic they never use.

Source: Initial repository structure (commit `c771b38`); confirmed by the Contentful SDK coverage matrix and internal SDK documentation [internal-doc].

## Consequences

- CDA and CMA functionality require two separate `pip install` commands: `pip install contentful` (CDA) and `pip install contentful-management` (CMA)
- Feature parity between language SDKs is tracked across both repos separately
- Users who need both read and write in the same application must initialize two clients — an acceptable trade-off given the different token scopes required
- `contentful.py` can stay lean and focused; its public API surface is strictly the CDA resource types
