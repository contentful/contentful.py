from .resource import FieldsResource
from .utils import is_link, is_link_array, resource_for_link, unresolvable
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

    def _coerce(self, field_id, value, localized, includes, errors, resources=None):
        if is_link(value):
            if unresolvable(value, errors):
                return None
            return self._build_nested_resource(
                value,
                localized,
                includes,
                errors,
                resources=resources
            )
        elif is_link_array(value):
            items = []
            for link in value:
                if unresolvable(link, errors):
                    continue
                items.append(
                    self._build_nested_resource(
                        link,
                        localized,
                        includes,
                        errors,
                        resources=resources
                    )
                )

            return items

        content_type = ContentTypeCache.get(
            self.sys['content_type'].id
        )
        if content_type is not None:
            content_type_field = content_type.field_for(field_id)
            if content_type_field is not None:
                return content_type_field.coerce(
                    value,
                    includes=includes,
                    errors=errors,
                    resources=resources,
                    default_locale=self.default_locale,
                    locale=self.sys.get('locale', '*')
                )

        return super(Entry, self)._coerce(
            field_id,
            value,
            localized,
            includes,
            errors,
            resources
        )

    def _build_nested_resource(self, value, localized, includes, errors, resources=None):
        # Maximum include Depth is 10 in the API, but we raise it to 20 (default),
        # in case one of the included items has a reference in an upper level,
        # so we can keep the include chain for that object as well
        # Any included object after the 20th level of depth will be just a Link.
        # When using reuse_entries, this is not the case if the entry was previously
        # cached.

        resource = resource_for_link(
            value,
            includes,
            resources=resources,
            locale=self.sys.get('locale', '*')
        )

        if isinstance(resource, FieldsResource):  # Resource comes from instance cache
            return resource

        if self._depth < self._max_depth:
            if resource is not None:
                return self._resolve_include(
                    resource,
                    localized,
                    includes,
                    errors,
                    resources=resources
                )

        return self._build_link(value)

    def _resolve_include(self, resource, localized, includes, errors, resources=None):
        from .resource_builder import ResourceBuilder
        return ResourceBuilder(
            self.default_locale,
            localized,
            resource,
            includes_for_single=includes,
            errors_for_single=errors,
            reuse_entries=bool(resources),
            resources=resources,
            depth=self._depth + 1,
            max_depth=self._max_depth
        ).build()

    def incoming_references(self, client=None, query={}):
        """Fetches all entries referencing the entry

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/search-parameters/links-to-asset

        :param client Client instance
        :param query: (optional) Dict with API options.
        :return: List of :class:`Entry <contentful.entry.Entry>` objects.
        :rtype: List of contentful.entry.Entry

        Usage:
            >>> entries = entry.incoming_references(client)
            [<Entry[cat] id='happycat'>]
        """

        if client is None:
            return False

        query.update({'links_to_entry': self.id})
        return client.entries(query)

    def __repr__(self):
        return "<Entry[{0}] id='{1}'>".format(
            self.sys['content_type'].sys.get('id', ''),
            self.sys.get('id', '')
        )
