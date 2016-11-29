from re import sub
from .resource import Resource


"""
contentful.sync_page
~~~~~~~~~~~~~~~~~~~~

This module implements the SyncPage class.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/synchronization

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class SyncPage(Resource):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/synchronization
    """

    def __init__(
            self,
            item,
            default_locale='en-US',
            includes=None,
            localized=True,
            depth=0):
        super(SyncPage, self).__init__(
            item,
            default_locale,
            includes,
            localized,
            depth
        )

        self.next_sync_url = item.get('nextSyncUrl', '')
        self.next_sync_token = self._get_sync_token()
        self.items = self._hydrate_items()

    def next(self, client):
        """Fetches next SyncPage

        :param client: CDA Client.
        :return: :class:`SyncPage <SyncPage>`
        :rtype: contentful.sync_page.SyncPage
        """

        return client.sync({'sync_token': self.next_sync_token})

    def _get_sync_token(self):
        return sub(r'.*sync_token=', '', self.next_sync_url)

    def _hydrate_items(self):
        from .resource_builder import ResourceBuilder
        items = []
        for item in self.raw.get('items', []):
            items.append(
                ResourceBuilder(
                    self.default_locale,
                    True,
                    item
                ).build()
            )

        return items

    def __repr__(self):
        return "<SyncPage next_sync_token='{0}'>".format(
            self.next_sync_token
        )
