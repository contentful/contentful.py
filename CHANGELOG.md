# CHANGELOG

## Unreleased

## v1.1.1
### Fixed
* Fix JSON Deserialization when Arrays are included in the JSON Object fields
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
