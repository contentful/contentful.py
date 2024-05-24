from __future__ import annotations

from typing import Dict, Any, Iterator, Callable

"""
contentful.client.queries
~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements normalization for query parameters.

Complete API Documentation: https://www.contentful.com/developers/docs/references/content-delivery-api/

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


__all__ = ("normalize",)


def normalize(**query: Any) -> NormalizedQueryT:
    if "initial" in query:
        query["initial"] = normalize_nonstring(query["initial"])

    if "select" in query:
        query["select"] = normalize_select(query["select"])

    normalized = {
        k: (
            ",".join(iternormalize(*v))
            if isinstance(v, (list, tuple, set, frozenset))
            else v
        )
        for k, v in query.items()
    }
    return normalized


def normalize_select(select: str | list[str]) -> str:
    """

    If the query contains the :select operator, we enforce :sys properties.
    The SDK requires sys.type to function properly, but as other of our
    SDKs require more parts of the :sys properties, we decided that every
    SDK should include the complete :sys block to provide consistency
    accross our SDKs.
    """

    q: list[str] | str = select
    if isinstance(q, str):
        q = q.split(",")

    filtered = ",".join(iternormalize(*q, filter=_filter_sys))
    normalized = ",".join((filtered, "sys"))
    return normalized


def _filter_sys(string: str) -> bool:
    if string.startswith("sys.") or string == "sys":
        return False
    return True


def iternormalize(
    *items: list[Any], filter: Callable[[str], bool] | None = None
) -> Iterator[str]:
    gen = (
        # Always remove whitespace from strings,
        #   Always normalize non-strings into strings.
        normalize_string(item) if isinstance(item, str) else normalize_nonstring(item)
        for item in items
    )
    if filter is not None:
        yield from (it for it in gen if filter(it))
        return
    yield from gen


def normalize_string(item: str) -> str:
    """Remove whitespace padding from strings."""

    return item.strip()


def normalize_nonstring(item: Any) -> str:
    """Convert int, bool to string and lowercase bools."""

    # add a .strip() to be consistent, this is a fall-through.
    return str(item).lower().strip()


NormalizedQueryT = Dict[str, str]
