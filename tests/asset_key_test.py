import time
import unittest
import vcr

from contentful import ContentTypeCache
from contentful.client import Client
from contentful.asset_key import AssetKey


class AssetKeyTest(unittest.TestCase):
    def setUp(self):
        ContentTypeCache.__CACHE__ = {}
        self.client = Client(
            'o4h6g9w3pooi',
            'test_token',
            environment='master',
            content_type_cache=False,
            authorization_as_header=True
        )

    def tearDown(self):
        ContentTypeCache.__CACHE__ = {}

    def _get_expires_at(self, hours_from_now):
        """Helper to get expiry timestamp"""
        return int(time.time() + (hours_from_now * 60 * 60))

    @vcr.use_cassette('fixtures/asset_key/create.yaml')
    def test_create_asset_key(self):
        """Tests creating an asset key with 48h expiry"""
        
        asset_key = self.client.create_asset_key(self._get_expires_at(24))

        self.assertIsInstance(asset_key, AssetKey)
        self.assertTrue(asset_key.policy)
        self.assertTrue(asset_key.secret)

