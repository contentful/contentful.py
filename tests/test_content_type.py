from unittest import TestCase
from contentful.content_type import ContentType


class ContentTypeTest(TestCase):
    def test_content_type(self):
        content_type = ContentType({
            "sys": {
                "space": {
                    "sys": {
                        "type": "Link",
                        "linkType": "Space",
                        "id": "cfexampleapi"
                    }
                },
                "id": "cat",
                "type": "ContentType",
                "createdAt": "2013-06-27T22:46:12.852Z",
                "updatedAt": "2016-11-21T15:01:43.860Z",
                "revision": 6
            },
            "displayField": "name",
            "name": "Cat",
            "description": "Meow.",
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
                },
                {
                    "id": "color",
                    "name": "Color",
                    "type": "Symbol",
                    "localized": False,
                    "required": False,
                    "disabled": False,
                    "omitted": False
                },
                {
                    "id": "bestFriend",
                    "name": "Best Friend",
                    "type": "Link",
                    "localized": False,
                    "required": False,
                    "disabled": False,
                    "omitted": False,
                    "linkType": "Entry"
                },
                {
                    "id": "birthday",
                    "name": "Birthday",
                    "type": "Date",
                    "localized": False,
                    "required": False,
                    "disabled": False,
                    "omitted": False
                },
                {
                    "id": "lifes",
                    "name": "Lifes left",
                    "type": "Integer",
                    "localized": False,
                    "required": False,
                    "disabled": True,
                    "omitted": False
                },
                {
                    "id": "lives",
                    "name": "Lives left",
                    "type": "Integer",
                    "localized": False,
                    "required": False,
                    "disabled": False,
                    "omitted": False
                },
                {
                    "id": "image",
                    "name": "Image",
                    "type": "Link",
                    "localized": False,
                    "required": False,
                    "disabled": False,
                    "omitted": False,
                    "linkType": "Asset"
                }
            ]
        })

        self.assertEqual(content_type.name, 'Cat')
        self.assertEqual(content_type.description, 'Meow.')
        self.assertEqual(content_type.display_field, 'name')
        self.assertEqual(str(content_type.fields[0]), "<ContentTypeField[Name] id='name' type='Text'>")
        self.assertEqual(str(content_type), "<ContentType[Cat] id='cat'>")

        self.assertEqual(str(content_type.field_for('name')), "<ContentTypeField[Name] id='name' type='Text'>")
