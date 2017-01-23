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
    ObjectField
)

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

        self.assertRaises(Exception, object_field.coerce, 123)
        self.assertRaises(Exception, object_field.coerce, 'foo')
        self.assertRaises(Exception, object_field.coerce, [1, 2, 3])
