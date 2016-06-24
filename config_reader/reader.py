import json
import os
from builtins import str
from collections import Mapping
from distutils import util

from config_reader.exceptions import (ConfigKeyNotFoundError,
                                      ConfigParseError,
                                      ConfigTypeCastError,
                                      ConfigTypeError)
from past.builtins import basestring  # noqa, redefined-builtin


class ConfigReader(object):
    """
    Instantiate a ConfigReader instance and load all the files by reading the filenames passed in the given list.
    Each element of filenames could be a valid filename or just a plain dictionary. We load the respective json
    files for the filenames and plainly store the dict in memory when it is just a dict.
    :param filenames: list of filenames as strings or plain dictionaries
    :return: None
    """
    def __init__(self, filenames):
        self.configs = []

        for name in filenames:
            if isinstance(name, Mapping):
                self.configs.append(name)
            elif isinstance(name, basestring):
                path = os.path.abspath(name)
                if os.path.exists(path):
                    try:
                        self.configs.append(json.loads(open(path).read()))
                    except ValueError as e:
                        raise ConfigParseError(path, e)
            else:
                msg = "ConfigReader expects list of basestring|Mapping. Got {type} instead".format(type=type(name))
                raise ValueError(msg)

    def get_int(self, key, optional=False):
        """
        Tries to fetch a variable from the config and expects it to be strictly an int
        :param key: Variable to look for
        :param optional: Whether to raise ConfigKeyNotFoundError if key was not found.
        :return: int
        """
        return self._get_typed_value(key, int, lambda x: int(x), optional)

    def get_float(self, key, optional=False):
        """
        Tries to fetch a variable from the config and expects it to be strictly a float
        :param key: Variable to look for
        :param optional: Whether to raise ConfigKeyNotFoundError if key was not found
        :return: float
        """
        return self._get_typed_value(key, float, lambda x: float(x), optional)

    def get_boolean(self, key, optional=False):
        """
        Tries to fetch a variable from the config and expects it to be a truthy value. This could be a string ("1", "Y")
        or an actual boolean. This is because we use the strtobool function in the case we find a string. The function
        strtobool expects values of the form ("1", "Y", "YES", "true", "True", "t") and so forth for truthy values. The
        variables populated from os env will always be strings, but we should make sure that we set expected boolean
        variables to either truthy/falsy strings conforming to the pattern above or actual boolean values.
        :param key: Variable to look for
        :param optional: Whether to raise ConfigKeyNotFoundError if key was not found.
        :return: bool
        """
        return self._get_typed_value(key, bool, lambda x: bool(util.strtobool(x)), optional)

    def get_string(self, key, optional=False):
        """
        Tries to fetch a variable from the config and expects it to be a string
        :param key: The variable to search for in a possible list of configs
        :param optional: Whether to raise ConfigKeyNotFoundError if key was not found.
        :return: str string
        """
        return self._get_typed_value(key, str, lambda x: str(x), optional)

    def get_string_list(self, key, optional=False):
        """
        Tries to fetch a string which could be composed of multiple lines, with each line having some sort of
        separator. Try to convert the string fetched into a list by separating on the given separator, defaulting to
        the newline character. If the string is not present we just return None.
        :param key: The variable to look for
        :param optional: Throw a ConfigKeyNotFoundError if key is not found and this was set to False
        :return: list
        """
        s = self.get_string(key, optional)

        if s is None:
            return None

        return s.splitlines()

    def _get(self, key):
        """
        Iterate over all the config dictionaries that have been loaded into the list of configs. If value is found,
        immediately return it. Otherwise, raise a ConfigKeyNotFoundError with an appropriate message.
        :param key: The variable to search for in the possible list of configs.
        :return: The corresponding value of the key if found.
        """
        for conf in self.configs:
            if key in conf:
                return conf[key]

        raise ConfigKeyNotFoundError(key)

    def _get_typed_value(self, key, target_type, type_convert, optional=False):
        """
        Returns value converted to a particular target_type and raises a ConfigTypeError if we can't cast the value to
        the expected type. Also propagates the error to the caller function 'get_<type>'. If optional was set, just
        returns None if the variable is not found.
        :param key: The variable to search for in the possible list of configs
        :param target_type: The type we expect the variable or key to be in.
        :param type_convert: A lambda expression that converts the key to the desired type.
        :param optional: If we should raise a ConfigKeyNotFoundError when the key is not found at all.
        :return: type_convert(value)
        """
        try:
            value = self._get(key)
        except ConfigKeyNotFoundError:
            if not optional:
                # Propagate the ConfigKeyNotFoundError which was caught
                raise
            return None

        if isinstance(value, basestring):
            try:
                return type_convert(value)
            except ValueError:
                raise ConfigTypeCastError(key, value, target_type)

        if isinstance(value, target_type):
            return value
        raise ConfigTypeError(key, value, target_type)
