from unittest import TestCase
from urllib.parse import parse_qs, urlsplit
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

    def test_metadata_concepts(self):
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
                'tags': [],
                'concepts': [
                    {
                        "sys": {
                          "type": "Link",
                          "linkType": "TaxonomyConcept",
                          "id": "3DMf5gdax6J22AfcJ6fvsC"
                        }
                    }
                ]
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

        self.assertEqual(len(asset._metadata['concepts']), 1)
        concept = asset._metadata['concepts'][0]
        self.assertEqual(str(concept), "<Link[TaxonomyConcept] id='3DMf5gdax6J22AfcJ6fvsC'>")
        self.assertEqual(concept.id, '3DMf5gdax6J22AfcJ6fvsC')
        self.assertEqual(concept.link_type, 'TaxonomyConcept')

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

    def _asset_for_url(self, url):
        return Asset({'sys': {'type': 'Asset', 'id': 'image'},
                      'fields': {'file': {'url': url}}})

    def test_options_preserve_existing_query(self):
        asset = self._asset_for_url('//images.ctfassets.net/image.jpg?token=a%2Bb&policy=x')
        result = urlsplit(asset.url(w=120, h=160))
        self.assertEqual(parse_qs(result.query),
                         {'token': ['a+b'], 'policy': ['x'], 'w': ['120'], 'h': ['160']})

    def test_options_precede_fragment(self):
        result = urlsplit(self._asset_for_url('//images.ctfassets.net/image.jpg#preview').url(w=120))
        self.assertEqual(result.query, 'w=120')
        self.assertEqual(result.fragment, 'preview')

    def test_options_preserve_query_and_fragment(self):
        result = urlsplit(self._asset_for_url('//images.ctfassets.net/image.jpg?token=a%2Bb#preview').url(w=120))
        self.assertEqual(parse_qs(result.query), {'token': ['a+b'], 'w': ['120']})
        self.assertEqual(result.fragment, 'preview')

    def test_no_options_preserves_url_verbatim(self):
        url = '//images.ctfassets.net/image.jpg?token=a%2Bb#preview'
        self.assertEqual(self._asset_for_url(url).url(), url)

    def test_plain_url_retains_option_format(self):
        self.assertEqual(self._asset_for_url('//images.ctfassets.net/image.jpg').url(w=120, h=160),
                         '//images.ctfassets.net/image.jpg?w=120&h=160')
