# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import asyncio
import inspect
import time

import requests_mock
import vcr
from unittest import TestCase

from requests_mock import ANY

from contentful.async_client import AsyncClient, ASYNC_METHODS
from contentful.client import Client
from contentful.content_type import ContentType
from contentful.content_type_cache import ContentTypeCache


class AsyncClientTest(TestCase):
    def setUp(self):
        ContentTypeCache.__CACHE__ = {}

    def test_async_client_repr(self):
        self.assertEqual(
            '<contentful.AsyncClient space_id="cfexampleapi" access_token="b4c0n73n7fu1" default_locale="en-US">',
            str(AsyncClient('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False))
        )

    @vcr.use_cassette('fixtures/client/entry.yaml', decode_compressed_response=True)
    def test_async_client_entry(self):
        client = AsyncClient('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entry = asyncio.run(client.entry('nyancat'))

        self.assertEqual(str(entry), "<Entry[cat] id='nyancat'>")
        self.assertEqual(str(entry.best_friend), "<Entry[cat] id='happycat'>")

    @vcr.use_cassette('fixtures/client/entries.yaml', decode_compressed_response=True)
    def test_async_client_entries(self):
        client = AsyncClient('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entries = asyncio.run(client.entries())

        self.assertTrue(len(entries) > 0)

    @vcr.use_cassette('fixtures/client/content_type_cache.yaml', decode_compressed_response=True, allow_playback_repeats=True)
    def test_async_client_caches_content_types_with_default_options(self):
        client = AsyncClient('cfexampleapi', 'b4c0n73n7fu1')
        asyncio.run(client.content_types())

        cached = ContentTypeCache.__CACHE__['cfexampleapi']
        self.assertTrue(len(cached) > 0)
        for content_type in cached:
            self.assertIsInstance(content_type, ContentType)

    def test_async_client_reports_requested_content_type_cache_setting(self):
        self.assertTrue(AsyncClient('cfexampleapi', 'b4c0n73n7fu1').content_type_cache)
        self.assertFalse(
            AsyncClient('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False).content_type_cache
        )

    def test_async_client_does_not_perform_io_on_construction(self):
        with requests_mock.mock() as m:
            m.register_uri('GET', ANY, status_code=200, json={'items': []})
            AsyncClient('cfexampleapi', 'b4c0n73n7fu1')

            self.assertEqual(m.call_count, 0)

    @vcr.use_cassette('fixtures/client/entry.yaml', decode_compressed_response=True)
    def test_async_client_does_not_poison_cache_for_sync_client(self):
        AsyncClient('cfexampleapi', 'b4c0n73n7fu1')

        sync_client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entry = sync_client.entry('nyancat')

        self.assertEqual(str(entry), "<Entry[cat] id='nyancat'>")

    def test_async_client_runs_requests_concurrently(self):
        client = AsyncClient('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        def slow_entries(query=None):
            time.sleep(0.2)
            return []

        client.sync_client.entries = slow_entries

        async def fetch_many():
            return await asyncio.gather(*[client.entries() for _ in range(4)])

        started = time.perf_counter()
        results = asyncio.run(fetch_many())
        elapsed = time.perf_counter() - started

        self.assertEqual(len(results), 4)
        self.assertLess(elapsed, 0.5, "calls serialized instead of running concurrently")

    @vcr.use_cassette('fixtures/client/entry_incoming_references.yaml', decode_compressed_response=True)
    def test_async_client_supports_incoming_references_through_sync_client(self):
        client = AsyncClient('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        async def fetch_references():
            entry = await client.entry('nyancat')
            return await asyncio.to_thread(entry.incoming_references, client.sync_client)

        entries = asyncio.run(fetch_references())

        self.assertEqual(len(entries), 1)
        self.assertEqual(str(entries[0]), "<Entry[cat] id='happycat'>")

    def test_async_client_exposes_sync_client(self):
        client = AsyncClient('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        self.assertIsInstance(client.sync_client, Client)
        self.assertEqual(client.space_id, 'cfexampleapi')

    def test_async_client_forwards_attribute_writes(self):
        client = AsyncClient('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        client.timeout_s = 5

        self.assertEqual(client.sync_client.timeout_s, 5)

    def test_async_methods_are_coroutines(self):
        client = AsyncClient('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        for name in ASYNC_METHODS:
            self.assertTrue(
                inspect.iscoroutinefunction(getattr(client, name)),
                "{0} is not a coroutine function".format(name)
            )

    def test_async_methods_cover_every_networked_client_method(self):
        networked = set()
        for name, method in inspect.getmembers(Client, predicate=inspect.isfunction):
            if name.startswith('_'):
                continue
            source = inspect.getsource(method)
            if 'self._get(' in source or 'self._post(' in source:
                networked.add(name)

        self.assertEqual(networked, set(ASYNC_METHODS))

    def test_async_methods_preserve_signatures(self):
        self.assertEqual(
            inspect.signature(Client.entry),
            inspect.signature(AsyncClient.entry)
        )
