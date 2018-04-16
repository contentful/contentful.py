.. Contentful documentation master file, created by
   sphinx-quickstart on Wed Nov 30 12:51:32 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Contentful Delivery API SDK
===========================

.. image:: https://travis-ci.org/contentful/contentful.py.svg?branch=master
    :target: https://travis-ci.org/contentful/contentful.py

`Contentful <https://www.contentful.com>`_ provides a content infrastructure for digital teams to power content in websites, apps, and devices. Unlike a CMS, Contentful was built to integrate with the modern software stack. It offers a central hub for structured content, powerful management and delivery APIs, and a customizable web app that enable developers and content creators to ship digital products faster.

    This SDK is intended to replace the former unofficial Python CDA SDK. The old SDK can still be found at: https://github.com/contentful-labs/contentful.py

Installation
------------

Install Contentful from the Python Package Index::

    sudo pip install contentful

Usage
-----

Create a client::

    import contentful

    client = contentful.Client('cfexampleapi', 'b4c0n73n7fu1')

If you plan on using the `Preview API <https://www.contentful.com/developers/docs/references/content-preview-api/>`_ you need to specify the ``api_url``::

    client = contentful.Client('cfexampleapi', 'b4c0n73n7fu1', api_url='preview.contentful.com')

You can query for entries, assets, etc. very similar as described in the `Delivery API Documentation <https://www.contentful.com/developers/docs/references/content-delivery-api/>`_.
Please note, that all methods of the Python client library are ``snake_cased``, instead of JavaScript's ``camelCase``::

    client.content_types()
    client.entry('nyancat')

You can pass the usual filter options to the query::

    client.entries({'content_type': 'cat'}) # query for a content-type by its ID (not name)
    client.entries({'sys.id[ne]': 'nyancat'}) # query for all entries except 'nyancat'
    client.entries({'include': 1}) # include one level of linked resources
    client.entries({'content_type': 'cat', 'include': 1}) # you can also combine multiple parameters

The results are returned as `contentful.resource.Resource <contentful.resource.Resource>` objects. Multiple results will be returned as `list`::

    content_type = client.content_type('cat')
    content_type.description # "Meow."


System Properties behave the same and can be accessed via the ``#sys`` method::

    content_type.id # => 'cat'
    entry.type # => 'Entry'
    asset.sys # { 'id': '...', 'type': '...' }

Using different locales
-----------------------

Entries can have multiple locales, by default, the client only fetches the entry with only its default locale.
If you want to fetch a different locale you can do the following::

    entries = client.entries({'locale': 'de-DE'})

Then all the fields will be fetched for the requested locale.

Contentful Delivery API also allows to fetch all locales, you can do so by doing::

    entries = client.entries({'content_type': 'cat', 'locale': '*'})

    # assuming the entry has a field called name
    my_spanish_name = entries.first.fields('es-AR')['name']

When requesting multiple locales, the object accessor shortcuts only work for the default locale.

Links
-----

You can easily request a resource that is represented by a link by calling ``#resolve``::

    happycat = client.entry('happycat')
    happycat.space
    # <Link[Space] id='cfexampleapi'>
    happycat.space.resolve(client)
    # <Space[Contentful Example API] id='cfexampleapi'>

This works for any kind of Resource.

Assets
------

There is a helpful method to add image resize options for an asset image::

    client.asset('happycat').url()
    # => "//images.contentful.com/cfexampleapi/3MZPnjZTIskAIIkuuosCss/
    #     382a48dfa2cb16c47aa2c72f7b23bf09/happycatw.jpg"

    client.asset('happycat').url(w=300, h=200, fm='jpg', q=100)
    # => "//images.contentful.com/cfexampleapi/3MZPnjZTIskAIIkuuosCss/
    #     382a48dfa2cb16c47aa2c72f7b23bf09/happycatw.jpg?w=300&h=200&fm=jpg&q=100"

Entries
-------

Entries can have fields in it's default locale accessible with accessor methods::

    nyancat = client.entry('nyancat')
    nyancat.name
    # 'Nyan Cat'

Property Accessors
------------------

This SDK provides a simple API to interact with resources that come from the API,
by abstracting the underlying JSON structure of the objects, and exposing all the relevant fields as
object properties.

For all resources, ``sys`` properties will be available as top level properties, for example::

    space = client.space()
    space.id
    # will return the value of space.sys['id']

In the case of ``Entries`` and ``Assets``, as well as having ``sys`` available as properties,
also all the fields on present on ``fields`` will be available as properties, for example::

    entry = client.entry('nyancat')
    entry.name
    # 'Nyan Cat'
    # this is equivalent to entry.fields()['name']

    asset = client.assets()[0]
    asset.file['details']['size']
    # will return the size of the image
    # this is equivalent to asset.fields()['file']['details']['size']

Other resources, which contain top level properties other than ``sys`` or ``fields``,
have those available as object properties, for example::

    locale = client.locales()[0]
    locale.default
    # True

Client Configuration Options
----------------------------

``space_id``: Space ID of your target space.

``access_token``: API Access Token (Delivery by default, Preview if overriding api_url).

``api_url``: (optional) URL of the Contentful Target API, defaults to Delivery API (can be overriden for Preview API).

``api_version``: (optional) Target version of the Contentful API.

``default_locale``: (optional) Default Locale for your Space, defaults to 'en-US'.

``environment``: (optional) Default Environment for client, defaults to 'master'.

``https``: (optional) Boolean determining wether to use https or http, defaults to True.

``authorization_as_header``: (optional) Boolean determining wether to send access_token through a header or via GET params, defaults to True.

``raw_mode``: (optional) Boolean determining wether to process the response or return it raw after each API call, defaults to True.

``gzip_encoded``: (optional) Boolean determining wether to accept gzip encoded results, defaults to True.

``raise_errors``: (optional) Boolean determining wether to raise an exception on requests that aren't successful, defaults to True.

``content_type_cache``: (optional) Boolean determining wether to store a Cache of the Content Types in order to properly coerce Entry fields, defaults to True.

``proxy_host``: (optional) URL for Proxy, defaults to None.

``proxy_port``: (optional) Port for Proxy, defaults to None.

``proxy_username``: (optional) Username for Proxy, defaults to None.

``proxy_password``: (optional) Password for Proxy, defaults to None.

``max_rate_limit_retries``: (optional) Maximum amount of retries after RateLimitError, defaults to 1.

``max_rate_limit_wait``: (optional) Timeout (in seconds) for waiting for retry after RateLimitError, defaults to 60.

``max_include_resolution_depth``: (optional) Maximum include resolution level for Resources, defaults to 20 (max include level * 2).

``application_name``: (optional) User application name, defaults to None.

``application_version``: (optional) User application version, defaults to None.

``integration_name``: (optional) Integration name, defaults to None.

``integration_version``: (optional) Integration version, defaults to None.

Synchronization
---------------

The client also includes a wrapper for the synchronization endpoint.
You can call it either with ``initial=True`` or with a previous ``sync_token``,
additional options are described in the `API Documentation <https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/synchronization>`_::

    sync = client.sync({'initial': True}) # Returns all content currently in space
    # <SyncPage next_sync_token='w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-wo7CnDjChMKKGsK1wrzCrBzCqMOpZAwOOcOvCcOAwqHDv0XCiMKaOcOxZA8BJUzDr8K-wo1lNx7DnHE'>

    sync.items
    # [<Entry[1t9IbcfdCk6m04uISSsaIK] id='5ETMRzkl9KM4omyMwKAOki'>,
    #   <Entry[1t9IbcfdCk6m04uISSsaIK] id='7qVBlCjpWE86Oseo40gAEY'>,
    #   <Entry[1t9IbcfdCk6m04uISSsaIK] id='ge1xHyH3QOWucKWCCAgIG'>,
    #   <Entry[1t9IbcfdCk6m04uISSsaIK] id='4MU1s3potiUEM2G4okYOqw'>,
    #   <Asset id='1x0xpXu4pSGS4OukSyWGUK' url='//images.contentful.com/cfexampleapi/1x0xpXu4pSGS4OukSyWGUK/cc1239c6385428ef26f4180190532818/doge.jpg'>,
    #   <Entry[dog] id='jake'>,
    #   <Entry[cat] id='happycat'>,
    #   <Entry[dog] id='6KntaYXaHSyIw8M6eo26OK'>,
    #   <Entry[human] id='finn'>,
    #   <Entry[cat] id='nyancat'>,
    #   <Asset id='jake' url='//images.contentful.com/cfexampleapi/4hlteQAXS8iS0YCMU6QMWg/2a4d826144f014109364ccf5c891d2dd/jake.png'>,
    #   <Asset id='happycat' url='//images.contentful.com/cfexampleapi/3MZPnjZTIskAIIkuuosCss/382a48dfa2cb16c47aa2c72f7b23bf09/happycatw.jpg'>,
    #   <Asset id='nyancat' url='//images.contentful.com/cfexampleapi/4gp6taAwW4CmSgumq2ekUm/9da0cd1936871b8d72343e895a00d611/Nyan_cat_250px_frame.png'>,
    #   <Entry[cat] id='garfield'>]


    sync = client.sync({'initial': True, 'type': 'Deletion'}) # Only returns deleted entries and assets
    # <SyncPage next_sync_token='w5ZGw6JFwqZmVcKsE8Kow4grw45QdybCnV_Cg8OASMKpwo1UY8K8bsKFwqJrw7DDhcKnM2RDOVbDt1E-wo7CnDjChMKKGsK1w5zCrA3CnU7CgEvDtsK6w7B2wrRZwrwPIgDCjVo8PMOoUcK2wqTCl8O1wpY8wpjCkGM'>

    sync.items
    # [<DeletedEntry id='4rPdazIwWkuuKEAQgemSmO'>,
    #    <DeletedAsset id='5c6VY0gWg0gwaIeYkUUiqG'>,
    #    <DeletedAsset id='finn'>,
    #    <DeletedAsset id='3MZPnjZTIskAIIkuuosCss'>,
    #    <DeletedAsset id='4gp6taAwW4CmSgumq2ekUm'>,
    #    <DeletedAsset id='1uf1qqyZuEuiwmigoUYkeu'>,
    #    <DeletedAsset id='4hlteQAXS8iS0YCMU6QMWg'>,
    #    <DeletedEntry id='CVebBDcQsSsu6yKKIayy'>]

    sync = sync.next(client) # equivalent to client.sync(sync_token=sync.next_sync_token)

Logging
-------

To use the logger, use the standard library ``logging`` module::

    import logging
    logging.basicConfig(level=logging.DEBUG)

    client.entries()
    # INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): cdn.contentful.com
    # DEBUG:requests.packages.urllib3.connectionpool:"GET /spaces/cfexampleapi/entries HTTP/1.1" 200 1994

License
-------

Copyright (c) 2016 Contentful GmbH. See `LICENSE <./LICENSE>`_ for further details.

Contributing
------------

Feel free to improve this tool by submitting a Pull Request.
