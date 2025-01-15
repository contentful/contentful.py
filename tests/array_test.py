from unittest import TestCase
from contentful.array import Array
from contentful.entry import Entry


class ArrayTest(TestCase):
    def test_asset(self):
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
        array = Array({
            'sys': {
                'type': 'Array'
            },
            'items': [
                entry.raw
            ],
            'total': 11,
            'skip': 10,
            'limit': 10
        }, [entry])

        self.assertEqual(len(array), 1)
        self.assertEqual(array.total, 11)
        self.assertEqual(array.skip, 10)
        self.assertEqual(array.limit, 10)
        self.assertEqual(array[0], entry)
        self.assertEqual(str(array), "<Array size='1' total='11' limit='10' skip='10'>")
        for e in array:
            # testing __iter__
            # should be only one, so assert is valid
            self.assertEqual(e, entry)
