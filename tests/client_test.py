# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import vcr
from unittest import TestCase
from contentful.client import Client
from contentful.content_type_cache import ContentTypeCache


class ClientTest(TestCase):
    def setUp(self):
        ContentTypeCache.__CACHE__ = []

    @vcr.use_cassette('fixtures/client/content_type_cache.yaml')
    def test_client_creates_a_content_type_cache(self):
        Client('cfexampleapi', 'b4c0n73n7fu1')

        self.assertTrue(len(ContentTypeCache.__CACHE__) > 0)

    def test_client_can_avoid_caching_content_types(self):
        Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        self.assertFalse(len(ContentTypeCache.__CACHE__) > 0)

    @vcr.use_cassette('fixtures/client/space.yaml')
    def test_client_get_space(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        space = client.space()

        self.assertEqual(str(space), "<Space[Contentful Example API] id='cfexampleapi'>")

    @vcr.use_cassette('fixtures/client/content_type.yaml')
    def test_client_get_content_type(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        ct = client.content_type('cat')

        self.assertEqual(str(ct), "<ContentType[Cat] id='cat'>")

    @vcr.use_cassette('fixtures/client/content_types.yaml')
    def test_client_get_content_types(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        cts = client.content_types()

        self.assertEqual(str(cts[0]), "<ContentType[City] id='1t9IbcfdCk6m04uISSsaIK'>")

    @vcr.use_cassette('fixtures/client/entry.yaml')
    def test_client_entry(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entry = client.entry('nyancat')

        self.assertEqual(str(entry), "<Entry[cat] id='nyancat'>")
        self.assertEqual(str(entry.best_friend), "<Entry[cat] id='happycat'>")

    @vcr.use_cassette('fixtures/client/entries.yaml')
    def test_client_entries(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entries = client.entries()

        self.assertEqual(str(entries[0]), "<Entry[cat] id='happycat'>")

    @vcr.use_cassette('fixtures/client/entries_select.yaml')
    def test_client_entries_select(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entries = client.entries({'content_type': 'cat', 'sys.id': 'nyancat', 'select': ['fields.name']})

        self.assertEqual(str(entries[0]), "<Entry[cat] id='nyancat'>")
        self.assertEqual(entries[0].fields(), {'name': 'Nyan Cat'})

    @vcr.use_cassette('fixtures/client/asset.yaml')
    def test_client_asset(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        asset = client.asset('nyancat')

        self.assertEqual(str(asset), "<Asset id='nyancat' url='//images.contentful.com/cfexampleapi/4gp6taAwW4CmSgumq2ekUm/9da0cd1936871b8d72343e895a00d611/Nyan_cat_250px_frame.png'>")

    @vcr.use_cassette('fixtures/client/assets.yaml')
    def test_client_assets(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        assets = client.assets()

        self.assertEqual(str(assets[0]), "<Asset id='1x0xpXu4pSGS4OukSyWGUK' url='//images.contentful.com/cfexampleapi/1x0xpXu4pSGS4OukSyWGUK/cc1239c6385428ef26f4180190532818/doge.jpg'>")

    @vcr.use_cassette('fixtures/client/sync.yaml')
    def test_client_sync(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        sync = client.sync({'initial': True})

        self.assertEqual(str(sync), "<SyncPage next_sync_token='w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-wo7CnDjChMKKGsK1wrzCrBzCqMOpZAwOOcOvCcOAwqHDv0XCiMKaOcOxZA8BJUzDr8K-wo1lNx7DnHE'>")
        self.assertEqual(str(sync.items[0]), "<Entry[1t9IbcfdCk6m04uISSsaIK] id='5ETMRzkl9KM4omyMwKAOki'>")

    @vcr.use_cassette('fixtures/client/array_endpoints.yaml')
    def test_client_creates_wrapped_arrays(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        self.assertEquals(str(client.content_types()), "<Array size='4' total='4' limit='100' skip='0'>")
        self.assertEquals(str(client.entries()), "<Array size='10' total='10' limit='100' skip='0'>")
        self.assertEquals(str(client.assets()), "<Array size='4' total='4' limit='100' skip='0'>")

    # Integration Tests

    @vcr.use_cassette('fixtures/integration/issue-4.yaml')
    def test_entries_dont_fail_with_unicode_characters(self):
        client = Client('wltm0euukdog', 'bbe871957bb60f988af6cbeeccbb178c36cae09e36e8098357e27b51dd38d88e', content_type_cache=True)
        entries = client.entries()
        self.assertEqual(entries[0].name, '😅')
