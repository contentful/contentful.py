"""
contentful.content_type_cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the ContentTypeCache class.

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class ContentTypeCache(object):
    """
    Cache for Content Types.

    Used for properly coercing Entry fields.
    """

    __CACHE__ = []

    @classmethod
    def get(cls, content_type_id):
        """
        Fetches a Content Type from the Cache.
        """

        for content_type in cls.__CACHE__:
            if content_type.sys.get('id') == content_type_id:
                return content_type
        return None

    @classmethod
    def update_cache(cls, client):
        """
        Updates the Cache with all Content Types from the Space.
        """

        cls.__CACHE__ = client.content_types()
