from .utils import snake_case
from .content_type_field_types import *  # noqa: F401

"""
contentful.content_type_field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the ContentTypeField class.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-types

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class ContentTypeField(object):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-types
    """

    def __init__(self, field_data):
        self.raw = field_data
        self.id = snake_case(field_data.get('id', ''))
        self.name = field_data.get('name', '')
        self.type = field_data.get('type', '')
        self.items = field_data.get('items', {})
        self.localized = field_data.get('localized', False)
        self.omitted = field_data.get('omitted', False)
        self.required = field_data.get('required', False)
        self.disabled = field_data.get('disabled', False)
        self._coercion = self._get_coercion()

    def coerce(self, value):
        """Coerces the value to the proper type."""

        return self._coercion.coerce(value)

    def _get_coercion(self):
        """Gets the proper coercion type"""

        return globals()["{0}Field".format(self.type)](self.items)

    def __repr__(self):
        return "<ContentTypeField[{0}] id='{1}' type='{2}'>".format(
            self.name,
            self.id,
            self.type
        )
