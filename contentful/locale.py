from .resource import Resource
"""
contentful.locale
~~~~~~~~~~~~~~~~~

This module implements the Locale class.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/localization

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class Locale(Resource):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/localization
    """

    def __init__(self, item, **kwargs):
        super(Locale, self).__init__(item, **kwargs)
        self.code = item.get('code', '')
        self.name = item.get('name', '')
        self.fallback_code = item.get('fallbackCode', '')
        self.default = item.get('default', False)
        self.optional = item.get('optional', False)

    def __repr__(self):
        return "<Locale[{0}] code='{1}' default={2} fallback_code={3} optional={4}>".format(
            self.name,
            self.code,
            self.default,
            "'{0}'".format(
              self.fallback_code
            ) if self.fallback_code is not None else 'None',
            self.optional
        )
