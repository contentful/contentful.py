from unittest import TestCase
from contentful.content_type_field import ContentTypeField


class ContentTypeFieldTest(TestCase):
    def test_content_type_field(self):
        content_type_field = ContentTypeField({
            "id": "name",
            "name": "Name",
            "type": "Text",
            "localized": True,
            "required": True,
            "disabled": False,
            "omitted": False
        })

        self.assertEqual(content_type_field.id, 'name')
        self.assertEqual(content_type_field.name, 'Name')
        self.assertEqual(content_type_field.type, 'Text')
        self.assertEqual(content_type_field.localized, True)
        self.assertEqual(content_type_field.omitted, False)
        self.assertEqual(content_type_field.required, True)
        self.assertEqual(content_type_field.disabled, False)
        self.assertEqual(str(content_type_field), "<ContentTypeField[Name] id='name' type='Text'>")

    def test_content_type_array_field(self):
        content_type_field = ContentTypeField({
            "id": "likes",
            "name": "Likes",
            "type": "Array",
            "localized": False,
            "required": False,
            "disabled": False,
            "omitted": False,
            "items": {
                "type": "Symbol",
                "validations": []
            }
        })

        self.assertEqual(content_type_field.id, 'likes')
        self.assertEqual(content_type_field.name, 'Likes')
        self.assertEqual(content_type_field.type, 'Array')
        self.assertEqual(content_type_field.items, {'type': 'Symbol', 'validations': []})
        self.assertEqual(content_type_field.localized, False)
        self.assertEqual(content_type_field.omitted, False)
        self.assertEqual(content_type_field.required, False)
        self.assertEqual(content_type_field.disabled, False)
        self.assertEqual(str(content_type_field), "<ContentTypeField[Likes] id='likes' type='Array'>")

    def test_none_values(self):
        field_types = [
            'Symbol',
            'Text',
            'Integer',
            'Number',
            'Date',
            'Boolean',
            'Location',
            'Link',
            'Array',
            'Object'
        ]
        for field_type in field_types:
            ct_field = ContentTypeField({
                "id": "likes",
                "name": "Likes",
                "type": field_type,
                "localized": False,
                "required": False,
                "disabled": False,
                "omitted": False,
                "items": {
                    "type": "Symbol",
                    "validations": []
                }
            })

            self.assertEqual(ct_field.coerce(None), None)
