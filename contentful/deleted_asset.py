from .resource import Resource


"""
contentful.deleted_asset
~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the DeletedAsset class.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/synchronization

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class DeletedAsset(Resource):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/synchronization
    """

    def __repr__(self):
        return "<DeletedAsset id='{0}'>".format(
            self.sys.get('id', '')
        )
