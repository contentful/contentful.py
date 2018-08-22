import re
import sys
import time
import json
from random import uniform
from .errors import RateLimitExceededError

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

"""
contentful.utils
~~~~~~~~~~~~~~~~

This module implements utilities.

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


logging.getLogger(__name__).addHandler(NullHandler())
log = logging.getLogger(__name__)


def unicode_class():
    """Returns the class that allows for unicode encoded strings
    depends on the Python version."""

    if sys.version_info[0] >= 3:
        return str
    return unicode  # noqa: F821


def string_class():
    """Returns the parent class for strings
    depends on the Python version."""
    if sys.version_info[0] >= 3:
        return str
    return basestring  # noqa: F821


def json_error_class():
    """Returns the class for JSON decode errors
    depends on the Python version."""
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 5:
        return json.JSONDecodeError
    return ValueError


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


class ConfigurationException(Exception):
    """Configuration Error Class"""
    pass


class NotSupportedException(Exception):
    """This exception is thrown when something is not supported by the API."""
    pass


class retry_request(object):
    """
    Decorator to retry function calls in case they raise rate limit exceptions
    """

    def __init__(self, client):
        self.client = client

    def __call__(self, http_call):
        def wrapper(url, query=None):
            exception = None
            for i in range(self.client.max_rate_limit_retries + 1):
                try:
                    return http_call(url, query)
                except RateLimitExceededError as error:
                    exception = error
                    reset_time = error.reset_time()

                    if reset_time > self.client.max_rate_limit_wait:
                        raise error

                    retry_message = 'Contentful API Rate Limit Hit! '
                    retry_message += "Retrying - Retries left: {0} ".format(
                        self.client.max_rate_limit_retries - i
                    )
                    retry_message += "- Time until reset (seconds): {0}".format(
                        reset_time
                    )
                    log.debug(retry_message)
                    time.sleep(reset_time * uniform(1.0, 1.2))
            if exception is not None:
                raise exception
        return wrapper
