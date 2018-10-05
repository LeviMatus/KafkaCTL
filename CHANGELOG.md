# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project should adhere to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Released]
### [0.0.1]

#### Updated
* [migration] Migrated KafkaCTL from off-github repository
#### Added
* [migration] added port parameter `-p` which defaults to `8081` or `2181` depending
on the toolset being used.
#### Removed
* [migration] domain specific host urls for Zookeeper and the Schema Registry.