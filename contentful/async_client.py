import asyncio
import functools
import threading

from .client import Client


"""
contentful.async_client
~~~~~~~~~~~~~~~~~~~~~~~~

Async-friendly wrapper around :class:`Client <contentful.Client>`.

Rather than reimplementing the HTTP layer with an async library, each API
method that performs a network request is exposed as a coroutine that runs
the original (blocking) call in a background thread via
:func:`asyncio.to_thread`.

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


ASYNC_METHODS = (
    'space',
    'content_type',
    'content_types',
    'entry',
    'entries',
    'asset',
    'assets',
    'locales',
    'sync',
    'taxonomy_concept',
    'taxonomy_concepts',
    'taxonomy_concept_scheme',
    'taxonomy_concept_schemes',
    'create_asset_key',
)


def _make_async(name, method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        return await asyncio.to_thread(self._invoke, name, *args, **kwargs)

    return wrapper


class AsyncClient(object):
    """Async version of :class:`Client <contentful.Client>`.

    Accepts the same arguments as :class:`Client <contentful.Client>`. Every
    method that performs a network request (``entries``, ``entry``, ``assets``,
    ``sync``, etc.) is a coroutine that can be awaited without blocking the
    event loop.

    Each awaited call occupies a thread from the default
    :mod:`asyncio` executor for the duration of the request, so throughput is
    bounded by that executor's size rather than by the event loop.

    The underlying synchronous client is available as ``sync_client``. It is
    required by helpers that take a client and call it synchronously, such as
    :meth:`Entry.incoming_references <contentful.entry.Entry.incoming_references>`,
    :meth:`Asset.incoming_references <contentful.asset.Asset.incoming_references>`
    and :meth:`SyncPage.next <contentful.sync_page.SyncPage.next>`.

    Usage:

        >>> import asyncio
        >>> from contentful import AsyncClient
        >>> client = AsyncClient('space_id', 'access_token')
        >>> entries = asyncio.run(client.entries())
    """

    def __init__(self, *args, **kwargs):
        self._pending_content_type_cache = kwargs.get('content_type_cache', True)
        self._cache_lock = threading.Lock()
        kwargs['content_type_cache'] = False
        self.sync_client = Client(*args, **kwargs)
        self.sync_client.content_type_cache = self._pending_content_type_cache

    def __getattr__(self, name):
        try:
            sync_client = self.__dict__['sync_client']
        except KeyError:
            raise AttributeError(name)
        return getattr(sync_client, name)

    def __setattr__(self, name, value):
        sync_client = self.__dict__.get('sync_client')
        if sync_client is not None and hasattr(sync_client, name):
            setattr(sync_client, name, value)
        else:
            object.__setattr__(self, name, value)

    def _invoke(self, name, *args, **kwargs):
        with self._cache_lock:
            if self._pending_content_type_cache:
                self._pending_content_type_cache = False
                self.sync_client._cache_content_types()
        return getattr(self.sync_client, name)(*args, **kwargs)

    def __repr__(self):
        return '<contentful.AsyncClient space_id="{0}" access_token="{1}" default_locale="{2}">'.format(  # noqa: E501
            self.sync_client.space_id,
            self.sync_client.access_token,
            self.sync_client.default_locale
        )


for _name in ASYNC_METHODS:
    setattr(AsyncClient, _name, _make_async(_name, getattr(Client, _name)))
