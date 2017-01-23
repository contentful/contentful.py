import dateutil.parser
from collections import namedtuple
from .utils import unicode_class

"""
contentful.content_type_field_types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the Field Coercion classes.

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class BasicField(object):
    """Base Coercion Class"""

    def __init__(self, items=None):
        self._items = items

    def coerce(self, value):
        """Just returns the value."""

        return value

    def __repr__(self):
        return "<{0}>".format(
            self.__class__.__name__
        )


class SymbolField(BasicField):
    """Symbol Coercion Class"""

    def coerce(self, value):
        """Coerces value to str"""

        return unicode_class()(value)


class TextField(BasicField):
    """Text Coercion Class"""

    def coerce(self, value):
        """Coerces value to str"""

        return unicode_class()(value)


class IntegerField(BasicField):
    """Integer Coercion Class"""

    def coerce(self, value):
        """Coerces value to int"""

        return int(value) if value is not None else None


class NumberField(BasicField):
    """Number Coercion Class"""

    def coerce(self, value):
        """Coerces value to float"""

        return float(value) if value is not None else None


class DateField(BasicField):
    """Date Coercion Class"""

    def coerce(self, value):
        """Coerces ISO8601 date to :class:`datetime.datetime` object."""

        return dateutil.parser.parse(value)


class BooleanField(BasicField):
    """Boolean Coercion Class"""

    def coerce(self, value):
        """Coerces value to boolean"""

        return bool(value)


class LocationField(BasicField):
    """Location Coercion Class"""

    def coerce(self, value):
        """Coerces value to Location object"""

        Location = namedtuple('Location', ['lat', 'lon'])
        return Location(float(value.get('lat')), float(value.get('lon')))


class LinkField(BasicField):
    """
    LinkField

    Nothing should be done here as include resolution is handled within
    entries due to depth handling (explained within Entry).
    Only present as a placeholder for proper resolution within ContentType.
    """
    pass


class ArrayField(BasicField):
    """Array Coercion Class

    Coerces items in collection with it's proper Coercion Class.
    """

    def __init__(self, items=None):
        super(ArrayField, self).__init__(items)
        self._coercion = self._get_coercion()

    def coerce(self, value):
        """Coerces array items with proper coercion."""

        result = []
        for v in value:
            result.append(self._coercion.coerce(v))
        return result

    def _get_coercion(self):
        return globals()["{0}Field".format(self._items.get('type'))]()


class ObjectField(BasicField):
    """Object Coercion Class"""

    def coerce(self, value):
        """Coerces value to dict"""

        return dict(value)
