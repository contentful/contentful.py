from unittest import TestCase
from contentful import utils


class UtilsTest(TestCase):
    def test_snake_case(self):
        self.assertEqual(utils.snake_case('foo'), 'foo')
        self.assertEqual(utils.snake_case('foo_bar'), 'foo_bar')
        self.assertEqual(utils.snake_case('Foo'), 'foo')
        self.assertEqual(utils.snake_case('FooBar'), 'foo_bar')
        self.assertEqual(utils.snake_case('fooBar'), 'foo_bar')

    def test_is_link(self):
        self.assertFalse(utils.is_link('foo'))
        self.assertFalse(utils.is_link([1, 2, 3]))
        self.assertFalse(utils.is_link({'foo': 'bar'}))
        self.assertFalse(utils.is_link({'sys': {'type': 'Space'}, 'id': 'foo'}))

        self.assertTrue(utils.is_link({'sys': {'type': 'Link'}, 'id': 'foo'}))

    def test_is_link_array(self):
        self.assertFalse(utils.is_link_array('foo'))
        self.assertFalse(utils.is_link_array([1, 2, 3]))
        self.assertFalse(utils.is_link_array({'foo': 'bar'}))
        self.assertFalse(utils.is_link_array({'sys': {'type': 'Space'}, 'id': 'foo'}))
        self.assertFalse(utils.is_link_array({'sys': {'type': 'Link'}, 'id': 'foo'}))
        self.assertFalse(utils.is_link_array([{'sys': {'type': 'Space'}, 'id': 'foo'}]))

        self.assertTrue(utils.is_link_array([{'sys': {'type': 'Link'}, 'id': 'foo'}]))

    def test_resource_for_link(self):
        includes = [
            {'sys': {'id': 'foo', 'type': 'Entry'}},
            {'sys': {'id': 'bar', 'type': 'Entry'}},
            {'sys': {'id': 'foo', 'type': 'Asset'}}
        ]

        foo_entry = utils.resource_for_link({'sys': {'type': 'Link', 'id': 'foo', 'linkType': 'Entry'}}, includes)
        self.assertEqual(foo_entry, includes[0])

        bar_entry = utils.resource_for_link({'sys': {'type': 'Link', 'id': 'bar', 'linkType': 'Entry'}}, includes)
        self.assertEqual(bar_entry, includes[1])

        foo_asset = utils.resource_for_link({'sys': {'type': 'Link', 'id': 'foo', 'linkType': 'Asset'}}, includes)
        self.assertEqual(foo_asset, includes[2])

    def test_resource_for_link_with_cached_resource(self):
        includes = []
        cached_resources = {"Entry:foo:*": "foobar"}

        foo_entry = utils.resource_for_link({'sys': {'type': 'Link', 'id': 'foo', 'linkType': 'Entry'}}, includes, resources=cached_resources, locale='*')
        self.assertEqual(foo_entry, cached_resources["Entry:foo:*"])

        bar_entry = utils.resource_for_link({'sys': {'type': 'Link', 'id': 'bar', 'linkType': 'Entry'}}, includes, resources=cached_resources, locale='*')
        self.assertIsNone(bar_entry)

    def _test_retry_request(self):
        """Tested as part of Errors"""
        pass

    def test_unresolvable_empty_item_returns_true(self):
        self.assertTrue(utils.unresolvable(None, []))
