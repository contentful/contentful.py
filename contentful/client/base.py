from __future__ import annotations

import platform
import re
from typing import TypedDict, TYPE_CHECKING, ClassVar

from contentful import resource_builder
from contentful.client import queries
from contentful.client.transport import abstract

if TYPE_CHECKING:
    from typing import TypeAlias, Any
    from contentful.resource import Resource

    QueryT: TypeAlias = dict[str, Any]


"""
contentful.client.base
~~~~~~~~~~~~~~~~~~~~~~

This module provides the base implementation for the Contentful API Client.

Complete API Documentation: https://www.contentful.com/developers/docs/references/content-delivery-api/

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""

__all__ = ("BaseClient", "ConfigurationException")


class BaseClient:
    """Constructs the API Client.

    :param space_id: Space ID of your target space.
    :param access_token: API Access Token (Delivery by default,
        Preview if overriding api_url).
    :param api_url: (optional) URL of the Contentful Target API,
        defaults to Delivery API (can be overriden for Preview API).
    :param api_version: (optional) Target version of the Contentful API.
    :param default_locale: (optional) Default Locale for your Space,
        defaults to 'en-US'.
    :param environment: (optional) Default Environment for client, defaults
        to 'master'.
    :param https: (optional) Boolean determining wether to use https
        or http, defaults to True.
    :param authorization_as_header: (optional) Boolean determining wether
        to send access_token through a header or via GET params,
        defaults to True.
    :param raw_mode: (optional) Boolean determining wether to process the
        response or return it raw after each API call, defaults to False.
    :param gzip_encoded: (optional) Boolean determining wether to accept
        gzip encoded results, defaults to True.
    :param raise_errors: (optional) Boolean determining wether to raise
        an exception on requests that aren't successful, defaults to True.
    :param content_type_cache: (optional) Boolean determining wether to
        store a Cache of the Content Types in order to properly coerce
        Entry fields, defaults to True.
    :param reuse_entries: (optional) Boolean determining wether to reuse
        hydrated Entry and Asset objects within the same request when possible.
        Defaults to False
    :param timeout_s: (optional) Max time allowed for each API call, in seconds.
        Defaults to 1s.
    :param proxy_host: (optional) URL for Proxy, defaults to None.
    :param proxy_port: (optional) Port for Proxy, defaults to None.
    :param proxy_username: (optional) Username for Proxy, defaults to None.
    :param proxy_password: (optional) Password for Proxy, defaults to None.
    :param max_rate_limit_retries: (optional) Maximum amount of retries
        after RateLimitError, defaults to 1.
    :param max_rate_limit_wait: (optional) Timeout (in seconds) for waiting
        for retry after RateLimitError, defaults to 60.
    :param max_include_resolution_depth: (optional) Maximum include resolution
        level for Resources, defaults to 20 (max include level * 2).
    :param application_name: (optional) User application name, defaults to None.
    :param application_version: (optional) User application version, defaults to None.
    :param integration_name: (optional) Integration name, defaults to None.
    :param integration_version: (optional) Integration version, defaults to None.
    :return: :class:`Client <Client>` object.
    :rtype: contentful.Client

    Usage:

        >>> import contentful
        >>> client = contentful.Client('cfexampleapi', 'b4c0n73n7fu1')
        <contentful.Client space_id="cfexampleapi"
          access_token="b4c0n73n7fu1"
          default_locale="en-US">
    """

    transport_cls: ClassVar[type[abstract.AbstractTransport]]

    def __init__(
        self,
        space_id: str,
        access_token: str,
        api_url: str = "cdn.contentful.com",
        api_version: int = 1,
        default_locale: str = "en-US",
        environment: str = "master",
        https: bool = True,
        authorization_as_header: bool = True,
        raw_mode: bool = False,
        gzip_encoded: bool = True,
        raise_errors: bool = True,
        content_type_cache: bool = True,
        reuse_entries: bool = False,
        timeout_s: int = 1,
        proxy_host: str | None = None,
        proxy_port: str | None = None,
        proxy_username: str | None = None,
        proxy_password: str | None = None,
        max_rate_limit_retries: str | None = 1,
        max_rate_limit_wait: int = 60,
        max_include_resolution_depth: int = 20,
        application_name: str | None = None,
        application_version: str | None = None,
        integration_name: str | None = None,
        integration_version: str | None = None,
    ):
        self.space_id = space_id
        self.access_token = access_token
        self.api_url = api_url
        self.api_version = api_version
        self.default_locale = default_locale
        self.environment = environment
        self.https = https
        self.authorization_as_header = authorization_as_header
        self.raw_mode = raw_mode
        self.gzip_encoded = gzip_encoded
        self.raise_errors = raise_errors
        self.content_type_cache = content_type_cache
        self.reuse_entries = reuse_entries
        self.timeout_s = timeout_s
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.max_rate_limit_retries = max_rate_limit_retries
        self.max_rate_limit_wait = max_rate_limit_wait
        self.max_include_resolution_depth = max_include_resolution_depth
        self.application_name = application_name
        self.application_version = application_version
        self.integration_name = integration_name
        self.integration_version = integration_version
        self._validate_configuration()
        self._headers = None
        self._client_info = None
        self._proxy_info = None
        self._transport = None

    def initialize(self):
        raise NotImplementedError()

    def _get(self, url: str, query: QueryT | None = None):
        """
        Wrapper for the HTTP Request,
        Rate Limit Backoff is handled here,
        Responses are Processed with ResourceBuilder.
        """
        raise NotImplementedError()

    def _cache_content_types(self):
        """
        Updates the Content Type Cache.
        """

        raise NotImplementedError()

    @property
    def client_info(self) -> ClientInfo:
        if self._client_info is None:
            self._client_info = self._get_client_info()

        return self._client_info

    @property
    def headers(self) -> dict[str, str]:
        if self._headers is None:
            self._headers = self._request_headers()

        return self._headers

    @property
    def proxy_info(self) -> abstract.ProxyInfo:
        if self._proxy_info is None:
            self._proxy_info = self._proxy_parameters()

        return self._proxy_info

    @property
    def transport(self) -> abstract.AbstractTransport:
        if self._transport is None:
            self._transport = self._get_transport()

        return self._transport

    def qualified_url(self) -> str:
        scheme = "https" if self.https else "http"
        hostname = self.api_url
        if hostname.startswith("http"):
            scheme = ""

        path = f"/spaces/{self.space_id}/environments/{self.environment}/"
        url = f"{scheme}://{hostname}{path}"
        return url

    def _get_transport(self) -> abstract.AbstractTransport:
        base_url = self.qualified_url()
        transport = self.transport_cls(
            base_url=base_url,
            timeout_s=self.timeout_s,
            proxy_info=self.proxy_info,
            default_headers=self.headers,
            max_retries=self.max_rate_limit_retries,
            max_retry_wait_seconds=self.max_rate_limit_wait,
        )
        return transport

    def _get_client_info(self) -> ClientInfo:
        from contentful import __version__

        os_name = platform.system()
        if os_name == "Darwin":
            os_name = "macOS"
        elif not os_name or os_name == "Java":
            os_name = None
        elif os_name and os_name not in ("macOS", "Windows"):
            os_name = "Linux"

        return ClientInfo(
            sdk=VersionInfo(name="contentful.py", version=__version__),
            platform=VersionInfo(name="python", version=platform.python_version()),
            app=VersionInfo(
                name=self.application_name, version=self.application_version
            ),
            integration=VersionInfo(
                name=self.integration_name, version=self.integration_version
            ),
            os=VersionInfo(name=os_name, version=platform.release()),
        )

    def _validate_configuration(self):
        """
        Validates that required parameters are present.
        """

        if not self.space_id:
            raise ConfigurationException(
                "You will need to initialize a client with a Space ID"
            )
        if not self.access_token:
            raise ConfigurationException(
                "You will need to initialize a client with an Access Token"
            )
        if not self.api_url:
            raise ConfigurationException(
                "The client configuration needs to contain an API URL"
            )
        if not self.default_locale:
            raise ConfigurationException(
                "The client configuration needs to contain a Default Locale"
            )
        if not self.api_version or self.api_version < 1:
            raise ConfigurationException("The API Version must be a positive number")

    def _contentful_user_agent(self):
        """
        Sets the X-Contentful-User-Agent header.
        """

        header_encoded = ""
        for key, values in self.client_info.items():
            if values["name"] is None:
                continue

            name = f"{key} {values['name']}"
            if values["version"]:
                name = f"{name}/{values['version']}"
            header_encoded += f"{name}; "

        return header_encoded.rstrip(" ")

    def _request_headers(self):
        """
        Sets the default Request Headers.
        """

        headers = {
            "X-Contentful-User-Agent": self._contentful_user_agent(),
            "Content-Type": f"application/vnd.contentful.delivery.v{self.api_version}+json",
            "Accept-Encoding": "gzip" if self.gzip_encoded else "identity",
        }

        if self.authorization_as_header:
            headers["Authorization"] = f"Bearer {self.access_token}"

        return headers

    def _url(self, url):
        """
        Creates the Request URL.
        """

        protocol = "https" if self.https else "http"
        return "{0}://{1}/spaces/{2}{3}".format(
            protocol, self.api_url, self.space_id, url
        )

    def _format_params(self, query: QueryT | None) -> dict[str, str]:
        query = query or {}
        params = queries.normalize(**query)
        if not self.authorization_as_header:
            params["access_token"] = self.access_token

        return params

    def _format_response(
        self, *, response: dict[str, Any], query: dict[str, str]
    ) -> Resource:
        localized = query.get("locale", "") == "*"
        builder = resource_builder.ResourceBuilder(
            default_locale=self.default_locale,
            localized=localized,
            json=response,
            max_depth=self.max_include_resolution_depth,
            reuse_entries=self.reuse_entries,
        )
        return builder.build()

    def _has_proxy(self) -> bool:
        """
        Checks if a Proxy was set.
        """

        return self.proxy_host is not None

    def _proxy_parameters(self) -> abstract.ProxyInfo:
        """
        Builds Proxy parameters Dict from
        client options.
        """
        if not self._has_proxy():
            return {"http": None, "https": None}

        proxy_protocol = "https" if self.proxy_host.startswith("https") else "http"
        proxy = f"{proxy_protocol}://"
        if self.proxy_username and self.proxy_password:
            proxy += f"{self.proxy_username}:{self.proxy_password}@"

        proxy += re.sub(r"https?(://)?", "", self.proxy_host)

        if self.proxy_port:
            proxy += f":{self.proxy_port}"

        return {"http": proxy, "https": proxy}

    def __repr__(self):
        return (
            f"<contentful.{self.__class__.__name__} "
            f"space_id={self.space_id!r} "
            f"access_token={self.access_token!r} "
            f"default_locale={self.default_locale!r}>"
        )


class ClientInfo(TypedDict):
    sdk: VersionInfo
    platform: VersionInfo
    app: VersionInfo
    integration: VersionInfo
    os: VersionInfo


class VersionInfo(TypedDict):
    name: str
    version: str | int | None


class ConfigurationException(Exception):
    """Configuration Error Class"""

    pass
