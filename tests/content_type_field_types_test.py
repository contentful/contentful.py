# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from datetime import datetime
from contentful.content_type_field_types import (
    BasicField,
    SymbolField,
    TextField,
    IntegerField,
    NumberField,
    DateField,
    BooleanField,
    LocationField,
    LinkField,
    ArrayField,
    ObjectField,
    RichTextField,
    ResourceLinkField
)
from contentful.resource import Link


class BasicFieldTest(TestCase):
    def test_basic_field(self):
        self.assertEqual(BasicField().coerce('foo'), 'foo')
        self.assertEqual(BasicField().coerce(123), 123)

    def test_unicode_chars_dont_fail(self):
        self.assertEqual(TextField().coerce('😅'), '😅')


class SymbolFieldTest(TestCase):
    def test_symbol_field(self):
        self.assertEqual(SymbolField().coerce('foo'), 'foo')
        self.assertEqual(SymbolField().coerce(123), '123')

    def test_unicode_chars_dont_fail(self):
        self.assertEqual(TextField().coerce('😅'), '😅')


class TextFieldTest(TestCase):
    def test_text_field(self):
        self.assertEqual(TextField().coerce('foo'), 'foo')
        self.assertEqual(TextField().coerce(123), '123')

    def test_unicode_chars_dont_fail(self):
        self.assertEqual(TextField().coerce('😅'), '😅')


class IntegerFieldTest(TestCase):
    def test_integer_field(self):
        integer_field = IntegerField()
        self.assertEqual(integer_field.coerce(123), 123)
        self.assertEqual(integer_field.coerce(123.0), 123)
        self.assertEqual(integer_field.coerce('123'), 123)

        self.assertRaises(Exception, integer_field.coerce, 'foo')


class NumberFieldTest(TestCase):
    def test_number_field(self):
        number_field = NumberField()
        self.assertEqual(number_field.coerce(123), 123.0)
        self.assertEqual(number_field.coerce(123.0), 123.0)
        self.assertEqual(number_field.coerce('123'), 123.0)

        self.assertRaises(Exception, number_field.coerce, 'foo')


class DateFieldTest(TestCase):
    def test_date_field(self):
        date_field = DateField()
        self.assertEqual(date_field.coerce('2016-05-05'), datetime(2016, 5, 5))

        self.assertRaises(Exception, date_field.coerce, 'foo')


class BooleanFieldTest(TestCase):
    def test_boolean_field(self):
        self.assertEqual(BooleanField().coerce('foo'), True)
        self.assertEqual(BooleanField().coerce(True), True)
        self.assertEqual(BooleanField().coerce(''), False)
        self.assertEqual(BooleanField().coerce(False), False)


class LocationFieldTest(TestCase):
    def test_location_field(self):
        location_field = LocationField()
        self.assertEqual(location_field.coerce({'lat': 123, 'lon': 456}), (123, 456))

        location = location_field.coerce({'lat': 123, 'lon': 456})
        self.assertEqual(location.lat, 123)
        self.assertEqual(location.lon, 456)

        self.assertRaises(Exception, location_field.coerce, 'foo')


class LinkFieldTest(TestCase):
    def test_link_field(self):
        self.assertEqual(LinkField().coerce('foo'), 'foo')
        self.assertEqual(LinkField().coerce(123), 123)


class ArrayFieldTest(TestCase):
    def test_symbol_array_field(self):
        array_field = ArrayField({'type': 'Symbol'})

        self.assertEqual(array_field.coerce([123, 'foo']), ['123', 'foo'])

        self.assertRaises(Exception, array_field.coerce, 123)

    def test_link_array_field(self):
        array_field = ArrayField({'type': 'Link', 'linkType': 'Entry'})

        self.assertEqual(array_field.coerce([123, 'foo']), [123, 'foo'])

        self.assertRaises(Exception, array_field.coerce, 123)

    def test_link_array_field_other_type(self):
        self.assertRaises(Exception, ArrayField, {'type': 'foo'})


class ObjectFieldTest(TestCase):
    def test_object_field(self):
        object_field = ObjectField()

        self.assertEqual(object_field.coerce({'foo': 'bar'}), {'foo': 'bar'})
        self.assertEqual(object_field.coerce(123), 123)
        self.assertEqual(object_field.coerce('foo'), 'foo')
        self.assertEqual(object_field.coerce([1, 2, 3]), [1, 2, 3])
        self.assertEqual(object_field.coerce([{'foo': 'bar'}, {'baz': 'qux'}]), [{'foo': 'bar'}, {'baz': 'qux'}])


class RichTextFieldTest(TestCase):
    def test_rich_text_field(self):
        rt_field = RichTextField()

        self.assertEqual(repr(rt_field), '<RichTextField>')

        # on empty or non rich text field will return the value as is
        self.assertEqual(rt_field.coerce({}), {})
        self.assertEqual(rt_field.coerce(123), 123)

        # on proper rich text field, but without embedded entries will return as is
        document = {
            "nodeType": "document",
            "content": [{
                "nodeType": "paragraph",
                "nodeClass": "block",
                "content": [{
                    "nodeClass": "text",
                    "nodeType": "text",
                    "value": "This text is bold",
                    "marks": [{
                        "type": "bold"
                    }]
                }]
            }]
        }
        self.assertEqual(rt_field.coerce(document), document)

        # with embedded entries but with errors, will remove the node
        document = {
            "nodeType": "document",
            "content": [{
                "nodeType": "embedded-entry-block",
                "nodeClass": "block",
                "data": {
                    "target": {
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": "4JJ21pcEI0QSsea20g6K6K"
                        }
                    }
                }
            }]
        }

        errors = [{"details": {"id": "4JJ21pcEI0QSsea20g6K6K"}}]

        self.assertEqual(rt_field.coerce(document, errors=errors), {
            "nodeType": "document",
            "content": []
        })

        # With embedded entry that's unresolvable
        document = {
            "nodeType": "document",
            "content": [{
                "nodeType": "embedded-entry-block",
                "nodeClass": "block",
                "data": {
                    "target": {
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": "4JJ21pcEI0QSsea20g6K6K"
                        }
                    }
                }
            }]
        }

        coerced = rt_field.coerce(document)
        self.assertTrue(isinstance(coerced['content'][0]['data']['target'], Link))

        # with 2 embedded entries that have errors, both will be removed
        # without a list index out of range error
        document = {
            "nodeType": "document",
            "content": [{
                "nodeType": "embedded-entry-block",
                "nodeClass": "block",
                "data": {
                    "target": {
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": "4JJ21pcEI0QSsea20g6K6K"
                        }
                    }
                }
            }, {
                "nodeType": "embedded-entry-block",
                "nodeClass": "block",
                "data": {
                    "target": {
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": "4JJ21pcEI0QSsea20g6K6K"
                        }
                    }
                }
            }]
        }

        errors = [{"details": {"id": "4JJ21pcEI0QSsea20g6K6K"}}]

        self.assertEqual(rt_field.coerce(document, errors=errors), {
            "nodeType": "document",
            "content": []
        })


class ResourceLinkFieldTest(TestCase):
    def test_resource_link_field(self):
        resource_link_field = ResourceLinkField()

        self.assertEqual(resource_link_field.coerce('foo'), 'foo')
