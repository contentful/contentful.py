from .resource import Resource


"""
contentful.asset_key
~~~~~~~~~~~~~~~~~~
This module implements the AssetKey class.
API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/asset-keys
:copyright: (c) 2024 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class AssetKey(Resource):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/asset-keys
    """

    def __init__(self, item, **kwargs):
        super(AssetKey, self).__init__(item, **kwargs)
        self.policy = item.get('policy', '')
        self.secret = item.get('secret', '')

    def __repr__(self):
        return "<AssetKey policy='{0}' secret='{1}'>".format(
            self.policy,
            self.secret
        )
