from unittest import TestCase
from contentful.taxonomy_concept_scheme import TaxonomyConceptScheme


class TaxonomyConceptSchemeTest(TestCase):
    def test_taxonomy_concept_scheme(self):
        scheme = TaxonomyConceptScheme({
            "sys": {
                "id": "7CzXPy6XvYYd0D7SomitgI",
                "type": "TaxonomyConceptScheme",
                "createdAt": "2016-12-20T10:43:35.772Z",
                "updatedAt": "2016-12-20T10:43:35.772Z",
                "version": 0,
                'space': {
                    'sys': {
                        'type': 'Link',
                        'linkType': 'Space',
                        'id': 'foo'
                    }
                }
            },
            "uri": None,
            "prefLabel": {
                "en-US": "furniture"
            },
            "definition": {
                "en-US": ""
            },
            "topConcepts": [
                {
                    "sys": {
                        "id": "5YRe68gqRx6QlLyEE00Ue6",
                        "type": "Link",
                        "linkType": "TaxonomyConcept"
                    }
                }
            ],
            "concepts": [
                {
                    "sys": {
                        "id": "5YRe68gqRx6QlLyEE00Ue6",
                        "type": "Link",
                        "linkType": "TaxonomyConcept"
                    }
                }
            ],
            "totalConcepts": 1
        })

        self.assertEqual(str(scheme), "<TaxonomyConceptScheme id='7CzXPy6XvYYd0D7SomitgI'>")
        self.assertEqual(scheme.id, '7CzXPy6XvYYd0D7SomitgI')
        self.assertEqual(scheme.type, 'TaxonomyConceptScheme')
        self.assertEqual(scheme.pref_label, {'en-US': 'furniture'})
        self.assertEqual(scheme.total_concepts, 1)
        self.assertEqual(len(scheme.concepts), 1)
        self.assertEqual(scheme.concepts[0]['sys']['linkType'], 'TaxonomyConcept')
