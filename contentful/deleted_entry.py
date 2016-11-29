from .resource import Resource


"""
contentful.deleted_entry
~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the DeletedEntry class.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/synchronization

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class DeletedEntry(Resource):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/synchronization
    """

    def __repr__(self):
        return "<DeletedEntry id='{0}'>".format(
            self.sys.get('id', '')
        )
