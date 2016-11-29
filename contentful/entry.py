from .resource import FieldsResource
from .utils import is_link, is_link_array, resource_for_link
from .content_type_cache import ContentTypeCache


"""
contentful.entry
~~~~~~~~~~~~~~~~

This module implements the Entry class.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/entries

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class Entry(FieldsResource):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/entries
    """

    def _coerce(self, field_id, value, localized, includes):
        if is_link(value):
            return self._build_nested_resource(
                value,
                localized,
                includes
            )
        elif is_link_array(value):
            items = []
            for link in value:
                items.append(
                    self._build_nested_resource(
                        link,
                        localized,
                        includes
                    )
                )

            return items

        content_type = ContentTypeCache.get(
            self.sys['content_type'].id
        )
        if content_type is not None:
            content_type_field = content_type.field_for(field_id)
            if content_type_field is not None:
                return content_type_field.coerce(value)

        return super(Entry, self)._coerce(
            field_id,
            value,
            localized,
            includes
        )

    def _build_nested_resource(self, value, localized, includes):
        # Maximum include Depth is 10 in the API, but we raise it to 20,
        # in case one of the included items has a reference in an upper level,
        # so we can keep the include chain for that object as well
        # Any included object after the 20th level of depth will be just a Link
        if self._depth <= 20:
            resource = resource_for_link(value, includes)

            if resource is not None:
                return self._resolve_include(
                    resource,
                    localized,
                    includes
                )

        return self._build_link(value)

    def _resolve_include(self, resource, localized, includes):
        from .resource_builder import ResourceBuilder
        return ResourceBuilder(
            self.default_locale,
            localized,
            resource,
            includes,
            depth=self._depth + 1
        ).build()

    def __repr__(self):
        return "<Entry[{0}] id='{1}'>".format(
            self.sys['content_type'].sys.get('id', ''),
            self.sys.get('id', '')
        )
