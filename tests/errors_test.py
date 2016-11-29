from unittest import TestCase
from contentful.errors import (
    HTTPError,
    NotFoundError,
    BadRequestError,
    AccessDeniedError,
    UnauthorizedError,
    RateLimitExceededError,
    ServerError,
    ServiceUnavailableError,
    get_error
)
from contentful.utils import retry_request
from contentful.client import Client


class MockResponse(object):
    def __init__(self, status_code, json, headers=None):
        self.status_code = status_code
        self._json = json
        self.headers = headers if headers is not None else {}

    def json(self):
        return self._json


http_attempts = 0
def mock_http_call(url, query):
    global http_attempts
    if http_attempts < query.get('fail_until', 1):
        http_attempts += 1
        raise RateLimitExceededError(
            MockResponse(429, {'message': 'foo'}, headers={'x-contentful-ratelimit-reset': query.get('reset', 0.1)})
        )
    return 'succeed'


class ErrorsTest(TestCase):
    def test_not_found_error(self):
        response = MockResponse(404, {
            'message': 'Resource not Found'
        })

        error = get_error(response)

        self.assertEqual(error.status_code, 404)
        self.assertEqual(str(error), 'Resource not Found')
        self.assertTrue(isinstance(error, NotFoundError))

    def test_bad_request_error(self):
        response = MockResponse(400, {
            'message': 'Bad Request'
        })

        error = get_error(response)

        self.assertEqual(error.status_code, 400)
        self.assertEqual(str(error), 'Bad Request')
        self.assertTrue(isinstance(error, BadRequestError))

    def test_access_denied_error(self):
        response = MockResponse(403, {
            'message': 'Access Denied'
        })

        error = get_error(response)

        self.assertEqual(error.status_code, 403)
        self.assertEqual(str(error), 'Access Denied')
        self.assertTrue(isinstance(error, AccessDeniedError))

    def test_unauthorized_error(self):
        response = MockResponse(401, {
            'message': 'Unauthorized'
        })

        error = get_error(response)

        self.assertEqual(error.status_code, 401)
        self.assertEqual(str(error), 'Unauthorized')
        self.assertTrue(isinstance(error, UnauthorizedError))

    def test_rate_limit_exceeded_error(self):
        response = MockResponse(429, {
            'message': 'Rate Limit Exceeded'
        })

        error = get_error(response)

        self.assertEqual(error.status_code, 429)
        self.assertEqual(str(error), 'Rate Limit Exceeded')
        self.assertTrue(isinstance(error, RateLimitExceededError))

    def test_server_error(self):
        response = MockResponse(500, {
            'message': 'Server Error'
        })

        error = get_error(response)

        self.assertEqual(error.status_code, 500)
        self.assertEqual(str(error), 'Server Error')
        self.assertTrue(isinstance(error, ServerError))

    def test_service_unavailable_error(self):
        response = MockResponse(503, {
            'message': 'Service Unavailable'
        })

        error = get_error(response)

        self.assertEqual(error.status_code, 503)
        self.assertEqual(str(error), 'Service Unavailable')
        self.assertTrue(isinstance(error, ServiceUnavailableError))

    def test_other_error(self):
        response = MockResponse(418, {
            'message': "I'm a Teapot"
        })

        error = get_error(response)

        self.assertEqual(error.status_code, 418)
        self.assertEqual(str(error), "I'm a Teapot")
        self.assertTrue(isinstance(error, HTTPError))

    def test_rate_limit_retries(self):
        global http_attempts
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        http_attempts = 0
        result = retry_request(client)(mock_http_call)('/foo', {})

        self.assertEqual(http_attempts, 1)
        self.assertEqual(result, 'succeed')

    def test_rate_limit_max_retries(self):
        global http_attempts
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        http_attempts = 0
        self.assertRaises(RateLimitExceededError, retry_request(client)(mock_http_call), '/foo', {'fail_until': 2})

    def test_rate_limit_max_wait(self):
        global http_attempts
        client = Client('cfexampleapi', 'b4c0n73n7fu1', content_type_cache=False)

        http_attempts = 0
        self.assertRaises(RateLimitExceededError, retry_request(client)(mock_http_call), '/foo', {'reset': 100})
