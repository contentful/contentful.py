import vcr
from unittest import TestCase
from contentful.content_type_cache import ContentTypeCache
from contentful import Client


class ContentTypeCacheTest(TestCase):
    @vcr.use_cassette('fixtures/cache/cache.yaml')
    def test_cache(self):
        Client('o4h6g9w3pooi', 'b4c0n73n7fu1')

        cat_ct = ContentTypeCache.get('o4h6g9w3pooi', 'article')
        self.assertEqual(str(cat_ct), "<ContentType[Article] id='article'>")

    @vcr.use_cassette('fixtures/cache/cache.yaml')
    def test_cache_update(self):
        ContentTypeCache.__CACHE__ = {}
        client = Client('o4h6g9w3pooi', 'b4c0n73n7fu1', content_type_cache=False)

        ContentTypeCache.update_cache(client)

        cat_ct = ContentTypeCache.get('o4h6g9w3pooi', 'article')
        self.assertEqual(str(cat_ct), "<ContentType[Article] id='article'>")
