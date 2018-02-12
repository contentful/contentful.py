# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import vcr
import re
from unittest import TestCase
from contentful.client import Client
from contentful.content_type_cache import ContentTypeCache
from contentful.errors import EntryNotFoundError
from contentful.utils import ConfigurationException


class ClientTest(TestCase):
    def setUp(self):
        ContentTypeCache.__CACHE__ = []

    def test_client_repr(self):
        self.assertEqual(
            '<contentful.Client space_id="cfexampleapi" access_token="b4c0n73n7fu1" default_locale="en-US">',
            str(Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False))
        )

    def test_client_validations(self):
        with self.assertRaises(ConfigurationException):
            Client(None, 'foo')
        with self.assertRaises(ConfigurationException):
            Client('foo', None)
        with self.assertRaises(ConfigurationException):
            Client('foo', 'bar', api_url=None)
        with self.assertRaises(ConfigurationException):
            Client('foo', 'bar', default_locale=None)
        with self.assertRaises(ConfigurationException):
            Client('foo', 'bar', api_version=None)

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

    @vcr.use_cassette('fixtures/client/entry_not_found.yaml')
    def test_client_entry_not_found(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        self.assertRaises(EntryNotFoundError, client.entry, 'foobar')

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

    @vcr.use_cassette('fixtures/client/entries_links_to_entry.yaml')
    def test_client_entries_links_to_entry(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entries = client.entries({'links_to_entry': 'nyancat'})
        self.assertEqual(len(entries), 1)
        self.assertEqual(str(entries[0]), "<Entry[cat] id='happycat'>")

    @vcr.use_cassette('fixtures/client/entry_incoming_references.yaml')
    def test_entry_incoming_references(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entry = client.entry('nyancat')
        entries = entry.incoming_references(client)
        self.assertEqual(len(entries), 1)
        self.assertEqual(str(entries[0]), "<Entry[cat] id='happycat'>")

    @vcr.use_cassette('fixtures/client/entry_incoming_references_with_query.yaml')
    def test_entry_incoming_references_with_query(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entry = client.entry('nyancat')
        entries = entry.incoming_references(client, { 'content_type': 'cat', 'select': ['fields.name'] })
        self.assertEqual(len(entries), 1)
        self.assertEqual(str(entries[0]), "<Entry[cat] id='happycat'>")
        self.assertEqual(entries[0].fields(), {'name': 'Happy Cat'})

    @vcr.use_cassette('fixtures/client/entries_links_to_asset.yaml')
    def test_client_entries_links_to_asset(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        entries = client.entries({'links_to_asset': 'nyancat'})
        self.assertEqual(len(entries), 1)
        self.assertEqual(str(entries[0]), "<Entry[cat] id='nyancat'>")

    @vcr.use_cassette('fixtures/client/asset_incoming_references.yaml')
    def test_asset_incoming_references(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)
        asset = client.asset('nyancat')
        entries = asset.incoming_references(client)
        self.assertEqual(len(entries), 1)
        self.assertEqual(str(entries[0]), "<Entry[cat] id='nyancat'>")

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
        self.assertEqual(str(client.content_types()), "<Array size='4' total='4' limit='100' skip='0'>")
        self.assertEqual(str(client.entries()), "<Array size='10' total='10' limit='100' skip='0'>")
        self.assertEqual(str(client.assets()), "<Array size='4' total='4' limit='100' skip='0'>")

    # X-Contentful-User-Agent Headers

    def test_client_default_contentful_user_agent_headers(self):
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        from contentful import __version__
        import platform
        expected = [
            'sdk contentful.py/{0};'.format(__version__),
            'platform python/{0};'.format(platform.python_version())
        ]
        header = client._contentful_user_agent()
        for e in expected:
            self.assertTrue(e in header)

        self.assertTrue(re.search('os (Windows|macOS|Linux)(\/.*)?;', header))

        self.assertTrue('integration' not in header)
        self.assertTrue('app' not in header)

    def test_client_with_integration_name_only_headers(self):
        client = Client(
            'cfexampleapi',
            'b4c0n73n7fu1',
            content_type_cache=False,
            integration_name='foobar')

        header = client._contentful_user_agent()
        self.assertTrue('integration foobar;' in header)
        self.assertFalse('integration foobar/;' in header)

    def test_client_with_integration_headers(self):
        client = Client(
            'cfexampleapi',
            'b4c0n73n7fu1',
            content_type_cache=False,
            integration_name='foobar',
            integration_version='0.1.0')

        header = client._contentful_user_agent()
        self.assertTrue('integration foobar/0.1.0;' in header)

    def test_client_with_application_name_only_headers(self):
        client = Client(
            'cfexampleapi',
            'b4c0n73n7fu1',
            content_type_cache=False,
            application_name='foobar')

        header = client._contentful_user_agent()
        self.assertTrue('app foobar;' in header)
        self.assertFalse('app foobar/;' in header)

    def test_client_with_application_headers(self):
        client = Client(
            'cfexampleapi',
            'b4c0n73n7fu1',
            content_type_cache=False,
            application_name='foobar',
            application_version='0.1.0')

        header = client._contentful_user_agent()
        self.assertTrue('app foobar/0.1.0;' in header)

    def test_client_with_integration_version_only_does_not_include_integration_in_header(self):
        client = Client(
            'cfexampleapi',
            'b4c0n73n7fu1',
            content_type_cache=False,
            integration_version='0.1.0')

        header = client._contentful_user_agent()
        self.assertFalse('integration /0.1.0' in header)

    def test_client_with_application_version_only_does_not_include_integration_in_header(self):
        client = Client(
            'cfexampleapi',
            'b4c0n73n7fu1',
            content_type_cache=False,
            application_version='0.1.0')

        header = client._contentful_user_agent()
        self.assertFalse('app /0.1.0;' in header)

    def test_client_with_all_headers(self):
        client = Client(
            'cfexampleapi',
            'b4c0n73n7fu1',
            content_type_cache=False,
            application_name='foobar_app',
            application_version='1.1.0',
            integration_name='foobar integ',
            integration_version='0.1.0')

        from contentful import __version__
        import platform
        expected = [
            'sdk contentful.py/{0};'.format(__version__),
            'platform python/{0};'.format(platform.python_version()),
            'app foobar_app/1.1.0;',
            'integration foobar integ/0.1.0;'
        ]
        header = client._contentful_user_agent()
        for e in expected:
            self.assertTrue(e in header)

        self.assertTrue(re.search('os (Windows|macOS|Linux)(\/.*)?;', header))

    def test_client_headers(self):
        client = Client(
            'cfexampleapi',
            'b4c0n73n7fu1',
            content_type_cache=False,
            application_name='foobar_app',
            application_version='1.1.0',
            integration_name='foobar integ',
            integration_version='0.1.0')

        from contentful import __version__
        import platform
        expected = [
            'sdk contentful.py/{0};'.format(__version__),
            'platform python/{0};'.format(platform.python_version()),
            'app foobar_app/1.1.0;',
            'integration foobar integ/0.1.0;'
        ]
        header = client._request_headers()['X-Contentful-User-Agent']
        for e in expected:
            self.assertTrue(e in header)

        self.assertTrue(re.search('os (Windows|macOS|Linux)(\/.*)?;', header))

    # Integration Tests

    @vcr.use_cassette('fixtures/integration/issue-4.yaml')
    def test_entries_dont_fail_with_unicode_characters(self):
        client = Client('wltm0euukdog', 'bbe871957bb60f988af6cbeeccbb178c36cae09e36e8098357e27b51dd38d88e', content_type_cache=True)
        entries = client.entries()
        self.assertEqual(entries[0].name, '😅')

    @vcr.use_cassette('fixtures/integration/json-arrays.yaml')
    def test_entries_dont_fail_with_arrays_as_json_root(self):
        client = Client('4int1zgmkwcf', 'd2ac2076019bd4a8357811cbdd5563bb7186d90d77e53c265a1bafd9f83439e8', content_type_cache=True)
        entries = client.entries()
        self.assertEqual(entries[0].json, [{'foo': 'bar'}, {'baz': 'qux'}])

    @vcr.use_cassette('fixtures/integration/issue-11.yaml')
    def test_entries_with_none_values_on_all_fields(self):
        client = Client('rtx5c7z0zbas', 'a6c8dc438d470c51d1094dad146a1f20fcdba41e21f4e263af6c3f70d8583634', content_type_cache=True)
        entry = client.entries()[0]
        self.assertEqual(entry.symbol, None)
        self.assertEqual(entry.text, None)
        self.assertEqual(entry.integer, None)
        self.assertEqual(entry.number, None)
        self.assertEqual(entry.date, None)
        self.assertEqual(entry.location, None)
        self.assertEqual(entry.asset, None)
        self.assertEqual(entry.bool, None)
        self.assertEqual(entry.json, None)
        self.assertEqual(entry.link, None)

    @vcr.use_cassette('fixtures/integration/circular-references.yaml')
    def test_circular_references_default_depth(self):
        client = Client('rk19fq93y3vw', '821aa502a7ce820e46adb30fa6942889619aac4342a7021cfe15197c52a593cc', content_type_cache=True)
        a = client.entry('6kdfS7uMs8owuEIoSaOcQk')
        self.assertEqual(str(a), "<Entry[a] id='6kdfS7uMs8owuEIoSaOcQk'>")
        self.assertEqual(str(a.b), "<Entry[b] id='7oADpDPuneEAsWUiO2CmEo'>")
        self.assertEqual(str(a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a), "<Entry[a] id='6kdfS7uMs8owuEIoSaOcQk'>")
        self.assertEqual(str(a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b), "<Link[Entry] id='7oADpDPuneEAsWUiO2CmEo'>")

    @vcr.use_cassette('fixtures/integration/circular-references.yaml')
    def test_circular_references_set_depth(self):
        client = Client(
            'rk19fq93y3vw',
            '821aa502a7ce820e46adb30fa6942889619aac4342a7021cfe15197c52a593cc',
            content_type_cache=True,
            max_include_resolution_depth=1
        )
        a = client.entry('6kdfS7uMs8owuEIoSaOcQk')
        self.assertEqual(str(a), "<Entry[a] id='6kdfS7uMs8owuEIoSaOcQk'>")
        self.assertEqual(str(a.b), "<Entry[b] id='7oADpDPuneEAsWUiO2CmEo'>")
        self.assertEqual(str(a.b.a), "<Link[Entry] id='6kdfS7uMs8owuEIoSaOcQk'>")
