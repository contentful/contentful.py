import vcr
import pickle
from datetime import datetime
from unittest import TestCase
from contentful.resource import Resource, FieldsResource, Link
from contentful.client import Client


class ResourceTest(TestCase):
    def test_resource(self):
        resource = Resource({
            'sys': {
                'space': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'Space',
                        'id': 'foo'
                    }
                },
                'contentType': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'ContentType',
                        'id': 'bar'
                    }
                },
                'type': 'Entry',
                'createdAt': '2016-06-06',
                'updatedAt': '2016-06-06',
                'deletedAt': '2016-06-06',
                'id': 'foobar',
                'version': 1
            }
        })

        self.assertEqual(str(resource.space), "<Link[Space] id='foo'>")
        self.assertEqual(str(resource.content_type), "<Link[ContentType] id='bar'>")
        self.assertEqual(resource.created_at, datetime(2016, 6, 6))
        self.assertEqual(resource.updated_at, datetime(2016, 6, 6))
        self.assertEqual(resource.deleted_at, datetime(2016, 6, 6))
        self.assertEqual(resource.id, 'foobar')
        self.assertEqual(resource.version, 1)

        self.assertRaises(AttributeError, resource.__getattr__, 'foo')


class FieldsResourceTest(TestCase):
    def test_fields_resource(self):
        resource = FieldsResource({
            'sys': {
                'space': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'Space',
                        'id': 'foo'
                    }
                },
                'contentType': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'ContentType',
                        'id': 'bar'
                    }
                },
                'type': 'Entry',
                'createdAt': '2016-06-06',
                'updatedAt': '2016-06-06',
                'deletedAt': '2016-06-06',
                'id': 'foobar',
                'version': 1,
                'locale': 'foo-locale'
            },
            'fields': {
                'foo': 'bar',
                'baz': 123,
                'qux': True
            }
        })

        self.assertEqual(resource.foo, 'bar')
        self.assertEqual(resource.baz, 123)
        self.assertEqual(resource.qux, True)
        self.assertEqual(resource.fields(), {'foo': 'bar', 'baz': 123, 'qux': True})
        self.assertEqual(resource.fields('foo-locale'), {'foo': 'bar', 'baz': 123, 'qux': True})
        self.assertEqual(resource.fields('bar-locale'), {})

        self.assertRaises(AttributeError, resource.__getattr__, 'foobar')

    def test_pickleable_resource(self):
        resource = FieldsResource({
            'sys': {
                'space': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'Space',
                        'id': 'foo'
                    }
                },
                'contentType': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'ContentType',
                        'id': 'bar'
                    }
                },
                'type': 'Entry',
                'createdAt': '2016-06-06',
                'updatedAt': '2016-06-06',
                'deletedAt': '2016-06-06',
                'id': 'foobar',
                'version': 1,
                'locale': 'foo-locale'
            },
            'fields': {
                'foo': 'bar',
                'baz': 123,
                'qux': True
            }
        })

        serialized_resource = pickle.dumps(resource)
        deserialized_resource = pickle.loads(serialized_resource)

        self.assertEqual(resource.foo, deserialized_resource.foo)
        self.assertEqual(resource.baz, deserialized_resource.baz)
        self.assertEqual(resource.qux, deserialized_resource.qux)
        self.assertEqual(resource.fields(), deserialized_resource.fields())
        self.assertEqual(resource.fields('foo-locale'), deserialized_resource.fields('foo-locale'))
        self.assertEqual(resource.fields('bar-locale'), deserialized_resource.fields('bar-locale'))

        self.assertRaises(AttributeError, resource.__getattr__, 'foobar')

    def test_fields_resource_localized(self):
        resource = FieldsResource({
            'sys': {
                'space': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'Space',
                        'id': 'foo'
                    }
                },
                'contentType': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'ContentType',
                        'id': 'bar'
                    }
                },
                'type': 'Entry',
                'createdAt': '2016-06-06',
                'updatedAt': '2016-06-06',
                'deletedAt': '2016-06-06',
                'id': 'foobar',
                'version': 1,
                'locale': 'foo-locale'
            },
            'fields': {
                'foo': {'foo-locale': 'bar-foo', 'bar-locale': 'bar-bar'},
                'baz': {'foo-locale': 123, 'bar-locale': 456},
                'qux': {'foo-locale': True, 'bar-locale': False}
            }
        },
        localized=True)

        self.assertEqual(resource.foo, 'bar-foo')
        self.assertEqual(resource.baz, 123)
        self.assertEqual(resource.qux, True)
        self.assertEqual(resource.fields(), {'foo': 'bar-foo', 'baz': 123, 'qux': True})
        self.assertEqual(resource.fields('foo-locale'), {'foo': 'bar-foo', 'baz': 123, 'qux': True})
        self.assertEqual(resource.fields('bar-locale'), {'foo': 'bar-bar', 'baz': 456, 'qux': False})
        self.assertEqual(resource.fields('baz-locale'), {})

        self.assertRaises(AttributeError, resource.__getattr__, 'foobar')


class LinkTest(TestCase):
    def test_link(self):
        link = Link({
            'sys': {
                'type': 'Link',
                'linkType': 'Space',
                'id': 'foo'
            }
        })

        self.assertEqual(link.id, 'foo')
        self.assertEqual(link.type, 'Link')
        self.assertEqual(link.link_type, 'Space')
        self.assertEqual(str(link), "<Link[Space] id='foo'>")

    @vcr.use_cassette('fixtures/link/resolve_space.yaml', decode_compressed_response=True)
    def test_link_space_resource(self):
        link = Link({
            'sys': {
                'type': 'Link',
                'linkType': 'Space',
                'id': 'cfexampleapi'
            }
        })
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        space = link.resolve(client)

        self.assertEqual(str(space), "<Space[Contentful Example API] id='cfexampleapi'>")

    @vcr.use_cassette('fixtures/link/resolve_other.yaml', decode_compressed_response=True)
    def test_link_other_resource(self):
        link = Link({
            'sys': {
                'type': 'Link',
                'linkType': 'ContentType',
                'id': 'cat'
            }
        })
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        cat_ct = link.resolve(client)

        self.assertEqual(str(cat_ct), "<ContentType[Cat] id='cat'>")
