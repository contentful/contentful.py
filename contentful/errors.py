"""
contentful.errors
~~~~~~~~~~~~~~~~~

This module implements the Error classes.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/introduction/errors

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class HTTPError(Exception):
    """
    Base HTTP Error Class
    """

    def __init__(self, response):
        super(HTTPError, self).__init__(response.json()['message'])
        self.response = response
        self.status_code = response.status_code


class NotFoundError(HTTPError):
    """
    404
    """
    pass


class BadRequestError(HTTPError):
    """
    400
    """
    pass


class AccessDeniedError(HTTPError):
    """
    403
    """
    pass


class UnauthorizedError(HTTPError):
    """
    401
    """
    pass


class RateLimitExceededError(HTTPError):
    """
    429
    """
    pass


class ServerError(HTTPError):
    """
    500
    """
    pass


class ServiceUnavailableError(HTTPError):
    """
    503
    """
    pass


def get_error(response):
    """Gets Error by HTTP Status Code"""

    errors = {
        400: BadRequestError,
        401: UnauthorizedError,
        403: AccessDeniedError,
        404: NotFoundError,
        429: RateLimitExceededError,
        500: ServerError,
        503: ServiceUnavailableError
    }

    error_class = HTTPError
    if response.status_code in errors:
        error_class = errors[response.status_code]

    return error_class(response)
