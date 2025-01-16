import sys
import os

from .asset_test import AssetTest
from .client_test import ClientTest
from .content_type_cache_test import ContentTypeCacheTest
from .content_type_field_types_test import BasicFieldTest, LinkFieldTest, RichTextFieldTest, SymbolFieldTest, ArrayFieldTest, ObjectFieldTest
from .content_type_field_test import ContentTypeFieldTest
from .content_type_test import ContentTypeTest
from .deleted_asset_test import DeletedAssetTest
from .deleted_entry_test import DeletedEntryTest
from .entry_test import EntryTest
from .errors_test import ErrorsTest
from .locale_test import LocaleTest
from .resource_builder_test import ResourceBuilderTest
from .resource_test import ResourceTest
from .space_test import SpaceTest
from .sync_page_test import SyncPageTest
from .utils_test import UtilsTest

sys.path.insert(0, os.path.abspath('..'))

__all__ = [
    'AssetTest',
    'ClientTest',
    'ContentTypeCacheTest',
    'BasicFieldTest',
    'LinkFieldTest',
    'RichTextFieldTest',
    'SymbolFieldTest',
    'ArrayFieldTest',
    'ObjectFieldTest',
    'ContentTypeFieldTest',
    'ContentTypeTest',
    'DeletedAssetTest',
    'DeletedEntryTest',
    'EntryTest',
    'ErrorsTest',
    'LocaleTest',
    'ResourceBuilderTest',
    'ResourceTest',
    'SpaceTest',
    'SyncPageTest',
    'UtilsTest'
]
