# flake8: noqa
from importlib import metadata

from .client import Client, AsyncClient
from .entry import Entry
from .asset import Asset
from .space import Space
from .locale import Locale
from .resource import Link
from .content_type import ContentType
from .deleted_asset import DeletedAsset
from .deleted_entry import DeletedEntry
from .content_type_cache import ContentTypeCache
from .content_type_field import ContentTypeField

__all__ = (
    "Client",
    "AsyncClient",
    "Entry",
    "Asset",
    "Space",
    "Locale",
    "Link",
    "ContentType",
    "DeletedAsset",
    "DeletedEntry",
    "ContentTypeCache",
    "ContentTypeField",
)

_metadata = metadata.metadata(__package__)

__version__ = _metadata.get("version")
__author__ = _metadata.get("author")
__email__ = _metadata.get("author-email")
