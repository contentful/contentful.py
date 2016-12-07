import dateutil.parser

from .utils import snake_case


"""
contentful.resource
~~~~~~~~~~~~~~~~~~~

This module implements the Resource, FieldResource and Link classes.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/introduction/common-resource-attributes

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class Resource(object):
    """
    Base Resource Class

    Implements common resource attributes.

    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/introduction/common-resource-attributes
    """

    def __init__(
            self,
            item,
            default_locale='en-US',
            includes=None,
            localized=False,
            depth=0):
        self.raw = item
        self.default_locale = default_locale
        self._depth = depth
        self.sys = self._hydrate_sys(item)

    def _hydrate_sys(self, item):
        sys = {}
        for k, v in item['sys'].items():
            if k in ['space', 'contentType']:
                v = self._build_link(v)
            if k in ['createdAt', 'updatedAt', 'deletedAt']:
                v = dateutil.parser.parse(v)
            sys[snake_case(k)] = v
        return sys

    def _build_link(self, link):
        return Link(link)

    def __getattr__(self, name):
        if name in self.sys:
            return self.sys[name]
        raise AttributeError(
            "'{0}' object has no attribute '{1}'".format(
                self.__class__.__name__,
                name
            )
        )


class FieldsResource(Resource):
    """Fields Resource Class

    Implements locale handling for Resource fields.
    """
    def __init__(
            self,
            item,
            default_locale='en-US',
            includes=None,
            localized=False,
            depth=0):
        super(FieldsResource, self).__init__(
            item,
            default_locale,
            includes,
            localized,
            depth
        )

        self._fields = self._hydrate_fields(item, localized, includes)

    def _hydrate_fields(self, item, localized, includes):
        if 'fields' not in item:
            return {}

        if includes is None:
            includes = []

        locale = self._locale()
        fields = {locale: {}}
        if localized:
            for k, locales in item['fields'].items():
                for locale, v in locales.items():
                    if locale not in fields:
                        fields[locale] = {}
                    fields[locale][snake_case(k)] = self._coerce(
                        snake_case(k),
                        v,
                        localized,
                        includes
                    )
        else:
            for k, v in item['fields'].items():
                fields[locale][snake_case(k)] = self._coerce(
                    snake_case(k),
                    v,
                    localized,
                    includes
                )
        return fields

    def _coerce(self, field_id, value, localized, includes):
        return value

    def fields(self, locale=None):
        """Get fields for a specific locale

        :param locale: (optional) Locale to fetch, defaults to default_locale.
        """

        if locale is None:
            locale = self._locale()
        return self._fields.get(locale, {})

    @property
    def locale(self):
        return self.sys.get('locale', None)

    def _locale(self):
        return self.locale or self.default_locale

    def __getattr__(self, name):
        locale = self._locale()
        if name in self._fields.get(locale, {}):
            return self._fields[locale][name]
        return super(FieldsResource, self).__getattr__(name)


class Link(Resource):
    """Link Class

    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/links
    """

    def resolve(self, client):
        """Resolves Link to a specific Resource"""

        resolve_method = getattr(client, snake_case(self.link_type))
        if self.link_type == 'Space':
            return resolve_method()
        else:
            return resolve_method(self.id)

    def __repr__(self):
        return "<Link[{0}] id='{1}'>".format(
            self.link_type,
            self.id
        )
