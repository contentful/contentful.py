from .array import Array
from .entry import Entry
from .asset import Asset
from .space import Space
from .content_type import ContentType
from .deleted_asset import DeletedAsset
from .deleted_entry import DeletedEntry
from .locale import Locale
from .sync_page import SyncPage
from .utils import unresolvable


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
            errors_for_single=None,
            reuse_entries=False,
            resources=None,
            depth=0,
            max_depth=20):
        self.default_locale = default_locale
        self.localized = localized
        self.json = json
        self.includes_for_single = includes_for_single
        self.errors_for_single = errors_for_single
        self.reuse_entries = reuse_entries
        self.depth = depth
        self.max_depth = max_depth

        if resources is None:
            resources = {} if self.reuse_entries else None
        self.resources = resources

    def build(self):
        """Creates the objects from the JSON response"""

        if self.json['sys']['type'] == 'Array':
            if any(k in self.json for k in ['nextSyncUrl', 'nextPageUrl']):
                return SyncPage(
                    self.json,
                    default_locale=self.default_locale,
                    localized=True
                )
            return self._build_array()
        return self._build_single()

    def _build_single(self):
        includes = []
        errors = []
        if self.includes_for_single is not None:
            includes = self.includes_for_single
        if self.errors_for_single is not None:
            errors = self.errors_for_single

        return self._build_item(
            self.json,
            includes=includes,
            errors=errors
        )

    def _build_array(self):
        includes = self._includes()
        errors = self._errors()

        items = [self._build_item(
                    item,
                    includes=includes,
                    errors=errors
                 ) for item in self.json['items']
                 if not unresolvable(item, self._errors())]

        return Array(self.json, items)

    def _build_item(self, item, includes=None, errors=None):
        if includes is None:
            includes = []
        if errors is None:
            errors = []

        buildables = {
            'Entry': Entry,
            'Asset': Asset,
            'ContentType': ContentType,
            'Space': Space,
            'DeletedEntry': DeletedEntry,
            'DeletedAsset': DeletedAsset,
            'Locale': Locale
        }

        resource = self._resource_from_cache(item) if self.reuse_entries else None
        if resource is not None:
            return resource

        if item['sys']['type'] in buildables:
            return buildables[item['sys']['type']](
                item,
                default_locale=self.default_locale,
                localized=self.localized,
                includes=includes,
                errors=errors,
                resources=self.resources,
                depth=self.depth,
                max_depth=self.max_depth
            )

    def _resource_from_cache(self, item):
        cache_key = "{0}:{1}:{2}".format(
            item['sys']['type'],
            item['sys']['id'],
            item['sys'].get('locale', '*')
        )
        if self.resources and cache_key in self.resources:
            return self.resources[cache_key]

    def _includes(self):
        includes = list(self.json['items'])
        for e in ['Entry', 'Asset']:
            if e in self.json.get('includes', {}):
                includes += [item for item in self.json['includes'].get(e, [])
                             if not unresolvable(item, self._errors())]
        return includes

    def _errors(self):
        errors = []
        if self.errors_for_single is not None:
            errors = self.errors_for_single
        errors += self.json.get('errors', [])

        return errors
