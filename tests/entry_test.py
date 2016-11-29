from datetime import datetime
from unittest import TestCase
from contentful.entry import Entry
from contentful.content_type import ContentType
from contentful.content_type_cache import ContentTypeCache


class EntryTest(TestCase):
    def test_entry(self):
        ContentTypeCache.__CACHE__ = []

        entry = Entry({
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
                        'id': 'foo'
                    }
                },
                'type': 'Entry',
                'createdAt': '2016-06-06',
                'updatedAt': '2016-06-06',
                'deletedAt': '2016-06-06',
                'id': 'foobar',
                'version': 1
            },
            'fields': {
                'name': 'foobar',
                'date': '2016-06-06'
            }
        })

        self.assertEqual(str(entry), "<Entry[foo] id='foobar'>")
        self.assertEqual(entry.name, 'foobar')
        self.assertEqual(entry.date, '2016-06-06')

    def test_cached_content_type_entry(self):
        ContentTypeCache.__CACHE__ = []

        foo_ct = ContentType({
            'sys': {
                'type': 'ContentType',
                'id': 'foo'
            },
            "displayField": "name",
            "name": "Foo",
            "description": "",
            "fields": [
                {
                    "id": "name",
                    "name": "Name",
                    "type": "Text",
                    "localized": True,
                    "required": True,
                    "disabled": False,
                    "omitted": False
                },
                {
                    "id": "date",
                    "name": "Date",
                    "type": "Date",
                    "localized": True,
                    "required": True,
                    "disabled": False,
                    "omitted": False
                }
            ]
        })

        ContentTypeCache.__CACHE__.append(foo_ct)

        entry = Entry({
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
                        'id': 'foo'
                    }
                },
                'type': 'Entry',
                'createdAt': '2016-06-06',
                'updatedAt': '2016-06-06',
                'deletedAt': '2016-06-06',
                'id': 'foobar',
                'version': 1
            },
            'fields': {
                'name': 'foobar',
                'date': '2016-06-06'
            }
        })

        self.assertEqual(entry.name, 'foobar')
        self.assertEqual(entry.date, datetime(2016, 6, 6))


    def test_entry_includes(self):
        entry = Entry({
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
                        'id': 'foo'
                    }
                },
                'type': 'Entry',
                'createdAt': '2016-06-06',
                'updatedAt': '2016-06-06',
                'deletedAt': '2016-06-06',
                'id': 'foobar',
                'version': 1
            },
            'fields': {
                'name': 'foobar',
                'date': '2016-06-06',
                'entryLink': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'Entry',
                        'id': 'linkedEntry'
                    }
                },
                'assetLink': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'Asset',
                        'id': 'linkedAsset'
                    }
                },
                'arrayLink': [
                    {
                        'sys': {
                            'type': 'Link',
                            'linkType': 'Entry',
                            'id': 'otherLinkedEntry'
                        }
                    }
                ]
            }
        },
        includes=[
            {
                'sys': {
                    'id': 'linkedEntry',
                    'type': 'Entry',
                    'contentType': {
                        'sys': {
                            'id': 'foobar'
                        }
                    }
                },
                'fields': {
                    'foo': 'bar'
                }
            },
            {
                'sys': {
                    'id': 'otherLinkedEntry',
                    'type': 'Entry',
                    'contentType': {
                        'sys': {
                            'id': 'foobar'
                        }
                    }
                },
                'fields': {
                    'foo': 'baz'
                }
            },
            {
                'sys': {
                    'id': 'linkedAsset',
                    'type': 'Asset'
                },
                'fields': {
                    'file': {
                        'url': '//images.contentful.com/...'
                    }
                }
            }
        ])

        self.assertEqual(str(entry.entry_link), "<Entry[foobar] id='linkedEntry'>")
        self.assertEqual(str(entry.asset_link), "<Asset id='linkedAsset' url='//images.contentful.com/...'>")
        self.assertEqual(str(entry.array_link[0]), "<Entry[foobar] id='otherLinkedEntry'>")
