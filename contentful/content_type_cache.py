from __future__ import annotations

from contentful.content_type import ContentType
"""
contentful.content_type_cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the ContentTypeCache class.

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class ContentTypeCache:
    """
    Cache for Content Types.

    Used for properly coercing Entry fields.
    """

    __CACHE__ = {}

    @classmethod
    def get(cls, space_id: str, content_type_id: str) -> ContentType | None:
        """
        Fetches a Content Type from the Cache.
        """

        for content_type in cls.__CACHE__.get(space_id, []):
            if content_type.sys.get('id') == content_type_id:
                return content_type
        return None

    @classmethod
    def update_cache(cls, *, space_id: str, content_types: list[ContentType]):
        """
        Updates the Cache with all Content Types from the Space.
        """

        cls.__CACHE__[space_id] = content_types
