from __future__ import annotations

import contextlib
import gzip
import urllib.parse
from typing import AsyncIterator, Iterator, Any

import aiohttp

from contentful.client.transport import errors, abstract, retry

"""
contentful.client.transport.aio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides the implementation for communicating with the Contentful API over HTTP using asynchronous IO.

Complete API Documentation: https://www.contentful.com/developers/docs/references/content-delivery-api/

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class AsyncTransport(
    abstract.AbstractAsyncTransport[aiohttp.ClientSession, aiohttp.ClientResponse]
):
    retry_cls = retry.AsyncRetry

    async def initialize(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout_s),
                headers=self.default_headers,
                auto_decompress=True,
            )

        return self._session

    async def close(self) -> None:
        if self._session is None:
            return
        try:
            await self._session.close()
        finally:
            self._session = None

    async def get(
        self,
        url: str,
        *,
        query: dict[str, Any] | None = None,
        session: aiohttp.ClientSession | None = None,
        raw_mode: bool = False,
        **headers: str,
    ) -> dict[str, Any] | aiohttp.ClientResponse:
        response = await self.retry(
            self._get, url, query=query, session=session, raw_mode=raw_mode, **headers
        )
        return response

    async def _get(
        self,
        url: str,
        *,
        query: dict[str, Any] | None = None,
        session: aiohttp.ClientSession | None = None,
        raw_mode: bool = False,
        **headers: str,
    ) -> dict[str, Any] | aiohttp.ClientResponse:
        url = urllib.parse.urljoin(self.base_url, url)
        async with self.session(session=session) as sess:
            response: aiohttp.ClientResponse
            async with sess.get(url, params=query, headers=headers) as response:
                content = await response.read()
                status_code = response.status
                headers = response.headers
                # For some reason aiohttp is failing to auto-decompress these.
                if headers.get("Content-Encoding") == "gzip":
                    try:
                        content = gzip.decompress(content)
                    except gzip.BadGzipFile:
                        pass

                reason = response.reason
                parsed = abstract.parse_response(
                    status_code=status_code,
                    reason=reason,
                    content=content,
                    headers=headers,
                    raw=response,
                    raw_mode=raw_mode,
                )
                return parsed

    @contextlib.asynccontextmanager
    async def session(
        self, *, session: aiohttp.ClientSession | None = None
    ) -> AsyncIterator[aiohttp.ClientSession]:
        with translate_async_transport_errors():
            if session is not None:
                yield session
                return

            session = await self.initialize()
            yield session


@contextlib.contextmanager
def translate_async_transport_errors() -> Iterator[None]:
    try:
        yield
    # Can't connect to the Server
    except aiohttp.ClientConnectionError as e:
        raise errors.TransientHTTPError(str(e)) from e
    # Malformed request, etc.
    except (aiohttp.ClientError, ValueError) as e:
        raise errors.PermanentHTTPError(e) from e
