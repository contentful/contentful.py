import vcr
from unittest import TestCase
from contentful.content_type_cache import ContentTypeCache
from contentful import Client


class ContentTypeCacheTest(TestCase):
    @vcr.use_cassette('fixtures/cache/cache.yaml')
    def test_cache(self):
        Client('cfexampleapi', 'b4c0n73n7fu1')

        cat_ct = ContentTypeCache.get('cat')
        self.assertEqual(str(cat_ct), "<ContentType[Cat] id='cat'>")

    @vcr.use_cassette('fixtures/cache/cache.yaml')
    def test_cache_update(self):
        ContentTypeCache.__CACHE__ = []
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        ContentTypeCache.update_cache(client)

        cat_ct = ContentTypeCache.get('cat')
        self.assertEqual(str(cat_ct), "<ContentType[Cat] id='cat'>")
