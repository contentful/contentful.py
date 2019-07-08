from .resource import FieldsResource


"""
contentful.asset
~~~~~~~~~~~~~~~~

This module implements the Asset class.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/assets

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class Asset(FieldsResource):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/assets
    """

    def url(self, **kwargs):
        """Returns a formatted URL for the Asset's File
        with serialized parameters.

        Usage:
            >>> my_asset.url()
            "//images.contentful.com/spaces/foobar/..."
            >>> my_asset.url(w=120, h=160)
            "//images.contentful.com/spaces/foobar/...?w=120&h=160"
        """

        if not hasattr(self, 'file') or not self.file:
            return ""

        url = self.file['url']
        args = ['{0}={1}'.format(k, v) for k, v in kwargs.items()]

        if args:
            url += '?{0}'.format('&'.join(args))

        return url

    def incoming_references(self, client=None, query={}):
        """Fetches all entries referencing the asset

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/search-parameters/links-to-asset
        :param client Client instance
        :param query: (optional) Dict with API options.
        :return: List of :class:`Entry <contentful.entry.Entry>` objects.
        :rtype: List of contentful.entry.Entry

        Usage:
            >>> entries = asset.incoming_references(client)
            [<Entry[cat] id='happycat'>]
        """

        if client is None:
            return False

        query.update({'links_to_asset': self.id})
        return client.entries(query)

    def __repr__(self):
        return "<Asset id='{0}' url='{1}'>".format(
            self.sys.get('id', ''),
            self.url()
        )
