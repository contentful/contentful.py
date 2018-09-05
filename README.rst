.. image:: ./.github/header.png
   :target: ./.github/header.png

.. raw:: html

   <p align="center">
     <a href="https://www.contentful.com/slack/">
       <img src="https://img.shields.io/badge/-Join%20Community%20Slack-2AB27B.svg?logo=slack&maxAge=31557600" alt="Join Contentful Community Slack" />
     </a>
     &nbsp;
     <a href="https://www.contentfulcommunity.com/">
       <img src="https://img.shields.io/badge/-Join%20Community%20Forum-3AB2E6.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MiA1OSI+CiAgPHBhdGggZmlsbD0iI0Y4RTQxOCIgZD0iTTE4IDQxYTE2IDE2IDAgMCAxIDAtMjMgNiA2IDAgMCAwLTktOSAyOSAyOSAwIDAgMCAwIDQxIDYgNiAwIDEgMCA5LTkiIG1hc2s9InVybCgjYikiLz4KICA8cGF0aCBmaWxsPSIjNTZBRUQyIiBkPSJNMTggMThhMTYgMTYgMCAwIDEgMjMgMCA2IDYgMCAxIDAgOS05QTI5IDI5IDAgMCAwIDkgOWE2IDYgMCAwIDAgOSA5Ii8+CiAgPHBhdGggZmlsbD0iI0UwNTM0RSIgZD0iTTQxIDQxYTE2IDE2IDAgMCAxLTIzIDAgNiA2IDAgMSAwLTkgOSAyOSAyOSAwIDAgMCA0MSAwIDYgNiAwIDAgMC05LTkiLz4KICA8cGF0aCBmaWxsPSIjMUQ3OEE0IiBkPSJNMTggMThhNiA2IDAgMSAxLTktOSA2IDYgMCAwIDEgOSA5Ii8+CiAgPHBhdGggZmlsbD0iI0JFNDMzQiIgZD0iTTE4IDUwYTYgNiAwIDEgMS05LTkgNiA2IDAgMCAxIDkgOSIvPgo8L3N2Zz4K&maxAge=31557600"
         alt="Join Contentful Community Forum" />
     </a>
   </p>

contentful.py - Contentful Python Delivery SDK
==============================================

.. raw:: html

   <p align="center">
     <img src="https://img.shields.io/badge/Status-Maintained-green.svg" alt="This repository is actively maintained" /> &nbsp;
     <a href="LICENSE.txt">
       <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg" alt="MIT License" />
     </a>
     &nbsp;
     <a href="https://travis-ci.org/contentful/contentful.py">
       <img src="https://travis-ci.org/contentful/contentful.py.svg?branch=master" alt="Build Status" />
     </a>
   </p>

**What is Contentful?**

`Contentful <https://www.contentful.com>`_ provides a content infrastructure for digital teams to power content in websites, apps, and devices. Unlike a CMS, Contentful was built to integrate with the modern software stack. It offers a central hub for structured content, powerful management and delivery APIs, and a customizable web app that enable developers and content creators to ship digital products faster.

    This SDK is intended to replace the former unofficial Python CDA SDK. The old SDK can still be found at: https://github.com/contentful-labs/contentful.py

.. raw:: html
    <details>
    <summary>Table of contents</summary>

    <!-- TOC -->

    <ul>
        <li><a href="#contentfulpy---contentful-python-delivery-sdk">contentful.py - Contentful Python Delivery SDK</a></li>
        <ul>
            <li><a href="#core-features">Core Features</a></li>
            <li><a href="#getting-started">Getting started</a></li>
            <ul>
                <li><a href="#installation">Installation</a></li>
                <li><a href="#your-first-request">Your first request</a></li>
                <li><a href="#using-this-sdk-with-the-preview-api">Using this SDK with the Preview API</a></li>
                <li><a href="#authentication">Authentication</a></li>
            </ul>
            <li><a href="#documentation--references">Documentation & References</a></li>
            <ul>
                <li><a href="#configuration">Configuration</a></li>
                <li><a href="#reference-documentation">Reference documentation</a></li>
                <ul>
                    <li><a href="#basic-queries">Basic queries</a></li>
                    <li><a href="#filtering-options">Filtering options</a></li>
                    <li><a href="#accessing-fields-and-sys-properties">Accessing fields and sys properties</a></li>
                    <li><a href="#using-different-locales">Using different locales</a></li>
                    <li><a href="#links">Links</a></li>
                    <li><a href="#assets">Assets</a></li>
                </ul>
                <li><a href="#advanced-concepts">Advanced concepts</a></li>
                <ul>
                    <li><a href="#logging">Logging</a></li>
                    <li><a href="#proxy-example">Proxy example</a></li>
                    <li><a href="#synchronization">Synchronization</a></li>
                </ul>
                <li><a href="#tutorials--other-resources">Tutorials & other resources</a></li>
            </ul>
            <li><a href="#reach-out-to-us">Reach out to us</a></li>
            <ul>
                <li><a href="#you-have-questions-about-how-to-use-this-library">You have questions about how to use this library?</a></li>
                <li><a href="#you-found-a-bug-or-want-to-propose-a-feature">You found a bug or want to propose a feature?</a></li>
                <li><a href="#you-need-to-share-confidential-information-or-have-other-questions">You need to share confidential information or have other questions?</a></li>
            </ul>
            <li><a href="#get-involved">Get involved</a></li>
            <li><a href="#license">License</a></li>
            <li><a href="#code-of-conduct">Code of Conduct</a></li>
        </ul>
    </ul>

    <!-- /TOC -->
    </details>

Core Features
-------------

- Content retrieval through `Content Delivery API <https://www.contentful.com/developers/docs/references/content-delivery-api/) and [Content Preview API](https://www.contentful.com/developers/docs/references/content-preview-api/>`_.
- `Synchronization <https://www.contentful.com/developers/docs/concepts/sync/>`_.
- `Localization support <https://www.contentful.com/developers/docs/concepts/locales/>`_.
- `Link resolution <https://www.contentful.com/developers/docs/concepts/links/>`_.
- Built in rate limiting recovery procedures.
- Supports `Environments <https://www.contentful.com/developers/docs/concepts/multiple-environments/>`_ (**since v1.7.0 - 16. April 2018**).

Getting Started
---------------

In order to get started with the Contentful Ruby SDK you'll need not only to install it, but also to get credentials which will allow you to have access to your content in Contentful.

.. raw:: html

    <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#your-first-request">Your first request</a></li>
        <li><a href="#using-this-sdk-with-the-preview-api">Using this SDK with the Preview API</a></li>
        <li><a href="#authentication">Authentication</a></li>
    </ul>

Installation
~~~~~~~~~~~~

Install Contentful from the Python Package Index::

    pip install contentful

Your first request
~~~~~~~~~~~~~~~~~~

The following code snippet is the most basic one you can use to get some content from Contentful with this SDK::

    import contentful

    client = contentful.Client(
      'cfexampleapi',  # This is the space ID. A space is like a project folder in Contentful terms
      'b4c0n73n7fu1'  # This is the access token for this space. Normally you get both ID and the token in the Contentful web app
    )

    # This API call will request an entry with the specified ID from the space defined at the top, using a space-specific access token.
    entry = client.entry('nyancat')

Using this SDK with the Preview API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This SDK can also be used with the Preview API. In order to do so, you need to use the Preview API Access token, available on the same page where you get the Delivery API token, and specify the host of the preview API, such as::

    client = contentful.Client('cfexampleapi', 'b4c0n73n7fu1', api_url='preview.contentful.com')

You can query for entries, assets, etc. very similar as described in the `Delivery API Documentation <https://www.contentful.com/developers/docs/references/content-delivery-api/>`_.
Please note, that all methods of the Python client library are ``snake_cased``, instead of JavaScript's ``camelCase``.

Authentication
~~~~~~~~~~~~~~

To get your own content from Contentful, an app should authenticate with an OAuth bearer token.

You can create API keys using the `Contentful web interface <https://app.contentful.com>`_. Go to the app, open the space that you want to access (top left corner lists all the spaces), and navigate to the APIs area. Open the API Keys section and create your first token. Done.

Don't forget to also get your Space ID.

For more information, check the [Contentful REST API reference on Authentication](https://www.contentful.com/developers/docs/references/authentication/).

Documentation & References
--------------------------

.. raw:: html

    <ul>
        <li><a href="#configuration">Configuration</a></li>
        <li><a href="#reference-documentation">Reference documentation</a></li>
        <li><a href="#tutorials--other-resources">Tutorials & other resources</a></li>
        <li><a href="#advanced-concepts">Advanced Concepts</a></li>
    </ul>

To help you get the most out of this SDK, we've prepared all available client configuration options, reference documentation, tutorials and other examples that will help you learn and understand how to use this library.

Configuration
~~~~~~~~~~~~~

The client constructor supports several options you may set to achieve the expected behavior::

    client = contentful.Client(
        SPACE_ID,
        ACCESS_TOKEN,
        # ... your options here ...
    )

.. raw:: html

    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Default</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>space_id</code></td>
          <td></td>
          <td><strong>Required</strong>. Your space ID.</td>
        </tr>
        <tr>
          <td><code>access_token</code></td>
          <td></td>
          <td><strong>Required</strong>. Your access token.</td>
        </tr>
        <tr>
          <td><code>environment</code></td>
          <td>'master'</td>
          <td>Your environment ID.</td>
        </tr>
        <tr>
          <td><code>api_url</code></td>
          <td><code>'cdn.contentful.com'</code></td>
          <td>Set the host used to build the request URIs.</td>
        </tr>
        <tr>
          <td><code>default_locale</code></td>
          <td><code>'en-US'</code></td>
          <td>Defines default locale for the client.</td>
        </tr>
        <tr>
          <td><code>secure</code></td>
          <td><code>True</code></td>
          <td>Defines whether to use HTTPS or HTTP. By default we use HTTPS.</td>
        </tr>
        <tr>
          <td><code>authorization_as_header</code></td>
          <td><code>True</code></td>
          <td>Sets the authentication mechanisms, if <code>False</code> will send authentication via query string.</td>
        </tr>
        <tr>
          <td><code>raise_errors</code></td>
          <td><code>True</code></td>
          <td>Determines whether errors are raised or returned.</td>
        </tr>
        <tr>
          <td><code>content_type_cache</code></td>
          <td><code>True</code></td>
          <td>
            Determines if content type caching is enabled automatically or not,
            allowing for accessing of fields even when they are not present on the response.
          </td>
        </tr>
        <tr>
          <td><code>raw_mode</code></td>
          <td><code>False</code></td>
          <td>If enabled, API responses are not parsed and the raw response object is returned instead.</td>
        </tr>
        <tr>
          <td><code>gzip_encoded</code></td>
          <td><code>True</code></td>
          <td>Enables gzip response content encoding.</td>
        </tr>
        <tr>
          <td><code>max_rate_limit_retries</code></td>
          <td><code>1</code></td>
          <td>
            To increase or decrease the retry attempts after a 429 Rate Limit error. Default value is 1. Using 0 will disable retry behaviour.
            Each retry will be attempted after the value (in seconds) of the <code>X-Contentful-RateLimit-Reset</code> header,
            which contains the amount of seconds until the next non rate limited request is available, has passed.
            This is blocking per execution thread.
          </td>
        </tr>
        <tr>
          <td><code>max_rate_limit_wait</code></td>
          <td><code>60</code></td>
          <td>
            Maximum time to wait for next available request (in seconds). Default value is 60 seconds.
            Keep in mind that if you hit the hourly rate limit maximum, you can have up to 60 minutes of blocked requests.
            It is set to a default of 60 seconds in order to avoid blocking processes for too long, as rate limit retry behaviour
            is blocking per execution thread.
          </td>
        </tr>
        <tr>
          <td><code>max_include_resolution_depth</code></td>
          <td><code>20</code></td>
          <td>
            Maximum amount of levels to resolve includes for SDK entities
            (this is independent of API-level includes - it represents the maximum depth the include resolution
            tree is allowed to resolved before falling back to <code>Link</code> objects).
            This include resolution strategy is in place in order to avoid having infinite circular recursion on resources with circular dependencies.
            <strong>Note</strong>: If you're using an application cache it's advisable to considerably lower this value
            (around 5 has proven to be a good compromise - but keep it higher or equal than your maximum API-level include parameter if you need the entire tree resolution).
            Note that when <code>reuse_entries</code> is enabled, the max include resolution depth only affects
            deep chains of unique objects (ie, not simple circular references).
          </td>
        </tr>
        <tr>
          <td><code>reuse_entries</code></td>
          <td><code>False</code></td>
          <td>
            When enabled, reuse hydrated Entry and Asset objects within the same request when possible.
            Can result in a large speed increase and better handles cyclical object graphs.
            This can be a good alternative to <code>max_include_resolution_depth</code> if your content model contains (or can contain) circular references.
            <strong>Caching may break if this option is enabled, as it may generate stack errors.</strong>
            When caching, deactivate this option and opt for a conservative <code>max_include_resolution_depth</code> value.
          </td>
        </tr>
        <tr>
          <td><code>proxy_host</code></td>
          <td><code>None</code></td>
          <td>To be able to perform a request behind a proxy, this needs to be set. It can be a domain or IP address of the proxy server.</td>
        </tr>
        <tr>
          <td><code>proxy_port</code></td>
          <td><code>None</code></td>
          <td>Specify the port number that is used by the proxy server for client connections.</td>
        </tr>
        <tr>
          <td><code>proxy_username</code></td>
          <td><code>None</code></td>
          <td>Username for proxy authentication.</td>
        </tr>
        <tr>
          <td><code>proxy_password</code></td>
          <td><code>None</code></td>
          <td>Password for proxy authentication.</td>
        </tr>
      </tbody>
    </table>

Reference documentation
~~~~~~~~~~~~~~~~~~~~~~~

Basic queries
.............

::

    content_types = client.content_types()
    cat_content_type = client.content_type('cat')
    nyancat = client.entry('nyancat')
    entries = client.entries()
    assets = client.assets()
    nyancat_asset = client.asset('nyancat')

Filtering options
.................

You can pass the usual filter options to the query::

    client.entries({'content_type': 'cat'}) # query for a content-type by its ID (not name)
    client.entries({'sys.id[ne]': 'nyancat'}) # query for all entries except 'nyancat'
    client.entries({'include': 1}) # include one level of linked resources
    client.entries({'content_type': 'cat', 'include': 1}) # you can also combine multiple parameters

To read more about filtering options you can check our `search parameters documentation <https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/search-parameters>`_.

The results are returned as `contentful.resource.Resource <contentful.resource.Resource>` objects. Multiple results will be returned as `list`.

Accessing fields and sys properties
...................................

::

    content_type = client.content_type('cat')
    content_type.description # "Meow."

System Properties behave the same and can be accessed via the ``#sys`` method.

::

    content_type.id # => 'cat'
    entry.type # => 'Entry'
    asset.sys # { 'id': '...', 'type': '...' }

Entry fields also have direct accessors and will be coerced to the type defined in it's content type.

::

    entry = client.entry('nyancat')
    entry.lives # 1337
    entry.fields() # { 'name': '...', 'lives': '...', ... }

Using different locales
.......................

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
.....

You can easily request a resource that is represented by a link by calling ``#resolve``::

    happycat = client.entry('happycat')
    happycat.space
    # <Link[Space] id='cfexampleapi'>
    happycat.space.resolve(client)
    # <Space[Contentful Example API] id='cfexampleapi'>

This works for any kind of Resource.

Assets
......

There is a helpful method to add image resize options for an asset image::

    client.asset('happycat').url()
    # => "//images.contentful.com/cfexampleapi/3MZPnjZTIskAIIkuuosCss/
    #     382a48dfa2cb16c47aa2c72f7b23bf09/happycatw.jpg"

    client.asset('happycat').url(w=300, h=200, fm='jpg', q=100)
    # => "//images.contentful.com/cfexampleapi/3MZPnjZTIskAIIkuuosCss/
    #     382a48dfa2cb16c47aa2c72f7b23bf09/happycatw.jpg?w=300&h=200&fm=jpg&q=100"

Entries
.......

Entries can have fields in it's default locale accessible with accessor methods::

    nyancat = client.entry('nyancat')
    nyancat.name
    # 'Nyan Cat'

Property Accessors
..................

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

Advanced Concepts
~~~~~~~~~~~~~~~~~

Logging
.......

To use the logger, use the standard library ``logging`` module::

    import logging
    logging.basicConfig(level=logging.DEBUG)

    client.entries()
    # INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): cdn.contentful.com
    # DEBUG:requests.packages.urllib3.connectionpool:"GET /spaces/cfexampleapi/entries HTTP/1.1" 200 1994

Proxy example
.............

::

    client = contentful.Client(
        'cfexampleapi',
        'b4c0n7n37fu1',
        proxy_host='127.0.0.1',
        proxy_port=8000,
        proxy_username='username',
        proxy_password='secrect_password'
    )

Synchronization
...............

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

Tutorials & other resources
---------------------------

* This library is a wrapper around our Contentful Delivery REST API. Some more specific details such as search parameters and pagination are better explained on the `REST API reference <https://www.contentful.com/developers/docs/references/content-delivery-api/>`_, and you can also get a better understanding of how the requests look under the hood.
* Check the `Contentful for Python <https://www.contentful.com/developers/docs/python/>`_ page for Tutorials, Demo Apps, and more information on other ways of using Python with Contentful

Reach out to us
---------------

You have questions about how to use this library?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

  <ul>
    <li>
      Reach out to our community forum:
      <a href="https://support.contentful.com/">
        <img alt="Contentful Community Forum" src="https://img.shields.io/badge/-Join%20Community%20Forum-3AB2E6.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MiA1OSI+CiAgPHBhdGggZmlsbD0iI0Y4RTQxOCIgZD0iTTE4IDQxYTE2IDE2IDAgMCAxIDAtMjMgNiA2IDAgMCAwLTktOSAyOSAyOSAwIDAgMCAwIDQxIDYgNiAwIDEgMCA5LTkiIG1hc2s9InVybCgjYikiLz4KICA8cGF0aCBmaWxsPSIjNTZBRUQyIiBkPSJNMTggMThhMTYgMTYgMCAwIDEgMjMgMCA2IDYgMCAxIDAgOS05QTI5IDI5IDAgMCAwIDkgOWE2IDYgMCAwIDAgOSA5Ii8+CiAgPHBhdGggZmlsbD0iI0UwNTM0RSIgZD0iTTQxIDQxYTE2IDE2IDAgMCAxLTIzIDAgNiA2IDAgMSAwLTkgOSAyOSAyOSAwIDAgMCA0MSAwIDYgNiAwIDAgMC05LTkiLz4KICA8cGF0aCBmaWxsPSIjMUQ3OEE0IiBkPSJNMTggMThhNiA2IDAgMSAxLTktOSA2IDYgMCAwIDEgOSA5Ii8+CiAgPHBhdGggZmlsbD0iI0JFNDMzQiIgZD0iTTE4IDUwYTYgNiAwIDEgMS05LTkgNiA2IDAgMCAxIDkgOSIvPgo8L3N2Zz4K&maxAge=31557600" />
      </a>
    </li>
    <li>
      Jump into our community slack channel:
      <a href="https://www.contentful.com/slack/">
        <img alt="Contentful Community Slack" src="https://img.shields.io/badge/-Join%20Community%20Slack-2AB27B.svg?logo=slack&maxAge=31557600" />
      </a>
    </li>
  </ul>

You found a bug or want to propose a feature?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

  <ul>
    <li>
      File an issue here on GitHub:
      <a href="https://github.com/contentful/contentful.rb/issues/new">
        <img alt="File an Issue" src="https://img.shields.io/badge/-Create%20Issue-6cc644.svg?logo=github&maxAge=31557600" />
      </a>.
      Make sure to remove any credential from your code before sharing it.
    </li>
  </ul>

You need to share confidential information or have other questions?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

  <ul>
    <li>
       File a support ticket at our Contentful Customer Support:
       <a href="https://www.contentful.com/support/">
         <img alt="File support ticket" src="https://img.shields.io/badge/-Submit%20Support%20Ticket-3AB2E6.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MiA1OSI+CiAgPHBhdGggZmlsbD0iI0Y4RTQxOCIgZD0iTTE4IDQxYTE2IDE2IDAgMCAxIDAtMjMgNiA2IDAgMCAwLTktOSAyOSAyOSAwIDAgMCAwIDQxIDYgNiAwIDEgMCA5LTkiIG1hc2s9InVybCgjYikiLz4KICA8cGF0aCBmaWxsPSIjNTZBRUQyIiBkPSJNMTggMThhMTYgMTYgMCAwIDEgMjMgMCA2IDYgMCAxIDAgOS05QTI5IDI5IDAgMCAwIDkgOWE2IDYgMCAwIDAgOSA5Ii8+CiAgPHBhdGggZmlsbD0iI0UwNTM0RSIgZD0iTTQxIDQxYTE2IDE2IDAgMCAxLTIzIDAgNiA2IDAgMSAwLTkgOSAyOSAyOSAwIDAgMCA0MSAwIDYgNiAwIDAgMC05LTkiLz4KICA8cGF0aCBmaWxsPSIjMUQ3OEE0IiBkPSJNMTggMThhNiA2IDAgMSAxLTktOSA2IDYgMCAwIDEgOSA5Ii8+CiAgPHBhdGggZmlsbD0iI0JFNDMzQiIgZD0iTTE4IDUwYTYgNiAwIDEgMS05LTkgNiA2IDAgMCAxIDkgOSIvPgo8L3N2Zz4K&maxAge=31557600" />
       </a>
    </li>
  </ul>

Get involved
------------

.. raw:: html

  <a href="http://makeapullrequest.com">
    <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?maxAge=31557600" />
  </a>

We appreciate any help on our repositories. For more details about how to contribute see our `CONTRIBUTING.md <./CONTRIBUTING.md>`_ document.

License
-------

Copyright (c) 2016 Contentful GmbH. See `LICENSE <./LICENSE>`_ for further details.

Code of Conduct
---------------

We want to provide a safe, inclusive, welcoming, and harassment-free space and experience for all participants, regardless of gender identity and expression, sexual orientation, disability, physical appearance, socioeconomic status, body size, ethnicity, nationality, level of experience, age, religion (or lack thereof), or other identity markers.

`Read our full Code of Conduct <https://github.com/contentful-developer-relations/community-code-of-conduct>`_
