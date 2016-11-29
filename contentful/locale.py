"""
contentful.locale
~~~~~~~~~~~~~~~~~

This module implements the Locale class.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/localization

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class Locale(object):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/localization
    """

    def __init__(self, locale_data):
        self.code = locale_data.get('code', '')
        self.name = locale_data.get('name', '')
        self.fallback_code = locale_data.get('fallbackCode', '')
        self.default = locale_data.get('default', False)

    def __repr__(self):
        return "<Locale[{0}] code='{1}' default={2}>".format(
            self.name,
            self.code,
            self.default
        )
