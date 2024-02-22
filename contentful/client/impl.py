from __future__ import annotations

from typing import TYPE_CHECKING

from contentful.client import base
from contentful.client.transport import aio, sio, errors

if TYPE_CHECKING:
    from contentful import (
        Asset,
        ContentType,
        Entry,
        Locale,
        Space,
    )
    from contentful.sync_page import SyncPage
    from contentful.client.base import QueryT

"""
contentful.client.impl
~~~~~~~~~~~~~~~~~~~~~~

This module implements the Contentful Delivery API Client,
allowing interaction with every method present in it.

Complete API Documentation: https://www.contentful.com/developers/docs/references/content-delivery-api/

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""

__all__ = ("Client", "AsyncClient")


class Client(base.BaseClient):
    transport_cls = sio.SyncTransport

    def space(self, query: QueryT | None = None) -> Space:
        """Fetches the current Space.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/spaces/get-a-space

        :param query: (optional) Dict with API options.
        :return: :class:`Space <contentful.space.Space>` object.
        :rtype: contentful.space.Space

        Usage:

            >>> space = client.space()
            <Space[Contentful Example API] id='cfexampleapi'>
        """

        return self._get("", query)

    def content_type(
        self, content_type_id: str, query: QueryT | None = None
    ) -> ContentType:
        """Fetches a Content Type by ID.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-types/content-type/get-a-single-content-type

        :param content_type_id: The ID of the target Content Type.
        :param query: (optional) Dict with API options.
        :return: :class:`ContentType <contentful.content_type.ContentType>` object.
        :rtype: contentful.content_type.ContentType

        Usage:
            >>> cat_content_type = client.content_type('cat')
            <ContentType[Cat] id='cat'>
        """

        return self._get(f"content_types/{content_type_id}", query)

    def content_types(self, query: QueryT | None = None) -> list[ContentType]:
        """Fetches all Content Types from the Space.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-types/content-model/get-the-content-model-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`ContentType <contentful.content_type.ContentType>` objects.
        :rtype: List of contentful.content_type.ContentType

        Usage:
            >>> content_types = client.content_types()
            [<ContentType[City] id='1t9IbcfdCk6m04uISSsaIK'>,
             <ContentType[Human] id='human'>,
             <ContentType[Dog] id='dog'>,
             <ContentType[Cat] id='cat'>]
        """

        return self._get("content_types", query)

    def entry(self, entry_id: str, query: QueryT | None = None) -> Entry:
        """Fetches an Entry by ID.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/entries/entry/get-a-single-entry

        :param entry_id: The ID of the target Entry.
        :param query: (optional) Dict with API options.
        :return: :class:`Entry <contentful.entry.Entry>` object.
        :rtype: contentful.entry.Entry

        Usage:
            >>> nyancat_entry = client.entry('nyancat')
            <Entry[cat] id='nyancat'>
        """
        if query is None:
            query = {}

        query = {**query, "sys.id": entry_id}
        response = self._get("entries", query)
        if self.raw_mode:
            return response
        return self._entry_callback(response, entry_id=entry_id)

    @staticmethod
    def _entry_callback(entries: list[Entry], *, entry_id: str) -> Entry:
        if not entries:
            raise errors.EntryNotFoundError(f"Entry not found for ID: {entry_id!r}")
        return entries[0]

    def entries(self, query: QueryT | None = None) -> list[Entry]:
        """Fetches all Entries from the Space (up to the set limit, can be modified in `query`).

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/entries/entries-collection/get-all-entries-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`Entry <contentful.entry.Entry>` objects.
        :rtype: List of contentful.entry.Entry

        Usage:
            >>> entries = client.entries()
            [<Entry[cat] id='happycat'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='5ETMRzkl9KM4omyMwKAOki'>,
             <Entry[dog] id='6KntaYXaHSyIw8M6eo26OK'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='7qVBlCjpWE86Oseo40gAEY'>,
             <Entry[cat] id='garfield'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='4MU1s3potiUEM2G4okYOqw'>,
             <Entry[cat] id='nyancat'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='ge1xHyH3QOWucKWCCAgIG'>,
             <Entry[human] id='finn'>,
             <Entry[dog] id='jake'>]
        """
        return self._get("entries", query)

    def asset(self, asset_id: str, query: QueryT | None = None) -> Asset:
        """Fetches an Asset by ID.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/assets/asset/get-a-single-asset

        :param asset_id: The ID of the target Asset.
        :param query: (optional) Dict with API options.
        :return: :class:`Asset <Asset>` object.
        :rtype: contentful.asset.Asset

        Usage:
            >>> nyancat_asset = client.asset('nyancat')
            <Asset id='nyancat' url='//images.contentful.com/cfex...'>
        """
        return self._get(f"assets/{asset_id}", query)

    def assets(self, query: QueryT | None = None) -> list[Asset]:
        """Fetches all Assets from the Space (up to the set limit, can be modified in `query`).

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/assets/assets-collection/get-all-assets-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`Asset <contentful.asset.Asset>` objects.
        :rtype: List of contentful.asset.Asset

        Usage:
            >>> assets = client.assets()
            [<Asset id='1x0xpXu4pSGS4OukSyWGUK' url='//images.content...'>,
             <Asset id='happycat' url='//images.contentful.com/cfexam...'>,
             <Asset id='nyancat' url='//images.contentful.com/cfexamp...'>,
             <Asset id='jake' url='//images.contentful.com/cfexamplea...'>]
        """
        return self._get("assets", query)

    def locales(self, query: QueryT | None = None) -> list[Locale]:
        """Fetches all Locales from the Environment (up to the set limit, can be modified in `query`).

        # TODO: fix url
        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/assets/assets-collection/get-all-assets-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`Locale <contentful.locale.Locale>` objects.
        :rtype: List of contentful.locale.Locale

        Usage:
            >>> locales = client.locales()
            [<Locale[English (United States)] code='en-US' default=True fallback_code=None optional=False>]
        """

        return self._get("locales", query)

    def sync(self, query: QueryT | None = None) -> SyncPage:
        """Fetches content from the Sync API.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/synchronization/initial-synchronization/query-entries

        :param query: (optional) Dict with API options.
        :return: :class:`SyncPage <contentful.sync_page.SyncPage>` object.
        :rtype: contentful.sync_page.SyncPage

        Usage:
            >>> sync_page = client.sync({'initial': True})
            <SyncPage next_sync_token='w5ZGw6JFwqZmVcKsE8Kow4grw45QdybC...'>
        """
        return self._get("sync", query)

    def initialize(self):
        self.transport.initialize()
        if self.content_type_cache:
            self._cache_content_types()

    def _cache_content_types(self): ...

    def _get(self, url: str, query: QueryT | None = None):
        params = self._format_params(query)
        response = self.transport.get(url, params=params, raw_mode=self.raw_mode)
        if self.raw_mode:
            return response
        return self._format_response(response)


class AsyncClient(base.BaseClient):
    transport_cls = aio.AsyncTransport

    async def initialize(self):
        await self.transport.initialize()
        if self.content_type_cache:
            await self._cache_content_types()

    async def _cache_content_types(self): ...

    async def _get(self, url: str, query: QueryT | None = None):
        params = self._format_params(query)
        response = await self.transport.get(url, params=params, raw_mode=self.raw_mode)
        if self.raw_mode:
            return response
        return self._format_response(response)

    async def space(self, query: QueryT | None = None) -> Space:
        """Fetches the current Space.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/spaces/get-a-space

        :param query: (optional) Dict with API options.
        :return: :class:`Space <contentful.space.Space>` object.
        :rtype: contentful.space.Space

        Usage:

            >>> space = await client.space()
            <Space[Contentful Example API] id='cfexampleapi'>
        """

        return await self._get("", query)

    async def content_type(
        self, content_type_id: str, query: QueryT | None = None
    ) -> ContentType:
        """Fetches a Content Type by ID.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-types/content-type/get-a-single-content-type

        :param content_type_id: The ID of the target Content Type.
        :param query: (optional) Dict with API options.
        :return: :class:`ContentType <contentful.content_type.ContentType>` object.
        :rtype: contentful.content_type.ContentType

        Usage:
            >>> cat_content_type = await client.content_type('cat')
            <ContentType[Cat] id='cat'>
        """

        return await self._get(f"content_types/{content_type_id}", query)

    async def content_types(self, query: QueryT | None = None) -> list[ContentType]:
        """Fetches all Content Types from the Space.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-types/content-model/get-the-content-model-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`ContentType <contentful.content_type.ContentType>` objects.
        :rtype: List of contentful.content_type.ContentType

        Usage:
            >>> content_types = await client.content_types()
            [<ContentType[City] id='1t9IbcfdCk6m04uISSsaIK'>,
             <ContentType[Human] id='human'>,
             <ContentType[Dog] id='dog'>,
             <ContentType[Cat] id='cat'>]
        """

        return await self._get("content_types", query)

    async def entry(self, entry_id: str, query: QueryT | None = None) -> Entry:
        """Fetches an Entry by ID.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/entries/entry/get-a-single-entry

        :param entry_id: The ID of the target Entry.
        :param query: (optional) Dict with API options.
        :return: :class:`Entry <contentful.entry.Entry>` object.
        :rtype: contentful.entry.Entry

        Usage:
            >>> nyancat_entry = await client.entry('nyancat')
            <Entry[cat] id='nyancat'>
        """
        if query is None:
            query = {}

        query = {**query, "sys.id": entry_id}
        response = await self._get("entries", query)
        if self.raw_mode:
            return response
        return self._entry_callback(response, entry_id=entry_id)

    @staticmethod
    def _entry_callback(entries: list[Entry], *, entry_id: str) -> Entry:
        if not entries:
            raise errors.EntryNotFoundError(f"Entry not found for ID: {entry_id!r}")
        return entries[0]

    async def entries(self, query: QueryT | None = None) -> list[Entry]:
        """Fetches all Entries from the Space (up to the set limit, can be modified in `query`).

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/entries/entries-collection/get-all-entries-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`Entry <contentful.entry.Entry>` objects.
        :rtype: List of contentful.entry.Entry

        Usage:
            >>> entries = await client.entries()
            [<Entry[cat] id='happycat'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='5ETMRzkl9KM4omyMwKAOki'>,
             <Entry[dog] id='6KntaYXaHSyIw8M6eo26OK'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='7qVBlCjpWE86Oseo40gAEY'>,
             <Entry[cat] id='garfield'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='4MU1s3potiUEM2G4okYOqw'>,
             <Entry[cat] id='nyancat'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='ge1xHyH3QOWucKWCCAgIG'>,
             <Entry[human] id='finn'>,
             <Entry[dog] id='jake'>]
        """
        return await self._get("entries", query)

    async def asset(self, asset_id: str, query: QueryT | None = None) -> Asset:
        """Fetches an Asset by ID.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/assets/asset/get-a-single-asset

        :param asset_id: The ID of the target Asset.
        :param query: (optional) Dict with API options.
        :return: :class:`Asset <Asset>` object.
        :rtype: contentful.asset.Asset

        Usage:
            >>> nyancat_asset = await client.asset('nyancat')
            <Asset id='nyancat' url='//images.contentful.com/cfex...'>
        """
        return await self._get(f"assets/{asset_id}", query)

    async def assets(self, query: QueryT | None = None) -> list[Asset]:
        """Fetches all Assets from the Space (up to the set limit, can be modified in `query`).

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/assets/assets-collection/get-all-assets-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`Asset <contentful.asset.Asset>` objects.
        :rtype: List of contentful.asset.Asset

        Usage:
            >>> assets = await client.assets()
            [<Asset id='1x0xpXu4pSGS4OukSyWGUK' url='//images.content...'>,
             <Asset id='happycat' url='//images.contentful.com/cfexam...'>,
             <Asset id='nyancat' url='//images.contentful.com/cfexamp...'>,
             <Asset id='jake' url='//images.contentful.com/cfexamplea...'>]
        """
        return await self._get("assets", query)

    async def locales(self, query: QueryT | None = None) -> list[Locale]:
        """Fetches all Locales from the Environment (up to the set limit, can be modified in `query`).

        # TODO: fix url
        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/assets/assets-collection/get-all-assets-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`Locale <contentful.locale.Locale>` objects.
        :rtype: List of contentful.locale.Locale

        Usage:
            >>> locales = await client.locales()
            [<Locale[English (United States)] code='en-US' default=True fallback_code=None optional=False>]
        """

        return await self._get("locales", query)

    async def sync(self, query: QueryT | None = None) -> SyncPage:
        """Fetches content from the Sync API.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/synchronization/initial-synchronization/query-entries

        :param query: (optional) Dict with API options.
        :return: :class:`SyncPage <contentful.sync_page.SyncPage>` object.
        :rtype: contentful.sync_page.SyncPage

        Usage:
            >>> sync_page = await client.sync({'initial': True})
            <SyncPage next_sync_token='w5ZGw6JFwqZmVcKsE8Kow4grw45QdybC...'>
        """
        return await self._get("sync", query)
