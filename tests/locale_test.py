from unittest import TestCase
from contentful.locale import Locale


class LocaleTest(TestCase):
    def test_locale(self):
        locale = Locale({
            'code': 'en-US',
            'name': 'English U.S.',
            'fallbackCode': None,
            'default': True
        })

        self.assertEqual(locale.code, 'en-US')
        self.assertEqual(locale.name, 'English U.S.')
        self.assertEqual(locale.fallback_code, None)
        self.assertEqual(locale.default, True)
        self.assertEqual(str(locale), "<Locale[English U.S.] code='en-US' default=True fallback_code=None optional=False>")
