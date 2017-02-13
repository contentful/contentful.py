"""
contentful.array
~~~~~~~~~~~~~~~~

This module implements the Array class.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/introduction/collection-resources-and-pagination

:copyright: (c) 2017 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class Array(object):
    """
    API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/introduction/collection-resources-and-pagination
    """

    def __init__(self, json, items):
        self.items = items
        self.skip = json.get('skip', 0)
        self.limit = json.get('limit', 100)
        self.total = json.get('total', 0)

    def __iter__(self):
        for item in self.items:
            yield item

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return "<Array size='{0}' total='{1}' limit='{2}' skip='{3}'>".format(
            len(self),
            self.total,
            self.limit,
            self.skip
        )
