from unittest import TestCase
from contentful.taxonomy_concept import TaxonomyConcept


class TaxonomyConceptTest(TestCase):
    def test_taxonomy_concept(self):
        concept = TaxonomyConcept({
            "sys": {
                "id": "3DMf5gdax6J22AfcJ6fvsC",
                "type": "TaxonomyConcept",
                "createdAt": "2016-12-20T10:43:35.772Z",
                "updatedAt": "2016-12-20T10:43:35.772Z",
                "version": 1,
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
                "en-US": "sofa"
            },
            "altLabels": {
                "en-US": []
            },
            "hiddenLabels": {
                "en-US": []
            },
            "notations": [],
            "note": {
                "en-US": ""
            },
            "changeNote": {
                "en-US": ""
            },
            "definition": {
                "en-US": ""
            },
            "editorialNote": {
                "en-US": ""
            },
            "example": {
                "en-US": ""
            },
            "historyNote": {
                "en-US": ""
            },
            "scopeNote": {
                "en-US": ""
            },
            "broader": [
                {
                    "sys": {
                        "id": "5YRe68gqRx6QlLyEE00Ue6",
                        "type": "Link",
                        "linkType": "TaxonomyConcept"
                    }
                }
            ],
            "related": [
                {
                    "sys": {
                        "id": "5YRe68gqRx6QlLyEE00Ue6",
                        "type": "Link",
                        "linkType": "TaxonomyConcept"
                    }
                }
            ],
            "conceptSchemes": [
                {
                    "sys": {
                        "type": "Link",
                        "linkType": "TaxonomyConceptScheme",
                        "id": "2s0F7127ajju1AVToMaCtE"
                    }
                }
            ]
        })

        self.assertEqual(str(concept), "<TaxonomyConcept id='3DMf5gdax6J22AfcJ6fvsC'>")
        self.assertEqual(concept.id, '3DMf5gdax6J22AfcJ6fvsC')
        self.assertEqual(concept.type, 'TaxonomyConcept')
        self.assertEqual(concept.pref_label, {'en-US': 'sofa'})
        self.assertEqual(len(concept.broader), 1)
        self.assertEqual(concept.broader[0]['sys']['linkType'], 'TaxonomyConcept')
