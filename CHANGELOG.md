# CHANGELOG

## Unreleased
### Added
* Added support for `StructuredText` field type.

## v1.9.1
### Fixed
* Ensure all arrays sent as parameters to the API are properly serialized.

## v1.9.0
### Added
* Added support to reuse entries. This is a performance improvement, which is disabled by default due to backwards compatibility. All users are highly encouraged to enable it and test it in their applications. Inspired by @rezonant in [contentful/contentful.rb#164]((https://github.com/contentful/contentful.rb/pull/164).

## v1.8.0
### Added
* Added support of environments to `sync`.

## v1.7.0
### Added
* Added support of `environments` functionality.

## v1.6.0
### Added
* Added filtering of invalid entries from API responses.

## v1.5.0
### Added
* Added incoming links functionality.

## v1.4.3
### Fixed
* Fixed an edge case for 404 error returning a `sys` object wrapping details.

## v1.4.2
### Fixed
* Fixed edge case for 404 error returning a string as details.

## v1.4.1
### Fixed
* Fixed `sync_token` fetching [#17](https://github.com/contentful/contentful.py/pull/17)
* Fixed `unpickle` recursion error [#19](https://github.com/contentful/contentful.py/pull/19)

### Changed
* Improved error messages and handling for all API errors.

## v1.3.0
### Added
* Added `X-Contentful-User-Agent` header for more information.

## v1.2.0
### Added
* Added configuration option `max_include_resolution_depth` for controlling depth of reference resolution.

## v1.1.1
### Fixed
* Fix JSON Deserialization when Arrays are included in the JSON Object fields.
* Fix return values when value is `None` [#11](https://github.com/contentful/contentful.py/issues/11)

## v1.1.0
### Added
* Add wrapper object around array-like endpoints [#9](https://github.com/contentful/contentful.py/issues/9)

### Fixed
* Fix exception thrown on Entry not found [#8](https://github.com/contentful/contentful.py/issues/8)

## v1.0.3
### Fixed
* Fixed Unicode Decode for 2.x Python [#4](https://github.com/contentful/contentful.py/issues/4)

## v1.0.2
### Fixed
* Fixed Typo in Attribute Error [#3](https://github.com/contentful/contentful.py/issues/3)

### Removed
* Removed `contentful==1.0.0` as a dependency.


## v1.0.1
### Removed
* Removed version pinning on setup.py [#1](https://github.com/contentful/contentful.py/issues/1)

## v1.0.0

Initial release of the Official CDA SDK.

* Support for all suppoerted CDA Endpoints.
* Serrialization for all Endpoint resources.
* Recursive included resource resolution for Entries and Assets.
* Link Resolution.
* Rate Limit automatic back-off.
* Proxy support.
