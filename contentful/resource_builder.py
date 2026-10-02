from .array import Array
from .asset_key import AssetKey
from .entry import Entry
from .asset import Asset
from .space import Space
from .content_type import ContentType
from .deleted_asset import DeletedAsset
from .deleted_entry import DeletedEntry
from .locale import Locale
from .sync_page import SyncPage
from .utils import unresolvable, build_includes_index, build_error_ids_set
from .taxonomy_concept import TaxonomyConcept
from .taxonomy_concept_scheme import TaxonomyConceptScheme


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
            max_depth=20,
            includes_index=None,
            error_ids=None):
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

        # Cached values for performance optimization
        self._cached_errors = None
        self._cached_error_ids = error_ids
        self._cached_includes = None
        self._cached_includes_index = includes_index

    def build(self):
        """Creates the objects from the JSON response"""
        if 'policy' in self.json and 'secret' in self.json:
            return self._build_asset_key()
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

        # Use cached indexes if available, otherwise build them
        includes_index = self._cached_includes_index
        if includes_index is None and includes:
            includes_index = build_includes_index(includes)

        error_ids = self._cached_error_ids
        if error_ids is None and errors:
            error_ids = build_error_ids_set(errors)

        return self._build_item(
            self.json,
            includes=includes,
            errors=errors,
            includes_index=includes_index,
            error_ids=error_ids
        )

    def _build_array(self):
        errors = self._errors()
        error_ids = self._error_ids()
        includes = self._includes(error_ids)
        includes_index = self._includes_index(includes)

        items = [self._build_item(
                    item,
                    includes=includes,
                    errors=errors,
                    includes_index=includes_index,
                    error_ids=error_ids
                 ) for item in self.json['items']
                 if not unresolvable(item, errors, error_ids=error_ids)]

        return Array(self.json, items)

    def _build_item(self, item, includes=None, errors=None, includes_index=None, error_ids=None):
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
            'Locale': Locale,
            'TaxonomyConcept': TaxonomyConcept,
            'TaxonomyConceptScheme': TaxonomyConceptScheme
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
                max_depth=self.max_depth,
                includes_index=includes_index,
                error_ids=error_ids
            )

    def _resource_from_cache(self, item):
        cache_key = "{0}:{1}:{2}".format(
            item['sys']['type'],
            item['sys']['id'],
            item['sys'].get('locale', '*')
        )
        if self.resources and cache_key in self.resources:
            return self.resources[cache_key]

    def _includes(self, error_ids=None):
        if self._cached_includes is not None:
            return self._cached_includes

        includes = list(self.json['items'])
        errors = self._errors()
        if error_ids is None:
            error_ids = self._error_ids()

        for e in ['Entry', 'Asset']:
            if e in self.json.get('includes', {}):
                includes += [item for item in self.json['includes'].get(e, [])
                             if not unresolvable(item, errors, error_ids=error_ids)]

        self._cached_includes = includes
        return includes

    def _errors(self):
        if self._cached_errors is not None:
            return self._cached_errors

        errors = []
        if self.errors_for_single is not None:
            errors = list(self.errors_for_single)
        errors = errors + self.json.get('errors', [])

        self._cached_errors = errors
        return errors

    def _error_ids(self):
        if self._cached_error_ids is not None:
            return self._cached_error_ids

        self._cached_error_ids = build_error_ids_set(self._errors())
        return self._cached_error_ids

    def _includes_index(self, includes=None):
        if self._cached_includes_index is not None:
            return self._cached_includes_index

        if includes is None:
            includes = self._includes()

        self._cached_includes_index = build_includes_index(includes)
        return self._cached_includes_index

    def _build_asset_key(self):
        """Creates an AssetKey Resource."""

        return AssetKey(
            self.json,
            default_locale=self.default_locale
        )
