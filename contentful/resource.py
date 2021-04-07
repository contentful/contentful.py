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
            errors=None,
            localized=False,
            resources=None,
            depth=0,
            max_depth=20):
        self.raw = item
        self.default_locale = default_locale
        self._depth = depth
        self._max_depth = max_depth
        self.sys = self._hydrate_sys(item)
        self._metadata = self._hydrate_metadata(item)

        if resources is not None and 'sys' in item:
            cache_key = "{0}:{1}:{2}".format(
                item['sys']['type'],
                item['sys']['id'],
                item['sys'].get('locale', '*')
            )
            resources[cache_key] = self

    def _hydrate_sys(self, item):
        sys = {}
        for k, v in item.get('sys', {}).items():
            if k in ['space', 'contentType', 'environment']:
                v = self._build_link(v)
            if k in ['createdAt', 'updatedAt', 'deletedAt']:
                v = dateutil.parser.parse(v)
            sys[snake_case(k)] = v
        return sys

    def _hydrate_metadata(self, item):
        _metadata = {}
        for k, v in item.get('metadata', {}).items():
            if k == 'tags':
                v = list(map(self._build_link, v))
            _metadata[snake_case(k)] = v
        return _metadata

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

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d


class FieldsResource(Resource):
    """Fields Resource Class

    Implements locale handling for Resource fields.
    """
    def __init__(
            self,
            item,
            includes=None,
            errors=None,
            localized=False,
            resources=None,
            **kwargs):
        super(FieldsResource, self).__init__(
            item,
            includes=includes,
            errors=errors,
            localized=localized,
            resources=resources,
            **kwargs
        )

        self._fields = self._hydrate_fields(item, localized, includes, errors, resources=resources)

    def _hydrate_fields(self, item, localized, includes, errors, resources=None):
        if 'fields' not in item:
            return {}

        if includes is None:
            includes = []

        if errors is None:
            errors = []

        locale = self._locale()
        fields = {locale: {}}
        if localized:
            self._hydrate_localized_entry(fields, item, includes, errors, resources)
        else:
            self._hydrate_non_localized_entry(fields, item, includes, errors, resources)
        return fields

    def _hydrate_localized_entry(self, fields, item, includes, errors, resources=None):
        for k, locales in item['fields'].items():
            for locale, v in locales.items():
                if locale not in fields:
                    fields[locale] = {}
                fields[locale][snake_case(k)] = self._coerce(
                    snake_case(k),
                    v,
                    True,
                    includes,
                    errors,
                    resources=resources
                )

    def _hydrate_non_localized_entry(self, fields, item, includes, errors, resources=None):
        for k, v in item['fields'].items():
            fields[self._locale()][snake_case(k)] = self._coerce(
                snake_case(k),
                v,
                False,
                includes,
                errors,
                resources=resources
            )

    def _coerce(self, field_id, value, localized, includes, errors, resources=None):
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
