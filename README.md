## Config Reader

Config parser is a nice little helper enabling you to automatically load different configuration values from various sources including .json files and the OS environment in a unified way.
It was initially created to help clean up configuration values for Django projects and make settings easily overridable but can also be used in various other use cases.

[![Build Status](https://travis-ci.org/dubsmash/config-reader.svg?branch=master)](https://travis-ci.org/dubsmash/config-reader)
[![PyPI version](https://badge.fury.io/py/config-reader.svg)](https://pypi.python.org/pypi/config-reader/)


## Requirements

* Tested for python 2.7

## Installation:

    pip install config-reader
    
## Usage:

    # Create a new config reader
    config = ConfigReader([
        'my_config_override.json',  # Easily override configurations locally
        os.environ,  # Use configurations from OS environments (e.g. on Heroku)
        'defaults.json'  # Use some default configuration values
    ])
    
    # Use the new config reader
    # Please note: These command while raise an ConfigKeyNotFoundError if the config key is not found in any of the
    # data providers used above.
    integer_value = config.get_int("MY_INT_KEY")
    float_value = config.get_float("MY_FLOAT_KEY")
    boolean_value = config.get_boolean("MY_BOOLEAN_KEY")
    string_value = config.get_string("MY_STRING_KEY")
    
    # Get an optional key by setting optional=False. The return value is then either the value from the configuration
    # or None if the value hasn't been configured.
    optional_value = config.get_int("MY_OPTIONAL_INT_KEY", optional=True)
    

## Development

Running the tests:

    
    $ python setup.py test

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


## Contributors

This project was created by Saurav Biswas, Benedikt Forchhammer and Tim Specht.
