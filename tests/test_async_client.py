import aioresponses
import vcr
import re
from unittest import TestCase, IsolatedAsyncioTestCase, mock

from contentful.client import AsyncClient
from contentful.content_type_cache import ContentTypeCache
from contentful.errors import EntryNotFoundError
from contentful.errors import HTTPError
from contentful.client.base import ConfigurationException
from contentful.entry import Entry


class AsyncClientTest(IsolatedAsyncioTestCase):
    def setUp(self):
        ContentTypeCache.__CACHE__ = {}

    async def asyncSetUp(self):
        self.client = AsyncClient("cfexampleapi", "b4c0n73n7fu1")
        self.client_no_cache = AsyncClient(
            "cfexampleapi", "b4c0n73n7fu1", content_type_cache=False
        )

    async def asyncTearDown(self):
        await self.client.teardown()
        await self.client_no_cache.teardown()

    async def test_client_repr(self):
        self.assertEqual(
            "<contentful.AsyncClient space_id='cfexampleapi' access_token='b4c0n73n7fu1' default_locale='en-US'>",
            str(self.client),
        )

    async def test_client_validations(self):
        with self.assertRaises(ConfigurationException):
            AsyncClient(None, "foo")
        with self.assertRaises(ConfigurationException):
            AsyncClient("foo", None)
        with self.assertRaises(ConfigurationException):
            AsyncClient("foo", "bar", api_url=None)
        with self.assertRaises(ConfigurationException):
            AsyncClient("foo", "bar", default_locale=None)
        with self.assertRaises(ConfigurationException):
            AsyncClient("foo", "bar", api_version=None)

    async def test_uses_timeouts(self):

        with aioresponses.aioresponses() as m:
            c = AsyncClient("cfexampleapi", "b4c0n73n7fu1", max_rate_limit_retries=0)
            m.get(re.compile(".*"), status=500)
            with self.assertRaises(HTTPError):
                await c.entries()
            self.assertEqual(len(m.requests), 1)
            self.assertEqual(c.transport._session.timeout.total, 1)
            await c.teardown()

        with aioresponses.aioresponses() as m:
            c = AsyncClient(
                "cfexampleapi",
                "b4c0n73n7fu1",
                timeout_s=0.1231570235,
                max_rate_limit_retries=0,
            )
            m.get(re.compile(".*"), status=500)
            with self.assertRaises(HTTPError):
                await c.entries()

            self.assertEqual(len(m.requests), 1)
            self.assertEqual(c.transport._session.timeout.total, c.timeout_s)
            await c.teardown()

    async def test_client_creates_a_content_type_cache(self):
        with vcr.use_cassette(
            "fixtures/client/content_type_cache.yaml", match_on=["method", "path"]
        ):
            client = AsyncClient("cfexampleapi", "b4c0n73n7fu1")
            await client.initialize()
            self.assertTrue(len(ContentTypeCache.__CACHE__) > 0)
            await client.teardown()

    async def test_client_can_avoid_caching_content_types(self):
        await self.client_no_cache.initialize()
        self.assertFalse(len(ContentTypeCache.__CACHE__) > 0)

    async def test_client_get_space(self):
        with vcr.use_cassette(
            "fixtures/client/space.yaml", match_on=["method", "path", "query"]
        ):
            space = await self.client_no_cache.space()

            self.assertEqual(
                str(space), "<Space[Contentful Example API] id='cfexampleapi'>"
            )

    async def test_client_get_content_type(self):
        with vcr.use_cassette(
            "fixtures/client/content_type.yaml", match_on=["method", "path", "query"]
        ):
            ct = await self.client_no_cache.content_type("cat")

            self.assertEqual(str(ct), "<ContentType[Cat] id='cat'>")

    async def test_client_get_content_types(self):
        with vcr.use_cassette(
            "fixtures/client/content_types.yaml", match_on=["method", "path", "query"]
        ):
            cts = await self.client_no_cache.content_types()

            self.assertEqual(
                str(cts[0]), "<ContentType[City] id='1t9IbcfdCk6m04uISSsaIK'>"
            )

    async def test_client_entry(self):
        with vcr.use_cassette(
            "fixtures/client/entry.yaml", match_on=["method", "path", "query"]
        ):

            entry = await self.client_no_cache.entry("nyancat")

            self.assertEqual(str(entry), "<Entry[cat] id='nyancat'>")
            self.assertEqual(str(entry.best_friend), "<Entry[cat] id='happycat'>")

    async def test_client_entry_not_found(self):
        with vcr.use_cassette(
            "fixtures/client/entry_not_found.yaml", match_on=["method", "path", "query"]
        ):
            with self.assertRaises(EntryNotFoundError):
                await self.client_no_cache.entry("foobar")

    async def test_client_entries(self):
        with vcr.use_cassette(
            "fixtures/client/entries.yaml", match_on=["method", "path", "query"]
        ):
            entries = await self.client_no_cache.entries()

            self.assertEqual(str(entries[0]), "<Entry[cat] id='happycat'>")

    async def test_client_entries_select(self):
        with vcr.use_cassette(
            "fixtures/client/entries_select.yaml", match_on=["method", "path", "query"]
        ):

            entries = await self.client_no_cache.entries(
                {"content_type": "cat", "sys.id": "nyancat", "select": ["fields.name"]}
            )

            self.assertEqual(str(entries[0]), "<Entry[cat] id='nyancat'>")
            self.assertEqual(entries[0].fields(), {"name": "Nyan Cat"})

    async def test_client_entries_links_to_entry(self):
        with vcr.use_cassette(
            "fixtures/client/entries_links_to_entry.yaml",
            match_on=["method", "path", "query"],
        ):
            entries = await self.client_no_cache.entries({"links_to_entry": "nyancat"})
            self.assertEqual(len(entries), 1)
            self.assertEqual(str(entries[0]), "<Entry[cat] id='happycat'>")

    async def test_entry_incoming_references(self):
        with vcr.use_cassette(
            "fixtures/client/entry_incoming_references.yaml",
            match_on=["method", "path", "query"],
        ):
            entry = await self.client_no_cache.entry("nyancat")
            entries = await entry.incoming_references(self.client_no_cache)
            self.assertEqual(len(entries), 1)
            self.assertEqual(str(entries[0]), "<Entry[cat] id='happycat'>")

    async def test_entry_incoming_references_with_query(self):
        with vcr.use_cassette(
            "fixtures/client/entry_incoming_references_with_query.yaml",
            match_on=["method", "path", "query"],
        ):
            entry = await self.client_no_cache.entry("nyancat")
            entries = await entry.incoming_references(
                self.client_no_cache, {"content_type": "cat", "select": ["fields.name"]}
            )
            self.assertEqual(len(entries), 1)
            self.assertEqual(str(entries[0]), "<Entry[cat] id='happycat'>")
            self.assertEqual(entries[0].fields(), {"name": "Happy Cat"})

    async def test_client_entries_links_to_asset(self):
        with vcr.use_cassette(
            "fixtures/client/entries_links_to_asset.yaml",
            match_on=["method", "path", "query"],
        ):
            entries = await self.client_no_cache.entries({"links_to_asset": "nyancat"})
            self.assertEqual(len(entries), 1)
            self.assertEqual(str(entries[0]), "<Entry[cat] id='nyancat'>")

    async def test_asset_incoming_references(self):
        with vcr.use_cassette(
            "fixtures/client/asset_incoming_references.yaml",
            match_on=["method", "path", "query"],
        ):
            asset = await self.client_no_cache.asset("nyancat")
            entries = await asset.incoming_references(self.client_no_cache)
            self.assertEqual(len(entries), 1)
            self.assertEqual(str(entries[0]), "<Entry[cat] id='nyancat'>")

    async def test_client_asset(self):
        with vcr.use_cassette(
            "fixtures/client/asset.yaml", match_on=["method", "path", "query"]
        ):
            asset = await self.client_no_cache.asset("nyancat")

            self.assertEqual(
                str(asset),
                "<Asset id='nyancat' url='//images.contentful.com/cfexampleapi/4gp6taAwW4CmSgumq2ekUm/9da0cd1936871b8d72343e895a00d611/Nyan_cat_250px_frame.png'>",
            )

    async def test_client_locales_on_environment(self):
        with vcr.use_cassette(
            "fixtures/client/locales_on_environment.yaml",
            match_on=["method", "path", "query"],
        ):
            client = AsyncClient(
                "facgnwwgj5fe",
                "<ACCESS_TOKEN>",
                environment="testing",
                content_type_cache=False,
            )
            locales = await client.locales()
            await client.teardown()

        self.assertEqual(
            str(locales), "<Array size='3' total='3' limit='1000' skip='0'>"
        )
        self.assertEqual(
            str(locales[0]),
            "<Locale[U.S. English] code='en-US' default=True fallback_code=None optional=False>",
        )

    async def test_client_assets(self):
        with vcr.use_cassette(
            "fixtures/client/assets.yaml", match_on=["method", "path", "query"]
        ):
            assets = await self.client_no_cache.assets()

            self.assertEqual(
                str(assets[0]),
                "<Asset id='1x0xpXu4pSGS4OukSyWGUK' url='//images.contentful.com/cfexampleapi/1x0xpXu4pSGS4OukSyWGUK/cc1239c6385428ef26f4180190532818/doge.jpg'>",
            )

    async def test_client_sync(self):
        with vcr.use_cassette(
            "fixtures/client/sync.yaml", match_on=["method", "path", "query"]
        ):
            sync = await self.client_no_cache.sync({"initial": True})

            self.assertEqual(
                str(sync),
                "<SyncPage next_sync_token='{0}'>".format(
                    "w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-wo7CnDjChMKKGsK1wrzCrBzCqMOpZAwOOcOvCcOAwqHDv0XCiMKaOcOxZA8BJUzDr8K-wo1lNx7DnHE"
                ),
            )
            self.assertEqual(
                str(sync.items[0]),
                "<Entry[1t9IbcfdCk6m04uISSsaIK] id='5ETMRzkl9KM4omyMwKAOki'>",
            )

    async def test_client_sync_with_environments(self):
        with vcr.use_cassette(
            "fixtures/client/sync_environments.yaml",
            match_on=["method", "path", "query"],
        ):
            client = AsyncClient(
                "a22o2qgm356c",
                "bfbc63cf745a037125dbcc64f716a9a0e9d091df1a79e84920b890f87a6e7ab9",
                environment="staging",
                content_type_cache=False,
            )
            sync = await client.sync({"initial": True})
            await client.teardown()

            self.assertEqual(sync.items[0].environment.id, "staging")

    async def test_client_creates_wrapped_arrays(self):
        with vcr.use_cassette(
            "fixtures/client/array_endpoints.yaml", match_on=["method", "path", "query"]
        ):
            client = AsyncClient(
                "cfexampleapi", "b4c0n73n7fu1", content_type_cache=False
            )
            self.assertEqual(
                str(await client.content_types()),
                "<Array size='4' total='4' limit='100' skip='0'>",
            )
            self.assertEqual(
                str(await client.entries()),
                "<Array size='10' total='10' limit='100' skip='0'>",
            )
            self.assertEqual(
                str(await client.assets()),
                "<Array size='4' total='4' limit='100' skip='0'>",
            )
            await client.teardown()

    # X-Contentful-User-Agent Headers

    def test_client_default_contentful_user_agent_headers(self):
        client = AsyncClient("cfexampleapi", "b4c0n73n7fu1", content_type_cache=False)

        from contentful import __version__
        import platform

        expected = [
            "sdk contentful.py/{0};".format(__version__),
            "platform python/{0};".format(platform.python_version()),
        ]
        header = client._contentful_user_agent()
        for e in expected:
            self.assertTrue(e in header)

        self.assertTrue(re.search("os (Windows|macOS|Linux)(\/.*)?;", header))

        self.assertTrue("integration" not in header)
        self.assertTrue("app" not in header)

    def test_client_with_integration_name_only_headers(self):
        client = AsyncClient(
            "cfexampleapi",
            "b4c0n73n7fu1",
            content_type_cache=False,
            integration_name="foobar",
        )

        header = client._contentful_user_agent()
        self.assertTrue("integration foobar;" in header)
        self.assertFalse("integration foobar/;" in header)

    def test_client_with_integration_headers(self):
        client = AsyncClient(
            "cfexampleapi",
            "b4c0n73n7fu1",
            content_type_cache=False,
            integration_name="foobar",
            integration_version="0.1.0",
        )

        header = client._contentful_user_agent()
        self.assertTrue("integration foobar/0.1.0;" in header)

    def test_client_with_application_name_only_headers(self):
        client = AsyncClient(
            "cfexampleapi",
            "b4c0n73n7fu1",
            content_type_cache=False,
            application_name="foobar",
        )

        header = client._contentful_user_agent()
        self.assertTrue("app foobar;" in header)
        self.assertFalse("app foobar/;" in header)

    def test_client_with_application_headers(self):
        client = AsyncClient(
            "cfexampleapi",
            "b4c0n73n7fu1",
            content_type_cache=False,
            application_name="foobar",
            application_version="0.1.0",
        )

        header = client._contentful_user_agent()
        self.assertTrue("app foobar/0.1.0;" in header)

    def test_client_with_integration_version_only_does_not_include_integration_in_header(
        self,
    ):
        client = AsyncClient(
            "cfexampleapi",
            "b4c0n73n7fu1",
            content_type_cache=False,
            integration_version="0.1.0",
        )

        header = client._contentful_user_agent()
        self.assertFalse("integration /0.1.0" in header)

    def test_client_with_application_version_only_does_not_include_integration_in_header(
        self,
    ):
        client = AsyncClient(
            "cfexampleapi",
            "b4c0n73n7fu1",
            content_type_cache=False,
            application_version="0.1.0",
        )

        header = client._contentful_user_agent()
        self.assertFalse("app /0.1.0;" in header)

    def test_client_with_all_headers(self):
        client = AsyncClient(
            "cfexampleapi",
            "b4c0n73n7fu1",
            content_type_cache=False,
            application_name="foobar_app",
            application_version="1.1.0",
            integration_name="foobar integ",
            integration_version="0.1.0",
        )

        from contentful import __version__
        import platform

        expected = [
            "sdk contentful.py/{0};".format(__version__),
            "platform python/{0};".format(platform.python_version()),
            "app foobar_app/1.1.0;",
            "integration foobar integ/0.1.0;",
        ]
        header = client._contentful_user_agent()
        for e in expected:
            self.assertTrue(e in header)

        self.assertTrue(re.search("os (Windows|macOS|Linux)(\/.*)?;", header))

    def test_client_headers(self):
        client = AsyncClient(
            "cfexampleapi",
            "b4c0n73n7fu1",
            content_type_cache=False,
            application_name="foobar_app",
            application_version="1.1.0",
            integration_name="foobar integ",
            integration_version="0.1.0",
        )

        from contentful import __version__
        import platform

        expected = [
            "sdk contentful.py/{0};".format(__version__),
            "platform python/{0};".format(platform.python_version()),
            "app foobar_app/1.1.0;",
            "integration foobar integ/0.1.0;",
        ]
        header = client._request_headers()["X-Contentful-User-Agent"]
        for e in expected:
            self.assertTrue(e in header)

        self.assertTrue(re.search("os (Windows|macOS|Linux)(\/.*)?;", header))

    # Integration Tests

    async def test_entries_dont_fail_with_unicode_characters(self):
        with vcr.use_cassette(
            "fixtures/integration/issue-4.yaml", match_on=["method", "path", "query"]
        ):
            client = AsyncClient(
                "wltm0euukdog",
                "bbe871957bb60f988af6cbeeccbb178c36cae09e36e8098357e27b51dd38d88e",
                content_type_cache=True,
            )
            entries = await client.entries()
            self.assertEqual(entries[0].name, "😅")
            await client.teardown()

    async def test_entries_dont_fail_with_arrays_as_json_root(self):
        with vcr.use_cassette(
            "fixtures/integration/json-arrays.yaml",
            match_on=["method", "path", "query"],
        ):
            client = AsyncClient(
                "4int1zgmkwcf",
                "d2ac2076019bd4a8357811cbdd5563bb7186d90d77e53c265a1bafd9f83439e8",
                content_type_cache=True,
            )
            entries = await client.entries()
            self.assertEqual(entries[0].json, [{"foo": "bar"}, {"baz": "qux"}])
            await client.teardown()

    async def test_entries_with_none_values_on_all_fields(self):
        with vcr.use_cassette(
            "fixtures/integration/issue-11.yaml", match_on=["method", "path", "query"]
        ):
            client = AsyncClient(
                "rtx5c7z0zbas",
                "a6c8dc438d470c51d1094dad146a1f20fcdba41e21f4e263af6c3f70d8583634",
                content_type_cache=True,
            )
            entry = (await client.entries())[0]
            await client.teardown()
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

    async def test_circular_references_default_depth(self):
        with vcr.use_cassette(
            "fixtures/integration/circular-references.yaml",
            match_on=["method", "path", "query"],
        ):
            client = AsyncClient(
                "rk19fq93y3vw",
                "821aa502a7ce820e46adb30fa6942889619aac4342a7021cfe15197c52a593cc",
                content_type_cache=True,
            )
            a = await client.entry("6kdfS7uMs8owuEIoSaOcQk")
            await client.teardown()
            self.assertEqual(str(a), "<Entry[a] id='6kdfS7uMs8owuEIoSaOcQk'>")
            self.assertEqual(str(a.b), "<Entry[b] id='7oADpDPuneEAsWUiO2CmEo'>")
            self.assertEqual(
                str(a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a),
                "<Entry[a] id='6kdfS7uMs8owuEIoSaOcQk'>",
            )
            self.assertEqual(
                str(a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b),
                "<Link[Entry] id='7oADpDPuneEAsWUiO2CmEo'>",
            )

    async def test_circular_references_set_depth(self):
        with vcr.use_cassette(
            "fixtures/integration/circular-references.yaml",
            match_on=["method", "path", "query"],
        ):
            client = AsyncClient(
                "rk19fq93y3vw",
                "821aa502a7ce820e46adb30fa6942889619aac4342a7021cfe15197c52a593cc",
                content_type_cache=True,
                max_include_resolution_depth=1,
            )
            a = await client.entry("6kdfS7uMs8owuEIoSaOcQk")
            await client.teardown()
            self.assertEqual(str(a), "<Entry[a] id='6kdfS7uMs8owuEIoSaOcQk'>")
            self.assertEqual(str(a.b), "<Entry[b] id='7oADpDPuneEAsWUiO2CmEo'>")
            self.assertEqual(str(a.b.a), "<Link[Entry] id='6kdfS7uMs8owuEIoSaOcQk'>")

    async def test_circular_references_with_reusable_entries(self):
        with vcr.use_cassette(
            "fixtures/integration/circular-references.yaml",
            match_on=["method", "path", "query"],
        ):
            client = AsyncClient(
                "rk19fq93y3vw",
                "821aa502a7ce820e46adb30fa6942889619aac4342a7021cfe15197c52a593cc",
                content_type_cache=True,
                reuse_entries=True,
            )
            a = await client.entry("6kdfS7uMs8owuEIoSaOcQk")
            await client.teardown()
            self.assertEqual(str(a), "<Entry[a] id='6kdfS7uMs8owuEIoSaOcQk'>")
            self.assertEqual(str(a.b), "<Entry[b] id='7oADpDPuneEAsWUiO2CmEo'>")
            self.assertEqual(
                str(a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a),
                "<Entry[a] id='6kdfS7uMs8owuEIoSaOcQk'>",
            )
            self.assertEqual(
                str(a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b),
                "<Entry[b] id='7oADpDPuneEAsWUiO2CmEo'>",
            )
            self.assertEqual(a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b._depth, 1)
            self.assertEqual(a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a._depth, 0)
            self.assertEqual(
                str(
                    a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a.b.a
                ),
                "<Entry[a] id='6kdfS7uMs8owuEIoSaOcQk'>",
            )

    async def test_unresolvable_entries_dont_get_included(self):
        with vcr.use_cassette(
            "fixtures/integration/errors-filtered.yaml",
            match_on=["method", "path", "query"],
        ):
            client = AsyncClient(
                "011npgaszg5o",
                "42c9d93410a7319e9a735671fc1e415348f65e94a99fc768b70a7c649859d4fd",
            )
            entry = await client.entry("1HR1QvURo4MoSqO0eqmUeO")
            await client.teardown()
            self.assertEqual(len(entry.modules), 2)

    async def test_rich_text_field(self):
        with vcr.use_cassette(
            "fixtures/fields/rich_text.yaml", match_on=["method", "path", "query"]
        ):
            client = AsyncClient(
                "jd7yc4wnatx3",
                "6256b8ef7d66805ca41f2728271daf27e8fa6055873b802a813941a0fe696248",
                gzip_encoded=False,
            )
            await client.initialize()

            entry = await client.entry("4BupPSmi4M02m0U48AQCSM")

            await client.teardown()

            expected_entry_occurrances = 2
            embedded_entry_index = 1
            for content in entry.body["content"]:
                if content["nodeType"] == "embedded-entry-block":
                    self.assertTrue(isinstance(content["data"]["target"], Entry))
                    self.assertEqual(
                        content["data"]["target"].body,
                        "Embedded {0}".format(embedded_entry_index),
                    )
                    expected_entry_occurrances -= 1
                    embedded_entry_index += 1
            self.assertEqual(expected_entry_occurrances, 0)

    async def test_rich_text_field_with_embeds_in_lists(self):
        with vcr.use_cassette(
            "fixtures/fields/rich_text_lists_with_embeds.yaml",
            match_on=["method", "path", "query"],
        ):
            client = AsyncClient(
                "jd7yc4wnatx3",
                "6256b8ef7d66805ca41f2728271daf27e8fa6055873b802a813941a0fe696248",
                gzip_encoded=False,
            )
            await client.initialize()

            entry = await client.entry("6NGLswCREsGA28kGouScyY")

            await client.teardown()

            # Hyperlink data is conserved
            self.assertEqual(
                entry.body["content"][0],
                {
                    "data": {},
                    "content": [
                        {
                            "marks": [],
                            "value": "A link to ",
                            "nodeType": "text",
                            "nodeClass": "text",
                        },
                        {
                            "data": {"uri": "https://google.com"},
                            "content": [
                                {
                                    "marks": [],
                                    "value": "google",
                                    "nodeType": "text",
                                    "nodeClass": "text",
                                }
                            ],
                            "nodeType": "hyperlink",
                            "nodeClass": "inline",
                        },
                        {
                            "marks": [],
                            "value": "",
                            "nodeType": "text",
                            "nodeClass": "text",
                        },
                    ],
                    "nodeType": "paragraph",
                    "nodeClass": "block",
                },
            )

            # Unordered lists and ordered lists can contain embedded entries
            self.assertEqual(entry.body["content"][3]["nodeType"], "unordered-list")
            self.assertEqual(
                str(
                    entry.body["content"][3]["content"][2]["content"][0]["data"][
                        "target"
                    ]
                ),
                "<Entry[embedded] id='49rofLvvxCOiIMIi6mk8ai'>",
            )

            self.assertEqual(entry.body["content"][4]["nodeType"], "ordered-list")
            self.assertEqual(
                str(
                    entry.body["content"][4]["content"][2]["content"][0]["data"][
                        "target"
                    ]
                ),
                "<Entry[embedded] id='5ZF9Q4K6iWSYIU2OUs0UaQ'>",
            )

    async def test_rich_text_fields_should_not_get_hydrated_twice(self):
        with vcr.use_cassette(
            "fixtures/integration/issue-41.yaml", match_on=["method", "path", "query"]
        ):
            client = AsyncClient(
                "fds721b88p6b",
                "45ba81cc69423fcd2e3f0a4779de29481bb5c11495bc7e14649a996cf984e98e",
                gzip_encoded=False,
            )

            entry = await client.entry("1tBAu0wP9qAQEg6qCqMics")

            await client.teardown()

            # Not failing is already a success
            self.assertEqual(str(entry.children[0]), str(entry.children[1]))
            self.assertEqual(str(entry.children[0].body), str(entry.children[1].body))
