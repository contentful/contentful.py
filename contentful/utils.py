import re

import logging

"""
contentful.utils
~~~~~~~~~~~~~~~~

This module implements utilities.

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger(__name__)


def snake_case(a_string):
    """Returns a snake cased version of a string.

    :param a_string: any :class:`str` object.

    Usage:
        >>> snake_case('FooBar')
        "foo_bar"
    """

    partial = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', a_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', partial).lower()


def is_link(value):
    """Checks if value is link or not.

    :param value: any object.
    :return: Boolean
    :rtype: bool

    Usage:
        >>> is_link('foo')
        False
        >>> is_link({'sys': {'type': 'Link', 'id': 'foobar'}})
        True
    """

    return (
        isinstance(value, dict) and
        value.get('sys', {}).get('type', '') == 'Link'
    )


def is_link_array(value):
    """Checks if value is an array of links.

    :param value: any object.
    :return: Boolean
    :rtype: bool

    Usage:
        >>> is_link_array('foo')
        False
        >>> is_link_array([1, 2, 3])
        False
        >>> is_link([{'sys': {'type': 'Link', 'id': 'foobar'}}])
        True
    """

    if isinstance(value, list) and len(value) > 0:
        return is_link(value[0])
    return False


def unresolvable(item, errors):
    if not item:
        return True

    for error in errors:
        if error.get('details', {}).get('id', None) == item['sys']['id']:
            return True
    return False


def resource_for_link(link, includes, resources=None, locale=None):
    """Returns the resource that matches the link"""

    if resources is not None:
        cache_key = "{0}:{1}:{2}".format(
            link['sys']['linkType'],
            link['sys']['id'],
            locale
        )
        if cache_key in resources:
            return resources[cache_key]

    for i in includes:
        if (i['sys']['id'] == link['sys']['id'] and
                i['sys']['type'] == link['sys']['linkType']):
            return i
    return None
