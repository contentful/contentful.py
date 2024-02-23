from unittest import TestCase
from contentful.space import Space


class SpaceTest(TestCase):
    def test_space(self):
        space = Space({
            "sys": {
                "type": "Space",
                "id": "cfexampleapi"
            },
            "name": "Contentful Example API",
            "locales": [
                {
                    "code": "en-US",
                    "default": True,
                    "name": "English",
                    "fallbackCode": None
                },
                {
                    "code": "tlh",
                    "default": False,
                    "name": "Klingon",
                    "fallbackCode": "en-US"
                }
            ]
        })

        self.assertEqual(space.id, 'cfexampleapi')
        self.assertEqual(space.name, 'Contentful Example API')
        self.assertEqual(len(space.locales), 2)
        self.assertEqual(str(space.locales[0]), "<Locale[English] code='en-US' default=True fallback_code=None optional=False>")
        self.assertEqual(str(space.locales[1]), "<Locale[Klingon] code='tlh' default=False fallback_code='en-US' optional=False>")
        self.assertEqual(str(space), "<Space[Contentful Example API] id='cfexampleapi'>")
