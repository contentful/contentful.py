from __future__ import annotations

import contextlib
import urllib.parse
from typing import Iterator, Any

import requests

from contentful.client.transport import errors, abstract, retry

"""
contentful.client.transport.sio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides the implementation for communicating with the Contentful API over HTTP using synchronous IO.

Complete API Documentation: https://www.contentful.com/developers/docs/references/content-delivery-api/

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class SyncTransport(
    abstract.AbstractSyncTransport[requests.Session, requests.Response]
):
    retry_cls = retry.Retry

    def initialize(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()

        return self._session

    def close(self) -> None:
        if self._session is None:
            return
        try:
            self._session.close()
        finally:
            self._session = None

    def get(
        self,
        url: str,
        *,
        query: dict[str, Any] | None = None,
        session: requests.Response | None = None,
        raw_mode: bool = False,
        **headers: str,
    ) -> dict[str, Any] | requests.Response:
        response = self.retry(
            self._get, query=query, session=session, raw_mode=raw_mode, **headers
        )
        return response

    def _get(
        self,
        url: str,
        *,
        query: dict[str, Any] | None = None,
        session: requests.Response | None = None,
        raw_mode: bool = False,
        **headers: str,
    ) -> dict[str, Any] | requests.Response:
        qualified_url = urllib.parse.urljoin(self.base_url, url)
        sess: requests.Session
        with self.session(session=session) as sess:
            response: requests.Response
            with sess.get(qualified_url, params=query, headers=headers) as response:
                content = response.content
                status_code = response.status_code
                headers = response.headers
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

    @contextlib.contextmanager
    def session(
        self, *, session: requests.Session | None = None
    ) -> Iterator[requests.Session]:
        with translate_sync_transport_errors():
            if session is not None:
                yield session
                return

            session = self.initialize()
            yield session


@contextlib.contextmanager
def translate_sync_transport_errors() -> Iterator[None]:
    try:
        yield
    # Can't connect to the server.
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
    ) as e:
        raise errors.TransientHTTPError(e) from e
    # Malformed request, etc.
    except requests.exceptions.RequestException as e:
        raise errors.PermanentHTTPError(e) from e
