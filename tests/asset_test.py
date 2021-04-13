from unittest import TestCase
from contentful.asset import Asset


class AssetTest(TestCase):
    def test_asset(self):
        asset = Asset({
            'sys': {
                'type': 'Asset',
                'id': 'foo',
                'createdAt': '2016-12-01T11:39:20.257859',
                'updatedAt': '2016-12-01T11:39:20.257859',
                'space': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'Space',
                        'id': 'foo'
                    }
                }
            },
            'fields': {
                'title': 'Awesome Pic',
                'description': 'A picture of something',
                'file': {
                    'fileName': 'foobar',
                    'contentType': 'image/jpeg',
                    'url': '//images.contentful.com/...',
                    'details': {
                        'size': 300
                    }
                }
            }
        })

        self.assertEqual(asset.id, 'foo')
        self.assertEqual(asset.title, 'Awesome Pic')
        self.assertEqual(asset.description, 'A picture of something')
        self.assertEqual(asset.url(), '//images.contentful.com/...')
        self.assertEqual(asset.url(w=123), '//images.contentful.com/...?w=123')
        self.assertEqual(str(asset), "<Asset id='foo' url='//images.contentful.com/...'>")

    def test_metadata_tags(self):
        asset = Asset({
            'sys': {
                'type': 'Asset',
                'id': 'foo',
                'createdAt': '2016-12-01T11:39:20.257859',
                'updatedAt': '2016-12-01T11:39:20.257859',
                'space': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'Space',
                        'id': 'foo'
                    }
                }
            },
            'metadata': {
                'tags': [
                    {
                        'sys': {
                            'type': 'Link',
                            'linkType': 'Tag',
                            'id': 'nyCampaign'
                        }
                    }
                ]
            },
            'fields': {
                'title': 'Awesome Pic',
                'metadata': 'A picture of something',
                'file': {
                    'fileName': 'foobar',
                    'contentType': 'image/jpeg',
                    'url': '//images.contentful.com/...',
                    'details': {
                        'size': 300
                    }
                }
            }
        })

        self.assertEqual(len(asset._metadata['tags']), 1)

        tag = asset._metadata['tags'][0]
        self.assertEqual(str(tag), "<Link[Tag] id='nyCampaign'>")
        self.assertEqual(tag.id, 'nyCampaign')
        self.assertEqual(tag.link_type, 'Tag')

    def test_asset_with_no_file_can_be_serialized_correctly(self):
        asset = Asset({
            'sys': {
                'type': 'Asset',
                'id': 'foo',
                'createdAt': '2016-12-01T11:39:20.257859',
                'updatedAt': '2016-12-01T11:39:20.257859',
                'space': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'Space',
                        'id': 'foo'
                    }
                }
            },
            'fields': {
                'title': 'Awesome Pic',
                'description': 'A picture of something'
            }
        })

        self.assertEqual(str(asset), "<Asset id='foo' url=''>")

    def test_asset_with_empty_file_can_be_serialized_correctly(self):
        asset = Asset({
            'sys': {
                'type': 'Asset',
                'id': 'foo',
                'createdAt': '2016-12-01T11:39:20.257859',
                'updatedAt': '2016-12-01T11:39:20.257859',
                'space': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'Space',
                        'id': 'foo'
                    }
                }
            },
            'fields': {
                'title': 'Awesome Pic',
                'description': 'A picture of something',
                'file': {}
            }
        })

        self.assertEqual(str(asset), "<Asset id='foo' url=''>")
