import requests
import sys
from re import sub
from .utils import ConfigurationException, retry_request
from .errors import get_error, RateLimitExceededError, EntryNotFoundError
from .resource_builder import ResourceBuilder
from .content_type_cache import ContentTypeCache


"""
contentful.client
~~~~~~~~~~~~~~~~~

This module implements the Contentful Delivery API Client,
allowing interaction with every method present in it.

Complete API Documentation: https://www.contentful.com/developers/docs/references/content-delivery-api/

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


class Client(object):
    """Constructs the API Client.

    :param space_id: Space ID of your target space.
    :param access_token: API Access Token (Delivery by default,
        Preview if overriding api_url).
    :param api_url: (optional) URL of the Contentful Target API,
        defaults to Delivery API (can be overriden for Preview API).
    :param api_version: (optional) Target version of the Contentful API.
    :param default_locale: (optional) Default Locale for your Space,
        defaults to 'en-US'.
    :param https: (optional) Boolean determining wether to use https
        or http, defaults to True.
    :param authorization_as_header: (optional) Boolean determining wether
        to send access_token through a header or via GET params,
        defaults to True.
    :param raw_mode: (optional) Boolean determining wether to process the
        response or return it raw after each API call, defaults to True.
    :param gzip_encoded: (optional) Boolean determining wether to accept
        gzip encoded results, defaults to True.
    :param raise_errors: (optional) Boolean determining wether to raise
        an exception on requests that aren't successful, defaults to True.
    :param content_type_cache: (optional) Boolean determining wether to
        store a Cache of the Content Types in order to properly coerce
        Entry fields, defaults to True.
    :param proxy_host: (optional) URL for Proxy, defaults to None.
    :param proxy_port: (optional) Port for Proxy, defaults to None.
    :param proxy_username: (optional) Username for Proxy, defaults to None.
    :param proxy_password: (optional) Password for Proxy, defaults to None.
    :param max_rate_limit_retries: (optional) Maximum amount of retries
        after RateLimitError, defaults to 1.
    :param max_rate_limit_wait: (optional) Timeout (in seconds) for waiting
        for retry after RateLimitError, defaults to 60.
    :return: :class:`Client <Client>` object.
    :rtype: contentful.Client

    Usage:

        >>> import contentful
        >>> client = contentful.Client('cfexampleapi', 'b4c0n73n7fu1')
        <contentful.Client space_id="cfexampleapi"
          access_token="b4c0n73n7fu1"
          default_locale="en-US">
    """

    def __init__(
            self,
            space_id,
            access_token,
            api_url='cdn.contentful.com',
            api_version=1,
            default_locale='en-US',
            https=True,
            authorization_as_header=True,
            raw_mode=False,
            gzip_encoded=True,
            raise_errors=True,
            content_type_cache=True,
            proxy_host=None,
            proxy_port=None,
            proxy_username=None,
            proxy_password=None,
            max_rate_limit_retries=1,
            max_rate_limit_wait=60):
        self.space_id = space_id
        self.access_token = access_token
        self.api_url = api_url
        self.api_version = api_version
        self.default_locale = default_locale
        self.https = https
        self.authorization_as_header = authorization_as_header
        self.raw_mode = raw_mode
        self.gzip_encoded = gzip_encoded
        self.raise_errors = raise_errors
        self.content_type_cache = content_type_cache
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.max_rate_limit_retries = max_rate_limit_retries
        self.max_rate_limit_wait = max_rate_limit_wait

        self._validate_configuration()
        if self.content_type_cache:
            self._cache_content_types()

    def space(self, query=None):
        """Fetches the current Space.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/spaces/get-a-space

        :param query: (optional) Dict with API options.
        :return: :class:`Space <contentful.space.Space>` object.
        :rtype: contentful.space.Space

        Usage:

            >>> space = client.space()
            <Space[Contentful Example API] id='cfexampleapi'>
        """

        return self._get('', query)

    def content_type(self, content_type_id, query=None):
        """Fetches a Content Type by ID.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-types/content-type/get-a-single-content-type

        :param content_type_id: The ID of the target Content Type.
        :param query: (optional) Dict with API options.
        :return: :class:`ContentType <contentful.content_type.ContentType>` object.
        :rtype: contentful.content_type.ContentType

        Usage:
            >>> cat_content_type = client.content_type('cat')
            <ContentType[Cat] id='cat'>
        """

        return self._get(
            '/content_types/{0}'.format(content_type_id),
            query
        )

    def content_types(self, query=None):
        """Fetches all Content Types from the Space.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-types/content-model/get-the-content-model-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`ContentType <contentful.content_type.ContentType>` objects.
        :rtype: List of contentful.content_type.ContentType

        Usage:
            >>> content_types = client.content_types()
            [<ContentType[City] id='1t9IbcfdCk6m04uISSsaIK'>,
             <ContentType[Human] id='human'>,
             <ContentType[Dog] id='dog'>,
             <ContentType[Cat] id='cat'>]
        """

        return self._get(
            '/content_types',
            query
        )

    def entry(self, entry_id, query=None):
        """Fetches an Entry by ID.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/entries/entry/get-a-single-entry

        :param entry_id: The ID of the target Entry.
        :param query: (optional) Dict with API options.
        :return: :class:`Entry <contentful.entry.Entry>` object.
        :rtype: contentful.entry.Entry

        Usage:
            >>> nyancat_entry = client.entry('nyancat')
            <Entry[cat] id='nyancat'>
        """

        if query is None:
            query = {}
        self._normalize_select(query)

        try:
            query.update({'sys.id': entry_id})
            return self._get(
                '/entries',
                query
            )[0]
        except IndexError:
            raise EntryNotFoundError(
                "Entry not found for ID: '{0}'".format(entry_id)
            )

    def entries(self, query=None):
        """Fetches all Entries from the Space (up to the set limit, can be modified in `query`).

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/entries/entries-collection/get-all-entries-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`Entry <contentful.entry.Entry>` objects.
        :rtype: List of contentful.entry.Entry

        Usage:
            >>> entries = client.entries()
            [<Entry[cat] id='happycat'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='5ETMRzkl9KM4omyMwKAOki'>,
             <Entry[dog] id='6KntaYXaHSyIw8M6eo26OK'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='7qVBlCjpWE86Oseo40gAEY'>,
             <Entry[cat] id='garfield'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='4MU1s3potiUEM2G4okYOqw'>,
             <Entry[cat] id='nyancat'>,
             <Entry[1t9IbcfdCk6m04uISSsaIK] id='ge1xHyH3QOWucKWCCAgIG'>,
             <Entry[human] id='finn'>,
             <Entry[dog] id='jake'>]
        """

        if query is None:
            query = {}
        self._normalize_select(query)

        return self._get(
            '/entries',
            query
        )

    def asset(self, asset_id, query=None):
        """Fetches an Asset by ID.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/assets/asset/get-a-single-asset

        :param asset_id: The ID of the target Asset.
        :param query: (optional) Dict with API options.
        :return: :class:`Asset <Asset>` object.
        :rtype: contentful.asset.Asset

        Usage:
            >>> nyancat_asset = client.asset('nyancat')
            <Asset id='nyancat' url='//images.contentful.com/cfex...'>
        """

        return self._get(
            '/assets/{0}'.format(asset_id),
            query
        )

    def assets(self, query=None):
        """Fetches all Assets from the Space (up to the set limit, can be modified in `query`).

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/assets/assets-collection/get-all-assets-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`Asset <contentful.asset.Asset>` objects.
        :rtype: List of contentful.asset.Asset

        Usage:
            >>> assets = client.assets()
            [<Asset id='1x0xpXu4pSGS4OukSyWGUK' url='//images.content...'>,
             <Asset id='happycat' url='//images.contentful.com/cfexam...'>,
             <Asset id='nyancat' url='//images.contentful.com/cfexamp...'>,
             <Asset id='jake' url='//images.contentful.com/cfexamplea...'>]
        """

        if query is None:
            query = {}
        self._normalize_select(query)

        return self._get(
            '/assets',
            query
        )

    def sync(self, query=None):
        """Fetches content from the Sync API.

        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/synchronization/initial-synchronization/query-entries

        :param query: (optional) Dict with API options.
        :return: :class:`SyncPage <contentful.sync_page.SyncPage>` object.
        :rtype: contentful.sync_page.SyncPage

        Usage:
            >>> sync_page = client.sync({'initial': True})
            <SyncPage next_sync_token='w5ZGw6JFwqZmVcKsE8Kow4grw45QdybC...'>
        """

        if query is None:
            query = {}
        self._normalize_sync(query)

        return self._get(
            '/sync',
            query
        )

    def _normalize_select(self, query):
        """
        If the query contains the :select operator, we enforce :sys properties.
        The SDK requires sys.type to function properly, but as other of our
        SDKs require more parts of the :sys properties, we decided that every
        SDK should include the complete :sys block to provide consistency
        accross our SDKs.
        """

        if 'select' not in query:
            return

        global basestring
        if sys.version_info[0] >= 3:
            basestring = str
        if isinstance(
                query['select'],
                basestring):
            query['select'] = [s.strip() for s in query['select'].split(',')]

        query['select'] = [s for s
                           in query['select']
                           if not s.startswith('sys.')]

        if 'sys' not in query['select']:
            query['select'].append('sys')

    def _normalize_sync(self, query):
        """
        Booleans are not properly serialized for GET params,
        therefore we enforce it to a truthy value.
        """

        if 'initial' in query:
            query['initial'] = 'true'

    def _validate_configuration(self):
        """
        Validates that required parameters are present.
        """

        if not self.space_id:
            raise ConfigurationException(
                'You will need to initialize a client with a Space ID'
            )
        if not self.access_token:
            raise ConfigurationException(
                'You will need to initialize a client with an Access Token'
            )
        if not self.api_url:
            raise ConfigurationException(
                'The client configuration needs to contain an API URL'
            )
        if not self.default_locale:
            raise ConfigurationException(
                'The client configuration needs to contain a Default Locale'
            )
        if not self.api_version or self.api_version < 1:
            raise ConfigurationException(
                'The API Version must be a positive number'
            )

    def _cache_content_types(self):
        """
        Updates the Content Type Cache.
        """

        ContentTypeCache.update_cache(self)

    def _request_headers(self):
        """
        Sets the default Request Headers.
        """

        from . import __version__
        headers = {
            'User-Agent': 'PythonContentfulClient/{0}'.format(__version__),
            'Content-Type': 'application/vnd.contentful.delivery.v{0}+json'.format(  # noqa: E501
                self.api_version
            )
        }

        if self.authorization_as_header:
            headers['Authorization'] = 'Bearer {0}'.format(self.access_token)
        if self.gzip_encoded:
            headers['Accept-Encoding'] = 'gzip'

        return headers

    def _url(self, url):
        """
        Creates the Request URL.
        """

        protocol = 'https' if self.https else 'http'
        return '{0}://{1}/spaces/{2}{3}'.format(
            protocol,
            self.api_url,
            self.space_id,
            url
        )

    def _normalize_query(self, query):
        """
        Converts Arrays in the query to comma
        separaters lists for proper API handling.
        """

        for k, v in query.items():
            if isinstance(v, list):
                query[k] = ','.join(v)

    def _http_get(self, url, query):
        """
        Performs the HTTP GET Request.
        """

        if not self.authorization_as_header:
            query.update({'access_token': self.access_token})

        response = None

        self._normalize_query(query)

        kwargs = {
            'params': query,
            'headers': self._request_headers()
        }

        if self._has_proxy():
            kwargs['proxies'] = self._proxy_parameters()

        response = requests.get(
            self._url(url),
            **kwargs
        )

        if response.status_code == 429:
            raise RateLimitExceededError(response)

        return response

    def _get(self, url, query=None):
        """
        Wrapper for the HTTP Request,
        Rate Limit Backoff is handled here,
        Responses are Processed with ResourceBuilder.
        """

        if query is None:
            query = {}

        response = retry_request(self)(self._http_get)(url, query=query)

        if self.raw_mode:
            return response

        if response.status_code != 200:
            error = get_error(response)
            if self.raise_errors:
                raise error
            return error

        localized = query.get('locale', '') == '*'
        return ResourceBuilder(
            self.default_locale,
            localized,
            response.json()
        ).build()

    def _has_proxy(self):
        """
        Checks if a Proxy was set.
        """

        return self.proxy_host

    def _proxy_parameters(self):
        """
        Builds Proxy parameters Dict from
        client options.
        """

        proxy_protocol = ''
        if self.proxy_host.startswith('https'):
            proxy_protocol = 'https'
        else:
            proxy_protocol = 'http'

        proxy = '{0}://'.format(proxy_protocol)
        if self.proxy_username and self.proxy_password:
            proxy += '{0}:{1}@'.format(self.proxy_username, self.proxy_password)

        proxy += sub(r'https?(://)?', '', self.proxy_host)

        if self.proxy_port:
            proxy += ':{0}'.format(self.proxy_port)

        return {
            'http': proxy,
            'https': proxy
        }

    def __repr__(self):
        return '<contentful.Client space_id="{0}" access_token="{1}" default_locale="{2}">'.format(  # noqa: E501
            self.space_id,
            self.access_token,
            self.default_locale
        )
