from __future__ import annotations

import abc
import http
import types
from typing import (
    Generic,
    Protocol,
    TypeVar,
    overload,
    Any,
    Literal,
    TypedDict,
    Mapping,
    ClassVar,
)

import orjson

from contentful.client.transport import errors, retry

"""
contentful.client.transport.abstract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides the abstract interface for communicating with the Contentful API over HTTP.

Complete API Documentation: https://www.contentful.com/developers/docs/references/content-delivery-api/

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


SessionT = TypeVar("SessionT")
ResponseT = TypeVar("ResponseT")


class AbstractTransport(abc.ABC, Generic[SessionT, ResponseT]):
    retry_cls: ClassVar[retry.BaseRetry]

    def __init__(
        self,
        *,
        base_url: str,
        timeout_s: int,
        proxy_info: ProxyInfo | None = None,
        default_headers: dict[str, str] | None = None,
        max_retries: int = 1,
        max_retry_wait_seconds: int = 60,
    ) -> None:
        self.base_url = base_url
        self.timeout_s = timeout_s
        self.proxy_info = proxy_info
        self.default_headers = default_headers
        self.max_retries = max_retries
        self.max_retry_wait_seconds = max_retry_wait_seconds
        self.retry = self.retry_cls(
            max_retries=max_retries, max_wait_seconds=max_retry_wait_seconds
        )
        self._session = None

    @abc.abstractmethod
    def initialize(self) -> SessionT: ...

    @abc.abstractmethod
    def close(self) -> None: ...

    @overload
    def get(
        self,
        url: str,
        *,
        query: dict[str, Any] | None = None,
        session: SessionT | None = None,
        raw_mode: Literal[False],
        **headers: str,
    ) -> dict[str, Any]: ...

    @overload
    def get(
        self,
        url: str,
        *,
        query: dict[str, Any] | None = None,
        session: SessionT | None = None,
        raw_mode: Literal[True],
        **headers: str,
    ) -> ResponseT: ...

    @abc.abstractmethod
    def get(
        self,
        url: str,
        *,
        query: dict[str, Any] | None = None,
        session: SessionT | None = None,
        raw_mode: bool = False,
        **headers: str,
    ) -> dict[str, Any] | ResponseT: ...


class AbstractAsyncTransport(
    AbstractTransport[SessionT, ResponseT], abc.ABC, Generic[SessionT, ResponseT]
):

    @abc.abstractmethod
    def session(
        self, *, session: SessionT | None = None
    ) -> AsyncSessionContext[SessionT]: ...


class AbstractSyncTransport(
    AbstractTransport[SessionT, ResponseT], abc.ABC, Generic[SessionT, ResponseT]
):

    @abc.abstractmethod
    def session(
        self, *, session: SessionT | None = None
    ) -> SyncSessionContext[SessionT]: ...


class AsyncSessionContext(Protocol[SessionT]):
    async def __aenter__(self) -> SessionT: ...

    @overload
    async def __aexit__(self, exc_type: None, exc_val: None, exc_tb: None): ...

    @overload
    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: types.TracebackType,
    ): ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ): ...


class SyncSessionContext(Protocol[SessionT]):

    def __enter__(self) -> SessionT: ...

    @overload
    def __exit__(self, exc_type: None, exc_val: None, exc_tb: None): ...

    @overload
    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: types.TracebackType,
    ): ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ): ...


class ProxyInfo(TypedDict):
    http: str | None
    https: str | None


@overload
def parse_response(
    *,
    status_code: int,
    reason: str | None,
    content: bytes,
    headers: Mapping[str, str],
    raw: ResponseT,
    raw_mode: Literal[True],
) -> ResponseT: ...


@overload
def parse_response(
    *,
    status_code: int,
    reason: str | None,
    content: bytes,
    headers: Mapping[str, str],
    raw: ResponseT,
    raw_mode: Literal[False],
) -> dict[str, Any]: ...


def parse_response(
    *,
    status_code: int,
    reason: str | None,
    content: bytes,
    headers: Mapping[str, str],
    raw: ResponseT,
    raw_mode: bool,
) -> ResponseT | dict[str, Any]:
    """Parse the received response, raising an error if necessary."""
    if status_code >= 400:
        if reason is None:
            reason = http.HTTPStatus(status_code).phrase

        err = errors.get_error_for_status_code(
            status_code,
            content=content,
            reason=reason,
            headers=headers,
        )
        raise err

    if raw_mode:
        # Read the data from the fd before closing the connection.
        return raw

    # Don't bother with .text/.json() since we know this is JSON.
    #   Passing the raw bytes to orjson will be much more efficient.
    body = orjson.loads(content)
    return body
