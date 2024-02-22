from __future__ import annotations

import dataclasses

"""
contentful.client.transport.errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the Error classes.

API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/introduction/errors

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


__all__ = (
    "get_error_for_status_code",
    "HTTPError",
    "PermanentHTTPError",
    "BadRequestError",
    "UnauthorizedError",
    "AccessDeniedError",
    "NotFoundError",
    "EntryNotFoundError",
    "TransientHTTPError",
    "RateLimitExceededError",
    "ServerError",
    "BadGatewayError",
    "ServiceUnavailableError",
    "ErrorResponseInfo",
)


def get_error_for_status_code(
    status_code, *, default: type[HTTPError] | None = None
) -> type[HTTPError]:
    default = default or PermanentHTTPError
    return _HTTP_STATUS_TO_ERROR_MAP.get(status_code, default)


class HTTPError(Exception):
    response: ErrorResponseInfo

    def __init__(
        self, message: str | None = None, *, response: ErrorResponseInfo = None
    ):
        self.response = response or ErrorResponseInfo()
        message = message or self._best_available_message()
        super().__init__(message)

    def _default_error_message(self) -> str:
        return f"The following error was received: {self.response.content}"

    def _handle_details(self, details: list[dict] | str) -> str:
        return f"{details}"

    def _has_additional_error_info(self):
        return False

    def _additional_error_into(self) -> list[str]:
        return []

    def _best_available_message(self) -> str:
        message = self.response.body.get("message")
        details = self.response.body.get("details")
        request_id = self.response.body.get("requestId")
        status_str = (
            f"HTTP status code: {self.response.status_code}"
            if self.response.status_code
            else None
        )
        message_str = f"Message: {message or self._default_error_message()}"
        details_str = f"Details: {self._handle_details(details)}" if details else None
        request_id_str = f"RequestId: {request_id}" if request_id else None

        messages = (
            status_str,
            message_str,
            details_str,
            request_id_str,
            *self._additional_error_into(),
        )
        error_message = "\n".join(s for s in messages if s is not None)
        return error_message


class PermanentHTTPError(HTTPError): ...


class BadRequestError(PermanentHTTPError):

    def _default_error_message(self) -> str:
        return "The request was malformed or missing a required parameter."

    def _handle_details(self, details: list[dict | str] | str) -> str:
        if isinstance(details, str):
            return details

        gen = (
            s
            for d in details
            if (s := (d if isinstance(d, str) else d.get("details"))) is not None
        )
        formatted = "\n\t".join(gen)
        return formatted


class UnauthorizedError(PermanentHTTPError):

    def _default_error_message(self) -> str:
        return "The authorization token was invalid"


class AccessDeniedError(PermanentHTTPError):
    def _default_error_message(self) -> str:
        return "The specified token does not have access to the requested resource."

    def _handle_details(self, details: dict) -> str:
        return "\n\tReasons:\n\t\t{0}".format("\n\t\t".join(details["reasons"]))


class NotFoundError(PermanentHTTPError):
    def _default_error_message(self) -> str:
        return "The requested resource or endpoint could not be found"

    def _handle_details(self, details: dict | str) -> str:
        if isinstance(details, str):
            return details

        if "sys" in details:
            resource_type = details["sys"].get("type", None)
            resource_id = details["sys"].get("id", None)
        else:
            resource_type = details["type"]
            resource_id = details.get("id", None)

        message = f"The requested {resource_type} could not be found."
        if resource_id is not None:
            message += f" ID: {resource_id}."

        return message


class EntryNotFoundError(NotFoundError): ...


class TransientHTTPError(HTTPError):

    def reset_time(self) -> int:
        return 1


class RateLimitExceededError(TransientHTTPError):

    RATE_LIMIT_RESET_HEADER_KEY = "x-contentful-ratelimit-reset"

    def reset_time(self) -> int:
        """Returns the reset time in seconds until next available request."""
        if not self._has_reset_time():
            return super().reset_time()

        return int(self.response.headers[self.RATE_LIMIT_RESET_HEADER_KEY])

    def _has_reset_time(self) -> bool:
        return self.RATE_LIMIT_RESET_HEADER_KEY in self.response.headers

    def _has_additional_error_info(self) -> bool:
        return self._has_reset_time()

    def _additional_error_info(self) -> bool:
        if not self._has_additional_error_info():
            return []

        return [f"Time until reset (seconds): {self.reset_time()}"]

    def _default_error_message(self):
        return "Rate limit exceeded. Too many requests."


class ServerError(TransientHTTPError):
    def _default_error_message(self) -> str:
        return "Internal server error."


class BadGatewayError(TransientHTTPError):

    def _default_error_message(self) -> str:
        return "The requested space is hibernated"


class ServiceUnavailableError(TransientHTTPError):
    def _default_error_message(self) -> str:
        return "The request was malformed or missing a required parameter."


@dataclasses.dataclass
class ErrorResponseInfo:
    status_code: int = 0
    reason: str = "Unknown error"
    headers: dict = dataclasses.field(default_factory=dict)
    content: str = ""
    body: dict = dataclasses.field(default_factory=dict)


_HTTP_STATUS_TO_ERROR_MAP = {
    # User error, treat as "permanent" to not trigger unnecessary retries.
    400: BadRequestError,
    401: UnauthorizedError,
    403: AccessDeniedError,
    404: NotFoundError,
    # Server errors, treat as "transient" to allow for retries.
    429: RateLimitExceededError,
    499: ServiceUnavailableError,
    500: ServerError,
    502: BadGatewayError,
    503: ServiceUnavailableError,
}
