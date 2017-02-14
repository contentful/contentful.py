# Classes imported here are meant to be used via globals() on build
from .array import Array  # noqa: F401
from .entry import Entry  # noqa: F401
from .asset import Asset  # noqa: F401
from .space import Space  # noqa: F401
from .content_type import ContentType  # noqa: F401
from .deleted_asset import DeletedAsset  # noqa: F401
from .deleted_entry import DeletedEntry  # noqa: F401
from .sync_page import SyncPage


"""
contentful.resource_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the Resource Builder class.

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class ResourceBuilder(object):
    """Creates objects of the proper Resource Type"""

    def __init__(
            self,
            default_locale,
            localized,
            json,
            includes_for_single=None,
            depth=0):
        self.default_locale = default_locale
        self.localized = localized
        self.json = json
        self.includes_for_single = includes_for_single
        self.depth = depth

    def build(self):
        """Creates the objects from the JSON response"""

        if self.json['sys']['type'] == 'Array':
            if 'nextSyncUrl' in self.json:
                return SyncPage(
                    self.json,
                    default_locale=self.default_locale,
                    localized=True
                )
            return self._build_array()
        return self._build_single()

    def _build_single(self):
        includes = []
        if self.includes_for_single is not None:
            includes = self.includes_for_single
        return self._build_item(self.json, includes)

    def _build_array(self):
        includes = self._includes()
        items = [self._build_item(
            item,
            includes=includes
        ) for item in self.json['items']]
        return Array(self.json, items)

    def _build_item(self, item, includes=None):
        if includes is None:
            includes = []

        buildables = [
            'Entry',
            'Asset',
            'ContentType',
            'Space',
            'DeletedEntry',
            'DeletedAsset'
        ]
        if item['sys']['type'] in buildables:
            return globals()[item['sys']['type']](
                item,
                default_locale=self.default_locale,
                localized=self.localized,
                includes=includes,
                depth=self.depth
            )

    def _includes(self):
        includes = list(self.json['items'])
        for e in ['Entry', 'Asset']:
            if e in self.json.get('includes', {}):
                includes += self.json['includes'].get(e, [])
        return includes
