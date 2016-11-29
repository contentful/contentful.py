from .resource import Resource
from .locale import Locale


"""
contentful.space
~~~~~~~~~~~~~~~~

This module implements the Space class.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/spaces

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class Space(Resource):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/spaces
    """

    def __init__(
            self,
            item,
            default_locale='en-US',
            includes=None,
            localized=False,
            depth=0):
        super(Space, self).__init__(
            item,
            default_locale,
            includes,
            localized,
            depth
        )
        self.name = item.get('name', '')
        self.locales = [Locale(locale) for locale in item.get('locales', [])]

    def __repr__(self):
        return "<Space[{0}] id='{1}'>".format(
            self.name,
            self.id
        )
