import os

from pyflakes.test.harness import TestCase
import pytest
from config_reader import reader

from config_reader.exceptions import ConfigTypeCastError, \
    ConfigKeyNotFoundError


class TestConfigReaderFunctionality(TestCase):
    """
    Tests the various functionalities in the ConfigReader class
    """
    def setUp(self):
        """
        Creates a config object and populates it with a list of dicts,
        where each dict is either loaded from a JSON file
        or is a custom dictionary (e.g os.environ)
        """
        self.config = reader.ConfigReader([os.environ,
                                           "tests/static/test_config.json"])

    def test_get_boolean_type_variable_from_config(self):
        """
        Tests for the presence of a variable in the configs list
        which has a value of 'true'
        """
        key = "use_anonymous"
        value = self.config.get_boolean(key)
        self.assertEqual(type(value), bool)
        self.assertEqual(value, True)

    def test_gets_boolean_type_for_valid_representation(self):
        """
        Tests for the presence of a variable in the configs list
        which has a value 'T', which should represent a TRUE value.
        """
        key = "bool_setting"
        value = self.config.get_boolean(key)
        self.assertEqual(type(value), bool)
        self.assertEqual(value, True)

    def test_raises_exception_for_incorrect_type_expected(self):
        """
        Test that asserts for a ConfigTypeCastError being raised
        when trying to get a non floating point variable
        """
        with pytest.raises(ConfigTypeCastError):
            self.config.get_float("host")

    def test_variable_present_in_os(self):
        """
        Tests that a variable which is not present in the JSON file,
        but has been added to the OS env, exists
        """
        import os
        os.environ["SECRET_KEY"] = "topsecret"
        value = self.config.get_string("SECRET_KEY")
        self.assertEqual(value, "topsecret")

    def test_non_existant_variable_lookup_raises_error(self):
        """
        Tests that trying to get a non existant variable in the configs list,
        raises a ConfigKeyNotFoundError.
        """
        with pytest.raises(ConfigKeyNotFoundError):
            self.config.get_string("SOMEMONKEYVALUE")

    def test_optional_variable_returns_none(self):
        """
        Test that trying to get a non existant variable
        with optional set to False returns None
        """
        value = self.config.get_string("NON_EXISTANT", optional=True)
        self.assertEqual(value, None)

    def test_for_string_separated_by_newline(self):
        """
        Test that we can get a list of strings from a string
        present in the config,separated by newlines
        """
        value = self.config.get_string_list("list_of_strings")
        self.assertGreater(len(value), 1)

    def test_ignore_file_not_present(self):
        """
        ConfigReader expects either strings (filenames) or Mapping types.
        If the file is not present, it should ignore it
        merely and move on.
        :return:
        """
        from collections import Mapping
        filename_to_ignore = "i_do_not_exist"
        config = reader.ConfigReader([os.environ, filename_to_ignore])
        self.assertEqual(len(config.configs), 1)
        self.assertEqual(isinstance(config.configs[0], Mapping), True)
