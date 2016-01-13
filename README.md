## Config Reader

Config parser is a nice little helper enabling you to automatically load different configuration values from various sources including .json files and the OS environment in a unified way.
It was initially created to help clean up configuration values for Django projects and make settings easily overridable but can also be used in various other use cases.

[![Build Status](https://travis-ci.org/dubsmash/config-parser.svg?branch=master)](https://travis-ci.org/dubsmash/config-parser)
[![Downloads](https://pypip.in/download/config-parser/badge.png)](https://pypi.python.org/pypi/config-parser/)
[![Latest Version](https://pypip.in/version/config-parser/badge.png)](https://pypi.python.org/pypi/config-parser/)


## Requirements

* Tested for python 2.7

## Installation:

    pip install config-parser

## Development

Running the tests:

    
    $ pip install -r requirements_testing.txt
    $ py.test tests --pep8 --flakes

## Developing new features

Every new feature should be:

* Documented
* Tested
* Implemented
* Pushed to main repository

### How to write documentation

When new feature implementation starts you should place it into `development version` pull. Add `Development version`
section to `Release notes` and describe every new feature in it. Use `#anchors` to facilitate navigation.

Every feature should have title and information that it was implemented in current development version.


## Publishing new releases

Increment version in `config_reader/__init__.py`. For example:

    __version__ = '0.1.1'  # from 0.1

Move to new version section all release notes in documentation.

Add date for release note section.

Run tests.

Commit changes with message "Version 0.1.1"

Add new tag version for commit:

    $ git tag 0.1.1

Push to master with tags:

    $ git push origin master --tags

Publish to pypi:

    $ python setup.py publish