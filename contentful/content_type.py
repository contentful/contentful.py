from .resource import Resource
from .content_type_field import ContentTypeField


"""
contentful.content_type
~~~~~~~~~~~~~~~~~~~~~~~

This module implements the ContentType class.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-types

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class ContentType(Resource):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-types
    """

    def __init__(self, item, **kwargs):
        super(ContentType, self).__init__(item, **kwargs)
        self.name = item.get('name', '')
        self.description = item.get('description', '')
        self.display_field = item.get('displayField', '')
        self.fields = [ContentTypeField(field)
                       for field in item.get('fields', [])]

    def field_for(self, field_id):
        """Fetches the field for the given Field ID.

        :param field_id: ID for Field to fetch.
        :return: :class:`ContentTypeField <ContentTypeField>` object.
        :rtype: contentful.ContentTypeField
        """

        for field in self.fields:
            if field.id == field_id:
                return field
        return None

    def __repr__(self):
        return "<ContentType[{0}] id='{1}'>".format(
            self.name,
            self.sys.get('id', '')
        )
