import vcr
from unittest import TestCase
from contentful.content_type_cache import ContentTypeCache
from contentful import Client


class ContentTypeCacheTest(TestCase):
    def test_cache(self):
        with vcr.use_cassette("fixtures/cache/cache.yaml"):
            client = Client("o4h6g9w3pooi", "b4c0n73n7fu1")
            client.initialize()
            cat_ct = ContentTypeCache.get("o4h6g9w3pooi", "article")
            self.assertEqual(str(cat_ct), "<ContentType[Article] id='article'>")

    def test_cache_update(self):
        with vcr.use_cassette("fixtures/cache/cache.yaml"):
            ContentTypeCache.__CACHE__ = {}
            client = Client("o4h6g9w3pooi", "b4c0n73n7fu1", content_type_cache=False)
            content_types = client.content_types()
            ContentTypeCache.update_cache(
                space_id=client.space_id, content_types=content_types
            )

        cat_ct = ContentTypeCache.get("o4h6g9w3pooi", "article")
        self.assertEqual(str(cat_ct), "<ContentType[Article] id='article'>")
