from __future__ import annotations

from unittest import TestCase
from contentful import client
from contentful.client.transport import errors
from contentful.client.transport.compat import json as mod_json


class MockResponse(object):
    def __init__(
        self,
        status_code: int,
        json: dict | list | str,
        headers: dict | None = None,
        invalid_json: bool = False,
    ):
        self.status_code = status_code
        self._json = json.encode() if isinstance(json, str) else mod_json.dumps(json)
        if isinstance(self._json, str):
            self._json = self._json.encode()
        self._invalid_json = invalid_json
        self.headers = headers if headers is not None else {}

    def json(self):
        if self._invalid_json:
            raise mod_json.JSONDecodeError("foo", "foo", 0)
        return mod_json.loads(self._json)

    @property
    def content(self) -> bytes:
        return self._json

    @property
    def text(self):
        return self._json.decode()


http_attempts = 0


def mock_http_call(url: str, query: dict) -> str:
    global http_attempts
    if http_attempts < query.get("fail_until", 1):
        http_attempts += 1
        error = errors.get_error_for_status_code(
            status_code=429,
            content=b'{"message": "foo"}',
            headers={"x-contentful-ratelimit-reset": query.get("reset", 0.1)},
        )
        raise error
    return "succeed"


class ErrorsTest(TestCase):
    def test_default_additional_info_is_empty(self):
        error = errors.get_error_for_status_code(
            512,
            content=b"not json",
        )
        self.assertEqual(error._additional_error_info(), [])

    def test_default_error_message(self):
        error = errors.get_error_for_status_code(
            512,
            content=b"not json",
        )

        expected_error = "\n".join(
            [
                "HTTP status code: 512",
                "Message: The following error was received: not json",
            ]
        )
        self.assertEqual(str(error), expected_error)

    def test_generic_details(self):
        error = errors.get_error_for_status_code(
            512,
            content=b'{"details":"some text"}',
        )

        expected_error = "\n".join(
            [
                "HTTP status code: 512",
                'Message: The following error was received: {"details":"some text"}',
                "Details: some text",
            ]
        )
        self.assertEqual(str(error), expected_error)

    def test_not_found_error(self):
        response = MockResponse(
            404,
            {
                "message": "The resource could not be found.",
                "details": {"type": "Asset", "id": "foobar"},
                "requestId": "$foobar123",
            },
        )

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 404)
        expected_error = "\n".join(
            [
                "HTTP status code: 404",
                "Message: The resource could not be found.",
                "Details: The requested Asset could not be found. ID: foobar.",
                "Request ID: $foobar123",
            ]
        )
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.NotFoundError))

    def test_not_found_error_with_sys_on_details(self):
        response = MockResponse(
            404,
            {
                "message": "The resource could not be found.",
                "details": {"sys": {"type": "Space", "id": "foobar"}},
                "requestId": "$foobar123",
            },
        )

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 404)
        expected_error = "\n".join(
            [
                "HTTP status code: 404",
                "Message: The resource could not be found.",
                "Details: The requested Space could not be found. ID: foobar.",
                "Request ID: $foobar123",
            ]
        )
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.NotFoundError))

    def test_not_found_error_details_is_a_string(self):
        response = MockResponse(
            404,
            {
                "message": "The resource could not be found.",
                "details": "The resource could not be found",
                "requestId": "$foobar123",
            },
        )

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 404)
        expected_error = "\n".join(
            [
                "HTTP status code: 404",
                "Message: The resource could not be found.",
                "Details: The resource could not be found",
                "Request ID: $foobar123",
            ]
        )
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.NotFoundError))

    def test_bad_request_error(self):
        response = MockResponse(
            400,
            {
                "message": "The query you sent was invalid. Probably a filter or ordering specification is not applicable to the type of a field.",
                "details": {
                    "errors": [
                        {"details": 'The path "invalid_param" is not recognized'}
                    ]
                },
                "requestId": "$foobar234",
            },
        )

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 400)
        expected_error = "\n".join(
            [
                "HTTP status code: 400",
                "Message: The query you sent was invalid. Probably a filter or ordering specification is not applicable to the type of a field.",
                'Details: The path "invalid_param" is not recognized',
                "Request ID: $foobar234",
            ]
        )
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.BadRequestError))

    def test_bad_request_error_details_is_string(self):
        response = MockResponse(
            400,
            {
                "message": "The query you sent was invalid. Probably a filter or ordering specification is not applicable to the type of a field.",
                "details": "some error",
                "requestId": "$foobar234",
            },
        )

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 400)
        expected_error = "\n".join(
            [
                "HTTP status code: 400",
                "Message: The query you sent was invalid. Probably a filter or ordering specification is not applicable to the type of a field.",
                "Details: some error",
                "Request ID: $foobar234",
            ]
        )
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.BadRequestError))

    def test_bad_request_error_errors_details_is_string(self):
        response = MockResponse(
            400,
            {
                "message": "The query you sent was invalid. Probably a filter or ordering specification is not applicable to the type of a field.",
                "details": {"errors": ["some error"]},
                "requestId": "$foobar234",
            },
        )

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 400)
        expected_error = "\n".join(
            [
                "HTTP status code: 400",
                "Message: The query you sent was invalid. Probably a filter or ordering specification is not applicable to the type of a field.",
                "Details: some error",
                "Request ID: $foobar234",
            ]
        )
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.BadRequestError))

    def test_access_denied_error(self):
        response = MockResponse(
            403, {"message": "Access Denied", "details": {"reasons": ["foo", "bar"]}}
        )

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 403)
        expected_error = "\n".join(
            [
                "HTTP status code: 403",
                "Message: Access Denied",
                "Details: ",
                "\tReasons:",
                "\t\tfoo",
                "\t\tbar",
            ]
        )
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.AccessDeniedError))

    def test_unauthorized_error(self):
        response = MockResponse(
            401,
            {
                "message": "The access token you sent could not be found or is invalid.",
                "requestId": "$foobar123",
            },
        )

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 401)
        expected_error = "\n".join(
            [
                "HTTP status code: 401",
                "Message: The access token you sent could not be found or is invalid.",
                "Request ID: $foobar123",
            ]
        )
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.UnauthorizedError))

    def test_rate_limit_exceeded_error(self):
        response = MockResponse(429, {"message": "Rate Limit Exceeded"})

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 429)
        expected_error = "\n".join(
            ["HTTP status code: 429", "Message: Rate Limit Exceeded"]
        )
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.RateLimitExceededError))

    def test_rate_limit_exceeded_error_with_time(self):
        response = MockResponse(429, {}, headers={"x-contentful-ratelimit-reset": 60})

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 429)
        expected_error = "\n".join(
            [
                "HTTP status code: 429",
                "Message: Rate limit exceeded. Too many requests.",
                "Time until reset (seconds): 60",
            ]
        )
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.RateLimitExceededError))

    def test_server_error(self):
        response = MockResponse(500, {"message": "Server Error"})

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 500)
        expected_error = "\n".join(["HTTP status code: 500", "Message: Server Error"])
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.ServerError))

    def test_service_unavailable_error(self):
        response = MockResponse(503, {"message": "Service Unavailable"})

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 503)
        expected_error = "\n".join(
            ["HTTP status code: 503", "Message: Service Unavailable"]
        )
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.ServiceUnavailableError))

    def test_other_error(self):
        response = MockResponse(418, {"message": "I'm a Teapot"})

        error = errors.get_error_for_status_code(
            response.status_code,
            content=response.content,
            headers=response.headers,
        )

        self.assertEqual(error.response.status_code, 418)
        expected_error = "\n".join(["HTTP status code: 418", "Message: I'm a Teapot"])
        self.assertEqual(str(error), expected_error)
        self.assertTrue(isinstance(error, errors.HTTPError))

    def test_rate_limit_retries(self):
        global http_attempts
        client_ = client.Client(
            "cfexampleapi", "b4c0n73n7fu1", content_type_cache=False
        )

        http_attempts = 0
        result = client_.transport.retry(mock_http_call, url="/foo", query={})

        self.assertEqual(http_attempts, 1)
        self.assertEqual(result, "succeed")

    def test_rate_limit_max_retries(self):
        global http_attempts
        client_ = client.Client(
            "cfexampleapi", "b4c0n73n7fu1", content_type_cache=False
        )

        http_attempts = 0
        with self.assertRaises(errors.RateLimitExceededError):
            client_.transport.retry(mock_http_call, url="/foo", query={"fail_until": 2})

    def test_rate_limit_max_wait(self):
        global http_attempts
        client_ = client.Client(
            "cfexampleapi", "b4c0n73n7fu1", content_type_cache=False
        )

        http_attempts = 0
        with self.assertRaises(
            errors.RateLimitExceededError,
        ):
            client_.transport.retry(mock_http_call, url="/foo", query={"reset": 100})

    def test_predefined_errors_default_message(self):
        messages = {
            400: "The request was malformed or missing a required parameter.",
            401: "The authorization token was invalid.",
            403: "The specified token does not have access to the requested resource.",
            404: "The requested resource or endpoint could not be found.",
            429: "Rate limit exceeded. Too many requests.",
            500: "Internal server error.",
            502: "The requested space is hibernated.",
            503: "The request was malformed or missing a required parameter.",
        }

        for status_code, message in messages.items():
            response = MockResponse(status_code, "foo", invalid_json=True)

            error = errors.get_error_for_status_code(
                response.status_code,
                content=response.content,
                headers=response.headers,
            )

            expected_error = "\n".join(
                [
                    "HTTP status code: {0}".format(status_code),
                    "Message: {0}".format(message),
                ]
            )
            self.assertEqual(str(error), expected_error)
